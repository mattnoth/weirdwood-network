#!/usr/bin/env python3
"""Mint the AEGON causal spine (S128) — all 4 junctures A1-A4.

Container `aegon` was entirely causally DARK (PART_OF + role scaffolding, 0 causal
edges). This wires the single causal river: conspiracy seed -> reveal -> crossing ->
landing -> (parallel) Stormlands siege + KL assassinations. Spec:
working/aegon-decomposition.md (S127 read-only dip). 2 nodes minted out-of-band
(golden-company-sails-for-westeros A2; aegon-revealed-to-the-golden-company A1);
8 A3 nodes container-retagged out-of-band; build-step 0 edge fixes already applied.

Junctures (one run_id each so fresh-verify can flip verified_by per-arc):
  A2 (Rank 1) — GC sails west -> landing (spine ignition). 1 CAUSES + 2 MOTIVATES.
  A4 (Rank 2) — landing MOTIVATES the Varys assassinations + 3 role edges (the node
                had 0 incoming AND 0 role edges). Cross-theater motive (epilogue:293)
                -> REQUIRES L2 fresh-verify. NO Kevan-regency event node exists
                (regency-of-aegon-iii / regent-wars are historical Dance nodes) -> the
                KL-endgame attach is via the character role edges only, as the dip allowed.
  A3 (Rank 3) — landing CAUSES siege-of-storms-end-300 + connington MOTIVATES it.
                NO CAUSES between the 6 sibling takings (simultaneous; PART_OF is correct
                + complete -- the NORTH-section-4 granularity-overclaim trap).
  A1 (Rank 4) — varys CONSPIRES_WITH illyrio (dyad, book-curator, symmetric); varys
                MOTIVATES the reveal; reveal TRIGGERS the crossing (joins A1->A2).

Slug discipline (dip-verified): VICTIM target is `pycelle` (NOT grand-maester-pycelle);
all AEGON edges target `aegon-targaryen-young-griff` (NOT the historical infant
`aegon-targaryen-son-of-rhaegar`); GC siege attaches to `siege-of-storms-end-300`
(NOT taking-of-storms-end, Stannis/WO5K).

Edge types: locked vocab only (CAUSES / TRIGGERS / MOTIVATES + roles AGENT_IN /
VICTIM_IN + relationship CONSPIRES_WITH). Causal/agency + the interpretive dyad carry
verified_by='pending-*-verify' until a fresh subagent confirms.
Re-run safe: aborts if any run_id is already present.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-aegon-spine-mint-2026-06-22.jsonl"

RUN_A2 = "causal-arc-a2-gc-sails-west-20260622"
RUN_A4 = "causal-arc-a4-varys-assassinations-20260622"
RUN_A3 = "causal-arc-a3-stormlands-siege-20260622"
RUN_A1 = "causal-arc-a1-conspiracy-reveal-20260622"
PRODUCED_AT = "2026-06-22T00:00:00+00:00"


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
A2 = [
    ("golden-company-sails-for-westeros", "CAUSES", "landing-of-the-golden-company", 2, "adwd", "adwd-the-lost-lord-01", 217,
     "If my aunt wants Meereen, she's welcome to it. I will claim the Iron Throne by myself, with your swords and your allegiance. Move fast and strike hard, and we can win some easy victories before the Lannisters even know that we have landed.",
     "Aegon's decision at the war council to sail west and invade Westeros is the proximate cause of the stormlands landing. The crossing to Cape Wrath follows directly from this vote; without it the Golden Company would have marched east to Daenerys. Prior decision -> the campaign-igniting event => CAUSES Tier-2.",
     "pending-a2-verify"),
    ("aegon-targaryen-young-griff", "MOTIVATES", "golden-company-sails-for-westeros", 2, "adwd", "adwd-the-lost-lord-01", 217,
     "If my aunt wants Meereen, she's welcome to it. I will claim the Iron Throne by myself, with your swords and your allegiance.",
     "Aegon himself drives the sail-west decision over Strickland's caution -- it is his choice to claim the throne by himself rather than wait on his aunt. The claimant's agency is the motive force of the crossing => MOTIVATES Tier-2.",
     "pending-a2-verify"),
    ("tyrion-lannister", "MOTIVATES", "golden-company-sails-for-westeros", 2, "adwd", "adwd-tyrion-06", 145,
     "Go to Westeros, though … ah, then you are a rebel, not a beggar. Bold, reckless, a true scion of House Targaryen, walking in the footsteps of Aegon the Conqueror. A dragon.",
     "Tyrion's goad aboard the Shy Maid -- challenging Aegon to go to Westeros and prove himself rather than beg Daenerys for her hand -- plants the sail-west idea the prince later acts on. Tyrion later realises the 'pretty princeling' may have 'swallowed the bait' (adwd-tyrion-07:257). Goad -> the decision => MOTIVATES Tier-2.",
     "pending-a2-verify"),
]

A4 = [
    ("landing-of-the-golden-company", "MOTIVATES", "assassinations-of-pycelle-and-kevan-lannister", 2, "adwd", "adwd-epilogue", 293,
     "Doubt, division, and mistrust will eat the very ground beneath your boy king, whilst Aegon raises his banner above Storm's End and the lords of the realm gather round him.",
     "Varys's own stated motive ties the killings directly to Aegon's landing: he murders Kevan -- who was successfully stabilising Tommen's regency (reconciling Highgarden + Casterly Rock, binding the Faith) -- precisely so the realm collapses into chaos that Aegon's invasion needs. The landing/Storm's-End campaign is the reason for the assassinations. Cross-theater motive (CONTESTED, cross-book) => MOTIVATES Tier-2, L2 fresh-verify required.",
     "pending-a4-verify"),
    ("varys", "AGENT_IN", "assassinations-of-pycelle-and-kevan-lannister", 1, "adwd", "adwd-epilogue", 277,
     "He stood in a pool of shadow by a bookcase, plump, pale-faced, round-shouldered, clutching a crossbow in soft powdered hands.",
     "Varys is the killer -- he holds the crossbow that shot Kevan and has already murdered Pycelle. Central acting participant => AGENT_IN Tier-1.",
     None),
    ("kevan-lannister", "VICTIM_IN", "assassinations-of-pycelle-and-kevan-lannister", 1, "adwd", "adwd-epilogue", 269,
     "A quarrel was sunk almost to the fletching in his chest.",
     "Kevan Lannister is shot through the chest with a crossbow quarrel by Varys and dies. Victim => VICTIM_IN Tier-1.",
     None),
    ("pycelle", "VICTIM_IN", "assassinations-of-pycelle-and-kevan-lannister", 1, "adwd", "adwd-epilogue", 289,
     "The Grand Maester befouled himself in dying, and the stink was so abominable that I thought I might choke.",
     "Grand Maester Pycelle is killed (bludgeoned by Varys's child-assassins) before Kevan; Varys remarks on his corpse. Victim => VICTIM_IN Tier-1. (Target slug is `pycelle`, not grand-maester-pycelle.)",
     None),
]

A3 = [
    ("landing-of-the-golden-company", "CAUSES", "siege-of-storms-end-300", 2, "adwd", "adwd-the-griffin-reborn-01", 173,
     "We did not cross half the world to wait. Our best chance is to strike hard and fast, before King's Landing knows who we are. I mean to take Storm's End. A nigh-impregnable stronghold, and Stannis Baratheon's last foothold in the south.",
     "The successful landing and the four-castles-in-four-days stormlands campaign are the precondition and springboard for the move on Storm's End; Connington commits to the siege off the momentum of the landing. Prior enabling campaign -> the siege => CAUSES Tier-2. (The 6 takings stay PART_OF the landing -- siblings, simultaneous; NO CAUSES between them.)",
     "pending-a3-verify"),
    ("jon-connington", "MOTIVATES", "siege-of-storms-end-300", 2, "adwd", "adwd-the-griffin-reborn-01", 173,
     "I mean to take Storm's End. A nigh-impregnable stronghold, and Stannis Baratheon's last foothold in the south. Once taken, it will give us a secure fastness to which we may retreat at need, and winning it will prove our strength.",
     "Connington's war-council decision drives the siege -- he overrides Strickland's caution and insists on taking Storm's End to prove the Golden Company's strength. Commander's agency => MOTIVATES Tier-2.",
     "pending-a3-verify"),
]

A1 = [
    ("varys", "MOTIVATES", "aegon-revealed-to-the-golden-company", 2, "adwd", "adwd-epilogue", 297,
     "Aegon has been shaped for rule since before he could walk.",
     "Varys (with Illyrio) orchestrated raising Aegon in secret and shaping him for the throne; the conspiracy's whole purpose is the eventual restoration the reveal makes active. The orchestrator's long plan motivates the unveiling => MOTIVATES Tier-2.",
     "pending-a1-verify"),
    ("aegon-revealed-to-the-golden-company", "TRIGGERS", "golden-company-sails-for-westeros", 2, "adwd", "adwd-the-lost-lord-01", 127,
     "My lords, I give you Aegon Targaryen, firstborn son of Rhaegar, Prince of Dragonstone, by Princess Elia of Dorne",
     "The unveiling of the living Targaryen prince to the Golden Company's war council is the specific spark that precipitates the same-scene vote to sail west and invade. Reveal -> the war-council decision => TRIGGERS Tier-2.",
     "pending-a1-verify"),
]

# A1 dyad — relationship edge (NOT causal). book-curator, symmetric. Built explicitly
# (not via make_row) so it carries evidence_kind=book-curator + symmetric=true.
DYAD = {
    "edge_type": "CONSPIRES_WITH",
    "source_slug": "varys",
    "target_slug": "illyrio-mopatis",
    "decision": "emit_edge",
    "candidate_kind": "book-curator-dyad",
    "evidence_kind": "book-curator",
    "typed_by": "curator-causal-arc",
    "schema_version": "curator-v1",
    "produced_at": PRODUCED_AT,
    "run_id": RUN_A1,
    "evidence_book": "agot",
    "evidence_chapter": "agot-arya-03",
    "evidence_ref": "sources/chapters/agot/agot-arya-03.md:93",
    "evidence_quote": "The princess is with child. The khal will not bestir himself until his son is born.",
    "confidence_tier": 2,
    "symmetric": True,
    "asserted_relation": "The AGOT tunnels conspiracy (Arya witnesses Varys + Illyrio beneath the Red Keep): they plot the Targaryen restoration -- keep Aegon hidden, await Daenerys's child, delay open war. The conspiracy seed of the whole AEGON container. Modeled as a symmetric dyad on the two character nodes, NOT a tunnel-meeting event node (D1 resolved dyad-only; Arya WITNESS_IN parked -- her seeing has no clean outgoing causal edge).",
    "verified_by": "pending-a1-verify",
}

ARCS = [(RUN_A2, A2), (RUN_A4, A4), (RUN_A3, A3), (RUN_A1, A1)]


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
    all_slugs = {DYAD["source_slug"], DYAD["target_slug"]}
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
    new_rows.append(DYAD)

    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    causal_types = ("CAUSES", "TRIGGERS", "ENABLES", "MOTIVATES")
    n_causal = sum(1 for _, specs in ARCS for s in specs if s[1] in causal_types)
    n_role = sum(1 for _, specs in ARCS for s in specs if s[1] in ("AGENT_IN", "VICTIM_IN", "COMMANDS_IN", "WITNESS_IN"))
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges: {n_causal} causal/agency + {n_role} role Tier-1 + 1 CONSPIRES_WITH dyad.")
    print(f"  A2={len(A2)}  A4={len(A4)}  A3={len(A3)}  A1={len(A1)}+dyad")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
