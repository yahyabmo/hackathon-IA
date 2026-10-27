"""Outils exclusivement simulés, état et journal isolés par conversation."""
from __future__ import annotations

from copy import deepcopy
from datetime import date, datetime, timezone
from decimal import Decimal
import logging
from typing import Any

from ..contrats import Action, EtatConversation
from . import catalogue as cat
from .validation import monnaie

OUTILS = {
    "consulter_profil": {"effet": False}, "expliquer_frais": {"effet": False},
    "bloquer_carte": {"effet": True}, "preparer_virement": {"effet": True},
    "transmettre_conseiller": {"effet": True},
}


class ConfirmationRequise(RuntimeError):
    """L'appelant doit demander un accord explicite avant de réessayer."""


def demande_confirmation(outil: str) -> bool:
    """Tout outil inconnu est sensible par défaut."""
    return OUTILS.get(outil, {"effet": True})["effet"]


def _ref(prefixe: str, profil: dict, action: Action) -> str:
    return f"{prefixe}-{profil['id']}-{action.identifiant[:12]}"


def _refus(motif: str) -> dict:
    return {"ok": False, "statut": "refus", "simule": True, "motif": motif}


def _bloquer_carte(profil: dict, action: Action, etat: EtatConversation) -> dict:
    cartes = profil.get("cartes", [])
    cible = action.parametres.get("carte_id")
    cartes = [c for c in cartes if c["id"] == cible] if cible else cartes
    if len(cartes) != 1:
        return _refus("précisez une carte existante et unique")
    carte = cartes[0]
    if carte["statut"] != "active":
        return _refus("carte déjà bloquée ou inactive ; aucune nouvelle opposition")
    carte["statut"] = "opposition"
    return {"reference": _ref("OPP", profil, action), "carte": carte["id"],
            "heure": datetime.now().strftime("%H h %M")}


def _expliquer_frais(profil: dict, action: Action, etat: EtatConversation) -> dict:
    periode = action.parametres.get("periode", date.today().strftime("%Y-%m"))
    date.fromisoformat(periode + "-01")
    frais = deepcopy([f for f in profil.get("historique_frais", []) if f["date"].startswith(periode + "-")])
    normal = cat.parametre_detail("commission_intervention_max")
    fragile = cat.parametre_detail("commission_intervention_max_fragile")
    return {"frais": frais, "periode": periode,
            "total": float(sum((monnaie(f["montant"]) for f in frais), Decimal(0))),
            "plafond_operation": normal["valeur"], "plafond_mois": normal["par_mois"],
            "plafond_fragile_operation": fragile["valeur"], "plafond_fragile_mois": fragile["par_mois"],
            "decouverts_12_mois": profil.get("decouverts_12_mois", 0),
            "proposer_offre_fragile": profil.get("decouverts_12_mois", 0) >= cat.parametre("seuil_incidents_offre_fragile"),
            "sources": [normal["source"], fragile["source"]],
            "limites": "Ces plafonds concernent les commissions d'intervention. Le nombre de découverts est seulement un signal interne d'orientation, pas un critère légal de fragilité."}


def _preparer_virement(profil: dict, action: Action, etat: EtatConversation) -> dict:
    montant = monnaie(action.parametres.get("montant"), positif=True)
    cible = action.parametres.get("beneficiaire")
    beneficiaires = [b for b in profil.get("beneficiaires", []) if cible in (b.get("id"), b.get("lien")) and cible]
    if len(beneficiaires) != 1:
        return _refus("bénéficiaire non enregistré ou ambigu")
    solde = monnaie(profil["solde"])
    if montant > solde:
        return _refus("solde insuffisant pour ce montant")
    b = beneficiaires[0]
    profil["solde"] = float(solde - montant)
    return {"reference": _ref("VIR", profil, action), "montant": float(montant),
            "beneficiaire": b["nom"], "iban_masque": b["iban_masque"], "solde_apres": profil["solde"]}


def _transmettre_conseiller(profil: dict, action: Action, etat: EtatConversation) -> dict:
    return {"ticket": _ref("TCK", profil, action), "resume": {
        "client": profil["id"], "sujet": etat.parcours, "infos": deepcopy(etat.slots),
        "derniers_messages": [m["content"] for m in etat.historique if m["role"] == "user"][-3:]}}


_EXECUTION = {
    "consulter_profil": lambda p, a, e: {"profil": deepcopy(p)},
    "expliquer_frais": _expliquer_frais, "bloquer_carte": _bloquer_carte,
    "preparer_virement": _preparer_virement, "transmettre_conseiller": _transmettre_conseiller,
}


def executer(action: Action, profil: dict[str, Any], etat: EtatConversation) -> Action:
    """Valide, exécute sur une copie, puis publie l'effet en mémoire.

    Le rejeu du même identifiant restitue son résultat. Un identifiant réutilisé
    avec d'autres paramètres est refusé. Pas de SI externe ni de journal global.
    """
    if etat.client_id is not None and etat.client_id != profil.get("id"):
        action.resultat = _refus("client différent de celui de la conversation")
        return action
    etat.client_id = profil.get("id")
    if demande_confirmation(action.outil) and action.confirmee is not True:
        action.resultat = {"ok": False, "statut": "en_attente", "simule": True}
        raise ConfirmationRequise(action.outil)
    empreinte = {"client": profil.get("id"), "outil": action.outil, "parametres": deepcopy(action.parametres)}
    precedent = etat.operations.get(action.identifiant)
    if precedent:
        action.resultat = (deepcopy(precedent["resultat"]) if precedent["demande"] == empreinte
                           else _refus("identifiant déjà utilisé avec une autre demande"))
        return action
    travail = deepcopy(profil)
    try:
        if action.outil not in _EXECUTION:
            resultat = _refus("outil inconnu")
        else:
            resultat = _EXECUTION[action.outil](travail, action, etat)
            resultat = {"ok": True, "statut": "succes", "simule": True, **resultat}
    except (ValueError, TypeError, KeyError, IndexError) as exc:
        resultat = _refus(f"paramètres invalides : {exc}")
    except Exception:
        # Publier uniquement une réussite complète : aucun effet partiel.
        logging.getLogger(__name__).exception("Échec de l'outil simulé %s", action.outil)
        resultat = {"ok": False, "statut": "echec", "simule": True,
                    "motif": "erreur interne ; aucune modification appliquée"}
    if resultat["ok"]:
        profil.clear()
        profil.update(travail)
    action.resultat = deepcopy(resultat)
    etat.operations[action.identifiant] = {"demande": empreinte, "resultat": deepcopy(resultat)}
    etat.journal_actions.append({"id": action.identifiant, "horodatage": datetime.now(timezone.utc).isoformat(),
        **empreinte, "confirmee": action.confirmee, "resultat": deepcopy(resultat)})
    return action
