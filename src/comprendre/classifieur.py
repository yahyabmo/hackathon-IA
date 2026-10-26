"""Second niveau de l'étage 1 : encodeur multilingue + régression logistique.

Bouchon tant que M1 n'a pas entraîné les têtes : il ne prédit rien, ce qui
laisse la main à la question de clarification.

Ce qui est attendu ici (Younes) :
- ``intfloat/multilingual-e5-small`` avec le préfixe ``query:`` ;
- deux têtes de régression logistique, famille puis intention, entraînées sur
  Banking77 en anglais, sans traduction, plus nos phrases françaises ;
- ``SEUIL_TAU`` fixé par balayage (97 % de précision sur les messages acceptés) ;
- la phrase d'entraînement la plus proche dans ``exemple_proche``.
"""

from __future__ import annotations

from ..contrats import Comprehension

MODELE = "e5-small+lr"
SEUIL_TAU = 0.6  # provisoire, à fixer par balayage


def predire(message: str) -> Comprehension | None:
    """Compréhension au niveau ``classifieur``, ou ``None`` tant qu'il n'est pas entraîné.

    Quand elle est rendue, ``alternatives`` porte les deux familles les plus
    probables, même sous le seuil : elles servent à la question de clarification.
    """

    return None
