"""Second niveau de l'étage 1 : encodeur multilingue + régression logistique.

``intfloat/multilingual-e5-small`` (préfixe ``query:``) transforme le message
en vecteur ; deux têtes de régression logistique, entraînées sur Banking77 en
anglais sans traduction et sur nos phrases (``python -m src.comprendre.entrainer``),
donnent la famille puis l'intention dans cette famille. La confiance est la
probabilité de la famille ; sous ``SEUIL_TAU``, l'orchestrateur pose une
question de clarification avec les deux familles les plus probables.

À l'exécution, les têtes sont deux produits matrice-vecteur (numpy) : ni
scikit-learn ni pickle. Sans les têtes, sans ``sentence-transformers`` ou avec
``ASSISTANT_CLASSIFIEUR=0``, le classifieur ne prédit rien et la cascade passe
directement à la clarification.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from ..contrats import NIVEAU_CLASSIFIEUR, Alternative, Comprehension
from ..taxonomie import famille_de

ENCODEUR = "intfloat/multilingual-e5-small"
PREFIXE = "query: "
MODELE = "e5-small+lr"
RACINE = Path(__file__).resolve().parents[2]
TETES = RACINE / "data" / "processed" / "classifieur.npz"
META = RACINE / "data" / "processed" / "classifieur.json"
EXEMPLES = RACINE / "models" / "exemples.npz"
SEUIL_PAR_DEFAUT = 0.6


def _lire_tau() -> float:
    try:
        return float(json.loads(META.read_text(encoding="utf-8"))["tau"])
    except (OSError, KeyError, ValueError):
        return SEUIL_PAR_DEFAUT


SEUIL_TAU = _lire_tau()  # fixé par balayage à l'entraînement (97 % de routages corrects)


def _softmax(scores: np.ndarray) -> np.ndarray:
    exp = np.exp(scores - scores.max())
    return exp / exp.sum()


class Tetes:
    """Les deux régressions logistiques : poids, biais et noms des classes."""

    def __init__(self, familles: np.ndarray, coef_famille: np.ndarray, biais_famille: np.ndarray,
                 intentions: np.ndarray, coef_intention: np.ndarray, biais_intention: np.ndarray):
        self.familles, self.coef_famille, self.biais_famille = familles, coef_famille, biais_famille
        self.intentions, self.coef_intention, self.biais_intention = intentions, coef_intention, biais_intention
        self._famille_des_intentions = np.array([famille_de(str(i)) for i in intentions])

    @classmethod
    def depuis_sklearn(cls, tete_famille: Any, tete_intention: Any) -> Tetes:
        return cls(tete_famille.classes_, tete_famille.coef_.astype(np.float32),
                   tete_famille.intercept_.astype(np.float32), tete_intention.classes_,
                   tete_intention.coef_.astype(np.float32), tete_intention.intercept_.astype(np.float32))

    @classmethod
    def charger(cls, chemin: Path) -> Tetes:
        with np.load(chemin) as d:
            return cls(d["familles"], d["coef_famille"], d["biais_famille"],
                       d["intentions"], d["coef_intention"], d["biais_intention"])

    def enregistrer(self, chemin: Path) -> None:
        np.savez_compressed(chemin, familles=self.familles, coef_famille=self.coef_famille,
                            biais_famille=self.biais_famille, intentions=self.intentions,
                            coef_intention=self.coef_intention, biais_intention=self.biais_intention)

    def predire(self, vecteur: np.ndarray) -> tuple[str, str, float, list[tuple[str, float]]]:
        """(famille, intention dans cette famille, confiance, deux familles les plus probables)."""

        p_famille = _softmax(self.coef_famille @ vecteur + self.biais_famille)
        p_intention = _softmax(self.coef_intention @ vecteur + self.biais_intention)
        rang = np.argsort(p_famille)[::-1]
        famille = str(self.familles[rang[0]])
        dans_la_famille = np.where(self._famille_des_intentions == famille, p_intention, -1.0)
        intention = str(self.intentions[int(np.argmax(dans_la_famille))])
        alternatives = [(str(self.familles[i]), float(p_famille[i])) for i in rang[:2]]
        return famille, intention, float(p_famille[rang[0]]), alternatives


@lru_cache(maxsize=1)
def _charger() -> tuple[Any, Tetes, dict[str, Any] | None] | None:
    if os.environ.get("ASSISTANT_CLASSIFIEUR", "1") == "0" or not TETES.exists():
        return None
    try:
        from sentence_transformers import SentenceTransformer

        encodeur = SentenceTransformer(ENCODEUR, device="cpu")
    except (ImportError, OSError, ValueError):  # bibliothèque absente, modèle introuvable hors ligne
        return None
    exemples = None
    if EXEMPLES.exists():
        import torch

        # Recherche de la phrase proche en torch, comme l'encodeur : alterner les fils de torch
        # et ceux de numpy pour un grand produit matriciel coûtait 130 ms par message.
        with np.load(EXEMPLES) as d:
            exemples = {"vecteurs": torch.from_numpy(d["vecteurs"].astype(np.float32)), "textes": d["textes"]}
    return encodeur, Tetes.charger(TETES), exemples


def disponible() -> bool:
    return _charger() is not None


def _encoder(message: str) -> Any:
    return _charger()[0].encode([PREFIXE + message], normalize_embeddings=True, convert_to_tensor=True,
                                show_progress_bar=False)[0]


def vecteur(message: str) -> np.ndarray | None:
    return None if _charger() is None else _encoder(message).numpy()


def predire(message: str) -> Comprehension | None:
    """Compréhension au niveau ``classifieur``, ou ``None`` s'il n'est pas disponible.

    Quand elle est rendue, ``alternatives`` porte les deux familles les plus
    probables, même sous le seuil : elles servent à la question de clarification.
    """

    if _charger() is None:
        return None
    _, tetes, exemples = _charger()
    v = _encoder(message)
    famille, intention, confiance, alternatives = tetes.predire(v.numpy())
    proche = None
    if exemples is not None:
        proche = str(exemples["textes"][int((exemples["vecteurs"] @ v).argmax())])
    return Comprehension(
        famille=famille, intention=intention, confiance=confiance, niveau=NIVEAU_CLASSIFIEUR,
        modele=MODELE, alternatives=[Alternative(f, p) for f, p in alternatives], exemple_proche=proche,
    )


def prechauffer() -> bool:
    """Charge l'encodeur et fait un premier calcul, pour que le premier client n'attende pas."""

    return vecteur("bonjour") is not None
