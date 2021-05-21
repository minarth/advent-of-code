with open("06/input.txt", "r") as f:
    test_input = [s.strip() for s in f.readlines()]

INSTRUCTIONS = ["turn off", "turn on", "toggle"]
COMMANDS_ONE = [0, 1, -1]
COMMANDS_TWO = [-1, 1, 2]

def _parse_input(command):
    """
    >>> _parse_input("turn off 660,55 through 986,197")
    ('turn off', [660, 55], [986, 197])
    >>> _parse_input("turn off 341,304 through 638,850")
    ('turn off', [341, 304], [638, 850])
    >>> _parse_input("toggle 322,558 through 977,958")
    ('toggle', [322, 558], [977, 958])
    >>> _parse_input("turn on 240,129 through 703,297")
    ('turn on', [240, 129], [703, 297])
    >>> _parse_input("toggle 478,7 through 573,148")
    ('toggle', [478, 7], [573, 148])
    """

    cmd, start, end = None, None, None
    for instr in INSTRUCTIONS:
        if command.startswith(instr):
            cmd = instr
            rest = command.split(instr)[1].strip()
            start, end = rest.split(" through ")
    
    start = [int(x) for x in start.split(",")]
    end = [int(x) for x in end.split(",")]
    return cmd, start, end

def _create_grid(n):
    grid = []
    for i in range(n):
        grid.append([0]*n)

    return grid

def _set_grid(grid, value, start, end):
    """
    >>> _set_grid([[0,0,0], [0,0,0], [0,0,0]], 1, [0,0], [1,1])
    [[1, 1, 0], [1, 1, 0], [0, 0, 0]]

    >>> _set_grid([[0,0,0], [0,0,0], [0,0,0]], 1, [0,0], [2,0])
    [[1, 0, 0], [1, 0, 0], [1, 0, 0]]

    >>> _set_grid([[1,1,1], [1,1,1], [1,1,1]], 0, [1,1], [2,2])
    [[1, 1, 1], [1, 0, 0], [1, 0, 0]]

    >>> _set_grid([[1, 1, 1], [1, 0, 0], [1, 0, 0]], -1, [0,0], [2,2])
    [[0, 0, 0], [0, 1, 1], [0, 1, 1]]
    """

    for i in range(start[0], end[0]+1):
        for j in range(start[1], end[1]+1):
            grid[i][j] = value if value != -1 else (grid[i][j]+1)%2
    return grid

def _set_grid_two(grid, value, start, end):
    """
    >>> _set_grid_two([[0,0,0], [0,0,0], [0,0,0]], 1, [0,0], [1,1])
    [[1, 1, 0], [1, 1, 0], [0, 0, 0]]

    >>> _set_grid_two([[0,0,0], [0,0,0], [0,0,0]], 1, [0,0], [2,0])
    [[1, 0, 0], [1, 0, 0], [1, 0, 0]]

    >>> _set_grid_two([[1,1,1], [1,1,1], [1,1,1]], 2, [1,1], [2,2])
    [[1, 1, 1], [1, 3, 3], [1, 3, 3]]

    >>> _set_grid_two([[1, 1, 1], [1, 0, 0], [1, 0, 0]], -1, [0,0], [2,2])
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    """

    for i in range(start[0], end[0]+1):
        for j in range(start[1], end[1]+1):
            grid[i][j] = max(0, grid[i][j] + value)
    return grid

def p(instructs, set_grid, commands):
    grid = _create_grid(1000)
    for instr in instructs:
        cmd, start, end = _parse_input(instr)
        grid = set_grid(grid, commands[INSTRUCTIONS.index(cmd)], start, end)

    return sum([sum(g) for g in grid])

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print("01")
    print(p(test_input, _set_grid, COMMANDS_ONE))
    print("02")
    print(p(test_input, _set_grid_two, COMMANDS_TWO))
