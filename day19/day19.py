#!/usr/bin/env python3
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            lines = f.read().strip().splitlines()
    except Exception as e:
        print(f"cannot open {sys.argv[1] }", file=sys.stderr)
        sys.exit(1)

    ORE, CLAY, OBSIDIAN, GEODE = 0, 1, 2, 3

    def add(a, b):
        return tuple(a[i]+b[i] for i in range(4))

    def greater_equal(a, b):
        return all(a[i] >= b[i] for i in range(4))

    def sub(a, b):
        return tuple(a[i]-b[i] for i in range(4))

    def scale(a, b):
        return tuple(a[i]*b for i in range(4))

    def dot(a, b):
        return sum(a[i]*b[i] for i in range(4))

    def max_geodes(blueprints, time_budget):
        identity = [
            (1, 0, 0, 0),
            (0, 1, 0, 0),
            (0, 0, 1, 0),
            (0, 0, 0, 1)
        ]
        stack = [(
            0,                  # time
            (0, 0, 0, 0),       # materials
            (1, 0, 0, 0),       # robots
        )]
        best = 0
        while stack:
            time, materials, robots = stack.pop()
            if time == time_budget:
                if best < materials[GEODE]:
                    best = materials[GEODE]
                continue

            time_left = time_budget - time
            if materials[GEODE] + robots[GEODE] * time_left + time_left * (time_left+1) // 2 < best:
                continue

            for i in range(4-1, -1, -1):
                blueprint = blueprints[i]
                dt = -1
                for j in range(4):
                    if not blueprint[j]:
                        pass
                    elif not robots[j]:
                        dt = -1
                        break
                    else:
                        d = (blueprint[j] - materials[j] + robots[j] - 1) // robots[j]
                        if dt < d:
                            dt = d

                if dt < 0:
                    continue

                if time + dt >= time_budget:
                    stack.append((
                        time_budget,
                        add(materials, scale(robots, time_budget - time)),
                        robots
                    ))
                else:
                    stack.append((
                        time + dt + 1,
                        sub(add(materials, scale(robots, dt+1)), blueprint),
                        add(robots, identity[i])
                    ))

        return best

    blueprint = re.compile(r"^Blueprint (\d+):")
    robot = re.compile(r"Each (ore|clay|obsidian|geode) robot costs ([^.]*)\.")
    names = ["ore", "clay", "obsidian", "geode"]

    lst = []
    for line in lines:
        m = re.match(blueprint, line)
        if not m:
            continue
        blueprint_id = int(m.group(1))

        blueprints = [[0]*4 for i in range(4)]
        for name, materials in re.findall(robot, line):
            row = blueprints[names.index(name)]
            for material in materials.split(" and "):
                splitted = material.split()
                row[names.index(splitted[1])] = int(splitted[0])

        lst.append((blueprint_id, blueprints))

    quality = 0
    for bid, blueprints in lst:
        geodes = max_geodes(blueprints, 24)
        quality += bid * geodes

    print("Part1:", quality)

    part2 = 1
    for bid, blueprints in lst[:3]:
        geodes = max_geodes(blueprints, 32)
        part2 *= geodes

    print("Part2:", part2)
