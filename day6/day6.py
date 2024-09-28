#!/usr/bin/env python3

value = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
value = "bvwbjplbgvbhsrlpgdmjqwftvncz"

def has_repetitions(buf):
    for i in range(len(buf)):
        for j in range(i+1, len(buf)):
            if buf[i] == buf[j]:
                return True
    return False

def last_marker_index(value, length = 4):
    buf = list(value[:length])
    for i, c in enumerate(value[length:], length):
        buf[i % length] = c
        if not has_repetitions(buf):
            return i + 1

    return None

assert last_marker_index("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
assert last_marker_index("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
assert last_marker_index("nppdvjthqldpwncqszvftbrmjlhg") == 6
assert last_marker_index("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
assert last_marker_index("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

assert last_marker_index("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
assert last_marker_index("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
assert last_marker_index("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
assert last_marker_index("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
assert last_marker_index("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26


import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "rt") as f:
        txt = f.read()

    print("Part1: ", last_marker_index(txt))
    print("Part2: ", last_marker_index(txt, 14))
