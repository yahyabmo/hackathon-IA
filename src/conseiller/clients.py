"""Adaptateur de la base clients : le reste du code ne voit que des profils.

Aujourd'hui : les 8 clients de démonstration (``data/processed/clients.json``).
Le jour où la version enrichie de Bank Marketing arrive, seul ce fichier change.
"""

from __future__ import annotations

import copy
import json
from functools import lru_cache
from pathlib import Path
from typing import Any
from datetime import date
import re

from .validation import nombre

FICHIER = Path(__file__).resolve().parents[2] / "data" / "processed" / "clients.json"


@lru_cache(maxsize=1)
def _clients() -> dict[str, dict[str, Any]]:
    donnees = json.loads(FICHIER.read_text(encoding="utf-8"))
    vus = set()
    for client in donnees["clients"]:
        valider_profil(client)
        if client["id"] in vus:
            raise ValueError("identifiant client dupliqué")
        vus.add(client["id"])
    return {c["id"]: c for c in donnees["clients"]}


def valider_profil(client: dict[str, Any]) -> None:
    """Refuse une source incohérente ; None signifie inconnu pour les finances."""
    requis = ("id", "prenom", "age", "metier", "situation", "revenus_nets", "epargne",
              "solde", "mensualites_credits", "enfants", "livrets", "cartes",
              "beneficiaires", "historique_frais", "simule", "provenance")
    if not isinstance(client, dict) or any(k not in client for k in requis):
        raise ValueError("profil incomplet")
    if not isinstance(client["id"], str) or not re.fullmatch(r"C\d{2}", client["id"]):
        raise ValueError("identifiant client invalide")
    nombre(client["age"], maximum=120, entier=True)
    for k in ("prenom", "metier", "situation"):
        if not isinstance(client[k], str) or not client[k].strip():
            raise ValueError(f"{k} invalide")
    for k in ("revenus_nets", "epargne", "mensualites_credits", "solde"):
        if client[k] is not None:
            nombre(client[k], minimum=-1e12 if k == "solde" else 0)
    for k in ("enfants", "cartes", "beneficiaires", "historique_frais", "simule"):
        if not isinstance(client[k], list):
            raise ValueError(f"{k} doit être une liste")
    for age in client["enfants"]:
        nombre(age, maximum=client["age"], entier=True)
    if not isinstance(client["livrets"], dict):
        raise ValueError("livrets invalides")
    for solde in client["livrets"].values():
        nombre(solde)
    if client["epargne"] is not None and sum(client["livrets"].values()) > client["epargne"]:
        raise ValueError("livrets supérieurs à l'épargne déclarée")
    ids = set()
    for carte in client["cartes"]:
        if not isinstance(carte, dict) or not isinstance(carte.get("id"), str) or not carte["id"] or carte.get("statut") not in ("active", "opposition", "inactive"):
            raise ValueError("carte invalide")
        if carte["id"] in ids:
            raise ValueError("carte dupliquée")
        ids.add(carte["id"])
    for b in client["beneficiaires"]:
        if not isinstance(b, dict) or any(not isinstance(b.get(k), str) or not b[k] for k in ("nom", "lien", "iban_masque")):
            raise ValueError("bénéficiaire invalide")
    for f in client["historique_frais"]:
        if not isinstance(f, dict) or not isinstance(f.get("date"), str) or "montant" not in f:
            raise ValueError("frais invalides")
        date.fromisoformat(f["date"])
        nombre(f["montant"])
        if not f.get("libelle") or not f.get("cause"):
            raise ValueError("frais incomplets")
    for k in ("contacts_aujourdhui", "decouverts_12_mois"):
        nombre(client.get(k, 0), entier=True)
    for k in ("residence_france", "domicile_fiscal_france", "rattache_foyer_parents", "est_etudiant", "peu_a_laise_en_ligne"):
        if client.get(k) is not None and type(client[k]) is not bool:
            raise ValueError(f"{k} doit être booléen ou inconnu")
    for k in ("rfr", "parts_fiscales", "annee_rfr"):
        if client.get(k) is not None:
            nombre(client[k], strict=k != "rfr", entier=k == "annee_rfr")
    if not isinstance(client["provenance"], dict):
        raise ValueError("provenance absente")
    for k in client:
        if k in ("simule", "provenance", "ancrage_bank_marketing"):
            continue
        p = client["provenance"].get(k, {})
        if not isinstance(p, dict) or p.get("nature") not in ("simulation", "scenario_cgi", "bank_marketing") or not p.get("source"):
            raise ValueError(f"provenance manquante : {k}")
        if (p["nature"] == "simulation") != (k in client["simule"]):
            raise ValueError(f"marquage simulation incohérent : {k}")


def profil(client_id: str) -> dict[str, Any]:
    """Copie du profil : le chatbot peut personnaliser ses conseils sans modifier la source."""

    try:
        return copy.deepcopy(_clients()[client_id])
    except KeyError:
        raise KeyError(f"client inconnu : {client_id}") from None


def lister() -> list[tuple[str, str]]:
    """``[(id, libellé)]`` pour le sélecteur de l'interface."""

    return [(c["id"], f"{c['id']} — {c['prenom']}, {c['age']} ans") for c in _clients().values()]


def est_simule(profil_client: dict[str, Any], champ: str) -> bool:
    return champ in profil_client.get("simule", [])
