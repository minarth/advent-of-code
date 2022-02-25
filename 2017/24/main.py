from copy import copy

def _parse(lines):
    return [tuple(map(int, l.strip().split("/"))) for l in lines]

def _combs(components, bridge):
    last = bridge[-1]
    bridges = [bridge]
    for c in components:
        if last[1] not in c: continue
        p1, p2 = c
        new_cpts = copy(components)
        new_cpts.remove(c)
        if last[1] == p1:
            bridges += _combs(new_cpts, bridge+[c])
        else:
            bridges += _combs(new_cpts, bridge+[(p2, p1)])
        
    return bridges

def part_one(components):
    starting_pieces = [c for c in components if 0 in c]
    bridges = []
    for start in starting_pieces:
        cmpts = copy(components)
        cmpts.remove(start)

        bridges += _combs(cmpts, [tuple(sorted(start))])
    
    longest = max(len(b) for b in bridges)

    sums = []
    for b in bridges:
        #_print(b)
        #print(sum([sum(c) for c in b]))
        if len(b) == longest:
            sums.append(sum([sum(c) for c in b]))
    return max(sums)

def _print(bridge):
    repr = []
    for p1, p2 in bridge:
        repr.append(f"{p1}/{p2}")
    print("--".join(repr))

if __name__ == "__main__":
    test_input = [(0, 2), (2,2), (2,3), (3,4), (3,5), (0,1), (10,1), (9,10)]
    part_one(test_input)

    with open("2017/24/input.txt", "r") as fd:
        components = _parse(fd.readlines())
        mx = part_one(components)
        print(f"Part one {mx}")