"""Rejoue 30 conversations libres et écrit un rapport à juger, réponse par réponse.

Les conversations (``eval/conversations_libres.yaml``) imitent de vrais clients :
fautes, familier, plusieurs demandes, changements de sujet, questions ouvertes,
refus, hors sujet. Il n'y a pas de résultat attendu automatique : le rapport
montre chaque réponse avec son niveau, ce qui a été compris et sa latence, plus
les signaux qui méritent un coup d'œil (incompris, clarification, orientation
faute de comprendre, « Bonjour ! » hors de propos, repli du garde-fou).

Usage, depuis la racine du dépôt :
    ASSISTANT_LLM=1 python -m eval.rejouer_conversations      # avec les niveaux 1 et 2
    python -m eval.rejouer_conversations                      # sans LLM
Écrit ``eval/resultats/conversations-libres.md`` (et ``.json``).
"""

from __future__ import annotations

import json
import os
import platform
import statistics
import tempfile
from collections import Counter
from datetime import datetime
from pathlib import Path

import yaml

os.environ.setdefault("INCOMPRIS_FICHIER", str(Path(tempfile.gettempdir()) / "incompris-conversations.jsonl"))

from src import llm  # noqa: E402
from src.assistant import reply  # noqa: E402
from src.comprendre import classifieur  # noqa: E402
from src.contrats import EtatConversation  # noqa: E402

RACINE = Path(__file__).resolve().parents[1]
CONVERSATIONS = RACINE / "eval" / "conversations_libres.yaml"
SORTIE = RACINE / "eval" / "resultats" / "conversations-libres.md"
SIGNAUX = {
    "incompris": "Je n'ai pas bien compris",
    "clarification": "Pour bien vous aider",
    "question fermée": "Pour être sûr de bien vous aider",
    "orienté faute de comprendre": "Je préfère ne pas deviner",
    "« Bonjour ! »": "Bonjour !",
    "pas de fiche": "Je n'ai pas encore de fiche",
    "hors de nos fiches": "Je n'ai pas cette information",
}


def rejouer() -> list[dict]:
    resultats = []
    for conversation in yaml.safe_load(CONVERSATIONS.read_text(encoding="utf-8")):
        etat, tours = EtatConversation(), []
        for message in conversation["messages"]:
            reponse, etat = reply(message, conversation["client"], etat)
            c = reponse.comprehension
            replis = [e.modele for e in reponse.trace if e.appel_llm and "refusé" in (e.modele or "")]
            tours.append({
                "message": message, "texte": reponse.texte, "niveau": reponse.niveau,
                "raison": reponse.raison_niveau, "intention": c.intention, "comprise_par": c.niveau,
                "confiance": round(c.confiance, 2), "appels_llm": reponse.appels_llm,
                "latence_ms": round(sum(e.latence_ms for e in reponse.trace), 1),
                "signaux": [nom for nom, motif in SIGNAUX.items() if motif in reponse.texte]
                           + (["repli du garde-fou"] if replis else []),
                "sources": [s["titre"] for s in reponse.sources],
            })
        resultats.append({**{k: conversation[k] for k in ("id", "client", "theme")}, "tours": tours})
    return resultats


def rapport(resultats: list[dict]) -> str:
    tours = [t for c in resultats for t in c["tours"]]
    niveaux = Counter(t["niveau"] for t in tours)
    signaux = Counter(s for t in tours for s in t["signaux"])
    latences = sorted(t["latence_ms"] for t in tours)
    mode = (f"niveaux 1 et 2 actifs ({llm.MODELE_NIVEAU1} / {llm.MODELE_NIVEAU2})" if llm.actif()
            else "sans LLM (niveau 0, RAG en extrait)")
    lignes = [
        "# Conversations libres : 30 conversations rejouées", "",
        f"Généré le {datetime.now():%d/%m/%Y à %H h %M} sur {platform.node()}, {mode}.", "",
        "## Résumé", "",
        f"- {len(tours)} messages, dans {len(resultats)} conversations.",
        f"- Niveaux : 0 : {niveaux[0]} · 1 : {niveaux[1]} · 2 : {niveaux[2]}.",
        f"- Appels au LLM : {sum(t['appels_llm'] for t in tours)}. Latence p50 {statistics.median(latences):.1f} ms, "
        f"p95 {latences[int(0.95 * (len(latences) - 1))]:.0f} ms.",
        "- Signaux à regarder : " + (", ".join(f"{nom} : {n}" for nom, n in signaux.most_common()) or "aucun") + ".",
        "",
    ]
    for c in resultats:
        lignes += [f"## {c['id']}. {c['client']} — {c['theme']}", ""]
        for numero, t in enumerate(c["tours"], start=1):
            etiquette = (f"niveau {t['niveau']} · {t['intention']} ({t['comprise_par']}, {t['confiance']})"
                         f" · {t['latence_ms']} ms" + (f" · {t['appels_llm']} LLM" if t["appels_llm"] else ""))
            texte = t["texte"].split("\n\nSources :")[0].replace("\n\n", " ⏎ ")
            lignes += [f"**{numero}. Client** : {t['message']}", "",
                       f"> {texte}", "",
                       f"<sub>{etiquette} — {t['raison']}"
                       + (f" — ⚠ {', '.join(t['signaux'])}" if t["signaux"] else "")
                       + (f" — sources : {', '.join(t['sources'])}" if t["sources"] else "") + "</sub>", ""]
    return "\n".join(lignes) + "\n"


def main() -> int:
    classifieur.prechauffer()
    if llm.actif():
        llm.prechauffer(llm.MODELE_NIVEAU1)
    resultats = rejouer()
    SORTIE.parent.mkdir(exist_ok=True)
    SORTIE.write_text(rapport(resultats), encoding="utf-8")
    SORTIE.with_suffix(".json").write_text(json.dumps(resultats, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(rapport(resultats).split("\n## 1.")[0])
    print(f"écrit : {SORTIE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
