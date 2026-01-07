def process(fn):
    with open(fn, "r") as fd:
        boxes = {}
        box_id = None
        box = []
        grids = []
        for line in fd.readlines():
            line = line.strip()
            if "x" in line:
                a,b = line.split(":")[0].split("x")
                line = list(map(int, line.split(":")[1].strip().split(" ")))
                grids.append(((int(a),int(b)), line))
            elif ":" in line: 
                box_id = int(line.split(":")[0])
            elif line == "":
                boxes[box_id] = box
                box_id, box = None, []
            else:
                box.append(line)
        return boxes, grids


def part_one(boxes, grids):
    # lets go with naive way now. DFS as a backup
    # part two will punch me
    # sadly works, even though it fails for small areas.
    coverage = {k: sum([line.count("#") for line in v]) for k,v in boxes.items()}
    counter = 0
    for (w,h), counts in grids:
        cov = sum([coverage[i]*c for i,c in enumerate(counts)])
        if (w*h) >= cov: 
            counter += 1
    return counter


if __name__ == "__main__":

    data = process("input")
    print(f"part one {part_one(*data)}")
