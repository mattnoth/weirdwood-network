#!/usr/bin/env python3
"""Mint the Sack of King's Landing causal arc (S106 causal-arc track).

Appends role + SUB_BEAT_OF + causal edges to graph/edges/edges.jsonl after
backing it up. Causal edges (Tier-2) carry verified_by='pending-s106-arc-verify'
until a fresh subagent confirms them against the local cache; role + SUB_BEAT_OF
edges (Tier-1, factual presence) are stamped directly.

Re-run safe: refuses to append if run_id already present in the file.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-sack-kl-arc-2026-06-19.jsonl"

RUN_ID = "causal-arc-sack-kl-20260619"
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

HUB = "sack-of-kings-landing"
KL = "kings-landing"

# (src, etype, tgt, tier, book, chapter, ref_line, quote, asserted)
ROWS = [
    # --- Beat 1: Pycelle opens the gates (event.deception) ---
    ("pycelle", "AGENT_IN", "pycelle-opens-the-gates-of-kings-landing", 1, "acok", "acok-tyrion-06", 291,
     "'twas I who bid Aerys open his gates . . .",
     "Pycelle counseled Aerys to open the gates to Tywin's host."),
    ("pycelle-opens-the-gates-of-kings-landing", "LOCATED_AT", KL, 1, "acok", "acok-tyrion-06", 291,
     "'twas I who bid Aerys open his gates . . .",
     "The betrayal took place at King's Landing."),
    # --- Beat 2: Aerys orders the city burned (event.incident) ---
    ("aerys-ii-targaryen", "COMMANDS_IN", "aerys-commands-the-city-burned", 1, "asos", "asos-jaime-05", 57,
     "The traitors want my city, I heard him tell Rossart, but I'll give them naught but ashes.",
     "Aerys ordered Rossart to ignite the wildfire and burn the city."),
    ("aerys-commands-the-city-burned", "LOCATED_AT", KL, 1, "asos", "asos-jaime-05", 57,
     "The traitors want my city, I heard him tell Rossart, but I'll give them naught but ashes.",
     "The order was given in King's Landing during the Sack."),
    # --- Beat 3: The Kingslaying (event.assassination) ---
    ("jaime-lannister", "AGENT_IN", "slaying-of-aerys-ii-the-kingslaying", 1, "asos", "asos-jaime-05", 63,
     "I slew him first. Then I slew Aerys, before he could find someone else to carry his message to the pyromancers.",
     "Jaime Lannister slew Aerys II."),
    ("aerys-ii-targaryen", "VICTIM_IN", "slaying-of-aerys-ii-the-kingslaying", 1, "asos", "asos-jaime-05", 63,
     "Then I slew Aerys, before he could find someone else to carry his message to the pyromancers.",
     "Aerys II was the victim of the kingslaying."),
    ("slaying-of-aerys-ii-the-kingslaying", "LOCATED_AT", KL, 1, "asos", "asos-jaime-05", 63,
     "Then I slew Aerys, before he could find someone else to carry his message to the pyromancers.",
     "The kingslaying occurred in the throne room at King's Landing."),
    # --- Beat 4: Murder of Elia and Rhaegar's children (event.assassination) ---
    ("gregor-clegane", "AGENT_IN", "murder-of-elia-martell-and-rhaegars-children", 1, "asos", "asos-tyrion-06", 191,
     "Because I did not tell him to spare her. . . . The rape . . . even you will not accuse me of giving that command.",
     "Gregor Clegane raped and killed Elia and smashed the infant Aegon."),
    ("amory-lorch", "AGENT_IN", "murder-of-elia-martell-and-rhaegars-children", 1, "asos", "asos-tyrion-06", 191,
     "Ser Amory was almost as bestial with Rhaenys. I asked him afterward why it had required half a hundred thrusts to kill a girl.",
     "Amory Lorch killed Princess Rhaenys."),
    ("tywin-lannister", "COMMANDS_IN", "murder-of-elia-martell-and-rhaegars-children", 1, "asos", "asos-tyrion-06", 187,
     "even he knew that Rhaegar's children had to die if his throne was ever to be secure. ... When I laid those bodies before the throne, no man could doubt that we had forsaken House Targaryen forever.",
     "Tywin ordered Rhaegar's children dead (but, by his own account, not the rape/brutality)."),
    ("elia-martell", "VICTIM_IN", "murder-of-elia-martell-and-rhaegars-children", 1, "asos", "asos-tyrion-06", 191,
     "Then why did the Mountain kill her? Because I did not tell him to spare her.",
     "Princess Elia Martell was murdered."),
    ("rhaenys-targaryen-daughter-of-rhaegar", "VICTIM_IN", "murder-of-elia-martell-and-rhaegars-children", 1, "asos", "asos-tyrion-06", 191,
     "Ser Amory was almost as bestial with Rhaenys.",
     "Princess Rhaenys was murdered."),
    ("aegon-targaryen-son-of-rhaegar", "VICTIM_IN", "murder-of-elia-martell-and-rhaegars-children", 1, "asos", "asos-tyrion-06", 187,
     "even he knew that Rhaegar's children had to die if his throne was ever to be secure.",
     "The infant Prince Aegon was murdered."),
    ("murder-of-elia-martell-and-rhaegars-children", "LOCATED_AT", KL, 1, "asos", "asos-tyrion-06", 191,
     "Because I did not tell him to spare her.",
     "The murders occurred in the Red Keep at King's Landing."),
    # --- SUB_BEAT_OF (beat-in-event containment) ---
    ("pycelle-opens-the-gates-of-kings-landing", "SUB_BEAT_OF", HUB, 1, "acok", "acok-tyrion-06", 291,
     "'twas I who bid Aerys open his gates . . .",
     "Pycelle opening the gates is an enabling beat of the Sack."),
    ("aerys-commands-the-city-burned", "SUB_BEAT_OF", HUB, 1, "asos", "asos-jaime-05", 57,
     "I'll give them naught but ashes.",
     "Aerys's burn-order is a beat within the Sack."),
    ("slaying-of-aerys-ii-the-kingslaying", "SUB_BEAT_OF", HUB, 1, "asos", "asos-jaime-05", 63,
     "Then I slew Aerys.",
     "The kingslaying is a beat within the Sack."),
    ("murder-of-elia-martell-and-rhaegars-children", "SUB_BEAT_OF", HUB, 1, "asos", "asos-tyrion-06", 187,
     "When I laid those bodies before the throne.",
     "The murder of Elia and the children is a beat within the Sack."),
]

# Causal edges (Tier-2, interpretive link) — verified_by pending until subagent CONFIRM.
CAUSAL = [
    ("pycelle-opens-the-gates-of-kings-landing", "CAUSES", HUB, 2, "acok", "acok-tyrion-06", 291,
     "'twas I who bid Aerys open his gates . . .",
     "Pycelle's persuading Aerys to open the gates let Tywin's host take the city — the mediated cause of the Sack (Tywin's decision to sack is captured as COMMANDS_IN)."),
    ("aerys-commands-the-city-burned", "TRIGGERS", "slaying-of-aerys-ii-the-kingslaying", 2, "asos", "asos-jaime-05", 63,
     "Then I slew Aerys, before he could find someone else to carry his message to the pyromancers.",
     "Aerys's order to fire the city was the immediate spark for Jaime slaying him to stop it."),
    ("murder-of-elia-martell-and-rhaegars-children", "MOTIVATES", "eddard-stark", 2, "agot", "agot-eddard-02", 71,
     "Ned had named that murder; Robert called it war. ... Eddard Stark had ridden out that very day in a cold rage.",
     "The murders of Rhaegar's children drove Ned's estrangement from Robert."),
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
    new_rows += [make_row(s, verified="pending-s106-arc-verify") for s in CAUSAL]

    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges "
          f"({len(ROWS)} role/sub-beat tier-1 + {len(CAUSAL)} causal tier-2).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines.")


if __name__ == "__main__":
    main()
