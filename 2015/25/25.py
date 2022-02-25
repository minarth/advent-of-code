def part_one(starter, end_row, end_column):
    grid = [[starter]]
    row, col = 0, 0
    while row != end_row or col != end_column:
        prev_value = grid[row][col]
        if row == 0:
            row, col = len(grid), 0
            grid.append([])
        else:
            row -= 1
            col += 1

        grid[row].append((prev_value * 252533) % 33554393)

    return grid[end_row][end_column]

if __name__ == '__main__':
    print(f"Part one {part_one(20151125, 3009, 3018)}")