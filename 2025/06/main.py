from functools import reduce 

def process(fn):
    with open(fn, "r") as fd:
        data = fd.readlines()
        data = [[el.strip() for el in line.split()] for line in data]

    return [list(map(int, line)) for line in data[:-1]] + [data[-1]]


def process_part_two(fn):
    with open(fn, "r") as fd:
        d = fd.readlines()
        problems = []
        problem, op = [], None

        # this would be best to do transposed or in numpy, but lets continue with ugly approach
        # i assume only 3 lines with numbers. Oh I was wrong
        for i in range(len(d[0])):
            column = [line[i] for line in d]
            if not len("".join(column).strip()):
                problems.append(problem + [op])
                problem, op = [], None
            else:
                number = "".join([el for el in column[:-1] if el.strip()])
                problem.append(int(number))
            if column[-1].strip():
                op = column[-1]

    return problems 


def part_one(data):
    # I first rotate data so I have problems arranged like normal person
    r_data = []
    for i in range(len(data[0])):
        r_data.append([line[i] for line in data])
    results = [] 
    fnc = {
            "*": lambda x,y: x*y,
            "+": lambda x,y: x+y
            }

    for prob in r_data:
        results.append(reduce(fnc[prob[-1]], prob[:-1]))
    return sum(results)


def part_two(data):
    results = [] 
    fnc = {
            "*": lambda x,y: x*y,
            "+": lambda x,y: x+y
            }
    for prob in data:
        results.append(reduce(fnc[prob[-1]], prob[:-1]))
    return sum(results)

if __name__ == "__main__":
    data = process("test")
    print(f"part one {part_one(data)}")
    data = process_part_two("test")
    print(f"part two {part_two(data)}")
    print("="*10)
    data = process("input")
    print(f"part one {part_one(data)}")
    data = process_part_two("input")
    print(f"part two {part_two(data)}")
