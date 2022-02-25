import sys

record = []

with open('input_2016_20.txt') as fd:
    for line in fd.readlines():
        a, b = [int(i) for i in line.strip().split("-")]
        record.append((a, b))

record.sort()
total, ip, index = 0, 0, 0
while ip < 2**32:
    lower, upper = record[index]
    if ip >= lower:
        if ip <= upper:
            ip = upper + 1
            continue
        index += 1
    else:
        print(ip)
        total += 1
        ip += 1

print(total)