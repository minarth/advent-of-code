from hashlib import md5

def part_one(door):
    """
    >>> part_one("abc")
    '18f47a30'
    """
    password = []
    index = 0
    while len(password) < 8:
        hash = md5((door + str(index)).encode()).hexdigest()
        if hash.startswith("00000"):
            password.append(hash[5])
        index += 1
    return "".join(password)

def part_two(door):
    """
    >>> part_two("abc")
    '05ace8e3'
    """
    password = [None] * 8
    index = 0
    while password.count(None) > 0:
        hash = md5((door + str(index)).encode()).hexdigest()
        if hash.startswith("00000") and hash[5].isnumeric():
            if 0 <= int(hash[5]) <= 7 and password[int(hash[5])] is None:
                password[int(hash[5])] = hash[6]
        index += 1
    return "".join(password)

if __name__ == "__main__":
    from doctest import testmod
    testmod()

    test_input = "uqwqemis"

    print(f"Part one {part_one(test_input)}")
    print(f"Part two {part_two(test_input)}")
    