"""Banc du niveau 2 : quel est le plus petit LLM qui répond juste depuis nos fiches ?

Les 22 questions de ``data/processed/banc_niveau2.yaml`` passent par le vrai
RAG : recherche des 3 passages, seuil de pertinence, rédaction, garde-fou
(chiffres des extraits, fidélité lexicale, citation), repli. Mesures :
- la recherche (indépendante du modèle) : bonne fiche dans les 3 passages ;
  questions hors de nos fiches bien refusées ;
- la rédaction : part des réponses du LLM acceptées par le garde-fou, et part
  des réponses finales qui contiennent les faits attendus.
La configuration « sans LLM » (repli : extrait de la meilleure fiche) sert de
référence.

Usage : ``python -m eval.bench_niveau2 qwen3:1.7b ministral-3:3b gemma4:e2b ministral-3:8b``
Écrit ``eval/resultats/niveau2.json`` et ``rapport/resultats-niveau2.tex``.
"""

from __future__ import annotations

import json
import os
import platform
import statistics
import sys
from datetime import datetime
from pathlib import Path

import yaml

from src import llm, rag
from src.texte import normaliser

RACINE = Path(__file__).resolve().parents[1]
BANC = RACINE / "data" / "processed" / "banc_niveau2.yaml"
RESULTATS = RACINE / "eval" / "resultats" / "niveau2.json"
SORTIE = RACINE / "rapport" / "resultats-niveau2.tex"


def evaluer(item: dict, modele: str | None) -> dict:
    reponse = rag.repondre(item["question"], avec_llm=modele is not None, modele=modele)
    ids = [s["id"] for s in reponse.sources]
    redaction = [e for e in reponse.etapes if e.appel_llm]
    if item.get("hors_fiches"):
        juste = not reponse.pertinent
    else:
        texte = normaliser(reponse.texte.split("\n\nSources :")[0])
        juste = reponse.pertinent and all(any(normaliser(v) in texte for v in f.split("|")) for f in item["faits"])
    return {"question": item["question"], "trouvee": item.get("hors_fiches") or item["fiche"] in ids,
            "refus_juste": (not reponse.pertinent) if item.get("hors_fiches") else reponse.pertinent,
            "accepte": reponse.repli is None, "juste": juste, "repli": reponse.repli,
            "latence_ms": sum(e.latence_ms for e in reponse.etapes), "tokens": sum(e.tokens for e in redaction)}


def latex(resultats: dict) -> str:
    rech = resultats["recherche"]
    lignes = []
    for r in sorted(resultats["configurations"].values(), key=lambda r: (r["modele"] != "sans LLM", r["modele"])):
        nom = "\\textit{sans LLM (extrait)}" if r["modele"] == "sans LLM" else f"\\texttt{{{r['modele']}}}"
        accepte = "---" if r["modele"] == "sans LLM" else f"{r['acceptes']}/{r['a_rediger']}"
        latence = f"{r['latence_p50_ms'] / 1000:.1f}".replace(".", ",")
        lignes.append(f"{nom} & {accepte} & {r['justes']}/{r['total']} & {latence} s & {r['tokens']:.0f} \\\\")
    return ("\\scriptsize\n\\begin{tabular}{@{}l c c r r@{}}\n\\toprule\n\\textbf{Rédaction} & \\textbf{Garde-fou réussi} & "
            "\\textbf{Réponses justes} & \\textbf{Latence p50} & \\textbf{Tokens} \\\\\n\\midrule\n" + "\n".join(lignes)
            + "\n\\bottomrule\n\\end{tabular}\n\n\\smallskip\n{\\tiny Recherche (e5-small, 37 fiches) : bonne fiche parmi "
            f"les 3 passages pour {rech['trouvees']}/{rech['dans_fiches']} questions ; {rech['refus']}/{rech['hors_fiches']} "
            "questions hors de nos fiches refusées. Mesuré sur " + resultats["machine"].replace("_", "\\_") + ".}\n")


def main(modeles: list[str]) -> int:
    if modeles and not llm.joignable("niveau2"):
        print(f"Serveur LLM injoignable ({llm.URL}).")
        return 1
    if not rag.disponible():
        print("Index du RAG indisponible : installer sentence-transformers.")
        return 1
    banc = yaml.safe_load(BANC.read_text(encoding="utf-8"))
    resultats = json.loads(RESULTATS.read_text(encoding="utf-8")) if RESULTATS.exists() else {"configurations": {}}
    for modele in [None, *modeles]:
        if modele:
            llm.prechauffer(modele)
        lignes = [evaluer(item, modele) for item in banc]
        dans = [l for l, i in zip(lignes, banc) if not i.get("hors_fiches")]
        nom = modele or "sans LLM"
        r = {"modele": nom, "total": len(lignes), "justes": sum(l["juste"] for l in lignes),
             "a_rediger": sum(1 for l in dans if l["refus_juste"]), "acceptes": sum(l["accepte"] for l in dans),
             "latence_p50_ms": statistics.median(l["latence_ms"] for l in lignes),
             "tokens": statistics.mean(l["tokens"] for l in lignes),
             "erreurs": [{k: l[k] for k in ("question", "repli")} for l in lignes if not l["juste"]]}
        resultats["configurations"][nom] = r
        if modele is None:
            hors = [l for l, i in zip(lignes, banc) if i.get("hors_fiches")]
            resultats["recherche"] = {"dans_fiches": len(dans), "trouvees": sum(l["trouvee"] for l in dans),
                                      "hors_fiches": len(hors), "refus": sum(l["refus_juste"] for l in hors)}
        print(f"{nom:18} justes {r['justes']}/{r['total']}  garde-fou {r['acceptes']}/{r['a_rediger']}  "
              f"p50 {r['latence_p50_ms']:.0f} ms")
    resultats.update(machine=os.environ.get("BANC_MACHINE") or f"{platform.node()} ({platform.machine()})",
                     date=datetime.now().isoformat(timespec="seconds"))
    RESULTATS.parent.mkdir(exist_ok=True)
    RESULTATS.write_text(json.dumps(resultats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SORTIE.write_text(latex(resultats), encoding="utf-8")
    print(f"Recherche : {resultats['recherche']}")
    print(f"écrit : {RESULTATS} et {SORTIE}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
