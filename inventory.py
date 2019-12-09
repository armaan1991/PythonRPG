# Inventory
from utils import print_slow, print_options, clear_screen, input_int


# inventory = {'Coins': 0, 'Weapons': ['Sword','Dagger'], 'Helms':[],'Chest Armour':[], 'Leg Armour':[], 'Shields':[]}
# equipped = {'Weapons': 'Battle Axe', 'Helms': 'Rune helm' ,'Chest Armour':[], 'Leg Armour':[], 'Shields':[]}

# loot drop function


def view_inventory(hero):
    inventory_options = {
            1: "coins",
            2: "weapons",
            3: "helms",
            4: "chest armour",
            5: "leg armour",
            6: "shields",
            7: "back"
    }
    while True:
        clear_screen()
        print("Inventory:")
        print_options(inventory_options)
        action = int(input(" -->"))
        if action == 1:
            print_slow(
                "You have {} Coins in your purse\n".format(
                    hero.inventory["Coins"]
                )
            )
            break
        elif action > 1 and action < 7:
            clear_screen()
            print_slow(
                "You have chosen to see {} : {} \n".format(
                    action, inventory_options.get(action)
                )
            )
            view_category(action, inventory_options.get(action), hero)
        elif action == 7:
            clear_screen()
            break
        else:
            print_slow("Choose valid option")
            continue


def view_category(action, category, hero):
    hero.print_inventory(category)
    # Need to better understand what the point of this
    # function is, the current implementation is still messy
    # Also, this should just be a function in the hero class
    # Since you're making a view of a hero attribute
    n_invent = hero.get_n_inventory(category) + 1
    while True:
        response = input_int()
        if response < n_invent:
            item = hero.inventory[category][response - 1]
            clear_screen()
            options(item, category, action, hero)
            break
        elif response == n_invent:
            clear_screen()
            view_inventory(hero)
            break
        else:
            print_slow("Choose valid option")
            continue


def options(item, category, action, hero):
    options_map = {1: "equip", 2: "drop", 3: "back"}
    while True:
        old_item = hero.get_equipped(category)
        print_slow("Currently equipped: {} \n".format(old_item))
        print_slow("Selected item : {} \n".format(item))
        print_options(options_map)
        answer = options_map[int(input("\n -->"))]
        if answer == "equip":
            hero.equip(item, category, old_item)
            view_category(action, category, hero)
            break
        elif answer == "drop":
            while True:
                print_slow("Are you sure you want to drop item? \n")
                print_slow("1. Yes \n" + "2. No \n")
                answer = input_int()
                if answer == 1:
                    hero.drop(item, category)
                    options(item, category, action, hero)
                elif answer == 2:
                    options(item, category, action, hero)
                    break
                else:
                    print_slow("Please choose a valid option")
                    continue
