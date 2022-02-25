from copy import copy, deepcopy
from typing import final

from math import ceil, sqrt

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
    ip = int(lines[0].strip().split(" ")[-1])
    program: list = []
    for l in lines[1:]:
        l = l.strip().split(" ")
        program.append((l[0],) + tuple(map(int, l[1:])))
    
    return ip, program


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


def part_one(ip_pointer, program):
    ip = 0
    memory = [0]*6
    while ip < len(program):
        memory[ip_pointer] = ip
        line = program[memory[ip_pointer]]
        memory = exec(line[0], line[1:], memory)
        ip = memory[ip_pointer]
        ip += 1
    
    return memory[0]


def get_divisor(ip_pointer, program):
    ip = 0
    memory = [1,0,0,0,0,0]
    runs = 0
    while ip < len(program):
        memory[ip_pointer] = ip
        line = program[memory[ip_pointer]]
        memory = exec(line[0], line[1:], memory)        
        ip = memory[ip_pointer]
        ip += 1
        runs += 1
        
        if runs > 50: break

    return memory[2]

def part_two(number):
    divisors = set()
    for i in range(1, ceil(sqrt(number))+1):      
        if number % i == 0:            
            divisors.add(i)
            divisors.add(number // i)
    return sum(divisors)


if __name__ == "__main__":
    with open("2018/19/example.txt", "r") as fd:
        ip_pointer, program = _parse(fd.readlines())
        print(f"Example part one {part_one(ip_pointer, program)}")
        
    with open("2018/19/input.txt", "r") as fd:
        ip_pointer, program = _parse(fd.readlines())
        print(f"Part one {part_one(ip_pointer, program)}")
        # After looking at the code, I found that it is basically sum of all divisors
        print(f"Part two {part_two(get_divisor(ip_pointer, program))}")