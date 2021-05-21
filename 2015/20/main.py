def _battle(player_stats, boss_stats):
    """
    >>> _battle({"hp": 8, "dmg": 5, "armor": 5}, {"hp": 12, "dmg": 7, "armor": 2})
    True

    >>> _battle({"hp": 8, "dmg": 5, "armor": 5}, {"hp": 12, "dmg": 7, "armor": 5})
    False
    """    
    plr_hp, boss_hp = player_stats["hp"], boss_stats["hp"]
    while plr_hp > 0 and boss_hp > 0:
        boss_hp -= max(1, player_stats["dmg"] - boss_stats["armor"])
        if boss_hp <= 0: return True

        plr_hp -= max(1, boss_stats["dmg"] - player_stats["armor"])
    
    return False


def _create_stats(wearing, hp):
    """
    >>> _create_stats([(1, 1, 1), (2, 0, 2), (3, 3, 0)], 10)
    {'hp': 10, 'dmg': 4, 'armor': 3, 'cost': 6}
    """

    stats = {"hp": hp, "dmg": 0, "armor": 0, "cost":0}
    for w in wearing:
        stats["cost"] += w[0]
        stats["dmg"] += w[1]
        stats["armor"] += w[2]
    return stats

def _search_through_eq(equipment):
    for weapon in equipment["weapons"]:
        yield [weapon]
        for armor in equipment["armor"]:
            yield [weapon, armor]
            for ring1 in equipment["rings"]:
                yield [weapon, ring1]
                yield [weapon, ring1, armor]
                for ring2 in equipment["rings"]:
                    if ring1 == ring2: continue
                    yield [weapon, ring1, ring2]
                    yield [weapon, ring2]
                    yield [weapon, armor, ring1, ring2]
                    yield [weapon, armor, ring2]
            

def part_one(equipment, boss, hp):
    best_cost = 74+102+100+80  # max possible price for eq
    equip_combs = _search_through_eq(equipment)

    for combination in equip_combs:
        plr_stats = _create_stats(combination, hp)
        if plr_stats["cost"] >= best_cost: continue
        if _battle(plr_stats, boss):
            best_cost = plr_stats["cost"]
    
    return best_cost
        
def part_two(equipment, boss, hp):
    worst_cost = 8  # min possible price for eq
    equip_combs = _search_through_eq(equipment)

    for combination in equip_combs:
        plr_stats = _create_stats(combination, hp)
        if _battle(plr_stats, boss): continue
        if plr_stats["cost"] > worst_cost: 
            worst_cost = plr_stats["cost"]
    
    return worst_cost

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    equipment = {
        "weapons": [(8, 4, 0), (10, 5, 0), (25, 6, 0), (40, 7, 0), (74, 8, 0)],
        "armor": [(13, 0, 1), (31, 0, 2), (53, 0, 3), (75, 0, 4), (102, 0, 5)],
        "rings": [(25, 1, 0), (20, 0, 1), (40, 0, 2), (50, 2, 0), (80, 0, 3), (100, 3, 0)],
    }

    print(f'Part one {part_one(equipment, {"hp": 109, "dmg": 8, "armor": 2}, 100)}')
    print(f'Part two {part_two(equipment, {"hp": 109, "dmg": 8, "armor": 2}, 100)}')
