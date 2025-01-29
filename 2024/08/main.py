from collections import defaultdict

def process(fn: str):
    with open(fn, "r") as fd:
        grid = [l.strip() for l in fd.readlines()]
        antennas = defaultdict(list)
        for i, l in enumerate(grid):
            for j, e in enumerate(l):
                if e != ".":
                    antennas[e].append((i,j))
    return grid, antennas


def part_one(g,a):
    antidote = set()
    x_max, y_max = len(g), len(g[0])
    for k,vals in a.items():
        for (x1,y1) in vals:
            for (x2,y2) in vals:
                if (x1,y1) == (x2,y2): continue
                x,y = 2*x1-x2, 2*y1-y2
                # candidate
                if 0 <= x < x_max and 0 <= y < y_max:
                    antidote.add((x,y))

    return len(antidote)
                

def part_two(g,a):
    antidote = set()
    x_max, y_max = len(g), len(g[0])
    for k,vals in a.items():
        for (x1,y1) in vals:
            for (x2,y2) in vals:
                if (x1,y1) == (x2,y2): continue
                dx,dy = x1-x2, y1-y2
                # candidate
                x, y = x1+dx, y1+dy
                antidote.add((x1,y1))
                antidote.add((x2,y2))
                while 0 <= x < x_max and 0 <= y < y_max:
                    antidote.add((x,y))
                    x,y = x+dx, y+dy
    return len(antidote) 


if __name__ == "__main__":
    g,a = process("input")
    print(part_one(g,a))          
    print(part_two(g,a))
                    
