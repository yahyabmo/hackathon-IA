"""L'aiguilleur : à chaque message, le plus petit moyen qui suffit.

Il regarde cinq signaux, calculés sans LLM sur ce que l'entrée commune a déjà
produit (mots-clés, classifieur, entités, contexte de la conversation) :

1. plusieurs demandes dans le message ;
2. une confiance sous τ ;
3. une réponse attendue que les règles ne savent pas lire ;
4. un renvoi au contexte (« mais ma carte ? ») ;
5. une question ouverte sur un produit ou une règle (« je peux… », « pourquoi »).

Niveau 0 (règles) quand la demande est claire ; niveau 1 (petit LLM interprète)
pour les signaux 1 à 4 que les règles ne savent pas trancher ; niveau 2 (RAG et
LLM rédacteur) pour le signal 5. La décision est prise à chaque message : la
conversation peut passer de 1 à 2, puis à 0, puis à 2. La mémoire (parcours,
demandes en file, informations déjà données) est commune à tous les niveaux.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .contrats import NIVEAU_MOTS_CLES, NIVEAU_REPONSE, Comprehension, EtatConversation
from .converser.dialogue import parcours_disponibles
from .texte import contient, normaliser

# Ordre de traitement de plusieurs demandes dans un même message : l'urgence d'abord.
URGENCE = ("lost_or_stolen_card", "compromised_card", "card_swallowed", "lost_or_stolen_phone",
           "insatisfaction", "faire_virement", "extra_charge_on_statement", "pret_etudiant",
           "credit_conso", "credit_immobilier", "epargne_projet")
DERNIERS = ("question_definition", "hors_sujet")

# Marqueurs d'une question d'information (forts), ou qui peuvent aussi introduire une demande
# (faibles : « je peux faire un virement ? » est une demande, « je peux retirer de mon PEL ? » une question).
QUESTION_FORTE = (
    "pourquoi", "ai je le droit", "a t on le droit", "comment fonctionne", "comment ca marche", "ca marche comment",
    "a quoi sert", "quelle difference", "difference entre", "quelles sont les conditions", "quelles conditions",
    "plafond", "combien de temps", "quel delai", "quel taux", "c est combien", "combien de frais",
    "a partir de quel age", "jusqu a quel age", "qui peut", "j ai droit", "ai je droit", "droit a",
    "quel est le", "quelle est la", "minimum", "maximum", "combien rapporte", "ca rapporte", "rapporte combien",
)
QUESTION_FAIBLE = (
    "est ce que je peux", "est ce qu on peut", "est ce que je pourrais", "puis je", "peut on", "je peux",
    "je pourrais", "est il possible", "est ce possible", "comment faire pour", "comment je fais",
)
RENVOI = ("mais", "et pour", "et ma", "et mon", "et le", "et la", "au fait", "pour revenir", "et sinon")


def trier_par_urgence(intentions: list[str]) -> list[str]:
    def rang(intention: str) -> int:
        if intention in URGENCE:
            return URGENCE.index(intention)
        return len(URGENCE) + (1 + DERNIERS.index(intention) if intention in DERNIERS else 0)

    return sorted(dict.fromkeys(intentions), key=rang)


def question_ouverte(message: str) -> str | None:
    """« forte », « faible » ou None."""

    texte = normaliser(message)
    if any(contient(texte, m) for m in QUESTION_FORTE):
        return "forte"
    if any(contient(texte, m) for m in QUESTION_FAIBLE):
        return "faible"
    return None


def renvoi_au_contexte(message: str) -> bool:
    texte = normaliser(message)
    return len(texte.split()) <= 6 and any(texte.startswith(m) for m in RENVOI)


@dataclass
class Aiguillage:
    niveau: int
    raison: str
    signaux: list[int] = field(default_factory=list)


def aiguiller(message: str, comprehension: Comprehension, etat: EtatConversation, *,
              lisible: bool, sujets_cites: list[str], llm_ok: bool, rag_ok: bool) -> Aiguillage:
    """Le niveau de ce message, et pourquoi.

    ``lisible`` : les règles savent lire la réponse attendue ; ``sujets_cites`` :
    les fiches du RAG dont le message nomme le sujet ; ``llm_ok`` : le niveau 1
    est permis et joignable ; ``rag_ok`` : l'index du niveau 2 est disponible.
    """

    signaux: list[int] = []
    if comprehension.autres_intentions:
        signaux.append(1)
    if not comprehension.comprise:
        signaux.append(2)
    attente = comprehension.niveau == NIVEAU_REPONSE and etat.info_attendue
    if attente and not lisible:
        signaux.append(3)
    if renvoi_au_contexte(message) and (etat.parcours or etat.niveaux):
        signaux.append(4)
    # Une demande sûre des mots-clés ouvre son parcours guidé (« pourquoi j'ai payé 8 € de frais ? »).
    # La suite d'un parcours terminé (« et avec 1000 ? ») aussi : elle se recalcule par les règles.
    suite = comprehension.niveau == NIVEAU_REPONSE and not etat.info_attendue
    parcours_sur = ((comprehension.niveau == NIVEAU_MOTS_CLES or suite)
                    and comprehension.intention in parcours_disponibles()
                    and comprehension.intention != "question_definition")
    pourquoi_conseil = normaliser(message).startswith("pourquoi") and bool(etat.explication)
    force = question_ouverte(message)
    if not parcours_sur and ((force == "forte" and (sujets_cites or pourquoi_conseil))
                             or (force == "faible" and sujets_cites)):
        signaux.append(5)

    if 5 in signaux and rag_ok and not (attente and lisible):
        return Aiguillage(2, "question ouverte sur un sujet de nos fiches", signaux)
    if attente and lisible:
        return Aiguillage(0, "réponse attendue, lue par les règles", signaux)
    if 1 in signaux and comprehension.comprise:
        return Aiguillage(0, "plusieurs demandes nettes : traitées par ordre d'urgence", signaux)
    if comprehension.comprise and not attente and 4 not in signaux:
        return Aiguillage(0, f"demande claire ({comprehension.niveau})", signaux)
    if llm_ok and ({2, 3, 4} & set(signaux)):
        raisons = {2: "confiance sous le seuil", 3: "réponse libre, illisible par les règles",
                   4: "renvoi au contexte"}
        return Aiguillage(1, " ; ".join(raisons[s] for s in signaux if s in raisons), signaux)
    return Aiguillage(0, "règles (LLM non disponible)" if not llm_ok and signaux else "règles", signaux)
