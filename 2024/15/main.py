def process(fn):
    grid, instr, empty = [], "", False
    with open(fn, "r") as fd:
        for line in fd.readlines():
            line = line.strip()
            if line == "":
                empty = True
            if not empty: grid.append(list(line))
            else: instr += line

        return grid, instr


def _move(g, i, p):
    # g ~ grid 
    # i ~ one instruction
    # p ~ position of robot
    x,y = p
    if i == "v": a,b = x+1,y
    elif i == "^": a,b = x-1,y
    elif i == "<": a,b = x,y-1
    elif i == ">": a,b = x,y+1
    
    if g[a][b] == "#": return g,p
    elif g[a][b] == ".": 
        g[x][y] = "."
        g[a][b] = "@"
        return g, (a,b)
    elif g[a][b] == "O":
        # can we move the whole column or row?
        u,v = a,b   # u,v are traversal vars for seeking what is at the end of the boxes line
        while g[u][v] == "O":
            if i == "<":   v-=1      # row right
            elif i == ">": v+=1      # row left
            elif i == "^": u-=1      # col up
            elif i == "v": u+=1      # col down

        assert g[u][v] in "#."

        if g[u][v] == "#": return g,p
        g[u][v] = "O"
        g[a][b] = "@"
        g[x][y] = "."

    return g, (a,b)


def _print(g):
    for line in g:
        print("".join(line))


def part_one(g, instr):
    # find position
    for x, line in enumerate(g):
        for y, el in enumerate(line):
            if el == "@": 
                p = (x,y)
                break
    # move
    for i in instr:
        g,p = _move(g, i, p)
    
    # calculate gps
    score = 0
    for x, line in enumerate(g):
        for y, el in enumerate(line):
            if el == "O": score += 100*x+y
    return score


def _expand_grid(g):
    expanded = []
    for line in g:
        exp_line = []
        for el in line:
            if el == "#": exp_line.extend("##")
            elif el == "O": exp_line.extend("[]")
            elif el == ".": exp_line.extend("..")
            elif el == "@": exp_line.extend("@.")
        expanded.append(exp_line)
    return expanded


def _move_boxes(g, instr, p, move_fn):
    queue = {p}
    # split into two part - search relevant boxes, move if possible
    to_move = {p}
    while queue:
        x,y = queue.pop()
        el = g[x][y]
        if el == "#": return g,p
        elif el == ".": continue
        to_move.add((x,y))
        assert el in "[]@"

        nxt = move_fn(x,y)
        if instr in "><":
            queue.add(nxt)
        elif instr in "v^":
            a,b = nxt
            queue.add(nxt)
            if g[a][b] == "[": queue.add((a,b+1))
            elif g[a][b] == "]": queue.add((a,b-1))

    # wall not found, lets move everything
    ordered_move = list(to_move)
    if instr in ">v": ordered_move = sorted(ordered_move, reverse=True)
    else: ordered_move = sorted(ordered_move)
    for mv in ordered_move:
        x,y = mv
        a,b = move_fn(x,y)
        g[a][b] = g[x][y]
        g[x][y] = "."
        if g[a][b] == "@": p = (a,b)
        
    return g, p


def _move_two(g, instr, p, move_fn):
    # move fn is a function that prescribes change of coordinates -> hope for more readable code 
    #def _move(g, i, p):
    # g ~ grid 
    # i ~ one instruction
    # p ~ position of robot
    x,y = p
    
    a,b = move_fn(x,y)
    if g[a][b] == "#": return g,p
    elif g[a][b] == ".": 
        g[x][y] = "."
        g[a][b] = "@"
        return g, (a,b)
    elif g[a][b] in "[]":
        g, p = _move_boxes(g, instr, p, move_fn)
    else:
        raise Exception("unexpected element")
    return g, p


def part_two(g, instr):
    g = _expand_grid(g)
    p = None
    for i, line in enumerate(g):
        if p is not None: break
        for j, el in enumerate(line):
            if el == "@": 
                p = (i,j)
                break
    for i in instr:
        if   i == ">": fn = lambda x,y: (x,y+1)
        elif i == "<": fn = lambda x,y: (x,y-1)
        elif i == "v": fn = lambda x,y: (x+1,y)
        elif i == "^": fn = lambda x,y: (x-1,y)
        else: raise Exception("unexpected inst")
        g,p = _move_two(g, i, p, fn)
    
    # calc the GPS values
    score = 0
    for i, line in enumerate(g):
        for j, el in enumerate(line): 
            if el == "[":
                score += 100*i + j
    return score

if __name__ == "__main__":
    grid, instr = process("test")
    print(f"part one {part_one(grid, instr)}")
    grid, instr = process("test2")
    print(f"part one {part_one(grid, instr)}")
    grid, instr = process("input")
    print(f"part one {part_one(grid, instr)}")
    
    print("test part two")
    g, i = process("test3")
    print(f"part two {part_two(g,i)}")

    g,i = process("test2")
    print(f"part two {part_two(g,i)}")

    g, i = process("input")
    print(f"part two {part_two(g,i)}")
