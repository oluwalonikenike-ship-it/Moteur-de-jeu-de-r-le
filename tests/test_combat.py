import unittest
from models.hero import Hero
from models.personnage import Personnage
from engine.combat_engine import CombatEngine


class MonstreTest(Personnage):
    """Monstre simplifié pour les tests."""

    def __init__(self):
        super().__init__(
            nom="Gobelin",
            pv_max=30,
            attaque=8,
            defense=2,
            vitesse=5
        )
        self.xp_donne = 50


class TestCombatEngine(unittest.TestCase):
    """Tests unitaires pour la classe CombatEngine."""

    def setUp(self):
        self.hero = Hero(nom="Kael", classe_hero="Guerrier")
        self.monstre = MonstreTest()
        self.combat = CombatEngine(self.hero, self.monstre)

    def test_creation_combat(self):
        self.assertEqual(self.combat.hero, self.hero)
        self.assertEqual(self.combat.monstre, self.monstre)
        self.assertEqual(self.combat.tour, 0)

    def test_calculer_degats(self):
        degats = self.combat.calculer_degats(self.hero, self.monstre)
        self.assertEqual(degats, 13)

    def test_degats_minimum_1(self):
        self.hero.attaque = 1
        self.monstre.defense = 10
        degats = self.combat.calculer_degats(self.hero, self.monstre)
        self.assertEqual(degats, 1)

    def test_verifier_fin_victoire(self):
        self.monstre.pv_actuel = 0
        self.assertEqual(self.combat.verifier_fin(), "victoire")

    def test_verifier_fin_defaite(self):
        self.hero.pv_actuel = 0
        self.assertEqual(self.combat.verifier_fin(), "defaite")

    def test_verifier_fin_continue(self):
        self.assertEqual(self.combat.verifier_fin(), "continue")


if __name__ == "__main__":
    unittest.main()