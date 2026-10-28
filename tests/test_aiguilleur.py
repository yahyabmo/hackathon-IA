"""L'aiguilleur et ses trois niveaux (LLM simulé : rapide et reproductible)."""

import json
import re

import pytest

from src import llm, rag
from src.aiguilleur import aiguiller, question_ouverte, trier_par_urgence
from src.assistant import reply
from src.comprendre import classifieur, interprete
from src.contrats import NIVEAU_MOTS_CLES, NIVEAU_REPONSE, Comprehension, EtatConversation
from src.texte import euros


def converser(client, messages, **options):
    etat, reponse = EtatConversation(**options), None
    for message in messages:
        reponse, etat = reply(message, client, etat)
    return reponse, etat


def faux_llm(interpretations):
    """Niveau 1 : le JSON prévu pour le message ; niveau 2 : la première phrase du premier extrait, citée."""

    def generer(modele, systeme, message, max_tokens=200, role="formulation", schema=None, delai=120):
        if schema is not None:
            client = re.search(r"Message du client : « (.*) »", message).group(1)
            return json.dumps(interpretations.get(client, {"intentions": [], "reponse_a_la_question": ""})), 40
        extrait = re.search(r"\[1\] [^:]+ : (.*)", message).group(1)
        return extrait.split(". ")[0].rstrip(".") + " [1].", 60
    return generer


# ── Niveau 0 : les règles, sans LLM ──

def test_deux_demandes_l_urgence_d_abord():
    reponse, etat = converser("C01", ["J'ai perdu ma carte et je veux faire un virement."])
    assert reponse.niveau == 0 and reponse.appels_llm == 0
    assert reponse.texte.index("opposition") < reponse.texte.index("Passons maintenant à votre autre demande")
    assert reponse.question == "beneficiaire" and etat.file_demandes == []
    assert trier_par_urgence(["faire_virement", "hors_sujet", "lost_or_stolen_card"])[0] == "lost_or_stolen_card"


def test_la_carte_perdue_est_traitee_tout_de_suite():
    reponse, _ = converser("C01", ["ma carte est perdue"])
    assert "Faites opposition tout de suite" in reponse.texte and reponse.question is None


def test_un_montant_invraisemblable_est_signale():
    reponse, _ = converser("C01", ["Je veux faire un virement", "mon père", "100000000"])
    assert "très inhabituel" in reponse.texte and euros(1450) in reponse.texte


def test_un_montant_au_dela_du_solde_est_signale():
    reponse, _ = converser("C01", ["Je veux faire un virement", "mon père", "2000"])
    assert f"dépasse votre solde ({euros(1450)})" in reponse.texte


def test_une_demande_interrompue_reprend_ensuite():
    reponse, etat = converser("C01", ["Je veux faire un virement", "j'ai perdu ma carte"])
    assert "opposition" in reponse.texte
    assert "Revenons à un virement : à qui voulez-vous envoyer l'argent ?" in reponse.texte
    assert etat.parcours == "faire_virement" and etat.info_attendue == "beneficiaire"


def test_merci_quand_rien_n_est_en_attente():
    reponse, _ = converser("C01", ["merci"])
    assert reponse.texte.startswith("Avec plaisir.")


# ── L'aiguilleur : les signaux ──

def test_les_signaux_de_l_aiguilleur():
    etat = EtatConversation(parcours="faire_virement", famille="virement", info_attendue="beneficiaire")
    attente = Comprehension(famille="virement", intention="faire_virement", niveau=NIVEAU_REPONSE)
    claire = Comprehension(famille="epargne", intention="epargne_projet", niveau=NIVEAU_MOTS_CLES)
    floue = Comprehension()
    options = dict(sujets_cites=[], llm_ok=True, rag_ok=True)
    assert aiguiller("mon père", attente, etat, lisible=True, **options).niveau == 0
    assert aiguiller("oui", attente, etat, lisible=False, **options).niveau == 1
    assert aiguiller("je veux épargner", claire, EtatConversation(), lisible=True, **options).niveau == 0
    assert aiguiller("bof", floue, EtatConversation(), lisible=True, **options).niveau == 1
    assert aiguiller("bof", floue, EtatConversation(), lisible=True,
                     **{**options, "llm_ok": False}).niveau == 0  # sans LLM : les règles et la clarification
    question = "Je peux retirer de mon PEL avant 4 ans ?"
    assert aiguiller(question, floue, etat, lisible=False, **{**options, "sujets_cites": ["produit:pel"]}).niveau == 2
    assert question_ouverte("Pourquoi j'ai payé des frais ?") == "forte"
    assert question_ouverte("Je peux faire un virement ?") == "faible"


# ── Niveau 1 : le JSON est lu et vérifié par le code ──

def test_la_lecture_du_niveau_1_ecarte_ce_qui_n_est_pas_dans_le_message():
    lu = interprete.lire('{"intentions": ["faire_virement", "aucune"], "reponse_a_la_question": "à ma grand-mère"}',
                         "je veux envoyer de l'argent")
    assert lu.intentions == ["faire_virement"] and lu.reponse is None and lu.valide
    lu = interprete.lire('{"intentions": ["carte_perdue"], "reponse_a_la_question": "mon papa"}', "à mon papa")
    assert lu.intentions == ["lost_or_stolen_card"] and lu.reponse == "mon papa"
    assert not interprete.lire("pas du JSON", "oui").valide


def test_le_schema_impose_une_liste_fermee_de_sujets():
    sujets = interprete.SCHEMA["properties"]["intentions"]["items"]["enum"]
    assert "carte_perdue" in sujets and "faire_virement" in sujets and "aucune" in sujets
    assert interprete.SCHEMA["properties"]["intentions"]["maxItems"] == 3


def test_niveau_1_meme_sujet_on_repose_la_question_avec_des_exemples(monkeypatch):
    monkeypatch.setattr(llm, "generer", faux_llm({"oui": {"intentions": ["faire_virement"],
                                                          "reponse_a_la_question": "oui"}}))
    reponse, _ = converser("C01", ["Je veux faire un virement", "oui"], llm_actif=True)
    assert reponse.niveau == 1 and reponse.appels_llm == 1
    assert reponse.texte.startswith("Bien sûr. À qui voulez-vous envoyer l'argent ?")
    assert "Par exemple : votre fils" in reponse.texte


def test_niveau_1_une_reponse_libre_remplit_l_information(monkeypatch):
    monkeypatch.setattr(llm, "generer", faux_llm({"c'est pour mon papa": {
        "intentions": ["faire_virement"], "reponse_a_la_question": "mon papa"}}))
    reponse, etat = converser("C01", ["Je veux faire un virement", "c'est pour mon papa"], llm_actif=True)
    assert etat.slots["beneficiaire"] == "pere" and reponse.question == "montant"


def test_niveau_1_injoignable_repli_sur_les_regles(monkeypatch):
    monkeypatch.setattr(llm, "URL", "http://127.0.0.1:9")
    reponse, _ = converser("C01", ["Je veux faire un virement", "oui"], llm_actif=True)
    assert reponse.niveau == 1 and "Je n'ai pas bien compris" in reponse.texte


# ── Niveau 2 : RAG sur nos fiches (vrai encodeur) ──

@pytest.fixture
def index_rag():
    if not rag.disponible():
        pytest.skip("encodeur e5-small absent")


@pytest.mark.classifieur
def test_les_fiches_gardent_leur_source(index_rag):
    assert len(rag.fiches()) >= 30
    assert all(f["source"] and f["texte"] for f in rag.fiches())
    assert rag.rechercher("Je peux retirer de mon PEL avant 4 ans ?")[0]["id"] == "produit:pel"


@pytest.mark.classifieur
def test_le_garde_fou_du_niveau_2_refuse_une_affirmation_inventee(index_rag):
    question = "Quelle est la différence entre le LDDS et le Livret A ?"
    passages = rag.rechercher(question)
    invente = "Le LDDS est destiné aux majeurs et imposable [1]."
    fidele = "Le LDDS demande un domicile fiscal en France et une imposition séparée [1]."
    assert "affirmations absentes des extraits" in rag.verifier(invente, passages, question)
    assert rag.verifier(fidele, passages, question) == []


@pytest.mark.classifieur
def test_niveau_2_sans_llm_repli_sur_la_meilleure_fiche(index_rag):
    reponse, _ = converser("C01", ["Je peux retirer de mon PEL avant 4 ans ?"])
    assert reponse.niveau == 2 and reponse.appels_llm == 0
    assert reponse.texte.startswith("D'après nos fiches : Plan épargne logement (PEL)")
    assert reponse.sources[0]["id"] == "produit:pel"


@pytest.mark.classifieur
def test_niveau_2_hors_de_nos_fiches_on_ne_repond_pas(index_rag):
    resultat = rag.repondre("Qui a gagné le match hier soir ?", avec_llm=False)
    assert not resultat.pertinent and "Je n'ai pas cette information" in resultat.texte


# ── Les niveaux changent à chaque message : la chaîne 1 → 2 → 0 → 2 ──

@pytest.mark.classifieur
def test_la_chaine_1_2_0_2_avec_reprise(monkeypatch, index_rag):
    monkeypatch.setattr(classifieur, "predire", lambda message: None)  # le premier message reste flou
    monkeypatch.setattr(llm, "generer", faux_llm({"j'ai un truc à régler avec quelqu'un": {
        "intentions": ["faire_virement"], "reponse_a_la_question": ""}}))
    etat = EtatConversation(llm_actif=True)
    niveaux = []
    for message in ["j'ai un truc à régler avec quelqu'un", "Je peux retirer de mon PEL avant 4 ans ?",
                    "mon père", "Pourquoi vous ne pouvez pas faire le virement vous-même ?"]:
        reponse, etat = reply(message, "C01", etat)
        niveaux.append(reponse.niveau)
    assert niveaux == [1, 2, 0, 2] and etat.niveaux == niveaux
    assert "Revenons à un virement : quel montant voulez-vous envoyer ?" in reponse.texte
    assert reponse.sources and "[1]" in reponse.texte


def test_un_renvoi_au_contexte_retrouve_le_sujet_deja_traite(monkeypatch):
    monkeypatch.setattr(llm, "generer", faux_llm({"mais ma carte ?": {"intentions": ["carte_usage"],
                                                                      "reponse_a_la_question": ""}}))
    reponse, _ = converser("C01", ["J'ai perdu ma carte", "mais ma carte ?"], llm_actif=True)
    assert reponse.niveau == 1 and "Faites opposition tout de suite" in reponse.texte


def test_niveau_1_une_valeur_de_liste_fermee_est_acceptee(monkeypatch):
    monkeypatch.setattr(llm, "generer", faux_llm({"pour la petite dernière de la famille": {
        "intentions": ["faire_virement"], "reponse_a_la_question": "ma fille"}}))
    reponse, etat = converser("C01", ["Je veux faire un virement", "pour la petite dernière de la famille"],
                              llm_actif=True)
    assert etat.slots["beneficiaire"] == "fille" and reponse.question == "montant"


def test_niveau_1_un_nombre_absent_du_message_est_refuse(monkeypatch):
    monkeypatch.setattr(llm, "generer", faux_llm({"le même que la dernière fois": {
        "intentions": ["faire_virement"], "reponse_a_la_question": "300 €"}}))
    reponse, etat = converser("C01", ["Je veux faire un virement", "mon père", "le même que la dernière fois"],
                              llm_actif=True)
    assert "montant" not in etat.slots and reponse.question == "montant"


@pytest.mark.classifieur
def test_pourquoi_apres_un_conseil_explique_le_conseil(monkeypatch, index_rag):
    monkeypatch.setattr(llm, "generer", faux_llm({}))
    reponse, _ = converser("C07", ["Je veux acheter un appartement", "250000, apport 25000", "pourquoi ?"],
                           llm_actif=True)
    assert reponse.niveau == 2 and reponse.sources[0]["titre"] == "Votre simulation"
    assert "n'est pas proposé" in reponse.sources[0]["texte"]


def test_la_suite_d_un_parcours_termine_reste_au_niveau_0():
    reponse, _ = converser("C01", ["Je veux faire un virement", "mon père", "100000",
                                   "ok je peux envoyer 1000 ?"], llm_actif=True)
    assert reponse.niveau == 0 and reponse.appels_llm == 0
    assert "100 000" not in reponse.texte and "espace bancaire sécurisé" in reponse.texte


@pytest.mark.classifieur
def test_une_reponse_fidele_sans_citation_est_acceptee_avec_la_meilleure_fiche(monkeypatch, index_rag):
    monkeypatch.setattr(llm, "generer", lambda *a, **k: ("Tout retrait anticipé entraîne la clôture du plan", 30))
    resultat = rag.repondre("Je peux retirer de mon PEL avant 4 ans ?")
    assert resultat.repli is None and "clôture du plan [1]" in resultat.texte


# ── Règles ajoutées après le test de l'école (mercredi matin) ──

def test_un_nombre_seul_continue_le_parcours():
    reponse, _ = converser("C01", ["Je veux faire un virement", "mon père", "100000", "1000"])
    assert "Bonjour" not in reponse.texte and "espace bancaire sécurisé" in reponse.texte


def test_un_petit_credit_n_est_pas_un_projet_immobilier():
    reponse, etat = converser("C01", ["Je veux acheter un appartement", "verifie si je peux avoir un credit de 10000 euro"])
    assert reponse.texte.startswith("Pour emprunter")
    assert etat.parcours == "credit_conso" and etat.slots["montant"] == 10000


def test_oui_ou_non_n_est_pas_un_refus():
    reponse, etat = converser("C01", ["Je veux un crédit pour acheter une voiture.", "12000",
                                      "dis moi si je peux, oui ou non ?"])
    assert "on laisse ça de côté" not in reponse.texte and etat.parcours == "credit_conso"


def test_rendez_vous_et_releves_sans_acces_au_compte():
    reponse, _ = converser("C01", ["je veux prendre un rendez vous stp"])
    assert "rubrique Rendez-vous" in reponse.texte
    reponse, etat = converser("C01", ["Je veux un crédit pour acheter une voiture.", "12000",
                                      "dis moi en se basant sur mes relevés"])
    assert "aucun accès à vos relevés" in reponse.texte and "Revenons à un crédit" in reponse.texte
