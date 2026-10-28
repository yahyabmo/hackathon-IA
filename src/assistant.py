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

import re

from . import incompris, llm, rag
from .aiguilleur import URGENCE, Aiguillage, aiguiller, renvoi_au_contexte, trier_par_urgence
from .comprendre import classifieur, comprendre, escalader, interprete, mots_cles
from .comprendre.entites import extraire
from .conseiller import clients, conseiller
from .conseiller import integration as m3
from .contrats import (NIVEAU_CLASSIFIEUR, NIVEAU_FILE, NIVEAU_INTERPRETE, NIVEAU_MOTS_CLES, NIVEAU_REPONSE,
                       Comprehension, Conseil, EtatConversation, Etape, Reponse)
from .converser import Decision, avancer, formuler, glossaire
from .converser.dialogue import _mettre_de_cote, parcours_disponibles, question_en_attente, reponse_lisible
from .converser.formuler import mots_simples, politesse, question_clarification, reprise, simplifier, transition
from .mesure import mesurer
from .taxonomie import LIBELLES_FAMILLES, famille_de
from .texte import contient, euros, normaliser

# Informations de la question M3 qui complètent le profil plutôt que le projet.
CHAMPS_PROFIL = {"age": "age", "est_etudiant": "est_etudiant", "ages_enfants": "enfants"}
# Décisions qui terminent une demande : la suivante (file, ou parcours interrompu) peut venir.
TERMINALES = ("orienter", "fiche", "conseil", "rag", "abandon")
# Demandes qui n'attendent pas la fin d'une question en cours : la carte perdue ou volée.
URGENTES = URGENCE[:4]
# Demandes traitées par une règle, avant tout le reste (aucun accès au compte, aucun rendez-vous pris).
RENDEZ_VOUS = ("rendez vous", "rdv", "parler a un conseiller", "voir un conseiller", "contacter un conseiller",
               "etre rappele", "me rappeler", "parler a quelqu un")
DONNEES_COMPTE = ("releve", "releves", "mes donnees", "en se basant sur mes", "regarde mon compte",
                  "consulte mon compte", "verifie mon compte", "mon historique", "mes operations")
# Réponses données à part : elles ne terminent pas le parcours en cours, qui reprend ensuite.
A_PART_REGLES = ("rendez_vous", "acces_compte", "code_secret", "hors_sujet", "question_definition")
MOTS_CREDIT = ("credit", "pret", "emprunt", "emprunter")
BIEN_MINIMUM = 40_000  # sous ce montant, « un crédit de 10 000 € » n'est pas un projet immobilier
NOMBRE_SEUL = re.compile(r"[\d\s.,€k]+(?:euros?)?", re.IGNORECASE)
# « finalement oui » après un refus : le parcours laissé de côté reprend là où il en était.
REPRENDRE = ("finalement oui", "finalement si", "oui finalement", "si finalement", "en fait oui", "on reprend",
             "reprenons", "on continue", "je veux bien finalement", "finalement je veux bien", "finalement d accord")
# « et si j'emprunte sur 30 ans ? », « non plutôt 300 € » : une variante du parcours, pas un nouveau sujet.
SUITE = ("et si", "et avec", "et sur", "et pour", "et en", "plutot", "reessayer", "finalement", "si j emprunte",
         "si je prends", "si je mets")
# « je vais être remboursée ? » après un vol de carte : le classifieur, qui ne voit pas la conversation,
# n'a pas le dernier mot sur une question de suite d'un autre domaine ; le niveau 1 la lit avec le contexte.
QUESTION_DE_SUITE = re.compile(r"\?\s*$|^(et|est ce|je |il |elle |ca |c est )")
# « il veut aussi mon code de carte » : jamais, à personne (règle de sécurité, avant tout le reste).
CODE_SECRET = ("code de carte", "code de ma carte", "code de la carte", "code confidentiel", "code secret",
               "mon code", "mot de passe", "mes identifiants")
DEMANDE_DE_CODE = ("veut", "veulent", "demande", "demandent", "donner", "donne", "envoyer", "communiquer",
                   "quelqu un", "telephone", "sms", "mail")


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


def _politesse_seule(message: str, texte_normalise: str) -> str | None:
    """Le genre de politesse (``formuler.politesse``) d'un message qui ne contient aucune autre demande."""

    trouvees = mots_cles.expressions_trouvees(message)
    if set(trouvees) - {"hors_sujet"} or extraire(message).get("montants"):
        return None
    return politesse(texte_normalise)


def _parcours_a_reprendre(etat: EtatConversation) -> str | None:
    """Le parcours guidé auquel rattacher la suite : celui en cours, sinon le dernier laissé de côté."""

    if etat.parcours in parcours_disponibles() and etat.parcours not in A_PART_REGLES:
        return etat.parcours
    return next(reversed(etat.memoire), None)


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
    bascule: str | None = None
    lu = message
    # Une question restait en attente : après une parenthèse, on y revient.
    en_cours = (etat.parcours, etat.famille, dict(etat.slots), etat.info_attendue) if etat.info_attendue else None

    # 0. Barrières : montant ambigu, information manquante pour un conseil.
    texte_normalise = normaliser(message)
    poli = _politesse_seule(message, texte_normalise)
    if any(contient(texte_normalise, c) for c in CODE_SECRET) and any(
            contient(texte_normalise, d) for d in DEMANDE_DE_CODE):
        decision = Decision("orienter", parcours="code_secret")
    elif m3.montant_ambigu(message):
        decision = Decision("montant_ambigu")
    elif poli in ("fin", "reflechir"):
        # « au revoir » pendant une question : on salue, la demande reste en mémoire si le client revient.
        _mettre_de_cote(etat)
        etat.parcours = etat.famille = etat.info_attendue = None
        etat.slots, etat.file_demandes, en_cours = {}, [], None
        comprehension = Comprehension(famille=famille_de("hors_sujet"), intention="hors_sujet", confiance=1.0,
                                      niveau=NIVEAU_MOTS_CLES, modele="regles")
        decision = Decision("fiche", parcours="hors_sujet")
    elif any(contient(texte_normalise, e) for e in RENDEZ_VOUS):
        decision = Decision("orienter", parcours="rendez_vous")
    elif any(contient(texte_normalise, e) for e in DONNEES_COMPTE):
        decision = Decision("orienter", parcours="acces_compte")
    elif etat.question_m3:
        decision = _reprendre_question_m3(message, etat, profil)

    # 1. Entrée commune, puis l'aiguilleur choisit le niveau de ce message.
    if decision is None:
        comprehension, etape = mesurer("comprendre", lambda: comprendre(message, etat))
        etape.modele = comprehension.modele
        trace.append(etape)
        montants = comprehension.entites.get("montants") or []
        nombre_seul = bool(NOMBRE_SEUL.fullmatch(message.strip()))
        cible = _parcours_a_reprendre(etat)
        suite = any(contient(texte_normalise, m) for m in SUITE) and comprehension.niveau != NIVEAU_MOTS_CLES
        sans_demande = (not comprehension.comprise or nombre_seul or suite
                        or comprehension.intention == "hors_sujet")
        valeurs = montants or any(comprehension.entites.get(k) for k in ("duree_mois", "lien", "objet"))
        reprendre = (cible and not etat.info_attendue and comprehension.niveau != NIVEAU_MOTS_CLES
                     and any(contient(texte_normalise, r) for r in REPRENDRE))
        if cible and cible != etat.parcours and ((sans_demande and valeurs) or reprendre):
            # « finalement oui », ou « 500 » après un refus : le parcours laissé de côté reprend.
            comprehension = Comprehension(
                famille=etat.memoire[cible].get("famille") or famille_de(cible), intention=cible, confiance=1.0,
                niveau=NIVEAU_MOTS_CLES, modele="regles", entites=comprehension.entites)
            bascule = f"Très bien, reprenons : {LIBELLES_FAMILLES.get(famille_de(cible), 'votre demande')}."
        elif sans_demande and cible and (montants or comprehension.entites.get("duree_mois")):
            # « Et avec un bien à 200 000 ? », ou « 1000 » : la suite du parcours en cours.
            comprehension = Comprehension(
                famille=etat.famille or "", intention=etat.parcours, confiance=1.0,
                niveau=NIVEAU_REPONSE, modele="regles", entites=comprehension.entites)
        elif (cible and comprehension.niveau == NIVEAU_CLASSIFIEUR and not etat.info_attendue
              and comprehension.intention not in parcours_disponibles()
              and _domaine(comprehension.intention) != _domaine(cible)
              and QUESTION_DE_SUITE.search(message.strip().lower())):
            comprehension = Comprehension(entites=comprehension.entites, alternatives=comprehension.alternatives,
                                          modele=comprehension.modele)
        if (etat.parcours == "credit_immobilier" and montants and max(montants) < BIEN_MINIMUM
                and any(contient(texte_normalise, m) for m in MOTS_CREDIT)):
            # « Un crédit de 10 000 € » n'est pas un bien à 10 000 € : c'est un crédit à la consommation.
            etat.memoire.pop("credit_immobilier", None)
            etat.parcours = etat.info_attendue = None
            etat.slots, en_cours = {}, None
            bascule = (f"Pour emprunter {euros(max(montants))}, il s'agit d'un crédit à la consommation, "
                       "pas d'un crédit immobilier.")
            comprehension = Comprehension(famille="credit", intention="credit_conso", confiance=1.0,
                                          niveau=NIVEAU_MOTS_CLES, modele="regles", entites=comprehension.entites)
        lisible = (comprehension.niveau != NIVEAU_REPONSE or poli in ("merci", "salut")
                   or reponse_lisible(message, comprehension.entites, etat))
        llm_ok = _llm_permis(etat)
        aiguillage = aiguiller(message, comprehension, etat, lisible=lisible,
                               sujets_cites=rag.vocabulaire_cite(message), llm_ok=llm_ok,
                               rag_ok=rag.disponible())
        if (aiguillage.niveau == 0 and comprehension.intention == "question_definition" and rag.disponible()
                and glossaire.chercher(message, approchant=True) is None):
            aiguillage = Aiguillage(2, "terme absent du glossaire : recherche dans nos fiches", aiguillage.signaux)
        if etat.niveau_force is not None:
            aiguillage = Aiguillage(etat.niveau_force, "niveau forcé (démonstration)", aiguillage.signaux)

        if aiguillage.niveau == 1 and llm_ok:
            interpretation = interprete.interpreter(message, _contexte(etat, profil))
            trace.append(interpretation.etape)
            if interpretation.valide:
                comprehension, lu, meme_sujet = _appliquer(interpretation, comprehension, etat, message)
            aiguillage.raison += f" → {interpretation.raison}"
            if (comprehension.intention == "question_definition" and rag.disponible()
                    and glossaire.chercher(message, approchant=True) is None):
                aiguillage = Aiguillage(2, aiguillage.raison + " ; aucun terme du glossaire : nos fiches",
                                        aiguillage.signaux)
        if aiguillage.niveau == 2:
            pourquoi = message.strip().lower().startswith("pourquoi")
            reponse_rag = rag.repondre(message, etat.explication if pourquoi else None, avec_llm=llm_ok)
            trace += reponse_rag.etapes
            sources = reponse_rag.sources
            if reponse_rag.pertinent or etat.niveau_force == 2:
                texte_rag, decision = reponse_rag.texte, Decision("rag")
            else:
                aiguillage = Aiguillage(0, "aucune fiche assez proche : retour aux règles", aiguillage.signaux)

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
    if (meme_sujet or poli) and decision.type == "question" and decision.relance == "incompris":
        decision.relance = "merci" if poli == "merci" else "meme_sujet"  # « merci » ou « ok » : pas un incompris
    if bascule:
        decision.accroche = bascule

    # 4. Formuler (le niveau 2 a déjà rédigé sa réponse).
    if texte_rag is not None:
        texte = simplifier(texte_rag, expliquer_jargon=False) if mots_simples(profil, etat) else texte_rag
        trace.append(Etape(nom="formuler", modele="rag"))
    else:
        texte, etape = formuler(decision, conseil, profil, etat, message)
        trace.append(etape)

    # 5. La suite : reprendre la question interrompue, ou passer à la demande suivante en file.
    a_part = decision.parcours in A_PART_REGLES
    if (decision.type in TERMINALES and decision.type != "rag" and not a_part and etat.parcours
            and etat.parcours not in etat.traites):
        etat.traites.append(etat.parcours)
    if decision.type in TERMINALES and not etat.question_m3:
        interrompu = (en_cours and decision.type != "abandon" and en_cours[0] not in etat.file_demandes
                      and (decision.type == "rag" or a_part or etat.parcours != en_cours[0]))
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
