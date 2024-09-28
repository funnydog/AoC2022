#!/usr/bin/env python3

import sys

FILE_TYPE = "f"
DIR_TYPE = "d"

class INode(object):
    def __init__(self, typ, size = 0):
        self.parent = None
        self.typ = typ
        self.size = size
        self.entries = {}

    def add_child(self, name, obj):
        assert self.typ == DIR_TYPE, "Trying to add an object to another file"
        self.entries[name] = obj
        obj.parent = self

    def get_parent(self):
        return self.parent

    def get_child(self, name):
        return self.entries[name]

    def get_size(self):
        if not self.size:
            self.size = sum(x.get_size() for x in self.entries.values())
        return self.size

def preorder(inode, fn):
    for name, obj in inode.entries.items():
        fn(obj)
        preorder(obj, fn)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            txt = f.read()
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    cur = root = INode(DIR_TYPE)
    for line in txt.splitlines():
        values = line.split()
        if values[0] == "$":
            # commands
            if values[1] == "cd":
                if values[2] == "/":
                    cur = root
                elif values[2] == "..":
                    cur = cur.get_parent()
                else:
                    cur = cur.get_child(values[2])
            elif values[1] == "ls":
                pass
        else:
            # contents
            if values[0] == "dir":
                child = INode(DIR_TYPE, None)
            else:
                child = INode(FILE_TYPE, int(values[0]))
            cur.add_child(values[1], child)

    size = 0
    def part1(obj):
        global size
        if obj.typ == DIR_TYPE:
            dsize = obj.get_size()
            if dsize <= 100000:
                size += dsize

    preorder(root, part1)
    print("Part1:", size)

    needed_space = 30000000 - (70000000 - root.get_size())
    minsize = 70000000
    def part2(obj):
        global lowest, minsize
        if obj.typ == DIR_TYPE:
            dsize = obj.get_size()
            if dsize >= needed_space and dsize < minsize:
                minsize = dsize

    preorder(root, part2)
    print("Part2:", minsize)


