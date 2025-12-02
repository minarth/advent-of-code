def process(fn):
    with open(fn, "r") as fd:
        data = fd.readline().strip().split(",")
        data = [d.split("-") for d in data]
        return [(int(a),int(b)) for (a,b) in data]


def part_one(data):
    invalids = 0
    for a,b in data:
        for i in range(a,b+1):
            num = str(i)
            if num[:len(num)//2] == num[len(num)//2:]: invalids += i
    return invalids


def part_two(data):
    invalids = 0
    for a,b in data:
        for i in range(a,b+1):
            num = str(i)
            for size in range(1,len(num)):
                if size > len(num)//2: break
                part = num[:size] * (len(num) // size)
                if part == num: 
                    invalids += i
                    break
    return invalids


if __name__ == "__main__":
    data = process("test")
    print(f"one: {part_one(data)}")
    print(f"two: {part_two(data)}")
    print("====")
    data = process("input")
    print(f"one: {part_one(data)}")
    print(f"two: {part_two(data)}")
