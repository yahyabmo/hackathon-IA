"""Choisir le LLM de formulation en descendant en taille.

Protocole du rapport : on part d'un modèle qui parle clairement bien (14B), on
descend, et on garde le plus petit qui tient le seuil fixé à l'avance :
**zéro nombre inventé** (garde-fou) et **au moins 27 réponses sur 30 jugées
bonnes** (exact, clair, ton juste) par deux membres de l'équipe.

Pour chaque modèle, les 30 mêmes situations de conseil sont reformulées. Le
garde-fou est vérifié automatiquement ; le jugement humain se fait dans le CSV
produit (colonnes ``juge_1`` et ``juge_2`` à remplir par oui / non, facultatives).

Usage, depuis la racine du dépôt, sur un poste où Ollama tourne :
    python -m eval.bench_formulation --situations          # les 30 situations, sans LLM
    python -m eval.bench_formulation ministral-3:14b gemma4:e2b ministral-3:8b \\
        ministral-3:3b qwen3:1.7b gemma3:1b
"""

from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path
from time import perf_counter
from typing import Any

from src import llm
from src.conseiller import clients, conseiller
from src.contrats import EtatConversation
from src.converser.dialogue import Decision, parcours_disponibles
from src.converser.formuler import SYSTEME_FORMULATION, gabarit
from src.converser.garde_fou import nombres, verifier
from src.taxonomie import famille_de

RESULTATS = Path(__file__).resolve().parent / "resultats"

# (client, parcours, informations recueillies) : 30 conseils variés, acceptés et refusés.
SITUATIONS: list[tuple[str, str, dict[str, Any]]] = [
    *[(c, "credit_immobilier", {"prix_bien": p, "apport": a})
      for c in ("C07", "C01", "C05")
      for p, a in ((150000, 20000), (250000, 25000), (320000, 60000))],
    *[(c, "credit_conso", {"objet": "voiture", "montant": m, "duree_mois": d})
      for c in ("C05", "C01", "C08")
      for m, d in ((5000, 24), (12000, 48), (20000, 60))],
    *[(c, "epargne_projet", {"pour_qui": q, "horizon_mois": h, "montant_mensuel": m})
      for c, q in (("C03", "enfants"), ("C08", "soi"), ("C01", "soi"), ("C07", "soi"), ("C04", "soi"))
      for h, m in ((24, 50), (120, 100))],
    ("C08", "pret_etudiant", {"montant": 5000}),
    ("C01", "pret_etudiant", {"montant": 8000}),
]


def preparer(client: str, parcours: str, infos: dict[str, Any]) -> tuple[str, str]:
    """Le gabarit de la situation, construit par le vrai pipeline (règles + formulation)."""

    profil = clients.profil(client)
    slots = {"revenus_nets": profil["revenus_nets"], "mensualites_en_cours": profil["mensualites_credits"],
             **infos}
    fin = parcours_disponibles()[parcours]["fin"]
    decision = Decision("conseil", parcours=parcours, mention_legale=fin.get("mention_legale"),
                        proposer=fin.get("proposer"))
    etat = EtatConversation(parcours=parcours, famille=famille_de(parcours), slots=slots)
    return f"{client}-{parcours}-{'-'.join(str(v) for v in infos.values())}", \
        gabarit(decision, conseiller(parcours, profil, slots), None, profil, etat, "")


def evaluer(modele: str) -> list[dict[str, Any]]:
    lignes = []
    for client, parcours, infos in SITUATIONS:
        nom, texte = preparer(client, parcours, infos)
        debut = perf_counter()
        reformule, tokens = llm.generer(modele, SYSTEME_FORMULATION, texte)
        problemes = verifier(reformule, set(nombres(texte)))
        lignes.append({
            "situation": nom, "gabarit": texte, "reformulation": reformule,
            "garde_fou": "ok" if not problemes else "; ".join(problemes),
            "latence_ms": round((perf_counter() - debut) * 1000), "tokens": tokens,
            "juge_1": "", "juge_2": "",
        })
    return lignes


def main(arguments: list[str]) -> int:
    if not arguments or arguments == ["--situations"]:
        for client, parcours, infos in SITUATIONS:
            nom, texte = preparer(client, parcours, infos)
            print(f"— {nom}\n  {texte}\n")
        print(f"{len(SITUATIONS)} situations")
        return 0
    if not llm.joignable():
        print(f"Ollama ne répond pas sur {llm.URL} : lancer « ollama serve » d'abord.")
        return 1
    RESULTATS.mkdir(exist_ok=True)
    print(f"{'modèle':22} {'garde-fou ok':>13} {'latence p50':>12} {'p95':>8} {'tokens':>7}")
    for modele in arguments:
        lignes = evaluer(modele)
        chemin = RESULTATS / f"formulation-{modele.replace(':', '_')}.csv"
        with chemin.open("w", newline="", encoding="utf-8") as f:
            ecrivain = csv.DictWriter(f, fieldnames=list(lignes[0]))
            ecrivain.writeheader()
            ecrivain.writerows(lignes)
        latences = sorted(l["latence_ms"] for l in lignes)
        ok = sum(l["garde_fou"] == "ok" for l in lignes)
        print(f"{modele:22} {ok:>9}/{len(lignes)} {statistics.median(latences):>10} ms "
              f"{latences[int(0.95 * (len(latences) - 1))]:>5} ms {statistics.mean(l['tokens'] for l in lignes):>7.0f}")
    print(f"\nCSV dans {RESULTATS} : remplir juge_1 et juge_2 (oui / non), puis garder le plus petit "
          "modèle à zéro nombre inventé et 27 bonnes réponses sur 30.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
