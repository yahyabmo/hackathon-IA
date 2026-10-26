"""Mesure de la cascade : latence par étage, appels au LLM (module de Younes).

L'énergie (CodeCarbon) se mesure par lots de requêtes dans ``eval/``, pas
requête par requête : une requête dure trop peu pour être mesurée seule.
"""

from __future__ import annotations

from collections.abc import Callable
from time import perf_counter
from typing import TypeVar

from ..contrats import Etape

T = TypeVar("T")


def mesurer(nom: str, fonction: Callable[[], T], modele: str | None = None) -> tuple[T, Etape]:
    """Exécute ``fonction`` et rend son résultat avec l'étape mesurée."""

    debut = perf_counter()
    resultat = fonction()
    latence_ms = (perf_counter() - debut) * 1000
    return resultat, Etape(nom=nom, modele=modele, latence_ms=latence_ms)


def resumer(trace: list[Etape]) -> dict[str, float]:
    """Totaux d'une trace, pour le panneau « frugalité »."""

    return {
        "latence_ms": sum(e.latence_ms for e in trace),
        "tokens": sum(e.tokens for e in trace),
        "appels_llm": sum(1 for e in trace if e.appel_llm),
    }
