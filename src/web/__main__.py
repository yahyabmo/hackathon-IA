"""``python -m src.web`` : lance l'interface sur http://localhost:8000 (``PORT`` pour en changer)."""

import os

import uvicorn

from ..comprendre import classifieur
from .. import llm, rag

if __name__ == "__main__":
    classifieur.prechauffer()  # le jury ne paie pas le chargement de l'encodeur
    rag.disponible()  # index des fiches, une fois
    if llm.actif():  # le petit LLM des niveaux 1 et 2, chargé avant le premier client
        for modele in dict.fromkeys((llm.MODELE_NIVEAU1, llm.MODELE_NIVEAU2)):
            print(f"Préchargement de {modele} : {'prêt' if llm.prechauffer(modele) else 'injoignable'}")
    uvicorn.run("src.web.api:app", host=os.getenv("HOTE", "0.0.0.0"), port=int(os.getenv("PORT", "8000")))
