#!/usr/bin/env python3
import json
import sys

# Read all candidates files and output classification decisions
input_files = [
    "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-merrett.candidates.jsonl",
    "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-rhaegar.candidates.jsonl",
    "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-walton.candidates.jsonl",
    "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-rivers-daughter-of-aemon.candidates.jsonl",
    "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walder-frey-son-of-emmon.candidates.jsonl"
]

output_files = {
    "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-merrett.candidates.jsonl": "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-frey-daughter-of-merrett.edges.jsonl",
    "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-rhaegar.candidates.jsonl": "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-frey-daughter-of-rhaegar.edges.jsonl",
    "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-walton.candidates.jsonl": "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-frey-daughter-of-walton.edges.jsonl",
    "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-rivers-daughter-of-aemon.candidates.jsonl": "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-rivers-daughter-of-aemon.edges.jsonl",
    "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walder-frey-son-of-emmon.candidates.jsonl": "working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walder-frey-son-of-emmon.edges.jsonl"
}

# Collect all candidates and count
for input_file in input_files:
    output_file = output_files[input_file]
    print(f"Processing: {input_file}")

    count = 0
    try:
        with open(input_file, 'r') as f:
            for line in f:
                if line.strip():
                    count += 1
        print(f"  Found {count} candidates")
    except Exception as e:
        print(f"  Error: {e}")

