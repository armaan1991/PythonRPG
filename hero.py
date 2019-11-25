import os
from utils import write_cool, input_str, roll

# $str,defense,agi,intel,hitchance,critchance,critmulti
night_elf = [8, 10, 5, 10, 80, 10, 1.5]
shadow_assasin = [2, 10, 15, 10, 90, 10, 1.5]
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
    ):  # , hit_chance, crit_chance, crit_multi, defense, intel, agility, looting, greed)
        self.name = name
        self.strength = strength
        self.hp = 100 + self.strength
        self.health = self.hp
        self.damage = strength * 0.5 + 5
        self.agility = agility
        self.hit_chance = hit_chance
        self.crit_chance = crit_chance + self.agility
        self.defense = defense
        self.intel = intel
        self.agility = agility
        self.crit_multi = crit_multi
        self.greed = 1
        self.weapon = []
        self.weapon_wielded = []
        self.gear = []
        self.gear_wielded = []
        self.wealth = []
        self.pots = {"small": 1, "medium": 0, "large": 0}
        self.coins = 0
        self.hero_class = hero_class

    def levelup(self):
        self.strength += 1
        self.agility += 1
        self.intel += 1
        self.hp += 10

    def status(self):
        print("{} the {}".format(self.name, self.hero_class))
        print("HP: {}/{}".format(self.health, self.hp))
        print("Current Level {}".format(level))

    def death(self):
        os.system("clear")
        print("  =   =  ====  =  =   ===  =  ===  ===")
        print("  =====  =  =  =  =   = =  =  ===  = =")
        print("      =  =  =  =  =   = =  =  =    = =")
        print("      =  ====  ====   ===  =  ===  ===")
        print("")
        print(self.name + " the " + self.hero_class)
        print("Died at level {}".format(level))
        print("Score = " + str(self.wealth))

    @classmethod
    def hero_setup(cls):
        t1 = "What is your ancient name?" + "\n"
        write_cool(t1)

        playername = input_str()

        # assigning the hero class based on user input
        t2 = "Choose from any of the below roles for today!" + "\n"
        write_cool(t2)

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
                print(hero.name + " the " + "Night elf has entered the game")

            elif playerhero == "2":
                char_class = "Shadow assasin"
                hero = cls(playername, char_class, *shadow_assasin)
                print(
                    hero.name + " the " + "Shadow assasin has entered the game"
                )

            elif playerhero == "3":
                char_class = "Blood priest"
                hero = cls(playername, char_class, *blood_priest)
                print(
                    hero.name + " the " + "blood priest has entered the game"
                )

            else:
                print("Please choose from the available roles!" + "\n")
                playerhero = 0
        return hero

    def crit_check(self):
        if roll() < self.crit_chance:
            print("You unleash a critical strike")
            return self.crit_multi
        return 1
