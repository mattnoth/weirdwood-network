#!/usr/bin/env python3
"""Mint the AFFC "Brienne -> Lady Stoneheart" causal arc (S115 causal-arc track).

Major-arc backlog #15 (Stoneheart reveal) + #19 (Brienne's "death") + AFFC
smoke-test #3 fumble (working/session-results/2026-06-20-affc-smoke.md). The
entire AFFC causal layer was DARK before S114; this is the third AFFC arc and
the best cross-book auto-join: it roots at the already-built Red Wedding chain.

Cross-book hinge: `catelyn-is-killed` (ASOS Catelyn VII; SUB_BEAT_OF red-wedding,
0 causal edges before this) is the precise antecedent the Brotherhood reverses.
Rooting there (not at red-wedding) ties the resurrection to the specific manner
of Catelyn's murder, and the existing SUB_BEAT_OF auto-joins the full RW arc.

New beat-nodes (written as .node.md, not here):
  - catelyn-rises-as-lady-stoneheart      (event.incident; ASOS Epilogue + AFFC Brienne VIII)
  - brienne-brought-before-lady-stoneheart (event.capture; AFFC Brienne VIII)

Causal spine (chain-as-arc, NO umbrella parent; Tier-2, verified_by pending):
  catelyn-is-killed --CAUSES--> catelyn-rises-as-lady-stoneheart
  catelyn-rises-as-lady-stoneheart --CAUSES--> brienne-brought-before-lady-stoneheart

Role edges (Tier-1):
  beric-dondarrion --AGENT_IN--> catelyn-rises-as-lady-stoneheart   (performs the last kiss)
  thoros --AGENT_IN--> catelyn-rises-as-lady-stoneheart             (recovers body, declines kiss)
  brotherhood-without-banners --AGENT_IN--> catelyn-rises-as-lady-stoneheart
  catelyn-stark --VICTIM_IN--> catelyn-rises-as-lady-stoneheart     (corpse acted upon)
  brotherhood-without-banners --AGENT_IN--> brienne-brought-before-lady-stoneheart
  brienne-tarth --VICTIM_IN--> brienne-brought-before-lady-stoneheart
  catelyn-stark --COMMANDS_IN--> brienne-brought-before-lady-stoneheart  (Stoneheart's judgment)
  podrick-payne --VICTIM_IN--> brienne-brought-before-lady-stoneheart
  hyle-hunt --VICTIM_IN--> brienne-brought-before-lady-stoneheart

CAUSES vs MOTIVATES: both causal links target EVENTS, so MOTIVATES (actor target)
is type-invalid; CAUSES is correct (both mediated -- the Brotherhood's choice to
resurrect intervenes in edge 1; the Stoneheart-led vengeance campaign mediates
edge 2). The agency-collapse check passed: no hidden intermediate beat (the inn
skirmish is a sub-detail of the capture, not its own arc beat). A defensible
`catelyn-is-killed MOTIVATES catelyn-stark` was deliberately NOT minted -- odd to
motivate a character with her own death, and the vengeance is already carried by
the CAUSES spine + the COMMANDS_IN role edge.

TRAP avoided: `brienne-arrested` is the ASOS Harrenhal cell event (Jaime/Balon
Swann, asos-jaime-07), NOT this AFFC Stoneheart capture -- not wired.

HARD-STOP: arc terminates at brienne-brought-before-lady-stoneheart. The chapter
ends on an unresolved cliffhanger ("screamed a word") -- no downstream beat exists.

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-brienne-stoneheart-arc-2026-06-20.jsonl"

RUN_ID = "causal-arc-brienne-stoneheart-20260620"
PRODUCED_AT = "2026-06-20T00:00:00+00:00"
PENDING = "pending-s115-brienne-stoneheart-verify"
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
KILLED = "catelyn-is-killed"
RISES = "catelyn-rises-as-lady-stoneheart"
CAPTURE = "brienne-brought-before-lady-stoneheart"
BERIC = "beric-dondarrion"
THOROS = "thoros"
BWB = "brotherhood-without-banners"
CATELYN = "catelyn-stark"
BRIENNE = "brienne-tarth"
POD = "podrick-payne"
HYLE = "hyle-hunt"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified)
EDGES_SPEC = [
    # --- causal spine (Tier-2, pending verify) ---
    (KILLED, "CAUSES", RISES, 2, "affc", "affc-brienne-08", 311,
     "The Freys slashed her throat from ear to ear. When we found her by the river she was three days dead. Harwin begged me to give her the kiss of life, but it had been too long. I would not do it, so Lord Beric put his lips to hers instead, and the flame of life passed from him to her. And . . . she rose.",
     "Catelyn's murder at the Red Wedding is the precise antecedent the Brotherhood reverses; the manner of her death (slashed throat, three days drowned) produces the mute, vengeful Stoneheart. Mediated by the Brotherhood's choice to resurrect => CAUSES Tier-2. Cross-book hinge onto the built RW chain.",
     PENDING),
    (RISES, "CAUSES", CAPTURE, 2, "affc", "affc-brienne-08", 105,
     "Guest right don't mean so much as it used to. Not since m'lady come back from the wedding. Some o' them swinging down by the river figured they was guests too.",
     "The risen Stoneheart turns the Brotherhood into a hanging campaign against perceived Lannister allies; that campaign is why Brienne (carrying the Lannister-gilded Oathkeeper) is captured, condemned, and given the sword-or-noose. Mediated => CAUSES Tier-2.",
     PENDING),
    # --- role edges (Tier-1), beat 1: catelyn-rises-as-lady-stoneheart ---
    (BERIC, "AGENT_IN", RISES, 1, "affc", "affc-brienne-08", 311,
     "Lord Beric put his lips to hers instead, and the flame of life passed from him to her. And . . . she rose.",
     "Beric Dondarrion performs the last-kiss resurrection, giving his own life-spark. Role edge => AGENT_IN Tier-1.",
     None),
    (THOROS, "AGENT_IN", RISES, 1, "affc", "affc-brienne-08", 311,
     "Harwin begged me to give her the kiss of life, but it had been too long. I would not do it, so Lord Beric put his lips to hers instead.",
     "Thoros, the red priest, recovers the body and is the rite's officiant who declines the kiss and hands it to Beric. Core participant. Role edge => AGENT_IN Tier-1.",
     None),
    (BWB, "AGENT_IN", RISES, 1, "affc", "affc-brienne-08", 311,
     "When we found her by the river she was three days dead.",
     "The Brotherhood Without Banners recovers Catelyn's corpse and is the band Stoneheart then takes command of. Role edge => AGENT_IN Tier-1.",
     None),
    (CATELYN, "VICTIM_IN", RISES, 1, "asos", "asos-epilogue", 169,
     "No. No, I saw her die. She was dead for a day and night before they stripped her naked and threw her body in the river. Raymund opened her throat from ear to ear. She was dead.",
     "Catelyn is the subject acted upon -- her corpse is resurrected; she has no agency at the moment of rising. Role edge => VICTIM_IN Tier-1.",
     None),
    # --- role edges (Tier-1), beat 2: brienne-brought-before-lady-stoneheart ---
    (BWB, "AGENT_IN", CAPTURE, 1, "affc", "affc-brienne-08", 235,
     "There were four of them, and she was weak and wounded, naked beneath the woolen shift. She had to bend her neck to keep from hitting her head as they marched her through the twisting passage.",
     "The Brotherhood captures, binds, and marches Brienne before Stoneheart. Role edge => AGENT_IN Tier-1.",
     None),
    (BRIENNE, "VICTIM_IN", CAPTURE, 1, "affc", "affc-brienne-08", 327,
     "She says that you must choose. Take the sword and slay the Kingslayer, or be hanged for a betrayer. The sword or the noose, she says.",
     "Brienne is the captive condemned to the sword-or-noose choice. Role edge => VICTIM_IN Tier-1.",
     None),
    (CATELYN, "COMMANDS_IN", CAPTURE, 1, "affc", "affc-brienne-08", 331,
     "This time Brienne understood her words. There were only two. Hang them, she croaked.",
     "Lady Stoneheart (the catelyn-stark node) issues the judgment -- the sword-or-noose ultimatum and the hanging order. Role edge => COMMANDS_IN Tier-1.",
     None),
    (POD, "VICTIM_IN", CAPTURE, 1, "affc", "affc-brienne-08", 337,
     "Hyle Hunt and Podrick Payne were given elms.",
     "Podrick is captured alongside Brienne and condemned to hang. Role edge => VICTIM_IN Tier-1.",
     None),
    (HYLE, "VICTIM_IN", CAPTURE, 1, "affc", "affc-brienne-08", 337,
     "Hyle Hunt and Podrick Payne were given elms.",
     "Hyle Hunt is captured alongside Brienne and condemned to hang. Role edge => VICTIM_IN Tier-1.",
     None),
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

    n_causal = sum(1 for s in EDGES_SPEC if s[1] in ("CAUSES", "TRIGGERS", "MOTIVATES"))
    n_role = len(EDGES_SPEC) - n_causal
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges ({n_causal} causal Tier-2 pending-verify + {n_role} role Tier-1).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
