# Moteur-de-jeu-de-r-le

## Description

Moteur de jeu de role en mode en mode 2D développé en python 3 avec affichage graphique via pygame.
Un héros explore un donjon , affronte des monstres en combat tour par tour , gere un inventaire et progresse en gagnant
de l'expérience.
Projet realisé dans le cadre du cours de programmation python (L2).

## ETUDIANTS
    -LASSOU Hanine
    -YOLOU Abdel Wadjid 

## Chargé de cours 
    - Dr MOUSSE Ange Mikaël

## Prérequis 
    -Python 3.10+
    -Pygame 2.x

## Installation 
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt 

## Lancement 
    python main.py

## Structure
    -models/ -Classes métier (hero, Monstre, Item, Inventaire)
    -engine/ -Moteurs (combat, jeu)
    -data/ -Fichiers JSON (Sauvegarde, sprites, maps)
    -tests/ -Tests unitaires
    -utils -Fonctons utilitaires