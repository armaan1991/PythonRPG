from hero import Hero


def test_night_elf():
    hero = Hero._hero_setup("night elf", "test_hero_1")
    hero.print_status()


def test_blood_priest():
    hero = Hero._hero_setup("blood priest", "test_hero_2")
    hero.print_status()


def test_shadow_assassin():
    hero = Hero._hero_setup("shadow assassin", "test_hero_3")
    hero.print_status()


def main():
    test_night_elf()
    test_blood_priest()
    test_shadow_assassin()


if __name__ == "__main__":
    main()
