#!/usr/bin/env python3
import re
import sys

def map_function():
    """Map function to read log entries from standard input and output (hour, ip) pairs."""
    pattern = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?\d{4}:(?P<hour>\d{2}):\d{2}.*?')

    for line in sys.stdin:
        match = pattern.search(line)
        if match:
            ip = match.group('ip')
            hour = match.group('hour')
            # Output the (hour, ip) pairs
            print(f"{hour}\t{ip}")

if __name__ == "__main__":
    map_function()
