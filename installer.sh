#!/usr/bin/env bash
# Installation de zéro sur un poste (salle, RTX) : environnement, dépendances, modèles, vérifications.
#
#   ./installer.sh          # torch avec CUDA (poste à GPU)
#   ./installer.sh cpu      # torch sans CUDA, bien plus léger (portable)
#   MODELES="ministral-3:3b" ./installer.sh   # ne télécharger que ces modèles Ollama
set -euo pipefail
cd "$(dirname "$0")"

MODELES="${MODELES:-ministral-3:14b ministral-3:8b gemma4:e2b ministral-3:3b qwen3:1.7b gemma3:1b}"

python3 -m venv .venv
. .venv/bin/activate
pip install -q --upgrade pip
if [ "${1:-}" = "cpu" ]; then
    pip install -q --index-url https://download.pytorch.org/whl/cpu torch
fi
pip install -q -r requirements.txt

echo "Encodeur de compréhension (une fois, ensuite hors ligne)…"
python -c "from sentence_transformers import SentenceTransformer as S; S('intfloat/multilingual-e5-small')"
[ -f models/exemples.npz ] || python -m src.comprendre.entrainer --exemples-seulement

if command -v ollama >/dev/null; then
    for modele in $MODELES; do ollama pull "$modele"; done
else
    echo "Ollama absent : https://ollama.com/download, puis relancer ce script."
fi

python -m pytest -q
python -m eval.run_scenarios
echo
echo "Prêt. Démo : . .venv/bin/activate && streamlit run app.py"
echo "Mesures : ./mesurer.sh (voir le README)"
