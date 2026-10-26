from src.assistant import reply
from src.contrats import (
    Action,
    Conseil,
    Comprehension,
    EtatConversation,
    Etape,
    Proposition,
    Reponse,
)


def test_contracts_are_constructible():
    assert Comprehension().intention == "inconnue"
    assert isinstance(Proposition("demo").raisons, list)
    assert isinstance(Conseil().propositions, list)
    assert Action().confirmee is False
    assert Etape("test").nom == "test"
    assert Reponse("ok").texte == "ok"


def test_reply_returns_contracts_and_updates_state():
    etat = EtatConversation()
    reponse, nouvel_etat = reply("Ma carte est perdue", "CLIENT-001", etat)

    assert isinstance(reponse, Reponse)
    assert isinstance(nouvel_etat, EtatConversation)
    assert reponse.comprehension.intention == "carte_perdue"
    assert nouvel_etat.intention == "carte_perdue"
    assert len(nouvel_etat.historique) == 2
    assert reponse.action.confirmee is False


def test_reply_keeps_conversation_context():
    etat = EtatConversation()
    _, etat = reply("Bonjour", "CLIENT-001", etat)
    _, etat = reply("Je ne sais pas quoi demander", "CLIENT-001", etat)

    assert len(etat.historique) == 4
    assert etat.derniere_reponse is not None


def test_unknown_intent_escalates_without_action():
    reponse, _ = reply("Une demande totalement inconnue", "CLIENT-001", EtatConversation())

    assert reponse.escalade is True
    assert reponse.action.confirmee is False
    assert reponse.action.resultat is None
