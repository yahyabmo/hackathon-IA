"""Étage 2 : l'automate de dialogue.

Il lit les parcours YAML (``parcours/*.yaml``) : informations nécessaires,
source (profil ou question), ordre, et ce qui se passe à la fin. Déterministe,
testable, modifiable sans toucher au code.

Règle de personnalisation : on ne demande jamais ce que le profil sait déjà ;
on le confirme.

Les cas limites gérés ici :
- « je ne sais pas » : valeur par défaut annoncée (``si_inconnu``), sinon relance rassurante ;
- une réponse incomprise : la même question, précédée d'une relance ;
- « non » à une question qui l'admet (``si_non``), sinon abandon du parcours ;
- une correction après la fin (« et avec 200 000 ? ») : le conseil est recalculé.
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
NE_SAIT_PAS = ("je ne sais pas", "je sais pas", "sais pas", "aucune idee", "je ne suis pas sur",
               "pas sur", "j hesite")
REFUS = ("non", "laisse tomber", "annule", "annuler", "finalement non", "pas maintenant",
         "on arrete", "stop")


@dataclass
class Decision:
    """Ce que l'orchestrateur doit faire de ce tour."""

    type: str  # question | conseil | action | transmettre | fiche | clarifier | orienter
    #            | action_faite | action_annulee | abandon
    parcours: str | None = None
    info: str | None = None
    question: str | None = None
    outil: str | None = None
    accroche: str | None = None
    confirmations: list[str] = field(default_factory=list)
    relance: str | None = None  # "incompris" | "ne_sait_pas" quand la question est reposée
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


def _est(texte_normalise: str, expressions: tuple[str, ...]) -> bool:
    return any(contient(texte_normalise, e) for e in expressions)


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


def corriger(message: str, entites: dict[str, Any], etat: EtatConversation, spec: dict[str, Any]) -> bool:
    """Met à jour un parcours terminé avec les valeurs du message. Vrai si quelque chose a changé.

    Un seul montant va à l'information que désignent ses indices (« prix », « apport »…),
    sinon à la première information demandée au client. Plusieurs montants sont rangés
    dans l'ordre des informations demandées.
    """

    texte = normaliser(message)
    demandees = [n for n, i in spec["infos"].items() if i["type"] == "montant" and "source" not in i]
    montants = entites.get("montants", [])
    modifie = False
    if len(montants) == 1:
        cible = next((n for n, i in spec["infos"].items() if i["type"] == "montant"
                      and any(contient(texte, normaliser(m)) for m in i.get("indices", []))),
                     demandees[0] if demandees else None)
        if cible:
            etat.slots[cible], modifie = montants[0], True
    else:
        for nom, montant in zip(demandees, montants):
            etat.slots[nom], modifie = montant, True
    duree = next((n for n, i in spec["infos"].items() if i["type"] == "duree"), None)
    if duree and entites.get("duree_mois"):
        etat.slots[duree], modifie = entites["duree_mois"], True
    return modifie


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

    texte = normaliser(message)
    attendue, relance, supposition = etat.info_attendue, None, None
    if attendue:
        info = spec["infos"][attendue]
        if _est(texte, NE_SAIT_PAS):
            if "si_inconnu" in info:
                etat.slots[attendue] = info["si_inconnu"]["valeur"]
                supposition = info["si_inconnu"]["phrase"]
            else:
                relance = "ne_sait_pas"
        elif _est(texte, REFUS) and not comprehension.entites.get("montants"):
            if "si_non" in info:
                etat.slots[attendue] = info["si_non"]
            else:
                etat.parcours = etat.famille = etat.info_attendue = None
                etat.slots = {}
                return Decision("abandon")
    elif not nouveau:
        corriger(message, comprehension.entites, etat, spec)

    confirmations = _remplir(spec, message, comprehension.entites, etat, profil)
    if supposition:
        confirmations.append(supposition)
    accroche = spec.get("accroche") if nouveau else None

    for nom, info in spec["infos"].items():
        if nom not in etat.slots:
            if nom == attendue and relance is None:
                relance = "incompris"
            etat.info_attendue = nom
            return Decision(
                "question", parcours=etat.parcours, info=nom, accroche=accroche,
                confirmations=confirmations, relance=relance,
                question=info["question"].format(**_profil_affiche(profil)),
            )

    etat.info_attendue = None
    fin = spec["fin"]
    return Decision(
        fin["type"], parcours=etat.parcours, outil=fin.get("outil"), accroche=accroche,
        confirmations=confirmations, mention_legale=fin.get("mention_legale"),
        proposer=fin.get("proposer"),
    )
