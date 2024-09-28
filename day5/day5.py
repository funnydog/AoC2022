#!/usr/bin/env python3

import sys

def parse(data):
    state = 0
    stackmap = {}
    instructions = []
    for row, line in enumerate(data.splitlines()):
        if state == 0:
            if line == "":
                state = 1
            else:
                i = line.find("[")
                while i >= 0:
                    col = i // 4
                    stackmap[col, row] = line[i+1]
                    i = line.find("[", i+1)
        else:
            values = line.split()
            instructions.append((int(values[1]), int(values[3]), int(values[5])))

    stacks = [[] for x in range(col+1)]
    for y in range(row):
        for x in range(col+1):
            y1 = row-y-1
            if (x, y1) in stackmap:
                stacks[x].append(stackmap[x, y1])

    return stacks, instructions

def top(stacks):
    v = []
    for s in stacks:
        if s:
            v.append(s[-1])
    return "".join(v)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        printf(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "rt") as f:
        data = f.read()

    initial, instructions = parse(data)

    stacks = [x[:] for x in initial]
    for count, src, dst in instructions:
        for _ in range(count):
            stacks[dst-1].append(stacks[src-1].pop())
    part1 = top(stacks)

    stacks = initial
    for count, src, dst in instructions:
        tmp = stacks[src-1][-count:]
        stacks[src-1] = stacks[src-1][:-count]
        stacks[dst-1].extend(tmp)
    part2 = top(stacks)

    print("Part1:", part1)
    print("Part2:", part2)
