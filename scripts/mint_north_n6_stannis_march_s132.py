#!/usr/bin/env python3
"""Mint NORTH N6 — Stannis marches south (S131, low-value remainder #2).

The NORTH spine is complete (S125/S126). This remainder wires Stannis's ADWD
southward campaign: the fight by Deepwood Motte -> the march on Winterfell -> the
army's snowbound stall at the crofters' village. Spec: working/north-decomposition.md
N6 (Rank 6), refined by the S131 research dip.

KEY DIP CORRECTIONS:
  - Upstream attach is `fight-by-deepwood-motte` (Stannis's ADWD reconquest), NOT
    `taking-of-deepwood-motte` (the ACOK ironborn seizure -- a different event that
    correctly stays in the ironborn-invasion arc).
  - Arnolf Karstark SUSPECTED_OF edge DROPPED: he is suspected of an intended
    betrayal that does not execute in published ADWD (TWOW-gated), not of causing the
    stall -- semantic mis-fit. His treachery is already recorded by the existing
    `arnolf-karstark BETRAYS stannis-baratheon` character edge.

RED LINES (held):
  - Battle of Ice / `battle-of-winterfell` (TWOW, unwritten) NOT minted, NOT wired.
  - `pink-letter-delivered` NOT wired upstream (the unwritten battle sits between the
    march and Ramsay's letter; its only edge stays the downstream TRIGGERS jon-is-stabbed).
  - The stall's proximate cause is the BLIZZARD (weather), so march->stall is ENABLES
    (precondition), NOT CAUSES. Both ENABLES edges are interpretive -> fresh-verify.

2 nodes minted out-of-band (stannis-march-on-winterfell, stannis-s-army-stalls-at-
crofters-village), both event.incident, both tagged `containers: [north]`.

Edge types: locked vocab only (ENABLES + roles AGENT_IN / VICTIM_IN). The 2 ENABLES
carry verified_by='pending-n6-verify' until a fresh subagent confirms ENABLES-not-CAUSES.
Re-run safe: aborts if the run_id is already present.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-north-n6-2026-06-22.jsonl"

RUN_N6 = "causal-arc-n6-stannis-march-20260622"
PRODUCED_AT = "2026-06-22T00:00:00+00:00"

MARCH = "stannis-march-on-winterfell"
STALL = "stannis-s-army-stalls-at-crofters-village"


def common(run_id):
    return {
        "decision": "emit_edge",
        "candidate_kind": "causal-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-causal-arc",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": run_id,
    }


# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified)
N6 = [
    ("fight-by-deepwood-motte", "ENABLES", MARCH, 2, "adwd", "adwd-the-kings-prize-01", 11,
     "host departed Deepwood Motte by the light of a golden dawn",
     "Stannis's victory at Deepwood Motte gives him the castle, the staging ground, and the northern mountain clans -- the precondition that makes the march on Winterfell possible. The host literally marches OUT of the captured Deepwood. Enabling victory -> the campaign => ENABLES Tier-2 (not CAUSES: Stannis's intent to take Winterfell is the efficient cause).",
     "pending-n6-verify"),
    (MARCH, "ENABLES", STALL, 2, "adwd", "adwd-the-kings-prize-01", 251,
     "no more than a few huts, a longhall, and a watchtower",
     "The march carries the host into the open wolfswood and halts it at the abandoned crofters' village, where the blizzard then pins it. The march is the precondition state that puts the army in the place it gets snowbound; the stall's PROXIMATE cause is the weather, not the march => ENABLES Tier-2 (deliberately NOT CAUSES -- the blizzard is the active cause).",
     "pending-n6-verify"),
    ("stannis-baratheon", "AGENT_IN", MARCH, 1, "adwd", "adwd-the-kings-prize-01", 11,
     "host departed Deepwood Motte by the light of a golden dawn",
     "Stannis leads the host on the march south from Deepwood toward Winterfell -- the commanding acting participant => AGENT_IN Tier-1.",
     None),
    ("asha-greyjoy", "VICTIM_IN", MARCH, 1, "adwd", "adwd-the-kings-prize-01", 19,
     "Asha Greyjoy rode in the baggage train, in a covered wayn with two huge iron-rimmed wheels, fettered at wrist and ankle",
     "Asha is Stannis's fettered captive, carried in the baggage train to be displayed in chains at Winterfell -- a passive prisoner, not a combatant => VICTIM_IN Tier-1.",
     None),
    ("stannis-baratheon", "VICTIM_IN", STALL, 1, "adwd", "adwd-the-kings-prize-01", 261,
     "sat snowbound and unmoving, walled in by ice and snow, starving",
     "Stannis is the commander whose entire host is trapped, snowbound and starving, by the blizzard -- the king is the subject the stall victimizes (his campaign frozen in place) => VICTIM_IN Tier-1.",
     None),
]

ARCS = [(RUN_N6, N6)]


def make_row(spec, run_id):
    src, etype, tgt, tier, book, chap, line, quote, asserted, verified = spec
    row = {
        "edge_type": etype,
        "source_slug": src,
        "target_slug": tgt,
        **common(run_id),
        "evidence_book": book,
        "evidence_chapter": chap,
        "evidence_ref": f"sources/chapters/{book}/{chap}.md:{line}",
        "evidence_quote": quote,
        "confidence_tier": tier,
        "asserted_relation": asserted,
    }
    if verified is not None:
        row["verified_by"] = verified
    return row


def main():
    all_slugs = set()
    for _, specs in ARCS:
        for s in specs:
            all_slugs.add(s[0])
            all_slugs.add(s[2])
    resolved, missing = precheck_slugs(all_slugs)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed (non-existent targets): {missing}")
    print(f"slug pre-check OK: {len(resolved)} resolved.")

    lines = EDGES.read_text(encoding="utf-8").splitlines()
    for run_id, _ in ARCS:
        if any(run_id in ln for ln in lines):
            sys.exit(f"ABORT: run_id {run_id} already present -- already minted.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    new_rows = []
    for run_id, specs in ARCS:
        new_rows.extend(make_row(s, run_id) for s in specs)

    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    n_causal = sum(1 for _, specs in ARCS for s in specs if s[1] in ("CAUSES", "TRIGGERS", "ENABLES", "MOTIVATES"))
    n_role = sum(1 for _, specs in ARCS for s in specs if s[1] in ("AGENT_IN", "VICTIM_IN", "COMMANDS_IN", "WITNESS_IN", "WIELDED_IN"))
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges: {n_causal} ENABLES (interpretive) + {n_role} role Tier-1.")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
