#!/usr/bin/env python3
"""Count tokens in raw arcade response files using tiktoken."""

import json
import os
import sys

try:
    import tiktoken
except ImportError:
    print("tiktoken not installed. Run: pip3 install tiktoken")
    sys.exit(1)

enc = tiktoken.get_encoding("cl100k_base")

ARCADE_DIR = os.path.join(os.path.dirname(__file__), "..", "raw", "arcade")

files = [
    ("01", "01-list-all-companies.json"),
    ("02", "02-deals-by-stage.json"),
    ("03", "03-deals-over-50k.json"),
    ("04", "04-companies-name-search.json"),
    ("05", "05-technology-companies.json"),
    ("06", "06-deals-by-close-date.json"),
    ("07", "07-compound-filter.json"),
    ("08", "08-sort-and-limit.json"),
]

print(f"\n{'#':<4} {'File':<40} {'Tokens':>8} {'Records':>8}")
print("-" * 64)

total_tokens = 0
rows = []

for qid, filename in files:
    filepath = os.path.join(ARCADE_DIR, filename)
    if not os.path.exists(filepath):
        print(f"{qid:<4} {filename:<40} {'MISSING':>8}")
        continue

    with open(filepath, "r") as f:
        raw = f.read()

    tokens = len(enc.encode(raw))
    total_tokens += tokens

    try:
        data = json.loads(raw)
        response = data.get("response") or {}
        records = len(response.get("records", [])) if response else 0
        if data.get("error"):
            records = "ERR"
    except Exception:
        records = "?"

    rows.append((qid, filename, tokens, records))
    print(f"{qid:<4} {filename:<40} {tokens:>8,} {str(records):>8}")

print("-" * 64)
print(f"{'TOTAL':<44} {total_tokens:>8,}")
print()
