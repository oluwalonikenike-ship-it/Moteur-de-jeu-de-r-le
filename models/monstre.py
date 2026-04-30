"""Module contenant la classe Monstre."""
import random
from models.personnage import Personnage


class Monstre(Personnage):
    """Adversaire créé aléatoirement dans le jeu."""

    def __init__(self, nom, pv_max, attaque, defense, xp_donne, loot_possible):
        """Initialisation du monstre."""
        if not isinstance(xp_donne, (int, float)) or xp_donne < 0:
            raise ValueError("L'XP donnée doit être un nombre positif.")
        if not isinstance(loot_possible, list):
            raise ValueError("Le loot possible doit être une liste.")
        super().__init__(
            nom=nom,
            pv_max=pv_max,
            attaque=attaque,
            defense=defense,
            vitesse=5
        )
        self.type_monstre = nom
        self.xp_donne = xp_donne
        self.loot_possible = loot_possible

    def generer_loot(self):
        """Retourne un objet aléatoire du loot possible."""
        if not self.loot_possible:
            return None
        loot = random.choice(self.loot_possible)
        print(f"{self.nom} laisse tomber : {loot.nom} !")
        return loot

    def attaque_speciale(self):
        """Déclenche une attaque spéciale."""
        degats = int(self.attaque * 1.5)
        print(f"{self.nom} utilise une attaque speciale ! ({degats} degats)")
        return degats

    def __str__(self):
        """Retourne une représentation lisible du monstre."""
        return (f"{self.nom} | PV: {self.pv_actuel}/{self.pv_max} "
                f"| ATQ: {self.attaque} | DEF: {self.defense}")