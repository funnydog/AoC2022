#!/usr/bin/env python3
from heapq import heappush, heappop
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            lines = f.read().splitlines()
    except Exception as e:
        print(f"cannot open {sys.argv[1] }", file=sys.stderr)
        sys.exit(1)

    height, width = len(lines), len(lines[0])
    blizzards: list[tuple[str,int,int]] = []
    for y, row in enumerate(lines):
        for x, v in enumerate(row):
            if v in "^v<>":
                blizzards.append((v,x,y))

    # move the blizzards
    def move(blizzards: list[tuple[str,int,int]]) -> list[tuple[str,int,int]]:
        result: list[tuple[str,int,int]] = []
        for k, x, y in blizzards:
            if k == "^":
                y -= 1
            elif k == ">":
                x += 1
            elif k == "v":
                y += 1
            elif k == "<":
                x -= 1
            else:
                assert False, "Unknown blizzard"

            x = (x-1) % (width-2) + 1
            y = (y-1) % (height-2) + 1
            result.append((k, x, y))

        return result

    # precompute the obstacles
    obstacles = []
    initial = {(x, y):True for _, x, y in blizzards}
    obstacles.append(initial)
    while True:
        blizzards = move(blizzards)
        newmap = {(x, y):True for _, x, y in blizzards}
        if initial == newmap:
            break
        obstacles.append(newmap)

    # dijkstra
    def time_spent(start: tuple[int,int,int], end: tuple[int,int,int]) -> int:
        global obstacles

        queue: list[tuple[int,int,int]] = []
        heappush(queue, start)
        time: dict[tuple[int,int,int],int] = {}
        time[start] = start[0]
        while queue:
            t, x, y = heappop(queue)
            if x == end[1] and y == end[2]:
                return t

            nt = t + 1
            obstacle = obstacles[nt % len(obstacles)]
            for dx, dy in (0,0),(0,-1),(1,0),(0,1),(-1, 0):
                nx = x + dx
                ny = y + dy
                if nx < 0 or nx >= width or ny < 0 or ny >= height:
                    continue

                if lines[ny][nx] == "#":
                    continue

                if (nx, ny) in obstacle:
                    continue

                nstate = (nt, nx, ny)
                if nstate in time and time[nstate] < nt:
                    continue

                time[nstate] = True
                heappush(queue, nstate)

        return 0

    t1 = time_spent((0,1,0), (0,width-2,height-1))
    print("Part1:", t1)
    t2 = time_spent((t1,width-2,height-1), (0,1,0))
    t3 = time_spent((t2,1,0), (0,width-2,height-1))
    print("Part2:", t3)
