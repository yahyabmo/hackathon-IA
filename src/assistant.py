"""Point d'entrée unique de l'assistant : un tour de conversation, la cascade.

comprendre → (clarifier, puis escalader) → converser → conseiller → formuler

Chaque étage ne passe la main au suivant que s'il ne sait pas faire lui-même.
Dans le cas normal, un tour fait au plus un appel au LLM, à la fin (formuler) ;
l'escalade est l'exception, comptée dans la trace. Le chatbot ne possède aucun
accès bancaire et guide les demandes sensibles vers le canal approprié.

Les barrières métier de M3 (montant ambigu, information manquante pour un
conseil) produisent des décisions comme les autres : tout tour sort par
``formuler()``, avec sa trace et le mode « mots simples ».
"""

from __future__ import annotations

from . import incompris
from .comprendre import comprendre, escalader
from .conseiller import clients, conseiller
from .conseiller import integration as m3
from .contrats import NIVEAU_REPONSE, Comprehension, Conseil, EtatConversation, Etape, Reponse
from .converser import Decision, avancer, formuler
from .converser.formuler import question_clarification
from .mesure import mesurer

# Informations de la question M3 qui complètent le profil plutôt que le projet.
CHAMPS_PROFIL = {"age": "age", "est_etudiant": "est_etudiant", "ages_enfants": "enfants"}


def decision_conseil(etat: EtatConversation) -> Decision:
    """La décision de conseil d'un parcours (publique : le banc de formulation la réutilise)."""

    credit = etat.famille == "credit"
    return Decision("conseil", parcours=etat.parcours, mention_legale="credit" if credit else None,
                    proposer="transmettre_conseiller" if credit else None)


def _reprendre_question_m3(message: str, etat: EtatConversation, profil: dict) -> Decision:
    """Réponse à l'information qu'un conseil attendait (``Conseil.manque``)."""

    champ = etat.question_m3
    if m3.confirmation(message) is False and champ not in ("est_etudiant", "besoin_liquidite"):
        etat.question_m3 = etat.info_attendue = etat.parcours = None
        etat.slots = {}
        return Decision("abandon")
    valeur = m3.lire_reponse(champ, message)
    if valeur is None:
        return Decision("question_m3", parcours=etat.parcours, info=champ, relance="incompris")
    if champ in CHAMPS_PROFIL:
        profil[CHAMPS_PROFIL[champ]] = valeur
    else:
        etat.slots[champ] = valeur
    etat.question_m3 = etat.info_attendue = None
    return decision_conseil(etat)


def reply(
    message: str, client_id: str, etat: EtatConversation | None = None
) -> tuple[Reponse, EtatConversation]:
    """Traite un message du client et rend la réponse, avec l'état mis à jour."""

    etat = etat if etat is not None else EtatConversation()
    if etat.client_id is not None and etat.client_id != client_id:
        etat = EtatConversation(mots_simples=etat.mots_simples)
    if etat.profil_simule is None:
        etat.profil_simule = clients.profil(client_id)
    etat.client_id = client_id
    profil = etat.profil_simule  # copie de session : le contexte client y persiste
    etat.historique.append({"role": "user", "content": message})
    trace: list[Etape] = []
    comprehension = Comprehension()
    conseil: Conseil | None = None
    escalade = False
    decision: Decision | None = None

    # 0. Barrière de saisie : M1 perd certains nombres mal formés.
    if m3.montant_ambigu(message):
        decision = Decision("montant_ambigu")
    elif etat.question_m3:
        decision = _reprendre_question_m3(message, etat, profil)

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
                decision = Decision("clarifier", question=question_clarification(comprehension.alternatives))
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

    # 2. Converser. Une demande sensible devient un guidage sans accès au compte.
    if decision is None:
        etat.clarification_demandee = False
        decision, etape = mesurer("converser", lambda: avancer(message, comprehension, etat, profil),
                                  modele="automate")
        trace.append(etape)
        if decision.type == "transmettre":
            decision = Decision("orienter", parcours=etat.parcours, accroche=decision.accroche)

    # 3. Conseiller ; s'il manque une information indispensable, on la demande.
    if decision.type == "conseil":
        conseil, etape = mesurer("conseiller", lambda: conseiller(etat.parcours, profil, etat.slots),
                                 modele="regles")
        trace.append(etape)
        if conseil.manque:
            etat.question_m3 = conseil.manque[0]
            decision = Decision("question_m3", parcours=etat.parcours, info=etat.question_m3)


    # 5. Formuler : le seul appel LLM du tour, et seulement pour un conseil complet.
    texte, etape = formuler(decision, conseil, profil, etat, message)
    trace.append(etape)

    etat.derniere_reponse = texte
    etat.historique.append({"role": "assistant", "content": texte})
    reponse = Reponse(
        texte=texte, comprehension=comprehension, conseil=conseil,
        question=decision.info if decision.type in ("question", "question_m3") else None,
        escalade=escalade, trace=trace,
    )
    return reponse, etat
