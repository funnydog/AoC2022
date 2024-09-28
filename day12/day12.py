#!/usr/bin/env python3

import sys

def bfs(mymap, start, end, forbidfn):
    start_position = None
    for y, row in enumerate(mymap):
        for x, val in enumerate(row):
            if val == start:
                start_position = (x, y)

    height, width = len(mymap), len(mymap[0])
    distance = {start_position: 0}
    queue = [start_position]
    while queue:
        pos = queue.pop(0)
        val = mymap[pos[1]][pos[0]]
        if val == end:
            break
        elif val == "S":
            val = "a"
        elif val == "E":
            val = "z"

        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            npos = (pos[0] + dx, pos[1] + dy)
            if npos[1] < 0 or npos[1] >= height or npos[0] < 0 or npos[0] >= width:
                continue

            nval = mymap[npos[1]][npos[0]]
            if nval == "S":
                nval = "a"
            elif nval == "E":
                nval = "z"

            if forbidfn(val, nval):
                continue

            nd = distance.get(pos) + 1
            if not npos in distance:
                distance[npos] = nd
                queue.append(npos)

    return distance[pos]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            txt = f.read()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    mymap = txt.splitlines()
    print("Part1:", bfs(mymap, "S", "E", lambda old, new: ord(new) - ord(old) > 1))
    print("Part2:", bfs(mymap, "E", "a", lambda old, new: ord(old) - ord(new) > 1))
