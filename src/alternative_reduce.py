#!/usr/bin/env python3

# ---- Command line args ----
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths', nargs='+', required=True)
parser.add_argument('--output_path', required=True)
parser.add_argument('--hashtags', nargs='+', required=True)
args = parser.parse_args()

# ---- Imports ----
import os
import json
import glob
import re
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt

results = defaultdict(dict)

for pattern in args.input_paths:
    matched_files = glob.glob(pattern)

    if not matched_files:
        print(f"No files matched pattern: {pattern}")

    for path in matched_files:

        filename = os.path.basename(path)

        match = re.search(r'geoTwitter20-(\d{2}-\d{2})\.zip\.lang', filename)

        date = "2020-" + match.group(1)

        with open(path) as f:
            data = json.load(f)

        for hashtag in args.hashtags:
            if hashtag in data:
                total_count = sum(data[hashtag].values())
            else:
                total_count = 0

            results[hashtag][date] = total_count

# ---- Write Combined JSON ----
with open(args.output_path, 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# ---- Plot ----
plt.figure(figsize=(10, 6))

for hashtag, date_counts in results.items():

    if not date_counts:
        continue

    sorted_dates = sorted(date_counts.keys())

    import matplotlib.dates as mdates
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in sorted_dates]
    counts = [date_counts[d] for d in sorted_dates]

    plt.plot(dates, counts, label=hashtag)

if results:
    plt.xlabel("Day of Year")
    plt.ylabel("Hashtag Count")
    plt.title("Hashtag Count Relating to COVID-19 over 2020")
    plt.legend()
    plt.grid(True)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.tight_layout()
    plt.savefig("Hashtags.png")
else:
    print("No data available to plot.")
