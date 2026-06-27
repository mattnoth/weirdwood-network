#!/usr/bin/env python3
"""Finalize the Arya/Braavos enrichment (S150) after independent fresh-verify
(8 CONFIRM / 3 ADJUST / 0 REJECT; 1 retirement; no theory leakage; 0 drift 44/44).

Applies, to graph/edges/edges.jsonl:
  ADJUST (run_id arya-braavos-enrichment-s150, matched by candidate_id):
    - RL18 kindly-man COMMANDS_IN arya-assassinates-the-insurance-broker
           confidence_tier 1 -> 2 (distributed authority: the FORMAL assignment is the unnamed
           plague-face priest's; the kindly man is the day-to-day handler/briefer/confirmer).
    - SP4  killing-of-dareon CAUSES blinding-of-arya
           NOTE sharpened (acceleration-not-sole-cause): the blinding was a planned blind-acolyte
           training step; the unsanctioned kill brought it forward ~6 months as punishment.
           Type stays CAUSES (the punitive blinding-NOW is produced through the kindly man's
           decision; mediation is allowed under CAUSES). Fresh-verify endorsed CAUSES+note.
    - RL13 waif AGENT_IN blinding-of-arya  NOTE tightened (executor of the ongoing milk regime,
           ADWD:79; the kindly man is principal/orderer, RL11). Type/tier unchanged (Tier-2).
  STAMP verified_by='fresh-verify-s150' on every run_id edge whose verified_by=='pending'.
  RETIRE (existing edge, NOT this run_id — confirmed direction error by fresh-verify):
    - RC1  arya-stark TUTORS kindly-man  (affc-arya-02:23 — the Kindly Man tutors Arya, not the
           reverse; redundant with the correct existing `kindly-man TEACHES arya-stark`.)

Backup + re-run guard. Idempotent: aborts if RL18 is already Tier-2."""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-arya-braavos-finalize-2026-06-26.jsonl"
RUN_ID = "arya-braavos-enrichment-s150"
VERIFIED_BY = "fresh-verify-s150"

NOTE_UPDATES = {
    "SP4": ("The blinding is the FM punishment for the UNSANCTIONED killing of Dareon — but the "
            "blinding was a planned blind-acolyte training step the kindly man says they would have "
            "done 'anyway'; the kill brought it forward by ~half a year. CAUSES (mediated by his "
            "punitive decision) of the early/punitive blinding-now, not of the eventual blinding."),
    "RL13": ("The waif is the EXECUTOR of the ongoing blinding draught (the nightly milk regime, "
             "ADWD blind-girl:79); the kindly man is the principal who ORDERS it (RL11). Tier-2 "
             "reflects executor-not-principal."),
    "RL18": ("The FORMAL kill-assignment is given by an unnamed plague-face priest (single-use, not "
             "graphed); the kindly man is the day-to-day handler who briefs the target, sets the "
             "method, and confirms the kill ('his heart gave out'). Best-available COMMANDS_IN "
             "attribution; Tier-2 for the distributed authority."),
}
TIER_UPDATES = {"RL18": 2}

RETIRE = [
    ("arya-stark", "TUTORS", "kindly-man"),
]


def main():
    lines = [ln for ln in EDGES.read_text(encoding="utf-8").splitlines() if ln.strip()]
    rows = [json.loads(ln) for ln in lines]

    # re-run guard
    for r in rows:
        if r.get("run_id") == RUN_ID and r.get("candidate_id") == "RL18" and r.get("confidence_tier") == 2:
            sys.exit("ABORT: RL18 already Tier-2 — finalize already applied.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    retire_set = set(RETIRE)
    out = []
    n_adjust = n_tier = n_stamp = n_retire = 0
    for r in rows:
        key = (r.get("source_slug"), r.get("edge_type"), r.get("target_slug"))
        if key in retire_set:
            n_retire += 1
            continue  # drop
        if r.get("run_id") == RUN_ID:
            cid = r.get("candidate_id")
            if cid in NOTE_UPDATES:
                r["asserted_relation"] = NOTE_UPDATES[cid]
                n_adjust += 1
            if cid in TIER_UPDATES:
                r["confidence_tier"] = TIER_UPDATES[cid]
                n_tier += 1
            if r.get("verified_by") == "pending":
                r["verified_by"] = VERIFIED_BY
                n_stamp += 1
        out.append(json.dumps(r, ensure_ascii=False))

    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("── FINALIZE SUMMARY ──")
    print(f"Backup -> {BACKUP.relative_to(REPO)}")
    print(f"Notes adjusted: {n_adjust}  (SP4, RL13, RL18)")
    print(f"Tier downgrades: {n_tier}  (RL18 -> 2)")
    print(f"verified_by stamped: {n_stamp}")
    print(f"Edges retired: {n_retire}  (arya-stark TUTORS kindly-man)")
    print(f"Final edge count: {len(out)}")


if __name__ == "__main__":
    main()
