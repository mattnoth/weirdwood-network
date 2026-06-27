#!/usr/bin/env python3
"""S121 wedding join-hub refactor (continue-prompt item 1.6).

The wedding of Hizdahr zo Loraq + Daenerys is a many-to-one CONVERGENCE, but the graph routed it off a
single over-strong edge:  sons-of-the-harpy-kill-twenty-nine TRIGGERS wedding-of-hizdahr...
TRIGGERS over-claims immediacy (weeks of deliberation + the Green Grace's brokering + an explicit
ninety-day bargain sit between the killings and the wedding) and implies a single spark.

Research (orchestrator close-read of adwd-daenerys-04..06, S121): the real proximate, citable driver of
the *Hizdahr* choice is the Green Grace Galazza Galare's counsel to take a Ghiscari king. Dany's internal
drivers (the killings, the siege) are already carried by two MOTIVATES daenerys edges. So:

  DROP : sons-of-the-harpy-kill-twenty-nine TRIGGERS wedding   (over-strong; killings' role = the
         existing MOTIVATES daenerys edge, untouched)
  MINT : galazza-counsels-the-ghiscari-marriage (event.incident node, minted alongside this script)
  ADD  : galazza-counsels... CAUSES   wedding-of-hizdahr...      (Tier-2; proximate external cause)
         galazza-counsels... MOTIVATES daenerys-targaryen        (Tier-2; counsel drives her decision)
         galazza-galare      AGENT_IN galazza-counsels...        (Tier-1; she is the counsellor)

Result: the wedding becomes an honest convergence hub — CAUSES-in from the Green Grace's counsel +
the two existing MOTIVATES-daenerys (Dany's drivers) + the downstream ENABLES drogon-returns. Quotes
re-pinned vs adwd-daenerys-04.md by the orchestrator (verified-at-mint / L1; single-book, clear call).

Re-run safe: refuses to append if RUN_ID present; the DROP is idempotent (only fires while the TRIGGERS
row still exists).
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-wedding-joinhub-2026-06-21.jsonl"

RUN_ID = "curator-wedding-joinhub-refactor-20260621"
PRODUCED_AT = "2026-06-21T00:00:00+00:00"
VERIFIED = "orchestrator-source-repin-2026-06-21"

WEDDING = "wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen"
COUNSEL = "galazza-counsels-the-ghiscari-marriage"
GALAZZA = "galazza-galare"
DANY = "daenerys-targaryen"
KILLINGS = "sons-of-the-harpy-kill-twenty-nine"

COMMON = {
    "decision": "emit_edge",
    "candidate_kind": "causal-curator-arc",
    "evidence_kind": "book-pass1",
    "typed_by": "curator-causal-arc",
    "schema_version": "pass1-derived-v1",
    "produced_at": PRODUCED_AT,
    "run_id": RUN_ID,
}

CH = "adwd-daenerys-04"
REF = lambda line: f"sources/chapters/adwd/{CH}.md:{line}"

# (src, etype, tgt, tier, line, quote, asserted, verified-or-None)
NEW_EDGES = [
    (COUNSEL, "CAUSES", WEDDING, 2, 83,
     "You know why you are here. The Green Grace seems to feel that if I take you for my husband, all my woes will vanish.",
     "The Green Grace's counsel to take a Ghiscari husband is the proximate cause of the Hizdahr marriage "
     "(it answers 'why Hizdahr'). Mediated through Dany's assent (CAUSES allows mediation) => CAUSES Tier-2. "
     "Replaces the dropped over-strong sons-of-harpy TRIGGERS edge as the wedding's causal-in.",
     VERIFIED),
    (COUNSEL, "MOTIVATES", DANY, 2, 171,
     "The Green Grace has the right of that. I need a king beside me, a king of old Ghiscari blood.",
     "Dany explicitly adopts the Green Grace's reasoning as her own decision driver (she repeatedly cites "
     "'the Green Grace says I must take a Ghiscari king'). Counsel -> actor decision => MOTIVATES Tier-2.",
     VERIFIED),
    (GALAZZA, "AGENT_IN", COUNSEL, 1, 279,
     "“The Green Grace says that I must take a Ghiscari king,” she said, flustered. “She urges me to wed the noble Hizdahr zo Loraq.”",
     "Galazza Galare is the counsellor who urges the Ghiscari marriage and brokers Hizdahr. Role edge => AGENT_IN Tier-1.",
     None),
]


def make_row(spec):
    src, etype, tgt, tier, line, quote, asserted, verified = spec
    row = {
        "edge_type": etype, "source_slug": src, "target_slug": tgt,
        **COMMON,
        "evidence_book": "adwd", "evidence_chapter": CH,
        "evidence_ref": REF(line), "evidence_quote": quote,
        "confidence_tier": tier, "asserted_relation": asserted,
    }
    if verified is not None:
        row["verified_by"] = verified
    return row


def main():
    lines = EDGES.read_text(encoding="utf-8").splitlines()
    if any(RUN_ID in ln for ln in lines):
        sys.exit(f"ABORT: run_id {RUN_ID} already present — already minted.")

    resolved, missing = precheck_slugs({WEDDING, COUNSEL, GALAZZA, DANY})
    if missing:
        sys.exit(f"ABORT: slug pre-check failed: {missing}")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    # --- DROP the over-strong TRIGGERS edge ---
    dropped = 0
    out = []
    for ln in lines:
        try:
            row = json.loads(ln)
        except json.JSONDecodeError:
            out.append(ln)
            continue
        if (row.get("edge_type") == "TRIGGERS"
                and row.get("source_slug") == KILLINGS
                and row.get("target_slug") == WEDDING):
            dropped += 1
            continue  # drop it
        out.append(ln)

    new_rows = [make_row(s) for s in NEW_EDGES]
    out.extend(json.dumps(r, ensure_ascii=False) for r in new_rows)
    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")

    print(f"Backed up -> {BACKUP.name}")
    print(f"DROPPED over-strong TRIGGERS: {dropped} row(s) (expected 1).")
    print(f"Appended {len(new_rows)} edges (1 CAUSES + 1 MOTIVATES Tier-2, 1 AGENT_IN Tier-1).")
    print(f"edges.jsonl now: {len(out)} lines (was {len(lines)}).")
    if dropped != 1:
        print("WARNING: expected exactly 1 TRIGGERS drop — inspect manually.", file=sys.stderr)


if __name__ == "__main__":
    main()
