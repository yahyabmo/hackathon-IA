"""Validation commune : nombres finis et montants exacts."""
from decimal import Decimal, InvalidOperation
import math
from typing import Any


def nombre(valeur: Any, *, minimum: float = 0, maximum: float = 1e12,
           strict: bool = False, entier: bool = False) -> float:
    if isinstance(valeur, bool) or not isinstance(valeur, (int, float, Decimal)):
        raise ValueError("nombre requis")
    try:
        n = float(valeur)
    except (OverflowError, ValueError):
        raise ValueError("nombre hors limites") from None
    if not math.isfinite(n) or n > maximum or n < minimum or (strict and n == minimum):
        raise ValueError("nombre hors limites")
    if entier and not n.is_integer():
        raise ValueError("entier requis")
    return n


def monnaie(valeur: Any, *, positif: bool = False) -> Decimal:
    """Deux décimales maximum ; aucun arrondi implicite d'un ordre."""
    nombre(valeur, minimum=0 if positif else -1e12, strict=positif)
    try:
        d = Decimal(str(valeur))
        if d != d.quantize(Decimal("0.01")):
            raise ValueError("deux décimales maximum")
        return d.quantize(Decimal("0.01"))
    except InvalidOperation:
        raise ValueError("montant invalide") from None
