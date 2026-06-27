#!/usr/bin/env python3
"""Mint the J3 "Robb proclaimed King in the North" causal beat (S113 causal-arc track).

WO5K decomposition #1 (working/wo5k-decomposition.md, rank 1). `execution-of-
eddard-stark` had ZERO causal *downstream* edges; its load-bearing consequence —
the North secedes and the northern lords proclaim Robb King in the North — was
DARK. This extends the already-built B3 Ned's-downfall chain (S108) one hop.

New beat-node (written as .node.md, not here):
  - robb-proclaimed-king-in-the-north  (event.ceremony; AGOT Catelyn XI grounding)

Edges (chain-as-arc, NO umbrella parent):
  execution-of-eddard-stark --CAUSES--> robb-proclaimed-king-in-the-north  (Tier-2)
  execution-of-eddard-stark --MOTIVATES--> robb-stark                       (Tier-2)
  robb-stark --AGENT_IN--> robb-proclaimed-king-in-the-north                (Tier-1, role)

CAUSES (not TRIGGERS): the execution produces a political crisis that a lords'
council at Riverrun resolves by declaring independence — a mediated consequence,
not an immediate spark (per the S104 coarse-hub rule + agency-collapse check:
the lords'-council-proclaims-Robb is the clean single beat; the Greatjon's speech
is a step inside it, not a separate node). The lords explicitly cite Ned's murder
as the grounds (Galbart Glover: "He put your father to death").

MOTIVATES (execution -> robb-stark): Ned's murder is Robb's stated personal
motive for refusing peace and accepting the crown ("they murdered my lord
father ... This is the only peace I have for Lannisters").

AGENT_IN (robb-stark -> proclamation): links the subject to the event node so the
proclamation is directly traversable from Robb (per the decomposition doc's clean
model).

HARD-STOP: no causal edge into war-of-the-five-kings. The further WO5K mesh
(Robb's westerlands campaign, etc.) stays deferred.

Causal edges (Tier-2) carry verified_by='pending-s113-robb-king-verify' until a
fresh subagent confirms against the local cache.

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-robb-king-arc-2026-06-20.jsonl"

RUN_ID = "causal-arc-robb-king-20260620"
PRODUCED_AT = "2026-06-20T00:00:00+00:00"
COMMON = {
    "decision": "emit_edge",
    "candidate_kind": "causal-curator-arc",
    "evidence_kind": "book-pass1",
    "typed_by": "curator-causal-arc",
    "schema_version": "pass1-derived-v1",
    "produced_at": PRODUCED_AT,
    "run_id": RUN_ID,
}

NED_EXEC = "execution-of-eddard-stark"
ROBB_KING = "robb-proclaimed-king-in-the-north"
ROBB = "robb-stark"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified)
EDGES_SPEC = [
    (NED_EXEC, "CAUSES", ROBB_KING, 2, "agot", "agot-catelyn-11", 155,
     "You cannot mean to hold to Joffrey, my lord, Galbart Glover said. He put your father to death.",
     "Ned's execution is the political grounds the northern and river lords give for rejecting Joffrey's claim and declaring independence; the Riverrun war council that proclaims Robb king is convened in response to the murder. Mediated lords'-council decision => CAUSES Tier-2.",
     "pending-s113-robb-king-verify"),
    (NED_EXEC, "MOTIVATES", ROBB, 2, "agot", "agot-catelyn-11", 179,
     "My lady, they murdered my lord father, your husband, he said grimly. ... This is the only peace I have for Lannisters.",
     "Ned's murder is Robb's stated personal motive for refusing a negotiated peace and accepting the crown; he draws his sword as his answer to Catelyn's plea. Event-condition -> actor => MOTIVATES Tier-2.",
     "pending-s113-robb-king-verify"),
    (ROBB, "AGENT_IN", ROBB_KING, 1, "agot", "agot-catelyn-11", 209,
     "There sits the only king I mean to bow my knee to, m'lords, he thundered. The King in the North!",
     "Robb Stark is the subject of the proclamation; the Greatjon points to him and names him King in the North, and the assembled lords kneel. Role edge linking participant to event hub => AGENT_IN Tier-1.",
     None),
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
    lines = EDGES.read_text(encoding="utf-8").splitlines()
    if any(RUN_ID in ln for ln in lines):
        sys.exit(f"ABORT: run_id {RUN_ID} already present in {EDGES} — already minted.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    new_rows = [make_row(s) for s in EDGES_SPEC]

    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges ({sum(1 for s in EDGES_SPEC if s[1] in ('CAUSES','MOTIVATES'))} causal Tier-2 + role).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines.")


if __name__ == "__main__":
    main()
