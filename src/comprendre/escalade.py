"""Escalade : le LLM d'escalade classe la demande, en dernier recours.

Appelée seulement quand ni les mots-clés ni le classifieur n'ont compris, et
après une question de clarification restée sans effet. Chaque appel est compté
dans la trace : une escalade fréquente signalerait un classifieur insuffisant,
pas un besoin de gros modèle. Responsable : M2.
"""

from __future__ import annotations

from time import perf_counter

from .. import llm
from ..contrats import NIVEAU_ESCALADE, Comprehension, Etape
from ..taxonomie import FAMILLES, NOUVELLES_INTENTIONS, famille_de, representante
from ..texte import normaliser

_CHOIX = tuple(NOUVELLES_INTENTIONS) + tuple(f for f in FAMILLES if representante(f) not in NOUVELLES_INTENTIONS)

_SYSTEME = (
    "Tu classes la demande d'un client de banque. Réponds par un seul mot, exactement "
    "l'un de ceux-ci, ou « inconnue » : " + ", ".join(_CHOIX) + "."
)


def escalader(message: str) -> tuple[Comprehension | None, Etape | None]:
    """Compréhension par le LLM d'escalade, ou ``None`` si le LLM est désactivé ou hésite."""

    if not llm.escalade_active():
        return None, None
    debut = perf_counter()
    texte, tokens = llm.generer(llm.MODELE_ESCALADE, _SYSTEME, message, max_tokens=12)
    etape = Etape(
        nom="escalade", modele=llm.MODELE_ESCALADE, latence_ms=(perf_counter() - debut) * 1000,
        tokens=tokens, appel_llm=True,
    )
    choix = normaliser(texte).replace(" ", "_")
    if choix in NOUVELLES_INTENTIONS:
        intention = choix
    elif choix in FAMILLES:
        intention = representante(choix)
    else:
        return None, etape
    return (
        Comprehension(
            famille=famille_de(intention), intention=intention, confiance=0.0,
            niveau=NIVEAU_ESCALADE, modele=llm.MODELE_ESCALADE,
        ),
        etape,
    )
