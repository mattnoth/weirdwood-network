#!/usr/bin/env python3
"""S116 — mint `euron-hunts-aeron-damphair` (Matt: capture it now, don't log-for-later).

Extends Aeron's enrichment sub-arc one hop: his resistance vow + disappearance
CAUSES Euron to hunt him (via Erik Ironmaker). The "Crow's Eye slit his throat"
line is the in-world RUMOR (Tris Botley) — recorded as a node quote, NOT a
SUSPECTED_OF edge, because Aeron's death is unconfirmed in the 5 books (and TWOW
shows him alive). Downstream (TWOW capture) left dark.

Edges:
  aeron-vows-to-raise-the-ironborn-smallfolk --CAUSES--> euron-hunts-aeron-damphair  (Tier-2, pending)
  euron-greyjoy --COMMANDS_IN--> euron-hunts-aeron-damphair                          (Tier-1)
  erik-ironmaker --AGENT_IN--> euron-hunts-aeron-damphair                            (Tier-1)
  aeron-greyjoy --VICTIM_IN--> euron-hunts-aeron-damphair                            (Tier-1)
Re-run safe.
"""
import json, shutil, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-euron-hunts-aeron-2026-06-20.jsonl"
RUN_ID = "causal-arc-euron-hunts-aeron-20260620"
PENDING = "pending-s116-euron-hunts-aeron-verify"
COMMON = {"decision": "emit_edge", "candidate_kind": "causal-curator-arc", "evidence_kind": "book-pass1",
          "typed_by": "curator-causal-arc", "schema_version": "pass1-derived-v1",
          "produced_at": "2026-06-20T00:00:00+00:00", "run_id": RUN_ID}

VOWS = "aeron-vows-to-raise-the-ironborn-smallfolk"
HUNT = "euron-hunts-aeron-damphair"
EURON = "euron-greyjoy"; ERIK = "erik-ironmaker"; AERON = "aeron-greyjoy"

EDGES_SPEC = [
    (VOWS, "CAUSES", HUNT, 2, "adwd", "adwd-the-wayward-bride-01", 183,
     "Ironmaker's search is just to make us believe the priest escaped.",
     "Aeron's vow to raise the smallfolk against Euron makes the vanished priest a standing threat to Euron's rule; Euron sets Erik Ironmaker to hunt him. Mediated by Euron's need to silence the resistance => CAUSES Tier-2.",
     PENDING),
    (EURON, "COMMANDS_IN", HUNT, 1, "adwd", "adwd-the-wayward-bride-01", 183,
     "Ironmaker's search is just to make us believe the priest escaped.",
     "Euron orders the search for Aeron (the orderer, not the executor). Role edge => COMMANDS_IN Tier-1.",
     None),
    (ERIK, "AGENT_IN", HUNT, 1, "adwd", "adwd-the-wayward-bride-01", 183,
     "Ironmaker's search is just to make us believe the priest escaped.",
     "Erik Ironmaker conducts the hunt for the Damphair. Role edge => AGENT_IN Tier-1.",
     None),
    (AERON, "VICTIM_IN", HUNT, 1, "adwd", "adwd-the-wayward-bride-01", 183,
     "I think the Damphair's dead. I think the Crow's Eye slit his throat for him.",
     "Aeron is the hunted target (and the subject of the murder rumor). Role edge => VICTIM_IN Tier-1.",
     None),
]


def make_row(spec):
    src, etype, tgt, tier, book, chap, line, quote, asserted, verified = spec
    row = {"edge_type": etype, "source_slug": src, "target_slug": tgt, **COMMON,
           "evidence_book": book, "evidence_chapter": chap,
           "evidence_ref": f"sources/chapters/{book}/{chap}.md:{line}",
           "evidence_quote": quote, "confidence_tier": tier, "asserted_relation": asserted}
    if verified is not None:
        row["verified_by"] = verified
    return row


def main():
    lines = EDGES.read_text(encoding="utf-8").splitlines()
    if any(RUN_ID in ln for ln in lines):
        sys.exit(f"ABORT: run_id {RUN_ID} already present — already minted.")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)
    new_rows = [make_row(s) for s in EDGES_SPEC]
    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges (1 causal Tier-2 pending + 3 role). Now {len(lines)+len(new_rows)} (was {len(lines)}).")


if __name__ == "__main__":
    main()
