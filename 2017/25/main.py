input_automaton = {
    "A": {
        0: {"next": "B", "position": 1, "write": 1},
        1: {"next": "C", "position": -1, "write": 0},
    },
    "B": {
        0: {"next": "A", "position": -1, "write": 1},
        1: {"next": "D", "position": -1, "write": 1},
    },
    "C": {
        0: {"next": "D", "position": 1, "write": 1},
        1: {"next": "C", "position": 1, "write": 0},
    },
    "D": {
        0: {"next": "B", "position": -1, "write": 0},
        1: {"next": "E", "position": 1, "write": 0},
    },
    "E": {
        0: {"next": "C", "position": 1, "write": 1},
        1: {"next": "F", "position": -1, "write": 1},
    },
    "F": {
        0: {"next": "E", "position": -1, "write": 1},
        1: {"next": "A", "position": 1, "write": 1},
    },
    "steps": 12656374, 
    "start": "A",
} 

example_automaton = {
    "A": {
        0: {"next": "B", "position": 1, "write": 1},
        1: {"next": "B", "position": -1, "write": 0},
    },
    "B": {
        0: {"next": "A", "position": -1, "write": 1},
        1: {"next": "A", "position": 1, "write": 1},
    },
    "steps": 6,
    "start": "A",
}

def move_tape(tape, position):
    if 0 <= position < len(tape):
        return tape, position
    
    while position < 0:
        tape = [0] + tape
        position += 1
    
    while position >= len(tape):
        tape += [0]
    
    return tape, position

def part(automaton):
    tape = [0]
    position = 0
    state = automaton["start"]
    for i in range(automaton["steps"]):
        #print(f"After {i} steps {tape} {position} {state}")
        tape, position = move_tape(tape, position)
        action = automaton[state][tape[position]]
        tape[position] = action["write"]
        position += action["position"]
        state = action["next"]

    return tape

if __name__ == "__main__":
    print(f"Test output {sum(part(example_automaton))}")
    print(f"Part one {sum(part(input_automaton))}")