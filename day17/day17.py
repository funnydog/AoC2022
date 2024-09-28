#!/usr/bin/env python3

import sys
import time

class Map(object):
    SHAPES = [
        ["####"],
        [".#.", "###", ".#."],
        ["###", "..#", "..#"],
        ["#", "#", "#", "#"],
        ["##", "##"],
    ]

    def __init__(self, jet):
        self.height = 0
        self.data = {}
        self.jet = jet
        self.jet_index = 0
        self.rock_index = 0

    def update(self, rock, x0, y0):
        for y, row in enumerate(rock, y0):
            for x, value in enumerate(row, x0):
                if value == "#":
                    self.data[x, y] = "#"

        y0 += len(rock)
        if self.height < y0:
            self.height = y0

    def get_rock_position(self):
        return (2, self.height + 3)

    def collision(self, rock, x0, y0):
        if y0 < 0:
            return True
        for y, row in enumerate(rock, y0):
            for x, value in enumerate(row, x0):
                if value == "#":
                    if x < 0 or x >= 7:
                        return True
                    elif (x, y) in self.data:
                        return True
        return False

    def fall_shape(self):
        rock = self.SHAPES[self.rock_index]
        self.rock_index = (self.rock_index + 1) % len(self.SHAPES)

        x, y = 2, self.height + 3
        while True:
            # move
            move = self.jet[self.jet_index]
            self.jet_index = (self.jet_index + 1) % len(txt)

            if move == ">":
                nx = x + 1
            elif move == "<":
                nx = x - 1
            else:
                assert False, "'{}'".format(move)

            # collision check
            if not self.collision(rock, nx, y):
                x = nx

            # move down
            ny = y - 1
            if self.collision(rock, x, ny):
                break

            y = ny

        self.update(rock, x, y)
        return self.height

    def __str__(self):
        data = []
        for y in range(self.height, -1, -1):
            data.append("|")
            for x in range(width):
                data.append(mymap.get((x, y), "."))
            data.append("|\n")
        data.append("+-------+")
        return "".join(data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            txt = f.read().strip()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    index = 0
    jet = 0
    mymap = Map(txt)
    for _ in range(2022):
        mymap.fall_shape()

    print("Part1:", mymap.height)

    def fn(mymap):
        while True:
            mymap.fall_shape()
            if mymap.rock_index == 0:
                break
        return mymap

    tortoise = Map(txt)
    hare = Map(txt)
    tortoise = fn(tortoise)
    hare = fn(fn(hare))
    while tortoise.jet_index != hare.jet_index:
        tortoise = fn(tortoise)
        hare = fn(fn(hare))

    mu = 0
    tortoise = Map(txt)
    while tortoise.jet_index != hare.jet_index:
        tortoise = fn(tortoise)
        hare = fn(hare)
        mu += 1

    lam = 1
    tortoise = fn(tortoise)
    while tortoise.jet_index != hare.jet_index:
        tortoise = fn(tortoise)
        lam += 1

    cycles = (1000000000000 - mu * 5)
    residual = cycles % (lam * 5)
    cycles //= (lam * 5)

    test = Map(txt)
    for _ in range(mu):
        test = fn(test)
    h1 = test.height

    for _ in range(lam):
        test = fn(test)
    h2 = test.height

    for _ in range(residual):
        test.fall_shape()
    h3 = test.height

    print("Part2:", h1 + (h2 - h1) * cycles + (h3 - h2))
