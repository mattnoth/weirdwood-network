#!/usr/bin/env python3
"""Mint the Tywin's-death causal arc (S109 causal-arc track).

Dip-driven (fresh arc-weighted dip, 2026-06-19, working/session-results/
2026-06-19-fresh-arc-dip.md): Q14 "consequences of Tywin's death" was a DOUBLE
failure — (a) the natural phrase "death of Tywin" resolved to the WRONG node
(`tyrion-processes-the-assassination-attempt`, score 1.00) because
`assassination-of-tywin-lannister` had empty aliases, and (b) the assassination
node had ZERO causal edges (only PART_OF war-of-the-five-kings). This builds the
UPSTREAM causal chain (the iconic ASOS killing) and fixes discoverability.

Node repairs (done in the .node.md files, not here):
  - assassination-of-tywin-lannister: retyped event.battle -> event.assassination;
    junk misparsed-infobox display edges removed; natural-phrase aliases added.

Three new beat-nodes (all ASOS Tyrion XI = asos-tyrion-11, all Tier-1 quotes):
  - jaime-frees-tyrion-from-the-black-cells (event.incident)
  - jaime-reveals-the-truth-of-tysha       (event.incident)
  - tyrion-kills-shae-in-tywins-bed         (event.death)

Reused existing nodes (verified vs edges.jsonl, NOT re-minted):
  - trial-of-tyrion-lannister (the built Q3 chain terminus — upstream attaches here)
  - gregor-confesses-and-kills-oberyn (the trial-by-combat that condemns Tyrion;
    causal-dark, correct role edges: gregor AGENT_IN / oberyn VICTIM_IN / cersei
    COMMANDS_IN)
  - assassination-of-tywin-lannister (repaired, not re-minted)

Causal spine (all Tier-2, chain-as-arc, NO umbrella parent):
  trial            --TRIGGERS-->  gregor-kills-oberyn   (trial-by-combat verdict; S109 verifier retype CAUSES->TRIGGERS)
  gregor-kills-oberyn --CAUSES--> jaime-frees-tyrion    (death sentence -> rescue)
  jaime-frees      --CAUSES-->    tysha-revelation      (same encounter)
  tysha-revelation --CAUSES-->    assassination-of-tywin (the patricide)
  tysha-revelation --CAUSES-->    tyrion-kills-shae     (same path up the ladder)
  tysha-revelation --MOTIVATES--> tyrion-lannister      (the truth drives his choice)

Agency-collapse handled on role edges / MOTIVATES, NOT collapsed arrows:
  - The freeing carries Jaime AGENT_IN + Varys COMMANDS_IN (whose decision freed him).
  - The patricide is Tyrion's choice: tysha-revelation MOTIVATES tyrion-lannister
    + tyrion AGENT_IN the assassination. The Shae killing is a co-located sibling
    beat (caused by the same revelation that sent Tyrion up the shaft), NOT a cause
    of the patricide (whose motive is Tysha) — avoids granularity-overclaim.

HARD-STOP: no causal edge into war-of-the-five-kings. The assassination's PART_OF
war-of-the-five-kings is pre-existing structural, untouched. Downstream consequences
(Cersei's unchecked regency, Tommen's reign) are DEFERRED — those beat-nodes don't
exist yet; minting a long-distance ASOS->ADWD CAUSES would be a thesis, not an edge.

Slugs verified to exist vs graph/nodes/: tyrion-lannister, tywin-lannister,
jaime-lannister, varys, shae (characters); tower-of-the-hand, black-cells
(locations). No `crossbow` node exists -> WIELDED_IN skipped (would orphan).

Causal edges (Tier-2) carry verified_by='pending-s109-tywin-verify' until a fresh
subagent confirms against the local cache. Role edges Tier-1.

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-tywin-death-arc-2026-06-19.jsonl"

RUN_ID = "causal-arc-tywin-death-20260619"
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

ASSN = "assassination-of-tywin-lannister"
SHAE = "tyrion-kills-shae-in-tywins-bed"
FREE = "jaime-frees-tyrion-from-the-black-cells"
TYSHA = "jaime-reveals-the-truth-of-tysha"
TRIAL = "trial-of-tyrion-lannister"
OBERYN = "gregor-confesses-and-kills-oberyn"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted)
ROLE = [
    # assassination-of-tywin-lannister
    ("tyrion-lannister", "AGENT_IN", ASSN, 1, "asos", "asos-tyrion-11", 259,
     "Tyrion's finger clenched. The crossbow whanged just as Lord Tywin started to rise. The bolt slammed into him above the groin and he sat back down with a grunt.",
     "Tyrion looses the crossbow bolt that kills Tywin — the actor of the assassination."),
    ("tywin-lannister", "VICTIM_IN", ASSN, 1, "asos", "asos-tyrion-11", 259,
     "The bolt slammed into him above the groin and he sat back down with a grunt.",
     "Tywin is the victim shot on the privy."),
    (ASSN, "LOCATED_AT", "tower-of-the-hand", 1, "asos", "asos-tyrion-11", 217,
     "He found his father where he knew he'd find him, seated in the dimness of the privy tower, bedrobe hiked up around his hips.",
     "The killing takes place in the privy tower of the Tower of the Hand."),
    # tyrion-kills-shae-in-tywins-bed
    ("tyrion-lannister", "AGENT_IN", SHAE, 1, "asos", "asos-tyrion-11", 209,
     "Tyrion slid a hand under his father's chain, and twisted. The links tightened, digging into her neck.",
     "Tyrion strangles Shae with the gold Hand's chain — the actor of the killing."),
    ("shae", "VICTIM_IN", SHAE, 1, "asos", "asos-tyrion-11", 209,
     "The links tightened, digging into her neck. \"For hands of gold are always cold, but a woman's hands are warm,\" he said.",
     "Shae is the victim strangled in Tywin's bed."),
    (SHAE, "LOCATED_AT", "tower-of-the-hand", 1, "asos", "asos-tyrion-11", 189,
     "When he found himself in what had once been his bedchamber, he stood a long moment, breathing the silence.",
     "Shae is killed in Tywin's bedchamber, in the Tower of the Hand."),
    # jaime-frees-tyrion-from-the-black-cells
    ("jaime-lannister", "AGENT_IN", FREE, 1, "asos", "asos-tyrion-11", 45,
     "\"You won't need last words. I'm rescuing you.\" Jaime's voice was strangely solemn.",
     "Jaime physically opens the cell and frees Tyrion — the executor of the rescue."),
    ("varys", "COMMANDS_IN", FREE, 1, "asos", "asos-tyrion-11", 57,
     "The eunuch dosed their wine with sweetsleep, but not enough to kill them. ... He is waiting back at the stair, dressed up in a septon's robe.",
     "Varys orchestrated the escape (drugged the turnkeys, arranged the galley and the route) without personally opening the cell => COMMANDS_IN."),
    (FREE, "LOCATED_AT", "black-cells", 1, "asos", "asos-tyrion-11", 145,
     "On the third level the cells are smaller and the doors are wood. The black cells, men call them. That was where you were kept, and Eddard Stark before you.",
     "Tyrion is freed from the black cells (third dungeon level of the Red Keep)."),
    # jaime-reveals-the-truth-of-tysha
    ("jaime-lannister", "AGENT_IN", TYSHA, 1, "asos", "asos-tyrion-11", 79,
     "\"She was no whore. I never bought her for you. That was a lie that Father commanded me to tell. Tysha was . . . she was what she seemed to be. A crofter's daughter, chance met on the road.\"",
     "Jaime speaks the confession revealing Tysha's truth — the actor of the revelation."),
    (TYSHA, "LOCATED_AT", "black-cells", 1, "asos", "asos-tyrion-11", 95,
     "Before he had gone a dozen yards, he bumped up against an iron gate that closed the passage.",
     "The revelation happens in the dungeon corridor outside the black cells, immediately after the freeing."),
]

# Causal edges (Tier-2) — verified_by pending until subagent CONFIRM.
CAUSAL = [
    # TRIGGERS (not CAUSES) per fresh-verifier S109: the trial-by-combat death is
    # the trial's immediate, unmediated decisive act (the verdict itself), not a
    # mediated downstream effect.
    (TRIAL, "TRIGGERS", OBERYN, 2, "asos", "asos-tyrion-10", 249,
     "He never heard his father speak the words that condemned him. Perhaps no words were necessary. I put my life in the Red Viper's hands, and he dropped it.",
     "Tyrion's trial proceeds to trial by combat; the Mountain killing Oberyn (Tyrion's champion) IS the trial's decisive culminating act that condemns Tyrion — immediate, no mediating human decision => TRIGGERS Tier-2."),
    (OBERYN, "CAUSES", FREE, 2, "asos", "asos-tyrion-11", 41,
     "\"Well no, if truth be told. You're to be beheaded on the morrow, out on the old tourney grounds.\"",
     "Oberyn's death condemns Tyrion to execution, which gives Jaime (and Varys) the reason to free him the night before. Mediated by their choice (carried on the freeing's AGENT_IN/COMMANDS_IN roles) => CAUSES Tier-2."),
    (FREE, "CAUSES", TYSHA, 2, "asos", "asos-tyrion-11", 75,
     "His brother looked away. \"Tysha,\" he said softly.",
     "The freeing is the encounter in which Jaime, prompted by Tyrion demanding the truth, confesses the Tysha lie. The rescue occasions the revelation => CAUSES Tier-2."),
    (TYSHA, "CAUSES", ASSN, 2, "asos", "asos-tyrion-11", 159,
     "Tyrion walked slowly to the ladder, ran his hand across the lowest rung. \"This will take me up to my bedchamber.\"",
     "The Tysha revelation turns Tyrion from fleeing escape to climbing the shaft to kill Tywin. Mediated by Tyrion's choice (carried on MOTIVATES + the assassination's AGENT_IN) => CAUSES Tier-2."),
    (TYSHA, "CAUSES", SHAE, 2, "asos", "asos-tyrion-11", 189,
     "When he found himself in what had once been his bedchamber, he stood a long moment, breathing the silence.",
     "The same revelation sends Tyrion up the shaft, where he finds and kills Shae in Tywin's bed. The Shae killing is a sibling beat on the path, not a cause of the patricide => CAUSES Tier-2."),
    (TYSHA, "MOTIVATES", "tyrion-lannister", 2, "asos", "asos-tyrion-11", 123,
     "part of him wanted to call out, to tell him that it wasn't true, to beg for his forgiveness. But then he thought of Tysha, and he held his silence.",
     "The Tysha truth is the explicit motive that drives Tyrion's choice to kill Tywin (and Shae). Event/condition -> actor => MOTIVATES Tier-2."),
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
    new_rows += [make_row(s, verified="pending-s109-tywin-verify") for s in CAUSAL]

    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges "
          f"({len(ROLE)} role/structural + {len(CAUSAL)} causal tier-2).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines.")


if __name__ == "__main__":
    main()
