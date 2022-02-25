import re

def _parse(discs):
    """
    >>> _parse("Disc #1 has 5 positions; at time=0, it is at position 4. Disc #2 has 2 positions; at time=0, it is at position 1.")
    [(1, 5, 4), (2, 2, 1)]
    """
    r = r"#(\d) has (\d+) .*? position (\d+)"
    parsed = []
    for d in re.findall(r, discs):
        parsed.append(tuple(map(int, d)))
    return parsed

def _arrangement_in_time(discs, time):
    arr = [(d[2]+time+d[0]) % d[1] for d in discs]
    return sum(arr)

def part_one(discs):
    """
    The most naive solution. 

    >>> part_one([(1, 5, 4), (2, 2, 1)])
    5

    """
    time = 0
    arrangement = _arrangement_in_time(discs, time)
    while arrangement != 0:
        time += 1
        arrangement = _arrangement_in_time(discs, time)
    
    return time

if __name__ == "__main__":
    from doctest import testmod
    testmod()
    with open("2016/15/input.txt", "r") as f:
        input_discs = _parse(f.read())
        print(f"Part one {part_one(input_discs)}")
        appeared_disc = [(7, 11, 0)]
        print(f"Part two {part_one(input_discs + appeared_disc)}")
