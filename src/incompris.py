"""Journal des messages non compris : la boucle d'amélioration (responsable : M2).

Chaque message que ni les mots-clés ni le classifieur n'ont compris est ajouté
à un fichier JSONL, avec la suite donnée (question de clarification ou rappel
proposé). On le relit pour enrichir le lexique et les phrases d'entraînement,
plutôt que d'appeler un gros modèle à chaque doute.

Lire le journal : ``python -m src.incompris``
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from .contrats import Comprehension

FICHIER_DEFAUT = Path(__file__).resolve().parents[1] / "eval" / "incompris.jsonl"


def fichier() -> Path:
    """Chemin du journal ; ``INCOMPRIS_FICHIER`` le remplace (les tests l'utilisent)."""

    return Path(os.getenv("INCOMPRIS_FICHIER", str(FICHIER_DEFAUT)))


def noter(message: str, client_id: str, suite: str, comprehension: Comprehension) -> None:
    """Ajoute une ligne au journal."""

    ligne = {
        "horodatage": datetime.now().isoformat(timespec="seconds"),
        "client": client_id,
        "message": message,
        "suite": suite,
        "alternatives": [asdict(a) for a in comprehension.alternatives],
    }
    chemin = fichier()
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")


def lire() -> list[dict[str, Any]]:
    chemin = fichier()
    if not chemin.exists():
        return []
    return [json.loads(l) for l in chemin.read_text(encoding="utf-8").splitlines() if l.strip()]


if __name__ == "__main__":
    lignes = lire()
    print(f"{len(lignes)} messages non compris dans {fichier()}")
    for ligne in lignes[-20:]:
        print(f"  [{ligne['suite']:9}] {ligne['client']}  {ligne['message']}")
