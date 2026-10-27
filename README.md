# Hackathon IA — Assistant bancaire frugal

Prototype pour le hackathon La Banque Postale × CGI × ENSEIRB-MATMECA (sujet 1).
Un assistant bancaire personnalisé, explicable, local et open source, qui
comprend, pose les bonnes questions, conseille et agit — avec le plus petit
calcul qui suffit. La proposition complète est dans [`main-resume.pdf`](main-resume.pdf).

## Architecture : une cascade

Chaque étage ne passe la main au suivant que s'il ne sait pas faire lui-même.
Dans le cas normal, un tour de conversation fait **au plus un appel au LLM, à la fin**.

```text
app.py
  → src.assistant.reply(message, client_id, etat)
      1. comprendre   réponse attendue ? → mots-clés → classifieur (e5-small + LR, seuil τ)
                      sinon : question de clarification, puis escalade (LLM 14B, comptée)
      2. converser    automate qui lit les parcours YAML ; ne redemande jamais ce que le profil sait
      3. conseiller   règles publiques (HCSF, plafonds) : propositions, raisons, produits écartés
      4. agir         outils sur un SI simulé ; tout effet de bord exige un « oui » du client
      5. formuler     gabarit, ou petit LLM (ministral-3:3b) sous garde-fou ; mention légale crédit
      ·  mesurer      trace par étage : latence, modèle, tokens, appels au LLM
```

Les contrats partagés sont dans `src/contrats.py` ; la taxonomie commune
(14 familles, 85 intentions : les 77 de Banking77, non traduites, et 8 créées
par l'équipe) dans `src/taxonomie.py`.

## Responsabilités

| Membre | Module | Fichiers |
|---|---|---|
| Younes (M1) | Comprendre et mesurer | `src/comprendre/`, `src/mesure/`, bancs dans `eval/` |
| Yahya (M2) | Converser, formuler, escalade, interface | `src/assistant.py`, `src/converser/`, `src/llm.py`, `app.py` |
| Sohayb (M3) | Conseiller et agir, rejeu des scénarios | `src/conseiller/`, `eval/run_scenarios.py`, `tests/` |

## Structure

```text
├── app.py                      interface Streamlit
├── src/
│   ├── contrats.py             structures partagées
│   ├── taxonomie.py            14 familles, 85 intentions
│   ├── assistant.py            reply() : la cascade
│   ├── llm.py                  accès à Ollama (désactivé par défaut)
│   ├── texte.py                normalisation, format des nombres
│   ├── comprendre/             mots_cles, entites, classifieur (e5-small), entrainer, escalade
│   ├── converser/              dialogue, parcours/*.yaml, formuler, garde_fou, glossaire
│   ├── conseiller/             clients, catalogue, regles, outils
│   └── mesure/                 latence par étage
├── data/
│   ├── raw/                    Banking77 et Bank Marketing, tels que téléchargés (versionnés)
│   └── processed/              clients, catalogue, glossaire, exemples_fr, test_fr, têtes du classifieur
├── eval/
│   ├── scenarios/*.yaml        conversations de référence
│   ├── run_scenarios.py
│   ├── bench_comprendre.py     compréhension, anglais et français
│   ├── bench_formulation.py    choix du LLM en descendant en taille
│   ├── bench_abc.py            A/B/C : réussite, énergie, latence, mémoire
│   └── resultats/              mesures (CSV, JSON)
├── installer.sh                installation de zéro sur un poste
├── mesurer.sh                  les mesures sur le poste à GPU
└── tests/
```

## Installation et lancement

Python 3.10 ou supérieur. Sur un nouveau poste, une commande installe tout (environnement,
dépendances, encodeur, modèles Ollama) et lance les tests et les scénarios :

```bash
./installer.sh          # poste à GPU ; « ./installer.sh cpu » sur un portable
source .venv/bin/activate
streamlit run app.py
```

L'encodeur `multilingual-e5-small` est téléchargé une fois, puis `HF_HUB_OFFLINE=1` évite
tout accès réseau. Les têtes du classifieur sont versionnées
(`data/processed/classifieur.npz`) ; `python -m src.comprendre.entrainer` les réentraîne
(environ 4 min sur CPU) et refixe τ par balayage.

Sans modèle installé, l'assistant répond avec ses gabarits. Pour activer le LLM
de formulation (sur un poste de la salle, après `ollama pull ministral-3:3b`) :

```bash
cp .env.example .env            # puis ASSISTANT_LLM=1
set -a && source .env && set +a
streamlit run app.py
```

Le serveur se choisit par rôle : Ollama sur un poste de la salle (défaut) ou vLLM
sur DeepEirb (`LLM_API=vllm`, `VLLM_BASE_URL=…/v1`) ; `LLM_API_FORMULATION` et
`LLM_API_ESCALADE` permettent de garder le petit modèle en local et le gros sur
DeepEirb. L'interface affiche l'état réel du serveur et précharge le modèle.

L'escalade vers le gros modèle reste désactivée (`ASSISTANT_ESCALADE=0`) : un
message incompris après la question de clarification est noté dans
`eval/incompris.jsonl` (lecture : `python -m src.incompris`) et le client se voit
proposer un conseiller. Le journal sert à enrichir le lexique et l'entraînement.

## Tests et scénarios

```bash
python -m pytest -q             # contrats, compréhension, règles, outils, garde-fou, interface
python -m eval.run_scenarios    # les conversations de référence, de bout en bout
python -m eval.bench_formulation --situations     # les 30 conseils du banc, sans LLM
python -m eval.bench_formulation ministral-3:14b gemma4:e2b ministral-3:8b ministral-3:3b qwen3:1.7b gemma3:1b
```

Le banc de formulation choisit le LLM en descendant en taille : on garde le plus
petit à zéro nombre inventé et 27 bonnes réponses sur 30 (CSV à juger dans
`eval/resultats/`, colonnes `juge_1` et `juge_2`). Le LLM ne réécrit que le corps
du conseil : la question oui / non, les hypothèses et la mention légale restent
hors LLM. `BANC_MACHINE="RTX 3070"` nomme le poste de mesure ; ensuite
`python -m eval.tableau_formulation` écrit le tableau du support.

`python -m eval.demo_secours` rejoue le script de la démo et écrit
`rapport/demo-secours.tex`, à compiler, au cas où la démo en direct échoue.

Un scénario qui passait et qui échoue bloque la fusion.

## Mesures sur le poste à GPU

```bash
./mesurer.sh formulation     # 14B → 1B ; puis juger les CSV de eval/resultats/ (juge_1, juge_2)
./mesurer.sh comprendre      # compréhension, plus le LLM qui classe seul
./mesurer.sh abc qwen3:1.7b  # A/B/C et énergie, avec le modèle de formulation retenu
./mesurer.sh support         # tableaux et support recompilés
```

Le 14B (9,1 Go) déborde des 8 Go d'une RTX 3070 : il tourne en partie sur le processeur,
plus lentement, et ses mesures restent valables. S'il est trop lent, le retirer de
`mesurer.sh formulation` et le mesurer sur une RTX 3060 (12 Go) de la salle.

## Ce qui reste à faire

Tout le code est en place ; il reste des mesures et des décisions d'équipe.

- **Sur le poste à GPU** : `./mesurer.sh formulation`, `comprendre`, puis `abc` (voir plus haut).
- **Jugement humain** : deux membres jugent les réponses du banc de formulation ; on retient le
  plus petit modèle à zéro nombre inventé et 27 bonnes réponses sur 30, puis on le met dans
  `OLLAMA_MODEL`. Les réponses de la configuration A sont aussi à juger
  (`eval/resultats/abc-A-transcriptions.csv`).
- **Test français** (`data/processed/test_fr.yaml`) : à relire par l'équipe.
- **M3** : le modèle d'appétence n'est pas fait, par choix : les règles sont explicables et
  aucune notation de client n'est faite. Points de coordination :
  [`infos/M3_INTEGRATION.md`](infos/M3_INTEGRATION.md).

## Conventions Git

- `main` doit rester exécutable, et ses tests verts.
- Branches courtes : `m1/<sujet>`, `m2/<sujet>`, `m3/<sujet>`, fusionnées dans la demi-journée
  après relecture du suppléant.
- Garder les parcours, les prompts et les règles versionnés.
- Mettre le code livré dans `src/`, pas seulement dans des notebooks.
- Ne jamais versionner de secrets (`.env`), de modèles ou de caches.
