import os
from time import sleep
from utils import print_slow, input_int, print_options
from hero import Hero
from rooms import room
from inventory import view_inventory


def start():
    os.system("clear")
    print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
    print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
    print("_-_-_-_-_Welcome to DUNGEON OF GREED_-_-_-_-_")
    print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
    print("_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_")
    print("")
    print("")
    sleep(1)

    hero = Hero.hero_setup()
    return hero


def base_choices():
    choice_map = {1: "explore", 2: "inventory", 3: "quit"}
    choice = 0
    while True:
        print_options(choice_map)
        choice = choice_map.get(input_int())
        if choice in choice_map.values():
            break
        print("Choose a valid option...")

    return choice


def main_game_loop(hero):
    print(hero.name)
    game_levels = ("room", "boss", "room", "room", "boss", "end")
    for level in range(len(game_levels)):
        # cause everything is zero index
        LEVEL = level + 1
        game_level = game_levels[level]
        print("You are at level {}: {}".format(LEVEL, game_level))
        print_slow("What would you like to do?" + "\n")
        choice = base_choices()
        while choice != "explore":
            if choice == "inventory":
                view_inventory(hero)
                choice = base_choices()
            if choice == "quit":
                quit("Only cowards run from glory...")

        room(hero, LEVEL, game_level)
        hero.level_up()
        LEVEL += 1
        # proceed to junction

        # handle room should not proceed if inventory option chosen

        if hero.health <= 0:
            break
    print("Well played! Game over...")

    # check inventory etc.
    # if proceed ->
    # create room
    # room = Room(hero, level, level_type, hero_selected_room_type)

    # hero = room.run()

    # create a monster
    # user unput to fight, flee, or potion
    # return a result

    # move on to next level


# ask user, want to play a game? or quit?


class PathRoom(object):
    def __init__(self, level):
        self.level = level
        self.room_type = "path"
        self.difficult = "nightmare"


class TrapRoom(PathRoom):
    def __init__(self):
        self.__super__(self)
        self.traps = 5
        self.trap_dmg = 2

    def run():
        pass
        # get trap
        # hero fight trap
        # do real time cut scene dodge
        # return hero

