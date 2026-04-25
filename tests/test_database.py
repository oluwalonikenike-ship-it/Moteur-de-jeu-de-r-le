"""Tests unitaires pour la classe Database."""
import unittest
import os
from database import Database
from models.hero import Hero


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database()
        self.hero = Hero("TestHero", "Guerrier")

    def test_creation_tables(self):
        curseur = self.db.connexion.cursor()
        curseur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in curseur.fetchall()]
        self.assertIn("historique", tables)
        self.assertIn("scores", tables)

    def test_enregistrer_partie_victoire(self):
        self.db.enregistrer_partie(self.hero, "victoire")
        lignes = self.db.get_historique(1)
        self.assertEqual(len(lignes), 1)
        self.assertEqual(lignes[0]["resultat"], "victoire")

    def test_enregistrer_partie_defaite(self):
        self.db.enregistrer_partie(self.hero, "defaite")
        lignes = self.db.get_historique(1)
        self.assertEqual(lignes[0]["resultat"], "defaite")

    def test_enregistrer_score(self):
        self.db.enregistrer_score(self.hero)
        curseur = self.db.connexion.cursor()
        curseur.execute("SELECT * FROM scores WHERE nom_hero=?", (self.hero.nom,))
        lignes = curseur.fetchall()
        self.assertGreater(len(lignes), 0)

    def test_get_historique(self):
        self.db.enregistrer_partie(self.hero, "victoire")
        historique = self.db.get_historique(10)
        self.assertIsInstance(historique, list)

    def tearDown(self):
        self.db.fermer()

    def test_afficher_historique(self):
        self.db.enregistrer_partie(self.hero, "victoire")
        try:
            self.db.afficher_historique()
        except Exception as e:
            self.fail(f"afficher_historique a levé une exception : {e}")

    def test_afficher_classement(self):
        self.db.enregistrer_score(self.hero)
        try:
            self.db.afficher_classement()
        except Exception as e:
            self.fail(f"afficher_classement a levé une exception : {e}")

if __name__ == "__main__":
    unittest.main()