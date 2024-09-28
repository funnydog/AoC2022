#!/usr/bin/env python3

import sys
from functools import cache

def grid_check(grid, x, y):
    score = 1
    visible = False
    for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        nx = x + dx
        ny = y + dy
        count = 0
        hidden = False
        while 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            count += 1
            if grid[ny][nx] >= grid[y][x]:
                hidden = True
                break
            nx = nx + dx
            ny = ny + dy

        score *= count
        if not hidden:
            visible = True

    return visible, score

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            txt = f.read()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    grid = tuple(tuple(int(x) for x in row) for row in txt.splitlines())

    count = 0
    maxscore = 0
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            visible, score = grid_check(grid, x, y)
            if visible:
                count += 1

            if maxscore < score:
                maxscore = score

    print("Part1:", count)
    print("Part2:", maxscore)
