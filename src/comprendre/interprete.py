"""Niveau 1 de l'aiguilleur : un petit LLM qui comprend un message flou, sans répondre.

Il intervient quand les règles ne concluent pas : réponse libre à une question
en attente (« oui », « je veux envoyer de l'argent »), message qui mêle une
réponse et une nouvelle demande, renvoi au contexte (« mais ma carte ? »),
confiance du classifieur sous τ.

- **RAG d'exemples** : les 8 phrases d'entraînement les plus proches (index de
  e5-small, déjà en mémoire) sont données au LLM avec leur sujet.
- **JSON imposé** : la sortie suit un schéma (sortie contrainte d'Ollama ou de
  vLLM) ; les sujets sont une liste fermée. Même un très petit modèle ne peut
  pas produire un JSON invalide ni un sujet inconnu.
- **Vérifié par le code** : la réponse extraite doit reprendre des mots du
  message, et aucun nombre absent du message n'est accepté.

Le LLM ne voit pas le profil du client et ne lui répond jamais : ce qu'il a
compris repart dans l'automate (niveau 0), qui répond avec ses gabarits.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from time import perf_counter

from .. import llm
from ..contrats import Etape
from ..converser import garde_fou
from ..taxonomie import FAMILLES, LIBELLES_FAMILLES, NOUVELLES_INTENTIONS, famille_de, representante
from ..texte import normaliser
from . import classifieur
from .escalade import _CHOIX

AUCUNE = "aucune"
NOMBRE_EXEMPLES = 8
DESCRIPTIONS = {
    "epargne_projet": "mettre de l'argent de côté, épargner",
    "credit_immobilier": "emprunter pour acheter un logement",
    "credit_conso": "crédit pour une voiture, des travaux, un achat",
    "pret_etudiant": "financer ses études",
    "faire_virement": "envoyer de l'argent à quelqu'un",
    "question_definition": "demander ce que veut dire un mot bancaire",
    "insatisfaction": "se plaindre, être mécontent",
    "hors_sujet": "salutation, remerciement ou demande sans rapport",
}
MOTS_VIDES = {"le", "la", "les", "un", "une", "des", "de", "du", "mon", "ma", "mes", "ton", "ta", "votre", "vos",
              "a", "au", "aux", "et", "pour", "c", "est", "l", "d", "je", "j", "il", "elle", "en", "sur"}
SCHEMA = {
    "type": "object",
    "properties": {
        "intentions": {"type": "array", "items": {"type": "string", "enum": [*_CHOIX, AUCUNE]}, "maxItems": 3},
        "reponse_a_la_question": {"type": "string"},
    },
    "required": ["intentions", "reponse_a_la_question"],
}
SYSTEME = (
    "Tu analyses le message d'un client de banque pour un assistant. Tu ne réponds pas au client. "
    "Rends : intentions, les sujets que le client demande dans ce message, dans l'ordre, choisis dans "
    "la liste (« aucune » s'il ne demande rien de nouveau) ; reponse_a_la_question, si une question est "
    "en attente, les mots du message qui y répondent, sinon une chaîne vide."
)


def _libelle(choix: str) -> str:
    return DESCRIPTIONS.get(choix) or LIBELLES_FAMILLES.get(choix, choix)


def _choix_de(intention: str) -> str:
    return intention if intention in NOUVELLES_INTENTIONS else famille_de(intention)


def _intention_de(choix: str) -> str | None:
    if choix in NOUVELLES_INTENTIONS:
        return choix
    if choix in FAMILLES:
        return representante(choix)
    return None


@dataclass
class Interpretation:
    intentions: list[str] = field(default_factory=list)  # intentions de la taxonomie, dans l'ordre
    reponse: str | None = None  # les mots du message qui répondent à la question en attente
    valide: bool = False
    raison: str = ""
    etape: Etape | None = None
    exemples: list[tuple[str, str]] = field(default_factory=list)


def consigne(message: str, contexte: dict[str, str | None], exemples: list[tuple[str, str]]) -> str:
    lignes = ["Sujets possibles : " + " ; ".join(f"{c} ({_libelle(c)})" for c in _CHOIX) + f" ; {AUCUNE}."]
    lignes.append("Contexte : sujet en cours : " + (contexte.get("sujet") or "aucun")
                  + " ; question en attente : " + (f"« {contexte['question']} »" if contexte.get("question") else "aucune")
                  + " ; déjà traité : " + (contexte.get("traite") or "rien") + ".")
    if exemples:
        lignes.append("Messages proches déjà classés :")
        lignes += [f"- « {texte} » → {_choix_de(intention)}" for texte, intention in exemples]
    lignes.append(f"Message du client : « {message} »")
    return "\n".join(lignes)


def _reponse_fidele(reponse: str, message: str) -> bool:
    """La réponse extraite reprend des mots du message, sans nombre inventé."""

    mots = [m for m in normaliser(reponse).split() if m not in MOTS_VIDES]
    texte = normaliser(message)
    if not mots or not all(m in texte.split() for m in mots):
        return False
    return set(garde_fou.nombres(reponse)) <= set(garde_fou.nombres(message))


def lire(sortie: str, message: str) -> Interpretation:
    """Vérifie la sortie du LLM et la traduit en intentions de la taxonomie."""

    try:
        donnees = json.loads(sortie)
        choix = donnees["intentions"]
        reponse = str(donnees.get("reponse_a_la_question") or "").strip()
    except (ValueError, KeyError, TypeError):
        return Interpretation(raison="sortie illisible")
    intentions: list[str] = []
    for c in choix if isinstance(choix, list) else []:
        intention = _intention_de(str(c))
        if intention and intention not in intentions:
            intentions.append(intention)
    reponse_ok = reponse if reponse and _reponse_fidele(reponse, message) else None
    raison = "compris" if intentions or reponse_ok else "rien de net"
    if reponse and not reponse_ok:
        raison += " (réponse écartée : absente du message)"
    return Interpretation(intentions=intentions, reponse=reponse_ok, valide=bool(intentions or reponse_ok),
                          raison=raison)


def interpreter(message: str, contexte: dict[str, str | None], modele: str | None = None,
                avec_exemples: bool = True) -> Interpretation:
    """Un appel au petit LLM, JSON imposé ; ``valide`` faux si rien d'exploitable."""

    modele = modele or llm.MODELE_NIVEAU1
    exemples = classifieur.exemples_proches(message, NOMBRE_EXEMPLES) if avec_exemples else []
    debut = perf_counter()
    etape = Etape(nom="interpreter", modele=modele, appel_llm=True)
    try:
        sortie, etape.tokens = llm.generer(modele, SYSTEME, consigne(message, contexte, exemples),
                                           max_tokens=120, role="niveau1", schema=SCHEMA, delai=30)
        resultat = lire(sortie, message)
    except (OSError, KeyError, ValueError) as erreur:
        resultat = Interpretation(raison=f"LLM injoignable ({type(erreur).__name__})")
    etape.latence_ms = (perf_counter() - debut) * 1000
    resultat.etape, resultat.exemples = etape, exemples
    return resultat
