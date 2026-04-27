"""Module contenant la classe Personnage."""


class Personnage:
    """Classe de base pour tous les personnages du jeu."""

    def __init__(self, nom, pv_max, attaque, defense, vitesse):
        """Initialise un personnage avec ses statistiques de base."""
        if not isinstance(nom, str) or not nom.strip():
            raise ValueError("Le nom doit être une chaine de caractères non vide.")
        if pv_max <= 0:
            raise ValueError("Les PV max doivent être positifs.")
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
        """Retourne True si le personnage a encore des PV."""
        return self.pv_actuel > 0

    def recevoir_degats(self, degats):
        """Calcule et applique les dégâts reçus après défense."""
        if not isinstance(degats, (int, float)) or degats < 0:
            raise ValueError("Les dégâts doivent être un nombre positif.")
        degats_reels = max(1, degats - self.defense)
        self.pv_actuel -= degats_reels
        self.pv_actuel = max(0, self.pv_actuel)
        return degats_reels

    def attaquer(self, cible):
        """Attaque une cible et retourne les dégâts infligés."""
        if cible is None:
            raise ValueError("La cible ne peut pas être None.")
        return cible.recevoir_degats(self.attaque)

    def __str__(self):
        """Retourne une description lisible du personnage."""
        return (
            f"{self.nom} | PV: {self.pv_actuel}/{self.pv_max} | "
            f"ATQ: {self.attaque} | DEF: {self.defense} | Niveau: {self.niveau}"
        )