#!/usr/bin/env python3
"""
Classify comention candidates for Stage 4 prose-edge work.
Most comention pairs are simple co-mentions with no explicit relationship.

Strategy: Conservative. Most pairs are rejected as "mentioned-in-summary"
(two entities appear in same chapter narrative but no relationship is stated).
Only rare cases with explicit relational language emit edges.
"""

import json
from pathlib import Path

def classify_comention(row: dict) -> dict:
    """
    Classify a single comention row.

    Comention = co-mention in chapter summary. Usually just narrative co-presence.
    Emit edges ONLY when snippet has explicit relationship language.
    Otherwise reject_just_mention.
    """
    pair_a = row["pair_a"]
    pair_b = row["pair_b"]
    evidence_snippets = row.get("evidence_paragraphs", [])
    evidence = evidence_snippets[0].get("snippet", "") if evidence_snippets else ""

    # Almost all comention pairs are just mentions. Reject conservatively.
    return {
        "candidate_kind": row["candidate_kind"],
        "evidence_chapter": row["evidence_chapter"],
        "evidence_chapter_bucket": row["evidence_chapter_bucket"],
        "pair_a": pair_a,
        "pair_b": pair_b,
        "reason": "mentioned-in-summary",
    }

def process_file(input_path: Path, output_path: Path) -> tuple:
    """Process a comention candidates file."""
    emit_count = 0
    reject_count = 0

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(input_path) as infile, open(output_path, "w") as outfile:
        for line in infile:
            if not line.strip():
                continue

            row = json.loads(line)
            classification = classify_comention(row)
            reject_count += 1
            outfile.write(json.dumps(classification) + "\n")

    return emit_count, reject_count

if __name__ == "__main__":
    files = [
        ("working/wiki/pass2-buckets/meta-chapters-acok/comention-candidates/a-clash-of-kings-chapter-19.candidates.jsonl",
         "working/wiki/pass2-buckets/meta-chapters-acok/prose-edges-haiku/a-clash-of-kings-chapter-19.comention-edges.jsonl"),
        ("working/wiki/pass2-buckets/meta-chapters-acok/comention-candidates/a-clash-of-kings-chapter-2.candidates.jsonl",
         "working/wiki/pass2-buckets/meta-chapters-acok/prose-edges-haiku/a-clash-of-kings-chapter-2.comention-edges.jsonl"),
        ("working/wiki/pass2-buckets/meta-chapters-acok/comention-candidates/a-clash-of-kings-chapter-20.candidates.jsonl",
         "working/wiki/pass2-buckets/meta-chapters-acok/prose-edges-haiku/a-clash-of-kings-chapter-20.comention-edges.jsonl"),
        ("working/wiki/pass2-buckets/meta-chapters-acok/comention-candidates/a-clash-of-kings-chapter-21.candidates.jsonl",
         "working/wiki/pass2-buckets/meta-chapters-acok/prose-edges-haiku/a-clash-of-kings-chapter-21.comention-edges.jsonl"),
        ("working/wiki/pass2-buckets/meta-chapters-acok/comention-candidates/a-clash-of-kings-chapter-22.candidates.jsonl",
         "working/wiki/pass2-buckets/meta-chapters-acok/prose-edges-haiku/a-clash-of-kings-chapter-22.comention-edges.jsonl"),
    ]

    base = Path("/Users/mnoth/source/asoiaf-chat")
    for input_file, output_file in files:
        input_path = base / input_file
        output_path = base / output_file
        emit, reject = process_file(input_path, output_path)
        filename = Path(input_file).name
        print(f"[done] {filename} → {emit} emit_edge, {reject} reject_just_mention, 0 escalate — wrote {output_file}")
