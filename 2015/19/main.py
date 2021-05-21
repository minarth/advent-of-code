def _parse(line):
    """
    >>> _parse("H => NTh")
    ('H', 'NTh', ['N', 'Th'])
    """
    split = line.strip().split(" => ")
    return (split[0], split[1], _split_on_symbol(split[1]))


def part_one(rules, molecule):
    """
    >>> part_one([("H", "HO"), ("H", "OH"), ("O", "HH")], "HOH")
    ['HHHH', 'HOHO', 'HOOH', 'OHOH']
    """
    possibilities = []
    for i in range(len(molecule)):
        for rule in rules: 
            if molecule[i:].startswith(rule[0]):
                possibilities.append(molecule[:i] + molecule[i:].replace(rule[0], rule[1], 1))
    return sorted(list(set(possibilities)))

def _split_on_symbol(molecule):
    splitted = []
    for u, v in zip(molecule[:-1], molecule[1:]):
        if u.lower() == u: continue
        if v.lower() == v: splitted.append(u+v)
        else: splitted.append(u)
    if molecule[-1].lower() != molecule[-1]:
        splitted.append(molecule[-1])
    return splitted

def _chnf_one(rule, glb_i):
    name = rule[0]
    r = rule[2]
    if len(r) <= 2: return [(name, r)]
    
    new_rules = [(name, [r[0], name+str(glb_i)+"0"])]
    for i in range(len(r)-2):
        if len(r[(i+1):]) == 2:
            new_rules.append((name+str(glb_i)+str(i), r[(i+1):]))
        else:
            new_rules.append((name+str(glb_i)+str(i), [r[i+1], name+str(glb_i)+str(i+1)]))
    
    return new_rules

def _chnf(rules):
    transformed_rules = []
    for i, rule in enumerate(rules):
        transformed_rules += _chnf_one(rule, i)    
    return transformed_rules

def part_two(memory, rules):
    """
    Using CYK Algorithm https://en.wikipedia.org/wiki/CYK_algorithm with n^3 complexity

    Takes 2 or 3 minuters to run
    """

    length = len(memory[0])
    rule_mem = [[0 for _ in range(length)]]
    for r in range(1, length):
        new_line, rule_line = [], []
        for c in range(length-r):
            new_cell, rule_cell = [], []
            for i in range(r):
                for rule in rules:
                    if rule[-1][0] in memory[i][c] and rule[-1][1] in memory[r-1-i][c+1+i]:
                        if rule[0] not in new_cell:                                
                            new_cell.append(rule[0])
                        additive = 1 if len(rule[0]) < 3 else 0
                        new_value = rule_mem[i][c] + rule_mem[r-1-i][c+1+i] + additive
                        rule_cell.append(new_value)
            new_line.append(new_cell)
            rule_line.append(min(rule_cell) if rule_cell else None)

        memory.append(new_line)
        rule_mem.append(rule_line)
        
    return rule_mem[-1]


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    input_molecule = "CRnCaCaCaSiRnBPTiMgArSiRnSiRnMgArSiRnCaFArTiTiBSiThFYCaFArCaCaSiThCaPBSiThSiThCaCaPTiRnPBSiThRnFArArCaCaSiThCaSiThSiRnMgArCaPTiBPRnFArSiThCaSiRnFArBCaSiRnCaPRnFArPMgYCaFArCaPTiTiTiBPBSiThCaPTiBPBSiRnFArBPBSiRnCaFArBPRnSiRnFArRnSiRnBFArCaFArCaCaCaSiThSiThCaCaPBPTiTiRnFArCaPTiBSiAlArPBCaCaCaCaCaSiRnMgArCaSiThFArThCaSiThCaSiRnCaFYCaSiRnFYFArFArCaSiRnFYFArCaSiRnBPMgArSiThPRnFArCaSiRnFArTiRnSiRnFYFArCaSiRnBFArCaSiRnTiMgArSiThCaSiThCaFArPRnFArSiRnFArTiTiTiTiBCaCaSiRnCaCaFYFArSiThCaPTiBPTiBCaSiThSiRnMgArCaF"

    with open("2015/19/input.txt", "r") as f:
        test_input = f.readlines()
        parsed_input = [_parse(t) for t in test_input]
        print(f"Part one: {len(part_one(parsed_input, input_molecule))}")

        part_two_input = [[i] for i in _split_on_symbol(input_molecule)]
        print(f"Part two: {part_two([part_two_input], _chnf(parsed_input))}")