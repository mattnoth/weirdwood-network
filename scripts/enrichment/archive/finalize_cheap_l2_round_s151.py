#!/usr/bin/env python3
"""Finalize the S151 cheap-L2 enrichment round after independent fresh-verify
(9 CONFIRM / 2 ADJUST / 0 REJECT; gated-boundary PASS x3 — Robert-Strong != Gregor,
gravedigger != Sandor, Frey-pies framed as implication).

Applies, to graph/edges/edges.jsonl:

  DROP (run_id cheap-l2-round-s151, by candidate_id):
    - B2-E06  creation-of-robert-strong ENABLES cersei-resolves-on-trial-by-combat
              TEMPORALLY BACKWARDS. At the AFFC resolution (affc-cersei-10:313) Cersei
              explicitly CANNOT use Robert Strong ("I am forbidden to make use of him ...
              My honor can only be defended by a Sworn Brother of the Kingsguard") and
              resolves on trial by battle while sending for JAIME as champion. Robert Strong
              only becomes a usable champion in ADWD (Tommen names him to the Kingsguard),
              AFTER the resolution. So the creation does not ENABLE the resolution. The
              champion-for-the-trial payoff is captured in the node prose (accurate) and
              awaits a future trial-by-combat node. (Verifier flagged ADJUST/re-cite; synthesis
              judgment is DROP — re-citing can't fix the temporal inversion.)

  NOTE-ADJUST (run_id, by candidate_id):
    - B4-E05  varys MANIPULATES eddard-stark (via_threat) — note sharpened to record that the
              compound method's false-promise dimension (the Wall bargain the queen never honors)
              is already covered by the existing S137 `varys DECEIVES eddard-stark` (T2), so the
              via_threat MANIPULATES stays the distinct coercion edge. Tier/qualifier unchanged.

  RETIRE (existing edges, NOT this run_id — confirmed data errors / slug misfires):
    - elder-brother HEALS sandor-clegane   (Pass-1 slug artifact: the HEALS sits on the TITLE
           node `elder-brother`, not the PERSON `elder-brother-quiet-isle`; superseded by the
           corrected B3-E2 edge minted this round.)
    - sandor-clegane OWNS stranger         (`stranger` is the RELIGION node; the horse is
           `stranger-horse`. The correct `sandor-clegane OWNS stranger-horse` already exists.)
    - sandor-clegane BONDED_TO stranger    (same religion-vs-horse misfire; correct
           `stranger-horse BONDED_TO sandor-clegane` already exists.)

  STAMP verified_by='fresh-verify-s151' on every surviving run_id edge whose verified_by=='pending'.

Backup + re-run guard (aborts if B2-E06 already gone)."""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-cheap-l2-finalize-2026-06-26.jsonl"
RUN_ID = "cheap-l2-round-s151"
VERIFIED_BY = "fresh-verify-s151"

DROP_CANDIDATE_IDS = {"B2-E06"}

NOTE_UPDATES = {
    "B4-E05": ("The closing ultimatum is an explicit conditional threat (Sansa's head) -> via_threat. "
               "The compound method's false-promise dimension (the Wall bargain the queen never honors) "
               "is already covered by the existing S137 `varys DECEIVES eddard-stark` (T2); this "
               "MANIPULATES is the distinct coercion-by-threat edge."),
}

RETIRE = [
    ("elder-brother", "HEALS", "sandor-clegane"),
    ("sandor-clegane", "OWNS", "stranger"),
    ("sandor-clegane", "BONDED_TO", "stranger"),
]


def main():
    lines = [ln for ln in EDGES.read_text(encoding="utf-8").splitlines() if ln.strip()]
    rows = [json.loads(ln) for ln in lines]

    # re-run guard: B2-E06 must still be present
    if not any(r.get("run_id") == RUN_ID and r.get("candidate_id") in DROP_CANDIDATE_IDS for r in rows):
        sys.exit("ABORT: B2-E06 not present — finalize already applied.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    retire_set = set(RETIRE)
    out = []
    n_drop = n_note = n_stamp = n_retire = 0
    for r in rows:
        key = (r.get("source_slug"), r.get("edge_type"), r.get("target_slug"))
        if r.get("run_id") == RUN_ID and r.get("candidate_id") in DROP_CANDIDATE_IDS:
            n_drop += 1
            continue  # drop the anachronistic edge
        if key in retire_set and r.get("run_id") != RUN_ID:
            n_retire += 1
            continue  # retire the misfire
        if r.get("run_id") == RUN_ID:
            cid = r.get("candidate_id")
            if cid in NOTE_UPDATES:
                r["asserted_relation"] = NOTE_UPDATES[cid]
                n_note += 1
            if r.get("verified_by") == "pending":
                r["verified_by"] = VERIFIED_BY
                n_stamp += 1
        out.append(json.dumps(r, ensure_ascii=False))

    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("── FINALIZE SUMMARY ──")
    print(f"Backup -> {BACKUP.relative_to(REPO)}")
    print(f"Edges dropped (this run): {n_drop}  (B2-E06 anachronistic ENABLES)")
    print(f"Notes adjusted: {n_note}  (B4-E05)")
    print(f"Misfires retired (pre-existing): {n_retire}  (elder-brother HEALS; sandor OWNS/BONDED_TO stranger-religion)")
    print(f"verified_by stamped: {n_stamp}")
    print(f"Final edge count: {len(out)}")


if __name__ == "__main__":
    main()
