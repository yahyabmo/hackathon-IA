import pytest

from src.comprendre import comprendre
from src.comprendre.entites import extraire, oui_non
from src.comprendre.mots_cles import detecter
from src.contrats import EtatConversation


@pytest.mark.parametrize("message, intention", [
    ("J'ai perdu ma carte hier soir, je fais quoi ?", "lost_or_stolen_card"),
    ("ON M'A VOLÉ MA CB", "lost_or_stolen_card"),
    ("Bonjour, j'ai perdu ma carte", "lost_or_stolen_card"),
    ("Pourquoi j'ai payé 8 € de frais ce mois-ci ?", "extra_charge_on_statement"),
    ("Je voudrais mettre de côté pour mes enfants.", "epargne_projet"),
    ("Je dois envoyer 500 € à mon fils.", "faire_virement"),
    ("Je veux un crédit pour acheter une voiture.", "credit_conso"),
    ("Votre appli ne marche jamais !", "insatisfaction"),
    ("Je veux acheter un appartement", "credit_immobilier"),
    ("Je veux faire un prêt étudiant, comment je fais ?", "pret_etudiant"),
    ("C'est quoi un TAEG ?", "question_definition"),
])
def test_les_mots_cles_reconnaissent_les_situations_du_sujet(message, intention):
    resultat = detecter(message)
    assert resultat is not None and resultat.intention == intention


def test_le_mot_carte_seul_ne_suffit_pas():
    assert detecter("Je voudrais commander une nouvelle carte") is None


def test_un_seul_mot_cle_dans_une_longue_phrase_ne_suffit_pas():
    long = ("Je voulais vous demander, avant de prendre une décision pour la suite de mes projets "
            "personnels et familiaux, si je pourrais envoyer quelque chose")
    assert detecter(long) is None


def test_deux_sujets_a_la_fois_ne_concluent_pas():
    assert detecter("J'ai perdu ma carte et je veux acheter un appartement") is None


def test_une_reponse_attendue_n_est_pas_une_nouvelle_demande():
    etat = EtatConversation(parcours="credit_immobilier", famille="credit", info_attendue="prix_bien")
    resultat = comprendre("250000", etat)
    assert resultat.niveau == "reponse_attendue"
    assert resultat.intention == "credit_immobilier"


def test_un_nouveau_sujet_interrompt_le_parcours():
    etat = EtatConversation(parcours="credit_immobilier", famille="credit", info_attendue="prix_bien")
    assert comprendre("J'ai perdu ma carte", etat).intention == "lost_or_stolen_card"


def test_entites():
    entites = extraire("Autour de 250 000, et je peux mettre les 25 000")
    assert entites["montants"] == [250000, 25000]
    assert extraire("hier soir vers 22h").get("montants") is None
    assert extraire("dans 10 ans, 100 euros par mois") == {"duree_mois": 120, "montants": [100]}
    assert extraire("250k")["montants"] == [250000]
    assert extraire("envoyer 500 € à mon fils")["lien"] == "fils"


@pytest.mark.parametrize("message, attendu", [("oui", True), ("Oui, vas-y", True), ("non merci", False),
                                              ("je ne sais pas", None)])
def test_oui_non(message, attendu):
    assert oui_non(message) is attendu
