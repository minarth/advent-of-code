def _get_value(x, registers):
    if x.isnumeric():
        return int(x)
    return registers[x]

def _parse(instruction):
    return instruction.strip().split(" ")

def _get_clock(length):
    return "".join([str(i%2) for i in range(length)])


def _run_code(instructions, registers={"a": 0, "b": 0, "c": 0, "d": 0}, test_l=1000):
    # just empirical test, no real proof

    pointer = 0
    output = ""
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
        elif cmd == "out":
            output += str(_get_value(x, registers))
            if output != _get_clock(len(output)):
                #print(output, _get_clock(len(output)))
                return False

        if len(output) == test_l: break

        pointer += 1

    return output == _get_clock(len(output))

if __name__ == '__main__':
    with open("input_2016_25.txt", "r") as f:
        inp = [_parse(line) for line in f.readlines()]
        for a in range(10000):
            if _run_code(inp, {'a': a, 'b': 0, 'c': 0, 'd': 0}):
                
                print(f"  --------  Found {a}")
            if a % 200 == 0: 
                print(f"Testing {a}")
        #print(f"Part two {_run_code(inp, {'a': 0, 'b': 0, 'c': 1, 'd': 0})}")