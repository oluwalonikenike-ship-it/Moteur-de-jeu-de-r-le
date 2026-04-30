with open('tests/test_personnage.py', 'wb') as f:
    code = (
        'import unittest\n'
        'from models.personnage import Personnage\n\n\n'
        'class TestPersonnage(unittest.TestCase):\n\n'
        '    def setUp(self):\n'
        '        self.p = Personnage("Test", 100, 15, 5, 10)\n\n'
        '    def test_creation(self):\n'
        '        self.assertEqual(self.p.nom, "Test")\n'
        '        self.assertEqual(self.p.pv_max, 100)\n\n'
        '    def test_est_vivant(self):\n'
        '        self.assertTrue(self.p.est_vivant())\n\n'
        '    def test_est_mort(self):\n'
        '        self.p.pv_actuel = 0\n'
        '        self.assertFalse(self.p.est_vivant())\n\n'
        '    def test_degats(self):\n'
        '        d = self.p.recevoir_degats(20)\n'
        '        self.assertEqual(d, 15)\n\n'
        '    def test_pv_zero(self):\n'
        '        self.p.recevoir_degats(999)\n'
        '        self.assertEqual(self.p.pv_actuel, 0)\n'
    )
    f.write(code.encode('utf-8'))
print('OK')