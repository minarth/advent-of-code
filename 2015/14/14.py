test_input = """Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds.
    Blitzen can fly 13 km/s for 4 seconds, but then must rest for 49 seconds.
    Rudolph can fly 20 km/s for 7 seconds, but then must rest for 132 seconds.
    Cupid can fly 12 km/s for 4 seconds, but then must rest for 43 seconds.
    Donner can fly 9 km/s for 5 seconds, but then must rest for 38 seconds.
    Dasher can fly 10 km/s for 4 seconds, but then must rest for 37 seconds.
    Comet can fly 3 km/s for 37 seconds, but then must rest for 76 seconds.
    Prancer can fly 9 km/s for 12 seconds, but then must rest for 97 seconds.
    Dancer can fly 37 km/s for 1 seconds, but then must rest for 36 seconds."""

def _parse(string):
    """
    >>> _parse("Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds.")
    ('Vixen', 8, 8, 53)
    """
    splitted = string.strip().split(" ")
    name, speed, travel_time, rest_time = splitted[0], int(splitted[3]), int(splitted[6]), int(splitted[-2])

    return name, speed, travel_time, rest_time


def _get_from_dict(data, fnc):
    fnc_val = fnc(data.values())
    return {k: v for k,v in data.items() if v == fnc_val}


def part_one(stats, time):
    """
    >>> part_one([("Comet", 14, 10, 127), ("Dancer", 16, 11, 162)], 1)
    {'Comet': 14, 'Dancer': 16}

    >>> part_one([("Comet", 14, 10, 127), ("Dancer", 16, 11, 162)], 1000)
    {'Comet': 1120, 'Dancer': 1056}
    """
    distances = {}
    for name, speed, tt, rt in stats:
        status = ([speed]*tt + [0]*rt)*((time // (tt+rt))+1)
        distances[name] = sum(status[:time])

    return distances

def part_two(stats, time):
    """
    >>> part_two([("Comet", 14, 10, 127), ("Dancer", 16, 11, 162)], 1)
    {'Comet': 0, 'Dancer': 1}

    >>> part_two([("Comet", 14, 10, 127), ("Dancer", 16, 11, 162)], 1000)
    {'Comet': 312, 'Dancer': 689}
    """

    distances = {}
    points = {}
    for name, speed, tt, rt in stats:
        points[name] = [0]*time
        status = ([speed]*tt + [0]*rt)*((time // (tt+rt))+1)

        # Create cummulative distances 
        for t in range(time):
            if t == 0:
                distances[name] = [status[t]]
            else:
                distances[name].append(distances[name][-1] + status[t])
        
    for t in range(time):
        max_val = 0
        for name, _, _, _ in stats:
            max_val = max(distances[name][t], max_val)

        for name, _, _, _ in stats:
            if distances[name][t] == max_val: 
                points[name][t] = 1    

    return {k: sum(v) for k,v in points.items()}


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    parsed_input = [_parse(line) for line in test_input.split("\n")]

    print(f"Part one: {_get_from_dict(part_one(parsed_input, 2503), max)}")
    print(f"Part two: {_get_from_dict(part_two(parsed_input, 2503), max)}")