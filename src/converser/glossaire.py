"""Glossaire : fiches écrites et relues par l'équipe, affichées sans LLM.

Recherche par terme exact (le plus long gagne). Prochaine étape (M2) : une
recherche par similarité de vecteurs, en mémoire avec numpy, pour les termes
mal orthographiés.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from ..texte import contient, normaliser

FICHIER = Path(__file__).resolve().parents[2] / "data" / "processed" / "glossaire.json"


@lru_cache(maxsize=1)
def _fiches() -> list[dict[str, Any]]:
    return json.loads(FICHIER.read_text(encoding="utf-8"))["fiches"]


def chercher(message: str) -> dict[str, Any] | None:
    """La fiche dont un terme apparaît dans le message, ou ``None``."""

    texte = normaliser(message)
    candidats = [
        (len(terme), fiche)
        for fiche in _fiches()
        for terme in (normaliser(t) for t in [fiche["terme"], *fiche["synonymes"]])
        if contient(texte, terme)
    ]
    return max(candidats, key=lambda c: c[0])[1] if candidats else None
