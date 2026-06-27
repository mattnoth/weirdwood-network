#!/usr/bin/env python3
"""Mint the ESSOS E2 "Slaver's Bay" causal arc (S119 essos-root track, juncture 2).

ESSOS container decomposition (working/essos-decomposition.md) juncture E2. The
whole Slaver's Bay campaign was causally DARK (all nodes existed via Plate-3/wiki
promotion with only PART_OF / role edges). 0 new beat-nodes -- pure causal wiring
of existing nodes. Built per the arc-mint machine; this run's edges were ADJUDICATED
by a fresh read-only research+verify subagent (2026-06-21) BEFORE minting, so they
are stamped verified at mint time (no pending pass).

Fresh-verify reshaped the decomposition's naive 3-CAUSES sketch:
  - fall-of-astapor -> siege-of-meereen: CAUSES downgraded to ENABLES, and ROUTED
    THROUGH Yunkai (army-enablement + campaign sequence, not direct cause). Canonical
    Yunkai node is `battle-near-yunkai` (`battle-of-yunkai` is a redirect stub).
  - siege -> sons-of-the-harpy-kill-twenty-nine: CAUSES type kept; the single
    incident node is an imprecise target for "the whole occupation's consequence"
    (a `sons-of-the-harpy-insurgency` CONDITION node would be cleaner -- FLAGGED as a
    future refinement in the worklog, NOT minted mid-build).
  - ADDED two strong edges the sketch missed: `siege-of-meereen MOTIVATES daenerys`
    (the stay-and-rule decision -- "the most important missing edge") and
    `sons-of-the-harpy-kill-twenty-nine TRIGGERS wedding-of-hizdahr...`.

Causal spine (chain-as-arc, NO umbrella; Tier-2; verified at mint):
  fall-of-astapor --ENABLES--> battle-near-yunkai --ENABLES--> siege-of-meereen
  siege-of-meereen --MOTIVATES--> daenerys-targaryen        (stay & rule, the pivot)
  siege-of-meereen --CAUSES--> sons-of-the-harpy-kill-twenty-nine   (occupation breeds insurgency; compressed target)
  sons-of-the-harpy-kill-twenty-nine --MOTIVATES--> daenerys-targaryen    (the marriage calculus)
  sons-of-the-harpy-kill-twenty-nine --TRIGGERS--> wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen

ENABLES vs CAUSES: Astapor/Yunkai -> Meereen is ENABLES (the bought army makes the
later siege possible; Yunkai is a real waypoint, not the cause). siege -> harpy is
CAUSES (occupation + abolition mechanically breed the insurgency). harpy -> wedding
is TRIGGERS (the killings are the specific spark for the marriage process Dany sets
in motion with Hizdahr's 90-day quest). MOTIVATES x2 carry Dany's two decisions.

ROOT: E2 is a STANDALONE military prime mover at `fall-of-astapor` (the dragon-birth
arc E1 ends at the hatching; the army-acquisition that opens Slaver's Bay is its own
root -- declared standalone, like Balon's death S116). No causal edge joins E1->E2
(the gap "dragons exist -> she sails to Slaver's Bay" is deliberately not over-rooted).

HARD-STOP: terminates at the Hizdahr wedding. The Daznak's-Pit -> Drogon-flees ->
Dothraki-sea endpoint is juncture E3 (3 mints), built later.

FLAGGED FOLLOW-UP (worklog): mint a `sons-of-the-harpy-insurgency` condition node and
demote `sons-of-the-harpy-kill-twenty-nine` to a TRIGGERS sub-beat of it -- a graph-
architecture call deferred out of this build. Also: `battle-of-yunkai` redirect-stub
dup of `battle-near-yunkai` (small-fixes).

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-essos-e2-arc-2026-06-21.jsonl"

RUN_ID = "causal-arc-essos-e2-slavers-bay-20260621"
PRODUCED_AT = "2026-06-21T00:00:00+00:00"
VERIFIED = "subagent-local-source-check-2026-06-21"
COMMON = {
    "decision": "emit_edge",
    "candidate_kind": "causal-curator-arc",
    "evidence_kind": "book-pass1",
    "typed_by": "curator-causal-arc",
    "schema_version": "pass1-derived-v1",
    "produced_at": PRODUCED_AT,
    "run_id": RUN_ID,
}

# slugs
ASTAPOR = "fall-of-astapor"
YUNKAI = "battle-near-yunkai"
MEEREEN = "siege-of-meereen"
HARPY = "sons-of-the-harpy-kill-twenty-nine"
WEDDING = "wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen"
DANY = "daenerys-targaryen"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified)
EDGES_SPEC = [
    (ASTAPOR, "ENABLES", YUNKAI, 2, "asos", "asos-daenerys-05", 139,
     "You stopped at Astapor to buy an army, not to start a war.",
     "The Unsullied army Dany wins at the fall of Astapor is the host that then takes Yunkai. Astapor produces the army (Jorah: she came to Astapor 'to buy an army'); the army makes the Yunkai victory possible -- condition, not mechanical cause. ENABLES Tier-2. Routed through Yunkai (a real campaign waypoint) rather than skipping to Meereen.",
     VERIFIED),
    (YUNKAI, "ENABLES", MEEREEN, 2, "asos", "asos-daenerys-05", 31,
     "Her host numbered more than eighty thousand after Yunkai, but fewer than a quarter of them were soldiers.",
     "The host swollen by the Yunkai campaign (eighty thousand 'after Yunkai') is what Dany brings to bear on Meereen; the Yunkai victory is the precondition for the Meereen siege, not its direct cause. ENABLES Tier-2.",
     VERIFIED),
    (MEEREEN, "MOTIVATES", DANY, 2, "asos", "asos-daenerys-06", 321,
     "But how can I rule seven kingdoms if I cannot rule a single city? ... I will not let this city go the way of Astapor. ... I will not march.",
     "Taking Meereen drives Dany's pivotal decision to STAY and rule rather than march west -- the choice that creates the entire occupation and everything downstream. Event -> actor decision => MOTIVATES Tier-2. (Fresh-verify: 'the most important missing edge' -- without it there is no causal account of why the occupation happens.)",
     VERIFIED),
    (MEEREEN, "CAUSES", HARPY, 2, "adwd", "adwd-daenerys-02", 31,
     "Every night the shadow war was waged anew beneath the stepped pyramids of Meereen. Every morn the sun rose upon fresh corpses, with harpies drawn in blood on the bricks beside them. ... Nine in one night, though ... That frightened her.",
     "Dany's conquest and occupation of Meereen and her abolition of slavery breed the Sons of the Harpy insurgency; this killing is its represented escalation. Occupation -> insurgency, mediated => CAUSES Tier-2. NOTE (fresh-verify): the target is a single incident node standing in for the ongoing insurgency -- defensible-but-imprecise; a `sons-of-the-harpy-insurgency` condition node is the cleaner future model (flagged, not minted).",
     VERIFIED),
    (HARPY, "MOTIVATES", DANY, 2, "adwd", "adwd-daenerys-04", 67,
     "She thought of Stalwart Shield, of Missandei's brother, of the woman Rylona Rhee ... No marriage would ever bring them back to life, but if a husband could help end the slaughter, then she owed it to her dead to marry.",
     "The Harpy killings drive Dany's decision to make the political marriage -- she explicitly reasons that she owes it to her murdered freedmen to wed if it will end the slaughter. Event -> actor decision => MOTIVATES Tier-2.",
     VERIFIED),
    (HARPY, "TRIGGERS", WEDDING, 2, "adwd", "adwd-daenerys-05", 313,
     "I need Hizdahr zo Loraq.",
     "The insurgency is the specific spark that sets the marriage in motion: Dany concludes she cannot fight an enemy within and without, and takes Hizdahr (whose 90-day quest to stop the killings is the bargain). Immediate spark for the marriage process => TRIGGERS Tier-2.",
     VERIFIED),
]


def make_row(spec):
    src, etype, tgt, tier, book, chap, line, quote, asserted, verified = spec
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

    new_rows = [make_row(s) for s in EDGES_SPEC]
    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} causal edges (all Tier-2, verified at mint).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
