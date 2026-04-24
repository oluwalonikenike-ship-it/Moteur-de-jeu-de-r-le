import unittest
from models.personnage import Personnage


class TestPersonnage(unittest.TestCase):

    def setUp(self):
        self.p = Personnage("Test", 100, 15, 5, 10)

    def test_creation(self):
        self.assertEqual(self.p.nom, "Test")
        self.assertEqual(self.p.pv_max, 100)

    def test_est_vivant(self):
        self.assertTrue(self.p.est_vivant())

    def test_est_mort(self):
        self.p.pv_actuel = 0
        self.assertFalse(self.p.est_vivant())

    def test_degats(self):
        d = self.p.recevoir_degats(20)
        self.assertEqual(d, 15)

    def test_pv_zero(self):
        self.p.recevoir_degats(999)
        self.assertEqual(self.p.pv_actuel, 0)
