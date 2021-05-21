with open("2015/07/input.txt", "r") as f:
    test_input = [s.strip() for s in f.readlines()]

INSTRUCTIONS = ["AND", "OR", "NOT", "LSHIFT", "RSHIFT"]

def _parse_input(command):
    """
    >>> _parse_input("123 -> x")
    (None, 123, None, 'x')
    >>> _parse_input("456 -> y")
    (None, 456, None, 'y')
    >>> _parse_input("x AND y -> d")
    ('AND', 'x', 'y', 'd')
    >>> _parse_input("x OR y -> e")
    ('OR', 'x', 'y', 'e')
    >>> _parse_input("x LSHIFT 2 -> f")
    ('LSHIFT', 'x', 2, 'f')
    >>> _parse_input("y RSHIFT 2 -> g")
    ('RSHIFT', 'y', 2, 'g')
    >>> _parse_input("NOT x -> h")
    ('NOT', 'x', None, 'h')
    >>> _parse_input("NOT y -> i")
    ('NOT', 'y', None, 'i')
    """

    cmd, first, second, target = None, None, None, None
    parsed = command.split()
    if parsed[0] == "NOT":
        cmd = "NOT"
        try:
            first = int(parsed[1])
        except:
            first = parsed[1]
    elif len(parsed) == 3:
        try:
            first = int(parsed[0])
        except:
            first = parsed[0]
    else:
        cmd = parsed[1]
        try:
            first = int(parsed[0])
        except:
            first = parsed[0]
        try:
            second = int(parsed[2])
        except:
            second = parsed[2]
    target = parsed[-1]
    
    return cmd, first, second, target

def _eval(first, second, cmd):
    """
    >>> _eval(123, None, None)
    123

    >>> _eval(156, 52, "AND")
    20

    >>> _eval(156, 52, "OR")
    188

    >>> _eval(156, None, "NOT")
    65379

    >>> _eval(39, 2, "LSHIFT")
    156

    >>> _eval(157, 1, "RSHIFT")
    78
    """

    if cmd is None: return first
    elif cmd == "AND": return first & second
    elif cmd == "OR": return first | second
    elif cmd == "NOT": return (~first) & 65535
    elif cmd == "LSHIFT": return first << second
    elif cmd == "RSHIFT": return first >> second

    return None

def p(instructs, circuit={}):
    unresolved = []
    for inst in instructs:
        unresolved.append(_parse_input(inst))
    
    # I am not proud of this :)
    tmp_unresolved = []
    while len(unresolved) > 0:        
        for inst in unresolved:
            cmd, first, second, target = inst
            if type(first) == str and first not in circuit:
                tmp_unresolved.append(inst)
                continue
            first_val = first if type(first) == int else circuit[first]
            if second:
                if type(second) == str and second not in circuit:
                    tmp_unresolved.append(inst)
                    continue

                second_val = second if type(second) == int else circuit[second]
            else: second_val = None
            if target not in circuit:
                # The if resolves 
                circuit[target] = _eval(first_val, second_val, cmd)
        unresolved = tmp_unresolved    
        tmp_unresolved = []
  
    return circuit

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    t = """123 -> x
        456 -> y
        x AND y -> d
        x OR y -> e
        x LSHIFT 2 -> f
        y RSHIFT 2 -> g
        NOT x -> h
        NOT y -> i"""
    #p(t.split("\n"))
    print("01")
    part_one = p(test_input)
    print(p(test_input)["a"])
    print("02")
    print(p(test_input, {"b": part_one["a"]})["a"])
