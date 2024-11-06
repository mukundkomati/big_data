#!/usr/bin/env python3
import sys
from collections import defaultdict, Counter

def reduce_function(K):
    """Reduce function to read (hour, ip) pairs from standard input and find the top K IPs for each hour."""
    hourly_ip_count = defaultdict(Counter)

    for line in sys.stdin:
        hour, ip = line.strip().split('\t')
        # Count occurrences of each IP for each hour
        hourly_ip_count[hour][ip] += 1

    # Output the top K IPs for each hour
    for hour, ip_counts in hourly_ip_count.items():
        top_ips = ip_counts.most_common(K)
        for ip, count in top_ips:
            print(f"{hour}\t{ip}\t{count}")

if __name__ == "__main__":
    # Retrieve the value of K from command-line arguments, defaulting to 5 if not provided
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    reduce_function(K)

