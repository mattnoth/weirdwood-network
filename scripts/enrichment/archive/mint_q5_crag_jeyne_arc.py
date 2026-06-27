#!/usr/bin/env python3
"""Mint the Q5 "Storming of the Crag -> Robb weds Jeyne" causal beat (WO5K-remainder track, S123).

WO5K decomposition Rank 2 / Q5 (working/wo5k-decomposition.md). `robb-weds-jeyne-
westerling` already had its DOWNSTREAM wired (TRIGGERS red-wedding-conspiracy) but
ZERO causal UPSTREAM. The honest causal model (per the Q5 dip): the storming itself
does NOT cause the marriage -- it ENABLES it (wounds Robb, puts him in Jeyne's care).
The load-bearing driver is the FALSE NEWS of Bran and Rickon's deaths, which has no
node. So we mint one intermediate beat and wire a 2-cause convergence on the wedding.

DEDUP NOTE: `battle-of-the-crag` is a confirmed redirect dup of `storming-of-the-crag`
(carries `same_as: storming-of-the-crag`, 0 edges) -- canonical node is
`storming-of-the-crag`. No causal edge on the dup.

UPSTREAM CORRECTION (vs the dip's first pass): the false deaths come from THEON'S
DECEPTION during `capture-of-winterfell` (tarred miller's-boy heads above the gates),
NOT the later `sack-of-winterfell` (Ramsay's burning). The capture-of-winterfell node
itself states "the grief over the alleged deaths of Bran and Rickon causes Robb Stark
... to seek solace in Jeyne Westerling's arms and then marry her at the Crag." So the
upstream is `capture-of-winterfell` (already tagged [wo5k, north] -- seam-safe, drawing
an edge FROM it, not re-tagging).

New beat-node (written as .node.md, not here):
  - robb-receives-false-news-of-brans-death  (event.incident; ASOS Catelyn II)

Edges (chain-as-arc, NO umbrella parent; vocab-locked CAUSES/TRIGGERS/ENABLES/MOTIVATES):
  storming-of-the-crag        --ENABLES--> robb-weds-jeyne-westerling             (Tier-2)
  capture-of-winterfell       --CAUSES-->  robb-receives-false-news-of-brans-death (Tier-2)
  robb-receives-false-news... --TRIGGERS-> robb-weds-jeyne-westerling             (Tier-2)
  robb-receives-false-news... --MOTIVATES-> robb-stark                            (Tier-2)

ENABLES (storming -> wedding): the storming is the SETTING/precondition (Robb wounded,
nursed by Jeyne at the Crag) -- makes the marriage possible but is not its sufficient
cause. Per the ENABLES-vs-CAUSES rule, not-sufficient => ENABLES.

CAUSES (capture -> false-news): Theon's faked deaths generate the false report that
travels to the Crag -- a mediated consequence (deception + travel), not an immediate
spark => CAUSES.

TRIGGERS (false-news -> wedding): the night of grief-comfort -> marriage "the next day"
is the immediate specific spark the storming itself lacks => TRIGGERS.

MOTIVATES (false-news -> robb-stark): the grief drives Robb's honor-bound decision to
wed ("It was the only honorable thing to do"). Event-condition -> named character =>
MOTIVATES. Agency lands on the character, not the wedding event (agency-collapse-safe).

HARD-STOP: no causal edge into war-of-the-five-kings. Downstream (TRIGGERS red-wedding-
conspiracy) already wired; this completes the upstream.

Causal edges (Tier-2) carry verified_by='pending-q5-verify' until a fresh subagent
confirms against the local cache.

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-q5-crag-jeyne-2026-06-22.jsonl"

RUN_ID = "causal-arc-q5-crag-jeyne-20260622"
PRODUCED_AT = "2026-06-22T00:00:00+00:00"
COMMON = {
    "decision": "emit_edge",
    "candidate_kind": "causal-curator-arc",
    "evidence_kind": "book-pass1",
    "typed_by": "curator-causal-arc",
    "schema_version": "pass1-derived-v1",
    "produced_at": PRODUCED_AT,
    "run_id": RUN_ID,
}

CRAG = "storming-of-the-crag"
WEDDING = "robb-weds-jeyne-westerling"
CAPTURE = "capture-of-winterfell"
NEWS = "robb-receives-false-news-of-brans-death"
ROBB = "robb-stark"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified)
EDGES_SPEC = [
    (CRAG, "ENABLES", WEDDING, 2, "asos", "asos-catelyn-02", 143,
     "I took an arrow in the arm just before Ser Rolph yielded us the castle. It seemed nothing at first, but it festered. Jeyne had me taken to her own bed, and she nursed me until the fever passed.",
     "The storming wounds Robb and puts him in Jeyne's care at the Crag -- the precondition for the bedding and marriage, but not its sufficient cause (the grief from the false news is the driver). Not-sufficient setting => ENABLES Tier-2.",
     "pending-q5-verify"),
    (CAPTURE, "CAUSES", NEWS, 2, "asos", "asos-catelyn-02", 143,
     "And she was with me when the Greatjon brought me the news of . . . of Winterfell. Bran and Rickon.",
     "Theon's capture of Winterfell and his faked deaths (tarred miller's-boy heads displayed as Bran and Rickon) generate the false report that reaches Robb at the Crag. Mediated by deception + travel => CAUSES Tier-2.",
     "pending-q5-verify"),
    (NEWS, "TRIGGERS", WEDDING, 2, "asos", "asos-catelyn-02", 145,
     "Catelyn did not need to be told what sort of comfort Jeyne Westerling had offered her son. “And you wed her the next day.”",
     "The night of grief-comfort following the news -> marriage 'the next day' is the immediate specific spark of the wedding (the storming itself lacks this tight link) => TRIGGERS Tier-2.",
     "pending-q5-verify"),
    (NEWS, "MOTIVATES", ROBB, 2, "asos", "asos-catelyn-02", 147,
     "It was the only honorable thing to do. She’s gentle and sweet, Mother, she will make me a good wife.",
     "The grief from the false news drives Robb's honor-bound decision to wed Jeyne after taking her maidenhead. Event-condition -> named character => MOTIVATES Tier-2 (agency lands on Robb, not the wedding event).",
     "pending-q5-verify"),
]


def make_row(spec):
    src, etype, tgt, tier, book, chap, line, quote, asserted, verified = spec
    row = {
        "edge_type": etype,
        "source_slug": src,
        "target_slug": tgt,
        **COMMON,
        "evidence_book": book,
        "evidence_chapter": chap,
        "evidence_ref": f"sources/chapters/{book}/{chap}.md:{line}",
        "evidence_quote": quote,
        "confidence_tier": tier,
        "asserted_relation": asserted,
    }
    if verified is not None:
        row["verified_by"] = verified
    return row


def main():
    all_slugs = {s[0] for s in EDGES_SPEC} | {s[2] for s in EDGES_SPEC}
    resolved, missing = precheck_slugs(all_slugs)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed (non-existent targets): {missing}")
    print(f"slug pre-check OK: {len(resolved)} resolved.")

    lines = EDGES.read_text(encoding="utf-8").splitlines()
    if any(RUN_ID in ln for ln in lines):
        sys.exit(f"ABORT: run_id {RUN_ID} already present in {EDGES} -- already minted.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    new_rows = [make_row(s) for s in EDGES_SPEC]
    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    n_causal = sum(1 for s in EDGES_SPEC if s[1] in ("CAUSES", "TRIGGERS", "ENABLES", "MOTIVATES"))
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges ({n_causal} causal Tier-2).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines.")


if __name__ == "__main__":
    main()
