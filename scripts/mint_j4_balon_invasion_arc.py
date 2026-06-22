#!/usr/bin/env python3
"""Mint the J4 "Balon's invasion -> Capture of Winterfell" arc (WO5K-remainder track, S123).

WO5K decomposition J4 (working/wo5k-decomposition.md, Rank 5). `capture-of-winterfell`
had ZERO causal UPSTREAM; the whole Greyjoy invasion thread feeding it was DARK. This
extends the B2 (greyjoy-ward) terminus through Balon's declaration + the invasion to the
capture.

NORTH SEAM: `capture-of-winterfell` and `sack-of-winterfell` are ALREADY dual-tagged
[wo5k, north] (S122). This builds UNDER wo5k and draws edges INTO capture-of-winterfell;
it does NOT re-tag north. The two new mints are wo5k-only.

TWO-LEVEL AGENCY (modeled, not collapsed):
  (1) Balon DECIDES to invade rather than ally -> `balon-declares-himself-king MOTIVATES balon-greyjoy`.
  (2) Theon DECIDES, against his Stony-Shore orders, to take Winterfell ->
      `balon-declares-himself-king MOTIVATES theon-greyjoy` (his drive to prove himself) +
      `theon-greyjoy AGENT_IN capture-of-winterfell`, with the Stony-Shore raid as ENABLES cover.

POLICY NOTE (S120 granularity): the dip proposed a 3rd mint `theon-seizes-winterfell-against-
orders` TRIGGERS capture-of-winterfell. DROPPED: Theon's seizing-against-orders IS the
capture (a constitutive action within it), not a chronologically-prior prerequisite -- minting
it to TRIGGER the capture would be the "constitutive beat promoted to cause" anti-pattern. The
defiance is instead modeled via MOTIVATES->theon + theon AGENT_IN capture + the raid-as-cover
ENABLES edge (asserted_relation records the against-orders nature). 2 mints, not 3.

New beat-nodes (written as .node.md, not here):
  - balon-declares-himself-king        (event.ceremony; ACOK Theon I)
  - ironborn-invasion-of-the-north     (event.incident; ACOK Theon II)

Edges (vocab-locked CAUSES/TRIGGERS/ENABLES/MOTIVATES + roles):
  theon-greyjoy-taken-as-ward   --ENABLES-->   balon-declares-himself-king        (T2, weakest -- verify)
  balon-declares-himself-king   --CAUSES-->    ironborn-invasion-of-the-north     (T2)
  balon-declares-himself-king   --MOTIVATES--> balon-greyjoy                      (T2, agency L1)
  balon-declares-himself-king   --MOTIVATES--> theon-greyjoy                      (T2, agency L2)
  ironborn-invasion-of-the-north --CAUSES-->   fall-of-moat-cailin                (T2)
  ironborn-invasion-of-the-north --CAUSES-->   harrying-of-the-stony-shore        (T2)
  ironborn-invasion-of-the-north --ENABLES-->  capture-of-winterfell              (T2)
  harrying-of-the-stony-shore   --ENABLES-->   capture-of-winterfell              (T2, raid-as-cover)
  + roles (T1): balon AGENT_IN declaration; balon COMMANDS_IN invasion;
    theon/asha/victarion AGENT_IN invasion; theon AGENT_IN capture-of-winterfell

HARD-STOP: terminus is capture-of-winterfell (a concrete sub-event). No edge into
war-of-the-five-kings. The sack-of-winterfell (Ramsay's later burning) stays downstream,
NOT a J4 terminus.

Causal/agency edges (Tier-2) carry verified_by='pending-j4-verify' until a fresh subagent
confirms. Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-j4-balon-invasion-2026-06-22.jsonl"

RUN_ID = "causal-arc-j4-balon-invasion-20260622"
PRODUCED_AT = "2026-06-22T00:00:00+00:00"
COMMON = {
    "decision": "emit_edge",
    "candidate_kind": "causal-curator-arc",
    "evidence_kind": "book-pass1",
    "typed_by": "curator-causal-arc",
    "schema_version": "pass1-derived-v1",
    "produced_at": PRODUCED_AT,
    "run_id": RUN_ID,
}

WARD = "theon-greyjoy-taken-as-ward"
DECLARE = "balon-declares-himself-king"
INVASION = "ironborn-invasion-of-the-north"
MOAT = "fall-of-moat-cailin"
STONY = "harrying-of-the-stony-shore"
CAPTURE = "capture-of-winterfell"
BALON = "balon-greyjoy"
THEON = "theon-greyjoy"
ASHA = "asha-greyjoy"
VICTARION = "victarion-greyjoy"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified)
EDGES_SPEC = [
    # fresh-verify (2026-06-22) REJECTED two edges, removed here:
    #   (WARD ENABLES DECLARE)  -- sequence-not-cause: ward/envoy status is incidental to Balon's
    #       trait-driven refusal; his fleet was already mustering. The arc roots at DECLARE as an
    #       intentional standalone (prime mover = Balon's opportunism + fixed character, cf. Kingsmoot arc).
    #   (DECLARE MOTIVATES BALON) -- circular self-MOTIVATES: an event can't motivate its own sole
    #       agent; the declaration IS Balon's decision. His pride is captured in the node ## Quotes.
    (DECLARE, "CAUSES", INVASION, 2, "acok", "acok-theon-01", 365,
     "I mean to carve out a kingdom with fire and sword . . . but not from the west, and not at the bidding of King Robb the Boy.",
     "Balon's decision to refuse vassalage and take a crown by the iron price is what produces the invasion (he names the undefended North as his target). Mediated decision => CAUSES Tier-2.",
     "pending-j4-verify"),
    (DECLARE, "MOTIVATES", THEON, 2, "acok", "acok-theon-03", 119,
     "I am a Greyjoy, and I mean to be my father’s heir. How can I do that unless I prove myself with some great deed?",
     "Agency level 2: scorned by Balon at the declaration and pressed to prove he is no Stark, Theon is driven to a great deed -- the drive that becomes the unauthorized seizure of Winterfell. Event-condition -> named character => MOTIVATES Tier-2.",
     "pending-j4-verify"),
    (INVASION, "CAUSES", MOAT, 2, "acok", "acok-theon-02", 413,
     "Once we hold Moat Cailin, the pup will not be able to win back to the north",
     "The fall of Moat Cailin is an explicit ordered thrust of the invasion (Victarion's main thrust up the Saltspear). Invasion-launch produces the prong battle => CAUSES Tier-2.",
     "pending-j4-verify"),
    (INVASION, "CAUSES", STONY, 2, "acok", "acok-theon-02", 399,
     "You are to harry the Stony Shore, raiding the fishing villages and sinking any ships you chance to meet.",
     "The harrying of the Stony Shore is an explicit ordered prong of the invasion (Theon's assigned raid). Invasion-launch produces the prong => CAUSES Tier-2.",
     "pending-j4-verify"),
    (INVASION, "ENABLES", CAPTURE, 2, "acok", "acok-theon-02", 417,
     "The lords are gone south with the pup. Those who remained behind are the cravens, old men, and green boys.",
     "The invasion (and the prior southward march) strips the North of its defenders, creating the opening Theon exploits. Precondition, not the order to take Winterfell (which was never given) => ENABLES Tier-2.",
     "pending-j4-verify"),
    (STONY, "ENABLES", CAPTURE, 2, "acok", "acok-theon-03", 63,
     "Theon’s bloody work along the Stony Shore would be put down to sea raiders out for plunder. The northmen would not realize their true peril",
     "Theon's assigned Stony-Shore raid is the diversionary cover that masks his unauthorized inland strike on Winterfell -- the operational precondition for the surprise. The against-orders nature: he repurposed the raid he was ordered to make. ENABLES Tier-2.",
     "pending-j4-verify"),
    # --- role edges (Tier-1) ---
    (BALON, "AGENT_IN", DECLARE, 1, "acok", "acok-theon-01", 361,
     "I am the Greyjoy, Lord Reaper of Pyke, King of Salt and Rock, Son of the Sea Wind",
     "Balon is the agent who proclaims himself king. Role edge => AGENT_IN Tier-1.",
     None),
    (BALON, "COMMANDS_IN", INVASION, 1, "acok", "acok-theon-02", 413,
     "the main thrust shall fall to you",
     "Balon directs the invasion from Pyke, assigning each thrust. Role edge => COMMANDS_IN Tier-1.",
     None),
    (THEON, "AGENT_IN", INVASION, 1, "acok", "acok-theon-02", 399,
     "You are to harry the Stony Shore, raiding the fishing villages and sinking any ships you chance to meet.",
     "Theon leads the Stony-Shore prong of the invasion. Role edge => AGENT_IN Tier-1.",
     None),
    (ASHA, "AGENT_IN", INVASION, 1, "acok", "acok-theon-03", 63,
     "His thrice-damned sister was sailing her Black Wind north even now, sure to win a castle of her own.",
     "Asha leads the Deepwood Motte prong of the invasion. Role edge => AGENT_IN Tier-1.",
     None),
    (VICTARION, "AGENT_IN", INVASION, 1, "acok", "acok-theon-02", 413,
     "the main thrust shall fall to you",
     "Victarion leads the main thrust up the Saltspear to Moat Cailin. Role edge => AGENT_IN Tier-1.",
     None),
    (THEON, "AGENT_IN", CAPTURE, 1, "acok", "acok-theon-03", 119,
     "I am a Greyjoy, and I mean to be my father’s heir.",
     "Theon is the agent who seizes Winterfell (against his orders). Role edge linking the seizer to the event hub => AGENT_IN Tier-1.",
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
    all_slugs = {s[0] for s in EDGES_SPEC} | {s[2] for s in EDGES_SPEC}
    resolved, missing = precheck_slugs(all_slugs)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed (non-existent targets): {missing}")
    print(f"slug pre-check OK: {len(resolved)} resolved.")

    lines = EDGES.read_text(encoding="utf-8").splitlines()
    if any(RUN_ID in ln for ln in lines):
        sys.exit(f"ABORT: run_id {RUN_ID} already present in {EDGES} -- already minted.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    new_rows = [make_row(s) for s in EDGES_SPEC]
    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    n_causal = sum(1 for s in EDGES_SPEC if s[1] in ("CAUSES", "TRIGGERS", "ENABLES", "MOTIVATES"))
    n_role = len(EDGES_SPEC) - n_causal
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges ({n_causal} causal/agency Tier-2 + {n_role} role Tier-1).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines.")


if __name__ == "__main__":
    main()
