"""Moteur de règles : éligibilité, pertinence, classement, raisons et écarts.

Une décision financière doit être reproductible et justifiable : aucune règle
n'appelle de LLM. Chaque nombre qu'une réponse peut citer est rangé dans
``Conseil.faits`` ; le garde-fou de la formulation refuse tout autre nombre.

Implémentations de référence (crédit immobilier complet, épargne simplifiée) :
à compléter par M3, notamment avec le modèle d'appétence pour le classement.
"""

from __future__ import annotations

from typing import Any

from ..contrats import Conseil, Ecart, Proposition
from ..texte import euros, pourcent
from . import catalogue as cat


def _annuite(taux_annuel: float, mois: int) -> float:
    """Capital remboursé par 1 € de mensualité : (1 - (1 + i)^-n) / i."""

    i = taux_annuel / 12
    return (1 - (1 + i) ** -mois) / i


def credit_immobilier(profil: dict[str, Any], slots: dict[str, Any]) -> Conseil:
    revenus = slots["revenus_nets"]
    en_cours = slots.get("mensualites_en_cours", 0)
    prix, apport = slots["prix_bien"], slots["apport"]
    effort_max = cat.parametre("taux_effort_max")
    duree_ans = cat.parametre("duree_max_credit_immobilier_ans")
    notaire = cat.parametre("frais_notaire_ancien")
    taux = cat.parametre("taux_indicatif_credit_immobilier")

    facteur = _annuite(taux, duree_ans * 12)
    besoin = max(prix * (1 + notaire) - apport, 0)
    mensualite = besoin / facteur
    effort = (mensualite + en_cours) / revenus
    mensualite_max = max(effort_max * revenus - en_cours, 0)
    prix_max = round((mensualite_max * facteur + apport) / (1 + notaire), -3)

    conseil = Conseil(faits={
        "prix_bien": prix, "apport": apport, "revenus_nets": revenus,
        "mensualites_en_cours": en_cours, "taux_frais_notaire": notaire,
        "besoin": round(besoin), "taux_indicatif": taux, "duree_ans": duree_ans,
        "mensualite": round(mensualite), "taux_effort": round(effort, 4),
        "taux_effort_max": effort_max, "prix_max": prix_max,
    })
    sources = [cat.source_parametre("taux_effort_max"), cat.source_parametre("taux_indicatif_credit_immobilier")]
    if effort <= effort_max:
        conseil.propositions.append(Proposition(
            "credit_immobilier",
            raisons=[f"Mensualité estimée à {euros(mensualite)} sur {duree_ans} ans, soit {pourcent(effort)} "
                     f"de vos revenus : sous les {pourcent(effort_max)}."],
            sources=sources,
        ))
    else:
        conseil.alertes.append(
            f"Taux d'effort de {pourcent(effort)} : au-delà des {pourcent(effort_max)} retenus pour un crédit immobilier."
        )
        conseil.ecartees.append(Ecart(
            "credit_immobilier",
            f"mensualité d'environ {euros(mensualite)}, soit {pourcent(effort)} de vos revenus "
            f"(maximum {pourcent(effort_max)})",
            "HCSF-taux-effort",
        ))
    conseil.propositions.append(Proposition(
        "rdv_conseiller",
        raisons=[f"Avec votre apport, un bien autour de {euros(prix_max)} resterait sous les {pourcent(effort_max)}.",
                 "Un conseiller étudie les leviers (apport, co-emprunteur, aides comme le PTZ selon conditions) et décide."],
        sources=sources,
    ))
    conseil.ecartees.append(Ecart(
        "credit_immobilier_30_ans", f"au-delà de la durée maximale de {duree_ans} ans", "HCSF-duree",
    ))
    return conseil


def credit_conso(profil: dict[str, Any], slots: dict[str, Any]) -> Conseil:
    revenus, en_cours = slots["revenus_nets"], slots.get("mensualites_en_cours", 0)
    montant, mois = slots["montant"], slots["duree_mois"]
    effort_max = cat.parametre("taux_effort_max")
    taux = cat.parametre("taux_indicatif_pret_personnel")
    mensualite = montant / _annuite(taux, mois)
    effort = (mensualite + en_cours) / revenus

    conseil = Conseil(faits={
        "montant": montant, "duree_mois": mois, "taux_indicatif": taux, "mensualite": round(mensualite),
        "mensualites_en_cours": en_cours, "revenus_nets": revenus, "taux_effort": round(effort, 4),
        "taux_effort_max": effort_max,
    })
    raison_effort = (f"Mensualité estimée à {euros(mensualite)} sur {mois} mois ; avec votre crédit en cours "
                     f"({euros(en_cours)} par mois), {pourcent(effort)} de vos revenus.")
    if effort <= effort_max:
        conseil.propositions.append(Proposition("pret_personnel", raisons=[raison_effort],
                                                sources=[cat.source_produit("pret_personnel")]))
    else:
        conseil.ecartees.append(Ecart("pret_personnel", raison_effort + f" Au-delà de {pourcent(effort_max)}.",
                                      "taux-effort"))
        conseil.alertes.append(f"Taux d'effort de {pourcent(effort)} : prudence, l'endettement serait trop élevé.")
    conseil.propositions.append(Proposition("rdv_conseiller", raisons=["Un conseiller étudie la demande et décide."]))
    return conseil


def epargne_projet(profil: dict[str, Any], slots: dict[str, Any]) -> Conseil:
    pour_enfants = slots.get("pour_qui") in ("enfants", "enfant", "fils", "fille") and profil.get("enfants")
    age = profil["age"]
    livrets = profil.get("livrets", {})
    conseil = Conseil(faits={
        "horizon_mois": slots.get("horizon_mois"), "montant_mensuel": slots.get("montant_mensuel"),
        "plafond_livret_a": cat.produit("livret_a")["plafond"],
        "plafond_livret_jeune": cat.produit("livret_jeune")["plafond"],
        "plafond_ldds": cat.produit("ldds")["plafond"], "ages_enfants": profil.get("enfants", []),
    })

    if pour_enfants:
        conseil.propositions.append(Proposition(
            "livret_a", raisons=["Ouvrable au nom de chaque enfant mineur ; argent disponible ; intérêts sans impôt."],
            sources=[cat.source_produit("livret_a")]))
        for age_enfant in profil["enfants"]:
            if 12 <= age_enfant <= 25:
                conseil.propositions.append(Proposition(
                    "livret_jeune", raisons=[f"Votre enfant de {age_enfant} ans peut en ouvrir un (de 12 à 25 ans)."],
                    sources=[cat.source_produit("livret_jeune")]))
        conseil.ecartees += [
            Ecart("ldds", "réservé aux majeurs", "LDDS-age"),
            Ecart("lep", "réservé aux personnes sous un plafond de revenu fiscal, pas ouvert à un enfant", "LEP-revenu"),
        ]
        return conseil

    if 12 <= age <= 25:
        conseil.propositions.append(Proposition(
            "livret_jeune", raisons=[f"Vous avez {age} ans : le Livret Jeune est réservé aux 12-25 ans."],
            sources=[cat.source_produit("livret_jeune")], score=1.0))
    else:
        conseil.ecartees.append(Ecart("livret_jeune", "réservé aux 12-25 ans", "LJ-age"))
    for produit_id, regle in (("livret_a", "LA-plafond"), ("ldds", "LDDS-plafond")):
        plafond = cat.produit(produit_id)["plafond"]
        if age < cat.produit(produit_id).get("age_min", 0):
            conseil.ecartees.append(Ecart(produit_id, "réservé aux majeurs", "LDDS-age"))
        elif livrets.get(produit_id, 0) >= plafond:
            conseil.ecartees.append(Ecart(produit_id, "plafond déjà atteint", regle))
        else:
            conseil.propositions.append(Proposition(
                produit_id, raisons=["Argent disponible à tout moment ; intérêts sans impôt."],
                sources=[cat.source_produit(produit_id)], score=0.8))
    if cat.parametre("plafond_revenu_lep") is None:
        conseil.ecartees.append(Ecart("lep", "éligibilité à vérifier : le plafond de revenu n'est pas encore renseigné",
                                      "LEP-revenu"))
    conseil.ecartees.append(Ecart("pel", "adapté à un projet immobilier ; l'argent n'est pas disponible avant la fin du plan",
                                  "PEL-objectif"))
    conseil.propositions.sort(key=lambda p: p.score or 0, reverse=True)
    return conseil


def pret_etudiant(profil: dict[str, Any], slots: dict[str, Any]) -> Conseil:
    conseil = Conseil(faits={"age": profil["age"], "montant": slots.get("montant")})
    if profil["metier"].startswith("étudiant") and profil["age"] >= 18:
        conseil.propositions.append(Proposition(
            "pret_etudiant",
            raisons=["Vous êtes étudiant et majeur : un prêt étudiant est possible, avec un remboursement "
                     "qui peut être différé à la fin des études.",
                     "Une version garantie par l'État existe, sous conditions : un conseiller vérifie l'éligibilité."],
            sources=[cat.source_produit("pret_etudiant")]))
    else:
        conseil.ecartees.append(Ecart("pret_etudiant", "réservé aux étudiants majeurs", "PE-statut"))
    if 12 <= profil["age"] <= 25:
        conseil.propositions.append(Proposition(
            "livret_jeune", raisons=["Pour commencer à épargner : réservé aux 12-25 ans."],
            sources=[cat.source_produit("livret_jeune")]))
    conseil.propositions.append(Proposition("rdv_conseiller", raisons=["Un conseiller monte le dossier avec vous."]))
    return conseil


REGLES = {
    "credit_immobilier": credit_immobilier,
    "credit_conso": credit_conso,
    "epargne_projet": epargne_projet,
    "pret_etudiant": pret_etudiant,
}
