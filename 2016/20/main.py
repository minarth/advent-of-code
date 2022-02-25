from typing import Tuple


def _parse(line):
    """
    >>> _parse("0-9")
    (0, 9)

    >>> _parse("1231-4444")
    (1231, 4444)
    """
    f, t = line.strip().split("-")
    return int(f), int(t)

def _merge_input(blacklist):
    blacklist = sorted(blacklist)

    merged = [blacklist[0]]
    for l in blacklist[1:]:
        last_f, last_t = merged[-1]
        next_f, next_t = l

        if next_f <= (last_t+1):
            merged = merged[:-1] + [(last_f, next_t)]
        else:
            merged.append(l)
    
    return merged


def part_one(blacklist):    
    return blacklist[0][1]+1
    
def part_two(blacklist, UB=2**32):

    gaps = set()
    for _, t in blacklist:
        if t+1 >= UB:
            continue
        for f1, t1 in blacklist:
            if f1<=t+1<=t1:
                break
        else:
            gaps.add(t+1)
    return len(gaps)


if __name__ == "__main__":
    from doctest import testmod
    testmod()

    with open("2016/20/input.txt", "r") as f:
        test_input = [_parse(line) for line in f.readlines()]
        merged_input = _merge_input(test_input)

        print(f"Part one {part_one(merged_input)}")
        print(f"Part two {part_two(test_input)}")

        
            