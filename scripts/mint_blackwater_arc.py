#!/usr/bin/env python3
"""Mint the Battle-of-the-Blackwater downstream causal arc (S111 causal-arc track).

Dip-driven (fresh arc-weighted dip, 2026-06-20, working/session-results/
2026-06-20-fresh-arc-dip.md, re-confirming the S109 ranking): Q12 "consequences
of the Battle of the Blackwater" was the #1 genuine fumble — `battle-of-the-
blackwater` had ZERO causal edges (only PART_OF war-of-the-five-kings, PRECEDES,
DIED_AT, SUB_BEAT_OF), despite being one of the most consequential battles in the
saga. This wires its three load-bearing downstream consequences.

Two new beat-nodes (written as .node.md, not here):
  - stannis-retreats-to-dragonstone  (event.incident; ASOS Davos II grounding)
  - tywin-named-savior-of-the-city   (event.incident; ACOK Sansa VIII grounding)

Reused existing node (verified vs graph/nodes/, NOT re-minted):
  - joffrey-sets-sansa-aside-and-agrees-to-wed-margaery (Plate-3 beat, 0 causal edges)

Causal spine (all Tier-2, chain-as-arc, NO umbrella parent — three parallel
downstream consequences of the battle hub):
  battle-of-the-blackwater --CAUSES--> joffrey-sets-sansa-aside-and-agrees-to-wed-margaery
  battle-of-the-blackwater --CAUSES--> stannis-retreats-to-dragonstone
  battle-of-the-blackwater --CAUSES--> tywin-named-savior-of-the-city

CAUSES (not TRIGGERS) for all three: the battle is a coarse hub and each
consequence is mediated (the Tyrell-Lannister marriage compact; Stannis's
constrained retreat decision; the crown's honors ceremony). Per the S104 rule
(coarse hub -> CAUSES; named specific spark -> TRIGGERS) and the agency-collapse
check (research subagent 2026-06-20 confirmed all three CLEAR for CAUSES; no
mandatory intermediate beat node — Joffrey/Stannis/court agency is theater or
constrained, not a hidden pivotal scene).

HARD-STOP: no causal edge into war-of-the-five-kings. The battle's PART_OF
war-of-the-five-kings is pre-existing structural, untouched. The full WO5K causal
mesh stays deferred (Tier C, strategy doc).

Causal edges (Tier-2) carry verified_by='pending-s111-blackwater-verify' until a
fresh subagent confirms against the local cache. (No role/structural edges this
batch — the consequences are event->event; participant roles on the new beats are
deferred to a later enrichment pass if a dip shows demand.)

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-blackwater-arc-2026-06-20.jsonl"

RUN_ID = "causal-arc-blackwater-20260620"
PRODUCED_AT = "2026-06-20T00:00:00+00:00"
COMMON = {
    "decision": "emit_edge",
    "candidate_kind": "causal-curator-arc",
    "evidence_kind": "book-pass1",
    "typed_by": "curator-causal-arc",
    "schema_version": "pass1-derived-v1",
    "produced_at": PRODUCED_AT,
    "run_id": RUN_ID,
}

BLACKWATER = "battle-of-the-blackwater"
SANSA_ASIDE = "joffrey-sets-sansa-aside-and-agrees-to-wed-margaery"
STANNIS_RETREAT = "stannis-retreats-to-dragonstone"
TYWIN_SAVIOR = "tywin-named-savior-of-the-city"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted)
CAUSAL = [
    (BLACKWATER, "CAUSES", SANSA_ASIDE, 2, "acok", "acok-sansa-08", 41,
     "Your Grace, in the judgment of your small council, it would be neither proper nor wise for you to wed the daughter of a man beheaded for treason ... set Sansa Stark aside. The Lady Margaery will make you a far more suitable queen.",
     "The Tyrell alliance that relieved King's Landing and won the battle was sealed by the marriage realignment: Joffrey sets Sansa aside and weds Margaery. Mediated by the pre-battle Tyrell-Lannister compact (Tywin/Littlefinger/Tyrell agency); Joffrey's assent is performative => CAUSES Tier-2."),
    (BLACKWATER, "CAUSES", STANNIS_RETREAT, 2, "asos", "asos-davos-02", 25,
     "Captain Khorane had told him of the end of Stannis's hopes, on the night the river burned. The Lannisters had taken him from the flank, and his fickle bannermen had abandoned him by the hundreds in the hour of his greatest need.",
     "Stannis's defeat at the Blackwater (fleet burned, flanked by Tywin's host, bannermen fled) forces his withdrawal to Dragonstone with a fraction of his army. His retreat decision is constrained to the single option => CAUSES Tier-2."),
    (BLACKWATER, "CAUSES", TYWIN_SAVIOR, 2, "acok", "acok-sansa-08", 19,
     "Joffrey had to step gingerly around it as he descended to embrace his grandfather and proclaim him Savior of the City.",
     "Tywin's relief host arriving at dusk was the decisive intervention that won the battle; the throne-room honors ceremony (Savior of the City + Hand restored) is its direct political consequence. The crown nominally confers but the outcome is battle-determined => CAUSES Tier-2."),
]


def make_row(spec, *, verified):
    src, etype, tgt, tier, book, chap, line, quote, asserted = spec
    row = {
        "edge_type": etype,
        "source_slug": src,
        "target_slug": tgt,
        **COMMON,
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
    lines = EDGES.read_text(encoding="utf-8").splitlines()
    if any(RUN_ID in ln for ln in lines):
        sys.exit(f"ABORT: run_id {RUN_ID} already present in {EDGES} — already minted.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    new_rows = [make_row(s, verified="pending-s111-blackwater-verify") for s in CAUSAL]

    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} causal tier-2 edges.")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines.")


if __name__ == "__main__":
    main()
