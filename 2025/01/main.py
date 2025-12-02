from collections import deque


def process(fn):
    with open(fn, "r") as fd:
        data = fd.readlines()

    parsed = []
    for d in data:
        if d.startswith("R"):
            parsed.append(-1*int(d[1:]))
        else:
            parsed.append(int(d[1:]))
    return parsed


def part_one(data):
    dial = deque(range(0,100))
    dial.rotate(50)
    zero_counter = 0
    for d in data:
        dial.rotate(d)
        if dial[0] == 0:
            zero_counter += 1

    return zero_counter


def part_two(data):
    dial = 50
    pass_counter = 0
    for d in data:
        if d <= 0: # moving right = easy 
            pass_counter += (dial - d) // 100
        else: # moving left
            if dial == 0: 
                pass_counter += d // 100
            elif d >= dial:
                pass_counter += (d - dial) // 100 + 1
        dial = (dial - d) % 100
    return pass_counter


if __name__ == "__main__":
    data = process("test")
    print(f"part one {part_one(data)}")
    print(f"part two {part_two(data)}") 
    print("===")
    data = process("input")
    print(f"part one {part_one(data)}")
    print(f"part one {part_two(data)}")
