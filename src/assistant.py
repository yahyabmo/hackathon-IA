"""Point d'entrée unique de l'assistant bancaire."""

from __future__ import annotations

from .comprendre import comprendre
from .conseiller import conseiller
from .contrats import Action, Conseil, EtatConversation, Reponse
from .converser import prochaine_etape
from .mesure import mesurer


def reply(
    message: str,
    client_id: str,
    etat: EtatConversation,
) -> tuple[Reponse, EtatConversation]:
    """Orchestre les stubs du pipeline et conserve l'état de conversation.

    Cette version ne déclenche aucune action bancaire et ne prétend pas
    produire une recommandation validée. Elle sert uniquement de contrat
    d'intégration pour les trois modules.
    """

    comprehension, etape_comprendre = mesurer("comprendre", lambda: comprendre(message))
    etat.intention = comprehension.intention
    etat.historique.append({"role": "user", "content": message})
    etape_dialogue = prochaine_etape(comprehension, etat)
    conseil = conseiller(client_id, comprehension.intention, etat.slots)

    if comprehension.intention == "carte_perdue":
        texte = (
            "Je peux vous guider pour sécuriser votre carte. "
            "Aucune action bancaire n'est exécutée dans ce prototype."
        )
    elif comprehension.intention == "salutation":
        texte = "Bonjour ! Comment puis-je vous aider aujourd'hui ?"
    else:
        texte = (
            "Je n'ai pas encore identifié votre demande. "
            "Pouvez-vous préciser votre besoin bancaire ?"
        )

    etat.derniere_reponse = texte
    etat.historique.append({"role": "assistant", "content": texte})
    reponse = Reponse(
        texte=texte,
        comprehension=comprehension,
        conseil=conseil,
        action=Action(),
        escalade=comprehension.intention == "inconnue",
        trace=[etape_comprendre],
    )
    reponse.trace.append(type(etape_comprendre)(nom="dialogue", modele=etape_dialogue))
    return reponse, etat
