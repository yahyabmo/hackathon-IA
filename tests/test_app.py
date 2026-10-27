from pathlib import Path

import pytest

testing = pytest.importorskip("streamlit.testing.v1")
APP = str(Path(__file__).resolve().parents[1] / "app.py")


def test_l_interface_demarre_sans_erreur():
    app = testing.AppTest.from_file(APP, default_timeout=30)
    app.run()
    assert not app.exception
    assert any("assistant automatique" in c.value for c in app.caption)
    assert any("LLM : désactivé" in c.value for c in app.sidebar.caption)


def test_l_interface_repond_et_change_de_client_proprement():
    app = testing.AppTest.from_file(APP, default_timeout=30)
    app.run()
    app.sidebar.selectbox[0].set_value("C07").run()
    app.chat_input[0].set_value("Je veux acheter un appartement").run()
    assert not app.exception
    assert "beau projet" in app.chat_message[-1].markdown[0].value

    app.sidebar.selectbox[0].set_value("C08").run()  # nouveau client : conversation remise à zéro
    assert len(app.chat_message) == 0


def test_le_mode_mots_simples_s_active_depuis_l_interface():
    app = testing.AppTest.from_file(APP, default_timeout=30)
    app.run()
    app.sidebar.toggle(key="mots_simples").set_value(True).run()
    app.chat_input[0].set_value("J'ai perdu ma carte").run()
    assert not app.exception
    assert "veut dire" in app.chat_message[-1].markdown[0].value


def test_le_profil_et_l_action_refletent_la_simulation():
    app = testing.AppTest.from_file(APP, default_timeout=30)
    app.run()
    app.sidebar.selectbox[0].set_value("C04").run()
    app.chat_input[0].set_value("Je dois envoyer 500 € à mon fils.").run()
    app.chat_input[0].set_value("oui").run()
    assert not app.exception
    textes = " ".join(m.value for m in app.markdown)
    assert "exécutée (simulation)" in textes
    assert "1 800,00 €" in textes
    assert app.session_state.etat.profil_simule["solde"] == 1800


def test_bouton_confirmation_et_rerun_sans_double_debit():
    app = testing.AppTest.from_file(APP, default_timeout=30).run()
    app.sidebar.selectbox[0].set_value("C04").run()
    app.button(key="suggestion-0").click().run()
    assert app.session_state.etat.profil_simule["solde"] == 2300
    bouton = next(b for b in app.button if b.label == "Confirmer la simulation")
    bouton.click().run()
    assert not app.exception
    assert app.session_state.etat.profil_simule["solde"] == 1800
    app.run()
    assert app.session_state.etat.profil_simule["solde"] == 1800
    assert not any(b.label == "Confirmer la simulation" for b in app.button)


def test_simulation_credit_affiche_calculs_et_sources():
    app = testing.AppTest.from_file(APP, default_timeout=30).run()
    app.sidebar.selectbox[0].set_value("C07").run()
    app.button(key="suggestion-0").click().run()
    app.button(key="suite-demo").click().run()
    assert not app.exception
    assert any(m.label == "Mensualité" for m in app.metric)
    assert any("Relevé le" in m.value for m in app.markdown)
    assert app.session_state.derniere.conseil.faits["mensualite"] > 0


def test_annulation_interface_sans_opposition():
    app = testing.AppTest.from_file(APP, default_timeout=30).run()
    app.button(key="suggestion-0").click().run()
    next(b for b in app.button if b.label == "Annuler").click().run()
    assert not app.exception
    assert app.session_state.etat.profil_simule["cartes"][0]["statut"] == "active"
    assert any("Demande annulée" in m.value for m in app.markdown)
