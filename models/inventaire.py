"""Module contenant la classe Inventaire"""

class Inventaire:
    """Gestion des objets du héros"""
    def __init__(self):
        self.items = []
        self.capacite_max = 10
    def ajouter(self, item):
        if len(self.items) >= self.capacite_max :
            print(f"Inventaire plein ! Impossible d'ajouter {item.nom}.")
            return False
        self.items.append(item)
        print(f"{item.nom}  ajouté a l'inventaire")
        return True
    def supprimer(self, item):
        if item in self.items :
            self.items.remove(item)
            print(f"{item.nom} retire de l'inventaire")
            return True
        print(f"{item.nom} n'est pas dans l'inventaire")
        return False
    def utiliser(self, item, personnage):
       if item in self.items:
           item.utiliser(personnage)
           self.supprimer(item)
       else:
           print(f"{item.nom} n'est pas dans l'inventaire")
    def afficher(self):
        if not self.items:
            print("L'inventaire est vide")
            return
        print(f"=== Inventaire ({len(self.items)}/{self.capacite_max})")
        for i, item in enumerate(self.items, 1):
            print(f" {i}. {item}")
    def __str__(self):
        if not self.items:
            return "Inventaire vide"
        contenu = ", ".join([item.nom for item in self.items])
        return f"Inventaire ({len(self.items)}/{self.capacite_max}) : {contenu}"
