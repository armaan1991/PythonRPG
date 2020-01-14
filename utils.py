from os import system
import sys
import random
from time import sleep


def print_slow(text, sleep_time=0.03):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        sleep(sleep_time)


def print_options(text_dict):
    options = []
    for num, option in text_dict.items():
        # Ensure first letter is uppercase in options
        options.append("{}. {}".format(num, option.capitalize()))

    print_slow("\n".join(options) + "\n")


def input_str():
    return str(input("-->"))


def input_int():
    return int(input("-->"))


def roll(a=1, b=100):
    return random.randint(a, b)


def clear_screen():
    system("clear")
