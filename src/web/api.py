"""API web de l'assistant : une page de chat (style Timso AI) interroge cette API.

Chaque message part en POST ; l'aiguilleur choisit le niveau ; l'API renvoie la
réponse avec tout ce qui l'explique : niveau et raison, chaîne des niveaux de la
conversation, compréhension, conseil (proposés, écartés, hypothèses), passages
du RAG avec leur score, étapes mesurées et énergie estimée.

Lancement : ``python -m src.web`` (port 8000), puis http://localhost:8000.
Les conversations sont gardées en mémoire, par identifiant de session.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .. import llm, rag
from ..assistant import reply
from ..comprendre import classifieur
from ..conseiller import clients
from ..contrats import EtatConversation, Reponse
from ..converser.formuler import nom_produit

STATIC = Path(__file__).resolve().parent / "static"
MESURES_ABC = Path(__file__).resolve().parents[2] / "eval" / "resultats" / "abc.json"
CHAMPS_PROFIL = (("age", "Âge"), ("metier", "Métier"), ("situation", "Situation"), ("revenus_nets", "Revenus nets / mois"),
                 ("epargne", "Épargne"), ("solde", "Solde"), ("mensualites_credits", "Crédits en cours / mois"))
EXEMPLES = {
    "C01": ["J'ai perdu ma carte et je veux faire un virement.", "mon père", "Je peux retirer de mon PEL avant 4 ans ?",
            "100000000", "mais ma carte ?", "Ma carte ne marche plus au distributeur"],
    "C02": ["Pourquoi j'ai payé 8 € de frais ce mois-ci ?", "Comment je fais une réclamation ?"],
    "C03": ["Je voudrais mettre de côté pour mes enfants.", "Dans 10 ans, 100 euros par mois",
            "Quelle est la différence entre le LDDS et le Livret A ?"],
    "C04": ["Je dois envoyer 500 € à mon fils.", "oui", "Pourquoi vous ne pouvez pas faire le virement vous-même ?"],
    "C05": ["Je veux un crédit pour acheter une voiture.", "12000", "48 mois", "pourquoi ?"],
    "C06": ["Votre appli ne marche jamais !", "Comment je fais une réclamation ?"],
    "C07": ["Je veux acheter un appartement", "Autour de 250 000, et je peux mettre les 25 000",
            "Et avec un bien à 200 000 ?", "pourquoi ?", "Combien de frais de notaire pour un appartement ancien ?"],
    "C08": ["Je voudrais mettre de côté", "Dans 2 ans", "50 euros", "C'est quoi le TEAG ?",
            "Je voudrais un prêt étudiant", "5000"],
}

app = FastAPI(title="Assistant bancaire frugal")
SESSIONS: dict[str, EtatConversation] = {}


class Message(BaseModel):
    session: str
    client_id: str
    message: str
    mots_simples: bool = False
    llm_actif: bool | None = None
    niveau_force: int | None = None


class Session(BaseModel):
    session: str


def _cout_par_niveau() -> dict[int, float] | None:
    """Énergie par message (Wh), tirée du banc A/B/C : sans LLM, et par appel au LLM."""

    try:
        configurations = json.loads(MESURES_ABC.read_text(encoding="utf-8"))["configurations"]
        c = configurations["C"]
        b = configurations.get("B") or configurations["B_reformulation"]  # coût d'un appel au petit LLM
    except (OSError, KeyError, ValueError):
        return None
    sans_llm = c["wh_par_1000"] / 1000
    par_appel = max(0.0, (b["wh_par_1000"] - c["wh_par_1000"]) / 1000 / max(1e-6, 1 - b["sans_llm"]))
    return {0: sans_llm, 1: sans_llm + par_appel, 2: sans_llm + par_appel}


def serialiser(reponse: Reponse, etat: EtatConversation) -> dict[str, Any]:
    c, conseil = reponse.comprehension, reponse.conseil
    couts = _cout_par_niveau()
    energie = None
    if couts is not None:
        energie = couts[0] + (couts[1] - couts[0]) * reponse.appels_llm
    return {
        "texte": reponse.texte,
        "niveau": reponse.niveau,
        "raison": reponse.raison_niveau,
        "chaine": etat.niveaux,
        "question": reponse.question,
        "comprehension": {
            "intention": c.intention, "famille": c.famille, "niveau": c.niveau, "modele": c.modele,
            "confiance": round(c.confiance, 3), "tau": classifieur.SEUIL_TAU, "exemple_proche": c.exemple_proche,
            "alternatives": [{"famille": a.famille, "confiance": round(a.confiance, 3)} for a in c.alternatives],
            "autres": c.autres_intentions,
        },
        "conseil": None if conseil is None else {
            "propositions": [{"nom": nom_produit(p.produit_id), "raisons": p.raisons,
                              "sources": list(dict.fromkeys(p.sources))} for p in conseil.propositions],
            "ecartees": [{"nom": nom_produit(e.produit_id), "raison": e.raison, "regle": e.regle}
                         for e in conseil.ecartees],
            "alertes": conseil.alertes,
            "hypotheses": conseil.faits.get("hypotheses", []),
        },
        "sources": [{"n": n, "titre": s["titre"], "texte": s["texte"], "source": s["source"], "date": s.get("date", ""),
                     "score": s["score"]} for n, s in enumerate(reponse.sources, start=1)],
        "trace": [{"nom": e.nom, "modele": e.modele, "latence_ms": round(e.latence_ms, 2), "tokens": e.tokens,
                   "appel_llm": e.appel_llm} for e in reponse.trace],
        "latence_ms": round(sum(e.latence_ms for e in reponse.trace), 1),
        "tokens": sum(e.tokens for e in reponse.trace),
        "appels_llm": reponse.appels_llm,
        "energie_wh": energie,
        "file": etat.file_demandes,
    }


@app.get("/")
def page() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@app.get("/api/config")
def config() -> dict[str, Any]:
    liste = []
    for client_id, _ in clients.lister():
        p = clients.profil(client_id)
        liste.append({"id": client_id, "libelle": f"{p.get('prenom', client_id)}, {p.get('age', '?')} ans — {p.get('metier', '')}"})
    return {
        "clients": liste,
        "exemples": EXEMPLES,
        "llm": {"actif": llm.actif(), "joignable": llm.joignable("niveau1"),
                "niveau1": llm.MODELE_NIVEAU1, "niveau2": llm.MODELE_NIVEAU2},
        "classifieur": {"disponible": classifieur.disponible(), "tau": classifieur.SEUIL_TAU},
        "rag": {"fiches": len(rag.fiches()), "disponible": rag.disponible()},
        "mesures": _cout_par_niveau() is not None,
    }


@app.get("/api/profil/{client_id}")
def profil(client_id: str) -> dict[str, Any]:
    p = clients.profil(client_id)
    champs = [{"libelle": libelle, "valeur": p.get(cle), "simule": clients.est_simule(p, cle)}
              for cle, libelle in CHAMPS_PROFIL]
    return {"id": client_id, "prenom": p.get("prenom"), "champs": champs}


@app.post("/api/message")
def message(demande: Message) -> dict[str, Any]:
    etat = SESSIONS.get(demande.session) or EtatConversation()
    etat.mots_simples, etat.llm_actif, etat.niveau_force = demande.mots_simples, demande.llm_actif, demande.niveau_force
    reponse, etat = reply(demande.message, demande.client_id, etat)
    SESSIONS[demande.session] = etat
    return serialiser(reponse, etat)


@app.post("/api/nouvelle")
def nouvelle(demande: Session) -> dict[str, bool]:
    SESSIONS.pop(demande.session, None)
    return {"ok": True}
