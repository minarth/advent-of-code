from functools import reduce

def process(fn):
    with open(fn, "r") as fd:
        data = [d.strip() for d in fd.readlines()]
        data = [list(map(int, d)) for d in data]
        return data

def part_one(data):
    # naive way
    counter = 0
    for number in data:
        highest = 0
        for i, n in enumerate(number):
            for m in number[i+1:]:
                if n*10 + m > highest:
                    highest = n*10 + m
        counter += highest
    return counter


def find_highest(current: list, number: list, highest: list):
    # list comparation should work
    if current and highest > current:
        return highest
    
    # hardcoded length
    if len(current) + len(number) < 12:
        return highest

    if len(current) == 12 and current > highest:
        return current

    # try add first element to the 
    explored = set()
    for i,n in enumerate(number):
        if n in explored: continue
        highest = find_highest(current + [n], number[i+1:], highest)
        explored.add(n)

    return highest



def part_two(data):
    counter = 0
    for number in data:
        h = find_highest([], number, [0]*12)
        counter += reduce(lambda x,y: x*10+y, h)

    return counter



if __name__ == "__main__":
    data = process("test")
    print(f"one: {part_one(data)}")
    print(f"two: {part_two(data)}")
    print("===")
    data = process("input")
    print(f"one: {part_one(data)}")
    print(f"two: {part_two(data)}")
    # not a answer 17439
