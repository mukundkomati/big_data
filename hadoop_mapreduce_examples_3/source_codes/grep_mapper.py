#!/usr/bin/env python3
import sys
import re

def grep_mapper(pattern):
    """Mapper function for Grep. Outputs lines containing the specified pattern."""
    regex = re.compile(pattern)

    for line in sys.stdin:
        line = line.strip()
        if regex.search(line):  # Check if the line contains the pattern
            print(line)  # Output the matching line

if __name__ == "__main__":
    # Example pattern; change this to any desired pattern
    pattern = sys.argv[1] if len(sys.argv) > 1 else "Hadoop"
    grep_mapper(pattern)
