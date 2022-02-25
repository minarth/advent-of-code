from collections import deque
from operator import xor
from functools import reduce

def knot_hash(lengths, length=256, position=0, skip_size=0):
    lengths = [ord(s) for s in str(lengths)] + [17, 31, 73, 47, 23]
    h = range(length)
    for i in range(64):
        for l in lengths:
            if l > len(h): continue
            h = list(h) 
            h = deque(h[:l][::-1] + h[l:])
            h.rotate(-1*(l+skip_size))
            position += l+skip_size
            skip_size += 1

    # h is now sparse hash
    h.rotate(position)
    h = list(h)
    dense = []
    for i in range(16):
        dense.append(f"{reduce(xor, h[i*16:(i+1)*16]):0{2}x}")

    return "".join(dense)

def _generate_grid(inp_string):
    grid = []
    for i in range(128):
        row = knot_hash(f"{inp_string}-{i}")
        binary_row = ""
        for r in row:
            binary_row += str(bin(int(r, 16))[2:].zfill(4))
        binary_row = binary_row.replace("0", ".").replace("1", "#")
        grid.append(list(binary_row))

    return grid

def part_one(inp_string):
    grid = _generate_grid(inp_string)
    return sum([g.count("#") for g in grid])

def _map_region(top_left, grid):
    positions = set([top_left])
    orig_length = 0
    while orig_length < len(positions):
        orig_length = len(positions)
        new_pos = set()
        for p in positions:
            x,y = p
            # left
            x1, y1 = x, max(y-1, 0)
            if grid[x1][y1] == "#":
                new_pos.add((x1,y1))
            # right
            x1, y1 = x, min(y+1,len(grid[0])-1)
            if grid[x1][y1] == "#":
                new_pos.add((x1,y1))
            # up
            x1, y1 = max(x-1, 0), y
            if grid[x1][y1] == "#":
                new_pos.add((x1,y1))
            # bottom
            x1, y1 = min(x+1, len(grid)-1), y
            #print(x1,y1, len(grid), len(grid[x1]))
            if grid[x1][y1] == "#":
                new_pos.add((x1,y1))
        positions = positions.union(new_pos)
    return positions

def part_two(inp_string):
    grid = _generate_grid(inp_string)

    regions = 0
    while sum([g.count("#") for g in grid]) > 0:

        for i, row in enumerate(grid):
            if "#" in row:
                position = row.index("#")
                positions = _map_region((i, position), grid)
                for p in positions:
                    x,y = p
                    grid[x][y] = regions
                regions += 1
                break

    return regions, grid




if __name__ == '__main__':
    print(f"Test {part_one('flqrgnkx')}")
    print(f"Part {part_one('wenycdww')}")

    print(f"Test 2 {part_two('flqrgnkx')[0]}")
    print(f"Part 2 {part_two('wenycdww')[0]}")