# Hackathon IA — Assistant bancaire frugal

Prototype pour le hackathon La Banque Postale × CGI × ENSEIRB-MATMECA.
L'objectif est de construire un assistant bancaire personnalisé, explicable,
local et open source. Le socle actuel fonctionne sans GPU, Ollama ni modèle
téléchargé ; les modules spécialisés seront ajoutés progressivement.

## Architecture

```text
app.py
  → src.assistant.reply()
      → comprendre : intention et entités
      → converser : état et parcours déterministe
      → conseiller : profils, produits et règles explicables
      → agir : actions simulées avec confirmation obligatoire
      → formuler : gabarits ou petit LLM local
      → mesure : latence, énergie, taille et qualité
```

Les contrats partagés sont définis dans `src/contrats.py`. Les implémentations
actuelles sont des stubs volontairement prudents : elles ne simulent pas une
prédiction ML ni une recommandation bancaire validée.

## Responsabilités

| Membre | Module principal |
|---|---|
| Younes (M1) | Compréhension des intentions, modèles et mesures |
| Yahya (M2) | Dialogue, orchestration, LLM local et interface |
| Sohayb (M3) | Profils clients, recommandations, actions simulées et tests |

Les contrats de `src/contrats.py` sont la référence commune pour travailler en
parallèle sans coupler les modules.

## Structure

```text
├── app.py
├── src/
│   ├── contrats.py
│   ├── assistant.py
│   ├── comprendre/
│   ├── converser/parcours/
│   ├── conseiller/
│   └── mesure/
├── data/raw/       # données publiques ou fournies, ignorées par Git
├── data/processed/ # données préparées, versionnables si nécessaire
├── eval/
└── tests/
```

Les documents du briefing et les données locales existantes sont conservés.
Ne jamais placer de secrets ou de nouvelles données sensibles dans Git.

## Installation et lancement

Python 3.11 ou supérieur est recommandé.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

L'application affiche un chat minimal et un panneau technique. Le scénario
« carte perdue » permet de vérifier la chaîne sans service externe.

## Tests

```bash
python -m pytest -q
```

## Configuration future

Copier `.env.example` vers `.env` lorsque le module LLM local sera branché.
Les paramètres Ollama resteront configurables par environnement ; aucune clé
ou donnée sensible ne doit être commitée.

## Conventions Git

- `main` doit rester exécutable.
- Utiliser des branches courtes : `feat/<sujet>` ou `fix/<sujet>`.
- Garder les prompts et les règles versionnés.
- Mettre le code livré dans `src/`, pas seulement dans des notebooks.
- Ne pas versionner `data/raw/`, les modèles, les caches ou `.env`.
