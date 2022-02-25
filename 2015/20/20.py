from math import sqrt, floor

def _calculate_presents(house):
    presents = 0
    for i in range(1, floor(sqrt(house))+1):
        if house % i == 0:
            presents += i*10 

        if house % i == 0 and i != sqrt(house):
            presents += (house // i)*10

    return presents


def _calculate_limited_presents(house):
    presents = 0
    for i in range(1, floor(sqrt(house))+1):
        if house % i == 0 and house // i <= 50:
            presents += i*11
        if house % i == 0 and i != sqrt(house) and i <= 50:
            presents += (house // i)*11

    return presents

def part_one(number):
    """
    Slowest implementation possible
    >>> part_one(120)
    6
    >>> part_one(130)
    8
    """
    presents = 0
    house = 0

    while presents < number:
        house += 1
        presents = _calculate_presents(house)
    return house


def part_two(number):
    """
    
    """
    presents = 0
    house = 0

    while presents < number:
        house += 1
        presents = _calculate_limited_presents(house)
    return house


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    test_input = 33100000

    #print(f"Part one: {part_one(test_input)}")
    print(f"Part two: {part_two(test_input)}")

