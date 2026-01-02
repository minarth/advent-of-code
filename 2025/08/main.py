from heapq import heappush, heappop
from collections import defaultdict

def process(fn):
    with open(fn, "r") as fd:
        data = fd.readlines()
        data = [line.strip().split(",") for line in data]
        data = [tuple(map(int, line)) for line in data]
        return data


def part_one(points, connections = 10):
    distances = []
    for i, p in enumerate(points):
        for j, q in enumerate(points[:i]):
            d = sum([(a-b)**2 for a,b in zip(p,q)])**0.5
            heappush(distances, (d, (i, j)))
    # clustering var
    c = {i: i for i,_ in enumerate(points)}
    clusters = {i: {i} for i in c}
    counter = 0
    while distances and counter < connections:
        d, (i,j) = heappop(distances)
        if c[i] != c[j]:
            new_cluster = min(c[i], c[j])
            clusters[new_cluster] = clusters[c[i]].union(clusters[c[j]])
            del clusters[max(c[i], c[j])]
            for k in clusters[new_cluster]:
                c[k] = new_cluster
        counter += 1

    x,y,z = sorted([len(v) for v in clusters.values()])[::-1][:3]    
    return x*y*z


def part_two(points):
    # ugly duplication
    distances = []
    for i, p in enumerate(points):
        for j, q in enumerate(points[:i]):
            d = sum([(a-b)**2 for a,b in zip(p,q)])**0.5
            heappush(distances, (d, (i, j)))
    # clustering var
    c = {i: i for i,_ in enumerate(points)}
    clusters = {i: {i} for i in c}
    
    while distances:
        d, (i,j) = heappop(distances)
        if c[i] != c[j]:
            new_cluster = min(c[i], c[j])
            clusters[new_cluster] = clusters[c[i]].union(clusters[c[j]])
            del clusters[max(c[i], c[j])]
            for k in clusters[new_cluster]:
                c[k] = new_cluster
        if len(clusters) == 1: 
            print(points[i], points[j])
            return points[i][0]*points[j][0]
    return -1


if __name__ == "__main__":
    data = process("test")
    print(f"part one {part_one(data)}")
    print(f"part two {part_two(data)}")
    print("=")
    data = process("input")
    print(f"part one {part_one(data, 1000)}")
    print(f"part two {part_two(data)}")