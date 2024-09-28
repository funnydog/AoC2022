#!/usr/bin/env python3

import sys

class MCU(object):
    def __init__(self):
        self.xreg = 1
        self.cycles = 0
        self.signal_strength = 0
        self.screen = ["."] * 240

    def update(self, cycles):
        for _ in range(cycles):
            if self.xreg - 1 <= self.cycles % 40 <= self.xreg + 1:
                self.screen[self.cycles % 240] = "#"

            self.cycles += 1
            if self.cycles <= 220 and (self.cycles + 20) % 40 == 0:
                self.signal_strength += self.xreg * self.cycles

    def execute(self, line):
        args = line.split()
        if args[0] == "noop":
            self.update(1)
        elif args[0] == "addx":
            self.update(2)
            self.xreg += int(args[1])
        else:
            pass

    def __str__(self):
        return "\n".join("".join(self.screen[x:x+40]) for x in range(0, 240, 40))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    mcu = MCU()
    try:
        with open(sys.argv[1], "rt") as f:
            for line in f:
                mcu.execute(line)

        print("Part1:", mcu.signal_strength)
        print("Part2:")
        print(mcu)
    except Exception as e:
        print(e)
        sys.exit(1)
