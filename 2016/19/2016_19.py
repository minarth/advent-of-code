from collections import deque
from math import floor

def part_one(elves_num):
    elves = deque(range(1,elves_num+1))
    while len(elves) > 1:
        del elves[1]
        #elves.remove(elves[1])
        elves.rotate(-1)

    return elves

def part_two(elves_num):
    """
    Written in late night, deletions with O(n) are not a great idea
    It works though
    """
    elves = deque(range(1,elves_num+1))
    while len(elves) > 1:
        del elves[floor(len(elves)/2)]
        elves.rotate(-1)

    return elves


if __name__ == '__main__':
    print(f"Test {part_one(5)}")
    #print(f"Part one {part_one(3005290)}")

    print(f"Test two {part_two(5)}")
    #print(f"Part two {part_two(3005290)}")