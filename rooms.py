from utils import print_slow, input_int, print_options
from monster import Monster
from dungeon2 import battle_choices

# class Room


def room(hero, level, game_level):
    junction_map = {1: "battle room", 2: "trap room", 3: "aeon chamber"}

    if game_level == "room":
        room_choice = 0
        print_slow("Which room would you to enter?\n")

        while room_choice not in junction_map.keys():
            print_options(junction_map)
            choice = input_int()
            room_choice = junction_map.get(choice)
            if room_choice == "battle room":
                enemy = Monster.monster_spawn(level)
                print_slow(
                    "You encounter some dangerous looking"
                    " {}\n".format(enemy.name)
                )
                battle_choices(hero, enemy)
                junction_map.pop(choice)
                break
            elif room_choice == "trap room":
                junction_map.pop(choice)
                print("Trap room coming soon...")
                continue
                # call trap room function
            elif room_choice == "aeon chamber":
                junction_map.pop(choice)
                print("Aeon Chamber coming soon...")
                # call Aeon chamber function
                continue
            else:
                print("Please choose a valid input...")
    if game_level == "boss":
        print_slow("You've entered the lair of a dangerous boss!")
        print_slow("Boss content coming soon...")
        # create boss
        # fight boss
        # send output to level progression function)


# class Room(object):
# 	def __init__(self,room_type,LEVEL):
# 		self.name = room_type
# 		self.level = LEVEL

# 	def create(cls,room_type,LEVEL = 1,):
# 		if room_type == 'battleroom':
# 			enemy = (Monster.monster_spawn(LEVEL))
# 			return cls(enemy)
# 			print("\n" + "You encounter some dangerous looking " + enemy.name)
