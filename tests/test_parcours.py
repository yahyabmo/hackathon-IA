from pathlib import Path

import pytest

from eval.run_scenarios import rejouer
from src.assistant import reply
from src.comprendre import classifieur
from src.contrats import EtatConversation

SCENARIOS = sorted((Path(__file__).resolve().parents[1] / "eval" / "scenarios").glob("*.yaml"))


@pytest.mark.classifieur  # de bout en bout : avec le vrai classifieur, comme eval/run_scenarios.py
@pytest.mark.parametrize("fichier", SCENARIOS, ids=lambda f: f.stem)
def test_scenarios_de_bout_en_bout(fichier):
    if "classifieur" in fichier.stem and not classifieur.disponible():
        pytest.skip("scénario du classifieur : sentence-transformers ou e5-small absent")
    assert rejouer(fichier) == []


def test_le_profil_n_est_jamais_redemande_mais_confirme():
    reponse, etat = reply("Je veux acheter un appartement", "C07", EtatConversation())
    assert reponse.question == "prix_bien"
    assert "J'ai noté vos revenus" in reponse.texte
    assert etat.slots["revenus_nets"] == 2900


def test_meme_phrase_deux_clients_deux_conseils():
    def conseiller(client, messages):
        etat = EtatConversation()
        for message in messages:
            reponse, etat = reply(message, client, etat)
        return [p.produit_id for p in reponse.conseil.propositions]

    sophie = conseiller("C03", ["Je voudrais mettre de côté pour mes enfants.", "Dans 10 ans, 100 euros par mois"])
    lucas = conseiller("C08", ["Je voudrais mettre de côté", "Dans 10 ans, 100 euros par mois"])
    assert sophie != lucas
    assert lucas[0] == "livret_jeune"


def test_une_demande_sensible_reste_un_guidage():
    reponse, etat = reply("J'ai perdu ma carte", "C01", EtatConversation())
    assert "Je ne peux pas bloquer" in reponse.texte


def test_sans_llm_aucun_appel_ni_escalade():
    etat = EtatConversation()
    for message in ["Je ne sais pas", "rien de précis"]:
        reponse, etat = reply(message, "C01", etat)
        assert reponse.appels_llm == 0
        assert reponse.escalade is False
    assert "aucun accès" in reponse.texte.lower()


def test_trace_mesure_chaque_etage():
    etat = EtatConversation()
    _, etat = reply("Je veux acheter un appartement", "C07", etat)
    reponse, _ = reply("250 000 et 25 000 d'apport", "C07", etat)
    noms = [e.nom for e in reponse.trace]
    assert noms == ["comprendre", "converser", "conseiller", "formuler"]
    assert all(e.latence_ms >= 0 for e in reponse.trace)
