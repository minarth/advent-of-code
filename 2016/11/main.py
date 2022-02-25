from itertools import combinations
from copy import deepcopy
from math import ceil
from heapq import heappush, heappop
from typing import DefaultDict
from collections import defaultdict

GEN = "generator"
CHIP = "chip"
lab_objects = {
    "po_g": {"t": GEN, "material": "polonium"},
    "po_c": {"t": CHIP, "material": "polonium"},
    "tm_g": {"t": GEN, "material": "thuilium"},
    "tm_c": {"t": CHIP, "material": "thuilium"},
    "pm_g": {"t": GEN, "material": "promethium"},
    "pm_c": {"t": CHIP, "material": "promethium"},
    "ru_g": {"t": GEN, "material": "ruthenium"},
    "ru_c": {"t": CHIP, "material": "ruthenium"},
    "co_g": {"t": GEN, "material": "cobalt"},
    "co_c": {"t": CHIP, "material": "cobalt"},

    "hg_g": {"t": GEN, "material": "hydrogen"},
    "hg_c": {"t": CHIP, "material": "hydrogen"},
    "li_g": {"t": GEN, "material": "lithium"},
    "li_c": {"t": CHIP, "material": "lithium"},

    "el_g": {"t": GEN, "material": "elerium"},
    "el_c": {"t": CHIP, "material": "elerium"},
    "di_g": {"t": GEN, "material": "dilithium"},
    "di_c": {"t": CHIP, "material": "dilithium"},
}

test_lab = [["hg_c", "li_c"], ["hg_g"], ["li_g"], []]
ELEMENTS = sum([len(floor) for floor in test_lab])

def _hash_lab(lab, floor_num):
    hash_lab = [[], [], [], []]
    for h_floor, floor in zip(hash_lab, lab):
        for element in floor:
            if "_c" in element:
                opposite = element.replace("_c", "_g")
                for i, gen_floor in enumerate(lab):
                    if opposite in gen_floor:
                        h_floor.append(i)
                
    return str([sorted(floor) for floor in hash_lab]) + " " + str(floor_num)
                    

def _print(lab):
    print("-"*10)
    print("\n".join([" . ".join([str(4-i)] + floor) for i, floor in enumerate(reversed(lab))]))
    print("-"*10)

def _finish(lab):
    return sum([len(floor) for floor in lab[:-1]]) == 0

def _fried(lab):
    """
    >>> _fried([["po_c", "tm_c"], ["po_g"], ["tm_g"], []])
    False

    >>> _fried([["po_c"], ["tm_c", "po_g"], ["tm_g"], []])
    True

    >>> _fried([["tm_c"], ["po_c", "po_g"], ["tm_g"], []])
    False

    >>> _fried([[], ["tm_c", "tm_g", "po_c", "po_g"], [], []])
    False

    """
    for floor in lab:
        if len(floor) == 0: continue
        gens = [obj for obj in floor if lab_objects[obj]["t"] == GEN]
        chips = [obj for obj in floor if lab_objects[obj]["t"] == CHIP]

        if len(gens) == 0 or len(chips) == 0: continue

        unpaired_chips = [chip for chip in chips if chip.split("_")[0]+"_g" not in gens]

        if len(unpaired_chips) > 0 and len(gens) > 0: return True
    
    return False

def _evaluate_lab(lab):
    steps_estimate = 0
    for i, floor in enumerate(lab[:-1]):
        steps_estimate += (len(lab)-1-i)*ceil(len(floor)/2)

    return steps_estimate

def _sort_lab(lab):
    return [sorted(floor) for floor in lab]

def _possible_moves(lab, elevator_floor, path_length):
    all_possible_takes = list(combinations(lab[elevator_floor], 2)) + [(el,) for el in lab[elevator_floor]]
    possible_floors = [max(0, elevator_floor-1), min(len(lab)-1, elevator_floor+1)]
    if elevator_floor in possible_floors:
        possible_floors.remove(elevator_floor)
    if len(lab[0]) == 0:
        if 0 in possible_floors:
            possible_floors.remove(0)

    labs = []
    for floor in possible_floors:
        moved = set()
        for change in all_possible_takes:
            current_lab = deepcopy(lab)
            for c in change:
                current_lab[elevator_floor].remove(c)
            current_lab[floor] += change
            if not _fried(current_lab):
                labs.append((_evaluate_lab(current_lab)+path_length, _sort_lab(current_lab), floor, path_length))
    
    return labs

def a_star(starting_lab, floor):
    explored = set()
    queue = [(_evaluate_lab(starting_lab), _sort_lab(starting_lab), floor, 0)]
    discovered_heuristics = set()
    while queue:
        prio, lab, floor, path = heappop(queue)
        hashed = _hash_lab(lab, floor)
        if (prio-path) not in discovered_heuristics:
            discovered_heuristics.add(prio-path)
        
        if _finish(lab): 
            return path

        for move in _possible_moves(lab, floor, path+1):
            if _hash_lab(move[1], move[2]) in explored:
                continue
            if move not in queue: 
                heappush(queue, move)
        explored.add(hashed)

    return None

if __name__ == "__main__":
    from doctest import testmod
    testmod()

    my_input_lab = [["po_g", "tm_g", "tm_c", "pm_g", "ru_g", "ru_c", "co_g", "co_c"], ["po_c", "pm_c"], [], []]

    print(f"Test one {a_star(test_lab, 0)}")
    # Takes about 5 seconds
    print(f"Part one {a_star(my_input_lab, 0)}")

    my_input_lab_two = [["el_g", "el_c", "di_g", "di_c","po_g", "tm_g", "tm_c", "pm_g", "ru_g", "ru_c", "co_g", "co_c"], ["po_c", "pm_c"], [], []]
    # Takes about 2 minutes
    print(f"Part one {a_star(my_input_lab_two, 0)}")