from hashlib import md5

UP = ((-1, 0), "U")
DOWN = ((1, 0), "D")
LEFT = ((0, -1), "L")
RIGHT = ((0, 1), "R")
DIRS = (UP, DOWN, LEFT, RIGHT)

def _man_dist(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)

def _opened_doors(position, path, target, passcode):
    """
    Too many functionalities per function:
     - get new position coordinates
     - check hashes a.k.a. locked doors
     - check if not over/under flowing the grid
     - sort next moves by heuristics
    """
    hash = md5((passcode + "".join(path)).encode()).hexdigest()
    opened_doors = [d for h, d in zip(hash[:4], DIRS) if h in "bcdef"]
    possible_doors = []
    for door in opened_doors:
        x1, y1 = position
        x2, y2 = door[0]
        if 0 <= x1 + x2 <= 3 and 0 <= y1 + y2 <= 3:
            new_position = (x1+x2,y1+y2)
            possible_doors.append((_man_dist(*new_position, *target), 
                door, new_position))
    if possible_doors:
        return sorted(possible_doors)
    
    return []


def _shortest_path(position, path, target, passcode, best_val, cut_longer=True):
    best = best_val["val"]
    if position == target:
        return [(len(path), path)]

    if cut_longer and best is not None and len(path) > best:
        return []
    
    #print(position, path)

    next_possitions = _opened_doors(position, path, target, passcode)
    outcomes = []

    for (_, door, new_pos) in next_possitions:
        next_paths = _shortest_path(new_pos, path+door[1], target, passcode, {"val": best}, cut_longer)
        if next_paths:
            next_path = next_paths[0]
            outcomes += next_paths
            if best is None:
                best, _ = next_path
            best = min(next_path[0], best)
    
    if outcomes:
        return sorted(outcomes)

    return outcomes


def part_one(passcode):
    """
    >>> part_one("ihgpwlah")
    6

    >>> part_one("kglvqrro")
    12

    >>> part_one("ulqzkmiv")
    30
    """
    paths = _shortest_path((0,0), "", (3,3), passcode, {"val": None})
    return paths[0][0]

def part_two(passcode):
    """
    >>> part_two("ihgpwlah")
    370

    >>> part_two("kglvqrro")
    492

    >>> part_two("ulqzkmiv")
    830
    """
    paths = _shortest_path((0,0), "", (3,3), passcode, {"val": None}, False)
    return paths[-1][0]

if __name__ == "__main__":
    from doctest import testmod
    testmod()
    print(f"Part One {part_one('pvhmgsws')}")
    print(f"Part two {part_two('pvhmgsws')}")
