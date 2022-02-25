from collections import deque

# This is not how the coordinates work in assignment
# X .. row
# Y .. col

# cart = {"position": (X,Y), "orientation": ENUM, "next": deque "previous": char}
UP = ((-1, 0), "^")
DOWN = ((1, 0), "v")
LEFT = ((0, -1), "<")
RIGHT = ((0, 1), ">")
# POSITIVE rotates to the LEFT
# NEGATIVE to the RIGHT
DIRS = (UP, RIGHT, DOWN, LEFT)
TRANSLATE_DIR = {
    "^": UP, 
    "v": DOWN,
    "<": LEFT,
    ">": RIGHT,
}

CART_SYMS = "<^>v"

def _parse(lines):
    grid = []
    for line in lines:
        grid.append(list(line.rstrip()))
    
    carts = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell in CART_SYMS:
                orientation = deque(DIRS)
                orientation.rotate(-orientation.index(TRANSLATE_DIR[cell]))
                carts.append({
                    "pos": (i,j),
                    "orientation": orientation,
                    "next": deque([1, 0, -1]),
                    "prev": "|" if cell in "v^" else "-",
                    "active": True
                })
    return grid, carts

def _print(grid):
    for row in grid:
        row_str = ""
        for cell in row:
            if cell in CART_SYMS:
                row_str += _cart_str(cell)
            else:
                row_str += cell
        print(row_str)

def _update_pos(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return (x1+x2, y1+y2)

def _tick(grid, carts, fail_on_crash=True):


    for cart in sorted(carts, key=lambda cart: cart["pos"]):
        x,y = _update_pos(cart["pos"], cart["orientation"][0][0])
        next_symbol = grid[x][y]
        curr_x,curr_y = cart["pos"]
        grid[curr_x][curr_y] = cart["prev"]

        if not cart["active"]: continue

        if next_symbol in CART_SYMS and fail_on_crash:
            raise Exception(f"Collision detected on {(x, y)}")
        elif next_symbol in CART_SYMS:
            cart["active"] = False
            for next_cart in carts:
                if next_cart["pos"] == (x,y):
                    next_cart["active"] = False
                    break
            continue
        
        cart["prev"] = next_symbol

        if next_symbol == "+":
            cart["orientation"].rotate(cart["next"][0])
            cart["next"].rotate(-1)
        elif next_symbol in "-|":
            # just continue, nothing to see here
            pass
        elif next_symbol == "/":
            orient = cart["orientation"][0]
            if orient in (UP, DOWN):
                cart["orientation"].rotate(-1)
            elif orient in (LEFT, RIGHT):
                cart["orientation"].rotate(1)
            
        elif next_symbol == "\\":
            orient = cart["orientation"][0]
            if orient in (UP, DOWN):
                cart["orientation"].rotate(1)
            elif orient in (LEFT, RIGHT):
                cart["orientation"].rotate(-1)

        grid[x][y] = cart["orientation"][0][1]
        cart["pos"] = (x, y)
    
    return grid, carts
            
def part_one(grid, carts):
    ticks = 0
    while True:         
        grid, carts = _tick(grid, carts)
        ticks += 1


def part_two(grid, carts):
    ticks = 0
    while len([cart for cart in carts if cart["active"]]) != 1:         
        grid, carts = _tick(grid, carts, False)
        ticks += 1
        
    print([cart for cart in carts if cart["active"]])
    return carts

def _cart_str(cart):
    OKCYAN = '\033[96m'
    ENDC = '\033[0m'
    return f"{OKCYAN}{cart}{ENDC}"

if __name__ == "__main__":
    #with open("2018/13/test.txt", "r") as fd:
    #    g, c = _parse(fd.readlines())
    #    part_one(g, c)

    with open("2018/13/input.txt", "r") as fd:
        g, c = _parse(fd.readlines())
        part_two(g, c)

