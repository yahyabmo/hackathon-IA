"""Point d'entrée unique de l'assistant : un tour de conversation, aiguillé.

entrée commune (barrières, entités, mots-clés, classifieur) → aiguilleur →
  niveau 0 : converser → conseiller → formuler (règles et gabarits, sans LLM)
  niveau 1 : un petit LLM comprend le message (JSON imposé), puis niveau 0
  niveau 2 : RAG sur nos fiches, un LLM rédige en citant, sous garde-fou

L'aiguilleur décide à chaque message : une conversation peut passer de 1 à 2,
puis à 0, puis à 2. La mémoire est commune à tous les niveaux : parcours en
cours, demandes en file (plusieurs demandes dans un même message, traitées par
urgence), informations déjà données, question restée en attente, reprise après
une parenthèse. Le chatbot n'a aucun accès bancaire ; il guide les demandes
sensibles vers le canal approprié.

Les barrières métier de M3 (montant ambigu, information manquante pour un
conseil) produisent des décisions comme les autres.
"""

from __future__ import annotations

from . import incompris, llm, rag
from .aiguilleur import URGENCE, Aiguillage, aiguiller, renvoi_au_contexte, trier_par_urgence
from .comprendre import classifieur, comprendre, escalader, interprete, mots_cles
from .comprendre.entites import extraire
from .conseiller import clients, conseiller
from .conseiller import integration as m3
from .contrats import (NIVEAU_FILE, NIVEAU_INTERPRETE, NIVEAU_REPONSE, Comprehension, Conseil,
                       EtatConversation, Etape, Reponse)
from .converser import Decision, avancer, formuler
from .converser.dialogue import question_en_attente, reponse_lisible
from .converser.formuler import mots_simples, question_clarification, reprise, simplifier, transition
from .mesure import mesurer
from .taxonomie import LIBELLES_FAMILLES, famille_de
from .texte import normaliser

# Informations de la question M3 qui complètent le profil plutôt que le projet.
CHAMPS_PROFIL = {"age": "age", "est_etudiant": "est_etudiant", "ages_enfants": "enfants"}
# Décisions qui terminent une demande : la suivante (file, ou parcours interrompu) peut venir.
TERMINALES = ("orienter", "fiche", "conseil", "rag", "abandon")
# Demandes qui n'attendent pas la fin d'une question en cours : la carte perdue ou volée.
URGENTES = URGENCE[:4]


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


def _llm_permis(etat: EtatConversation) -> bool:
    return etat.llm_actif if etat.llm_actif is not None else llm.actif()


def _contexte(etat: EtatConversation, profil: dict) -> dict[str, str | None]:
    """Ce que le niveau 1 sait de la conversation : jamais le profil du client."""

    sujet = LIBELLES_FAMILLES.get(etat.famille or famille_de(etat.parcours or "")) if etat.parcours else None
    deja = list(dict.fromkeys(LIBELLES_FAMILLES.get(famille_de(i), i) for i in etat.traites))
    return {"sujet": sujet, "question": question_en_attente(etat, profil),
            "traite": ", ".join(deja) if deja else None}


TYPES_FERMES = ("lien", "objet")  # valeurs d'une liste fermée : sans risque d'invention


def _domaine(intention: str) -> str:
    return famille_de(intention).split("_")[0]  # carte_perdue, carte_usage… → carte


# Mots qui désignent un domaine, pour rattacher un renvoi au contexte (« et pour ma carte ? »).
MOTS_DOMAINES = {"carte": "carte", "cb": "carte", "virement": "virement", "frais": "frais", "epargne": "epargne",
                 "livret": "epargne", "credit": "credit", "pret": "credit", "apport": "credit", "emprunt": "credit"}


def _rattacher(interpretation: interprete.Interpretation, etat: EtatConversation, message: str) -> None:
    """Ce que le code impose au niveau 1 : l'urgence d'abord, et les renvois au contexte.

    « mais ma carte ? » renvoie au sujet déjà traité du même domaine, pas à un sujet voisin.
    """

    if renvoi_au_contexte(message):
        texte = normaliser(message).split()
        domaines = [d for mot, d in MOTS_DOMAINES.items() if mot in texte]
        for domaine in domaines:  # un mot du message désigne le domaine : il prime sur le choix du LLM
            traite = next((t for t in reversed(etat.traites) if _domaine(t) == domaine), None)
            if traite:
                interpretation.intentions = [traite, *[i for i in interpretation.intentions if _domaine(i) != domaine]]
        for i, intention in enumerate(interpretation.intentions):
            traite = next((t for t in reversed(etat.traites) if _domaine(t) == _domaine(intention)), None)
            if traite:
                interpretation.intentions[i] = traite
    interpretation.intentions = trier_par_urgence(interpretation.intentions)


def _confirmee(intention: str, message: str) -> bool:
    """Une nouvelle demande proposée par le LLM pendant une question : les mots-clés ou le classifieur la voient-ils ?"""

    if intention in mots_cles.expressions_trouvees(message):
        return True
    prediction = classifieur.predire(message)
    return prediction is not None and famille_de(intention) in {a.famille for a in prediction.alternatives}


def _appliquer(interpretation: interprete.Interpretation, comprehension: Comprehension,
               etat: EtatConversation, message: str) -> tuple[Comprehension, str, bool]:
    """Ce que le niveau 1 a compris, rendu à l'automate : (compréhension, message lu, même sujet)."""

    _rattacher(interpretation, etat, message)
    nouvelles = [i for i in interpretation.intentions if i != etat.parcours and i != "hors_sujet"]
    if etat.info_attendue:
        nouvelles = [i for i in nouvelles if _confirmee(i, message)]
    modele = interpretation.etape.modele if interpretation.etape else None
    if etat.info_attendue and etat.parcours:
        for reponse, fermee in ((interpretation.reponse, False), (interpretation.reponse_brute, True)):
            if not reponse:
                continue
            entites = extraire(reponse)
            if fermee:  # hors des mots du message : seulement une valeur d'une liste fermée, jamais un nombre
                entites = {k: v for k, v in entites.items() if k in TYPES_FERMES}
                if not entites:
                    continue
            if reponse_lisible(reponse, entites, etat):
                return (Comprehension(famille=etat.famille or famille_de(etat.parcours), intention=etat.parcours,
                                      confiance=1.0, niveau=NIVEAU_REPONSE, modele=modele, entites=entites,
                                      autres_intentions=nouvelles), reponse, False)
        if nouvelles:
            # Une nouvelle demande pendant une question : la question attendra, en mémoire.
            etat.file_demandes = trier_par_urgence([etat.parcours, *etat.file_demandes])
            return (Comprehension(famille=famille_de(nouvelles[0]), intention=nouvelles[0], confiance=0.0,
                                  niveau=NIVEAU_INTERPRETE, modele=modele, entites=comprehension.entites,
                                  autres_intentions=nouvelles[1:]), message, False)
        if etat.parcours in interpretation.intentions:
            return comprehension, message, True  # même sujet, pas de réponse : on repose la question, doucement
        return comprehension, message, False
    if interpretation.intentions:
        premiere = interpretation.intentions[0]
        return (Comprehension(famille=famille_de(premiere), intention=premiere, confiance=0.0,
                              niveau=NIVEAU_INTERPRETE, modele=modele, entites=comprehension.entites,
                              autres_intentions=interpretation.intentions[1:]), message, False)
    return comprehension, message, False


def _explication(conseil: Conseil) -> list[str]:
    """Le conseil en phrases, pour répondre à un « pourquoi ? » au tour suivant (niveau 2)."""

    from .converser.formuler import nom_produit

    phrases = [f"{nom_produit(p.produit_id)} : {' '.join(p.raisons)}" for p in conseil.propositions if p.raisons]
    phrases += [f"{nom_produit(e.produit_id)} n'est pas proposé : {e.raison}" for e in conseil.ecartees]
    return phrases + list(conseil.alertes) + list(conseil.faits.get("hypotheses", []))


def _traiter(decision: Decision, message: str, comprehension: Comprehension, etat: EtatConversation,
             profil: dict, trace: list[Etape]) -> tuple[Decision, Conseil | None]:
    """Converser puis conseiller, à partir d'une compréhension (niveau 0)."""

    conseil = None
    if decision is None:
        etat.clarification_demandee = False
        decision, etape = mesurer("converser", lambda: avancer(message, comprehension, etat, profil),
                                  modele="automate")
        trace.append(etape)
        if decision.type == "transmettre":
            decision = Decision("orienter", parcours=etat.parcours, accroche=decision.accroche)
    if decision.type == "conseil":
        conseil, etape = mesurer("conseiller", lambda: conseiller(etat.parcours, profil, etat.slots),
                                 modele="regles")
        trace.append(etape)
        if conseil.manque:
            etat.question_m3 = conseil.manque[0]
            decision = Decision("question_m3", parcours=etat.parcours, info=etat.question_m3)
        else:
            etat.explication = _explication(conseil)
    return decision, conseil


def reply(
    message: str, client_id: str, etat: EtatConversation | None = None
) -> tuple[Reponse, EtatConversation]:
    """Traite un message du client et rend la réponse, avec l'état mis à jour."""

    etat = etat if etat is not None else EtatConversation()
    if etat.client_id is not None and etat.client_id != client_id:
        etat = EtatConversation(mots_simples=etat.mots_simples, llm_actif=etat.llm_actif,
                                niveau_force=etat.niveau_force)
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
    aiguillage = Aiguillage(0, "règles")
    sources: list[dict] = []
    texte_rag: str | None = None
    meme_sujet = False
    lu = message
    # Une question restait en attente : après une parenthèse, on y revient.
    en_cours = (etat.parcours, etat.famille, dict(etat.slots), etat.info_attendue) if etat.info_attendue else None

    # 0. Barrières : montant ambigu, information manquante pour un conseil.
    if m3.montant_ambigu(message):
        decision = Decision("montant_ambigu")
    elif etat.question_m3:
        decision = _reprendre_question_m3(message, etat, profil)

    # 1. Entrée commune, puis l'aiguilleur choisit le niveau de ce message.
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
        lisible = comprehension.niveau != NIVEAU_REPONSE or reponse_lisible(message, comprehension.entites, etat)
        llm_ok = _llm_permis(etat)
        aiguillage = aiguiller(message, comprehension, etat, lisible=lisible,
                               sujets_cites=rag.vocabulaire_cite(message), llm_ok=llm_ok,
                               rag_ok=rag.disponible())
        if etat.niveau_force is not None:
            aiguillage = Aiguillage(etat.niveau_force, "niveau forcé (démonstration)", aiguillage.signaux)

        if aiguillage.niveau == 2:
            pourquoi = message.strip().lower().startswith("pourquoi")
            reponse_rag = rag.repondre(message, etat.explication if pourquoi else None, avec_llm=llm_ok)
            trace += reponse_rag.etapes
            sources = reponse_rag.sources
            if reponse_rag.pertinent or etat.niveau_force == 2:
                texte_rag, decision = reponse_rag.texte, Decision("rag")
            else:
                aiguillage = Aiguillage(0, "aucune fiche assez proche : retour aux règles", aiguillage.signaux)
        elif aiguillage.niveau == 1 and llm_ok:
            interpretation = interprete.interpreter(message, _contexte(etat, profil))
            trace.append(interpretation.etape)
            if interpretation.valide:
                comprehension, lu, meme_sujet = _appliquer(interpretation, comprehension, etat, message)
            aiguillage.raison += f" → {interpretation.raison}"

        if comprehension.autres_intentions:
            etat.file_demandes = trier_par_urgence(
                [*etat.file_demandes, *[i for i in comprehension.autres_intentions if i != comprehension.intention]])

        if decision is None and not comprehension.comprise:
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

    # 2 et 3. Converser, puis conseiller (niveau 0, ou après le niveau 1).
    if decision is None or decision.type == "conseil":
        decision, conseil = _traiter(decision, lu, comprehension, etat, profil, trace)
    if meme_sujet and decision.type == "question" and decision.relance == "incompris":
        decision.relance = "meme_sujet"

    # 4. Formuler (le niveau 2 a déjà rédigé sa réponse).
    if texte_rag is not None:
        texte = simplifier(texte_rag, expliquer_jargon=False) if mots_simples(profil, etat) else texte_rag
        trace.append(Etape(nom="formuler", modele="rag"))
    else:
        texte, etape = formuler(decision, conseil, profil, etat, message)
        trace.append(etape)

    # 5. La suite : reprendre la question interrompue, ou passer à la demande suivante en file.
    if decision.type in TERMINALES and decision.type != "rag" and etat.parcours and etat.parcours not in etat.traites:
        etat.traites.append(etat.parcours)
    if decision.type in TERMINALES and not etat.question_m3:
        interrompu = (en_cours and decision.type != "abandon" and en_cours[0] not in etat.file_demandes
                      and (decision.type == "rag" or etat.parcours != en_cours[0]))
        if interrompu:
            etat.parcours, etat.famille, etat.slots, etat.info_attendue = en_cours
            etat.memoire.pop(en_cours[0], None)
            texte += "\n\n" + reprise(en_cours[0], question_en_attente(etat, profil))
        elif etat.file_demandes and not etat.info_attendue:
            suivante = etat.file_demandes.pop(0)
            suite = Comprehension(famille=famille_de(suivante), intention=suivante, confiance=1.0,
                                  niveau=NIVEAU_FILE, modele="file")
            decision_suite, conseil_suite = _traiter(None, "", suite, etat, profil, trace)
            texte_suite, etape = formuler(decision_suite, conseil_suite, profil, etat, "")
            trace.append(etape)
            texte += "\n\n" + transition(suivante) + " " + texte_suite
            decision, conseil = decision_suite, conseil_suite or conseil
    elif decision.type == "question" and etat.file_demandes and etat.file_demandes[0] in URGENTES:
        # « mon père, et au fait j'ai perdu ma carte » : l'urgence tout de suite, puis la question.
        garde = (etat.parcours, etat.famille, dict(etat.slots), etat.info_attendue)
        urgente = etat.file_demandes.pop(0)
        decision_u, conseil_u = _traiter(None, "", Comprehension(famille=famille_de(urgente), intention=urgente,
                                                                 confiance=1.0, niveau=NIVEAU_FILE, modele="file"),
                                         etat, profil, trace)
        texte_u, etape = formuler(decision_u, conseil_u, profil, etat, "")
        trace.append(etape)
        etat.traites.append(urgente)
        etat.parcours, etat.famille, etat.slots, etat.info_attendue = garde
        etat.memoire.pop(garde[0], None)
        texte = texte_u + "\n\n" + reprise(garde[0], question_en_attente(etat, profil))
    elif en_cours and etat.parcours != en_cours[0] and en_cours[0] not in etat.file_demandes:
        etat.file_demandes.insert(0, en_cours[0])  # la question interrompue reviendra ensuite

    etat.niveaux.append(aiguillage.niveau)
    etat.derniere_reponse = texte
    etat.historique.append({"role": "assistant", "content": texte})
    reponse = Reponse(
        texte=texte, comprehension=comprehension, conseil=conseil,
        question=decision.info if decision.type in ("question", "question_m3") else None,
        escalade=escalade, trace=trace, niveau=aiguillage.niveau, raison_niveau=aiguillage.raison,
        sources=sources,
    )
    return reponse, etat
