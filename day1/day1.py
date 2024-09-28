#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            txt = f.read() + "\n"

        elves = []
        cur = 0
        for line in txt.splitlines():
            if not line:
                elves.append(cur)
                cur = 0
            else:
                cur += int(line)
        elves.sort(key=lambda x: -x)
        print("Part1:", elves[0])
        print("Part2:", sum(elves[:3]))
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
