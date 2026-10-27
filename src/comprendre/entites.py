"""Entités extraites par règles : montants, durées, liens, objets, moments.

Aucun LLM : ce qui manque après les règles est demandé au client, pas deviné.
"""

from __future__ import annotations

import re
from typing import Any

from ..texte import contient, normaliser

# Durées et heures d'abord, pour que « 10 ans » ou « 22h » ne soient pas lus comme des montants.
_DUREE = re.compile(r"\b(\d+)\s*(ans?|annees?|années?|mois)\b", re.IGNORECASE)
_HEURE = re.compile(r"\b\d{1,2}\s*h(?:\s*\d{2})?\b", re.IGNORECASE)
_POURCENT = re.compile(r"\b\d+(?:[.,]\d+)?\s*%")
_MONTANT = re.compile(
    r"(?<![\d.,])(\d{1,3}(?:[   .]\d{3})+|\d+(?:[.,]\d+)?)\s*(k\b)?", re.IGNORECASE
)

LIENS = ("fils", "fille", "enfants", "enfant", "mere", "pere", "frere", "soeur", "conjoint",
         "femme", "mari", "compagne", "compagnon")
SYNONYMES_LIENS = {"papa": "pere", "maman": "mere", "epouse": "femme", "epoux": "mari", "copine": "compagne",
                   "copain": "compagnon", "fiston": "fils"}
OBJETS = ("voiture", "appartement", "maison", "logement", "etudes", "travaux", "moto")
MOMENTS = ("hier soir", "hier", "ce matin", "ce soir", "aujourd hui", "cette nuit")
OUI = ("oui", "ok", "d accord", "vas y", "allez y", "je confirme", "confirme", "bien sur", "yes")
NON = ("non", "annule", "annuler", "pas maintenant", "laisse tomber", "surtout pas")


def _montant(texte: str, suffixe: str | None) -> float:
    valeur = float(re.sub(r"[   .]", "", texte).replace(",", "."))
    return valeur * 1000 if suffixe else valeur


def extraire(message: str) -> dict[str, Any]:
    """Toutes les entités reconnues dans le message."""

    entites: dict[str, Any] = {}
    reste = message
    durees = _DUREE.findall(reste)
    if durees:
        nombre, unite = durees[0]
        entites["duree_mois"] = int(nombre) * (1 if unite.lower().startswith("mois") else 12)
    for motif in (_DUREE, _HEURE, _POURCENT):
        reste = motif.sub(" ", reste)
    montants = [_montant(m, k) for m, k in _MONTANT.findall(reste)]
    if montants:
        entites["montants"] = montants

    texte = normaliser(message)
    for cle, valeurs in (("lien", LIENS), ("objet", OBJETS), ("moment", MOMENTS)):
        trouve = next((v for v in valeurs if contient(texte, v)), None)
        if trouve:
            entites[cle] = trouve
    if "lien" not in entites:
        trouve = next((v for k, v in SYNONYMES_LIENS.items() if contient(texte, k)), None)
        if trouve:
            entites["lien"] = trouve
    return entites


def oui_non(message: str) -> bool | None:
    """Vrai pour un accord, faux pour un refus, ``None`` si ce n'est ni l'un ni l'autre."""

    texte = normaliser(message)
    if any(texte.startswith(n) or texte == n for n in NON):
        return False
    if any(texte.startswith(o) or texte == o for o in OUI):
        return True
    return None
