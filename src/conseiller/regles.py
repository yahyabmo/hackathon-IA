"""Conseils déterministes : données inconnues explicites, estimations sans décision d'octroi."""
from __future__ import annotations

import math
from typing import Any

from ..contrats import Conseil, Ecart, Proposition
from ..texte import euros, pourcent
from . import catalogue as cat
from .validation import nombre


def _annuite(taux_annuel: float, mois: int) -> float:
    """Facteur d'amortissement constant ; taux zéro traité sans division."""
    taux = nombre(taux_annuel, maximum=1)
    n = nombre(mois, minimum=1, maximum=600, entier=True)
    if taux == 0:
        return n
    i = taux / 12
    return -math.expm1(-n * math.log1p(i)) / i


def _valeurs(conseil: Conseil, donnees: dict, specs: dict) -> dict[str, float]:
    valeurs = {}
    for cle, options in specs.items():
        try:
            valeurs[cle] = nombre(donnees.get(cle), **options)
        except ValueError:
            conseil.manque.append(cle)
            conseil.alertes.append(f"Information absente ou invalide : {cle}.")
    return valeurs


def _rdv(c: Conseil, raison: str = "Un conseiller vérifie les justificatifs et décide ; cette orientation ne vaut pas accord.") -> None:
    c.propositions.append(Proposition("rdv_conseiller", raisons=[raison],
                                      sources=[cat.source_produit("rdv_conseiller")]))


def _taux(c: Conseil, slots: dict, cle: str) -> float | None:
    fiche = cat.parametre_detail(cle)
    valeur = slots.get("taux_annuel", fiche["valeur"] if fiche["statut"] == "verifie" else None)
    try:
        taux = nombre(valeur, maximum=1)
    except ValueError:
        c.manque.append("taux_annuel")
        return None
    c.faits["source_taux"] = ("Hypothèse fournie par le client, non vérifiée" if "taux_annuel" in slots
                              else fiche["source"])
    c.faits["date_taux"] = fiche["releve_le"] if "taux_annuel" not in slots else None
    c.faits["hypotheses"].append(
        f"Taux annuel de {pourcent(taux)} : " + ("hypothèse fournie par le client." if "taux_annuel" in slots
        else f"repère statistique Banque de France, période {fiche.get('periode', '')}, relevé le {fiche['releve_le']}."))
    return taux


def _credit(profil: dict[str, Any], slots: dict[str, Any], immobilier: bool) -> Conseil:
    c = Conseil(faits={"hypotheses": [], "decision_bancaire": False})
    donnees = {"revenus_nets": profil.get("revenus_nets"),
               "mensualites_en_cours": profil.get("mensualites_credits"), **slots}
    specs = {"revenus_nets": {"strict": True}, "mensualites_en_cours": {}}
    if immobilier:
        specs.update({"prix_bien": {"strict": True}, "apport": {},
                      "duree_ans": {"minimum": 1, "maximum": 50, "entier": True}})
        donnees.setdefault("duree_ans", cat.parametre("duree_max_credit_immobilier_ans"))
    else:
        specs.update({"montant": {"strict": True}, "duree_mois": {"minimum": 1, "maximum": 600, "entier": True}})
    v = _valeurs(c, donnees, specs)
    age = _valeurs(c, profil, {"age": {"maximum": 120, "entier": True}}).get("age")
    taux = _taux(c, slots, "taux_indicatif_credit_immobilier" if immobilier else "taux_indicatif_pret_personnel")
    assurance = slots.get("assurance_mensuelle")
    assurance_connue = assurance is not None
    if assurance_connue:
        assurance = _valeurs(c, slots, {"assurance_mensuelle": {}}).get("assurance_mensuelle")
    else:
        assurance = 0
        c.alertes.append("Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise.")
    if c.manque:
        return c
    produit = "credit_immobilier" if immobilier else "pret_personnel"
    if age < 18:
        c.ecartees.append(Ecart(produit, "Le titulaire est mineur : étude avec un représentant et un conseiller.", "CREDIT-majorite"))
        _rdv(c)
        return c
    if immobilier:
        duree = int(v["duree_ans"])
        limite = cat.parametre("duree_max_credit_immobilier_ans")
        if duree > limite:
            c.ecartees.append(Ecart(produit, "Durée hors du cadre général modélisé ; cas particuliers à examiner par la banque.", "HCSF-duree"))
            _rdv(c)
            return c
        nature = slots.get("type_bien", "ancien")
        if nature not in ("ancien", "neuf"):
            c.manque.append("type_bien")
            return c
        cle_frais = "frais_notaire_" + nature
        frais = _valeurs(c, {"taux_frais_notaire": slots.get("taux_frais_notaire", cat.parametre(cle_frais))},
                        {"taux_frais_notaire": {"maximum": 1}}).get("taux_frais_notaire")
        if c.manque:
            return c
        besoin = max(v["prix_bien"] * (1 + frais) - v["apport"], 0)
        mois = duree * 12
        c.faits.update(prix_bien=v["prix_bien"], apport=v["apport"], taux_frais_notaire=frais, duree_ans=duree)
        c.faits["hypotheses"].append(f"Bien {nature}, frais d'acquisition estimés à {pourcent(frais)} ; estimation à confirmer par un notaire.")
        c.faits["source_frais"] = cat.source_parametre(cle_frais)
        if besoin == 0:
            c.faits["besoin"] = 0
            c.ecartees.append(Ecart(produit, "L'apport couvre le prix et les frais estimés : aucun emprunt nécessaire dans cette simulation.", "CREDIT-besoin-nul"))
            _rdv(c)
            return c
        seuil = cat.parametre("taux_effort_max")
    else:
        besoin, mois = v["montant"], int(v["duree_mois"])
        seuil = cat.parametre("seuil_prudence_conso")
        c.faits.update(montant=besoin, duree_mois=mois)
        c.alertes.append("Le seuil de prudence consommation est une heuristique interne, pas une obligation HCSF.")
    facteur = _annuite(taux, mois)
    hors_assurance = besoin / facteur
    mensualite = hors_assurance + assurance
    effort = (mensualite + v["mensualites_en_cours"]) / v["revenus_nets"]
    c.faits.update(besoin=round(besoin, 2), revenus_nets=v["revenus_nets"],
                   mensualites_en_cours=v["mensualites_en_cours"], taux_indicatif=taux,
                   mensualite=round(mensualite, 2), mensualite_hors_assurance=round(hors_assurance, 2),
                   assurance_mensuelle=assurance if assurance_connue else None,
                   assurance_connue=assurance_connue, taux_effort=effort, taux_effort_max=seuil)
    c.faits["hypotheses"].append("Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre.")
    if profil.get("revenus_nature") != "net_avant_impot":
        c.alertes.append("La nature des revenus nets avant impôt doit être confirmée.")
    sources = [cat.source_produit(produit), c.faits["source_taux"]]
    base = f"Mensualité indicative de {euros(mensualite)} sur {mois} mois, soit {pourcent(effort)} des revenus avec les crédits en cours."
    if effort <= seuil:
        c.propositions.append(Proposition(produit, [base + " Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants."], sources))
    else:
        c.alertes.append(f"Taux d'effort indicatif de {pourcent(effort)} : au-delà du repère de {pourcent(seuil)}.")
        c.ecartees.append(Ecart(produit, base + " Projet non retenu dans cette simulation ; aucun refus bancaire n'est prononcé.",
                               "HCSF-taux-effort" if immobilier else "PRUDENCE-conso"))
    if immobilier:
        disponible = max(seuil * v["revenus_nets"] - v["mensualites_en_cours"] - assurance, 0)
        prix_max = (disponible * facteur + v["apport"]) / (1 + frais)
        c.faits["prix_max"] = math.floor(prix_max / 1000) * 1000
        c.alertes.append(f"Budget indicatif sous ces hypothèses : environ {euros(c.faits['prix_max'])}. Assurance inconnue : budget à réviser." if not assurance_connue
                         else f"Budget indicatif sous ces hypothèses : environ {euros(c.faits['prix_max'])}.")
        c.ecartees.append(Ecart("credit_immobilier_30_ans", "Option de durée hors du cadre général de 25 ans modélisé.", "HCSF-duree"))
        c.alertes.append("Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque.")
    _rdv(c)
    return c


def credit_immobilier(profil: dict[str, Any], slots: dict[str, Any]) -> Conseil:
    return _credit(profil, slots, True)


def credit_conso(profil: dict[str, Any], slots: dict[str, Any]) -> Conseil:
    return _credit(profil, slots, False)



# Libellés lisibles des informations à vérifier : le client ne voit jamais un nom de champ.
LIBELLES_A_VERIFIER = {
    "situation_fiscale_enfants": "situation fiscale des enfants",
    "rfr_enfants": "revenu fiscal des enfants",
    "residence_france": "résidence en France",
    "domicile_fiscal_france": "domicile fiscal en France",
    "rattache_foyer_parents": "rattachement au foyer fiscal des parents",
    "revenus_personnels": "revenus personnels",
    "rfr": "revenu fiscal de référence",
    "parts_fiscales": "nombre de parts fiscales",
    "annee_rfr": "année du revenu fiscal",
    "territoire_fiscal": "territoire fiscal",
    "conditions_catalogue_non_verifiees": "conditions du produit non vérifiées",
}


def _libelle_a_verifier(champ: str) -> str:
    if champ.startswith("solde_"):
        return "solde actuel du livret"
    return LIBELLES_A_VERIFIER.get(champ, champ.replace("_", " "))

def epargne_projet(profil: dict[str, Any], slots: dict[str, Any]) -> Conseil:
    c = Conseil(faits={"eligibilite": {}, "a_verifier": [], "hypotheses": [],
                        "classement": "priorités heuristiques, pas probabilités"})
    v = _valeurs(c, slots, {"horizon_mois": {"minimum": 1, "maximum": 1200, "entier": True},
                           "montant_mensuel": {"strict": True}})
    age = _valeurs(c, profil, {"age": {"maximum": 120, "entier": True}}).get("age")
    liquidite = slots.get("besoin_liquidite", True)
    if type(liquidite) is not bool:
        c.manque.append("besoin_liquidite")
    if c.manque:
        return c
    c.faits.update(v, age=age, besoin_liquidite=liquidite)
    if "besoin_liquidite" not in slots:
        c.faits["hypotheses"].append("Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.")
    c.alertes.append("Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus.")
    livrets = profil.get("livrets", {})
    if not isinstance(livrets, dict):
        c.manque.append("livrets")
        return c

    def exclure(pid: str, raison: str, regle: str) -> None:
        c.ecartees.append(Ecart(pid, raison, regle))
        c.faits["eligibilite"][pid] = "ecarte"

    def inconnu(pid: str, champs: list[str]) -> None:
        c.faits["eligibilite"][pid] = "inconnue"
        c.faits["a_verifier"].extend(champs)
        libelles = ", ".join(_libelle_a_verifier(champ) for champ in champs)
        c.alertes.append(f"{cat.nom(pid)} : éligibilité à vérifier ({libelles}), aucune inéligibilité déduite.")

    def proposer(pid: str, raison: str, score: float) -> None:
        p = cat.produit(pid)
        if p["statut"] != "verifie":
            inconnu(pid, ["conditions_catalogue_non_verifiees"])
            return
        try:
            solde = nombre(livrets.get(pid, 0))
        except ValueError:
            inconnu(pid, ["solde_" + pid])
            return
        plafond = p.get("plafond")
        if plafond is not None:
            c.faits["plafond_" + pid] = plafond
            disponible = max(plafond - solde, 0)
            c.faits["place_" + pid] = disponible
            if disponible == 0:
                exclure(pid, "Plafond des versements atteint ; aucun nouveau versement proposé.", "PLAFOND")
                return
            if pid in livrets:
                raison = "Alimenter le livret existant, sans en ouvrir un second. " + raison
            if v["montant_mensuel"] * v["horizon_mois"] > disponible:
                raison += f" Les versements prévus dépassent la place disponible de {euros(disponible)} ; prévoir une répartition."
        c.propositions.append(Proposition(pid, [raison], [cat.source_produit(pid)], score))
        c.faits["eligibilite"][pid] = "orientation_conditionnelle"

    enfants = slots.get("pour_qui") in ("enfants", "enfant", "fils", "fille")
    if enfants:
        ages = profil.get("enfants", [])
        if not ages:
            c.manque.append("ages_enfants")
            return c
        try:
            for a in ages:
                nombre(a, maximum=120, entier=True)
        except ValueError:
            c.manque.append("ages_enfants")
            return c
        # Les avoirs du parent ne sont pas ceux des enfants.
        livrets = {}
        c.faits["ages_enfants"] = list(ages)
        proposer("livret_a", "Piste au nom de chaque enfant ; vérifier l'absence de Livret A déjà détenu et les représentants légaux.", 1)
        if any(12 <= a <= 25 for a in ages):
            proposer("livret_jeune", "Piste pour l'enfant de 12 à 25 ans, sous réserve de résidence en France et d'absence de livret identique.", .9)
        else:
            exclure("livret_jeune", "Aucun enfant dans la tranche d'âge de 12 à 25 ans.", "LJ-age")
        inconnu("ldds", ["situation_fiscale_enfants"])
        inconnu("lep", ["situation_fiscale_enfants", "rfr_enfants"])
        c.alertes.append("Les soldes et la situation fiscale des enfants ne sont pas connus ; ne pas utiliser ceux du parent.")
        return c

    jeune = cat.produit("livret_jeune")
    if not jeune["age_min"] <= age <= jeune["age_max"]:
        exclure("livret_jeune", "Hors de la tranche d'âge du Livret Jeune.", "LJ-age")
    elif profil.get("residence_france") is True:
        proposer("livret_jeune", f"À {int(age)} ans, tranche d'âge compatible ; épargne disponible.", 1)
    elif profil.get("residence_france") is False:
        exclure("livret_jeune", "Résidence habituelle hors de France déclarée.", "LJ-residence")
    else:
        inconnu("livret_jeune", ["residence_france"])
    proposer("livret_a", "Épargne disponible ; adaptée à une réserve ou un projet sans immobilisation.", .8)
    domicile = slots.get("domicile_fiscal_france", profil.get("domicile_fiscal_france"))
    rattache = slots.get("rattache_foyer_parents", profil.get("rattache_foyer_parents"))
    for pid in ("ldds", "lep"):
        if pid == "lep" and age < cat.produit(pid)["age_min"]:
            exclure(pid, "Le titulaire est mineur ; ouverture du LEP non proposée.", "LEP-age")
        elif domicile is False or rattache is True:
            exclure(pid, "Domicile fiscal français et imposition séparée nécessaires.", "FISCALITE")
        elif domicile is not True or rattache is not False:
            inconnu(pid, ["domicile_fiscal_france", "rattache_foyer_parents"])
        elif pid == "ldds":
            if age < 18 and profil.get("revenus_personnels") is not True:
                inconnu(pid, ["revenus_personnels"])
            else:
                proposer(pid, "Domicile fiscal français et imposition séparée déclarés ; épargne disponible.", .7)
        else:
            table = cat.parametre_detail("plafond_revenu_lep")
            fiscal = {k: slots.get(k, profil.get(k)) for k in ("rfr", "parts_fiscales", "annee_rfr", "territoire_fiscal")}
            try:
                rfr = nombre(fiscal["rfr"])
                parts = nombre(fiscal["parts_fiscales"], strict=True, maximum=20)
                annee = nombre(fiscal["annee_rfr"], minimum=1900, maximum=2100, entier=True)
                plafond = table["plafonds"].get(f"{parts:g}")
                if fiscal["territoire_fiscal"] != table["territoire"] or annee not in (table["annee"]-1, table["annee"]-2) or plafond is None:
                    raise ValueError()
            except ValueError:
                inconnu(pid, ["rfr", "parts_fiscales", "annee_rfr", "territoire_fiscal"])
                continue
            c.faits.update(rfr=rfr, plafond_rfr_lep=plafond)
            if rfr > plafond:
                exclure(pid, "RFR fourni au-dessus du plafond d'ouverture correspondant ; autre avis ou maintien d'un livret existant à vérifier.", "LEP-RFR")
            else:
                proposer(pid, "Conditions fiscales déclarées compatibles avec la table d'ouverture ; justificatifs à contrôler.", 1.1)
    pel = cat.produit("pel")
    if liquidite or v["horizon_mois"] < pel["horizon_min_mois"]:
        exclure("pel", "Besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages.", "PEL-liquidite")
    elif v["montant_mensuel"] * 12 < pel["versement_annuel_min"]:
        exclure("pel", "Versements annoncés insuffisants pour le minimum annuel du plan.", "PEL-versements")
    else:
        proposer("pel", "Horizon long et absence de besoin immédiat de liquidité déclarés ; versement initial et conditions du plan à vérifier.", .9)
    if slots.get("objectif") == "immobilier":
        proposer("cel", "Piste épargne logement avec disponibilité sous réserve du solde minimum ; conditions et fiscalité à étudier.", .6)
    c.propositions.sort(key=lambda p: p.score or 0, reverse=True)
    return c


def pret_etudiant(profil: dict[str, Any], slots: dict[str, Any]) -> Conseil:
    c = Conseil(faits={"hypotheses": [], "decision_bancaire": False})
    v = _valeurs(c, {**profil, **slots}, {"age": {"maximum": 120, "entier": True}, "montant": {"strict": True}})
    if c.manque:
        return c
    c.faits.update(v)
    produit = cat.produit("pret_etudiant")
    if "duree_mois" in slots:
        _valeurs(c, slots, {"duree_mois": {"minimum": produit["duree_min_mois"],
                                          "maximum": produit["duree_max_mois"], "entier": True}})
        if c.manque:
            return c
    etudiant = slots.get("est_etudiant", profil.get("est_etudiant"))
    if not produit["age_min"] <= v["age"] <= produit["age_max"]:
        c.ecartees.append(Ecart("pret_etudiant", "Âge hors des conditions de l'offre LBP référencée.", "PE-age"))
    elif etudiant is False:
        c.ecartees.append(Ecart("pret_etudiant", "Statut étudiant non déclaré.", "PE-statut"))
    elif etudiant is not True:
        c.manque.append("est_etudiant")
    elif v["montant"] < produit["montant_min"]:
        c.ecartees.append(Ecart("pret_etudiant", "Montant inférieur au minimum de l'offre référencée.", "PE-montant"))
    else:
        c.propositions.append(Proposition("pret_etudiant",
            ["Piste LBP compatible avec l'âge, le montant et le statut déclarés ; justificatif étudiant et étude du prêteur nécessaires. Différé selon contrat, sous réserve d'acceptation du prêteur."],
            [cat.source_produit("pret_etudiant")]))
    _rdv(c)
    return c


REGLES = {"credit_immobilier": credit_immobilier, "credit_conso": credit_conso,
          "epargne_projet": epargne_projet, "pret_etudiant": pret_etudiant}
