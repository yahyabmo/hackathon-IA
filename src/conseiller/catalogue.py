"""Catalogue de produits et paramètres réglementaires, avec leur source.

Aucun taux n'est écrit dans le code : tout vient de
``data/processed/catalogue.json``, où chaque valeur porte sa source et sa date.
"""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Any
from .validation import nombre

FICHIER = Path(__file__).resolve().parents[2] / "data" / "processed" / "catalogue.json"


@lru_cache(maxsize=1)
def _catalogue() -> dict[str, Any]:
    donnees = json.loads(FICHIER.read_text(encoding="utf-8"))
    valider_catalogue(donnees)
    return donnees


def valider_catalogue(donnees: dict[str, Any]) -> None:
    """Valide aussi les métadonnées, sans confondre vérifié et applicable partout."""
    if not isinstance(donnees, dict):
        raise ValueError("catalogue invalide")
    for groupe in ("produits", "parametres"):
        if not isinstance(donnees.get(groupe), dict) or not donnees[groupe]:
            raise ValueError(f"{groupe} absent")
        for cle, fiche in donnees[groupe].items():
            if not isinstance(fiche, dict):
                raise ValueError(f"fiche invalide : {cle}")
            if not fiche.get("source") or fiche["source"] == "À relever":
                raise ValueError(f"source absente : {cle}")
            if not isinstance(fiche.get("releve_le"), str):
                raise ValueError(f"date absente : {cle}")
            date.fromisoformat(fiche["releve_le"])
            if fiche.get("nature") not in ("reglementaire", "condition_commerciale", "hypothese_simulation",
                                          "reference_statistique", "heuristique_interne", "simulation"):
                raise ValueError(f"nature inconnue : {cle}")
            if fiche.get("statut") not in ("verifie", "partiel", "non_verifie"):
                raise ValueError(f"statut absent : {cle}")
            if groupe == "produits":
                if not fiche.get("nom") or not fiche.get("conditions") or not fiche.get("categorie"):
                    raise ValueError(f"produit incomplet : {cle}")
                for champ in ("plafond", "age_min", "age_max", "montant_min", "solde_min",
                              "versement_initial_min", "versement_annuel_min", "horizon_min_mois",
                              "duree_min_mois", "duree_max_mois"):
                    if champ in fiche:
                        nombre(fiche[champ], entier="age" in champ or "mois" in champ)
                if "plafond" in fiche and fiche.get("unite_plafond") != "EUR":
                    raise ValueError("unité du plafond absente")
                if fiche.get("age_max", 120) < fiche.get("age_min", 0):
                    raise ValueError("âges incohérents")
                if fiche.get("duree_max_mois", 1200) < fiche.get("duree_min_mois", 0):
                    raise ValueError("durées incohérentes")
            else:
                if not fiche.get("unite") or "valeur" not in fiche:
                    raise ValueError(f"paramètre incomplet : {cle}")
                if fiche["valeur"] is not None:
                    nombre(fiche["valeur"], maximum=1 if fiche["unite"] == "ratio" else 1e12)
                elif fiche["statut"] == "verifie":
                    raise ValueError("valeur vérifiée absente")


def produit(produit_id: str) -> dict[str, Any]:
    return deepcopy(_catalogue()["produits"][produit_id])


def nom(produit_id: str) -> str:
    return produit(produit_id)["nom"]


def parametre(cle: str) -> Any:
    return deepcopy(_catalogue()["parametres"][cle]["valeur"])


def parametre_detail(cle: str) -> dict[str, Any]:
    """Le paramètre complet : valeur, champs annexes (``par_mois``), source, date."""

    return deepcopy(_catalogue()["parametres"][cle])


def source_parametre(cle: str) -> str:
    return _catalogue()["parametres"][cle]["source"]


def source_produit(produit_id: str) -> str:
    return produit(produit_id).get("source", "À relever")
