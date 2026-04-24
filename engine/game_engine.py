"""Module contenant le moteur principal du jeu"""
import json
import os
import random
from models.hero import Hero
from models.monstre import Monstre
from models.item import Arme, Potion

class GameEngine:
    STATS_CLASSE = {
        "Guerrier": {"pv_max": 120, "attaque": 18, "defense": 8},
        "Mage": {"pv_max": 80, "attaque": 25, "defense": 4},
        "Archer": {"pv_max": 100, "attaque": 20, "defense": 6},
    }
    def __init__(self):
        self.hero = None
        self.etat_jeu = "menu"
        self.chemin_sauvegarde = "data/sauvegarde.json"
        self.chemin_monstres = "data/monsters.JSON"
        self.templates_monstres = self.charge_monstres()


    def charge_monstres(self):
        if not os.path.exists(self.chemin_monstres):
            print("Fichier monsters.JSON introuvable.")
            return []
        with open(self.chemin_monstres, "r", encoding="utf-8") as f:
            return json.load(f)


    def demarrer(self):
        print("\n" + "="*50)
        print("     BIENVENUE DANS LE JEU RPG PYTHON")
        print("="*50)

        while self.etat_jeu != "fin":
            if self.etat_jeu == "menu":
                self.afficher_menu()
            elif self.etat_jeu == "exploration":
                self.boucle_exploration()



    def afficher_menu(self):
        print("\n--- MENU PRINCIPAL ---")
        print("1. Nouvelle partie")
        print("2. Charger partie")
        print("3. Quitter")

        choix = input("\nVotre choix :").strip()

        if choix == "1":
            self.nouvelle_partie()
        elif choix == "2":
            self.charger()
        elif choix == "3":
            print("\nMerci d'avoir joué !")
            self.etat_jeu = "fin"
        else:
            print("choix invalide")


    def nouvelle_partie(self):
        print("\n--- CREATION DU HERO ---")
        nom = input("Nom de votre heros :").strip()
        if not nom:
            nom = "Heros"

        print("\nClesses disponibles :")
        print("1. Guerrier (PV: 120, ATQ: 18, DEF: 8)")
        print("2. Mage (PV: 80, ATQ: 25, DEF: 4)")
        print("3. Archer (PV: 100, ATQ: 20, DEF: 6")

        choix = input("\nVotre choix : ").strip()
        classes = {
            "1": "Guerrier",
            "2": "Marge",
            "3": "Archer"
        }

        classe = classes.get(choix, "Guerrier")
        self.hero = Hero(nom, classe)

        stats = self.STATS_CLASSE[classe]
        self.hero.pv_max = stats["pv_max"]
        self.hero.pv_actuel = stats["pv_max"]
        self.hero.attaque = stats["attaque"]
        self.hero.defense = stats["defense"]

        potion_depart = Potion(nom="Potion de soin", soin=30, valeur=10)
        self.hero.inventaire.ajouter(potion_depart)

        print(f"\n {self.hero.nom} le {classe} est prêt à l'aventure !")
        print(self.hero)
        self.etat_jeu = "exploration"


    def boucle_exploration(self):
        print("\n--- EXPLORATION ---")
        print("1. Avancer dans le donjon")
        print("2. Afficher mes statistiques")
        print("3. Afficher mon inventaire")
        print("4. Sauvegarder et quitter")

        choix = input("\nVotre choix :").strip()
        if choix == "1":
            self.evenement_aleatoire()
        elif choix == "2":
            print(f"\n{self.hero}")
        elif choix == "3":
            self.hero.inventaire.afficher()
        elif choix == "4":
            self.sauvegarder()
            print("\nPartie sauvegardée. À bientôt !")
            self.etat_jeu = "menu"
        else:
            print("Choix invalide")

        print("\nVous avancez prudemment dans le donjon...")
        tirage = random.random()

        if tirage < 0.60:
            monstre = self.generer_monstre()
            if monstre:
                self.lancer_combat(monstre)
        elif tirage < 0.80:
            self.trouver_coffre()
        else:
            self.se_reposer()

        if not self.hero.est_vivant():
            print(f"\n {self.hero.nom} est mort. Fin de partie.")
            self.etat_jeu = "menu"

    def trouver_coffre(self):
        print("\nVous trouvez un coffre !")
        butin = random.choice([
            Potion(nom="Potion de soin", soin=30, valeur=10),
            Potion(nom="Grande Potion", soin=60, valeur=25),
            Arme(nom="Épée rouillée", degats_bonus=3, valeur=15),
            Arme(nom="Dague acérée", degats_bonus=5, valeur=30),
        ])
        print(f"Vous obtenez : {butin}")
        self.hero.inventaire.ajouter(butin)

    def se_reposer(self):
        soin = int(self.hero.pv_max * 0.3)
        soin_reel = min(soin, self.hero.pv_max - self.hero.pv_actuel)
        self.hero.pv_actuel += soin_reel
        print(f"\n Vous trouvez un endroit calme pour vous reposer.")
        print(f"Vous récupérez {soin_reel} PV. ({self.hero.pv_actuel}/{self.hero.pv_max})")

    def generer_monstre(self):
        niveau_hero = self.hero.niveau

        disponibles = [
            m for m in self.templates_monstres
            if m["niveau_min"] <= niveau_hero
        ]

        if not disponibles:
            disponibles = self.templates_monstres
        template = random.choice(disponibles)

        facteur = 1 + (niveau_hero - 1) * 0.2
        pv = int(template["pv"] * facteur)
        attaque = int(template["attaque"] * facteur)
        defense = int(template["defense"] * facteur)

        loot = [
            Potion(nom="Potion de soin", soin=30, valeur=10),
            Arme(nom="Épée rouillée", degats_bonus=3, valeur=15),
        ]
        return Monstre(
            nom=template["nom"],
            pv_max=pv,
            attaque=attaque,
            defense=defense,
            xp_donne=template["xp_donne"],
            loot_possible=loot
        )

    """DEBUT DU SYSTEM DE COMBAT"""

    def lancer_combat(self, monstre):
        print(f"\nUn {monstre.nom} apparaît !")
        print(f"   {monstre}")
        print("-" * 40)

        while self.hero.est_vivant() and monstre.est_vivant():
            self.afficher_etat_combat(monstre)
            action = self.choisir_action_combat()

            if action == "1":
                self.action_attaquer(monstre)
            elif action == "2":
                self.action_utiliser_objet()
            elif action == "3":
                if self.action_fuir():
                    return
            else:
                print("Choix invalide.")
                continue

        def afficher_etat_combat(self, monstre):
            print(f"\n  {self.hero.nom} : {self.hero.pv_actuel}/{self.hero.pv_max} PV")
            print(f"  {monstre.nom}  : {monstre.pv_actuel}/{monstre.pv_max} PV")

        def choisir_action_combat(self):
            print("\n  Que faites-vous ?")
            print("  1. Attaquer")
            print("  2. Utiliser un objet")
            print("  3. Fuir")
            return input("  Votre choix : ").strip()

        def action_attaquer(self, monstre):
            degats = self.hero.attaquer(monstre)
            print(f"\n  {self.hero.nom} attaque {monstre.nom} pour {degats} dégâts !")
            if not monstre.est_vivant():
                print(f"  {monstre.nom} est vaincu !")

        def action_utiliser_objet(self):
            self.hero.inventaire.afficher()
            if not self.hero.inventaire.items:
                return

            choix = input("  Numéro de l'objet (0 pour annuler) : ").strip()
            if not choix.isdigit():
                print("  Entrée invalide.")
                return

            index = int(choix) - 1
            if choix == "0":
                return
            if 0 <= index < len(self.hero.inventaire.items):
                item = self.hero.inventaire.items[index]
                self.hero.inventaire.utiliser(item, self.hero)
            else:
                print("  Numéro invalide.")

        def action_fuir(self):
            if random.random() < 0.5:
                print(f"\n {self.hero.nom} prend la fuite !")
                return True
            print(f"\n  {self.hero.nom} ne peut pas fuir !")
            return False

        def tour_monstre(self, monstre):
            if random.random() < 0.2:
                degats_bruts = monstre.attaque_speciale()
                degats = self.hero.recevoir_degats(degats_bruts)
            else:
                degats = monstre.attaquer(self.hero)
            print(f"  {monstre.nom} attaque {self.hero.nom} pour {degats} dégâts !")

        def victoire(self, monstre):
            print(f"\nVictoire ! Vous avez vaincu {monstre.nom} !")
            self.hero.gagner_xp(monstre.xp_donne)
            loot = monstre.generer_loot()
            if loot:
                self.hero.inventaire.ajouter(loot)

        def defaite(self):
            print(f"\n{self.hero.nom} est tombé au combat...")
            print("Game Over.")

        def sauvegarder(self):
            if self.hero is None:
                print("Aucun héros à sauvegarder.")
                return
            os.makedirs(name="data", exist_ok=True)

        donnees = {
            "nom": self.hero.nom,
            "classe": self.hero.classe_hero,
            "niveau": self.hero.niveau,
            "xp": self.hero.xp,
            "xp_pour_niveau": self.hero.xp_pour_niveau,
            "pv_actuel": self.hero.pv_actuel,
            "pv_max": self.hero.pv_max,
            "attaque": self.hero.attaque,
            "defense": self.hero.defense,
            "vitesse": self.hero.vitesse,
            "or": self.hero.or_possede,
            "inventaire": [
                {
                    "nom": item.nom,
                    "type": item.type_item,
                    "effet": item.effet,
                    "valeur": item.valeur,
                    "soin": getattr(item, "soin", 0),
                    "degats_bonus": getattr(item, "degats_bonus", 0),
                }
                for item in self.hero.inventaire.items
            ]
        }

        with open(self.chemin_sauvegarde, "w", encoding="utf-8") as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)

    def charger(self):
        if not os.path.exists(self.chemin_sauvegarde):
            print("\nAucune sauvegarde trouvée.")
            return

        with open(self.chemin_sauvegarde, "r", encoding="utf-8") as f:
            donnees = json.load(f)

        self.hero = Hero(donnees["nom"], donnees["classe"])
        self.hero.niveau = donnees["niveau"]
        self.hero.xp = donnees["xp"]
        self.hero.xp_pour_niveau = donnees["xp_pour_niveau"]
        self.hero.pv_actuel = donnees["pv_actuel"]
        self.hero.pv_max = donnees["pv_max"]
        self.hero.attaque = donnees["attaque"]
        self.hero.defense = donnees["defense"]
        self.hero.vitesse = donnees["vitesse"]
        self.hero.or_possede = donnees["or"]

        for item_data in donnees["inventaire"]:
            if item_data["type"] == "arme":
                item = Arme(item_data["nom"], item_data["degats_bonus"], item_data["valeur"])
            elif item_data["type"] == "potion":
                item = Potion(item_data["nom"], item_data["soin"], item_data["valeur"])
            else:
                continue
            self.hero.inventaire.ajouter(item)

        print(f"\nPartie de {self.hero.nom} chargée avec succès !")
        print(self.hero)
        self.etat_jeu = "exploration"