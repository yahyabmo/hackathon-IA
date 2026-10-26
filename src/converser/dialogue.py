"""Étage 2 : l'automate de dialogue.

Il lit les parcours YAML (``parcours/*.yaml``) : informations nécessaires,
source (profil ou question), ordre, et ce qui se passe à la fin. Déterministe,
testable, modifiable sans toucher au code.

Règle de personnalisation : on ne demande jamais ce que le profil sait déjà ;
on le confirme.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from ..contrats import NIVEAU_REPONSE, Comprehension, EtatConversation
from ..texte import contient, euros, normaliser

DOSSIER = Path(__file__).resolve().parent / "parcours"
CHAMPS_MONETAIRES = ("revenus_nets", "epargne", "solde", "mensualites_credits")


@dataclass
class Decision:
    """Ce que l'orchestrateur doit faire de ce tour."""

    type: str  # question | conseil | action | transmettre | fiche | clarifier | orienter | action_faite | action_annulee
    parcours: str | None = None
    info: str | None = None
    question: str | None = None
    outil: str | None = None
    accroche: str | None = None
    confirmations: list[str] = field(default_factory=list)
    mention_legale: str | None = None
    proposer: str | None = None


@lru_cache(maxsize=1)
def parcours_disponibles() -> dict[str, dict[str, Any]]:
    """``{intention: spécification du parcours}``."""

    tous: dict[str, dict[str, Any]] = {}
    for fichier in sorted(DOSSIER.glob("*.yaml")):
        spec = yaml.safe_load(fichier.read_text(encoding="utf-8"))
        spec["nom"] = fichier.stem
        spec["infos"] = spec.get("infos") or {}
        for intention in spec["intentions"]:
            tous[intention] = spec
    return tous


def _profil_affiche(profil: dict[str, Any]) -> dict[str, Any]:
    return {k: euros(v) if k in CHAMPS_MONETAIRES and isinstance(v, (int, float)) else v
            for k, v in profil.items()}


def _remplir(spec, message, entites, etat, profil) -> list[str]:
    """Remplit ce qui peut l'être ; rend les phrases de confirmation des infos lues dans le profil."""

    confirmations: list[str] = []
    texte = normaliser(message)
    montants = list(entites.get("montants", []))
    ordre = list(spec["infos"])
    if etat.info_attendue in ordre:  # la réponse attendue d'abord
        i = ordre.index(etat.info_attendue)
        ordre = ordre[i:] + ordre[:i]

    for nom in ordre:
        if nom in etat.slots:
            continue
        info, valeur = spec["infos"][nom], None
        if info.get("source") and profil.get(info["source"]) is not None:
            valeur = profil[info["source"]]
            if info.get("confirmer") and valeur:
                affiche = euros(valeur) if info["type"] == "montant" else valeur
                confirmations.append(info["confirmer"].format(valeur=affiche))
        elif info["type"] == "montant" and montants:
            valeur = montants.pop(0)
        elif info["type"] == "duree":
            valeur = entites.get("duree_mois")
        elif info["type"] in ("lien", "objet"):
            valeur = entites.get(info["type"])
        elif info["type"] == "choix":
            valeur = next((option for option, mots in info["options"].items()
                           if any(contient(texte, normaliser(m)) for m in mots)), None)
        elif info["type"] == "texte" and nom == etat.info_attendue:
            valeur = message.strip()
        if valeur is None and "defaut" in info:
            valeur = info["defaut"]
        if valeur is not None:
            etat.slots[nom] = valeur
    return confirmations


def avancer(
    message: str, comprehension: Comprehension, etat: EtatConversation, profil: dict[str, Any]
) -> Decision:
    """Fait avancer le parcours d'un tour et dit quoi faire."""

    nouveau = comprehension.niveau != NIVEAU_REPONSE and comprehension.intention != etat.parcours
    if nouveau:
        etat.parcours, etat.famille = comprehension.intention, comprehension.famille
        etat.slots, etat.info_attendue = {}, None

    spec = parcours_disponibles().get(etat.parcours)
    if spec is None:  # intention de service sans parcours guidé
        etat.info_attendue = None
        return Decision("fiche", parcours=etat.parcours)

    confirmations = _remplir(spec, message, comprehension.entites, etat, profil)
    accroche = spec.get("accroche") if nouveau else None

    for nom, info in spec["infos"].items():
        if nom not in etat.slots:
            etat.info_attendue = nom
            return Decision(
                "question", parcours=etat.parcours, info=nom, accroche=accroche,
                confirmations=confirmations,
                question=info["question"].format(**_profil_affiche(profil)),
            )

    etat.info_attendue = None
    fin = spec["fin"]
    return Decision(
        fin["type"], parcours=etat.parcours, outil=fin.get("outil"), accroche=accroche,
        confirmations=confirmations, mention_legale=fin.get("mention_legale"),
        proposer=fin.get("proposer"),
    )
