# Conversations libres : 30 conversations rejouées (conversations_nouvelles.yaml)

Généré le 28/10/2026 à 11 h 23 sur ail, niveaux 1 et 2 actifs (qwen3:1.7b / qwen3:1.7b).

## Résumé

- 300 messages, dans 30 conversations.
- Niveaux : 0 : 150 · 1 : 122 · 2 : 28.
- Appels au LLM : 161. Latence p50 172.6 ms, p95 540 ms.
- Signaux à regarder : incompris : 29, repli du garde-fou : 16, hors de nos fiches : 6, clarification : 4, question fermée : 2, « Bonjour ! » : 1.

## 31. C08 — langage SMS et verlan, carte bloquée

**1. Client** : wesh ma cb elle marche pa

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 236.3 ms · 1 LLM — confiance sous le seuil → compris</sub>

**2. Client** : jsui au distrib la

> Pour bien vous aider, pouvez-vous préciser ? Par exemple : votre carte, un virement, des frais, votre épargne ou un projet de crédit.

<sub>niveau 1 · inconnue (aucun, 0.0) · 191.9 ms · 1 LLM — confiance sous le seuil → rien de net — ⚠ clarification</sub>

**3. Client** : elle a été avalé

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.91) · 9.7 ms — demande claire (classifieur)</sub>

**4. Client** : jfai koi

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 213.9 ms · 1 LLM — confiance sous le seuil → compris</sub>

**5. Client** : c chaud jai besoin de tune ce soir

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 205.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**6. Client** : jpeu faire un retrait sans carte ?

> D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 1 · faire_virement (interprete, 0.0) · 267.3 ms · 1 LLM — confiance sous le seuil → compris</sub>

**7. Client** : ok

> Bien sûr. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 189.2 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**8. Client** : et pour en avoir une nouvelle ca prend cb de tps

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 184.1 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**9. Client** : trkl merci

> Avec plaisir. À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**10. Client** : a+

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 190.3 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

## 32. C04 — client âgé, très formel, messages longs

**1. Client** : Bonjour Madame, je me permets de vous écrire car mon petit-fils m'a dit que je pouvais vous poser mes questions ici.

> Je ne suis pas sûr de bien vous comprendre. ⏎ Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. ⏎ Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.92) · 11.9 ms — demande claire (classifieur)</sub>

**2. Client** : Je souhaiterais envoyer un peu d'argent à ma petite-fille pour son anniversaire, elle va avoir dix-huit ans.

> D'accord, je vous guide pas à pas. ⏎ Quel montant voulez-vous envoyer ?

<sub>niveau 0 · faire_virement (classifieur, 0.83) · 11.6 ms — demande claire (classifieur)</sub>

**3. Client** : Ce serait pour ma petite fille Camille

> Je n'ai pas bien compris. ⏎ Quel montant voulez-vous envoyer ? ⏎ Par exemple : 200 €.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 219.7 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**4. Client** : Je pensais à cent cinquante euros, est-ce raisonnable ?

> Bonne idée de mettre de côté. ⏎ Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 1 · epargne_projet (interprete, 0.0) · 238.6 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**5. Client** : 150 €

> D'accord, je vous guide pas à pas. ⏎ Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. ⏎ Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation. ⏎ Passons maintenant à votre autre demande : un virement. Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. ⏎ Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation.

<sub>niveau 1 · faire_virement (interprete, 0.0) · 227.6 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**6. Client** : Je vous remercie. Pouvez-vous me rappeler ce qu'est un IBAN, je ne m'en souviens jamais ?

> Je ne peux pas prendre de rendez-vous pour vous : je n'ai aucun accès à votre compte. ⏎ Pour voir un conseiller, prenez rendez-vous depuis votre espace bancaire sécurisé, rubrique Rendez-vous, ou appelez votre agence. ⏎ Préparez votre projet : montant, durée, revenus. ⏎ Passons maintenant à votre autre demande : votre épargne. Bonne idée de mettre de côté. ⏎ Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.4 ms — règles</sub>

**7. Client** : Et où puis-je trouver le sien ?

> Je comprends que votre demande concerne la commande d'une carte. ⏎ Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. ⏎ Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. ⏎ Passons maintenant à votre autre demande : votre épargne. Bonne idée de mettre de côté. ⏎ Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 1 · order_physical_card (interprete, 0.0) · 256.5 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**8. Client** : Je préférerais vraiment en parler avec quelqu'un au téléphone.

> Je n'ai pas bien compris. ⏎ Dans combien de temps pensez-vous avoir besoin de cet argent ? ⏎ Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 200.9 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**9. Client** : Vous êtes bien aimable.

> Je n'ai pas bien compris. ⏎ Dans combien de temps pensez-vous avoir besoin de cet argent ? ⏎ Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 179.0 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**10. Client** : Je vous souhaite une excellente journée.

> Je n'ai pas bien compris. ⏎ Dans combien de temps pensez-vous avoir besoin de cet argent ? ⏎ Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 183.6 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

## 33. C01 — trois demandes dans un seul message

**1. Client** : j'ai perdu ma carte, je dois envoyer 200 euros à ma mère et j'ai des frais bizarres sur mon relevé

> Je n'ai aucun accès à vos relevés ni à votre compte : je ne peux pas les consulter. Je m'appuie seulement sur les informations de votre profil (revenus, épargne, crédits en cours). Pour un examen de vos relevés, un conseiller peut le faire avec vous.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**2. Client** : c'est fait pour l'opposition

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 0 · insatisfaction (classifieur, 0.91) · 10.6 ms — demande claire (classifieur)</sub>

**3. Client** : à ma mère

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.94) · 10.2 ms — demande claire (classifieur)</sub>

**4. Client** : 200

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 0 · insatisfaction (reponse_attendue, 1.0) · 10.0 ms — demande claire (reponse_attendue)</sub>

**5. Client** : et les frais alors ?

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 248.0 ms · 1 LLM — renvoi au contexte → compris</sub>

**6. Client** : c'était 8 euros

> Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 0 · extra_charge_on_statement (reponse_attendue, 1.0) · 10.5 ms — demande claire (reponse_attendue)</sub>

**7. Client** : c'est quoi une commission d'intervention

> Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais. ⏎ Passons maintenant à votre autre demande : une explication. Je n'ai pas cette information dans mes fiches. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · extra_charge_on_statement (mots_cles, 0.9) · 0.7 ms — plusieurs demandes nettes : traitées par ordre d'urgence — ⚠ hors de nos fiches</sub>

**8. Client** : ok je vois

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.94) · 10.1 ms — demande claire (classifieur)</sub>

**9. Client** : c'est tout pour moi

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 196.8 ms · 1 LLM — confiance sous le seuil → compris</sub>

**10. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 34. C07 — montants en lettres et en k

**1. Client** : je veux acheter une maison à deux cent mille euros

> C'est un beau projet. J'ai noté vos revenus de 2 900 € nets par mois. Quel est le prix du bien que vous visez, et quelle part de vos 25 000 € d'épargne souhaitez-vous y consacrer ?

<sub>niveau 0 · credit_immobilier (mots_cles, 0.9) · 0.2 ms — demande claire (mots_cles)</sub>

**2. Client** : j'ai 25k d'apport

> Quelle part de vos 25 000 € d'épargne souhaitez-vous consacrer à l'achat ?

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**3. Client** : et avec un bien à 180k ?

> Non proposé — Crédit immobilier : l'apport couvre le prix et les frais estimés : aucun emprunt nécessaire dans cette simulation. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**4. Client** : et si je mets trente mille d'apport ?

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 1 · epargne_projet (interprete, 0.0) · 276.8 ms · 1 LLM — confiance sous le seuil → compris</sub>

**5. Client** : pourquoi la mensualité baisse ?

> D'après votre simulation : Crédit immobilier n'est pas proposé : L'apport couvre le prix et les frais estimés : aucun emprunt nécessaire dans cette simulation. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · epargne_projet (reponse_attendue, 1.0) · 333.7 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**6. Client** : c'est quoi le reste à vivre

> reste à vivre : Ce qui vous reste chaque mois une fois payés vos charges et vos crédits. ⏎ Revenons à votre épargne : dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 0.4 ms — demande claire (mots_cles)</sub>

**7. Client** : et si on emprunte à deux avec mon conjoint ?

> C'est un beau projet. J'ai noté vos revenus de 2 900 € nets par mois. Quel est le prix du bien que vous visez, et quelle part de vos 25 000 € d'épargne souhaitez-vous y consacrer ?

<sub>niveau 1 · credit_immobilier (interprete, 0.0) · 326.5 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**8. Client** : il gagne 2000 par mois

> Quelle part de vos 25 000 € d'épargne souhaitez-vous consacrer à l'achat ?

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**9. Client** : je peux avoir un rendez-vous ?

> Je ne peux pas prendre de rendez-vous pour vous : je n'ai aucun accès à votre compte. Pour voir un conseiller, prenez rendez-vous depuis votre espace bancaire sécurisé, rubrique Rendez-vous, ou appelez votre agence. Préparez votre projet : montant, durée, revenus. ⏎ Revenons à un crédit : quelle part de vos 25 000 € d'épargne souhaitez-vous consacrer à l'achat ?

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**10. Client** : super merci

> Avec plaisir. Quelle part de vos 25 000 € d'épargne souhaitez-vous consacrer à l'achat ?

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

## 35. C02 — anglais d'un bout à l'autre

**1. Client** : hello, I was charged a fee I don't understand

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**2. Client** : it was 8 euros last week

> Je comprends que votre demande concerne le change ou l'étranger. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · fiat_currency_support (classifieur, 0.94) · 10.3 ms — demande claire (classifieur)</sub>

**3. Client** : why do you charge that?

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 0 · extra_charge_on_statement (classifieur, 1.0) · 10.5 ms — demande claire (classifieur)</sub>

**4. Client** : can I get a refund?

> Je comprends que votre demande concerne des frais ou une opération contestée. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · request_refund (classifieur, 1.0) · 11.6 ms — demande claire (classifieur)</sub>

**5. Client** : I want to talk to someone

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 200.8 ms · 1 LLM — confiance sous le seuil → compris</sub>

**6. Client** : what is an overdraft?

> Je n'ai pas cette information dans mes fiches. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · question_definition (classifieur, 0.8) · 21.4 ms — aucune fiche assez proche : retour aux règles — ⚠ hors de nos fiches — sources : Livret de développement durable et solidaire (LDDS), Emprunter pour un logement : durée maximale et taux d'effort (HCSF), agios</sub>

**7. Client** : how do I send money to my brother?

> D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · faire_virement (classifieur, 1.0) · 10.2 ms — demande claire (classifieur)</sub>

**8. Client** : to my brother

> Bien sûr. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 233.8 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**9. Client** : 100 euros

> Bien sûr. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 234.1 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**10. Client** : thanks, bye

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 36. C06 — colère, émojis, menace de partir

**1. Client** : 😡😡😡 encore des frais !!!

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 225.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**2. Client** : vous vous foutez de moi

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 0 · insatisfaction (classifieur, 0.9) · 9.2 ms — demande claire (classifieur)</sub>

**3. Client** : je vais changer de banque

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 228.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**4. Client** : c'est la troisième fois ce mois ci

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 249.7 ms · 1 LLM — confiance sous le seuil → compris</sub>

**5. Client** : comment je fais une réclamation 🙄

> En cas de désaccord, adressez d'abord une réclamation à votre banque : à votre conseiller, puis au service réclamations. Si la réponse ne vous convient pas, ou sans réponse, vous pouvez saisir gratuitement le médiateur bancaire. [1]

<sub>niveau 2 · insatisfaction (classifieur, 0.9) · 460.5 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Faire une réclamation, Livret Jeune, Carte perdue ou volée</sub>

**6. Client** : et si personne répond ?

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 264.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**7. Client** : c'est qui le médiateur ?

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 236.2 ms · 1 LLM — confiance sous le seuil → compris</sub>

**8. Client** : bon ok

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.83) · 9.9 ms — demande claire (classifieur)</sub>

**9. Client** : merci quand même 🙏

> Avec plaisir ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**10. Client** : bye

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 37. C04 — fraude, faux conseiller au téléphone

**1. Client** : un monsieur m'a appelé en disant qu'il était de la banque

> Je ne suis pas sûr de bien vous comprendre. ⏎ Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. ⏎ Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 209.4 ms · 1 LLM — confiance sous le seuil → compris</sub>

**2. Client** : il m'a demandé mon code pour sécuriser mon compte

> Ne donnez jamais votre code confidentiel, ni vos identifiants, à personne : ni par téléphone, ni par SMS, ni par mail, même à quelqu'un qui se présente comme la banque. ⏎ La banque ne vous les demandera jamais. ⏎ Si vous l'avez déjà donné, faites opposition sur votre carte tout de suite, dans votre espace bancaire sécurisé, et prévenez votre conseiller. ⏎ « opposition » veut dire : le blocage définitif d'une carte perdue ou volée, pour que personne ne puisse s'en servir.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.2 ms — règles</sub>

**3. Client** : je lui ai donné

> D'accord, je vous guide pas à pas. ⏎ À qui voulez-vous envoyer l'argent ?

<sub>niveau 1 · faire_virement (interprete, 0.0) · 229.1 ms · 1 LLM — confiance sous le seuil → compris</sub>

**4. Client** : qu'est-ce que je dois faire maintenant ?

> Je n'ai pas bien compris. ⏎ À qui voulez-vous envoyer l'argent ? ⏎ Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 244.7 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**5. Client** : comment je fais opposition ?

> D'après nos fiches : En cas de perte ou de vol de votre carte, faites opposition immédiatement : depuis votre espace bancaire sécurisé, rubrique Opposition, ou en appelant votre conseiller. ⏎ Les opérations frauduleuses faites après l'opposition ne sont pas à votre charge. ⏎ La banque ne vous demandera jamais votre code confidentiel. ⏎ [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · faire_virement (reponse_attendue, 1.0) · 355.7 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Carte perdue ou volée, opposition, Faire une réclamation</sub>

**6. Client** : j'ai aussi reçu un SMS avec un lien

> Je n'ai pas bien compris. ⏎ À qui voulez-vous envoyer l'argent ? ⏎ Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 221.2 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**7. Client** : j'ai cliqué dessus

> Je n'ai pas bien compris. ⏎ À qui voulez-vous envoyer l'argent ? ⏎ Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 178.9 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**8. Client** : est-ce que je vais perdre mon argent ?

> Je n'ai pas bien compris. ⏎ À qui voulez-vous envoyer l'argent ? ⏎ Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 221.7 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**9. Client** : je veux parler à mon conseiller

> Je suis désolé pour ce désagrément. ⏎ Je n'ai aucun accès à votre compte, mais votre réclamation compte. ⏎ Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. ⏎ Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis. ⏎ Passons maintenant à votre autre demande : un virement. D'accord, je vous guide pas à pas. ⏎ À qui voulez-vous envoyer l'argent ?

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 238.6 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**10. Client** : merci beaucoup

> Avec plaisir. ⏎ À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

## 38. C08 — étudiant, premier budget, jargon

**1. Client** : salut je suis étudiant et je sais pas trop gérer mon argent

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**2. Client** : je voudrais mettre un peu de côté

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 1 · epargne_projet (interprete, 0.0) · 264.9 ms · 1 LLM — confiance sous le seuil → compris (réponse écartée : absente du message)</sub>

**3. Client** : pour dans 1 an

> Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**4. Client** : genre 30 balles par mois

> Voici ce que je vous propose. Livret Jeune : à 20 ans, tranche d'âge compatible ; épargne disponible. Livret A : épargne disponible ; adaptée à une réserve ou un projet sans immobilisation. ⏎ Non proposé — Livret de développement durable et solidaire (LDDS) : domicile fiscal français et imposition séparée nécessaires. Non proposé — Livret d'épargne populaire (LEP) : domicile fiscal français et imposition séparée nécessaires. Non proposé — Plan épargne logement (PEL) : besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.3 ms — réponse attendue, lue par les règles</sub>

**5. Client** : c'est quoi la différence entre le livret jeune et le livret A

> Quelle est la différence entre le Livret Jeune et le Livret A ? [1] Le Livret Jeune est destiné aux jeunes de 12 à 25 ans, avec un plafond des versements de 1 600 €. [2] Le Livret A est pour tout le monde, y compris les mineurs, avec un plafond des versements de 22 950 €.

<sub>niveau 2 · inconnue (aucun, 0.0) · 604.5 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Livret Jeune, Livret Jeune, Livret A</sub>

**6. Client** : et ça rapporte combien ?

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 0 · extra_charge_on_statement (classifieur, 0.95) · 10.2 ms — demande claire (classifieur)</sub>

**7. Client** : je voudrais aussi un prêt étudiant

> C'est une question fréquente pendant les études. De quel montant auriez-vous besoin, à peu près ?

<sub>niveau 0 · pret_etudiant (mots_cles, 0.9) · 0.2 ms — demande claire (mots_cles)</sub>

**8. Client** : 3000 euros

> Voici ce que je vous propose. Prêt étudiant : piste LBP compatible avec l'âge, le montant et le statut déclarés ; justificatif étudiant et étude du prêteur nécessaires. Différé selon contrat, sous réserve d'acceptation du prêteur. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · pret_etudiant (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**9. Client** : je rembourse à partir de quand ?

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais. ⏎ Passons maintenant à votre autre demande : l'alimentation de votre compte. Je comprends que votre demande concerne l'alimentation de votre compte. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 345.4 ms · 1 LLM — confiance sous le seuil → compris</sub>

**10. Client** : cimer

> Pour être sûr de bien vous aider : votre demande concerne-t-elle votre compte ou votre identité, ou une explication ?

<sub>niveau 1 · inconnue (aucun, 0.0) · 182.5 ms · 1 LLM — confiance sous le seuil → rien de net — ⚠ question fermée</sub>

## 39. C05 — crédit énorme, hésitations, corrections

**1. Client** : je veux emprunter 50000 pour une voiture

> Je peux vous aider à y voir clair, avec prudence. J'ai noté vos revenus de 1 900 € nets par mois. Vous remboursez déjà 150 € de crédit par mois. Sur combien de mois souhaitez-vous rembourser ?

<sub>niveau 0 · credit_conso (classifieur, 0.99) · 10.7 ms — demande claire (classifieur)</sub>

**2. Client** : euh non plutôt 30000

> Bien sûr. Sur combien de mois souhaitez-vous rembourser ? Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · credit_conso (reponse_attendue, 1.0) · 211.7 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**3. Client** : sur 5 ans

> Non proposé — Prêt personnel : mensualité indicative de 581 € sur 60 mois, soit 38,4 % des revenus avec les crédits en cours. Projet non retenu dans cette simulation ; aucun refus bancaire n'est prononcé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Le seuil de prudence consommation est une heuristique interne, pas une obligation HCSF. Taux d'effort indicatif de 38,4 % : au-delà du repère de 35 %. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 6 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**4. Client** : attends, sur 7 ans plutôt

> Voici ce que je vous propose. Prêt personnel : mensualité indicative de 439 € sur 84 mois, soit 31 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Le seuil de prudence consommation est une heuristique interne, pas une obligation HCSF. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 6 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 10.4 ms — demande claire (reponse_attendue)</sub>

**5. Client** : c'est refusé ?

> Je comprends que votre demande concerne l'utilisation de votre carte. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 1 · card_not_working (interprete, 0.0) · 244.0 ms · 1 LLM — confiance sous le seuil → compris</sub>

**6. Client** : pourquoi ?

> D'après votre simulation : Prêt personnel : Mensualité indicative de 439 € sur 84 mois, soit 31 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 478.4 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**7. Client** : et avec 15000 ?

> Pour bien vous aider, pouvez-vous préciser ? Par exemple : votre carte, un virement, des frais, votre épargne ou un projet de crédit.

<sub>niveau 1 · inconnue (aucun, 0.0) · 268.7 ms · 1 LLM — confiance sous le seuil → compris — ⚠ clarification</sub>

**8. Client** : sur 48 mois

> Je peux vous aider à y voir clair, avec prudence. J'ai noté vos revenus de 1 900 € nets par mois. Vous remboursez déjà 150 € de crédit par mois. Quel montant souhaitez-vous emprunter ?

<sub>niveau 1 · credit_conso (interprete, 0.0) · 216.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**9. Client** : c'est quoi le TAEG

> TAEG : Le coût total d'un crédit (intérêts, frais, assurance obligatoire) exprimé en pourcentage par an. C'est le chiffre qui permet de comparer deux offres. ⏎ Revenons à un crédit : quel montant souhaitez-vous emprunter ?

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 0.4 ms — demande claire (mots_cles)</sub>

**10. Client** : bon je vais réfléchir

> Bien sûr, prenez le temps d'y réfléchir. Je reste disponible si vous avez une question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 40. C03 — épargne enfants, nombres en lettres, renvois

**1. Client** : je voudrais ouvrir un livret pour ma fille

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · epargne_projet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**2. Client** : elle a dix ans

> Bien sûr. Dans combien de temps pensez-vous avoir besoin de cet argent ? Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 234.0 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**3. Client** : dans huit ans environ

> Bien sûr. Dans combien de temps pensez-vous avoir besoin de cet argent ? Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 234.6 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**4. Client** : cinquante euros par mois

> Bien sûr. Dans combien de temps pensez-vous avoir besoin de cet argent ? Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 240.7 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**5. Client** : et pour mon fils de 15 ans ?

> Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**6. Client** : pourquoi pas un PEL ?

> D'après nos fiches : Plan épargne logement (PEL) : Un plan par personne. Retrait anticipé entraînant clôture et conséquences selon ancienneté ; les fonds ne sont pas définitivement bloqués. Plafond des versements : 61 200 €. Durée minimale : 4 ans. Versement initial minimum : 225 € ; versements annuels minimum : 540 €. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · epargne_projet (reponse_attendue, 1.0) · 539.5 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Plan épargne logement (PEL), PEL, Livret d'épargne populaire (LEP)</sub>

**7. Client** : c'est quoi le plafond du livret A ?

> D'après nos fiches : Livret A : Le livret d'épargne le plus courant : argent disponible à tout moment, intérêts sans impôt, taux fixé par l'État, plafond de 22 950 €. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · question_definition (mots_cles, 0.9) · 287.9 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Livret A, Livret A, Livret Jeune</sub>

**8. Client** : et le LDDS ?

> Bien sûr. Combien pouvez-vous mettre de côté chaque mois ? Par exemple : 200 €.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 278.5 ms · 1 LLM — réponse libre, illisible par les règles ; renvoi au contexte → compris</sub>

**9. Client** : mes enfants peuvent avoir un LDDS ?

> Bien sûr. Combien pouvez-vous mettre de côté chaque mois ? Par exemple : 200 €.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 244.6 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**10. Client** : merci, bonne soirée

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 41. C01 — hors sujet en série

**1. Client** : quel temps il fait demain à Bordeaux ?

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.98) · 9.4 ms — demande claire (classifieur)</sub>

**2. Client** : t'es une IA ?

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 203.4 ms · 1 LLM — confiance sous le seuil → compris</sub>

**3. Client** : raconte moi une blague

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.91) · 10.2 ms — demande claire (classifieur)</sub>

**4. Client** : qui a gagné le match hier

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.93) · 10.3 ms — demande claire (classifieur)</sub>

**5. Client** : tu peux m'aider à faire mes devoirs de maths ?

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 299.4 ms · 1 LLM — confiance sous le seuil → compris</sub>

**6. Client** : ok et la bourse, je dois acheter des actions Tesla ?

> C'est un beau projet. J'ai noté vos revenus de 3 200 € nets par mois. Quel est le prix du bien que vous visez, et quelle part de vos 8 000 € d'épargne souhaitez-vous y consacrer ?

<sub>niveau 0 · credit_immobilier (classifieur, 0.88) · 10.7 ms — demande claire (classifieur)</sub>

**7. Client** : bon, j'ai une vraie question : mon virement n'est pas arrivé

> Je n'ai pas bien compris. Quel est le prix du bien que vous visez, et quelle part de vos 8 000 € d'épargne souhaitez-vous y consacrer ? Par exemple : 200 €.

<sub>niveau 1 · credit_immobilier (reponse_attendue, 1.0) · 268.0 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**8. Client** : je l'ai fait hier à mon frère

> D'accord, je vous guide pas à pas. Quel montant voulez-vous envoyer ?

<sub>niveau 1 · faire_virement (interprete, 0.0) · 261.1 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**9. Client** : c'est normal ?

> Je n'ai pas bien compris. Quel montant voulez-vous envoyer ? Par exemple : 200 €.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 210.2 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**10. Client** : merci

> Avec plaisir. Quel montant voulez-vous envoyer ?

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

## 42. C07 — primo-accédante, questions ouvertes en série

**1. Client** : c'est mon premier achat immobilier, par où je commence ?

> C'est un beau projet. J'ai noté vos revenus de 2 900 € nets par mois. Quel est le prix du bien que vous visez, et quelle part de vos 25 000 € d'épargne souhaitez-vous y consacrer ?

<sub>niveau 0 · credit_immobilier (mots_cles, 0.9) · 0.2 ms — demande claire (mots_cles)</sub>

**2. Client** : j'ai droit au prêt à taux zéro ?

> Bien sûr. Quel est le prix du bien que vous visez, et quelle part de vos 25 000 € d'épargne souhaitez-vous y consacrer ? Par exemple : 200 €.

<sub>niveau 1 · credit_immobilier (reponse_attendue, 1.0) · 270.9 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**3. Client** : c'est quoi l'apport minimum ?

> D'après nos fiches : apport personnel : L'argent que vous mettez vous-même dans un achat, sans l'emprunter. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · question_definition (mots_cles, 0.9) · 424.8 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : apport personnel, Compte épargne logement (CEL), Livret de développement durable et solidaire (LDDS)</sub>

**4. Client** : on peut emprunter sur 30 ans ?

> Bien sûr. Quel est le prix du bien que vous visez, et quelle part de vos 25 000 € d'épargne souhaitez-vous y consacrer ? Par exemple : 200 €.

<sub>niveau 1 · credit_immobilier (reponse_attendue, 1.0) · 297.5 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**5. Client** : c'est quoi le HCSF ?

> D'après nos fiches : Pour emprunter et acheter un logement, le cadre du HCSF limite la durée du crédit immobilier à 25 ans et le taux d'effort à 35 % des revenus, assurance comprise. La banque garde une part de flexibilité et décide après étude du dossier : aucun accord n'est automatique. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · question_definition (interprete, 0.0) · 954.4 ms · 2 LLM — réponse libre, illisible par les règles → compris (réponse écartée : absente du message) ; aucun terme du glossaire : nos fiches — ⚠ repli du garde-fou — sources : Emprunter pour un logement : durée maximale et taux d'effort (HCSF), Crédit immobilier, reste à vivre</sub>

**6. Client** : les frais de notaire c'est combien ?

> Les frais de notaire sont estimés à environ 7,5 % dans l'ancien et 2,5 % dans le neuf, selon le prix du logement [1]. Le notaire précise le montant exact.

<sub>niveau 2 · credit_immobilier (reponse_attendue, 1.0) · 335.8 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Frais d'acquisition (notaire), frais de notaire, Commission d'intervention</sub>

**7. Client** : c'est quoi une assurance emprunteur

> assurance emprunteur : Une assurance qui rembourse tout ou partie de votre crédit si vous ne pouvez plus le faire (décès, invalidité…). Elle est presque toujours demandée pour un crédit immobilier.

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 0.5 ms — demande claire (mots_cles)</sub>

**8. Client** : le bien coûte 230000

> Quelle part de vos 25 000 € d'épargne souhaitez-vous consacrer à l'achat ?

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**9. Client** : 15000

> Non proposé — Crédit immobilier : mensualité indicative de 1 140 € sur 300 mois, soit 39,3 % des revenus avec les crédits en cours. Projet non retenu dans cette simulation ; aucun refus bancaire n'est prononcé. Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Taux d'effort indicatif de 39,3 % : au-delà du repère de 35 %. Budget indicatif sous ces hypothèses : environ 206 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager. ⏎ Passons maintenant à votre autre demande : un crédit. Non proposé — Crédit immobilier : mensualité indicative de 1 140 € sur 300 mois, soit 39,3 % des revenus avec les crédits en cours. Projet non retenu dans cette simulation ; aucun refus bancaire n'est prononcé. Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Taux d'effort indicatif de 39,3 % : au-delà du repère de 35 %. Budget indicatif sous ces hypothèses : environ 206 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.4 ms — réponse attendue, lue par les règles</sub>

**10. Client** : merci pour tout

> Avec plaisir ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 43. C02 — découvert, rejet de prélèvement, situation fragile

**1. Client** : je suis à découvert depuis 2 semaines

> Je comprends que votre demande concerne la commande d'une carte. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · card_arrival (classifieur, 0.84) · 10.7 ms — demande claire (classifieur)</sub>

**2. Client** : j'ai eu un prélèvement rejeté

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 270.3 ms · 1 LLM — confiance sous le seuil → compris</sub>

**3. Client** : ça va me coûter combien ?

> Je comprends que votre demande concerne des frais ou une opération contestée. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · top_up_by_bank_transfer_charge (classifieur, 0.96) · 9.3 ms — demande claire (classifieur)</sub>

**4. Client** : je suis au chômage en ce moment

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 197.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**5. Client** : est-ce qu'il y a une aide ?

> Pour bien vous aider, pouvez-vous préciser ? Par exemple : votre carte, un virement, des frais, votre épargne ou un projet de crédit.

<sub>niveau 1 · inconnue (aucun, 0.0) · 202.3 ms · 1 LLM — confiance sous le seuil → rien de net — ⚠ clarification</sub>

**6. Client** : c'est quoi l'offre clientèle fragile

> L'offre clientèle fragile est une offre spéciale pour les clients en situation de fragilité financière, avec des frais d'incidents plafonnés [1]. La commission d'intervention est prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé, et elle est plafonnée à 8 € par opération et 80 € par mois [2].

<sub>niveau 2 · question_definition (classifieur, 0.96) · 599.7 ms · 1 LLM — terme absent du glossaire : recherche dans nos fiches — sources : Offre clientèle fragile, Commission d'intervention, Emprunter pour un logement : durée maximale et taux d'effort (HCSF)</sub>

**7. Client** : comment je fais pour l'avoir ?

> D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 1 · faire_virement (interprete, 0.0) · 300.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**8. Client** : je peux avoir un petit crédit pour finir le mois ?

> Je peux vous aider à y voir clair, avec prudence. J'ai noté vos revenus de 1 850 € nets par mois. Quel montant souhaitez-vous emprunter ?

<sub>niveau 1 · credit_conso (interprete, 0.0) · 224.7 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**9. Client** : 500 euros

> Sur combien de mois souhaitez-vous rembourser ?

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**10. Client** : ok merci

> Avec plaisir. Sur combien de mois souhaitez-vous rembourser ?

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

## 44. C06 — fermeture de compte, données, RGPD

**1. Client** : je veux clôturer mon compte

> Je comprends que votre demande concerne votre compte ou votre identité. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · terminate_account (classifieur, 0.77) · 10.4 ms — demande claire (classifieur)</sub>

**2. Client** : vous allez garder mes données ?

> Je n'ai aucun accès à vos relevés ni à votre compte : je ne peux pas les consulter. Je m'appuie seulement sur les informations de votre profil (revenus, épargne, crédits en cours). Pour un examen de vos relevés, un conseiller peut le faire avec vous.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**3. Client** : c'est quoi le RGPD

> Je n'ai pas cette information dans mes fiches. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · question_definition (interprete, 0.0) · 501.9 ms · 1 LLM — aucune fiche assez proche : retour aux règles — ⚠ hors de nos fiches — sources : LEP, Prêt personnel, Livret de développement durable et solidaire (LDDS)</sub>

**4. Client** : et mon livret A il devient quoi si je pars ?

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 1 · epargne_projet (interprete, 0.0) · 241.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**5. Client** : je peux transférer mon argent ailleurs ?

> D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 1 · faire_virement (interprete, 0.0) · 308.4 ms · 1 LLM — réponse libre, illisible par les règles → compris (réponse écartée : absente du message)</sub>

**6. Client** : combien de temps ça prend ?

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 253.4 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**7. Client** : il y a des frais pour partir ?

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais. ⏎ Passons maintenant à votre autre demande : un virement. D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 229.9 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**8. Client** : je veux un rendez-vous

> Je ne peux pas prendre de rendez-vous pour vous : je n'ai aucun accès à votre compte. Pour voir un conseiller, prenez rendez-vous depuis votre espace bancaire sécurisé, rubrique Rendez-vous, ou appelez votre agence. Préparez votre projet : montant, durée, revenus. ⏎ Revenons à un virement : à qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**9. Client** : non

> D'accord, on laisse ça de côté. Puis-je vous aider pour autre chose ? ⏎ Passons maintenant à votre autre demande : votre épargne. Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**10. Client** : au revoir

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 45. C04 — deuil, sujet sensible

**1. Client** : mon épouse est décédée le mois dernier

> Je suis désolé pour ce désagrément. ⏎ Je n'ai aucun accès à votre compte, mais votre réclamation compte. ⏎ Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. ⏎ Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 198.3 ms · 1 LLM — confiance sous le seuil → compris</sub>

**2. Client** : qu'est-ce qui se passe pour notre compte joint ?

> L’assistant n’a aucun accès à votre compte et ne réalise aucune opération : ni virement, ni opposition, ni modification. ⏎ Il explique, conseille à partir de règles publiques et vous oriente vers votre espace bancaire sécurisé ou un conseiller [1].

<sub>niveau 2 · question_definition (interprete, 0.0) · 736.6 ms · 2 LLM — confiance sous le seuil → compris ; aucun terme du glossaire : nos fiches — sources : Ce que l'assistant peut faire, agios, Compte épargne logement (CEL)</sub>

**3. Client** : je ne comprends rien à toutes ces démarches

> Je n'ai aucun accès à votre compte, mais votre réclamation compte. ⏎ Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. ⏎ Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 0 · insatisfaction (classifieur, 0.94) · 10.8 ms — demande claire (classifieur)</sub>

**4. Client** : parlez moi simplement s'il vous plaît

> Je ne suis pas sûr de bien vous comprendre. ⏎ Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. ⏎ Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.96) · 10.8 ms — demande claire (classifieur)</sub>

**5. Client** : est-ce que je peux encore utiliser la carte ?

> D'après nos fiches : En cas de perte ou de vol de votre carte, faites opposition immédiatement : depuis votre espace bancaire sécurisé, rubrique Opposition, ou en appelant votre conseiller. ⏎ Les opérations frauduleuses faites après l'opposition ne sont pas à votre charge. ⏎ La banque ne vous demandera jamais votre code confidentiel. ⏎ [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 382.2 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Carte perdue ou volée, Faire une réclamation, Ce que l'assistant peut faire</sub>

**6. Client** : je dois faire un virement pour les pompes funèbres

> D'accord, je vous guide pas à pas. ⏎ À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · faire_virement (mots_cles, 0.9) · 0.3 ms — demande claire (mots_cles)</sub>

**7. Client** : aux pompes funèbres

> Je n'ai pas bien compris. ⏎ À qui voulez-vous envoyer l'argent ? ⏎ Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 236.1 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**8. Client** : 2400 euros

> Bien sûr. ⏎ À qui voulez-vous envoyer l'argent ? ⏎ Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 245.4 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**9. Client** : merci de votre patience

> Avec plaisir. ⏎ À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**10. Client** : au revoir

> Au revoir, et bonne journée ! ⏎ Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 46. C08 — fautes d'orthographe très lourdes

**1. Client** : je veu fair un viremant

> D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · faire_virement (classifieur, 0.99) · 9.5 ms — demande claire (classifieur)</sub>

**2. Client** : a mon coloc

> Bien sûr. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 213.6 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**3. Client** : pour le loyé

> Bien sûr. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 238.4 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**4. Client** : 350

> Bien sûr. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 213.3 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**5. Client** : sa arive quand

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 178.7 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**6. Client** : jai u des fré sur mon conte

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 229.6 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**7. Client** : pk

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 164.5 ms · 1 LLM — réponse libre, illisible par les règles → rien de net — ⚠ incompris</sub>

**8. Client** : c koi le decouver

> découvert autorisé : La possibilité, prévue avec votre banque, d'avoir un solde négatif jusqu'à un certain montant. Il coûte des agios.

<sub>niveau 1 · question_definition (interprete, 0.0) · 214.1 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**9. Client** : jpeu epargné ou pa

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 1 · epargne_projet (interprete, 0.0) · 217.2 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**10. Client** : mrc

> Je n'ai pas bien compris. Dans combien de temps pensez-vous avoir besoin de cet argent ? Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 172.1 ms · 1 LLM — réponse libre, illisible par les règles → rien de net — ⚠ incompris</sub>

## 47. C05 — parenthèse au milieu d'un crédit

**1. Client** : je veux un crédit pour des travaux

> Je peux vous aider à y voir clair, avec prudence. J'ai noté vos revenus de 1 900 € nets par mois. Vous remboursez déjà 150 € de crédit par mois. Quel montant souhaitez-vous emprunter ?

<sub>niveau 0 · credit_conso (classifieur, 1.0) · 10.5 ms — demande claire (classifieur)</sub>

**2. Client** : 15000

> Sur combien de mois souhaitez-vous rembourser ?

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**3. Client** : attends j'ai perdu ma carte je crois

> Je comprends, il faut agir vite. Faites opposition tout de suite : dans votre espace bancaire sécurisé, rubrique Opposition, ou en appelant votre conseiller. Je ne peux pas bloquer votre carte depuis cette conversation. Rappel : la banque ne vous demandera jamais votre code confidentiel. ⏎ Revenons à un crédit : sur combien de mois souhaitez-vous rembourser ?

<sub>niveau 0 · lost_or_stolen_card (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**4. Client** : non c'est bon je l'ai retrouvée

> D'accord, on laisse ça de côté. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**5. Client** : on en était où ?

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 203.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**6. Client** : sur 3 ans

> Très bien, reprenons : un crédit. Voici ce que je vous propose. Prêt personnel : mensualité indicative de 457 € sur 36 mois, soit 31,9 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Le seuil de prudence consommation est une heuristique interne, pas une obligation HCSF. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 6 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_conso (mots_cles, 1.0) · 9.2 ms — demande claire (mots_cles)</sub>

**7. Client** : et sur 5 ans ça fait combien ?

> Voici ce que je vous propose. Prêt personnel : mensualité indicative de 290 € sur 60 mois, soit 23,2 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Le seuil de prudence consommation est une heuristique interne, pas une obligation HCSF. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 6 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 9.2 ms — demande claire (reponse_attendue)</sub>

**8. Client** : c'est quoi le taux d'endettement

> taux d'endettement : La part de vos revenus qui part chaque mois dans vos crédits. Pour un crédit immobilier, elle ne doit pas dépasser 35 %.

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 0.5 ms — demande claire (mots_cles)</sub>

**9. Client** : le mien il est de combien ?

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 1 · epargne_projet (interprete, 0.0) · 267.9 ms · 1 LLM — confiance sous le seuil → compris</sub>

**10. Client** : merci

> Avec plaisir. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

## 48. C03 — messages vides, ponctuation, menu

**1. Client** : ?

> Pour bien vous aider, pouvez-vous préciser ? Par exemple : votre carte, un virement, des frais, votre épargne ou un projet de crédit.

<sub>niveau 1 · inconnue (aucun, 0.0) · 194.5 ms · 1 LLM — confiance sous le seuil → rien de net — ⚠ clarification</sub>

**2. Client** : aide

> Je n'ai aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 1 · inconnue (aucun, 0.0) · 218.3 ms · 1 LLM — confiance sous le seuil → rien de net</sub>

**3. Client** : ...

> Je comprends que votre demande concerne votre compte ou votre identité. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · verify_source_of_funds (classifieur, 0.78) · 10.4 ms — demande claire (classifieur)</sub>

**4. Client** : menu

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.8) · 9.7 ms — demande claire (classifieur)</sub>

**5. Client** : épargne

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 1 · epargne_projet (interprete, 0.0) · 262.1 ms · 1 LLM — confiance sous le seuil → compris</sub>

**6. Client** : ???

> Bien sûr. Dans combien de temps pensez-vous avoir besoin de cet argent ? Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 214.6 ms · 1 LLM — réponse libre, illisible par les règles → compris (réponse écartée : absente du message)</sub>

**7. Client** : dans 3 ans

> Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**8. Client** : 100

> Voici ce que je vous propose. Livret A : alimenter le livret existant, sans en ouvrir un second. Épargne disponible ; adaptée à une réserve ou un projet sans immobilisation. Livret de développement durable et solidaire (LDDS) : domicile fiscal français et imposition séparée déclarés ; épargne disponible. ⏎ Non proposé — Livret Jeune : hors de la tranche d'âge du Livret Jeune. Non proposé — Plan épargne logement (PEL) : besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. Livret d'épargne populaire (LEP) : éligibilité à vérifier (revenu fiscal de référence, nombre de parts fiscales, année du revenu fiscal, territoire fiscal), aucune inéligibilité déduite. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**9. Client** : pourquoi

> Parce que l’âge du client est hors de la tranche d’âge du Livret Jeune.  
Pourquoi [2] ? Parce que le besoin de disponibilité est hors de l’horizon court du Plan épargne logement.  
Pourquoi [3] ? Parce que le Livret A est adapté à une réserve ou un projet sans immobilisation.

<sub>niveau 2 · inconnue (aucun, 0.0) · 545.0 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**10. Client** : ok

> D'accord. Puis-je vous aider pour autre chose ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 239.4 ms · 1 LLM — confiance sous le seuil → compris</sub>

## 49. C01 — mélange de langues, darija et anglais

**1. Client** : salam, j'ai un problème avec ma carte

> Je comprends, il faut agir vite. Faites opposition tout de suite : dans votre espace bancaire sécurisé, rubrique Opposition, ou en appelant votre conseiller. Je ne peux pas bloquer votre carte depuis cette conversation. Rappel : la banque ne vous demandera jamais votre code confidentiel. ⏎ Passons maintenant à votre autre demande : l'utilisation de votre carte. Je comprends que votre demande concerne l'utilisation de votre carte. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 1 · lost_or_stolen_card (interprete, 0.0) · 293.1 ms · 1 LLM — confiance sous le seuil → compris</sub>

**2. Client** : elle marche plus f l'étranger, I'm in Spain

> Je comprends que votre demande concerne le change ou l'étranger. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · country_support (classifieur, 0.78) · 9.5 ms — demande claire (classifieur)</sub>

**3. Client** : j'ai besoin d'argent urgent

> D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 1 · faire_virement (interprete, 0.0) · 254.5 ms · 1 LLM — confiance sous le seuil → compris</sub>

**4. Client** : my mom wants to send me money, comment elle fait ?

> Bien sûr. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 244.3 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**5. Client** : c'est quoi mon IBAN

> IBAN : Le numéro qui identifie un compte bancaire ; il faut le donner pour recevoir un virement. ⏎ Revenons à un virement : à qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 0.3 ms — demande claire (mots_cles)</sub>

**6. Client** : ok and what about fees abroad ?

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais. ⏎ Passons maintenant à votre autre demande : un virement. D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 239.6 ms · 1 LLM — réponse libre, illisible par les règles → compris (réponse écartée : absente du message)</sub>

**7. Client** : c'est cher les frais à l'étranger ?

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais. ⏎ Passons maintenant à votre autre demande : un virement. D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 264.8 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**8. Client** : bon je fais comment pour débloquer

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 204.0 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**9. Client** : shukran

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 176.2 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**10. Client** : bslama

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 170.4 ms · 1 LLM — réponse libre, illisible par les règles → rien de net — ⚠ incompris</sub>

## 50. C07 — projet locatif, variantes de durée et d'apport

**1. Client** : je veux investir dans un studio pour le louer

> C'est un beau projet. J'ai noté vos revenus de 2 900 € nets par mois. Quel est le prix du bien que vous visez, et quelle part de vos 25 000 € d'épargne souhaitez-vous y consacrer ?

<sub>niveau 0 · credit_immobilier (classifieur, 0.96) · 11.0 ms — demande claire (classifieur)</sub>

**2. Client** : 120000

> Quelle part de vos 25 000 € d'épargne souhaitez-vous consacrer à l'achat ?

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**3. Client** : j'ai 10000 d'apport

> Voici ce que je vous propose. Crédit immobilier : mensualité indicative de 584 € sur 300 mois, soit 20,1 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Budget indicatif sous ces hypothèses : environ 201 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.3 ms — réponse attendue, lue par les règles</sub>

**4. Client** : et sur 20 ans ?

> Voici ce que je vous propose. Crédit immobilier : mensualité indicative de 584 € sur 300 mois, soit 20,1 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Budget indicatif sous ces hypothèses : environ 201 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 10.1 ms — demande claire (reponse_attendue)</sub>

**5. Client** : et avec 30000 d'apport ?

> Voici ce que je vous propose. Crédit immobilier : mensualité indicative de 486 € sur 300 mois, soit 16,8 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Budget indicatif sous ces hypothèses : environ 220 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 10.5 ms — demande claire (reponse_attendue)</sub>

**6. Client** : les loyers comptent dans mes revenus ?

> Voici ce que je vous propose. Crédit immobilier : mensualité indicative de 486 € sur 300 mois, soit 16,8 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Budget indicatif sous ces hypothèses : environ 220 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (classifieur, 0.77) · 11.9 ms — demande claire (classifieur)</sub>

**7. Client** : c'est quoi le taux d'effort

> taux d'endettement : La part de vos revenus qui part chaque mois dans vos crédits. Pour un crédit immobilier, elle ne doit pas dépasser 35 %.

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 0.6 ms — demande claire (mots_cles)</sub>

**8. Client** : pourquoi 35 % ?

> D'après votre simulation : Un prêt immobilier sur 30 ans n'est pas proposé : Option de durée hors du cadre général de 25 ans modélisé. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 547.8 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**9. Client** : et si j'achète à 100000 ?

> Voici ce que je vous propose. Crédit immobilier : mensualité indicative de 381 € sur 300 mois, soit 13,1 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Budget indicatif sous ces hypothèses : environ 220 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 9.9 ms — demande claire (reponse_attendue)</sub>

**10. Client** : parfait merci

> Avec plaisir ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 51. C02 — réclamation polie mais insistante

**1. Client** : bonjour, je souhaite contester des frais

> Bonjour ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles) — ⚠ « Bonjour ! »</sub>

**2. Client** : on m'a prélevé 16 euros pour deux opérations

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 325.3 ms · 1 LLM — confiance sous le seuil → compris (réponse écartée : absente du message)</sub>

**3. Client** : je ne savais pas que mon solde était négatif

> Je n'ai pas cette information dans mes fiches. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · question_definition (interprete, 0.0) · 259.1 ms · 1 LLM — aucune fiche assez proche : retour aux règles — ⚠ hors de nos fiches — sources : Faire une réclamation, Carte perdue ou volée, découvert autorisé</sub>

**4. Client** : est-ce qu'on peut me rembourser ?

> Je comprends que votre demande concerne des frais ou une opération contestée. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · request_refund (classifieur, 0.82) · 8.8 ms — demande claire (classifieur)</sub>

**5. Client** : qui décide ?

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.85) · 9.2 ms — demande claire (classifieur)</sub>

**6. Client** : je veux faire une réclamation officielle

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 0 · insatisfaction (classifieur, 0.88) · 9.7 ms — demande claire (classifieur)</sub>

**7. Client** : en combien de temps on me répond ?

> D'après nos fiches : Livret Jeune : De 12 à 25 ans. Plafond des versements : 1 600 €. De 12 à 25 ans. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · question_definition (interprete, 0.0) · 567.1 ms · 2 LLM — confiance sous le seuil → compris ; aucun terme du glossaire : nos fiches — ⚠ repli du garde-fou — sources : Livret Jeune, Prêt étudiant, Prêt personnel</sub>

**8. Client** : et si la réponse ne me convient pas ?

> adressez d'abord une réclamation à votre banque : à votre conseiller, puis au service réclamations. Si la réponse ne vous convient pas, ou sans réponse, vous pouvez saisir gratuitement le médiateur bancaire. [1]

<sub>niveau 2 · question_definition (interprete, 0.0) · 700.8 ms · 2 LLM — confiance sous le seuil → compris ; aucun terme du glossaire : nos fiches — sources : Faire une réclamation, Carte perdue ou volée, Ce que l'assistant peut faire</sub>

**9. Client** : d'accord, merci pour ces informations

> Avec plaisir ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**10. Client** : bonne journée

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 52. C08 — questions sur l'assistant lui-même

**1. Client** : tu peux voir mon solde ?

> Je comprends que votre demande concerne votre compte ou votre identité. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 1 · edit_personal_details (interprete, 0.0) · 274.2 ms · 1 LLM — confiance sous le seuil → compris (réponse écartée : absente du message)</sub>

**2. Client** : tu peux faire un virement à ma place ?

> D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · faire_virement (mots_cles, 0.9) · 0.2 ms — demande claire (mots_cles)</sub>

**3. Client** : pourquoi tu peux pas ?

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 210.8 ms · 1 LLM — réponse libre, illisible par les règles → compris (réponse écartée : absente du message) — ⚠ incompris</sub>

**4. Client** : tu enregistres ce que je dis ?

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 177.2 ms · 1 LLM — réponse libre, illisible par les règles → rien de net — ⚠ incompris</sub>

**5. Client** : tu es fiable ?

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 184.0 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**6. Client** : d'où viennent tes informations ?

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 227.7 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**7. Client** : ok alors c'est quoi le plafond du livret jeune

> Le plafond du Livret Jeune est de 1 600 €. [1]

<sub>niveau 2 · question_definition (mots_cles, 0.9) · 208.2 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Livret Jeune, Livret Jeune, Livret d'épargne populaire (LEP)</sub>

**8. Client** : j'ai 20 ans j'y ai droit ?

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 244.3 ms · 1 LLM — réponse libre, illisible par les règles → compris — ⚠ incompris</sub>

**9. Client** : merci

> Avec plaisir. À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**10. Client** : salut

> Bien sûr. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

## 53. C05 — mariage, deux projets à la fois

**1. Client** : on se marie l'année prochaine et on veut acheter un appart

> C'est un beau projet. J'ai noté vos revenus de 1 900 € nets par mois. Vous remboursez déjà 150 € de crédits par mois. Quel est le prix du bien que vous visez, et quelle part de vos 1 500 € d'épargne souhaitez-vous y consacrer ?

<sub>niveau 0 · credit_immobilier (classifieur, 0.95) · 9.6 ms — demande claire (classifieur)</sub>

**2. Client** : je voudrais d'abord épargner pour le mariage

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · epargne_projet (mots_cles, 0.9) · 0.2 ms — demande claire (mots_cles)</sub>

**3. Client** : dans 1 an

> Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**4. Client** : 300 € par mois

> Voici ce que je vous propose. Livret A : alimenter le livret existant, sans en ouvrir un second. Épargne disponible ; adaptée à une réserve ou un projet sans immobilisation. Livret de développement durable et solidaire (LDDS) : domicile fiscal français et imposition séparée déclarés ; épargne disponible. ⏎ Non proposé — Livret Jeune : hors de la tranche d'âge du Livret Jeune. Non proposé — Plan épargne logement (PEL) : besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. Livret d'épargne populaire (LEP) : éligibilité à vérifier (revenu fiscal de référence, nombre de parts fiscales, année du revenu fiscal, territoire fiscal), aucune inéligibilité déduite. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide. ⏎ Passons maintenant à votre autre demande : un crédit. C'est un beau projet. Quel est le prix du bien que vous visez, et quelle part de vos 1 500 € d'épargne souhaitez-vous y consacrer ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.3 ms — réponse attendue, lue par les règles</sub>

**5. Client** : et pour l'appart maintenant

> Bien sûr. Quel est le prix du bien que vous visez, et quelle part de vos 1 500 € d'épargne souhaitez-vous y consacrer ? Par exemple : 200 €.

<sub>niveau 1 · credit_immobilier (reponse_attendue, 1.0) · 237.0 ms · 1 LLM — réponse libre, illisible par les règles ; renvoi au contexte → compris</sub>

**6. Client** : autour de 180000

> Quelle part de vos 1 500 € d'épargne souhaitez-vous consacrer à l'achat ?

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**7. Client** : on a 20000

> Non proposé — Crédit immobilier : mensualité indicative de 852 € sur 300 mois, soit 52,7 % des revenus avec les crédits en cours. Projet non retenu dans cette simulation ; aucun refus bancaire n'est prononcé. Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Taux d'effort indicatif de 52,7 % : au-delà du repère de 35 %. Budget indicatif sous ces hypothèses : environ 116 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**8. Client** : c'est possible ?

> Je n'ai pas cette information dans mes fiches. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · question_definition (interprete, 0.0) · 230.2 ms · 1 LLM — aucune fiche assez proche : retour aux règles — ⚠ hors de nos fiches — sources : reste à vivre, Livret Jeune, Prêt personnel</sub>

**9. Client** : pourquoi pas ?

> parce que la simulation ne propose pas de crédit immobilier, et [2] parce que le prêt immobilier sur 30 ans n'est pas proposé.

<sub>niveau 2 · inconnue (aucun, 0.0) · 288.7 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**10. Client** : ok on va réfléchir

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.8) · 9.5 ms — demande claire (classifieur)</sub>

## 54. C06 — application en panne, virement urgent

**1. Client** : l'appli plante quand je veux faire un virement

> D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · faire_virement (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**2. Client** : c'est urgent je dois payer mon loyer aujourd'hui

> Bien sûr. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 263.6 ms · 1 LLM — réponse libre, illisible par les règles → compris (réponse écartée : absente du message)</sub>

**3. Client** : à mon propriétaire

> Bien sûr. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 230.6 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**4. Client** : 780 euros

> Bien sûr. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 241.3 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**5. Client** : mais l'appli marche pas !!

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis. ⏎ Passons maintenant à votre autre demande : un virement. D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 236.9 ms · 1 LLM — réponse libre, illisible par les règles ; renvoi au contexte → compris (réponse écartée : absente du message)</sub>

**6. Client** : y a un autre moyen ?

> Je n'ai pas bien compris. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 173.2 ms · 1 LLM — réponse libre, illisible par les règles → rien de net — ⚠ incompris</sub>

**7. Client** : je peux le faire au guichet ?

> Bien sûr. À qui voulez-vous envoyer l'argent ? Par exemple : votre fils, votre mère, un ami.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 251.1 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**8. Client** : vous êtes nuls

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis. ⏎ Passons maintenant à votre autre demande : un virement. D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 181.4 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**9. Client** : bon merci

> Avec plaisir. À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**10. Client** : au revoir

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 55. C03 — changements de sujet très rapides

**1. Client** : épargne

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 1 · epargne_projet (interprete, 0.0) · 252.9 ms · 1 LLM — confiance sous le seuil → compris</sub>

**2. Client** : non en fait crédit

> D'accord, on laisse ça de côté. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**3. Client** : non laisse, plutôt une question sur ma carte

> Votre carte a été perdue ou volée. Faites opposition immédiatement via votre espace bancaire sécurisé ou en appelant votre conseiller [1]. La banque ne vous demandera jamais votre code confidentiel.

<sub>niveau 2 · question_definition (interprete, 0.0) · 543.8 ms · 2 LLM — confiance sous le seuil → compris ; aucun terme du glossaire : nos fiches — sources : Carte perdue ou volée, Faire une réclamation, opposition</sub>

**4. Client** : elle a été volée

> Je comprends, il faut agir vite. Faites opposition tout de suite : dans votre espace bancaire sécurisé, rubrique Opposition, ou en appelant votre conseiller. Je ne peux pas bloquer votre carte depuis cette conversation. Rappel : la banque ne vous demandera jamais votre code confidentiel.

<sub>niveau 1 · lost_or_stolen_card (interprete, 0.0) · 295.1 ms · 1 LLM — confiance sous le seuil → compris (réponse écartée : absente du message)</sub>

**5. Client** : et je voulais aussi envoyer de l'argent

> D'accord, je vous guide pas à pas. À qui voulez-vous envoyer l'argent ?

<sub>niveau 0 · faire_virement (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**6. Client** : à mon frère

> Quel montant voulez-vous envoyer ?

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**7. Client** : et si je le fais demain ?

> Bien sûr. Quel montant voulez-vous envoyer ? Par exemple : 200 €.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 282.2 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**8. Client** : 100

> Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation.

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**9. Client** : c'est quoi un virement SEPA

> D'après nos fiches : Un virement se fait depuis votre espace bancaire sécurisé : choisissez ou ajoutez le bénéficiaire, vérifiez son IBAN, puis validez. Vérifiez toujours le bénéficiaire avant de valider, et méfiez-vous d'une demande pressante d'un inconnu. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · question_definition (interprete, 0.0) · 629.9 ms · 2 LLM — confiance sous le seuil → compris ; aucun terme du glossaire : nos fiches — ⚠ repli du garde-fou — sources : Faire un virement, IBAN, Livret d'épargne populaire (LEP)</sub>

**10. Client** : merci

> Avec plaisir. Puis-je vous aider pour autre chose ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

## 56. C04 — client qui ne comprend pas et demande des mots simples

**1. Client** : je suis pas à l'aise avec tout ça

> Je suis désolé pour ce désagrément. ⏎ Je n'ai aucun accès à votre compte, mais votre réclamation compte. ⏎ Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. ⏎ Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 0 · insatisfaction (classifieur, 0.99) · 10.8 ms — demande claire (classifieur)</sub>

**2. Client** : je voudrais placer mes économies

> Bonne idée de mettre de côté. ⏎ Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · epargne_projet (classifieur, 0.96) · 10.6 ms — demande claire (classifieur)</sub>

**3. Client** : je ne sais pas

> Je pars sur un an ; vous pourrez ajuster. ⏎ Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.3 ms — réponse attendue, lue par les règles</sub>

**4. Client** : je sais pas non plus

> Pas de souci, une estimation suffit. ⏎ Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.3 ms — réponse attendue, lue par les règles</sub>

**5. Client** : c'est trop compliqué

> Je suis désolé pour ce désagrément. ⏎ Je n'ai aucun accès à votre compte, mais votre réclamation compte. ⏎ Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. ⏎ Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis. ⏎ Passons maintenant à votre autre demande : votre épargne. Bonne idée de mettre de côté. ⏎ Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 230.3 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**6. Client** : vous pouvez dire ça plus simplement ?

> Je n'ai pas bien compris. ⏎ Combien pouvez-vous mettre de côté chaque mois ? ⏎ Par exemple : 200 €.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 170.6 ms · 1 LLM — réponse libre, illisible par les règles → rien de net — ⚠ incompris</sub>

**7. Client** : c'est quoi un livret

> D'après nos fiches : LEP : Un livret mieux rémunéré, réservé aux personnes dont les revenus sont sous un plafond. ⏎ [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · question_definition (interprete, 0.0) · 922.3 ms · 2 LLM — réponse libre, illisible par les règles → compris ; aucun terme du glossaire : nos fiches — ⚠ repli du garde-fou — sources : LEP, Livret A, Livret Jeune</sub>

**8. Client** : et ça rapporte ?

> Je n'ai pas bien compris. ⏎ Combien pouvez-vous mettre de côté chaque mois ? ⏎ Par exemple : 200 €.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 204.0 ms · 1 LLM — réponse libre, illisible par les règles → rien de net — ⚠ incompris</sub>

**9. Client** : merci jeune homme

> Avec plaisir. ⏎ Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**10. Client** : au revoir

> Au revoir, et bonne journée ! ⏎ Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 57. C07 — négociation et questions chiffrées

**1. Client** : quel est le taux pour un crédit immobilier sur 25 ans ?

> C'est un beau projet. J'ai noté vos revenus de 2 900 € nets par mois. Quel est le prix du bien que vous visez, et quelle part de vos 25 000 € d'épargne souhaitez-vous y consacrer ?

<sub>niveau 0 · credit_immobilier (mots_cles, 0.9) · 0.2 ms — demande claire (mots_cles)</sub>

**2. Client** : c'est négociable ?

> Je n'ai pas cette information dans mes fiches. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · question_definition (interprete, 0.0) · 223.3 ms · 1 LLM — aucune fiche assez proche : retour aux règles — ⚠ hors de nos fiches — sources : Frais d'acquisition (notaire), reste à vivre, apport personnel</sub>

**3. Client** : je veux acheter à 300000

> Quelle part de vos 25 000 € d'épargne souhaitez-vous consacrer à l'achat ?

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.2 ms — réponse attendue, lue par les règles</sub>

**4. Client** : 50000

> Non proposé — Crédit immobilier : mensualité indicative de 1 338 € sur 300 mois, soit 46,1 % des revenus avec les crédits en cours. Projet non retenu dans cette simulation ; aucun refus bancaire n'est prononcé. Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Taux d'effort indicatif de 46,1 % : au-delà du repère de 35 %. Budget indicatif sous ces hypothèses : environ 238 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager. ⏎ Passons maintenant à votre autre demande : un crédit. Non proposé — Crédit immobilier : mensualité indicative de 1 338 € sur 300 mois, soit 46,1 % des revenus avec les crédits en cours. Projet non retenu dans cette simulation ; aucun refus bancaire n'est prononcé. Non proposé — Un prêt immobilier sur 30 ans : option de durée hors du cadre général de 25 ans modélisé. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Taux d'effort indicatif de 46,1 % : au-delà du repère de 35 %. Budget indicatif sous ces hypothèses : environ 238 000 €. Assurance inconnue : budget à réviser. Le cadre HCSF comporte des cas particuliers et une flexibilité réservée à la banque. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 3,3 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Bien ancien, frais d'acquisition estimés à 7,5 % ; estimation à confirmer par un notaire. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.

<sub>niveau 0 · credit_immobilier (reponse_attendue, 1.0) · 0.4 ms — réponse attendue, lue par les règles</sub>

**5. Client** : c'est trop cher ?

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 246.6 ms · 1 LLM — confiance sous le seuil → compris</sub>

**6. Client** : et à 250000 ?

> Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 0 · extra_charge_on_statement (reponse_attendue, 1.0) · 10.4 ms — demande claire (reponse_attendue)</sub>

**7. Client** : c'est quoi la différence entre le taux et le TAEG

> Le taux d'endettement est la part des revenus allouée aux crédits, tandis que le TAEG représente le coût total d'un crédit (intérêts, frais, assurance obligatoire) exprimé en pourcentage par an. Ils sont différents car le taux d'endettement est un indicateur global, tandis que le TAEG est un chiffre de comparaison. [1]

<sub>niveau 2 · question_definition (mots_cles, 0.9) · 556.4 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : TAEG, taux d'endettement, Taux moyen des crédits : repères de la Banque de France</sub>

**8. Client** : le notaire dans le neuf c'est combien

> Le notaire dans le neuf donne le montant exact des frais d'acquisition, qui est estimé à 2,5 % du prix. [1]

<sub>niveau 2 · credit_immobilier (classifieur, 0.94) · 268.0 ms · 1 LLM — question ouverte sur un sujet de nos fiches — sources : Frais d'acquisition (notaire), frais de notaire, Livret Jeune</sub>

**9. Client** : je peux avoir un rendez-vous la semaine prochaine ?

> Je ne peux pas prendre de rendez-vous pour vous : je n'ai aucun accès à votre compte. Pour voir un conseiller, prenez rendez-vous depuis votre espace bancaire sécurisé, rubrique Rendez-vous, ou appelez votre agence. Préparez votre projet : montant, durée, revenus.

<sub>niveau 0 · inconnue (aucun, 0.0) · 0.0 ms — règles</sub>

**10. Client** : top

> Je comprends que votre demande concerne l'alimentation de votre compte. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · top_up_reverted (classifieur, 0.98) · 10.1 ms — demande claire (classifieur)</sub>

## 58. C01 — carte sans contact, plafond, code oublié

**1. Client** : mon paiement sans contact ne marche plus

> Je comprends que votre demande concerne l'utilisation de votre carte. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 0 · contactless_not_working (classifieur, 0.99) · 10.3 ms — demande claire (classifieur)</sub>

**2. Client** : et mon plafond de carte c'est combien ?

> D'après nos fiches : La commission d'intervention est prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. Elle est plafonnée à 8 € par opération et 80 € par mois, et à 4 € et 20 € pour la clientèle fragile. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 636.6 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Commission d'intervention, Livret d'épargne populaire (LEP), Livret Jeune</sub>

**3. Client** : je peux l'augmenter ?

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (classifieur, 0.77) · 10.5 ms — demande claire (classifieur)</sub>

**4. Client** : j'ai oublié mon code aussi

> Je comprends que votre demande concerne votre compte ou votre identité. Je n'ai pas de parcours guidé pour ce point, et aucun accès à votre compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence.

<sub>niveau 1 · edit_personal_details (interprete, 0.0) · 262.6 ms · 1 LLM — confiance sous le seuil → compris</sub>

**5. Client** : je l'ai tapé 3 fois faux

> Je suis désolé pour ce désagrément. Je n'ai aucun accès à votre compte, mais votre réclamation compte. Un conseiller peut reprendre votre demande : prenez rendez-vous depuis votre espace bancaire sécurisé ou contactez votre agence. Si le problème persiste, le service réclamations puis le médiateur bancaire peuvent être saisis.

<sub>niveau 1 · insatisfaction (interprete, 0.0) · 272.9 ms · 1 LLM — confiance sous le seuil → compris (réponse écartée : absente du message)</sub>

**6. Client** : elle est bloquée pour toujours ?

> Je ne suis pas sûr de bien vous comprendre. Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 1 · hors_sujet (interprete, 0.0) · 197.3 ms · 1 LLM — confiance sous le seuil → compris</sub>

**7. Client** : je dois refaire une carte ?

> Pour être sûr de bien vous aider : votre demande concerne-t-elle la commande d'une carte, ou l'alimentation de votre compte ?

<sub>niveau 1 · inconnue (aucun, 0.0) · 216.1 ms · 1 LLM — confiance sous le seuil → compris — ⚠ question fermée</sub>

**8. Client** : ça coûte combien ?

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais.

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 247.6 ms · 1 LLM — confiance sous le seuil → compris</sub>

**9. Client** : ok merci

> Avec plaisir ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**10. Client** : bonne soirée

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 59. C02 — épargne de précaution avec petits revenus

**1. Client** : j'ai pas beaucoup de revenus mais je veux mettre un peu de côté

> Bonne idée de mettre de côté. Dans combien de temps pensez-vous avoir besoin de cet argent ?

<sub>niveau 0 · epargne_projet (classifieur, 0.9) · 11.1 ms — demande claire (classifieur)</sub>

**2. Client** : pour les imprévus

> Bien sûr. Dans combien de temps pensez-vous avoir besoin de cet argent ? Par exemple : 2 ans, ou 48 mois.

<sub>niveau 1 · epargne_projet (reponse_attendue, 1.0) · 236.5 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**3. Client** : je sais pas

> Je pars sur un an ; vous pourrez ajuster. Combien pouvez-vous mettre de côté chaque mois ?

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**4. Client** : 10 euros par mois c'est possible ?

> Voici ce que je vous propose. Livret A : épargne disponible ; adaptée à une réserve ou un projet sans immobilisation. Livret de développement durable et solidaire (LDDS) : domicile fiscal français et imposition séparée déclarés ; épargne disponible. ⏎ Non proposé — Livret Jeune : hors de la tranche d'âge du Livret Jeune. Non proposé — Plan épargne logement (PEL) : besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. Livret d'épargne populaire (LEP) : éligibilité à vérifier (revenu fiscal de référence, nombre de parts fiscales, année du revenu fiscal, territoire fiscal), aucune inéligibilité déduite. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 0 · epargne_projet (reponse_attendue, 1.0) · 0.3 ms — réponse attendue, lue par les règles</sub>

**5. Client** : c'est quoi le LEP

> LEP : Un livret mieux rémunéré, réservé aux personnes dont les revenus sont sous un plafond.

<sub>niveau 0 · question_definition (mots_cles, 0.9) · 0.3 ms — demande claire (mots_cles)</sub>

**6. Client** : j'y ai droit ?

> Voici ce que je vous propose. Livret A : épargne disponible ; adaptée à une réserve ou un projet sans immobilisation. Livret de développement durable et solidaire (LDDS) : domicile fiscal français et imposition séparée déclarés ; épargne disponible. ⏎ Non proposé — Livret Jeune : hors de la tranche d'âge du Livret Jeune. Non proposé — Plan épargne logement (PEL) : besoin de disponibilité ou horizon court : un retrait anticipé entraîne la clôture et peut réduire les avantages. ⏎ Le versement mensuel est celui déclaré par le client ; sa capacité d'épargne n'est pas déduite de ses seuls revenus. Livret d'épargne populaire (LEP) : éligibilité à vérifier (revenu fiscal de référence, nombre de parts fiscales, année du revenu fiscal, territoire fiscal), aucune inéligibilité déduite. ⏎ Disponibilité privilégiée tant que le client n'a pas indiqué accepter une épargne moins liquide.

<sub>niveau 1 · epargne_projet (interprete, 0.0) · 245.7 ms · 1 LLM — confiance sous le seuil → compris</sub>

**7. Client** : ça rapporte plus que le livret A ?

> D'après nos fiches : Livret A : Tout le monde, mineurs compris ; un par personne. Plafond des versements : 22 950 €. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 708.5 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Livret A, Livret A, Livret Jeune</sub>

**8. Client** : pourquoi ?

> D'après votre simulation : Livret Jeune n'est pas proposé : Hors de la tranche d'âge du Livret Jeune. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · inconnue (aucun, 0.0) · 590.2 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**9. Client** : merci c'est clair

> Avec plaisir ! Je peux vous aider pour votre carte, un virement, des frais, votre épargne ou un projet de crédit. Que puis-je faire pour vous ?

<sub>niveau 0 · hors_sujet (mots_cles, 0.9) · 0.1 ms — demande claire (mots_cles)</sub>

**10. Client** : bye

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

## 60. C05 — tout en même temps, puis au revoir

**1. Client** : bonjour je veux un crédit auto, faire un virement à ma femme et comprendre mes frais

> D'accord, je vous guide pas à pas. Quel montant voulez-vous envoyer ?

<sub>niveau 0 · faire_virement (mots_cles, 0.9) · 0.2 ms — plusieurs demandes nettes : traitées par ordre d'urgence</sub>

**2. Client** : le crédit d'abord

> Je peux vous aider à y voir clair, avec prudence. J'ai noté vos revenus de 1 900 € nets par mois. Vous remboursez déjà 150 € de crédit par mois. Quel montant souhaitez-vous emprunter ?

<sub>niveau 1 · credit_conso (interprete, 0.0) · 255.6 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**3. Client** : 10000

> Sur combien de mois souhaitez-vous rembourser ?

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**4. Client** : 36 mois

> Voici ce que je vous propose. Prêt personnel : mensualité indicative de 304 € sur 36 mois, soit 23,9 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. ⏎ Assurance non renseignée : estimation hors assurance, effort sous-estimé si une assurance est requise. Le seuil de prudence consommation est une heuristique interne, pas une obligation HCSF. ⏎ Pour aller plus loin, un conseiller peut étudier votre projet : prenez rendez-vous depuis votre espace bancaire sécurisé. ⏎ Taux annuel de 6 % : repère statistique Banque de France, période 2026-08, relevé le 2026-10-27. Amortissement à mensualité constante, taux annuel divisé par douze ; hors frais de dossier et garantie. Ce n'est pas un TAEG ni une offre. ⏎ Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager. ⏎ Passons maintenant à votre autre demande : un virement. D'accord, je vous guide pas à pas. Quel montant voulez-vous envoyer ?

<sub>niveau 0 · credit_conso (reponse_attendue, 1.0) · 0.3 ms — réponse attendue, lue par les règles</sub>

**5. Client** : pourquoi ?

> D'après votre simulation : Prêt personnel : Mensualité indicative de 304 € sur 36 mois, soit 23,9 % des revenus avec les crédits en cours. Orientation conditionnelle, sous réserve de l'étude du dossier et des coûts manquants. [1] ⏎ Pour votre situation précise, un conseiller peut vous répondre.

<sub>niveau 2 · faire_virement (reponse_attendue, 1.0) · 396.3 ms · 1 LLM — question ouverte sur un sujet de nos fiches — ⚠ repli du garde-fou — sources : Votre simulation, Votre simulation, Votre simulation</sub>

**6. Client** : maintenant le virement

> Bien sûr. Quel montant voulez-vous envoyer ? Par exemple : 200 €.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 261.6 ms · 1 LLM — réponse libre, illisible par les règles → compris (réponse écartée : absente du message)</sub>

**7. Client** : à ma femme

> Bien sûr. Quel montant voulez-vous envoyer ? Par exemple : 200 €.

<sub>niveau 1 · faire_virement (reponse_attendue, 1.0) · 243.8 ms · 1 LLM — réponse libre, illisible par les règles → compris</sub>

**8. Client** : 500

> Pour effectuer ce virement, utilisez votre espace bancaire sécurisé et vérifiez le bénéficiaire avant de valider. Je ne peux pas accéder à votre compte ni exécuter le virement depuis cette conversation. ⏎ Passons maintenant à votre autre demande : un crédit. Je peux vous aider à y voir clair, avec prudence. J'ai noté vos revenus de 1 900 € nets par mois. Vous remboursez déjà 150 € de crédit par mois. Quel montant souhaitez-vous emprunter ?

<sub>niveau 0 · faire_virement (reponse_attendue, 1.0) · 0.1 ms — réponse attendue, lue par les règles</sub>

**9. Client** : et les frais ?

> Je vous explique. Je n'ai aucun accès à votre compte, mais voici ce qui explique le plus souvent ces frais : une commission d'intervention, prélevée quand la banque traite une opération qui dépasse votre solde ou votre découvert autorisé. La loi la plafonne à 8 € par opération et 80 € par mois (4 € et 20 € pour la clientèle fragile). Le détail figure sur votre relevé, dans votre espace bancaire sécurisé. Si ces frais reviennent souvent, l'offre clientèle fragile les limite : un conseiller peut vérifier si vous y avez droit, et c'est aussi à lui qu'on conteste un frais. ⏎ Passons maintenant à votre autre demande : un crédit. Je peux vous aider à y voir clair, avec prudence. Quel montant souhaitez-vous emprunter ?

<sub>niveau 1 · extra_charge_on_statement (interprete, 0.0) · 226.6 ms · 1 LLM — réponse libre, illisible par les règles ; renvoi au contexte → compris</sub>

**10. Client** : merci, à bientôt

> Au revoir, et bonne journée ! Je reste disponible si vous avez une autre question.

<sub>niveau 0 · hors_sujet (mots_cles, 1.0) · 0.0 ms — règles</sub>

