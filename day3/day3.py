#!/usr/bin/env python3

import string
import sys

priorities = string.ascii_lowercase + string.ascii_uppercase

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stederr)
        sys.exit(1)

    with open(sys.argv[1], "rt") as f:
        lines = f.read().splitlines()

    part1 = 0
    for line in lines:
        half = len(line) // 2
        shared = set(line[:half]).intersection(set(line[half:]))
        for x in shared:
            part1 += priorities.index(x) + 1

    part2 = 0
    for i in range(0, len(lines), 3):
        shared = set(priorities)
        for j in range(i, i + 3):
            shared = shared.intersection(lines[j])
        for x in shared:
            part2 += priorities.index(x) + 1

    print("Part1:", part1)
    print("Part2:", part2)
