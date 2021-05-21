import json

def part_one(data, ignore=None):
    """
    >>> part_one([1, 2, 3])
    6
    >>> part_one({"a":2,"b":4})
    6
    >>> part_one([[[3]]])
    3
    >>> part_one({"a":{"b":4},"c":-1})
    3
    >>> part_one([[[]]])
    0
    >>> part_one({})
    0
    >>> part_one([1,{"c":"red","b":2},3], 'red')
    4

    >>> part_one([1,"red",5], 'red')
    6
    """
    if type(data) == int:
        return data

    elif type(data) == list and len(data) > 0:
        return sum([part_one(d, ignore) for d in data])
    
    elif type(data) == dict and len(data) > 0:
        if ignore is not None and ignore in data.values(): 
            return 0
        return sum([part_one(d, ignore) for d in data.values()])

    return 0

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    with open("2015/12/input.txt", "r") as f:
        test_input = json.load(f)
        print(f"Part one: {part_one(test_input)}")
        print(f"Part two: {part_one(test_input, 'red')}")
