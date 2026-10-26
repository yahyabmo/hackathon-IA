"""Outils de texte partagés : normalisation et format des nombres en français."""

from __future__ import annotations

import re
import unicodedata

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def normaliser(texte: str) -> str:
    """Minuscules, sans accents, ponctuation remplacée par des espaces.

    « On m'a VOLÉ ma CB ! » devient « on m a vole ma cb ».
    """

    sans_accents = unicodedata.normalize("NFD", texte.lower())
    sans_accents = "".join(c for c in sans_accents if unicodedata.category(c) != "Mn")
    return _NON_ALNUM.sub(" ", sans_accents).strip()


def contient(texte_normalise: str, expression: str) -> bool:
    """L'expression (déjà normalisée) apparaît-elle en mots entiers ?"""

    return f" {expression} " in f" {texte_normalise} "


def euros(montant: float) -> str:
    """1220.4 -> « 1 220 € »."""

    return f"{round(montant):,}".replace(",", " ") + " €"


def pourcent(ratio: float) -> str:
    """0.4207 -> « 42,1 % » ; 0.35 -> « 35 % »."""

    valeur = f"{ratio * 100:.1f}".removesuffix(".0")
    return valeur.replace(".", ",") + " %"
