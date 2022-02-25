import re

def _parse(ip):
    re_brackets = re.compile(r"(\[[a-z]+\])")
    brackets = re.findall(re_brackets, ip)

    inner_bracket = []

    for bracket in brackets:
        ip = ip.replace(bracket, "###")
        inner_bracket.append(bracket[1:-1])

    return (ip.split("###"), inner_bracket)


def _is_abba(substr):
    """
    >>> _is_abba("abba")
    True
    >>> _is_abba("aaaa")
    False
    >>> _is_abba("ioxxoj")
    True
    >>> _is_abba("qwer")
    False
    """
    for a, b in zip(substr[:-1], substr[1:]):
        if (a + b) + (a + b)[::-1] in substr and a != b:
            #print(substr)
            return True

    return False


def _get_abas(substr):
    abas = []
    for a, b in zip(substr[:-1], substr[1:]):
        if (a + b + a) in substr and a != b:
            abas.append((b+a+b))

    return abas


def part_one(ips):
    tls_ip = 0
    for good, bad in ips:
        if any([_is_abba(g) for g in good]) and not any([_is_abba(b) for b in bad]):
            tls_ip += 1
    return tls_ip

def part_two(ips):
    ssl_ip = 0
    
    for good, bad in ips:
        abas = []
        for g in good:
            abas += _get_abas(g)

        for a in abas:
            if a in "#".join(bad):
                ssl_ip += 1
                break
    return ssl_ip


if __name__ == '__main__':
    from doctest import testmod
    testmod()

    with open("input_2016_07.txt", "r") as f:
        test_input = f.readlines()
        test_input = [_parse(ti) for ti in test_input]
        print(f"Part one {part_one(test_input)}")
        print(f"Part two {part_two(test_input)}")