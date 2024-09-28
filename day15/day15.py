#!/usr/bin/env python3

import re
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

    if sys.argv[1] == "test":
        part1_y = 10
        part2_side = 20
    else:
        part1_y = 2000000
        part2_side = 4000000

    r = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    sensors = []
    for line in txt.splitlines():
        match = r.match(line)
        if match:
            sensors.append(tuple(int(x) for x in match.groups()))

    # compute the intervals covered by the sensors at the line part1_y
    intervals = []
    for sx, sy, bx, by in sensors:
        d = abs(bx-sx)+abs(by-sy)
        if sy - d <= part1_y <= sy + d:
            d -= abs(part1_y-sy)
            intervals.append((sx - d, sx + d))

    intervals.sort()
    count = 0
    pos = intervals[0][0]-1
    for start, end in intervals:
        if end < pos:
            pass
        elif start <= pos <= end:
            count += end - pos
            pos = end
        else:
            count += end - start+1
            pos = end

    # remove the spaces already occupied by beacons
    beacons = set((bx, by) for _, _, bx, by in sensors)
    for bx, by in beacons:
        if by == part1_y:
            count -= 1
    print("Part1:", count)

    # check if the point is outside the sensors coverage
    def outside(p, sensors):
        x, y = p
        for s in sensors:
            sx, sy, bx, by = s
            d0 = abs(bx-sx) + abs(by-sy)
            d1 = abs(x-sx) + abs(y-sy)
            if d1 <= d0:
                return False
        return True

    # intersection of segments
    def intersect(s1, s2):
        (x1, y1), (x2, y2) = s1
        (x3, y3), (x4, y4) = s2

        if (x1 == x2 and y1 == y2) or (x3 == x4 and y3 == y4):
            return None

        den = ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        numa = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3))
        numb = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3))
        if den == 0:
            return None

        if 0 <= numa <= den and 0 <= numb <= den:
            return (x1 + numa * (x2 - x1) // den,
                    y1 + numa * (y2 - y1) // den)

        return None

    # any point of interest is in the intersection of the outside
    # perimeters of each sensor
    def find_inside(segments, cliprect):
        for i, s1 in enumerate(segments):
            for j in range(i+1, len(segments)):
                s2 = segments[j]
                p = intersect(s1, s2)
                if p \
                   and cliprect[0] <= p[0] <= cliprect[2] \
                   and cliprect[1] <= p[1] <= cliprect[3] \
                   and outside(p, sensors):
                    return p
        return None

    # build a list of segments for the outside perimeter of each sensor
    segments = []
    for sx, sy, bx, by in sensors:
        d = abs(bx-sx) + abs(by-sy)
        p0 = (sx, sy - d - 1)
        p1 = (sx + d + 1, sy)
        p2 = (sx, sy + d + 1)
        p3 = (sx - d - 1, sy)
        segments.append((p0, p1))
        segments.append((p1, p2))
        segments.append((p2, p3))
        segments.append((p3, p0))

    p = find_inside(segments, (0, 0, part2_side, part2_side))
    if p:
        print("Part2:", p[0] * 4000000 + p[1])
