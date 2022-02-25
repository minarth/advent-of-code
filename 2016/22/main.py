import re
import curses
from curses import wrapper
from time import sleep

def _parse(lines):
    line_r = r"\/dev\/grid\/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%"
    matches = re.findall(line_r, lines)
    # x, y, size, used, avail, use%
    return [tuple(map(int, m)) for m in matches]


def part_one(nodes):
    viable_pairs = 0
    unmovable = set()
    for i, n1 in enumerate(nodes):
        _, _, _, used, _, _ = n1
        moved = 0
        for j, n2 in enumerate(nodes):
            if i == j: continue
            _, _, _, _, avail, _ = n2
            if used <= avail and used > 0:
                viable_pairs += 1
                moved += 1
            elif used == 0:
                moved += 1
        if moved == 0: 
            unmovable.add((n1[0], n1[1]))

    return viable_pairs, unmovable


def part_two(nodes, source, target, unmovable):

    """
    This was look and see, so I just made the plan without looking for shortest path
    TODO: refactore the repeating code

    """

    stdscr = curses.initscr()
    curses.noecho()

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1,0,0)
    curses.init_pair(2,1,0)
    curses.init_pair(3,3,0)
    curses.init_pair(4,4,0)
    stdscr.clear

    rows = max([x[0] for x in nodes])
    cols = max([x[1] for x in nodes])
    grid = [[None for _ in range(cols+1)] for _ in range(rows+1)]

    for x, y, _, used, avail, _ in nodes:
        grid[x][y] = (used, avail)
    
    x_s, y_s = source
    x_t, y_t = target
    gold_size, _ = grid[x_s][y_s]
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell[1] >= gold_size:
                x_e, y_e = i, j

    # number of steps needed to overcome wall of imovable data
    steps = 0
    _print(rows, cols, (x_s, y_s), (x_e, y_e), (x_t, y_t), unmovable, stdscr, steps)

    while x_e != 1:
        x_e -= 1
        _print(rows, cols, (x_s, y_s), (x_e, y_e), (x_t, y_t), unmovable, stdscr, steps)
        steps += 1
    
    while y_e != 0:
        y_e -= 1
        _print(rows, cols, (x_s, y_s), (x_e, y_e), (x_t, y_t), unmovable, stdscr, steps)
        steps += 1
    
    while x_e != 34:
        x_e += 1
        _print(rows, cols, (x_s, y_s), (x_e, y_e), (x_t, y_t), unmovable, stdscr, steps)
        steps += 1

    x_s -= 1
    x_e += 1
    steps += 1
    _print(rows, cols, (x_s, y_s), (x_e, y_e), (x_t, y_t), unmovable, stdscr, steps)


    while x_s != 0:
        y_e += 1
        steps += 1
        _print(rows, cols, (x_s, y_s), (x_e, y_e), (x_t, y_t), unmovable, stdscr, steps)

        x_e -= 1
        steps += 1
        _print(rows, cols, (x_s, y_s), (x_e, y_e), (x_t, y_t), unmovable, stdscr, steps)

        x_e -= 1
        steps += 1
        _print(rows, cols, (x_s, y_s), (x_e, y_e), (x_t, y_t), unmovable, stdscr, steps)

        y_e -= 1
        steps += 1
        _print(rows, cols, (x_s, y_s), (x_e, y_e), (x_t, y_t), unmovable, stdscr, steps)

        x_s -= 1
        x_e += 1
        steps += 1
        _print(rows, cols, (x_s, y_s), (x_e, y_e), (x_t, y_t), unmovable, stdscr, steps)
    
    sleep(2)
    curses.echo()
    curses.endwin()
    return steps

def _print(rows, cols, gold, empty, target, unmovable, screen, steps=100):
    grid = [[None for _ in range(cols+1)] for _ in range(rows+1)]
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            color = 4
            if (i, j) == gold: 
                cell = "G"
                color = 2
            elif (i, j) == target:
                cell = "O"
                color = 3
            elif (i, j) == empty:
                cell = "@"
                color = 0
            elif (i, j) in unmovable:
                cell = "#"
            else:
                cell = "."
            screen.addstr(i, j, cell, curses.color_pair(color) | curses.A_BOLD)    
    screen.addstr(rows+1, 0, f"Steps: {steps}", curses.color_pair(3) | curses.A_BOLD)    
    screen.refresh()
    screen.timeout(200)
    sleep(0.2)

if __name__ == "__main__":
    from doctest import testmod
    testmod()

    with open("2016/22/input.txt", "r") as fd:
        test_input = _parse(fd.read())
        pairs, unmovable = part_one(test_input)
        print(f"Part One {pairs}")
        steps = part_two(test_input, (35, 0), (0, 0), unmovable)
        print(f"Part Two {steps}")