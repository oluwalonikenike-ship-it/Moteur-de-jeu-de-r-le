# Moteur de Jeu de Rôle RPG

## Description
Moteur de jeu de rôle en mode texte (terminal) développé en Python 3.
Un héros explore un donjon, affronte des monstres en combat tour par tour,
gère un inventaire et progresse en gagnant de l'expérience.
Les parties sont sauvegardées en JSON et l'historique est enregistré en SQLite.

Projet réalisé dans le cadre du cours de Programmation Python (L2).

## Étudiants
- LASSOU Hanine
- YOLOU Abdel Wadjid

## Chargé de cours
- Dr MOUSSE Ange Mikaël

## Fonctionnalités
- Création d'un héros (Guerrier, Mage, Archer)
- Combat tour par tour contre des monstres générés aléatoirement
- Système de progression (XP, niveaux, statistiques)
- Inventaire (potions, armes, armures)
- Sauvegarde et chargement de partie (JSON)
- Historique des parties et classement (SQLite)
- 51 tests unitaires — coverage 61%

## Prérequis
- Python 3.10+

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement
```bash
python main.py
```

## Structure

Moteur-de-jeu-RPG/
├── data/           # Fichiers JSON (monstres, items)
├── engine/         # Moteurs (game_engine, combat_engine)
├── models/         # Classes métier (Hero, Monstre, Item, Inventaire)
├── tests/          # Tests unitaires (pytest)
├── utils/          # Fonctions utilitaires
├── database.py     # Gestion SQLite
├── data_loader.py  # Chargement des données JSON
├── main.py         # Point d'entrée
└── requirements.txt

## Tests
```bash
pytest tests/ -v
pytest tests/ --cov=. --cov-report=term-missing
```

## Tags
- v0.3 — Sprint 3 : GameEngine, CombatEngine, Database
- v0.4 — Sprint 4/5 : Sauvegarde JSON, SQLite, 51 tests, coverage 61%