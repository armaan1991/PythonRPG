import os
import random
import pandas as pd
from time import sleep
from utils import write_cool, roll
from hero import Hero
from monster import Monster

global enemy
global level


def main():
    # Start game
    os.system("clear")
    print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
    print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
    print("_-_-_-_-_Welcome to DUNGEON OF GREED_-_-_-_-_")
    print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
    print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
    print("")
    print("")
    sleep(1)

    wealth_list = pd.read_csv(
        "dog_wealth_v1.csv"
    )  # importing all wealth drops of the game
    coin_list = pd.read_csv(
        "dog_coins_v1.csv"
    )  # importing all coin drops of the game

    # This function let's the play choose which room to enter
    junction_history = [
        "1",
        "2",
        "3",
    ]  # handler to prevent room re-enter abuse. This should be reset after level clear.

    def junction():
        t3 = "Which room would you to enter?" + "\n"
        write_cool(t3, 0.03)

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
        write_cool(t4, 0.02)
        enemy = (
            Monster.monster_spawn()
        )  # stored the return value (class object) of the function in a new variale to be reused in fight function
        print("\n" + "You encounter some dangerous looking " + enemy.name)
        battle_choices(hero, enemy)

    def battle_choices(hero, enemy):
        print(
            "1. Attack"
            + "\n"
            + "2. Flee"
            + "\n"
            + "3. Potion"
            + "\n"
            + "Your Turn!"
            + "\n"
        )  # make functions for 2 and 3
        battle_action = input(
            str("->")
        )  # validate input for incorrect options
        if battle_action == "1":
            fight(hero, enemy)
        elif battle_action == "2":
            flee(hero, enemy)  # attemps to flee the battle room
        elif battle_action == "3":
            potion(hero, enemy)  # allows hero to consume potions
        else:
            print("Please s2elect a valid input...")
            battle_choices(hero, enemy)

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
                crit_enemy = enemy.crit_check(
                    enemy
                )  # should have been a common function in parent class
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
            )  # code a common function for clearing battle room that levels you up, drops loot, resets room handler, takes you to next level
        else:
            battle_choices(hero, enemy)

    def battle_room_success(hero, enemy):
        global level
        t5 = "You have cleared level " + str(level) + "!" + "\n"
        write_cool(t5, 0.02)
        print("Your greed bonus has increased")
        print(" ")
        input("Press any key to continue...")
        hero.status()
        hero.greed += 0.10
        print("\n" + "Greed bonus has increased by 10%")
        wealth_drop(enemy, 1)  # pending
        # potion_drop create a potion drop function which drops heals across rooms based on room type and level
        # level_handler() #Create a function that progresses the game across levels 1-5
        # inventory allow player to change inventory

    def monster_drop(enemy): #complete this
        global level
        coin_drop_chance = int(enemy.lootchance_coins) #takes the chance of the monster to drop coins
        if roll() <= coin_drop_chance:
            coin_drops_level = coin_list.loc[coin_list['Level'] == level] #gets all dropabble coins for the current level
            coin_roll = roll() - hero.greed #rolls to see which drops you can get, factors greed
            coin_drops = coin_drops_level.loc[coin_drops_level['Rarity'] >= coin_roll] #makes a df of all dropabble items
            coin_drops = coin_drops.sample() #takes a random drop from above dataframe
            hero.coins += int(coin_drops['Amount']) #adds coins to hero's inventory
            print('The monster drops ' + str(coin_drops.iloc[0,0]) + ' coins')
            print('Current coins: ' + str(hero.coins))

        wealth_drop_chance = int(enemy.lootchance_wealth) #takes the chance of the monster to drop coins    
        if roll() <= wealth_drop_chance:
            wealth_drops_level = wealth_list.loc[wealth_list['Level'] == level] #gets all dropabble coins for the current level
            wealth_roll = random.randint(1,101) - hero.greed #rolls to see which drops you can get, factors greed
            wealth_drops = wealth_drops_level.loc[wealth_drops_level['Rarity'] >= wealth_roll] #makes a df of all dropabble items
            if wealth_drops.empty:
                pass
            else:
                wealth_drops = wealth_drops.sample() #takes a random drop from above dataframe
                hero.wealth.append(wealth_drops.iloc[0,0])
                print('The monster drops a ' + str(wealth_drops.iloc[0,0]))
                print(hero.wealth)
            
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
        write_cool(t6, 0.02)
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
                hero.health -= enemy_damage
                hero.status()
                battle_choices(hero, enemy)
                if hero.health <= 0:
                    hero.death()
            else:
                print("You dodge an incoming attack" + "\n")
                battle_choices(hero, enemy)

    # Gameplay begins
    hero = Hero.hero_setup()
    junction()
    # wealth_drop()


if __name__ == "__main__":
    main()
