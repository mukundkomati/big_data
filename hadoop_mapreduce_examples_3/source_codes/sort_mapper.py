#!/usr/bin/env python3
import sys

def sort_mapper():
    """Mapper function for Sort."""
    for line in sys.stdin:
        # Strip any trailing whitespace and emit each word as the key with a placeholder value
        word = line.strip()
        print(f"{word}\t1")

if __name__ == "__main__":
    sort_mapper()
