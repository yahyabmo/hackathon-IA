"""Niveau 2 de l'aiguilleur : répondre à une question ouverte depuis nos fiches (RAG).

1. Les fiches : une par produit du catalogue, une par paramètre réglementaire,
   une par terme du glossaire, plus quelques fiches écrites à la main
   (``data/processed/fiches.yaml``). Chacune garde sa source et sa date.
2. L'index : le même encodeur que le classifieur (``multilingual-e5-small``,
   préfixe ``passage:``), calculé une fois, en mémoire. Aucun modèle en plus.
3. La recherche : les 3 passages les plus proches de la question ; sous le seuil
   de pertinence, on ne répond pas (« je n'ai pas cette information »).
4. La rédaction : un LLM, une fois, à la fin, qui ne s'appuie que sur les
   passages et les cite [1] [2]. Garde-fou : aucun chiffre absent des passages,
   aucune formule interdite, au moins une citation. Sinon, ou sans LLM, le repli
   affiche l'extrait de la meilleure fiche, avec sa source.

Les chiffres restent ceux du catalogue : le LLM ne calcule rien.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from time import perf_counter
from typing import Any

import yaml

from . import llm
from .comprendre import classifieur
from .conseiller import catalogue as cat
from .contrats import Etape
from .converser import garde_fou
from .converser.glossaire import _fiches as fiches_glossaire
from .texte import contient, euros, normaliser

FICHES_MAIN = Path(__file__).resolve().parents[1] / "data" / "processed" / "fiches.yaml"
PREFIXE_PASSAGE = "passage: "
NOMBRE_PASSAGES = 3
SEUIL_PERTINENCE = 0.82  # cosinus e5 ; fixé sur le banc du niveau 2
BONUS_LEXICAL = 0.02  # par mot du sujet de la fiche cité dans la question (au plus deux) : recherche hybride
BONUS_CHIFFRE = 0.015  # une question chiffrée (« combien », « plafond ») préfère une fiche qui donne le chiffre
QUESTION_CHIFFREE = ("combien", "plafond", "taux", "minimum", "maximum", "quel age", "montant", "a partir de")
LONGUEUR_MAX = 900
FIDELITE_MIN = 0.8  # part des mots de la réponse présents dans les extraits ; fixée sur des cas jugés
MOTS_VIDES = {"vous", "votre", "vos", "cette", "dans", "pour", "avec", "sans", "mais", "tandis", "plus", "tout",
              "tous", "toutes", "elle", "elles", "sont", "etre", "avoir", "fait", "peut", "pouvez", "faut", "aussi",
              "comme", "donc", "alors", "leur", "leurs", "ceux", "celle", "dont", "entre", "selon", "oui", "non",
              "bien", "tres", "avez", "etes", "sera", "cela", "ceci", "quel", "quelle", "notre", "nous", "lors",
              "avant", "apres", "depuis", "conseiller", "extraits", "extrait"}
SYSTEME_REDACTION = (
    "Tu es l'assistant d'une banque française. Réponds à la question du client en 2 à 4 phrases "
    "courtes, au vouvoiement, en reprenant au plus près les mots des extraits numérotés, et rien "
    "d'autre. Cite l'extrait utilisé entre crochets, par exemple [1]. N'ajoute aucun chiffre ni "
    "aucune affirmation (âge, impôt, condition) qui ne figure pas dans les extraits. Si les extraits "
    "ne suffisent pas, dis-le et propose un conseiller. Ne répète pas la question. Tu n'as aucun accès au "
    "compte du client."
)


def _pourcent(ratio: float) -> str:
    return f"{ratio * 100:.2f}".rstrip("0").rstrip(".").replace(".", ",") + " %"


def _sigle(nom: str) -> str | None:
    return nom[nom.index("(") + 1:nom.index(")")] if "(" in nom and ")" in nom else None


def _fiche_produit(pid: str, p: dict[str, Any]) -> dict[str, Any]:
    morceaux = [f"{p['nom']} : {p['conditions'].rstrip('.')}."]
    if p.get("plafond"):
        morceaux.append(f"Plafond des versements : {euros(p['plafond'])}.")
    if p.get("age_min") and p.get("age_max"):
        morceaux.append(f"De {p['age_min']} à {p['age_max']} ans.")
    elif p.get("age_min"):
        morceaux.append(f"À partir de {p['age_min']} ans.")
    if p.get("horizon_min_mois"):
        morceaux.append(f"Durée minimale : {p['horizon_min_mois'] // 12} ans.")
    if p.get("versement_initial_min"):
        morceaux.append(f"Versement initial minimum : {euros(p['versement_initial_min'])} ; "
                        f"versements annuels minimum : {euros(p['versement_annuel_min'])}.")
    if p.get("solde_min"):
        morceaux.append(f"Solde minimum à conserver : {euros(p['solde_min'])}.")
    if p.get("montant_min"):
        morceaux.append(f"Montant minimum : {euros(p['montant_min'])} ; durée de "
                        f"{p['duree_min_mois']} à {p['duree_max_mois']} mois.")
    mots = [normaliser(p["nom"]), normaliser(pid.replace("_", " "))]
    if _sigle(p["nom"]):
        mots.append(normaliser(_sigle(p["nom"])))
    return {"id": f"produit:{pid}", "titre": p["nom"], "texte": " ".join(morceaux),
            "source": cat.source_produit(pid), "date": p.get("releve_le", ""), "mots": mots}


def _fiches_parametres() -> list[dict[str, Any]]:
    effort, duree = cat.parametre_detail("taux_effort_max"), cat.parametre_detail("duree_max_credit_immobilier_ans")
    ci, cif = cat.parametre_detail("commission_intervention_max"), cat.parametre_detail("commission_intervention_max_fragile")
    ancien, neuf = cat.parametre_detail("frais_notaire_ancien"), cat.parametre_detail("frais_notaire_neuf")
    immo, perso = cat.parametre_detail("taux_indicatif_credit_immobilier"), cat.parametre_detail("taux_indicatif_pret_personnel")
    return [
        {"id": "regle:hcsf", "titre": "Emprunter pour un logement : durée maximale et taux d'effort (HCSF)",
         "texte": f"Pour emprunter et acheter un logement, le cadre du HCSF limite la durée du crédit immobilier à "
                  f"{duree['valeur']} ans et le taux d'effort à {_pourcent(effort['valeur'])} des revenus, assurance "
                  "comprise. La banque garde une part de flexibilité et décide après étude du dossier : aucun accord "
                  "n'est automatique.",
         "source": effort["source"], "date": effort["releve_le"],
         "mots": ["hcsf", "taux d effort", "endettement", "credit immobilier", "pret immobilier", "emprunter",
                  "duree maximale", "combien d annees"]},
        {"id": "regle:commission", "titre": "Commission d'intervention",
         "texte": "La commission d'intervention est prélevée quand la banque traite une opération qui dépasse "
                  f"votre solde ou votre découvert autorisé. Elle est plafonnée à {euros(ci['valeur'])} par opération "
                  f"et {euros(ci['par_mois'])} par mois, et à {euros(cif['valeur'])} et {euros(cif['par_mois'])} "
                  "pour la clientèle fragile.",
         "source": ci["source"], "date": ci["releve_le"],
         "mots": ["commission", "commission d intervention", "frais", "decouvert", "plafond"]},
        {"id": "regle:notaire", "titre": "Frais d'acquisition (notaire)",
         "texte": f"Les frais d'acquisition, dits frais de notaire, sont estimés à environ {_pourcent(ancien['valeur'])} "
                  f"du prix dans l'ancien et {_pourcent(neuf['valeur'])} dans le neuf ; le notaire donne le montant exact.",
         "source": ancien["source"], "date": ancien["releve_le"],
         "mots": ["frais de notaire", "notaire", "frais d acquisition", "ancien", "neuf"]},
        {"id": "regle:taux", "titre": "Taux moyen des crédits : repères de la Banque de France",
         "texte": f"Taux moyens relevés par la Banque de France : environ {_pourcent(immo['valeur'])} pour un crédit "
                  f"immobilier et {_pourcent(perso['valeur'])} pour un prêt personnel. Ce sont des moyennes, ni des "
                  "offres ni des TAEG.",
         "source": immo["source"], "date": immo["releve_le"],
         "mots": ["taux d interet", "taux moyen", "banque de france", "taux du credit", "taux actuel"]},
    ]


@lru_cache(maxsize=1)
def fiches() -> tuple[dict[str, Any], ...]:
    """Toutes les fiches : catalogue, paramètres, glossaire, fiches écrites à la main."""

    produits = cat._catalogue()["produits"]
    tout = [_fiche_produit(pid, p) for pid, p in produits.items() if pid != "rdv_conseiller"]
    tout += _fiches_parametres()
    tout += [{"id": f"glossaire:{normaliser(f['terme'])}", "titre": f["terme"], "texte": f"{f['terme']} : {f['explication']}",
              "source": "Glossaire de l'équipe (fiches vérifiées)", "date": "2026-10-27",
              "mots": [normaliser(t) for t in [f["terme"], *f.get("synonymes", [])]]}
             for f in fiches_glossaire()]
    for f in yaml.safe_load(FICHES_MAIN.read_text(encoding="utf-8")):
        tout.append({**f, "texte": " ".join(f["texte"].split()), "mots": [normaliser(m) for m in f.get("mots", [])]})
    return tuple(tout)


def _mots_cites(texte: str, fiche: dict[str, Any]) -> int:
    return sum(1 for m in fiche["mots"] if m and contient(texte, m))


def vocabulaire_cite(message: str) -> list[str]:
    """Les fiches dont le message nomme le sujet (produit, terme, règle) : un signal du niveau 2."""

    texte = normaliser(message)
    return [f["id"] for f in fiches() if _mots_cites(texte, f)]


@lru_cache(maxsize=1)
def _index() -> Any | None:
    """Vecteurs des fiches (torch), ou None si l'encodeur n'est pas disponible."""

    charge = classifieur._charger()
    if charge is None:
        return None
    return charge[0].encode([PREFIXE_PASSAGE + f["titre"] + " : " + f["texte"] for f in fiches()],
                            normalize_embeddings=True, convert_to_tensor=True, show_progress_bar=False)


def disponible() -> bool:
    return _index() is not None


def _passages_explication(explication: list[str]) -> list[dict[str, Any]]:
    """Le dernier conseil en passages : d'abord ce qui n'est pas proposé (« pourquoi pas ? »)."""

    ordonnees = sorted(explication, key=lambda phrase: "n'est pas proposé" not in phrase)
    return [{"id": f"simulation:{i}", "titre": "Votre simulation", "texte": phrase,
             "source": "Calcul du prototype (règles publiques)", "date": "", "mots": [],
             "score": 1.0, "pertinence": 1.0} for i, phrase in enumerate(ordonnees)]


def rechercher(question: str, explication: list[str] | None = None,
               k: int = NOMBRE_PASSAGES) -> list[dict[str, Any]]:
    """Les k passages les plus proches, avec leur score ; l'explication du dernier conseil en plus.

    Un « pourquoi ? » sans autre mot, ou qui ne nomme aucune fiche (« pourquoi c'est refusé ? »),
    porte sur le dernier conseil : ses phrases sont les passages.
    """

    import torch

    texte = normaliser(question)
    if explication and (len(texte.split()) <= 3 or (texte.startswith("pourquoi") and not vocabulaire_cite(question))):
        return _passages_explication(explication)[:k]

    index = _index()
    if index is None:
        return []
    candidates, vecteurs = list(fiches()), index
    if explication:
        encodeur = classifieur._charger()[0]
        extra = [{"id": f"simulation:{i}", "titre": "Votre simulation", "texte": phrase,
                  "source": "Calcul du prototype (règles publiques)", "date": "", "mots": []}
                 for i, phrase in enumerate(explication)]
        candidates += extra
        vecteurs = torch.cat([index, encodeur.encode([PREFIXE_PASSAGE + e["texte"] for e in extra],
                                                     normalize_embeddings=True, convert_to_tensor=True,
                                                     show_progress_bar=False)])
    q = classifieur._encoder(question)
    pertinences = (vecteurs @ q).tolist()  # cosinus seul : c'est lui qui décide si une fiche répond
    scores = list(pertinences)  # avec les bonus : seulement pour classer les fiches entre elles
    texte = normaliser(question)
    chiffree = any(contient(texte, m) for m in QUESTION_CHIFFREE)
    for i, candidate in enumerate(candidates):
        scores[i] += BONUS_LEXICAL * min(2, _mots_cites(texte, candidate))
        if chiffree and any(c.isdigit() for c in candidate["texte"]):
            scores[i] += BONUS_CHIFFRE
    meilleurs = sorted(range(len(candidates)), key=lambda i: -scores[i])[:k]
    return [{**candidates[i], "score": round(scores[i], 3), "pertinence": round(pertinences[i], 3)}
            for i in meilleurs]


@dataclass
class ReponseRag:
    texte: str
    sources: list[dict[str, Any]] = field(default_factory=list)
    etapes: list[Etape] = field(default_factory=list)
    repli: str | None = None  # None si le LLM a rédigé ; sinon la raison du repli
    pertinent: bool = True


def _sources_affichees(passages: list[dict[str, Any]]) -> str:
    return "Sources : " + " ; ".join(
        f"[{n}] {p['titre']} ({p['source']}{', ' + p['date'] if p.get('date') else ''})"
        for n, p in enumerate(passages, start=1))


def _consigne(question: str, passages: list[dict[str, Any]]) -> str:
    extraits = "\n".join(f"[{n}] {p['titre']} : {p['texte']}" for n, p in enumerate(passages, start=1))
    return f"Extraits :\n{extraits}\n\nQuestion du client : {question}"


def _racines(texte: str) -> set[str]:
    return {m[:6] for m in normaliser(texte).split() if len(m) >= 4 and m not in MOTS_VIDES}


def fidelite(texte: str, passages: list[dict[str, Any]], question: str) -> float:
    """Part des mots de la réponse qui figurent dans les extraits ou la question.

    Une affirmation inventée (« le LDDS est imposable ») apporte des mots absents des extraits.
    """

    mots = _racines(texte)
    if not mots:
        return 1.0
    base = _racines(question)
    for p in passages:
        base |= _racines(p["titre"] + " " + p["texte"])
    return 1 - len(mots - base) / len(mots)


def verifier(texte: str, passages: list[dict[str, Any]], question: str) -> list[str]:
    """Le garde-fou du niveau 2 : chiffres des passages seulement, fidélité, formules, citation, longueur."""

    autorises = set(garde_fou.nombres(question))
    for p in passages:
        autorises |= set(garde_fou.nombres(p["texte"]))
    autorises |= set(range(1, len(passages) + 1))  # les numéros des citations
    problemes = garde_fou.verifier(texte, autorises, longueur_min=40, longueur_max=LONGUEUR_MAX)
    if "[" not in texte:
        problemes.append("aucune citation")
    if fidelite(texte, passages, question) < FIDELITE_MIN:
        problemes.append("affirmations absentes des extraits")
    return problemes


def _extraits_de_repli(question: str, passages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """La meilleure fiche, et une seconde si la question en nomme deux (« LDDS et Livret A »)."""

    cites = set(vocabulaire_cite(question))
    second = next((p for p in passages[1:] if p["id"] in cites and p["id"].split(":")[0] == "produit"
                   and passages[0]["id"].split(":")[0] == "produit"), None)
    return [passages[0], second] if second else [passages[0]]


def repondre(question: str, explication: list[str] | None = None, avec_llm: bool = True,
             modele: str | None = None) -> ReponseRag:
    """Recherche, puis rédaction sous garde-fou, ou repli sur l'extrait de la meilleure fiche."""

    debut = perf_counter()
    passages = rechercher(question, explication)
    recherche = Etape(nom="rag", modele="e5-small", latence_ms=(perf_counter() - debut) * 1000)
    if not passages or max(p["pertinence"] for p in passages) < SEUIL_PERTINENCE:
        return ReponseRag(
            texte="Je n'ai pas cette information dans mes fiches. Un conseiller peut vous répondre : prenez "
                  "rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.",
            sources=passages, etapes=[recherche], repli="aucune fiche assez proche", pertinent=False)

    modele = modele or llm.MODELE_NIVEAU2
    if avec_llm:
        debut = perf_counter()
        etape = Etape(nom="rediger", modele=modele, appel_llm=True)
        try:
            texte, etape.tokens = llm.generer(modele, SYSTEME_REDACTION, _consigne(question, passages),
                                              max_tokens=260, role="niveau2", delai=llm.DELAI_NIVEAU2)
            texte = texte.strip().strip('"').strip()
            if normaliser(texte).startswith(normaliser(question)):  # l'écho de la question, retiré
                texte = texte[len(question):].lstrip(" ?[]0123456789").strip()
            problemes = verifier(texte, passages, question)
            if problemes == ["aucune citation"]:  # fidèle, mais sans [1] : on cite la meilleure fiche
                texte, problemes = texte.rstrip() + " [1]", []
        except (OSError, KeyError, ValueError) as erreur:
            texte, problemes = "", [f"LLM injoignable ({type(erreur).__name__})"]
        etape.latence_ms = (perf_counter() - debut) * 1000
        if not problemes:
            return ReponseRag(texte=f"{texte}\n\n{_sources_affichees(passages)}", sources=passages,
                              etapes=[recherche, etape])
        etape.modele = f"{modele} (refusé : {problemes[0]})"
        repli, etapes = "garde-fou : " + "; ".join(problemes), [recherche, etape]
    else:
        repli, etapes = "LLM désactivé", [recherche]
    retenus = _extraits_de_repli(question, passages)
    extraits = " ".join(f"{p['texte']} [{n}]" for n, p in enumerate(retenus, start=1))
    origine = "votre simulation" if retenus[0]["id"].startswith("simulation:") else "nos fiches"
    texte = (f"D'après {origine} : {extraits}\n\nPour votre situation précise, un conseiller peut "
             f"vous répondre.\n\n{_sources_affichees(retenus)}")
    return ReponseRag(texte=texte, sources=passages, etapes=etapes, repli=repli)
