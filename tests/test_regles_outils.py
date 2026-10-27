import pytest

from src.conseiller import clients, conseiller, outils
from src.contrats import Action, EtatConversation


def test_credit_immobilier_calcul_hcsf():
    slots = {"revenus_nets": 2900, "mensualites_en_cours": 0, "prix_bien": 250000, "apport": 25000}
    conseil = conseiller("credit_immobilier", clients.profil("C07"), slots)

    assert conseil.faits["besoin"] == 243750
    # Référence statistique BDF août 2026 : 3,32 %, pas l'ancien taux fictif.
    assert conseil.faits["mensualite"] == 1196.87
    assert round(conseil.faits["taux_effort"] * 100, 1) == 41.3
    assert conseil.faits["prix_max"] == 215000
    assert [e.produit_id for e in conseil.ecartees] == ["credit_immobilier", "credit_immobilier_30_ans"]
    assert conseil.ecartees[0].regle == "HCSF-taux-effort"


def test_credit_immobilier_finançable():
    slots = {"revenus_nets": 2900, "mensualites_en_cours": 0, "prix_bien": 180000, "apport": 25000}
    conseil = conseiller("credit_immobilier", clients.profil("C07"), slots)
    assert "credit_immobilier" in [p.produit_id for p in conseil.propositions]
    assert conseil.faits["decision_bancaire"] is False
    assert any("Assurance non renseignée" in a for a in conseil.alertes)


def test_chaque_proposition_et_chaque_ecart_se_justifie():
    slots = {"pour_qui": "soi", "horizon_mois": 24, "montant_mensuel": 50}
    conseil = conseiller("epargne_projet", clients.profil("C08"), slots)
    assert all(p.raisons for p in conseil.propositions)
    assert all(e.raison for e in conseil.ecartees)


def test_une_action_a_effet_de_bord_exige_une_confirmation():
    profil, etat = clients.profil("C01"), EtatConversation()
    with pytest.raises(outils.ConfirmationRequise):
        outils.executer(Action("bloquer_carte"), profil, etat)
    action = outils.executer(Action("bloquer_carte", confirmee=True), profil, etat)
    assert action.resultat["reference"].startswith("OPP-C01-")


def test_la_lecture_est_libre():
    action = outils.executer(Action("expliquer_frais"), clients.profil("C02"), EtatConversation())
    assert action.resultat["total"] == 8
    assert action.resultat["proposer_offre_fragile"] is True


def test_virement_vers_un_beneficiaire_inconnu_refuse():
    action = Action("preparer_virement", {"beneficiaire": "soeur", "montant": 50}, confirmee=True)
    resultat = outils.executer(action, clients.profil("C04"), EtatConversation()).resultat
    assert resultat["ok"] is False


@pytest.mark.parametrize("montant", [-1, 0, float("nan"), float("inf"), True, "10", 10.001, None, 10**30])
def test_virement_invalide_sans_mutation(montant):
    p, e = clients.profil("C04"), EtatConversation()
    avant = p["solde"]
    a = outils.executer(Action("preparer_virement", {"montant": montant, "beneficiaire": "fils"}, True), p, e)
    assert a.resultat["statut"] == "refus"
    assert p["solde"] == avant
    assert len(e.journal_actions) == 1


def test_virement_centimes_rejeu_et_demande_modifiee():
    p, e = clients.profil("C04"), EtatConversation()
    p["solde"] = .30
    a = Action("preparer_virement", {"montant": .10, "beneficiaire": "fils"}, True)
    outils.executer(a, p, e)
    assert p["solde"] == .20
    outils.executer(a, p, e)
    assert p["solde"] == .20 and len(e.journal_actions) == 1
    a.parametres["montant"] = .20
    outils.executer(a, p, e)
    assert a.resultat["statut"] == "refus" and p["solde"] == .20


@pytest.mark.parametrize("outil", ["bloquer_carte", "preparer_virement", "transmettre_conseiller"])
@pytest.mark.parametrize("confirmation", [False, None, "oui", 1])
def test_tous_les_effets_exigent_un_booleen_vrai(outil, confirmation):
    p, e = clients.profil("C04"), EtatConversation()
    a = Action(outil, confirmee=confirmation)
    with pytest.raises(outils.ConfirmationRequise):
        outils.executer(a, p, e)
    assert a.resultat["statut"] == "en_attente"


def test_solde_insuffisant_beneficiaire_ambigu_et_mauvais_client():
    p, e = clients.profil("C04"), EtatConversation()
    for montant in (p["solde"] + 1,):
        a = Action("preparer_virement", {"montant": montant, "beneficiaire": "fils"}, True)
        assert not outils.executer(a, p, e).resultat["ok"]
    p["beneficiaires"] *= 2
    a = Action("preparer_virement", {"montant": 10, "beneficiaire": "fils"}, True)
    assert not outils.executer(a, p, e).resultat["ok"]
    e.client_id = "C01"
    assert not outils.executer(Action("bloquer_carte", confirmee=True), p, e).resultat["ok"]


def test_carte_deja_bloquee_et_resultats_independants():
    p, e = clients.profil("C01"), EtatConversation()
    a = outils.executer(Action("bloquer_carte", confirmee=True), p, e)
    assert p["cartes"][0]["statut"] == "opposition"
    a.resultat["reference"] = "falsifie"
    assert e.journal_actions[0]["resultat"]["reference"] != "falsifie"
    assert not outils.executer(Action("bloquer_carte", confirmee=True), p, e).resultat["ok"]


def test_echec_interne_atomique(monkeypatch):
    p, e = clients.profil("C01"), EtatConversation()
    def panne(profil, action, etat):
        profil["solde"] = 0
        raise RuntimeError("panne simulée")
    monkeypatch.setitem(outils._EXECUTION, "bloquer_carte", panne)
    a = outils.executer(Action("bloquer_carte", confirmee=True), p, e)
    assert a.resultat["statut"] == "echec"
    assert p["solde"] == clients.profil("C01")["solde"]
    assert e.journal_actions[-1]["resultat"]["statut"] == "echec"


def test_frais_periode_et_ticket_simule():
    p, e = clients.profil("C02"), EtatConversation()
    a = outils.executer(Action("expliquer_frais", {"periode": "2026-10"}), p, e)
    assert a.resultat["total"] == 8 and a.resultat["sources"]
    a = outils.executer(Action("expliquer_frais", {"periode": "2026-09"}), p, e)
    assert a.resultat["total"] == 0
    a = outils.executer(Action("transmettre_conseiller", confirmee=True), p, e)
    assert a.resultat["simule"] and a.resultat["ticket"].startswith("TCK-C02-")


def test_lecture_profil_independante():
    p, e = clients.profil("C01"), EtatConversation()
    a = outils.executer(Action("consulter_profil"), p, e)
    a.resultat["profil"]["solde"] = 0
    assert p["solde"] > 0


@pytest.mark.parametrize("champ,valeur", [
    ("revenus_nets", 0), ("revenus_nets", float("inf")), ("prix_bien", -1),
    ("apport", -1), ("mensualites_en_cours", -1), ("duree_ans", 0),
    ("duree_ans", 12.5), ("taux_annuel", -0.01), ("taux_annuel", 1.01),
    ("assurance_mensuelle", float("nan")), ("taux_frais_notaire", -1),
])
def test_credit_entrees_invalides_sans_calcul(champ, valeur):
    s = {"prix_bien": 250000, "apport": 25000, champ: valeur}
    c = conseiller("credit_immobilier", clients.profil("C07"), s)
    assert champ in c.manque
    assert "mensualite" not in c.faits


def test_credit_taux_zero_assurance_et_financement_nul():
    p = clients.profil("C07")
    s = {"prix_bien": 100000, "apport": 7500, "duree_ans": 10, "taux_annuel": 0,
         "assurance_mensuelle": 25}
    c = conseiller("credit_immobilier", p, s)
    assert c.faits["besoin"] == 100000
    assert c.faits["mensualite"] == 858.33
    assert c.faits["assurance_connue"] is True
    assert c.faits["taux_effort"] == pytest.approx((100000 / 120 + 25) / 2900)
    c = conseiller("credit_immobilier", p, {**s, "apport": 200000})
    assert c.faits["besoin"] == 0 and "mensualite" not in c.faits


def test_duree_hors_cadre_et_conso_non_hcsf():
    p = clients.profil("C07")
    c = conseiller("credit_immobilier", p, {"prix_bien": 200000, "apport": 10000, "duree_ans": 30})
    assert c.ecartees[0].regle == "HCSF-duree"
    c = conseiller("credit_conso", p, {"montant": 100000, "duree_mois": 12})
    assert c.ecartees[0].regle == "PRUDENCE-conso"
    assert any("pas une obligation HCSF" in a for a in c.alertes)


@pytest.mark.parametrize("montant,duree,taux", [(1.25, 1, 0), (1000, 600, 1e-15), (5000, 12, 1)])
def test_conso_calculs_limites_finis(montant, duree, taux):
    import math
    c = conseiller("credit_conso", clients.profil("C01"), {"montant": montant, "duree_mois": duree, "taux_annuel": taux})
    assert not c.manque
    assert math.isfinite(c.faits["mensualite"])
    assert c.faits["mensualite"] > 0


def epargne(p=None, **slots):
    return conseiller("epargne_projet", p or clients.profil("C03"),
                      {"horizon_mois": 60, "montant_mensuel": 100, "pour_qui": "soi", **slots})


def test_fiscalite_inconnue_puis_connue():
    p = clients.profil("C03")
    c = epargne(p)
    assert c.faits["eligibilite"]["lep"] == "inconnue"
    assert "lep" not in [e.produit_id for e in c.ecartees]
    p.update(rfr=20000, parts_fiscales=1, annee_rfr=2025)
    assert "lep" in [x.produit_id for x in epargne(p).propositions]
    p["rfr"] = 30000
    assert "lep" in [x.produit_id for x in epargne(p).ecartees]
    p["territoire_fiscal"] = "guadeloupe"
    assert epargne(p).faits["eligibilite"]["lep"] == "inconnue"


def test_livret_existant_plafond_liquidite_et_mensualite():
    p = clients.profil("C03")
    p["livrets"] = {"livret_a": 100}
    c = epargne(p)
    assert "Alimenter" in next(x for x in c.propositions if x.produit_id == "livret_a").raisons[0]
    p["livrets"]["livret_a"] = 22950
    assert "livret_a" in [x.produit_id for x in epargne(p).ecartees]
    assert "pel" in [x.produit_id for x in epargne(p, besoin_liquidite=False).propositions]
    assert "pel" in [x.produit_id for x in epargne(p, besoin_liquidite=True).ecartees]
    assert "pel" in [x.produit_id for x in epargne(p, besoin_liquidite=False, montant_mensuel=10).ecartees]
    assert "montant_mensuel" in epargne(p, montant_mensuel=None).manque


def test_sophie_et_lucas_conseils_distincts():
    sophie = epargne(clients.profil("C03"), pour_qui="enfants")
    lucas = epargne(clients.profil("C08"))
    assert sophie.faits["eligibilite"]["lep"] == "inconnue"
    assert lucas.faits["eligibilite"]["lep"] == "ecarte"
    assert sophie.propositions[0].produit_id == "livret_a"
    assert lucas.propositions[0].produit_id == "livret_jeune"


def test_pret_etudiant_conditions_et_inconnus():
    p = clients.profil("C08")
    c = conseiller("pret_etudiant", p, {"montant": 5000})
    assert "pret_etudiant" in [x.produit_id for x in c.propositions]
    p["est_etudiant"] = None
    assert "est_etudiant" in conseiller("pret_etudiant", p, {"montant": 5000}).manque
    p.update(est_etudiant=True, age=36)
    assert conseiller("pret_etudiant", p, {"montant": 5000}).ecartees[0].regle == "PE-age"


@pytest.mark.parametrize("duree", [0, 11, 121, float("inf"), 12.5])
def test_pret_etudiant_duree_connue_hors_offre(duree):
    c = conseiller("pret_etudiant", clients.profil("C08"), {"montant": 5000, "duree_mois": duree})
    assert "duree_mois" in c.manque


def test_taux_non_verifie_demande_information(monkeypatch):
    from src.conseiller import catalogue
    original = catalogue.parametre_detail
    def fiche(cle):
        p = original(cle)
        if cle == "taux_indicatif_credit_immobilier":
            p["statut"] = "non_verifie"
        return p
    monkeypatch.setattr(catalogue, "parametre_detail", fiche)
    c = conseiller("credit_immobilier", clients.profil("C07"), {"prix_bien": 250000, "apport": 25000})
    assert "taux_annuel" in c.manque and "mensualite" not in c.faits
