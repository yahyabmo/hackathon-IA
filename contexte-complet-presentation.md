# Assistant bancaire frugal : tout le contexte, pour préparer la présentation

> **À qui sert ce document.** Il rassemble tout ce qu'il faut savoir sur notre projet du hackathon
> La Banque Postale × CGI × ENSEIRB-MATMECA : le sujet, les règles, ce que nous avons construit et
> pourquoi, les chiffres mesurés, ce qui marche et ce qui ne marche pas, la démo, le support, et les
> questions probables du jury. Il est écrit pour être donné tel quel à un assistant (ou lu par une
> personne) qui doit préparer et tenir la soutenance sans avoir suivi le projet.
>
> **Les chiffres viennent de nos fichiers de mesure** (`eval/resultats/`, `infos/choix-modeles-niveaux.md`)
> et du code. Quand une valeur est une estimation, c'est dit. Rien n'est arrondi à notre avantage.
>
> **Dernière mise à jour** : mercredi 28 octobre 2026, vers 12 h 30. Soutenance à **13 h 30**.

---

## Sommaire

1. [Le projet en une page](#1-le-projet-en-une-page)
2. [Le hackathon : organisateurs, règles, jury, calendrier](#2-le-hackathon--organisateurs-règles-jury-calendrier)
3. [Le sujet 1 en détail](#3-le-sujet-1-en-détail)
4. [L'équipe et la répartition](#4-léquipe-et-la-répartition)
5. [L'histoire du projet et les décisions clés](#5-lhistoire-du-projet-et-les-décisions-clés)
6. [L'architecture finale : l'aiguilleur et ses trois niveaux](#6-larchitecture-finale--laiguilleur-et-ses-trois-niveaux)
7. [Les données](#7-les-données)
8. [Technologies et modèles](#8-technologies-et-modèles)
9. [Évaluation et résultats chiffrés](#9-évaluation-et-résultats-chiffrés)
10. [Explicabilité](#10-explicabilité)
11. [Confiance, conformité, inclusion](#11-confiance-conformité-inclusion)
12. [Limites, en toute honnêteté](#12-limites-en-toute-honnêteté)
13. [L'interface de démonstration](#13-linterface-de-démonstration)
14. [La démo en direct : les trois scénarios](#14-la-démo-en-direct--les-trois-scénarios)
15. [Le support de présentation, diapositive par diapositive](#15-le-support-de-présentation-diapositive-par-diapositive)
16. [Proposition de déroulé des 15 minutes](#16-proposition-de-déroulé-des-15-minutes)
17. [Questions probables du jury, et réponses](#17-questions-probables-du-jury-et-réponses)
18. [Aide-mémoire : les chiffres à retenir](#18-aide-mémoire--les-chiffres-à-retenir)
19. [Glossaire du projet](#19-glossaire-du-projet)
20. [Fichiers et commandes utiles](#20-fichiers-et-commandes-utiles)

---

## 1. Le projet en une page

**Le titre de la soutenance** : *Un assistant bancaire frugal, explicable et prudent* — sous-titre :
*Un aiguilleur : à chaque message, le plus petit moyen qui suffit.*

**Le problème.** Un client écrit à sa banque : « Je veux acheter un appartement », « J'ai perdu ma
carte hier soir, je fais quoi ? », « Pourquoi j'ai payé 8 € de frais ce mois-ci ? ». L'assistant doit
comprendre, poser les bonnes questions, tenir compte de la situation du client (âge, revenus,
historique) et proposer une piste adaptée. Contrainte du hackathon : **open source, local, le plus
petit modèle qui suffit, frugalité mesurée** (taille, énergie avec CodeCarbon, latence).

**Notre réponse : un aiguilleur.** À chaque message, un aiguilleur (du code, sans LLM) choisit le
plus petit moyen qui suffit :

| Niveau | Quand | Comment | Coût |
|---|---|---|---|
| **0 — règles** | La demande est claire | Mots-clés ou classifieur e5-small, parcours de conversation en YAML, règles métier publiques (HCSF, plafonds), gabarits de réponse | **aucun LLM**, ~ms |
| **1 — comprendre** | Message flou, réponse libre, renvoi au contexte | Un **petit LLM** (qwen3:1.7b) lit le message avec un **RAG d'exemples** et rend un **JSON imposé par une grammaire**, vérifié par le code. Il ne répond jamais au client : le niveau 0 reprend la main | 1 appel |
| **2 — répondre** | Question ouverte sur un produit ou une règle | **RAG sur 37 fiches sourcées** ; le LLM rédige en citant [1] ; un **garde-fou** vérifie chiffres et fidélité, sinon on donne l'extrait de la fiche | 1 appel |

La décision est prise **à chaque message** : une même conversation passe du niveau 1 au 2, puis au 0,
puis au 2. La **mémoire est commune** aux trois niveaux (parcours en cours, demandes en attente,
informations déjà données), et après une parenthèse on reprend où on en était.

**L'image à retenir** (donnée par un organisateur) : *« le vélo pour aller chercher le pain, la
voiture pour le week-end »*.

**Les chiffres clés** (mesurés sur le serveur DeepEirb de l'école, 2 × RTX 6000 Ada 48 Go) :

- **76 % des messages n'appellent aucun LLM** (niveau 0) ; 12 % passent au niveau 1, 12 % au niveau 2.
- **17 fois moins d'énergie** qu'un LLM de 14 milliards de paramètres qui répond à tout
  (11,5 contre 194 Wh pour 1 000 messages, consommation au repos comprise ; 5,5 contre 115 Wh au repos soustrait).
- **5 fois moins de mémoire** (1,9 Go contre 9,1 Go), **latence p95 de 0,5 s** au lieu de 2,3 s.
- **Un seul petit modèle de 1,4 Go** (`qwen3:1.7b`), choisi en descendant en taille sur deux bancs.
- **Compréhension** : 92,3 % sur le test anglais de Banking77 (la référence BERT affiné de l'article
  fait 93,7 %), 84,8 % de bon routage sur 250 phrases françaises écrites par l'équipe, **sans avoir
  traduit Banking77**.
- **15 scénarios de bout en bout sur 15** réussis ; **152 tests automatisés** au vert.
- Chaque réponse affiche son niveau, sa raison, ses sources, sa latence, son énergie et son CO₂ estimé
  (≈ 10 µg de CO₂e sans LLM, ≈ 1,3 mg avec un appel au LLM).

**Le périmètre** : l'assistant n'a **aucun accès au compte** et ne fait aucune opération (c'est le
périmètre donné au kick-off). Il explique, conseille, oriente vers l'espace bancaire sécurisé ou un
conseiller. Il ne fait **pas** de notation de solvabilité : un conseiller décide.

---

## 2. Le hackathon : organisateurs, règles, jury, calendrier

### Les organisateurs

- **La Banque Postale (LBP)** : environ **un Français sur quatre** est client ; **17 000 points de
  contact** (bureaux de poste, outre-mer compris) ; un milliard d'euros investis dans le numérique
  depuis 2020. Valeurs mises en avant au kick-off : **accessibilité** (handicap), **inclusion bancaire**
  (clients fragiles), **entreprise responsable** (finance durable). Ses **priorités IA**, dans l'ordre :
  1. **l'expérience client** — chatbot conversationnel (contrats, **réclamations**), analyse
     prédictive et personnalisation des offres : **c'est notre sujet** ;
  2. l'optimisation des processus et la lutte anti-blanchiment / anti-fraude (sujet 2) ;
  3. l'innovation (outils internes).
  Annonce faite au kick-off : en novembre, un outil d'IA générative dans les bureaux de poste pour
  dialoguer avec des clients qui parlent arabe, espagnol, etc.
- **CGI** : ESN mondiale (environ 95 000 personnes, 15 000 en France), LBP est l'un de ses 10 premiers
  clients en France ; enjeux portés : expérience client, gestion du risque (réglementation, cyber,
  **souveraineté**), **RSE** (accessibilité, empreinte carbone) ; première ESN française certifiée
  ISO 14001.
- **ENSEIRB-MATMECA** : l'école hôte (Bordeaux) ; Denis Barthou fournit les machines.

### La règle commune

**Une IA frugale et open source pour le domaine bancaire.**

- Open source uniquement, **aucune API de LLM externe** dans la solution, données en local.
- **Le plus petit modèle qui suffit** ; un modèle plus gros seulement si le gain est **mesuré**.
  Critère de taille : **en Go, quantisation comprise**.
- La solution tourne sur les machines de l'école. Utiliser d'autres IA **pour développer** est autorisé.
- **Mesurer sa frugalité** : taille du modèle, énergie (**CodeCarbon**), latence.
- Conseils donnés à l'oral : « **pour gagner, c'est moins de LLM, plus d'algo** » ; en entrée, un
  algorithme de catégorisation suffit, des **mots-clés règlent environ 30 % des cas** ; en sortie, un
  LLM pour parler français, le moins d'appels possible ; **choisir la taille en descendant** ; « une
  architecture peut appeler un gros modèle à un instant précis, pour un besoin précis, et des petits
  modèles le reste du temps : **c'est là que se joue l'innovation** ».

### La soutenance

- **Mercredi 28 octobre, à partir de 13 h 30.** Créneau de 30 minutes : **15 min de présentation
  avec la démo en direct**, puis questions (environ 10 min), puis débrief du jury (5 min).
- **La démo se fait en direct sur les machines de l'école.**
- **À rendre avant** : le code (dépôt Git) et le support de présentation.
- **Jury** : Adrien (CGI, aussi coach IA), Denis Barthou (ENSEIRB), Jean-Michel (La Banque Postale,
  à distance). Le jury évalue **la démarche autant que le résultat**.
- **Prix** : une journée à l'InnovTech de CGI à Paris (25 novembre) avec un pitch de 30 minutes, et
  un échange avec le responsable du développement de l'IA chez CGI France.

### La grille du jury

| Poids | Critère | Ce qui est regardé | Ce que nous mettons en avant |
|---|---|---|---|
| **25 %** | Pertinence métier | Utile pour un client | Les 6 situations du sujet traitées ; aucun accès au compte mais un vrai guidage ; mots simples, clients fragiles, réclamations |
| **20 %** | Qualité technique | Résultats mesurés et bien évalués | Bancs dédiés (compréhension, niveau 1, niveau 2, A/B/C), tests, scénarios, conversations libres |
| **20 %** | Frugalité | Taille, énergie, latence | 76 % sans LLM, 17× moins d'énergie que le 14B, modèle de 1,4 Go, CO₂ par réponse |
| **15 %** | Explicabilité | Chaque conseil se justifie | Pourquoi et pourquoi pas, règles nommées, sources datées, « pourquoi ? » expliqué au niveau 2 |
| **10 %** | Démonstration | Elle fonctionne et se comprend | Interface avec niveaux visibles, barre de scénario, vue utilisateur |
| **10 %** | Présentation | Claire, tenue en 15 min | Support Beamer, schémas |

### Les machines

| Machine | Caractéristiques | Usage pour nous |
|---|---|---|
| **DeepEirb** | 2 × RTX 6000 Ada 48 Go (serveur de l'école) | **Toutes les mesures officielles** (bancs, énergie) |
| **Machines de la salle** (dont `ail`) | RTX 3060 12 Go, Ollama | **La démo en direct** et les tests en conditions réelles |
| Portables de l'équipe | CPU | Développement ; le LLM y est lent (~3 s par appel) |

### Le calendrier

| Jour | Ce qui s'est passé |
|---|---|
| **Lundi 26** | Kick-off à 14 h, choix du sujet 1, proposition de solution (architecture en cascade), socle du code le soir |
| **Mardi 27** | Le cœur du travail : classifieur, conseiller (M3), bancs, mesures sur DeepEirb, puis **l'aiguilleur** (fin d'après-midi), interface |
| **Mercredi 28** | Tests en conditions réelles sur `ail`, corrections, 60 conversations libres jugées, interface finale, barre de scénario. Rendu à 11 h 30, soutenance à 13 h 30 |

---

## 3. Le sujet 1 en détail

> « Un client écrit : *Je veux acheter un appartement.* Votre assistant doit comprendre, poser les
> bonnes questions et lui proposer une piste adaptée à sa situation. »

**Objectifs** : comprendre les questions en langage naturel ; personnaliser selon l'âge, les revenus et
l'historique ; conseiller un produit bancaire simple.

**Démarche attendue** : Cadrer → Préparer (données exploitables en français) → Concevoir (pourquoi la
plus sobre ?) → Démontrer (prouver la valeur et la frugalité).

**Livrables attendus** et où ils sont chez nous :

| Livrable | Chez nous |
|---|---|
| Données préparées en français | 672 phrases françaises écrites par l'équipe pour nos 8 intentions et les familles Banking77, un test français de 250 phrases, 37 fiches et un glossaire en français. **Banking77 n'est pas traduit** : l'encodeur multilingue transfère de l'anglais au français |
| Modèle de compréhension des intentions | Mots-clés + classifieur e5-small et régressions logistiques, seuil de confiance τ = 0,76 ; petit LLM au niveau 1 pour les cas flous |
| Chatbot relié à une base clients simulée | 8 profils fictifs C01–C08 (`data/processed/clients.json`), ancrés documentairement sur Bank Marketing |
| Moteur de conseils personnalisés | Règles métier publiques et explicables (M3), catalogue de 12 produits sourcés |
| Mesures de frugalité | Banc A/B/C avec CodeCarbon, latence par étape, taille des modèles, CO₂ par réponse |

**Données fournies** : **Banking77** (questions clients en anglais, 77 intentions de *service* :
carte, frais, virements…), **Bank Marketing** (base clients enrichie de revenus et d'historique
simulés), catalogue de produits **à construire nous-mêmes** à partir d'informations publiques.

**Les six situations données en exemple, et ce que fait notre assistant** :

| Thème | Message | Profil | Attendu | Notre assistant |
|---|---|---|---|---|
| Carte | « J'ai perdu ma carte hier soir, je fais quoi ? » | **Inès**, 34 ans, cadre (C01) | Réagir vite, guider l'opposition, rassurer | Traité **en premier** même au milieu d'autre chose ; explique où faire opposition ; rappel « la banque ne demande jamais votre code » |
| Réclamation | « Pourquoi j'ai payé 8 € de frais ce mois-ci ? » | **Marc**, 52 ans, découverts fréquents (C02) | Expliquer, orienter | Cause la plus fréquente (commission d'intervention), plafond légal (8 €/opération, 80 €/mois ; 4 € et 20 € pour la clientèle fragile), offre clientèle fragile, à qui contester |
| Épargne | « Je voudrais mettre de côté pour mes enfants. » | **Sophie**, 41 ans, deux enfants (C03) | Demander l'horizon, proposer une piste | Demande l'horizon et l'effort mensuel, propose Livret A / Livret Jeune au nom des enfants, explique les produits écartés |
| Virement | « Je dois envoyer 500 € à mon fils. » | **Paul**, 68 ans, peu à l'aise en ligne (C04) | Guider pas à pas, mots simples | Mots simples **automatiquement** (dès 70 ans ou « peu à l'aise »), guidage vers l'espace sécurisé, contrôle de vraisemblance du montant |
| Crédit | « Je veux un crédit pour acheter une voiture. » | **Karim**, 29 ans, 1 900 € de revenus (C05) | Questionner, rester prudent | Demande montant et durée, calcule la mensualité et le taux d'effort, mention légale crédit, « pourquoi ? » expliqué |
| Insatisfaction | « Votre appli ne marche jamais ! » | **Julie**, 37 ans, 3ᵉ message du jour (C06) | Reconnaître la frustration, passer la main | Reconnaît la frustration, oriente vers le conseiller, le service réclamations puis le médiateur |

Deux profils ajoutés par l'équipe : **Léa**, 31 ans, cadre, 2 900 € nets, 25 000 € d'épargne (C07,
projet immobilier) ; **Lucas**, 20 ans, étudiant, 450 € de revenus (C08, prêt étudiant, épargne jeune).

À l'oral, les organisateurs ont précisé : ils veulent **notre regard de jeunes clients** (« je veux
faire un prêt étudiant, comment je fais ? ») ; **expliquer le jargon bancaire** fait partie des
attentes ; **la profondeur est à nous de choisir** (agir ou seulement guider).

---

## 4. L'équipe et la répartition

| Membre | Spécialité | Module | Ce qu'il a fait |
|---|---|---|---|
| **Yahya** | IA | **M2 — Aiguilleur, converser, formuler, interface** | L'architecture de l'aiguilleur, les niveaux 1 et 2 (LLM interprète, RAG, garde-fou), l'automate de dialogue et les parcours, la formulation, l'interface web, les bancs des niveaux et des conversations, le support |
| **Sohayb** | Génie logiciel | **M3 — Conseiller** | Les profils clients, le catalogue sourcé (12 produits), les règles métier (HCSF, plafonds, frais), les simulations, les scénarios de référence et les tests ; la décision « aucune action bancaire » |
| **Younes** | Calcul intensif | **M1 — Comprendre et mesurer** | Les mots-clés, l'extraction des montants et durées, le classifieur, les bancs de compréhension et d'énergie |

Dans le support, les diapositives sont attribuées : **Yahya** (problème, démarche, architecture,
niveaux, démo, choix des modèles), **Younes** (résultats compréhension et frugalité, limites),
**Sohayb** (explicabilité, confiance et conformité, commente la démo).

---

## 5. L'histoire du projet et les décisions clés

Le jury note **la démarche**. Voici comment le projet a évolué, et pourquoi chaque choix a été fait.

### Lundi : une cascade sans LLM au centre

Proposition initiale (rapport `rapport/main-resume.pdf`) : une **cascade** en cinq étages —
Comprendre, Converser, Conseiller, Agir, Formuler — où **chaque étage ne passe la main que s'il ne sait
pas faire**. Le LLM n'intervenait qu'à la fin, pour reformuler, et en escalade quand le classifieur
doutait (un 14B pour classer).

Choix fondateurs, gardés jusqu'au bout :
- **Ne pas traduire Banking77** : un encodeur multilingue (multilingual-e5-small) donne des vecteurs
  proches à une phrase anglaise et à sa traduction ; on entraîne sur l'anglais, on comprend le français.
- **Créer 8 intentions** que Banking77 n'a pas : Banking77 couvre le **service** (carte, frais,
  virement), pas le **conseil** (épargne, crédit, logement). Nos 8 : `epargne_projet`,
  `credit_immobilier`, `credit_conso`, `pret_etudiant`, `faire_virement`, `question_definition`,
  `insatisfaction`, `hors_sujet`.
- **Exclure la colonne `duration` de Bank Marketing** : elle n'est connue qu'après l'appel (fuite de
  données) ; de toute façon, Bank Marketing ne sert pas de moteur de recommandation chez nous.
- **Les décisions de conseil viennent de règles publiques**, pas d'un modèle : elles sont explicables
  et vérifiables à la main.

### Mardi matin : les briques et les mesures

- Classifieur e5-small + régressions logistiques entraîné **sans traduction** (10 003 phrases
  Banking77 anglaises + 672 phrases de l'équipe), seuil τ fixé pour viser 97 % de précision sur les
  messages acceptés.
- Le conseiller (M3) : catalogue sourcé et daté, règles HCSF, calculs de mensualité, hypothèses
  affichées.
- Bancs : compréhension (anglais et français), formulation (choisir le LLM qui reformule, en
  descendant en taille), banc A/B/C de l'énergie avec CodeCarbon.

### Mardi après-midi : on retire les actions bancaires

Le premier prototype « agissait » (faire opposition en deux messages, préparer un virement). **Décision
de l'équipe : l'assistant n'a aucun accès au compte et n'exécute rien** — c'est le périmètre du
kick-off, et c'est plus sûr. Il explique, guide vers l'espace bancaire sécurisé ou le conseiller, et
rappelle de ne jamais donner son code.

### Mardi fin d'après-midi : les remarques des encadrants, et l'aiguilleur

Les encadrants ont regardé la proposition et demandé **un LLM dans le pipeline et un mécanisme qui
choisit le modèle selon la demande** (« le plus petit modèle qui suffit » peut aussi vouloir dire :
plusieurs modèles, chacun au bon moment). Ils ont fait trois remarques, toutes intégrées :

1. **Le JSON du petit modèle doit être imposé par une grammaire** (sortie contrainte : Ollama `format`,
   vLLM `response_format`), pas seulement demandé dans le prompt. Résultat : **100 % de JSON valide,
   même avec un modèle de 1 milliard de paramètres**.
2. **Deux RAG** : un **RAG d'exemples** au niveau 1 (les 8 phrases d'entraînement les plus proches,
   données au LLM avec leur sujet) et un **RAG de fiches** au niveau 2 (les fiches sourcées où il
   puise sa réponse).
3. **« Remarque très importante » : le niveau doit pouvoir changer à chaque message** — une
   conversation peut faire niveau 1 → 2 → 0 → 2. D'où un aiguilleur qui décide message par message,
   avec une mémoire commune.

La cascade est devenue **l'aiguilleur à trois niveaux**. L'escalade vers le 14B a été remplacée par le
niveau 1 (un modèle de 1,4 Go au lieu de 9 Go).

### Mardi soir : choisir les modèles, en descendant en taille

Deux bancs dédiés (36 messages difficiles pour le niveau 1, 22 questions pour le niveau 2), cinq
modèles testés sur DeepEirb (de 0,8 à 6 Go). **`qwen3:1.7b` (1,4 Go) retenu pour les deux niveaux** :
c'est le plus petit qui tient le niveau 1 (30/36, avec le RAG d'exemples), et le seul à 22/22 au
niveau 2. Un seul modèle chargé.

**La reformulation des conseils par un LLM a été mesurée puis écartée** (désactivée par défaut) :
elle coûtait plus d'énergie (6,2 contre 5,5 Wh pour 1 000 messages) et faisait perdre un scénario
(13/14), sans gain visible. Les gabarits suffisent.

### Mercredi matin : l'épreuve du réel

- Test sur la machine de la salle (`ail`, RTX 3060) : un premier appel de **58 s** (modèle pas encore
  chargé) → délais maximum par niveau (10 s / 20 s), modèle gardé en mémoire 4 h, préchauffage au
  lancement. **La démo ne peut jamais être bloquée par le LLM** : si le LLM ne répond pas, on reste au
  niveau 0 ou on donne l'extrait de la fiche.
- Un test libre à la main a révélé des défauts (un nombre seul pris pour un « Bonjour », un crédit de
  10 000 € lu comme un bien immobilier, « oui ou non ? » pris pour un refus, rendez-vous, relevés) →
  cinq règles ajoutées.
- **Banc de 30 conversations libres de 10 messages**, puis **30 nouvelles jamais vues** pour juger
  honnêtement (voir §9.7) : des corrections sur la politesse, la reprise après un refus, les
  corrections en cours de question, les définitions ; une règle de sécurité (« on ne donne jamais son
  code »).
- Interface finale dans le style Timso AI (projet antérieur de Yahya), vue démo / vue utilisateur,
  CO₂ par réponse, barre de scénario pour la démo.

---

## 6. L'architecture finale : l'aiguilleur et ses trois niveaux

Le point d'entrée unique est `src.assistant.reply(message, client_id, etat)`. Schéma : diapositive 3
du support (`rapport/schema-aiguilleur.pdf`, page 1 ; les pages suivantes détaillent chaque niveau).

```text
message du client
  │
  ▼
ENTRÉE COMMUNE (sans LLM, ~6 ms)
  barrières (règles prioritaires) · entités (montants, durées, liens familiaux) · contexte
  mots-clés (toutes les demandes du message) · classifieur e5-small + régressions (confiance vs τ)
  │
  ▼
AIGUILLEUR (du code) : 5 signaux → un niveau
  │
  ├── niveau 0 : automate + parcours YAML → conseiller (règles M3) → gabarits
  ├── niveau 1 : petit LLM interprète (RAG d'exemples, JSON imposé) → vérifié → retour au niveau 0
  └── niveau 2 : RAG sur 37 fiches → LLM rédige en citant → garde-fou → sinon extrait
  │
  ▼
MÉMOIRE COMMUNE : parcours en cours, informations données, demandes en file, parcours mis de côté
  │
  ▼
réponse + niveau + raison + sources + étapes mesurées (latence, modèle, tokens, appel LLM)
```

### 6.1 L'entrée commune (sans LLM)

1. **Barrières**, avant tout le reste :
   - **sécurité** : quelqu'un demande le code de carte ou les identifiants → « Ne donnez jamais votre
     code confidentiel, ni vos identifiants, à personne… si vous l'avez déjà donné, faites opposition
     tout de suite » ;
   - **montant ambigu** (point décimal, signe) → on demande de reformuler ;
   - **rendez-vous** → l'assistant ne peut pas en prendre : il dit comment faire ;
   - **données du compte** (« regarde mes relevés ») → il n'y a pas accès, il le dit et oriente ;
   - **au revoir / je vais réfléchir** → on salue, la demande en cours reste en mémoire.
2. **Entités** (expressions régulières) : montants (« 25k », « 200 000 € »), durées (« 48 mois »,
   « sur 3 ans »), liens familiaux (« mon papa » → père, « ma frangine » → sœur).
3. **Mots-clés** : un petit lexique par intention ; s'il trouve une seule intention, sûr de lui, c'est
   fini (19 % des messages français, **100 % justes**). Il trouve aussi **toutes** les demandes d'un
   message (« j'ai perdu ma carte et je veux faire un virement »).
4. **Classifieur** : multilingual-e5-small (118 M de paramètres) encode le message ; deux régressions
   logistiques donnent l'intention (85) et la famille (14) avec une probabilité. **Au-dessus de τ = 0,76,
   on lui fait confiance** ; en dessous, c'est un doute.
5. **Contexte** : si une question est en attente (« À qui voulez-vous envoyer l'argent ? »), le message
   est d'abord lu comme sa réponse, sauf s'il ouvre clairement un autre sujet.

### 6.2 L'aiguilleur : cinq signaux, calculés sans LLM

| Signal | Exemple | Effet |
|---|---|---|
| 1. Plusieurs demandes dans le message | « J'ai perdu ma carte et je veux faire un virement » | Niveau 0 si elles sont nettes : **l'urgence d'abord** (carte perdue avant virement, avant crédit…), les autres en file |
| 2. Confiance sous τ | « jsui au distrib la » | Niveau 1 |
| 3. Réponse libre que les règles ne savent pas lire | « oui » quand on attend un bénéficiaire | Niveau 1 |
| 4. Renvoi au contexte | « mais ma carte ? », « et pour mon fils ? » | Niveau 1 |
| 5. Question ouverte sur un sujet de nos fiches | « Je peux retirer de mon PEL avant 4 ans ? », « pourquoi ? » après un conseil | Niveau 2 |

Le signal 5 combine des **marqueurs de question** (forts : « pourquoi », « ai-je le droit », « plafond »,
« combien de temps », « quelle différence »… ; faibles : « je peux », « est-ce possible »…) et la
présence d'un **sujet de nos fiches** dans le message (PEL, LDDS, HCSF, notaire…). Une demande nette
qui ouvre un parcours guidé reste au niveau 0 (« pourquoi j'ai payé 8 € de frais ? » ouvre le parcours
frais, pas le RAG).

Si le LLM n'est pas disponible (`ASSISTANT_LLM` non activé, serveur injoignable, délai dépassé),
l'aiguilleur **reste au niveau 0** : une question de clarification, ou l'extrait de la fiche.

### 6.3 Le niveau 0 : règles et gabarits

- **Automate de dialogue** (`src/converser/dialogue.py`) qui lit **9 parcours YAML** (un par
  situation) : carte perdue, virement, frais, épargne, crédit immobilier, crédit conso, prêt étudiant,
  insatisfaction, définition. Chaque parcours liste les informations nécessaires, leur source (le profil
  ou une question) et la fin (conseil, orientation, fiche). **On ne redemande jamais ce que le profil
  sait** : on le confirme (« J'ai noté vos revenus de 2 900 € nets par mois »).
- **Cas limites gérés** : « je ne sais pas » (valeur par défaut annoncée : « Je pars sur un an ; vous
  pourrez ajuster »), refus (« non », « laisse tomber » → le parcours est mis de côté), « finalement
  oui » (il reprend), une correction (« non plutôt 8000 », « et sur 60 mois ? » → le conseil est
  recalculé), un nombre seul (« 1000 ») qui continue le parcours, un crédit de 10 000 € qui n'est pas
  un bien immobilier (bascule vers le crédit conso).
- **Mémoire et reprise** : une parenthèse (une définition, une question au niveau 2) ne fait pas perdre
  le parcours : « Revenons à votre virement : quel montant voulez-vous envoyer ? ». Plusieurs demandes :
  traitées par ordre d'urgence, puis « Passons maintenant à votre autre demande ».
- **Vraisemblance des montants** : au-delà de 10 fois les revenus mensuels, « Attention : 100 000 000 €,
  c'est un montant très inhabituel, bien au-delà de votre solde (1 450 €) : vérifiez-le ».
- **Conseiller (M3)** : règles publiques (voir 6.6).
- **Gabarits de réponse** (`src/converser/formuler.py`) : phrases écrites par l'équipe, mention légale
  sur tout crédit (« Un crédit vous engage et doit être remboursé… »), **mots simples** automatiques
  dès 70 ans ou si le client dit être peu à l'aise (le jargon est expliqué : « opposition veut dire… »),
  **glossaire** de 18 termes (TAEG, HCSF, apport, découvert autorisé, IBAN…).

### 6.4 Le niveau 1 : un petit LLM qui comprend, mais ne répond pas

Fichier : `src/comprendre/interprete.py`.

1. **Contexte donné au LLM** : le sujet en cours, la question en attente, les sujets déjà traités.
   **Jamais le profil du client.**
2. **RAG d'exemples** : e5-small cherche les **8 phrases d'entraînement les plus proches** du message
   et les donne au LLM avec leur sujet (« messages proches déjà classés »). Mesuré : cela **double la
   justesse** de qwen3:1.7b (de 15 à 30 messages justes sur 36).
3. **JSON imposé par une grammaire** : le serveur (Ollama ou vLLM) ne peut produire que du JSON conforme
   au schéma — une liste de 1 à 3 intentions prises dans une énumération fermée (+ « aucune »), et la
   réponse à la question en attente. **100 % de JSON valide** sur tous les modèles testés.
4. **Vérifié par le code** : une valeur lue doit être dans le message ou dans une liste fermée (jamais
   un nombre inventé) ; une nouvelle demande proposée pendant une question doit être confirmée par les
   mots-clés ou le classifieur ; l'urgence est réordonnée par le code ; un renvoi « mais ma carte ? » est
   rattaché au sujet déjà traité du même domaine.
5. **Le LLM ne parle jamais au client** : ce qu'il a compris repart au niveau 0, qui pose la question
   suivante ou donne le conseil. Délai maximum : 10 s, sinon niveau 0.

### 6.5 Le niveau 2 : RAG sur nos fiches, sous garde-fou

Fichier : `src/rag.py`.

- **37 fiches sourcées** : 11 fiches produit (catalogue), 4 fiches de règles (paramètres
  réglementaires : HCSF, frais de notaire, plafonds de frais…), 18 fiches de glossaire, 4 fiches écrites
  à la main (périmètre de l'assistant, opposition, réclamation, virement). Chaque fiche a sa source et
  sa date (Service-Public, HCSF, Banque de France, notaires, LBP, Trésor ; relevé du 27 octobre 2026).
- **Recherche** : index e5-small en mémoire, 3 passages ; **recherche hybride** (bonus de 0,02 par mot
  du sujet de la fiche cité, au plus deux ; bonus de 0,015 pour une fiche chiffrée quand la question
  est chiffrée). **Seuil de pertinence : cosinus 0,82** — en dessous, « Je n'ai pas cette information
  dans mes fiches » et orientation vers un conseiller (jamais de réponse inventée).
- **« Pourquoi ? » après un conseil** : les phrases du dernier conseil (« Crédit immobilier n'est pas
  proposé : 41,3 % des revenus… ») deviennent les passages de « Votre simulation ».
- **Rédaction** : le LLM rédige en citant [1], [2]. Délai maximum 20 s.
- **Garde-fou** (le code vérifie la rédaction) :
  - **tous les chiffres** de la réponse doivent être dans les extraits ;
  - **fidélité ≥ 0,8** : la part des mots de la réponse présents dans les extraits ;
  - pas de formule interdite, longueur plausible (≤ 900 caractères) ;
  - une citation ; si la réponse est fidèle mais sans citation, on ajoute [1].
  Si le garde-fou refuse, on donne **l'extrait de la meilleure fiche** (« D'après nos fiches : … »).
  La réponse reste donc juste dans tous les cas ; seule la fluidité varie.
  Le texte refusé est gardé et affiché dans l'interface, avec les mots absents des fiches surlignés
  (le LLM écrit avec un peu de hasard, température 0,2 : la même question peut être acceptée une fois et
  refusée une autre ; c'est le garde-fou qui garantit la réponse, pas le modèle).

### 6.6 Le conseiller (M3) : des règles publiques, pas un score

- **Quatre parcours métier** : immobilier, consommation, épargne, prêt étudiant.
- **Catalogue de 12 produits** : Livret A, LDDS, LEP, Livret Jeune, PEL, CEL, crédit immobilier, PTZ,
  prêt personnel, prêt étudiant, offre clientèle fragile, rendez-vous avec un conseiller.
- **Paramètres sourcés et datés** :
  - **HCSF** : taux d'effort ≤ 35 % des revenus, assurance comprise ; durée ≤ 25 ans (le cadre
    général ; la banque garde une part de flexibilité) ;
  - **taux** : repère statistique Banque de France (3,3 % pour l'immobilier, période août 2026 ;
    6 % pour la consommation), **pas une offre LBP** ;
  - **frais de notaire** : ~7,5 % dans l'ancien, ~2,5 % dans le neuf ;
  - **plafonds** : Livret A 22 950 €, LDDS 12 000 €, Livret Jeune 1 600 € (12–25 ans), PEL 61 200 € ;
  - **frais d'incident** : commission d'intervention plafonnée à 8 € par opération et 80 € par mois
    (4 € et 20 € pour la clientèle fragile).
- **Chaque conseil contient** : les produits proposés avec leurs raisons, les produits **écartés** avec
  la règle qui les écarte (identifiant de règle, ex. `HCSF-taux-effort`), les hypothèses (assurance
  inconnue, frais non couverts), les sources. Pour un crédit : `decision_bancaire = False` — **ce n'est
  jamais un accord ni un refus**, un conseiller étudie le dossier.
- **Distinction tenue partout** : éligibilité (conditions d'un produit) ≠ pertinence (adéquation au
  projet) ≠ estimation (calcul sous hypothèses) ≠ octroi (décision humaine de la banque).

### 6.7 Un exemple de bout en bout : l'appartement de Léa

Léa (C07) : 31 ans, cadre, 2 900 € nets par mois, 25 000 € d'épargne, aucun crédit.

1. « Je veux acheter un appartement » → **niveau 0** (mots-clés) : « C'est un beau projet. J'ai noté vos
   revenus de 2 900 € nets par mois. Quel est le prix du bien que vous visez, et quelle part de vos
   25 000 € d'épargne souhaitez-vous y consacrer ? »
2. « Autour de 250 000, et je peux mettre les 25 000 » → **niveau 0** : les deux montants sont lus ;
   le conseiller calcule : frais de notaire (~7,5 % dans l'ancien), mensualité ≈ **1 197 € sur 25 ans**
   à 3,3 % hors assurance, soit **41,3 % des revenus > 35 %** → « Non proposé — projet non retenu dans
   cette simulation ; aucun refus bancaire n'est prononcé ». Écarté aussi : le prêt sur 30 ans (règle
   HCSF durée). Budget indicatif sous ces hypothèses : ≈ 215 000 €. Mention légale.
3. « pourquoi ? » → **niveau 2** : réponse tirée de « Votre simulation », citée.
4. « Et avec un bien à 200 000 ? » → **niveau 0** : recalcul, **933 €/mois, 32,2 %** → proposé, sous
   réserve de l'étude du dossier ; un conseiller peut étudier le projet.

### 6.8 Un exemple multi-niveaux : le test des encadrants (Inès, C01)

| Message | Niveau | Pourquoi |
|---|---|---|
| « J'ai perdu ma carte et je veux faire un virement. » | 0 | Deux demandes nettes : la carte d'abord (urgence), puis le virement est engagé |
| « oui » | 1 | Pas une réponse lisible à « À qui voulez-vous envoyer l'argent ? » : le LLM comprend que c'est le même sujet, sans valeur → la question est reposée avec des exemples |
| « c'est pour mon papa » | 0 | Les règles lisent « papa » → père |
| « Je peux retirer de mon PEL avant 4 ans ? » | 2 | Question ouverte sur une fiche : réponse citée, puis « Revenons à votre virement » |
| « 100000000 » | 0 | Montant invraisemblable comparé au solde : avertissement |
| « mais ma carte ? » | 1 | Renvoi au contexte : rattaché à la carte perdue déjà traitée |

---

## 7. Les données

| Donnée | Taille | Rôle | Fichier |
|---|---|---|---|
| **Banking77** (anglais, non traduit) | 10 003 phrases d'entraînement, 3 080 de test, 77 intentions | Entraîner le classifieur ; test anglais | `data/raw/` |
| **Phrases de l'équipe** (français) | 672 phrases | Nos 8 intentions + exemples des familles Banking77 ; aussi le RAG d'exemples du niveau 1 | `data/processed/exemples_fr.yaml` |
| **Test français** (écrit à la main, jamais vu à l'entraînement) | 250 phrases (10 par famille Banking77, 20 par intention de l'équipe) | Mesurer la compréhension en français | `data/processed/test_fr.yaml` |
| **Bank Marketing** | — | Ancrage documentaire des profils (ligne, valeurs, SHA256) ; colonne `duration` exclue (fuite) | `data/raw/` |
| **Profils clients** C01–C08 | 8 personnages fictifs | Profil, historique simulé (frais du mois, découverts, contacts du jour), provenance de chaque champ | `data/processed/clients.json` |
| **Catalogue** | 12 produits + paramètres | Règles de conseil, fiches produit du RAG | `data/processed/catalogue.json` |
| **Glossaire** | 18 termes | Définitions en mots simples ; fiches du RAG | `data/processed/glossaire.json` |
| **Fiches à la main** | 4 | Périmètre, opposition, réclamation, virement | `data/processed/fiches.yaml` |
| **Banc du niveau 1** | 36 messages difficiles | Choisir le modèle du niveau 1 | `data/processed/banc_niveau1.yaml` |
| **Banc du niveau 2** | 22 questions (18 couvertes + 4 hors fiches) | Choisir le modèle du niveau 2 | `data/processed/banc_niveau2.yaml` |
| **Scénarios de référence** | 15 conversations | Tests de bout en bout | `eval/scenarios/` |
| **Conversations libres** | 2 × 30 conversations de 10 messages | Juger le produit sur des conversations réalistes | `eval/conversations_libres.yaml`, `eval/conversations_nouvelles.yaml` |

**Taxonomie** (`src/taxonomie.py`) : **14 familles**, **85 intentions** (les 77 de Banking77 + nos 8).
Familles : carte perdue, utilisation de la carte, commande de carte, frais ou opération contestée,
virement, compte ou identité, espèces, change ou étranger, alimentation du compte, épargne, crédit,
explication, réclamation, autre chose.

**Profils** :

| Id | Prénom | Âge | Situation | Revenus nets | Épargne | Solde | Crédits en cours |
|---|---|---|---|---|---|---|---|
| C01 | Inès | 34 | cadre, célibataire | 3 200 € | 8 000 € | 1 450 € | 0 |
| C02 | Marc | 52 | ouvrier, marié, découverts fréquents | 1 850 € | 0 € | −120 € | 0 |
| C03 | Sophie | 41 | employée, mariée, enfants de 8 et 12 ans | 2 400 € | 6 000 € | 980 € | 0 |
| C04 | Paul | 68 | retraité, veuf, un fils | 1 600 € | 12 000 € | 2 300 € | 0 |
| C05 | Karim | 29 | technicien, célibataire | 1 900 € | 1 500 € | 640 € | 150 €/mois |
| C06 | Julie | 37 | employée de services | 2 100 € | 3 000 € | 410 € | 0 |
| C07 | Léa | 31 | cadre, célibataire | 2 900 € | 25 000 € | 1 800 € | 0 |
| C08 | Lucas | 20 | étudiant | 450 € | 0 € | 120 € | 0 |

Les champs simulés sont marqués « simulé » dans l'interface.

---

## 8. Technologies et modèles

| Brique | Technologie | Pourquoi |
|---|---|---|
| Langage | Python 3.10+ | Écosystème ML |
| Encodeur | **intfloat/multilingual-e5-small** (118 M paramètres, 0,47 Go), préfixe `query:` | Multilingue (pas de traduction), petit, quelques ms même sur CPU ; déjà maîtrisé (projet Timso AI) |
| Classifieur | **Régressions logistiques** (scikit-learn) sur les vecteurs e5, têtes de 141 Ko | Entraînées en ~4 min sur CPU, donnent des **probabilités** (seuil τ, deux familles quand on doute) |
| LLM | **qwen3:1.7b** (1,4 Go) pour les niveaux 1 et 2, via **Ollama** (ou vLLM) | Le plus petit qui tient chaque niveau, mesuré (§9) ; un seul modèle chargé |
| Sortie contrainte | Schéma JSON (Ollama `format`, vLLM `response_format`) | JSON valide à 100 % |
| Dialogue | Automate + **parcours YAML** | Lisible, modifiable sans code, déterministe, sans LLM |
| Règles de conseil | Python (M3), paramètres sourcés en JSON | Explicables, vérifiables à la main |
| Interface | **FastAPI** + une page HTML (thème Timso AI) ; Streamlit « Noria » en secours | Léger, sans dépendance front |
| Mesure | **CodeCarbon** (hors ligne, France), chronométrage par étape | Exigé par le hackathon |
| Tests | pytest (152 tests), 15 scénarios de bout en bout | `main` toujours exécutable |
| Support | LaTeX Beamer | — |

**Modèles testés et non retenus** : `ministral-3:14b` (9,1 Go, la configuration « tout LLM » de
comparaison, et l'ancienne escalade), `ministral-3:8b` (6 Go), `gemma4:e2b` (4,6 Go — il fallait couper
sa « réflexion »), `ministral-3:3b` (3 Go — 33/36 au niveau 1, l'alternative si on veut plus de marge),
`gemma3:1b` (0,8 Go — trop faible au niveau 1 : 17/36).

**Pas de fine-tuning** : les têtes logistiques s'entraînent en minutes ; le transfert multilingue
d'e5 suffit ; un fine-tuning coûterait de l'énergie et du temps pour un gain non démontré.

---

## 9. Évaluation et résultats chiffrés

Toutes les mesures « officielles » ont été faites sur **DeepEirb (2 × RTX 6000 Ada 48 Go)** le
27 octobre. **La justesse est jugée par du code contre des réponses attendues**, pas par un LLM juge.

### 9.1 Comprendre (Younes)

| Configuration | Anglais (intention, 77) | Français (routage) | Latence p50 | Taille |
|---|---|---|---|---|
| *Référence : BERT affiné (article Banking77)* | *93,7 %* | — | — | *0,44 Go* |
| Mots-clés seuls | — | 19,2 % acceptés, **100 % justes** | < 0,1 ms | 2 Ko |
| TF-IDF + régression logistique | 89,2 % | 66,8 % | 0,3 ms | 3,9 Mo |
| **e5-small + régression logistique** | **92,3 %** | **84,8 %** | 6,3 ms | 471 Mo |
| **Étage 1 : mots-clés puis e5 (au-dessus de τ)** | — | **76,4 % compris, 96,9 % justes** | 6,1 ms | — |
| `ministral-3:14b` qui classe seul | famille 52,9 % | 83,2 % | 77,6 ms | 9,1 Go |
| `qwen3:1.7b` qui classe seul | famille 6,8 % | 29,2 % | 17,7 ms | 1,4 Go |

- **Français (routage)** : bonne famille pour une demande de service Banking77, bonne intention pour nos
  8 intentions.
- **À dire** : on est à 1,4 point du BERT affiné de l'article, **sans avoir traduit** ; et un LLM de 14B
  qui classe seul fait moins bien, 12 fois plus lentement et 20 fois plus lourd. **Un petit LLM seul ne
  sait pas classer** (29 %) : c'est pour cela qu'il n'est appelé que pour lire un message flou, guidé par
  des exemples et une grammaire.
- Sous τ, l'assistant **ne devine pas** : il pose une question fermée (« votre demande concerne-t-elle
  un virement, ou la commande d'une carte ? ») ou passe au niveau 1.
- Validation du classifieur : exactitude intention 91,3 %, routage 94,1 %, précision des acceptés 97,1 %
  pour 88,7 % de messages acceptés (τ = 0,76).

### 9.2 Niveau 1 : le plus petit LLM qui comprend (36 messages difficiles)

| Modèle | Taille | Justes, avec RAG d'exemples | Sans | JSON valide | Latence p50 |
|---|---|---|---|---|---|
| `ministral-3:8b` | 6,0 Go | 31/36 | 31/36 | 100 % | 264 ms |
| `gemma4:e2b` | 4,6 Go | 29/36 | 23/36 | 100 % | 217 ms |
| `ministral-3:3b` | 3,0 Go | **33/36** | 31/36 | 100 % | 250 ms |
| **`qwen3:1.7b` (retenu)** | **1,4 Go** | **30/36** | 15/36 | 100 % | **188 ms** |
| `gemma3:1b` | 0,8 Go | 17/36 | 16/36 | 100 % | 454 ms |

- **« Juste »** = les bons sujets (le premier mène au bon parcours, tous les sujets attendus sont trouvés)
  **et** la bonne valeur retenue (« à ma frangine » → sœur ; rien quand il n'y a rien à retenir). Le
  message passe par le vrai chemin : contexte, RAG d'exemples, JSON imposé, vérification par le code.
- **Le RAG d'exemples double la justesse de qwen3:1.7b** (15 → 30) ; il n'apporte rien au 8B.
- **La grammaire donne 100 % de JSON valide, même à 1B** : le seul risque restant est le sens, et c'est
  lui que le banc mesure.

### 9.3 Niveau 2 : répondre en citant nos fiches (22 questions)

| Rédaction | Réponses justes | Rédactions acceptées par le garde-fou | Latence p50 |
|---|---|---|---|
| Sans LLM (extrait de la fiche) | 21/22 | — | 12 ms |
| **`qwen3:1.7b` (retenu)** | **22/22** | **9/18** | **391 ms** |
| `gemma3:1b` | 21/22 | 1/18 | 355 ms |
| `ministral-3:3b` | 21/22 | 3/18 | 476 ms |
| `gemma4:e2b` | 21/22 | 9/18 | 300 ms |
| `ministral-3:8b` | 21/22 | 4/18 | 703 ms |

- **La recherche trouve la bonne fiche parmi les 3 passages pour 18 questions sur 18**, et **refuse
  les 4 questions hors de nos fiches** (météo, match…).
- **« Juste »** = la réponse finale (rédigée ou repli) contient les faits attendus (ex. « 22 950 » pour
  le plafond du Livret A) ; hors fiches : l'assistant refuse.
- **Les réponses restent justes quel que soit le modèle**, grâce au repli sûr. **Les gros modèles
  réécrivent plus librement**, donc le garde-fou les écarte plus souvent : plus gros ne veut pas dire
  plus fidèle.

### 9.4 Formulation (reformuler un conseil) : mesurée, puis écartée

Banc de 30 conseils, six modèles. Le garde-fou (aucun chiffre inventé ni oublié) accepte 30/30 pour
qwen3:1.7b, 27/30 pour ministral-3:8b et gemma4:e2b, 23/30 pour le 14B. Mais dans le banc A/B/C, la
reformulation **coûtait plus** (6,2 contre 5,5 Wh pour 1 000 messages) et faisait perdre un scénario
(13/14). **Décision : les gabarits restent, la reformulation est désactivée par défaut**
(`ASSISTANT_REFORMULER=1` pour la réactiver).

### 9.5 Frugalité : A/B/C (Younes)

Mesure : **CodeCarbon hors ligne (France)**, lots de 200 messages × 3 répétitions après chauffe
(A : 40 messages × 1, parce que le 14B répond à chaque message), puissance au repos de la machine
(186,9 W) mesurée puis soustraite.

| Configuration | Scénarios | Wh / 1 000 messages (repos soustrait) | Wh / 1 000 (brut) | Latence p95 | Mémoire | Sans LLM |
|---|---|---|---|---|---|---|
| **A** : `ministral-3:14b` répond à tout | à juger | 115,4 | 194,3 | 2,3 s | 9,1 Go | 0 % |
| **B : notre aiguilleur (`qwen3:1.7b`)** | **15/15** | **5,5** | **11,5** | **0,53 s** | **1,9 Go** | **76 %** |
| **C** : niveau 0 seul (règles) | 15/15 | 0,18 | 0,40 | 19 ms | 0,5 Go | 100 % |

- **À dire** : l'aiguilleur consomme **17 fois moins** que le 14B, **sans même soustraire le repos**
  (11,5 contre 194 Wh) — 21 fois moins au repos soustrait. **5 fois moins de mémoire**, latence p95
  **0,5 s au lieu de 2,3 s**. Le niveau 0 seul consomme **près de 500 fois moins** que le 14B.
- Répartition dans l'aiguilleur : niveau 0 : 76 %, niveau 1 : 12 %, niveau 2 : 12 %.
- **CO₂** : CodeCarbon applique **56,039 g de CO₂e par kWh** au réseau français (version 3.3.2).
  Par réponse, l'interface affiche ≈ **10 µg de CO₂e** sans LLM et ≈ **1,3 mg** avec un appel au LLM
  (estimation : énergie mesurée par type de réponse × intensité ; on ne mesure pas une requête de 20 ms
  en direct). Pour 1 000 messages : ≈ 0,65 g de CO₂e pour l'aiguilleur contre ≈ 10,9 g pour le 14B
  (valeurs brutes).

### 9.6 Tests et scénarios

- **152 tests automatisés** (pytest) : contrats, compréhension, règles, conseil, garde-fou, aiguilleur
  (dont la chaîne de niveaux 1 → 2 → 0 → 2), interface.
- **15 scénarios de bout en bout sur 15** (Inès carte, Marc frais, Sophie épargne, Paul virement et
  correction, Karim crédit auto, Lucas prêt étudiant / épargne jargon / crédit non retenu, Léa
  appartement, Julie insatisfaction, clarification, le test des encadrants…). Un scénario qui casse
  bloque la fusion.
- **Démo de secours** : `rapport/demo-secours.pdf`, 19 tours rejoués par le vrai pipeline avec le LLM,
  **15 sans aucun appel au LLM**, 4 appels au total.

### 9.7 Conversations libres : ce que donne le produit sur des conversations réalistes

C'est la mesure la plus exigeante, et la plus honnête. Elle n'est **pas** dans le support, mais il faut
la connaître pour les questions.

**Méthode.** 30 conversations de 10 messages, écrites comme de vrais clients (fautes, familier,
plusieurs demandes, changements de sujet, refus, hors sujet), rejouées par le vrai pipeline sur la
machine de la salle (`ail`, RTX 3060, qwen3:1.7b). Chaque réponse est ensuite **jugée à la main**
(juste / acceptable / fausse), avec des signaux automatiques (incompris, clarification, repli du
garde-fou…). Rapports complets, réponse par réponse : `eval/resultats/conversations-libres.md` et
`conversations-nouvelles.md`.

**Premier jeu (30 conversations, qui ont servi à corriger)** : en trois passages, les « Bonjour ! » mal
placés sont passés de 46 à 1, les « je n'ai pas bien compris » de 20 à 4, les « pas de fiche » de 12 à 0,
les clarifications de 3–7 à 2. Mais ce jeu a servi aux corrections : il ne prouve pas la généralisation.

**Second jeu : 30 nouvelles conversations jamais vues** (langage SMS, fautes lourdes, client âgé très
formel, anglais, mélange arabe-français-anglais, émojis, montants en lettres, trois demandes en une,
fraude, deuil, colère, messages vides, questions sur l'assistant lui-même).

- Niveaux : 0 : 150 · 1 : 122 · 2 : 28 messages ; 161 appels au LLM ; latence p50 0,17 s, p95 0,54 s.
- **Jugement réponse par réponse : environ une réponse sur deux est juste (≈ 47 %)**.
- **Ce qui marche bien (7 à 8,5 réponses justes sur 10)** : les demandes claires et les parcours guidés
  (crédit, épargne, immobilier, plusieurs projets), les variantes (« et sur 5 ans ? », « plutôt
  30000 »), les définitions, les questions sur nos fiches (notaire, plafonds, différence entre livrets),
  la politesse (« au revoir »), la réclamation, l'alerte quand on demande le code.
- **Ce qui casse** :
  1. **La boucle sur la question en attente** (première cause) : si le client parle d'autre chose
     pendant une question, l'assistant repose la même question, parfois plusieurs fois ; et un
     bénéficiaire hors de notre liste de liens (« à mon propriétaire », « to my brother ») n'est pas lu.
  2. **Le petit LLM du niveau 1 invente parfois un virement** (« retrait sans carte », « je lui ai
     donné »).
  3. **Le classifieur se trompe sur certaines phrases libres** (« je suis à découvert » → commande de
     carte).
  4. **Quelques règles se déclenchent à tort** (« pouvez-vous me rappeler ce qu'est un IBAN » →
     rendez-vous ; « frais sur mon relevé » → « je n'ai pas accès à vos relevés »).
  5. **Le deuil** reçoit une réponse de réclamation (« désolé pour ce désagrément ») : inadaptée.
  6. **La langue** : langage SMS et nombres en lettres mal lus.
- **Comment en parler si on nous interroge** : « Sur nos 15 scénarios et nos bancs, c'est solide. Sur
  30 conversations libres jamais vues, écrites pour être difficiles, environ une réponse sur deux est
  juste ; la première cause d'échec est la gestion d'un hors-sujet pendant une question en attente,
  et nous savons la corriger (mettre le parcours de côté après une relance sans réponse). Nous avons
  préféré mesurer ce qui ne marche pas plutôt que de ne montrer que les cas qui marchent. »

---

## 10. Explicabilité

- **Chaque réponse dit son niveau et pourquoi** (« Niveau 0 · règles — demande claire (mots-clés) »,
  « Niveau 1 — confiance sous le seuil », « Niveau 2 — question ouverte sur un sujet de nos fiches »).
- **Chaque conseil dit pourquoi, et pourquoi pas** : produits proposés avec leurs raisons, produits
  écartés avec la règle (identifiant `HCSF-taux-effort`, `HCSF-duree`…), hypothèses, sources datées.
- **Le calcul se vérifie à la main** (Léa : 1 197 €/mois, 41,3 % > 35 %).
- **« Pourquoi ? »** après un conseil → le niveau 2 répond à partir du conseil lui-même, en citant.
- **Les réponses du niveau 2 citent leurs fiches** [1], avec la source et la date ; l'interface montre
  les passages retrouvés et leur score.
- **Compréhension visible** : intention, famille, confiance vs τ, phrase d'entraînement la plus proche,
  autres demandes mises en file.
- **Étapes mesurées** : pour chaque réponse, chaque étape (comprendre, converser, conseiller, rag,
  rédiger, formuler) avec sa latence, son modèle, ses tokens.

---

## 11. Confiance, conformité, inclusion

- **Règlement européen sur l'IA (AI Act)** : la notation de solvabilité de personnes physiques est un
  usage à **haut risque** ; nous n'en faisons pas — un conseiller décide. Le client sait qu'il parle à
  une IA.
- **Mention légale** sur toute réponse de crédit ; aucune promesse, jamais d'accord ni de refus.
- **Aucun accès au compte, aucune opération** : l'assistant explique et oriente (espace bancaire
  sécurisé, conseiller, agence). Rappel systématique : la banque ne demande jamais le code confidentiel.
- **LLM encadrés** : au niveau 1, il ne voit pas le profil et ne répond pas au client ; au niveau 2, il
  ne répond qu'à partir de fiches sourcées, sous garde-fou, sinon « je n'ai pas cette information ».
- **Données simulées, traitement local** : rien ne sort de la machine (souveraineté), modèles open
  source.
- **Inclusion** (valeur clé de LBP) : mots simples automatiques pour les plus âgés ou les clients peu à
  l'aise, jargon expliqué, offre clientèle fragile proposée aux clients en difficulté, plafonds des frais
  rappelés.
- **Réclamations** (sujet « prégnant » pour LBP) : frustration reconnue, chemin conseiller → service
  réclamations → médiateur bancaire (gratuit).

---

## 12. Limites, en toute honnêteté

- **Simulé** : profils et historiques (Bank Marketing enrichi), système bancaire, taux indicatifs
  (repères Banque de France, pas des offres LBP). Le catalogue n'est pas exhaustif ; pas de TAEG complet ;
  le PTZ est une fiche d'orientation.
- **Conversations libres** : environ une réponse juste sur deux sur des conversations jamais vues et
  difficiles (§9.7). Points faibles connus : hors-sujet pendant une question en attente, langage SMS,
  nombres en lettres, sujets sensibles (deuil), quelques confusions du petit LLM et du classifieur.
- **Les bancs sont petits** (36 et 22 messages pour les niveaux, 250 phrases françaises) et écrits par
  l'équipe ; une seule passe par modèle. Le niveau 2 a été mis au point sur une partie de ses questions
  (titres de deux fiches, bonus de recherche).
- **Énergie** : mesurée sur DeepEirb ; le CO₂ par réponse affiché est une **estimation** (énergie par
  type de réponse × intensité du réseau français), pas une mesure par requête.
- **Pas de voix, pas de multilingue en réponse** (l'assistant comprend un peu d'anglais mais répond en
  français).

**La suite, pour 17 000 bureaux** : le coût par requête est mesuré, donc extrapolable ; compréhension
et règles tournent sur CPU ; un serveur partagé pour le petit LLM ; voix locale et réponse dans la langue
du client (en lien avec l'annonce LBP de novembre) ; corriger la boucle de la question en attente ;
enrichir les liens et les montants en lettres ; un parcours « deuil / succession » dédié.

---

## 13. L'interface de démonstration

Lancement : `ASSISTANT_LLM=1 python -m src.web`, puis `http://localhost:8000`. FastAPI + une page HTML,
**thème repris de Timso AI** (projet antérieur de Yahya) : clair « Bordeaux & lin » (bordeaux sur fond
lin), polices Archivo Expanded et Inter, mode sombre.

**En-tête** : « Assistant bancaire » ; bascule **« Démo : tout voir » / « Utilisateur : les
messages »** ; bouton **« Scénarios »** ; « Mode sombre » ; « Nouvelle conversation ».

**Vue démo** :
- à gauche : le **profil simulé** (champs simulés marqués), l'**aiguillage** (automatique, ou forcer un
  niveau pour la démonstration), « LLM actif », « Mots simples », les **exemples** du profil, les
  statistiques de la conversation (**chaîne des niveaux** 0→1→0→2…, appels au LLM, tokens, latence,
  énergie, **carbone**), l'état du système (LLM joignable, modèles, τ, nombre de fiches) ;
- sous chaque réponse : la **pastille de niveau** (vert : 0, ambre : 1, bordeaux : 2), le LLM utilisé,
  la latence, l'énergie, le **CO₂ estimé** ; les volets **« + Pourquoi »** (aiguillage, compréhension,
  produits proposés / écartés, hypothèses), **« Sources »** (passages et scores), **« Étapes
  mesurées »** ; un avis quand le garde-fou a écarté la rédaction du LLM. Dans ce cas, « + Pourquoi »
  montre **le texte que le LLM avait écrit**, sa fidélité (ex. 52 % pour un minimum de 80 %) et **les mots
  absents des fiches, surlignés** : on voit concrètement ce que le garde-fou a bloqué.

**Vue utilisateur** : seulement la conversation, en bulles (comme une vraie application), avec une ligne
« Sources : » quand une fiche est citée.

**Barre de scénario** (pour la démo) : voir §14.

**Adresses utiles** : `?client=C07` (choisir le client), `?rejouer` (rejoue les exemples du profil),
`?scenario=2` (ouvre le scénario 2), `?utilisateur` / `?demo` (impose la vue). Exemple :
`http://localhost:8000/?scenario=1&utilisateur`.

**Secours** : l'interface Streamlit « Noria » (`streamlit run app.py`) et le PDF
`rapport/demo-secours.pdf`.

---

## 14. La démo en direct : les trois scénarios

On n'en jouera qu'un en entier (le temps est court) ; les deux autres sont des secours ou des extraits.
Les trois ont été **rejoués avec le LLM** : chaque message donne le niveau prévu.

### Comment jouer un scénario

1. Cliquer sur **« Scénarios »**, choisir **1 · Inès**, **2 · Léa** ou **3 · Karim** : le bon client
   est sélectionné et une nouvelle conversation s'ouvre.
2. **« Envoyer › »** ou **la flèche →** : le message suivant est **tapé lettre par lettre** dans la zone
   de saisie (≈ 1 s), puis envoyé. Le jury voit une vraie frappe.
3. **Cliquer sur « Prochain : … »** met le message dans la zone de saisie **sans l'envoyer** : on peut le
   modifier si le jury demande une variante.
4. **Vue utilisateur** : la barre devient une pastille « ▶ 4 / 10 » en bas à droite ; → marche aussi ;
   Échap cache tout.
5. « Nouvelle conversation » remet le scénario au début.

**Conseil** : jouer la démo en **vue démo** (on voit les niveaux, c'est ce qui prouve l'aiguilleur),
et basculer une fois en **vue utilisateur** pour montrer ce que verrait le client.

### Scénario 1 — Inès (C01) : l'aiguilleur passe d'un niveau à l'autre (recommandé)

Chaîne obtenue : **0 → 1 → 0 → 2 → 0 → 1 → 0 → 0 → 0 → 0**.

| # | Message | Niveau | Ce qu'on montre |
|---|---|---|---|
| 1 | « J'ai perdu ma carte et je veux faire un virement. » | 0 | Deux demandes : **la carte d'abord** (opposition, rappel du code), puis le virement est engagé |
| 2 | « oui » | 1 | Pas une réponse : le **petit LLM** comprend que c'est le même sujet ; la question est reposée avec des exemples |
| 3 | « c'est pour mon papa » | 0 | Les règles lisent « papa » → père ; question suivante : le montant |
| 4 | « Je peux retirer de mon PEL avant 4 ans ? » | 2 | **RAG** : réponse citée (retrait anticipé = clôture du plan, fonds pas bloqués), puis **« Revenons à votre virement »** |
| 5 | « 100000000 » | 0 | **Vraisemblance** : « montant très inhabituel, bien au-delà de votre solde (1 450 €) » |
| 6 | « mais ma carte ? » | 1 | **Renvoi au contexte** : rattaché à la carte perdue |
| 7 | « Ma carte ne marche plus au distributeur » | 0 | Compris par le **classifieur** (aucun mot-clé ne conclut) |
| 8 | « Un conseiller m'appelle et me demande mon code, je lui donne ? » | 0 | **Sécurité** : ne jamais donner son code |
| 9 | « Je voudrais un rendez-vous » | 0 | Pas d'accès : explique comment prendre rendez-vous |
| 10 | « merci, au revoir » | 0 | Au revoir |

### Scénario 2 — Léa (C07) : conseil, « pourquoi », fiches citées

Chaîne : **0 → 0 → 2 → 0 → 0 → 2 → 2 → 2 → 0 → 0**.

| # | Message | Niveau | Ce qu'on montre |
|---|---|---|---|
| 1 | « Je veux acheter un appartement » | 0 | Revenus et épargne confirmés depuis le profil ; une seule question |
| 2 | « Autour de 250 000, et je peux mettre les 25 000 » | 0 | Conseil : 1 197 €/mois, **41,3 % > 35 %** → non retenu, **sans refus bancaire** ; 30 ans écarté (HCSF) ; mention légale |
| 3 | « pourquoi ? » | 2 | Le niveau 2 explique **le conseil lui-même**, en citant « Votre simulation » |
| 4 | « Et avec un bien à 200 000 ? » | 0 | Recalcul : 933 €/mois, **32,2 %** → proposé, sous réserve |
| 5 | « c'est quoi le taux d'endettement » | 0 | Glossaire, mots simples |
| 6 | « Combien de frais de notaire pour un appartement ancien ? » | 2 | Réponse citée : ~7,5 % dans l'ancien |
| 7 | « pourquoi pas sur 30 ans ? » | 2 | Le prêt sur 30 ans dépasse le cadre général de 25 ans |
| 8 | « c'est quoi le HCSF ? » | 2 | Fiche HCSF : 25 ans, 35 % |
| 9 | « je peux avoir un rendez-vous ? » | 0 | Orientation |
| 10 | « merci beaucoup » | 0 | Politesse |

### Scénario 3 — Karim (C05) : crédit, corrections, plusieurs sujets (le plus frugal)

Chaîne : **0 → 0 → 0 → 2 → 0 → 0 → 0 → 0 → 0 → 0** (un seul appel au LLM sur 10 messages).

| # | Message | Niveau | Ce qu'on montre |
|---|---|---|---|
| 1 | « Je veux un crédit pour acheter une voiture. » | 0 | Revenus et crédit en cours (150 €/mois) confirmés |
| 2 | « 12000 » | 0 | Un nombre seul continue le parcours |
| 3 | « 48 mois » | 0 | Conseil : 282 €/mois, **22,7 %** des revenus avec les crédits en cours |
| 4 | « pourquoi ? » | 2 | Explication citée |
| 5 | « et sur 60 mois ? » | 0 | Recalcul : 232 €/mois, 20,1 % |
| 6 | « non plutôt 8000 » | 0 | Correction : 155 €/mois, 16 % |
| 7 | « c'est quoi le TAEG » | 0 | Glossaire |
| 8 | « au fait je dois envoyer 200 € à ma mère » | 0 | Nouveau sujet, montant et bénéficiaire lus d'un coup → guidage |
| 9 | « Pourquoi j'ai payé 8 € de frais ce mois-ci ? » | 0 | Explication des frais, plafond légal |
| 10 | « je vais réfléchir, merci » | 0 | « Prenez le temps d'y réfléchir » |

### Préparer la démo (avant 13 h 30)

```bash
# sur la machine de la salle (ail)
cd ~/hackathon-IA && git pull
source .venv/bin/activate
ollama ps                          # vérifier que qwen3:1.7b est chargé (100 % GPU)
ASSISTANT_LLM=1 python -m src.web  # attendre « Préchargement de qwen3:1.7b : prêt »
# puis http://localhost:8000/?scenario=1
```

- **Jouer chaque scénario une fois en entier avant de passer** : le premier appel au LLM est plus lent.
- **Si le LLM tombe** : l'aiguilleur reste au niveau 0 (clarification ou extrait de fiche) ; la démo
  continue. Décocher « LLM actif » montre d'ailleurs le niveau 0 seul.
- **Si tout tombe** : `rapport/demo-secours.pdf` (la démo rejouée par le vrai pipeline).
- **Ne pas improviser de messages hors scénario pendant une question en attente** : c'est la faiblesse
  connue (§9.7).

---

## 15. Le support de présentation, diapositive par diapositive

Fichier : `rapport/soutenance.pdf` (source `rapport/soutenance.tex`, Beamer, 13 diapositives).
Titre : *Un assistant bancaire frugal, explicable et prudent* — *Un aiguilleur : à chaque message, le
plus petit moyen qui suffit* — Yahya, Sohayb, Younes — Hackathon IA La Banque Postale × CGI ×
ENSEIRB-MATMECA, sujet 1, 28 octobre 2026.

| # | Titre | Orateur prévu | Contenu | Message à faire passer |
|---|---|---|---|---|
| 1 | Titre | — | — | — |
| 2 | Le problème | Yahya | Trois messages de clients ; comprendre, questionner, personnaliser ; un Français sur quatre client de LBP, l'expérience client = priorité IA n° 1 ; open source, local, frugalité mesurée | Le besoin est réel et c'est la priorité n° 1 de LBP |
| 3 | Notre démarche, en quatre temps | Yahya | Cadrer (9 situations ; Banking77 = service, pas conseil), Préparer (pas de traduction, 8 intentions, test français, `duration` exclue), Concevoir (cascade), Démontrer (tests, scénarios, comparaison « tout LLM », démo) | Une démarche rigoureuse, pas un chatbot branché sur un LLM |
| 4 | L'architecture : un aiguilleur | Yahya | Le schéma (page 1 de `schema-aiguilleur.pdf`) | Entrée commune sans LLM → aiguilleur → 3 niveaux → mémoire commune |
| 5 | Le plus petit moyen qui suffit, message par message | Yahya | Tableau des 3 niveaux, quand, comment, coût ; « la décision est prise à chaque message » ; « le vélo pour le pain, la voiture pour le week-end » | Le LLM n'est appelé qu'à un instant précis, pour un besoin précis |
| 6 | Démonstration en direct | Yahya pilote, Sohayb commente | Tableau des moments de la démo | Voir §14 |
| 7 | Choisir le LLM de chaque niveau | Yahya | Tableaux des niveaux 1 et 2 ; qwen3:1.7b retenu, un seul modèle ; le RAG d'exemples double sa justesse ; plus gros n'est pas plus fidèle | On a choisi en descendant en taille, sur mesures |
| 8 | Résultats : comprendre | Younes | Tableau §9.1 | 92,3 % sans traduire ; sous τ, jamais de devinette |
| 9 | Résultats : frugalité | Younes | Tableau A/B/C | 17× moins d'énergie, 5× moins de mémoire, p95 0,5 s, 76 % sans LLM |
| 10 | Explicabilité : pourquoi, et pourquoi pas | Sohayb | L'exemple de Léa chiffré | Le calcul se vérifie à la main, les règles sont nommées |
| 11 | Confiance et conformité | Sohayb | AI Act, mention légale, aucun accès au compte, LLM encadrés, local, inclusion | Prudence et conformité dès la conception |
| 12 | Limites et suite | Younes | Ce qui est simulé ; pour 17 000 bureaux | Honnêteté ; passage à l'échelle crédible |
| 13 | Merci | — | Phrase de conclusion | « Notre assistant comprend avec de simples mots-clés ou un modèle de 118 millions de paramètres, décide avec des règles que le client peut lire, et n'appelle un petit LLM qu'à un instant précis : pour comprendre un message flou, ou répondre en citant nos fiches. » |

**À mettre à jour si possible** : la diapositive 6 (démonstration) liste encore l'ancien déroulé
(Inès, Léa, Sophie/Lucas, Marc, Paul). La démo finale suit les **trois scénarios de la barre** (§14) :
Inès est identique dans ses 6 premiers messages ; Léa aussi ; le scénario Karim remplace
Sophie/Lucas/Marc/Paul. On peut soit mettre la diapositive à jour, soit la présenter comme « ce que
nous allons montrer » et suivre le scénario Inès. La diapositive mentionne aussi « coût de chaque
réponse » : l'interface affiche désormais l'énergie **et le CO₂** de chaque réponse.

**Autres documents** : `rapport/main-resume.pdf` (la proposition initiale, cascade),
`rapport/guide-solution.pdf` (guide du code), `rapport/schema-projet.pdf` (schéma global : données →
préparation → modèles → évaluation), `rapport/schema-aiguilleur.pdf` (5 pages : vue d'ensemble, niveaux
0, 1, 2, interface), `rapport/demo-secours.pdf`, `infos/choix-modeles-niveaux.md` (méthode des mesures).

---

## 16. Proposition de déroulé des 15 minutes

| Temps | Diapositives | Contenu |
|---|---|---|
| 0:00 – 1:30 | 1–2 | Le problème, la priorité n° 1 de LBP, les règles (open source, local, frugal) |
| 1:30 – 3:00 | 3 | La démarche ; les deux choix forts : ne pas traduire, créer 8 intentions pour le conseil |
| 3:00 – 5:00 | 4–5 | L'aiguilleur, les trois niveaux, les deux RAG, la grammaire JSON, la mémoire commune |
| 5:00 – 9:30 | 6 + interface | **Démo en direct** : scénario Inès (10 messages, ≈ 3 min), en vue démo ; montrer une pastille de niveau, un « + Pourquoi », une source ; basculer 20 s en vue utilisateur ; si le temps le permet, les messages 2–4 de Léa (conseil, « pourquoi ? ») |
| 9:30 – 11:00 | 7–9 | Choix des modèles, compréhension, frugalité (le chiffre « 17 fois moins ») |
| 11:00 – 13:30 | 10–11 | Explicabilité (Léa), confiance et conformité |
| 13:30 – 15:00 | 12–13 | Limites honnêtes, la suite, conclusion |

Si la démo est le cœur de la note « démonstration » (10 %), elle est aussi la meilleure preuve de la
pertinence métier (25 %) et de l'explicabilité (15 %) : montrer les **pastilles de niveau qui changent**
et un **« pourquoi ? »** expliqué.

---

## 17. Questions probables du jury, et réponses

**Pourquoi ne pas utiliser un LLM pour tout ?**
Parce que la plupart des messages n'en ont pas besoin : 76 % sont traités par des règles en quelques
millisecondes. Un 14B qui répond à tout consomme 17 fois plus, demande 5 fois plus de mémoire, est
4 fois plus lent au p95, et nous ne pouvons pas garantir qu'il n'invente pas un taux ou un plafond. Et
un LLM qui classe seul fait moins bien que notre classifieur (83 % contre 85 % en français pour le 14B,
29 % pour le petit).

**Où est le LLM, alors ? Le sujet demandait de l'IA générative.**
À deux endroits précis, choisis message par message par l'aiguilleur : pour **comprendre** un message
flou (niveau 1) et pour **rédiger** une réponse à une question ouverte à partir de nos fiches (niveau 2).
C'est l'idée « un modèle à un instant précis, pour un besoin précis » évoquée au kick-off.

**Comment l'aiguilleur décide-t-il ?**
Cinq signaux calculés sans LLM : plusieurs demandes, confiance sous τ, réponse libre illisible par les
règles, renvoi au contexte, question ouverte sur un sujet de nos fiches. Chaque réponse affiche le
niveau choisi et la raison.

**Pourquoi qwen3:1.7b ?**
On a testé cinq modèles de 0,8 à 6 Go sur deux bancs dédiés, en descendant en taille. C'est le plus petit
qui atteint le seuil au niveau 1 (30/36 avec le RAG d'exemples) et le seul à 22/22 au niveau 2. Un seul
modèle de 1,4 Go est chargé. ministral-3:3b fait 33/36 au niveau 1 pour deux fois la taille : c'est
l'alternative si on veut plus de marge.

**Comment empêchez-vous le LLM d'halluciner ?**
Au niveau 1 : il ne voit pas le profil, ne parle pas au client, sa sortie est contrainte par une
grammaire (énumération fermée d'intentions), et le code vérifie chaque valeur (un nombre doit être dans
le message). Au niveau 2 : il ne rédige qu'à partir de passages retrouvés au-dessus d'un seuil de
pertinence ; le garde-fou vérifie que **tous les chiffres** sont dans les extraits et que 80 % des mots
en viennent ; sinon on donne l'extrait de la fiche. Hors de nos fiches : « je n'ai pas cette
information ».

**Que veut dire « JSON imposé par une grammaire » ?**
Le serveur d'inférence (Ollama, vLLM) contraint le décodage : à chaque token, seuls ceux qui gardent le
JSON conforme au schéma sont autorisés. Le modèle ne peut pas produire un JSON invalide ou une intention
hors de la liste. Mesuré : 100 % de JSON valide, même pour un modèle de 1B.

**Pourquoi deux RAG ?**
Ils ne servent pas à la même chose. Au niveau 1, le RAG d'exemples donne au LLM les 8 phrases
d'entraînement les plus proches avec leur sujet : il classe par analogie (justesse doublée pour
qwen3:1.7b). Au niveau 2, le RAG de fiches donne les passages sourcés à partir desquels il rédige.

**Pourquoi ne pas avoir traduit Banking77 ?**
Traduire 10 000 phrases coûte (un LLM ou un service de traduction) et introduit des erreurs. L'encodeur
multilingual-e5 place une phrase anglaise et sa traduction française au même endroit : on entraîne en
anglais, on comprend le français (84,8 % sur 250 phrases françaises jamais vues). Nos 8 intentions, elles,
ont des phrases françaises écrites par l'équipe (672).

**Pourquoi une régression logistique et pas un réseau de neurones ou un fine-tuning ?**
Sur des vecteurs d'un bon encodeur, un classifieur linéaire atteint presque l'état de l'art (92,3 %
contre 93,7 % pour un BERT affiné), s'entraîne en 4 minutes sur CPU, pèse 141 Ko et donne des
probabilités utilisables pour le seuil τ. Un fine-tuning coûterait de l'énergie pour un gain non
démontré.

**Comment avez-vous fixé τ = 0,76 ?**
Par balayage sur un jeu de validation, pour viser 97 % de précision sur les messages acceptés
(obtenu : 97,1 %, avec 88,7 % de messages acceptés). Sous τ, on ne devine pas.

**Comment avez-vous mesuré l'énergie ?**
CodeCarbon hors ligne (France) sur DeepEirb, par lots de 200 messages répétés 3 fois après chauffe,
en mesurant aussi la puissance au repos (186,9 W) pour la soustraire. On donne les deux chiffres : brut
(11,5 contre 194 Wh pour 1 000 messages) et repos soustrait (5,5 contre 115). Le « 17 fois » est le
chiffre brut, le moins favorable.

**Et le CO₂ affiché par réponse ?**
C'est l'énergie mesurée par type de réponse (sans LLM, avec un appel) multipliée par l'intensité carbone
du réseau français que CodeCarbon utilise (56 g de CO₂e par kWh) : ≈ 10 µg sans LLM, ≈ 1,3 mg avec. C'est
une estimation : CodeCarbon ne mesure pas une requête de 20 ms en direct.

**Comment évaluez-vous la qualité du conseil ?**
Les décisions viennent de règles publiques (HCSF, plafonds légaux) que des tests vérifient (15 scénarios,
152 tests). Les montants se vérifient à la main. Pour la conversation, nous avons rejoué 60 conversations
libres et jugé chaque réponse.

**Ça marche sur des conversations imprévues ?**
Partiellement, et nous l'avons mesuré : sur 30 conversations jamais vues et volontairement difficiles
(SMS, anglais, deuil, fraude…), environ une réponse sur deux est juste. Les demandes claires et les
parcours guidés marchent bien ; la première cause d'échec est un hors-sujet pendant une question en
attente (l'assistant repose sa question). La correction est identifiée : mettre le parcours de côté
après une relance sans réponse.

**L'assistant peut-il faire opposition, un virement ?**
Non, par choix et conformément au périmètre du kick-off : il n'a aucun accès au compte. Il guide vers
l'espace bancaire sécurisé ou le conseiller, et ne demande jamais de code.

**Et le RGPD, les données ?**
Profils fictifs, traitement 100 % local, aucun appel externe, modèles open source : rien ne sort de la
machine. Le LLM du niveau 1 ne voit même pas le profil.

**Et l'AI Act ?**
La notation de crédit des personnes est à haut risque : nous n'en faisons pas. L'assistant estime sous
hypothèses et oriente ; un conseiller décide. Le client sait qu'il parle à une IA ; mention légale sur
tout crédit.

**Comment passer à l'échelle (17 000 bureaux) ?**
Le coût par requête est mesuré, donc extrapolable. Compréhension et règles tournent sur CPU ; le petit
LLM (1,4 Go) peut être servi par un serveur partagé (vLLM) ; 76 % des messages ne le sollicitent pas.

**Pourquoi des parcours en YAML ?**
Lisibles par un métier, modifiables sans toucher au code, déterministes, testables, sans LLM.

**Qu'avez-vous changé après les remarques des encadrants ?**
Trois choses : la grammaire JSON au niveau 1, les deux RAG, et surtout un aiguilleur qui peut changer de
niveau à chaque message (1 → 2 → 0 → 2), avec une mémoire commune.

**Pourquoi la reformulation par LLM n'est-elle pas utilisée ?**
Mesurée : plus d'énergie et un scénario perdu, sans gain visible. Les gabarits sont écrits par l'équipe,
avec la mention légale et les hypothèses hors LLM.

**Quelle est la part de l'IA dans le développement ?**
Le règlement autorise d'utiliser d'autres IA pour développer ; la solution, elle, ne fait appel qu'à des
modèles locaux open source.

**Que feriez-vous avec deux jours de plus ?**
Corriger la boucle de la question en attente ; accepter un bénéficiaire libre ; un parcours deuil ;
lire les nombres en lettres et le langage SMS ; enrichir les fiches ; mesurer sur un jeu de conversations
plus grand, relu par plusieurs personnes ; la voix et la réponse multilingue.

---

## 18. Aide-mémoire : les chiffres à retenir

| Quoi | Valeur |
|---|---|
| Messages sans aucun LLM (aiguilleur) | **76 %** (0 : 76 %, 1 : 12 %, 2 : 12 %) |
| Énergie, aiguilleur vs 14B qui fait tout | **11,5 vs 194 Wh / 1 000 messages (brut) → 17× moins** ; 5,5 vs 115 au repos soustrait |
| Niveau 0 seul | 0,40 Wh / 1 000 (brut) → près de **500× moins** que le 14B |
| Mémoire | **1,9 Go vs 9,1 Go** |
| Latence p95 | **0,53 s vs 2,3 s** ; niveau 0 seul : 19 ms |
| Modèle retenu | **qwen3:1.7b, 1,4 Go**, pour les deux niveaux |
| Niveau 1 | 30/36 avec RAG d'exemples (15/36 sans) ; JSON valide 100 % ; p50 188 ms |
| Niveau 2 | 22/22 justes ; garde-fou 9/18 rédactions acceptées ; bonne fiche 18/18 ; hors fiches refusé 4/4 ; p50 391 ms |
| Classifieur | e5-small 118 M paramètres ; **92,3 %** anglais (BERT affiné : 93,7 %) ; **84,8 %** français ; τ = 0,76 |
| Étage de compréhension | 76,4 % des messages français compris, **96,9 %** justes, 6 ms |
| Mots-clés | 19 % des messages, **100 %** justes |
| Données | 10 003 phrases Banking77 (anglais), 672 phrases de l'équipe, test français 250 |
| Taxonomie | 14 familles, 85 intentions (77 + 8) |
| Fiches du RAG | 37 (11 produits, 4 règles, 18 glossaire, 4 à la main) ; seuil cosinus 0,82 |
| Catalogue | 12 produits sourcés et datés |
| Tests | **152** tests, **15/15** scénarios |
| CO₂ par réponse | ≈ 10 µg (sans LLM) ; ≈ 1,3 mg (un appel) ; 56 g CO₂e/kWh (France, CodeCarbon) |
| Conversations libres jamais vues | ≈ **1 réponse juste sur 2** (30 conversations difficiles) |
| Léa | 250 000 € : 1 197 €/mois, **41,3 % > 35 %** ; 200 000 € : 933 €/mois, **32,2 %** |
| Karim | 12 000 € sur 48 mois : 282 €/mois, 22,7 % |
| Frais (Marc) | Commission d'intervention : 8 €/op., 80 €/mois (4 € et 20 € clientèle fragile) |
| Plafonds | Livret A 22 950 € ; LDDS 12 000 € ; Livret Jeune 1 600 € ; PEL 61 200 € |
| HCSF | Taux d'effort ≤ 35 % (assurance comprise), durée ≤ 25 ans |

---

## 19. Glossaire du projet

- **Aiguilleur** : le code qui, à chaque message, choisit le niveau (0, 1 ou 2) à partir de 5 signaux.
- **Niveau 0** : règles, automate, parcours YAML, conseiller, gabarits. Aucun LLM.
- **Niveau 1** : le petit LLM « interprète » qui comprend un message flou et rend un JSON ; il ne répond
  pas au client.
- **Niveau 2** : RAG sur nos fiches + rédaction citée par le LLM + garde-fou.
- **Parcours** : un fichier YAML qui décrit une conversation guidée (informations à recueillir, fin).
- **Slots** : les informations recueillies pendant la conversation (prix, apport, montant, durée…).
- **Mémoire commune** : l'état de la conversation partagé par les niveaux (parcours en cours, question
  en attente, demandes en file, parcours mis de côté, dernier conseil pour un « pourquoi ? »).
- **File des demandes** : plusieurs demandes dans un message, traitées par ordre d'urgence.
- **τ (tau)** : le seuil de confiance du classifieur (0,76) ; en dessous, on ne devine pas.
- **RAG d'exemples** : au niveau 1, les 8 phrases d'entraînement les plus proches données au LLM.
- **RAG de fiches** : au niveau 2, les passages des 37 fiches sourcées.
- **Garde-fou** : vérification par le code de la rédaction du LLM (chiffres, fidélité, citation,
  longueur) ; sinon, l'extrait de la fiche.
- **Repli** : la réponse sûre quand le LLM est écarté ou injoignable.
- **Banc** : un jeu de messages avec réponses attendues, pour mesurer et choisir.
- **A/B/C** : A = un 14B fait tout ; B = notre aiguilleur ; C = niveau 0 seul.
- **p50 / p95** : la latence en dessous de laquelle sont 50 % / 95 % des messages.
- **HCSF** : Haut Conseil de stabilité financière ; cadre du crédit immobilier (35 %, 25 ans).
- **M1 / M2 / M3** : les trois modules (comprendre et mesurer ; aiguilleur, converser, formuler,
  interface ; conseiller).
- **DeepEirb** : le serveur GPU de l'école, où sont faites les mesures officielles.
- **ail** : la machine de la salle (RTX 3060) où tourne la démo.
- **Timso AI** : projet antérieur de Yahya (assistant de rédaction RAG pour une agence de voyage) dont
  l'interface a repris le thème.

---

## 20. Fichiers et commandes utiles

**Dépôt** : `github.com/yahyabmo/hackathon-IA`, branche `main`.

| Fichier | Contenu |
|---|---|
| `src/assistant.py` | `reply()` : l'entrée commune, l'aiguillage, les niveaux, la mémoire |
| `src/aiguilleur.py` | Les 5 signaux, le choix du niveau, l'ordre d'urgence |
| `src/comprendre/` | Mots-clés, entités, classifieur, interprète (niveau 1) |
| `src/rag.py` | Niveau 2 : fiches, index, recherche, rédaction, garde-fou |
| `src/converser/` | Automate, parcours YAML, formulation, glossaire |
| `src/conseiller/` | Profils, catalogue, règles (M3) |
| `src/llm.py` | Ollama / vLLM, sortie contrainte, délais |
| `src/web/` | Interface (FastAPI + page), `scenarios.yaml` (les 3 scénarios de la démo) |
| `eval/` | Bancs, scénarios, conversations libres, résultats |
| `rapport/` | Support (`soutenance.pdf`), schémas, démo de secours, proposition |
| `infos/choix-modeles-niveaux.md` | Méthode et résultats du choix des modèles |
| `infos/synthese.md` | Synthèse du kick-off (règles, sujet, jury) |

```bash
# Lancer la démo
ASSISTANT_LLM=1 python -m src.web               # http://localhost:8000
#   ?scenario=1  ?client=C07&rejouer  ?utilisateur  ?demo

# Vérifier que tout marche
python -m pytest -q                             # 152 tests
python -m eval.run_scenarios                    # 15/15 scénarios

# Rejouer les conversations libres (rapport dans eval/resultats/)
ASSISTANT_LLM=1 python -m eval.rejouer_conversations
CONVERSATIONS_FICHIER=conversations_nouvelles.yaml CONVERSATIONS_SORTIE=conversations-nouvelles.md \
  ASSISTANT_LLM=1 python -m eval.rejouer_conversations

# Mesures (poste à GPU)
./mesurer.sh niveaux        # choix des modèles des niveaux 1 et 2
./mesurer.sh comprendre     # compréhension
./mesurer.sh abc qwen3:1.7b # énergie A/B/C
```

**Variables utiles** : `ASSISTANT_LLM=1` (niveaux 1 et 2), `OLLAMA_MODEL_NIVEAU1` /
`OLLAMA_MODEL_NIVEAU2` (changer de modèle), `ASSISTANT_REFORMULER=1` (reformulation, écartée),
`ASSISTANT_ESCALADE=1` (ancienne escalade vers le 14B, désactivée).
