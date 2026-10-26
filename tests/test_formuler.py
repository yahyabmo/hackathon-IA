from src.assistant import reply
from src.contrats import EtatConversation
from src.converser import garde_fou


def test_garde_fou_refuse_un_nombre_invente():
    autorises = set(garde_fou.nombres("mensualité de 1 220 €, soit 42,1 % de vos revenus"))
    assert garde_fou.verifier("Votre mensualité serait de 1 220 € (42,1 %).", autorises) == []
    assert garde_fou.verifier("Votre mensualité serait de 1 150 €.", autorises) == ["nombre inventé : 1150"]


def test_garde_fou_refuse_une_promesse():
    assert garde_fou.verifier("Votre crédit est accordé.", set())


def test_la_mention_legale_accompagne_tout_conseil_de_credit():
    etat = EtatConversation()
    _, etat = reply("Je veux acheter un appartement", "C07", etat)
    reponse, _ = reply("250000, apport 25000", "C07", etat)
    assert reponse.texte.endswith("Vérifiez vos capacités de remboursement avant de vous engager.")


def test_le_glossaire_repond_sans_llm():
    reponse, _ = reply("C'est quoi un découvert autorisé ?", "C08", EtatConversation())
    assert reponse.texte.startswith("découvert autorisé")
    assert reponse.appels_llm == 0


def test_llm_injoignable_retombe_sur_le_gabarit(monkeypatch):
    monkeypatch.setenv("ASSISTANT_LLM", "1")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://127.0.0.1:9")  # port fermé
    monkeypatch.setattr("src.llm.URL", "http://127.0.0.1:9")
    etat = EtatConversation()
    _, etat = reply("Je veux acheter un appartement", "C07", etat)
    reponse, _ = reply("250000, apport 25000", "C07", etat)
    assert "42,1" in reponse.texte  # le gabarit, intact
    assert reponse.appels_llm == 1  # l'appel est compté, même raté
