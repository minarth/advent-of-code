from copy import deepcopy
def _get_value(x, registers):
    try:
        return int(x)
    except:
        return registers[x]

def _parse(instruction):
    return instruction.strip().split(" ")

def _is_multiplication(instructions):
    if len(instructions) != 6: return False

    cmds = [c[0] for c in instructions]
    muls = [["cpy", "inc", "dec", "jnz", "dec", "jnz"], 
            ["cpy", "dec", "inc", "jnz", "dec", "jnz"]]

    if cmds not in muls: return False
    return instructions[3][-1] == "-2" and instructions[5][-1] == "-5"

def _multiply(instructions, registers):


    cmds = [c[0] for c in instructions]
    a = instructions[0][1]
    b = instructions[-1][1]

    if cmds[1] == "inc":
        target = instructions[1][1]
    elif cmds[2] == "inc":
        target = instructions[2][1]

    registers[target] += _get_value(a, registers) * _get_value(b, registers)
    registers[instructions[0][-1]] = 0   # set 0 the temp var
    registers[b] = 0

    return registers


def _run_code(instructions, registers={"a": 0, "b": 0, "c": 0, "d": 0}):
    pointer = 0
    while pointer < len(instructions):
        instruction = instructions[pointer]
        cmd, x = instruction[0], instruction[1]
            
        #print(f"{pointer} {instruction} {x} {_get_value(x, registers)}, {registers}")
        if _is_multiplication(instructions[pointer:pointer+6]):
            registers = _multiply(instructions[pointer:pointer+6], registers)
            pointer += 6
            continue
        elif cmd == "cpy":
            y = instruction[2]
            if type(y) != int: 
                registers[y] = _get_value(x, registers)    
        elif cmd == "inc":
            registers[x] += 1
        elif cmd == "dec":
            registers[x] -= 1
        elif cmd == "jnz":
            y = _get_value(instruction[2], registers)
            if _get_value(x, registers) != 0:
                pointer += y
                continue
        elif cmd == "tgl":
            x = _get_value(x, registers)
            if (x+pointer) < len(instructions):
                changed = instructions[pointer+x]
                if len(changed) == 2:
                    c1, val = changed
                    c1 = "dec" if c1 == "inc" else "inc"
                    toggled = [c1, val]
                elif len(changed) == 3:
                    c1, val1, val2 = changed
                    c1 = "cpy" if c1 == "jnz" else "jnz"
                    toggled = [c1, val1, val2]
                instructions[pointer+x] = toggled

        pointer += 1

    return registers

if __name__ == '__main__':
    
    test_input = """cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a"""
    test_input = [_parse(ti) for ti in test_input.split("\n")]
    print(f"Test {_run_code(test_input)}")
    with open("input_2016_23.txt", "r") as f:
         inp = [_parse(line) for line in f.readlines()]
         print(f"Part one {_run_code(deepcopy(inp), {'a': 7, 'b': 0, 'c': 1, 'd': 0})}")
         # It's too late, I'll just wait
         print(f"Part two {_run_code(inp, {'a': 12, 'b': 0, 'c': 0, 'd': 0})}")