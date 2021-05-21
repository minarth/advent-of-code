def part_one(string):
    """
    >>> part_one(r"")
    (2, 0)

    >>> part_one(r"abc")
    (5, 3)

    >>> part_one(r'aaa\"aaa')
    (10, 7)

    >>> part_one(r"\x27")
    (6, 1)
    """
    for letter in string:
        pass #print(letter)
    return len(string.encode()) + 2, len(string)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print("01")
    
    print("02")
    
