import os
from utils import (
    print_slow,
    input_str,
    roll,
    input_int,
    print_options,
    clear_screen,
)
import pandas as pd

# $str,defense,agi,intel,hitchance,critchance,critmulti
WEAPON_LIST = pd.read_csv("dog_weapons_v1.csv")

night_elf = [1000, 10, 5, 10, 80, 10, 1.5]
shadow_assasin = [2, 10, 15, 10, 90, 30, 1.5]
blood_priest = [6, 6, 3, 10, 85, 10, 1.5]
level = 1


class Hero:
    # class attributes
    _inventory_options = {
        1: "coins",
        2: "weapons",
        3: "helms",
        4: "chest armour",
        5: "leg armour",
        6: "shields",
        7: "back",
    }

    def __init__(
        self,
        name,
        hero_class,
        strength,
        defense,
        agility,
        intel,
        hit_chance,
        crit_chance,
        crit_multi,
    ):
        self.name = name
        self.hero_class = hero_class
        self.strength = strength
        self.hp = 100 + self.strength
        self.health = self.hp
        self.damage = self.strength * 0.5 + 5
        self.agility = agility
        self.hit_chance = hit_chance
        self.crit_chance = crit_chance + self.agility
        self.defense = defense
        self.intel = intel
        self.crit_multi = crit_multi
        self.greed = 1
        self.inventory = {
            "coins": 1000,
            "weapons": [],
            "helms": [],
            "chest armour": [],
            "leg armour": [],
            "shields": [],
        }
        self.equipped = {
            "weapons": "",
            "helms": "",
            "chest armour": "",
            "leg armour": "",
            "shields": "",
        }
        self.wealth = []
        self.pots = {"small": 1, "medium": 0, "large": 0}
        self.coins = 0

    ################
    # ERROR CHECKS #
    ################
    def _check_equipped(self, category):
        if category not in self.equipped:
            raise KeyError(
                "The category {} is not in the list of "
                "available categories for equipped items".format(category)
            )

    def _check_inventory(self, category):
        if category not in self.inventory:
            raise KeyError(
                "The category {} is not in the list of "
                "available categories for inventory items".format(category)
            )

    ###########
    # GETTERS #
    ###########
    def get_equipped(self, category):
        self._check_equipped(category)
        return self.equipped[category]

    def get_n_equipped(self, category):
        self._check_equipped(category)
        return len(self.equipped[category])

    def get_inventory(self, category):
        self._check_inventory(category)
        return self.inventory[category]

    def get_n_inventory(self, category):
        self._check_inventory(category)
        return len(self.inventory[category])

    #################
    # PRINT METHODS #
    #################
    def print_inventory(self, category):
        inventory = self.get_inventory(category)
        if not inventory:
            print_slow(" You currently have no items for this slot \n")
            return

        for i, item in enumerate(inventory, 1):
            print_slow("{} : {} \n".format(i, item))

        print_slow("{} : Back".format(len(inventory) + 1))

    ################
    # CORE METHODS #
    ################

    def level_up(self):
        self.strength += 5
        self.agility += 1
        self.intel += 1
        self.hp += 10

    def pick_up(self, item, category):
        # item is the return value from each individual loot (name)
        self.inventory.get(category).append(item)
        print_slow("Picked up:".format(item))

    def drop(self, item, category):
        self.inventory.get(category).remove(item)
        print_slow("Dropped:", item)

    def status(self):
        print("{} the {}".format(self.name, self.hero_class))
        print("HP: {}/{}".format(self.health, self.hp))

    def death(self):
        os.system("clear")
        print("  =   =  ====  =  =   ===  =  ===  ===")
        print("  =====  =  =  =  =   = =  =  ===  = =")
        print("      =  =  =  =  =   = =  =  =    = =")
        print("      =  ====  ====   ===  =  ===  ===")
        print("")
        print(self.name + " the " + self.hero_class)
        print_slow("Your greed has lead to your downfall...", 0.05)
        print("\n" + "Wealth = " + str(self.wealth))
        print("\n" + "Coins = " + str(self.coins))

    def set_weapon(self):
        self.weapon = WEAPON_LIST.loc[
            WEAPON_LIST["Name"] == self.equipped.get("Weapons")
        ]
        self.crit_chance = self.weapon["Crit_chance"]
        print(self.crit_chance)

    def crit_check(self):
        if roll() < self.crit_chance:
            print("You unleash a critical strike")
            return self.crit_multi
        return 1

    def equip(self, item, category, old_item):
        self.equipped[category] = item
        print("Equipped:", self.equipped)
        self.inventory.get(category, []).remove(item)
        if old_item:
            self.inventory.get(category).append(old_item)
        print("Inventory:", self.inventory)

    #####################
    # INVENTORY METHODS #
    #####################

    # options, view category and view inventory need a rework
    # because they're doing some super dangerous stuff like cyclical
    # calls. i.e. view category calls options which calls view category
    # which calls view inventory which calls view category etc.
    # we want clean code, single flat call, with a clear result
    def _options(self, item, category, action):
        options_map = {1: "equip", 2: "drop", 3: "back"}
        while True:
            old_item = self.get_equipped(category)
            print_slow("Currently equipped: {} \n".format(old_item))
            print_slow("Selected item : {} \n".format(item))
            print_options(options_map)
            answer = options_map[input_int()]
            if answer == "equip":
                self.equip(item, category, old_item)
                self.view_category(action, category)
                break
            elif answer == "drop":
                while True:
                    print_slow("Are you sure you want to drop item? \n")
                    print_slow("1. Yes \n" + "2. No \n")
                    answer = input_int()
                    if answer == 1:
                        self.drop(item, category)
                        self._options(item, category, action)
                    elif answer == 2:
                        self._options(item, category, action)
                        break
                    else:
                        print_slow("Please choose a valid option")
                        continue

    def view_category(self, action, category):
        self.print_inventory(category)
        # Need to better understand what the point of this
        # function is, the current implementation is still messy
        # Also, this should just be a function in the hero class
        # Since you're making a view of a hero attribute
        n_invent = self.get_n_inventory(category) + 1
        while True:
            response = input_int()
            if response < n_invent:
                item = self.inventory[category][response - 1]
                clear_screen()
                self._options(item, category, action)
                break
            elif response == n_invent:
                clear_screen()
                self.view_inventory()
                break
            else:
                print_slow("Choose valid option")
                continue

    def view_inventory(self):
        while True:
            clear_screen()
            print("Inventory:")
            print_options(self._inventory_options)
            action = input_int()
            if action == 1:
                print_slow(
                    "You have {} Coins in your purse\n".format(
                        self.inventory["Coins"]
                    )
                )
                break
            elif action > 1 and action < 7:
                clear_screen()
                print_slow(
                    "You have chosen to see {} : {} \n".format(
                        action, self._inventory_options.get(action)
                    )
                )
                self.view_category(action, self._inventory_options.get(action))
            elif action == 7:
                clear_screen()
                break
            else:
                print_slow("Choose valid option")
                continue

    #################
    # CLASS METHODS #
    #################
    @classmethod
    def _test_hero(cls):
        return cls("test", "class", 10, 10, 10, 10, 0.9, 0.2, 3)

    @classmethod
    def hero_setup(cls):
        print_slow("What is your ancient name?\n")
        playername = input_str()

        # assigning the hero class based on user input
        print_slow("Choose from any of the below roles for today!\n")

        hero_options = {
            1: "night elf",
            2: "shadow assassin",
            3: "blood priest",
        }
        print_options(hero_options)
        char_class = False
        while not char_class:
            char_class = hero_options.get(input_int())
            if char_class == "night elf":
                char = night_elf
                # Create the hero object
                starting_weapon = {"weapons": "Elven Bow"}
            elif char_class == "shadow assassin":
                char = shadow_assasin
                starting_weapon = {"weapons": "Midnight Dagger"}
            elif char_class == "blood priest":
                char = blood_priest
                starting_weapon = {"weapons": "Warlock Wand"}
            else:
                print("Please choose from the available roles!\n")
                playerhero = 0

        hero = cls(playername, char_class, *char)
        hero.equipped.update(starting_weapon)
        print(
            "{} the {} has entered the game".format(
                hero.name, playerhero.capitalize()
            )
        )
        return hero
