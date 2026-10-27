"""Moteur de conseil personnalisé (module de Sohayb)."""

from __future__ import annotations

from typing import Any

from ..contrats import Conseil
from .regles import REGLES
from . import catalogue

__all__ = ["conseiller"]


def conseiller(intention: str, profil: dict[str, Any], slots: dict[str, Any]) -> Conseil:
    """Conseil explicable pour un parcours dont toutes les informations sont réunies."""

    regle = REGLES.get(intention)
    conseil = regle(profil, slots) if regle else Conseil()
    if regle:
        # Ecart conserve son contrat léger ; ses références sont consultables ici.
        sources = {}
        for element in [*conseil.propositions, *conseil.ecartees]:
            pid = element.produit_id
            if pid == "credit_immobilier_30_ans":
                pid = "credit_immobilier"
            sources[element.produit_id] = catalogue.source_produit(pid)
        conseil.faits["sources_produits"] = sources
    return conseil
