import os
from utils import print_slow, input_str, roll
import pandas as pd

# $str,defense,agi,intel,hitchance,critchance,critmulti
WEAPON_LIST = pd.read_csv("dog_weapons_v1.csv")

night_elf = [1000, 10, 5, 10, 80, 10, 1.5]
shadow_assasin = [2, 10, 15, 10, 90, 30, 1.5]
blood_priest = [6, 6, 3, 10, 85, 10, 1.5]
level = 1


class Hero:
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

    #################
    # CLASS METHODS #
    #################

    @classmethod
    def _test_hero(cls):
        return cls("test", "class", 10, 10, 10, 10, 0.9, 0.2, 3)

    @classmethod
    def hero_setup(cls):
        t1 = "What is your ancient name?" + "\n"
        print_slow(t1)

        playername = input_str()

        # assigning the hero class based on user input
        t2 = "Choose from any of the below roles for today!" + "\n"
        print_slow(t2)

        print("Press 1 to play as NIGHT ELF")
        print("Press 2 to play as SHADOW ASSASSIN")
        print("Press 3 to play as BLOOD PRIEST")
        print("\n")

        playerhero = 0
        while playerhero == 0:
            playerhero = input_str()
            if playerhero == "1":
                char_class = "Night elf"
                # Create the hero object
                hero = cls(playername, char_class, *night_elf)
                starting_weapon = {"Weapons": "Elven Bow"}
                hero.equipped.update(starting_weapon)
                print(hero.name + " the " + "Night elf has entered the game")

            elif playerhero == "2":
                char_class = "Shadow assasin"
                hero = cls(playername, char_class, *shadow_assasin)
                starting_weapon = {"Weapons": "Midnight Dagger"}
                hero.equipped.update(starting_weapon)
                print(
                    hero.name + " the " + "Shadow assasin has entered the game"
                )

            elif playerhero == "3":
                char_class = "Blood priest"
                hero = cls(playername, char_class, *blood_priest)
                starting_weapon = {"Weapons": "Warlock Wand"}
                hero.equipped.update(starting_weapon)
                print(
                    hero.name + " the " + "blood priest has entered the game"
                )

            else:
                print("Please choose from the available roles!" + "\n")
                playerhero = 0
        return hero
