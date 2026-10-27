"""Adaptation M3/M2 : questions métier et lecture stricte des réponses, sans changer M1."""
from __future__ import annotations

import re
from typing import Any
from ..texte import normaliser
from ..contrats import EtatConversation, Etape, Reponse

QUESTIONS = {
    "revenus_nets": "Quels sont vos revenus nets mensuels avant impôt (montant positif) ?",
    "mensualites_en_cours": "Quel total remboursez-vous déjà chaque mois, assurance comprise ? Indiquez 0 si aucun.",
    "prix_bien": "Quel est le prix du bien, en euros ?",
    "apport": "Quel apport souhaitez-vous consacrer au projet, en euros ?",
    "montant": "Quel montant positif souhaitez-vous emprunter ?",
    "duree_ans": "Quelle durée souhaitez-vous, en années entières ?",
    "duree_mois": "Quelle durée souhaitez-vous, en mois entiers ?",
    "taux_annuel": "Quel taux annuel souhaitez-vous utiliser comme hypothèse ? Indiquez-le en pourcentage, par exemple avec le signe %.",
    "assurance_mensuelle": "Quel est le coût mensuel connu de l'assurance, en euros ?",
    "taux_frais_notaire": "Quel pourcentage de frais d'acquisition souhaitez-vous utiliser ?",
    "type_bien": "Le bien est-il ancien ou neuf ?",
    "age": "Quel est l'âge du bénéficiaire, en années ?",
    "horizon_mois": "Dans combien de mois pensez-vous avoir besoin de l'argent ?",
    "montant_mensuel": "Quel montant positif pouvez-vous mettre de côté chaque mois ?",
    "besoin_liquidite": "Avez-vous besoin de pouvoir récupérer cet argent à tout moment ? (oui / non)",
    "est_etudiant": "Avez-vous actuellement le statut étudiant ? (oui / non)",
    "ages_enfants": "Quels sont les âges des enfants concernés, séparés par des virgules ?",
}
ACCORDS = {"oui", "oui je confirme", "je confirme", "oui vas y", "oui allez y", "d accord", "ok"}
REFUS = {"non", "non merci", "annule", "annuler", "pas maintenant", "laisse tomber"}


def confirmation(message: str) -> bool | None:
    """Seules les réponses complètes non ambiguës valent accord ou refus."""
    if "?" in message:
        return None
    texte = normaliser(message)
    return True if texte in ACCORDS else False if texte in REFUS else None


def montant_ambigu(message: str) -> bool:
    """Barrière provisoire : M1 perd le signe et certains points décimaux."""
    return bool(re.search(r"[-−]\s*\d|\d+\.\d{1,2}(?!\d)|\d+[.,]\d{3,}\s*(?:€|euros)", message))


def question(champ: str) -> str:
    return QUESTIONS.get(champ, f"Information à vérifier avec un conseiller : {champ}. Vous pouvez annuler ce parcours.")


def lire_reponse(champ: str, message: str) -> Any:
    texte = normaliser(message)
    if champ in ("besoin_liquidite", "est_etudiant"):
        return confirmation(message)
    if champ == "type_bien":
        return texte if texte in ("ancien", "neuf") else None
    if champ == "ages_enfants":
        return [int(x.strip()) for x in message.split(",")] if re.fullmatch(r"\d+(\s*,\s*\d+)*", message.strip()) else None
    if champ not in QUESTIONS:
        return None
    chiffres = re.findall(r"\d{1,3}(?:[   ]\d{3})+(?:,\d+)?|\d+(?:,\d+)?", message)
    if len(chiffres) != 1:
        return None
    valeur = float(re.sub(r"[   ]", "", chiffres[0]).replace(",", "."))
    return valeur / 100 if champ in ("taux_annuel", "taux_frais_notaire") else valeur


def directe(texte: str, etat: EtatConversation, **kwargs: Any) -> tuple[Reponse, EtatConversation]:
    """Réponse de validation sans LLM ; le message utilisateur est déjà historisé."""
    etat.derniere_reponse = texte
    etat.historique.append({"role": "assistant", "content": texte})
    kwargs.setdefault("trace", [Etape("validation_m3", modele="regles")])
    return Reponse(texte=texte, **kwargs), etat
