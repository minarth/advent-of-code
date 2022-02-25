def _parse(inp):
    return tuple(map(lambda x: int(x), inp.strip().split()))

def _is_triangle(triangle):
    a, b, c = triangle
    return (a + b) > c and (b + c) > a and (a + c) > b

def part_one(triangles):
    return len([t for t in triangles if _is_triangle(t)])

def part_two(data):
    triangles = 0
    for row in range(3):
        row_data = [d[row] for d in data]
        for triangle in range(0, len(row_data), 3):
            a,b,c = row_data[triangle], row_data[triangle+1], row_data[triangle+2]
            triangles += 1 if _is_triangle((a,b,c)) else 0

    return triangles

if __name__ == '__main__':
    with open("input_2016_03.txt", "r") as f:
        test_input = list(map(_parse, f.readlines()))
        print(f"Part one {part_one(test_input)}")
        print(f"Part two {part_two(test_input)}")