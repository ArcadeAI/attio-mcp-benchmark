#!/usr/bin/env python3
"""
Re-count tokens from raw benchmark responses.
No API keys needed — just tiktoken.

Usage:
    pip install tiktoken
    python count_tokens.py
"""

import json
import os
import csv
from pathlib import Path

try:
    import tiktoken
except ImportError:
    print("Install tiktoken: pip install tiktoken")
    exit(1)


def count_tokens(text: str, model: str = "cl100k_base") -> int:
    enc = tiktoken.get_encoding(model)
    return len(enc.encode(text))


def main():
    data_dir = Path(__file__).parent.parent / "data" / "raw"

    if not data_dir.exists():
        # Also check sibling raw/ directory
        data_dir = Path(__file__).parent.parent / "raw"

    if not data_dir.exists():
        print(f"Error: No raw data directory found.")
        print(f"Looked in: {Path(__file__).parent.parent / 'data' / 'raw'}")
        print(f"       and: {Path(__file__).parent.parent / 'raw'}")
        exit(1)

    results = []

    for toolkit_dir in sorted(data_dir.iterdir()):
        if not toolkit_dir.is_dir() or toolkit_dir.name == "schemas":
            continue
        toolkit = toolkit_dir.name

        for response_file in sorted(toolkit_dir.glob("*.json")):
            with open(response_file) as f:
                content = f.read()

            tokens = count_tokens(content)
            bytes_size = len(content.encode("utf-8"))

            # Try to count records and fields
            try:
                data = json.loads(content)
                if isinstance(data, list):
                    records = len(data)
                    fields = len(data[0]) if data else 0
                elif isinstance(data, dict) and "data" in data:
                    records = len(data["data"]) if isinstance(data["data"], list) else 1
                    fields = len(data["data"][0]) if isinstance(data["data"], list) and data["data"] else 0
                elif isinstance(data, dict):
                    records = 1
                    fields = len(data)
                else:
                    records = 0
                    fields = 0
            except (json.JSONDecodeError, IndexError, TypeError):
                records = 0
                fields = 0

            results.append({
                "scenario": response_file.stem,
                "toolkit": toolkit,
                "tokens": tokens,
                "bytes": bytes_size,
                "records": records,
                "fields_per_record": fields,
                "file": str(response_file.relative_to(data_dir.parent)),
            })

    if not results:
        print("No JSON files found in raw data directories.")
        exit(1)

    # Print detailed table
    print(f"\n{'Scenario':<45} {'Toolkit':<20} {'Tokens':>10} {'Bytes':>10} {'Records':>8}")
    print("-" * 95)

    for r in results:
        print(f"{r['scenario']:<45} {r['toolkit']:<20} {r['tokens']:>10,} {r['bytes']:>10,} {r['records']:>8}")

    # Print comparison summary
    scenarios = sorted(set(r["scenario"] for r in results))
    toolkits = sorted(set(r["toolkit"] for r in results))

    print(f"\n\nComparison Summary")
    print(f"{'Scenario':<45}", end="")
    for t in toolkits:
        print(f" {t:>15}", end="")
    print(f" {'Ratio':>10}")
    print("-" * (45 + 16 * len(toolkits) + 11))

    for scenario in scenarios:
        print(f"{scenario:<45}", end="")
        token_counts = {}
        for toolkit in toolkits:
            match = [r for r in results if r["scenario"] == scenario and r["toolkit"] == toolkit]
            if match:
                token_counts[toolkit] = match[0]["tokens"]
                print(f" {match[0]['tokens']:>14,}", end="")
            else:
                print(f" {'—':>14}", end="")
        print(end="")

        # Compute ratio (max / min)
        if len(token_counts) >= 2:
            min_t = min(token_counts.values())
            max_t = max(token_counts.values())
            if min_t > 0:
                print(f" {max_t/min_t:>9.1f}x", end="")
        print()

    # Write CSV
    csv_path = data_dir.parent / "token-counts-verified.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["scenario", "toolkit", "tokens", "bytes", "records", "fields_per_record", "file"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nCSV written to {csv_path}")


if __name__ == "__main__":
    main()
