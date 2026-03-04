#!/bin/bash

for file in /data/Twitter\ dataset/geoTwitter20-*-*.zip; do
    python3 map.py --input_path "$file" 
done
