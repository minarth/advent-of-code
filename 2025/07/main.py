def process(fn):
    with open(fn, "r") as fd:
        grid = fd.readlines()
        grid = [l.strip() for l in grid]
        for i, line in enumerate(grid):
            if "S" in line:
                start = (i, line.index("S"))
                break
        return grid, start

def part_one(g, start):
    # BFS approach
    counter = 0
    queue = [start]
    visited = set()
    while queue:
        (x,y) = queue.pop(0)  # FIFO
        x += 1
        if x == len(g) or (x,y) in visited: continue # edge of map or already explored
        visited.add((x,y))
        if g[x][y] == ".": queue.append((x,y))
        elif g[x][y] == "^": 
            queue.extend([(x,y-1), (x,y+1)])
            counter += 1

    return counter


def part_two(g, point, memory):
    # find all possible paths down
    # lets recurse with dynamic memory - on its own its too much
    x,y = point
    if (x,y) not in memory: 
        if x == len(g): memory[(x,y)] = 1
        elif g[x][y] in ".S": memory[(x,y)] = part_two(g, (x+1, y), memory)
        elif g[x][y] == "^": memory[(x,y)] = (part_two(g, (x,y-1), memory) + part_two(g, (x,y+1), memory))
    
    return memory[(x,y)]


if __name__ == "__main__":
    g,s = process("test")
    print(g,s)
    print(f"part one {part_one(g,s)}")
    print(f"part two {part_two(g,s, {})}")
    print("="*10)
    g,s = process("input")
    print(f"part one {part_one(g,s)}")
    print(f"part two {part_two(g,s, {})}")
