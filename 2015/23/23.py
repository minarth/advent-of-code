def _parse(instr):
    cmd, mem, dist = None, None, None
    splitted = instr.strip().split(" ")
    cmd = splitted[0]
    mem = splitted[1]
    if len(splitted) == 3:
        dist = int(instr.strip().split(", ")[-1])
        mem = splitted[1][:-1]

    return cmd, mem, dist

def part(instructions, memory={"a": 0, "b": 0}):
    instr_pointer = 0
    
    while instr_pointer < len(instructions):
        cmd, mem, dist = _parse(instructions[instr_pointer])
        print(f"Executing line {instr_pointer} {instructions[instr_pointer]} with {cmd} {mem} {dist} having {memory}")
        if cmd == "hlf":
            memory[mem] //= 2
        elif cmd == "tpl":
            memory[mem] *= 3
        elif cmd == "inc":
            memory[mem] += 1
        elif cmd == "jmp":
            instr_pointer += int(mem)
            continue
        elif cmd == "jie":
            if memory[mem] % 2 == 0:
                instr_pointer += dist
                continue
        elif cmd == "jio":
            if memory[mem] == 1:
                instr_pointer += dist
                continue

        instr_pointer += 1


    return memory

test_data = ["inc a", "jio a, +2", "tpl a", "inc a"]
task_data = ["jio a, +16", "inc a", "inc a", "tpl a", "tpl a", "tpl a", "inc a", "inc a", "tpl a", "inc a", "inc a", "tpl a", "tpl a", "tpl a", "inc a", "jmp +23", "tpl a", "inc a", "inc a", "tpl a", "inc a", "inc a", "tpl a", "tpl a", "inc a", "inc a", "tpl a", "inc a", "tpl a", "inc a", "tpl a", "inc a", "inc a", "tpl a", "inc a", "tpl a", "tpl a", "inc a", "jio a, +8", "inc b", "jie a, +4", "tpl a", "inc a", "jmp +2", "hlf a", "jmp -7"]
