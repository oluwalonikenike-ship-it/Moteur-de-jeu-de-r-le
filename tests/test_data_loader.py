"""Tests unitaires pour la classe DataLoader."""
import unittest
from data_loader import DataLoader


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.loader = DataLoader()

    def test_charger_monstres(self):
        monstres = self.loader.charger_monstres()
        self.assertIsInstance(monstres, list)
        self.assertGreater(len(monstres), 0)

    def test_charger_items(self):
        items = self.loader.charger_items()
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)

    def test_get_items_par_type_potion(self):
        potions = self.loader.get_items_par_type("potion")
        for p in potions:
            self.assertEqual(p["type_item"], "potion")

    def test_get_items_par_type_arme(self):
        armes = self.loader.get_items_par_type("arme")
        for a in armes:
            self.assertEqual(a["type_item"], "arme")

    def test_get_monstres_par_niveau(self):
        monstres = self.loader.get_monstres_par_niveau(1)
        self.assertIsInstance(monstres, list)
        for m in monstres:
            self.assertLessEqual(m["niveau_min"], 1)

    def test_get_monstre_par_nom(self):
        monstre = self.loader.get_monstre_par_nom("Gobelin")
        self.assertIsNotNone(monstre)
        self.assertEqual(monstre["nom"], "Gobelin")

    def test_get_monstre_par_nom_inexistant(self):
        monstre = self.loader.get_monstre_par_nom("Inconnu")
        self.assertIsNone(monstre)

    def test_get_item_par_nom(self):
        item = self.loader.get_item_par_nom("Potion de soin")
        self.assertIsNotNone(item)

    def test_get_item_par_nom_inexistant(self):
        item = self.loader.get_item_par_nom("Objet inexistant")
        self.assertIsNone(item)

    def test_afficher_catalogue_items(self):
        # Vérifie que la méthode ne lève pas d'exception
        try:
            self.loader.afficher_catalogue_items()
        except Exception as e:
            self.fail(f"afficher_catalogue_items a levé une exception : {e}")

    def test_afficher_catalogue_monstres(self):
        try:
            self.loader.afficher_catalogue_monstres()
        except Exception as e:
            self.fail(f"afficher_catalogue_monstres a levé une exception : {e}")

    def test_get_items_par_type_armure(self):
        armures = self.loader.get_items_par_type("armure")
        for a in armures:
            self.assertEqual(a["type_item"], "armure")
if __name__ == "__main__":
    unittest.main()