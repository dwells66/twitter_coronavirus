#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
items_k = []
items_v = []

for k,v in items:
    #print(k,':',v)
    items_k.append(k)
    items_v.append(v)

items_k = items_k[0:10]
items_v = items_v[0:10]

import matplotlib.pyplot as plt
import numpy as np

plt.bar(items_k, items_v)

plt.xlabel("Languages")
plt.ylabel("Frequency")
plt.title("Languages of 2020 Tweets Containing #coronavirus")

plt.savefig('lang_coronavirus.png', bbox_inches='tight', dpi=300)
