import re
from collections import defaultdict


class SolutionFound(BaseException):
    pass

def _parse(line):
    value = re.match(r"(value) ([\d]+) goes to bot ([\d]+)", line.strip())
    if value:
        v, number, target = value.groups()
        return (v, (int(number), target))
    transfers = re.match(f"bot ([\d]+) gives (low|high) to (bot|output) ([\d]+) and (low|high) to (bot|output) ([\d]+)", line.strip())
    if transfers:
        tr = transfers.groups()
        return ("transfer", {
            "from": tr[0],
            "to": [
                {"type": tr[1], "target": tr[2], "id":tr[3]},
                {"type": tr[4], "target": tr[5], "id":tr[6]},
            ]
        })
    
    raise ValueError(f"Cannot parse {line}")

def _step(outputs, bots, rules, end_vals, end_fn):
    for bot, chips in bots.items():
        if len(chips) == 2:
            if bot not in rules:
                continue
            low, high = sorted(chips)
            for rule in rules[bot]:
                if rule["type"] == "low":
                    passing_value = low
                elif rule["type"] == "high":
                    passing_value = high
                
                if rule["target"] == "bot":
                    bots[rule["id"]].append(passing_value)
                else:
                    outputs[rule["id"]].append(passing_value)
            end = end_fn(bots, outputs, end_vals)
            if end:
                raise SolutionFound(f"Solution found {end}")
            bots[bot] = []
    
    return outputs, bots

def _end(bots, _, end_chips):
    end_chips = sorted(end_chips)
    for bot, chips in bots.items():
        if sorted(chips) == end_chips:
            return (bot, bots[bot])
    return False

def _end_two(_, outputs, end_outputs):
    for out in end_outputs:
        if len(outputs[out]) == 0:
            return False
    
    return [outputs[out] for out in end_outputs]

def part_one(program, end_chips, end_fn):
    outputs = defaultdict(list)
    bots = defaultdict(list)
    rules = {}

    for tp, value in program:
        if tp == "transfer":
            bots[value["from"]]
            for to in value["to"]:
                if to["target"] == "bot":
                    bots[to["id"]]
    try: 
        for tp, value in program:
            if tp == "value":
                bots[value[1]].append(value[0])
            elif tp == "transfer":
                rules[value["from"]] = value["to"]
            outputs, bots = _step(outputs, bots, rules, end_chips, end_fn)
        end = end_fn(bots, outputs, end_chips)
        while not end:
            outputs, bots = _step(outputs, bots, rules, end_chips, end_fn)
            end = end_fn(bots, outputs, end_chips)
        return end
    except SolutionFound as sf:
        print(sf)


if __name__ == "__main__":
    test_input = """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2""".split("\n")

    test_input = [_parse(line) for line in test_input]
    #print(f"Test run {part_one(test_input, [2,3])}")

    with open("2016/10/input.txt", "r") as f:
        test_input = [_parse(line) for line in f.readlines()]
        print("Part one")
        part_one(test_input, [17, 61], _end)
        print("Part two")
        part_one(test_input, ["0", "1", "2"], _end_two)
