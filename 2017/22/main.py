from collections import deque
from copy import deepcopy

UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
orient = deque([UP, RIGHT, DOWN, LEFT])
 
def _access_coordinates(grid, x, y):
    # if accessing out of grid position -> extend
    if x < 0:
        for _ in range(abs(x)):
            grid = [["." for _ in range(len(grid[0]))]] + grid
            x = 0
    elif x >= len(grid):
        while x >= len(grid):
            grid += [["." for _ in range(len(grid[0]))]]

    if y < 0:
        for _ in range(abs(y)):
            for i in range(len(grid)):
                grid[i] = ["."] + grid[i]
        y = 0

    elif y >= len(grid[0]):
        while y >= len(grid[0]):
            for i in range(len(grid)):
                grid[i] += ["."]
    
    return grid, x, y

def _print(grid, x, y):
    for i, row in enumerate(grid):
        print_row = ""
        for j, cell in enumerate(row):
            if (i, j) == (x, y):
                print_row += f"[{cell}]"
            else:
                print_row += f" {cell} "
        print(print_row)


def _burst(grid, x, y, orientation):
    grid, x, y = _access_coordinates(grid, x, y)
    if grid[x][y] == "#":
        orientation.rotate(-1)
        infected = False
        grid[x][y] = "."
    else:
        orientation.rotate(1)
        infected = True
        grid[x][y] = "#"

    new_x = x + orientation[0][0]
    new_y = y + orientation[0][1]

    return grid, new_x, new_y, orientation, infected

def _burst2(grid, x, y, orientation):
    grid, x, y = _access_coordinates(grid, x, y)
    infected = False
    if grid[x][y] == "#":
        orientation.rotate(-1)
        grid[x][y] = "F"

    elif grid[x][y] == ".":
        orientation.rotate(1)
        grid[x][y] = "W"

    elif grid[x][y] == "W":
        infected = True
        grid[x][y] = "#"

    elif grid[x][y] == "F":
        orientation.rotate(2)
        grid[x][y] = "."

    new_x = x + orientation[0][0]
    new_y = y + orientation[0][1]

    return grid, new_x, new_y, orientation, infected

def part(grid, x, y, orientation, burst, bursts=10000):
    infected = 0
    for _ in range(bursts):
        grid, x, y, orientation, inf = burst(grid, x, y, orientation)
        # _print(grid, x, y)
        # print(orientation[0])
        # print()
        infected += 1 if inf else 0
    return grid, x, y, orientation, infected

if __name__ == "__main__":
    test_grid = [[".", ".", "#"], ["#", ".", "."], [".", ".","."]]
    *g, i = part(deepcopy(test_grid), 1, 1, deque([UP, RIGHT, DOWN, LEFT]), _burst, 10000)
    print(f"Test run {i}")

    *g, i = part(deepcopy(test_grid), 1, 1, deque([UP, RIGHT, DOWN, LEFT]), _burst2, 10000000)
    print(f"Test run 2 {i}")

    with open("2017/22/input.txt", "r") as fd:
        task_grid = [list(l.strip()) for l in fd.readlines()]
        *g, i = part(deepcopy(task_grid), 12, 12, deque([UP, RIGHT, DOWN, LEFT]), _burst)
        print(f"Part one {i}")
        *g, i = part(deepcopy(task_grid), 12, 12, deque([UP, RIGHT, DOWN, LEFT]), _burst2, 10000000)
        print(f"Part two {i}")
