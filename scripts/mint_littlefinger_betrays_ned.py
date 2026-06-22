#!/usr/bin/env python3
"""Mint the `littlefinger-betrays-ned` beat + fix the broken BETRAYS dyad quote (S121).

Carried from the S120 continue prompt (verified S120 + fresh-critic-reviewed). There is NO
Littlefinger-betrays-Ned *event* node; his betrayal of Ned was captured only obliquely via
`gold-cloaks-betray-ned`. The node `littlefinger-betrays-ned.node.md` (event.incident) was minted
alongside this script; this wires the structural + role edges AND repairs the pre-existing
`petyr-baelish BETRAYS eddard-stark` dyad whose evidence_quote was BROKEN (it cited the
will/Protector passage, agot-eddard-14.md:63 -- not a betrayal at all).

GRANULARITY POLICY (S120, architecture.md): the betrayal *moment* (dagger under chin) is a
CONSTITUTIVE action WITHIN the arrest, not a prior cause of it => `SUB_BEAT_OF` ONLY, NO `CAUSES`.
(Mirror of the sequence-trap: don't under-draw causation, but don't fake convergence with
constitutive beats either.)

Edges:
  1. littlefinger-betrays-ned  SUB_BEAT_OF  arrest-of-eddard-stark   (Tier-3 structural)
  2. petyr-baelish             AGENT_IN     littlefinger-betrays-ned (Tier-1 role)
In-place fix:
  3. petyr-baelish BETRAYS eddard-stark -- repoint evidence_quote + evidence_ref from the broken
     will-passage (agot-eddard-14.md:63) to the dagger payoff (agot-eddard-14.md:125). NOT a new dyad.

Both quotes re-pinned against the chapter file by the orchestrator (0 drift):
  agot-eddard-14.md:125 = "As his men died around him, Littlefinger slid Ned's dagger..."

Re-run safe: refuses to append if RUN_ID already present; the BETRAYS fix is idempotent (only rewrites
the row while it still cites :63).
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-littlefinger-betrays-ned-2026-06-21.jsonl"
NODES = REPO / "graph" / "nodes"

RUN_ID = "curator-littlefinger-betrays-ned-20260621"
PRODUCED_AT = "2026-06-21T00:00:00+00:00"
VERIFIED = "orchestrator-source-repin-2026-06-21"

DAGGER_QUOTE = (
    "As his men died around him, Littlefinger slid Ned’s dagger from its sheath and shoved it up "
    "under his chin. His smile was apologetic. “I did warn you not to trust me, you know.”"
)
DAGGER_REF = "sources/chapters/agot/agot-eddard-14.md:125"

COMMON = {
    "decision": "emit_edge",
    "candidate_kind": "causal-curator-arc",
    "evidence_kind": "book-pass1",
    "typed_by": "curator-causal-arc",
    "schema_version": "pass1-derived-v1",
    "produced_at": PRODUCED_AT,
    "run_id": RUN_ID,
}

# (src, etype, tgt, tier, ref, quote, asserted, verified-or-None)
NEW_EDGES = [
    ("littlefinger-betrays-ned", "SUB_BEAT_OF", "arrest-of-eddard-stark", 3,
     DAGGER_REF, DAGGER_QUOTE,
     "Littlefinger's throne-room betrayal is a constitutive beat WITHIN Ned's arrest (it IS the arrest "
     "springing), not a prior cause of it => SUB_BEAT_OF only, no CAUSES (S120 granularity policy).",
     None),
    ("petyr-baelish", "AGENT_IN", "littlefinger-betrays-ned", 1,
     DAGGER_REF, DAGGER_QUOTE,
     "Petyr Baelish is the agent of the betrayal -- he personally draws Ned's dagger and holds it to "
     "Ned's throat. Role edge => AGENT_IN Tier-1.",
     VERIFIED),
]


def make_row(spec):
    src, etype, tgt, tier, ref, quote, asserted, verified = spec
    book = "agot"
    chap = "agot-eddard-14"
    row = {
        "edge_type": etype,
        "source_slug": src,
        "target_slug": tgt,
        **COMMON,
        "evidence_book": book,
        "evidence_chapter": chap,
        "evidence_ref": ref,
        "evidence_quote": quote,
        "confidence_tier": tier,
        "asserted_relation": asserted,
    }
    if verified is not None:
        row["verified_by"] = verified
    return row


def precheck_slugs(slugs):
    """Inline slug-existence check (mint_arc_lib not yet available). Node file must exist."""
    missing = []
    for s in slugs:
        if not list(NODES.glob(f"**/{s}.node.md")):
            missing.append(s)
    return missing


def main():
    lines = EDGES.read_text(encoding="utf-8").splitlines()
    if any(RUN_ID in ln for ln in lines):
        sys.exit(f"ABORT: run_id {RUN_ID} already present in {EDGES} -- already minted.")

    # Floor-check both new endpoints resolve to real node files.
    endpoints = {"littlefinger-betrays-ned", "arrest-of-eddard-stark", "petyr-baelish", "eddard-stark"}
    missing = precheck_slugs(endpoints)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed -- no node file for: {missing}")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    # --- in-place fix of the broken BETRAYS dyad ---
    fixed = 0
    out = []
    for ln in lines:
        try:
            row = json.loads(ln)
        except json.JSONDecodeError:
            out.append(ln)
            continue
        if (row.get("edge_type") == "BETRAYS"
                and row.get("source_slug") == "petyr-baelish"
                and row.get("target_slug") == "eddard-stark"
                and row.get("evidence_ref", "").endswith("agot-eddard-14.md:63")):
            row["evidence_quote"] = DAGGER_QUOTE
            row["evidence_ref"] = DAGGER_REF
            row["locate_status"] = "verbatim"
            row["quote_fixed_by"] = VERIFIED
            row["quote_fix_note"] = (
                "S121: prior evidence_quote cited the will/Protector passage (:63), not a betrayal; "
                "repointed to the dagger-under-chin payoff (:125)."
            )
            out.append(json.dumps(row, ensure_ascii=False))
            fixed += 1
        else:
            out.append(ln)

    new_rows = [make_row(s) for s in NEW_EDGES]
    out.extend(json.dumps(r, ensure_ascii=False) for r in new_rows)

    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")

    print(f"Backed up -> {BACKUP.name}")
    print(f"BETRAYS dyad quote fixed: {fixed} row(s) (expected 1).")
    print(f"Appended {len(new_rows)} edges (1 SUB_BEAT_OF Tier-3, 1 AGENT_IN Tier-1).")
    print(f"edges.jsonl now: {len(out)} lines (was {len(lines)}).")
    if fixed != 1:
        print("WARNING: expected exactly 1 BETRAYS fix -- inspect manually.", file=sys.stderr)


if __name__ == "__main__":
    main()
