#!/usr/bin/env python3

import sys

def is_inside(r1, r2):
    return r2[0] <= r1[0] and r1[1] <= r2[1]

def overlap(r1, r2):
    if r1[0] > r2[0]:
        r1, r2 = r2, r1
    return r1[0] <= r2[1] and r1[1] >= r2[0]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "rt") as f:
        pairs = []
        for line in f:
            pairs.append([tuple(map(int, x.split("-"))) for x in line.strip().split(",")])

    part1 = 0
    part2 = 0
    for r1, r2 in pairs:
        if is_inside(r1, r2) or is_inside(r2, r1):
            part1 += 1
        if overlap(r1, r2):
            part2 += 1

    print("Part1:", part1)
    print("Part2:", part2)
