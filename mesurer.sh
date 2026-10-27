#!/usr/bin/env bash
# Les mesures sur le poste à GPU, par étape (environnement de ./installer.sh).
#
#   ./mesurer.sh formulation     # banc de formulation, du 14B au 1B (CSV à juger ensuite)
#   ./mesurer.sh comprendre      # compréhension : CPU, puis le LLM qui classe seul
#   ./mesurer.sh abc qwen3:1.7b  # A/B/C et énergie, avec le modèle de formulation retenu
#   ./mesurer.sh support         # tableaux et support de soutenance recompilés
set -euo pipefail
cd "$(dirname "$0")"
. .venv/bin/activate
export BANC_MACHINE="${BANC_MACHINE:-RTX 3070}" ASSISTANT_ESCALADE=0

case "${1:-}" in
    formulation)
        python -m eval.bench_formulation ministral-3:14b ministral-3:8b gemma4:e2b ministral-3:3b \
            qwen3:1.7b gemma3:1b
        python -m eval.tableau_formulation ;;
    comprendre)
        python -m eval.bench_comprendre
        python -m eval.bench_comprendre --llm=ministral-3:14b --llm=qwen3:1.7b ;;
    abc)
        python -m eval.bench_abc C B --modele-b="${2:?modèle de formulation retenu, ex. qwen3:1.7b}"
        # A : le 14B répond à chaque message ; un lot de 40 suffit pour l'énergie par requête.
        python -m eval.bench_abc A --requetes=40 --repetitions=1 ;;
    support)
        python -m eval.tableau_formulation
        (cd rapport && pdflatex -interaction=nonstopmode soutenance.tex >/dev/null \
            && pdflatex -interaction=nonstopmode soutenance.tex >/dev/null \
            && rm -f soutenance.aux soutenance.log soutenance.nav soutenance.out soutenance.snm soutenance.toc)
        echo "rapport/soutenance.pdf recompilé" ;;
    *)
        sed -n 2,7p "$0"; exit 2 ;;
esac
