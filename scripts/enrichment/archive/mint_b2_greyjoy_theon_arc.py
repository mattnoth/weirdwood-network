#!/usr/bin/env python3
"""Mint the B2 Greyjoy-Rebellion -> Theon-as-ward arc (S107 causal-arc track).

Dip-driven (arc-weighted re-dip, 2026-06-19): Q8 "consequences of the Greyjoy
Rebellion / how did Theon become a ward?" was only *partial* — greyjoy-rebellion
was causally dark. This wires the single missing consequence.

Chain:
  greyjoy-rebellion --CAUSES--> theon-greyjoy-taken-as-ward   (HARD-STOP at the wardship)

The new beat carries the agency on role edges (Eddard AGENT_IN takes him; Theon
VICTIM_IN the hostage; Robert COMMANDS_IN-Tier-2 decreed it) rather than
collapsing a blunt rebellion->Theon arrow. HARD-STOP: no downstream edge to
Theon's ACOK invasion of the North (separate, larger arc).

Wires to `greyjoy-rebellion` (CANONICAL hub: 26 edges incl. all role edges,
type event.war, resolver target) — NOT the `greyjoys-rebellion` dup (7 stray
edges, mistyped event.battle; flagged to todos for a merge). The
`theon-greyjoy WARD_OF eddard-stark` dyad already exists (agot-catelyn-03:185)
and is NOT re-minted.

Causal edge (Tier-2) carries verified_by='pending-s107-b2-verify' until a fresh
subagent confirms. Role edges Tier-1 except Robert COMMANDS_IN (Tier-2).

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-b2-greyjoy-theon-arc-2026-06-19.jsonl"

RUN_ID = "causal-arc-b2-greyjoy-theon-20260619"
PRODUCED_AT = "2026-06-19T00:00:00+00:00"
COMMON = {
    "decision": "emit_edge",
    "candidate_kind": "causal-curator-arc",
    "evidence_kind": "book-pass1",
    "typed_by": "curator-causal-arc",
    "schema_version": "pass1-derived-v1",
    "produced_at": PRODUCED_AT,
    "run_id": RUN_ID,
}

REBELLION = "greyjoy-rebellion"   # canonical hub (verified vs edges.jsonl)
WARD = "theon-greyjoy-taken-as-ward"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted)
ROWS = [
    ("theon-greyjoy", "VICTIM_IN", WARD, 1, "acok", "acok-theon-01", 43,
     "I was a boy of ten when I was taken to Winterfell as a ward of Eddard Stark.",
     "Theon is the hostage/ward taken as surety for Balon's loyalty."),
    ("eddard-stark", "AGENT_IN", WARD, 1, "acok", "acok-theon-01", 11,
     "Robert Baratheon's war galley had borne him away to be a ward of Eddard Stark",
     "Eddard Stark takes Theon into his care as ward at Winterfell."),
    ("robert-i-baratheon", "COMMANDS_IN", WARD, 2, "acok", "acok-theon-01", 11,
     "Robert Baratheon's war galley had borne him away to be a ward of Eddard Stark",
     "Robert spared Balon and decreed the hostage arrangement (his war galley carried Theon away); his command role is interpretive => Tier-2."),
    (WARD, "LOCATED_AT", "pyke", 1, "acok", "acok-theon-01", 11,
     "Robert Baratheon's war galley had borne him away",
     "Theon was taken from Pyke, the Greyjoy seat."),
]

# Causal edge (Tier-2) — verified_by pending until subagent CONFIRM.
CAUSAL = [
    (REBELLION, "CAUSES", WARD, 2, "acok", "acok-theon-01", 207,
     "The whole castle, from Lady Stark to the lowliest kitchen scullion, knew he was hostage to his father's good behavior",
     "The lost rebellion is the mediated cause of the hostage-taking — Theon is held as surety for the defeated Balon's good behavior (Robert/Ned's decision sits between, modeled on the beat's role edges)."),
]


def make_row(spec, *, verified):
    src, etype, tgt, tier, book, chap, line, quote, asserted = spec
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
    lines = EDGES.read_text(encoding="utf-8").splitlines()
    if any(RUN_ID in ln for ln in lines):
        sys.exit(f"ABORT: run_id {RUN_ID} already present in {EDGES} — already minted.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    new_rows = [make_row(s, verified=None) for s in ROWS]
    new_rows += [make_row(s, verified="pending-s107-b2-verify") for s in CAUSAL]

    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges "
          f"({len(ROWS)} role + {len(CAUSAL)} causal tier-2).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines.")


if __name__ == "__main__":
    main()
