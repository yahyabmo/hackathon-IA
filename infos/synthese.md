# Synthèse du kick-off — 26 octobre

Sources :
- `presentation/20261026- Hackathon IA ENSEIRB x CGI x LBP OJ Kick-Off v0.1.pdf` (CGI)
- `presentation/hackathon.pdf` (Denis Barthou)
- [transcription-1-regles-et-sujets.txt](transcription-1-regles-et-sujets.txt) : CGI présente les règles, les sujets, le jury et les prix
- [transcription-2-presentation-lbp-cgi.txt](transcription-2-presentation-lbp-cgi.txt) : La Banque Postale et CGI se présentent
- [transcription-3-echange-organisateur.txt](transcription-3-echange-organisateur.txt) : échange informel avec un organisateur, lundi vers 17h30

Les transcriptions sont automatiques (Whisper) : les noms propres et certains chiffres peuvent être mal reconnus.

---

## La règle commune aux deux sujets

**Une IA frugale et open source pour le domaine bancaire.**

| Règle | Ce que ça veut dire |
|---|---|
| Open source uniquement | Licences ouvertes, **aucune API de LLM externe**, données en local |
| Le plus petit modèle qui suffit | Le GPU est partagé : une base simple d'abord, un modèle plus gros seulement si le gain est **mesuré** |
| Serveur GPU sur site | Un serveur on premise est fourni ; données et modèles restent en interne |
| Mesurer sa frugalité | Taille du modèle, énergie (**CodeCarbon**) et latence, à présenter dans le pitch |

Précisions de Denis Barthou :
- La **solution** tourne uniquement sur les machines locales. Utiliser d'autres IA **pour le développement** (coder, discuter des solutions) est autorisé.
- Dans la solution, privilégier des petits LLM, **des algorithmes au lieu de LLM quand c'est possible**, des bases de données, d'autres types d'IA (classifieurs…).
- Critère de frugalité : le plus petit LLM **en Go, quantisation comprise**.

---

## Ce qui a été dit à l'oral sur les règles et les sujets (audio 1)

Ce qui n'est pas dans les slides, ou qui les nuance :

- **Frugalité** : consommer peu de tokens, mais **surtout peu d'énergie**. Avec des modèles open source qui tournent sur nos machines, on peut calculer la consommation réelle.
- **« Le plus petit modèle qui suffit » est une phrase « à double tranchant »** : une architecture peut appeler **un gros modèle à un instant précis, pour un besoin précis**, et des petits modèles le reste du temps. Selon eux, c'est **là que se joue l'innovation**.
- **Les deux sujets n'ont pas la même nature** :
  - Sujet 1 = **IA générative qu'on orchestre**. C'est « du chatbot, mais pas du chatbot traditionnel : un chatbot avancé ».
  - Sujet 2 = **analyse de données et de graphes**, recherche de « signaux faibles ».
- **Sujet 1, précisions** :
  - Ils veulent **notre regard de jeunes clients** : quel niveau de service et de réponse on attend de sa banque (exemple cité : « je veux faire un prêt étudiant, comment je fais ? »).
  - Les jeux de données sont **indicatifs** ; on est libres d'en croiser d'autres.
  - Le catalogue est à construire (Livret A, LDDS…), avec notre propre stratégie.
  - **La profondeur est à nous de choisir** : un agent qui va au bout du workflow et **fait l'action lui-même** (faire opposition sur la carte selon la gravité), ou un assistant qui guide seulement.
  - **Expliquer le jargon bancaire et les sigles** en mots simples fait partie des attentes.
  - Les attentes seront précisées avec chaque équipe au fil des jours.
- **Sujet 2, précisions** :
  - Entraîner un modèle et afficher un score ne suffit pas.
  - Une chaîne va **injecter des transactions en temps réel, avec des schémas aléatoires**, et ils vérifieront qu'on les détecte.
  - **Plus on détecte vite**, plus on peut bloquer la transaction avant que l'argent ne se propage.
- **Temps réel dans les deux cas** : le chatbot doit répondre immédiatement ; la détection doit être dynamique.
- **Choix du sujet** : l'un ou l'autre, celui avec lequel on est le plus à l'aise. **« Si vous voulez les deux, encore mieux. »** Les sujets « paraissent simples, mais l'idée c'est d'aller le plus loin possible ».
- **Le code source est à déposer sur un dépôt Git.**
- **Prix pour l'équipe gagnante** :
  - Une journée à l'**InnovTech de CGI** (13ᵉ édition, **mercredi 25 novembre à Paris**), avec **un pitch de 30 minutes pendant la keynote** devant la communauté technique de CGI.
  - Un **échange privilégié à Bordeaux** avec le responsable du développement de l'IA chez CGI France (nom mal compris à l'enregistrement).

---

## Qui sont les partenaires (audio 2)

### La Banque Postale

Présentée par Valérie, directrice SI, en charge des projets d'IA générative et de data.

- **Une des grandes banques françaises.** Elle compte **17 000 points de contact** (les bureaux de poste, y compris en outre-mer), et **environ un Français sur quatre** en est client : compte courant, Livret A, épargne financière, crédit à la consommation, crédit immobilier.
- **Elle a investi un milliard d'euros dans la transformation numérique depuis 2020**, dans l'IA traditionnelle et l'IA générative.
- **Ses valeurs, sur lesquelles elle a insisté** :
  - **Accessibilité** : clients et collaborateurs en situation de handicap (malentendants, malvoyants). Tout ce que construit la DSI doit être compatible avec le handicap.
  - **Inclusion bancaire** : la banque a le devoir d'accueillir **tous** les clients, y compris les plus fragiles financièrement.
  - **Entreprise responsable** : financements verts, finance durable, « banque citoyenne ».
- **Annonce pour novembre** : un outil d'IA générative dans les bureaux de poste, qui permettra à un conseiller francophone de dialoguer avec des clients qui parlent arabe, espagnol, etc.
- **La DSI** compte environ 1 600 personnes sur 4 sites (Paris, Nantes, Toulouse, **Bordeaux**), plus environ 3 000 personnes chez des partenaires comme CGI.

**Les priorités IA de La Banque Postale**, dans l'ordre où elles ont été présentées :

1. **L'expérience client.** Elle passe par **un chatbot conversationnel** pour échanger sur ses contrats ou **une réclamation** (« un sujet prégnant »), et par **l'analyse prédictive et la personnalisation des offres** : regarder les avoirs d'un client pour lui proposer les produits adaptés. **C'est le sujet 1.**
2. **L'optimisation des processus**, par exemple accélérer l'analyse d'un dossier de crédit (ressources, risques), et **la détection des risques en lutte anti-blanchiment et anti-fraude** : « on y travaille énormément ». **C'est le sujet 2.**
3. **L'innovation** : outils d'IA générative pour les tâches administratives des collaborateurs (comptes rendus de réunion), et un incubateur de start-up.

Qualités qu'ils recherchent : la créativité, l'expertise technique, et le fait de rester à jour sur une technologie qui évolue en semaines.

### CGI

- **L'un des leaders mondiaux du conseil et des services numériques.** L'entreprise a été fondée en 1976 (50 ans cette année), son siège est à Montréal. Elle compte environ 95 000 collaborateurs dans 400 bureaux et 40 pays, dont **15 000 en France** sur une trentaine de sites.
- **Son modèle est la proximité** : être là où sont les clients, et bien connaître leur métier.
- **Quatre métiers** : conseil (stratégie, IT), intégration de systèmes, services managés, et solutions propriétaires réutilisables.
- **La Banque Postale fait partie de ses 10 premiers clients en France.**
- **Les enjeux sur lesquels elle accompagne ses clients** : efficacité opérationnelle, expérience client, expérience collaborateur, **gestion du risque** (réglementation, cyber, **souveraineté**), et **RSE** (accessibilité, empreinte carbone).
- C'est la première ESN en France certifiée ISO 14001 (management environnemental).

---

## Conseils d'un organisateur (audio 3)

Échange informel avec un organisateur du hackathon, lundi vers 17h30. Whisper a mal transcrit plusieurs termes : « l'élève » ou « NLM » veulent dire **LLM**, « RAC » ou « ragas » veulent dire **RAG**, « GMA4 » veut dire **Gemma 4**.

- **« Pour gagner, c'est moins de LLM, plus d'algo »**, ou des algorithmes différents, ou des modèles d'IA plus spécialisés. Ça vaut aussi pour le sujet 1.
- **En entrée, pas besoin de LLM** pour savoir de quoi parle la personne : un algorithme qui trouve la catégorie du sujet est plus rapide. Le RAG est une autre façon de le trouver.
- **Les mots-clés, presque gratuits, règlent une partie des cas.** Une simple recherche de mots-clés peut trouver le sujet dans environ 30 % des cas : « ça fait 30 % de gagné ». Elle peut aussi donner **un degré de confiance** : « j'ai trouvé un seul mot-clé dans une longue phrase, je ne suis pas sûr ». Les cas restants passent à un outil plus lourd.
- **En sortie, un LLM** : pour le sujet 1, il faut parler français à un humain. Mais il faut **minimiser les appels** et l'appeler **une seule fois, à la fin**.
- **Choisir la taille en descendant** : commencer avec un modèle qui parle correctement (un 15B ou un 30B), puis descendre. Un 2B ou un 4B devrait marcher, « même le Gemma 4 que vous avez ». Essayer ensuite un 2B ou un 1B pour voir.
- **À chaque endroit, se demander si un LLM est vraiment nécessaire** : jamais, ou seulement pour une partie des cas. Ne traiter que 30 % des cas avec un LLM, c'est déjà intéressant. Son image : prendre le vélo pour aller chercher le pain, et garder la voiture pour le week-end.
- **Un seul sujet** : il n'y aura pas le temps de bien faire les deux.
- **D'abord une solution sûre, ensuite les idées.** Une fois qu'une solution tient, essayer des idées nouvelles, même « un peu crazy » ou exotiques, et vérifier si elles s'appliquent aux données.
- **Utiliser l'IA pour développer**, franchement : génération de code, discussion d'idées, recherche de méthodes (par exemple pour trouver la catégorie d'un sujet).
- **Se faire plaisir** : c'est le but du hackathon. Découvrir, défricher, essayer des méthodes qu'on ne connaît pas.

---

## Sujet 1 — Assistant bancaire personnalisé

> « Un client écrit : *Je veux acheter un appartement.* Votre assistant doit comprendre, poser les bonnes questions et lui proposer une piste adaptée à sa situation. »

**Objectifs**
1. **Comprendre** les questions des clients en langage naturel
2. **Personnaliser** selon l'âge, les revenus et l'historique
3. **Conseiller** : recommander un produit bancaire simple

**Démarche attendue** : Cadrer (quels besoins et intentions prioriser ?) → Préparer (rendre les données exploitables en français) → Concevoir (quelle architecture, pourquoi la plus sobre ?) → Démontrer (prouver la valeur et la frugalité).

**Livrables attendus**
- Données préparées en français
- Modèle de compréhension des intentions
- Chatbot relié à une base clients simulée
- Moteur de conseils personnalisés
- Mesures de frugalité

**Données fournies**
- **Banking77** : questions clients étiquetées en 77 intentions. Le jeu de données est **en anglais**, d'où le livrable « données préparées en français ».
- **Bank Marketing**, enrichi de revenus et d'historique simulés : la base clients.
- **Catalogue de produits** : à construire nous-mêmes à partir d'informations publiques.

**Six situations clients données en exemple**

| Thème | Message | Profil | Attendu |
|---|---|---|---|
| Carte | « J'ai perdu ma carte hier soir, je fais quoi ? » | Inès, 34 ans, cadre | Réagir vite, guider l'opposition, rassurer |
| Réclamation | « Pourquoi j'ai payé 8 € de frais ce mois-ci ? » | Marc, 52 ans, découverts fréquents | Expliquer les frais, orienter si besoin |
| Épargne | « Je voudrais mettre de côté pour mes enfants. » | Sophie, 41 ans, deux enfants | Demander l'horizon, proposer une piste |
| Virement | « Je dois envoyer 500 € à mon fils. » | Paul, 68 ans, peu à l'aise en ligne | Guider pas à pas, mots simples |
| Crédit | « Je veux un crédit pour acheter une voiture. » | Karim, 29 ans, 1 900 € de revenus | Questionner, rester prudent sur l'endettement |
| Insatisfaction | « Votre appli ne marche jamais ! » | Client mécontent, 3ᵉ message du jour | Reconnaître la frustration, passer la main |

---

## Sujet 2 — Lutte contre le blanchiment d'argent

> « Des millions de virements, quelques milliers suspects. Votre outil doit les repérer à temps, expliquer pourquoi et préparer le dossier de l'analyste. »

**Objectifs**
1. **Analyser** le réseau de transactions et ses motifs suspects
2. **Alerter** en temps réel sur les transactions à risque
3. **Déclarer** : rédiger automatiquement les rapports réglementaires

**Démarche attendue** : Cadrer (quels schémas cibler en priorité ?) → Explorer (que révèlent les données et le graphe ?) → Concevoir (quelle détection, pourquoi la plus sobre ?) → Démontrer (prouver la pertinence des alertes).

**Livrables attendus**
- Graphe des transactions visualisé
- Modèle de détection des motifs suspects
- Alertes en temps réel
- Rapports générés automatiquement
- Interface de suivi des alertes
- Mesures de frugalité

**Données fournies**
- **IBM AML HI-Small** : environ 5 millions de transactions synthétiques, avec les transactions de blanchiment étiquetées.
- Un **script de rejeu en flux**, pour simuler le temps réel.
- Un **modèle de rapport** inspiré de la déclaration de soupçon **TRACFIN**.

**Six schémas suspects donnés en exemple**

| Schéma | Exemple | Pourquoi suspect |
|---|---|---|
| Fractionnement | 9 dépôts de 1 400 € en espèces en une semaine | Montants juste sous les seuils |
| Rassemblement | 25 comptes virent 300 € vers un seul, vidé le lendemain | Nombreuses sources, une seule cible |
| Dispersion | 50 000 € reçus, répartis en 48 h sur 20 comptes | Somme éclatée pour brouiller la piste |
| Circuit fermé | A → B → C → D → A en trois jours | L'argent tourne sans raison |
| Compte réveillé | Inactif deux ans, puis 40 virements en un mois | Changement brutal de comportement |
| Chaîne rapide | Les fonds traversent 5 comptes en moins de 24 h | Cascade pour masquer l'origine |

---

## Soutenance (mercredi 28, à partir de 13h30)

**30 minutes par équipe** (20 minutes s'il y a plus de 7 groupes), devant un jury de trois personnes : ENSEIRB, CGI et La Banque Postale. Le jury évalue **la démarche autant que le résultat**.

| Temps | Contenu |
|---|---|
| 0 – 15 min | Présentation : le problème, la démarche, **la démo en direct**, le bilan |
| 15 – 25 min | Questions / réponses |
| 25 – 30 min | Débrief du jury à chaud |

**La démo se fait en direct, sur le serveur fourni**, et non sur un ordinateur perso. À l'oral, ils ont dit « sur vos postes » : dans les deux cas, ce sont les machines de l'école.

À l'oral, ils ont parlé d'environ 5 minutes de questions ; la slide en indique 10.

**Grille du jury**

| Poids | Critère | Ce qui est regardé |
|---|---|---|
| 25 % | Pertinence métier | Utile pour un client ou un analyste |
| 20 % | Qualité technique | Résultats mesurés et bien évalués |
| 20 % | Frugalité | Taille, énergie, latence |
| 15 % | Explicabilité | Chaque conseil ou alerte se justifie |
| 10 % | Démonstration | Elle fonctionne et se comprend |
| 10 % | Présentation | Claire et tenue en 15 minutes |

**À remettre avant la soutenance** : le code source déposé et le support de présentation.

---

## Agenda

| Jour | Matin | Après-midi |
|---|---|---|
| **Lun. 26** | Logistique, configuration des postes, constitution des équipes | 13h30 accueil des partenaires · 14h kick-off, cas d'usage, Q&R · 15h30–18h brainstorming, ébauche de solution |
| **Mar. 27** | Delivery de la solution | Delivery de la solution |
| **Mer. 28** | Finalisation et préparation de la soutenance | 13h15 accueil du jury · 13h30–16h30 soutenances · 16h30 délibération · 17h remise des prix · 17h30 cocktail |

**Accompagnement** : Corentin (organisateur), Damien (coach IA, ancien de l'école, présent les deux matinées), Adrien (coach IA **et membre du jury**).

**Jury** : Adrien (CGI), Denis Barthou (ENSEIRB) et Jean-Michel (La Banque Postale, à distance). Jean-Michel connaît les sujets et **les équipes peuvent lui poser des questions**.

---

## Ressources matérielles

| Machine | Caractéristiques | Usage | Disponibilité |
|---|---|---|---|
| **DeepEirb** | 2 × A6000 48 Go, Xeon 56 cœurs, 32 Go RAM | SSH ; serveur d'inférence (vLLM) pour tous les groupes : **dire à Denis Barthou quels modèles on veut** | Lundi |
| **Machines de la salle** | RTX 3060 12 Go, 30 Go RAM | **Machine principale de développement** ; pip + venv + git | Lundi |
| **Jetson AGX Orin** (× 2) | 32 Go, 12 cœurs ARM, 15–40 W | Déploiement, test | Mardi |
| **OrangePi 6+** | 12 cœurs ARM + NPU, 15–35 W | Déploiement uniquement | Mardi |
| **OrangePi Zero 4** | 4 Go RAM, NPU, 3–7 W ; Qwen 0.5B et 1.5B disponibles | Déploiement uniquement | Mardi |

Les identifiants des machines de la salle sont sur la slide 2 de `presentation/hackathon.pdf` ; on ne les recopie pas dans le dépôt.

- **Fine-tuning et RAG** : à faire sur DeepEirb ou sur les stations de la salle.
- **Parallélisme sur plusieurs GPU** : pas adapté (réseau lent), sauf sur DeepEirb.
- **Télécharger les modèles** via Ollama ou Hugging Face, **pas en wifi** : attention à la taille.

## Logiciels conseillés

| Catégorie | Outils |
|---|---|
| Données | DuckDB (SQL local, CSV, Parquet), Pandas, PyArrow, NumPy |
| ML tabulaire | LightGBM |
| Graphes | igraph, leidenalg (communautés), NetworkX |
| ML / LLM | PyTorch, Transformers ; llama.cpp, Ollama (salle) et vLLM (DeepEirb) déjà installés |
| Services | FastAPI, FastMCP |
| Mesure | CodeCarbon (sur GPU Nvidia), Matplotlib |

## Ollama sur les machines de la salle

```bash
export PATH=/opt/ollama/bin:${PATH}
export OLLAMA_MODELS=/opt/ollama/models
export OLLAMA_CONTEXT_LENGTH=16384
ollama serve                 # terminal 1 : un seul serveur par machine
ollama list                  # terminal 2
ollama run ministral-3:14b
```

| Modèle installé | Taille |
|---|---|
| `gemma4:e2b` | 7,2 Go |
| `ministral-3:14b` | 9,1 Go |

Rappels du cours : 1 paramètre ≈ 2 octets en 16 bits ; la quantisation en 8 ou 4 bits divise la taille par 2 ou 4 mais dégrade les réponses. Chaque token de contexte coûte de la mémoire, donc on règle la taille du contexte au plus juste.

---

## Ce que ça implique pour nous

**Valable quel que soit le sujet**
- **Frugalité et explicabilité pèsent 35 % de la note.** Le LLM ne doit faire que ce qu'un algorithme ou un classifieur ne sait pas faire (formuler une réponse, rédiger un rapport), avec le plus petit modèle qui suffit.
- **Mesurer dès le premier jour** : taille du modèle en Go, énergie CodeCarbon, latence. Le jury veut des chiffres, et une comparaison « petit modèle vs gros modèle » montre la démarche.
- **La démo finale tourne sur le serveur fourni.** Tester tôt sur les machines de l'école, pas seulement sur nos ordinateurs perso.
- **Le jury note la démarche** : garder une trace des choix et des mesures au fil de l'eau, pour le support de présentation.
- **Parler le langage des valeurs de La Banque Postale** pour la pertinence métier (25 %) : accessibilité, inclusion des clients fragiles, souveraineté (tout tourne en local). La frugalité s'inscrit aussi dans leur engagement RSE et dans celui de CGI.
- **Un organisateur a confirmé l'architecture en cascade** : mots-clés puis classifieur en entrée, un seul appel au LLM à la fin, taille du LLM choisie en descendant depuis un modèle qui marche.
- **Les deux sujets correspondent à de vraies priorités de La Banque Postale** : le sujet 1 à sa priorité n°1 (chatbot, réclamations, offres personnalisées), le sujet 2 à sa priorité n°2 (anti-blanchiment et anti-fraude).

**Comparaison rapide des deux sujets**

| | Sujet 1 — Assistant | Sujet 2 — Anti-blanchiment |
|---|---|---|
| Point fort | Démo très parlante ; six scénarios déjà fournis | Frugalité et explicabilité naturelles : algorithmes de graphe, LightGBM, LLM seulement pour le rapport |
| Évaluation | Intentions mesurables sur Banking77 ; la qualité du conseil est plus difficile à chiffrer | Données étiquetées, donc précision et rappel faciles à mesurer |
| Difficulté | Traduire les données en français, construire le catalogue produits à la main | 5 M de transactions à traiter, temps réel, six livrables |
| Rôle du LLM | Central (dialogue), donc frugalité plus dure à défendre | Marginal (rapport TRACFIN), donc facile à garder petit |

## Questions à poser aux organisateurs

- Quels modèles demander sur le serveur vLLM de DeepEirb, et avant quand ?
- Comment accéder à DeepEirb depuis un ordinateur perso (SSH direct, VPN) ?
- Où récupérer les données, le script de rejeu et le modèle de rapport TRACFIN ?
- Sur quel dépôt Git déposer le code source, et pour quand ?
- La démo se fait-elle sur DeepEirb ou sur un poste de la salle ?
- Comment poser nos questions à Jean-Michel (La Banque Postale) ?
- Combien de groupes, donc soutenance de 30 ou de 20 minutes ?
