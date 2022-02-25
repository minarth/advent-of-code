import re

with open("input_08.txt") as f:
    test_input = f.readlines()

def _memory_length(s):
    #print([(x, ) for x in s.strip()])
    return len(s.strip())

def _escaped_length(s):
    hex_re = re.compile(r"(\\x[0-9abcdef][0-9abcdef])")
    new = re.sub(hex_re, "X", s.strip()).replace("\\\"", "Y").replace("\\\\", "Z")
    #print(new)
    return len(new) - 2

def _descaped_length(s):
    #hex_re = re.compile(r"(\\x[0-9abcdef][0-9abcdef])")
    #new = re.sub(hex_re, "XXXXX", s.strip()[1:-1]).replace("\\\\", "YYYY").replace("\\\"", "\\\\\"")
    new = s.strip().replace("\\", "\\\\")
    new = new.replace('"', '\\"')    
    print(f"New {new}")
    return len(new) + 2

if __name__ == '__main__':
    space_diff = 0    
    descaped_diff = 0
    for line in test_input:
        #rint(line, _memory_length(line), _escaped_length(line))
        print("="*10)
        space_diff += _memory_length(line) - _escaped_length(line)
        print(line, _memory_length(line), _descaped_length(line))
        descaped_diff += _descaped_length(line) - _memory_length(line)
    print(space_diff, descaped_diff)
    #print(_memory_length('""'), _escaped_length('""'), _memory_length('"abc"'), _escaped_length('"abc"'), _memory_length('"aaa\"aaa"'), _escaped_length('"aaa\"aaa"'), _memory_length('"\x27"'), _escaped_length('"\x27"'))