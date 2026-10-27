"""Chaîne publique reply : aucune dépendance à un modèle ou serveur bancaire."""
import pytest

from src.assistant import reply
from src.conseiller import clients
from src.contrats import EtatConversation


@pytest.fixture(autouse=True)
def sans_llm(monkeypatch):
    monkeypatch.setenv("ASSISTANT_LLM", "0")


def demande_virement():
    r, e = reply("Je dois envoyer 500 € à mon fils.", "C04", EtatConversation())
    assert e.action_en_attente.outil == "preparer_virement"
    return r, e


@pytest.mark.parametrize("message", ["oui mais pas maintenant", "oui si le solde suffit", "peut-être", "non finalement oui", "oui ?"])
def test_accord_ambigu_ne_declenche_rien(message):
    _, e = demande_virement()
    avant = e.profil_simule["solde"]
    r, e = reply(message, "C04", e)
    assert e.profil_simule["solde"] == avant
    assert not e.journal_actions
    assert e.action_en_attente is not None


def test_persistance_solde_et_pas_de_double_oui():
    _, e = demande_virement()
    avant = e.profil_simule["solde"]
    r, e = reply("oui", "C04", e)
    assert r.action.resultat["statut"] == "succes"
    assert e.profil_simule["solde"] == avant - 500
    _, e = reply("oui", "C04", e)
    assert e.profil_simule["solde"] == avant - 500
    assert len(e.journal_actions) == 1
    assert clients.profil("C04")["solde"] == avant


def test_correction_montant_exige_nouvel_accord():
    _, e = demande_virement()
    ancien_id = e.action_en_attente.identifiant
    avant = e.profil_simule["solde"]
    _, e = reply("Non, plutôt 12,50 euros", "C04", e)
    assert not e.journal_actions
    assert e.action_en_attente.identifiant != ancien_id
    assert e.action_en_attente.parametres["montant"] == 12.5
    r, e = reply("oui", "C04", e)
    assert r.action.resultat["montant"] == 12.5
    assert e.profil_simule["solde"] == avant - 12.5


@pytest.mark.parametrize("message", ["-500 euros", "12.50 euros", "12,555 euros"])
def test_montants_mal_interpretes_par_m1_bloques(message):
    _, e = demande_virement()
    avant = e.profil_simule["solde"]
    _, e = reply(message, "C04", e)
    assert e.action_en_attente is None
    _, e = reply("oui", "C04", e)
    assert not e.journal_actions
    assert e.profil_simule["solde"] == avant


def test_refus_et_isolation_clients():
    _, e = demande_virement()
    _, e = reply("non", "C04", e)
    assert not e.journal_actions
    _, e = reply("J'ai perdu ma carte", "C01", e)
    assert e.client_id == "C01"
    r, e = reply("oui", "C01", e)
    assert r.action.resultat["ok"]
    _, e = reply("bonjour", "C01", e)
    assert e.profil_simule["cartes"][0]["statut"] == "opposition"
    assert clients.profil("C01")["cartes"][0]["statut"] == "active"
    _, autre = reply("bonjour", "C04", e)
    assert autre.profil_simule["solde"] == clients.profil("C04")["solde"]
    assert not autre.journal_actions


def test_manque_metier_pose_question_avant_calcul():
    _, e = reply("Je veux acheter un appartement", "C07", EtatConversation())
    e.slots["revenus_nets"] = 0
    r, e = reply("250000, apport 25000", "C07", e)
    assert r.question == "revenus_nets"
    assert "mensualite" not in r.conseil.faits
    assert e.action_en_attente is None
    r, e = reply("2900", "C07", e)
    assert not r.conseil.manque
    assert r.conseil.faits["mensualite"] == 1196.87
    assert e.question_m3 is None
