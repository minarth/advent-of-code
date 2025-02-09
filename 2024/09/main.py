from dataclasses import dataclass
from typing import Any
def process(fn):
    with open(fn, "r") as fd:
        files, empty = [], []
        for i,d in enumerate(fd.readlines()[0].strip()):
            if i % 2: empty.append(int(d))
            else: files.append(int(d))
        return files, empty


def part_one(files, empty):
    # there will be no empty spaces at the end
    #   treating end file as (ID, space it takes)
    final = [(0, files[0])]
    file_start_id, file_end_id = 1, len(files)-1
    files = files[1:]
    # i take as much of end files as possible to fill in the current empty
    while empty :
        free_space = empty[0]
        while free_space >= files[-1]:
            final.append((file_end_id, files[-1]))
            free_space -= files[-1] 
            file_end_id -= 1
            files = files[:-1]
            empty = empty[:-1]  # no need to resolve empty spaces at the end
        if free_space:
            final.append((file_end_id, free_space))
            size = files.pop()-free_space
            files.append(size)
        final.append((file_start_id, files[0]))
        file_start_id += 1
        files = files[1:]
        empty = empty[1:]
    idx, counter = 0, 0
    for e, c in final:
        for _ in range(c):
            counter += idx*e
            idx += 1
    return counter
    

def print_mem(memory):
    mem_s = ""
    for (idx, val, _) in memory:
        for _ in range(val):
            mem_s += str(idx) if idx >= 0 else "."
    print(mem_s)

def part_two(files, empties):
    memory = []
    for idx, (f,e) in enumerate(zip(files, empties + [0])):
        memory.append((idx, f, False))
        memory.append((-1, e, True))
    # we r going for O(n^2) ?
    pointer = len(memory)-1
    while pointer >= 0:
        (idx, value, moved) = memory[pointer]
        if idx == -1 or moved: 
            pointer -= 1  # idx==-1 is redundant, just to be sure
            continue
        found = False
        for search_pointer in range(pointer):
            (s_idx, s_value, s_moved) = memory[search_pointer]
            if s_idx == -1 and s_value >= value:
                found = True
                memory = memory[:pointer]+[(-1, value, True)]+memory[pointer+1:]
                memory = memory[:search_pointer] + [(idx, value, True), (-1, s_value-value, s_moved)] + memory[search_pointer+1:]
                break
        if not found:
            memory[pointer] = (idx, value, True)
        pointer = len(memory)-1
    
    result, position = 0, 0
    for (idx, value, _) in memory:
        for _ in range(value):
            if idx > 0: result += position*idx
            position += 1
    
    return result


if __name__ == "__main__":
    f,e = process("input")
    print(part_one(f,e))
    print(part_two(f,e))
    
