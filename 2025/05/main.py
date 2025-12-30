from functools import cmp_to_key

def process(fn):
    with open(fn, "r") as fd:
        data = fd.readlines()
        intervals, ids = [], []
        ints_end = False
        for d in data:
            d = d.strip()
            if not d:
                ints_end = True
                continue
            if not ints_end: intervals.append(tuple(map(int, d.split("-"))))
            else: ids.append(int(d))

    return intervals, ids


def cmp_tuple(first, second):
    a,b = first
    x,y = second
    return a-x if a!=x else b-y


def _merge_intervals(ints):
    # will keep `merged` as always sorted list of non-overlapping intervals (ints)
    merged = []
    
    # start from sorted ints, that we will continuously add to `merged`
    # merge if overlap and lets see
    ints = sorted(ints, key=cmp_to_key(cmp_tuple))
    for i in ints:
        if not len(merged):
            # add first interval into list
            merged.append(i)
        else:
            a,b = i  # unpack interval
            m,n = merged[-1]
            if m <= a <= n:
                merged.pop()
                merged.append((m, max(b,n)))
            else:
                merged.append(i)

    return merged


def _bisection(ints, value):
    # expecting ints to be ordered and merged
    # recursing this
    if len(ints) == 0: return False
    if len(ints) == 1: 
        a,b = ints[0]
        return a <= value <= b

    half = len(ints) // 2
    i,j = ints[half]
    if i <= value <= j: return True

    if value <= j: return _bisection(ints[:half], value)
    else: return _bisection(ints[half:], value)


def part_one(ints, vals):
    ints = _merge_intervals(ints)
    # here `filter` would be prettier
    counter = 0
    for v in vals:
        b = _bisection(ints, v)
        if b: counter += 1
    return counter


def part_two(ints):
    # i got prep for part two just right
    ints = _merge_intervals(ints)
    counter = 0
    for (x,y) in ints: 
        counter += y-x+1
        #print(f"{(x,y)} leads to {y-x}")
    return counter


if __name__ == "__main__":
    data = process("test")
    print(f"part one {part_one(*data)}")
    print(f"part two {part_two(data[0])}")

    print("="*10)
    data = process("input")
    print(f" part one {part_one(*data)}")
    print(f"part two {part_two(data[0])}")
