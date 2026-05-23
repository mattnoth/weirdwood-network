#!/usr/bin/env python3
"""
Stage 4 Comention Candidate Classifier Helper
Loads comention candidates from JSONL, formats for systematic classification.
"""

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: stage4-haiku-classify-comention.py <input.candidates.jsonl> [--start N] [--end M]", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    start_idx = 0
    end_idx = None

    # Parse optional flags
    for i, arg in enumerate(sys.argv[2:], 1):
        if arg == '--start' and i < len(sys.argv) - 2:
            start_idx = int(sys.argv[i+1])
        elif arg == '--end' and i < len(sys.argv) - 2:
            end_idx = int(sys.argv[i+1])

    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    candidates = []
    with open(input_path) as f:
        for line in f:
            if line.strip():
                candidates.append(json.loads(line))

    total = len(candidates)
    if end_idx is None:
        end_idx = total

    print(f"\n=== Comention Candidates: {input_path.name} ===", file=sys.stderr)
    print(f"Total candidates: {total}, showing {start_idx} to {end_idx-1}", file=sys.stderr)
    print("", file=sys.stderr)

    for idx in range(start_idx, min(end_idx, total)):
        candidate = candidates[idx]

        print(f"\n{'='*80}")
        print(f"CANDIDATE {idx+1}/{total}")
        print(f"{'='*80}")

        pair_a = candidate.get('pair_a', 'UNKNOWN')
        pair_b = candidate.get('pair_b', 'UNKNOWN')
        evidence_chapter = candidate.get('evidence_chapter', 'UNKNOWN')

        print(f"Pair A: {pair_a}")
        print(f"Pair B: {pair_b}")
        print(f"Evidence Chapter: {evidence_chapter}")

        # Print evidence paragraphs
        evidence_paragraphs = candidate.get('evidence_paragraphs', [])
        if evidence_paragraphs:
            print(f"\nEvidence ({len(evidence_paragraphs)} paragraphs):")
            for i, para in enumerate(evidence_paragraphs):
                section = para.get('section', 'UNKNOWN SECTION')
                idx_num = para.get('paragraph_index', '?')
                snippet = para.get('snippet', 'NO SNIPPET')

                print(f"\n  [{i}] Section: {section} (paragraph {idx_num})")
                print(f"      Snippet: {snippet[:150]}...")

        # Print enriched fields if available
        if 'valid_edge_types' in candidate:
            valid_types = candidate.get('valid_edge_types', [])
            print(f"\nValid edge types: {', '.join(valid_types[:5])}")
            if len(valid_types) > 5:
                print(f"                  ... and {len(valid_types)-5} more")

        if 'target_type' in candidate:
            print(f"Target type: {candidate.get('target_type')}")

        # Decision prompt
        print(f"\n[ DECISION ]")
        print(f"Choose one:")
        print(f"  1. emit_edge <TYPE>")
        print(f"  2. reject_just_mention <REASON>")
        print(f"  3. escalate_cross_identity")
        print(f"  4. escalate_disambiguation")


if __name__ == '__main__':
    main()
