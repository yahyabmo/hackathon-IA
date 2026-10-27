"""Rejoue les scénarios YAML de bout en bout et vérifie leurs attentes.

Usage, depuis la racine du dépôt : ``python -m eval.run_scenarios``

Un scénario est une conversation avec un client de démonstration. Pour chaque
tour : ce qui est attendu (intention, niveau, information demandée, produits
proposés ou écartés, texte) et ce qui est interdit (redemander une information
connue, proposer un produit). Le chatbot reste sans accès au compte et sans
effet de bord.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

from src.assistant import reply
from src.contrats import EtatConversation, Reponse

DOSSIER = Path(__file__).resolve().parent / "scenarios"


def _ids(liste) -> list[str]:
    return [element.produit_id for element in liste]


def verifier_tour(reponse: Reponse, etat: EtatConversation, attendu: dict[str, Any],
                  interdit: dict[str, Any]) -> list[str]:
    """Écarts entre la réponse et les attentes du tour ; vide si tout va bien."""

    erreurs: list[str] = []
    c, conseil = reponse.comprehension, reponse.conseil
    proposes = _ids(conseil.propositions) if conseil else []
    ecartes = _ids(conseil.ecartees) if conseil else []

    def attendre(cle: str, obtenu: Any) -> None:
        if cle in attendu and obtenu != attendu[cle]:
            erreurs.append(f"{cle} : attendu {attendu[cle]!r}, obtenu {obtenu!r}")

    attendre("intention", c.intention)
    attendre("famille", c.famille)
    attendre("aiguillage", reponse.niveau)
    attendre("niveau", c.niveau)
    attendre("demande", reponse.question)
    attendre("escalade", reponse.escalade)
    # Le kick-off demande un guidage ; aucune action bancaire n'est exécutée.
    for produit, statut in attendu.get("eligibilite", {}).items():
        if not conseil or conseil.faits.get("eligibilite", {}).get(produit) != statut:
            erreurs.append(f"éligibilité inattendue : {produit}")
    erreurs += [f"produit non proposé : {p}" for p in attendu.get("propose", []) if p not in proposes]
    erreurs += [f"produit non écarté : {p}" for p in attendu.get("ecarte", []) if p not in ecartes]
    if "alerte" in attendu and not any(attendu["alerte"] in a for a in (conseil.alertes if conseil else [])):
        erreurs.append(f"alerte absente : {attendu['alerte']}")
    if "texte_contient" in attendu and attendu["texte_contient"].lower() not in reponse.texte.lower().replace(" ", " ").replace(" ", " "):
        erreurs.append(f"texte sans « {attendu['texte_contient']} »")

    erreurs += [f"information redemandée : {d}" for d in interdit.get("demande", []) if reponse.question == d]
    erreurs += [f"produit interdit proposé : {p}" for p in interdit.get("propose", []) if p in proposes]

    if reponse.appels_llm > (1 if not reponse.escalade else 2):
        erreurs.append(f"{reponse.appels_llm} appels au LLM dans un tour")
    return erreurs


def rejouer(fichier: Path) -> list[str]:
    """Rejoue un scénario ; rend la liste des erreurs, préfixées par le numéro du tour."""

    scenario = yaml.safe_load(fichier.read_text(encoding="utf-8"))
    etat, erreurs = EtatConversation(), []
    for numero, tour in enumerate(scenario["tours"], start=1):
        reponse, etat = reply(tour["client"], scenario["client"], etat)
        erreurs += [f"tour {numero} — {e}" for e in
                    verifier_tour(reponse, etat, tour.get("attendu", {}), tour.get("interdit", {}))]
    return erreurs


def main() -> int:
    fichiers = sorted(DOSSIER.glob("*.yaml"))
    reussis = 0
    for fichier in fichiers:
        erreurs = rejouer(fichier)
        reussis += not erreurs
        print(f"{'OK ' if not erreurs else 'ÉCHEC'}  {fichier.stem}")
        for erreur in erreurs:
            print(f"       {erreur}")
    print(f"\n{reussis}/{len(fichiers)} scénarios réussis")
    return 0 if reussis == len(fichiers) else 1


if __name__ == "__main__":
    sys.exit(main())
