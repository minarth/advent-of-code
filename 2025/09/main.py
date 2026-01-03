from heapq import heappop, heappush

def process(fn):
    with open(fn, "r") as fd:
        return [tuple(map(int,line.strip().split(","))) for line in fd.readlines()]


def part_one(points):
    dists = []
    for i, (a,b) in enumerate(points):
        for j, (c,d) in enumerate(points):
            heappush(dists,-1*(abs(a-c)+1)*(abs(b-d)+1))
    return -1*heappop(dists)


def _is_inner(lines, p, q):
    # is rectangle made by p,q corners inner?
    # check if there are any lines "inside"
    # sadly this is not general enough, but implementing raytracing seemed overkill
    a,b = p
    c,d = q
    min_x, max_x = min(a,c), max(a,c)
    min_y, max_y = min(b,d), max(b,d)
    for i in range(min_x+1, max_x):
        # horizontal insides
        if (i, min_y+1) in lines or (i, max_y-1) in lines: return False
    for j in range(min_y+1, max_y):
        # vertical insides
        if (min_x+1, j) in lines or (max_x-1, j) in lines: return False
    return True


def part_two(points):
    # I hate the rotation of assignemnt vs what is the most convenient way
    # x ar columns, y are rows
    x,y = max([p[0] for p in points]), max([p[1] for p in points])
    # lets start with naive way
    lines = set()
    for (a,b),(c,d) in zip(points, points[1:]+[points[0]]):
        if a != c:  # horizontal
            for i in range(min(a,c), max(a,c)+1):
                lines.add((i,b))
        else:   # vertical 
            for i in range(min(b,d), max(b,d)+1):
                lines.add((a,i))
    
    dists = []
    for i, (a,b) in enumerate(points):
        for j, (c,d) in enumerate(points[:i]):
            dists.append(((abs(a-c)+1)*(abs(b-d)+1), (a,b), (c,d)))
    
    dists = sorted(dists, key=lambda x: x[0], reverse=True)   
    # this is ugly bruteforce, but it works
    while dists:
        d, p, q = dists.pop(0)
        if _is_inner(lines, p, q): return d
    return None
        

if __name__ == "__main__":
    points = process("test")
    print(f"part one {part_one(points)}")
    print(f"part two {part_two(points)}")
    print("="*10)
    points = process("input")
    print(f"part one {part_one(points)}")
    print(f"part two {part_two(points)}")
