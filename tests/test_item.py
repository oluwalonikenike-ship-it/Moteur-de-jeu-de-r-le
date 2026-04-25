"""Tests unitaires pour les classes Item, Arme, Potion, Armure."""
import unittest
from models.item import Arme, Potion, Armure
from models.hero import Hero


class TestArme(unittest.TestCase):

    def setUp(self):
        self.arme = Arme("Epee", degats_bonus=5, valeur=50)
        self.hero = Hero("Test", "Guerrier")

    def test_creation_arme(self):
        self.assertEqual(self.arme.nom, "Epee")
        self.assertEqual(self.arme.degats_bonus, 5)
        self.assertEqual(self.arme.type_item, "arme")

    def test_equiper_arme(self):
        attaque_avant = self.hero.attaque
        self.arme.equiper(self.hero)
        self.assertEqual(self.hero.attaque, attaque_avant + 5)


class TestPotion(unittest.TestCase):

    def setUp(self):
        self.potion = Potion("Potion", soin=30, valeur=10)
        self.hero = Hero("Test", "Guerrier")

    def test_creation_potion(self):
        self.assertEqual(self.potion.soin, 30)
        self.assertEqual(self.potion.type_item, "potion")

    def test_utiliser_potion(self):
        self.hero.pv_actuel = 50
        self.potion.utiliser(self.hero)
        self.assertEqual(self.hero.pv_actuel, 80)

    def test_potion_ne_depasse_pas_pv_max(self):
        self.hero.pv_actuel = self.hero.pv_max
        self.potion.utiliser(self.hero)
        self.assertEqual(self.hero.pv_actuel, self.hero.pv_max)


class TestArmure(unittest.TestCase):

    def setUp(self):
        self.armure = Armure("Bouclier", defense_bonus=3, valeur=30)
        self.hero = Hero("Test", "Guerrier")

    def test_creation_armure(self):
        self.assertEqual(self.armure.defense_bonus, 3)
        self.assertEqual(self.armure.type_item, "armure")

    def test_equiper_armure(self):
        defense_avant = self.hero.defense
        self.armure.equiper(self.hero)
        self.assertEqual(self.hero.defense, defense_avant + 3)

    def test_utiliser_armure(self):
        defense_avant = self.hero.defense
        self.armure.utiliser(self.hero)
        self.assertEqual(self.hero.defense, defense_avant + 3)


if __name__ == "__main__":
    unittest.main()