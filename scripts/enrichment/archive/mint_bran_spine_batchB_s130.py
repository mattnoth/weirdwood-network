#!/usr/bin/env python3
"""Mint BRAN causal spine — Batch B (S130): BR4 + BR5 + BR6 + BR7 (the journey).

Spine 2 (the flight + journey north) was entirely dark. Batch B lights the whole
journey top-down from the container TERMINUS: party-split -> Black Gate (Sam) ->
Coldhands -> the cave (Bloodraven) -> Bran becomes a greenseer. Spec:
working/bran-decomposition.md (S129 dip) §5, confirmed + corrected by the Batch-B
research dip (line-checked quotes; key correction: Luwin does NOT counsel the split
-> BR3->BR4 is ENABLES not TRIGGERS; wight-attack folded into BR6).

5 node files minted out-of-band (party-split, black-gate, meets-coldhands, reaches-cave,
becomes-greenseer). All beat->beat links are ENABLES (continuous journey) EXCEPT the
single CAUSES BR6->BR7 (the transformation). NO CAUSES between sibling beats.

Slug discipline: greenseer/crow edges target `brynden-rivers` (the character), NOT the
`three-eyed-crow` species node. Coldhands is Bloodraven's instrument -> AGENT_IN the
escort, never a causal driver. Bran's warging of Hodor is preserved as AGENT_IN (agency).

Edge types: locked vocab only (CAUSES / ENABLES / MOTIVATES + roles AGENT_IN / VICTIM_IN).
Causal/agency edges carry verified_by='pending-*-verify' until a fresh subagent confirms.
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
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-bran-spine-batchB-2026-06-22.jsonl"

RUN_BR4 = "causal-arc-br4-party-split-20260622"
RUN_BR5 = "causal-arc-br5-blackgate-coldhands-20260622"
RUN_BR6 = "causal-arc-br6-cave-bloodraven-20260622"
RUN_BR7 = "causal-arc-br7-becomes-greenseer-20260622"
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
BR4 = [
    ("bran-and-rickon-survive-the-sack-in-the-crypts", "ENABLES", "bran-s-party-splits-from-rickon", 2, "acok", "acok-bran-07", 191,
     "I will take Rickon with me.",
     "Surviving the sack and emerging at the godswood is the precondition for the group to divide; there is no single named spark (Luwin does NOT counsel the split -- Osha and the Reeds decide it). Precondition => ENABLES Tier-2 (corrected from TRIGGERS at the research dip).",
     "pending-br4-verify"),
    ("jojen-reed", "MOTIVATES", "bran-s-party-splits-from-rickon", 2, "acok", "acok-bran-07", 207,
     "“Our road is north,” Jojen announced.",
     "Jojen's green-dream conviction drives Bran's contingent north, away from Rickon's route. The decision foregrounds Jojen's agency => MOTIVATES Tier-2.",
     "pending-br4-verify"),
    ("bran-stark", "AGENT_IN", "bran-s-party-splits-from-rickon", 1, "acok", "acok-bran-07", 191,
     "Hodor must stay with Bran, to be his legs,",
     "Bran is a principal of the split (his party goes north). AGENT_IN Tier-1.",
     None),
    ("jojen-reed", "AGENT_IN", "bran-s-party-splits-from-rickon", 1, "acok", "acok-bran-07", 207,
     "“Our road is north,” Jojen announced.",
     "Jojen declares the northward course. AGENT_IN Tier-1.",
     None),
    ("osha", "AGENT_IN", "bran-s-party-splits-from-rickon", 1, "acok", "acok-bran-07", 191,
     "I will take Rickon with me.",
     "Osha allocates the split, taking Rickon. AGENT_IN Tier-1.",
     None),
    ("meera-reed", "AGENT_IN", "bran-s-party-splits-from-rickon", 1, "acok", "acok-bran-07", 189,
     "“Take the boys.”",
     "Meera physically leads Rickon out and is an active mover in the split. AGENT_IN Tier-1.",
     None),
    ("rickon-stark", "VICTIM_IN", "bran-s-party-splits-from-rickon", 1, "acok", "acok-bran-07", 201,
     "Rickon sobbed and clung to Hodor’s leg",
     "Rickon is passively allocated to Osha's party (he resists, then is taken). VICTIM_IN Tier-1.",
     None),
]

BR5 = [
    ("bran-s-party-splits-from-rickon", "ENABLES", "bran-passes-the-black-gate", 2, "asos", "asos-bran-04", 209,
     "The Black Gate, he called it.",
     "The northward journey from the split brings the party to the Nightfort and its hidden gate. Continuous-journey precondition => ENABLES Tier-2.",
     "pending-br5-verify"),
    ("samwell-tarly", "ENABLES", "bran-passes-the-black-gate", 2, "asos", "asos-bran-04", 217,
     "Only a man of the Night’s Watch can open it, he said. A Sworn Brother who has said his words.",
     "Only a Sworn Brother of the Night's Watch who has said his words can open the Black Gate; Sam speaks the oath and it opens. Sam's presence is structurally required => ENABLES Tier-2.",
     "pending-br5-verify"),
    ("bran-stark", "AGENT_IN", "bran-passes-the-black-gate", 1, "asos", "asos-bran-04", 317,
     "and then it was Bran’s turn.",
     "Bran passes through the opened gate. AGENT_IN Tier-1.",
     None),
    ("samwell-tarly", "AGENT_IN", "bran-passes-the-black-gate", 1, "asos", "asos-bran-04", 315,
     "“I am the sword in the darkness,” Samwell Tarly said.",
     "Sam speaks the Night's Watch oath that opens the gate -- the acting agent of the passage. AGENT_IN Tier-1.",
     None),
    ("bran-passes-the-black-gate", "ENABLES", "bran-meets-coldhands", 2, "adwd", "adwd-bran-01", 211,
     "A friend. Dreamer, wizard, call him what you will. The last greenseer.",
     "Crossing beneath the Wall is the precondition for joining Coldhands' escort north. Continuous-journey precondition => ENABLES Tier-2.",
     "pending-br5-verify"),
    ("bran-stark", "AGENT_IN", "bran-meets-coldhands", 1, "adwd", "adwd-bran-01", 213,
     "“A monster,” Bran said.",
     "Bran is the POV principal who encounters and interrogates Coldhands. AGENT_IN Tier-1.",
     None),
    ("coldhands", "AGENT_IN", "bran-meets-coldhands", 1, "adwd", "adwd-bran-01", 211,
     "A friend. Dreamer, wizard, call him what you will. The last greenseer.",
     "Coldhands meets the party, names their destination, and becomes their escort. AGENT_IN Tier-1 (Bloodraven's instrument, not a causal driver).",
     None),
]

BR6 = [
    ("bran-meets-coldhands", "ENABLES", "bran-reaches-the-cave-of-the-three-eyed-crow", 2, "adwd", "adwd-bran-02", 197,
     "And now you are come to me at last, Brandon Stark, though the hour is late.",
     "Coldhands' escort north brings the party to the cave. Continuous-journey precondition => ENABLES Tier-2.",
     "pending-br6-verify"),
    ("bran-stark", "AGENT_IN", "bran-reaches-the-cave-of-the-three-eyed-crow", 1, "adwd", "adwd-bran-02", 111,
     "Bran ripped Hodor’s longsword from his belt.",
     "On the final approach Bran wargs Hodor to fight off the wights -- a deliberate act of human agency. AGENT_IN Tier-1 (agency preserved, not collapsed).",
     None),
    ("leaf", "AGENT_IN", "bran-reaches-the-cave-of-the-three-eyed-crow", 1, "adwd", "adwd-bran-02", 131,
     "It was her who saved us, though. The torch … fire kills them.",
     "Leaf and the children of the forest drive the wights back with fire and bring the party into the cave. AGENT_IN Tier-1.",
     None),
    ("meera-reed", "AGENT_IN", "bran-reaches-the-cave-of-the-three-eyed-crow", 1, "adwd", "adwd-bran-02", 113,
     "Meera Reed was there, driving her frog spear deep into the wight’s back.",
     "Meera fights off the wights on the approach. AGENT_IN Tier-1.",
     None),
    ("coldhands", "AGENT_IN", "bran-reaches-the-cave-of-the-three-eyed-crow", 1, "adwd", "adwd-bran-02", 95,
     "Bran saw Coldhands slash one across the face.",
     "Coldhands fights the wights on the approach but cannot enter the warded cave. AGENT_IN Tier-1.",
     None),
    ("brynden-rivers", "AGENT_IN", "bran-reaches-the-cave-of-the-three-eyed-crow", 1, "adwd", "adwd-bran-02", 205,
     "“You will never walk again, Bran,” the pale lips promised, “but you will fly.”",
     "Brynden Rivers receives Bran inside the cave and makes the 'you will fly' promise (the echo of the coma-crow). AGENT_IN Tier-1.",
     None),
]

BR7 = [
    ("bran-reaches-the-cave-of-the-three-eyed-crow", "CAUSES", "bran-becomes-a-greenseer", 2, "adwd", "adwd-bran-03", 157,
     "“Your blood makes you a greenseer,” said Lord Brynden. “This will help awaken your gifts and wed you to the trees.”",
     "Reaching Bloodraven leads directly to the weirwood paste + instruction that transform Bran into a greenseer -- a real, concrete consequence => CAUSES Tier-2 (the one CAUSES in the journey chain).",
     "pending-br7-verify"),
    ("bran-stark", "AGENT_IN", "bran-becomes-a-greenseer", 1, "adwd", "adwd-bran-03", 161,
     "He ate.",
     "Bran chooses to eat the paste -- his own act. AGENT_IN Tier-1.",
     None),
    ("leaf", "AGENT_IN", "bran-becomes-a-greenseer", 1, "adwd", "adwd-bran-03", 149,
     "“You must eat of this,” said Leaf. She handed Bran a wooden spoon.",
     "Leaf administers the weirwood paste. AGENT_IN Tier-1.",
     None),
    ("brynden-rivers", "AGENT_IN", "bran-becomes-a-greenseer", 1, "adwd", "adwd-bran-03", 167,
     "“Close your eyes,” said the three-eyed crow. “Slip your skin, as you do when you join with Summer. But this time, go into the roots instead.",
     "Brynden Rivers instructs Bran to go into the roots -- the greenseer instruction that completes the transformation. AGENT_IN Tier-1.",
     None),
]

ARCS = [(RUN_BR4, BR4), (RUN_BR5, BR5), (RUN_BR6, BR6), (RUN_BR7, BR7)]


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

    causal_types = ("CAUSES", "TRIGGERS", "ENABLES", "MOTIVATES")
    n_causal = sum(1 for _, specs in ARCS for s in specs if s[1] in causal_types)
    n_role = sum(1 for _, specs in ARCS for s in specs if s[1] in ("AGENT_IN", "VICTIM_IN", "COMMANDS_IN", "WITNESS_IN"))
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges: {n_causal} causal/agency + {n_role} role Tier-1.")
    print(f"  BR4={len(BR4)}  BR5={len(BR5)}  BR6={len(BR6)}  BR7={len(BR7)}")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
