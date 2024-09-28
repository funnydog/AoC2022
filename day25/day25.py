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
        print(f"cannot open {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)

    def snafu_to_int(snafu: str) -> int:
        dct = "=-012"
        value = 0
        for v in snafu:
            value = value*5 + dct.index(v)-2
        return value

    def int_to_snafu(value: int) -> str:
        dct = "012=-"
        snafu = ""
        while value:
            rem = value % 5
            value //= 5
            snafu = dct[rem] + snafu
            if rem > 2:
                value += 1
        return snafu

    print("Part1:", int_to_snafu(sum(map(snafu_to_int, lines))))
