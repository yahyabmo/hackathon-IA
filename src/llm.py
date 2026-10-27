"""Accès aux LLM locaux, partagé par la formulation et l'escalade.

Désactivé par défaut : sans modèle installé, l'assistant répond avec ses
gabarits (c'est la configuration C des mesures). ``ASSISTANT_LLM=1`` l'active
pour la formulation ; ``ASSISTANT_ESCALADE=1`` permet en plus l'escalade.
Un tour de conversation fait au plus un appel, à la fin (formulation) ;
l'escalade est l'exception, comptée dans la trace.

Deux serveurs possibles, choisis par rôle :
- ``ollama`` (défaut) : un poste de la salle, ``OLLAMA_BASE_URL`` ;
- ``vllm`` : le serveur de DeepEirb, API compatible OpenAI, ``VLLM_BASE_URL``
  (par exemple ``http://deepeirb:8000/v1``).
``LLM_API`` fixe le serveur des deux rôles ; ``LLM_API_FORMULATION`` et
``LLM_API_ESCALADE`` le précisent (petit modèle en local, 14B sur DeepEirb).

Pour les modèles qui raisonnent (Qwen3), la réflexion est coupée : elle
consomme des tokens sans rien apporter ici.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODELE_FORMULATION = os.getenv("OLLAMA_MODEL", "ministral-3:3b")
MODELE_ESCALADE = os.getenv("OLLAMA_MODEL_ESCALADE", "ministral-3:14b")
OPTIONS = {"temperature": 0.2, "num_ctx": 4096}
MODELES_A_REFLEXION = ("qwen3", "gemma4")


def actif() -> bool:
    """Le LLM est-il activé ? Lu à chaque appel, pour que les tests puissent le changer."""

    return os.getenv("ASSISTANT_LLM", "0") == "1"


def escalade_active() -> bool:
    """L'escalade est-elle permise ? Désactivée par défaut, même si le LLM formule.

    Sans escalade, un message resté incompris après la question de
    clarification part au journal et le client se voit proposer un conseiller.
    """

    return actif() and os.getenv("ASSISTANT_ESCALADE", "0") == "1"


def serveur(role: str = "formulation") -> str:
    """``ollama`` ou ``vllm`` pour ce rôle (``formulation`` ou ``escalade``)."""

    return os.getenv(f"LLM_API_{role.upper()}", os.getenv("LLM_API", "ollama"))


def _requete(url: str, corps: dict | None = None, delai: float = 120) -> dict:
    donnees = json.dumps(corps).encode("utf-8") if corps is not None else None
    entetes = {"Content-Type": "application/json"}
    if os.getenv("VLLM_API_KEY"):
        entetes["Authorization"] = f"Bearer {os.environ['VLLM_API_KEY']}"
    requete = urllib.request.Request(url, data=donnees, headers=entetes)
    with urllib.request.urlopen(requete, timeout=delai) as reponse:
        return json.load(reponse)


def corps_ollama(modele: str, systeme: str, message: str, max_tokens: int) -> dict:
    """Requête ``/api/chat`` d'Ollama (publique pour les tests)."""

    corps = {
        "model": modele,
        "messages": [{"role": "system", "content": systeme}, {"role": "user", "content": message}],
        "stream": False,
        "keep_alive": "30m",
        "options": {**OPTIONS, "num_predict": max_tokens},
    }
    if modele.startswith(MODELES_A_REFLEXION):
        corps["think"] = False  # sinon la réflexion consomme le budget de tokens et la réponse reste vide
    return corps


def generer(modele: str, systeme: str, message: str, max_tokens: int = 200,
            role: str = "formulation") -> tuple[str, int]:
    """Un appel au modèle. Rend le texte et le nombre de tokens (entrée + sortie)."""

    if serveur(role) == "vllm":
        base = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1").rstrip("/")
        donnees = _requete(f"{base}/chat/completions", {
            "model": modele, "temperature": OPTIONS["temperature"], "max_tokens": max_tokens,
            "messages": [{"role": "system", "content": systeme}, {"role": "user", "content": message}],
        })
        return donnees["choices"][0]["message"]["content"].strip(), donnees.get("usage", {}).get("total_tokens", 0)

    donnees = _requete(f"{URL}/api/chat", corps_ollama(modele, systeme, message, max_tokens))
    tokens = donnees.get("prompt_eval_count", 0) + donnees.get("eval_count", 0)
    return donnees["message"]["content"].strip(), tokens


def joignable(role: str = "formulation", delai: float = 2.0) -> bool:
    """Le serveur répond-il vraiment ? Une configuration présente ne prouve rien."""

    url = (f"{os.getenv('VLLM_BASE_URL', 'http://localhost:8000/v1').rstrip('/')}/models"
           if serveur(role) == "vllm" else f"{URL}/api/tags")
    try:
        _requete(url, delai=delai)
        return True
    except (urllib.error.URLError, OSError, ValueError):
        return False


def prechauffer(modele: str | None = None) -> bool:
    """Charge le modèle en mémoire avant la démo, pour ne pas payer le chargement devant le jury."""

    try:
        generer(modele or MODELE_FORMULATION, "Réponds « ok ».", "ok", max_tokens=1)
        return True
    except (urllib.error.URLError, OSError, KeyError, ValueError):
        return False
