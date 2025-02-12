def read_map(fn: str):
    with open(fn, "r") as fd:
        data = fd.readlines()
        return [[int(e) for e in line.strip()] for line in data]

def _print_path(m, path):
    xs, ys = [x for (x, _) in path], [y for (_, y) in path]
    x_0, x_1, y_0, y_1 = min(xs), max(xs), min(ys), max(ys)
    x_0, x_1 = max(x_0-1, 0), min(x_1+1, len(m)-1)
    y_0, y_1 = max(y_0-1, 0), min(y_1+1, len(m[0])-1)
    for x in range(x_0, x_1+1):
        line = ""
        for y in range(y_0, y_1+1):
            line += str(m[x][y]) if (x,y) in path else "."
        print(line)


# using m instead of map, which is a keyword
def _dps(m, pos, visited):
    x,y = pos
    if m[x][y] == 9:
        return set((pos,))
    next_pos = []
    if x > 0: next_pos.append((x-1,y))            # UP
    if x < len(m)-1:  next_pos.append((x+1,y))    # DOWN
    if y > 0: next_pos.append((x,y-1))            # LEFT
    if y < len(m[0])-1: next_pos.append((x,y+1))  # RIGHT
    found = set()
    for n in next_pos:
        if m[n[0]][n[1]]-m[x][y] != 1: continue   # not a good hike
        if n in visited: continue
        visited = visited + [n]
        found = found | _dps(m, n, visited)
    return found

def part_one(m):
    starts = []
    for i, line in enumerate(m):
        for j, e in enumerate(line):
            if e == 0: starts.append((i,j))
    ends = {k: set() for k in starts}
    for s in starts:
        ends[s] = _dps(m, s,list()) 
    return sum([len(v) for v in ends.values()])

def _dps2(m, pos, visited):
    x,y = pos
    if m[x][y] == 9:
        return [pos]
    next_pos = []
    if x > 0: next_pos.append((x-1,y))            # UP
    if x < len(m)-1:  next_pos.append((x+1,y))    # DOWN
    if y > 0: next_pos.append((x,y-1))            # LEFT
    if y < len(m[0])-1: next_pos.append((x,y+1))  # RIGHT
    found = list()
    for n in next_pos:
        if m[n[0]][n[1]]-m[x][y] != 1: continue   # not a good hike
        if n in visited: continue
        visited = visited + [n]
        abc = _dps2(m,n,visited)
        found = found + abc 
    return found

def part_two(m):
    starts = []
    for i, line in enumerate(m):
        for j, e in enumerate(line):
            if e == 0: starts.append((i,j))
    ends = {k: list() for k in starts}
    for s in starts:
        ends[s] = _dps2(m, s, list()) 
    return sum([len(v) for v in ends.values()])

if __name__ == "__main__":
    m = read_map("input")
    # 1431 too high
    print(f"part one {part_one(m)}") 
    print(f"part two {part_two(m)}")
