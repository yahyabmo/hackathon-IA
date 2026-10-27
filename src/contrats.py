"""Contrats de données partagés entre les modules du projet.

Les dataclasses de ce fichier sont volontairement simples et sérialisables.
Elles constituent l'interface commune entre les étages de la cascade :
comprendre (M1), converser, conseiller et formuler, mesurer
(M1). Les noms de champs sont en français et sans accents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .taxonomie import INCONNUE

# Niveau de la cascade qui a compris la demande. Le panneau « frugalité » et
# les mesures comptent les demandes par niveau.
NIVEAU_REPONSE = "reponse_attendue"  # réponse à la question posée au tour précédent
NIVEAU_MOTS_CLES = "mots_cles"
NIVEAU_CLASSIFIEUR = "classifieur"
NIVEAU_ESCALADE = "escalade"  # le LLM d'escalade a été appelé
NIVEAU_INTERPRETE = "interprete"  # le petit LLM du niveau 1 a lu le message
NIVEAU_FILE = "file"  # demande mise en file par un message précédent
NIVEAU_AUCUN = "aucun"


@dataclass
class Alternative:
    """Famille candidate, proposée au client quand la confiance est trop basse."""

    famille: str
    confiance: float


@dataclass
class Comprehension:
    """Résultat de l'étage 1 pour un message du client."""

    famille: str = INCONNUE
    intention: str = INCONNUE
    confiance: float = 0.0
    niveau: str = NIVEAU_AUCUN
    modele: str | None = None
    alternatives: list[Alternative] = field(default_factory=list)
    entites: dict[str, Any] = field(default_factory=dict)
    insatisfaction: bool = False
    exemple_proche: str | None = None
    autres_intentions: list[str] = field(default_factory=list)  # autres demandes du même message

    @property
    def comprise(self) -> bool:
        return self.intention != INCONNUE


@dataclass
class Proposition:
    """Produit ou orientation proposée au client, avec ses raisons."""

    produit_id: str
    raisons: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    score: float | None = None


@dataclass
class Ecart:
    """Produit écarté, et la règle qui l'écarte : le « pourquoi pas »."""

    produit_id: str
    raison: str
    regle: str | None = None


@dataclass
class Conseil:
    """Résultat explicable du moteur de conseil (étage 3)."""

    propositions: list[Proposition] = field(default_factory=list)
    ecartees: list[Ecart] = field(default_factory=list)
    manque: list[str] = field(default_factory=list)  # informations à demander au client
    alertes: list[str] = field(default_factory=list)  # prudence, affichées au client
    faits: dict[str, Any] = field(default_factory=dict)  # les seuls nombres citables


@dataclass
class Etape:
    """Une ligne du panneau « frugalité »."""

    nom: str
    modele: str | None = None
    latence_ms: float = 0.0
    tokens: int = 0
    appel_llm: bool = False


@dataclass
class Reponse:
    """Réponse complète exposée à l'interface et aux tests."""

    texte: str
    comprehension: Comprehension = field(default_factory=Comprehension)
    conseil: Conseil | None = None
    question: str | None = None  # information demandée au client, s'il y en a une
    escalade: bool = False  # vrai seulement si le LLM d'escalade a été appelé
    trace: list[Etape] = field(default_factory=list)
    niveau: int = 0  # niveau choisi par l'aiguilleur : 0 règles, 1 petit LLM interprète, 2 RAG
    raison_niveau: str = ""
    sources: list[dict[str, Any]] = field(default_factory=list)  # passages du RAG cités

    @property
    def appels_llm(self) -> int:
        return sum(1 for etape in self.trace if etape.appel_llm)


@dataclass
class EtatConversation:
    """État conservé entre deux messages.

    ``parcours`` et ``info_attendue`` sont ce qui permet de lire « 250 000 »
    comme la réponse à la question posée, et non comme une nouvelle demande.
    """

    parcours: str | None = None  # intention du parcours en cours
    famille: str | None = None
    info_attendue: str | None = None  # information demandée au tour précédent
    slots: dict[str, Any] = field(default_factory=dict)  # informations recueillies
    clarification_demandee: bool = False
    mots_simples: bool = False  # demandé par le client ; automatique dès 70 ans ou « peu à l'aise »
    historique: list[dict[str, str]] = field(default_factory=list)
    derniere_reponse: str | None = None
    client_id: str | None = None
    profil_simule: dict[str, Any] | None = None
    question_m3: str | None = None
    # Aiguilleur : la mémoire est commune aux niveaux, qui peuvent changer à chaque message.
    file_demandes: list[str] = field(default_factory=list)  # demandes à traiter ensuite, par urgence
    memoire: dict[str, dict[str, Any]] = field(default_factory=dict)  # parcours interrompus : infos déjà données
    niveaux: list[int] = field(default_factory=list)  # chaîne des niveaux de la conversation
    explication: list[str] = field(default_factory=list)  # dernier conseil, pour un « pourquoi ? »
    traites: list[str] = field(default_factory=list)  # demandes déjà traitées dans la conversation
    llm_actif: bool | None = None  # choix de l'interface ; None : ASSISTANT_LLM
    niveau_force: int | None = None  # démonstration : forcer un niveau
