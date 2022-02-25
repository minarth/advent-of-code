from heapq import heappush, heappop

def _is_wall(x, y, odfn):
    """
    odfn ... office designer's favorite number
    
    >>> _is_wall(0, 0, 10)
    False

    >>> _is_wall(4, 3, 10)
    True

    >>> _is_wall(7, 5, 10)
    False

    >>> _is_wall(1, 0, 10)
    True

    >>> _is_wall(7, 4, 10)
    False
    
    """
    step = x**2 + 3*x + 2*x*y + y + y**2 + odfn
    binary = format(step, "b")
    return binary.count("1") % 2 == 1

def _a_star_heuristic(position, target):
    """
    >>> _a_star_heuristic((0, 0), (2, 3))
    5

    >>> _a_star_heuristic((2, 3), (0, 0))
    5
    """

    x1, y1 = position
    x2, y2 = target
    return abs(x1-x2) + abs(y1-y2)

def _next_nodes(x, y, odfn):
    up = (x, max(0, y-1))
    down = (x, y+1)
    left = (max(0, x-1), y)
    right = (x+1, y)

    possibilities = {up, down, left, right, (x,y)}
    possibilities.remove((x,y))
    return {p for p in possibilities if not _is_wall(*p, odfn)}

def shortest_path(start, target, odfn):
    """
    >>> shortest_path((1,1), (7,4), 10)
    11
    """
    positions = []
    explored = set()
    heappush(positions, (_a_star_heuristic(start, target), start, 0))
    while len(positions) > 0:
        _, current, path_length = heappop(positions)
        #print(f"Expanding {current} far {path_length} {explored}")
        if current == target:
            return path_length

        if current in explored:
            continue

        for nxt in _next_nodes(*current, odfn):
            heappush(positions, (_a_star_heuristic(nxt, target)+path_length+1, nxt, path_length+1))

        explored.add(current)

    return None

def full_search(start, length, odfn):
    positions = []
    explored = set()
    heappush(positions, (0, start))
    while len(positions) > 0:
        path_length, current = heappop(positions)
        #print(f"Expanding {current} far {path_length} {explored}")

        if current in explored or path_length > length:
            continue

        for nxt in _next_nodes(*current, odfn):
            heappush(positions, (path_length+1, nxt))

        explored.add(current)

    _print_maze(explored, odfn, length*2)
    return len(explored)

def _print_maze(searched, odfn, n=10):
    # x y is in different order so it matches web example
    maze = [list("."*n) for i in range(n)]
    
    for x in range(n):
        for y in range(n):
            if _is_wall(x, y, odfn):
                maze[y][x] = "#"

    for x, y in searched:
        if maze[y][x] == "#": raise Exception("searched the wall")
        maze[y][x] = "O"

    print("\n".join(["".join(cell) for cell in maze]))


if __name__ == '__main__':
    from doctest import testmod
    testmod()

    print(f"Part One {shortest_path((1, 1), (31, 39), 1362)}")
    print(f"Part two {full_search((1, 1), 50, 1362)}")