#!/usr/bin/env python3
"""Mint the J7 "Karstark execution -> Robb isolation" beat (WO5K-remainder track, S123).

WO5K decomposition J7 (working/wo5k-decomposition.md, Rank 4). Closes the gap between
two already-built B1 segments. The B1 chain had:
  karstark-murders-prisoners-at-riverrun --CAUSES--> execution-of-rickard-karstark  [built]
  ... [DARK GAP] ...
  robb-weds-jeyne-westerling --TRIGGERS--> red-wedding-conspiracy                   [built]
The execution had ZERO causal *outgoing*. Its load-bearing consequence -- the Karstark
host deserts, gutting Robb's army and forcing him into the fatal Frey reconciliation --
was DARK.

CHRONOLOGY CORRECTION vs the decomp doc: the decomp listed the terminus as
`robb-weds-jeyne-westerling`, but the wedding (299) PRECEDES the Karstark execution (299,
later) -- you cannot wire exec -> wedding. The correct terminus is `red-wedding-conspiracy`
(the Frey re-negotiation that the execution-driven weakness pushes Robb into). Verified
against the live graph (occurred years + the existing robb-weds-jeyne TRIGGERS conspiracy
edge) before building. Trust the verified graph over the task-scoped decomp doc.

New beat-node (written as .node.md, not here):
  - karstark-host-deserts-robb  (event.incident; ASOS Catelyn III)

Edges (vocab-locked):
  execution-of-rickard-karstark --CAUSES-->  karstark-host-deserts-robb   (Tier-2)
  karstark-host-deserts-robb    --ENABLES--> red-wedding-conspiracy        (Tier-2)

CAUSES (execution -> desertion): the men desert the night Robb condemns their lord rather
than serve the king who killed him -- mediated by the host's collective decision to flee.
ENABLES (desertion -> conspiracy): the loss of "all the mounted strength of Karhold"
weakens Robb and deepens his dependence on a renewed Frey alliance; that desperation is
the precondition that walks him into the Twins and the Red Wedding trap. ENABLES (not
CAUSES): the Freys/Bolton/Tywin plot is set off by the Jeyne snub (already wired via
robb-weds-jeyne TRIGGERS conspiracy); the Karstark loss makes Robb VULNERABLE to it, it
does not author the plot. Precondition => ENABLES.

HARD-STOP: terminates at red-wedding-conspiracy (a concrete sub-event), not the
war-of-the-five-kings hub.

Causal edges (Tier-2) carry verified_by='pending-j7-verify' until a fresh subagent confirms.
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
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-j7-karstark-desertion-2026-06-22.jsonl"

RUN_ID = "causal-arc-j7-karstark-desertion-20260622"
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

KARSTARK_EXEC = "execution-of-rickard-karstark"
KARSTARK_MURDERS = "karstark-murders-prisoners-at-riverrun"
DESERTS = "karstark-host-deserts-robb"
RW_CONSPIRACY = "red-wedding-conspiracy"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified)
EDGES_SPEC = [
    # fresh-verify re-pointed source execution -> murders: the desertion at nightfall PRECEDES the
    # dawn execution, so exec->desertion was a cause-after-effect inversion. The murders are the
    # chronologically-prior root cause of BOTH the execution and the desertion (sibling consequences).
    (KARSTARK_MURDERS, "CAUSES", DESERTS, 2, "asos", "asos-catelyn-03", 89,
     "They started leaving at nightfall, stealing off in ones and twos at first, and then in larger groups.",
     "Rickard's murder of the captives doomed him; anticipating Robb's certain justice, the Karstark riders deserted that night (before the dawn execution) rather than serve the king who would kill their lord. Murders = prior root cause of both the execution and the desertion. CAUSES Tier-2.",
     "pending-j7-verify"),
    (DESERTS, "ENABLES", RW_CONSPIRACY, 2, "asos", "asos-catelyn-03", 135,
     "no response from Walder Frey to our new offer",
     "The loss of all the mounted strength of Karhold guts Robb's army and deepens his dependence on a renewed Frey alliance (he chases 'our new offer' to Walder Frey); that desperation is the precondition that draws him to the Twins and the Red Wedding trap. The plot itself is set off by the Jeyne snub (robb-weds-jeyne TRIGGERS conspiracy, already wired) -- the Karstark loss makes Robb vulnerable to it => ENABLES Tier-2.",
     "pending-j7-verify"),
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

    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges (2 causal Tier-2).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines.")


if __name__ == "__main__":
    main()
