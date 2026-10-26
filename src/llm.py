"""Accès au LLM local (Ollama), partagé par la formulation et l'escalade.

Désactivé par défaut : sans modèle installé, l'assistant répond avec ses
gabarits (c'est la configuration C des mesures). ``ASSISTANT_LLM=1`` l'active.
Un tour de conversation fait au plus un appel, à la fin (formulation) ;
l'escalade est l'exception, comptée dans la trace.

Pour un modèle qui raisonne (Qwen3), ajouter ``"think": false`` à la requête :
la réflexion consomme des tokens sans rien apporter ici.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODELE_FORMULATION = os.getenv("OLLAMA_MODEL", "ministral-3:3b")
MODELE_ESCALADE = os.getenv("OLLAMA_MODEL_ESCALADE", "ministral-3:14b")


def actif() -> bool:
    """Le LLM est-il activé ? Lu à chaque appel, pour que les tests puissent le changer."""

    return os.getenv("ASSISTANT_LLM", "0") == "1"


def joignable(delai: float = 2.0) -> bool:
    """Ollama répond-il vraiment ? Une configuration présente ne prouve rien."""

    try:
        with urllib.request.urlopen(f"{URL}/api/tags", timeout=delai):
            return True
    except (urllib.error.URLError, OSError):
        return False


def generer(modele: str, systeme: str, message: str, max_tokens: int = 200) -> tuple[str, int]:
    """Un appel au modèle. Rend le texte et le nombre de tokens (entrée + sortie)."""

    corps = {
        "model": modele,
        "messages": [
            {"role": "system", "content": systeme},
            {"role": "user", "content": message},
        ],
        "stream": False,
        "keep_alive": "30m",
        "options": {"temperature": 0.2, "num_ctx": 4096, "num_predict": max_tokens},
    }
    requete = urllib.request.Request(
        f"{URL}/api/chat",
        data=json.dumps(corps).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(requete, timeout=120) as reponse:
        donnees = json.load(reponse)
    tokens = donnees.get("prompt_eval_count", 0) + donnees.get("eval_count", 0)
    return donnees["message"]["content"].strip(), tokens
