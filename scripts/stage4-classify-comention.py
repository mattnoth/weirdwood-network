#!/usr/bin/env python3
"""
Stage 4 comention classifier - processes candidates files and outputs edge classifications.
This is a reference classifier for testing the schema; actual classification requires human judgment.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def classify_candidate(candidate):
    """
    Attempt basic heuristic classification for testing purposes.
    In the actual batch, each candidate requires contextual human judgment.

    Returns: decision dict (emit_edge, reject_just_mention, escalate_*, etc.)
    """

    pair_a = candidate.get("pair_a", "")
    pair_b = candidate.get("pair_b", "")
    evidence_chapter = candidate.get("evidence_chapter", "")
    evidence_paragraphs = candidate.get("evidence_paragraphs", [])

    if not evidence_paragraphs:
        return {
            "decision": "reject_just_mention",
            "candidate_kind": "comention",
            "pair_a": pair_a,
            "pair_b": pair_b,
            "evidence_chapter": evidence_chapter,
            "reason": "no-evidence-paragraphs"
        }

    first_paragraph = evidence_paragraphs[0]
    section = first_paragraph.get("section", "## Unknown")
    paragraph_index = first_paragraph.get("paragraph_index", 0)
    snippet = first_paragraph.get("snippet", "")

    # Default: reject as temporal co-occurrence unless there's clear evidence of a relationship
    # This is a conservative default - actual classification needs full node context and manual judgment

    return {
        "decision": "reject_just_mention",
        "candidate_kind": "comention",
        "pair_a": pair_a,
        "pair_b": pair_b,
        "evidence_chapter": evidence_chapter,
        "reason": "comention-requires-manual-classification"
    }


def process_file(input_path, output_path):
    """Process a single candidates file and write classifications."""

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return

    # Create output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)

    classifications = []
    with open(input_path, 'r') as f:
        for line in f:
            if line.strip():
                try:
                    candidate = json.loads(line)
                    decision = classify_candidate(candidate)
                    classifications.append(decision)
                except json.JSONDecodeError as e:
                    print(f"JSON parse error in {input_path}: {e}")
                    continue

    # Write output
    with open(output_path, 'w') as f:
        for classification in classifications:
            f.write(json.dumps(classification) + '\n')

    print(f"Processed {len(classifications)} candidates from {input_path.name} → {output_path.name}")


if __name__ == "__main__":
    base_path = Path("/Users/mnoth/source/asoiaf-chat")

    files_to_process = [
        ("a-clash-of-kings-chapter-37", "acok"),
        ("a-clash-of-kings-chapter-38", "acok"),
        ("a-clash-of-kings-chapter-39", "acok"),
        ("a-clash-of-kings-chapter-4", "acok"),
        ("a-clash-of-kings-chapter-40", "acok"),
    ]

    for chapter_slug, book in files_to_process:
        input_path = base_path / f"working/wiki/pass2-buckets/meta-chapters-{book}/comention-candidates/{chapter_slug}.candidates.jsonl"
        output_path = base_path / f"working/wiki/pass2-buckets/meta-chapters-{book}/prose-edges-haiku/{chapter_slug}.comention-edges.jsonl"

        process_file(input_path, output_path)
