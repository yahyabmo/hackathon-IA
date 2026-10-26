"""Contrats de données partagés entre les modules du projet.

Les dataclasses de ce fichier sont volontairement simples et sérialisables.
Elles constituent l'interface commune entre compréhension, dialogue,
conseil, actions et mesure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Comprehension:
    """Résultat de l'analyse d'un message utilisateur."""

    famille: str = "inconnue"
    intention: str = "inconnue"
    confiance: float = 0.0
    alternatives: list[dict[str, Any]] = field(default_factory=list)
    entites: dict[str, Any] = field(default_factory=dict)
    insatisfaction: bool = False
    modele: str = "stub"
    exemple_proche: str | None = None


@dataclass
class Proposition:
    """Produit ou orientation proposée au client."""

    produit_id: str
    raisons: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    score: float | None = None


@dataclass
class Conseil:
    """Résultat explicable du moteur de conseil."""

    propositions: list[Proposition] = field(default_factory=list)
    ecartees: list[str] = field(default_factory=list)
    manque: list[str] = field(default_factory=list)
    alertes: list[str] = field(default_factory=list)
    faits: dict[str, Any] = field(default_factory=dict)


@dataclass
class Action:
    """Action bancaire simulée, jamais exécutée sans confirmation."""

    outil: str | None = None
    parametres: dict[str, Any] = field(default_factory=dict)
    confirmee: bool = False
    resultat: dict[str, Any] | None = None


@dataclass
class Etape:
    """Trace technique d'une étape du pipeline."""

    nom: str
    modele: str | None = None
    latence_ms: float | None = None
    tokens: int | None = None


@dataclass
class Reponse:
    """Réponse complète exposée à l'interface et aux tests."""

    texte: str
    comprehension: Comprehension = field(default_factory=Comprehension)
    conseil: Conseil = field(default_factory=Conseil)
    action: Action = field(default_factory=Action)
    escalade: bool = False
    trace: list[Etape] = field(default_factory=list)


@dataclass
class EtatConversation:
    """État minimal conservé entre deux messages."""

    intention: str | None = None
    slots: dict[str, Any] = field(default_factory=dict)
    derniere_reponse: str | None = None
    historique: list[dict[str, str]] = field(default_factory=list)
    action_en_attente: Action | None = None
