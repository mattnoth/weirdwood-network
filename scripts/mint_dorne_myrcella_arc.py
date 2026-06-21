#!/usr/bin/env python3
"""Mint the AFFC "Dorne / Myrcella" (Queenmaker) causal arc (S117 causal-arc track).

AFFC smoke-test fumble #4 (working/session-results/2026-06-20-affc-smoke.md) — the
last of the four AFFC arc-clusters. Major-arc backlog: Myrcella's maiming is the
foreshadowed event; this builds the Queenmaker-plot spine that produces it.

New beat-nodes (written as .node.md, not here):
  - the-queenmaker-plot              (event.conspiracy; AFFC Soiled Knight + Queenmaker)
  - myrcella-is-maimed-by-darkstar   (event.incident;   AFFC Queenmaker + Princess in the Tower)
Repaired existing nodes (aliases + quotes + clean body, done in the .md files):
  - arrest-of-the-sand-snakes        (root-thread node; prose body added)
  - areo-hotah-springs-the-ambush    (spaced aliases + quotes added)
  - arianne-collapses-and-is-captured(spaced aliases + quotes added)

ROOTED arc (NOT standalone): the Dorne thread roots cross-book at Oberyn's death.
  gregor-confesses-and-kills-oberyn --CAUSES--> arrest-of-the-sand-snakes
This is the S115 root-check (machine step 5b) cross-book auto-join: Oberyn dies in the
trial by combat (Tywin arc, S109); his death throws Dorne into war-fever, which is why
Doran arrests the Sand Snakes. The Queenmaker plot itself is a parallel prime mover
(Arianne's inheritance-fear, an actor-internal motive with no upstream event node);
it connects to the rooted thread via `arrest MOTIVATES arianne-martell` (she is
AGENT_IN the plot). Declared in the worklog: rooted, with one standalone prime-mover
thread (the plot's birthright motive), explicitly noted — not an oversight.

Causal spine (chain-as-arc, NO umbrella parent; Tier-2, verified_by pending):
  gregor-confesses-and-kills-oberyn --CAUSES--> arrest-of-the-sand-snakes   (ROOT)
  the-queenmaker-plot --CAUSES--> areo-hotah-springs-the-ambush
  areo-hotah-springs-the-ambush --TRIGGERS--> myrcella-is-maimed-by-darkstar
  areo-hotah-springs-the-ambush --CAUSES--> arianne-collapses-and-is-captured
Agency (Tier-2):
  arrest-of-the-sand-snakes --MOTIVATES--> arianne-martell

Role edges (Tier-1):
  arianne-martell  --AGENT_IN-->  the-queenmaker-plot              (instigator)
  arys-oakheart    --AGENT_IN-->  the-queenmaker-plot              (seduced, sworn)
  gerold-dayne     --AGENT_IN-->  the-queenmaker-plot              (recruited for sword+castle)
  myrcella-baratheon --VICTIM_IN--> the-queenmaker-plot            (the unwitting instrument)
  gerold-dayne     --AGENT_IN-->  myrcella-is-maimed-by-darkstar
  myrcella-baratheon --VICTIM_IN--> myrcella-is-maimed-by-darkstar

CAUSES vs TRIGGERS:
  - oberyn-death -> arrest is CAUSES (mediated by the Dornish war-fever the death
    provokes, plus Doran's deliberate decision to confine his nieces to defuse it).
  - plot -> ambush is CAUSES (mediated by the informer who betrays it and Doran's
    choice to let it run before springing Hotah "by your father's word").
  - ambush -> maiming is TRIGGERS (Darkstar strikes in the immediate chaos of the
    ambush — the ambush is the immediate occasion of the blow).
  - ambush -> Arianne's capture is CAUSES (the whole ambush action results in her
    collapse, binding, and return to Sunspear).

TRAP avoided: `conquest-of-dorne` = the HISTORICAL conquest of Dorne (Daeron I, AC 161),
NOT the AFFC Queenmaker plot. Not wired, not referenced.
SKIP (conservative, no new vocab): Arianne WITNESS_IN the maiming — WITNESS_IN is not a
live edge type (0 uses) and would need a worklog vocab decision; the role is not
load-bearing and Arianne is already AGENT_IN the plot + VICTIM_IN the capture. The
death of Arys Oakheart is folded into areo-hotah-springs-the-ambush (he is already a
VICTIM_IN there) rather than minted as a separate node (handoff scope: 1-2 mints).
Darkstar's war-aim (his motive for the maiming) is carried in the node body + AGENT_IN
role edge, not a MOTIVATES edge (MOTIVATES targets an actor, not a wound).

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-dorne-myrcella-arc-2026-06-20.jsonl"

RUN_ID = "causal-arc-dorne-myrcella-20260620"
PRODUCED_AT = "2026-06-20T00:00:00+00:00"
PENDING = "pending-s117-dorne-myrcella-verify"
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
OBERYN_DEATH = "gregor-confesses-and-kills-oberyn"
ARREST = "arrest-of-the-sand-snakes"
PLOT = "the-queenmaker-plot"
AMBUSH = "areo-hotah-springs-the-ambush"
MAIM = "myrcella-is-maimed-by-darkstar"
CAPTURE = "arianne-collapses-and-is-captured"
ARIANNE = "arianne-martell"
ARYS = "arys-oakheart"
DARKSTAR = "gerold-dayne"
MYRCELLA = "myrcella-baratheon"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified)
EDGES_SPEC = [
    # --- causal spine (Tier-2, pending verify) ---
    (OBERYN_DEATH, "CAUSES", ARREST, 2, "affc", "affc-the-captain-of-guards-01", 35,
     "In Sunspear, on the Broken Arm, along the Greenblood, in the mountains, out in the deep sand, everywhere, everywhere, women tear their hair and men cry out in rage. The same question is heard on every tongue—what will Doran do? What will his brother do to avenge our murdered prince?",
     "Oberyn's death in the trial by combat throws Dorne into a war-fever; the smallfolk cry for vengeance and Oberyn's daughters (the Sand Snakes) agitate to lead it. Doran confines his nieces to the Spear Tower precisely to defuse that fever and his loyalty to Tywin ('so he might know what a loyal friend he has in Sunspear', :353). Mediated by the climate the death provokes + Doran's decision => CAUSES Tier-2. Cross-book root: Oberyn's death is the Tywin-arc node (S109).",
     PENDING),
    (PLOT, "CAUSES", AMBUSH, 2, "affc", "affc-the-queenmaker-01", 267,
     "\"Yield, my princess,\" the captain called, \"else we must slay all but the child and yourself, by your father's word.\"",
     "Arianne's plot is betrayed to Doran ('Someone told', :299); he lets it run to confirm her guilt, then positions Hotah to ambush the conspirators 'by your father's word'. The ambush exists only because the plot does — mediated by the informer and Doran's deliberate decision => CAUSES Tier-2.",
     PENDING),
    (AMBUSH, "TRIGGERS", MAIM, 2, "affc", "affc-the-queenmaker-01", 291,
     "Myrcella was on the ground, wailing, shaking, her pale face in her hands, blood streaming through her fingers.",
     "In the immediate chaos of Hotah's ambush, Darkstar turns his sword on Myrcella and maims her — the ambush is the immediate occasion of the strike (he acts while 'all eyes were on your white knight'). Immediate specific spark => TRIGGERS Tier-2.",
     PENDING),
    (AMBUSH, "CAUSES", CAPTURE, 2, "affc", "affc-the-queenmaker-01", 293,
     "When they sought to bind her hands behind her back, she did not resist. One of the guardsmen jerked her to her feet. He wore her father's colors.",
     "Hotah's ambush results in Arianne's collapse, binding, and return to Sunspear as a prisoner — the capture is the outcome of the whole ambush action. Mediated => CAUSES Tier-2.",
     PENDING),
    # --- agency (Tier-2, pending verify) ---
    (ARREST, "MOTIVATES", ARIANNE, 2, "affc", "affc-the-soiled-knight-01", 233,
     "If she can be imprisoned, so can I, and for the same cause . . . this of Myrcella.",
     "The imprisonment of her cousins makes Arianne fear she will share their fate and hardens her resolve to act on the Myrcella scheme; freeing the Sand Snakes is also a stated aim of the plot (:83). Event -> actor => MOTIVATES Tier-2 (the secondary motive that links the rooted thread to the plot; the plot's prime mover is her inheritance-fear, an actor-internal motive carried in the node body).",
     PENDING),
    # --- role edges (Tier-1), the-queenmaker-plot ---
    (ARIANNE, "AGENT_IN", PLOT, 1, "affc", "affc-the-queenmaker-01", 85,
     "That, and my birthright. I want Sunspear, and my father's seat. I want Dorne. \"I want justice.\"",
     "Arianne Martell is the instigator and leader of the conspiracy. Role edge => AGENT_IN Tier-1.",
     None),
    (ARYS, "AGENT_IN", PLOT, 1, "affc", "affc-the-soiled-knight-01", 275,
     "\"I will.\" Ser Arys sank to one knee. \"Myrcella is the elder, and better suited to the crown... I am yours. What would you have of me?\"",
     "Ser Arys Oakheart, Myrcella's sworn shield, is seduced into the plot and pledges to crown her. Role edge => AGENT_IN Tier-1.",
     None),
    (DARKSTAR, "AGENT_IN", PLOT, 1, "affc", "affc-the-queenmaker-01", 55,
     "\"We need him,\" Arianne reminded them. \"It may be that we will need his sword, and we will surely need his castle.\"",
     "Ser Gerold Dayne (Darkstar) is recruited into the conspiracy for his sword and his castle. Role edge => AGENT_IN Tier-1.",
     None),
    (MYRCELLA, "VICTIM_IN", PLOT, 1, "affc", "affc-the-queenmaker-01", 109,
     "Confused, Myrcella clutched Arys Oakheart by the arm. \"Why do they call me Grace?\" she asked in a plaintive voice.",
     "Myrcella Baratheon is the plot's unwitting instrument — taken from Sunspear and hailed as queen without understanding what is happening to her. Role edge => VICTIM_IN Tier-1.",
     None),
    # --- role edges (Tier-1), myrcella-is-maimed-by-darkstar ---
    (DARKSTAR, "AGENT_IN", MAIM, 1, "affc", "affc-the-princess-in-the-tower-01", 169,
     "No, though Darkstar did his best... the slash opened her cheek down to the bone and sliced off her right ear.",
     "Ser Gerold Dayne (Darkstar) is the actor who slashes at and maims Myrcella. Role edge => AGENT_IN Tier-1.",
     None),
    (MYRCELLA, "VICTIM_IN", MAIM, 1, "affc", "affc-the-princess-in-the-tower-01", 169,
     "the slash opened her cheek down to the bone and sliced off her right ear. Maester Caleotte was able to save her life, but no poultice nor potion will ever restore her face.",
     "Myrcella Baratheon is the child wounded — cheek opened to the bone, right ear severed, face ruined forever. Role edge => VICTIM_IN Tier-1.",
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
