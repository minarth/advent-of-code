def _parse(in_s):
    """
    >>> _parse('Sue 195: trees: 1, vizslas: 8, akitas: 10')
    ('Sue 195', {'trees': 1, 'vizslas': 8, 'akitas': 10})
    """

    in_s = in_s.strip().split(":")
    name = in_s[0]
    params = ":".join(in_s[1:])
    params_dict = {}
    for param in params.split(", "):
        splitted = param.split(": ")
        params_dict[splitted[0].strip()] = int(splitted[1])
    
    return name, params_dict

def part_one(aunts, ticker_input):
    filtered_aunts = []

    for aunt, compound in aunts:  
        for k,v in compound.items():
            if ticker_input[k] != v: 
                break
        else:
            return aunt
        
    return None

def part_two(aunts, ticker):
    filtered_aunts = []

    for aunt, compound in aunts:  
        for k,v in compound.items():
            if k in ("cats", "trees"):
                if ticker[k] >= v: 
                    break
            elif k in ("pomeranians", "goldfish"):
                if ticker[k] <= v: 
                    break
            elif ticker[k] != v: 
                break
        else:
            return aunt, compound
        
    return None

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    ticker_tape = {
        "children": 3,"cats": 7,"samoyeds": 2,
        "pomeranians": 3,"akitas": 0,"vizslas": 0,
        "goldfish": 5,"trees": 3,"cars": 2,"perfumes": 1
        }

    with open("2015/16/input.txt", "r") as f:
        test_input = f.readlines()
        parsed_input = [_parse(t) for t in test_input]
        print(f"Part one: {part_one(parsed_input, ticker_tape)}")
        print(f"Part two: {part_two(parsed_input, ticker_tape)}")
