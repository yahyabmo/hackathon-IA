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
from ..taxonomie import LIBELLES_FAMILLES, famille_de
from ..texte import euros, normaliser, pourcent
from . import garde_fou, glossaire
from .dialogue import Decision

MENTIONS = {
    "credit": "Un crédit vous engage et doit être remboursé. "
              "Vérifiez vos capacités de remboursement avant de vous engager.",
}
RAPPEL_CODE = "Rappel : la banque ne vous demandera jamais votre code confidentiel."
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
    "Tu es l'assistant d'une banque française. Reformule le message ci-dessous pour un client, en "
    "français, au vouvoiement, avec des phrases courtes et un ton chaleureux. N'ajoute aucun chiffre, "
    "aucun produit et aucune promesse. Garde tous les chiffres exactement. Termine par la même question."
)
CONSIGNE_SIMPLE = " Le client est peu à l'aise : phrases très courtes, mots de tous les jours."


def mots_simples(profil: dict[str, Any], etat: EtatConversation) -> bool:
    """Le mode « mots simples » s'applique-t-il à ce client ?"""

    return (etat.mots_simples or bool(profil.get("peu_a_laise_en_ligne"))
            or profil.get("age", 0) >= AGE_MOTS_SIMPLES)


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


def _nom(produit_id: str) -> str:
    try:
        return cat.nom(produit_id)
    except KeyError:
        return NOMS_SPECIAUX.get(produit_id, produit_id)


def _date(iso: str) -> str:
    annee, mois, jour = iso.split("-")
    return f"{int(jour)} {MOIS[int(mois) - 1]}"


def _joindre(*morceaux: str | None) -> str:
    return " ".join(m for m in morceaux if m)


# ── Gabarits ──────────────────────────────────────────────────────────

def _conseil_credit_immobilier(faits: dict[str, Any]) -> str:
    texte = (
        f"Avec un prix de {euros(faits['prix_bien'])} et un apport de {euros(faits['apport'])}, il faudrait "
        f"emprunter environ {euros(faits['besoin'])}, frais de notaire estimés à "
        f"{pourcent(faits['taux_frais_notaire'])} compris. Sur {faits['duree_ans']} ans, à un taux indicatif "
        f"de {pourcent(faits['taux_indicatif'])}, la mensualité serait d'environ {euros(faits['mensualite'])}, "
        f"soit {pourcent(faits['taux_effort'])} de vos revenus"
    )
    if faits["taux_effort"] <= faits["taux_effort_max"]:
        return texte + f" : c'est sous les {pourcent(faits['taux_effort_max'])}, le projet paraît finançable."
    return texte + (
        f" : c'est au-delà des {pourcent(faits['taux_effort_max'])} retenus pour un crédit immobilier. "
        f"Avec votre apport, un bien autour de {euros(faits['prix_max'])} resterait dans cette limite. "
        f"Un conseiller peut étudier les leviers : un apport plus élevé, un co-emprunteur, des aides comme "
        f"le PTZ selon conditions."
    )


def _conseil_general(conseil: Conseil) -> str:
    proposes = [p for p in conseil.propositions if p.produit_id != "rdv_conseiller"]
    morceaux = []
    if proposes:
        morceaux.append("Voici ce que je vous propose. " + " ".join(
            f"{_nom(p.produit_id)} : {p.raisons[0][0].lower()}{p.raisons[0][1:]}" for p in proposes if p.raisons))
    if conseil.ecartees:
        morceaux.append("Je ne vous propose pas : " + " ; ".join(
            f"{_nom(e.produit_id)}, {e.raison}" for e in conseil.ecartees) + ".")
    morceaux += conseil.alertes
    return " ".join(morceaux)


def _gabarit_conseil(decision: Decision, conseil: Conseil) -> str:
    if decision.parcours == "credit_immobilier":
        corps = _conseil_credit_immobilier(conseil.faits)
    else:
        corps = _conseil_general(conseil)
    question = f"Voulez-vous qu'un conseiller vous rappelle ? {OUI_NON}" if decision.proposer else None
    return _joindre(corps, question)


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
    if action.outil == "bloquer_carte":
        return _joindre(f"C'est fait : votre carte est en opposition depuis {r['heure']} "
                        f"(référence {r['reference']}). Plus personne ne peut s'en servir, et les opérations "
                        "frauduleuses faites après l'opposition ne sont pas à votre charge. Une nouvelle carte "
                        "peut être commandée depuis votre espace client ou avec un conseiller.", RAPPEL_CODE)
    if action.outil == "preparer_virement":
        if not r.get("ok"):
            return f"Je ne peux pas préparer ce virement : {r['motif']}. Un conseiller peut vous aider."
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
        fiche = glossaire.chercher(message)
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

    if decision.type == "question":
        return _joindre(decision.accroche, *decision.confirmations, RELANCES.get(decision.relance),
                        decision.question)
    if decision.type == "abandon":
        return "D'accord, on laisse ça de côté. Puis-je vous aider pour autre chose ?"
    if decision.type == "conseil":
        return _joindre(decision.accroche, *decision.confirmations, _gabarit_conseil(decision, conseil))
    if decision.type == "action":
        return _gabarit_action_a_confirmer(decision, profil, etat)
    if decision.type == "action_faite":
        return _gabarit_action_faite(action)
    if decision.type == "action_annulee":
        return "D'accord, je ne fais rien. Puis-je vous aider pour autre chose ?"
    if decision.type == "transmettre":
        n = profil.get("contacts_aujourdhui", 0)
        contexte = f"C'est votre {n}e message aujourd'hui : je" if n >= 2 else "Je"
        return _joindre(decision.accroche, f"{contexte} préfère qu'un conseiller reprenne la main, avec le résumé "
                        f"de vos échanges. Voulez-vous qu'il vous rappelle ? {OUI_NON}")
    if decision.type == "fiche":
        return _gabarit_fiche(decision, message)
    if decision.type == "orienter":
        return f"Je préfère ne pas deviner. Voulez-vous qu'un conseiller vous rappelle ? {OUI_NON}"
    # clarifier
    return ("Pour bien vous aider, pouvez-vous préciser ? Par exemple : votre carte, un virement, des frais, "
            "votre épargne ou un projet de crédit.")


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
        systeme = SYSTEME_FORMULATION + (CONSIGNE_SIMPLE if simple else "")
        try:
            reformule, etape.tokens = llm.generer(llm.MODELE_FORMULATION, systeme, texte)
            if not garde_fou.verifier(reformule, set(garde_fou.nombres(texte))):
                texte = reformule
            else:
                etape.modele = f"{llm.MODELE_FORMULATION} (refusé par le garde-fou)"
        except OSError:
            etape.modele = f"{llm.MODELE_FORMULATION} (injoignable)"

    if simple:
        texte = simplifier(texte, expliquer_jargon=decision.type != "fiche")
    if decision.mention_legale:
        texte = (texte + "\n\n" if simple else texte + " ") + MENTIONS[decision.mention_legale]
    etape.latence_ms = (perf_counter() - debut) * 1000
    return texte, etape
