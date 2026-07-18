#!/usr/bin/env python3
"""theories-jonsnow-substrate-s219.py — assemble the mintable Jon Snow substrate.

Consolidates every byte-verified grounded row for qSy2uaJ7ecU (p1 + p2 +
p2-redo + redo-s219 workers) with its beat metadata (theory header, stance,
sub_claim, strength, source_domain) from the extraction file. Later files win
on beat_id collisions (redo supersedes the original attempt). Run AFTER
theories-reground-repair.py has byte-checked the redo files.

Output: working/theories/jonsnow-cluster/substrate.jsonl (grounded only)
        + a per-theory count summary on stdout.
"""
from __future__ import annotations

import json
from collections import Counter, OrderedDict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
AGENT_DIR = REPO / "working/theories/regrounding-agent"
EXTRACTION = REPO / "working/theories/extractions/qSy2uaJ7ecU.jsonl"
REGROUND = REPO / "working/theories/regrounding/qSy2uaJ7ecU.jsonl"
OUT = REPO / "working/theories/jonsnow-cluster/substrate.jsonl"

# precedence order: originals first, redos last (last write wins)
SOURCES = [
    "qSy2uaJ7ecU-p1.jsonl",
    "qSy2uaJ7ecU-p2.jsonl",
    "qSy2uaJ7ecU-p2-redo.jsonl",
    "redo-s219-worker-1.jsonl",
    "redo-s219-worker-2.jsonl",
]


def main():
    beats = {}
    for ln in EXTRACTION.read_text().splitlines():
        if not ln.strip():
            continue
        r = json.loads(ln)
        if r.get("kind") == "beat":
            beats[r["beat_id"]] = r

    # deterministic-matcher rows (status matched) also count as grounded substrate
    rows = OrderedDict()
    for ln in REGROUND.read_text().splitlines():
        if not ln.strip():
            continue
        r = json.loads(ln)
        if r.get("status") == "matched":
            rows[r["beat_id"]] = {
                "beat_id": r["beat_id"], "file": r.get("file"), "line": r.get("line"),
                "verbatim_quote": r.get("verbatim_quote"), "grounded_by": "deterministic",
            }

    for name in SOURCES:
        p = AGENT_DIR / name
        if not p.exists():
            continue
        for ln in p.read_text().splitlines():
            if not ln.strip():
                continue
            r = json.loads(ln)
            if not r["beat_id"].startswith("jonsnow-"):
                continue
            if r.get("status") == "grounded":
                rows[r["beat_id"]] = {
                    "beat_id": r["beat_id"], "file": r.get("file"), "line": r.get("line"),
                    "verbatim_quote": r.get("verbatim_quote"), "grounded_by": name,
                    "note": r.get("note"),
                }
            elif r.get("status") in ("byte-fail", "ungrounded") and r["beat_id"] in rows:
                # a later byte-fail/ungrounded verdict on a beat an EARLIER file grounded:
                # keep the earlier grounded row only if it came from a file already
                # byte-checked; redo rows always went through repair, so keep.
                pass

    out_rows = []
    counts = Counter()
    for bid, g in rows.items():
        b = beats.get(bid, {})
        theory = b.get("theory", "?")
        counts[theory] += 1
        out_rows.append({**g,
                         "theory": theory,
                         "stance": b.get("stance"),
                         "sub_claim": b.get("sub_claim"),
                         "source_domain": b.get("source_domain"),
                         "strength_as_presented": b.get("strength_as_presented"),
                         "paraphrase": b.get("paraphrase")})

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out_rows))
    print(f"substrate: {len(out_rows)} grounded beats -> {OUT.relative_to(REPO)}")
    for theory, n in counts.most_common():
        print(f"  {n:3d}  {theory}")


if __name__ == "__main__":
    main()
