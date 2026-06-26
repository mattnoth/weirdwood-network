#!/usr/bin/env python3
"""Finalize the Battle of Castle Black enrichment (S153) after independent fresh-verify
(35 CONFIRM / 2 ADJUST / 0 REJECT; theory-gate CLEAN; 0 drift 37/37; all negative decisions upheld).

Applies, to graph/edges/edges.jsonl (run_id battle-castle-black-enrichment-s153, by candidate_id):
  DROP:
    - E36  aemon-targaryen-son-of-maekar-i DECEIVES styr  — the scarecrow-sentinel ruse is real but
           FAILS (Styr attacks anyway); DECEIVES over-asserts a successful deception and the vocab has
           no attempted/failed qualifier. Per propose-then-gate, retire the edge; the ruse stays as
           node-prose / a pass-2 candidate.
  KEEP (adjudicated against the verifier):
    - E24  janos-slynt MANIPULATES jon-snow  qualifier stays via_threat — the verifier preferred
           'via_coercion' but that value is NOT in the locked MANIPULATES enum
           (via_bribe/via_flattery/via_false_information/via_threat/via_seduction/unknown); via_threat
           is the correct enum-valid choice and the verifier accepted it as the fallback.
  STAMP verified_by='fresh-verify-s153' on every surviving run_id edge whose verified_by=='pending'.

Backup + re-run guard (aborts if E36 already gone). Idempotent."""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-battle-castle-black-finalize-2026-06-26.jsonl"
RUN_ID = "battle-castle-black-enrichment-s153"
VERIFIED_BY = "fresh-verify-s153"

DROP_CIDS = {"E36"}


def main():
    lines = [ln for ln in EDGES.read_text(encoding="utf-8").splitlines() if ln.strip()]
    rows = [json.loads(ln) for ln in lines]

    # re-run guard: E36 must still be present
    if not any(r.get("run_id") == RUN_ID and r.get("candidate_id") in DROP_CIDS for r in rows):
        sys.exit("ABORT: E36 not present — finalize already applied (or mint missing).")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    out = []
    n_drop = n_stamp = 0
    for r in rows:
        if r.get("run_id") == RUN_ID and r.get("candidate_id") in DROP_CIDS:
            n_drop += 1
            continue  # drop E36
        if r.get("run_id") == RUN_ID and r.get("verified_by") == "pending":
            r["verified_by"] = VERIFIED_BY
            n_stamp += 1
        out.append(json.dumps(r, ensure_ascii=False))

    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("── FINALIZE SUMMARY ──")
    print(f"Backup -> {BACKUP.relative_to(REPO)}")
    print(f"Edges dropped: {n_drop}  (E36 aemon DECEIVES styr — failed-deception over-assert)")
    print(f"verified_by stamped: {n_stamp}")
    print(f"Final edge count: {len(out)}")


if __name__ == "__main__":
    main()
