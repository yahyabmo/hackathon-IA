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
│   ├── comprendre/             mots_cles, entites, classifieur (bouchon), escalade
│   ├── converser/              dialogue, parcours/*.yaml, formuler, garde_fou, glossaire
│   ├── conseiller/             clients, catalogue, regles, outils
│   └── mesure/                 latence par étage
├── data/
│   ├── raw/                    Banking77 et Bank Marketing, tels que téléchargés (versionnés)
│   └── processed/              clients.json, catalogue.json, glossaire.json
├── eval/
│   ├── scenarios/*.yaml        conversations de référence
│   └── run_scenarios.py
└── tests/
```

## Installation et lancement

Python 3.10 ou supérieur.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Sans modèle installé, l'assistant répond avec ses gabarits. Pour activer le LLM
(sur un poste de la salle, après `ollama pull ministral-3:3b`) :

```bash
cp .env.example .env            # puis ASSISTANT_LLM=1
set -a && source .env && set +a
streamlit run app.py
```

## Tests et scénarios

```bash
python -m pytest -q             # contrats, compréhension, règles, outils, garde-fou, interface
python -m eval.run_scenarios    # les conversations de référence, de bout en bout
```

Un scénario qui passait et qui échoue bloque la fusion.

## Ce qui reste à faire

- **M1** : entraîner le classifieur (`src/comprendre/classifieur.py`) ; fixer τ par balayage ;
  compléter le lexique de mots-clés en mesurant la précision de chaque expression ; écrire le
  test français à la main ; banc A/B/C et CodeCarbon.
- **M2** : choisir le petit LLM en descendant depuis le 14B ; brancher l'escalade sur DeepEirb ;
  glossaire par similarité ; mode « mots simples » ; vidéo de secours.
- **M3** : rattacher chaque client à sa ligne de Bank Marketing ; relever sources et dates du
  catalogue ; modèle d'appétence ; règles complètes ; scénarios jusqu'à 30.

## Conventions Git

- `main` doit rester exécutable, et ses tests verts.
- Branches courtes : `m1/<sujet>`, `m2/<sujet>`, `m3/<sujet>`, fusionnées dans la demi-journée
  après relecture du suppléant.
- Garder les parcours, les prompts et les règles versionnés.
- Mettre le code livré dans `src/`, pas seulement dans des notebooks.
- Ne jamais versionner de secrets (`.env`), de modèles ou de caches.
