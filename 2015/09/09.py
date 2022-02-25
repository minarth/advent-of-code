from itertools import permutations

instrs = ["London to Dublin = 464", "London to Belfast = 518", "Dublin to Belfast = 141"]


def _parse_input(input_s):
    s = input_s.strip().split()
    print(s)
    return s[0], s[2], int(s[-1])

def _all_paths(cities):
    paths = []
    perms = permutations(list(range(len(cities))))

    for perm in perms:
        path = []
        for city in perm:
            path.append(cities[city])
        paths.append(path)

    return paths

def part(input_s, comparison):
    distances = {}
    cities = set()
    for instr in input_s:
        a, b, dist = _parse_input(instr)
        distances[(a,b)] = dist
        distances[(b,a)] = dist
        cities.add(a)
        cities.add(b)

    cities = list(cities)

    paths = _all_paths(cities)
    target = None
    for path in paths:
        length = 0
        for start, end in zip(path[:-1], path[1:]):
            length += distances[(start, end)]

        if target: 
            target = comparison(target, length)
        else:
            target = length

    return target

