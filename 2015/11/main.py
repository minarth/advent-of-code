def _increment(password):
    password.reverse()

    overhead = 1
    for position in range(len(password)):
        password[position] += overhead
        overhead = 0
        if password[position] > 25:
            password[position] = 0
            overhead = 1

    password.reverse()
    return password

def _is_valid(password):
    # three straight letters
    found = False
    for a, b, c in zip(password[:-2], password[1:-1], password[2:]):
        if a+2 == b+1 == c: found = True
    if not found: return False

    # no i, o, l
    forbidden = [ord("i")-ord("a"), ord("o")-ord("a"), ord("l")-ord("a")]
    for f in forbidden:
        if f in password:
            return False

    # two non-overlapping pairs
    overlaps = [0 for _ in range(len(password))]
    for i, a,b in zip(range(len(password)-1), password[:-1], password[1:]):
        if a == b:
            overlaps[i], overlaps[i+1] = 1, 1

    return sum(overlaps) >= 4

def part_one(password):
    zero = ord("a")
    numerize = [ord(p) - zero for p in password]
    numerize = _increment(numerize)
    while not _is_valid(numerize):
        numerize = _increment(numerize)
    stringify = "".join([chr(p + zero) for p in numerize])
    return stringify


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print(f"Part One: {part_one('cqjxjnds')}")

    print(f"Part Two: {part_one(part_one('cqjxjnds'))}")
