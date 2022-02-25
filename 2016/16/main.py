def _randomize(a):
    """
    >>> _randomize("1")
    '100'

    >>> _randomize("0")
    '001'
    
    >>> _randomize("11111")
    '11111000000'

    >>> _randomize("111100001010")
    '1111000010100101011110000'
    """
    b = ["0" if i == "1" else "1" for i in reversed(a)]
    b = "".join(b)
    return f"{a}0{b}"


def _checksum(a):
    """
    >>> _checksum("110010110100")
    '100'
    """
    check = a
    while len(check) % 2 == 0:
        new_check = ""
        for i, j in zip(check[:-1:2], check[1::2]):
            if i == j:
                new_check += "1"
            else:
                new_check += "0"
        check = new_check
    
    return check


def part_one(initial, length):
    """
    >>> part_one("10000", 20)
    '01100'
    """
    curve = initial
    while len(curve) <= length:
        curve = _randomize(curve)

    return _checksum(curve[:length])


if __name__ == "__main__":
    from doctest import testmod
    testmod()

    print(f"Part one {part_one('00101000101111010', 272)}")
    print(f"Part two {part_one('00101000101111010', 35651584)}")
