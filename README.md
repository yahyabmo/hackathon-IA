# Hackathon IA — La Banque Postale × CGI

> **Des idées pour une finance plus intelligente** — 3 jours pour imaginer, développer et présenter une solution IA autour d'un défi du monde bancaire.
> ENSEIRB-MATMECA, salle IA · 26 → 28 octobre

---

## Le défi

> À compléter après la présentation des cas d'usage (lundi 14h30).

| | |
|---|---|
| **Cas d'usage choisi** | _…_ |
| **Problème** | _Quelle douleur, pour qui ?_ |
| **Utilisateur cible** | _Conseiller, client, analyste risque… ?_ |
| **Données fournies** | _Format, volume, confidentialité_ |
| **Notre solution en une phrase** | _…_ |
| **Critères du jury** | _À demander lundi pendant les Q&R_ |

## L'équipe

| Membre | Rôle principal | GitHub |
|---|---|---|
| _…_ | Produit & pitch : cadrage, slides, démo | |
| _…_ | LLM & prompts : client LLM, évaluation des réponses | |
| _…_ | Données & RAG : préparation, indexation, recherche | |
| _…_ | Interface : démo, intégration bout en bout | |

Les rôles indiquent qui est responsable de quoi. Tout le monde code.

## Planning

| Quand | Officiel | Nos jalons internes |
|---|---|---|
| **Lun. 11h** | Accueil salle IA, machines, accès LLM | Le LLM répond sur toutes les machines |
| **Lun. 14h–15h30** | Kickoff, cas d'usage, Q&R | Cas d'usage choisi, section « Le défi » remplie |
| **Lun. soir** | | Périmètre du MVP figé, squelette de bout en bout qui tourne |
| **Mar. midi** | | MVP utilisable sur un vrai exemple |
| **Mar. soir** | | **Gel des fonctionnalités**, on ne fait plus que corriger et peaufiner |
| **Mer. matin** | | Slides + démo enregistrée en secours + 2 répétitions chronométrées |
| **Mer. 13h30** | Soutenances | |
| **Mer. 17h** | Remise des prix, cocktail | |

## Démarrage rapide

```bash
git clone https://github.com/yahyabmo/hackathon-IA.git
cd hackathon-IA
python3 -m venv .venv
source .venv/bin/activate
```

> Les dépendances et les commandes de lancement seront ajoutées ici une fois le dépôt initialisé.

## Accès aux LLMs

| Backend | Où | Détails |
|---|---|---|
| **Ollama local** | Chaque machine de la salle IA | Ministral, nom exact donné par `ollama list` |
| **DeepEirb** | Serveur de l'école | Adresse et liste des modèles communiquées lundi 11h |

> À confirmer lundi 11h : si DeepEirb est compatible avec l'API OpenAI comme Ollama, un seul client suffit et on change de backend par configuration. Demander aussi s'il faut une clé d'API.

## Structure proposée

```
hackathon-IA/
├── app.py              # Démo, l'interface montrée au jury
├── src/                # Code livré (client LLM, traitement des données…)
├── notebooks/          # Explorations ; le code qui marche migre dans src/
├── data/               # Données du défi, jamais versionnées
├── .env.example        # Configuration à copier en .env
└── requirements.txt
```

## Règles d'équipe

1. **`main` doit toujours tourner.** À tout moment, on doit pouvoir lancer la démo depuis `main`.
2. **Branches courtes** : `feat/<sujet>` ou `fix/<sujet>`, mergées dans la demi-journée. On fait `git pull` souvent.
3. **Aucune donnée ni aucun secret dans git.** Les données fournies par les partenaires restent dans `data/` et les clés dans `.env`, les deux listés dans le `.gitignore`.
4. **Les notebooks servent à explorer, `src/` sert à livrer.** Une fonction utilisée par l'app vit dans `src/`.
5. **Un point toutes les ~3h** (5 min debout) : ce qui est fait, ce qui bloque, la suite.
6. **Les prompts sont du code** : on les versionne et on note ce qui a été essayé et pourquoi.

## Checklist soutenance

- [ ] Problème + utilisateur cible expliqués en 30 secondes
- [ ] Démo live sur un **cas réaliste** (préparé à l'avance, testé sur la machine de présentation)
- [ ] **Vidéo de secours** de la démo, au cas où le réseau ou le LLM ne répondrait pas
- [ ] Architecture en un schéma : données → LLM → interface
- [ ] Limites et risques assumés : hallucinations, confidentialité, RGPD, coût
- [ ] Suite du projet : comment La Banque Postale pourrait l'industrialiser
- [ ] Répétition chronométrée (durée à demander aux organisateurs)
