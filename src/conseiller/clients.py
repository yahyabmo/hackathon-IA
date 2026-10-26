"""Adaptateur de la base clients : le reste du code ne voit que des profils.

Aujourd'hui : les 8 clients de démonstration (``data/processed/clients.json``).
Le jour où la version enrichie de Bank Marketing arrive, seul ce fichier change.
"""

from __future__ import annotations

import copy
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

FICHIER = Path(__file__).resolve().parents[2] / "data" / "processed" / "clients.json"


@lru_cache(maxsize=1)
def _clients() -> dict[str, dict[str, Any]]:
    donnees = json.loads(FICHIER.read_text(encoding="utf-8"))
    return {c["id"]: c for c in donnees["clients"]}


def profil(client_id: str) -> dict[str, Any]:
    """Copie du profil : les outils peuvent la modifier sans toucher à la source."""

    try:
        return copy.deepcopy(_clients()[client_id])
    except KeyError:
        raise KeyError(f"client inconnu : {client_id}") from None


def lister() -> list[tuple[str, str]]:
    """``[(id, libellé)]`` pour le sélecteur de l'interface."""

    return [(c["id"], f"{c['id']} — {c['prenom']}, {c['age']} ans") for c in _clients().values()]


def est_simule(profil_client: dict[str, Any], champ: str) -> bool:
    return champ in profil_client.get("simule", [])
