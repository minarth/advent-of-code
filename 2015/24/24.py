from functools import reduce
from itertools import combinations

def _entangle(group):
    return reduce(lambda x,y: x*y, group, 1)

def _find_groups(elements, divisor):
    best_entanglement = _entangle(elements[-8:])
    third = sum(elements) // divisor
    for i in range(len(elements)):
        for group in combinations(elements, i):
            if sum(group) == third:
                best_entanglement = min(best_entanglement, _entangle(group))
        if best_entanglement != _entangle(elements[-8:]):
            return best_entanglement

def part_one(elements):
    """
    >>> part_one([11, 10, 9, 8, 7, 5, 4, 3, 2, 1])
    99
    """
    return _find_groups(elements, 3)

def part_two(elements):
    return _find_groups(elements, 4)


if __name__ == '__main__':
    test_input = [1, 3, 5, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    print(f"Part one {part_one(test_input)}")
    print(f"Part two {part_two(test_input)}")