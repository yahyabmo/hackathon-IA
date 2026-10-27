"""Étage 5 : formuler la réponse.

Gabarit d'abord : exact, instantané, gratuit. Le petit LLM n'intervient que
pour un conseil (plusieurs faits à articuler), une seule fois par tour, à la
fin, et seulement si ``ASSISTANT_LLM=1``. Il reçoit le texte gabarit et le
reformule ; le garde-fou n'autorise que les nombres déjà présents dans ce
gabarit. En cas d'échec, le gabarit est affiché.

Les mentions légales et les rappels de sécurité sont ajoutés hors du LLM.

Mode « mots simples » (client de 70 ans ou plus, « peu à l'aise en ligne », ou
sur demande) : une phrase par ligne, pas d'aparté entre parenthèses, et le
premier terme du glossaire présent dans la réponse est expliqué.
"""

from __future__ import annotations

import re
from time import perf_counter
from typing import Any

from .. import llm
from ..contrats import Alternative, Conseil, Etape, EtatConversation
from ..conseiller import catalogue as cat
from ..conseiller import integration as questions_m3
from ..taxonomie import LIBELLES_FAMILLES, famille_de
from ..texte import euros, normaliser
from . import garde_fou, glossaire
from .dialogue import Decision

MENTIONS = {
    "credit": "Un crédit vous engage et doit être remboursé. "
              "Vérifiez vos capacités de remboursement avant de vous engager.",
}
RAPPEL_CODE = "Rappel : la banque ne vous demandera jamais votre code confidentiel."
MESSAGES_FIXES = {
    "abandon": "D'accord, on laisse ça de côté. Puis-je vous aider pour autre chose ?",
    "orienter": ("Je préfère ne pas deviner. Un conseiller peut reprendre votre demande : prenez rendez-vous "
                 "depuis votre espace bancaire sécurisé ou contactez votre agence."),
    "clarifier": ("Pour bien vous aider, pouvez-vous préciser ? Par exemple : votre carte, un virement, des "
                  "frais, votre épargne ou un projet de crédit."),
}
CONFIANCE_QUESTION_FERMEE = 0.5
# Le chatbot n'a aucun accès au compte et ne transmet rien (périmètre du kick-off) : il dit comment
# joindre un conseiller, sans poser de question oui / non qui n'aurait aucune suite.
ORIENTATION_CONSEILLER = ("Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace "
                          "bancaire sécurisé ou contactez votre agence.")
SUITE_CONSEILLER = ("Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis "
                    "votre espace bancaire sécurisé.")
NOMS_SPECIAUX = {"credit_immobilier_30_ans": "Un prêt immobilier sur 30 ans"}
AGE_MOTS_SIMPLES = 70
RELANCES = {
    "incompris": "Je n'ai pas bien compris.",
    "ne_sait_pas": "Pas de souci, une estimation suffit.",
    "meme_sujet": "Bien sûr.",
}
ACCORDS = ("oui", "ok", "d accord", "merci", "parfait", "tres bien", "super", "non", "non merci", "c est bon")
SEUIL_MONTANT_INHABITUEL = 10  # fois les revenus mensuels
MOIS = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre")

SYSTEME_FORMULATION = (
    "Tu es l'assistant d'une banque française. On te donne un message déjà rédigé pour un client. "
    "Réécris-le en français, au vouvoiement, avec des phrases courtes et un ton chaleureux. Garde "
    "toutes les informations et tous les chiffres exactement ; n'ajoute aucun chiffre, aucun produit, "
    "aucune promesse ni aucune question. Réponds uniquement par le message réécrit."
)
CONSIGNE_MESSAGE = 'Message à réécrire :\n"""\n{texte}\n"""'
LONGUEUR_MIN_RELATIVE = 0.4
LONGUEUR_MAX_RELATIVE = 1.5
CARACTERES_PAR_TOKEN = 2  # un token fait 3 à 4 caractères en français : la marge couvre une réécriture plus longue
CONSIGNE_SIMPLE = " Le client est peu à l'aise : phrases très courtes, mots de tous les jours."


def mots_simples(profil: dict[str, Any], etat: EtatConversation) -> bool:
    """Le mode « mots simples » s'applique-t-il à ce client ?"""

    return (etat.mots_simples or bool(profil.get("peu_a_laise_en_ligne"))
            or profil.get("age", 0) >= AGE_MOTS_SIMPLES)


def reformuler(texte: str, modele: str, simple: bool = False) -> tuple[str | None, int, list[str]]:
    """Un appel au LLM pour réécrire un gabarit, vérifié par le garde-fou.

    Rend le texte réécrit (``None`` s'il est refusé), les tokens consommés et les
    problèmes trouvés. Partagé par la formulation et le banc de formulation.
    """

    systeme = SYSTEME_FORMULATION + (CONSIGNE_SIMPLE if simple else "")
    reecrit, tokens = llm.generer(modele, systeme, CONSIGNE_MESSAGE.format(texte=texte),
                                  max_tokens=max(200, len(texte) // CARACTERES_PAR_TOKEN))
    reecrit = reecrit.strip().strip('"').strip()
    reference = set(garde_fou.nombres(texte))
    problemes = garde_fou.verifier(
        reecrit, reference, obligatoires=reference, longueur_min=int(LONGUEUR_MIN_RELATIVE * len(texte)),
        longueur_max=max(garde_fou.LONGUEUR_MAX, int(LONGUEUR_MAX_RELATIVE * len(texte))))
    return (None if problemes else reecrit), tokens, problemes


def simplifier(texte: str, expliquer_jargon: bool = True) -> str:
    """Une phrase par paragraphe, sans aparté, et le premier terme technique expliqué."""

    texte = re.sub(r"\s*\((?!oui / non\))[^)]*\)", "", texte)
    phrases = [p.strip() for p in re.split(r"(?:(?<=[.?!])|(?<=\(oui / non\)))\s+(?!\()", texte) if p.strip()]
    if expliquer_jargon:
        fiche = glossaire.chercher(texte)
        if fiche:
            explication = fiche["explication"]
            phrases.append(f"« {fiche['terme']} » veut dire : {explication[0].lower()}{explication[1:]}")
    return "\n\n".join(phrases)


def question_clarification(alternatives: list[Alternative]) -> str | None:
    """Sous le seuil τ : une question fermée sur les deux familles les plus probables.

    Seulement si la première a un vrai appui ; sinon (message sans rapport, charabia),
    la question ouverte, plutôt que deux familles tirées au hasard.
    """

    if not alternatives or alternatives[0].confiance < CONFIANCE_QUESTION_FERMEE:
        return None
    libelles = [LIBELLES_FAMILLES[a.famille] for a in alternatives
                if a.famille in LIBELLES_FAMILLES and a.famille != "conversation"]
    if len(libelles) < 2:
        return None
    return f"Pour être sûr de bien vous aider : votre demande concerne-t-elle {libelles[0]}, ou {libelles[1]} ?"


def _libelle_demande(intention: str) -> str:
    return LIBELLES_FAMILLES.get(famille_de(intention), "votre demande")


def _exemples_de_reponse(decision: Decision) -> str | None:
    """Après une réponse qui ne répondait pas, des exemples de réponses attendues."""

    from .dialogue import parcours_disponibles

    if decision.relance not in ("meme_sujet", "incompris"):
        return None
    info = (parcours_disponibles().get(decision.parcours or "") or {}).get("infos", {}).get(decision.info or "", {})
    return {"lien": "Par exemple : votre fils, votre mère, un ami.",
            "montant": "Par exemple : 200 €.", "duree": "Par exemple : 2 ans, ou 48 mois."}.get(info.get("type"))


def transition(intention: str) -> str:
    """Entre deux demandes d'un même message : « Passons maintenant à votre autre demande : … »."""

    return f"Passons maintenant à votre autre demande : {_libelle_demande(intention)}."


def reprise(parcours: str, question: str | None) -> str:
    """Après une parenthèse, la question restée en attente."""

    return f"Revenons à {_libelle_demande(parcours)} : {question[0].lower()}{question[1:]}" if question else \
        f"Revenons à {_libelle_demande(parcours)}."


def _vraisemblance(montant: Any, profil: dict[str, Any]) -> str | None:
    """Un montant de virement comparé au solde et aux revenus du profil simulé."""

    if not isinstance(montant, (int, float)) or montant <= 0:
        return None
    solde, revenus = profil.get("solde"), profil.get("revenus_nets") or 0
    if revenus and montant >= SEUIL_MONTANT_INHABITUEL * revenus:
        return (f"Attention : {euros(montant)}, c'est un montant très inhabituel, bien au-delà de votre solde "
                f"({euros(solde)}) : vérifiez-le avant de valider." if solde is not None else
                f"Attention : {euros(montant)}, c'est un montant très inhabituel : vérifiez-le avant de valider.")
    if solde is not None and montant > solde:
        return f"Attention : {euros(montant)} dépasse votre solde ({euros(solde)}) : vérifiez le montant avant de valider."
    return None


def nom_produit(produit_id: str) -> str:
    """Nom lisible d'un produit, y compris ceux qui n'existent que comme écart."""

    try:
        return cat.nom(produit_id)
    except KeyError:
        return NOMS_SPECIAUX.get(produit_id, produit_id)


def _date(iso: str) -> str:
    annee, mois, jour = iso.split("-")
    return f"{int(jour)} {MOIS[int(mois) - 1]}"


def _joindre(*morceaux: str | None, sep: str = " ") -> str:
    return sep.join(m for m in morceaux if m)


# ── Gabarits ──────────────────────────────────────────────────────────

def _suite(raison: str) -> str:
    """Une raison de M3 placée après « : » : minuscule initiale (sauf sigle), un seul point final."""

    raison = raison.strip().rstrip(".")
    premier_mot = raison.split(" ", 1)[0]
    if len(premier_mot) == 1 or not premier_mot.isupper():
        raison = raison[0].lower() + raison[1:]
    return raison + "."


def _conseil_general(conseil: Conseil) -> str:
    """Un paragraphe pour ce qui est proposé, un pour ce qui ne l'est pas, un pour les alertes."""

    proposes = [p for p in conseil.propositions if p.produit_id != "rdv_conseiller" and p.raisons]
    paragraphes = []
    if proposes:
        paragraphes.append("Voici ce que je vous propose. " + " ".join(
            f"{nom_produit(p.produit_id)} : {_suite(p.raisons[0])}" for p in proposes))
    if conseil.ecartees:
        paragraphes.append(" ".join(
            f"Non proposé — {nom_produit(e.produit_id)} : {_suite(e.raison)}" for e in conseil.ecartees))
    if conseil.alertes:
        paragraphes.append(" ".join(conseil.alertes))
    return "\n\n".join(paragraphes)


def parties_conseil(decision: Decision, conseil: Conseil) -> tuple[str, str | None]:
    """Le conseil en deux parties : le corps, que le LLM peut réécrire, et la question finale.

    Le même gabarit sert tous les parcours : les règles de M3 calculent les raisons, les
    écarts et les alertes (assurance inconnue, frais non couverts…), le gabarit les restitue.
    La question reste mot pour mot hors LLM : le tour suivant attend un « oui » ou un
    « non » à cette question précise (un petit modèle l'a réécrite en « que je vous contacte »).
    """

    corps = _joindre(decision.accroche, *decision.confirmations, _conseil_general(conseil))
    return corps, SUITE_CONSEILLER if decision.proposer else None


def _gabarit_fiche(decision: Decision, message: str) -> str:
    if decision.parcours == "question_definition":
        fiche = glossaire.chercher(message, approchant=True)
        if fiche:
            return f"{fiche['terme']} : {fiche['explication']}"
        return "Je n'ai pas encore de fiche sur ce terme : un conseiller pourra vous l'expliquer."
    if decision.parcours == "hors_sujet":
        if normaliser(message) in ACCORDS:
            debut = "Avec plaisir." if "merci" in normaliser(message) else "D'accord."
            return f"{debut} Puis-je vous aider pour autre chose ?"
        debut = "Avec plaisir !" if "merci" in normaliser(message) else "Bonjour !"
        return (f"{debut} Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un "
                "projet de crédit. Que puis-je faire pour vous ?")
    sujet = LIBELLES_FAMILLES.get(famille_de(decision.parcours or ""), "ce sujet")
    return (f"Je comprends que votre demande concerne {sujet}. Je n'ai pas de parcours guidé pour ce point, "
            f"et aucun accès à votre compte. {ORIENTATION_CONSEILLER}")


def _gabarit_orientation(decision: Decision, profil: dict[str, Any], etat: EtatConversation) -> str:
    """Guide l'utilisateur sans accès au compte et sans exécution d'opération."""
    if decision.parcours == "lost_or_stolen_card":
        return _joindre(decision.accroche, "Faites opposition tout de suite : dans votre espace bancaire "
                        "sécurisé, rubrique Opposition, ou en appelant votre conseiller. Je ne peux pas bloquer "
                        "votre carte depuis cette conversation.", RAPPEL_CODE)
    if decision.parcours == "faire_virement":
        return _joindre(decision.accroche, _vraisemblance(etat.slots.get("montant"), profil),
                        "Pour effectuer ce virement, utilisez votre espace bancaire sécurisé "
                        "et vérifiez le bénéficiaire avant de valider. Je ne peux pas accéder à votre compte ni "
                        "exécuter le virement depuis cette conversation.")
    if famille_de(decision.parcours or "") == "frais_contestation":
        return _joindre(decision.accroche, _explication_frais())
    if decision.parcours == "insatisfaction":
        return _joindre(decision.accroche, "Je n'ai aucun accès à votre compte, mais votre réclamation compte.",
                        ORIENTATION_CONSEILLER, "Si le problème persiste, le service réclamations puis le "
                        "médiateur bancaire peuvent être saisis.")
    return _joindre(decision.accroche, "Je n'ai aucun accès à votre compte.", ORIENTATION_CONSEILLER)


def _explication_frais() -> str:
    """Sans accès au compte : la cause la plus fréquente et les plafonds légaux (catalogue sourcé)."""

    normal = cat.parametre_detail("commission_intervention_max")
    fragile = cat.parametre_detail("commission_intervention_max_fragile")
    return (
        "Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une "
        "commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou "
        f"votre découvert autorisé. La loi la plafonne à {euros(normal['valeur'])} par opération et "
        f"{euros(normal['par_mois'])} par mois ({euros(fragile['valeur'])} et {euros(fragile['par_mois'])} pour "
        "la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces "
        "frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y "
        "avez droit, et c'est aussi à lui qu'on conteste un frais."
    )


def gabarit(decision, conseil, profil, etat, message) -> str:
    """Le texte gabarit d'une décision (public : le banc de formulation s'en sert)."""

    if decision.type == "clarifier" and decision.question:
        return decision.question
    if decision.type == "orienter":
        return _gabarit_orientation(decision, profil, etat)
    if decision.type in MESSAGES_FIXES:
        return MESSAGES_FIXES[decision.type]
    if decision.type == "question":
        return _joindre(decision.accroche, *decision.confirmations, RELANCES.get(decision.relance),
                        decision.question, _exemples_de_reponse(decision))
    if decision.type == "question_m3":  # une information indispensable au conseil (Conseil.manque)
        return _joindre(RELANCES.get(decision.relance), questions_m3.question(decision.info))
    if decision.type == "conseil":
        return _joindre(*parties_conseil(decision, conseil), sep="\n\n")
    if decision.type == "fiche":
        return _gabarit_fiche(decision, message)
    raise ValueError(f"type de décision inconnu : {decision.type}")


# ── Point d'entrée ───────────────────────────────────────────────────

def formuler(
    decision: Decision, conseil: Conseil | None,
    profil: dict[str, Any], etat: EtatConversation, message: str,
) -> tuple[str, Etape]:
    """Le texte affiché au client, et l'étape mesurée (avec ou sans appel au LLM)."""

    debut = perf_counter()
    texte = gabarit(decision, conseil, profil, etat, message)
    etape = Etape(nom="formuler", modele="gabarit")
    simple = mots_simples(profil, etat)

    corps, question = parties_conseil(decision, conseil) if decision.type == "conseil" else ("", None)
    if corps and llm.reformulation_active():  # reformuler un conseil : mesuré, écarté ; désactivé par défaut
        etape.modele, etape.appel_llm = llm.MODELE_FORMULATION, True
        try:
            reecrit, etape.tokens, _ = reformuler(corps, llm.MODELE_FORMULATION, simple)
            if reecrit is not None:
                texte = _joindre(reecrit, question, sep="\n\n")
            else:
                etape.modele = f"{llm.MODELE_FORMULATION} (refusé par le garde-fou)"
        except (OSError, KeyError, ValueError):
            etape.modele = f"{llm.MODELE_FORMULATION} (injoignable)"

    if simple:
        texte = simplifier(texte, expliquer_jargon=decision.type != "fiche")
    if decision.type == "conseil" and conseil and conseil.faits.get("hypotheses"):
        # Les hypothèses du calcul, hors LLM : la reformulation ne peut pas les omettre.
        texte = _joindre(texte, " ".join(conseil.faits["hypotheses"]), sep="\n\n")
    if decision.mention_legale:
        texte = _joindre(texte, MENTIONS[decision.mention_legale],
                         sep="\n\n" if simple or "\n\n" in texte else " ")
    etape.latence_ms = (perf_counter() - debut) * 1000
    return texte, etape
