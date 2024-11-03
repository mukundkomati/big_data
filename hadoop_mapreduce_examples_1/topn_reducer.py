#!/usr/bin/env python3
import sys
from collections import defaultdict, Counter

def reduce_function(K=5):
    """Reduce function to read word count pairs and find the top K words."""
    word_count = defaultdict(int)

    # Count occurrences of each word
    for line in sys.stdin:
        word, count = line.strip().split('\t')
        word_count[word] += int(count)

    # Sort words by frequency (descending)
    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    # Output the top K words and their counts
    for word, count in sorted_word_count[:K]:
        print(f"{word}\t{count}")

if __name__ == "__main__":
    # Check if K is provided via command-line arguments
    if len(sys.argv) > 1:
        K = int(sys.argv[1])  # Retrieve K from command-line arguments
    else:
        K = 5  # Default value if not provided

    reduce_function(K)

