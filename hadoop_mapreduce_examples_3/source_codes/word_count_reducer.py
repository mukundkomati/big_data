#!/usr/bin/env python3
import sys

def wordcount_reducer():
    """Reducer function for WordCount."""
    current_word = None
    current_count = 0

    for line in sys.stdin:
        # Split the input line into word and count
        word, count = line.strip().split('\t')
        count = int(count)
        
        # If the word changes (new word), print the count for the previous word
        if current_word == word:
            current_count += count
        else:
            if current_word is not None:
                print(f"{current_word}\t{current_count}")
            current_word = word
            current_count = count

    # Print the last word count
    if current_word is not None:
        print(f"{current_word}\t{current_count}")

if __name__ == "__main__":
    wordcount_reducer()
