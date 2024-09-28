#!/usr/bin/env python3
from typing import Union

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

    monkeys: dict[str, Union[int, list[str]]] = {}
    for line in lines:
        semi = line.find(":")
        if semi < 0:
            continue

        name = line[:semi]
        value = line[semi+1:].strip()
        if value[0] in "0123456789":
            monkeys[name] = int(value)
        else:
            monkeys[name] = value.split()

    # topological sort of the monkey graph
    parent: dict[str, str] = {}
    array: list[str] = []
    def dfs(name: str) -> None:
        global monkeys, parent, array

        value = monkeys[name]
        if isinstance(value, list):
            a, _, b = value

            if not a in parent:
                parent[a] = name
                dfs(a)
            if not b in parent:
                parent[b] = name
                dfs(b)

        array.append(name)
    dfs("root")

    # execution in topological order
    values: dict[str, int] = {}
    for name in array:
        instr = monkeys[name]
        result: int
        if isinstance(instr, list):
            a, op, b = instr
            if op == "+":
                result = values[a] + values[b]
            elif op == "-":
                result = values[a] - values[b]
            elif op == "*":
                result = values[a] * values[b]
            elif op == "/":
                result = values[a] // values[b]
            else:
                assert False, "Unknown op"
        else:
            result = instr

        values[name] = result

    print("Part1:", values["root"])

    # remove the values of the monkeys depending on humn
    branch = "humn"
    while branch != "root":
        del values[branch]
        branch = parent[branch]
    del values["root"]

    # remove the independent monkeys from the array
    array.remove("humn")
    for k in values.keys():
        array.remove(k)

    # reverse the computation from root to humn
    t = 0
    for name in reversed(array):
        instr = monkeys[name]
        assert isinstance(instr, list)
        a, op, b = instr
        if name == "root":
            # va = vb
            if a is values:
                t = values[a]
            else:
                t = values[b]
        elif op == "+":
            # t = va + vb => { va = t - vb,  vb = t - va }
            if a in values:
                t -= values[a]
            else:
                t -= values[b]
        elif op == "*":
            # t = va * vb => { va = t // vb, vb = t // va }
            if a in values:
                t //= values[a]
            else:
                t //= values[b]
        elif op == "-":
            # t = va - vb => { va = t + vb, vb = va - t }
            if a in values:
                t = values[a] - t
            else:
                t = t + values[b]
        elif op == "/":
            # t = va // vb => { va = t * vb, vb = va // t }
            if a in values:
                t = values[a] // t
            else:
                t = values[b] * t

    print("Part2:", t)
