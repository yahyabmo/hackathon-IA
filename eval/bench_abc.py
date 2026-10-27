"""Banc A/B/C : réussite, énergie, latence et mémoire de trois façons de répondre.

- A : un LLM fait tout (``ministral-3:14b``) : profil, catalogue et historique
  dans la consigne, une réponse libre par message ;
- B : notre cascade : mots-clés, classifieur, automate, règles, gabarits, et un
  petit LLM pour formuler les conseils ;
- C : la cascade, gabarits seuls (aucun LLM).

Requêtes : les messages des scénarios de référence (``eval/scenarios``), rejoués
comme des conversations, en boucle jusqu'à N requêtes par lot.

Réussite : B et C par les vérifications des scénarios. A n'a pas de structure à
vérifier (ni intention, ni action, ni conseil) : ses réponses sont écrites dans
un CSV, à juger à la main.

Énergie : CodeCarbon hors ligne (pays FRA), par lots de N requêtes après une
chauffe ; la puissance de repos, mesurée au début, est soustraite :
(E − P0·t) / N, moyenne de plusieurs répétitions. Sur GPU, NVML mesure la carte ;
sans accès RAPL, le processeur est estimé par CodeCarbon (le tableau le signale).

Usage, depuis la racine du dépôt (poste à GPU, Ollama lancé) :
    python -m eval.bench_abc C B A                      # les trois, réglages du rapport
    python -m eval.bench_abc B --modele-b=qwen3:1.7b    # le modèle de formulation retenu
    python -m eval.bench_abc C --requetes=50 --repetitions=1 --repos=10   # essai rapide
Écrit ``eval/resultats/abc.json`` (les mesures s'ajoutent) et
``rapport/resultats-frugalite.tex`` (inclus par le support).
"""

from __future__ import annotations

import csv
import json
import os
import platform
import statistics
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from time import perf_counter
from typing import Any, Callable

import yaml

os.environ.setdefault("INCOMPRIS_FICHIER", str(Path(tempfile.gettempdir()) / "incompris-banc.jsonl"))

from eval.run_scenarios import DOSSIER, rejouer  # noqa: E402
from eval.tableau_formulation import _tailles  # noqa: E402
from src import llm  # noqa: E402
from src.assistant import reply  # noqa: E402
from src.comprendre import classifieur  # noqa: E402
from src.conseiller import catalogue, clients  # noqa: E402
from src.contrats import EtatConversation  # noqa: E402

RACINE = Path(__file__).resolve().parents[1]
RESULTATS = RACINE / "eval" / "resultats" / "abc.json"
TRANSCRIPTIONS_A = RACINE / "eval" / "resultats" / "abc-A-transcriptions.csv"
SORTIE = RACINE / "rapport" / "resultats-frugalite.tex"
TAILLE_ENCODEUR_GO = 0.47
REGLAGES = {"requetes": 200, "repetitions": 3, "repos": 60, "chauffe": 10}

SYSTEME_A = (
    "Tu es l'assistant d'une banque française. Réponds au client en français, au vouvoiement, en "
    "quelques phrases. Utilise uniquement son profil et le catalogue ci-dessous ; n'invente ni chiffre "
    "ni produit. Pour une demande sensible, oriente vers l'espace bancaire sécurisé.\n\n"
    "Profil du client : {profil}\n\nCatalogue : {catalogue}"
)


def conversations() -> list[tuple[str, list[str]]]:
    scenarios = [yaml.safe_load(f.read_text(encoding="utf-8")) for f in sorted(DOSSIER.glob("*.yaml"))]
    return [(s["client"], [t["client"] for t in s["tours"]]) for s in scenarios]


def _profil_court(client_id: str) -> str:
    profil = {k: v for k, v in clients.profil(client_id).items() if k not in ("provenance", "simule")}
    return json.dumps(profil, ensure_ascii=False)


def _catalogue_court() -> str:
    produits = catalogue._catalogue()["produits"]
    return json.dumps({pid: {k: p.get(k) for k in ("nom", "conditions", "plafond", "age_min", "age_max")
                             if p.get(k) is not None} for pid, p in produits.items()}, ensure_ascii=False)


def repondeur_a(modele: str) -> Callable[[str, str, list[str]], tuple[str, int]]:
    """A : le LLM reçoit tout et répond seul ; l'historique tient dans le message."""

    catalogue_texte = _catalogue_court()

    def repondre(message: str, client_id: str, historique: list[str]) -> tuple[str, int]:
        systeme = SYSTEME_A.format(profil=_profil_court(client_id), catalogue=catalogue_texte)
        conversation = "\n".join(historique + [f"Client : {message}"])
        texte, _ = llm.generer(modele, systeme, conversation, max_tokens=300, role="escalade")
        historique += [f"Client : {message}", f"Assistant : {texte}"]
        return texte, 1

    return repondre


def lot(configuration: str, n: int, modele_a: str, transcrire: list | None = None) -> dict[str, Any]:
    """N requêtes, conversations rejouées en boucle ; latences et appels au LLM."""

    latences, sans_llm, faites = [], 0, 0
    repondre_a = repondeur_a(modele_a) if configuration == "A" else None
    while faites < n:
        for client_id, messages in conversations():
            etat, historique = EtatConversation(), []
            for message in messages:
                if faites >= n:
                    break
                debut = perf_counter()
                if repondre_a:
                    texte, appels = repondre_a(message, client_id, historique)
                else:
                    reponse, etat = reply(message, client_id, etat)
                    texte, appels = reponse.texte, reponse.appels_llm
                latences.append((perf_counter() - debut) * 1000)
                sans_llm += appels == 0
                faites += 1
                if transcrire is not None:
                    transcrire.append({"client": client_id, "message": message, "reponse": texte, "juge": ""})
            if faites >= n:
                break
    return {"latences": latences, "sans_llm": sans_llm, "n": faites}


def _mesurer(fonction: Callable[[], Any]) -> tuple[float, float, Any]:
    """(énergie en Wh, durée en s, résultat), mesurés par CodeCarbon hors ligne."""

    from codecarbon import OfflineEmissionsTracker

    suivi = OfflineEmissionsTracker(country_iso_code="FRA", save_to_file=False, log_level="error",
                                    measure_power_secs=1)
    suivi.start()
    debut = perf_counter()
    resultat = fonction()
    duree = perf_counter() - debut
    suivi.stop()
    return suivi.final_emissions_data.energy_consumed * 1000, duree, resultat


def puissance_repos(secondes: int) -> float:
    energie, duree, _ = _mesurer(lambda: time.sleep(secondes))
    return energie / duree  # Wh par seconde


def reussite(configuration: str) -> str:
    if configuration == "A":
        return "à juger"
    fichiers = sorted(DOSSIER.glob("*.yaml"))
    return f"{sum(not rejouer(f) for f in fichiers)} / {len(fichiers)}"


def preparer(configuration: str, modele_b: str) -> str | None:
    """Règle l'assistant pour la configuration ; rend le modèle de formulation (B) ou None."""

    os.environ["ASSISTANT_ESCALADE"] = "0"
    if configuration == "B":
        os.environ["ASSISTANT_LLM"] = "1"
        llm.MODELE_FORMULATION = modele_b
        return modele_b
    os.environ["ASSISTANT_LLM"] = "0"
    return None


def banc(configuration: str, reglages: dict[str, int], modele_a: str, modele_b: str, p0: float) -> dict:
    modele = preparer(configuration, modele_b)
    classifieur.prechauffer()
    if configuration == "A":
        llm.prechauffer(modele_a)
    elif modele:
        llm.prechauffer(modele)
    lot(configuration, reglages["chauffe"], modele_a)
    transcriptions: list[dict] = [] if configuration == "A" else None
    mesures = []
    for repetition in range(reglages["repetitions"]):
        energie, duree, r = _mesurer(lambda: lot(configuration, reglages["requetes"], modele_a,
                                                 transcriptions if repetition == 0 else None))
        mesures.append({"energie_wh": energie, "duree_s": duree, **r})
    if transcriptions:
        with TRANSCRIPTIONS_A.open("w", newline="", encoding="utf-8") as f:
            ecrivain = csv.DictWriter(f, fieldnames=list(transcriptions[0]))
            ecrivain.writeheader()
            ecrivain.writerows(transcriptions)
    latences = sorted(l for m in mesures for l in m["latences"])
    par_requete = [(m["energie_wh"] - p0 * m["duree_s"]) / m["n"] for m in mesures]
    tailles = _tailles()
    go = {"A": tailles.get(modele_a), "B": TAILLE_ENCODEUR_GO + (tailles.get(modele_b) or 0),
          "C": TAILLE_ENCODEUR_GO}[configuration]
    return {
        "configuration": configuration, "modele": {"A": modele_a, "B": modele_b, "C": None}[configuration],
        "reussite": reussite(configuration),
        "wh_par_1000": round(max(0.0, 1000 * statistics.mean(par_requete)), 4),
        "wh_par_1000_brut": round(1000 * statistics.mean(m["energie_wh"] / m["n"] for m in mesures), 4),
        "latence_p50_ms": round(statistics.median(latences), 1),
        "latence_p95_ms": round(latences[max(0, -(-95 * len(latences) // 100) - 1)], 1),
        "go_charges": round(go, 2) if go else None,
        "sans_llm": round(sum(m["sans_llm"] for m in mesures) / sum(m["n"] for m in mesures), 3),
        "requetes": reglages["requetes"], "repetitions": reglages["repetitions"],
    }


def _nombre(x: float | None, decimales: int = 1) -> str:
    return "---" if x is None else f"{x:.{decimales}f}".replace(".", ",")


def _energie(wh: float) -> str:
    """Les gabarits coûtent si peu que deux décimales afficheraient zéro."""

    return "$<$ 0,001" if wh < 0.001 else _nombre(wh, 2 if wh >= 1 else 3)


def _lots(resultats: dict) -> str:
    """« lots de 200 requêtes × 3 (A : 40 × 1) » : les réglages réels de chaque configuration."""

    reglages = {c: (r["requetes"], r["repetitions"]) for c, r in sorted(resultats["configurations"].items())}
    if not reglages:
        return "lots de requêtes"
    courant = max(set(reglages.values()), key=list(reglages.values()).count)
    autres = [f"{c} : {n} × {k}" for c, (n, k) in reglages.items() if (n, k) != courant]
    return f"lots de {courant[0]} requêtes × {courant[1]}" + (f" ({' ; '.join(autres)})" if autres else "")


NOMS = {"A": "A --- un LLM fait tout", "B": "B --- cascade + petit LLM",
        "C": "\\textbf{C --- notre cascade, sans LLM}"}


def latex(resultats: dict) -> str:
    lignes = []
    for cle in ("A", "B", "C"):
        r = resultats["configurations"].get(cle)
        if r is None:
            lignes.append(f"{NOMS[cle]} & \\amesurer & \\amesurer & \\amesurer & --- & --- \\\\")
            continue
        modele = f" (\\texttt{{{r['modele']}}})" if r["modele"] else ""
        lignes.append(f"{NOMS[cle]}{modele} & {r['reussite']} & {_energie(r['wh_par_1000'])} & "
                      f"{_nombre(r['latence_p95_ms'], 0)} ms & {_nombre(r['go_charges'], 1)} & "
                      f"{_nombre(100 * r['sans_llm'], 0)}\\,\\% \\\\")
    return (
        "\\scriptsize\n\\begin{tabularx}{\\textwidth}{@{}Y c c c c c@{}}\n\\toprule\n"
        "\\textbf{Configuration} & \\textbf{Scénarios} & \\textbf{Wh / 1\\,000 req.} & \\textbf{Latence p95} & "
        "\\textbf{Go} & \\textbf{Sans LLM} \\\\\n\\midrule\n" + "\n".join(lignes) +
        "\n\\bottomrule\n\\end{tabularx}\n\n\\smallskip\n{\\tiny Énergie : CodeCarbon hors ligne, "
        + _lots(resultats) + " après chauffe, puissance de repos soustraite. Mesuré sur "
        + resultats["machine"].replace("_", "\\_") + ".}\n"
    )


def main(arguments: list[str]) -> int:
    reglages = dict(REGLAGES)
    modele_a, modele_b = llm.MODELE_ESCALADE, llm.MODELE_FORMULATION
    configurations = []
    for argument in arguments:
        if argument.startswith("--modele-a="):
            modele_a = argument.split("=", 1)[1]
        elif argument.startswith("--modele-b="):
            modele_b = argument.split("=", 1)[1]
        elif argument.startswith("--") and argument[2:].split("=")[0] in reglages:
            cle, valeur = argument[2:].split("=", 1)
            reglages[cle] = int(valeur)
        elif argument in ("A", "B", "C"):
            configurations.append(argument)
        else:
            print(__doc__)
            return 2
    configurations = configurations or ["C", "B", "A"]
    if any(c in ("A", "B") for c in configurations) and not llm.joignable():
        print(f"Ollama ne répond pas sur {llm.URL} : lancer « ollama serve » d'abord.")
        return 1
    resultats = json.loads(RESULTATS.read_text(encoding="utf-8")) if RESULTATS.exists() else {"configurations": {}}
    print(f"Puissance de repos sur {reglages['repos']} s…")
    p0 = puissance_repos(reglages["repos"])
    for configuration in configurations:
        print(f"Configuration {configuration}…")
        resultats["configurations"][configuration] = banc(configuration, reglages, modele_a, modele_b, p0)
        print(json.dumps(resultats["configurations"][configuration], ensure_ascii=False))
    resultats.update(machine=os.environ.get("BANC_MACHINE") or f"{platform.node()} ({platform.machine()})",
                     requetes=reglages["requetes"], date=datetime.now().isoformat(timespec="seconds"),
                     puissance_repos_w=round(p0 * 3600, 1))
    RESULTATS.parent.mkdir(exist_ok=True)
    RESULTATS.write_text(json.dumps(resultats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SORTIE.write_text(latex(resultats), encoding="utf-8")
    print(f"écrit : {RESULTATS} et {SORTIE}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
