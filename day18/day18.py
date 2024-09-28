#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            lines = f.read().strip().splitlines()
    except Exception as e:
        print(f"cannot open { sys.argv[1] }", file=sys.stderr)
        sys.exit(1)

    grid = set()
    for line in lines:
        pos = tuple(map(int, line.split(",")))
        grid.add(pos)

    offsets = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]
    sides = 0
    for (x, y, z) in grid:
        for dx, dy, dz in offsets:
            sides += (x+dx,y+dy,z+dz) in grid

    surface = len(grid)*6 - sides
    print("Part1:", surface)

    # find the size of an enclosing cube not touching any of the lava
    x0 = y0 = z0 = 100
    x1 = y1 = z1 = 0
    for x, y, z in grid:
        if x0 > x-1: x0 = x-1
        if y0 > y-1: y0 = y-1
        if z0 > z-1: z0 = z-1
        if x1 < x+1: x1 = x+1
        if y1 < y+1: y1 = y+1
        if z1 < z+1: z1 = z+1

    # compute the surface by counting the times we touch the grid
    surface = 0
    shell = set()
    queue = [(x0, y0, z0)]
    while queue:
        x, y, z = queue.pop(0)
        for dx, dy, dz in offsets:
            nx = x + dx
            ny = y + dy
            nz = z + dz
            np = (nx, ny, nz)
            if nx < x0 or nx > x1 or ny < y0 or ny > y1 or nz < z0 or nz > z1:
                pass
            elif np in grid:
                surface += 1
            elif np in shell:
                pass
            else:
                shell.add(np)
                queue.append(np)

    print("Part2:", surface)
