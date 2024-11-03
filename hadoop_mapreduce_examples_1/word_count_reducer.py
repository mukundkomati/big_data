#!/usr/bin/env python
import sys

current_word = None
current_count = 0

# Input comes from standard input (stdin)
for line in sys.stdin:
    # Read each line, which contains a word and its count
    word, count = line.strip().split('\t')
    count = int(count)
    
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # Output the count for the previous word
            print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = count

# Output the count for the last word
if current_word == word:
    print(f"{current_word}\t{current_count}")

