"""Intégrité des personnages fictifs et traçabilité, sans modifier les sources."""
import csv
import hashlib
from pathlib import Path

import pytest

from src.conseiller import clients


def test_huit_profils_valides_et_independants():
    assert [i for i, _ in clients.lister()] == [f"C{i:02}" for i in range(1, 9)]
    for identifiant, _ in clients.lister():
        p = clients.profil(identifiant)
        clients.valider_profil(p)
        p["cartes"].clear()
        p["provenance"]["solde"]["nature"] = "faux"
        assert clients.profil(identifiant)["cartes"]
        assert clients.est_simule(clients.profil(identifiant), "solde")
    with pytest.raises(KeyError, match="client inconnu"):
        clients.profil("C99")


@pytest.mark.parametrize("champ,valeur", [
    ("id", "123"), ("age", True), ("age", -1), ("age", 18.5),
    ("revenus_nets", float("nan")), ("epargne", -1),
    ("solde", float("inf")), ("livrets", {"livret_a": 999999}),
    ("cartes", [{"id": "X", "statut": "invente"}]),
    ("beneficiaires", [{}]), ("enfants", [130]),
    ("domicile_fiscal_france", "oui"), ("provenance", {}),
])
def test_profils_invalides(champ, valeur):
    p = clients.profil("C01")
    p[champ] = valeur
    with pytest.raises(ValueError):
        clients.valider_profil(p)


def test_absence_et_inconnu_distincts():
    p = clients.profil("C01")
    p["revenus_nets"] = None
    clients.valider_profil(p)
    del p["revenus_nets"]
    with pytest.raises(ValueError, match="incomplet"):
        clients.valider_profil(p)


def test_ancrages_documentaires_verifiables():
    racine = Path(__file__).resolve().parents[1]
    for identifiant, _ in clients.lister():
        p = clients.profil(identifiant)
        a = p["ancrage_bank_marketing"]
        fichier = racine / a["fichier"]
        if not fichier.exists():
            pytest.skip("données brutes facultatives absentes de ce checkout")
        assert hashlib.sha256(fichier.read_bytes()).hexdigest() == a["sha256"]
        with fichier.open() as flux:
            lignes = list(csv.DictReader(flux, delimiter=";"))
        ligne = lignes[a["ligne"] - 2]
        for champ in ("age", "job", "marital", "housing", "loan"):
            if champ in a:
                assert str(a[champ]) == ligne[champ]
        assert a["nature"] == "rapprochement_documentaire"
        assert p["provenance"]["solde"]["nature"] == "simulation"


def test_identifiants_dupliques_refuses(tmp_path, monkeypatch):
    import json
    fichier = tmp_path / "clients.json"
    p = clients.profil("C01")
    fichier.write_text(json.dumps({"clients": [p, p]}))
    monkeypatch.setattr(clients, "FICHIER", fichier)
    clients._clients.cache_clear()
    try:
        with pytest.raises(ValueError, match="dupliqué"):
            clients.lister()
    finally:
        clients._clients.cache_clear()
