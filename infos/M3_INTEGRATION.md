# M3 livré le 27 octobre 2026

## Contrats et flux

Les signatures publiques restent inchangées :

```python
clients.profil(client_id) -> dict
conseiller(intention, profil, slots) -> Conseil
outils.executer(action, profil, etat) -> Action
reply(message, client_id, etat=None) -> tuple[Reponse, EtatConversation]
```

Le profil contient les informations connues du personnage ; les slots sont les
déclarations relatives à son projet (prix, apport, horizon, mensualité souhaitée).
Les montants sont en euros, les taux API en ratios (`0.0332`), les durées selon
le suffixe du champ. Les questions complémentaires de taux attendent un pourcentage.

`Conseil.propositions` contient raisons, sources et scores heuristiques, jamais
des probabilités. `ecartees` contient une raison et un identifiant de règle.
`manque` désigne les informations indispensables absentes **ou invalides** :
aucune mensualité n'est alors calculée. `faits` contient calculs, hypothèses,
sources, assurance connue/inconnue et `decision_bancaire=False` pour les crédits.
En épargne, les informations fiscales facultatives sont dans `a_verifier` :
elles bloquent le produit concerné, pas les autres pistes disponibles.

Quatre parcours métier : immobilier, consommation, épargne, prêt étudiant.
Ils fonctionnent sans LLM et sans entraînement. Bank Marketing n'est pas un
moteur de recommandation ; aucun modèle d'appétence n'a été ajouté.

## Actions et état

Les cinq outils restent disponibles. Toute action sensible exige strictement
`action.confirmee is True`. Sinon, `resultat.statut=en_attente` et l'exception
publique `ConfirmationRequise` est levée. Une confirmation textuelle ambiguë
reste en attente dans `reply` ; un montant corrigé exige un nouvel accord.

Les virements utilisent `Decimal`, acceptent deux décimales maximum, refusent
les montants non positifs/non finis, les bénéficiaires inconnus ou ambigus et
le solde insuffisant. Les effets sont appliqués sur une copie, publiée uniquement
après réussite. Aucun appel bancaire externe, aucun véritable rendez-vous.

`Action.identifiant` est ajouté avec une valeur par défaut UUID. Le rejeu de cet
identifiant renvoie le résultat enregistré sans répéter l'effet ; sa réutilisation
avec d'autres paramètres est refusée. Une nouvelle action explicitement demandée
et confirmée est une nouvelle opération, même si son montant est identique.

Nouveaux champs à valeurs par défaut dans `EtatConversation` :

- `client_id`, `profil_simule` : copie indépendante conservée entre les tours ;
- `operations` : demandes et résultats indexés par identifiant ;
- `journal_actions` : opérations traitées, horodatage UTC, paramètres, confirmation,
  résultat `succes`, `refus` ou `echec` ;
- `question_m3` : reprise de collecte après un `Conseil.manque`.

L'état est en mémoire, propre à la conversation. Changer de client réinitialise
l'état ; une nouvelle conversation ou un redémarrage perd les simulations.
Ce n'est pas une base bancaire ni un mécanisme de transactions concurrentes.
Le cache des profils et du catalogue n'est jamais modifié par leurs accesseurs.

## Données et sources

Les huit personnages C01–C08 sont fictifs. `provenance` documente chaque champ :
scénario CGI ou simulation. Les ancrages Bank Marketing donnent fichier, ligne
physique (en-tête = 1), valeurs comparées et SHA256. Ce sont des rapprochements
documentaires vérifiables, **pas l'identité des clients ni l'origine de leurs
finances**. Le solde annuel moyen Bank Marketing n'est jamais un solde disponible.
Les données brutes sont inchangées. Le test des ancrages est ignoré si elles
ne sont pas présentes dans un autre checkout.

Le catalogue hors ligne conserve 12 produits. Sources, dates, unités, statut
de vérification et nature accompagnent ses fiches et paramètres :

- Service-Public : plafonds et conditions de l'épargne, PTZ et prêt personnel ;
- HCSF : cadre général immobilier, distinct d'une décision d'octroi ;
- Banque de France, août 2026 : repères statistiques de taux, pas offres LBP ;
- Notaires : fourchettes de frais d'acquisition, dont le milieu est une hypothèse ;
- La Banque Postale : conditions commerciales du prêt étudiant ;
- Trésor : plafonds de commissions d'intervention, pas de tous les frais bancaires.

Les liens exacts figurent dans `data/processed/catalogue.json`. La date de relevé
est le 27 octobre 2026. Les taux d'épargne non nécessaires n'ont pas été inventés.
Le seuil consommation et le signal de fragilité sont des heuristiques internes.
La table LEP est limitée aux quotités renseignées en métropole pour 2026 ; toute
autre situation reste à vérifier. Le revenu mensuel ne remplace jamais le RFR.

Éligibilité = conditions connues d'un produit ; pertinence = adéquation au projet ;
estimation = calcul sous hypothèses ; octroi = décision humaine de la banque.
Le prototype n'accomplit que les trois premières opérations, conditionnellement.
Assurance inconnue, frais non couverts et exceptions HCSF sont signalés.

## Coordination avec Yahya et Younes

Seuls `src/assistant.py` et `src/contrats.py` sont modifiés côté socle partagé.
Les modules `src/comprendre/`, `src/converser/`, les YAML et `app.py` restent intacts.

Dans `assistant.py` : profil de session, confirmations strictes, reprise sur
`Conseil.manque`, refus d'action explicite, gabarit général pour les conseils
M3 et ajout des hypothèses hors reformulation LLM. Le gabarit immobilier historique
présumait un financement sans assurance ; il n'est plus utilisé par `reply`.
La mention légale crédit reste en dernière position.

Points précis à reprendre ensemble :

- **M1** : l'extracteur actuel perd le signe négatif et interprète mal certains
  points décimaux. Une barrière M3 refuse ces messages et demande la virgule.
  Le parseur M1 n'a pas été modifié ; les montants en lettres restent hors MVP.
- **M2** : le panneau Profil recharge toujours le profil initial. Utiliser
  `etat.profil_simule` pour afficher ensuite les soldes/statuts simulés.
- **M2** : le panneau Action appelle actuellement tout résultat « exécutée ».
  Afficher `action.resultat['statut']` pour distinguer les refus/échecs ; le texte
  conversationnel les distingue déjà. Afficher les hypothèses et
  `faits['sources_produits']` si l'on veut compléter le panneau Pourquoi.
- **M2** : le banc autonome de formulation appelle encore les anciens gabarits
  directement ; ses évaluations LLM ne valent pas validation du nouveau flux M3.

Les anciens scénarios ont changé pour des raisons métier explicites : taux
statistique de Léa, LDDS non proposé à Lucas rattaché fiscalement dans la simulation,
fiscalité des enfants de Sophie inconnue au lieu d'une inéligibilité inventée.

## Validation et démonstration

```bash
ASSISTANT_LLM=0 .venv/bin/python -m pytest -q
ASSISTANT_LLM=0 ASSISTANT_ESCALADE=0 .venv/bin/python -m eval.run_scenarios
ASSISTANT_LLM=0 ASSISTANT_ESCALADE=0 .venv/bin/streamlit run app.py
```

Démo : Paul, virement de 500 €, « oui mais pas maintenant », correction « non,
plutôt 12,50 euros », « oui ». Puis Léa et son appartement ; Sophie et Lucas pour
montrer des conseils différents. Les tests d'intégration vérifient la persistance,
l'absence de double débit, la confirmation et l'isolation des clients.

Limites assumées : pas d'octroi, de TAEG complet, de catalogue commercial exhaustif,
de vérification des justificatifs, ni de garantie réglementaire sur les cas non
modélisés. Le PTZ reste une fiche d'orientation. Actualiser les références datées
avant toute réutilisation après le hackathon.
