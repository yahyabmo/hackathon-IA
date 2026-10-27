"""Tableau des résultats du banc de formulation, pour le support de soutenance.

Lit ``eval/resultats/formulation-*.csv`` et écrit ``rapport/resultats-formulation.tex``
(inclus par ``rapport/soutenance.tex``). Les modèles sont rangés du plus gros au
plus petit ; le retenu est le plus petit qui passe le garde-fou sur toutes les
situations et que les juges ont validé (27 sur 30), quand le jugement est fait.

Usage : ``python -m eval.tableau_formulation``
"""

from __future__ import annotations

import csv
import platform
import statistics
from pathlib import Path

from src import llm

RESULTATS = Path(__file__).resolve().parent / "resultats"
SORTIE = Path(__file__).resolve().parents[1] / "rapport" / "resultats-formulation.tex"
SEUIL_JUGES = 27
TAILLES_CONNUES = {  # Go, bibliothèque Ollama, si le serveur ne répond pas
    "ministral-3:14b": 9.1, "gemma4:e2b": 4.6, "ministral-3:8b": 6.0, "ministral-3:3b": 3.0,
    "qwen3:1.7b": 1.4, "gemma3:1b": 0.8, "qwen3:0.6b": 0.5, "gemma3:270m": 0.3,
}


def _tailles() -> dict[str, float]:
    tailles = dict(TAILLES_CONNUES)
    try:
        for m in llm._requete(f"{llm.URL}/api/tags", delai=2)["models"]:
            tailles[m["name"]] = round(m["size"] / 1e9, 1)
    except (OSError, KeyError, ValueError):
        pass
    return tailles


def lire() -> list[dict]:
    tailles, lignes = _tailles(), []
    for fichier in RESULTATS.glob("formulation-*.csv"):
        modele = fichier.stem.removeprefix("formulation-").replace("_", ":", 1)
        rangs = list(csv.DictReader(fichier.open(encoding="utf-8")))
        juges = [r for r in rangs if r["juge_1"] and r["juge_2"]]
        lignes.append({
            "modele": modele,
            "taille": tailles.get(modele),
            "garde_fou": sum(r["garde_fou"] == "ok" for r in rangs),
            "total": len(rangs),
            "latence": statistics.median(int(r["latence_ms"]) for r in rangs),
            "tokens": statistics.mean(int(r["tokens"]) for r in rangs),
            "juges": (sum(r["juge_1"] == "oui" and r["juge_2"] == "oui" for r in juges)
                      if len(juges) == len(rangs) else None),
            "machine": rangs[0].get("machine") or f"{platform.node()} (CPU)",
        })
    return sorted(lignes, key=lambda l: -(l["taille"] or 0))


def _retenu(lignes: list[dict]) -> str | None:
    valides = [l for l in lignes if l["garde_fou"] == l["total"] and (l["juges"] or 0) >= SEUIL_JUGES]
    return min(valides, key=lambda l: l["taille"] or 0)["modele"] if valides else None


def latex(lignes: list[dict]) -> str:
    if not lignes:
        return "\\centering\\textit{Banc en cours : résultats à venir.}\n"
    retenu = _retenu(lignes)
    corps = []
    for l in lignes:
        juges = (f"{l['juges']}/{l['total']}" if l["juges"] is not None else "\\textit{à juger}")
        nom = f"\\texttt{{{l['modele']}}}"
        if l["modele"] == retenu:
            nom = f"\\textbf{{{nom}}} \\textcolor{{okgreen}}{{(retenu)}}"
        taille = f"{l['taille']:.1f}".replace(".", ",") if l["taille"] else "?"
        latence = f"{l['latence'] / 1000:.1f}".replace(".", ",")
        corps.append(f"{nom} & {taille} Go & {l['garde_fou']}/{l['total']} & {juges} & "
                     f"{latence} s & {l['tokens']:.0f} \\\\")
    machines = ", ".join(sorted({l["machine"] for l in lignes})).replace("_", "\\_")
    gros = any((l["taille"] or 0) >= 9 for l in lignes)
    return (
        "\\centering\\small\n\\begin{tabular}{@{}l r c c r r@{}}\n\\toprule\n"
        "\\textbf{Modèle} & \\textbf{Taille} & \\textbf{Garde-fou} & \\textbf{Juges} & "
        "\\textbf{Latence p50} & \\textbf{Tokens} \\\\\n\\midrule\n" + "\n".join(corps) +
        "\n\\bottomrule\n\\end{tabular}\n\n\\medskip\n{\\scriptsize Mesuré sur " + machines +
        ("" if gros else " ; le 14B se mesure sur un poste à GPU") + ". Garde-fou : aucun chiffre "
        "inventé ni oublié, longueur plausible.}\n"
    )


if __name__ == "__main__":
    lignes = lire()
    SORTIE.write_text(latex(lignes), encoding="utf-8")
    for l in lignes:
        print(f"{l['modele']:18} {l['taille'] or '?':>5} Go  garde-fou {l['garde_fou']}/{l['total']}  "
              f"latence p50 {l['latence'] / 1000:.1f} s  tokens {l['tokens']:.0f}")
    print(f"écrit : {SORTIE}")
