#!/usr/bin/env python3
"""Finalize the A1.6 "Kingsmoot / Euron" enrichment (S157) after independent fresh-verify
(36 CONFIRM / 1 ADJUST / 0 REJECT; theory-gate CLEAN; the anarchy-in-the-reach trap-drop CONFIRMED correct).

One job: (A) apply the single fresh-verify ADJUST (E32 note tightening) + stamp verified_by on the 7
flagged run_id edges. No drops, no bug-fixes this dip (pure edge-only, all 37 survive).

(A) Fresh-verify result (run_id=euron-enrichment-s157, by candidate_id):
  CONFIRM ×36 — all interpretive/causal/borderline edges held:
    E3  euron COMMANDS_IN taking-of-the-shields  (Euron 'lazing in a castle' reaver:57 — orderer-not-present, correct)
    E15 aeron OFFICIATES kingsmoot               (silences/recites-liturgy/blesses — distinct from AGENT_IN)
    E17 cragorn AGENT_IN kingsmoot               (only one blew Dragonbinder; Euron names him Cragorn reaver:243-247)
    E33 euron MANIPULATES hotho-harlaw via_bribe (Hotho fills hands with gold then shouts Euron — correct frame)
    E34 kingsmoot MOTIVATES victarion            ('then all was changed' iron-captain:27 — sound)
    E37 euron AGENT_IN burning-of-the-lannister-fleet (shared-agency, Tier-2 planner — warranted)
  ADJUST ×1:
    E32 eurons-mongrel-sons CREW_OF silence — keep edge + Tier-2; TIGHTEN the note: the node is a SUBSET of
        the Silence's full 'mutes and mongrels' crew (which also includes mutes + Sothoryos foreigners), not
        coextensive with it. The bastard sons do serve aboard. Edge sound; only the identity claim is sharpened.
  REJECT ×0.
  STAMP verified_by='fresh-verify-s157' on every run_id edge whose verified_by=='pending'
    (the 7 flagged interpretive/borderline edges: E3, E15, E17, E32, E33, E34, E37).

Backup + re-run guard. Idempotent-ish (aborts if nothing left to do)."""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-euron-finalize-2026-06-27.jsonl"
RUN_ID = "euron-enrichment-s157"
VERIFIED_BY = "fresh-verify-s157"

NOTE_PATCH = {
    "E32": ("The Silence is crewed by Euron's mutes and mongrels; his bastard 'mongrel sons' serve aboard "
            "(one runs a message at the Reaver feast). NOTE (fresh-verify-s157): the node eurons-mongrel-sons "
            "is a SUBSET of the full crew — the 'motley crew of mutes and mongrels' (iron-captain-01:43) also "
            "includes voiceless mutes and squat hairy Sothoryos foreigners — not coextensive with it. The "
            "CREW_OF edge is sound; the identity claim is scoped to the bastard-sons subset. Lights the "
            "0-edge eurons-mongrel-sons node. Tier-2."),
}


def main():
    lines = [ln for ln in EDGES.read_text(encoding="utf-8").splitlines() if ln.strip()]
    rows = [json.loads(ln) for ln in lines]

    pending = [r for r in rows if r.get("run_id") == RUN_ID and r.get("verified_by") == "pending"]
    if not pending:
        sys.exit("ABORT: nothing to do — finalize already applied (or mint missing).")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    n_note = n_stamp = 0
    for r in rows:
        if r.get("run_id") != RUN_ID:
            continue
        cid = r.get("candidate_id")
        if cid in NOTE_PATCH:
            r["asserted_relation"] = NOTE_PATCH[cid]
            n_note += 1
        if r.get("verified_by") == "pending":
            r["verified_by"] = VERIFIED_BY
            n_stamp += 1

    EDGES.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    print("── FINALIZE SUMMARY ──")
    print(f"  note patches (E32):    {n_note}")
    print(f"  verified_by stamps:    {n_stamp}")
    print(f"  rows: {len(rows)} (unchanged — no drops)")


if __name__ == "__main__":
    main()
