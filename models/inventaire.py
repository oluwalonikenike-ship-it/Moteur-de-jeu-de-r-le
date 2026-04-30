"""Module contenant la classe Inventaire."""


class Inventaire:
    """Gestion des objets du héros."""

    def __init__(self):
        """Initialise un inventaire vide avec une capacité maximale de 10."""
        self.items = []
        self.capacite_max = 10

    def ajouter(self, item):
        """Ajoute un item si la capacité n'est pas atteinte."""
        if item is None:
            raise ValueError("Impossible d'ajouter un objet inexistant.")
        if len(self.items) >= self.capacite_max:
            print(f"Inventaire plein ! Impossible d'ajouter {item.nom}.")
            return False
        self.items.append(item)
        print(f"{item.nom} ajouté à l'inventaire.")
        return True

    def supprimer(self, item):
        """Supprime un item de l'inventaire."""
        if item is None:
            raise ValueError("Impossible de supprimer un objet qui n'existe pas.")
        if item in self.items:
            self.items.remove(item)
            print(f"{item.nom} retiré de l'inventaire.")
            return True
        print(f"{item.nom} n'est pas dans l'inventaire.")
        return False

    def utiliser(self, item, personnage):
        if item is None:
            raise ValueError("L'objet ne peut pas être Null/absent.")
        if personnage is None:
            raise ValueError("Le personnage ne peut pas être None.")
        if item in self.items:
            item.utiliser(personnage)
            self.supprimer(item)
        else:
            print(f"{item.nom} n'est pas dans l'inventaire.")

    def afficher(self):
        """Affiche tous les items de l'inventaire."""
        if not self.items:
            print("L'inventaire est vide.")
            return
        print(f"=== Inventaire ({len(self.items)}/{self.capacite_max}) ===")
        for i, item in enumerate(self.items, 1):
            print(f"  {i}. {item}")

    def __str__(self):
        """Retourne une représentation lisible de l'inventaire."""
        if not self.items:
            return "Inventaire vide"
        contenu = ", ".join([item.nom for item in self.items])
        return f"Inventaire ({len(self.items)}/{self.capacite_max}) : {contenu}"