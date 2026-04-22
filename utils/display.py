def afficher_titre(texte)
     print("\n"  + "=" * 40)
     print(f"{texte}")
     print("=" * 40)

def afficher_separateur():
    print("-" * 40)

def afficher_menu(options):
    for i, option in enumerate(options, 1):
     print(f"{i}. {option}")

def demander_choix(options):
    while True:
          
        choix = input("\n> ").strip()      
        if choix.isdigit() and 1 <= int(choix) <= nb_options:
            return int(choix)
        print(f"Choix invalide. Entre un nombre entre 1 et {nb_options}.")

def afficher_stats_hero(hero):
    afficher_separateur()
    print(f" Nom: {hero.nom} ({hero.classe_hero})")
    print(f" PV : {hero.pv_actuel}/{hero.pv_max}")
    print(f" Niveau : {hero.niveau}")
    print(f" XP: {hero.xp}/{hero.xp_pour_niveau}")
    print(f" Attaque : {hero.attaque}")
    print(f" Défense : {hero.defense}")
    print(f" Or : {hero.or_possede}")
    afficher_separateur()


