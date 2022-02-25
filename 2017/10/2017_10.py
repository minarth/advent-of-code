from collections import deque
from operator import xor
from functools import reduce

def knot_hash(lengths, length=256, position=0, skip_size=0):
    lengths = [ord(s) for s in str(lengths)] + [17, 31, 73, 47, 23]
    h = range(length)
    for i in range(64):
        for l in lengths:
            if l > len(h): continue
            h = list(h) 
            h = deque(h[:l][::-1] + h[l:])
            h.rotate(-1*(l+skip_size))
            position += l+skip_size
            skip_size += 1

    # h is now sparse hash
    h.rotate(position)
    h = list(h)
    dense = []
    for i in range(16):
        dense.append(f"{reduce(xor, h[i*16:(i+1)*16]):0{2}x}")

    return "".join(dense)


def part_one(length, position, skip_size, lenghts):
    h = range(length)
    for l in lenghts:
        if l > len(h): continue
        h = list(h) 
        h = deque(h[:l][::-1] + h[l:])
        h.rotate(-1*(l+skip_size))
        position += l+skip_size
        skip_size += 1

    h.rotate(position)
    return h[0]*h[1]

if __name__ == '__main__':
    test_input = [197,97,204,108,1,29,5,71,0,50,2,255,248,78,254,63]
    #test_input = [3, 4, 1, 5]
    print(f"Part one {part_one(256, 0, 0, test_input)}")
    print(f"Tests {knot_hash('')}")
    print(f"Tests {knot_hash('AoC 2017')}")
    print(f"Tests {knot_hash('1,2,3')}")
    print(f"Tests {knot_hash('1,2,4')}")
    print(f"Part two {knot_hash('197,97,204,108,1,29,5,71,0,50,2,255,248,78,254,63')}")
