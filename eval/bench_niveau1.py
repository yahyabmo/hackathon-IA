"""Banc du niveau 1 : quel est le plus petit LLM qui comprend les messages flous ?

Les 36 messages de ``data/processed/banc_niveau1.yaml`` (réponses libres,
réponse et nouvelle demande mêlées, messages flous, plusieurs demandes, renvois
au contexte) passent par le vrai chemin de l'assistant : contexte, RAG
d'exemples, JSON imposé, vérification et rattachement par le code. Chaque
modèle est mesuré avec et sans le RAG d'exemples.

Un message est juste si les sujets compris mènent au bon parcours (bonne
famille pour une demande de service, bonne intention pour nos parcours) et si
la valeur retenue pour l'information attendue est la bonne (ou rien, s'il n'y
en avait pas).

Usage, sur un poste où Ollama tourne (``BANC_MACHINE`` nomme le poste) :
    python -m eval.bench_niveau1 qwen3:1.7b gemma3:1b ministral-3:3b gemma4:e2b ministral-3:8b
Écrit ``eval/resultats/niveau1.json`` et ``rapport/resultats-niveau1.tex``.
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

from src import llm
from src.assistant import _appliquer, _contexte, _rattacher
from src.comprendre import interprete
from src.comprendre.entrainer import routage_correct
from src.conseiller import clients
from src.contrats import NIVEAU_REPONSE, Comprehension, EtatConversation
from src.converser.dialogue import parcours_disponibles
from src.taxonomie import famille_de
from src.texte import normaliser

RACINE = Path(__file__).resolve().parents[1]
BANC = RACINE / "data" / "processed" / "banc_niveau1.yaml"
RESULTATS = RACINE / "eval" / "resultats" / "niveau1.json"
SORTIE = RACINE / "rapport" / "resultats-niveau1.tex"
CLES = {"lien": "lien", "objet": "objet", "duree": "duree_mois", "montant": "montants"}


def etat_de(item: dict) -> EtatConversation:
    contexte = item.get("contexte") or {}
    parcours = contexte.get("parcours")
    return EtatConversation(parcours=parcours, famille=famille_de(parcours) if parcours else None,
                            info_attendue=contexte.get("info"), traites=list(contexte.get("traites", [])))


def _valeur_lue(comprehension: Comprehension, etat: EtatConversation, depart: Comprehension):
    if comprehension is depart or comprehension.niveau != NIVEAU_REPONSE or not etat.info_attendue:
        return None
    info = parcours_disponibles()[etat.parcours]["infos"][etat.info_attendue]
    valeur = comprehension.entites.get(CLES.get(info["type"], info["type"]))
    return valeur[0] if isinstance(valeur, list) else valeur


def evaluer(item: dict, modele: str, avec_exemples: bool) -> dict:
    etat, profil, message = etat_de(item), clients.profil("C01"), item["message"]
    resultat = interprete.interpreter(message, _contexte(etat, profil), modele, avec_exemples=avec_exemples)
    depart = (Comprehension(famille=etat.famille, intention=etat.parcours, niveau=NIVEAU_REPONSE)
              if etat.info_attendue else Comprehension())
    comprehension = depart
    if resultat.valide:
        comprehension, _, _ = _appliquer(resultat, depart, etat, message)
    else:
        _rattacher(resultat, etat, message)
    attendues, comprises = item["intentions"], [i for i in resultat.intentions if i != "inconnue"]
    valeur = _valeur_lue(comprehension, etat, depart)
    if etat.info_attendue and (valeur is not None or not comprises) and etat.parcours not in comprises:
        comprises = [etat.parcours, *comprises]  # la question en cours reçoit sa réponse (ou rien de nouveau)
    intentions_justes = bool(comprises) and routage_correct(comprises[0], attendues[0]) and all(
        any(routage_correct(c, a) for c in comprises) for a in attendues)
    attendue = item.get("valeur")
    valeur_juste = (normaliser(str(valeur)) == normaliser(str(attendue))) if attendue else valeur is None
    return {"message": message, "comprises": comprises, "attendues": attendues, "valeur": valeur,
            "juste": intentions_justes and (valeur_juste or not etat.info_attendue),
            "json_valide": resultat.raison != "sortie illisible",
            "latence_ms": resultat.etape.latence_ms, "tokens": resultat.etape.tokens}


def _pct(x: float) -> str:
    return f"{100 * x:.0f}\\,\\%"


def latex(resultats: dict) -> str:
    lignes = []
    for cle, r in sorted(resultats["configurations"].items(), key=lambda kv: (kv[1]["modele"], not kv[1]["exemples"])):
        lignes.append(f"\\texttt{{{r['modele']}}} & {'oui' if r['exemples'] else 'non'} & {r['justes']}/{r['total']} & "
                      f"{_pct(r['json_valide'])} & {r['latence_p50_ms'] / 1000:.1f} s & {r['tokens']:.0f} \\\\".replace(".", ","))
    return ("\\scriptsize\n\\begin{tabular}{@{}l c c c r r@{}}\n\\toprule\n\\textbf{Modèle} & \\textbf{RAG d'exemples} & "
            "\\textbf{Justes} & \\textbf{JSON valide} & \\textbf{Latence p50} & \\textbf{Tokens} \\\\\n\\midrule\n"
            + "\n".join(lignes) + "\n\\bottomrule\n\\end{tabular}\n\n\\smallskip\n{\\tiny 36 messages difficiles écrits par "
            "l'équipe (réponses libres, demandes mêlées, renvois au contexte). JSON imposé par une grammaire. Mesuré sur "
            + resultats["machine"].replace("_", "\\_") + ".}\n")


def main(modeles: list[str]) -> int:
    if not modeles:
        print(__doc__)
        return 2
    if not llm.joignable("niveau1"):
        print(f"Serveur LLM injoignable ({llm.URL}).")
        return 1
    banc = yaml.safe_load(BANC.read_text(encoding="utf-8"))
    resultats = json.loads(RESULTATS.read_text(encoding="utf-8")) if RESULTATS.exists() else {"configurations": {}}
    for modele in modeles:
        llm.prechauffer(modele)
        for avec in (True, False):
            lignes = [evaluer(item, modele, avec) for item in banc]
            r = {"modele": modele, "exemples": avec, "total": len(lignes), "justes": sum(l["juste"] for l in lignes),
                 "json_valide": sum(l["json_valide"] for l in lignes) / len(lignes),
                 "latence_p50_ms": statistics.median(l["latence_ms"] for l in lignes),
                 "tokens": statistics.mean(l["tokens"] for l in lignes),
                 "erreurs": [{k: l[k] for k in ("message", "comprises", "attendues", "valeur")} for l in lignes if not l["juste"]]}
            resultats["configurations"][f"{modele}|{'avec' if avec else 'sans'}"] = r
            print(f"{modele:18} exemples={'oui' if avec else 'non'}  justes {r['justes']}/{r['total']}  "
                  f"JSON valide {100 * r['json_valide']:.0f} %  p50 {r['latence_p50_ms']:.0f} ms")
    resultats.update(machine=os.environ.get("BANC_MACHINE") or f"{platform.node()} ({platform.machine()})",
                     date=datetime.now().isoformat(timespec="seconds"))
    RESULTATS.parent.mkdir(exist_ok=True)
    RESULTATS.write_text(json.dumps(resultats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SORTIE.write_text(latex(resultats), encoding="utf-8")
    print(f"écrit : {RESULTATS} et {SORTIE}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
