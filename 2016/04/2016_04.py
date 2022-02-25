import re
from collections import Counter, deque

def _parse(inp):
    room_r = re.compile(r"([a-z\-]+)\-(\d+)\[([a-z]{5})\]")
    inp = re.match(room_r, inp.strip())
    room, sector, checksum = inp.groups()

    return (room, int(sector), checksum)

def _checksum(room):
    """
    >>> _checksum("aaaaa-bbb-z-y-x")
    'abxyz'
    >>> _checksum("a-b-c-d-e-f-g-h")
    'abcde'
    >>> _checksum("not-a-real-room")
    'oarel'
    """
    counter = Counter(room)
    del counter["-"]
    checksum = []
    common = counter.most_common()

    for i in range(common[0][1], 0, -1):
        common_keys = [c[0] for c in common if c[1] == i]
        checksum += sorted(common_keys)

    return "".join(checksum[:5])

def part_one(rooms):
    return sum([sector for room, sector, checksum in rooms if _checksum(room) == checksum])

def _translate(room, sector):
    alph = "abcdefghijklmnopqrstuvwxyz"
    crypt = deque(alph)
    crypt.rotate(sector)
    translator = {c: a for c, a in zip(crypt, alph)}
    translator["-"] = " "

    return "".join(map(lambda letter: translator[letter], room))



def part_two(data):
    for room, sector, _ in data:
        translation = _translate(room, sector)
        if "pole" in translation or "north" in translation:
            print(translation)
            return sector
    

if __name__ == '__main__':
    from doctest import testmod
    testmod()
    with open("input_2016_04.txt", "r") as f:
        test_input = list(map(_parse, f.readlines()))
        print(f"Part one {part_one(test_input)}")
        print(f"Part two {part_two(test_input)}")