from src.assistant import reply
from src.contrats import (
    Comprehension,
    Conseil,
    Ecart,
    EtatConversation,
    Etape,
    Proposition,
    Reponse,
)


def test_contracts_are_constructible():
    assert Comprehension().intention == "inconnue"
    assert Comprehension().comprise is False
    assert isinstance(Proposition("demo").raisons, list)
    assert Ecart("lep", "raison").regle is None
    assert isinstance(Conseil().ecartees, list)
    assert Etape("test").appel_llm is False
    assert Reponse("ok").appels_llm == 0


def test_reply_returns_contracts_and_updates_state():
    reponse, etat = reply("Ma carte est perdue", "C01", EtatConversation())

    assert isinstance(reponse, Reponse)
    assert reponse.comprehension.intention == "lost_or_stolen_card"
    assert etat.parcours == "lost_or_stolen_card"
    assert len(etat.historique) == 2
    assert "ne peux pas bloquer" in reponse.texte


def test_reply_without_state_starts_a_conversation():
    reponse, etat = reply("Bonjour", "C01")

    assert "Bonjour" in reponse.texte
    assert etat.derniere_reponse == reponse.texte


def test_unknown_message_asks_before_escalating():
    reponse, etat = reply("Une demande totalement inconnue", "C01", EtatConversation())

    assert reponse.escalade is False  # aucune escalade sans LLM appelé
    assert reponse.appels_llm == 0
    assert etat.clarification_demandee is True
    assert "préciser" in reponse.texte
