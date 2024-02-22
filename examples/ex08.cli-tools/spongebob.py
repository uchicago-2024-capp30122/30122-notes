#!/usr/bin/env python3

import sys


def alt_case(text):
    result = ""
    for i, char in enumerate(text):
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result


if __name__ == "__main__":
    # stdin is a file-like object that we can read from
    print("an error occurred", file=sys.stderr)
    for line in sys.stdin:
        print(alt_case(line))
