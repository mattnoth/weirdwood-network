#!/usr/bin/env python3
"""Apply S146 Bran/greenseer fresh-verify adjustments to edges.jsonl
(independent Sonnet verdict: 10 CONFIRM / 4 ADJUST / 1 REJECT + 4 post-verify modifications).

  DROP   GD2 (jojen FORESHADOWS sack-of-winterfell)        — COLLAPSE into GD1 (DREAMS_OF already
         carries the reader-facing function; the line-81 quote is the same dream's next sentence)
         GD4 (jojen FORESHADOWS bran-becomes-a-greenseer)  — COLLAPSE into GD3 (Jojen's in-passage
         interpretation, not a distinct authorial foreshadowing signal)
         CF2 (leaf TEACHES bran-stark)                     — REJECT (Leaf gives contextual
         exposition + administers the paste ceremony; not sustained didactic instruction)
  RETARGET GD5 (jojen DREAMS_OF ...): target robb-receives-false-news-of-brans-death ->
         sack-of-winterfell — the 'Reek skinning your faces' dream is about Bran/Rickon's danger
         in the sack, NOT Robb's downstream information state. Keep T2 (subverted dream).
  TIER   BR2 (brynden-rivers BONDED_TO weirwood)  T2 -> T1 (Leaf states it outright + roots-through-
         flesh described graphically — canon fact, not interpretive)
         RV2 (brynden-rivers REVEALS_TO meera)    T2 -> T1 (first-person name disclosure)
  STAMP  verified_by = "fresh-verify-confirmed-s146" on every surviving verify=true edge
         (GD1 GD3 GD5 GD6 PR3 BR1 BR2 ME2 HO1 RV1 RV2 SB1).

  POST-VERIFY MODIFICATIONS — the `three-eyed-crow` slug-trap surgery (all 4 CONFIRMED by fresh-
  verify; the three-eyed crow IS Bloodraven = brynden-rivers, adwd-bran-02:195 "A crow? Once, aye" +
  adwd-bran-03:19 "the name she gave me at her breast was Brynden"):
    RE-POINT  coldhands SERVES   three-eyed-crow -> brynden-rivers (preserve evidence adwd-bran-01:73)
    RE-POINT  coldhands SWORN_TO three-eyed-crow -> brynden-rivers (preserve wiki provenance)
    RETIRE    three-eyed-crow TEACHES bran-stark  (superseded by minted brynden-rivers TUTORS, BR1)
    RETIRE    three-eyed-crow HOLDS_TITLE lord    (brynden-rivers already holds it)
  -> leaves the `three-eyed-crow` species node islanded; flagged for a future cross-identity pass
     (do NOT SAME_AS species<->character).

Backup-guarded; reports before/after counts.
"""
import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-bran-finalize-2026-06-25.jsonl"

RUN_ID = "bran-enrichment-s146"
DROP_IDS = {"GD2", "GD4", "CF2"}
TIER1_IDS = {"BR2", "RV2"}
CONFIRM_IDS = {"GD1", "GD3", "GD5", "GD6", "PR3", "BR1", "BR2", "ME2", "HO1", "RV1", "RV2", "SB1"}

# pre-existing edges to RE-POINT: (source, type, old_target) -> new_target
REPOINT = {
    ("coldhands", "SERVES", "three-eyed-crow"): "brynden-rivers",
    ("coldhands", "SWORN_TO", "three-eyed-crow"): "brynden-rivers",
}
# pre-existing edges to RETIRE (source, type, target)
RETIRE = {
    ("three-eyed-crow", "TEACHES", "bran-stark"),
    ("three-eyed-crow", "HOLDS_TITLE", "lord"),
}


def main():
    lines = [ln for ln in EDGES.read_text(encoding="utf-8").splitlines() if ln.strip()]
    shutil.copy2(EDGES, BACKUP)
    print(f"Backup -> {BACKUP.relative_to(REPO)}  ({len(lines)} lines)")

    out = []
    dropped, retired, repointed, retargeted, tiered, stamped = [], [], [], 0, 0, 0
    for ln in lines:
        r = json.loads(ln)
        sig = (r.get("source_slug"), r.get("edge_type"), r.get("target_slug"))
        cid = r.get("candidate_id")
        is_run = r.get("run_id") == RUN_ID

        # --- pre-existing surgery ---
        if not is_run and sig in RETIRE:
            retired.append(sig)
            continue
        if not is_run and sig in REPOINT:
            r["target_slug"] = REPOINT[sig]
            r["retargeted_from"] = "three-eyed-crow"
            r["retargeted_by"] = RUN_ID
            r["asserted_relation"] = "slug-trap fix: the three-eyed crow IS Bloodraven (brynden-rivers); re-pointed off the species node (fresh-verify-confirmed-s146)"
            repointed.append((sig[0], sig[1]))
            out.append(json.dumps(r, ensure_ascii=False))
            continue

        # --- this dip's minted edges ---
        if is_run:
            if cid in DROP_IDS:
                dropped.append(cid)
                continue
            if cid == "GD5":
                r["target_slug"] = "sack-of-winterfell"
                r["asserted_relation"] = ("the 'Reek skinning your faces' green dream -> the danger to "
                                          "Bran/Rickon in the sack (re-targeted off robb-receives-false-news "
                                          "per fresh-verify; partly subverted — the burned boys are miller's sons)")
                retargeted += 1
            if cid in TIER1_IDS:
                r["confidence_tier"] = 1
                tiered += 1
            if cid in CONFIRM_IDS:
                r["verified_by"] = "fresh-verify-confirmed-s146"
                stamped += 1
        out.append(json.dumps(r, ensure_ascii=False))

    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Dropped (REJECT/COLLAPSE): {dropped}")
    print(f"Retired (pre-existing): {[' '.join(s) for s in retired]}")
    print(f"Re-pointed (pre-existing): {[' '.join(s) + ' -> brynden-rivers' for s in repointed]}")
    print(f"Re-targeted: GD5 (x{retargeted})   Tier->1: {tiered}   Stamped confirmed: {stamped}")
    print(f"edges.jsonl: {len(lines)} -> {len(out)} lines ({len(out) - len(lines):+d})")


if __name__ == "__main__":
    main()
