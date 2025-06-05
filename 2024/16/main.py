from heapq import heappush as hpush, heappop as hpop

EAST = 0
WEST = 1
NORTH = 2
SOUTH = 3

DIRECTIONS = [EAST, SOUTH, WEST, NORTH]   # clockwise

def process(fn: str) -> list[list[str]]:
    with open(fn, "r") as fd:
        grid = [list(line.strip()) for line in fd.readlines()]

    return grid


def gprint(grid: list[list[str]]):
    for line in grid:
        print("".join([str(e)[-1]  for e in line]))


def heuristics(point: tuple, end: tuple) -> int:
    a,b = point
    x,y = end
    turn_h = 1000 if (a!=x) and (b!=y) else 0
    return abs(a-x) + abs(b-y) + turn_h   # move with optimistically only one turn needed


def next_actions(grid, point, e, orientation, orient_price=1000):
    n_act = list()
    
    # move
    x,y = point
    a,b = None, None
    if   orientation == EAST:  a,b = x,y+1
    elif orientation == WEST:  a,b = x,y-1
    elif orientation == SOUTH: a,b = x+1,y
    elif orientation == NORTH: a,b = x-1,y

    if grid[a][b] in "SE.":
        n_act.append(((a,b),orientation,1))

    # rotate
    idx = DIRECTIONS.index(orientation)
    n_act.append(((x,y), DIRECTIONS[(idx+1) % len(DIRECTIONS)],orient_price))
    n_act.append(((x,y), DIRECTIONS[(idx-1) % len(DIRECTIONS)],orient_price))
    
    return n_act

# todo i should have point as x,y,o not only x,y
def shortest(grid, s, e):
    s = (heuristics(s,e), s, EAST, 0, f"({s},{EAST})"),
    # print(s)
    q = list(s)
    visited = set()
    while q:
        point = hpop(q)
        h, p, o, s, path =  point   # heuristics, point (x,y), orientation, score so far, path
        if (p,o) in visited: continue
        visited.add((p,o))
        # print(f"expanding {p,o,path}")
        if p == e: return s
         
        for na in next_actions(grid, p, e, o):
            np, no, ns = na
            if (np, no) in visited: continue
            # print(f"adding to q {np, no, ns}")
            hpush(q, (heuristics(np, e)+s, np, no, s+ns,path+f"|{np},{no}"))  


def part_one(grid):
    s, e = None, None
    for i, line in enumerate(grid):
        for j, el in enumerate(line):
            if el == "S": s = (i,j)
            if el == "E": e = (i,j)
    return shortest(grid, s, e)


def all_shortest(grid, s, e, min_path):
    # need to move from astar to something like dijkstra
    x,y = s
    s = (0, s, EAST),
    # print(s)
    q = list(s)

    distances = [[[-1 for _ in range(4)] for _ in range(len(grid[0]))] for _ in range(len(grid))]
    paths = {}
    paths[(x,y,EAST)] = [(x,y,EAST)]
    visited = set()
    distances[x][y][EAST] = 0
    print(min_path) 
    while q:
        #print(q, visited)
        point = hpop(q)
        l, (x,y), o = point   # path length, point, orientation
        if ((x,y),o) in visited: continue
        visited.add(((x,y),o)) 
        if l > min_path: continue

        for (np, no, ns) in next_actions(grid, (x,y), e, o):
            a,b = np
            hpush(q, (l+ns, np, no))  
            if distances[a][b][no] == -1 or distances[a][b][no] > l+ns:
                distances[a][b][no] = l+ns
                paths[(a,b,no)] = [(x,y,o)]
            elif distances[a][b][no] == l+ns:
                paths[(a,b,no)].append((x,y,o))

    #gprint(distances)
    ## now reconstruct the paths
    points = list()
    traversing = list()
    a,b = e
    traversing = [(a,b,o) for o in DIRECTIONS]
    while traversing:
        p = traversing.pop()
        if p not in paths: continue
        for point in paths[p]:
            if point in points: continue
            traversing.append(point)
            points.append(point)

    for (x,y,_) in points:
        grid[x][y] = "O"
    #gprint(grid)

    return len(set([(x,y) for (x,y,_) in points]))

def part_two(grid):
    s, e = None, None
    for i, line in enumerate(grid):
        for j, el in enumerate(line):
            if el == "S": s = (i,j)
            if el == "E": e = (i,j)
    length = shortest(grid, s, e)
    return all_shortest(grid, s, e, length)


if __name__ == "__main__":
    gprint(data := process("test"))
    print(f"part one {part_one(data)}")
    print(f"part two {part_two(data)}")
    print("-"*10)
    gprint(data := process("test2"))
    print(f"part one {part_one(data)}")
    print(f"part two {part_two(data)}")
    print("="*10)
    data = process("input")
    print(f"part one {part_one(data)}")
    print(f"part two {part_two(data)}")
