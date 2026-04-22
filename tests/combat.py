import unittest
from models.hero import Hero
from models.personnage import Personnage
from engine.combat_engine import CombatEngine


class MonsstreTest(Personnage):

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
   
    def setUp(self):
       
        self.hero = Hero(nom="Kael", classe_hero="Guerrier")
        self.monstre = MonsstreTest()
        self.combat = CombatEngine(self.hero, self.monstre)

    def test_creation_combat(self):
       
        self.assertEqual(self.combat.hero, self.hero)
        self.assertEqual(self.combat.monstre, self.monstre)
        self.assertEqual(self.combat.tour, 0)

    def test_calculer_degats(self):
        degats = self.combat.calculer_degats(self.hero, self.monstre)
        self.assertEqual(degats, 13)  # 15 attaque - 2 defense = 13

    def test_degats_minimum_1(self):
        self.hero.attaque = 1