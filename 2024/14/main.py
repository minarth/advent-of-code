import re
import curses
from time import sleep

def parse(fn: str) -> list:
    REGEXP = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"
    parsed = []
    with open(fn, "r") as fd:
        for line in fd.readlines():
            match = re.match(REGEXP, line)
            parsed.append(tuple(map(int, match.groups())))
    
    return parsed


def _update(x,y,dx,dy,w,h):
    # update one point given deltas and grid sizes
    x += dx
    y += dy
    if x < 0: x += w
    if x >= w: x %= w
    if y < 0: y += h
    if y >= h: y %= h
    return x,y


def part_one(points, width=101, height=103, steps=100):
    for i in range(steps):
        updates = []
        
        for (x,y,dx,dy) in points:    
            updates.append((*_update(x,y,dx,dy,width, height), dx, dy))
        points = updates
    
    x_mid, y_mid = width // 2, height // 2 
    qs = [0,0,0,0]

    for (x,y,_,_) in points:
        if x < x_mid and y < y_mid: qs[0] += 1
        elif x > x_mid and y < y_mid: qs[1] += 1
        elif x < x_mid and y > y_mid: qs[2] += 1
        elif x > x_mid and y > y_mid: qs[3] += 1

    return qs[0]*qs[1]*qs[2]*qs[3]


def _test_symmetry(points, w, h):
    positions = {(x,y) for x,y,_,_ in points}
    line_nums = [set() for _ in range(h)]
    rows = [0 for _ in range(w)]
    for (x,y,_,_) in points:
        line_nums[y].add((x,y))
        rows[x] += 1

    max_y = max([len(x) for x in line_nums])
    if max_y >= 20: return True
    else: return False


def _show(stdscr, points, step=0):
    stdscr.clear()
    for (x,y,_,_) in points:
        stdscr.addch(y,x,"#")
    stdscr.addstr(104, 0, f"STEP {step}")
    stdscr.refresh()
    stdscr.getkey()


def part_two(stdscr, points, w=101, h=103):
    counter = 0
    while True:
        updates = []
        for (x,y,dx,dy) in points:    
            updates.append((*_update(x,y,dx,dy,w,h), dx, dy))
        points = updates
        counter += 1
        if not _test_symmetry(points, w, h): continue
        curses.wrapper(_show, points, counter)


if __name__ == "__main__":
    data = parse("test")
    print(f"part one {part_one(data, 11, 7)}")

    data = parse("input")
    print(f"part one {part_one(data)}")
    print(f" part two {part_two(None, data)}")
