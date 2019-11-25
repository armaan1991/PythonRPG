import sys
import random
from time import sleep


def write_cool(text, sleep_time=0.05):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        sleep(sleep_time)


def input_str():
    return input("->")


def roll(a=1, b=101):
    return random.randint(a, b)
