from collections import defaultdict
def load(fn):
    with open(fn, "r") as fd:
        return [list(l.strip()) for l in fd.readlines()]

def part_one(grid):
    x,y = [(i, line.index("^")) for i, line in enumerate(grid) if "^" in line][0]
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dir = 0
    while 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        _x, _y = x+dirs[dir][0], y+dirs[dir][1]
        grid[x][y] = "X"
        if not(0 <= _x < len(grid) and 0 <= _y < len(grid[0])):
            break
        while grid[_x][_y] == "#":
            dir = (dir+1) % 4
            _x, _y = x+dirs[dir][0], y+dirs[dir][1]
        x,y = _x,_y
    return sum([l.count("X") for l in grid])

def part_two(grid, passed_grid):
    pps = []
    for i, l in enumerate(passed_grid):
        for j,e in enumerate(l):
            if e == "X": pps.append((i,j))
    cntr = 0
    sx,sy = [(i, line.index("^")) for i, line in enumerate(grid) if "^" in line][0]
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    for pp in pps:
        x,y = sx,sy
        dir = 0
        if x == pp[0] and y == pp[1]: continue
        grid[pp[0]][pp[1]] = "O"
        dinged = defaultdict(int)
        dinged[f"{x},{y}"] = 0
        while 0 <= x < len(grid) and 0 <= y < len(grid[0]):
            _x, _y = x+dirs[dir][0], y+dirs[dir][1]
            if not(0 <= _x < len(grid) and 0 <= _y < len(grid[0])):
                break
            while grid[_x][_y] in "#O":
                dir = (dir+1) % 4
                dinged[f"{_x},{_y}"] += 1
                _x, _y = x+dirs[dir][0], y+dirs[dir][1]
            if max(dinged.values()) > 20:
                cntr += 1
                break
            x,y = _x,_y   
        grid[pp[0]][pp[1]] = "."
    return cntr

if __name__ == "__main__":
    grid = load("input")
    print(f"part 1 {part_one(grid)}")
    passed = grid
    grid = load("input")
    print(f"part 2 {part_two(grid, passed)}")

