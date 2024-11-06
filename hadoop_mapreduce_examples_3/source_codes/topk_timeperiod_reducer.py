#!/usr/bin/env python3
import sys
from collections import defaultdict, Counter

def reduce_function(K=5):
    """Reduce function to read (time_period, ip) pairs from standard input and find the top K IPs."""
    hourly_ip_count = defaultdict(Counter)

    for line in sys.stdin:
        time_period, ip = line.strip().split('\t')
        # Count occurrences of each IP for each time period
        hourly_ip_count[time_period][ip] += 1

    # Output the top K IPs for each time period
    for time_period, ip_counts in hourly_ip_count.items():
        top_ips = ip_counts.most_common(K)
        for ip, count in top_ips:
            print(f"{time_period}\t{ip}")

if __name__ == "__main__":
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 5  # Get K from command-line argument
    reduce_function(K)
