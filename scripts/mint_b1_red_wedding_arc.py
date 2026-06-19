#!/usr/bin/env python3
"""Mint the B1 Red Wedding upstream causal arc (S107 causal-arc track).

Dip-driven (arc-weighted Mode-3 dip, 2026-06-19): Q7 "what chain of events led
Robb to the Red Wedding?" failed because the red-wedding hub carried ZERO
upstream causal edges. This arc fills that gap.

Models TWO parallel consequence-chains, both dip-dark:
  (1) catelyn-releases-jaime-lannister --CAUSES--> karstark-murders-prisoners-at-riverrun
                                       --CAUSES--> execution-of-rickard-karstark
      (the cost of freeing Jaime: Robb loses the Karstarks)
  (2) robb-weds-jeyne-westerling --TRIGGERS--> red-wedding-conspiracy
                                 --CAUSES--> red-wedding   (terminus hub)
                                 --CAUSES--> robb-is-killed (sub-beat, for --causal-chain entry)
      (the broken Frey pact: betrayal at the Twins)

The two chains are PARALLEL causes of Robb's downfall, not sequential (the
research dedup + source check confirmed: the Karstark loss did NOT cause the Red
Wedding; the broken pact did). HARD-STOP at red-wedding — no edge onward to
war-of-the-five-kings (multi-attributed terminus).

red-wedding-conspiracy is an event.conspiracy beat wired CAUSALLY into the
red-wedding hub — NOT a SUB_BEAT_OF umbrella parent (consistent with the S106
chain-as-arc decision; event.conspiracy is a sanctioned type, 7 prior nodes).

Causal edges (Tier-2) carry verified_by='pending-s107-b1-verify' until a fresh
subagent confirms them. Role edges = factual presence = Tier-1, except
tywin COMMANDS_IN the conspiracy (Tier-2: sanction-by-protection, his own later
admission, interpretive).

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-b1-red-wedding-arc-2026-06-19.jsonl"

RUN_ID = "causal-arc-b1-red-wedding-20260619"
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

# new beat nodes
RELEASE = "catelyn-releases-jaime-lannister"
MURDERS = "karstark-murders-prisoners-at-riverrun"
EXEC = "execution-of-rickard-karstark"
WEDS = "robb-weds-jeyne-westerling"
CONSP = "red-wedding-conspiracy"
# reused existing nodes
RW = "red-wedding"
ROBB_KILLED = "robb-is-killed"

# Role edges (Tier-1 factual presence unless noted).
# (src, etype, tgt, tier, book, chapter, line, quote, asserted)
ROWS = [
    # --- N1: Catelyn releases Jaime (event.incident) ---
    ("catelyn-stark", "AGENT_IN", RELEASE, 1, "asos", "asos-catelyn-01", 21,
     "I understood what I was doing and knew it was treasonous . . . It was mine own act and mine alone",
     "Catelyn frees Jaime without Robb's consent and confesses it as her own act."),
    ("brienne-tarth", "AGENT_IN", RELEASE, 1, "asos", "asos-catelyn-01", 161,
     "Brienne will keep him safe. She swore it on her sword.",
     "Brienne is the escort tasked with delivering Jaime to King's Landing."),
    (RELEASE, "LOCATED_AT", "riverrun", 1, "asos", "asos-catelyn-01", 21,
     "we connived together to free Jaime Lannister",
     "The release takes place at Riverrun, where Jaime was held captive."),
    # --- N2: Karstark murders the prisoners (event.assassination) ---
    ("rickard-karstark", "AGENT_IN", MURDERS, 1, "asos", "asos-catelyn-03", 43,
     "The Kingslayer cut them down. These two were of his ilk. Only blood can pay for blood.",
     "Rickard Karstark murders the captives in vengeance for his sons."),
    ("tion-frey", "VICTIM_IN", MURDERS, 1, "asos", "asos-catelyn-03", 155,
     "They were asleep in their beds, naked and unarmed, in a cell where I put them.",
     "Tion Frey, a highborn captive, is murdered in his cell."),
    ("willem-lannister", "VICTIM_IN", MURDERS, 1, "asos", "asos-catelyn-03", 155,
     "Rickard Karstark killed more than a Frey and a Lannister.",
     "Willem Lannister, a highborn captive, is murdered in his cell."),
    (MURDERS, "LOCATED_AT", "riverrun", 1, "asos", "asos-catelyn-03", 155,
     "in a cell where I put them",
     "The murders occur in the dungeons of Riverrun."),
    # --- N3: Execution of Rickard Karstark (event.execution) ---
    ("robb-stark", "AGENT_IN", EXEC, 1, "asos", "asos-catelyn-03", 173,
     "In mine own name I condemn you. With mine own hand I take your life.",
     "Robb personally condemns and beheads Rickard Karstark (orderer and executor)."),
    ("rickard-karstark", "VICTIM_IN", EXEC, 1, "asos", "asos-catelyn-03", 173,
     "Rickard Karstark, Lord of Karhold . . . I judge you guilty of murder and high treason.",
     "Rickard Karstark is the condemned, executed for murder and treason."),
    (EXEC, "LOCATED_AT", "riverrun", 1, "asos", "asos-catelyn-03", 173,
     "Here in sight of gods and men",
     "The execution is held before the heart tree in the godswood at Riverrun."),
    # --- N4: Robb weds Jeyne Westerling (event.wedding) ---
    ("robb-stark", "AGENT_IN", WEDS, 1, "asos", "asos-catelyn-02", 143,
     "And you wed her the next day.",
     "Robb weds Jeyne Westerling, breaking his pact with House Frey."),
    ("jeyne-westerling", "AGENT_IN", WEDS, 1, "asos", "asos-catelyn-02", 143,
     "she . . . she comforted me, Mother.",
     "Jeyne Westerling weds Robb at the Crag."),
    (WEDS, "LOCATED_AT", "crag", 1, "asos", "asos-catelyn-02", 143,
     "The Crag was weakly garrisoned, so we took it by storm one night.",
     "The marriage takes place at the Crag, the Westerling seat."),
    # --- N5: Red Wedding conspiracy (event.conspiracy) ---
    ("walder-frey", "COMMANDS_IN", CONSP, 1, "asos", "asos-tyrion-06", 205,
     "I have no doubt he hatched this ugly chicken",
     "Walder Frey is the orderer/instigator of the conspiracy (Tywin attests)."),
    ("roose-bolton", "AGENT_IN", CONSP, 1, "asos", "asos-catelyn-07", 135,
     "Jaime Lannister sends his regards.",
     "Roose Bolton is the bannerman who turns traitor and executes the betrayal."),
    ("tywin-lannister", "COMMANDS_IN", CONSP, 2, "asos", "asos-tyrion-06", 205,
     "he would never have dared such a thing without a promise of protection",
     "Tywin sanctions the plot via a promise of protection (his own later admission; interpretive => Tier-2)."),
]

# Causal edges (Tier-2) — verified_by pending until subagent CONFIRM.
CAUSAL = [
    # Chain 1: freeing Jaime -> Karstark vengeance -> execution
    (RELEASE, "CAUSES", MURDERS, 2, "asos", "asos-catelyn-03", 57,
     "How can it be treason to kill Lannisters, when it is not treason to free them?",
     "Catelyn's release of Jaime is the cause Rickard Karstark names for the murders."),
    (MURDERS, "CAUSES", EXEC, 2, "asos", "asos-catelyn-03", 155,
     "Rickard Karstark killed more than a Frey and a Lannister. He killed my honor. I shall deal with him at dawn.",
     "The murders force Robb to condemn and execute Rickard (Robb's choice, modeled by his AGENT_IN role on the execution)."),
    # Chain 2: broken pact -> conspiracy -> Red Wedding / Robb's death
    (WEDS, "TRIGGERS", CONSP, 2, "asos", "asos-catelyn-02", 165,
     "Not only have you broken your oath, but you've slighted the honor of the Twins by choosing a bride from a lesser house.",
     "Robb's broken marriage pact is the immediate spark for Walder Frey's conspiracy (the conspirators' agency lives on the conspiracy node's role edges)."),
    (CONSP, "CAUSES", RW, 2, "asos", "asos-tyrion-06", 205,
     "I have no doubt he hatched this ugly chicken, but he would never have dared such a thing without a promise of protection.",
     "The Frey-Bolton-Lannister conspiracy is the covert engine that produces the Red Wedding massacre."),
    (CONSP, "CAUSES", ROBB_KILLED, 2, "asos", "asos-catelyn-07", 135,
     "Jaime Lannister sends his regards.",
     "The conspiracy specifically targets and kills Robb (edge added so --causal-chain robb-is-killed recovers the upstream chain)."),
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

    new_rows = [make_row(s, verified=None) for s in ROWS]
    new_rows += [make_row(s, verified="pending-s107-b1-verify") for s in CAUSAL]

    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges "
          f"({len(ROWS)} role + {len(CAUSAL)} causal tier-2).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines.")


if __name__ == "__main__":
    main()
