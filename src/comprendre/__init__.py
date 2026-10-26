"""Compréhension des intentions : stub initial pour le module de Younes."""

from ..contrats import Comprehension


def comprendre(message: str) -> Comprehension:
    """Retourne une compréhension provisoire sans prétendre faire du ML.

    Cette règle minimale permet de vérifier l'intégration avant l'arrivée du
    classifieur et du modèle d'embeddings.
    """

    texte = message.lower()
    if any(mot in texte for mot in ("perdu", "volée", "volee", "carte")):
        return Comprehension(
            famille="carte",
            intention="carte_perdue",
            confiance=0.55,
            modele="stub-keywords",
            exemple_proche="Ma carte est perdue.",
        )
    if any(mot in texte for mot in ("bonjour", "salut")):
        return Comprehension(
            famille="accueil",
            intention="salutation",
            confiance=0.9,
            modele="stub-keywords",
        )
    return Comprehension(modele="stub-keywords")
