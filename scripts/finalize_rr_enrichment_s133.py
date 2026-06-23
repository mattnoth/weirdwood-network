#!/usr/bin/env python3
"""Apply the S133 fresh-verify verdicts to the RR-enrichment edges (run_id rr-enrichment-s133).

6 CONFIRM / 2 ADJUST / 1 REJECT:
  - REJECT E4: drop  wedding-of-robert-i-baratheon-and-cersei-lannister --ENABLES--> death-of-robert-baratheon
  - ADJUST E2: confidence_tier 1 -> 2 (exile-of-jon-connington ENABLES aegon-revealed-to-the-golden-company)
  - ADJUST E21: re-anchor lyanna-stark SUSPECTED_OF knight-of-the-laughing-tree-incident to the she-wolf line
  - FIX  E9 (orchestrator nit): rhaegar AGENT_IN kotlt-incident quote -> the "dragon prince to seek the man" span
  - CONFIRM: flip verified_by pending -> subagent-fresh-verify-2026-06-22 on the surviving interpretive edges
Byte-exact quotes are extracted from the chapter files so verify-edge-quotes stays 0-drift.
Idempotent-ish: backs up first; safe to inspect output.
"""
import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph/edges/edges.jsonl"
BACKUP = REPO / "graph/edges/_regrounding/edges-pre-rr-finalize-2026-06-22.jsonl"
RUN_ID = "rr-enrichment-s133"
VERIFIED = "subagent-fresh-verify-2026-06-22"


def extract(chapter_rel: str, anchor: str, end_anchor: str) -> str:
    """Return the exact source substring from `anchor` through `end_anchor` (inclusive)."""
    text = (REPO / chapter_rel).read_text(encoding="utf-8")
    i = text.find(anchor)
    if i < 0:
        raise SystemExit(f"ANCHOR NOT FOUND in {chapter_rel}: {anchor!r}")
    j = text.find(end_anchor, i)
    if j < 0:
        raise SystemExit(f"END ANCHOR NOT FOUND in {chapter_rel}: {end_anchor!r}")
    return text[i : j + len(end_anchor)]


# Byte-exact replacement quotes pulled from source
E21_QUOTE = extract(
    "sources/chapters/asos/asos-bran-02.md",
    "The she-wolf laid into the squires",
    "scattering them all.",
)
E9_QUOTE = extract(
    "sources/chapters/asos/asos-bran-02.md",
    "even sent his son the dragon prince to seek the man",
    "hanging abandoned in a tree.",
)
print(f"E21 new quote: {E21_QUOTE!r}")
print(f"E9  new quote: {E9_QUOTE!r}")


def is_rr(r):
    return r.get("run_id") == RUN_ID


def match(r, etype, src, tgt):
    return (
        r.get("edge_type") == etype
        and r.get("source_slug") == src
        and r.get("target_slug") == tgt
    )


rows = [json.loads(l) for l in EDGES.read_text(encoding="utf-8").splitlines() if l.strip()]
shutil.copy2(EDGES, BACKUP)

out = []
dropped = adjusted = flipped = 0
for r in rows:
    if not is_rr(r):
        out.append(r)
        continue
    # REJECT E4
    if match(r, "ENABLES", "wedding-of-robert-i-baratheon-and-cersei-lannister", "death-of-robert-baratheon"):
        dropped += 1
        continue
    # ADJUST E2 tier
    if match(r, "ENABLES", "exile-of-jon-connington", "aegon-revealed-to-the-golden-company"):
        r["confidence_tier"] = 2
        adjusted += 1
    # ADJUST E21 re-anchor
    if match(r, "SUSPECTED_OF", "lyanna-stark", "knight-of-the-laughing-tree-incident"):
        r["evidence_ref"] = "sources/chapters/asos/asos-bran-02.md:187"
        r["evidence_quote"] = E21_QUOTE
        adjusted += 1
    # FIX E9 quote
    if match(r, "AGENT_IN", "rhaegar-targaryen", "knight-of-the-laughing-tree-incident"):
        r["evidence_quote"] = E9_QUOTE
        adjusted += 1
    # CONFIRM: flip pending -> verified
    if r.get("verified_by") == "pending":
        r["verified_by"] = VERIFIED
        flipped += 1
    out.append(r)

with EDGES.open("w", encoding="utf-8") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"\nbackup: {BACKUP}")
print(f"dropped (E4 reject): {dropped}")
print(f"adjusted (E2 tier / E21 re-anchor / E9 quote): {adjusted}")
print(f"verified_by flipped pending->confirmed: {flipped}")
print(f"edges.jsonl rows: {len(rows)} -> {len(out)}")
