"""Garde-fou sur le texte produit par le LLM.

Quatre contrôles : aucun nombre inventé (chaque nombre vient des faits), aucun
nombre oublié (la reformulation garde tous ceux du gabarit), aucune formule
interdite, et une longueur plausible (ni tronquée, ni bavarde). En cas d'échec,
la réponse gabarit est affichée à la place et l'échec est compté.

Le contrôle des oublis vient d'un test réel : un modèle de 270 M paramètres a
répondu « Oui, je suis prêt à reformuler le message », sans aucun chiffre ni
conseil — un texte qui passait le seul contrôle des nombres inventés.
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


def _present(n: float, valeurs) -> bool:
    return any(abs(n - v) < 0.051 for v in valeurs)


def verifier(texte: str, autorises: set[float], obligatoires: set[float] | None = None,
             longueur_min: int = 0) -> list[str]:
    """Liste des problèmes ; vide si le texte peut être affiché."""

    trouves = nombres(texte)
    problemes = [f"nombre inventé : {n:g}" for n in trouves if not _present(n, autorises)]
    problemes += [f"nombre oublié : {n:g}" for n in sorted(obligatoires or ()) if not _present(n, trouves)]
    texte_normalise = normaliser(texte)
    problemes += [f"formule interdite : {f}" for f in INTERDITS if contient(texte_normalise, normaliser(f))]
    if len(texte) > LONGUEUR_MAX:
        problemes.append("réponse trop longue")
    if len(texte) < longueur_min:
        problemes.append("réponse tronquée")
    return problemes
