# Conversations libres : 30 conversations rejouées (conversations_libres.yaml)

Généré le 28/10/2026 à 11 h 24 sur ail, niveaux 1 et 2 actifs (qwen3:1.7b / qwen3:1.7b).

## Résumé

- 300 messages, dans 30 conversations.
- Niveaux : 0 : 189 · 1 : 71 · 2 : 40.
- Appels au LLM : 122. Latence p50 10.2 ms, p95 564 ms.
- Signaux à regarder : repli du garde-fou : 20, hors de nos fiches : 4, incompris : 4, clarification : 2, « Bonjour ! » : 1.

## 1. C01 — carte perdue puis virement, avec fautes

**1. Client** : bonjour j'ai perdu ma cb hier soir

> Je comprends, il faut agir vite. Faites opposition tout de suite : dans votre espace bancaire sécurisé, rubrique Opposition, ou en appelant votre conseiller. Je ne peux pas bloquer votre carte depuis cette conversation. Rappel : la banque ne vous demandera jamais votre code confidentiel.

<sub>niveau 0 · lost_or_stolen_card (mots_cles, 0.9) · 0.2 ms — demande claire (mots_cles)</sub>

**2. Client** : jai deja fais opposition c bon ?

> opposition : Le blocage définitif d'une carte perdue ou volée, pour que personne ne puisse s'en servir.

<sub>niveau 1 · question_definition (interprete, 0.0) · 224.8 ms · 1 LLM — confiance sous le seuil → compris</sub>

**3. Client** : et du coup je voudrais faire un virement

> D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · faire_virement (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**4. Client** : a ma soeur

> Quel montant voulez-vous envoyer ?

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**5. Client** : 300 euros

> Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation.

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**6. Client** : elle va le recevoir quand ?

> D'après nos fiches : Livret Jeune : De 12 à 25 ans. Plafond des versements : 1 600 €. De 12 à 25 ans. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · question_definition (interprete, 0.0) · 434.2 ms · 2 LLM — confiance sous le seuil → compris ; aucun terme du glossaire : nos fiches — ⚠ repli du garde-fou — sources : Livret Jeune, Livret Jeune, Prêt étudiant</sub>

**7. Client** : et si je me suis trompé de montant ?

> Si vous vous êtes trompé de montant, adressez une réclamation à votre conseiller puis au service réclamations [1]. Si la réponse ne vous convient pas, ou si vous n’avez pas reçu de réponse, saisissez gratuitement le médiateur bancaire.

<sub>niveau 2 · question_definition (interprete, 0.0) · 704.6 ms · 2 LLM — confiance sous le seuil → compris ; aucun terme du glossaire : nos fiches — sources : Faire une réclamation, Livret d'épargne populaire (LEP), Commission d'intervention</sub>

**8. Client** : ok merci

> Avec plaisir ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**9. Client** : au fait comment je commande une nouvelle carte

> Je comprends que votre demande concerne la commande d'une carte. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 1 · order_physical_card (interprete, 0.0) · 293.0 ms · 1 LLM — confiance sous le seuil → compris</sub>

**10. Client** : merci bcp

> Avec plaisir ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 2. C01 — vol de carte, peur de la fraude, rendez-vous

**1. Client** : on m'a volé mon portefeuille avec ma carte dedans

> Je comprends, il faut agir vite. Faites opposition tout de suite : dans votre espace bancaire sécurisé, rubrique Opposition, ou en appelant votre conseiller. Je ne peux pas bloquer votre carte depuis cette conversation. Rappel : la banque ne vous demandera jamais votre code confidentiel.

<sub>niveau 0 · lost_or_stolen_card (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**2. Client** : y a des achats que j'ai pas fait

> Je comprends que votre demande concerne des frais ou une opération contestée. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · card_payment_not_recognised (classifieur, 0.78) · 10.9 ms — demande claire (classifieur)</sub>

**3. Client** : est-ce que je vais être remboursée ?

> Je comprends que votre demande concerne des frais ou une opération contestée. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · top_up_by_bank_transfer_charge (classifieur, 0.95) · 10.9 ms — demande claire (classifieur)</sub>

**4. Client** : je veux parler à un conseiller

> Je ne peux pas prendre de rendez-vous pour vous : je n'ai aucun accès à votre compte. Pour voir un conseiller, prenez rendez-vous depuis votre espace bancaire sécurisé, rubrique Rendez-vous, ou appelez votre agence. Préparez votre projet : montant, durée, revenus.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**5. Client** : c'est urgent

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 230.0 ms · 1 LLM — confiance sous le seuil → compris</sub>

**6. Client** : et pour mon téléphone volé aussi ?

> Je comprends, il faut agir vite. Faites opposition tout de suite : dans votre espace bancaire sécurisé, rubrique Opposition, ou en appelant votre conseiller. Je ne peux pas bloquer votre carte depuis cette conversation. Rappel : la banque ne vous demandera jamais votre code confidentiel.

<sub>niveau 1 · lost_or_stolen_card (interprete, 0.0) · 259.5 ms · 1 LLM — confiance sous le seuil ; renvoi au contexte → compris</sub>

**7. Client** : mon appli bancaire était dessus

> Faites opposition tout de suite : dans votre espace bancaire sécurisé, rubrique Opposition, ou en appelant votre conseiller. Je ne peux pas bloquer votre carte depuis cette conversation. Rappel : la banque ne vous demandera jamais votre code confidentiel.

<sub>niveau 1 · lost_or_stolen_card (interprete, 0.0) · 271.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**8. Client** : comment je bloque l'accès ?

> Je comprends que votre demande concerne l'utilisation de votre carte. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 1 · card_not_working (interprete, 0.0) · 245.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**9. Client** : ok

> D'accord. Puis-je vous aider pour autre chose ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 211.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**10. Client** : au revoir

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 3. C02 — frais, offre clientèle fragile, réclamation

**1. Client** : pourquoi j'ai payé 8 € de frais ce mois-ci ?

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 0 · extra_charge_on_statement (mots_cles, 0.9) · 0.2 ms — demande claire (mots_cles)</sub>

**2. Client** : c'est quoi une commission d'intervention

> Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais. ⏎ Passons maintenant à votre autre demande : une explication. Je n'ai pas cette information dans mes fiches. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · extra_charge_on_statement (mots_cles, 0.9) · 0.5 ms — plusieurs demandes nettes : traitées par ordre d'urgence — ⚠ hors de nos fiches</sub>

**3. Client** : j'en ai eu plusieurs ce mois ci

> Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 258.7 ms · 1 LLM — confiance sous le seuil → compris</sub>

**4. Client** : c'est pas normal

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 0 · insatisfaction (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**5. Client** : j'ai droit à l'offre clientèle fragile ?

> D'après nos fiches : Offre clientèle fragile : Situation de fragilité financière ; frais d'incidents plafonnés. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · credit_conso (classifieur, 0.76) · 625.4 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Offre clientèle fragile, Commission d'intervention, Emprunter pour un logement : durée maximale et taux d'effort (HCSF)</sub>

**6. Client** : comment je conteste ces frais ?

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 0 · extra_charge_on_statement (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**7. Client** : je veux faire une réclamation

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 0 · insatisfaction (classifieur, 0.89) · 10.4 ms — demande claire (classifieur)</sub>

**8. Client** : et si la banque répond pas ?

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 299.4 ms · 1 LLM — confiance sous le seuil → compris</sub>

**9. Client** : c'est qui le médiateur

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 226.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**10. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 4. C02 — découvert et jargon

**1. Client** : c'est quoi un découvert autorisé

> découvert autorisé : La possibilité, prévue avec votre banque, d'avoir un solde négatif jusqu'à un certain montant. Il coûte des agios.

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 0.5 ms — demande claire (mots_cles)</sub>

**2. Client** : et les agios c'est quoi

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais. ⏎ Passons maintenant à votre autre demande : une explication. Je n'ai pas cette information dans mes fiches. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · extra_charge_on_statement (mots_cles, 0.9) · 0.6 ms — plusieurs demandes nettes : traitées par ordre d'urgence — ⚠ hors de nos fiches</sub>

**3. Client** : j'ai un découvert de 200 € ça me coûte combien ?

> Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 0 · extra_charge_on_statement (reponse_attendue, 1.0) · 11.4 ms — demande claire (reponse_attendue)</sub>

**4. Client** : comment je peux éviter ça

> Pour bien vous aider, pouvez-vous préciser ? Par exemple : votre carte, un virement, des frais, votre épargne ou un projet de crédit.

<sub>niveau 1 · inconnue (aucun, 0.0) · 192.3 ms · 1 LLM — confiance sous le seuil → rien de net — ⚠ clarification</sub>

**5. Client** : je voudrais mettre un peu de côté pour pas être à découvert

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · epargne_projet (classifieur, 0.97) · 10.2 ms — demande claire (classifieur)</sub>

**6. Client** : dans 1 an

> Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**7. Client** : 50 euros par mois

> Voici ce que je vous propose. Livret A : épargne disponible ; adaptée à une réserve ou un projet sans immobilisation. Livret de développement durable et solidaire (LDDS) : domicile fiscal français et imposition séparée déclarés ; épargne disponible. ⏎ Non proposé — Livret Jeune : hors de la tranche d'âge du Livret Jeune. Non proposé — Plan épargne logement (PEL) : besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. Livret d'épargne populaire (LEP) : éligibilité à vérifier (revenu fiscal de référence, nombre de parts fiscales, année du revenu fiscal, territoire fiscal), aucune inéligibilité déduite. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.3 ms — réponse attendue, lue par les règles</sub>

**8. Client** : pourquoi ?

> [Votre simulation : Livret Jeune n'est pas proposé : Hors de la tranche d'âge du Livret Jeune.]  
[Votre simulation : Plan épargne logement (PEL) n'est pas proposé : Besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages.]  
[Votre simulation : Livret A : Épargne disponible ; adaptée à une réserve ou un projet sans immobilisation.]   ⏎ Le problème est lié à votre âge ou à votre horizon de dépenses. Si vous souhaitez une simulation plus adaptée, je peux vous proposer un conseiller.

<sub>niveau 2 · inconnue (aucun, 0.0) · 808.7 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**9. Client** : c'est quoi le LDDS

> LDDS : Un livret d'épargne disponible, sans impôt sur les intérêts, plafonné à 12 000 €, réservé aux majeurs.

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 0.3 ms — demande claire (mots_cles)</sub>

**10. Client** : ok super

> D'accord. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (classifieur, 0.8) · 9.4 ms — demande claire (classifieur)</sub>

## 5. C03 — épargne pour les enfants, comparaison de livrets

**1. Client** : je voudrais mettre de côté pour mes enfants

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · epargne_projet (mots_cles, 0.9) · 0.2 ms — demande claire (mots_cles)</sub>

**2. Client** : dans 10 ans

> Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**3. Client** : 100 euros par mois

> Voici ce que je vous propose. Livret A : piste au nom de chaque enfant ; vérifier l'absence de Livret A déjà détenu et les représentants légaux. Livret Jeune : piste pour l'enfant de 12 à 25 ans, sous réserve de résidence en France et d'absence de livret identique. Les versements prévus dépassent la place disponible de 1 600 € ; prévoir une répartition. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. Livret de développement durable et solidaire (LDDS) : éligibilité à vérifier (situation fiscale des enfants), aucune inéligibilité déduite. Livret d'épargne populaire (LEP) : éligibilité à vérifier (situation fiscale des enfants, revenu fiscal des enfants), aucune inéligibilité déduite. Les soldes et la situation fiscale des enfants ne sont pas connus ; ne pas utiliser ceux du parent. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**4. Client** : pourquoi pas le LDDS ?

> Le LDDS est adapté pour les personnes éligibles, avec un plafond des versements de 12 000 €. [2] Il est disponible sans impôt sur les intérêts, mais se limite à 12 000 €. [3] Il faut vérifier l'éligibilité en fonction de la situation fiscale des enfants. Si vous avez des enfants, il faut vérifier si vous êtes éligible.

<sub>niveau 2 · inconnue (aucun, 0.0) · 729.1 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Livret de développement durable et solidaire (LDDS), LDDS, Votre simulation</sub>

**5. Client** : quelle est la différence entre le livret A et le LDDS

> Le livret A est ouvert à tous, y compris les mineurs, et a un plafond des versements de 22 950 €. [2] Le LDDS est destiné aux majeurs, avec un plafond des versements de 12 000 € et un domicile fiscal en France.

<sub>niveau 2 · inconnue (aucun, 0.0) · 534.3 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Livret de développement durable et solidaire (LDDS), LDDS, Livret A</sub>

**6. Client** : et le livret jeune c'est à partir de quel âge

> D'après nos fiches : Livret Jeune : De 12 à 25 ans. Plafond des versements : 1 600 €. De 12 à 25 ans. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 172.7 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Livret Jeune, Livret Jeune, Prêt étudiant</sub>

**7. Client** : mon grand a 12 ans

> Voici ce que je vous propose. Livret A : piste au nom de chaque enfant ; vérifier l'absence de Livret A déjà détenu et les représentants légaux. Livret Jeune : piste pour l'enfant de 12 à 25 ans, sous réserve de résidence en France et d'absence de livret identique. Les versements prévus dépassent la place disponible de 1 600 € ; prévoir une répartition. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. Livret de développement durable et solidaire (LDDS) : éligibilité à vérifier (situation fiscale des enfants), aucune inéligibilité déduite. Livret d'épargne populaire (LEP) : éligibilité à vérifier (situation fiscale des enfants, revenu fiscal des enfants), aucune inéligibilité déduite. Les soldes et la situation fiscale des enfants ne sont pas connus ; ne pas utiliser ceux du parent. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 12.0 ms — demande claire (reponse_attendue)</sub>

**8. Client** : et le PEL ?

> PEL : Plan épargne logement : on verse régulièrement pendant plusieurs années, en vue d'un projet immobilier ; un retrait ferme le plan.

<sub>niveau 1 · question_definition (interprete, 0.0) · 253.5 ms · 1 LLM — confiance sous le seuil ; renvoi au contexte → compris (réponse écartée : absente du message)</sub>

**9. Client** : je peux retirer de l'argent d'un PEL avant 4 ans ?

> D'après nos fiches : Plan épargne logement (PEL) : Un plan par personne. Retrait anticipé entraînant clôture et conséquences selon ancienneté ; les fonds ne sont pas définitivement bloqués. Plafond des versements : 61 200 €. Durée minimale : 4 ans. Versement initial minimum : 225 € ; versements annuels minimum : 540 €. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · epargne_projet (classifieur, 0.92) · 563.9 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Plan épargne logement (PEL), PEL, Livret d'épargne populaire (LEP)</sub>

**10. Client** : merci beaucoup

> Avec plaisir ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 6. C03 — épargne puis projet immobilier

**1. Client** : je veux épargner

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · epargne_projet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**2. Client** : pour moi

> Je n'ai pas bien compris. Dans combien de temps pensez-vous avoir besoin de cet argent ? Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 211.5 ms · 1 LLM — réponse libre, illisible par les règles → rien de net — ⚠ incompris</sub>

**3. Client** : je sais pas trop, quelques années

> Je pars sur un an ; vous pourrez ajuster. Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**4. Client** : 200 € par mois

> Voici ce que je vous propose. Livret A : alimenter le livret existant, sans en ouvrir un second. Épargne disponible ; adaptée à une réserve ou un projet sans immobilisation. Livret de développement durable et solidaire (LDDS) : domicile fiscal français et imposition séparée déclarés ; épargne disponible. ⏎ Non proposé — Livret Jeune : hors de la tranche d'âge du Livret Jeune. Non proposé — Plan épargne logement (PEL) : besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. Livret d'épargne populaire (LEP) : éligibilité à vérifier (revenu fiscal de référence, nombre de parts fiscales, année du revenu fiscal, territoire fiscal), aucune inéligibilité déduite. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.3 ms — réponse attendue, lue par les règles</sub>

**5. Client** : en fait on pense acheter une maison

> C'est un beau projet. J'ai noté vos revenus de 2 400 € nets par mois. Quel est le prix du bien que vous visez, et quelle part de vos 6 000 € d'épargne souhaitez-vous y consacrer ?

<sub>niveau 0 · credit_immobilier (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**6. Client** : 300000

> Quelle part de vos 6 000 € d'épargne souhaitez-vous consacrer à l'achat ?

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**7. Client** : on a 40000 d'apport

> Non proposé — Crédit immobilier : mensualité indicative de 1 387 € sur 300 mois, soit 57,8 % des revenus avec les crédits en cours. Projet non retenu dans cette simulation ; aucun refus bancaire n'est prononcé. Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Taux d'effort indicatif de 57,8 % : au-delà du repère de 35 %. Budget indicatif sous ces hypothèses : environ 196 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**8. Client** : et avec 250000 ?

> Non proposé — Crédit immobilier : mensualité indicative de 1 123 € sur 300 mois, soit 46,8 % des revenus avec les crédits en cours. Projet non retenu dans cette simulation ; aucun refus bancaire n'est prononcé. Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Taux d'effort indicatif de 46,8 % : au-delà du repère de 35 %. Budget indicatif sous ces hypothèses : environ 196 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 10.6 ms — demande claire (reponse_attendue)</sub>

**9. Client** : pourquoi ce n'est pas possible ?

> [1] La simulation ne propose pas de crédit immobilier car la mensualité indicative est trop élevée. [2] Le projet n'est pas retenu car la durée du crédit est hors du cadre général de 25 ans. [3] Il est recommandé de rendez-vous avec un conseiller pour vérifier les justificatifs.

<sub>niveau 2 · inconnue (aucun, 0.0) · 468.8 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**10. Client** : je peux avoir le prêt à taux zéro ?

> Non proposé — Crédit immobilier : mensualité indicative de 1 123 € sur 300 mois, soit 46,8 % des revenus avec les crédits en cours. Projet non retenu dans cette simulation ; aucun refus bancaire n'est prononcé. Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Taux d'effort indicatif de 46,8 % : au-delà du repère de 35 %. Budget indicatif sous ces hypothèses : environ 196 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (classifieur, 0.9) · 11.1 ms — demande claire (classifieur)</sub>

## 7. C04 — Paul, virement pas à pas, hésitations

**1. Client** : je dois envoyer 500 € à mon fils

> D'accord, je vous guide pas à pas. ⏎ Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. ⏎ Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation.

<sub>niveau 0 · faire_virement (mots_cles, 0.9) · 0.5 ms — demande claire (mots_cles)</sub>

**2. Client** : oui mais pas maintenant

> D'accord. ⏎ Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (classifieur, 0.91) · 10.6 ms — demande claire (classifieur)</sub>

**3. Client** : non plutôt 300 €

> Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. ⏎ Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation.

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 11.6 ms — demande claire (reponse_attendue)</sub>

**4. Client** : comment je fais exactement ?

> Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. ⏎ Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation.

<sub>niveau 1 · faire_virement (interprete, 0.0) · 293.3 ms · 1 LLM — confiance sous le seuil → compris</sub>

**5. Client** : je trouve pas le bouton

> Je ne suis pas sûr de bien vous comprendre. ⏎ Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. ⏎ Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 196.4 ms · 1 LLM — confiance sous le seuil → compris</sub>

**6. Client** : c'est où l'espace sécurisé ?

> Je n'ai pas cette information dans mes fiches. ⏎ Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · question_definition (interprete, 0.0) · 247.6 ms · 1 LLM — aucune fiche assez proche : retour aux règles — ⚠ hors de nos fiches — sources : Carte perdue ou volée, Faire un virement, Ce que l'assistant peut faire</sub>

**7. Client** : vous pouvez le faire pour moi ?

> Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. ⏎ Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation.

<sub>niveau 1 · faire_virement (interprete, 0.0) · 255.2 ms · 1 LLM — confiance sous le seuil → compris</sub>

**8. Client** : pourquoi vous ne pouvez pas ?

> L'assistant n'a aucun accès à votre compte et ne réalise aucune opération : ni virement, ni opposition, ni modification. ⏎ Il explique, conseille à partir de règles publiques et vous oriente vers votre espace bancaire sécurisé ou un conseiller. ⏎ [1]

<sub>niveau 2 · inconnue (aucun, 0.0) · 479.6 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Ce que l'assistant peut faire, Faire une réclamation, Carte perdue ou volée</sub>

**9. Client** : bon d'accord

> D'accord. ⏎ Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (classifieur, 0.99) · 10.4 ms — demande claire (classifieur)</sub>

**10. Client** : merci madame

> Avec plaisir ! ⏎ Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. ⏎ Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 8. C04 — Paul ne comprend pas le vocabulaire

**1. Client** : c'est quoi un RIB

> IBAN : Le numéro qui identifie un compte bancaire ; il faut le donner pour recevoir un virement.

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 0.5 ms — demande claire (mots_cles)</sub>

**2. Client** : et un IBAN c'est pareil ?

> IBAN : Le numéro qui identifie un compte bancaire ; il faut le donner pour recevoir un virement.

<sub>niveau 1 · question_definition (interprete, 0.0) · 280.9 ms · 1 LLM — confiance sous le seuil → compris</sub>

**3. Client** : mon petit-fils m'a demandé mon IBAN c'est normal ?

> IBAN : Le numéro qui identifie un compte bancaire ; il faut le donner pour recevoir un virement.

<sub>niveau 1 · question_definition (interprete, 0.0) · 511.7 ms · 1 LLM — confiance sous le seuil → compris (réponse écartée : absente du message)</sub>

**4. Client** : il veut aussi mon code de carte

> Ne donnez jamais votre code confidentiel, ni vos identifiants, à personne : ni par téléphone, ni par SMS, ni par mail, même à quelqu'un qui se présente comme la banque. ⏎ La banque ne vous les demandera jamais. ⏎ Si vous l'avez déjà donné, faites opposition sur votre carte tout de suite, dans votre espace bancaire sécurisé, et prévenez votre conseiller. ⏎ « opposition » veut dire : le blocage définitif d'une carte perdue ou volée, pour que personne ne puisse s'en servir.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.2 ms — règles</sub>

**5. Client** : je fais quoi alors

> Je ne suis pas sûr de bien vous comprendre. ⏎ Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. ⏎ Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 203.8 ms · 1 LLM — confiance sous le seuil → compris</sub>

**6. Client** : je veux envoyer 50 € à mon petit-fils

> D'accord, je vous guide pas à pas. ⏎ Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. ⏎ Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation.

<sub>niveau 0 · faire_virement (mots_cles, 0.9) · 0.3 ms — demande claire (mots_cles)</sub>

**7. Client** : mon petit fils

> Je ne suis pas sûr de bien vous comprendre. ⏎ Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. ⏎ Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.93) · 10.8 ms — demande claire (classifieur)</sub>

**8. Client** : 50

> Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. ⏎ Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation.

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 10.1 ms — demande claire (reponse_attendue)</sub>

**9. Client** : merci

> Avec plaisir. ⏎ Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**10. Client** : au revoir

> Au revoir, et bonne journée ! ⏎ Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 9. C05 — Karim, crédit auto, variantes

**1. Client** : je veux un crédit pour acheter une voiture

> Je peux vous aider à y voir clair, avec prudence. J'ai noté vos revenus de 1 900 € nets par mois. Vous remboursez déjà 150 € de crédit par mois. Quel montant souhaitez-vous emprunter ?

<sub>niveau 0 · credit_conso (mots_cles, 0.9) · 0.2 ms — demande claire (mots_cles)</sub>

**2. Client** : 12000

> Sur combien de mois souhaitez-vous rembourser ?

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**3. Client** : 48 mois

> Voici ce que je vous propose. Prêt personnel : mensualité indicative de 282 € sur 48 mois, soit 22,7 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Le seuil de prudence consommation est une heuristique interne, pas une obligation HCSF. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 6 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.3 ms — réponse attendue, lue par les règles</sub>

**4. Client** : pourquoi ?

> D'après votre simulation : Prêt personnel : Mensualité indicative de 282 € sur 48 mois, soit 22,7 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 352.6 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**5. Client** : et sur 60 mois ?

> Voici ce que je vous propose. Prêt personnel : mensualité indicative de 232 € sur 60 mois, soit 20,1 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Le seuil de prudence consommation est une heuristique interne, pas une obligation HCSF. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 6 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 10.3 ms — demande claire (reponse_attendue)</sub>

**6. Client** : et si j'emprunte 8000 ?

> Voici ce que je vous propose. Prêt personnel : mensualité indicative de 155 € sur 60 mois, soit 16 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Le seuil de prudence consommation est une heuristique interne, pas une obligation HCSF. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 6 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 11.2 ms — demande claire (reponse_attendue)</sub>

**7. Client** : c'est quoi le TAEG

> TAEG : Le coût total d'un crédit (intérêts, frais, assurance obligatoire) exprimé en pourcentage par an. C'est le chiffre qui permet de comparer deux offres.

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 0.6 ms — demande claire (mots_cles)</sub>

**8. Client** : je peux avoir un rendez-vous pour en parler

> Je ne peux pas prendre de rendez-vous pour vous : je n'ai aucun accès à votre compte. Pour voir un conseiller, prenez rendez-vous depuis votre espace bancaire sécurisé, rubrique Rendez-vous, ou appelez votre agence. Préparez votre projet : montant, durée, revenus.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**9. Client** : ok

> D'accord. Puis-je vous aider pour autre chose ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 238.2 ms · 1 LLM — confiance sous le seuil → compris</sub>

**10. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 10. C05 — Karim, crédit trop gros, refus et reprise

**1. Client** : il me faut un prêt de 25000 pour une voiture neuve

> Je peux vous aider à y voir clair, avec prudence. J'ai noté vos revenus de 1 900 € nets par mois. Vous remboursez déjà 150 € de crédit par mois. Sur combien de mois souhaitez-vous rembourser ?

<sub>niveau 0 · credit_conso (classifieur, 1.0) · 9.7 ms — demande claire (classifieur)</sub>

**2. Client** : sur 3 ans

> Non proposé — Prêt personnel : mensualité indicative de 761 € sur 36 mois, soit 47,9 % des revenus avec les crédits en cours. Projet non retenu dans cette simulation ; aucun refus bancaire n'est prononcé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Le seuil de prudence consommation est une heuristique interne, pas une obligation HCSF. Taux d'effort indicatif de 47,9 % : au-delà du repère de 35 %. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 6 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**3. Client** : pourquoi c'est refusé ?

> D'après votre simulation : Prêt personnel n'est pas proposé : Mensualité indicative de 761 € sur 36 mois, soit 47,9 % des revenus avec les crédits en cours. Projet non retenu dans cette simulation ; aucun refus bancaire n'est prononcé. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 346.9 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**4. Client** : c'est quoi le taux d'effort

> taux d'endettement : La part de vos revenus qui part chaque mois dans vos crédits. Pour un crédit immobilier, elle ne doit pas dépasser 35 %.

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 0.4 ms — demande claire (mots_cles)</sub>

**5. Client** : laisse tomber

> D'accord. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (classifieur, 0.95) · 9.0 ms — demande claire (classifieur)</sub>

**6. Client** : finalement je veux bien réessayer avec 10000

> Voici ce que je vous propose. Prêt personnel : mensualité indicative de 304 € sur 36 mois, soit 23,9 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Le seuil de prudence consommation est une heuristique interne, pas une obligation HCSF. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 6 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 10.0 ms — demande claire (reponse_attendue)</sub>

**7. Client** : sur 48 mois

> Voici ce que je vous propose. Prêt personnel : mensualité indicative de 235 € sur 48 mois, soit 20,3 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Le seuil de prudence consommation est une heuristique interne, pas une obligation HCSF. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 6 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 9.6 ms — demande claire (reponse_attendue)</sub>

**8. Client** : et l'assurance elle est comprise ?

> D'après nos fiches : Un virement se fait depuis votre espace bancaire sécurisé : choisissez ou ajoutez le bénéficiaire, vérifiez son IBAN, puis validez. Vérifiez toujours le bénéficiaire avant de valider, et méfiez-vous d'une demande pressante d'un inconnu. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · question_definition (interprete, 0.0) · 716.0 ms · 2 LLM — confiance sous le seuil → compris (réponse écartée : absente du message) ; aucun terme du glossaire : nos fiches — ⚠ repli du garde-fou — sources : Faire un virement, assurance emprunteur, Livret d'épargne populaire (LEP)</sub>

**9. Client** : je vais réfléchir

> Bien sûr, prenez le temps d'y réfléchir. Je reste disponible si vous avez une question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

**10. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 11. C06 — Julie, mécontente, application en panne

**1. Client** : votre appli ne marche jamais !

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 0 · insatisfaction (mots_cles, 0.95) · 0.1 ms — demande claire (mots_cles)</sub>

**2. Client** : ça fait 3 fois que j'essaie

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 0 · insatisfaction (reponse_attendue, 1.0) · 9.3 ms — demande claire (reponse_attendue)</sub>

**3. Client** : c'est inadmissible

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 0 · insatisfaction (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**4. Client** : je veux faire une réclamation

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 0 · insatisfaction (classifieur, 0.89) · 9.1 ms — demande claire (classifieur)</sub>

**5. Client** : et ça va prendre combien de temps

> D'après nos fiches : Prêt étudiant : Offre LBP pour étudiants de 18 à 35 ans révolus, sur justificatifs et sous réserve d'étude et d'acceptation. Différé selon contrat. Aucune garantie d'État présumée. De 18 à 35 ans. Montant minimum : 1 000 € ; durée de 12 à 120 mois. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · question_definition (interprete, 0.0) · 960.0 ms · 2 LLM — confiance sous le seuil → compris (réponse écartée : absente du message) ; aucun terme du glossaire : nos fiches — ⚠ repli du garde-fou — sources : Prêt étudiant, Livret Jeune, Emprunter pour un logement : durée maximale et taux d'effort (HCSF)</sub>

**6. Client** : je veux parler à quelqu'un de vrai

> Je ne peux pas prendre de rendez-vous pour vous : je n'ai aucun accès à votre compte. Pour voir un conseiller, prenez rendez-vous depuis votre espace bancaire sécurisé, rubrique Rendez-vous, ou appelez votre agence. Préparez votre projet : montant, durée, revenus.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**7. Client** : vous êtes un robot ?

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 251.6 ms · 1 LLM — confiance sous le seuil → compris</sub>

**8. Client** : bon et je fais comment pour mon virement alors

> D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · faire_virement (classifieur, 0.99) · 9.5 ms — demande claire (classifieur)</sub>

**9. Client** : à ma mère, 200 €

> Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation.

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**10. Client** : merci quand même

> Avec plaisir ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 12. C06 — Julie veut fermer son compte

**1. Client** : j'en ai marre je veux fermer mon compte

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 0 · insatisfaction (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**2. Client** : comment je fais ?

> D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 1 · faire_virement (interprete, 0.0) · 264.7 ms · 1 LLM — confiance sous le seuil → compris (réponse écartée : absente du message)</sub>

**3. Client** : et mon livret A il devient quoi

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 1 · epargne_projet (interprete, 0.0) · 222.7 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**4. Client** : vous gardez mes données ?

> Je n'ai aucun accès à vos relevés ni à votre compte : je ne peux pas les consulter. Je m'appuie seulement sur les informations de votre profil (revenus, épargne, crédits en cours). Pour un examen de vos relevés, un conseiller peut le faire avec vous. ⏎ Revenons à votre épargne : dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**5. Client** : en fait j'ai aussi des frais que je comprends pas

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais. ⏎ Passons maintenant à votre autre demande : un virement. D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 222.9 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**6. Client** : des frais de 8 €

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais. ⏎ Passons maintenant à votre autre demande : un virement. D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 247.7 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**7. Client** : c'est scandaleux

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis. ⏎ Revenons à un virement : à qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · insatisfaction (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**8. Client** : je veux un rendez-vous

> Je ne peux pas prendre de rendez-vous pour vous : je n'ai aucun accès à votre compte. Pour voir un conseiller, prenez rendez-vous depuis votre espace bancaire sécurisé, rubrique Rendez-vous, ou appelez votre agence. Préparez votre projet : montant, durée, revenus. ⏎ Revenons à un virement : à qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**9. Client** : ok

> Bien sûr. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 196.7 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**10. Client** : au revoir

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 13. C07 — Léa, appartement, pourquoi, notaire

**1. Client** : je veux acheter un appartement

> C'est un beau projet. J'ai noté vos revenus de 2 900 € nets par mois. Quel est le prix du bien que vous visez, et quelle part de vos 25 000 € d'épargne souhaitez-vous y consacrer ?

<sub>niveau 0 · credit_immobilier (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**2. Client** : autour de 250 000, et je peux mettre les 25 000

> Non proposé — Crédit immobilier : mensualité indicative de 1 197 € sur 300 mois, soit 41,3 % des revenus avec les crédits en cours. Projet non retenu dans cette simulation ; aucun refus bancaire n'est prononcé. Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Taux d'effort indicatif de 41,3 % : au-delà du repère de 35 %. Budget indicatif sous ces hypothèses : environ 215 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**3. Client** : pourquoi ?

> D'après votre simulation : Crédit immobilier n'est pas proposé : Mensualité indicative de 1 197 € sur 300 mois, soit 41,3 % des revenus avec les crédits en cours. Projet non retenu dans cette simulation ; aucun refus bancaire n'est prononcé. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 489.3 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**4. Client** : et avec un bien à 200 000 ?

> Voici ce que je vous propose. Crédit immobilier : mensualité indicative de 933 € sur 300 mois, soit 32,2 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Budget indicatif sous ces hypothèses : environ 215 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 11.0 ms — demande claire (reponse_attendue)</sub>

**5. Client** : combien de frais de notaire pour un appartement ancien ?

> Les frais d'acquisition, dits frais de notaire, sont estimés à environ 7,5 % du prix dans l'ancien et 2,5 % dans le neuf. [1]

<sub>niveau 2 · credit_immobilier (classifieur, 0.96) · 409.5 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Frais d'acquisition (notaire), frais de notaire, Plan épargne logement (PEL)</sub>

**6. Client** : et si j'emprunte sur 30 ans ?

> Voici ce que je vous propose. Crédit immobilier : mensualité indicative de 933 € sur 300 mois, soit 32,2 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Budget indicatif sous ces hypothèses : environ 215 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 10.7 ms — demande claire (reponse_attendue)</sub>

**7. Client** : c'est quoi le HCSF

> D'après nos fiches : Pour emprunter et acheter un logement, le cadre du HCSF limite la durée du crédit immobilier à 25 ans et le taux d'effort à 35 % des revenus, assurance comprise. La banque garde une part de flexibilité et décide après étude du dossier : aucun accord n'est automatique. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · question_definition (classifieur, 0.94) · 528.3 ms · 1 LLM — terme absent du glossaire : recherche dans nos fiches — ⚠ repli du garde-fou — sources : Emprunter pour un logement : durée maximale et taux d'effort (HCSF), Crédit immobilier, reste à vivre</sub>

**8. Client** : le taux d'effort maximum c'est combien

> D'après nos fiches : Pour emprunter et acheter un logement, le cadre du HCSF limite la durée du crédit immobilier à 25 ans et le taux d'effort à 35 % des revenus, assurance comprise. La banque garde une part de flexibilité et décide après étude du dossier : aucun accord n'est automatique. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 265.4 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Emprunter pour un logement : durée maximale et taux d'effort (HCSF), taux d'endettement, Taux moyen des crédits : repères de la Banque de France</sub>

**9. Client** : je peux avoir un rendez-vous

> Je ne peux pas prendre de rendez-vous pour vous : je n'ai aucun accès à votre compte. Pour voir un conseiller, prenez rendez-vous depuis votre espace bancaire sécurisé, rubrique Rendez-vous, ou appelez votre agence. Préparez votre projet : montant, durée, revenus.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**10. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 14. C07 — Léa, questions ouvertes sur le crédit immobilier

**1. Client** : c'est quoi le taux moyen d'un crédit immobilier en ce moment ?

> C'est un beau projet. J'ai noté vos revenus de 2 900 € nets par mois. Quel est le prix du bien que vous visez, et quelle part de vos 25 000 € d'épargne souhaitez-vous y consacrer ?

<sub>niveau 0 · credit_immobilier (classifieur, 0.96) · 23.7 ms — demande claire (classifieur)</sub>

**2. Client** : sur combien d'années maximum on peut emprunter

> D'après nos fiches : Pour emprunter et acheter un logement, le cadre du HCSF limite la durée du crédit immobilier à 25 ans et le taux d'effort à 35 % des revenus, assurance comprise. La banque garde une part de flexibilité et décide après étude du dossier : aucun accord n'est automatique. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · credit_immobilier (reponse_attendue, 1.0) · 195.4 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Emprunter pour un logement : durée maximale et taux d'effort (HCSF), Prêt étudiant, Prêt personnel</sub>

**3. Client** : j'ai droit au prêt à taux zéro ?

> Bien sûr. Quel est le prix du bien que vous visez, et quelle part de vos 25 000 € d'épargne souhaitez-vous y consacrer ? Par exemple : 200 €.

<sub>niveau 1 · credit_immobilier (reponse_attendue, 1.0) · 307.4 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**4. Client** : c'est quoi une assurance emprunteur

> assurance emprunteur : Une assurance qui rembourse tout ou partie de votre crédit si vous ne pouvez plus le faire (décès, invalidité…). Elle est presque toujours demandée pour un crédit immobilier. ⏎ Revenons à un crédit : quel est le prix du bien que vous visez, et quelle part de vos 25 000 € d'épargne souhaitez-vous y consacrer ?

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 0.5 ms — demande claire (mots_cles)</sub>

**5. Client** : je veux acheter un studio pour le louer

> Bien sûr. Quel est le prix du bien que vous visez, et quelle part de vos 25 000 € d'épargne souhaitez-vous y consacrer ? Par exemple : 200 €.

<sub>niveau 1 · credit_immobilier (reponse_attendue, 1.0) · 254.4 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**6. Client** : 120000

> Quelle part de vos 25 000 € d'épargne souhaitez-vous consacrer à l'achat ?

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**7. Client** : 20000

> Voici ce que je vous propose. Crédit immobilier : mensualité indicative de 535 € sur 300 mois, soit 18,5 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Budget indicatif sous ces hypothèses : environ 210 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**8. Client** : pourquoi ?

> parce que la durée du prêt est hors du cadre général de 25 ans. [2] parce que la mensualité est indicative et l'orientation est conditionnelle. [3] parce que le conseiller vérifie les justificatifs et la décision ne vaut pas accord.

<sub>niveau 2 · inconnue (aucun, 0.0) · 434.0 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**9. Client** : et le frais de notaire dans le neuf ?

> frais de notaire : Les taxes et frais payés lors de l'achat d'un logement, en plus du prix : environ 7 à 8 % dans l'ancien, 2 à 3 % dans le neuf.

<sub>niveau 1 · question_definition (interprete, 0.0) · 269.0 ms · 1 LLM — confiance sous le seuil → compris</sub>

**10. Client** : ok merci

> Avec plaisir ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 15. C08 — Lucas, épargne courte, jargon, prêt étudiant

**1. Client** : je voudrais mettre de côté

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · epargne_projet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**2. Client** : dans 2 ans

> Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**3. Client** : 50 euros

> Voici ce que je vous propose. Livret Jeune : à 20 ans, tranche d'âge compatible ; épargne disponible. Livret A : épargne disponible ; adaptée à une réserve ou un projet sans immobilisation. ⏎ Non proposé — Livret de développement durable et solidaire (LDDS) : domicile fiscal français et imposition séparée nécessaires. Non proposé — Livret d'épargne populaire (LEP) : domicile fiscal français et imposition séparée nécessaires. Non proposé — Plan épargne logement (PEL) : besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**4. Client** : c'est quoi le TEAG ?

> TAEG : Le coût total d'un crédit (intérêts, frais, assurance obligatoire) exprimé en pourcentage par an. C'est le chiffre qui permet de comparer deux offres.

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 5.0 ms — demande claire (mots_cles)</sub>

**5. Client** : je voudrais un prêt étudiant

> C'est une question fréquente pendant les études. De quel montant auriez-vous besoin, à peu près ?

<sub>niveau 0 · pret_etudiant (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**6. Client** : 5000

> Voici ce que je vous propose. Prêt étudiant : piste LBP compatible avec l'âge, le montant et le statut déclarés ; justificatif étudiant et étude du prêteur nécessaires. Différé selon contrat, sous réserve d'acceptation du prêteur. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · pret_etudiant (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**7. Client** : pourquoi ?

> D'après votre simulation : Prêt étudiant : Piste LBP compatible avec l'âge, le montant et le statut déclarés ; justificatif étudiant et étude du prêteur nécessaires. Différé selon contrat, sous réserve d'acceptation du prêteur. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 290.5 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Votre simulation, Votre simulation</sub>

**8. Client** : je rembourse quand ?

> D'après nos fiches : Livret Jeune : De 12 à 25 ans. Plafond des versements : 1 600 €. De 12 à 25 ans. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · question_definition (interprete, 0.0) · 544.8 ms · 2 LLM — confiance sous le seuil → compris ; aucun terme du glossaire : nos fiches — ⚠ repli du garde-fou — sources : Livret Jeune, Livret d'épargne populaire (LEP), Prêt étudiant</sub>

**9. Client** : il faut un garant ?

> Voici ce que je vous propose. Prêt étudiant : piste LBP compatible avec l'âge, le montant et le statut déclarés ; justificatif étudiant et étude du prêteur nécessaires. Différé selon contrat, sous réserve d'acceptation du prêteur. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 1 · pret_etudiant (interprete, 0.0) · 288.6 ms · 1 LLM — confiance sous le seuil → compris</sub>

**10. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 16. C08 — Lucas, prêt étudiant avec fautes

**1. Client** : slt je ve un pret pour mes etudes

> C'est une question fréquente pendant les études. De quel montant auriez-vous besoin, à peu près ?

<sub>niveau 1 · pret_etudiant (interprete, 0.0) · 251.3 ms · 1 LLM — confiance sous le seuil → compris</sub>

**2. Client** : jsp combien, mon ecole coute 7000 par an

> Voici ce que je vous propose. Prêt étudiant : piste LBP compatible avec l'âge, le montant et le statut déclarés ; justificatif étudiant et étude du prêteur nécessaires. Différé selon contrat, sous réserve d'acceptation du prêteur. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · pret_etudiant (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**3. Client** : 7000

> Voici ce que je vous propose. Prêt étudiant : piste LBP compatible avec l'âge, le montant et le statut déclarés ; justificatif étudiant et étude du prêteur nécessaires. Différé selon contrat, sous réserve d'acceptation du prêteur. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · pret_etudiant (reponse_attendue, 1.0) · 9.2 ms — demande claire (reponse_attendue)</sub>

**4. Client** : jai 20 ans je suis en master

> Voici ce que je vous propose. Prêt étudiant : piste LBP compatible avec l'âge, le montant et le statut déclarés ; justificatif étudiant et étude du prêteur nécessaires. Différé selon contrat, sous réserve d'acceptation du prêteur. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · pret_etudiant (reponse_attendue, 1.0) · 9.9 ms — demande claire (reponse_attendue)</sub>

**5. Client** : c'est quoi un différé

> Je n'ai pas cette information dans mes fiches. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · question_definition (classifieur, 0.98) · 24.8 ms — aucune fiche assez proche : retour aux règles — ⚠ hors de nos fiches — sources : LEP, Offre clientèle fragile, Livret de développement durable et solidaire (LDDS)</sub>

**6. Client** : et si je rate mon année

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 244.9 ms · 1 LLM — confiance sous le seuil → compris</sub>

**7. Client** : je peux en parler à quelqu'un ?

> Je ne peux pas prendre de rendez-vous pour vous : je n'ai aucun accès à votre compte. Pour voir un conseiller, prenez rendez-vous depuis votre espace bancaire sécurisé, rubrique Rendez-vous, ou appelez votre agence. Préparez votre projet : montant, durée, revenus.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**8. Client** : ok

> D'accord. Puis-je vous aider pour autre chose ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 204.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**9. Client** : merci bcp

> Avec plaisir ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**10. Client** : a+

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 201.7 ms · 1 LLM — confiance sous le seuil → compris</sub>

## 17. C01 — problème de carte flou, en langage SMS

**1. Client** : slt

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 209.0 ms · 1 LLM — confiance sous le seuil → compris</sub>

**2. Client** : jsuis perdu

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 201.8 ms · 1 LLM — confiance sous le seuil → compris</sub>

**3. Client** : j'ai un pb avec ma cb

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 198.8 ms · 1 LLM — confiance sous le seuil → compris</sub>

**4. Client** : elle passe pas

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 190.6 ms · 1 LLM — confiance sous le seuil → compris</sub>

**5. Client** : au distributeur

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 191.2 ms · 1 LLM — confiance sous le seuil → compris</sub>

**6. Client** : et en magasin non plus

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 241.7 ms · 1 LLM — confiance sous le seuil → compris</sub>

**7. Client** : mon code est bon pourtant

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 232.4 ms · 1 LLM — confiance sous le seuil → compris</sub>

**8. Client** : c'est peut être bloqué ?

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 241.2 ms · 1 LLM — confiance sous le seuil → compris</sub>

**9. Client** : je fais quoi

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 200.3 ms · 1 LLM — confiance sous le seuil → compris</sub>

**10. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 18. C02 — opérations contestées

**1. Client** : il y a un prélèvement que je connais pas

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 284.3 ms · 1 LLM — confiance sous le seuil → compris</sub>

**2. Client** : de 45 €

> Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 0 · extra_charge_on_statement (reponse_attendue, 1.0) · 10.2 ms — demande claire (reponse_attendue)</sub>

**3. Client** : j'ai aussi été débité deux fois pour le même achat

> Je comprends que votre demande concerne des frais ou une opération contestée. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · transaction_charged_twice (classifieur, 0.84) · 11.5 ms — demande claire (classifieur)</sub>

**4. Client** : comment je me fais rembourser ?

> Je comprends que votre demande concerne des frais ou une opération contestée. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · request_refund (classifieur, 0.76) · 11.9 ms — demande claire (classifieur)</sub>

**5. Client** : c'est quoi un prélèvement

> prélèvement : Un paiement demandé directement à votre banque par une entreprise que vous avez autorisée (énergie, téléphone…).

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 0.6 ms — demande claire (mots_cles)</sub>

**6. Client** : je peux le bloquer ?

> Je ne peux pas vous bloquer directement, car l'assistant n'a aucun accès à votre compte et ne peut pas réaliser d'opération. Pour bloquer une carte perdue ou volée, faites opposition immédiatement depuis votre espace bancaire sécurisé [1].

<sub>niveau 2 · inconnue (aucun, 0.0) · 438.7 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Carte perdue ou volée, Faire une réclamation, Ce que l'assistant peut faire</sub>

**7. Client** : je veux parler à un conseiller

> Je ne peux pas prendre de rendez-vous pour vous : je n'ai aucun accès à votre compte. Pour voir un conseiller, prenez rendez-vous depuis votre espace bancaire sécurisé, rubrique Rendez-vous, ou appelez votre agence. Préparez votre projet : montant, durée, revenus.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**8. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**9. Client** : ah et mes frais de 8 € ?

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 0 · transfer_fee_charged (classifieur, 0.86) · 10.6 ms — demande claire (classifieur)</sub>

**10. Client** : ok

> D'accord. Puis-je vous aider pour autre chose ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 254.6 ms · 1 LLM — confiance sous le seuil → compris</sub>

## 19. C03 — virement aux enfants et épargne mêlés

**1. Client** : je veux virer 100 € à ma fille et mettre de côté pour elle

> D'accord, je vous guide pas à pas. Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation.

<sub>niveau 0 · faire_virement (classifieur, 0.98) · 11.3 ms — demande claire (classifieur)</sub>

**2. Client** : ma fille

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.9) · 10.1 ms — demande claire (classifieur)</sub>

**3. Client** : 100

> Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation.

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 11.3 ms — demande claire (reponse_attendue)</sub>

**4. Client** : pour l'épargne c'est pour dans 5 ans

> Bonne idée de mettre de côté. Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (classifieur, 0.8) · 12.4 ms — demande claire (classifieur)</sub>

**5. Client** : 30 euros par mois

> Voici ce que je vous propose. Livret A : alimenter le livret existant, sans en ouvrir un second. Épargne disponible ; adaptée à une réserve ou un projet sans immobilisation. Livret de développement durable et solidaire (LDDS) : domicile fiscal français et imposition séparée déclarés ; épargne disponible. ⏎ Non proposé — Livret Jeune : hors de la tranche d'âge du Livret Jeune. Non proposé — Plan épargne logement (PEL) : besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. Livret d'épargne populaire (LEP) : éligibilité à vérifier (revenu fiscal de référence, nombre de parts fiscales, année du revenu fiscal, territoire fiscal), aucune inéligibilité déduite. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.4 ms — réponse attendue, lue par les règles</sub>

**6. Client** : pourquoi le livret jeune ?

> D'après nos fiches : Livret Jeune : De 12 à 25 ans. Plafond des versements : 1 600 €. De 12 à 25 ans. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 527.0 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Livret Jeune, Livret Jeune, Votre simulation</sub>

**7. Client** : elle a 14 ans

> Voici ce que je vous propose. Livret A : alimenter le livret existant, sans en ouvrir un second. Épargne disponible ; adaptée à une réserve ou un projet sans immobilisation. Livret de développement durable et solidaire (LDDS) : domicile fiscal français et imposition séparée déclarés ; épargne disponible. ⏎ Non proposé — Livret Jeune : hors de la tranche d'âge du Livret Jeune. Non proposé — Plan épargne logement (PEL) : besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. Livret d'épargne populaire (LEP) : éligibilité à vérifier (revenu fiscal de référence, nombre de parts fiscales, année du revenu fiscal, territoire fiscal), aucune inéligibilité déduite. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 10.5 ms — demande claire (reponse_attendue)</sub>

**8. Client** : et pour mon fils aussi

> Voici ce que je vous propose. Livret A : alimenter le livret existant, sans en ouvrir un second. Épargne disponible ; adaptée à une réserve ou un projet sans immobilisation. Livret de développement durable et solidaire (LDDS) : domicile fiscal français et imposition séparée déclarés ; épargne disponible. ⏎ Non proposé — Livret Jeune : hors de la tranche d'âge du Livret Jeune. Non proposé — Plan épargne logement (PEL) : besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. Livret d'épargne populaire (LEP) : éligibilité à vérifier (revenu fiscal de référence, nombre de parts fiscales, année du revenu fiscal, territoire fiscal), aucune inéligibilité déduite. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 1 · epargne_projet (interprete, 0.0) · 282.0 ms · 1 LLM — confiance sous le seuil ; renvoi au contexte → compris</sub>

**9. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**10. Client** : au revoir

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 20. C04 — Paul perdu dans l'application

**1. Client** : je comprends rien à l'appli

> D'après nos fiches : L'assistant n'a aucun accès à votre compte et ne réalise aucune opération : ni virement, ni opposition, ni modification. ⏎ Il explique, conseille à partir de règles publiques et vous oriente vers votre espace bancaire sécurisé ou un conseiller. ⏎ [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · question_definition (interprete, 0.0) · 765.0 ms · 2 LLM — confiance sous le seuil → compris ; aucun terme du glossaire : nos fiches — ⚠ repli du garde-fou — sources : Ce que l'assistant peut faire, Carte perdue ou volée, Faire une réclamation</sub>

**2. Client** : comment je fais un virement

> Pour faire un virement, choisissez ou ajoutez le bénéficiaire, vérifiez son IBAN, puis validez. ⏎ Vérifiez toujours le bénéficiaire avant de valider, et méfiez-vous d'une demande pressante d'un inconnu [1]. ⏎ L'assistant ne peut pas effectuer l'opération, mais il peut vous orienter vers votre espace bancaire sécurisé ou un conseiller.

<sub>niveau 2 · faire_virement (classifieur, 1.0) · 590.9 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Faire un virement, Ce que l'assistant peut faire, Carte perdue ou volée</sub>

**3. Client** : c'est quoi un bénéficiaire

> D'après nos fiches : Un virement se fait depuis votre espace bancaire sécurisé : choisissez ou ajoutez le bénéficiaire, vérifiez son IBAN, puis validez. ⏎ Vérifiez toujours le bénéficiaire avant de valider, et méfiez-vous d'une demande pressante d'un inconnu. ⏎ [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · question_definition (interprete, 0.0) · 681.3 ms · 2 LLM — confiance sous le seuil → compris (réponse écartée : absente du message) ; aucun terme du glossaire : nos fiches — ⚠ repli du garde-fou — sources : Faire un virement, IBAN, LEP</sub>

**4. Client** : mon fils

> Je ne suis pas sûr de bien vous comprendre. ⏎ Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. ⏎ Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.92) · 10.2 ms — demande claire (classifieur)</sub>

**5. Client** : 200

> Je ne suis pas sûr de bien vous comprendre. ⏎ Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. ⏎ Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.78) · 10.9 ms — demande claire (classifieur)</sub>

**6. Client** : je peux le faire au guichet ?

> Bonne idée de mettre de côté. ⏎ Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 1 · epargne_projet (interprete, 0.0) · 305.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**7. Client** : je préfère voir quelqu'un

> Je n'ai pas bien compris. ⏎ Dans combien de temps pensez-vous avoir besoin de cet argent ? ⏎ Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 192.6 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**8. Client** : merci

> Avec plaisir. ⏎ Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**9. Client** : vous êtes gentille

> Je n'ai pas bien compris. ⏎ Dans combien de temps pensez-vous avoir besoin de cet argent ? ⏎ Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 174.9 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**10. Client** : au revoir

> Au revoir, et bonne journée ! ⏎ Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 21. C05 — capacité d'emprunt, questions générales

**1. Client** : combien je peux emprunter

> Vous pouvez emprunter jusqu'à 25 ans et un taux d'effort de 35 % des revenus, assurance comprise. La banque garde une part de flexibilité et décide après étude du dossier : aucun accord n'est automatique. [1]

<sub>niveau 2 · credit_conso (classifieur, 0.99) · 452.0 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Emprunter pour un logement : durée maximale et taux d'effort (HCSF), Prêt étudiant, Compte épargne logement (CEL)</sub>

**2. Client** : pour une voiture

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.78) · 9.6 ms — demande claire (classifieur)</sub>

**3. Client** : 15000

> Pour bien vous aider, pouvez-vous préciser ? Par exemple : votre carte, un virement, des frais, votre épargne ou un projet de crédit.

<sub>niveau 1 · inconnue (aucun, 0.0) · 242.1 ms · 1 LLM — confiance sous le seuil → rien de net — ⚠ clarification</sub>

**4. Client** : 60 mois

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.81) · 10.3 ms — demande claire (classifieur)</sub>

**5. Client** : pourquoi ?

> reste à vivre : reste à vivre : Ce qui vous reste chaque mois une fois payés vos charges et vos crédits. [2] LEP : LEP : Un livret mieux rémunéré, réservé aux personnes dont les revenus sont sous un plafond. [3] prélèvement : prélèvement : Un paiement demandé directement à votre banque par une entreprise que vous avez autorisée (énergie, téléphone…).   ⏎ Si les extraits ne suffisent pas, je propose de parler à un conseiller.

<sub>niveau 2 · question_definition (interprete, 0.0) · 929.0 ms · 2 LLM — confiance sous le seuil → compris (réponse écartée : absente du message) ; aucun terme du glossaire : nos fiches — sources : reste à vivre, LEP, prélèvement</sub>

**6. Client** : et c'est quoi le taux moyen d'un prêt personnel

> Je peux vous aider à y voir clair, avec prudence. J'ai noté vos revenus de 1 900 € nets par mois. Vous remboursez déjà 150 € de crédit par mois. Quel montant souhaitez-vous emprunter ?

<sub>niveau 0 · credit_conso (mots_cles, 0.9) · 7.5 ms — plusieurs demandes nettes : traitées par ordre d'urgence</sub>

**7. Client** : je peux avoir un crédit sans justificatif ?

> Bien sûr. Quel montant souhaitez-vous emprunter ? Par exemple : 200 €.

<sub>niveau 1 · credit_conso (reponse_attendue, 1.0) · 302.7 ms · 1 LLM — réponse libre, illisible par les règles → compris (réponse écartée : absente du message)</sub>

**8. Client** : et un crédit renouvelable ?

> Bien sûr. Quel montant souhaitez-vous emprunter ? Par exemple : 200 €.

<sub>niveau 1 · credit_conso (reponse_attendue, 1.0) · 240.3 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**9. Client** : ok

> Bien sûr. Quel montant souhaitez-vous emprunter ? Par exemple : 200 €.

<sub>niveau 1 · credit_conso (reponse_attendue, 1.0) · 187.4 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**10. Client** : merci

> Avec plaisir. Quel montant souhaitez-vous emprunter ?

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

## 22. C06 — bavardage puis vraie demande

**1. Client** : salut ça va ?

> Bonjour ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles) — ⚠ « Bonjour ! »</sub>

**2. Client** : t'es un robot ?

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.98) · 9.5 ms — demande claire (classifieur)</sub>

**3. Client** : il fait beau aujourd'hui

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 1.0) · 9.7 ms — demande claire (classifieur)</sub>

**4. Client** : bon j'ai une vraie question

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.87) · 10.1 ms — demande claire (classifieur)</sub>

**5. Client** : j'ai des frais bizarres sur mon compte

> Je comprends que votre demande concerne des frais ou une opération contestée. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · card_payment_not_recognised (classifieur, 0.98) · 10.2 ms — demande claire (classifieur)</sub>

**6. Client** : pourquoi ?

> reste à vivre : reste à vivre : Ce qui vous reste chaque mois une fois payés vos charges et vos crédits. [2] LEP : LEP : Un livret mieux rémunéré, réservé aux personnes dont les revenus sont sous un plafond. [3] prélèvement : prélèvement : Un paiement demandé directement à votre banque par une entreprise que vous avez autorisée (énergie, téléphone…).  ⏎ Si les extraits ne suffisent pas, je propose de parler à un conseiller.

<sub>niveau 2 · question_definition (interprete, 0.0) · 910.9 ms · 2 LLM — confiance sous le seuil → compris (réponse écartée : absente du message) ; aucun terme du glossaire : nos fiches — sources : reste à vivre, LEP, prélèvement</sub>

**7. Client** : c'est la troisième fois que je vous écris aujourd'hui

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 237.1 ms · 1 LLM — confiance sous le seuil → compris</sub>

**8. Client** : vous êtes nuls

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 197.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**9. Client** : bon je veux un rendez-vous

> Je ne peux pas prendre de rendez-vous pour vous : je n'ai aucun accès à votre compte. Pour voir un conseiller, prenez rendez-vous depuis votre espace bancaire sécurisé, rubrique Rendez-vous, ou appelez votre agence. Préparez votre projet : montant, durée, revenus.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**10. Client** : bye

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 23. C07 — questions ouvertes sur l'épargne (RAG)

**1. Client** : quel est le plafond du livret A ?

> Le plafond du Livret A est de 22 950 € [1].

<sub>niveau 2 · inconnue (aucun, 0.0) · 220.7 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Livret A, Livret A, Livret Jeune</sub>

**2. Client** : et du LDDS

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 1 · epargne_projet (interprete, 0.0) · 292.9 ms · 1 LLM — confiance sous le seuil → compris</sub>

**3. Client** : est-ce que je peux ouvrir un LEP ?

> Est-ce que vous pouvez ouvrir un LEP ? [1] Oui, si vous avez un domicile fiscal français et que vos revenus sont sous un plafond. [2] Le LEP est un livret mieux rémunéré, réservé aux personnes dont les revenus sont sous un plafond. [3] Le LEP est un livret mieux rémunéré, réservé aux personnes dont les revenus sont sous un plafond. Vous pouvez ouvrir un LEP si vous avez un domicile fiscal français et que vos revenus sont sous un plafond.

<sub>niveau 2 · epargne_projet (reponse_attendue, 1.0) · 748.2 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Livret d'épargne populaire (LEP), LEP, Plan épargne logement (PEL)</sub>

**4. Client** : combien faut-il garder au minimum sur un CEL ?

> Sur un compte épargne logement (CEL), le solde minimum à conserver est de 300 € [1].

<sub>niveau 2 · epargne_projet (reponse_attendue, 1.0) · 237.4 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Compte épargne logement (CEL), Plan épargne logement (PEL), Emprunter pour un logement : durée maximale et taux d'effort (HCSF)</sub>

**5. Client** : quel est le versement minimum pour ouvrir un PEL ?

> Le versement minimum pour ouvrir un PEL est de 225 € initial et 540 € annuels [1].

<sub>niveau 2 · epargne_projet (reponse_attendue, 1.0) · 232.8 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Plan épargne logement (PEL), PEL, Livret d'épargne populaire (LEP)</sub>

**6. Client** : c'est quoi la différence entre un PEL et un CEL

> Quel est la différence entre un PEL et un CEL ? [1] Le PEL est un plan épargne logement par personne, avec un plafond de versements de 61 200 € et une durée minimale de 4 ans, tandis que le CEL est un compte épargne logement, avec un plafond de 15 300 € et un solde minimum de 300 €. Le PEL permet un retrait anticipé, tandis que le CEL ne peut être retiré qu'avec le minimum conservé.

<sub>niveau 2 · question_definition (mots_cles, 0.9) · 723.5 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Plan épargne logement (PEL), Compte épargne logement (CEL), PEL</sub>

**7. Client** : et ça rapporte combien ?

> Bien sûr. Dans combien de temps pensez-vous avoir besoin de cet argent ? Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 284.3 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**8. Client** : je veux épargner pour un apport

> Bien sûr. Dans combien de temps pensez-vous avoir besoin de cet argent ? Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 231.8 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**9. Client** : dans 5 ans

> Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**10. Client** : 300 € par mois

> Voici ce que je vous propose. Livret de développement durable et solidaire (LDDS) : alimenter le livret existant, sans en ouvrir un second. Domicile fiscal français et imposition séparée déclarés ; épargne disponible. Les versements prévus dépassent la place disponible de 9 950 € ; prévoir une répartition. ⏎ Non proposé — Livret Jeune : hors de la tranche d'âge du Livret Jeune. Non proposé — Livret A : plafond des versements atteint ; aucun nouveau versement proposé. Non proposé — Plan épargne logement (PEL) : besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. Livret d'épargne populaire (LEP) : éligibilité à vérifier (revenu fiscal de référence, nombre de parts fiscales, année du revenu fiscal, territoire fiscal), aucune inéligibilité déduite. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

## 24. C08 — carte bloquée, code PIN, virement à la mère

**1. Client** : ma carte est bloquée j'ai tapé 3 fois le mauvais code

> Je comprends que votre demande concerne l'utilisation de votre carte. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · pin_blocked (classifieur, 0.86) · 11.1 ms — demande claire (classifieur)</sub>

**2. Client** : comment je la débloque

> Je comprends que votre demande concerne l'utilisation de votre carte. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 1 · card_not_working (interprete, 0.0) · 249.6 ms · 1 LLM — confiance sous le seuil → compris</sub>

**3. Client** : et je peux changer mon code ?

> Je comprends que votre demande concerne l'utilisation de votre carte. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 1 · card_not_working (interprete, 0.0) · 234.9 ms · 1 LLM — confiance sous le seuil → compris</sub>

**4. Client** : en attendant je dois envoyer de l'argent à ma mère

> D'accord, je vous guide pas à pas. Quel montant voulez-vous envoyer ?

<sub>niveau 0 · faire_virement (mots_cles, 0.9) · 0.2 ms — demande claire (mots_cles)</sub>

**5. Client** : 80

> Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation.

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**6. Client** : elle a un compte dans une autre banque ça marche ?

> Je comprends que votre demande concerne un virement. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · receiving_money (classifieur, 0.79) · 11.0 ms — demande claire (classifieur)</sub>

**7. Client** : combien de temps ça prend

> D'après nos fiches : Pour emprunter et acheter un logement, le cadre du HCSF limite la durée du crédit immobilier à 25 ans et le taux d'effort à 35 % des revenus, assurance comprise. La banque garde une part de flexibilité et décide après étude du dossier : aucun accord n'est automatique. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · question_definition (interprete, 0.0) · 792.7 ms · 2 LLM — confiance sous le seuil → compris ; aucun terme du glossaire : nos fiches — ⚠ repli du garde-fou — sources : Emprunter pour un logement : durée maximale et taux d'effort (HCSF), Prêt étudiant, Livret Jeune</sub>

**8. Client** : ok

> D'accord. Puis-je vous aider pour autre chose ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 256.7 ms · 1 LLM — confiance sous le seuil → compris</sub>

**9. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**10. Client** : a plus

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 25. C01 — trois demandes d'un coup

**1. Client** : j'ai perdu ma carte, je veux faire un virement et je voudrais épargner

> Je comprends, il faut agir vite. Faites opposition tout de suite : dans votre espace bancaire sécurisé, rubrique Opposition, ou en appelant votre conseiller. Je ne peux pas bloquer votre carte depuis cette conversation. Rappel : la banque ne vous demandera jamais votre code confidentiel. ⏎ Passons maintenant à votre autre demande : un virement. D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · lost_or_stolen_card (mots_cles, 0.9) · 0.2 ms — plusieurs demandes nettes : traitées par ordre d'urgence</sub>

**2. Client** : à mon frère

> Quel montant voulez-vous envoyer ?

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**3. Client** : 150

> Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation. ⏎ Passons maintenant à votre autre demande : votre épargne. Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**4. Client** : pour l'épargne dans 3 ans

> Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**5. Client** : 100 par mois

> Voici ce que je vous propose. Livret A : alimenter le livret existant, sans en ouvrir un second. Épargne disponible ; adaptée à une réserve ou un projet sans immobilisation. Livret de développement durable et solidaire (LDDS) : domicile fiscal français et imposition séparée déclarés ; épargne disponible. ⏎ Non proposé — Livret Jeune : hors de la tranche d'âge du Livret Jeune. Non proposé — Plan épargne logement (PEL) : besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. Livret d'épargne populaire (LEP) : éligibilité à vérifier (revenu fiscal de référence, nombre de parts fiscales, année du revenu fiscal, territoire fiscal), aucune inéligibilité déduite. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.3 ms — réponse attendue, lue par les règles</sub>

**6. Client** : pourquoi ?

> [Votre simulation : Livret Jeune] : [1] Hors de la tranche d'âge du Livret Jeune.  
[Votre simulation : Plan épargne logement (PEL)] : [2] Besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages.  
[Votre simulation : Livret A] : [3] Alimenter le livret existant, sans en ouvrir un second. Épargne disponible ; adaptée à une réserve ou un projet sans immobilisation.   ⏎ Il faut vérifier les conditions spécifiques de votre situation. Si besoin, contactez un conseiller pour plus d'information.

<sub>niveau 2 · inconnue (aucun, 0.0) · 886.0 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**7. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**8. Client** : et mes frais ?

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 0 · transfer_fee_charged (classifieur, 0.97) · 10.3 ms — demande claire (classifieur)</sub>

**9. Client** : 8 €

> Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 0 · transfer_fee_charged (reponse_attendue, 1.0) · 11.0 ms — demande claire (reponse_attendue)</sub>

**10. Client** : ok

> D'accord. Puis-je vous aider pour autre chose ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 255.1 ms · 1 LLM — confiance sous le seuil → compris</sub>

## 26. C02 — rendez-vous, relevés, accès au compte

**1. Client** : regarde mon compte et dis moi si j'ai assez pour un crédit

> Je n'ai aucun accès à vos relevés ni à votre compte : je ne peux pas les consulter. Je m'appuie seulement sur les informations de votre profil (revenus, épargne, crédits en cours). Pour un examen de vos relevés, un conseiller peut le faire avec vous.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**2. Client** : consulte mes relevés stp

> Je n'ai aucun accès à vos relevés ni à votre compte : je ne peux pas les consulter. Je m'appuie seulement sur les informations de votre profil (revenus, épargne, crédits en cours). Pour un examen de vos relevés, un conseiller peut le faire avec vous.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**3. Client** : pourquoi tu peux pas ?

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.79) · 10.6 ms — demande claire (classifieur)</sub>

**4. Client** : je veux un rdv avec mon conseiller

> Je ne peux pas prendre de rendez-vous pour vous : je n'ai aucun accès à votre compte. Pour voir un conseiller, prenez rendez-vous depuis votre espace bancaire sécurisé, rubrique Rendez-vous, ou appelez votre agence. Préparez votre projet : montant, durée, revenus.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**5. Client** : je veux un crédit pour des travaux

> Je peux vous aider à y voir clair, avec prudence. J'ai noté vos revenus de 1 850 € nets par mois. Quel montant souhaitez-vous emprunter ?

<sub>niveau 0 · credit_conso (classifieur, 1.0) · 11.8 ms — demande claire (classifieur)</sub>

**6. Client** : 6000

> Sur combien de mois souhaitez-vous rembourser ?

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**7. Client** : 36 mois

> Voici ce que je vous propose. Prêt personnel : mensualité indicative de 183 € sur 36 mois, soit 9,9 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Le seuil de prudence consommation est une heuristique interne, pas une obligation HCSF. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 6 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.3 ms — réponse attendue, lue par les règles</sub>

**8. Client** : pourquoi ?

> D'après votre simulation : Prêt personnel : Mensualité indicative de 183 € sur 36 mois, soit 9,9 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 334.6 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**9. Client** : ok

> D'accord. Puis-je vous aider pour autre chose ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 237.3 ms · 1 LLM — confiance sous le seuil → compris</sub>

**10. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 27. C03 — épargne avec réponses vagues et abandon

**1. Client** : je voudrais épargner

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · epargne_projet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**2. Client** : pour mes enfants

> Bien sûr. Dans combien de temps pensez-vous avoir besoin de cet argent ? Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 242.2 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**3. Client** : je sais pas

> Je pars sur un an ; vous pourrez ajuster. Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**4. Client** : je sais pas non plus

> Pas de souci, une estimation suffit. Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**5. Client** : euh

> Je n'ai pas bien compris. Combien pouvez-vous mettre de côté chaque mois ? Par exemple : 200 €.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 173.9 ms · 1 LLM — réponse libre, illisible par les règles → rien de net — ⚠ incompris</sub>

**6. Client** : laisse tomber

> D'accord, on laisse ça de côté. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**7. Client** : finalement oui

> Très bien, reprenons : votre épargne. Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (mots_cles, 1.0) · 10.5 ms — demande claire (mots_cles)</sub>

**8. Client** : dans 2 ans

> Bien sûr. Combien pouvez-vous mettre de côté chaque mois ? Par exemple : 200 €.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 230.4 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**9. Client** : 20 euros par mois

> Voici ce que je vous propose. Livret A : alimenter le livret existant, sans en ouvrir un second. Épargne disponible ; adaptée à une réserve ou un projet sans immobilisation. Livret de développement durable et solidaire (LDDS) : domicile fiscal français et imposition séparée déclarés ; épargne disponible. ⏎ Non proposé — Livret Jeune : hors de la tranche d'âge du Livret Jeune. Non proposé — Plan épargne logement (PEL) : besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. Livret d'épargne populaire (LEP) : éligibilité à vérifier (revenu fiscal de référence, nombre de parts fiscales, année du revenu fiscal, territoire fiscal), aucune inéligibilité déduite. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.3 ms — réponse attendue, lue par les règles</sub>

**10. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 28. C05 — refus et changement d'avis

**1. Client** : je veux un crédit conso

> Je peux vous aider à y voir clair, avec prudence. J'ai noté vos revenus de 1 900 € nets par mois. Vous remboursez déjà 150 € de crédit par mois. Quel montant souhaitez-vous emprunter ?

<sub>niveau 0 · credit_conso (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**2. Client** : non

> D'accord, on laisse ça de côté. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**3. Client** : finalement si

> Très bien, reprenons : un crédit. Quel montant souhaitez-vous emprunter ?

<sub>niveau 0 · credit_conso (mots_cles, 1.0) · 10.4 ms — demande claire (mots_cles)</sub>

**4. Client** : 10000

> Sur combien de mois souhaitez-vous rembourser ?

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**5. Client** : non je préfère 5000

> Bien sûr. Sur combien de mois souhaitez-vous rembourser ? Par exemple : 2 ans, ou 48 mois.

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**6. Client** : 24 mois

> Voici ce que je vous propose. Prêt personnel : mensualité indicative de 222 € sur 24 mois, soit 19,6 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Le seuil de prudence consommation est une heuristique interne, pas une obligation HCSF. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 6 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**7. Client** : pourquoi ?

> D'après votre simulation : Prêt personnel : Mensualité indicative de 222 € sur 24 mois, soit 19,6 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 383.4 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**8. Client** : c'est trop cher

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 277.7 ms · 1 LLM — confiance sous le seuil → compris</sub>

**9. Client** : laisse tomber

> D'accord. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (classifieur, 0.95) · 10.3 ms — demande claire (classifieur)</sub>

**10. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 29. C07 — anglais puis français

**1. Client** : I lost my card

> Je comprends, il faut agir vite. Faites opposition tout de suite : dans votre espace bancaire sécurisé, rubrique Opposition, ou en appelant votre conseiller. Je ne peux pas bloquer votre carte depuis cette conversation. Rappel : la banque ne vous demandera jamais votre code confidentiel.

<sub>niveau 1 · lost_or_stolen_card (interprete, 0.0) · 237.6 ms · 1 LLM — confiance sous le seuil → compris</sub>

**2. Client** : can you help me?

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 199.8 ms · 1 LLM — confiance sous le seuil → compris</sub>

**3. Client** : how do I block it

> Je comprends que votre demande concerne l'utilisation de votre carte. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · pin_blocked (classifieur, 0.76) · 9.6 ms — demande claire (classifieur)</sub>

**4. Client** : ok merci, je parle français en fait

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**5. Client** : je veux savoir combien coûte un crédit immobilier

> C'est un beau projet. J'ai noté vos revenus de 2 900 € nets par mois. Quel est le prix du bien que vous visez, et quelle part de vos 25 000 € d'épargne souhaitez-vous y consacrer ?

<sub>niveau 0 · credit_immobilier (mots_cles, 0.9) · 0.2 ms — demande claire (mots_cles)</sub>

**6. Client** : 220000

> Quelle part de vos 25 000 € d'épargne souhaitez-vous consacrer à l'achat ?

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**7. Client** : 30000

> Voici ce que je vous propose. Crédit immobilier : mensualité indicative de 1 014 € sur 300 mois, soit 35 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Budget indicatif sous ces hypothèses : environ 220 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**8. Client** : pourquoi ?

> parce que la durée du prêt est hors du cadre général de 25 ans. [2] parce que la mensualité est indicative et l'orientation est conditionnelle. [3] parce que le conseiller ne donne pas d'accord sans vérification des justificatifs.

<sub>niveau 2 · inconnue (aucun, 0.0) · 433.1 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**9. Client** : thank you

> Avec plaisir ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**10. Client** : bye

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 30. C04 — réponses très courtes, mots simples

**1. Client** : virement

> D'accord, je vous guide pas à pas. ⏎ À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · faire_virement (classifieur, 0.99) · 9.3 ms — demande claire (classifieur)</sub>

**2. Client** : oui

> Bien sûr. ⏎ À qui voulez-vous envoyer l'argent ? ⏎ Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 242.8 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**3. Client** : fils

> Quel montant voulez-vous envoyer ?

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**4. Client** : non

> D'accord, on laisse ça de côté. ⏎ Puis-je vous aider pour autre chose ?

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**5. Client** : 500

> Très bien, reprenons : un virement. ⏎ Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. ⏎ Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation.

<sub>niveau 0 · faire_virement (mots_cles, 1.0) · 9.6 ms — demande claire (mots_cles)</sub>

**6. Client** : oui

> D'accord. ⏎ Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (classifieur, 0.95) · 9.4 ms — demande claire (classifieur)</sub>

**7. Client** : merci

> Avec plaisir. ⏎ Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**8. Client** : carte

> Je comprends, il faut agir vite. ⏎ Faites opposition tout de suite : dans votre espace bancaire sécurisé, rubrique Opposition, ou en appelant votre conseiller. ⏎ Je ne peux pas bloquer votre carte depuis cette conversation. ⏎ Rappel : la banque ne vous demandera jamais votre code confidentiel. ⏎ « opposition » veut dire : le blocage définitif d'une carte perdue ou volée, pour que personne ne puisse s'en servir. ⏎ Passons maintenant à votre autre demande : l'utilisation de votre carte. Je comprends que votre demande concerne l'utilisation de votre carte. ⏎ Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. ⏎ Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 1 · lost_or_stolen_card (interprete, 0.0) · 236.1 ms · 1 LLM — confiance sous le seuil → compris</sub>

**9. Client** : perdue

> Je ne suis pas sûr de bien vous comprendre. ⏎ Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. ⏎ Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.87) · 9.2 ms — demande claire (classifieur)</sub>

**10. Client** : au revoir

> Au revoir, et bonne journée ! ⏎ Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

