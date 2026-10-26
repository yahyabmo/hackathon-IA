"""Étage 1 de la cascade : comprendre (module de Younes).

Ordre, du moins cher au plus cher :
1. la réponse attendue : si une question est en cours, le message y répond,
   sauf s'il ouvre clairement un autre sujet ;
2. les mots-clés ;
3. le classifieur (encodeur multilingue + régression logistique), au-dessus de τ ;
4. sinon, rien : l'orchestrateur pose une question de clarification, puis escalade.
"""

from __future__ import annotations

from ..contrats import NIVEAU_REPONSE, Comprehension, EtatConversation
from ..taxonomie import famille_de
from . import classifieur, mots_cles
from .entites import extraire
from .escalade import escalader

__all__ = ["comprendre", "escalader"]


def comprendre(message: str, etat: EtatConversation) -> Comprehension:
    """Compréhension du message, compte tenu de la conversation en cours."""

    entites = extraire(message)
    par_mots_cles = mots_cles.detecter(message)
    insatisfait = "insatisfaction" in mots_cles.expressions_trouvees(message)

    nouveau_sujet = (
        par_mots_cles is not None
        and par_mots_cles.intention not in (etat.parcours, "hors_sujet")
    )
    if etat.info_attendue and etat.parcours and not nouveau_sujet:
        return Comprehension(
            famille=etat.famille or famille_de(etat.parcours), intention=etat.parcours, confiance=1.0,
            niveau=NIVEAU_REPONSE, modele="regles", entites=entites, insatisfaction=insatisfait,
        )

    if par_mots_cles is not None:
        par_mots_cles.entites = entites
        return par_mots_cles

    par_classifieur = classifieur.predire(message)
    if par_classifieur is not None and par_classifieur.confiance >= classifieur.SEUIL_TAU:
        par_classifieur.entites = entites
        par_classifieur.insatisfaction = par_classifieur.insatisfaction or insatisfait
        return par_classifieur

    return Comprehension(
        entites=entites,
        insatisfaction=insatisfait,
        alternatives=par_classifieur.alternatives if par_classifieur else [],
        modele=mots_cles.MODELE if par_classifieur is None else classifieur.MODELE,
    )
