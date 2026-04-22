import unittest
from models.inventaire import Inventaire
from models.item import Item


class Testinventaire(unittest.TestCase):

    def setUp(self):
        self.inventaire = Inventaire()
        self.potion = Item(
            nom="Potion de soin",
            type_item="potion",
            effet=30,
            valeur=10
        )
        self.epee = Item(
            nom="Epée en fer",
            type_item="arme",
            effet=5,
            valeur=50
        )

    def test_creation_inventaire(self):
        self.assertEqual(len(self.inventaire.items), 0)
        self.assertEqual(self.inventaire.capacite_max, 10)

    def test_ajouter_item(self):
        self.inventaire.ajouter(self.potion)
        self.assertEqual(len(self.inventaire.items), 1)

    def test_capacite_maximale(self):
        for i in range(10):
            item = Item(f"Item {i}", "potion", 10, 5)
            self.inventaire.ajouter(item)
        resultat = self.inventaire.ajouter(self.epee)
        self.assertFalse(resultat)
        self.assertEqual(len(self.inventaire.items), 10)

    def test_supprimer_item(self):
       
        self.inventaire.ajouter(self.potion)
        self.inventaire.supprimer(self.potion)
        self.assertEqual(len(self.inventaire.items), 0)

    def test_supprimer_item_absent(self):
        
        resultat = self.inventaire.supprimer(self.potion)
        self.assertFalse(resultat)


if __name__ == "__main__":
    unittest.main()