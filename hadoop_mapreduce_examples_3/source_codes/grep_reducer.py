#!/usr/bin/env python3
import sys

def grep_reducer():
    """Reducer function for Grep. Forwards each line it receives."""
    for line in sys.stdin:
        print(line.strip())  # Output each line as is

if __name__ == "__main__":
    grep_reducer()
