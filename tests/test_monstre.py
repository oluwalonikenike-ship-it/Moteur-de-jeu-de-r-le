"""Tests unitaires pour la classe Monstre."""
import unittest
from models.monstre import Monstre
from models.item import Potion


class TestMonstre(unittest.TestCase):
    """Tests pour Monstre."""

    def setUp(self):
        self.loot = [Potion("Potion", soin=30, valeur=10)]
        self.monstre = Monstre(
            nom="Gobelin",
            pv_max=30,
            attaque=8,
            defense=2,
            xp_donne=50,
            loot_possible=self.loot
        )

    def test_creation_monstre(self):
        self.assertEqual(self.monstre.nom, "Gobelin")
        self.assertEqual(self.monstre.pv_max, 30)
        self.assertEqual(self.monstre.xp_donne, 50)

    def test_est_vivant(self):
        self.assertTrue(self.monstre.est_vivant())

    def test_est_mort(self):
        self.monstre.pv_actuel = 0
        self.assertFalse(self.monstre.est_vivant())

    def test_recevoir_degats(self):
        degats = self.monstre.recevoir_degats(10)
        self.assertEqual(degats, 8)
        self.assertEqual(self.monstre.pv_actuel, 22)

    def test_attaque_speciale(self):
        degats = self.monstre.attaque_speciale()
        self.assertEqual(degats, 12)

    def test_generer_loot(self):
        loot = self.monstre.generer_loot()
        self.assertIsNotNone(loot)

    def test_generer_loot_vide(self):
        self.monstre.loot_possible = []
        loot = self.monstre.generer_loot()
        self.assertIsNone(loot)


if __name__ == "__main__":
    unittest.main()