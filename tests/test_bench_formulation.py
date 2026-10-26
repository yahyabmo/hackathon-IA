from eval.bench_formulation import SITUATIONS, preparer
from src.converser.garde_fou import nombres, verifier


def test_trente_situations_de_conseil():
    assert len(SITUATIONS) == 30


def test_chaque_gabarit_existe_et_passe_le_garde_fou():
    for client, parcours, infos in SITUATIONS:
        nom, texte = preparer(client, parcours, infos)
        assert texte, nom
        assert verifier(texte, set(nombres(texte))) == [], nom
