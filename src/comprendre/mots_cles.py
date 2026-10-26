"""Premier filtre de l'étage 1 : les mots-clés.

Presque gratuit, il ne conclut que s'il est sûr : une seule intention touchée,
et soit une phrase courte, soit plusieurs expressions trouvées. Un seul mot-clé
perdu dans une longue phrase ne suffit pas : le message passe au classifieur.

Lexique v0, à compléter par M1 à partir des mots les plus discriminants des
données ; une expression n'y reste que si sa précision mesurée sur la
validation dépasse 97 %. Les expressions sont écrites normalisées (sans
accents ni ponctuation).
"""

from __future__ import annotations

from ..contrats import NIVEAU_MOTS_CLES, Comprehension
from ..taxonomie import famille_de
from ..texte import contient, normaliser

MODELE = "lexique-v0"
MOTS_MAX_PHRASE_COURTE = 12

LEXIQUE: dict[str, tuple[str, ...]] = {
    "lost_or_stolen_card": (
        "perdu ma carte", "perdu ma cb", "carte perdue", "cb perdue", "perdu mon portefeuille",
        "carte est perdue", "carte a ete perdue", "vole ma carte", "vole ma cb", "carte volee",
        "cb volee", "carte est volee", "carte a ete volee", "on m a vole", "faire opposition",
    ),
    "extra_charge_on_statement": (
        "de frais", "des frais", "ces frais", "frais bancaires", "commission d intervention", "agios",
    ),
    "faire_virement": (
        "faire un virement", "envoyer", "virer de l argent", "transferer de l argent",
    ),
    "epargne_projet": (
        "mettre de cote", "epargner", "economiser", "placer de l argent", "ouvrir un livret",
    ),
    "credit_immobilier": (
        "acheter un appartement", "acheter une maison", "acheter un logement",
        "achat immobilier", "pret immobilier", "credit immobilier",
    ),
    "credit_conso": (
        "acheter une voiture", "credit auto", "credit pour une voiture", "pret auto",
        "pret personnel", "credit conso", "credit a la consommation",
    ),
    "pret_etudiant": ("pret etudiant", "credit etudiant", "financer mes etudes"),
    "question_definition": (
        "c est quoi", "ca veut dire quoi", "que veut dire", "que signifie", "qu est ce qu un",
        "qu est ce qu une", "qu est ce que",
    ),
    "insatisfaction": (
        "ne marche jamais", "marche jamais", "j en ai marre", "ras le bol", "inadmissible",
        "scandaleux", "c est nul", "toujours en panne", "pas normal",
    ),
    "hors_sujet": ("bonjour", "bonsoir", "salut", "merci", "au revoir"),
}

# Les salutations ne comptent que si rien d'autre n'est trouvé :
# « Bonjour, j'ai perdu ma carte » est une carte perdue.
_POLITESSE = "hors_sujet"


def expressions_trouvees(message: str) -> dict[str, list[str]]:
    """Expressions du lexique présentes dans le message, par intention."""

    texte = normaliser(message)
    trouvees = {
        intention: [e for e in expressions if contient(texte, e)]
        for intention, expressions in LEXIQUE.items()
    }
    trouvees = {i: e for i, e in trouvees.items() if e}
    if len(trouvees) > 1:
        trouvees.pop(_POLITESSE, None)
    return trouvees


def detecter(message: str) -> Comprehension | None:
    """Une compréhension si le filtre est sûr de lui, sinon ``None``."""

    trouvees = expressions_trouvees(message)
    if len(trouvees) != 1:
        return None
    intention, expressions = next(iter(trouvees.items()))
    phrase_courte = len(normaliser(message).split()) <= MOTS_MAX_PHRASE_COURTE
    if not phrase_courte and len(expressions) < 2:
        return None
    return Comprehension(
        famille=famille_de(intention),
        intention=intention,
        confiance=0.95 if len(expressions) >= 2 else 0.9,
        niveau=NIVEAU_MOTS_CLES,
        modele=MODELE,
        insatisfaction=intention == "insatisfaction",
    )
