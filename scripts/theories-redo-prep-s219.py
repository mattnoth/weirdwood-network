#!/usr/bin/env python3
"""theories-redo-prep-s219.py — build the consolidated byte-fail redo worklist.

Collects every `byte-fail` row across working/theories/regrounding-agent/*.jsonl,
joins each back to its original beat context in working/theories/regrounding/<vid>.jsonl
(spoken_quote / paraphrase / stance / source_domain), and emits worker input
chunks to working/theories/redo-s219/worker-N.jsonl.

Whole-video assignment: a video's rows never split across workers (fewer files
per agent). jonsnow (qSy2uaJ7ecU*) is its own pair of workers by size.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
AGENT_DIR = REPO / "working/theories/regrounding-agent"
INPUT_DIR = REPO / "working/theories/regrounding"
OUT_DIR = REPO / "working/theories/redo-s219"

N_WORKERS = 4


def video_of(stem: str) -> str:
    # qSy2uaJ7ecU-p2-redo -> qSy2uaJ7ecU ; 1oEqnDAbCfE -> 1oEqnDAbCfE
    return re.sub(r"-(p\d+)(-redo.*)?$", "", stem)


def main():
    beats = {}  # (video, beat_id) -> beat row
    for f in INPUT_DIR.glob("*.jsonl"):
        for ln in f.read_text().splitlines():
            if not ln.strip():
                continue
            r = json.loads(ln)
            beats[(f.stem, r["beat_id"])] = r

    by_video = defaultdict(list)
    seen = set()  # (video, beat_id) — a beat may byte-fail in both p2 and p2-redo
    for f in sorted(AGENT_DIR.glob("*.jsonl")):
        vid = video_of(f.stem)
        for ln in f.read_text().splitlines():
            if not ln.strip():
                continue
            r = json.loads(ln)
            if r.get("status") != "byte-fail":
                continue
            key = (vid, r["beat_id"])
            if key in seen:
                continue
            seen.add(key)
            beat = beats.get(key, {})
            by_video[vid].append({
                "video": vid,
                "beat_id": r["beat_id"],
                "stance": beat.get("stance"),
                "source_domain": beat.get("source_domain"),
                "spoken_quote": beat.get("spoken_quote"),
                "paraphrase": beat.get("paraphrase"),
                "prior_file": r.get("file"),
                "prior_line": r.get("line"),
                "prior_failed_quote": r.get("verbatim_quote"),
                "prior_note": r.get("note"),
            })

    # jonsnow is the big pool: split it into 2 workers; everything else fills the rest.
    OUT_DIR.mkdir(exist_ok=True)
    jon = by_video.pop("qSy2uaJ7ecU", [])
    workers = [[] for _ in range(N_WORKERS)]
    half = (len(jon) + 1) // 2
    workers[0], workers[1] = jon[:half], jon[half:]
    rest = sorted(by_video.items(), key=lambda kv: -len(kv[1]))
    for vid, rows in rest:
        target = min(workers[2:], key=len)
        target.extend(rows)

    total = 0
    for i, rows in enumerate(workers, 1):
        p = OUT_DIR / f"worker-{i}.jsonl"
        p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        vids = sorted({r["video"] for r in rows})
        print(f"worker-{i}: {len(rows)} rows  videos={vids}")
        total += len(rows)
    missing = [k for k in seen if k not in beats]
    print(f"total byte-fail beats: {total}  (join-misses: {len(missing)})")
    for k in missing:
        print(f"  JOIN-MISS: {k}")


if __name__ == "__main__":
    main()
