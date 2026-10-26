import json
from pathlib import Path

import pytest

from src.taxonomie import FAMILLES, INTENTION_VERS_FAMILLE, INTENTIONS_BANKING77, NOUVELLES_INTENTIONS

CATEGORIES = Path(__file__).resolve().parents[1] / "data" / "raw" / "banking77" / "categories.json"


def test_quatorze_familles_et_quatre_vingt_cinq_intentions():
    assert len(FAMILLES) == 14
    assert len(INTENTION_VERS_FAMILLE) == 85
    assert len(NOUVELLES_INTENTIONS) == 8


def test_chaque_intention_dans_une_seule_famille():
    toutes = [i for intentions in FAMILLES.values() for i in intentions]
    assert len(toutes) == len(set(toutes))


@pytest.mark.skipif(not CATEGORIES.exists(), reason="données Banking77 absentes")
def test_les_77_intentions_de_banking77_sont_couvertes():
    officielles = set(json.loads(CATEGORIES.read_text(encoding="utf-8")))
    assert set(INTENTIONS_BANKING77) == officielles
