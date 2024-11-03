#!/usr/bin/env python
import sys
import re

# Input comes from standard input (stdin)
for line in sys.stdin:
    # Remove punctuation and numbers, and convert to lowercase
    line = re.sub(r'[^a-zA-Z\s]', '', line).lower()
    
    # Split the line into words
    words = line.split()
    
    # Output each word with count 1
    for word in words:
        print(f"{word}\t1")

