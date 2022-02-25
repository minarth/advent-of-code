def part_one(instructions):
    """
    >>> part_one(["ULL", "RRDDD", "LURDL", "UUUUD"])
    '1985'
    """
    pad = [[1,2,3], [4,5,6], [7,8,9]]
    x,y = 1,1

    code = []
    for line in instructions:
        line = line.strip()
        for command in line:
            if command == "U":
                x = max(0, x-1)
            elif command == "D":
                x = min(len(pad)-1, x+1)
            elif command == "L":
                y = max(0, y-1)
            elif command == "R":
                y = min(len(pad[0])-1, y+1)        
        code.append(str(pad[x][y]))

    return "".join(code)

def part_two(instructions):
    """
    >>> part_two(["ULL", "RRDDD", "LURDL", "UUUUD"])
    '5DB3'
    """
    pad = [[None, None, 1, None, None], [None, 2, 3, 4, None], [5,6,7,8,9], [None, "A", "B", "C", None], [None, None, "D", None, None]]
    x,y = 2,0

    code = []
    for line in instructions:
        line = line.strip()
        for command in line:
            new_x, new_y = x, y
            if command == "U":
                new_x = max(0, x-1)
            elif command == "D":
                new_x = min(len(pad)-1, x+1)
            elif command == "L":
                new_y = max(0, y-1)
            elif command == "R":
                new_y = min(len(pad[0])-1, y+1)  
            
            if pad[new_x][new_y] is not None:
                x,y = new_x, new_y      
        code.append(str(pad[x][y]))

    return "".join(code)

if __name__ == '__main__':
    from doctest import testmod
    testmod()

    with open("input_2016_02.txt", "r") as f:
        test_input = f.readlines()
        print(f"Part One {part_one(test_input)}")
        print(f"Part Two {part_two(test_input)}")