#!/usr/bin/env bash
# Les mesures sur le poste à GPU, par étape (environnement de ./installer.sh).
#
#   ./mesurer.sh niveaux                       # bancs des niveaux 1 et 2 : le plus petit modèle par niveau
#   ./mesurer.sh comprendre                    # compréhension : CPU, puis le LLM qui classe seul
#   ./mesurer.sh abc qwen3:1.7b ministral-3:8b # A/B/C et énergie, avec les modèles retenus (niveau 1, niveau 2)
#   ./mesurer.sh formulation                   # ancien banc : reformuler un conseil (mesuré, écarté)
set -euo pipefail
cd "$(dirname "$0")"
. .venv/bin/activate
export BANC_MACHINE="${BANC_MACHINE:-$(hostname)}" ASSISTANT_ESCALADE=0
MODELES="qwen3:1.7b gemma3:1b ministral-3:3b gemma4:e2b ministral-3:8b"

case "${1:-}" in
    niveaux)
        python -m eval.bench_niveau1 $MODELES
        python -m eval.bench_niveau2 $MODELES ;;
    comprendre)
        python -m eval.bench_comprendre
        python -m eval.bench_comprendre --llm=ministral-3:14b --llm=qwen3:1.7b ;;
    abc)
        n1="${2:?modèle du niveau 1 retenu, ex. qwen3:1.7b}"
        n2="${3:-$n1}"
        python -m eval.bench_abc C B --modele-n1="$n1" --modele-n2="$n2"
        # A : le 14B répond à chaque message ; un lot de 40 suffit pour l'énergie par requête.
        python -m eval.bench_abc A --requetes=40 --repetitions=1 ;;
    formulation)
        python -m eval.bench_formulation ministral-3:14b ministral-3:8b gemma4:e2b ministral-3:3b \
            qwen3:1.7b gemma3:1b
        python -m eval.tableau_formulation ;;
    *)
        sed -n 2,7p "$0"; exit 2 ;;
esac
