#!/usr/bin/env python
import sys
from collections import defaultdict

# Dictionary to store local counts of words
local_word_count = defaultdict(int)

# Input comes from standard input (stdin)
for line in sys.stdin:
    word, count = line.strip().split('\t')
    local_word_count[word] += int(count)

# Output each word with its local count
for word, count in local_word_count.items():
    print(f"{word}\t{count}")

