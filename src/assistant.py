"""Point d'entrée unique de l'assistant : un tour de conversation, la cascade.

comprendre → (clarifier, puis escalader) → converser → conseiller ou agir → formuler

Chaque étage ne passe la main au suivant que s'il ne sait pas faire lui-même.
Dans le cas normal, un tour fait au plus un appel au LLM, à la fin (formuler) ;
l'escalade est l'exception, comptée dans la trace. Aucune action à effet de
bord ne part sans un « oui » explicite du client.
"""

from __future__ import annotations

from .comprendre import comprendre, escalader
from .comprendre.entites import extraire, oui_non
from .conseiller import clients, conseiller, outils
from . import incompris
from .contrats import NIVEAU_REPONSE, Action, Comprehension, Conseil, EtatConversation, Etape, Reponse
from .converser import Decision, avancer, formuler
from .mesure import mesurer

# Fiches qui se suffisent : pas de proposition de rappel derrière.
FICHES_AUTONOMES = ("question_definition", "hors_sujet")


def _executer(action: Action, profil: dict, etat: EtatConversation, trace: list[Etape]) -> Action:
    action, etape = mesurer("agir", lambda: outils.executer(action, profil, etat), modele=action.outil)
    trace.append(etape)
    return action


def _action_suivante(decision: Decision, action: Action | None) -> Action | None:
    """L'action à proposer au tour suivant (elle attendra un « oui »)."""

    if decision.type in ("action", "transmettre") and action is not None and not action.confirmee:
        return action
    if decision.type == "conseil" and decision.proposer:
        return Action(outil=decision.proposer)
    if decision.type == "orienter" or (decision.type == "fiche" and decision.parcours not in FICHES_AUTONOMES):
        return Action(outil="transmettre_conseiller")
    if (decision.type == "action_faite" and action is not None and action.outil == "expliquer_frais"
            and action.resultat and action.resultat.get("proposer_offre_fragile")):
        return Action(outil="transmettre_conseiller")
    return None


def reply(
    message: str, client_id: str, etat: EtatConversation | None = None
) -> tuple[Reponse, EtatConversation]:
    """Traite un message du client et rend la réponse, avec l'état mis à jour."""

    etat = etat if etat is not None else EtatConversation()
    profil = clients.profil(client_id)
    etat.historique.append({"role": "user", "content": message})
    trace: list[Etape] = []
    comprehension = Comprehension()
    conseil: Conseil | None = None
    action: Action | None = None
    escalade = False
    decision: Decision | None = None

    # 0. Une action attend l'accord du client.
    if etat.action_en_attente is not None:
        en_attente, etat.action_en_attente = etat.action_en_attente, None
        accord = oui_non(message)
        if accord is False and extraire(message).get("montants"):
            accord = None  # « non, plutôt 300 € » : une correction, pas un refus
        if accord is not None:
            action = en_attente
            if accord:
                action.confirmee = True
                action = _executer(action, profil, etat, trace)
                decision = Decision("action_faite", parcours=etat.parcours, outil=action.outil)
            else:
                decision = Decision("action_annulee", parcours=etat.parcours, outil=action.outil)

    # 1. Comprendre ; sinon clarifier une fois, puis escalader.
    if decision is None:
        comprehension, etape = mesurer("comprendre", lambda: comprendre(message, etat))
        etape.modele = comprehension.modele
        trace.append(etape)
        if not comprehension.comprise and etat.parcours and (
                comprehension.entites.get("montants") or comprehension.entites.get("duree_mois")):
            # « Et avec un bien à 200 000 ? » : la suite du parcours en cours.
            comprehension = Comprehension(
                famille=etat.famille or "", intention=etat.parcours, confiance=1.0,
                niveau=NIVEAU_REPONSE, modele="regles", entites=comprehension.entites)
        if not comprehension.comprise:
            if not etat.clarification_demandee:
                etat.clarification_demandee = True
                decision = Decision("clarifier")
            else:
                par_escalade, etape = escalader(message)
                if etape is not None:
                    trace.append(etape)
                    escalade = True
                if par_escalade is not None:
                    comprehension = par_escalade
                else:
                    decision = Decision("orienter")
            if decision is not None:
                incompris.noter(message, client_id, decision.type, comprehension)

    # 2 à 4. Converser, puis conseiller ou agir.
    if decision is None:
        etat.clarification_demandee = False
        decision, etape = mesurer("converser", lambda: avancer(message, comprehension, etat, profil),
                                  modele="automate")
        trace.append(etape)
        if decision.type == "conseil":
            conseil, etape = mesurer("conseiller", lambda: conseiller(etat.parcours, profil, etat.slots),
                                     modele="regles")
            trace.append(etape)
        elif decision.type in ("action", "transmettre"):
            action = Action(outil=decision.outil, parametres=dict(etat.slots))
            if not outils.demande_confirmation(action.outil):
                action = _executer(action, profil, etat, trace)
                decision = Decision("action_faite", parcours=etat.parcours, outil=action.outil)

    etat.action_en_attente = _action_suivante(decision, action)

    # 5. Formuler : le seul appel LLM du tour, et seulement pour un conseil.
    texte, etape = formuler(decision, conseil, action, profil, etat, message)
    trace.append(etape)

    etat.derniere_reponse = texte
    etat.historique.append({"role": "assistant", "content": texte})
    reponse = Reponse(
        texte=texte, comprehension=comprehension, conseil=conseil, action=action,
        question=decision.info if decision.type == "question" else None,
        escalade=escalade, trace=trace,
    )
    return reponse, etat
