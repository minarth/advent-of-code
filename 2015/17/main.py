def part_one(remaining_value, remaining_jugs, used_jugs=()):
    """
    >>> part_one(25, [20, 15, 10, 5, 5])
    [(20, 5), (20, 5), (15, 10), (15, 5, 5)]
    """
    if remaining_value == 0:
        return [used_jugs]
    if remaining_value < 0:
        return []
    if sum(remaining_jugs) < remaining_value:
        return []

    value = remaining_jugs[0]
    return part_one(remaining_value-value, remaining_jugs[1:], used_jugs + (value, )) \
        + part_one(remaining_value, remaining_jugs[1:], used_jugs)


def part_two(combinations):
    """
    >>> part_two([(20, 5), (20, 5), (15, 10), (15, 5, 5)])
    [(20, 5), (20, 5), (15, 10)]
    """
    minimum = min([len(c) for c in combinations])

    return [c for c in combinations if len(c) == minimum]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    parsed_input = [33,14,18,20,45,35,16,35,1,13,18,13,50,44,48,6,24,41,30,42]
    p_o = part_one(150, parsed_input)
    print(f"Part one: {len(p_o)}")
    print(f"Part two: {len(part_two(p_o))}")
