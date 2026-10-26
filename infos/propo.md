a partir les données que t'as (presentation, data..), (on peut utiliser d autre data..), comment tu pense au workflow qu on peut faire pour avoir un MVP qui marche, ainsi comment on peut deviser les taches avec mon equipe de 3

Oui. À partir des slides et des données disponibles, je proposerais un MVP centré sur :

> Un assistant bancaire local qui comprend une demande en français, pose les questions manquantes, consulte un profil client et propose une orientation explicable.

Il ne faut pas chercher à couvrir les 77 intentions de Banking77. Il faut construire 3 ou 4 parcours parfaitement fonctionnels.

## 1. Périmètre fonctionnel du MVP

Je recommande ces parcours :

1. Carte perdue ou volée
   Facile à démontrer et couvert par Banking77.
2. Frais ou paiement contesté
   Également couvert par Banking77.
3. Projet d’épargne
   Basé sur les exemples du sujet, avec questions sur l’objectif, la durée et le montant.
4. Projet de crédit
   Avec revenus, charges, apport et montant souhaité.

Pour chaque parcours, l’assistant doit :

message client
→ intention
→ données manquantes
→ questions complémentaires
→ profil client
→ règles métier
→ recommandation
→ explication

## 2. Architecture simple et frugale

Interface Streamlit
        ↓
Gestionnaire de conversation
        ↓
Classification d’intention
        ↓
Extraction des informations
        ↓
Profil client + catalogue produits
        ↓
Moteur de règles
        ↓
Réponse générée par template ou petit LLM

Le LLM ne doit pas prendre seul la décision. Il peut :

- comprendre une formulation libre ;
- extraire des informations ;
- reformuler la réponse.

La recommandation doit venir de règles explicables.

## 3. Utilisation des données

### Banking77

Utilisation :

- comprendre les intentions bancaires ;
- récupérer des exemples de formulations ;
- créer ou tester le classifieur.

Comme les phrases sont en anglais, vous pouvez traduire uniquement les catégories utiles et créer quelques exemples français.

### Bank Marketing

Utilisation :

- créer des profils clients réalistes ;
- exploiter âge, métier, solde, prêts, situation familiale, etc. ;
- éventuellement entraîner un petit modèle de propension à l’épargne.

### Données synthétiques à ajouter

Créer un fichier local data/processed/customers.csv avec :

customer_id
age
job
monthly_income
monthly_expenses
balance
savings
housing_loan
personal_loan
family_status
children
risk_profile
financial_goal

Créer aussi un catalogue :

product_id
name
type
eligibility_rules
advantages
limits

Il vaut mieux générer ces données vous-mêmes plutôt que chercher beaucoup d’autres datasets. Cela permet de garder le contrôle et de respecter le scénario du sujet.

## 4. Répartition dans l’équipe

### Personne 1 — Données et métier

Responsabilités :

- sélectionner les intentions ;
- préparer les exemples français ;
- créer les profils clients synthétiques ;
- créer le catalogue de produits ;
- définir les règles de recommandation ;
- préparer les cas de démonstration.

Livrables :

data/processed/customers.csv
data/processed/products.json
data/processed/intents.json
src/rules.py

### Personne 2 — IA et backend

Responsabilités :

- créer le client Ollama ou llama.cpp ;
- classifier les intentions ;
- extraire les informations dans un format structuré ;
- gérer l’état de la conversation ;
- connecter les règles et le LLM ;
- ajouter un mode sans LLM en cas de problème.

Format de sortie recommandé :

{
  "intent": "credit",
  "slots": {
    "monthly_income": 2500,
    "monthly_expenses": 900,
    "down_payment": 20000,
    "amount": 180000
  },
  "missing_slots": ["duration"]
}

### Personne 3 — Interface, intégration et mesures

Responsabilités :

- construire l’interface Streamlit ;
- afficher l’historique de conversation ;
- afficher le profil client sélectionné ;
- montrer les règles utilisées ;
- ajouter les mesures de latence et consommation ;
- préparer la démonstration et les slides.

Livrables :

app.py
src/metrics.py
demo/scenarios.json

## 5. Contrat commun entre les membres

Pour éviter les problèmes d’intégration, définissez dès le début une fonction centrale :

answer = assistant.reply(
    message="Je veux acheter un appartement",
    customer_id="CUST_001",
    conversation_state={}
)

Elle doit retourner :

{
    "message": "...",
    "intent": "credit",
    "missing_information": ["revenus", "apport"],
    "recommendation": None,
    "explanation": "...",
    "latency_ms": 120
}

Tout le monde développe autour de ce format.

## 6. Planning pratique

### Première phase : cadrage

- choisir les 4 intentions ;
- définir 3 profils clients ;
- définir 5 à 8 règles métier ;
- figer le format JSON ;
- préparer un scénario de démo.

### Deuxième phase : construction parallèle

- données et règles ;
- backend et extraction ;
- interface et métriques.

### Troisième phase : intégration

Tester trois parcours complets :

client jeune → crédit automobile
parent → épargne pour enfants
client âgé → problème de virement ou de carte

### Dernière phase : fiabilisation

- tester les formulations imprévues ;
- ajouter un fallback ;
- mesurer la latence et la consommation ;
- préparer une vidéo de secours ;
- répéter la démonstration.

## 7. Ce qu’il faut montrer au jury

La démonstration doit prouver quatre choses :

1. l’assistant comprend une demande naturelle ;
2. il pose des questions pertinentes ;
3. sa recommandation dépend réellement du profil ;
4. son comportement est frugal et explicable.

Le message fort pourrait être :

> « Notre solution utilise un petit modèle local pour comprendre le client, mais la recommandation est calculée par des règles transparentes. Le LLM n’est jamais utilisé pour inventer une décision financière. »

La priorité absolue est d’avoir un seul parcours complet qui fonctionne parfaitement, puis d’en ajouter deux autres si le temps le permet.