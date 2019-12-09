import os
import random
import pandas as pd
from time import sleep
from utils import print_slow, roll, input_int, print_options
from hero import Hero
from monster import Monster
global lEVEL

WEALTH_LIST = pd.read_csv("dog_wealth_v1.csv")
COIN_LIST = pd.read_csv("dog_coins_v1.csv")
WEAPON_LIST = pd.read_csv("dog_weapons_v1.csv")
LEVEL = 1

def wealth_drop(enemy, hero):
    level = LEVEL
    if roll() <= int(enemy.lootchance_wealth):
        wealth_level = WEALTH_LIST.loc[WEALTH_LIST['Level'] == level] #gets all dropabble wealth for the current level
        wealth_roll = roll() - hero.greed #rolls to see which drops you can get, factors greed
        wealth_drops = wealth_level.loc[wealth_level['Rarity'] >= wealth_roll] #makes a df of all dropabble wealth
        if wealth_drops.empty:
            return 0
        wealth_drop = wealth_drops.sample()
        print(wealth_drop.iloc[0]["Name"])
        return (wealth_drop.iloc[0]["Name"])
    return 0


def monster_drop(enemy, hero): #everything that happens on monster death
    coins_gained = coin_drop(enemy, hero)
    if coins_gained:
        print('The monster drops ' + str(coins_gained) + ' coins')
        hero.coins += coins_gained
    wealth_gained = wealth_drop(enemy,hero)
    if wealth_gained: 
        print('The monster drops some rare wealth! ' '\n' + 'You find a {}'.format(wealth_gained))
        hero.wealth.append(wealth_gained)
    # drops potions based on the room type and level
    potion_drop(hero, 'battleroom')
    weapon_gained = weapon_drop(enemy,hero)
    if weapon_gained:
        print('The monster drops a weapon!' + '\n' + 'You find a {}'.format(weapon_gained))


def coin_drop(enemy, hero): 
    level = LEVEL
    if roll() <= int(enemy.lootchance_coins):
        coin_drops_level = COIN_LIST.loc[COIN_LIST['Level'] == level] #gets all dropabble coins for the current level
        coin_roll = roll() - hero.greed #rolls to see which drops you can get, factors greed
        coin_drops = coin_drops_level.loc[coin_drops_level['Rarity'] >= coin_roll] #makes a df of all dropabble items
        if coin_drops.empty:
            return 0
        coin_drops = coin_drops.sample() #takes a random drop from above dataframe
        return int(coin_drops['Amount']) #adds coins to hero's inventory
    return 0

def weapon_drop(enemy, hero):
    level = LEVEL
    if roll() <= int(enemy.lootchance_gear):
        weapon_drops_level = WEAPON_LIST.loc[WEAPON_LIST['Level'] == level]
        weapon_roll = roll() - hero.greed #rolls to see which drops you can get, factors greed
        weapon_drops = weapon_drops_level.loc[weapon_drops_level['Rarity'] >= weapon_roll] #makes a df of all dropabble items
        if weapon_drops.empty:
            return 0
        weapon_drops = weapon_drops.sample() #takes a random drop from above dataframe
        print(weapon_drops.iloc[0]["Name"], weapon_drops.iloc[0]["Category"])
        hero.pick_up(weapon_drops.iloc[0]["Name"], weapon_drops.iloc[0]["Category"])
        return (weapon_drops.iloc[0]["Name"])

    return 0

def potion_drop(hero, room):
    level = LEVEL
    if room == ("battleroom"):
        potion_types = ['small', 'medium']
        chance = (level - 1) * 10
        if roll() <= chance:
            potion = random.choice(potion_types)
            if potion == 'small':
                hero.pots['small'] +=1
                print('You pick up a small health potion')
                return 1
            elif potion == 'medium':
                hero.pots['medium'] += 1
                print('You pick up a medium health potion')
                return 1
        else:
            return 0
    if room == ("traproom"):
        potion_types = ['medium', 'large']
        chance = (level - 1) * 10
        if roll() <= chance:
            potion = random.choice(potion_types)
            if potion == 'medium':
                hero.pots['medium'] +=1
                print('You pick up a medium health potion')
                return 1
            elif potion == 'large':
                hero.pots['large'] += 1
                print('You pick up a large health potion')
                return 1
        else:
            return 0



# This function let's the play choose which room to enter
junction_history = ["1","2","3"]  # handler to prevent room re-enter abuse. This should be reset after level clear.

def junction():
    t3 = "Which room would you to enter?" + "\n"
    print_slow(t3, 0.03)

    while len(junction_history) > 0:
        if "1" in junction_history:
            print("Press 1 to enter the Battle Room")
        if "2" in junction_history:
            print("Press 2 to enter the Trap Room")
        if "3" in junction_history:
            print("Press 3 to enter the Aeon Chamber")
        room_choice = input("->")
        if room_choice == "1":
            junction_history.pop(0)
            battleroom()
            break
        elif room_choice == "2":
            junction_history.pop(1)
            break
            # call trap room function
        elif room_choice == "3":
            junction_history.pop(2)
            break
            # call Aeon chamber function
        else:
            print("You walk into a wall and hurt yourself..." + "\n")
            hero.health -= 1
            # handle death possibility

def battleroom():
    t4 = "You enter a dim cave and hear something sinister stir in the shadows..."
    print_slow(t4, 0.02)
    enemy = (Monster.monster_spawn(level))  #stored the return value (class object) of the function in a new variale to be reused in fight function
    print("\n" + "You encounter some dangerous looking " + enemy.name)
    battle_choices(hero, enemy)


def battle_choices(hero, enemy):
    battle_map = {1: "attack", 2: "flee", 3: "potion"}
    print_options(battle_map)
    battle_action = battle_map.get(input_int())
    if battle_action == "attack":
        fight(hero, enemy)  # launches battle
    elif battle_action == "flee":
        flee(hero, enemy)  # attemps to flee the battle room
    elif battle_action == "potion":
        potion(hero, enemy)  # allows hero to consume potions
    else:
        print("Please select a valid input...")
        battle_choices(hero, enemy)

    return hero


def fight(hero, enemy):
    initiative = roll() + hero.agility
    hero.status()
    print("\n" + "\n" + "--------battle-------")
    print(
        enemy.name
        + " health: "
        + str(enemy.health)
        + "/"
        + str(enemy.hp)
        + "\n"
    )
    if initiative > 50:
        hero_hit = roll()
        if hero_hit < (
            hero.hit_chance - enemy.defense
        ):  # factors if the hit is successful based on hit chance and monster defense
            crit_proc = hero.crit_check()
            attack_damage = int(
                random.randint(
                    int(0.8 * hero.damage), int((hero.damage) * crit_proc)
                )
            )
            print("You hit for {} damage".format(attack_damage))
            enemy.health -= attack_damage
        else:
            print("You swing wildly and miss...")
        enemy_hit = roll()
        if enemy_hit < (
            enemy.hit_chance - hero.defense
        ):  # factors if the hit is successful based on hit chance and hero defense
        # should have been a common function in parent class
            crit_enemy = enemy.crit_check()
            enemy_damage = int(
                random.randint(
                    int(0.8 * enemy.damage),
                    int((enemy.damage) * crit_enemy),
                )
            )
            print("You take {} damage".format(enemy_damage) + "\n")
            hero.health -= enemy_damage
        else:
            print("You successfully dodge the attack" + "\n")
    else:
        enemy_hit = roll()
        if enemy_hit < (enemy.hit_chance - hero.defense): 
            crit_enemy = enemy.crit_check()
            enemy_damage = int(
                random.randint(
                    int(0.8 * enemy.damage),
                    int((enemy.damage) * crit_enemy),
                )
            )
            print("You take {} damage".format(enemy_damage) + "\n")
            hero.health -= enemy_damage
        else:
            print("You successfully dodge the attack" + "\n")
        hero_hit = roll()
        if hero_hit < (
            hero.hit_chance - enemy.defense
        ):  # factors if the hit is successful based on hit chance and monster defense
            crit_proc = hero.crit_check()
            attack_damage = int(
                random.randint(
                    int(0.8 * hero.damage), int((hero.damage) * crit_proc)
                )
            )
            print("You hit for {} damage".format(attack_damage) + "\n")
            enemy.health -= attack_damage
        else:
            print("You swing wildly and miss..." + "\n")
    if hero.health <= 0:
        hero.death()  # handles death
    elif enemy.health <= 0:
        battle_room_success(
            hero, enemy
        ) 
    else:
        battle_choices(hero, enemy)

def battle_room_success(hero, enemy):
    level = LEVEL
    t5 = "You have cleared the level" + "\n"
    print_slow(t5, 0.02)
    print(" ")
    input("Press any key to continue...")
    hero.greed += 10
    print("\n" + "Greed bonus has increased! You have higher chances of finding wealth...")
    monster_drop(enemy,hero)  # done for coins and wealth
    hero.status()

    # level_handler() #Create a function that progresses the game across levels 1-5
    # inventory allow player to change inventory

   

def potion(hero, enemy):
    while (
        hero.pots["small"] > 0
        or hero.pots["medium"] > 0
        or hero.pots["large"] > 0
    ):
        print("Your Potions:")
        print("1. Small - " + str(hero.pots["small"]))
        print("2. Medium - " + str(hero.pots["medium"]))
        print("3. Large - " + str(hero.pots["large"]))
        consume_pot = input(str("-->" + "\n"))

        if consume_pot == "1":
            if hero.pots["small"] > 0:
                hero.health += 5
                print("You consume a potion and heal 5 HP")
                hero.pots["small"] = hero.pots["small"] - 1
                if hero.health > hero.hp:
                    hero.health = hero.hp
                battle_choices(hero, enemy)
            else:
                print("You do not have any small potions!")
                battle_choices(hero, enemy)
            break

        elif consume_pot == "2":
            if hero.pots["medium"] > 0:
                hero.health += 15
                print("You consume a potion and heal 15 HP")
                hero.pots["medium"] = hero.pots["medium"] - 1
                if hero.health > hero.hp:
                    hero.health = hero.hp
                battle_choices(hero, enemy)
            else:
                print("You do not have any medium potions!")
                battle_choices(hero, enemy)

        elif consume_pot == "3":
            if hero.pots["large"] > 0:
                hero.health += 30
                print("You consume a potion and heal 30 HP")
                hero.pots["large"] = hero.pots["large"] - 1
                if hero.health > hero.hp:
                    hero.health = hero.hp
                battle_choices(hero, enemy)
            else:
                print("You do not have any large potions!")
                battle_choices(hero, enemy)
            break

        else:
            print("Please select a valid input...")
            battle_choices(hero, enemy)

    else:
        print("You do not have any potions...")
        battle_choices(hero, enemy)

def flee(hero, enemy):
    t6 = "Trying to escape the room..."
    print_slow(t6, 0.02)
    flee_roll = 50 + hero.agility
    if roll() < flee_roll:
        print("You successfully escape from the " + enemy.name)
        junction()
    else:
        print("You can't find a way out!")
        enemy_hit = roll()
        if enemy_hit < (
            enemy.hit_chance - hero.defense
        ):  # factors if the hit is successful based on hit chance and hero defense
            crit_enemy = enemy.crit_check(
                enemy
            )  # should have been a common function in parent class
            enemy_damage = int(
                random.randint(
                    int(0.8 * enemy.damage),
                    int((enemy.damage) * crit_enemy),
                )
            )
            print(
                "The "
                + enemy.name
                + " attack you for "
                + str(enemy_damage)
                + " damage"
            )
            hero.hp -= enemy_damage
            hero.status()
            battle_choices(hero, enemy)
            if hero.hp <= 0:
                hero.death()
        else:
            print("You dodge an incoming attack" + "\n")
            battle_choices(hero, enemy)


