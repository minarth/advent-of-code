def _is_safe(triple):
    return triple not  in ("^^.", ".^^", "..^", "^..")


def _next_line(previous):
    """
    >>> _next_line("..^^.")
    '.^^^^'

    >>> _next_line(".^^^^")
    '^^..^'
    """
    next_line = "." if _is_safe("."+previous[:2]) else "^"
    for triple in zip(previous[:-2], previous[1:-1], previous[2:]):
        triple = "".join(triple)
        next_line += "." if _is_safe(triple) else "^"

    next_line += "." if _is_safe(previous[-2:] + ".") else "^"

    return next_line

def part_one(starting_row, length):
    trap_map = [starting_row]
    while len(trap_map) < length:
        trap_map.append(_next_line(trap_map[-1]))

    return "".join(trap_map).count(".")


if __name__ == '__main__':
    from doctest import testmod
    testmod()

    print(f"Test {part_one('.^^.^.^^^^', 10)}")

    print(f"Part one {part_one('^.^^^.^..^....^^....^^^^.^^.^...^^.^.^^.^^.^^..^.^...^.^..^.^^.^..^.....^^^.^.^^^..^^...^^^...^...^.', 40)}")
    print(f"Part two {part_one('^.^^^.^..^....^^....^^^^.^^.^...^^.^.^^.^^.^^..^.^...^.^..^.^^.^..^.....^^^.^.^^^..^^...^^^...^...^.', 400000)}")

