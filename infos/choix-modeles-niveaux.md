# Choix des modèles des niveaux 1 et 2

Mesuré sur **DeepEirb** (2 × RTX 6000 Ada, 48 Go), le 27 octobre 2026, avec
`./mesurer.sh niveaux`. Les fichiers détaillés sont `eval/resultats/niveau1.json`
et `eval/resultats/niveau2.json` (poussés depuis DeepEirb).

## Décision : `qwen3:1.7b` pour les deux niveaux

- **Niveau 1** : c'est le plus petit modèle qui atteint le seuil (30 messages
  justes sur 36), à condition d'avoir le RAG d'exemples.
- **Niveau 2** : c'est le seul à 22 réponses justes sur 22.
- **Un seul modèle de 1,4 Go** est donc chargé pour les deux niveaux.

C'est la règle du hackathon : le plus petit modèle qui suffit, choisi sur mesure.

Pour plus de marge au niveau 1, l'alternative est `ministral-3:3b` (33 sur 36),
pour un modèle deux fois plus gros. Ce n'est pas le choix retenu.

Le code utilise `qwen3:1.7b` par défaut (`src/llm.py`). Pour en changer :
`OLLAMA_MODEL_NIVEAU1` et `OLLAMA_MODEL_NIVEAU2`.

## Niveau 1 : comprendre un message flou (36 messages)

| Modèle | Taille | Avec RAG d'exemples | Sans RAG d'exemples | JSON valide | Latence p50 |
|---|---|---|---|---|---|
| **qwen3:1.7b** | **1,4 Go** | **30 / 36** | 15 / 36 | 100 % | **188 ms** |
| gemma3:1b | 0,8 Go | 17 / 36 | 16 / 36 | 100 % | 454 ms |
| ministral-3:3b | 3,0 Go | 33 / 36 | 31 / 36 | 100 % | 250 ms |
| gemma4:e2b | 4,6 Go | 29 / 36 | 23 / 36 | 100 % | 217 ms |
| ministral-3:8b | 6,0 Go | 31 / 36 | 31 / 36 | 100 % | 264 ms |

**Ce qu'on en retient**
- **Le RAG d'exemples double la justesse de qwen3:1.7b** (de 15 à 30). Il aide les petits modèles,
  mais n'apporte rien au 8B.
- **Le JSON est valide dans 100 % des cas, même pour le modèle de 1B.** La grammaire impose le format ;
  le seul risque qui reste est le sens, et c'est lui que le banc mesure.

## Niveau 2 : répondre en citant nos fiches (22 questions)

| Rédaction | Réponses justes | Rédactions acceptées par le garde-fou | Latence p50 |
|---|---|---|---|
| sans LLM (extrait de la fiche) | 21 / 22 | — | 12 ms |
| **qwen3:1.7b** | **22 / 22** | **9 / 18** | **391 ms** |
| gemma3:1b | 21 / 22 | 1 / 18 | 355 ms |
| ministral-3:3b | 21 / 22 | 3 / 18 | 476 ms |
| gemma4:e2b | 21 / 22 | 9 / 18 | 300 ms |
| ministral-3:8b | 21 / 22 | 4 / 18 | 703 ms |

La recherche (e5-small, 37 fiches) trouve la bonne fiche parmi les 3 passages pour 18 questions sur 18,
et refuse les 4 questions hors de nos fiches.

**Ce qu'on en retient**
- **Les réponses restent justes quel que soit le modèle**, grâce au repli sûr.
- **Les gros modèles réécrivent plus librement**, donc le garde-fou de fidélité les écarte plus souvent.
  On l'avait déjà vu en reformulant les conseils : plus gros ne veut pas dire plus fidèle.

## Comment chaque mesure est faite

### « Juste », au niveau 1

Chaque message du banc (`data/processed/banc_niveau1.yaml`) a été écrit par l'équipe ; aucun ne vient
de l'entraînement ni du test français. Chacun indique son contexte (le parcours en cours, la question en
attente, les sujets déjà traités) et ce qu'on attend. Le message passe par le vrai chemin de l'assistant :
le contexte, le RAG d'exemples, le JSON imposé, puis la vérification et le rattachement par le code.

Un message est **juste** si les deux conditions sont réunies :
1. **Les bons sujets.** Le premier sujet compris mène au bon parcours, et tous les sujets attendus sont trouvés.
   - Pour une demande de service Banking77, il suffit de la bonne famille, car c'est elle qui décide de la réponse.
   - Pour nos 8 intentions, il faut la bonne intention.
2. **La bonne valeur.** Ce que l'assistant retient pour la question en attente est le bon : par exemple « père »
   pour « c'est pour mon papa ». S'il n'y a rien à retenir (« oui »), il ne doit rien retenir.

Exemple : pendant « À qui voulez-vous envoyer l'argent ? », le message « à ma frangine » est juste si le
sujet compris est le virement et la valeur retenue « sœur ».

**JSON valide** : la part des sorties qui sont du JSON conforme au schéma.

### « Avec ou sans RAG d'exemples »

- **Avec** (« exemples = oui ») : avant d'appeler le LLM, e5-small cherche les **8 phrases d'entraînement les plus
  proches** du message et les lui donne avec leur sujet (« messages proches déjà classés »).
- **Sans** (« exemples = non ») : le LLM n'a que la liste des sujets et le contexte.

Comparer les deux mesure ce que ce RAG apporte.

### « Juste », au niveau 2

Chaque question du banc (`data/processed/banc_niveau2.yaml`) indique la fiche qui doit y répondre et les faits
attendus, par exemple « 22 950 » pour le plafond du Livret A.
- **Une question couverte par nos fiches** est juste si la réponse finale, rédigée par le LLM ou donnée par le repli,
  contient les faits attendus.
- **Une question hors de nos fiches** (la météo, un match) est juste si l'assistant refuse :
  « je n'ai pas cette information ».

**Garde-fou x / 18** : sur les 18 questions couvertes par nos fiches, le nombre de rédactions du LLM acceptées. Le garde-fou
vérifie les chiffres (tous présents dans les extraits), la fidélité (les mots viennent des extraits) et la
citation [1]. Les autres sont remplacées par l'extrait de la meilleure fiche.

### p50 et temps

- **p50, la médiane** : la moitié des messages a pris moins de temps, l'autre moitié plus. On la préfère à la
  moyenne, qui serait tirée vers le haut par un premier appel lent, quand le modèle se charge.
- **p95** : 95 % des messages ont pris moins de temps.
- **Ce qui est chronométré**, pour un message, sur le GPU de DeepEirb :
  - au niveau 1, l'appel au LLM qui rend le JSON (188 ms pour qwen3:1.7b) ;
  - au niveau 2, la recherche dans les fiches et la rédaction (391 ms).

  À titre de comparaison, le même qwen3:1.7b prend environ 2,7 s sur le processeur d'un portable.
- **Les tokens** : les morceaux de mots lus et écrits par le LLM (la consigne et les exemples, plus la réponse),
  en moyenne par message.

## Limites, à dire si on nous les demande

- **Les bancs sont petits** (36 et 22 messages) et écrits par l'équipe ; une seule passe par modèle.
- **Le niveau 2 a été mis au point sur une partie de ces questions** : les titres de deux fiches et le bonus de
  recherche ont été ajustés. Les questions hors sujet n'ont servi qu'à vérifier le refus.
- **Le niveau 1 compte le résultat final, après les corrections du code** (l'ordre d'urgence, le rattachement au contexte).

## Refaire les mesures

```bash
export BANC_MACHINE="DeepEirb, RTX 6000 Ada 48 Go"
./mesurer.sh niveaux          # les deux bancs, cinq modèles
./mesurer.sh abc qwen3:1.7b   # énergie de l'aiguilleur avec le modèle retenu
```
