"""Cas limites du dialogue, mode « mots simples », journal et escalade (module 2)."""

from src import incompris
from src.assistant import reply
from src.conseiller import clients
from src.contrats import NIVEAU_REPONSE, Comprehension, EtatConversation
from src.converser.dialogue import avancer


def converser(client, messages, etat=None):
    etat = etat or EtatConversation()
    for message in messages:
        reponse, etat = reply(message, client, etat)
    return reponse, etat


LEA = ["Je veux acheter un appartement", "Autour de 250 000, et je peux mettre les 25 000"]


# ── Corrections ──

def test_une_correction_apres_le_conseil_le_recalcule():
    reponse, etat = converser("C07", LEA + ["Et avec un bien à 200 000 ?"])
    assert etat.slots["prix_bien"] == 200000
    assert reponse.conseil.faits["prix_bien"] == 200000
    assert "credit_immobilier" in [p.produit_id for p in reponse.conseil.propositions]  # 32,8 % : finançable


def test_une_correction_a_deux_montants_suit_l_ordre_des_questions():
    _, etat = converser("C07", LEA + ["Et 300 000 avec 60 000 ?"])
    assert (etat.slots["prix_bien"], etat.slots["apport"]) == (300000, 60000)


def test_virement_reste_un_guidage_sans_action():
    reponse, etat = converser("C04", ["Je dois envoyer 500 € à mon fils."])
    assert "accéder à votre compte" in reponse.texte.lower()


# ── « Je ne sais pas », réponse incomprise, abandon, « non » ──

def test_je_ne_sais_pas_avec_valeur_par_defaut_annoncee():
    reponse, etat = converser("C03", ["Je voudrais mettre de côté pour mes enfants.", "Je ne sais pas trop"])
    assert etat.slots["horizon_mois"] == 12
    assert "Je pars sur un an" in reponse.texte
    assert reponse.question == "montant_mensuel"


def test_je_ne_sais_pas_sans_valeur_par_defaut_relance():
    reponse, _ = converser("C05", ["Je veux un crédit pour acheter une voiture.", "aucune idée"])
    assert reponse.question == "montant"
    assert "une estimation suffit" in reponse.texte


def test_reponse_incomprise_la_question_est_reposee():
    reponse, _ = converser("C05", ["Je veux un crédit pour acheter une voiture.", "beaucoup"])
    assert reponse.question == "montant"
    assert reponse.texte.startswith("Je n'ai pas bien compris.")


def test_laisse_tomber_abandonne_le_parcours():
    reponse, etat = converser("C07", ["Je veux acheter un appartement", "Laisse tomber"])
    assert "on laisse ça de côté" in reponse.texte
    assert etat.parcours is None and etat.slots == {}


def test_non_vaut_zero_quand_la_question_l_admet():
    profil = clients.profil("C07")
    profil["mensualites_credits"] = None  # le profil ne le sait pas : il faut le demander
    etat = EtatConversation()
    premier = Comprehension(famille="credit", intention="credit_immobilier", niveau="mots_cles")
    assert avancer("Je veux acheter un appartement", premier, etat, profil).info == "mensualites_en_cours"
    suite = Comprehension(famille="credit", intention="credit_immobilier", niveau=NIVEAU_REPONSE)
    decision = avancer("non", suite, etat, profil)
    assert etat.slots["mensualites_en_cours"] == 0
    assert decision.info == "prix_bien"


# ── Mots simples ──

def test_mots_simples_automatique_pour_paul():
    reponse, _ = converser("C04", ["Je dois envoyer 500 € à mon fils."])
    assert "\n\n" in reponse.texte
    assert "accéder à votre compte" in reponse.texte.lower()


def test_mots_simples_sur_demande_explique_le_jargon():
    etat = EtatConversation(mots_simples=True)
    reponse, _ = reply("J'ai perdu ma carte", "C01", etat)
    assert "ne peux pas bloquer" in reponse.texte.lower()


def test_sans_mots_simples_le_texte_reste_d_un_bloc():
    reponse, _ = reply("J'ai perdu ma carte", "C01", EtatConversation())
    assert "Je ne peux pas bloquer" in reponse.texte


# ── Journal des incompris et escalade ──

def test_les_messages_incompris_sont_journalises():
    converser("C01", ["Je ne sais pas quoi demander", "rien de précis"])
    lignes = incompris.lire()
    assert [l["suite"] for l in lignes] == ["clarifier", "orienter"]
    assert lignes[0]["message"] == "Je ne sais pas quoi demander"


def test_pas_d_escalade_par_defaut_meme_avec_le_llm(monkeypatch):
    monkeypatch.setenv("ASSISTANT_LLM", "1")
    monkeypatch.setattr("src.llm.URL", "http://127.0.0.1:9")
    reponse, etat = converser("C01", ["Je ne sais pas quoi demander", "rien de précis"])
    assert reponse.escalade is False
    assert reponse.appels_llm == 0
    assert "aucun accès" in reponse.texte.lower()


def test_la_clarification_propose_les_deux_familles_probables():
    from src.contrats import Alternative
    from src.converser.formuler import question_clarification

    question = question_clarification([Alternative("virement", 0.58), Alternative("insatisfaction", 0.23)])
    assert question.endswith("un virement, ou une réclamation ?")
    assert question_clarification([Alternative("compte_identite", 0.39), Alternative("especes", 0.2)]) is None
    assert question_clarification([Alternative("insatisfaction", 0.6), Alternative("conversation", 0.3)]) is None
