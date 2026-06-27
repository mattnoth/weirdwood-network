#!/usr/bin/env python3
"""Root the AFFC Cersei's-downfall arc at Tywin's death (S115 follow-up).

GAP (flagged by a parallel window, verified vs the live graph): the S114
Cersei's-downfall arc was built self-contained — `cersei-rearms-the-faith-and-
forgives-the-debt` had 0 causal upstream, so the Cersei chain was a cross-book
island. The "root each new arc at its existing upstream node" discipline was
missed. The true antecedent is the assassination of Tywin: while Tywin lived he
was Hand and controlled crown policy ("No one had ever balked her lord father.
When Tywin Lannister spoke, men obeyed." AFFC Cersei V, affc-cersei-05:281); his death makes Cersei
the unchecked Queen Regent ("It is my day now. It is my castle and my kingdom."
AFFC Cersei III), free to strike the disastrous Faith bargain a competent Hand
would never have permitted.

This is the 1-edge add that lets the Cersei downfall chain walk back through the
Tywin's-death arc (S109) to the Purple Wedding / Sansa's hairnet — the same
cross-book auto-join the Loremaster demo celebrates.

Edge (Tier-2, mediated via Cersei's unchecked regency; verified_by pending):
  assassination-of-tywin-lannister --CAUSES--> cersei-rearms-the-faith-and-forgives-the-debt

CAUSES vs MOTIVATES: target is an EVENT, so MOTIVATES (actor target) is type-
invalid; the regency mediation is carried inside the CAUSES edge (no separate
`cersei-becomes-regent` beat minted — scope creep; left to the verifier to
confirm the mediation doesn't require its own node). CAUSES not TRIGGERS: enabling
cause (removed the check), not an immediate spark.

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-cersei-tywin-root-2026-06-20.jsonl"

RUN_ID = "causal-arc-cersei-tywin-root-20260620"
PRODUCED_AT = "2026-06-20T00:00:00+00:00"
PENDING = "pending-s115-cersei-tywin-root-verify"

ROW = {
    "edge_type": "CAUSES",
    "source_slug": "assassination-of-tywin-lannister",
    "target_slug": "cersei-rearms-the-faith-and-forgives-the-debt",
    "decision": "emit_edge",
    "candidate_kind": "causal-curator-arc",
    "evidence_kind": "book-pass1",
    "typed_by": "curator-causal-arc",
    "schema_version": "pass1-derived-v1",
    "produced_at": PRODUCED_AT,
    "run_id": RUN_ID,
    "evidence_book": "affc",
    "evidence_chapter": "affc-cersei-03",
    "evidence_ref": "sources/chapters/affc/affc-cersei-03.md:229",
    "evidence_quote": (
        "All of them are burning now, she told herself, savoring the thought. They are dead "
        "and burning, every one, with all their plots and schemes and betrayals. It is my day "
        "now. It is my castle and my kingdom."
    ),
    "confidence_tier": 2,
    "asserted_relation": (
        "Tywin's assassination removes the one man who controlled crown policy (\"No one had "
        "ever balked her lord father. When Tywin Lannister spoke, men obeyed\"); as the now-"
        "unchecked Queen Regent (\"It is my day now. It is my castle and my kingdom\") Cersei is "
        "free to strike the disastrous bargain that rearms the Faith Militant and forgives the "
        "crown debt — a bargain a competent Hand would never have permitted. Mediated via her "
        "unchecked regency => CAUSES Tier-2. Roots the AFFC Cersei's-downfall chain into the "
        "S109 Tywin's-death arc (cross-book auto-join)."
    ),
    "verified_by": PENDING,
}


def main():
    lines = EDGES.read_text(encoding="utf-8").splitlines()
    if any(RUN_ID in ln for ln in lines):
        sys.exit(f"ABORT: run_id {RUN_ID} already present in {EDGES} — already minted.")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)
    with open(EDGES, "a", encoding="utf-8") as f:
        f.write(json.dumps(ROW, ensure_ascii=False) + "\n")
    print(f"Backed up -> {BACKUP.name}")
    print("Appended 1 causal Tier-2 edge (pending verify): "
          "assassination-of-tywin-lannister --CAUSES--> cersei-rearms-the-faith-and-forgives-the-debt")
    print(f"edges.jsonl now: {len(lines) + 1} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
