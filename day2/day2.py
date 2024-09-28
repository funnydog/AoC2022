#!/usr/bin/env python3

# A = Rock
# B = Paper
# C = Scissors

shape_points = {
    "A": 1,
    "B": 2,
    "C": 3,
}

part1_map = {
    "X": "A",
    "Y": "B",
    "Z": "C",
}

defeats = { "C": "A", "A": "B", "B": "C" }
defeated_by = { y: x for x, y in defeats.items() }

def points1(a, b):
    b = part1_map[b]
    if a == defeats[b]:
        return 0 + shape_points[b]
    elif a == b:
        return 3 + shape_points[b]
    else:
        return 6 + shape_points[b]

def points2(a, b):
    if b == "X":
        return 0 + shape_points[defeated_by[a]]
    elif b == "Y":
        return 3 + shape_points[a]
    else:
        return 6 + shape_points[defeats[a]]

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            txt = f.read()

        part1, part2 = 0, 0
        for line in txt.splitlines():
            a, b = line.split()
            part1 += points1(a, b)
            part2 += points2(a, b)

        print("Part1:", part1)
        print("Part2:", part2)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
