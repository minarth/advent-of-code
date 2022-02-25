TEST_CASE = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""




def _parse(input_data): 
    return [list(line.strip()) for line in input_data.split()]

def _print(grid):
    print("".join([str(i)[-1] for i in range(len(grid[0]))]))
    for line in grid:
        print("".join(line))

def _around(grid, x, y):
    counts = {".": 0, "#": 0, "|": 0}
    counts[grid[x][y]] = -1
    for line in grid[max(x-1, 0):x+2]:
        for  el in line[max(y-1, 0): y+2]:
            counts[el] += 1

    return counts

def gol_next_iteration(grid):
    new_grid = [["" for x in line] for line in grid]

    for x, line in enumerate(grid):
        for y, el in enumerate(line):
            counts = _around(grid, x, y)
            new_grid[x][y] = el
            if el == "." and counts["|"] >= 3:
                new_grid[x][y] = "|"
            elif el == "|" and counts["#"] >= 3:
                new_grid[x][y] = "#"
            elif el == "#" and counts["#"] >= 1 and counts["|"] >= 1:
                new_grid[x][y] = "#"
            elif el == "#": 
                new_grid[x][y] = "."

    return new_grid

def part_one(grid, minutes):
    for i in range(minutes):
        grid = gol_next_iteration(grid)
        print("=" * 10, str(i+1))
        _print(grid)
        print()

    trees = sum([line.count("|") for line in grid])
    lumbyards = sum([line.count("#") for line in grid])

    return trees * lumbyards

def _hash(grid):
    return "".join(["".join(line) for line in grid])

def part_two(grid, minutes):
    historical = []

    for i in range(minutes):
        grid = gol_next_iteration(grid)
        #print("=" * 10, str(i+1))
        h = _hash(grid)
        if h in historical:
            idx  = historical.index(h)
            diff = i - idx

            #print(historical.index(h), idx + ((minutes - i - 1) % diff))
            #print(i, idx, h.count("|"), h.count("#"), ((minutes - 1 - i)%diff)+idx)
            g = historical[((minutes - 1 - i)%diff)+idx]
            print(g.count("|"), g.count("#"))
            return g.count("|") * g.count("#")
        
        historical.append(h)


    trees = sum([line.count("|") for line in grid])
    lumbyards = sum([line.count("#") for line in grid])

if __name__ == '__main__':
    grid = _parse(TEST_CASE)
    
    print(f"Test example {part_one(grid, 10)}")

    with open("input_2018_18.txt", "r") as fd:
        grid = _parse(fd.read())
        print(f"Part one {part_one(grid, 10)}")
        # too low 195471
        print(f"Part two {part_two(grid, 1000000000)}")

    