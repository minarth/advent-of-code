
def combo_val(operand, mem):
    assert 0 <= operand < 7
    if operand <= 3: return operand
    return mem[operand-4]


def step(pointer, program, mem, out):
    """
    If register C contains 9, the program 2,6 would set register B to 1.
    If register B contains 29, the program 1,7 would set register B to 26.
    If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354

    >>> step(0, [2,6], [0, 0, 9], [])
    (2, [2, 6], [0, 1, 9], [])
    >>> step(0, [1,7], [0, 29, 0], [])
    (2, [1, 7], [0, 26, 0], [])
    >>> step(0, [4,0], [0, 2024, 43690], [])
    (2, [4, 0], [0, 44354, 43690], [])
    """
    cmd, val = program[pointer], program[pointer+1]


    if cmd == 0:   # adv = division
        mem[0] = int(mem[0] / (2**combo_val(val,mem)))
    elif cmd == 1:
        mem[1] = mem[1] ^ val
    elif cmd == 2:
        mem[1] = combo_val(val,mem) % 8
    elif cmd == 3:
        if mem[0] != 0:
            pointer = val - 2
    elif cmd == 4:
        mem[1] = mem[1] ^ mem[2]
    elif cmd == 5:
        out.append(combo_val(val,mem) % 8)
    elif cmd == 6:
        mem[1] = int(mem[0] / (2**combo_val(val,mem)))
    elif cmd == 7:
        mem[2] = int(mem[0] / (2**combo_val(val,mem)))

    pointer += 2

    return pointer, program, mem, out


def program(program, mem, early_stopping=False):
    """
    f register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A
    
    >>> program([5,0,5,1,5,4], [10,0,0])
    ([0, 1, 2], [10, 0, 0])
    >>> program([0,1,5,4,3,0], [2024,0,0])
    ([4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0], [0, 0, 0])
    >>> program([0,1,5,4,3,0], [729,0,0])
    ([4, 6, 3, 5, 6, 3, 5, 2, 1, 0], [0, 0, 0])
    
    """
    p = 0  # pointer
    out = []
    OA = mem[0]
    while p < len(program):
        p, program, mem, out = step(p, program, mem, out)
        #print(p,mem,out)
        if early_stopping and out:
            for a,b in zip(out, program):
                if a != b: return out, mem
    return out, mem


def part_one(code, mem):
    out, mem = program(code, mem)
    return ",".join([str(o) for o in out])


def part_two(code, mem):
    out = []
    A = 6**16 #465405 #0
    test_mem = {(i+1): [] for i in range(16)}
    counter = 0
    max_found = 0
    addition = 1
    while out != code:
        new_mem = [A, 0, 0]
        out, mem = program(code, new_mem, True)
        if len(out) > 5:
            test_mem[len(out)].append(A)
            counter += 1
            if len(out) > max_found:
                max_found = len(out)
                print(f"Found: {max_found}")
                print(f"a len {bin(mem[0])}")
            if len(test_mem[len(out)]) >= 2:
                if addition != test_mem[len(out)][1]-test_mem[len(out)][0]:
                    print(f"new addition {addition}")
                addition = test_mem[len(out)][1]-test_mem[len(out)][0]
        A += addition
    return A-1

if __name__ == "__main__":
    import doctest
    doctest.testmod()


    from input import code, mem
    print(f"part one {part_one(code, mem)}")

    #print(f" test part two {part_two([0,3,5,4,3,0], [0,0,0])}")
    # too high 108116164712956
    #          16926659444736
    #          913781004797
    #          2442789362173
    print(f"part two {part_two(code,mem)}")

