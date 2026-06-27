#!/usr/bin/env python3
"""Mint the Purple Wedding causal arc (S106 causal-arc track).

Appends role + SUB_BEAT_OF + causal edges to graph/edges/edges.jsonl after
backing it up. Causal edges (Tier-2) carry verified_by='pending-s106-pw-verify'
until a fresh subagent confirms them. Two role edges that rest on a later
confession rather than on-page narration are Tier-2 (petyr COMMANDS_IN hairnet;
cersei AGENT_IN accusation).

The whodunnit is NOT re-asserted: the Littlefinger/Olenna conspiracy already
lives on death-of-joffrey-baratheon; no tyrion KILLS/POISONS edge is created.

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-purple-wedding-arc-2026-06-19.jsonl"

RUN_ID = "causal-arc-purple-wedding-20260619"
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

HUB = "purple-wedding"
DEATH = "death-of-joffrey-baratheon"
RK = "red-keep"
HAIRNET = "sansa-receives-the-poisoned-hairnet"
ACCUSE = "tyrion-accused-of-poisoning-joffrey"
TRIAL = "trial-of-tyrion-lannister"
ESCAPE = "littlefinger-smuggles-sansa-out-of-kings-landing"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted)
ROWS = [
    # --- Beat N1: Sansa receives the poisoned hair net (event.deception) ---
    ("dontos-hollard", "AGENT_IN", HAIRNET, 1, "asos", "asos-sansa-02", 71,
     "wear the silver hair net and do as I told you, and afterward we make our escape",
     "Dontos delivers the hair net and insists Sansa wear it to the wedding feast."),
    ("sansa-stark", "VICTIM_IN", HAIRNET, 1, "asos", "asos-sansa-06", 145,
     "all Dontos had to do was lead you from the castle, and make certain you wore your silver hair net",
     "Sansa is the unwitting carrier of the strangler stone."),
    ("petyr-baelish", "COMMANDS_IN", HAIRNET, 2, "asos", "asos-sansa-06", 145,
     "Ser Dontos the Red was a skin of wine with legs. He could never have been trusted ... all Dontos had to do was lead you from the castle, and make certain you wore your silver hair net",
     "Littlefinger orchestrated the hair-net delivery (revealed in his later confession)."),
    (HAIRNET, "LOCATED_AT", RK, 1, "asos", "asos-sansa-02", 71,
     "wear the silver hair net and do as I told you",
     "The hair net was given to Sansa within the Red Keep."),
    # --- Beat N2: Tyrion accused / arrested (event.incident) ---
    ("cersei-lannister", "AGENT_IN", ACCUSE, 2, "asos", "asos-sansa-05", 157,
     "They think Tyrion poisoned Joffrey. Ser Dontos said they seized him.",
     "Cersei drives the accusation and seizure of Tyrion (she names him the poisoner)."),
    ("tyrion-lannister", "VICTIM_IN", ACCUSE, 1, "asos", "asos-sansa-05", 157,
     "They think Tyrion poisoned Joffrey. Ser Dontos said they seized him.",
     "Tyrion is accused and seized for Joffrey's murder (framed)."),
    (ACCUSE, "LOCATED_AT", RK, 1, "asos", "asos-sansa-05", 157,
     "They think Tyrion poisoned Joffrey. Ser Dontos said they seized him.",
     "The accusation and seizure occurred in the Red Keep."),
    # --- Beat N3: Trial of Tyrion (event.trial) ---
    ("tyrion-lannister", "VICTIM_IN", TRIAL, 1, "asos", "asos-tyrion-10", 65,
     "I did not do it. Yet now I wish I had. ... I am innocent, but I will get no justice here. ... I demand trial by battle.",
     "Tyrion is the defendant; framed, he demands trial by combat."),
    ("tywin-lannister", "AGENT_IN", TRIAL, 1, "asos", "asos-tyrion-10", 63,
     "Have you nothing to say in your defense?",
     "Tywin presides as chief judge at Tyrion's trial."),
    (TRIAL, "LOCATED_AT", RK, 1, "asos", "asos-tyrion-10", 65,
     "I am innocent, but I will get no justice here.",
     "The trial is held in the Red Keep."),
    # --- Beat N4: Littlefinger smuggles Sansa out (event.deception) ---
    ("petyr-baelish", "AGENT_IN", ESCAPE, 1, "asos", "asos-sansa-06", 145,
     "all Dontos had to do was lead you from the castle",
     "Littlefinger architects and executes Sansa's extraction (and has Dontos killed)."),
    ("dontos-hollard", "AGENT_IN", ESCAPE, 1, "asos", "asos-sansa-06", 145,
     "all Dontos had to do was lead you from the castle",
     "Dontos leads Sansa out of the castle, then is killed."),
    ("sansa-stark", "VICTIM_IN", ESCAPE, 1, "asos", "asos-sansa-06", 145,
     "all Dontos had to do was lead you from the castle",
     "Sansa is the manipulated, extracted party."),
    (ESCAPE, "LOCATED_AT", RK, 1, "asos", "asos-sansa-06", 145,
     "all Dontos had to do was lead you from the castle",
     "The escape originates at the Red Keep."),
    # --- SUB_BEAT_OF (beat-in-event containment); trial is NOT a sub-beat ---
    (HAIRNET, "SUB_BEAT_OF", HUB, 1, "asos", "asos-sansa-02", 71,
     "wear the silver hair net",
     "The hair-net delivery is a setup beat of the Purple Wedding arc."),
    (ACCUSE, "SUB_BEAT_OF", HUB, 1, "asos", "asos-sansa-05", 157,
     "They think Tyrion poisoned Joffrey.",
     "The accusation/seizure is a beat at the wedding feast."),
    (ESCAPE, "SUB_BEAT_OF", HUB, 1, "asos", "asos-sansa-06", 145,
     "all Dontos had to do was lead you from the castle",
     "Sansa's escape during the chaos is a beat of the Purple Wedding."),
]

# Causal edges (Tier-2) — verified_by pending until subagent CONFIRM.
CAUSAL = [
    (HAIRNET, "CAUSES", DEATH, 2, "asos", "asos-sansa-05", 45,
     "You poisoned him. You did. You took a stone from my hair . . .",
     "The hair net delivered the strangler stone that poisoned Joffrey (Olenna's hand and Littlefinger's design sit between, modeled as role edges on the death node)."),
    (DEATH, "TRIGGERS", ACCUSE, 2, "asos", "asos-sansa-05", 157,
     "They think Tyrion poisoned Joffrey. Ser Dontos said they seized him.",
     "Joffrey's death was the immediate spark for the accusation and seizure of Tyrion."),
    (ACCUSE, "CAUSES", TRIAL, 2, "asos", "asos-tyrion-09", 11,
     "if you are indeed innocent of Joffrey's death, you should have no difficulty proving it at trial",
     "The accusation led to Tyrion's trial."),
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
    new_rows += [make_row(s, verified="pending-s106-pw-verify") for s in CAUSAL]

    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges "
          f"({len(ROWS)} role/sub-beat + {len(CAUSAL)} causal tier-2).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines.")


if __name__ == "__main__":
    main()
