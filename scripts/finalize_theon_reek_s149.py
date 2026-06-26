#!/usr/bin/env python3
"""Finalize the Theon/Reek enrichment (S149) after independent fresh-verify (13 CONFIRM / 2 ADJUST
/ 0 REJECT; 4 retirements SAFE-TO-DROP + 1 finalize-driven re-point).

Applies, to graph/edges/edges.jsonl:
  ADJUST (run_id theon-reek-enrichment-s149):
    - W2  mance-rayder AGENT_IN the-winterfell-murders  -> SUSPECTED_OF (GRRM keeps the spearwives'
          culpability coy; AGENT_IN over-asserts. Stays Tier-2.)
    - W3  rowan        AGENT_IN the-winterfell-murders  -> SUSPECTED_OF (same)
  STAMP verified_by='fresh-verify-s149' on every run_id edge whose verified_by=='pending'.
  RETIRE (existing edges, NOT this run_id — confirmed safe by fresh-verify):
    - R1  theon-greyjoy KILLS bran-stark                                   (FACTUALLY FALSE — Bran lives;
          the killed boys were the miller's sons. Replaced by bran VICTIM_IN theon-fakes-the-deaths.)
    - R2  wedding-of-ramsay-bolton-and-arya-stark PRECEDES wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen
    - R3  fall-of-moat-cailin PRECEDES purple-wedding
    - R4  taking-of-deepwood-motte PRECEDES purple-wedding   (R2-R4 = cross-book chronology noise)
    - R5  capture-of-winterfell CAUSES robb-receives-false-news-of-brans-death  (causal-collapse —
          F8 theon-fakes-the-deaths CAUSES robb-receives-false-news is the proximate cause; the
          deception, not the capture, produces the false news. Chain stays intact via F7+F8.)

Backup + re-run guard. Idempotent: aborts if W2 is already SUSPECTED_OF."""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-theon-reek-finalize-2026-06-25.jsonl"
RUN_ID = "theon-reek-enrichment-s149"
VERIFIED_BY = "fresh-verify-s149"

ADJUST = {  # candidate_id -> new edge_type
    "W2": "SUSPECTED_OF",
    "W3": "SUSPECTED_OF",
}

# Existing edges to retire — matched by (source_slug, edge_type, target_slug).
RETIRE = [
    ("theon-greyjoy", "KILLS", "bran-stark"),
    ("wedding-of-ramsay-bolton-and-arya-stark", "PRECEDES", "wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen"),
    ("fall-of-moat-cailin", "PRECEDES", "purple-wedding"),
    ("taking-of-deepwood-motte", "PRECEDES", "purple-wedding"),
    ("capture-of-winterfell", "CAUSES", "robb-receives-false-news-of-brans-death"),
]


def main():
    lines = [ln for ln in EDGES.read_text(encoding="utf-8").splitlines() if ln.strip()]
    rows = [json.loads(ln) for ln in lines]

    # re-run guard: W2 already adjusted?
    for r in rows:
        if r.get("run_id") == RUN_ID and r.get("candidate_id") == "W2" and r.get("edge_type") == "SUSPECTED_OF":
            sys.exit("ABORT: W2 already SUSPECTED_OF — finalize already applied.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)
    print(f"Backup -> {BACKUP.relative_to(REPO)}")

    retire_set = set(RETIRE)
    out = []
    adjusted = stamped = dropped = 0
    dropped_detail = []
    for r in rows:
        key = (r.get("source_slug"), r.get("edge_type"), r.get("target_slug"))
        if key in retire_set:
            dropped += 1
            dropped_detail.append(key)
            continue
        if r.get("run_id") == RUN_ID:
            cid = r.get("candidate_id")
            if cid in ADJUST and r.get("edge_type") != ADJUST[cid]:
                r["edge_type"] = ADJUST[cid]
                adjusted += 1
            if r.get("verified_by") == "pending":
                r["verified_by"] = VERIFIED_BY
                stamped += 1
        out.append(r)

    missing = retire_set - set(dropped_detail)
    if missing:
        sys.exit(f"ABORT: retire targets not found (no change written): {sorted(missing)}")

    EDGES.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in out) + "\n", encoding="utf-8")

    print("\n── FINALIZE SUMMARY ──")
    print(f"Adjusted AGENT_IN->SUSPECTED_OF: {adjusted}  (W2 mance-rayder, W3 rowan)")
    print(f"Stamped verified_by={VERIFIED_BY}: {stamped}")
    print(f"Retired edges: {dropped}")
    for s, t, d in dropped_detail:
        print(f"    - {s} -{t}-> {d}")
    print(f"edges.jsonl: {len(rows)} -> {len(out)} lines ({len(out) - len(rows):+d})")


if __name__ == "__main__":
    main()
