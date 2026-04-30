class Personnage:
    def __init__(self, nom, pv_max, attaque, defense, vitesse):
        if not isinstance(nom, str) or not nom.strip():
            raise ValueError("Le nom ne peut pas etre vide.")
        if pv_max <= 0:
            raise ValueError("Les Point de Vie doivent être positifs.")
        if attaque < 0:
            raise ValueError("L'attaque doit être positive ou nulle.")
        if defense < 0:
            raise ValueError("La défense doit être positive ou nulle.")
        self.nom = nom
        self.pv_max = pv_max
        self.pv_actuel = pv_max
        self.attaque = attaque
        self.defense = defense
        self.vitesse = vitesse
        self.niveau = 1
        self.xp = 0

    def est_vivant(self):
        return self.pv_actuel > 0

    def recevoir_degats(self, degats):
        """Calcule des dégâts reçus après défense."""
        if not isinstance(degats, (int, float)) or degats < 0:
            raise ValueError("Les dégâts doivent être un nombre positif.")
        degats_reels = max(1, degats - self.defense)
        self.pv_actuel -= degats_reels
        self.pv_actuel = max(0, self.pv_actuel)
        return degats_reels

    def attaquer(self, cible):
        if cible is None:
            raise ValueError("La cible ne peut pas être absent.")
        return cible.recevoir_degats(self.attaque)

    def __str__(self):
        return (
            f"{self.nom} | PV: {self.pv_actuel}/{self.pv_max} | "
            f"ATQ: {self.attaque} | DEF: {self.defense} | Niveau: {self.niveau}"
        )