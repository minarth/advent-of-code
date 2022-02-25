from collections import deque

def _get_grid(cols=50, rows=6):
    return [[0]*cols for _ in range(rows)]

def _print(grid):
    formatted = []
    for row in grid:
        formatted.append("".join([str("#" if cell else ".") for cell in row]))

    print("\n".join(formatted))


def _rect(grid, cols, rows):
    for i in range(rows):
        for j in range(cols):
            grid[i][j] = 1
    return grid

def _rotate_col(grid, col, shift):
    c = deque([g[col] for g in grid])
    c.rotate(shift)

    for i in range(len(grid)):
        grid[i][col] = c[i]

    return grid


def _rotate_row(grid, row, shift):
    r = deque(grid[row])
    r.rotate(shift)
    grid[row] = list(r)

    return grid

def _parse(instruction):
    """
    >>> _parse("rect 1x1")
    ('rect', 1, 1)

    >>> _parse("rotate row y=0 by 5")
    ('row', 0, 5)

    >>> _parse("rotate column x=32 by 1")
    ('column', 32, 1)
    """
    instruction = instruction.strip().split()
    if instruction[0] == "rect":
        name = instruction[0]
        param1, param2 = instruction[1].split("x")
    else:
        name = instruction[1]
        param1 = instruction[2].split("=")[1]
        param2 = instruction[-1]

    return name, int(param1), int(param2)


def part_one(instructions):
    grid = _get_grid()
    for instruction, param1, param2 in instructions:
        if instruction == "rect":
            grid = _rect(grid, param1, param2)
        elif instruction == "column":
            grid = _rotate_col(grid, param1, param2)
        elif instruction == "row":
            grid = _rotate_row(grid, param1, param2)

    _print(grid)
    return sum([sum(row) for row in grid])

def _test_part_one():
    """
    >>> _test_part_one()
    6
    """
    instructions = [("rect", 3, 2), ("column", 1, 1), ("row", 0, 4), ("column", 1, 1)]
    return part_one(instructions)

if __name__ == '__main__':
    from doctest import testmod
    testmod()

    with open("input_2016_08.txt", "r") as f:
        test_input = [_parse(line) for line in f.readlines()]
        print(f"Part one {part_one(test_input)}")