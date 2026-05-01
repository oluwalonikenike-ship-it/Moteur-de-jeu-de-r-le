# -*- coding: utf-8 -*-
"""Tests unitaires pour la classe GameEngine."""

import unittest
import os
from models.hero import Hero
from engine.game_engine import GameEngine


class TestGameEngine(unittest.TestCase):
    """Tests pour GameEngine."""

    def setUp(self):
        """Preparation avant chaque test."""
        self.game = GameEngine()
        self.chemin_test = "data/test_sauvegarde.json"
        self.game.chemin_sauvegarde = self.chemin_test

    def tearDown(self):
        """Nettoyage apres chaque test."""
        if os.path.exists(self.chemin_test):
            os.remove(self.chemin_test)

    def test_creation_game_engine(self):
        """Test creation du moteur de jeu."""
        self.assertIsNone(self.game.hero)
        self.assertEqual(self.game.etat_jeu, "menu")

    def test_sauvegarde_sans_hero(self):
        """Test sauvegarde sans hero ne crash pas."""
        self.game.sauvegarder()
        self.assertFalse(os.path.exists(self.chemin_test))

    def test_sauvegarde_et_chargement(self):
        """Test sauvegarde et chargement d'un hero."""
        # Creer un hero
        self.game.hero = Hero("TestHero", "Guerrier")
        self.game.hero.niveau = 3
        self.game.hero.xp = 250

        # Sauvegarder
        self.game.sauvegarder()
        self.assertTrue(os.path.exists(self.chemin_test))

        # Creer un nouveau game engine
        game2 = GameEngine()
        game2.chemin_sauvegarde = self.chemin_test

        # Charger
        game2.charger()

        # Verifier
        self.assertIsNotNone(game2.hero)
        self.assertEqual(game2.hero.nom, "TestHero")
        self.assertEqual(game2.hero.niveau, 3)
        self.assertEqual(game2.hero.xp, 250)

    def test_chargement_sans_fichier(self):
        """Test chargement quand pas de sauvegarde."""
        game2 = GameEngine()
        game2.chemin_sauvegarde = "data/fichier_inexistant.json"
        game2.charger()
        self.assertIsNone(game2.hero)


if __name__ == "__main__":
    unittest.main()