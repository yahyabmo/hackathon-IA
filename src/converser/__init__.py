"""Dialogue déterministe et orchestration des parcours."""

from ..contrats import Comprehension, EtatConversation


def prochaine_etape(
    comprehension: Comprehension, etat: EtatConversation
) -> str:
    """Retourne le nom symbolique de la prochaine étape du dialogue."""

    if comprehension.intention == "carte_perdue":
        return "securiser_carte"
    if comprehension.intention == "salutation":
        return "accueillir"
    return "clarifier_intention"
