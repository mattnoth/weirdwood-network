#!/usr/bin/env python3
"""Mint the ESSOS E5 "Doran's pact reveal + Quentyn's death" arc.

ESSOS container decomposition (working/essos-decomposition.md) juncture E5 — closes
the S117 Dorne arc cross-book into Essos. Two NET-NEW beat nodes were minted as .md
files alongside this script (doran-reveals-fire-and-blood-pact, death-of-quentyn-martell).
This script wires the causal + role edges.

Built per the arc-mint machine. The causal types + the ONE structural question were
adjudicated by a fresh read-only research+verify subagent (2026-06-21,
working/session-results/2026-06-21-essos-e5-research.md) BEFORE minting, and every
evidence_ref line was re-pinned against the actual chapter file by the orchestrator
(0 drift found), so the causal edges are stamped verified at mint time.

STRUCTURAL VERDICT (subagent + decomposition anti-signal, CONFIRMED): TWO CLEAN
SEGMENTS, not one chain. The pact-reveal does NOT causally connect to the Quentyn-death
chain. Chronology forbids it: Quentyn's quest was already underway when Doran reveals
the pact to Arianne (Doran, past tense: "Your brother went ... on a long and perilous
voyage"). The reveal is an exposition beat (Arianne learning what was already in motion),
NOT the trigger of the quest. The deep upstream cause -- Doran's original pact-making /
sending of Quentyn -- is undated and unmodeled by design. The two segments are joined
through the shared Martell character nodes (doran-martell, quentyn-martell), not a forced
causal edge.

  Segment A (Dorne):  arianne-collapses-and-is-captured --CAUSES--> doran-reveals-fire-and-blood-pact
                      [doran-martell AGENT_IN, arianne-martell WITNESS_IN]
  Segment B (Meereen): quentyn-orders-the-attack --TRIGGERS--> death-of-quentyn-martell
                      [quentyn-martell VICTIM_IN, rhaegal AGENT_IN]

DRAGON ATTRIBUTION (verified close-read, adwd-the-dragontamer-01 lines 261-267): the
dragon that burns Quentyn is RHAEGAL (the green), striking from behind while Quentyn is
focused on whipping Viserion (the white). Frequently misattributed to Viserion in fan
discussion; the AGENT_IN edge is correctly on `rhaegal`.

ROOT: Segment A roots cross-book at the S117-built `arianne-collapses-and-is-captured`
(which walks upstream via arrest-of-the-sand-snakes -> Oberyn's death -> Sansa's hairnet).
Segment B roots locally at `quentyn-orders-the-attack` (its own undated upstream).

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-essos-e5-arc-2026-06-21.jsonl"

RUN_ID = "causal-arc-essos-e5-quentyn-20260621"
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
ARIANNE_CAPTURED = "arianne-collapses-and-is-captured"
REVEAL = "doran-reveals-fire-and-blood-pact"
QUENTYN_ORDERS = "quentyn-orders-the-attack"
QUENTYN_DEATH = "death-of-quentyn-martell"
DORAN = "doran-martell"
ARIANNE = "arianne-martell"
QUENTYN = "quentyn-martell"
RHAEGAL = "rhaegal"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified-or-None)
EDGES_SPEC = [
    # --- Segment A: Dorne reveal (causal + roles) ---
    (ARIANNE_CAPTURED, "CAUSES", REVEAL, 2, "affc", "affc-the-princess-in-the-tower-01", 293,
     "I dared not bring you any man you might accept. You were promised, Arianne.",
     "Doran withheld the pact for years (he could not risk Arianne knowing while he had to be seen seeking her a consort). Her imprisonment after the Queenmaker plot is what creates the private, controlled setting that forces -- and finally permits -- the reveal. The capture is the necessary precondition for the reveal scene => CAUSES Tier-2.",
     VERIFIED),
    (DORAN, "AGENT_IN", REVEAL, 1, "affc", "affc-the-princess-in-the-tower-01", 325,
     "Prince Doran pressed the onyx dragon into her palm with his swollen, gouty fingers, and whispered",
     "Doran is the disclosing agent -- he speaks the secret and presses the onyx-dragon token into Arianne's hand. Role edge => AGENT_IN Tier-1.",
     None),
    (ARIANNE, "WITNESS_IN", REVEAL, 1, "affc", "affc-the-princess-in-the-tower-01", 325,
     "Prince Doran pressed the onyx dragon into her palm with his swollen, gouty fingers, and whispered",
     "Arianne load-bearingly perceives the reveal: the chapter is her POV, she is the addressee, and she physically receives the onyx dragon into her palm and hears the whisper. Text-anchor gate passes => WITNESS_IN Tier-1.",
     None),
    # --- Segment B: Meereen death (causal + roles) ---
    (QUENTYN_ORDERS, "TRIGGERS", QUENTYN_DEATH, 2, "adwd", "adwd-the-dragontamer-01", 263,
     "And then a hot wind buffeted him and he heard the sound of leathern wings and the air was full of ash and cinders and a monstrous roar",
     "Quentyn's order to take the dragons sets off the fight; the chaos rouses the dragons and Rhaegal strikes. Immediate mechanistic chain (command -> fight -> dragon attack), not planning or enabling => TRIGGERS Tier-2.",
     VERIFIED),
    (QUENTYN, "VICTIM_IN", QUENTYN_DEATH, 1, "adwd", "adwd-the-dragontamer-01", 267,
     "When he raised his whip, he saw that the lash was burning. His hand as well. All of him, all of him was burning.",
     "Quentyn is the person who burns and dies. Role edge => VICTIM_IN Tier-1.",
     None),
    (RHAEGAL, "AGENT_IN", QUENTYN_DEATH, 1, "adwd", "adwd-the-dragontamer-01", 265,
     "Quentyn turned and threw his left arm across his face to shield his eyes from the furnace wind. Rhaegal, he reminded himself, the green one is Rhaegal.",
     "Rhaegal (the green dragon) is the agent who burns Quentyn from behind while Quentyn is focused on lashing Viserion. Dragons are modeled as autonomous violent agents in this graph. Role edge => AGENT_IN Tier-1. (NOT viserion -- common misattribution.)",
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

    n_causal = sum(1 for s in EDGES_SPEC if s[1] in ("CAUSES", "TRIGGERS", "ENABLES"))
    n_role = sum(1 for s in EDGES_SPEC if s[1] in ("AGENT_IN", "VICTIM_IN", "WITNESS_IN"))
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges ({n_causal} causal Tier-2 verified, {n_role} role Tier-1).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
