import re
from copy import copy

def _parse(lines):
    regex = r"p=\<([\-0-9]+),([\-0-9]+),([\-0-9]+)\>, v=\<([\-0-9]+),([\-0-9]+),([\-0-9]+)\>, a=\<([\-0-9]+),([\-0-9]+),([\-0-9]+)\>"
    parsed = []
    for line in lines:
        parsed.append(tuple(map(int, re.findall(regex, line)[0])))
    return parsed


def _system_update(system, colisions=False):
    for k, particle in system.items():
        # update velocity
        particle["prev_v"] = particle["v"]

        particle["v"] = tuple(map(sum, zip(particle["v"], particle["a"])))
        # update position
        particle["p"] = tuple(map(sum, zip(particle["p"], particle["v"])))
        
        # previous distance
        particle["prev_d"] = particle["d"]
        
        # calculate distance
        particle["d"] = sum(map(abs, particle["p"]))

        particle["changes"] = (particle["prev_d"] > particle["d"]) or \
                            (sum(map(abs, particle["prev_v"])) > sum(map(abs, particle["v"])))
    
    if colisions:
        for k1, particle1 in system.items():
            for k2, particle2 in system.items():
                if k1 == k2: continue
                if particle1["p"] == particle2["p"]:
                    particle1["active"] = False
                    particle2["active"] = False

    # changed in memory, but this is nicer
    return system    


def part_one(particles):
    system = {}
    for i, p in enumerate(particles):
        system[i] = {
            "p": p[:3],
            "v": p[3:6],
            "a": p[6:],
            "d": sum(map(abs, p[:3])),
            "changes": True
        }

    # The 1000 is needed, because I am lazy to compare speeds from origin, where 401 is closer than others
    # but moving faster away than the solution particle
    i = 0
    while i < 1000 or any([p["changes"] for _, p in system.items()]):    
        system = _system_update(system)
        distances = sorted([(p["d"], k) for k, p in system.items()])
        i += 1
    return distances[0][1]

def part_two(particles):
    system = {}
    for i, p in enumerate(particles):
        system[i] = {
            "p": p[:3],
            "v": p[3:6],
            "a": p[6:],
            "d": sum(map(abs, p[:3])),
            "changes": True,
            "active": True,
        }

    i = 0
    prev_len = 1000
    active_system = {k: p for k, p in system.items() if p["active"]}
    while i < 100 and len(active_system) > 0:
        active_system = {k: p for k, p in system.items() if p["active"]}
        if prev_len > len(active_system):
            i = 0
            prev_len = len(active_system)
        active_system = _system_update(active_system, True)

        i += 1

    return prev_len


if __name__ == "__main__":
    with open("2017/20/input.txt", "r") as fd:
        particles = _parse(fd.readlines())
        print(f"Part one {part_one(particles)}")
        print(f"Part two {part_two(particles)}")