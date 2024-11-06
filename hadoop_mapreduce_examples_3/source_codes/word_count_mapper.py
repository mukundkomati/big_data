#!/usr/bin/env python3
import sys

def wordcount_mapper():
    """Mapper function for WordCount."""
    for line in sys.stdin:
        # Strip whitespace and split the line into words
        words = line.strip().split()
        # Emit each word with a count of 1
        for word in words:
            print(f"{word}\t1")

if __name__ == "__main__":
    wordcount_mapper()
