def _parse(instructions):
    unit_instrs = instructions.strip().split(", ")
    return [(i[0], int(i[1:])) for i in unit_instrs]


def part_one(instructions, debug=False):
    """
    >>> part_one("R2, L3")
    5
    >>> part_one("R2, R2, R2")
    2
    >>> part_one("R5, L5, R5, R3")
    12
    """
    # NORTH SOUTH position
    ns = 0
    # EAST WEST position
    ew = 0
    # N, E, S, W
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    direction = 0
    for change, steps in _parse(instructions):
        direction += 1 if change == "R" else -1
        direction %= 4
        mod_ns, mod_ew = directions[direction]
        ns += mod_ns * steps
        ew += mod_ew * steps
    return abs(ns) + abs(ew)


def part_two(instructions):
    """
    >>> part_two("R8, R4, R4, R8")
    4
    """
    # NORTH SOUTH position
    ns = 0
    # EAST WEST position
    ew = 0
    # N, E, S, W
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    direction = 0
    visited = [(0, 0)]
    for change, steps in _parse(instructions):
        direction += 1 if change == "R" else -1
        direction %= 4
        mod_ns, mod_ew = directions[direction]
        for i in range(steps):
            ns += mod_ns 
            ew += mod_ew
            if (ns, ew) in visited:
                return abs(ns) + abs(ew)
            visited.append((ns, ew))

if __name__ == "__main__":
    from doctest import testmod
    testmod()
    test_input = "L1, L5, R1, R3, L4, L5, R5, R1, L2, L2, L3, R4, L2, R3, R1, L2, R5, R3, L4, R4, L3, R3, R3, L2, R1, L3, R2, L1, R4, L2, R4, L4, R5, L3, R1, R1, L1, L3, L2, R1, R3, R2, L1, R4, L4, R2, L189, L4, R5, R3, L1, R47, R4, R1, R3, L3, L3, L2, R70, L1, R4, R185, R5, L4, L5, R4, L1, L4, R5, L3, R2, R3, L5, L3, R5, L1, R5, L4, R1, R2, L2, L5, L2, R4, L3, R5, R1, L5, L4, L3, R4, L3, L4, L1, L5, L5, R5, L5, L2, L1, L2, L4, L1, L2, R3, R1, R1, L2, L5, R2, L3, L5, L4, L2, L1, L2, R3, L1, L4, R3, R3, L2, R5, L1, L3, L3, L3, L5, R5, R1, R2, L3, L2, R4, R1, R1, R3, R4, R3, L3, R3, L5, R2, L2, R4, R5, L4, L3, L1, L5, L1, R1, R2, L1, R3, R4, R5, R2, R3, L2, L1, L5"
    print(f"Part one {part_one(test_input, True)}")
    print(f"Part two {part_two(test_input)}")