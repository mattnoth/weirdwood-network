#!/usr/bin/env python3
"""Finalize Sansa/Vale enrichment pass 1 (S148) — apply the independent fresh-verify verdicts
(working/enrichment/sansa-vale/fresh-verify.md: 30 CONFIRM / 3 ADJUST / 0 REJECT + 3/3 nodes
confirmed + 1 retirement).

Actions:
  - RETIRE the S133 `petyr-baelish SUSPECTED_OF murder-of-jon-arryn` edge (run_id
    rr-enrichment-s133) — fresh-verify CONFIRMED the W1 upgrade to COMMANDS_IN (Lysa names LF as
    the order-giver directly to him, undenied; the in-world epistemic uncertainty SUSPECTED_OF
    encodes is removed). The SEPARATE `cersei-lannister SUSPECTED_OF` (AGOT/Ned's pre-confession
    suspicion, the false misdirection) is UNTOUCHED.
  - ADJUST SC3 (`robert-arryn WARD_OF petyr-baelish`): qualifier `formal` -> `unknown`. The
    verifier flagged that LF's authority is the Lord-Protector REGENCY Lysa granted, not a feudal
    wardship instrument (and the Lords Declarant contest it — Bronze Yohn wants Robert at
    Runestone). `de_facto` is not in the WARD_OF enum (formal/informal/hostage/unknown), so
    `unknown` honestly marks the regency-based custody that doesn't map to the feudal-ward enum.
  - ADJUST SP3 (`wedding ENABLES death-of-lysa-arryn`) note only: edge type/direction CONFIRMED;
    flag that the cited quote ("My sweet silly jealous wife") is from the murder scene, so the
    precondition logic (the instrumental marriage made LF Lord Protector + placed Lysa in his
    power) is inferential, not quote-proven.
  - ADJUST L6 (`moon-door WIELDED_IN death-of-lysa-arryn`) note only: CONFIRMED; clarify
    WIELDED_IN here = ENVIRONMENTAL instrument (the open Moon Door is the lethal feature she is
    shoved through), not a hand-held weapon.
  - STAMP verified_by 'pending' -> 'fresh-verify-s148' on all 34 surviving sansa-vale rows.

Net: 34 minted -0 dropped = 34 surviving edges; 3 nodes (all kept); +1 retirement (the old
SUSPECTED_OF). Backup first.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-sansa-vale-finalize-2026-06-25.jsonl"

RUN_ID = "sansa-vale-enrichment-s148"
VERIFIER = "fresh-verify-s148"

SC3_NOTE = ("Sweetrobin is in LF's care via the Lord-Protector regency (he 'rules the Eyrie' until "
            "Robert's sixteenth nameday) — a de-facto guardianship, NOT a feudal fostering compact; "
            "the Lords Declarant contest it (Bronze Yohn would take Robert to Runestone). qualifier "
            "'unknown' because the regency-custody does not map to the formal/informal/hostage enum.")
SP3_NOTE = ("BORDERLINE-CONFIRMED (fresh-verify): the instrumental loveless marriage made LF Lord "
            "Protector and placed Lysa in his power at the Eyrie, making the Moon Door murder both "
            "survivable and worthwhile (proximate trigger = Lysa's jealous rage over the snow-castle "
            "kiss). The precondition logic is INFERENTIAL — the cited quote is from the murder scene "
            "itself, not a passage that directly proves the marriage->murder enabling.")
L6_NOTE = ("The open Moon Door is the ENVIRONMENTAL instrument of death (Lysa is shoved backward "
           "through it to the valley floor), not a hand-held weapon — WIELDED_IN in the "
           "artifact-used-in-event sense. Lights the moon-door artifact node (0 prior edges).")


def main():
    raw = EDGES.read_text(encoding="utf-8").splitlines()
    rows = [json.loads(ln) for ln in raw if ln.strip()]

    shutil.copy2(EDGES, BACKUP)
    print(f"Backup written -> {BACKUP.relative_to(REPO)}")

    out = []
    dropped = stamped = adjusted = 0
    for r in rows:
        # RETIRE the S133 petyr SUSPECTED_OF murder-of-jon-arryn (NOT cersei's)
        if (r.get("run_id") == "rr-enrichment-s133"
                and r.get("edge_type") == "SUSPECTED_OF"
                and r.get("source_slug") == "petyr-baelish"
                and r.get("target_slug") == "murder-of-jon-arryn"):
            dropped += 1
            print("  RETIRED: petyr-baelish SUSPECTED_OF murder-of-jon-arryn (S133) "
                  "-> superseded by W1 COMMANDS_IN")
            continue

        if r.get("run_id") == RUN_ID:
            cid = r.get("candidate_id")
            if cid == "SC3":
                r["qualifier"] = "unknown"
                r["asserted_relation"] = SC3_NOTE
                adjusted += 1
            elif cid == "SP3":
                r["asserted_relation"] = SP3_NOTE
                adjusted += 1
            elif cid == "L6":
                r["asserted_relation"] = L6_NOTE
                adjusted += 1
            if r.get("verified_by") == "pending":
                r["verified_by"] = VERIFIER
                stamped += 1

        out.append(r)

    EDGES.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in out) + "\n",
                     encoding="utf-8")

    print("\n── FINALIZE SUMMARY ──")
    print(f"Retired (dropped): {dropped}")
    print(f"Adjusted (SC3/SP3/L6): {adjusted}")
    print(f"verified_by stamped -> {VERIFIER}: {stamped}")
    print(f"edges.jsonl: {len(rows)} -> {len(out)} lines ({len(out) - len(rows):+d})")


if __name__ == "__main__":
    main()
