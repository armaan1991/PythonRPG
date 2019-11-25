from utils import roll
import pandas as pd
import random


class Monster:
    def __init__(self, monster_data):
        self.name = monster_data["Name"]
        self.level = monster_data["Level"]
        self.max_hp = monster_data["HP"]
        self.damage = monster_data["Damage"]
        self.hit_chance = monster_data["Hit Chance"]
        self.crit_chance = monster_data["Crit Chance"]
        self.crit_multi = monster_data["Crit Multi"]
        self.defense = monster_data["Defense"]
        self.hp = self.max_hp
        self.lootchance_coins = monster_data["Coins"]
        self.lootchance_wealth = monster_data["Wealth"]
        self.lootchance_gear = monster_data["Gear"]

    @classmethod
    def monster_spawn(cls, level=1):
        monsterlist = pd.read_csv(
            "dog_monsters_v1.csv"
        )  # importing all the monsters of the game
        monster_options = monsterlist.loc[
            monsterlist["Level"] == level
        ]  # Makes a dataframe of monsters in current level from main dataframe
        monster_random = random.randint(
            0, (len(monster_options) - 1)
        )  # Generates a random number to pick the monster
        monster_data = monster_options.iloc[
            monster_random
        ]  # Generates a dataframe of the chosen monster

        return cls(monster_data)

    # combine all crit functions in parent class during refactorization
    def crit_check(self):
        if roll() < self.crit_chance:
            print("The {} attack you with a critical strike".format(self.name))
            return self.crit_multi
        return 1
