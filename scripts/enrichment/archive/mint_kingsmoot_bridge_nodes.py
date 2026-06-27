#!/usr/bin/env python3
"""S116 — mint the two Kingsmoot 'forward' nodes IN PLACE (not deferred).

Matt's call: deferral-by-doc is fragile ("are we gonna remember this?"). On
inspection neither node is actually forward-DANGLING — both have a clean AFFC/ADWD
upstream (the kingsmoot) in the LOCAL cache, with only their downstream dark (normal
for a terminal node). Pre-placing them now lets the future Essos-container arc find
them already wired (cross-book auto-join, S112) instead of relying on a reminder.

New beat-nodes (written as .node.md):
  - euron-weds-asha-to-erik-ironmaker-in-absentia   (event.incident; ADWD The Wayward Bride)
  - euron-commissions-victarion-to-fetch-daenerys    (event.incident; AFFC The Reaver I — Essos-bridge seed)

Edges:
  kingsmoot-on-old-wyk --CAUSES--> euron-weds-asha-to-erik-ironmaker-in-absentia   (Tier-2, pending)
  euron-greyjoy --AGENT_IN--> euron-weds-asha-...                                   (Tier-1)
  asha-greyjoy --VICTIM_IN--> euron-weds-asha-...                                   (Tier-1)
  erik-ironmaker --AGENT_IN--> euron-weds-asha-...                                  (Tier-2, proxy groom)
  kingsmoot-on-old-wyk --CAUSES--> euron-commissions-victarion-to-fetch-daenerys    (Tier-2, pending)
  euron-greyjoy --COMMANDS_IN--> euron-commissions-victarion-...                    (Tier-1)
  victarion-greyjoy --AGENT_IN--> euron-commissions-victarion-...                   (Tier-1)

Re-run safe.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-kingsmoot-bridge-nodes-2026-06-20.jsonl"

RUN_ID = "causal-arc-kingsmoot-bridge-20260620"
PENDING = "pending-s116-kingsmoot-bridge-verify"
COMMON = {
    "decision": "emit_edge",
    "candidate_kind": "causal-curator-arc",
    "evidence_kind": "book-pass1",
    "typed_by": "curator-causal-arc",
    "schema_version": "pass1-derived-v1",
    "produced_at": "2026-06-20T00:00:00+00:00",
    "run_id": RUN_ID,
}

KINGSMOOT = "kingsmoot-on-old-wyk"
WEDS = "euron-weds-asha-to-erik-ironmaker-in-absentia"
COMMISSION = "euron-commissions-victarion-to-fetch-daenerys"
EURON = "euron-greyjoy"
ASHA = "asha-greyjoy"
ERIK = "erik-ironmaker"
VICTARION = "victarion-greyjoy"

EDGES_SPEC = [
    (KINGSMOOT, "CAUSES", WEDS, 2, "adwd", "adwd-the-wayward-bride-01", 123,
     "With one stroke, Euron had turned a rival into a supporter, secured the isles in his absence, and removed Asha as a threat.",
     "Asha's loss at the kingsmoot makes her a rival to be neutralized; Euron's response is to wed her by proxy to a loyalist and bind the isles. Mediated by Euron's political calculus => CAUSES Tier-2.",
     PENDING),
    (EURON, "AGENT_IN", WEDS, 1, "adwd", "adwd-the-wayward-bride-01", 121,
     "He had married her to Erik Ironmaker and named the Anvil-Breaker to rule the Iron Islands whilst he was chasing dragons.",
     "Euron arranges and orders the in-absentia marriage. Role edge => AGENT_IN Tier-1.",
     None),
    (ASHA, "VICTIM_IN", WEDS, 1, "adwd", "adwd-the-wayward-bride-01", 123,
     "Tris Botley said that the Crow's Eye had used a seal to stand in for her at her wedding.",
     "Asha is married against her will and in her absence (a seal stands in for her). Role edge => VICTIM_IN Tier-1.",
     None),
    (ERIK, "AGENT_IN", WEDS, 2, "adwd", "adwd-the-wayward-bride-01", 121,
     "\"My wayward niece needs taming,\" the Crow's Eye was reported to have said, \"and I know the man to tame her.\"",
     "Erik Ironmaker is the proxy groom and is named to rule the isles; his own agency is minimal (Euron arranged it). Role edge => AGENT_IN Tier-2.",
     None),
    (KINGSMOOT, "CAUSES", COMMISSION, 2, "affc", "affc-the-reaver-01", 281,
     "\"The choice is yours, brother. Live a thrall or die a king. Do you dare to fly? Unless you take the leap, you'll never know.\"",
     "Euron's victory at the kingsmoot installs him as king with a promised dragon-conquest of Westeros; as king he dispatches Victarion to fetch Daenerys and her dragons to complete that plan. Mediated by Euron's conquest design => CAUSES Tier-2.",
     PENDING),
    (EURON, "COMMANDS_IN", COMMISSION, 1, "affc", "affc-the-reaver-01", 281,
     "\"The choice is yours, brother. Live a thrall or die a king. Do you dare to fly?\"",
     "Euron orders the mission (the orderer who does not personally execute it). Role edge => COMMANDS_IN Tier-1.",
     None),
    (VICTARION, "AGENT_IN", COMMISSION, 1, "affc", "affc-the-reaver-01", 286,
     "\"I'll go to Slaver's Bay, aye. I'll find this dragon woman, and I'll bring her back.\"",
     "Victarion accepts and will execute the charge (secretly intending to keep Daenerys for himself). Role edge => AGENT_IN Tier-1.",
     None),
]


def make_row(spec):
    src, etype, tgt, tier, book, chap, line, quote, asserted, verified = spec
    row = {
        "edge_type": etype, "source_slug": src, "target_slug": tgt, **COMMON,
        "evidence_book": book, "evidence_chapter": chap,
        "evidence_ref": f"sources/chapters/{book}/{chap}.md:{line}",
        "evidence_quote": quote, "confidence_tier": tier, "asserted_relation": asserted,
    }
    if verified is not None:
        row["verified_by"] = verified
    return row


def main():
    lines = EDGES.read_text(encoding="utf-8").splitlines()
    if any(RUN_ID in ln for ln in lines):
        sys.exit(f"ABORT: run_id {RUN_ID} already present — already minted.")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)
    new_rows = [make_row(s) for s in EDGES_SPEC]
    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    n_causal = sum(1 for s in EDGES_SPEC if s[1] in ("CAUSES", "TRIGGERS", "MOTIVATES"))
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges ({n_causal} causal Tier-2 pending + {len(EDGES_SPEC)-n_causal} role).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
