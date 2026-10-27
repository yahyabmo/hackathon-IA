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
from ..contrats import Action, Conseil, Etape, EtatConversation
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
SIMULATION = "Simulation uniquement : aucune opération réelle ni rappel réel."
MESSAGES_FIXES = {
    "abandon": "D'accord, on laisse ça de côté. Puis-je vous aider pour autre chose ?",
    "action_annulee": "D'accord, je ne fais rien. Puis-je vous aider pour autre chose ?",
    "montant_ambigu": ("Montant ambigu ou négatif : aucune opération effectuée. Utilisez un montant positif "
                       "avec une virgule pour les centimes, puis confirmez de nouveau."),
    "confirmation_attendue": ("Aucune opération effectuée. Confirmez la demande présentée par « oui » ou "
                              "annulez par « non »."),
    "un_seul_montant": "Indiquez un seul montant corrigé ; une nouvelle confirmation sera demandée.",
    "orienter": "Je préfère ne pas deviner. Voulez-vous qu'un conseiller vous rappelle ? (oui / non)",
    "clarifier": ("Pour bien vous aider, pouvez-vous préciser ? Par exemple : votre carte, un virement, des "
                  "frais, votre épargne ou un projet de crédit."),
}
OUI_NON = "(oui / non)"
NOMS_SPECIAUX = {"credit_immobilier_30_ans": "Un prêt immobilier sur 30 ans"}
AGE_MOTS_SIMPLES = 70
RELANCES = {
    "incompris": "Je n'ai pas bien compris.",
    "ne_sait_pas": "Pas de souci, une estimation suffit.",
}
MOIS = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre")

SYSTEME_FORMULATION = (
    "Tu es l'assistant d'une banque française. On te donne un message déjà rédigé pour un client. "
    "Réécris-le en français, au vouvoiement, avec des phrases courtes et un ton chaleureux. Garde "
    "toutes les informations et tous les chiffres exactement ; n'ajoute aucun chiffre, aucun produit "
    "et aucune promesse. Termine par la même question. Réponds uniquement par le message réécrit."
)
CONSIGNE_MESSAGE = 'Message à réécrire :\n"""\n{texte}\n"""'
LONGUEUR_MIN_RELATIVE = 0.4
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
    reecrit, tokens = llm.generer(modele, systeme, CONSIGNE_MESSAGE.format(texte=texte))
    reecrit = reecrit.strip().strip('"').strip()
    reference = set(garde_fou.nombres(texte))
    problemes = garde_fou.verifier(reecrit, reference, obligatoires=reference,
                                   longueur_min=int(LONGUEUR_MIN_RELATIVE * len(texte)))
    return (None if problemes else reecrit), tokens, problemes


def simplifier(texte: str, expliquer_jargon: bool = True) -> str:
    """Une phrase par paragraphe, sans aparté, et le premier terme technique expliqué."""

    texte = re.sub(r"\s*\((?!oui / non\))[^)]*\)", "", texte)
    phrases = [p.strip() for p in re.split(r"(?<=[.?!])\s+(?!\()", texte) if p.strip()]
    if expliquer_jargon:
        fiche = glossaire.chercher(texte)
        if fiche:
            explication = fiche["explication"]
            phrases.append(f"« {fiche['terme']} » veut dire : {explication[0].lower()}{explication[1:]}")
    return "\n\n".join(phrases)


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


def _gabarit_conseil(decision: Decision, conseil: Conseil) -> str:
    """Le même gabarit pour tous les parcours : les règles de M3 calculent les raisons, les
    écarts et les alertes (assurance inconnue, frais non couverts…), le gabarit les restitue."""

    question = f"Voulez-vous qu'un conseiller vous rappelle ? {OUI_NON}" if decision.proposer else None
    return _joindre(_conseil_general(conseil), question, sep="\n\n")


def _gabarit_action_a_confirmer(decision: Decision, profil: dict[str, Any], etat: EtatConversation) -> str:
    if decision.outil == "bloquer_carte":
        return _joindre(decision.accroche, "Je peux faire opposition sur votre carte maintenant : plus aucun "
                        f"paiement ne sera possible avec. Confirmez-vous ? {OUI_NON}")
    if decision.outil == "preparer_virement":
        lien, montant = etat.slots.get("beneficiaire"), etat.slots.get("montant")
        connu = next((b for b in profil.get("beneficiaires", []) if b["lien"] == lien), None)
        vers = f"votre {lien}, {connu['nom']}" if connu else f"votre {lien}"
        return _joindre(decision.accroche, f"Je récapitule : un virement de {euros(montant)} vers {vers}. "
                        f"Confirmez-vous ? {OUI_NON}", RAPPEL_CODE)
    return _joindre(decision.accroche, f"Confirmez-vous ? {OUI_NON}")


def _gabarit_action_faite(action: Action) -> str:
    r = action.resultat or {}
    if r.get("statut") == "echec":
        return f"L'opération simulée n'a pas pu aboutir : {r.get('motif', 'erreur interne')}. Rien n'a été modifié."
    if r.get("ok") is False:
        return f"Opération simulée refusée : {r.get('motif', 'demande invalide')}."
    return _joindre(_gabarit_action_reussie(action), SIMULATION, r.get("limites"), sep="\n\n")


def _gabarit_action_reussie(action: Action) -> str:
    r = action.resultat or {}
    if action.outil == "bloquer_carte":
        return _joindre(f"C'est fait : votre carte est en opposition depuis {r['heure']} "
                        f"(référence {r['reference']}). Plus personne ne peut s'en servir, et les opérations "
                        "frauduleuses faites après l'opposition ne sont pas à votre charge. Une nouvelle carte "
                        "peut être commandée depuis votre espace client ou avec un conseiller.", RAPPEL_CODE)
    if action.outil == "preparer_virement":
        return (f"C'est fait : le virement de {euros(r['montant'])} vers {r['beneficiaire']} "
                f"({r['iban_masque']}) est enregistré, référence {r['reference']}.")
    if action.outil == "expliquer_frais":
        if not r["frais"]:
            return "Je ne trouve aucun frais ce mois-ci sur votre compte."
        lignes = " ".join(f"Le {_date(f['date'])}, une {f['libelle']} de {euros(f['montant'])} : {f['cause']}."
                          for f in r["frais"])
        loi = (f"La loi plafonne ces commissions à {euros(r['plafond_operation'])} par opération "
               f"et {euros(r['plafond_mois'])} par mois.")
        fragile = None
        if r["proposer_offre_fragile"]:
            fragile = (f"Vous avez eu {r['decouverts_12_mois']} découverts en 12 mois : un conseiller peut vous "
                       f"présenter l'offre clientèle fragile, qui limite ces frais à "
                       f"{euros(r['plafond_fragile_operation'])} par opération et "
                       f"{euros(r['plafond_fragile_mois'])} par mois. Voulez-vous qu'il vous rappelle ? {OUI_NON}")
        return _joindre(lignes, loi, fragile)
    if action.outil == "transmettre_conseiller":
        return (f"C'est noté : un conseiller va vous rappeler (demande {r['ticket']}). Il aura le résumé de "
                "notre échange, vous n'aurez pas à tout répéter.")
    return "C'est fait."


def _gabarit_fiche(decision: Decision, message: str) -> str:
    if decision.parcours == "question_definition":
        fiche = glossaire.chercher(message, approchant=True)
        if fiche:
            return f"{fiche['terme']} : {fiche['explication']}"
        return "Je n'ai pas encore de fiche sur ce terme : un conseiller pourra vous l'expliquer."
    if decision.parcours == "hors_sujet":
        debut = "Avec plaisir !" if "merci" in normaliser(message) else "Bonjour !"
        return (f"{debut} Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un "
                "projet de crédit. Que puis-je faire pour vous ?")
    sujet = LIBELLES_FAMILLES.get(famille_de(decision.parcours or ""), "ce sujet")
    return (f"Je comprends que votre demande concerne {sujet}. Je n'ai pas encore de parcours guidé pour ce "
            f"point : un conseiller peut le traiter. Voulez-vous qu'il vous rappelle ? {OUI_NON}")


def gabarit(decision, conseil, action, profil, etat, message) -> str:
    """Le texte gabarit d'une décision (public : le banc de formulation s'en sert)."""

    if decision.type in MESSAGES_FIXES:
        return MESSAGES_FIXES[decision.type]
    if decision.type == "question":
        return _joindre(decision.accroche, *decision.confirmations, RELANCES.get(decision.relance),
                        decision.question)
    if decision.type == "question_m3":  # une information indispensable au conseil (Conseil.manque)
        return _joindre(RELANCES.get(decision.relance), questions_m3.question(decision.info))
    if decision.type == "conseil":
        return _joindre(decision.accroche, *decision.confirmations, _gabarit_conseil(decision, conseil))
    if decision.type == "action":
        return _gabarit_action_a_confirmer(decision, profil, etat)
    if decision.type == "action_faite":
        return _gabarit_action_faite(action)
    if decision.type == "transmettre":
        n = profil.get("contacts_aujourdhui", 0)
        contexte = f"C'est votre {n}e message aujourd'hui : je" if n >= 2 else "Je"
        return _joindre(decision.accroche, f"{contexte} préfère qu'un conseiller reprenne la main, avec le résumé "
                        f"de vos échanges. Voulez-vous qu'il vous rappelle ? {OUI_NON}")
    if decision.type == "fiche":
        return _gabarit_fiche(decision, message)
    raise ValueError(f"type de décision inconnu : {decision.type}")


# ── Point d'entrée ───────────────────────────────────────────────────

def formuler(
    decision: Decision, conseil: Conseil | None, action: Action | None,
    profil: dict[str, Any], etat: EtatConversation, message: str,
) -> tuple[str, Etape]:
    """Le texte affiché au client, et l'étape mesurée (avec ou sans appel au LLM)."""

    debut = perf_counter()
    texte = gabarit(decision, conseil, action, profil, etat, message)
    etape = Etape(nom="formuler", modele="gabarit")
    simple = mots_simples(profil, etat)

    if decision.type == "conseil" and llm.actif():
        etape.modele, etape.appel_llm = llm.MODELE_FORMULATION, True
        try:
            reecrit, etape.tokens, _ = reformuler(texte, llm.MODELE_FORMULATION, simple)
            if reecrit is not None:
                texte = reecrit
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
