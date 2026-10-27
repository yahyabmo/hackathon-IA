"""L'interface web (FastAPI) : configuration, profil, conversation aiguillée."""

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from src.web.api import app  # noqa: E402

client = TestClient(app)


def test_la_page_et_la_configuration():
    assert "Aiguillage" in client.get("/").text
    config = client.get("/api/config").json()
    assert len(config["clients"]) == 8 and config["exemples"]["C01"]
    assert {"niveau1", "niveau2", "actif"} <= set(config["llm"])


def test_le_profil_signale_les_champs_simules():
    profil = client.get("/api/profil/C01").json()
    assert profil["prenom"] == "Inès" and any(c["simule"] for c in profil["champs"])


def test_une_conversation_garde_sa_memoire_et_sa_chaine_de_niveaux():
    demande = {"session": "test-web", "client_id": "C01", "llm_actif": False}
    premier = client.post("/api/message", json={**demande, "message": "J'ai perdu ma carte et je veux faire un virement."}).json()
    assert premier["niveau"] == 0 and premier["question"] == "beneficiaire"
    second = client.post("/api/message", json={**demande, "message": "mon père"}).json()
    assert second["question"] == "montant" and second["chaine"] == [0, 0]
    assert {"trace", "sources", "comprehension", "energie_wh"} <= set(second)
    client.post("/api/nouvelle", json={"session": "test-web"})
    apres = client.post("/api/message", json={**demande, "message": "mon père"}).json()
    assert apres["chaine"] == [apres["niveau"]]  # nouvelle conversation : mémoire vidée
