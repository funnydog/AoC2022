#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            txt = f.read()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    mymap = {}
    for line in txt.splitlines():
        path = []
        coords = line.split(" -> ")
        for coord in coords:
            values = coord.split(",")
            path.append((int(values[0]), int(values[1])))

        # draw the path
        x0, y0 = path.pop(0)
        while path:
            x1, y1 = path.pop(0)
            dx = (x1 > x0) - (x1 < x0)
            dy = (y1 > y0) - (y1 < y0)
            while x0 != x1 or y0 != y1:
                mymap[x0, y0] = "#"
                x0 += dx
                y0 += dy

            mymap[x0, y0] = "#"
            x0, y0 = x1, y1

    bottom = 0
    for _, y in mymap.keys():
        if bottom < y:
            bottom = y

    count = 0
    while True:
        x, y = 500, 0
        while True:
            while y < bottom and not (x, y+1) in mymap:
                y += 1
            if y == bottom:
                break
            elif not (x-1, y+1) in mymap:
                x -= 1
            elif not (x+1, y+1) in mymap:
                x += 1
            else:
                break
        if y == bottom:
            break
        count += 1
        mymap[x, y] = "o"
        # for y in range(10):
        #     for x in range(494, 504):
        #         print(mymap.get((x, y), "."), end = "")
        #     print()

    print("Part1:", count)

    bottom += 2
    while True:
        x, y = 500, 0
        while True:
            while y+1 != bottom and not (x, y+1) in mymap:
                y += 1
            if y+1 == bottom:
                break
            elif not (x-1, y+1) in mymap:
                x -= 1
            elif not (x+1, y+1) in mymap:
                x += 1
            else:
                break
        count += 1
        mymap[x, y] = "o"
        if mymap.get((500,0)):
            break
        # for y in range(12):
        #     for x in range(470, 530):
        #         if y == bottom:
        #             print("#", end="")
        #         else:
        #             print(mymap.get((x, y), "."), end = "")
        #     print()

    print("Part2:", count)
