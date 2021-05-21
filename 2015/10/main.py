def _look_and_say(seq):
    """
    >>> _look_and_say("1")
    '11'
    >>> _look_and_say("11")
    '21'
    >>> _look_and_say("21")
    '1211'
    >>> _look_and_say("1211")
    '111221'
    >>> _look_and_say("111221")
    '312211'
    """
    counter, number = 0, 0
    new_seq = ""
    for current in seq:
        #print(f"{current} {number} {counter} {new_seq}")
        if current != number and number != 0:
            new_seq += f"{counter}{number}"

        if current != number:
            counter = 1
            number = current
        else:
            counter += 1
        
    new_seq += f"{counter}{number}" 

    return new_seq


def part_one(seq, count):
    for _ in range(count):
        seq = _look_and_say(seq)

    return seq


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print(f"Part One: {len(part_one('1321131112', 40))}")

    print(f"Part Two: {len(part_one('1321131112', 50))}")
