#!/usr/bin/env python3
import sys
import re

def map_function(time_period):
    """Map function to read the log file and output (time_period, ip) pairs."""
    # Regular expression to match IP addresses and timestamps
    pattern = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?\d{4}:(?P<hour>\d{2}):\d{2}.*?')
    
    start_hour, end_hour = map(int, time_period.split('-'))

    for line in sys.stdin:
        match = pattern.search(line)
        if match:
            ip = match.group('ip')
            hour = int(match.group('hour'))

            # Check if the hour is within the specified time period
            if start_hour <= hour < end_hour:
                # Output the (time_period, ip) pair
                print(f"{time_period}\t{ip}")

if __name__ == "__main__":
    # Read time period from command-line arguments
    if len(sys.argv) != 2:
        print("Usage: topk_timeperiod_mapper.py <time_period>")
        sys.exit(1)
    
    time_period = sys.argv[1]
    map_function(time_period)
