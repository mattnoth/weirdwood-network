#!/usr/bin/env python3
"""Finalize the A1.5 "Dorne / Queenmaker" enrichment (S156) after independent fresh-verify
(35 CONFIRM / 4 ADJUST / 0 REJECT; theory-gate CLEAN; informer non-mint CONFIRMED correct).

Two jobs: (A) apply the fresh-verify adjusts + stamp verified_by on the run_id edges; (B) fix the
wrong-target conspirator-Garin BUG (the new garin-of-the-orphans node now exists, so the mis-pointed
edges can be corrected).

(A) Fresh-verify adjusts (applied to run_id=dorne-enrichment-s156 by candidate_id):
  DROP E15 (doran-martell MARRIES_OFF sylva-santagar): fresh-verify REJECT. The text says "Her FATHER has
    shipped her to Greenstone to wed Lord Estermont" and Doran says she received "no punishment from me" —
    Doran-as-arranger is NOT supported; Sylva's father arranged it independently. Dropped.
  PATCH note E1 (myrcella CLAIMS iron-throne): clarify the claim is asserted ON Myrcella's behalf by the
    conspirators (she is a confused child who does not claim it herself); the Dornish-primogeniture claim
    nonetheless exists in-world. Type/tier confirmed right (T2 — disputed by Westerosi custom).
  PATCH note E19 (gerold-dayne OPPOSES the-queenmaker-plot): clarify OPPOSES = the METHOD/GOAL (he scorned
    crowning Myrcella and maimed her to spark war), NOT his physical participation (he is AGENT_IN the act).
    OPPOSES is Tier-3 → NO qualifier (the validator rejects Tier-3 qualifiers); the distinction lives in the note.
  KEEP E5 (arys-oakheart BREAKS_VOW tommen-baratheon): fresh-verify confirmed the TARGET (the reigning king
    he conspires against). The evidence_quote "I swore an oath" is Arys's OWN line (not Arianne's rhetorical
    "To Joffrey, not to Tommen"), so no re-anchor needed. Kept as-is.
  STAMP verified_by='fresh-verify-s156' on every surviving run_id edge whose verified_by=='pending'
    (the 9 surviving flagged interpretive/causal/borderline edges; E15's pending stamp is dropped with it).

(B) Conspirator-Garin wrong-target BUG fix (4 pre-existing edges mis-pointed at the LEGENDARY garin-the-great):
  DROP   arianne-martell CONSPIRES_WITH garin-the-great   (replaced by E8 garin-of-the-orphans CONSPIRES_WITH arianne)
  DROP   arianne-martell MILK_BROTHER_OF garin-the-great  (replaced by E9 garin-of-the-orphans MILK_BROTHER_OF arianne)
  REPOINT cedra LOVES garin-the-great        -> target garin-of-the-orphans (the Cedra/Garin fling; conspirator Garin)
  REPOINT garin-the-great LOVER_OF cedra     -> source garin-of-the-orphans (the reverse of the same fling)
  The 4 genuine legendary-Garin edges (HOLDS_TITLE prince-of-chroyane / SWORN_TO + CULTURE_OF rhoynar /
  DIED_AT chroyane) are UNTOUCHED.

Backup + re-run guard. Idempotent-ish (aborts if nothing left to do)."""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-dorne-finalize-2026-06-27.jsonl"
RUN_ID = "dorne-enrichment-s156"
VERIFIED_BY = "fresh-verify-s156"

DROP_CIDS = {"E15"}
NOTE_PATCH = {
    "E1": ("The Queenmaker plot's foundational legal premise: Myrcella's Dornish-primogeniture claim (older "
           "than Tommen). The claim is asserted ON her behalf by the conspirators (Tyene/Arianne lay it out) "
           "-- Myrcella herself is a confused child who does not claim it. FIRST CLAIMS-iron-throne edge in the "
           "graph; wires the Dorne arc to the throne it targets. Tier-2 -- disputed by Westerosi custom (no "
           "ruling queen). Fresh-verify-s156 confirmed type+tier, sharpened the note."),
    "E19": ("The saboteur-within: Darkstar scorned the plot's METHOD and GOAL from the start ('crowning the "
            "Lannister girl is a hollow gesture... nor will you get the war you want') and maimed Myrcella at "
            "the Greenblood to spark the war the plot was deliberately avoiding. OPPOSES captures his stance "
            "toward the PLAN -- NOT his physical participation (he is also AGENT_IN the act). Tier-3 (no "
            "qualifier). Fresh-verify-s156 confirmed; note sharpened to mark the AGENT_IN/OPPOSES coexistence."),
}

# (B) bug-fix tuples on (source, type, target)
BUG_DROP = {
    ("arianne-martell", "CONSPIRES_WITH", "garin-the-great"),
    ("arianne-martell", "MILK_BROTHER_OF", "garin-the-great"),
}
BUG_REPOINT_TARGET = {  # (source, type, target) -> new target
    ("cedra", "LOVES", "garin-the-great"): "garin-of-the-orphans",
}
BUG_REPOINT_SOURCE = {  # (source, type, target) -> new source
    ("garin-the-great", "LOVER_OF", "cedra"): "garin-of-the-orphans",
}


def trip(r):
    return (r.get("source_slug"), r.get("edge_type"), r.get("target_slug"))


def main():
    lines = [ln for ln in EDGES.read_text(encoding="utf-8").splitlines() if ln.strip()]
    rows = [json.loads(ln) for ln in lines]

    pending = [r for r in rows if r.get("run_id") == RUN_ID and r.get("verified_by") == "pending"]
    bug_present = any(trip(r) in BUG_DROP or trip(r) in BUG_REPOINT_TARGET or trip(r) in BUG_REPOINT_SOURCE for r in rows)
    if not pending and not bug_present:
        sys.exit("ABORT: nothing to do — finalize already applied (or mint missing).")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    out = []
    n_drop = n_note = n_stamp = n_bugdrop = n_repoint = 0
    for r in rows:
        cid = r.get("candidate_id")
        rid = r.get("run_id")
        t = trip(r)

        # (A) drop the fresh-verify rejects from this run
        if rid == RUN_ID and cid in DROP_CIDS:
            n_drop += 1
            continue

        # (B) drop the redundant wrong-target conspirator-Garin edges
        if t in BUG_DROP:
            n_bugdrop += 1
            continue

        # (B) re-point the Cedra/Garin fling edges to the new node
        if t in BUG_REPOINT_TARGET:
            r["target_slug"] = BUG_REPOINT_TARGET[t]
            r["repoint_note"] = "S156 bug-fix: re-pointed from legendary garin-the-great to conspirator garin-of-the-orphans"
            n_repoint += 1
        elif t in BUG_REPOINT_SOURCE:
            r["source_slug"] = BUG_REPOINT_SOURCE[t]
            r["repoint_note"] = "S156 bug-fix: re-pointed from legendary garin-the-great to conspirator garin-of-the-orphans"
            n_repoint += 1

        # (A) note patches + verified_by stamp on this run's edges
        if rid == RUN_ID:
            if cid in NOTE_PATCH:
                r["asserted_relation"] = NOTE_PATCH[cid]
                n_note += 1
            if r.get("verified_by") == "pending":
                r["verified_by"] = VERIFIED_BY
                n_stamp += 1

        out.append(r)

    EDGES.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in out) + "\n", encoding="utf-8")
    print("── FINALIZE SUMMARY ──")
    print(f"  fresh-verify DROP (E15):       {n_drop}")
    print(f"  note patches (E1,E19):         {n_note}")
    print(f"  verified_by stamps:            {n_stamp}")
    print(f"  bug DROP (arianne->garin-great): {n_bugdrop}")
    print(f"  bug REPOINT (cedra<->garin):     {n_repoint}")
    print(f"  rows: {len(rows)} -> {len(out)}")


if __name__ == "__main__":
    main()
