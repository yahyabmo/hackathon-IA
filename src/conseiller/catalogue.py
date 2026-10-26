"""Catalogue de produits et paramètres réglementaires, avec leur source.

Aucun taux n'est écrit dans le code : tout vient de
``data/processed/catalogue.json``, où chaque valeur porte sa source et sa date.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

FICHIER = Path(__file__).resolve().parents[2] / "data" / "processed" / "catalogue.json"


@lru_cache(maxsize=1)
def _catalogue() -> dict[str, Any]:
    return json.loads(FICHIER.read_text(encoding="utf-8"))


def produit(produit_id: str) -> dict[str, Any]:
    return _catalogue()["produits"][produit_id]


def nom(produit_id: str) -> str:
    return produit(produit_id)["nom"]


def parametre(cle: str) -> Any:
    return _catalogue()["parametres"][cle]["valeur"]


def parametre_detail(cle: str) -> dict[str, Any]:
    """Le paramètre complet : valeur, champs annexes (``par_mois``), source, date."""

    return _catalogue()["parametres"][cle]


def source_parametre(cle: str) -> str:
    return _catalogue()["parametres"][cle]["source"]


def source_produit(produit_id: str) -> str:
    return produit(produit_id).get("source", "À relever")
