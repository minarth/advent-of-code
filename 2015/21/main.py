from collections import defaultdict
from math import ceil
from itertools import product

# Possible keys cost, dmg, turns, armor, mana, heal
MM = defaultdict(int, {"cost": 53, "dmg": 4, "name": "mm"})
DRAIN = defaultdict(int, {"cost": 73, "dmg": 2, "heal": 2, "name": "drain"})
POISON = defaultdict(int, {"cost": 173, "dmg": 3, "turns": 6, "name": "poison"})
SHIELD = defaultdict(int, {"cost": 113, "armor": 7, "turns": 6, "name": "shield"})
RECHARGE = defaultdict(int, {"cost": 229, "mana": 101, "turns": 5, "name": "recharge"})

def _battle(plr_hp, plr_mana, boss_hp, boss_dmg, magic_seq, debug=False, hard=0):
    """
    >>> _battle(10, 250, 13, 8, [POISON, MM])
    True

    >>> _battle(10, 250, 13, 8, [POISON, SHIELD])
    False

    >>> _battle(10, 250, 14, 8, [RECHARGE, SHIELD, DRAIN, POISON, MM])
    True
    """
    effects = []
    spell_counter = 0

    while plr_hp > 0 and boss_hp > 0:
        plr_armor = 0
        plr_dmg = 0 
        if debug: print("===== PLR  =====")
        if debug: print(f"Plr {plr_hp} {plr_mana} Boss {boss_hp}")
        next_turn_effects = []

        plr_hp -= hard
        if debug: print(f"Plr {plr_hp} {plr_mana} Boss {boss_hp}")

        if plr_hp <= 0: return False

        for effect, turns in effects:
            if debug: print(f"Effect {effect['name']}")
            plr_mana += effect["mana"]
            boss_hp -= effect["dmg"]
            if (turns-1) > 0: next_turn_effects.append((effect, turns-1))
        
        effects = next_turn_effects

        spell = magic_seq[spell_counter]

        plr_mana -= spell["cost"]
        if debug: print(f"Player casts {spell['name']} {spell} with rems {plr_mana}")
        if plr_mana < 0: return False

        if spell["turns"] == 0:
            boss_hp -= spell["dmg"]
            plr_hp += spell["heal"]          
        else:
            applied_effects = [e[0] for e in effects]
            if spell not in applied_effects:
                effects.append((spell, spell["turns"]))

        if debug: print("=====  BOSS  =====")
        if debug: print(f"Plr {plr_hp} {plr_mana} Boss {boss_hp}")
        next_turn_effects = []
        for effect, turns in effects:
            if debug: print(f"Effect {effect['name']} {effect}")
            plr_mana += effect["mana"]
            plr_armor = max(effect["armor"], plr_armor)
            boss_hp -= effect["dmg"]
            if (turns-1) > 0: next_turn_effects.append((effect, turns-1))
        
        effects = next_turn_effects
        
        if boss_hp <= 0: return True

        if debug: print(f"Boss deals {boss_dmg} {plr_armor}")
        plr_hp -= max(1, boss_dmg - plr_armor)
        if debug: print(f"Plr {plr_hp} {plr_mana} Boss {boss_hp}")
        spell_counter += 1
        if spell_counter >= len(magic_seq): return False
    
    return False

def _generate_spell_seqs(max_spells=50):
    # max spell is estimate on number of rounds
    combs = [[]]
    while len(combs[0]) < max_spells:
        new_combs = []
        for c in combs:
            for spell in (MM, DRAIN, POISON, SHIELD, RECHARGE):
                if spell["turns"] > 1:
                    if spell not in c[-ceil(spell["turns"]/2):]:
                        yield c + [spell]
                        new_combs.append(c + [spell])    
                else:
                    yield c + [spell]
                    new_combs.append(c + [spell])
        combs = new_combs    
        
def _cost_of_sequence(seq):
    return sum([s["cost"] for s in seq])

def _is_good_spell(seq):
    """
    >>> _is_good_spell([MM, DRAIN, MM, POISON, POISON])
    False
    >>> _is_good_spell([MM])
    True
    >>> _is_good_spell([RECHARGE, MM, MM, RECHARGE])
    True
    >>> _is_good_spell([RECHARGE, MM, RECHARGE])
    False
    >>> _is_good_spell([RECHARGE, MM, POISON, SHIELD, DRAIN, MM, POISON])
    True
    
    """
    for i, spell in enumerate(seq):
        if spell["turns"] > 0 and spell in seq[i+1:i+ceil(spell["turns"]/2)]:
            return False

    return True
            

def part_one(plr_hp, plr_mana, boss_hp, boss_dmg, max_length=20, hard=0):
    best_mana_cost, best_seq = None, None
    seq_length, one_cheaper = 0, True
    for seq in _generate_spell_seqs(max_length):
        #print(len(seq), seq_length, best_mana_cost)
        if len(seq) > seq_length and one_cheaper:
            print(f"Searching through {len(seq)} combs with best {best_mana_cost}")
            seq_length = len(seq)
            one_cheaper = False
        elif len(seq) > seq_length and not one_cheaper: 
            return best_mana_cost, best_seq
        new_mana_cost = _cost_of_sequence(seq)
        if best_mana_cost is not None and new_mana_cost > best_mana_cost: continue
        one_cheaper = True
        if _battle(plr_hp, plr_mana, boss_hp, boss_dmg, seq, hard=hard):
            print()
            if best_mana_cost is None or best_mana_cost > new_mana_cost:
                best_mana_cost = new_mana_cost
                best_seq = seq
    
    return best_mana_cost, best_seq
    
def part_two(plr_hp, plr_mana, boss_hp, boss_dmg, max_length=20, hard=1):
    #return part_one(plr_hp, plr_mana, boss_hp, boss_dmg, max_length, 1)

    best_mana_cost, best_seq = None, None
    seq_length, one_cheaper = 0, True
    for i in range(1, max_length):
        if i > seq_length and one_cheaper:
            print(f"Searching through {i} combs with best {best_mana_cost}")
            seq_length = i
            one_cheaper = False
        elif i > seq_length and not one_cheaper: 
            return best_mana_cost, best_seq
        for seq in product([MM, POISON, DRAIN, SHIELD, RECHARGE], repeat=i):
            if not _is_good_spell(seq):
                continue
            new_mana_cost = _cost_of_sequence(seq)
            if best_mana_cost is not None and new_mana_cost > best_mana_cost: continue
            one_cheaper = True
            #print(f"Testing {[s['name'] for s in  seq]} {_battle(plr_hp, plr_mana, boss_hp, boss_dmg, seq, hard=hard)}")
            if _battle(plr_hp, plr_mana, boss_hp, boss_dmg, seq, hard=hard):
                if best_mana_cost is None or best_mana_cost > new_mana_cost:
                    best_mana_cost = new_mana_cost
                    best_seq = seq
        
    return best_mana_cost, best_seq


if __name__ == "__main__":
    from doctest import testmod
    testmod()