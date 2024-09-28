#!/usr/bin/env python3

import sys

dirmap = {
    "R": (1, 0),
    "U": (0, -1),
    "L": (-1, 0),
    "D": (0, 1),
}

def make_rope(length):
    return [(0, 0) for _ in range(length)]

def pull_rope(rope, dx, dy):
    rope[0] = (rope[0][0] + dx, rope[0][1] + dy)
    for i in range(1, len(rope)):
        dx = rope[i-1][0] - rope[i][0]
        dy = rope[i-1][1] - rope[i][1]
        if -1 <= dx <= 1 and -1 <= dy <= 1:
            continue

        sy = (dy > 0) - (dy < 0) # +1, 0, -1
        sx = (dx > 0) - (dx < 0) # +1, 0, -1
        rope[i] = (rope[i][0]+sx, rope[i][1]+sy)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            txt = f.read()
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    rope1 = make_rope(2)
    map1 = set()
    map1.add(rope1[-1])

    rope2 = make_rope(10)
    map2 = set()
    map2.add(rope2[-1])

    for line in txt.splitlines():
        direction, count = line.split()
        dx, dy = dirmap[direction]
        for _ in range(int(count)):
            pull_rope(rope1, dx, dy)
            pull_rope(rope2, dx, dy)
            map1.add(rope1[-1])
            map2.add(rope2[-1])

    print("Part1:", len(map1))
    print("Part2:", len(map2))
