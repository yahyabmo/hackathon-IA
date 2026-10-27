"""Banc de compréhension : l'étage 1, en anglais et en français, du moins cher au plus cher.

Deux jeux de test, jamais vus à l'entraînement :
- le test officiel Banking77 (3 080 phrases anglaises), comparable à l'article ;
- notre test français (250 phrases, ``data/processed/test_fr.yaml``).
L'écart entre les deux mesure ce que l'encodeur multilingue transfère sans traduction.

Configurations : mots-clés ; TF-IDF + régression logistique (mêmes données
d'entraînement) ; e5-small + régression logistique (le classifieur de
l'assistant) ; l'étage 1 complet (mots-clés, puis classifieur au-dessus de τ) ;
en option, un LLM qui classe seul, avec la consigne de l'escalade.

Mesures : intention exacte en anglais (77 classes, comme l'article) ; routage
correct en français (bonne famille pour une demande de service, bonne intention
pour nos parcours) ; part acceptée et précision des acceptés ; latence p50 par
message, un message à la fois ; taille en mémoire.

Usage, depuis la racine du dépôt :
    python -m eval.bench_comprendre                         # tout, sauf le LLM
    python -m eval.bench_comprendre --llm=ministral-3:14b   # ajoute le LLM (poste à GPU)
Écrit ``eval/resultats/comprendre.json`` (les mesures s'ajoutent) et
``rapport/resultats-comprendre.tex`` (inclus par le support).
"""

from __future__ import annotations

import json
import os
import platform
import statistics
import sys
from datetime import datetime
from pathlib import Path
from time import perf_counter

import numpy as np
import yaml

from src.comprendre import classifieur, comprendre, mots_cles
from src.comprendre.entrainer import lire_banking77, lire_exemples_equipe, routage_correct
from src.contrats import EtatConversation
from src.taxonomie import famille_de

RACINE = Path(__file__).resolve().parents[1]
TEST_FR = RACINE / "data" / "processed" / "test_fr.yaml"
RESULTATS = RACINE / "eval" / "resultats" / "comprendre.json"
SORTIE = RACINE / "rapport" / "resultats-comprendre.tex"
PAS_ECHANTILLON_LLM = 10  # le LLM classe une phrase anglaise sur 10 (308), pour rester raisonnable


def lire_test_fr() -> list[tuple[str, str]]:
    donnees = yaml.safe_load(TEST_FR.read_text(encoding="utf-8"))
    return [(phrase, intention) for lignes in donnees.values() for intention, phrase in lignes]


def _p50(latences: list[float]) -> float:
    return round(statistics.median(latences), 2)


def _taux(n: int, total: int) -> float | None:
    return round(n / total, 4) if total else None


def banc_mots_cles(test_fr: list[tuple[str, str]]) -> dict:
    latences, acceptes, corrects = [], 0, 0
    for phrase, vraie in test_fr:
        debut = perf_counter()
        c = mots_cles.detecter(phrase)
        latences.append((perf_counter() - debut) * 1000)
        if c is not None:
            acceptes += 1
            corrects += routage_correct(c.intention, vraie)
    return {"nom": "Mots-clés", "fr_part_acceptee": _taux(acceptes, len(test_fr)),
            "fr_precision_acceptes": _taux(corrects, acceptes), "latence_ms": _p50(latences),
            "taille_octets": len(json.dumps(mots_cles.LEXIQUE, ensure_ascii=False).encode())}


def banc_tfidf(test_en: list[tuple[str, str]], test_fr: list[tuple[str, str]]) -> dict:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression

    donnees = lire_banking77("train") + lire_exemples_equipe()
    vectoriseur = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=2)
    tete = LogisticRegression(C=10.0, max_iter=2000).fit(
        vectoriseur.fit_transform([t for t, _ in donnees]), [i for _, i in donnees])
    en = tete.predict(vectoriseur.transform([t for t, _ in test_en]))
    latences, corrects_fr = [], 0
    for phrase, vraie in test_fr:
        debut = perf_counter()
        predite = tete.predict(vectoriseur.transform([phrase]))[0]
        latences.append((perf_counter() - debut) * 1000)
        corrects_fr += routage_correct(predite, vraie)
    return {"nom": "TF-IDF + régression logistique",
            "en_intention": _taux(sum(p == v for p, (_, v) in zip(en, test_en)), len(test_en)),
            "en_famille": _taux(sum(famille_de(p) == famille_de(v) for p, (_, v) in zip(en, test_en)),
                                len(test_en)),
            "fr_routage": _taux(corrects_fr, len(test_fr)), "latence_ms": _p50(latences),
            "taille_octets": int(tete.coef_.size * 4 + sum(len(m) for m in vectoriseur.vocabulary_))}


def banc_e5(test_en: list[tuple[str, str]], test_fr: list[tuple[str, str]]) -> dict:
    if not classifieur.prechauffer():
        raise SystemExit("Classifieur indisponible : installer sentence-transformers et entraîner les têtes.")
    encodeur, tetes, _ = classifieur._charger()
    vecteurs = encodeur.encode([classifieur.PREFIXE + t for t, _ in test_en], batch_size=128,
                               normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False)
    intentions = tetes.intentions[np.argmax(vecteurs @ tetes.coef_intention.T + tetes.biais_intention, axis=1)]
    familles = tetes.familles[np.argmax(vecteurs @ tetes.coef_famille.T + tetes.biais_famille, axis=1)]
    latences, corrects, acceptes, corrects_acceptes = [], 0, 0, 0
    for phrase, vraie in test_fr:
        debut = perf_counter()
        c = classifieur.predire(phrase)
        latences.append((perf_counter() - debut) * 1000)
        juste = routage_correct(c.intention, vraie)
        corrects += juste
        if c.confiance >= classifieur.SEUIL_TAU:
            acceptes += 1
            corrects_acceptes += juste
    parametres = sum(p.numel() for p in encodeur.parameters())
    return {"nom": "e5-small + régression logistique",
            "en_intention": _taux(sum(str(p) == v for p, (_, v) in zip(intentions, test_en)), len(test_en)),
            "en_famille": _taux(sum(str(p) == famille_de(v) for p, (_, v) in zip(familles, test_en)),
                                len(test_en)),
            "fr_routage": _taux(corrects, len(test_fr)), "fr_part_acceptee": _taux(acceptes, len(test_fr)),
            "fr_precision_acceptes": _taux(corrects_acceptes, acceptes), "tau": classifieur.SEUIL_TAU,
            "latence_ms": _p50(latences), "parametres": int(parametres),
            "taille_octets": int(parametres * 4 + classifieur.TETES.stat().st_size)}


def banc_etage1(test_fr: list[tuple[str, str]]) -> dict:
    latences, comprises, corrects, niveaux = [], 0, 0, {}
    for phrase, vraie in test_fr:
        debut = perf_counter()
        c = comprendre(phrase, EtatConversation())
        latences.append((perf_counter() - debut) * 1000)
        if c.comprise:
            comprises += 1
            corrects += routage_correct(c.intention, vraie)
            niveaux[c.niveau] = niveaux.get(c.niveau, 0) + 1
    return {"nom": "Étage 1 : mots-clés, puis e5-small au-dessus de τ",
            "fr_part_acceptee": _taux(comprises, len(test_fr)),
            "fr_precision_acceptes": _taux(corrects, comprises), "niveaux": niveaux,
            "latence_ms": _p50(latences)}


def banc_llm(modele: str, test_en: list[tuple[str, str]], test_fr: list[tuple[str, str]]) -> dict:
    from src import llm
    from src.comprendre.escalade import classer

    def evaluer(test: list[tuple[str, str]], par_famille: bool) -> tuple[float | None, list[float]]:
        latences, corrects = [], 0
        for phrase, vraie in test:
            debut = perf_counter()
            predite, _ = classer(phrase, modele)
            latences.append((perf_counter() - debut) * 1000)
            if predite is not None:
                corrects += (famille_de(predite) == famille_de(vraie)) if par_famille else routage_correct(predite, vraie)
        return _taux(corrects, len(test)), latences

    llm.prechauffer(modele)
    en, _ = evaluer(test_en[::PAS_ECHANTILLON_LLM], par_famille=True)
    fr, latences = evaluer(test_fr, par_famille=False)
    from eval.tableau_formulation import _tailles

    taille = _tailles().get(modele)
    return {"nom": f"LLM {modele}, sans exemple", "en_famille": en, "fr_routage": fr,
            "latence_ms": _p50(latences), "taille_octets": int(taille * 1e9) if taille else None,
            "modele": modele}


def _pct(x: float | None) -> str:
    return "---" if x is None else f"{100 * x:.1f}".replace(".", ",") + "\\,\\%"


def _taille(octets: int | None) -> str:
    if not octets:
        return "---"
    if octets < 1e6:
        return f"{octets / 1e3:.0f} Ko"
    if octets < 1e9:
        return f"{octets / 1e6:.1f} Mo".replace(".", ",")
    return f"{octets / 1e9:.2f} Go".replace(".", ",")


def _latence(ms: float | None) -> str:
    if ms is None:
        return "---"
    return "$<$ 0,1 ms" if ms < 0.1 else f"{ms:.1f} ms".replace(".", ",")


def latex(resultats: dict) -> str:
    c = resultats["configurations"]
    lignes = ["\\textit{Référence : BERT affiné (article)} & \\textit{93,7\\,\\%} & --- & --- & \\textit{0,44 Go} \\\\"]
    if "mots_cles" in c:
        m = c["mots_cles"]
        lignes.append(f"Mots-clés & --- & {_pct(m['fr_part_acceptee'])} acceptés, {_pct(m['fr_precision_acceptes'])} justes"
                      f" & {_latence(m['latence_ms'])} & {_taille(m['taille_octets'])} \\\\")
    if "tfidf" in c:
        t = c["tfidf"]
        lignes.append(f"TF-IDF + rég. logistique & {_pct(t['en_intention'])} & {_pct(t['fr_routage'])}"
                      f" & {_latence(t['latence_ms'])} & {_taille(t['taille_octets'])} \\\\")
    if "e5" in c:
        e = c["e5"]
        lignes.append(f"\\textbf{{e5-small + rég. logistique}} & \\textbf{{{_pct(e['en_intention'])}}} & "
                      f"\\textbf{{{_pct(e['fr_routage'])}}} & {_latence(e['latence_ms'])} & {_taille(e['taille_octets'])} \\\\")
    if "etage1" in c:
        g = c["etage1"]
        lignes.append(f"\\textbf{{Étage 1}} : mots-clés puis e5 ($\\tau$) & --- & {_pct(g['fr_part_acceptee'])} compris, "
                      f"{_pct(g['fr_precision_acceptes'])} justes & {_latence(g['latence_ms'])} & --- \\\\")
    llms = [v for k, v in c.items() if k.startswith("llm:")]
    for l in llms:
        if not l.get("taille_octets"):  # mesures faites avant que la taille soit relevée
            from eval.tableau_formulation import TAILLES_CONNUES

            l["taille_octets"] = int(TAILLES_CONNUES.get(l["modele"], 0) * 1e9) or None
        lignes.append(f"\\texttt{{{l['modele']}}} seul & famille {_pct(l['en_famille'])} & {_pct(l['fr_routage'])}"
                      f" & {_latence(l['latence_ms'])} & {_taille(l['taille_octets'])} \\\\")
    if not llms:
        lignes.append("LLM 14B, sans exemple & \\amesurer & \\amesurer & \\amesurer & 9,1 Go \\\\")
    return (
        "\\scriptsize\n\\begin{tabularx}{\\textwidth}{@{}Y c c c c@{}}\n\\toprule\n"
        "\\textbf{Configuration} & \\textbf{Anglais (intention, 77)} & \\textbf{Français (routage)} & "
        "\\textbf{Latence p50} & \\textbf{Taille} \\\\\n\\midrule\n" + "\n".join(lignes) +
        "\n\\bottomrule\n\\end{tabularx}\n\n\\smallskip\n{\\tiny Test anglais : 3\\,080 phrases Banking77 ; "
        "test français : 250 phrases écrites par l'équipe, jamais vues à l'entraînement. Routage : bonne famille "
        "pour une demande de service, bonne intention pour nos parcours. Mesuré sur "
        + resultats["machine"].replace("_", "\\_") + ".}\n"
    )


def main(arguments: list[str]) -> int:
    test_en, test_fr = lire_banking77("test"), lire_test_fr()
    resultats = json.loads(RESULTATS.read_text(encoding="utf-8")) if RESULTATS.exists() else {"configurations": {}}
    modeles = [a.split("=", 1)[1] for a in arguments if a.startswith("--llm=")]
    if modeles:
        for modele in modeles:
            resultats["configurations"][f"llm:{modele}"] = banc_llm(modele, test_en, test_fr)
    else:
        resultats["configurations"].update(
            mots_cles=banc_mots_cles(test_fr), e5=banc_e5(test_en, test_fr),
            etage1=banc_etage1(test_fr), tfidf=banc_tfidf(test_en, test_fr))
    resultats["machine"] = os.environ.get("BANC_MACHINE") or f"{platform.node()} ({platform.machine()})"
    resultats["date"] = datetime.now().isoformat(timespec="seconds")
    RESULTATS.parent.mkdir(exist_ok=True)
    RESULTATS.write_text(json.dumps(resultats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SORTIE.write_text(latex(resultats), encoding="utf-8")
    for cle, r in resultats["configurations"].items():
        print(f"{cle:28} " + "  ".join(f"{k}={v}" for k, v in r.items() if k != "nom"))
    print(f"écrit : {RESULTATS} et {SORTIE}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
