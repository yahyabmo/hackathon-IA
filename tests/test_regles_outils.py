import pytest

from src.conseiller import clients, conseiller, outils
from src.contrats import Action, EtatConversation


def test_credit_immobilier_calcul_hcsf():
    slots = {"revenus_nets": 2900, "mensualites_en_cours": 0, "prix_bien": 250000, "apport": 25000}
    conseil = conseiller("credit_immobilier", clients.profil("C07"), slots)

    assert conseil.faits["besoin"] == 243750
    assert conseil.faits["mensualite"] == 1220
    assert round(conseil.faits["taux_effort"] * 100, 1) == 42.1
    assert conseil.faits["prix_max"] == 212000
    assert [e.produit_id for e in conseil.ecartees] == ["credit_immobilier", "credit_immobilier_30_ans"]
    assert conseil.ecartees[0].regle == "HCSF-taux-effort"


def test_credit_immobilier_finançable():
    slots = {"revenus_nets": 2900, "mensualites_en_cours": 0, "prix_bien": 180000, "apport": 25000}
    conseil = conseiller("credit_immobilier", clients.profil("C07"), slots)
    assert "credit_immobilier" in [p.produit_id for p in conseil.propositions]
    assert not conseil.alertes


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
