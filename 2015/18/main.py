def _parse(line):
    """
    >>> _parse("..#..##.##")
    [0, 0, 1, 0, 0, 1, 1, 0, 1, 1]
    """
    return [0 if s == "." else 1 for s in line.strip()]

def _print(grid):
    for row in grid:
        print("".join([str(cell) for cell in row])\
            .replace("0", ".").replace("1", "#"))

def _create_new_grid(grid):
    new_grid = []
    for row in range(len(grid)):
        new_row = []
        for col in range(len(grid[0])):
            # left upper row, left upper col
            lu_r, lu_c = max(0, row-1), max(0, col-1)
            # right bottom row, right bottom col
            br_r, br_c = min(len(grid), row+1), min(len(grid[0]), col+1)
            neighborhood = [g[lu_c:br_c+1] for g in grid[lu_r:br_r+1]]
            neighbor_value = sum([sum(row) for row in neighborhood])            
            current = grid[row][col]
            if current == 1:
                # current cell value is sumed in the neighbor_value
                neighbor_value -= 1
                new_value = 1 if 2 <= neighbor_value <= 3 else 0
            else:
                new_value = 1 if neighbor_value == 3 else 0

            new_row.append(new_value)
        new_grid.append(new_row)
    return new_grid

def part_one(in_s, steps):
    grid = in_s 
    for _ in range(steps):
        grid = _create_new_grid(grid)
    
    return sum([sum(row) for row in grid])

def part_two(in_s, steps):
    grid = in_s 
    for _ in range(steps):
        grid = _create_new_grid(grid)
        grid[0][0], grid[0][-1], grid[-1][0], grid[-1][-1] = 1,1,1,1
    return sum([sum(row) for row in grid])

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    with open("2015/18/input.txt", "r") as f:
        test_input = f.readlines()
        parsed_input = [_parse(t) for t in test_input]
        print(f"Part one: {part_one(parsed_input, 100)}")
        print(f"Part two: {part_two(parsed_input, 100)}")
