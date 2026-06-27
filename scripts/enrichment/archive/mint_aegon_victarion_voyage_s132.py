#!/usr/bin/env python3
"""Mint the AEGON Euron/Victarion downstream wire (S131) — low-value remainder #1.

The Kingsmoot->Euron AEGON spine is spine-complete (S116/S128), but the bridge node
`euron-commissions-victarion-to-fetch-daenerys` (minted S116) was DANGLING: 3 edges in,
0 out, explicitly flagged in its own body as "to be wired by a later Essos-container
pass." The whole Victarion ADWD voyage sat as a disconnected cluster of float-nodes
(captures, sacrifice, Moqorro near-execution, Kerwin killing) — each with role edges but
0 structural OUT edges. This pass wires that cluster.

PURE-SEQUENCE GUARD (the skeptic-advisor's constraint): Victarion's voyage is a single-POV
linear journey. The prize-captures are SEQUENTIAL STOPS, not causes of one another. So there
is exactly ONE interpretive edge — `euron-commissions ENABLES iron-fleet-departs` (the
commission authorizes the voyage; Victarion's agency executes it). Everything else is role
edges + SUB_BEAT_OF grouping under a new voyage hub. NO CAUSES between voyage beats.

TWOW red line: the fleet's ARRIVAL at Meereen's bay, and Victarion sounding Dragonbinder,
are unwritten (TWOW). The hub terminates with the fleet entering Meereenese home waters;
the Dragonbinder thread terminates at Moqorro's reading. `second-siege-of-meereen` is NOT
wired (Victarion's role in it is TWOW-sourced).

2 nodes minted out-of-band:
  - iron-fleet-departs-for-slavers-bay  (event.incident, the voyage hub)
  - moqorro-reads-dragonbinder-glyphs   (event.incident, wires the disconnected dragonbinder)

Groups (one run_id each so fresh-verify can flip verified_by on the interpretive edge):
  HUB   — euron-commissions ENABLES voyage (the ONE interpretive edge, L2 fresh-verify)
          + victarion AGENT_IN + iron-fleet AGENT_IN (role, Tier-1).
  BEATS — 9 SUB_BEAT_OF edges grouping the float cluster under the voyage hub (structural,
          Tier-1). Kerwin + crew-calls-for-Moqorro are from ADWD The Iron Suitor (ch 57,
          the voyage's first chapter); the captures + sacrifice + Dragonbinder-reading are
          from ADWD Victarion (ch 64, the second).
  REVEAL— victarion AGENT_IN + moqorro AGENT_IN + dragonbinder WIELDED_IN the reading
          (role/artifact, Tier-1). WIELDED_IN precedent: `ice WIELDED_IN execution-of-
          eddard-stark` — an artifact as the instrument/object of an event.

Edge types: locked vocab only (ENABLES + roles AGENT_IN / WIELDED_IN + structural SUB_BEAT_OF).
Quotes are clean (apostrophe-free) source substrings to dodge curly-quote citation mismatch.
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
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-aegon-victarion-voyage-2026-06-22.jsonl"

RUN_HUB = "aegon-victarion-voyage-hub-20260622"
RUN_BEATS = "aegon-victarion-voyage-subbeats-20260622"
RUN_REVEAL = "aegon-victarion-dragonbinder-reveal-20260622"
PRODUCED_AT = "2026-06-22T00:00:00+00:00"

HUB = "iron-fleet-departs-for-slavers-bay"
REVEAL = "moqorro-reads-dragonbinder-glyphs"


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
HUB_EDGES = [
    ("euron-commissions-victarion-to-fetch-daenerys", "ENABLES", HUB, 2, "affc", "affc-the-reaver-01", 286,
     "When Victarion opened his hand, his palm was red with blood.",
     "Euron's commission (the blood-oath charge to fetch Daenerys) authorizes and permits the voyage but does not directly cause it -- Victarion's own acceptance and agency are the executing force (he secretly means to take Daenerys for himself). Authorizing precondition -> the voyage => ENABLES Tier-2. This is the ONE interpretive edge of the pass; wires the dangling AFFC bridge downstream. Cross-arc -> L2 fresh-verify.",
     "pending-hub-verify"),
    ("victarion-greyjoy", "AGENT_IN", HUB, 1, "adwd", "adwd-the-iron-suitor-01", 81,
     "the only way to do this is to take the slavers unawares, as once I did at Lannisport.",
     "Victarion commands the voyage end to end -- he splits the fleet, sets the route, and directs the prize-taking. Central acting participant => AGENT_IN Tier-1.",
     None),
    ("iron-fleet", "AGENT_IN", HUB, 1, "adwd", "adwd-victarion-01", 83,
     "Victarion took the Iron Fleet out into the deeper waters, beyond the sight of land.",
     "The Iron Fleet is the instrument host of the voyage -- the body that crosses the world and takes the prizes. Acting collective => AGENT_IN Tier-1.",
     None),
]

BEAT_SUBJECTS = [
    # (source_float_slug, book, chapter, line, quote)
    ("iron-fleet-captures-ghiscari-dawn", "adwd", "adwd-victarion-01", 11,
     "The sea was black and the moon was silver as the Iron Fleet swept down on the prey."),
    ("iron-fleet-captures-myrish-cog-dove", "adwd", "adwd-victarion-01", 39,
     "The sea was blue and green and the sun blazing down from an empty blue sky when the Iron Fleet took its second prize, in the waters north and west of Astapor."),
    ("two-ghiscari-galleys-chased-and-captured", "adwd", "adwd-victarion-01", 51,
     "This time the prey proved to be a pair of galleys, long and sleek and fast."),
    ("slaver-galley-willing-maiden-captured", "adwd", "adwd-victarion-01", 85,
     "She was named the Willing Maiden."),
    ("slavers-killed-rowers-freed", "adwd", "adwd-victarion-01", 87,
     "Victarion put the slavers to the sword, then sent his men below to unchain the rowers."),
    ("seven-girls-sacrificed-on-burning-ketch", "adwd", "adwd-victarion-01", 93,
     "Then he had them put aboard the fishing ketch that they had captured, cut her loose, and had her set afire."),
    ("the-crew-calls-for-moqorro-s-death", "adwd", "adwd-the-iron-suitor-01", 151,
     "Cut his throat! Kill him before he calls his demons down on us!"),
    ("killing-of-maester-kerwin", "adwd", "adwd-the-iron-suitor-01", 175,
     "Cut his throat and throw him in the sea, and the winds will favor us all the way to Meereen."),
    (REVEAL, "adwd", "adwd-victarion-01", 99,
     "A twisted thing it was, six feet long from end to end, gleaming black and banded with red gold and dark Valyrian steel."),
]
BEAT_EDGES = [
    (src, "SUB_BEAT_OF", HUB, 1, book, chap, line, quote,
     "Episode of the Iron Fleet's ADWD voyage to Slaver's Bay; grouped under the voyage hub. Structural grouping (SUB_BEAT_OF Tier-1) -- NOT a causal link to its sibling beats (pure-sequence guard).",
     None)
    for (src, book, chap, line, quote) in BEAT_SUBJECTS
]

REVEAL_EDGES = [
    ("victarion-greyjoy", "AGENT_IN", REVEAL, 1, "adwd", "adwd-victarion-01", 99,
     "Victarion ran his hand along it.",
     "Victarion brings the hellhorn forth and presents it for reading -- the acting participant who initiates the scene => AGENT_IN Tier-1.",
     None),
    ("moqorro", "AGENT_IN", REVEAL, 1, "adwd", "adwd-victarion-01", 111,
     "Moqorro turned the hellhorn, examining the queer letters that crawled across a second of the golden bands.",
     "Moqorro reads and translates the Valyrian glyphs -- the performing actor of the revelation => AGENT_IN Tier-1.",
     None),
    ("dragonbinder", "WIELDED_IN", REVEAL, 1, "adwd", "adwd-victarion-01", 99,
     "A twisted thing it was, six feet long from end to end, gleaming black and banded with red gold and dark Valyrian steel.",
     "Dragonbinder (Euron's hellhorn) is the artifact at the center of the event -- the object brought forth, handled, and read. Artifact-as-instrument => WIELDED_IN Tier-1 (precedent: ice WIELDED_IN execution-of-eddard-stark). Wires the previously-disconnected horn into the graph.",
     None),
]

GROUPS = [(RUN_HUB, HUB_EDGES), (RUN_BEATS, BEAT_EDGES), (RUN_REVEAL, REVEAL_EDGES)]


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
    for _, specs in GROUPS:
        for s in specs:
            all_slugs.add(s[0])
            all_slugs.add(s[2])
    resolved, missing = precheck_slugs(all_slugs)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed (non-existent targets): {missing}")
    print(f"slug pre-check OK: {len(resolved)} resolved.")

    lines = EDGES.read_text(encoding="utf-8").splitlines()
    for run_id, _ in GROUPS:
        if any(run_id in ln for ln in lines):
            sys.exit(f"ABORT: run_id {run_id} already present -- already minted.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    new_rows = []
    for run_id, specs in GROUPS:
        new_rows.extend(make_row(s, run_id) for s in specs)

    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    n_causal = sum(1 for _, specs in GROUPS for s in specs if s[1] in ("CAUSES", "TRIGGERS", "ENABLES", "MOTIVATES"))
    n_role = sum(1 for _, specs in GROUPS for s in specs if s[1] in ("AGENT_IN", "VICTIM_IN", "COMMANDS_IN", "WITNESS_IN", "WIELDED_IN"))
    n_sub = sum(1 for _, specs in GROUPS for s in specs if s[1] == "SUB_BEAT_OF")
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges: {n_causal} ENABLES (interpretive) + {n_role} role Tier-1 + {n_sub} SUB_BEAT_OF.")
    print(f"  HUB={len(HUB_EDGES)}  BEATS={len(BEAT_EDGES)}  REVEAL={len(REVEAL_EDGES)}")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
