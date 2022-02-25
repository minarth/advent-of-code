def _rangify(inp):
    if len(inp) == 1:
        inp = 2*inp
    return list(range(inp[0], inp[1]+1))

def _parse(veins):
    clays = []
    for vein in veins.split("\n"):
        a,b = vein.strip().split(", ")
        # doing inversly so it matches same approach and visualizations as assignment
        if "x" in a:
            x, y = b, a
        else:
            x, y = a, b
        x, y = x.split("=")[1], y.split("=")[1]
        x, y = x.split(".."), y.split("..")
        x, y = list(map(int, x)), list(map(int, y))
        x, y = _rangify(x), _rangify(y)
        clays.append((x,y))

    m_x = max([max(c[0]) for c in clays])
    m_y = max([max(c[1]) for c in clays])

    grid = [["." for _ in range(m_y+1)] for _ in range(m_x+1)]
    for c_x, c_y in clays:
        for x in c_x:
            for y in c_y:
                grid[x][y] = "#"

    return grid 

def _is_between_walls(g, point):
    x,y = point
    # From https://stackoverflow.com/a/52452977/1253121
    wall_positions = [idx for idx, ch in enumerate(g[x]) if ch == "#"]
    if len(wall_positions) < 2: return False

    for start, end in zip(wall_positions[:-1], wall_positions[1:]):
        if start < y < end:
            # get bellow elements to check, if there is no "hole"
            elements = g[x+1][start+1:end]
            if "." not in elements:
                return (start, end)

    return False


def _simulate(g, focus, spring=(500, 0)):
    # move down
    fx, fy = focus
    if g[fx][fy] == "#": return []
    x,y = (fx+1, fy)
    #print(fx, fy, x, y)
    if x > len(g): 
        print("Line 55 break")
        return []
    
    # if down water or wall - fill layer
    walls = _is_between_walls(g, focus)
    if x == len(g) and g[fx][fy] == ".":
        g[fx][fy] = "|"
    elif g[x][y] in "~#" and walls:
        g[fx][walls[0]+1:walls[1]] = "~"*(walls[1]-walls[0]-1)
        return [(fx-1, fy)]
    elif g[x][y] in "~#":
        followups = []
        tmp_y = y
        while tmp_y >= 0 and g[fx][tmp_y] != "#":
            g[fx][tmp_y] = "|"
            if g[x][tmp_y] == ".":
                followups.append((x, tmp_y))
                break
            tmp_y -= 1
        tmp_y = y
        while tmp_y < len(g[0]) and g[fx][tmp_y] != "#":
            g[fx][tmp_y] = "|"
            if g[x][tmp_y] == ".":
                followups.append((x, tmp_y))
                break
            tmp_y += 1
        return followups
    else:
        g[fx][fy] = "|" 
        return [(x,y)]

    return []


def _print(grid, x_min=None, x_max=None, y_min=None, y_max=None):
    # y are cols
    # x are rows
    for line in grid[x_min:x_max]:
        print("".join(line[y_min:y_max]))

def part_one(veins):
    
    _print(g)

    x = [(1, 500)]
    while x:
        new_xs = []
        #print("="*10)
        for point in x:
            #print(point)
            new_xs += _simulate(g, point)
            #_print(g, y_min=495)        
            #print()
        x = new_xs

    level = sum([line.count("~") for line in g])
    flows = sum([line.count("|") for line in g])
    return level+flows

if __name__ == '__main__':
    test_veins = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""
    #g = _parse(test_veins)
    #print(f"Test {part_one(g)}")
    
    with open("input_2018_17.txt", "r") as fd:
        g = _parse(fd.read())
        print(f"Part one {part_one(g)}")
