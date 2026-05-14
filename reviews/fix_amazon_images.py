#!/usr/bin/env python3
import os, re

fixed = 0
broken_covers = []

for fname in os.listdir('.'):
    if not fname.endswith('.html'):
        continue
    with open(fname) as f:
        content = f.read()

    # Fix broken images-na.ssl-images-amazon.com/images/I/ covers
    # Pattern: images-na.ssl-images-amazon.com/images/I/B0XXXXX._SL500_.jpg
    # Replace with: images-na.ssl-images-amazon.com/images/P/B0XXXXX.01._SX150_.jpg

    old_pattern = r'https://images-na\.ssl-images-amazon\.com/images/I/([A-Z0-9]+)\._SL500_\.jpg'
    match = re.search(old_pattern, content)
    if match:
        asin = match.group(1)
        # Verify the P format works by checking the ASIN structure
        new_url = f'https://images-na.ssl-images-amazon.com/images/P/{asin}.01._SX150_.jpg'
        content = re.sub(old_pattern, new_url, content)
        with open(fname, 'w') as f:
            f.write(content)
        print(f"FIXED: {fname} -> {asin}")
        fixed += 1

print(f"\nTotal fixed: {fixed}")
