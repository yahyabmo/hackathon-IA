"""``python -m src.web`` : lance l'interface sur http://localhost:8000 (``PORT`` pour en changer)."""

import os

import uvicorn

from ..comprendre import classifieur
from .. import rag

if __name__ == "__main__":
    classifieur.prechauffer()  # le jury ne paie pas le chargement de l'encodeur
    rag.disponible()  # index des fiches, une fois
    uvicorn.run("src.web.api:app", host=os.getenv("HOTE", "0.0.0.0"), port=int(os.getenv("PORT", "8000")))
