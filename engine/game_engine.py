"""Module contenant le moteur principal du jeu."""
import json
import os
import random
from models.hero import Hero
from models.monstre import Monstre
from models.item import Arme, Potion, Armure
from database import Database
from data_loader import DataLoader

class CombatError(Exception):
    """Exception levée lors d'erreurs de combat."""
    pass
class GameEngine:
    """Orchestre la boucle principale du jeu."""

    STATS_CLASSE = {
        "Guerrier": {"pv_max": 120, "attaque": 18, "defense": 8},
        "Mage": {"pv_max": 80, "attaque": 25, "defense": 4},
        "Archer": {"pv_max": 100, "attaque": 20, "defense": 6},
    }

    def __init__(self):
        """Initialise le moteur de jeu."""
        self.hero = None
        self.etat_jeu = "menu"
        self.chemin_sauvegarde = "data/sauvegarde.json"
        try:
            self.loader = DataLoader()
            self.templates_monstres = self.loader.charger_monstres()
        except FileNotFoundError as e:
            print(f"Erreur chargement monstres : {e}")
            self.templates_monstres = []
        try:
            self.db = Database()
        except Exception as e:
            print(f"Erreur connexion base de données : {e}")
            self.db = None

    def demarrer(self):
        """Démarre le jeu et affiche le menu principal."""
        print("\n" + "=" * 50)
        print("     BIENVENUE DANS LE JEU RPG PYTHON")
        print("=" * 50)

        while self.etat_jeu != "fin":
            if self.etat_jeu == "menu":
                self.afficher_menu()
            elif self.etat_jeu == "exploration":
                self.boucle_exploration()

    def afficher_menu(self):
        """Affiche le menu principal."""
        print("\n--- MENU PRINCIPAL ---")
        print("1. Nouvelle partie")
        print("2. Charger partie")
        print("3. Quitter")

        try:
            choix = input("\nVotre choix :").strip()
        except EOFError:
            self.etat_jeu = "fin"
            return

        if choix == "1":
            self.nouvelle_partie()
        elif choix == "2":
            self.charger()
        elif choix == "3":
            print("\nMerci d'avoir joue !")
            self.etat_jeu = "fin"
        else:
            print("Choix invalide.")

    def nouvelle_partie(self):
        """Cree un nouveau heros et lance l'exploration."""
        print("\n--- CREATION DU HERO ---")
        try:
            nom = input("Nom de votre heros :").strip()
        except EOFError:
            nom = "Heros"
        if not nom:
            nom = "Heros"

        print("\nClasses disponibles :")
        print("1. Guerrier (PV: 120, ATQ: 18, DEF: 8)")
        print("2. Mage (PV: 80, ATQ: 25, DEF: 4)")
        print("3. Archer (PV: 100, ATQ: 20, DEF: 6)")

        try:
            choix = input("\nVotre choix : ").strip()
        except EOFError:
            choix = "1"

        classes = {
            "1": "Guerrier",
            "2": "Mage",
            "3": "Archer"
        }

        classe = classes.get(choix, "Guerrier")

        try:
            self.hero = Hero(nom, classe)
        except ValueError as e:
            print(f"Erreur creation héros : {e}")
            return

        stats = self.STATS_CLASSE[classe]
        self.hero.pv_max = stats["pv_max"]
        self.hero.pv_actuel = stats["pv_max"]
        self.hero.attaque = stats["attaque"]
        self.hero.defense = stats["defense"]

        try:
            potion_depart = Potion(nom="Potion de soin", soin=30, valeur=10)
            self.hero.inventaire.ajouter(potion_depart)
        except ValueError as e:
            print(f"Erreur ajout potion de départ : {e}")

        print(f"\n{self.hero.nom} le {classe} est pret a l'aventure !")
        print(self.hero)
        self.etat_jeu = "exploration"

    def boucle_exploration(self):
        """Boucle d'exploration principale."""
        print("\n--- EXPLORATION ---")
        print("1. Avancer dans le donjon")
        print("2. Afficher mes statistiques")
        print("3. Afficher mon inventaire")
        print("4. Sauvegarder et quitter")

        try:
            choix = input("\nVotre choix :").strip()
        except EOFError:
            choix = "4"

        if choix == "1":
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
                print(f"\n{self.hero.nom} est mort. Fin de partie.")
                self.etat_jeu = "menu"
        elif choix == "2":
            print(f"\n{self.hero}")
        elif choix == "3":
            self.hero.inventaire.afficher()
        elif choix == "4":
            self.sauvegarder()
            print("\nPartie sauvegardee. A bientot !")
            self.etat_jeu = "menu"
        else:
            print("Choix invalide.")

    def trouver_coffre(self):
        """Le heros trouve un coffre avec un item aleatoire."""
        print("\nVous trouvez un coffre !")
        try:
            items_data = self.loader.charger_items()
        except FileNotFoundError as e:
            print(f"Erreur chargement items : {e}")
            return

        if not items_data:
            print("Le coffre est vide.")
            return

        item_data = random.choice(items_data)
        type_item = item_data["type_item"]
        nom = item_data["nom"]
        effet = item_data["effet"]
        valeur = item_data["valeur"]

        try:
            if type_item == "arme":
                item = Arme(nom, degats_bonus=effet, valeur=valeur)
            elif type_item == "potion":
                item = Potion(nom, soin=effet, valeur=valeur)
            elif type_item == "armure":
                item = Armure(nom, defense_bonus=effet, valeur=valeur)
            else:
                return
            print(f"Vous obtenez : {item}")
            self.hero.inventaire.ajouter(item)
        except ValueError as e:
            print(f"Erreur creation item : {e}")

    def se_reposer(self):
        """Le heros se repose et recupere des PV."""
        soin = int(self.hero.pv_max * 0.3)
        soin_reel = min(soin, self.hero.pv_max - self.hero.pv_actuel)
        self.hero.pv_actuel += soin_reel
        print(f"\nVous trouvez un endroit calme pour vous reposer.")
        print(f"Vous recuperez {soin_reel} PV. ({self.hero.pv_actuel}/{self.hero.pv_max})")

    def generer_monstre(self):
        """Genere un monstre adapte au niveau du heros."""
        if not self.templates_monstres:
            print("Aucun monstre disponible.")
            return None

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

        try:
            loot = [
                Potion(nom="Potion de soin", soin=30, valeur=10),
                Arme(nom="Epee rouillee", degats_bonus=3, valeur=15),
            ]
            return Monstre(
                nom=template["nom"],
                pv_max=pv,
                attaque=attaque,
                defense=defense,
                xp_donne=template["xp_donne"],
                loot_possible=loot
            )
        except ValueError as e:
            print(f"Erreur creation monstre : {e}")
            return None

    # Systeme de combat

    def lancer_combat(self, monstre):
        """Lance et gere la boucle de combat complete."""
        if monstre is None:
            raise CombatError("Impossible de lancer un combat sans monstre.")

        print(f"\nUn {monstre.nom} apparait !")
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

            if monstre.est_vivant():
                self.tour_monstre(monstre)

        if not self.hero.est_vivant():
            self.defaite()
        elif not monstre.est_vivant():
            self.victoire(monstre)

    def afficher_etat_combat(self, monstre):
        """Affiche l'etat des deux combattants."""
        print(f"\n  {self.hero.nom} : {self.hero.pv_actuel}/{self.hero.pv_max} PV")
        print(f"  {monstre.nom}  : {monstre.pv_actuel}/{monstre.pv_max} PV")

    def choisir_action_combat(self):
        """Affiche les actions et retourne le choix."""
        print("\n  Que faites-vous ?")
        print("  1. Attaquer")
        print("  2. Utiliser un objet")
        print("  3. Fuir")
        try:
            return input("  Votre choix : ").strip()
        except EOFError:
            return "1"

    def action_attaquer(self, monstre):
        """Le heros attaque le monstre."""
        if monstre is None:
            raise ValueError("Le monstre ne peut pas être None.")
        degats = self.hero.attaquer(monstre)
        print(f"\n  {self.hero.nom} attaque {monstre.nom} pour {degats} degats !")
        if not monstre.est_vivant():
            print(f"  {monstre.nom} est vaincu !")

    def action_utiliser_objet(self):
        """Le heros utilise un objet de son inventaire."""
        self.hero.inventaire.afficher()
        if not self.hero.inventaire.items:
            return

        try:
            choix = input("  Numero de l'objet (0 pour annuler) : ").strip()
        except EOFError:
            return

        if not choix.isdigit():
            print("  Entree invalide.")
            return

        index = int(choix) - 1
        if choix == "0":
            return
        if 0 <= index < len(self.hero.inventaire.items):
            item = self.hero.inventaire.items[index]
            try:
                self.hero.inventaire.utiliser(item, self.hero)
            except ValueError as e:
                print(f"  Erreur utilisation objet : {e}")
        else:
            print("  Numero invalide.")

    def action_fuir(self):
        """Le heros tente de fuir le combat."""
        if random.random() < 0.5:
            print(f"\n{self.hero.nom} prend la fuite !")
            return True
        print(f"\n  {self.hero.nom} ne peut pas fuir !")
        return False

    def tour_monstre(self, monstre):
        """Le monstre attaque le heros."""
        if monstre is None:
            raise ValueError("Le monstre ne peut pas être None.")
        if random.random() < 0.2:
            degats_bruts = monstre.attaque_speciale()
            degats = self.hero.recevoir_degats(degats_bruts)
        else:
            degats = monstre.attaquer(self.hero)
        print(f"  {monstre.nom} attaque {self.hero.nom} pour {degats} degats !")

    def victoire(self, monstre):
        """Gere la victoire du heros."""
        print(f"\nVictoire ! Vous avez vaincu {monstre.nom} !")
        try:
            self.hero.gagner_xp(monstre.xp_donne)
        except ValueError as e:
            print(f"Erreur gain XP : {e}")
        loot = monstre.generer_loot()
        if loot:
            self.hero.inventaire.ajouter(loot)
        if self.db:
            try:
                self.db.enregistrer_partie(self.hero, "victoire")
                self.db.enregistrer_score(self.hero)
            except Exception as e:
                print(f"Erreur enregistrement : {e}")

    def defaite(self):
        """Gere la defaite du heros."""
        print(f"\n{self.hero.nom} est tombe au combat...")
        print("Game Over.")
        if self.db:
            try:
                self.db.enregistrer_partie(self.hero, "defaite")
            except Exception as e:
                print(f"Erreur enregistrement : {e}")

    def sauvegarder(self):
        """Sauvegarde la progression dans un fichier JSON."""
        if self.hero is None:
            print("Aucun heros a sauvegarder.")
            return
        try:
            os.makedirs("data", exist_ok=True)
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
                        "defense_bonus": getattr(item, "defense_bonus", 0),
                    }
                    for item in self.hero.inventaire.items
                ]
            }
            with open(self.chemin_sauvegarde, "w", encoding="utf-8") as f:
                json.dump(donnees, f, indent=4, ensure_ascii=False)
        except OSError as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    def charger(self):
        """Charge une partie depuis un fichier JSON."""
        if not os.path.exists(self.chemin_sauvegarde):
            print("\nAucune sauvegarde trouvee.")
            return
        try:
            with open(self.chemin_sauvegarde, "r", encoding="utf-8") as f:
                donnees = json.load(f)
        except json.JSONDecodeError:
            print("\nErreur : fichier de sauvegarde corrompu.")
            return
        except OSError as e:
            print(f"\nErreur lors du chargement : {e}")
            return

        try:
            self.hero = Hero(donnees["nom"], donnees["classe"])
        except (KeyError, ValueError) as e:
            print(f"Erreur recreation héros : {e}")
            return

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
            try:
                if item_data["type"] == "arme":
                    item = Arme(item_data["nom"], item_data["degats_bonus"], item_data["valeur"])
                elif item_data["type"] == "potion":
                    item = Potion(item_data["nom"], item_data["soin"], item_data["valeur"])
                elif item_data["type"] == "armure":
                    item = Armure(item_data["nom"], item_data["defense_bonus"], item_data["valeur"])
                else:
                    continue
                self.hero.inventaire.ajouter(item)
            except (KeyError, ValueError) as e:
                print(f"Erreur chargement item : {e}")
                continue

        print(f"\nPartie de {self.hero.nom} chargee avec succes !")
        print(self.hero)
        self.etat_jeu = "exploration"