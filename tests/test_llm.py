"""Branchement du LLM : serveurs, garde-fou complet, reformulation (LLM simulé)."""

from src import llm
from src.assistant import reply
from src.contrats import EtatConversation
from src.converser import garde_fou
from src.converser.formuler import SUITE_CONSEILLER, reformuler
from src.converser.glossaire import chercher

GABARIT = "La mensualité serait d'environ 1 220 €, soit 42,1 % de vos revenus. Voulez-vous un rendez-vous ?"


def test_la_reflexion_est_coupee_pour_les_modeles_qui_reflechissent():
    assert llm.corps_ollama("qwen3:1.7b", "s", "m", 10)["think"] is False
    assert llm.corps_ollama("gemma4:e2b", "s", "m", 10)["think"] is False
    assert "think" not in llm.corps_ollama("ministral-3:3b", "s", "m", 10)


def test_serveur_choisi_par_role(monkeypatch):
    monkeypatch.setenv("LLM_API_ESCALADE", "vllm")
    assert llm.serveur("escalade") == "vllm"
    assert llm.serveur("formulation") == "ollama"


def test_appel_vllm_compatible_openai(monkeypatch):
    appels = []

    def faux_serveur(url, corps=None, delai=120):
        appels.append((url, corps))
        return {"choices": [{"message": {"content": " réponse "}}], "usage": {"total_tokens": 42}}

    monkeypatch.setenv("LLM_API", "vllm")
    monkeypatch.setenv("VLLM_BASE_URL", "http://deepeirb:8000/v1/")
    monkeypatch.setattr(llm, "_requete", faux_serveur)
    assert llm.generer("ministral-3:14b", "s", "m") == ("réponse", 42)
    assert appels[0][0] == "http://deepeirb:8000/v1/chat/completions"
    assert appels[0][1]["model"] == "ministral-3:14b"


def test_le_garde_fou_refuse_un_oubli_et_une_reponse_tronquee():
    reference = set(garde_fou.nombres(GABARIT))
    problemes = garde_fou.verifier("Oui, je suis prêt à reformuler.", reference, reference, longueur_min=40)
    assert "nombre oublié : 1220" in problemes
    assert "réponse tronquée" in problemes


def test_reformuler_refuse_une_reponse_qui_perd_le_conseil(monkeypatch):
    monkeypatch.setattr(llm, "generer", lambda *a, **k: ("Oui, je suis prêt à reformuler le message.", 30))
    texte, tokens, problemes = reformuler(GABARIT, "petit-modele")
    assert texte is None and tokens == 30 and problemes


def test_reformuler_accepte_une_reecriture_fidele(monkeypatch):
    reecrit = "Votre mensualité serait d'environ 1 220 €, soit 42,1 % de vos revenus. Voulez-vous un rendez-vous ?"
    monkeypatch.setattr(llm, "generer", lambda *a, **k: (f'"{reecrit}"', 50))
    texte, _, problemes = reformuler(GABARIT, "petit-modele")
    assert texte == reecrit and problemes == []


def test_un_seul_appel_au_llm_et_seulement_pour_le_conseil(monkeypatch):
    appels = []

    def faux_llm(modele, systeme, message, max_tokens=200, role="formulation"):
        appels.append(role)
        return message.split('"""')[1].strip(), 10  # renvoie le gabarit tel quel

    monkeypatch.setenv("ASSISTANT_LLM", "1")
    monkeypatch.setattr(llm, "generer", faux_llm)
    etat = EtatConversation()
    premier, etat = reply("Je veux acheter un appartement", "C07", etat)
    second, _ = reply("250 000, apport 25 000", "C07", etat)
    assert premier.appels_llm == 0  # une question : gabarit
    assert second.appels_llm == 1 and appels == ["formulation"]
    assert "41,3" in second.texte  # taux statistique BDF de 3,32 %


def test_la_suite_conseiller_reste_hors_du_llm(monkeypatch):
    recus = []

    def faux_llm(modele, systeme, message, max_tokens=200, role="formulation"):
        recus.append(message)
        return message.split('"""')[1].strip() + " Je vous contacte demain.", 10

    monkeypatch.setenv("ASSISTANT_LLM", "1")
    monkeypatch.setattr(llm, "generer", faux_llm)
    etat = EtatConversation()
    _, etat = reply("Je veux acheter un appartement", "C07", etat)
    reponse, _ = reply("250 000, apport 25 000", "C07", etat)
    assert "rendez-vous" not in recus[0]
    assert SUITE_CONSEILLER in reponse.texte


def test_glossaire_tolere_les_fautes_seulement_pour_une_definition():
    assert chercher("c'est quoi le TEAG ?", approchant=True)["terme"] == "TAEG"
    assert chercher("que veut dire decouver autorisé", approchant=True)["terme"] == "découvert autorisé"
    assert chercher("c'est quoi le TEAG ?") is None
    assert chercher("c'est quoi une hypothèque", approchant=True) is None


def test_une_faute_de_frappe_dans_une_question_de_definition():
    reponse, _ = reply("C'est quoi le TEAG ?", "C08", EtatConversation())
    assert reponse.texte.startswith("TAEG :")
