#!/usr/bin/env python3
"""Mint the AFFC "Cersei's downfall" causal arc (S114 causal-arc track).

Major-arc backlog #17 + AFFC smoke-test #1 fumble
(working/session-results/2026-06-20-affc-smoke.md). The entire AFFC causal layer
was DARK (0 causal edges on every AFFC anchor). This is the cheapest+most-major
AFFC arc: a clean self-caused chain — Cersei arms the Faith Militant, then her
own plot against Margaery produces the confession the armed Faith uses to ruin
HER.

New beat-nodes (written as .node.md, not here):
  - cersei-rearms-the-faith-and-forgives-the-debt   (event.incident; AFFC Cersei IV+VI)
  - osney-kettleblack-confesses-to-high-sparrow      (event.incident; AFFC Cersei X)

Existing beat-nodes wired (already present):
  - cersei-plots-against-margaery / cersei-confronts-and-arrests-the-blue-bard
  - cersei-is-captured-in-the-sept / cersei-is-stripped-and-imprisoned

Causal spine (chain-as-arc, NO umbrella parent; Tier-2, verified_by pending):
  cersei-plots-against-margaery --CAUSES--> cersei-confronts-and-arrests-the-blue-bard
  cersei-plots-against-margaery --CAUSES--> osney-kettleblack-confesses-to-high-sparrow
  osney-kettleblack-confesses-to-high-sparrow --TRIGGERS--> cersei-is-captured-in-the-sept
  cersei-rearms-the-faith-and-forgives-the-debt --CAUSES--> cersei-is-captured-in-the-sept   [THE IRONY]
  cersei-is-captured-in-the-sept --CAUSES--> cersei-is-stripped-and-imprisoned

Role edges (Tier-1) for the two new nodes:
  cersei-lannister --AGENT_IN--> cersei-rearms-the-faith-and-forgives-the-debt
  high-sparrow --AGENT_IN--> cersei-rearms-the-faith-and-forgives-the-debt
  osney-kettleblack --AGENT_IN--> osney-kettleblack-confesses-to-high-sparrow
  high-sparrow --COMMANDS_IN--> osney-kettleblack-confesses-to-high-sparrow
  cersei-lannister --VICTIM_IN--> osney-kettleblack-confesses-to-high-sparrow

TRIGGERS vs CAUSES: Osney's tortured true confession is the immediate, specific
spark of the arrest (TRIGGERS); the rearming is the mediated enabling condition
(she armed the institution that seizes her) -> CAUSES. The Margaery plot CAUSES
both the Blue-Bard arrest and the Osney confession (mediated execution of the
scheme). All causal edges Tier-2 (interpretive link); role edges Tier-1.

The dropped edge (rearm -> plot): NOT minted. Cersei's plot against Margaery
springs from her own paranoia/jealousy, not from having armed the Faith; the
self-caused irony is fully carried by the rearm--CAUSES-->capture edge. Left to
the verifier to confirm the exclusion is right.

BONUS DATA FIX (same pass, S109-style): cersei-is-stripped-and-imprisoned had
LOCATED_AT -> tower-of-the-hand, but its own rationale + participant_name say
"Great Sept of Baelor" (where the stripping happens). Retarget -> great-sept-of-
baelor to match the sibling capture node.

HARD-STOP: arc terminates at cersei-is-stripped-and-imprisoned (AFFC). The walk
of atonement + trial are deferred ADWD beats.

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-cersei-downfall-arc-2026-06-20.jsonl"

RUN_ID = "causal-arc-cersei-downfall-20260620"
PRODUCED_AT = "2026-06-20T00:00:00+00:00"
PENDING = "pending-s114-cersei-downfall-verify"
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
REARM = "cersei-rearms-the-faith-and-forgives-the-debt"
OSNEY_CONF = "osney-kettleblack-confesses-to-high-sparrow"
PLOT = "cersei-plots-against-margaery"
BLUEBARD = "cersei-confronts-and-arrests-the-blue-bard"
CAPTURE = "cersei-is-captured-in-the-sept"
STRIPPED = "cersei-is-stripped-and-imprisoned"
CERSEI = "cersei-lannister"
SPARROW = "high-sparrow"
OSNEY = "osney-kettleblack"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified)
EDGES_SPEC = [
    # --- causal spine (Tier-2, pending verify) ---
    (PLOT, "CAUSES", BLUEBARD, 2, "affc", "affc-cersei-09", 163,
     "Liar! Cersei smashed the lute across the singer's face so hard the painted wood exploded into shards and splinters. Lord Orton, summon my guards and take this creature to the dungeons.",
     "The Blue Bard (Wat) is arrested and broken to manufacture corroborating 'evidence' of Margaery's adultery; the arrest is a direct step in executing Cersei's frame-up plot. Mediated execution of the scheme => CAUSES Tier-2.",
     PENDING),
    (PLOT, "CAUSES", OSNEY_CONF, 2, "affc", "affc-cersei-09", 311,
     "No, you must take yourself to the Great Sept of Baelor this very night and speak with the High Septon. ... Tell him how you bedded Margaery and her cousins.",
     "Cersei scripts and orders Osney's confession to the High Septon as the public mechanism of the frame-up against Margaery. Mediated execution of the plot => CAUSES Tier-2.",
     PENDING),
    (OSNEY_CONF, "TRIGGERS", CAPTURE, 2, "affc", "affc-cersei-10", 243,
     "That one there. She's the queen I fucked, the one sent me to kill the old High Septon. He never had no guards. I just come in when he was sleeping and pushed a pillow down across his face.",
     "Under the Faith's torture Osney recants the Margaery story and names Cersei as his lover and as the murderer of the previous High Septon; this expanded true confession is the immediate, specific grounds on which the Faith seizes her. Immediate spark => TRIGGERS Tier-2.",
     PENDING),
    (REARM, "CAUSES", CAPTURE, 2, "affc", "affc-cersei-10", 249,
     "There were women waiting for her there, more septas and silent sisters too ... they laid hands upon her. Cersei ran to the altar of the Mother, but they caught her there, a score of them, and dragged her kicking up the tower steps.",
     "Cersei restored the Warrior's Sons and Poor Fellows (the armed Faith Militant) in AFFC Cersei VI; in Cersei X that same rearmed, now-independent Faith seizes and imprisons her. The institution she armed to neutralize the Tyrells becomes the agent of her arrest. Mediated self-caused consequence => CAUSES Tier-2. THE IRONY SPINE.",
     PENDING),
    (CAPTURE, "CAUSES", STRIPPED, 2, "affc", "affc-cersei-10", 249,
     "Inside the cell three silent sisters held her down as a septa named Scolera stripped her bare. She even took her smallclothes.",
     "Immediately after the seizure at the altar Cersei is dragged to a tower cell and stripped; the imprisonment follows directly from the capture as the same detention event. Mediated consequence => CAUSES Tier-2.",
     PENDING),
    # --- role edges (Tier-1) for the two new nodes ---
    (CERSEI, "AGENT_IN", REARM, 1, "affc", "affc-cersei-06", 273,
     "As you wish. This debt shall be forgiven, and King Tommen will have his blessing. The Warrior's Sons shall escort me to him ...",
     "Cersei is the crown agent who forgives the debt and grants the rearming. Role edge => AGENT_IN Tier-1.",
     None),
    (SPARROW, "AGENT_IN", REARM, 1, "affc", "affc-cersei-06", 265,
     "The Faith Militant reborn ... If His Grace were to allow me to restore the ancient blessed orders of the Sword and Star ...",
     "The High Septon (High Sparrow) proposes and is the counterparty to the deal that rearms the Faith. Role edge => AGENT_IN Tier-1.",
     None),
    (OSNEY, "AGENT_IN", OSNEY_CONF, 1, "affc", "affc-cersei-10", 243,
     "That one there. She's the queen I fucked, the one sent me to kill the old High Septon.",
     "Osney Kettleblack is the confessor. Role edge => AGENT_IN Tier-1.",
     None),
    (SPARROW, "COMMANDS_IN", OSNEY_CONF, 1, "affc", "affc-cersei-10", 27,
     "Ser Osney Kettleblack has confessed his carnal knowledge of the queen to the High Septon himself, before the altar of the Father.",
     "The High Septon holds Osney and extracts the confession under the Faith's authority. Role edge => COMMANDS_IN Tier-1.",
     None),
    (CERSEI, "VICTIM_IN", OSNEY_CONF, 1, "affc", "affc-cersei-10", 243,
     "She's the queen I fucked, the one sent me to kill the old High Septon.",
     "The confession names and destroys Cersei; she is the party undone by it. Role edge => VICTIM_IN Tier-1.",
     None),
]

# LOCATED_AT data fix on the stripped node
FIX_SRC = STRIPPED
FIX_ETYPE = "LOCATED_AT"
FIX_OLD_TGT = "tower-of-the-hand"
FIX_NEW_TGT = "great-sept-of-baelor"


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

    # apply the LOCATED_AT data fix in place
    fixed = 0
    out_lines = []
    for ln in lines:
        try:
            obj = json.loads(ln)
        except json.JSONDecodeError:
            out_lines.append(ln)
            continue
        if (obj.get("edge_type") == FIX_ETYPE
                and obj.get("source_slug") == FIX_SRC
                and obj.get("target_slug") == FIX_OLD_TGT):
            obj["target_slug"] = FIX_NEW_TGT
            obj["located_at_fix"] = "s114-cersei-arc: retargeted tower-of-the-hand -> great-sept-of-baelor (own rationale/participant_name said Great Sept)"
            out_lines.append(json.dumps(obj, ensure_ascii=False))
            fixed += 1
        else:
            out_lines.append(ln)

    new_rows = [make_row(s) for s in EDGES_SPEC]

    with open(EDGES, "w", encoding="utf-8") as f:
        for ln in out_lines:
            f.write(ln + "\n")
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    n_causal = sum(1 for s in EDGES_SPEC if s[1] in ("CAUSES", "TRIGGERS", "MOTIVATES"))
    n_role = len(EDGES_SPEC) - n_causal
    print(f"Backed up -> {BACKUP.name}")
    print(f"LOCATED_AT fix applied to {fixed} row(s) ({FIX_OLD_TGT} -> {FIX_NEW_TGT}).")
    print(f"Appended {len(new_rows)} edges ({n_causal} causal Tier-2 pending-verify + {n_role} role Tier-1).")
    print(f"edges.jsonl now: {len(out_lines) + len(new_rows)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
