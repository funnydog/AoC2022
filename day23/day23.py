#!/usr/bin/env python3
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

    # potential movements of the elves
    MOVEMENTS = [
        [(-1,-1), (0,-1), (1,-1)],  # N
        [(1,1), (0,1), (-1,1)],     # S
        [(-1,1), (-1,0), (-1,-1)],  # W
        [(1,-1), (1,0), (1,1)],     # E
    ]
    MOVEMENTS += MOVEMENTS

    def make_turn(turn: int,
                  elves: list[tuple[int,int]],
                  grove: dict[tuple[int,int],bool],
                  dest: dict[tuple[int,int],bool]) -> None:

        # movements in order of preference
        start_at = turn % 4
        movements = MOVEMENTS[start_at:start_at+4]

        # find the potential new position
        ngrove: dict[tuple[int,int],int] = {}
        chosen: list[tuple[int,int]] = []
        for elf in elves:
            # find the new position of the elf
            pos = elf
            allowed: list[tuple[int,int]] = []
            for places in movements:
                for dx, dy in places:
                    npos = (elf[0]+dx, elf[1]+dy)
                    if grove.get(npos, False):
                        break
                else:
                    allowed.append(places[1])

            if allowed and len(allowed) < 4:
                pos = (elf[0]+allowed[0][0], elf[1]+allowed[0][1])

            # track the number of elves in the new position
            ngrove[pos] = ngrove.get(pos, 0) + 1
            chosen.append(pos)

        # make movements
        dest.clear()
        for i, choice in enumerate(chosen):
            if ngrove.get(choice, 0) < 2:
                elves[i] = choice
            dest[elves[i]] = True

    # convert the map into a sparse map and collect the positions of
    # the elves
    grove: dict[tuple[int,int],bool] = {}
    elves: list[tuple[int,int]] = []
    for y, row in enumerate(lines):
        for x, v in enumerate(row):
            if v == "#":
                grove[x, y] = True
                elves.append((x, y))

    # execute the first 10 turns
    i = 0
    prev: dict[tuple[int,int],bool] = {}
    while i < 10:
        prev, grove = grove, prev
        make_turn(i, elves, prev, grove)
        i += 1

    # count the free cells in the grove
    min_x = min_y = 100000000
    max_x = max_y = 0
    for x, y in grove.keys():
        if min_x > x: min_x = x
        if max_x < x: max_x = x
        if min_y > y: min_y = y
        if max_y < y: max_y = y

    count = (max_x + 1 - min_x) * (max_y + 1 - min_y) - len(grove)

    print("Part1:", count)

    # run until the grove doesn't change anymore
    while grove != prev:
        prev, grove = grove, prev
        make_turn(i, elves, prev, grove)
        i += 1

    print("Part2:", i)
