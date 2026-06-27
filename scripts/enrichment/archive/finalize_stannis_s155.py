#!/usr/bin/env python3
"""Finalize the A2.7 "Stannis Baratheon" enrichment (S155) after independent fresh-verify
(27 CONFIRM / 4 ADJUST / 0 REJECT; theory-gate CLEAN; all 3 nodes confirmed distinct).

Applies to graph/edges/edges.jsonl (by run_id stannis-enrichment-s155, matched on candidate_id):

  ADJUST E21 (renly-s-death-reflection MOTIVATES stannis-baratheon): downgrade tier-1 -> tier-2.
    The guilt-haunting is interpretive (one hop from "I dream of it" to "drives his severity"). The
    fresh-verify's separate "hold — staged node" concern is MOOT: `renly-s-death-reflection` is live in
    graph/nodes/events/ and already edge-bearing (stannis AGENT_IN it pre-dates this dip); the
    "Staging only" line in its body is stale plate-3 boilerplate. Target resolves — no hold needed.

  ADJUST E22 (davos MOTIVATES stannis-baratheon): refine the asserted_relation note for precision.
    The fresh-verify correctly noted the "a king protects his people" quote sits inside the Edric-Storm
    confrontation; that confrontation IS the asos-davos-06 scene where Stannis, having lost Edric to the
    smuggling, resolves to take his host north to the Wall. (The fresh-verify's guess that the march
    decision lives in adwd-jon-04 is wrong — adwd-jon-04 is Stannis already AT the Wall.) Edge structure
    unchanged; note sharpened.

  KEEP E7 (stannis WORSHIPS rhllor, tier-2) — REJECTED the fresh-verify's "WORSHIPS -> FOLLOWS" suggestion:
    FOLLOWS is NOT in the locked 170-type vocab, and SERVES (its fallback) carries wrong server->served
    semantics for a person->deity public conversion. WORSHIPS at Tier-2 + the node-prose capturing the
    skepticism ("I know little and care less of gods" / instrumental "red hawk") is the honest model and
    matches the existing graph pattern (thoros/harwin/selyse WORSHIPS rhllor). The fresh-verify itself
    allowed "If WORSHIPS is the only available edge type for person->deity, keep it at Tier-2."

  KEEP E31 (jon-snow ADVISES stannis-baratheon) — dup-check ran: no pre-existing jon ADVISES stannis edge.

  STAMP verified_by='fresh-verify-s155' on every surviving run_id edge whose verified_by=='pending'
    (the 10 flagged interpretive/causal/borderline edges).

Backup + re-run guard (aborts if nothing left to stamp). Idempotent."""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-stannis-finalize-2026-06-26.jsonl"
RUN_ID = "stannis-enrichment-s155"
VERIFIED_BY = "fresh-verify-s155"

TIER_DOWNGRADE = {"E21": "tier-2"}
NOTE_PATCH = {
    "E22": ("MARQUEE why-march-north: Davos's 'a king protects his people' argument in the asos-davos-06 "
            "Edric-Storm confrontation -- the scene where Stannis, having lost Edric to Davos's smuggling, "
            "resolves to take his host north to the Wall. The MOTIVATES the spine lacked (it had only "
            "retreat ENABLES move-to-wall, no character-motive). Fresh-verify-s155 sharpened the note."),
}


def main():
    lines = [ln for ln in EDGES.read_text(encoding="utf-8").splitlines() if ln.strip()]
    rows = [json.loads(ln) for ln in lines]

    pending = [r for r in rows if r.get("run_id") == RUN_ID and r.get("verified_by") == "pending"]
    if not pending:
        sys.exit("ABORT: no pending run_id edges to stamp — finalize already applied (or mint missing).")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    n_tier = n_note = n_stamp = 0
    for r in rows:
        if r.get("run_id") != RUN_ID:
            continue
        cid = r.get("candidate_id")
        if cid in TIER_DOWNGRADE and r.get("confidence_tier") != TIER_DOWNGRADE[cid]:
            r["confidence_tier"] = TIER_DOWNGRADE[cid]
            n_tier += 1
        if cid in NOTE_PATCH:
            r["asserted_relation"] = NOTE_PATCH[cid]
            n_note += 1
        if r.get("verified_by") == "pending":
            r["verified_by"] = VERIFIED_BY
            n_stamp += 1

    out = [json.dumps(r, ensure_ascii=False) for r in rows]
    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("── FINALIZE SUMMARY ──")
    print(f"Backup -> {BACKUP.relative_to(REPO)}")
    print(f"Tier downgrades applied: {n_tier}  (E21 -> tier-2)")
    print(f"Note patches applied: {n_note}  (E22 sharpened)")
    print(f"verified_by stamped: {n_stamp}")
    print(f"Edges dropped: 0  (fresh-verify 0 REJECT)")
    print(f"Final edge count: {len(out)}")


if __name__ == "__main__":
    main()
