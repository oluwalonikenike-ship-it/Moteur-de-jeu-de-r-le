"""Module contenant la classe Item et ses sous classes"""

class Item:
    """Objet utilisable (potion, arme, armure)"""
    def __init__(self, nom, type_item, effet, valeur):
        """Initialise un item"""
        self.nom = nom
        self.type_item = type_item
        self.effet = effet
        self.valeur = valeur
    def utiliser(self, personnage):
        """utilise l'item sur un personnage """
        pass
    def __str__(self):
        """Retourne une description de l'item """
        return f"{self.nom} ({self.type_item}) - Effet: {self.effet} - Valeur: {self.valeur} or"
class Arme(Item):
    """Arme équipable qui augmente l'attaque"""
    def __init__(self, nom, degats_bonus, valeur):
        """Initialise une arme"""
        super().__init__(
            nom=nom,
            type_item="arme",
            effet=f"+{degats_bonus} attaque",
            valeur=valeur,
        )
        self.degats_bonus = degats_bonus

    def equiper(self, hero):
        """Equipé l'arme sur le héro."""
        hero.attaque += self.degats_bonus
        print(f"{hero.nom} équipe {self.nom} (+{self.degats_bonus} ATQ)")

class Potion(Item):
    """Potion de soin"""
    def __init__(self, nom, soin, valeur):
        """Initialise une potion"""
        super().__init__(
            nom=nom,
            type_item="potion",
            effet=f"+{soin} PV",
            valeur=valeur
        )
        self.soin = soin
    def utiliser(self, personnage):
        """Restaure des PV au personnage"""
        soin_reel = min(self.soin, personnage.pv_max-personnage.pv_actuel)
        personnage.pv_actuel += soin_reel
        print(f"{personnage.nom} utilise {self.nom} et recupere {soin_reel} PV ! " 
              f"{personnage.pv_actuel}/{personnage.pv_max}")

class Armure(Item):
    """Armre equipable qui augmente la defense"""
    def __init__(self, nom, defense_bonus, valeur):
        super().__init__(
            nom = nom,
            type_item = "armure",
            effet =f"+{defense_bonus} defense",
            valeur = valeur,
        )
        self.defense_bonus = defense_bonus
    def equiper(self, hero):
        hero.defense += self.defense_bonus
        print(f"{hero.nom} équipe {self.nom} (+{self.defense_bonus} DEF)")
    def utiliser(self,hero):
        """Equiper l'arme sur hero"""
        self.equiper(hero)
