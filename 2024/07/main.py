def process(fn: str):
    tests, vals = [], []
    with open(fn, "r") as fd:
        for l in fd.readlines():
            l = l.strip()
            tests.append(int(l.split(": ")[0]))
            vals.append(list(map(int, l.split(": ")[1].split(" "))))
    return tests, vals


def traverse(target: int, current: int, vals: list):
    if not vals and target == current: return current
    if not vals: return -1
     
    left = traverse(target, current+vals[0], vals[1:])
    right = traverse(target, current*vals[0], vals[1:])

    return max(left, right)


def traverse_two(target: int, current: int, vals: list):
    if not vals and target == current: return current
    if not vals: return -1

    l = traverse_two(target, current*vals[0], vals[1:])
    m = traverse_two(target, current+vals[0], vals[1:])
    r = traverse_two(target, int(f"{current}{vals[0]}"), vals[1:])
    
    return max(l,m,r)

def part(ts: list, vs: list, trvs: callable):
    counter = 0
    for t, vals in zip(ts, vs):
        if trvs(t, vals[0], vals[1:]) == t:
            counter += t
    return counter                        


if __name__ == "__main__":
    t,v = process("input")
    print(f"part one {part(t, v, traverse)}")
    print(f"part two {part(t, v, traverse_two)}")

