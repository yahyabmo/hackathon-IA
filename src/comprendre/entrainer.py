"""Entraîner le classifieur de l'étage 1 : encodeur multilingue + deux têtes.

Données : Banking77 en anglais, tel quel (sans traduction), plus nos phrases
(``data/processed/exemples_fr.yaml``). 10 % sont mis de côté pour choisir la
régularisation et le seuil τ ; les têtes sont ensuite réentraînées sur tout.

Seuil τ : le plus petit qui donne au moins 97 % de routages corrects parmi les
messages acceptés (bonne famille pour une intention de service Banking77,
bonne intention pour une intention de l'équipe, qui a son propre parcours).

Sorties :
- ``data/processed/classifieur.npz`` et ``classifieur.json`` : les têtes
  (quelques centaines de Ko, versionnées) et le seuil, avec les mesures ;
- ``models/exemples.npz`` : les vecteurs des phrases d'entraînement, pour
  montrer la plus proche (non versionné, recréé par ce script).

Usage : ``python -m src.comprendre.entrainer [--energie]`` (CodeCarbon autour
de l'entraînement, pour le coût de la préparation hors ligne), ou
``--exemples-seulement`` pour recréer l'index des phrases sans toucher aux têtes
versionnées (installation d'un nouveau poste).
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from time import perf_counter

import numpy as np
import yaml

from ..taxonomie import NOUVELLES_INTENTIONS, famille_de
from .classifieur import ENCODEUR, EXEMPLES, META, PREFIXE, TETES

RACINE = Path(__file__).resolve().parents[2]
BANKING77 = RACINE / "data" / "raw" / "banking77"
EXEMPLES_FR = RACINE / "data" / "processed" / "exemples_fr.yaml"
PRECISION_VISEE = 0.97
PART_VALIDATION = 0.1
GRAINE = 0
REGULARISATIONS = (1.0, 10.0, 100.0)


def lire_banking77(nom: str) -> list[tuple[str, str]]:
    with (BANKING77 / f"{nom}.csv").open(encoding="utf-8") as f:
        return [(ligne["text"], ligne["category"]) for ligne in csv.DictReader(f)]


def lire_exemples_equipe() -> list[tuple[str, str]]:
    donnees = yaml.safe_load(EXEMPLES_FR.read_text(encoding="utf-8"))
    exemples = [(phrase, intention) for intention, langues in donnees["nouvelles_intentions"].items()
                for phrases in langues.values() for phrase in phrases]
    exemples += [(phrase, intention) for lignes in donnees["familles_banking77"].values()
                 for intention, phrase in lignes]
    return exemples


def encoder(textes: list[str], modele=None) -> np.ndarray:
    from sentence_transformers import SentenceTransformer

    modele = modele or SentenceTransformer(ENCODEUR, device="cpu")
    return modele.encode([PREFIXE + t for t in textes], batch_size=128, normalize_embeddings=True,
                         convert_to_numpy=True, show_progress_bar=False)


def routage_correct(predite: str, vraie: str) -> bool:
    """Ce qui compte pour la suite : la famille, et l'intention si elle a son parcours."""

    if vraie in NOUVELLES_INTENTIONS or predite in NOUVELLES_INTENTIONS:
        return predite == vraie
    return famille_de(predite) == famille_de(vraie)


def choisir_tau(confiances: np.ndarray, corrects: np.ndarray) -> tuple[float, float, float]:
    """Plus petit τ donnant la précision visée sur les acceptés : (τ, précision, part acceptée)."""

    for tau in np.arange(0.0, 1.0, 0.01):
        acceptes = confiances >= tau
        if acceptes.sum() and corrects[acceptes].mean() >= PRECISION_VISEE:
            return round(float(tau), 2), float(corrects[acceptes].mean()), float(acceptes.mean())
    return 0.99, float("nan"), 0.0


def _separer(n: int, etiquettes: list[str]) -> tuple[np.ndarray, np.ndarray]:
    """Séparation stratifiée par intention, graine fixe."""

    generateur = np.random.default_rng(GRAINE)
    validation = []
    for etiquette in sorted(set(etiquettes)):
        indices = [i for i, e in enumerate(etiquettes) if e == etiquette]
        generateur.shuffle(indices)
        validation += indices[:max(1, round(PART_VALIDATION * len(indices)))]
    masque = np.zeros(n, dtype=bool)
    masque[validation] = True
    return np.flatnonzero(~masque), np.flatnonzero(masque)


def indexer_exemples() -> int:
    """Seulement ``models/exemples.npz`` : les vecteurs des phrases, pour la plus proche."""

    donnees = lire_banking77("train") + lire_exemples_equipe()
    EXEMPLES.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(EXEMPLES, vecteurs=encoder([t for t, _ in donnees]).astype(np.float16),
                        textes=np.array([t for t, _ in donnees]), intentions=np.array([i for _, i in donnees]))
    return len(donnees)


def entrainer() -> dict:
    from sklearn.linear_model import LogisticRegression

    from . import classifieur

    debut = perf_counter()
    donnees = lire_banking77("train") + lire_exemples_equipe()
    textes, intentions = [t for t, _ in donnees], [i for _, i in donnees]
    familles = [famille_de(i) for i in intentions]
    vecteurs = encoder(textes)
    duree_encodage = perf_counter() - debut

    train, val = _separer(len(textes), intentions)
    y_int, y_fam = np.array(intentions), np.array(familles)

    def tete(y: np.ndarray, indices: np.ndarray, c: float) -> LogisticRegression:
        return LogisticRegression(C=c, max_iter=2000).fit(vecteurs[indices], y[indices])

    scores = {c: tete(y_int, train, c).score(vecteurs[val], y_int[val]) for c in REGULARISATIONS}
    c = max(scores, key=scores.get)
    tete_fam, tete_int = tete(y_fam, train, c), tete(y_int, train, c)
    tetes = classifieur.Tetes.depuis_sklearn(tete_fam, tete_int)
    predictions = [tetes.predire(v) for v in vecteurs[val]]
    confiances = np.array([p[2] for p in predictions])
    corrects = np.array([routage_correct(p[1], y_int[i]) for p, i in zip(predictions, val)])
    tau, precision, couverture = choisir_tau(confiances, corrects)

    # Têtes finales sur toutes les données, avec la régularisation et le seuil choisis.
    tous = np.arange(len(textes))
    tetes = classifieur.Tetes.depuis_sklearn(tete(y_fam, tous, c), tete(y_int, tous, c))
    duree = perf_counter() - debut

    TETES.parent.mkdir(parents=True, exist_ok=True)
    tetes.enregistrer(TETES)
    EXEMPLES.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(EXEMPLES, vecteurs=vecteurs.astype(np.float16), textes=np.array(textes),
                        intentions=y_int)
    meta = {
        "encodeur": ENCODEUR, "prefixe": PREFIXE, "tau": tau, "regularisation_C": c,
        "precision_visee": PRECISION_VISEE, "validation": {
            "taille": int(len(val)), "exactitude_intention": round(scores[c], 4),
            "routage_correct_tous": round(float(corrects.mean()), 4),
            "precision_acceptes": round(precision, 4), "part_acceptee": round(couverture, 4),
        },
        "exemples": {"banking77_anglais": len(lire_banking77("train")),
                     "equipe": len(lire_exemples_equipe()), "total": len(textes)},
        "taille_tetes_ko": round(TETES.stat().st_size / 1024, 1),
        "duree_entrainement_s": round(duree, 1), "duree_encodage_s": round(duree_encodage, 1),
        "date": datetime.now().isoformat(timespec="seconds"),
    }
    META.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return meta


def main(arguments: list[str]) -> int:
    if "--exemples-seulement" in arguments:
        print(f"{indexer_exemples()} phrases indexées dans {EXEMPLES}")
        return 0
    if "--energie" in arguments:
        from codecarbon import OfflineEmissionsTracker

        suivi = OfflineEmissionsTracker(country_iso_code="FRA", save_to_file=False, log_level="error")
        suivi.start()
        meta = entrainer()
        suivi.stop()
        meta["energie_wh"] = round(suivi.final_emissions_data.energy_consumed * 1000, 3)
        META.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        meta = entrainer()
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
