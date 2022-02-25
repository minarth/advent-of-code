from heapq import heappop, heappush
from itertools import permutations

def _parse(maze):
    poi = {}
    maze = [m.strip() for m in maze]
    for i, r in enumerate(maze):
        for j, c in enumerate(r):
            if c not in (".", "#"):
                poi[int(c)] = (i, j)
    list_maze = [list(m) for m in maze]
    return list_maze, poi

def _print(maze):
    for r in maze:
        print("".join([str(c)[-1] for c in r]))

def _next_actions(maze, position):
    x, y = position
    l, r, u, d = (x, y-1), (x, y+1), (x-1, y), (x+1, y)
    actions = [l, r, u, d]
    return [(ax, ay) for (ax, ay) in actions if maze[ax][ay] != "#"]

def _heuristics(position, target):
    xp, yp = position
    xt, yt = target
    return abs(xp-xt) + abs(yp-yt)

def _a_star(maze, start, target, heuristics, next_actions):
    # Here we go again
    # Nodes/positions are saved in tuples (PRIORITY OF SEARCH, POSITION, PATH TRAVELED)
    priority_queue = [(heuristics(start, target), start, [])]
    already_searched = set()
    while len(priority_queue) > 0:
        _, position, path = heappop(priority_queue)
        if position == target:
            return len(path), position, path
        if position in already_searched: continue
        for action in next_actions(maze, position):
            if action not in already_searched:
                heappush(priority_queue, (heuristics(action, target)+len(path)+1, action, path+[action]))

        already_searched.add(position)

    # No path found
    return None

def _maze_distances(maze, origin):
    unexpanded = [(0, origin)]
    expanded = set()
    distances = [["#" for _ in range(len(maze[0]))] for _ in range(len(maze))]
    filled = 0
    while len(unexpanded) > 0: # and filled < 20:
        d, point = heappop(unexpanded)
        if point in expanded: continue
        x, y = point
        distances[x][y] = d

        filled += 1
        if filled % 50 == 0: print(f"Progress {filled} {filled/3825}")
        for action in _next_actions(maze, point):
            if action not in expanded:
                heappush(unexpanded, (d+1, action))

        expanded.add(point)
    return distances

def part(maze, pois, start=0, end=None):
    max_poi = max(pois.keys())
    distances = [[None for _ in range(max_poi+1)] for _ in range(max_poi+1)]

    for poi_a in range(max_poi+1):
        for poi_b in range(poi_a+1, max_poi+1):
            dist, _, _ = _a_star(maze, pois[poi_a], pois[poi_b], _heuristics, _next_actions)
            distances[poi_a][poi_b] = distances[poi_b][poi_a] = dist

    best_dist = None
    for path in permutations(range(1, max_poi+1)):
        path = (start,) + path
        if end is not None:
            path += (end,)
        dist = 0
        for a, b in zip(path[:-1], path[1:]):
            dist += distances[a][b]
            if best_dist is not None and dist > best_dist:
                break
        else:
            if best_dist is None:
                best_dist = dist
            if dist < best_dist:
                best_dist = dist

    return best_dist


if __name__ == "__main__":
    # This is test from task assignment
    with open("2016/24/test.txt", "r") as fd:
        maze_input = fd.readlines()
        maze, poi = _parse(maze_input)
        _maze_distances(maze, (1, 1))
        print(f"Test one {part(maze, poi)}")

    # This is with my puzzle input
    with open("2016/24/input.txt", "r") as fd:
        maze_input = fd.readlines()
        maze, poi = _parse(maze_input)
        #_print(maze)
        #print()
        #_maze_distances(maze, (1, 1))
        print(f"Part one {part(maze, poi)}")
        print(f"Part two {part(maze, poi, end=0)}")