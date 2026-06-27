#!/usr/bin/env python3
"""Mint the B3 Ned's-downfall arc (S108 causal-arc track).

Dip-driven (arc-weighted re-dip, 2026-06-19): Q10 "what set Ned's execution in
motion / who is to blame?" returned NOTHING causal — execution-of-eddard-stark
had rich ROLE edges (Joffrey COMMANDS_IN, Ilyn Payne AGENT_IN, Ice WIELDED_IN)
but ZERO upstream causal chain. This builds the upstream arc.

The arrest cluster already existed densely (arrest-of-eddard-stark hub + 3
SUB_BEAT_OF children: cersei-orders-ned-s-arrest, gold-cloaks-betray-ned,
ned-orders-janos-slynt-to-arrest-cersei — all with role edges) but carried no
causal edges. Three new beats fill the gaps the dip exposed:
  - death-of-robert-baratheon (event.assassination — the boar hunt; missing
    entirely; the architecture's canonical event.assassination example)
  - ned-discovers-the-truth-of-joffrey-s-parentage (event.incident — the ROOT)
  - ned-confesses-to-treason (event.incident — forced false confession)

Causal spine (all Tier-2, chain-as-arc, NO umbrella parent):
  discovery        --MOTIVATES--> eddard-stark        (drives Ned's fatal moves)
  discovery        --MOTIVATES--> cersei-lannister    (drives Cersei to destroy Ned)
  death-of-robert  --CAUSES-->    arrest-of-eddard-stark   (removes Ned's shield)
  arrest           --CAUSES-->    execution-of-eddard-stark
  confession       --TRIGGERS-->  execution-of-eddard-stark (immediate public spark)

Agency-collapse handled on role edges, NOT collapsed arrows:
  - Robert's death: Lancel AGENT_IN (strongwine) + Cersei COMMANDS_IN (Tier-2).
  - Littlefinger's betrayal: petyr-baelish COMMANDS_IN gold-cloaks-betray-ned
    (Tier-2) is ADDITIVE — the beat previously credited only Cersei. The dyadic
    `petyr-baelish BETRAYS eddard-stark` ALREADY EXISTS (verified vs edges.jsonl)
    and is NOT re-minted.
  - Joffrey's choice to execute despite the mercy deal: already on the existing
    `joffrey-baratheon COMMANDS_IN execution-of-eddard-stark` role edge.

HARD-STOP: no causal edge into war-of-the-five-kings (the arrest's PART_OF
war-of-the-five-kings is pre-existing structural, untouched).

Canonical slugs verified vs edges.jsonl: robert-baratheon (58 AGOT in-saga
edges; NOT the robert-i-baratheon wiki/historical dup), petyr-baelish,
lancel-lannister, great-sept-of-baelor, cersei-lannister, eddard-stark.

Causal edges (Tier-2) carry verified_by='pending-s108-b3-verify' until a fresh
subagent confirms against the local cache. Role edges Tier-1 except the
interpretive ones (Lancel/Cersei on the death; Cersei on the confession;
Littlefinger COMMANDS_IN) which are Tier-2.

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-b3-ned-downfall-arc-2026-06-19.jsonl"

RUN_ID = "causal-arc-b3-ned-downfall-20260619"
PRODUCED_AT = "2026-06-19T00:00:00+00:00"
COMMON = {
    "decision": "emit_edge",
    "candidate_kind": "causal-curator-arc",
    "evidence_kind": "book-pass1",
    "typed_by": "curator-causal-arc",
    "schema_version": "pass1-derived-v1",
    "produced_at": PRODUCED_AT,
    "run_id": RUN_ID,
}

DEATH = "death-of-robert-baratheon"
DISCOVERY = "ned-discovers-the-truth-of-joffrey-s-parentage"
CONFESS = "ned-confesses-to-treason"
ARREST = "arrest-of-eddard-stark"
EXEC = "execution-of-eddard-stark"
BETRAYAL = "gold-cloaks-betray-ned"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted)
ROLE = [
    # death-of-robert-baratheon
    ("robert-baratheon", "VICTIM_IN", DEATH, 1, "agot", "agot-eddard-13", 35,
     '"A devil," the king husked. "My own fault. Too much wine, damn me to hell. Missed my thrust."',
     "Robert is the king gored by the boar — the victim of the death event."),
    ("lancel-lannister", "AGENT_IN", DEATH, 2, "agot", "agot-eddard-15", 111,
     "Cersei gave him the wineskins, and told him it was Robert's favorite vintage.",
     "Lancel kept the king's strongwine flowing on Cersei's instruction — the human instrument of the death; indirect agency => Tier-2."),
    ("cersei-lannister", "COMMANDS_IN", DEATH, 2, "agot", "agot-eddard-15", 111,
     "Cersei gave him the wineskins, and told him it was Robert's favorite vintage.",
     "Cersei engineered the death via the strongwine but did not personally act => COMMANDS_IN, interpretive Tier-2."),
    # ned-discovers-the-truth-of-joffrey-s-parentage
    ("eddard-stark", "AGENT_IN", DISCOVERY, 1, "agot", "agot-eddard-12", 129,
     '"All three are Jaime\'s," he said. It was not a question.',
     "Ned reads the lineage tome, works out the incest, and confronts Cersei — the actor of the discovery."),
    # ned-confesses-to-treason
    ("eddard-stark", "AGENT_IN", CONFESS, 1, "agot", "agot-arya-05", 149,
     '"I am Eddard Stark, Lord of Winterfell and Hand of the King ... and I come before you to confess my treason in the sight of gods and men."',
     "Ned speaks the forced public confession — the actor of the confession beat."),
    ("cersei-lannister", "COMMANDS_IN", CONFESS, 2, "agot", "agot-eddard-15", 131,
     "Cersei is no fool. She knows a tame wolf is of more use than a dead one.",
     "The confession-for-the-Wall deal is Cersei's design (brokered via Varys) — orderer who did not personally act => COMMANDS_IN Tier-2."),
    (CONFESS, "LOCATED_AT", "great-sept-of-baelor", 1, "agot", "agot-arya-05", 99,
     "The gold cloaks is carryin' him to the sept.",
     "The confession takes place on the steps of the Great Sept of Baelor."),
    (CONFESS, "SUB_BEAT_OF", EXEC, 3, "agot", "agot-arya-05", 149,
     '"I am Eddard Stark ... and I come before you to confess my treason in the sight of gods and men."',
     "The confession is a beat within the execution event-hub (same Baelor set-piece)."),
    # Littlefinger agency ADDED to the existing betrayal beat
    ("petyr-baelish", "COMMANDS_IN", BETRAYAL, 2, "agot", "agot-eddard-14", 125,
     "Littlefinger slid Ned's dagger from its sheath and shoved it up under his chin. His smile was apologetic. \"I did warn you not to trust me, you know.\"",
     "Littlefinger brokered the gold-cloak reversal (bribed Slynt) and personally sprang the trap — the hidden orchestrator of the betrayal; interpretive Tier-2. (BETRAYS dyad already exists.)"),
]

# Causal edges (Tier-2) — verified_by pending until subagent CONFIRM.
CAUSAL = [
    (DISCOVERY, "MOTIVATES", "eddard-stark", 2, "agot", "agot-eddard-12", 159,
     '"When the king returns from his hunt, I intend to lay the truth before him. You must be gone by then."',
     "The discovery drives Ned's fatal choices — to warn Cersei and move against Joffrey's claim. Event/condition -> actor => MOTIVATES."),
    (DISCOVERY, "MOTIVATES", "cersei-lannister", 2, "agot", "agot-eddard-12", 169,
     '"When you play the game of thrones, you win or you die. There is no middle ground."',
     "The discovery drives Cersei's decision to destroy Ned before he can act. Event/condition -> actor => MOTIVATES."),
    (DEATH, "CAUSES", ARREST, 2, "agot", "agot-eddard-14", 71,
     'Ned had expected Cersei to strike quickly; the summons came as no surprise. "The king is dead," he said, "but we shall go with you nonetheless."',
     "Robert's death removes Ned's royal protector and precipitates the throne-room showdown that ends in his arrest. Mediated (Ned's move + Littlefinger's betrayal sit between, captured on the arrest's sub-beats) => CAUSES Tier-2."),
    (ARREST, "CAUSES", EXEC, 2, "agot", "agot-arya-05", 161,
     'So long as I am your king, treason shall never go unpunished. Ser Ilyn, bring me his head!',
     "The arrest leads to imprisonment, the forced confession, and Joffrey's order. Mediated (Joffrey's choice sits between, on his COMMANDS_IN role edge) => CAUSES Tier-2."),
    (CONFESS, "TRIGGERS", EXEC, 2, "agot", "agot-arya-05", 161,
     'But they have the soft hearts of women. So long as I am your king, treason shall never go unpunished. Ser Ilyn, bring me his head!',
     "The public confession is the immediate set-piece that Joffrey turns into the execution order, breaking the mercy deal => TRIGGERS Tier-2."),
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

    new_rows = [make_row(s, verified=None) for s in ROLE]
    new_rows += [make_row(s, verified="pending-s108-b3-verify") for s in CAUSAL]

    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges "
          f"({len(ROLE)} role/structural + {len(CAUSAL)} causal tier-2).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines.")


if __name__ == "__main__":
    main()
