"""Module contenant la classe Item et ses sous-classes."""


class Item:
    """Objet utilisable (potion, arme, armure)."""

    def __init__(self, nom, type_item, effet, valeur):
        """Initialise un item."""
        if not isinstance(nom, str) or not nom.strip():
            raise ValueError("Le nom de l'item doit être une chaine non vide.")
        if not isinstance(valeur, (int, float)) or valeur < 0:
            raise ValueError("La valeur doit être un nombre positif.")
        self.nom = nom
        self.type_item = type_item
        self.effet = effet
        self.valeur = valeur

    def utiliser(self, personnage):
        """Utilise l'item sur un personnage."""
        if personnage is None:
            raise ValueError("Le personnage ne peut pas être None.")

    def __str__(self):
        """Retourne une description de l'item."""
        return f"{self.nom} ({self.type_item}) - Effet: {self.effet} - Valeur: {self.valeur} or"


class Arme(Item):
    """Arme équipable qui augmente l'attaque."""

    def __init__(self, nom, degats_bonus, valeur):
        """Initialise une arme."""
        if not isinstance(degats_bonus, (int, float)) or degats_bonus < 0:
            raise ValueError("Les dégâts bonus doivent être positifs.")
        super().__init__(
            nom=nom,
            type_item="arme",
            effet=f"+{degats_bonus} attaque",
            valeur=valeur,
        )
        self.degats_bonus = degats_bonus

    def equiper(self, hero):
        """Équipe l'arme sur le héros."""
        if hero is None:
            raise ValueError("Le héros ne peut pas être None.")
        hero.attaque += self.degats_bonus
        print(f"{hero.nom} équipe {self.nom} (+{self.degats_bonus} ATQ)")


class Potion(Item):
    """Potion de soin."""

    def __init__(self, nom, soin, valeur):
        """Initialise une potion."""
        if not isinstance(soin, (int, float)) or soin < 0:
            raise ValueError("Le soin doit être un nombre positif.")
        super().__init__(
            nom=nom,
            type_item="potion",
            effet=f"+{soin} PV",
            valeur=valeur
        )
        self.soin = soin

    def utiliser(self, personnage):
        """Restaure des PV au personnage sans dépasser le maximum."""
        if personnage is None:
            raise ValueError("Le personnage ne peut pas être None.")
        soin_reel = min(self.soin, personnage.pv_max - personnage.pv_actuel)
        personnage.pv_actuel += soin_reel
        print(f"{personnage.nom} utilise {self.nom} et récupère {soin_reel} PV ! "
              f"({personnage.pv_actuel}/{personnage.pv_max})")


class Armure(Item):
    """Armure équipable qui augmente la défense."""

    def __init__(self, nom, defense_bonus, valeur):
        """Initialise une armure."""
        if not isinstance(defense_bonus, (int, float)) or defense_bonus < 0:
            raise ValueError("Le bonus de défense doit être positif.")
        super().__init__(
            nom=nom,
            type_item="armure",
            effet=f"+{defense_bonus} defense",
            valeur=valeur,
        )
        self.defense_bonus = defense_bonus

    def equiper(self, hero):
        """Équipe l'armure sur le héros."""
        if hero is None:
            raise ValueError("Le héros ne peut pas être None.")
        hero.defense += self.defense_bonus
        print(f"{hero.nom} équipe {self.nom} (+{self.defense_bonus} DEF)")

    def utiliser(self, hero):
        """Utiliser une armure l'équipe automatiquement."""
        if hero is None:
            raise ValueError("Le héros ne peut pas être None.")
        self.equiper(hero)