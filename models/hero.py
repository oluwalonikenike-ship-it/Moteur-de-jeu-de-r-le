from models.personnage import Personnage


class Hero(Personnage):
    

    def __init__(self, nom, classe_hero):
        
        super().__init__(
            nom=nom,
            pv_max=100,
            attaque=15,
            defense=5,
            vitesse=10
        )
        self.classe_hero = classe_hero
        self.inventaire = []
        self.or_possede = 0
        self.xp_pour_niveau = 100

    def gagner_xp(self, montant):
        
        self.xp += montant
        print(f"{self.nom} gagne {montant} XP ! (Total : {self.xp})")
        if self.xp >= self.xp_pour_niveau:
            self.monter_niveau()

    def monter_niveau(self):
        
        self.niveau += 1
        self.xp = 0
        self.xp_pour_niveau = self.niveau * 100
        self.pv_max += 20
        self.pv_actuel = self.pv_max
        self.attaque += 3
        self.defense += 2
        print(f"🎉 {self.nom} monte au niveau {self.niveau} !")

    def utiliser_objet(self, item):
        
        if item in self.inventaire:
            item.utiliser(self)
            self.inventaire.remove(item)
        else:
            print("Cet objet n'est pas dans l'inventaire.")

    def sauvegarder(self):
        
        return {
            "nom": self.nom,
            "classe_hero": self.classe_hero,
            "pv_max": self.pv_max,
            "pv_actuel": self.pv_actuel,
            "attaque": self.attaque,
            "defense": self.defense,
            "vitesse": self.vitesse,
            "niveau": self.niveau,
            "xp": self.xp,
            "xp_pour_niveau": self.xp_pour_niveau,
            "or_possede": self.or_possede
        }

    def __str__(self):
        
        return (f"{self.nom} ({self.classe_hero}) | "
                f"PV: {self.pv_actuel}/{self.pv_max} | "
                f"Niveau: {self.niveau} | XP: {self.xp}/"
                f"{self.xp_pour_niveau}")