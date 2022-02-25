from copy import copy, deepcopy
from collections import defaultdict
import re
from typing import final

fncs = {
    "addr": lambda ins, r: r[ins[0]] + r[ins[1]],
    "addi": lambda ins, r: r[ins[0]] + ins[1],
    "mulr": lambda ins, r: r[ins[0]] * r[ins[1]],
    "muli": lambda ins, r: r[ins[0]] * ins[1],
    "banr": lambda ins, r: r[ins[0]] & r[ins[1]],
    "bani": lambda ins, r: r[ins[0]] & ins[1],
    "borr": lambda ins, r: r[ins[0]] | r[ins[1]],
    "bori": lambda ins, r: r[ins[0]] | ins[1],
    "setr": lambda ins, r: r[ins[0]],
    "seti": lambda ins, r: ins[0],
    "gtir": lambda ins, r: 1 if ins[0] > r[ins[1]] else 0,
    "gtri": lambda ins, r: 1 if r[ins[0]] > ins[1] else 0,
    "gtrr": lambda ins, r: 1 if r[ins[0]] > r[ins[1]] else 0,
    "eqir": lambda ins, r: 1 if ins[0] == r[ins[1]] else 0,
    "eqri": lambda ins, r: 1 if r[ins[0]] == ins[1] else 0,
    "eqrr": lambda ins, r: 1 if r[ins[0]] == r[ins[1]] else 0,
}

code2fnc = {k: set(fncs.keys()) for k in range(16)}

def _parse(lines):
    triplets = re.findall(r"Before: \[(\d+, \d+, \d+, \d+)\]\n(\d+ \d+ \d+ \d+)\nAfter:  \[(\d+, \d+, \d+, \d+)\]\n", lines)
    casted = []
    for bfr, cmd, after in triplets:
        bfr = list(map(int, bfr.strip().split(", ")))
        after = list(map(int, after.strip().split(", ")))
        cmd = list(map(int, cmd.strip().split(" ")))
        casted.append((bfr, cmd, after))

    return casted

def _parse2(line):
    return list(map(int, line.strip().split(" ")))

def exec(fn, inputs, registers):
    """
    >>> exec("addr", [0, 1, 2], [1,3,0,0])
    [1, 3, 4, 0]

    >>> exec("addr", [0, 1, 1], [1,3,0,0])
    [1, 4, 0, 0]
    """
    regs = copy(registers)
    regs[inputs[2]] = fncs[fn](inputs, registers)
    return regs

def part_one(inputs):
    counter = 0
    for bfr, cmd, aftr in inputs:
        viable = set()
        for f in fncs:
            output = exec(f, cmd[1:], bfr)
            if output == aftr: 
                viable.add(f)
        if len(viable) >= 3: counter += 1
        code2fnc[cmd[0]].intersection_update(viable)
    return counter

def fix_codes_2_fnc():
    """
    Very naive implementation, not general solution to finding valid assignment
    """

    final_codes = {k: None for k in range(16)}
    while None in final_codes.values():        
        for code, fns in code2fnc.items():
            if len(fns) == 1:
                final_codes[code] = fns.pop()
            for c2, fns2 in code2fnc.items():
                fns2.discard(final_codes[code])
    return final_codes

def part_two(code2fncs, program):
    memory = [0,0,0,0]
    for op in program:
        memory = exec(code2fncs[op[0]], op[1:], memory)
    
    return memory

if __name__ == "__main__":
    with open("2018/16/part_one.txt", "r") as fd:
        parsed = _parse(fd.read())

    #print(f"Test {part_one([([3,2,1,1],[9,2,1,2],[3,2,2,1])])}")
    # 516 too low
    print(f"Part one {part_one(parsed)}")
    print(len(parsed))
    from doctest import testmod
    testmod()

    code2fnc = fix_codes_2_fnc()

    with open("2018/16/part_two.txt", "r") as fd:
        parsed = [_parse2(line) for line in fd.readlines()]
        print(f"Part two {part_two(code2fnc, parsed)}")