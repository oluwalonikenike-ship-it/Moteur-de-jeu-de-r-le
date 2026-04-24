import random
from models.hero import Hero

class CombatEngine: 
    def __init__(self, hero, monstre):
        self.hero =hero
        self.monstre = monstre
        self.tour = 0

    def calculer_degats(self, attaquant, defenseur): 
        return max(1, attaquant.attaque - defenseur.defense)
    
    def afficher_log(self):
        print("-" *40)
        print(f" Tour {self.tour}")
        print(f"{self.hero}")
        print(f"{self.monstre}")
        print("-" *40)

    def tour_hero(self):
        print("\nQue fais-tu ?")
        print("[1]. Attaquer")
        print("[2] Défendre")
        print("[3] Utiliser un objet")

        choix = input("Choisis ton action : ")

        if choix == "1":
            degats =self.calculer_degats(self.hero, self.monstre)
            self.monstre.pv_actuel -= degats
            self.monstre.pv_actuel =max(0, self.monstre.pv_actuel)
            print(f"Tu frappes {self.monstre.nom} pour {degats} dégâts!")

        elif choix == "2":
            if random.random() < 0.5:
                print(f"{self.monstre.nom} a raté son attaque!")
                return "fuite"
            else:
                print("Impossible de fuir! Le monstre t'attaque!")
                degats =self.calculer_degats(self.monstre, self.hero)
                self.hero.pv_actuel -= degats
                self.hero.pv_actuel = max(0, self.hero.pv_actuel)
                print(f"{self.monstre.nom} t'inflige {degats} dégâts!")

        elif choix == "3":
            potions = [i for i in self.hero.inventaire.items if i.type_item  =="potion"]
            if potions :
                self.hero.utiliser_objet(potions[0])
            else: 
                print("Tu n'as pas de potion!")

        else:
            print("Choix invalide! Tu perds ton tour.")
            return "continue"

    def tour_monstre(self):
        """Gère le tour du monstre"""    
        degats = self.calculer_degats(self.monstre, self.hero)
        self.hero.pv_actuel -= degats
        self.hero.pv_actuel = max(0, self.hero.pv_actuel)
        print(f"{self.monstre.nom} t'attaque pour {degats} dégâts!") 

    def verifier_fin(self):
        if not self.hero.est_vivant():
            return "defaite"
        if not self.monstre.est_vivant():
            return "victoire"
        return "continue"
           
    def lancer_combat(self):
        print(f"\n  Un {self.monstre.nom} surgit!")
        while True:
            self.tour += 1
            self.afficher_log()
            resultat = self.tour_hero()
            if resultat == "fuite":
                return "fuite"
            fin = self.verifier_fin()
            if fin == "victoire":
               print(f"Tu as vaincu {self.monstre.nom}!")
               self.hero.gagner_xp(self.monstre.xp_donne)
               return "victoire"
            
            self.tour_monstre()

            fin = self.verifier_fin()
            if fin == "defaite":
                print(f"\n Tu as été vaincu par {self.monstre.nom}... Game Over.")
                return "defaite"
