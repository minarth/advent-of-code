from collections import defaultdict
from functools import cmp_to_key

def process_input(filename):
    with open(filename, "r") as fd:
        data = fd.readlines()
    empty, rules, order = False, defaultdict(list), []
    for line in data:
        line = line.strip()
        if len(line) == 0: 
            empty = True
        elif not empty:
            k,v = tuple(map(int, line.split("|")))
            rules[k].append(v)
        else:
            order.append(tuple(map(int, line.split(","))))
    return rules, order 

def part_one(rules, order):
    counter = 0    
    incorrect = []
    for i, o in enumerate(order):
        finished = True
        for num in o:
            for rule in rules[num]:
                if rule in o and o.index(rule) < o.index(num): 
                    finished = False 
                    incorrect.append(i)
                    break
            if not finished:
                break
        else:
            counter += o[len(o)//2]
    return counter, incorrect

def _compare(rules):
    def fnc(x,y):
        if y in rules[x]: return -1
        if x in rules[y]: return 1
        return 0
    return fnc

def part_two(rules, order, incorrect):
    counter = 0
    key_fnc = _compare(rules)
    for i in incorrect:
        reordered = sorted(order[i], key=cmp_to_key(key_fnc))
        counter += reordered[len(reordered)//2]
    return counter
if __name__ == "__main__":
    r, o = process_input("test")
    s, i = part_one(r,o)
    print(f"part one {s}")
    print(f"part two {part_two(r,o,i)}")
    print("="*10)
    r, o = process_input("input")
    s,i = part_one(r,o)
    print(f"part one {s}")
    print(f"part two {part_two(r,o,i)}")
