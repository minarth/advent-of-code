from heapq import heappop, heappush
import numpy as np
from scipy import optimize as opt


def process(fn):
    with open(fn, "r") as fd:
        parsed = []
        for line in fd.readlines():
            els = line.strip().split(" ")
            indicator = "".join(["1" if l=="#" else "0" for i,l in enumerate(els[0][1:-1])])
            buttons = [tuple(map(int, l[1:-1].split(","))) for l in els[1:-1]]
            joltage = tuple(map(int, els[-1][1:-1].split(",")))
            parsed.append({"indicator": indicator, "buttons": buttons, "joltage": joltage})
        return parsed


def _apply(state, btn):
    return "".join([s if i not in btn else "1" if s=="0" else "0" for i, s in enumerate(state)])


def _find_one(ind, btns):
    explored = set()  # visited states
    q = []
    start = "".join(["0" for _ in ind])
    heappush(q, (0, start))
    while q:
        d, state= heappop(q)
        if state == ind: 
            return d 
        if state in explored: continue
        explored.add(state)
        for b in btns:
            new_state = _apply(state, b)
            if new_state not in explored:
                heappush(q, (d+1, new_state))
    return best


def part_one(data):
    result = 0
    for machine in data:
        r = _find_one(machine["indicator"], machine["buttons"])
        result += r
    return result


def _optimize(jolt, btns):
    A = np.zeros([len(jolt), len(btns)])    
    for i,b in enumerate(btns):
        for j in b:
            A[j,i] = 1.
    c = np.ones([len(btns)]) 
    constr = opt.LinearConstraint(A=A, lb=np.array(jolt), ub=np.array(jolt))
    integrality = np.full_like(c, True)  # x_i are integers
    r = opt.milp(c, integrality=integrality, constraints=constr)
    if r.success:
        return int(np.round(np.sum(r.x)))
    
    return None


def part_two(data):
    result = 0
    for machine in data:
        result += _optimize(machine["joltage"], machine["buttons"])
    return result


if __name__ == "__main__":
    data = process("test")
    print(f"part one {part_one(data)}")
    print(f"part two {part_two(data)}")
    print("="*10)
    data = process("input")
    print(f"part one {part_one(data)}")
    print(f"part two {part_two(data)}")
     
