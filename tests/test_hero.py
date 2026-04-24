import unittest
from models.hero import Hero


class TestHero(unittest.TestCase):
    """Tests unitaires pour la classe Hero."""

    def setUp(self):
        self.hero = Hero(nom="Kael", classe_hero="Guerrier")

    def test_creation_hero(self):
        self.assertEqual(self.hero.nom, "Kael")
        self.assertEqual(self.hero.classe_hero, "Guerrier")
        self.assertEqual(self.hero.niveau, 1)
        self.assertEqual(self.hero.xp, 0)
        self.assertEqual(self.hero.xp_pour_niveau, 100)
        self.assertEqual(self.hero.pv_max, 100)
        self.assertEqual(self.hero.or_possede, 0)

    def test_gagner_xp(self):
        self.hero.gagner_xp(50)
        self.assertEqual(self.hero.xp, 50)

    def test_montee_de_niveau(self):
        self.hero.gagner_xp(100)
        self.assertEqual(self.hero.niveau, 2)
        self.assertEqual(self.hero.xp, 0)

    def test_stats_augmentent_apres_niveau(self):
        pv_avant = self.hero.pv_max
        attaque_avant = self.hero.attaque
        defense_avant = self.hero.defense
        self.hero.monter_niveau()
        self.assertEqual(self.hero.pv_max, pv_avant + 20)
        self.assertEqual(self.hero.attaque, attaque_avant + 3)
        self.assertEqual(self.hero.defense, defense_avant + 2)

    def test_sauvegarder(self):
        sauvegarde = self.hero.sauvegarder()
        self.assertIsInstance(sauvegarde, dict)
        self.assertEqual(sauvegarde["nom"], "Kael")
        self.assertEqual(sauvegarde["niveau"], 1)


if __name__ == "__main__":
    unittest.main()
    