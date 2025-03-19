import scipy
import numpy as np
from scipy import optimize
from scipy.optimize import milp
from scipy import linalg
import re
import math


def process(fn):
    with open(fn, "r") as fd:
        ln = fd.readlines()
        machines = []
        for i in range(0, len(ln), 4):
            a = ln[i].strip()
            a_x = float((match := re.search(r"X\+(\d+)", a)) and match.group(1))
            a_y = float((match := re.search(r"Y\+(\d+)", a)) and match.group(1))
            b = ln[i+1].strip()
            b_x = float((match := re.search(r"X\+(\d+)", b)) and match.group(1))
            b_y = float((match := re.search(r"Y\+(\d+)", b)) and match.group(1))
            target = ln[i+2].strip()
            t_x = float((m := re.search(r"X=(\d+)", target)) and m.group(1))
            t_y = float((m := re.search(r"Y=(\d+)", target)) and m.group(1))
            machines.append({"a": [a_x, a_y], "b": [b_x, b_y], "prize": [t_x, t_y]})
    return machines


def _optimize_machine(a, b, prize, bounds=100):
    xs = np.array([a[0], b[0]])
    ys = np.array([a[1], b[1]])
    values = np.array([3, 1])
    bounds = optimize.Bounds(0, bounds)  # 0 <= x_i <= 1
    integrality = np.full_like(values, True)  # x_i are integers
    constraints = optimize.LinearConstraint(A=[xs, ys], lb=prize, ub=prize)
    res = milp(c=values, constraints=constraints,
                    integrality=integrality, bounds=bounds)
    if res.success: 
        #print("-",a,b,prize, int(res.fun), res.x)
        return int(res.fun)
        
    return 0 


def part_one(machines):
    return sum([_optimize_machine(**m) for m in machines])


def cramer(a,b,prize):
    p = prize
    x = (p[0]*b[1] - b[0]*p[1]) / (a[0]*b[1] - b[0]*a[1])
    y = (a[0]*p[1] - a[1]*p[0]) / (a[0]*b[1] - b[0]*a[1])

    if x == int(x) and y == int(y):
        return 3*x+y
    return 0

def part_two(machines):
    result = 0
    for m in machines:
        m["prize"][0] += 10000000000000
        m["prize"][1] += 10000000000000
        result += cramer(**m)
    return result

if __name__ == "__main__":
    machines = process("test")
    print(f"part one {part_one(machines)}")
    print(f"part two {part_two(machines)}")
    machines = process("input")
    print(f"part one {part_one(machines)}")
    print(f"part two {part_two(machines)}")
