from hashlib import md5

hexadigits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
triplets = {k: k*3 for k in hexadigits}
pentatles = {k: k*5 for k in hexadigits}


def _get_first_triplet(hash):
    
    found = []
    for l, tri in triplets.items():
        if tri in hash:
            found.append((hash.index(tri), l))

    if found:
        return sorted(found)[0][1]   
   
    return False

def _chain_hash_fn(key):
    hash = md5(key)
    for _ in range(2016):
        hash = md5(hash.hexdigest().encode())
    return hash

def part(salt, hash_fn):
    """
    >>> part("abc", md5)
    22728

    >>> part("abc", _chain_hash_fn)
    22551
    """
    indicies = []
    checks = []  # {key, from, to, idx}
    idx = 0
    while len(indicies) < 64:
        hash = hash_fn((salt + str(idx)).encode()).hexdigest()
        triplet = _get_first_triplet(hash)
        if triplet:
            checks.append({"key": triplet, "from": idx+1, "to": idx+1000, "idx": idx})
        found = []
        for check in checks:
            if check["from"] <= idx <= check["to"] and pentatles[check["key"]] in hash:
                indicies.append(check["idx"])
                #print(indicies)
                found.append(check)
            elif check["to"] < idx:
                found.append(check)
        [checks.remove(f) for f in found]

        idx += 1

    return sorted(indicies)[63]



if __name__ == "__main__":
    from doctest import testmod
    testmod()

    print(f"Part One {part('jlmsuwbz', md5)}")
    print(f"Part two {part('jlmsuwbz', _chain_hash_fn)}")