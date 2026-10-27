import copy
import json

import pytest

from src.conseiller import catalogue as cat


def test_catalogue_complet_source_date_unites():
    d = json.loads(cat.FICHIER.read_text())
    cat.valider_catalogue(d)
    assert len(d["produits"]) == 12
    assert all(p["unite_plafond"] == "EUR" for p in d["produits"].values() if "plafond" in p)
    for cle in ("taux_indicatif_credit_immobilier", "taux_indicatif_pret_personnel"):
        p = cat.parametre_detail(cle)
        assert p["nature"] == "reference_statistique"
        assert "banque-france.fr" in p["source"]
    assert cat.parametre_detail("seuil_prudence_conso")["nature"] == "heuristique_interne"
    assert cat.parametre("plafond_revenu_lep") is None  # table, pas seuil universel


def test_accesseurs_ne_modifient_pas_la_source():
    p = cat.produit("livret_a")
    p["plafond"] = 0
    assert cat.produit("livret_a")["plafond"] == 22950
    p = cat.parametre_detail("plafond_revenu_lep")
    p["plafonds"].clear()
    assert cat.parametre_detail("plafond_revenu_lep")["plafonds"]


@pytest.mark.parametrize("champ,valeur", [("source", ""), ("nature", "inventee"),
    ("statut", ""), ("releve_le", "demain"), ("plafond", -1)])
def test_catalogue_invalide_refuse(champ, valeur):
    d = copy.deepcopy(cat._catalogue())
    d["produits"]["livret_a"][champ] = valeur
    with pytest.raises(ValueError):
        cat.valider_catalogue(d)
