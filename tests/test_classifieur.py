"""Le classifieur de l'étage 1 : têtes versionnées, seuil, routage (vrai modèle)."""

import json

import numpy as np
import pytest

from src.assistant import reply
from src.comprendre import classifieur
from src.contrats import EtatConversation
from src.taxonomie import INTENTION_VERS_FAMILLE

pytestmark = pytest.mark.classifieur


def test_les_tetes_couvrent_toute_la_taxonomie():
    tetes = classifieur.Tetes.charger(classifieur.TETES)
    assert set(tetes.intentions) == set(INTENTION_VERS_FAMILLE)
    assert tetes.coef_intention.shape == (85, 384) and tetes.coef_famille.shape == (14, 384)


def test_le_seuil_vient_du_balayage():
    meta = json.loads(classifieur.META.read_text(encoding="utf-8"))
    assert classifieur.SEUIL_TAU == meta["tau"]
    assert meta["validation"]["precision_acceptes"] >= meta["precision_visee"]


def test_l_intention_reste_dans_la_famille_choisie():
    tetes = classifieur.Tetes.charger(classifieur.TETES)
    for graine in range(20):
        v = np.random.default_rng(graine).normal(size=384).astype(np.float32)
        famille, intention, confiance, alternatives = tetes.predire(v / np.linalg.norm(v))
        assert INTENTION_VERS_FAMILLE[intention] == famille == alternatives[0][0]
        assert 0 <= confiance <= 1


@pytest.fixture(scope="module")
def modele():
    if not classifieur.disponible():
        pytest.skip("sentence-transformers ou le modèle e5-small absent")


def test_une_demande_de_service_en_francais_sans_traduction(modele):
    c = classifieur.predire("Je n'ai toujours pas reçu ma nouvelle carte")
    assert c.famille == "carte_commande" and c.confiance >= classifieur.SEUIL_TAU
    assert c.exemple_proche  # la phrase d'entraînement la plus proche, pour le panneau « pourquoi »


def test_le_classifieur_rattrape_ce_que_les_mots_cles_ratent(modele):
    reponse, _ = reply("Ma carte ne marche plus au distributeur", "C01", EtatConversation())
    assert reponse.comprehension.niveau == "classifieur"
    assert reponse.comprehension.famille == "carte_usage"
    assert "conseiller" in reponse.texte  # pas de parcours guidé : on propose le rappel
