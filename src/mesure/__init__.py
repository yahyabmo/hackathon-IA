"""Mesure de latence et consommation : stub initial pour le module de Younes."""

from time import perf_counter
from collections.abc import Callable
from typing import TypeVar

from ..contrats import Etape

T = TypeVar("T")


def mesurer(nom: str, fonction: Callable[[], T]) -> tuple[T, Etape]:
    """Mesure la latence locale d'une fonction sans dépendance externe."""

    debut = perf_counter()
    resultat = fonction()
    latence_ms = (perf_counter() - debut) * 1000
    return resultat, Etape(nom=nom, latence_ms=latence_ms)
