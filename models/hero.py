    
from models.personnage import Personnage
from models.inventaire import Inventaire

class Hero(Personnage):

    def __init__(self, nom, classe_hero):
        if not isinstance(classe_hero, str) or not classe_hero.strip():
            raise ValueError("La classe du héros ne doit pas etre vide.")
        super().__init__(
            nom=nom,
            pv_max=100,
            attaque=15,
            defense=5,
            vitesse=10
        )
        self.classe_hero = classe_hero
        self.inventaire = Inventaire()
        self.or_possede = 0
        self.xp_pour_niveau = 100

    def gagner_xp(self, montant):
        self.xp += montant
        print(f"{self.nom} gagne {montant} XP ! (Total : {self.xp})")
        if not isinstance(montant, (int, float)) or montant < 0:
            raise ValueError("L'XP doit être un nombre positif.")

    def monter_niveau(self):
        self.niveau += 1
        self.xp = 0
        self.xp_pour_niveau = self.niveau * 100
        self.pv_max += 20
        self.pv_actuel = self.pv_max
        self.attaque += 3
        self.defense += 2
        print(f"🎉 {self.nom} monte au niveau {self.niveau} !")
        print(f"PV max: { self.pv_max} | ATQ: {self.attaque} | DEF: {self.defense}")
    
    def utiliser_objet(self, item):
        """Utilise un objet de l'inventaire sur le héros."""
        if item is None:
            raise ValueError("L'objet ne peut pas être None.")
        if item in self.inventaire.items:
            item.utiliser(self)
            self.inventaire.supprimer(item)
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
       
