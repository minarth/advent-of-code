from collections import Counter
def part(messages, selection=0):
    """
    >>> part(["eedadn", "drvtee", "eandsr", "raavrd", "atevrs", "tsrnev", "sdttsa", "rasrtv", "nssdts", "ntnada", "svetve", "tesnvt", "vntsnd", "vrdear", "dvrsen", "enarar"])
    'easter'
    >>> part(["eedadn", "drvtee", "eandsr", "raavrd", "atevrs", "tsrnev", "sdttsa", "rasrtv", "nssdts", "ntnada", "svetve", "tesnvt", "vntsnd", "vrdear", "dvrsen", "enarar"], -1)
    'advent'
    """
    message = []
    for column in zip(*messages):
        message.append(Counter(column).most_common()[selection][0])
    
    return "".join(message)

if __name__ == "__main__":
    from doctest import testmod
    testmod()

    with open("2016/06/input.txt") as f:
        test_input = [l.strip() for l in f.readlines()]
        print(f"Part one {part(test_input)}")
        print(f"Part two {part(test_input, -1)}")