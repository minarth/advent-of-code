import hashlib

test_input = "yzbqklnj"

def p_one(in_s):
    """
    >>> p_one("abcdef")
    609043
    >>> p_one("pqrstuv")
    1048970
    
    """

    result = ""
    number = 0

    while not result.startswith("00000"):
        number += 1
        test_string = in_s + str(number)
        result = hashlib.md5(test_string.encode()).hexdigest()

    return number

def p_two(in_s):
    result = ""
    number = 0

    while not result.startswith("000000"):
        number += 1
        test_string = in_s + str(number)
        result = hashlib.md5(test_string.encode()).hexdigest()

    return number


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print("1")
    print(p_one(test_input))
    print("2")
    print(p_two(test_input))