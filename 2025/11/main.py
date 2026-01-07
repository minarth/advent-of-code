def process(fn):
    with open(fn, "r") as fd:
        return {v.split(":")[0]: v.split(":")[1].strip().split(" ") for v in fd.readlines()}


def part_one(data):
    q = ["you"]  # start with exploring from my place
    counter = 0

    while q:
        state = q.pop(0)
        if state == "out": 
            counter += 1
            continue
        for v in data[state]:
            q.append(v)
    return counter


def _find_path(data, state, end, memory):
    # already found solutions
    if state == end:
        return 1
    if state == "out" or state not in data: 
        return 0
    if state in memory:
        return memory[state]

    counter = 0
    for s in data[state]:
        counter += _find_path(data, s, end, memory)
    memory[state] = counter
    return counter


def part_two(data):
    # seriously ugly, but works very fast
    s_f = _find_path(data, "svr", "fft", {})
    s_d = _find_path(data, "svr", "dac", {})
    d_f = _find_path(data, "dac", "fft", {})
    f_d = _find_path(data, "fft", "dac", {})
    d_o = _find_path(data, "dac", "out", {})
    f_o = _find_path(data, "fft", "out", {})

    assert d_f == 0 or f_d == 0, "we should have one first"
    if d_f > 0:
        # dac is on the path before fft
        # svr -> dac -> fft -> out
        return s_d * d_f * f_o
    else:
        # svr -> fft -> dac -> out
        return s_f * f_d * d_o


if __name__ == "__main__":
    data = process("test")
    print(f"part one {part_one(data)}")
    data = process("test2")
    print(f"part two {part_two(data)}")
    print("="*10)
    data = process("input")
    print(f"part one {part_one(data)}")
    print(f"part two {part_two(data)}")
