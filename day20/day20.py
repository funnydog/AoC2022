#!/usr/bin/env python3
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

    numbers = [int(x) for x in lines]

    def decrypt(numbers: list[int], times: int) -> int:
        count = len(numbers)
        right = [(i+1)%count for i in range(count)]
        left  = [(i-1)%count for i in range(count)]
        while times > 0:
            times -= 1

            for j, num in enumerate(numbers):
                if num != 0:
                    # remove the number
                    right[left[j]] = right[j]
                    left[right[j]] = left[j]

                    # find the new position
                    t = j
                    for k in range(num % (count-1)):
                       t = right[t]

                    # insert j at the new position
                    right[j] = right[t]
                    left[j] = t
                    right[left[j]] = j
                    left[right[j]] = j

        result = 0
        zero = numbers.index(0)
        for j in 1000, 2000, 3000:
            t = zero
            for k in range(j % count):
                t = right[t]

            result += numbers[t]

        return result

    print("Part1:", decrypt(numbers, 1))

    numbers = [n * 811589153 for n in numbers]
    print("Part2:", decrypt(numbers, 10))
