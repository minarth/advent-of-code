import re
from heapq import heappush, heappop


def parse(input_string: str, grid_size: int = 20) -> int:
    grid = []
    mid = int(grid_size/2)-1
    #mid = 5
    for i in range(grid_size):
        if i % 2:
            grid.append(list("?."*grid_size))
        else:
            grid.append(list("#?"*grid_size))

    grid[mid][mid] = "X"
    expand_grid(mid, mid, grid, input_string)
    
    return grid, mid


def expand_grid(x, y, grid, path, hint=None):

    # walk through path until branching occurs

    # if branching, parse the branching group and recurse into 
    #    branching opt + rest of path

    subpath = ""
    options = []
    option = ""
    brackets = 0

    for i, ch in enumerate(path):

        if ch == "(": brackets += 1

        if brackets:
            subpath += ch
            option += ch
        else:
            if ch == "W":
                grid[x][y-1] = "|"
                y -= 2
                if hint:
                    grid[x][y] = str(hint)
            elif ch == "N":
                grid[x-1][y] = "-"
                x -= 2
            elif ch == "E":
                grid[x][y+1] = "|"
                y += 2
            elif ch == "S":
                grid[x+1][y] = "-"
                x += 2
            if hint is not None:
                grid[x][y] = str(hint)

        if ch == ")": 
            brackets -= 1
            if brackets == 0:
                options = options + [option]
                cleaned_opts = []
                for o, opt in enumerate(options):
                    if o == 0:
                        opt = opt[1:]
                    if len(opt) > 1:
                        cleaned_opts.append(opt[:-1])

                for c, co in enumerate(cleaned_opts):
                    expand_grid(x, y, grid, co + path[i+1:], hint+c+1 if hint is not None else None)
                break        
        elif ch == "|" and brackets == 1:
            options.append(option)
            option = ""
            
def get_neighbours(grid, x, y):
    n = []
    if x > 1 and grid[x-1][y] in "|-":
        n.append((x-2, y))
    if x+2 < len(grid) and grid[x+1][y] in "|-":
        n.append((x+2, y))
    if y > 1 and grid[x][y-1] in "|-":
        n.append((x, y-2))
    if y+2 < len(grid) and grid[x][y+1] in "|-":
        n.append((x, y+2))
    return n

def breadth_search(grid, x, y):
    searched = set()
    searching = []
    heappush(searching, (0, x, y))
    max_dist = 0

    while searching:
        (dist, nx, ny) = heappop(searching)
        searched.add((nx, ny))

        grid[nx][ny] = dist
        max_dist = max(max_dist, dist)

        for (n2x, n2y) in get_neighbours(grid, nx, ny):
            if (n2x, n2y) not in searched:
                heappush(searching, (dist+1, n2x, n2y))

    return max_dist
def print_grid(grid):
    print()
    for line in grid:
        print("".join([str(element) for element in line]))
    print()

def part_two(grid):
    far_rooms = 0
    for line in grid:
        for element in line:
            if type(element) is int and element >= 1000:
                far_rooms += 1
    return far_rooms


if __name__ == '__main__':
    grid, mid = parse("^ENWWW(NEEE|SSE(EE|N))$", 21)
    print(f" First example {breadth_search(grid, mid, mid)}")

    grid, mid = parse("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$", 21)
    print(f" Second example {breadth_search(grid, mid, mid)}")
    grid, mid = parse("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", 21)
    print(f" Third example {breadth_search(grid, mid, mid)}")

    grid, mid = parse("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", 21)
    print(f" Fourth example {breadth_search(grid, mid, mid)}")

    #print(parse_longest("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"))
    #print(parse_longest("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"))
    #print(parse_longest("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"))
    with open("input_2018_20.txt", "r") as f:
        grid, mid = parse(f.readlines()[0], 1001)
        print(f"Part one {breadth_search(grid, mid, mid)}")
        print(f"Part two {part_two(grid)}")


