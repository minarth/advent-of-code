def process(fn: str):
    with open(fn, "r") as fd:
        return [list(l.strip()) for l in fd.readlines()]


def _next_nodes(x,y,garden):
    nodes = []
    if x-1 >= 0: nodes.append((x-1, y))  # up
    if x+1 < len(garden): nodes.append((x+1, y))    # down
    if y-1 >= 0: nodes.append((x, y-1))    # left
    if y+1 < len(garden[0]): nodes.append((x, y+1))   # right

    lt = garden[x][y]
    return [(a,b) for (a,b) in nodes if garden[a][b] == lt]


def _explore_region(point, garden):
    x,y = point
    LETTER = garden[x][y]
    region = {(x,y)}
    position_neighbours = {} 
    explore_queue = [(x,y)]
    while explore_queue:
        i,j = explore_queue.pop()
        region.add((i,j))
        nn = _next_nodes(i,j,garden)
        for (a,b) in nn: 
            if (a,b) in region: continue
            explore_queue.append((a,b))
        position_neighbours[(i,j)] = nn    

    for (i,j) in region:
        garden[i][j] = "."
    
    perimeter = sum([4 - len(v) for v in position_neighbours.values()])

    return region, len(region), perimeter, LETTER


def part_one(garden):
    # will iterate over and change the garden map
    
    regions = []
    for i in range(len(garden)):
        for j in range(len(garden[0])):
            if garden[i][j] != ".":
                 regions.append(_explore_region((i,j), garden))

    result = 0
    for (r,a,p,l) in regions:
        result += a*p
    return regions, result


def _get_lines(x,y,garden):
    x_lines, y_lines = set(), set()
    lt = garden[x][y]

    if (x-1 >= 0 and garden[x-1][y] != lt) or (x == 0): x_lines.add((x-.25, y))
    if (x+1 < len(garden) and garden[x+1][y] != lt) or (x+1 == len(garden)): x_lines.add((x+.25, y))
    if (y-1 >= 0 and garden[x][y-1] != lt) or (y == 0): y_lines.add((x, y-.25))
    if (y+1 < len(garden[0]) and garden[x][y+1] != lt) or (y+1 == len(garden[0])): y_lines.add((x,y+.25))

    return x_lines, y_lines 


def _count_xs(x:int, y:int, xs: set):
    # (x,y) point, find the fixed x, and moving along y
    queue = [(x,y)]
    found = set()
    while queue:
        a,b = queue.pop()
        if (a,b) not in xs: continue
        found.add((a,b))
        if (a,b+1) not in found and (a,b+1) not in queue:
            queue.append((a, b+1))
        if (a,b-1) not in found and (a,b-1) not in queue:
            queue.append((a, b-1))
    return found, xs - found


def _count_ys(x:int, y:int, ys: set):
    # (x,y) point, find the fixed x, and moving along y
    queue = [(x,y)]
    found = set()
    while queue:
        a,b = queue.pop()
        if (a,b) not in ys: continue
        found.add((a,b))
        if (a+1,b) not in found and (a+1,b) not in queue:
            queue.append((a+1,b))
        if (a-1,b) not in found and (a-1,b) not in queue:
            queue.append((a-1,b))
    return found, ys - found


def part_two(regions, garden):
    result = 0
    for r in regions:
        x_l, y_l = set(), set()    # x = - , y = |
        for (x,y) in r[0]:
            x,y = _get_lines(x,y,garden)
            x_l = x_l | x
            y_l = y_l | y
        
        counter = 0
        while x_l:
            x,y = next(iter(x_l))
            counter += 1
            _, x_l = _count_xs(x,y,x_l)
        while y_l:
            x,y = next(iter(y_l))   # ugly but need to partially iterate over set
            counter += 1
            _, y_l = _count_ys(x,y,y_l)
        result += counter * r[1]
    return result

if __name__ == "__main__":
    garden = process("test")
    regions, result = part_one(garden)
    print(f"part one {result}")
    garden = process("test")
    print(f"part two {part_two(regions, garden)}")

    garden = process("input")
    regions, result = part_one(garden)
    print(f"part one {result}")
    garden = process("input")
    print(f"part two {part_two(regions, garden)}")
