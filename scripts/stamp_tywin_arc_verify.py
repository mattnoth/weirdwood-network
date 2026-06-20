#!/usr/bin/env python3
"""Apply the S109 fresh-verifier verdict to the Tywin-death arc edges.

The verifier (fresh general-purpose subagent vs local cache, 2026-06-19) returned:
  - Edge #1 trial-of-tyrion-lannister --CAUSES--> gregor-confesses-and-kills-oberyn:
    RETYPE CAUSES -> TRIGGERS (the trial-by-combat death is the trial's immediate
    unmediated decisive act, not a mediated downstream effect).
  - Edges #2-#6: CONFIRM as-is.
  - Node retype, role edges, hard-stop: all CONFIRM/CLEAN.

This script:
  1. backs up edges.jsonl,
  2. retypes the one CAUSES->TRIGGERS edge (+updates its asserted_relation),
  3. stamps verified_by='subagent-local-source-check-2026-06-19' on all 6 causal
     edges of run_id=causal-arc-tywin-death-20260619 (those carrying the pending
     marker), replacing 'pending-s109-tywin-verify'.

Re-run safe: idempotent — if no pending markers remain, it reports and exits.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-tywin-verify-stamp-2026-06-19.jsonl"

RUN_ID = "causal-arc-tywin-death-20260619"
PENDING = "pending-s109-tywin-verify"
CONFIRMED = "subagent-local-source-check-2026-06-19"

RETYPE_SRC = "trial-of-tyrion-lannister"
RETYPE_TGT = "gregor-confesses-and-kills-oberyn"
NEW_ASSERTED = ("Tyrion's trial proceeds to trial by combat; the Mountain killing "
                "Oberyn (Tyrion's champion) IS the trial's decisive culminating act "
                "that condemns Tyrion — immediate, no mediating human decision => "
                "TRIGGERS Tier-2.")


def main():
    lines = EDGES.read_text(encoding="utf-8").splitlines()
    if not any(PENDING in ln for ln in lines):
        sys.exit(f"Nothing to do: no '{PENDING}' markers present (already stamped?).")

    shutil.copy2(EDGES, BACKUP)

    out = []
    stamped = retyped = 0
    for ln in lines:
        if RUN_ID in ln and PENDING in ln:
            row = json.loads(ln)
            if row.get("verified_by") == PENDING:
                row["verified_by"] = CONFIRMED
                stamped += 1
                if (row["source_slug"] == RETYPE_SRC
                        and row["target_slug"] == RETYPE_TGT
                        and row["edge_type"] == "CAUSES"):
                    row["edge_type"] = "TRIGGERS"
                    row["asserted_relation"] = NEW_ASSERTED
                    retyped += 1
                out.append(json.dumps(row, ensure_ascii=False))
                continue
        out.append(ln)

    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Backed up -> {BACKUP.name}")
    print(f"Stamped verified_by={CONFIRMED} on {stamped} causal edges.")
    print(f"Retyped {retyped} edge CAUSES->TRIGGERS ({RETYPE_SRC} -> {RETYPE_TGT}).")


if __name__ == "__main__":
    main()
