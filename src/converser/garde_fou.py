"""Garde-fou sur le texte produit par le LLM.

Trois contrôles : chaque nombre du texte doit être autorisé (il vient des faits
calculés), aucune formule interdite, longueur bornée. En cas d'échec, la
réponse gabarit est affichée à la place et l'échec est compté.
"""

from __future__ import annotations

import re

from ..texte import contient, normaliser

INTERDITS = ("accorde", "garanti", "garantie", "sans risque", "promis", "je vous assure")
LONGUEUR_MAX = 1200
_NOMBRE = re.compile(r"\d{1,3}(?:[   ]\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?")


def nombres(texte: str) -> list[float]:
    """Les nombres écrits dans le texte : « 1 220 » -> 1220, « 42,1 » -> 42.1."""

    return [float(re.sub(r"[   ]", "", n).replace(",", ".")) for n in _NOMBRE.findall(texte)]


def verifier(texte: str, autorises: set[float]) -> list[str]:
    """Liste des problèmes ; vide si le texte peut être affiché."""

    problemes = [f"nombre inventé : {n:g}" for n in nombres(texte)
                 if not any(abs(n - a) < 0.051 for a in autorises)]
    texte_normalise = normaliser(texte)
    problemes += [f"formule interdite : {f}" for f in INTERDITS if contient(texte_normalise, normaliser(f))]
    if len(texte) > LONGUEUR_MAX:
        problemes.append("réponse trop longue")
    return problemes
