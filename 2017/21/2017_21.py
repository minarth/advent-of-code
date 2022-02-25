import re
from copy import copy

def _parse(line):
    return line.strip().split(" => ")


def _all_rotations_flips(cell):
    rotations = [copy(cell)]
    rotated = copy(cell)
    for _ in range(3):
        rotated = list(zip(*reversed(rotated)))
        rotations.append(rotated)

    flips = []  
    for rotation in rotations:
        flips.append(list(map(list, (map(reversed, rotation)))))

    combinations = rotations + flips

    return set(["/".join(["".join(x) for x in c]) for c in combinations])

def _enhance(grid, rules):
    
    if len(grid) % 2 == 0:
        split = len(grid) // 2
        old_size = 2
        cell_size = 3
    elif len(grid) % 3 == 0:
        split = len(grid) // 3
        old_size = 3
        cell_size = 4

    new_grid = [[None for _ in range(split*cell_size)] for _ in range(split*cell_size)]
    for row in range(split):
        for col in range(split):
            cell = [r[col*old_size:(col+1)*old_size] for r in grid[row*old_size:(row+1)*old_size]]
            combs = _all_rotations_flips(cell)
            for c in combs:
                if c in rules:
                    rule = rules[c].split("/")
                    for i in range(cell_size):
                        for j in range(cell_size):
                            new_grid[row*cell_size+i][col*cell_size+j] = rule[i][j]
                    break
    return new_grid

def part(grid, rules, its=5):
    for i in range(its):
        print(f"Iteration {i} with grid size {len(grid)}")
        grid = _enhance(grid, rules)

    return sum([row.count("#") for row in grid])


if __name__ == '__main__':
    with open("input_2017_21.txt", "r") as fd:
        task_rules = [_parse(line) for line in fd.readlines()]
        task_rules = {k: v for k,v in task_rules}
    test_rules = {"../.#": "##./#../...", ".#./..#/###": "#..#/..../..../#..#"}
    starting_grid = [[".","#","."], [".", ".", "#"], ["#","#","#"]]
    a = _enhance(starting_grid, test_rules)
    print("="*20)
    b = _enhance(a, test_rules)

    print(f"Part one {part(starting_grid, task_rules)}")
    print(f"Part two {part(starting_grid, task_rules, 18)}")

