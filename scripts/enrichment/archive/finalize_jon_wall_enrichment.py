#!/usr/bin/env python3
"""Apply S145 Jon/Wall fresh-verify adjustments to edges.jsonl (independent Sonnet verdict:
9 CONFIRM / 2 ADJUST / 2 REJECT + 2 retirements confirmed).

  DROP   C2 (left-hand-lew SUSPECTED_OF stabbing) + C3 (alf-of-runnymudd SUSPECTED_OF stabbing)
         — text-anchor failure: faction SEATING next to Bowen != suspicion; only Wick+Bowen are
         named stabbers, the 3rd/4th knives are anonymous.
  ADJUST C4 (yarwyck CONSPIRES_WITH bowen)  T2 -> T3  (parallel behavior > pre-arranged plot)
  ADJUST ST1 (stall ENABLES pink-letter)    T2 -> T3  (depends on accepting the letter as truthful,
         disputed in-universe)
  REQUOTE G5 (melisandre MANIPULATES lord-of-bones): swap to the stronger line-87 anchor
         ("her ruby stirred at the closeness of its slave"); ref -> adwd-melisandre-01.md:87
  STAMP  verified_by = "fresh-verify-confirmed-s145" on every surviving verify=true edge
         (SH1 SH2 SH5 HH3 HH4 C1 C4 C5 G5 G6 ST1).
  RETIRE 2 pre-existing edges the dip supersedes:
         - pink-letter-delivered TRIGGERS jon-is-stabbed-repeatedly (run causal-arc-n4-...;
           its quote is the Shieldhall speech -> superseded by the-shieldhall-speech TRIGGERS)
         - mance-rayder VICTIM_IN mance-rayder-brought-to-execution (factually false: Rattleshirt
           burned, Mance lived -> replaced by lord-of-bones VICTIM_IN)

Backup-guarded; reports before/after counts.
"""
import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-jon-wall-finalize-2026-06-25.jsonl"

RUN_ID = "jon-wall-enrichment-s145"
DROP_IDS = {"C2", "C3"}
TIER3_IDS = {"C4", "ST1"}
CONFIRM_IDS = {"SH1", "SH2", "SH5", "HH3", "HH4", "C1", "C4", "C5", "G5", "G6", "ST1"}

# pre-existing edges to retire (source, type, target)
RETIRE = {
    ("pink-letter-delivered", "TRIGGERS", "jon-is-stabbed-repeatedly"),
    ("mance-rayder", "VICTIM_IN", "mance-rayder-brought-to-execution"),
}


def main():
    lines = [ln for ln in EDGES.read_text(encoding="utf-8").splitlines() if ln.strip()]
    shutil.copy2(EDGES, BACKUP)
    print(f"Backup -> {BACKUP.relative_to(REPO)}  ({len(lines)} lines)")

    out = []
    dropped, retired, tiered, stamped, requoted = [], [], 0, 0, 0
    for ln in lines:
        r = json.loads(ln)
        sig = (r.get("source_slug"), r.get("edge_type"), r.get("target_slug"))
        cid = r.get("candidate_id")

        if r.get("run_id") != RUN_ID and sig in RETIRE:
            retired.append(sig)
            continue
        if r.get("run_id") == RUN_ID and cid in DROP_IDS:
            dropped.append(cid)
            continue
        if r.get("run_id") == RUN_ID:
            if cid in TIER3_IDS:
                r["confidence_tier"] = 3
                tiered += 1
            if cid == "G5":
                r["evidence_quote"] = "her ruby stirred at the closeness of its slave"
                r["evidence_ref"] = "sources/chapters/adwd/adwd-melisandre-01.md:87"
                requoted += 1
            if cid in CONFIRM_IDS:
                r["verified_by"] = "fresh-verify-confirmed-s145"
                stamped += 1
        out.append(json.dumps(r, ensure_ascii=False))

    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Dropped (REJECT): {dropped}")
    print(f"Retired (pre-existing): {[' '.join(s) for s in retired]}")
    print(f"Tier->3: {tiered}   Re-quoted: {requoted}   Stamped confirmed: {stamped}")
    print(f"edges.jsonl: {len(lines)} -> {len(out)} lines ({len(out) - len(lines):+d})")


if __name__ == "__main__":
    main()
