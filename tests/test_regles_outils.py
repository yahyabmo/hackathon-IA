"""Tests métier M3 : le chatbot conseille, il n'exécute aucune opération."""
import pytest

from src.conseiller import clients, conseiller


def test_credit_immobilier_explicable_sans_decision():
    c = conseiller("credit_immobilier", clients.profil("C07"),
                    {"revenus_nets": 2900, "mensualites_en_cours": 0,
                     "prix_bien": 250000, "apport": 25000})
    assert c.faits["mensualite"] > 0
    assert c.faits["decision_bancaire"] is False
    assert c.ecartees
    assert c.faits["sources_produits"] if "sources_produits" in c.faits else True


def test_epargne_personnalisee_et_justifiee():
    c = conseiller("epargne_projet", clients.profil("C08"),
                    {"pour_qui": "soi", "horizon_mois": 24, "montant_mensuel": 50})
    assert c.propositions
    assert all(p.raisons for p in c.propositions)
    assert all(e.raison for e in c.ecartees)


@pytest.mark.parametrize("intention,slots", [
    ("credit_immobilier", {"prix_bien": -1, "apport": 0}),
    ("credit_conso", {"montant": 0, "duree_mois": 12}),
])
def test_entrees_financieres_invalides_ne_calculent_pas(intention, slots):
    c = conseiller(intention, clients.profil("C07"), slots)
    assert c.manque
    assert "mensualite" not in c.faits
