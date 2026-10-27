from pathlib import Path

import pytest

testing = pytest.importorskip("streamlit.testing.v1")
APP = str(Path(__file__).resolve().parents[1] / "app.py")


def test_l_interface_demarre_sans_erreur():
    app = testing.AppTest.from_file(APP, default_timeout=30)
    app.run()
    assert not app.exception
    assert "assistant automatique" in app.info[0].value
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
