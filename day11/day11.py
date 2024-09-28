#!/usr/bin/env python3

import sys

class Monkey(object):
    def __init__(self):
        self.starting_items = []
        self.items = []
        self.op = None
        self.divisor = None
        self.true_index = None
        self.false_index = None
        self.inspected = 0

    def prepare(self):
        self.items = self.starting_items[:]
        self.inspected = 0

    def execute(self, monkeys, modulo):
        self.inspected += len(self.items)
        items, self.items = self.items, []
        while items:
            item = items.pop()
            if self.op[1] == "old":
                item *= item
            elif self.op[0] == "*":
                item *= self.op[1]
            elif self.op[0] == "+":
                item += self.op[1]
            else:
                print("Unknown op!", self.op)
                break

            if modulo:
                item %= modulo
            else:
                item //= 3

            if item % self.divisor == 0:
                dst = self.true_index
            else:
                dst = self.false_index

            monkeys[dst].items.append(item)

def monkey_business(monkeys, rounds, modulo):
    for m in monkeys:
        m.prepare()
    for _ in range(rounds):
        for m in monkeys:
            m.execute(monkeys, modulo)
    inspected = sorted([m.inspected for m in monkeys], key=lambda x: -x)
    return inspected[0] * inspected[1]

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

    modulo = 1
    monkeys = []
    cur = None
    for line in txt.splitlines():
        value = line.split()
        if not value:
            pass
        elif value[0] == "Monkey":
            cur = Monkey()
            monkeys.append(cur)
        elif value[0] == "Starting":
            for s in "".join(value[2:]).split(","):
                cur.starting_items.append(int(s))
        elif value[0] == "Operation:":
            if value[5] == "old":
                cur.op = value[4:]
            else:
                cur.op = [value[4], int(value[5])]
        elif value[0] == "Test:":
            cur.divisor = int(value[3])
            modulo *= cur.divisor
        elif value[0] == "If":
            if value[1] == "true:":
                cur.true_index = int(value[5])
            elif value[1] == "false:":
                cur.false_index = int(value[5])

    print("Part1:", monkey_business(monkeys, 20, 0))
    print("Part2:", monkey_business(monkeys, 10000, modulo))
