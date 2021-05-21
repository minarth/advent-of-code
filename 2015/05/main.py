with open("05/input.txt", "r") as f:
    test_input = [s.strip() for s in f.readlines()]

VOWELS = "aeiou"
FORBIDDEN_STRINGS = ["ab", "cd", "pq", "xy"]

def _check_string_one(s):
    """
    >>> _check_string_one("ugknbfddgicrmopn")
    True

    >>> _check_string_one("aaa")
    True

    >>> _check_string_one("jchzalrnumimnmhp")
    False

    >>> _check_string_one("haegwjzuvuyypxyu")
    False

    >>> _check_string_one("dvszwmarrgswjxmb")
    False
    """
    for forbidden in FORBIDDEN_STRINGS:
        if forbidden in s:
            return False

    vowels_count = sum([s.count(vowel) for vowel in VOWELS])
    double_count = sum([u == v for u,v in zip(s[:-1], s[1:])])

    return vowels_count >= 3 and double_count >= 1

def _check_string_two(s):
    """
    >>> _check_string_two("qjhvhtzxzqqjkmpb")
    True
    >>> _check_string_two("xxyxx")
    True
    >>> _check_string_two("uurcxstgmygtbstg")
    False
    >>> _check_string_two("ieodomkazucvgmuy")
    False
    """
    double = 0
    for i in range(len(s)-1):
        suspect = s[i]+s[i+1]
        if suspect in s[i+2:]: double += 1

    repeated = sum([u == v for u,v in zip(s[:-2], s[2:])])

    return double >= 1 and repeated >= 1

def p(in_s, checker):
    return sum([checker(s) for s in in_s])


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print("01")
    print(p(test_input, _check_string_one))
    print("02")
    print(p(test_input, _check_string_two))