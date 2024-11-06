#!/usr/bin/env python3
import sys

def sort_reducer():
    """Reducer function for Sort."""
    for line in sys.stdin:
        # Output each sorted word as is
        word, _ = line.strip().split('\t')
        print(word)

if __name__ == "__main__":
    sort_reducer()
