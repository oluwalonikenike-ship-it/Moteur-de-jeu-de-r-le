import json
import os

class DataLoader:
    FICHIER_ITEMS = "items.json"
    FICHIER_MONSTERS = "monsters.json"

def __init__(self, dossier_data: str = "data"):
    self.dossier_data = dossier_data

def charger_items(self) -> list:
    return self._lire_json(self.FICHIER_ITEMS)

def charger_monsters(self) -> list:
    return self._lire_json(self.FICHIER_MONSTERS)

def get_items_par_type(self,type_item:str) -> list:
    items = self.charger_items()
    return [item for item in items if item["type_item"] == type_item]

def get_monsters_par_type(self,niveau_hero: int) -> list:
    monsters = self.charger_monsters()
    return [m for m in monsters if m["niveau"] <= niveau_hero]

def get_monsters_par_nom(self, nom: str) -> dict |   None:
    monsters = self.charger_monsters()
    for monster in monsters:
        if monster["nom"].lower() == nom.lower():
            return monster
    return None

def get_item_par_nom(self, nom: str) -> dict | None:
    items = self.charger_items()
    for item in items:
        if item["nom"].lower() == nom.lower():
            return item
    return None

def afficher_catalogue_items(self):
    items = self.charger_items()
    types = ["potion", "arme", "armure"]
    print(f"\n{'=' * 40}")
    print("Catalogue des items :")
    print(f"{'='*40}")
    for type_item in types:
     groupe = [i for i in items if i ["type_item"] == type_item]
    if groupe:
        print(f"\n {type_item.upper()}S :")
        for item in groupe:
           int(
                        f"    • {item['nom']:<25} "
                        f"Effet: {item['effet']:>3}  "
                        f"Prix: {item['valeur']} or"
                    )
        print(f"\n{'='*40}\n")
 
    def afficher_catalogue_monstres(self) -> None:
        """Affiche dans la console tous les monstres disponibles."""
        monstres = self.charger_monstres()
        print(f"\n{'='*40}")
        print("  BESTIAIRE")
        print(f"{'='*40}")
        for m in monstres:
            print(
                f"  • {m['nom']:<12} "
                f"PV: {m['pv']:>3}  "
                f"ATK: {m['attaque']:>2}  "
                f"DEF: {m['defense']:>2}  "
                f"XP: {m['xp_donne']:>3}  "
                f"Niv.min: {m['niveau_min']}"
            )
        print(f"{'='*40}\n")

def _lire_json(self, nom_fichier: str) -> list:
    chemin = os.path.join(self.dossier_data, nom_fichier)
    if not os.path.isfile(chemin):
        raise FileNotFoundError(f"Fichier introuvable: {chemin}")
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            return json.load(f)
    
    except json.JSONDecodeError as e:
      raise ValueError(f" fichier JSON invalide ({nom_fichier}) : {e}") from e
    