import json

def _parse(string):
    """
    >>> _parse('Alice would gain 54 happiness units by sitting next to Bob.')
    ('Alice', 'Bob', 54)
    >>> _parse('Carol would lose 62 happiness units by sitting next to Alice.')
    ('Carol', 'Alice', -62)
    >>> _parse('David would lose 7 happiness units by sitting next to Bob.')
    ('David', 'Bob', -7)
    """
    splitted = string.strip().split(" ")
    return splitted[0], splitted[-1].replace(".", ""), \
        (1 if splitted[2] == "gain" else -1) * int(splitted[3])

def _all_combs(people, combs):
    if len(people) == 0: return combs

    downstream_combs = []
    for i, p in enumerate(people):
        downstream_combs += _all_combs(people[:i] + people[i+1:], [c + (p, ) for c in combs])
    
    return downstream_combs

def _evaluate_arrangement(arr, potential):
    start, end = arr[0], arr[-1]
    hapiness = potential[(start, end)] + potential[(end, start)]

    for s, e in zip(arr[:-1], arr[1:]):
        hapiness += potential[(s, e)] + potential[(e, s)]
    
    return hapiness

def part_one(data):
    potential = [_parse(d) for d in data]
    potential = {(f,t): v for f,t,v in potential}

    people = list(set([p[0] for p in potential]))

    best_hapiness = None
    for arr in _all_combs(people[1:], [(people[0],)]):
        happiness = _evaluate_arrangement(arr, potential)
        if best_hapiness is None: 
            best_hapiness = happiness
        best_hapiness = max(best_hapiness, happiness)
    
    return best_hapiness

def part_two(data):
    potential = [_parse(d) for d in data]
    potential = {(f,t): v for f,t,v in potential}

    people = list(set([p[0] for p in potential]))

    for p in people:
        potential[("ME", p)] = 0
        potential[(p, "ME")] = 0
    
    people += ["ME"]

    best_hapiness = None
    for arr in _all_combs(people[1:], [(people[0],)]):
        happiness = _evaluate_arrangement(arr, potential)
        if best_hapiness is None: 
            best_hapiness = happiness
        best_hapiness = max(best_hapiness, happiness)
    
    return best_hapiness


if __name__ == "__main__":
    import doctest
    #doctest.testmod()
    example_data = """Alice would gain 54 happiness units by sitting next to Bob.
    Alice would lose 79 happiness units by sitting next to Carol.
    Alice would lose 2 happiness units by sitting next to David.
    Bob would gain 83 happiness units by sitting next to Alice.
    Bob would lose 7 happiness units by sitting next to Carol.
    Bob would lose 63 happiness units by sitting next to David.
    Carol would lose 62 happiness units by sitting next to Alice.
    Carol would gain 60 happiness units by sitting next to Bob.
    Carol would gain 55 happiness units by sitting next to David.
    David would gain 46 happiness units by sitting next to Alice.
    David would lose 7 happiness units by sitting next to Bob.
    David would gain 41 happiness units by sitting next to Carol.""".split("\n")

    print(f"example data {part_one(example_data)}")

    with open("2015/13/input.txt", "r") as f:
        test_input = f.readlines()
        print(f"Part one: {part_one(test_input)}")
        print(f"Part two: {part_two(test_input)}")
