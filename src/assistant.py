"""Point d'entrée unique de l'assistant : un tour de conversation, la cascade.

comprendre → (clarifier, puis escalader) → converser → conseiller ou agir → formuler

Chaque étage ne passe la main au suivant que s'il ne sait pas faire lui-même.
Dans le cas normal, un tour fait au plus un appel au LLM, à la fin (formuler) ;
l'escalade est l'exception, comptée dans la trace. Aucune action à effet de
bord ne part sans un « oui » explicite du client.
"""

from __future__ import annotations
from dataclasses import replace

from .comprendre import comprendre, escalader
from .comprendre.entites import extraire
from .conseiller import clients, conseiller, outils
from .conseiller import integration as m3
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
    if etat.client_id is not None and etat.client_id != client_id:
        etat = EtatConversation(mots_simples=etat.mots_simples)
    if etat.profil_simule is None:
        etat.profil_simule = clients.profil(client_id)
    etat.client_id = client_id
    profil = etat.profil_simule
    etat.historique.append({"role": "user", "content": message})
    trace: list[Etape] = []
    comprehension = Comprehension()
    conseil: Conseil | None = None
    action: Action | None = None
    escalade = False
    decision: Decision | None = None
    if m3.montant_ambigu(message):
        etat.action_en_attente = None
        return m3.directe("Montant ambigu ou négatif : aucune opération effectuée. Utilisez un montant positif avec une virgule pour les centimes, puis confirmez de nouveau.", etat)

    if etat.question_m3:
        if m3.confirmation(message) is False and etat.question_m3 not in ("est_etudiant", "besoin_liquidite"):
            etat.question_m3 = etat.info_attendue = None
            etat.parcours = None
            etat.slots = {}
            return m3.directe("D'accord, le parcours est annulé.", etat)
        champ = etat.question_m3
        valeur = m3.lire_reponse(champ, message)
        if valeur is None:
            return m3.directe(m3.question(champ), etat, question=champ)
        if champ in ("age", "est_etudiant", "ages_enfants"):
            profil["enfants" if champ == "ages_enfants" else champ] = valeur
        else:
            etat.slots[champ] = valeur
        etat.question_m3 = etat.info_attendue = None
        decision = Decision("conseil", parcours=etat.parcours,
                            mention_legale="credit" if etat.famille == "credit" else None,
                            proposer="transmettre_conseiller" if etat.famille == "credit" else None)

    # 0. Une action attend l'accord du client.
    if etat.action_en_attente is not None:
        en_attente, etat.action_en_attente = etat.action_en_attente, None
        accord = m3.confirmation(message)
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
        elif not extraire(message).get("montants"):
            # Une phrase telle que « oui, mais pas maintenant » n'est pas un accord.
            etat.action_en_attente = en_attente
            return m3.directe("Aucune opération effectuée. Confirmez la demande présentée par « oui » ou annulez par « non ».", etat, action=en_attente)
        elif en_attente.outil == "preparer_virement" and len(extraire(message)["montants"]) > 1:
            etat.action_en_attente = en_attente
            return m3.directe("Indiquez un seul montant corrigé ; une nouvelle confirmation sera demandée.", etat, action=en_attente)

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
        if decision.type in ("action", "transmettre"):
            action = Action(outil=decision.outil, parametres=dict(etat.slots))
            if not outils.demande_confirmation(action.outil):
                action = _executer(action, profil, etat, trace)
                decision = Decision("action_faite", parcours=etat.parcours, outil=action.outil)

    if decision.type == "conseil":
        conseil, etape = mesurer("conseiller", lambda: conseiller(etat.parcours, profil, etat.slots), modele="regles")
        trace.append(etape)
        if conseil.manque:
            champ = conseil.manque[0]
            etat.question_m3 = champ
            etat.action_en_attente = None
            return m3.directe(m3.question(champ), etat, conseil=conseil, question=champ, trace=trace)

    etat.action_en_attente = _action_suivante(decision, action)

    # 5. Formuler : le seul appel LLM du tour, et seulement pour un conseil.
    if action and action.resultat and action.resultat.get("ok") is False:
        return m3.directe("Opération simulée refusée : " + action.resultat["motif"] + ".", etat, action=action, trace=trace)
    # Le gabarit immobilier historique présumait un financement sans assurance.
    # Le gabarit général existant restitue les raisons et alertes calculées par M3.
    decision_affichage = replace(decision, parcours="conseil_m3") if conseil else decision
    texte, etape = formuler(decision_affichage, conseil, action, profil, etat, message)
    if conseil:
        # Hypothèses hors LLM : ne doivent jamais être omises par la reformulation.
        mention = "Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager."
        suffixe = "\n\n" + mention if texte.endswith(mention) else ""
        if suffixe:
            texte = texte[:-len(mention)].rstrip()
        texte += "\n\n" + " ".join(conseil.faits.get("hypotheses", [])) + suffixe
    if action and action.resultat:
        texte += "\n\nSimulation uniquement : aucune opération réelle ni rappel réel."
        if action.resultat.get("limites"):
            texte += " " + action.resultat["limites"]
    trace.append(etape)

    etat.derniere_reponse = texte
    etat.historique.append({"role": "assistant", "content": texte})
    reponse = Reponse(
        texte=texte, comprehension=comprehension, conseil=conseil, action=action,
        question=decision.info if decision.type == "question" else None,
        escalade=escalade, trace=trace,
    )
    return reponse, etat
