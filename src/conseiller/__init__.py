"""Étages 3 et 4 : conseiller et agir (module de Sohayb)."""

from __future__ import annotations

from typing import Any

from ..contrats import Conseil
from .regles import REGLES

__all__ = ["conseiller"]


def conseiller(intention: str, profil: dict[str, Any], slots: dict[str, Any]) -> Conseil:
    """Conseil explicable pour un parcours dont toutes les informations sont réunies."""

    regle = REGLES.get(intention)
    return regle(profil, slots) if regle else Conseil()
