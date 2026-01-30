import utilities.dice as dice


def main():
    print(dice.roll("3d6"))
    print(dice.roll("2d10"))
    print(dice.roll("1d20"))
    print(dice.roll("5d4"))
    print(dice.roll("invalid"))  # Should return None

if __name__ == '__main__':
    main()