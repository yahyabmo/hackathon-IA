"""Étage 4 : les outils, sur un système bancaire simulé.

La séparation qui compte : la **déclaration** (nom, effet de bord ou non) et
l'**exécution**. La lecture est libre ; un outil à effet de bord refuse de
s'exécuter sans confirmation explicite du client, et chaque exécution laisse
une trace dans le journal.
"""

from __future__ import annotations

from datetime import datetime
from itertools import count
from typing import Any

from ..contrats import Action, EtatConversation
from . import catalogue as cat

OUTILS: dict[str, dict[str, Any]] = {
    "consulter_profil": {"effet": False, "description": "Lit le profil et l'historique du client"},
    "expliquer_frais": {"effet": False, "description": "Retrouve les frais du mois et leur cause"},
    "bloquer_carte": {"effet": True, "description": "Met la carte en opposition"},
    "preparer_virement": {"effet": True, "description": "Enregistre un virement vers un bénéficiaire connu"},
    "transmettre_conseiller": {"effet": True, "description": "Crée une demande de rappel avec un résumé"},
}

JOURNAL: list[dict[str, Any]] = []
_NUMEROS = count(1)


class ConfirmationRequise(RuntimeError):
    """Un outil à effet de bord a été appelé sans l'accord du client."""


def demande_confirmation(outil: str) -> bool:
    return OUTILS[outil]["effet"]


def _reference(prefixe: str, profil: dict[str, Any]) -> str:
    return f"{prefixe}-{profil['id']}-{next(_NUMEROS):04d}"


def _bloquer_carte(profil, parametres, etat):
    carte = profil["cartes"][0]
    carte["statut"] = "opposition"
    return {"reference": _reference("OPP", profil), "carte": carte["id"],
            "heure": datetime.now().strftime("%H h %M")}


def _expliquer_frais(profil, parametres, etat):
    frais = profil.get("historique_frais", [])
    seuil = cat.parametre("seuil_incidents_offre_fragile")
    plafond, plafond_fragile = (cat.parametre_detail("commission_intervention_max"),
                                cat.parametre_detail("commission_intervention_max_fragile"))
    return {
        "frais": frais,
        "total": sum(f["montant"] for f in frais),
        "plafond_operation": plafond["valeur"], "plafond_mois": plafond["par_mois"],
        "plafond_fragile_operation": plafond_fragile["valeur"],
        "plafond_fragile_mois": plafond_fragile["par_mois"],
        "decouverts_12_mois": profil.get("decouverts_12_mois", 0),
        "proposer_offre_fragile": profil.get("decouverts_12_mois", 0) >= seuil,
    }


def _preparer_virement(profil, parametres, etat):
    montant, lien = parametres.get("montant"), parametres.get("beneficiaire")
    beneficiaire = next((b for b in profil.get("beneficiaires", []) if b["lien"] == lien), None)
    if beneficiaire is None:
        return {"ok": False, "motif": "bénéficiaire non enregistré : il faut d'abord l'ajouter"}
    if montant is None or montant > profil["solde"]:
        return {"ok": False, "motif": "solde insuffisant pour ce montant"}
    profil["solde"] -= montant
    return {"ok": True, "reference": _reference("VIR", profil), "montant": montant,
            "beneficiaire": beneficiaire["nom"], "iban_masque": beneficiaire["iban_masque"]}


def _transmettre_conseiller(profil, parametres, etat: EtatConversation):
    demandes = [m["content"] for m in etat.historique if m["role"] == "user"][-3:]
    return {"ticket": _reference("TCK", profil),
            "resume": {"client": profil["id"], "sujet": etat.parcours, "infos": dict(etat.slots),
                       "derniers_messages": demandes}}


_EXECUTION = {
    "consulter_profil": lambda profil, parametres, etat: {"profil": profil},
    "expliquer_frais": _expliquer_frais,
    "bloquer_carte": _bloquer_carte,
    "preparer_virement": _preparer_virement,
    "transmettre_conseiller": _transmettre_conseiller,
}


def executer(action: Action, profil: dict[str, Any], etat: EtatConversation) -> Action:
    """Exécute l'action sur le SI simulé et la journalise."""

    if demande_confirmation(action.outil) and not action.confirmee:
        raise ConfirmationRequise(action.outil)
    action.resultat = _EXECUTION[action.outil](profil, action.parametres, etat)
    JOURNAL.append({"outil": action.outil, "client": profil["id"], "resultat": action.resultat})
    return action
