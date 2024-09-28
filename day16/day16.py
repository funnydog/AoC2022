#!/usr/bin/env python3

import re
import sys

from itertools import permutations

class Node(object):
    def __init__(self, flow_rate, edges):
        self.flow_rate = flow_rate
        self.edges = edges

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

    graph = {}
    pat = re.compile(r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)")
    for line in txt.splitlines():
        match = pat.match(line)
        if match:
            name = match.group(1)
            flow_rate = int(match.group(2))
            tunnels = match.group(3).split(", ")
            graph[name] = Node(flow_rate, tunnels)

    # BFS to compute the distance
    def bfs(graph, start):
        queue = [start]
        distance = {start: 0}
        while queue:
            valve = queue.pop(0)
            for dst in graph[valve].edges:
                if not dst in distance:
                    distance[dst] = distance[valve] + 1
                    queue.append(dst)

        return distance

    distance = {}
    candidates = list(graph.keys())
    for i, start in enumerate(candidates):
        dmap = bfs(graph, start)
        for end in candidates[i+1:]:
            distance[start, end] = distance[end, start] = dmap[end]

    maxflow = 0
    candidates = set(name for name, node in graph.items() if node.flow_rate > 0)
    def backtrack(graph, array, time, candidates, fr):
        global distance, maxflow

        deadlock = True
        for name in candidates:
            elapsed = distance[array[-1], name] + 1
            if time >= elapsed:
                deadlock = False
                candidates.remove(name)
                array.append(name)
                backtrack(
                    graph,
                    array, time - elapsed,
                    candidates,
                    fr + (time - elapsed) * graph[name].flow_rate
                )
                array.pop()
                candidates.add(name)

        if deadlock and maxflow < fr:
            maxflow = fr

    backtrack(graph, ["AA"], 30, candidates, 0)
    print("Part1:", maxflow)

    maxflow = 0
    def bt2(graph, a1, t1, a2, t2, fr, candidates):
        global distance, maxflow

        a1_cands = sorted(candidates, key = lambda x: distance[a1[-1], x])
        a2_cands = sorted(candidates, key = lambda x: distance[a2[-1], x])
        est1 = sum((t1 - i) * graph[x].flow_rate for i, x in enumerate(a1_cands, 1) if t1-i > 0)
        est2 = sum((t2 - i) * graph[x].flow_rate for i, x in enumerate(a2_cands, 1) if t2-i > 0)
        if max(est1, est2) + fr < maxflow:
            return

        deadlock = True
        for i in range(len(candidates)):
            if t1 >= t2:
                el1 = a1_cands[i]
                et1 = distance[a1[-1], el1] + 1
                candidates.remove(el1)
                if t1 > et1:
                    deadlock = False
                    a1.append(el1)
                    bt2(graph, a1, t1-et1, a2, t2, fr + (t1 - et1) * graph[el1].flow_rate, candidates)
                    a1.pop()
                candidates.add(el1)

            if t2 >= t1:
                el2 = a2_cands[i]
                et2 = distance[a2[-1], el2] + 1
                candidates.remove(el2)
                if t2 > et2:
                    deadlock = False
                    a2.append(el2)
                    bt2(graph, a1, t1, a2, t2-et2, fr + (t2 - et2) * graph[el2].flow_rate, candidates)
                    a2.pop()
                candidates.add(el2)

        if deadlock:
            if maxflow < fr:
                maxflow = fr

    bt2(graph, ["AA"], 26, ["AA"], 26, 0, candidates)
    print("Part2:", maxflow)
