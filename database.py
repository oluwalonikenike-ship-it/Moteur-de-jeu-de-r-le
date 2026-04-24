"""
Module de gestion de la base de données SQLite.
Enregistre l'historique des parties et le classement des scores.
"""

import sqlite3
import os
from datetime import datetime


class Database:

    FICHIER_DB = "data/jeu.db"

    def __init__(self):
        """Initialise la base de données et crée les tables si elles n'existent pas."""
        os.makedirs("data", exist_ok=True)
        self.connexion = sqlite3.connect(self.FICHIER_DB)
        self.connexion.row_factory = sqlite3.Row  # accès par nom de colonne
        self._creer_tables()

    def _creer_tables(self):
        """Crée les tables si elles n'existent pas encore."""
        curseur = self.connexion.cursor()

        curseur.execute("""
            CREATE TABLE IF NOT EXISTS historique (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_hero    TEXT    NOT NULL,
                classe      TEXT    NOT NULL,
                niveau      INTEGER NOT NULL,
                xp          INTEGER NOT NULL,
                resultat    TEXT    NOT NULL,  -- 'victoire', 'defaite', 'abandon'
                date        TEXT    NOT NULL
            )
        """)

        curseur.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_hero    TEXT    NOT NULL,
                classe      TEXT    NOT NULL,
                niveau_max  INTEGER NOT NULL,
                date        TEXT    NOT NULL
            )
        """)

        self.connexion.commit()

    def enregistrer_partie(self, hero, resultat: str):
        curseur = self.connexion.cursor()
        curseur.execute("""
            INSERT INTO historique (nom_hero, classe, niveau, xp, resultat, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            hero.nom,
            hero.classe_hero,
            hero.niveau,
            hero.xp,
            resultat,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        self.connexion.commit()
        print(f"  📝 Partie enregistrée : {hero.nom} — {resultat}")

    def get_historique(self, limite: int = 10) -> list:
        curseur = self.connexion.cursor()
        curseur.execute("""
            SELECT * FROM historique
            ORDER BY id DESC
            LIMIT ?
        """, (limite,))
        return curseur.fetchall()

    def afficher_historique(self, limite: int = 10):
        """Affiche les dernières parties dans la console."""
        lignes = self.get_historique(limite)
        if not lignes:
            print("\n  Aucune partie enregistrée.")
            return

        print(f"\n{'='*55}")
        print("   HISTORIQUE DES PARTIES")
        print(f"{'='*55}")
        print(f"  {'Héros':<12} {'Classe':<10} {'Niv':>4} {'Résultat':<10} {'Date'}")
        print(f"  {'-'*53}")
        for ligne in lignes:
            print(
                f"  {ligne['nom_hero']:<12} "
                f"{ligne['classe']:<10} "
                f"{ligne['niveau']:>4}  "
                f"{ligne['resultat']:<10} "
                f"{ligne['date']}"
            )
        print(f"{'='*55}\n")


    def enregistrer_score(self, hero):
        """
        Enregistre le score du héros (niveau atteint).

        Args:
            hero: Objet Hero avec nom, classe_hero, niveau.
        """
        curseur = self.connexion.cursor()
        curseur.execute("""
            INSERT INTO scores (nom_hero, classe, niveau_max, date)
            VALUES (?, ?, ?, ?)
        """, (
            hero.nom,
            hero.classe_hero,
            hero.niveau,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        self.connexion.commit()

    def afficher_classement(self, limite: int = 5):
        """Affiche le classement des meilleurs scores."""
        curseur = self.connexion.cursor()
        curseur.execute("""
            SELECT nom_hero, classe, MAX(niveau_max) as niveau_max, date
            FROM scores
            GROUP BY nom_hero
            ORDER BY niveau_max DESC
            LIMIT ?
        """, (limite,))
        lignes = curseur.fetchall()

        if not lignes:
            print("\n  Aucun score enregistré.")
            return

        print(f"\n{'='*45}")
        print("   🏆 CLASSEMENT DES MEILLEURS HÉROS")
        print(f"{'='*45}")
        for i, ligne in enumerate(lignes, 1):
            print(
                f"  {i}. {ligne['nom_hero']:<12} "
                f"({ligne['classe']:<8}) "
                f"Niveau {ligne['niveau_max']}"
            )
        print(f"{'='*45}\n")

    def fermer(self):
        """Ferme la connexion à la base de données."""
        if self.connexion:
            self.connexion.close()
