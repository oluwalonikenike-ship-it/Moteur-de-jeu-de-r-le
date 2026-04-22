import unittest
from models.personnage import Personnage


class TestPersonnage(unittest.TestCase):
    def setUp(self):
        self.personnage = Personnage(
            nom="Test",
            pv_max=100,
            attaque=15,
            defense=5,
            vitesse=10
        )

    def test_creation_personnage(self):
        self.assertEqual(self.personnage.nom, "Test")
        self.assertEqual(self.personnage.pv_max, 100)
        self.assertEqual(self.personnage.pv_actuel, 100)
        self.assertEqual(self.personnage.attaque, 15)
        self.assertEqual(self.personnage.defense, 5)
        self.assertEqual(self.personnage.niveau, 1)
        self.assertEqual(self.personnage.xp, 0)

    def test_est_vivant(self):
       
        self.assertTrue(self.personnage.est_vivant())

    def test_est_mort(self):
        
        self.personnage.pv_actuel = 0
        self.assertFalse(self.personnage.est_vivant())

    def test_recevoir_degats(self):
        
        degats_reels = self.personnage.recevoir_degats(20)
        self.assertEqual(degats_reels, 15)  # 20 - 5 defense = 15
        self.assertEqual(self.personnage.pv_actuel, 85)  # 100 - 15 = 85

    def test_degats_minimum_1(self):
       
        degats_reels = self.personnage.recevoir_degats(3)
        self.assertEqual(degats_reels, 1)  # 3 - 5 = -2 mais minimum 1

    def test_pv_ne_descend_pas_sous_zero(self):
        
        self.personnage.recevoir_degats(999)
        self.assertEqual(self.personnage.pv_actuel, 0)


if __name__ == "__main__":
    unittest.main()