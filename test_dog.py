from hero import Hero
from monster import Monster
from dungeon2 import wealth_drop, monster_drop, weapon_drop
from utils import roll
import random

LEVEL = 1
hero = Hero._test_hero()


def wealthdrops():
    hero = Hero._test_hero()
    monster = Monster.monster_spawn(1)
    test_drops = [wealth_drop(monster, hero) for i in range(1000)]
    real_drops = [t for t in test_drops if t != 0]
    print(
        "{} drops out of {} chances".format(len(real_drops), len(test_drops))
    )


def monsterdrop():
    hero = Hero._test_hero()
    monster = Monster.monster_spawn(1)
    drops = [monster_drop(monster, hero) for i in range(100)]
    print(hero.wealth)


def potion_drop(room):
    level = LEVEL
    if room == ("battleroom"):
        potion_types = ["small", "medium"]
        chance = (level - 1) * 10
        if roll() <= chance:
            potion = random.choice(potion_types)
            if potion == "small":
                hero.pots["small"] += 1
                return 1
            elif potion == "medium":
                hero.pots["medium"] += 1
                return 1
        else:
            return 0


def test_potion():
    test = [potion_drop("battleroom") for i in range(100)]
    pots = [t for t in test if t != 0]
    print("{} drops out of {} chances".format(len(pots), len(test)))


def test_weapon():
    hero = Hero._test_hero()
    monster = Monster.monster_spawn(1)
    test_drops = [weapon_drop(monster, hero) for i in range(100)]
    real_drops = [t for t in test_drops if t != 0]
    print(real_drops)
    print(
        "{} drops out of {} chances".format(len(real_drops), len(test_drops))
    )
