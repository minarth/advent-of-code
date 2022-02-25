def part_one(sequence):
    """
    >>> part_one("ADVENT")
    'ADVENT'

    >>> part_one("A(1x5)BC")
    'ABBBBBC'

    >>> part_one("(3x3)XYZ")
    'XYZXYZXYZ'

    >>> part_one("A(2x2)BCD(2x2)EFG")
    'ABCBCDEFEFG'

    >>> part_one("(6x1)(1x3)A")
    '(1x3)A'

    >>> part_one("X(8x2)(3x3)ABCY")
    'X(3x3)ABC(3x3)ABCY'

    """
    position = 0
    decompressed = ""
    marker = None
    while position < len(sequence):

        if marker is not None:
            if sequence[position] == ")":
                # DO
                chars, repeats = marker[1:].split("x")
                decompressed += sequence[position+1:position+int(chars)+1]*int(repeats)
                marker = None
                position += int(chars) + 1

                continue
            else: marker += sequence[position]
        elif sequence[position] == "(":
            marker = "("
        else:
            decompressed += sequence[position]

        position += 1

    return decompressed


def part_two(sequence):
    """
    
    >>> part_two("(3x3)XYZ") 
    9
    >>> part_two("X(8x2)(3x3)ABCY") 
    20
    >>> part_two("(27x12)(20x12)(13x14)(7x10)(1x12)A")
    241920
    >>> part_two("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN")
    445

    """

    if "(" not in sequence:
        return len(sequence)

    length = 0

    position, marker = 0, None
    while position < len(sequence):

        if marker is not None:
            if sequence[position] == ")":
                # DO
                chars, repeats = marker[1:].split("x")
                length += part_two(sequence[position+1:position+int(chars)+1])*int(repeats)
                marker = None
                position += int(chars) + 1

                continue
            else: marker += sequence[position]
        elif sequence[position] == "(":
            marker = "("
        else:
            length += 1

        position += 1

    return length

if __name__ == '__main__':
    from doctest import testmod
    testmod()

    with open("input_2016_09.txt", "r") as f:
        test_input = f.readlines()[0].strip()
        print(f"Part one {len(part_one(test_input))}")
        print(f"Part two {part_two(test_input)}")
