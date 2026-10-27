"""Glossaire : fiches écrites et relues par l'équipe, affichées sans LLM.

Recherche par terme exact d'abord (le plus long gagne). Pour une question de
définition, une recherche approchante rattrape les fautes de frappe (« TEAG »,
« decouver autorisé ») : similarité de chaînes de la bibliothèque standard
(``difflib``), sur des fenêtres de mots de la longueur du terme. Pas de modèle :
le glossaire compte une vingtaine de fiches.
"""

from __future__ import annotations

import json
from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path
from typing import Any

from ..texte import contient, normaliser

FICHIER = Path(__file__).resolve().parents[2] / "data" / "processed" / "glossaire.json"
SEUIL_APPROCHANT = 0.75
LONGUEUR_MIN_APPROCHANT = 4  # « lep » ou « pel » : trop courts pour une recherche approchante


@lru_cache(maxsize=1)
def _fiches() -> list[dict[str, Any]]:
    return json.loads(FICHIER.read_text(encoding="utf-8"))["fiches"]


def _termes(fiche: dict[str, Any]) -> list[str]:
    return [normaliser(t) for t in [fiche["terme"], *fiche["synonymes"]]]


def _approchante(texte: str) -> dict[str, Any] | None:
    mots = texte.split()
    meilleur, fiche_retenue = 0.0, None
    for fiche in _fiches():
        for terme in _termes(fiche):
            if len(terme) < LONGUEUR_MIN_APPROCHANT:
                continue
            n = len(terme.split())
            for i in range(len(mots) - n + 1):
                score = SequenceMatcher(None, " ".join(mots[i:i + n]), terme).ratio()
                if score > meilleur:
                    meilleur, fiche_retenue = score, fiche
    return fiche_retenue if meilleur >= SEUIL_APPROCHANT else None


def chercher(message: str, approchant: bool = False) -> dict[str, Any] | None:
    """La fiche dont un terme apparaît dans le message, ou ``None``.

    ``approchant`` tolère les fautes de frappe : à réserver aux questions de
    définition, où l'on sait que le client cherche un terme.
    """

    texte = normaliser(message)
    candidats = [(len(terme), fiche) for fiche in _fiches() for terme in _termes(fiche)
                 if contient(texte, terme)]
    if candidats:
        return max(candidats, key=lambda c: c[0])[1]
    return _approchante(texte) if approchant else None
