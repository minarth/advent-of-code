from dataclasses import dataclass

def process(fn):
    with open(fn, "r") as fd:
        return list(map(int, fd.readlines()[0].strip().split()))


def part_one(data):
    memory = [data]  # will store every calc step along the way
    for i in range(25):
        new_line = []
        for element in memory[-1]:
            if element == 0:
                new_line.append(1)
            elif len(str(element)) % 2 == 0:
                s_e = str(element)
                l_e = len(s_e)
                new_line += [int(s_e[:l_e//2]), int(s_e[l_e//2:])]
            else:
                new_line.append(element*2024)
        memory.append(new_line)
    return len(memory[-1])   #, memory[-1]


@dataclass
class Node:
    depth: int
    value: int


def _expand(node ):
    next_elements = []
    if node.value == 0:
        next_elements = [1]
    elif len(str(node.value)) % 2 == 0:
        s_e = str(node.value)
        l_e = len(s_e)
        next_elements = [int(s_e[:l_e//2]), int(s_e[l_e//2:])]
    else:
        next_elements = [node.value*2024]

    return next_elements


def _dfs(node, memory):
    if node.depth == 75: 
        return 1
    if (node.value, node.depth) in memory: 
        return memory[(node.value, node.depth)]
    
    length = 0
    for n in _expand(node):
        v = _dfs(Node(depth=node.depth+1, value=n), memory)
        memory[(n, node.depth+1)] = v
        length += v
    return length 
        

def part_two(data):
    # instead of naive way, implement it "dynamic programming way"
    # never recalculate what already calculated
    
    # I will try to do it as acyclic graph
    baseline = [Node(depth=0, value=d) for d in data]
    memory = {}
    l = 0
    for n in baseline:
        l += _dfs(n, memory)
    return l

if __name__ == "__main__":
    data = process("test")
    print(f"part one {part_one(data)}")
    print(f"part two {part_two(data)}")

    data = process("input")
    print(f"part one {part_one(data)}")
    print(f"part two {part_two(data)}")


