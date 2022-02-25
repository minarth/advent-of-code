def _get_value(x, registers):
    if x.isnumeric():
        return int(x)
    return registers[x]

def _parse(instruction):
    return instruction.strip().split(" ")

def _run_code(instructions, registers={"a": 0, "b": 0, "c": 0, "d": 0}):
    pointer = 0
    while pointer < len(instructions):
        instruction = instructions[pointer]
        cmd, x = instruction[0], instruction[1]
        if cmd == "cpy":
            y = instruction[2]
            registers[y] = _get_value(x, registers)    
        elif cmd == "inc":
            registers[x] += 1
        elif cmd == "dec":
            registers[x] -= 1
        elif cmd == "jnz":
            y = int(instruction[2])
            if _get_value(x, registers) != 0:
                pointer += y
                continue

        pointer += 1

    return registers

if __name__ == '__main__':
    
    test_input = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""
    test_input = [_parse(ti) for ti in test_input.split("\n")]
    print(f"Test {_run_code(test_input)}")
    with open("input_2016_12.txt", "r") as f:
        inp = [_parse(line) for line in f.readlines()]
        print(f"Part one {_run_code(inp)}")
        print(f"Part two {_run_code(inp, {'a': 0, 'b': 0, 'c': 1, 'd': 0})}")