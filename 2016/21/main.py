from collections import deque
import re
from itertools import permutations

def _parse(line):
    swap_p = r"(swap position) (\d+) with position (\d+)"
    swap_l = r"(swap letter) ([a-z]) with letter ([a-z])"
    reverse = r"(reverse) positions (\d+) through (\d+)"
    rotate = r"(rotate) (left|right) (\d+) step[s]*"
    rotate_p = r"(rotate) based on position of letter ([a-z])"
    move = r"(move) position (\d+) to position (\d+)"
    cmds = (swap_p, swap_l, reverse, rotate, rotate_p, move)
    for cmd in cmds:
        if re.findall(cmd, line):
            return re.findall(cmd, line)[0]

    raise Exception(f"Unable to parse {line}")

def _scramble(pwd, cmd):
    """
    >>> _scramble("abcde", ("swap position", 4, 0))
    'ebcda'

    >>> _scramble("ebcda", ("swap letter", "d", "b"))
    'edcba'

    >>> _scramble("edcba", ("reverse", 0, 4))
    'abcde'

    >>> _scramble("abcde", ("rotate", "left", 1))
    'bcdea'

    >>> _scramble("bcdea", ("move", 1, 4))
    'bdeac'

    >>> _scramble("bdeac", ("move", 3, 0))
    'abdec'

    >>> _scramble("abdec", ("rotate", "b"))
    'ecabd'

    >>> _scramble("ecabd", ("rotate", "d"))
    'decab'
    """

    if cmd[0].startswith("swap"):
        if cmd[0] == "swap position":
            _, p1, p2 = cmd
        else:
            _, l1, l2 = cmd
            p1, p2 = pwd.index(l1), pwd.index(l2)
        p1, p2 = sorted((int(p1), int(p2)))
        return pwd[:p1] + pwd[p2] + pwd[p1+1:p2] + pwd[p1] + pwd[p2+1:]
        
    elif cmd[0] == "reverse":
        _, p1, p2 = cmd
        p1, p2 = int(p1), int(p2)
        return pwd[:p1] + pwd[p1:p2+1][::-1] + pwd[p2+1:]
    elif cmd[0] == "rotate":
        if len(cmd) == 3:
            _, direction, steps = cmd
            steps = int(steps)
        else:
            _, letter = cmd
            direction = "right"
            steps = pwd.index(letter)
            steps = 1 + steps + (1 if steps >= 4 else 0)

        direction = 1 if direction == "right" else -1
        pwd = deque(pwd)
        pwd.rotate(direction * steps)
        return "".join(pwd)
            
    elif cmd[0] == "move":
        _, p1, p2 = cmd
        p1, p2 = int(p1), int(p2)
        letter = pwd[p1]
        pwd = pwd[:p1] + pwd[p1+1:]
        return pwd[:p2] + letter + pwd[p2:]
    else:
        raise Exception(f"Unknown cmd: {cmd}")

def part_one(pwd, instructions):
    for i in instructions:
        pwd = _scramble(pwd, i)
    
    return pwd

def part_two(pwd, instructions):
    for perm in permutations(pwd):
        if part_one("".join(perm), instructions) == pwd:
            return "".join(perm)
    

if __name__ == "__main__":
    from doctest import testmod
    testmod()
    with open("2016/21/input.txt", "r") as f:
        test_input = list(map(_parse, f.readlines()))
        print(f"Part one {part_one('abcdefgh', test_input)}")
        print(f"Part two {part_two('fbgdceah', test_input)}")