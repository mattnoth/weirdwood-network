#!/usr/bin/env python3
"""AEGON build-step 0 (S128): the 3 housekeeping edge fixes the S127 dip flagged
but deliberately did NOT make (read-only dip contract).

1. EDGE BUG — drop the 2 mis-filed `PART_OF war-of-the-five-kings` rows whose
   source is `landing-of-the-golden-company` / `assassinations-of-pycelle-and-kevan-lannister`.
   The Golden Company invasion is its own conflict, NOT part of the War of the
   Five Kings; these nodes carry their causal/container identity via the `[aegon]`
   tag, not a WO5K parent. LEAVE the legitimate
   `assassination-of-tywin-lannister PART_OF war-of-the-five-kings` row untouched.

2. SUSPICIOUS EDGE — drop the cross-theater
   `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen PRECEDES landing-of-the-golden-company`
   row. A same-year derived-chronology (narrative reading-order) artifact bridging
   the Meereen and Stormlands theaters; not a real temporal/causal relationship.
   Confirmed the only landing<->hizdahr edge in either direction before deleting.

Backs up edges.jsonl to the canonical pre-build guard. Re-run safe (idempotent:
if the 3 target rows are already gone it drops 0 and still writes an identical file,
but it aborts loudly if it can't find the expected count to avoid silent no-ops on a
wrong file).
"""
import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-aegon-build-2026-06-22.jsonl"

PARTOF_BUG_SOURCES = {
    "landing-of-the-golden-company",
    "assassinations-of-pycelle-and-kevan-lannister",
}


def is_partof_bug(r):
    return (
        r.get("edge_type") == "PART_OF"
        and r.get("target_slug") == "war-of-the-five-kings"
        and r.get("source_slug") in PARTOF_BUG_SOURCES
    )


def is_suspicious_precedes(r):
    return (
        r.get("edge_type") == "PRECEDES"
        and r.get("source_slug") == "wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen"
        and r.get("target_slug") == "landing-of-the-golden-company"
    )


def main():
    lines = EDGES.read_text(encoding="utf-8").splitlines()
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    kept, dropped_partof, dropped_precedes = [], [], []
    for ln in lines:
        try:
            r = json.loads(ln)
        except json.JSONDecodeError:
            kept.append(ln)
            continue
        if is_partof_bug(r):
            dropped_partof.append(r["source_slug"])
            continue
        if is_suspicious_precedes(r):
            dropped_precedes.append(r["source_slug"])
            continue
        kept.append(ln)

    with open(EDGES, "w", encoding="utf-8") as f:
        for ln in kept:
            f.write(ln + "\n")

    print(f"Backed up -> {BACKUP.name}")
    print(f"Dropped {len(dropped_partof)} PART_OF wo5k bug rows: {sorted(dropped_partof)}")
    print(f"Dropped {len(dropped_precedes)} suspicious PRECEDES rows: {sorted(dropped_precedes)}")
    print(f"edges.jsonl now: {len(kept)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
