import pytest

from src.comprendre import classifieur


def pytest_configure(config):
    config.addinivalue_line("markers", "classifieur: le test utilise le vrai classifieur (e5-small)")


@pytest.fixture(autouse=True)
def journal_temporaire(tmp_path, monkeypatch):
    """Les tests écrivent le journal des messages non compris hors du dépôt."""

    monkeypatch.setenv("INCOMPRIS_FICHIER", str(tmp_path / "incompris.jsonl"))


@pytest.fixture(autouse=True)
def sans_classifieur(request, monkeypatch):
    """Les tests de dialogue ne dépendent pas d'un modèle appris : le classifieur est
    coupé, sauf pour les tests marqués ``classifieur``. Le rejeu des scénarios
    (eval/run_scenarios.py) passe, lui, par le vrai classifieur."""

    if request.node.get_closest_marker("classifieur") is None:
        monkeypatch.setattr(classifieur, "predire", lambda message: None)
