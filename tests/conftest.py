import pytest


@pytest.fixture(autouse=True)
def journal_temporaire(tmp_path, monkeypatch):
    """Les tests écrivent le journal des messages non compris hors du dépôt."""

    monkeypatch.setenv("INCOMPRIS_FICHIER", str(tmp_path / "incompris.jsonl"))
