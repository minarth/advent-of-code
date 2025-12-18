def process(fn):    
    with open(fn, "r") as fd:
        data = fd.readlines()
        return [list(d.strip()) for d in data]

def print_grid(data):
    for d in data:
        print("".join(d))


def part_one(grid):
    # I pad the grid with extra dots
    padded_grid = [list("."*(len(grid[0])+2)) for _ in range(len(grid)+2)]
    for i, line in enumerate(grid):
        for j, el in enumerate(line):
            padded_grid[i+1][j+1] = el

    counter = 0
    for i, line in enumerate(padded_grid[:-1]):
        for j, el in enumerate(line[:-1]):
            if i == 0 or j == 0: continue
            if padded_grid[i][j] != "@": continue
            adj_cnt = padded_grid[i-1][j-1:j+2].count("@") + \
                        padded_grid[i][j-1:j+2].count("@") -1 + \
                        padded_grid[i+1][j-1:j+2].count("@")
            
            if adj_cnt < 4: 
                counter += 1
    return counter

def part_two(grid):
    # lets start with something seriously naive
    pg = [list("."*(len(grid[0])+2)) for _ in range(len(grid)+2)]
    for i, line in enumerate(grid):
        for j, el in enumerate(line):
            pg[i+1][j+1] = el

    removal = set("Dummy") 
    while len(removal):
        removal = set()
        for i, line in enumerate(pg[:-1]):
            for j, el in enumerate(line[:-1]):
                if i == 0 or j == 0: continue
                if pg[i][j] != "@": continue
                adj_cnt = pg[i-1][j-1:j+2].count("@") + \
                            pg[i][j-1:j+2].count("@") -1 + \
                            pg[i+1][j-1:j+2].count("@")
                
                if adj_cnt < 4: 
                    removal.add((i,j))
        for (i,j) in removal:
            pg[i][j] = "."
    original_count = sum([line.count("@") for line in grid])
    new_count = sum([line.count("@") for line in pg])
    return original_count - new_count




if __name__ == "__main__":
    data = process("test")
    print(f"part one {part_one(data)}")
    print(f"part two {part_two(data)}")
    print("="*3)
    data = process("input")
    print(f"part one {part_one(data)}")
    print(f"part two {part_two(data)}")
