# Hackathon IA — Assistant bancaire frugal

Prototype pour le hackathon La Banque Postale × CGI × ENSEIRB-MATMECA (sujet 1).
Un assistant bancaire personnalisé, explicable, local et open source, qui
comprend, pose les bonnes questions, conseille et oriente — avec, à chaque message,
le plus petit moyen qui suffit. La proposition complète est dans [`main-resume.pdf`](main-resume.pdf).

## Architecture : un aiguilleur

À chaque message, l'aiguilleur choisit le plus petit moyen qui suffit ; une
conversation peut passer d'un niveau à l'autre (1 → 2 → 0 → 2). La mémoire est
commune à tous les niveaux. Schémas : [`rapport/schema-aiguilleur.pdf`](rapport/schema-aiguilleur.pdf).

```text
src.assistant.reply(message, client_id, etat)
  entrée commune (sans LLM, ~6 ms) : barrières, entités (regex), contexte,
      mots-clés (toutes les demandes), classifieur e5-small + 2 régressions logistiques (τ)
  aiguilleur (src/aiguilleur.py) : 5 signaux → niveau
  niveau 0  règles : automate + parcours YAML, file des demandes par urgence, mémoire,
            reprise après une parenthèse, vraisemblance des montants ; règles de conseil
            (HCSF, plafonds) ; gabarits, mention légale, mots simples. Aucun LLM.
  niveau 1  petit LLM interprète (src/comprendre/interprete.py) : RAG d'exemples (8 phrases
            d'entraînement proches), JSON imposé par une grammaire (sortie contrainte), vérifié
            par le code ; il ne voit pas le profil et ne répond jamais : retour au niveau 0.
  niveau 2  RAG (src/rag.py) : 37 fiches sourcées, index e5-small en mémoire, seuil de
            pertinence ; un LLM rédige en citant [1] ; garde-fou (chiffres des extraits, fidélité,
            citation), sinon l'extrait de la meilleure fiche.
  mesure    chaque étape : latence, modèle, tokens, appel au LLM ; niveau et raison dans la réponse
```

L'assistant n'a **aucun accès au compte** et ne réalise aucune opération
(périmètre du kick-off) : il explique, conseille et oriente. Les contrats
partagés sont dans `src/contrats.py` ; la taxonomie commune (14 familles,
85 intentions : les 77 de Banking77, non traduites, et 8 créées par l'équipe)
dans `src/taxonomie.py`.

## Responsabilités

| Membre | Module | Fichiers |
|---|---|---|
| Younes (M1) | Comprendre et mesurer | `src/comprendre/`, `src/mesure/`, bancs dans `eval/` |
| Yahya (M2) | Aiguilleur, niveaux 1 et 2, converser, formuler, interface | `src/assistant.py`, `src/aiguilleur.py`, `src/rag.py`, `src/comprendre/interprete.py`, `src/converser/`, `src/llm.py`, `src/web/` |
| Sohayb (M3) | Profils, catalogue, conseiller, règles métier | `src/conseiller/`, `eval/run_scenarios.py`, `tests/` |

## Structure

```text
├── app.py                      interface Streamlit (secours)
├── src/
│   ├── contrats.py             structures partagées
│   ├── taxonomie.py            14 familles, 85 intentions
│   ├── assistant.py            reply() : entrée commune, aiguillage, niveaux, mémoire
│   ├── aiguilleur.py           les 5 signaux et le choix du niveau, l'ordre d'urgence
│   ├── rag.py                  niveau 2 : fiches, index, recherche, rédaction citée, garde-fou
│   ├── llm.py                  Ollama ou vLLM, sortie contrainte par un schéma JSON
│   ├── texte.py                normalisation, format des nombres
│   ├── comprendre/             mots_cles, entites, classifieur (e5-small), entrainer, interprete (niveau 1), escalade
│   ├── converser/              dialogue, parcours/*.yaml, formuler, garde_fou, glossaire
│   ├── conseiller/             clients, catalogue, regles, validation
│   ├── web/                    interface de la démo (FastAPI + page HTML, style Timso AI)
│   └── mesure/                 latence par étage
├── data/
│   ├── raw/                    Banking77 et Bank Marketing, tels que téléchargés (versionnés)
│   └── processed/              clients, catalogue, glossaire, fiches (RAG), exemples_fr, test_fr,
│                               bancs des niveaux, têtes du classifieur
├── eval/
│   ├── scenarios/*.yaml        conversations de référence
│   ├── run_scenarios.py
│   ├── bench_comprendre.py     compréhension, anglais et français
│   ├── bench_niveau1.py        niveau 1 : le plus petit LLM qui comprend (avec et sans RAG d'exemples)
│   ├── bench_niveau2.py        niveau 2 : recherche, rédaction citée, garde-fou
│   ├── bench_abc.py            A/B/C : réussite, énergie, latence, mémoire, part de chaque niveau
│   ├── bench_formulation.py    reformuler un conseil (mesuré, écarté)
│   └── resultats/              mesures (CSV, JSON)
├── installer.sh                installation de zéro sur un poste
├── mesurer.sh                  les mesures sur le poste à GPU
└── tests/
```

## Installation et lancement

Python 3.10 ou supérieur. Sur un nouveau poste, une commande installe tout
(environnement, dépendances, encodeur, modèles Ollama) et lance les tests et
les scénarios :

```bash
./installer.sh                    # poste à GPU ; « ./installer.sh cpu » sur un portable
source .venv/bin/activate
ASSISTANT_LLM=1 python -m src.web # interface de la démo : http://localhost:8000
```

`ASSISTANT_LLM=1` permet les niveaux 1 et 2 (Ollama ou vLLM) ; sans lui, ou si
le serveur ne répond pas, l'aiguilleur reste au niveau 0 et le RAG répond par
l'extrait de la fiche. Les modèles des niveaux se choisissent avec
`OLLAMA_MODEL_NIVEAU1` et `OLLAMA_MODEL_NIVEAU2`. `?client=C07&rejouer` rejoue
les exemples d'un profil.

L'interface a deux vues : « Démo » (niveaux, pourquoi, sources, énergie et CO₂ de
chaque réponse) et « Utilisateur » (les messages seuls). Le bouton « Scénarios »
ouvre les trois conversations de la démonstration (`src/web/scenarios.yaml`) :
chaque clic sur « Envoyer › », ou la flèche →, tape et envoie le message suivant.
`?scenario=2&utilisateur` ouvre directement le scénario 2 en vue utilisateur. L'interface Streamlit de secours reste disponible :
`streamlit run app.py`.

L'encodeur `multilingual-e5-small` est téléchargé une fois, puis `HF_HUB_OFFLINE=1`
évite tout accès réseau. Les têtes du classifieur sont versionnées
(`data/processed/classifieur.npz`) ; `python -m src.comprendre.entrainer` les
réentraîne (environ 4 min sur CPU) et refixe τ par balayage.

## Tests et scénarios

```bash
python -m pytest -q             # contrats, compréhension, règles, conseil, garde-fou, interface
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
./mesurer.sh niveaux                         # niveaux 1 et 2 : le plus petit modèle qui tient chacun
./mesurer.sh comprendre                      # compréhension, plus le LLM qui classe seul
./mesurer.sh abc qwen3:1.7b ministral-3:8b   # A/B/C et énergie, avec les modèles retenus
```

Les résultats (`eval/resultats/`) et les tableaux du support (`rapport/resultats-*.tex`)
sont écrits par ces commandes ; le support se recompile ensuite avec `pdflatex`.

## Ce qui reste à faire

- **Sur le poste à GPU** : `./mesurer.sh niveaux`, puis `abc` avec les modèles retenus.
- **Jugement humain** : les réponses de la configuration A sont à juger
  (`eval/resultats/abc-A-transcriptions.csv`) ; le test français
  (`data/processed/test_fr.yaml`) est à relire par l'équipe.
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
