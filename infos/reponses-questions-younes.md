# Réponses aux questions de Younes

Les chemins renvoient au code poussé sur `main`.

---

## L'essentiel

### 1. Comprendre : pourquoi `multilingual-e5-small` + régression logistique, et pas autre chose ?

- **Multilingue** : on ne traduit pas Banking77. Il faut un encodeur qui donne des vecteurs proches à une phrase anglaise et à son équivalent français. C'est ce qui permet d'entraîner sur l'anglais et de comprendre le français.
- **Petit** : 118 M de paramètres (~0,47 Go). Il répond en quelques millisecondes, même sur CPU. On connaît déjà la famille E5 (Timso AI), y compris son piège : le préfixe `query:`.
- **Régression logistique** : entraînée en quelques secondes sur CPU, elle pèse moins de 1 Mo. Elle donne des **probabilités** : on en a besoin pour le seuil τ et pour proposer deux familles quand on doute.
- **Assez bon** : dans l'article d'origine de Banking77, des encodeurs de phrases figés (USE, ConveRT) + un classifieur léger font 92,8 à 93,4 %, contre 93,7 % pour un BERT affiné, pour un coût bien plus faible. e5 est un encodeur de phrases du même type, plus récent ; à mesurer chez nous.
- **Ce n'est pas un dogme** : le banc (section 5) compare MiniLM, e5-base et un LLM qui classe seul. On garde le plus petit qui reste à moins d'1 point du meilleur.

### 2. Converser : c'est quoi ce YAML ?

Un fichier = **un parcours de conversation** pour une intention. Il décrit les informations nécessaires, d'où elles viennent (profil ou question), et ce qui se passe à la fin.

```yaml
# src/converser/parcours/credit_immobilier.yaml (extrait)
infos:
  revenus_nets: {type: montant, source: revenus_nets}     # lu dans le profil, confirmé
  prix_bien:    {type: montant, question: "Quel est le prix du bien ?"}
  apport:       {type: montant, question: "Quelle part de votre épargne ?"}
fin: {type: conseil, mention_legale: credit}
```

L'automate (`src/converser/dialogue.py`) lit ce fichier à chaque message :
1. il remplit ce qu'il peut, depuis le profil et depuis le message ;
2. il pose la première question qui manque ;
3. quand tout est rempli, il déclenche la fin : un conseil, une action ou un passage au conseiller.

Pourquoi un YAML : c'est lisible, on le modifie sans toucher au code, c'est déterministe, et ça n'utilise pas de LLM. Il y en a 9, un par situation du sujet.

### 3. Escalade : c'est quoi « le doute » ?

**Doute = la confiance du classifieur est sous le seuil τ.** La confiance, c'est la probabilité de la famille prédite. Dans ce cas :
1. **D'abord une question, sans LLM** : « Votre demande concerne-t-elle votre carte ou un virement ? » (les deux familles les plus probables).
2. **Si le doute reste, l'escalade** : appel au 14B pour classer la demande. Voir la question 13 : on propose de s'en passer.

---

## Sujet 1

### 4. Les informations retenues, et l'historique : où est-il stocké ? Faut-il l'enrichir ?

- **Le profil** est dans `data/processed/clients.json` : âge, métier, situation, revenus, épargne, crédits en cours, enfants, solde, cartes, bénéficiaires.
- **L'historique** est dans le même fichier : frais du mois (date, libellé, montant, cause), découverts sur 12 mois, contacts du jour. Bank Marketing n'en a pas, donc il est **simulé** et marqué `simule`. La version enrichie promise par les organisateurs se branchera dans `src/conseiller/clients.py`, sans toucher au reste.
- **À quoi il sert** :
  - expliquer les 8 € de Marc (frais du mois) ;
  - proposer l'offre clientèle fragile (au moins 3 découverts) ;
  - passer la main à Julie (3e contact du jour).
- **L'enrichir ?** Seulement quand une règle ou un parcours en a besoin. Un historique complet des opérations ne servirait à rien ici.
- **Les infos dites pendant la conversation** (prix, montant, horizon…) vivent dans `EtatConversation.slots`. Elles ne sont pas sauvegardées.

### 5. Les thèmes (carte…) : est-ce la même chose pour les actions et les réponses ?

Non, ce sont quatre niveaux différents, reliés entre eux :

| Niveau | Combien | Où |
|---|---|---|
| Familles / intentions (compréhension) | 14 / 85 | `src/taxonomie.py` |
| Parcours (conversation guidée) | 9 | `src/converser/parcours/*.yaml` |
| Outils (actions) | 5 | `src/conseiller/outils.py` |
| Réponses | gabarits par type de fin et par outil | `src/converser/formuler.py` |

Le chemin est : intention → parcours → fin (`conseil`, `action` avec un outil, `transmettre` ou `fiche`). Une intention sans parcours reçoit une fiche courte et une proposition de rappel.

### 6. La priorité « expérience client » : comment est-elle assurée ?

Concrètement :
- **une réponse immédiate** : quelques ms sans LLM ;
- **on ne redemande jamais** ce que le profil sait, et on pose une question à la fois ;
- **chaque conseil dit pourquoi, et pourquoi pas** ;
- **on agit** : l'opposition est faite en deux messages ;
- **mots simples**, jargon expliqué, empathie et passage de main pour un client mécontent ;
- **sécurité** : confirmation avant toute action, rappel « jamais de code ».

**Et c'est vérifié** : les scénarios (`eval/scenarios/`) testent le comportement attendu pour chaque situation des slides.

### 7. D'où vient « les mots-clés règlent environ 30 % » ?

De l'organisateur, dans l'audio 3, entre 1:12 et 1:20 : « ça permet déjà de trouver de quoi parle la personne dans, je ne sais pas, 30 % des cas ». **C'est son estimation, pas une mesure.** On mesurera notre propre part sur le test français.

---

## Banking77

### 8. Contient-il les 77 intentions dans lesquelles on classe la question du client ? Et la traduction ?

- **Oui** : 13 083 questions de clients **en anglais**, étiquetées par 77 intentions (10 003 pour l'entraînement, 3 080 pour le test). On classe dans ces 77, plus nos 8 nouvelles, soit 85.
- **On ne le traduit pas.** C'est une décision d'équipe, et tu as raison : ce qui compte, c'est le vecteur. L'encodeur multilingue donne des vecteurs proches à « I lost my card » et à « j'ai perdu ma carte ». Le classifieur entraîné sur les vecteurs anglais reconnaît donc les messages français.
- **Ce qui est en français** :
  - les mots-clés ;
  - les exemples des 8 nouvelles intentions ;
  - 5 phrases par famille ajoutées à l'entraînement ;
  - **un test de 250 phrases écrites à la main**, pour mesurer le passage anglais → français.

---

## La solution

### 9. Mots-clés : que veulent dire « il ne conclut que s'il est sûr » et « précision » ?

- **« Sûr »** = une règle précise (`src/comprendre/mots_cles.py`) :
  - **une seule** intention est touchée (les « bonjour » ne comptent pas s'il y a autre chose) ;
  - **et** la phrase fait au plus 12 mots, **ou** au moins 2 expressions sont trouvées.

  Sinon, le message passe au classifieur. Exemples :
  - « Je voudrais commander une nouvelle carte » : rien de conclu, « carte » seul n'est pas une expression ;
  - « J'ai perdu ma carte et je veux acheter un appartement » : deux intentions touchées, donc classifieur.
- **« Précision »** d'une expression = parmi les messages qui la contiennent, le pourcentage dont la vraie intention est bien celle qu'elle désigne. On la mesure sur nos phrases françaises étiquetées, hors jeu de test. Une expression sous 97 % est retirée du lexique (par exemple « envoyer », si elle apparaît trop souvent hors virement).

### 10. 14 familles puis 85 intentions : d'où viennent les familles, puisque Banking77 n'en a pas ?

**C'est nous qui les avons créées.**
- **Les 77 intentions de Banking77** sont rangées par sens en 9 familles : carte perdue, usage de la carte, commande de carte, frais et contestations, virements, compte et identité, espèces, change, alimentation du compte. Un script vérifie que chaque intention apparaît une seule fois.
- **5 familles de plus** accueillent nos 8 intentions : épargne, crédit, aide, insatisfaction, conversation. `faire_virement` va dans « virements ».
- **Le tout est dans `src/taxonomie.py`.**

**Pourquoi des familles** :
- la famille suffit à choisir le parcours ;
- elle résiste mieux aux erreurs d'étiquetage de Banking77 ;
- la question de clarification se pose par famille.

### 11. Le profil client est en YAML ? Pourquoi ?

**Non : les profils sont en JSON** (`data/processed/clients.json`), comme le catalogue et le glossaire. Le **YAML sert seulement aux parcours**, c'est-à-dire des règles de conversation écrites par nous. En résumé : JSON pour les données, YAML pour les parcours.

### 12. Règles publiques + appétence ? Agir utilise quoi ? Et sous le seuil, qui construit la question ?

- **Les règles publiques** sont dans `src/conseiller/regles.py`, avec leurs paramètres sourcés dans `catalogue.json` : taux d'effort ≤ 35 %, durée ≤ 25 ans (HCSF), plafonds des livrets, âges (Livret Jeune 12-25 ans, LDDS majeur). **Elles décident.**
- **L'appétence** est une régression logistique entraînée sur Bank Marketing : la colonne `y` dit si le client a souscrit un dépôt à terme. On n'utilise pas la colonne `duration` (c'est une fuite). Elle **ordonne** seulement les propositions d'épargne, elle ne décide rien. Elle n'est pas encore faite : c'est M3.
- **Agir** = 5 fonctions Python (`src/conseiller/outils.py`) sur un SI simulé : `bloquer_carte`, `preparer_virement`, `expliquer_frais`, `transmettre_conseiller` et `consulter_profil`. **Aucun LLM.** Tout outil qui modifie quelque chose exige un « oui ».
- **Sous le seuil, aucun LLM** : la question est un gabarit. Il est rempli avec les deux familles les plus probables données par le classifieur (« …votre carte ou un virement ? »). Sans candidats, l'assistant pose une question ouverte qui liste les thèmes.

### 13. Le 14B en escalade : pourquoi ne pas l'éviter, renvoyer vers le conseiller et journaliser pour améliorer le modèle ?

**D'accord, c'est mieux, et c'est déjà presque le comportement actuel.**
- **Par défaut (`ASSISTANT_LLM=0`), il n'y a pas d'escalade** : après une question restée sans effet, l'assistant propose un rappel par un conseiller.
- **À ajouter** : un journal des messages non compris (`eval/incompris.jsonl`). On le relit pour enrichir le lexique et les phrases d'entraînement : c'est une boucle d'amélioration, comme dans Timso AI.
- **Proposition** : l'escalade reste une **option**, et on mesure ce qu'elle apporte (combien de cas récupérés, et pour quel coût). Si elle n'apporte presque rien, on le dit au jury, et c'est un argument de frugalité de plus.

---

## 5. Évaluer et mesurer

### 14. Pourquoi TF-IDF ? Pourquoi MiniLM ? Pourquoi passer par la sémantique ?

- **TF-IDF + régression logistique** = la **base sans réseau de neurones** : quelques Mo, moins d'une milliseconde. Elle sert de point de comparaison : si elle fait aussi bien qu'e5, on la garde (le plus petit qui suffit). Sinon, on a la preuve chiffrée que l'encodeur apporte quelque chose. Elle compare des **mots** : entraînée sur l'anglais, elle ne devrait presque rien comprendre au français. **Ce résultat est en lui-même l'argument** pour l'encodeur multilingue.
- **MiniLM** (`paraphrase-multilingual-MiniLM-L12-v2`) = un autre encodeur multilingue **de la même taille** qu'e5-small (118 M). On compare deux candidats équivalents et on garde le meilleur.
- **La sémantique** : un client dit la même chose de mille façons (« j'ai paumé ma CB », « plus de carte depuis hier »). Les vecteurs capturent le sens au-delà des mots exacts. C'est aussi **la seule façon d'utiliser Banking77 en anglais pour des messages français sans le traduire**. Les mots-clés couvrent les formulations évidentes et fréquentes ; la sémantique couvre le reste.
