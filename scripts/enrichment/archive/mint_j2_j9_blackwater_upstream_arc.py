#!/usr/bin/env python3
"""Mint the J2+J9 "Blackwater UPSTREAM" arc (WO5K-remainder track, S123).

WO5K decomposition J2+J9 (working/wo5k-decomposition.md, Rank 3). The single
highest-salience dark gap: `battle-of-the-blackwater` had 3 downstream CAUSES (S111)
but ZERO causal UPSTREAM. This wires the two-pronged mechanism that put Stannis at
the gates AND formed the alliance that beat him -- completing foreshadowed event #7
(PARTIAL -> COMPLETE).

PRONG J2 (Stannis): Renly's shadow-death -> the stormlords/Reach host defects to
Stannis -> the absorbed host is the army he sails to King's Landing with.
PRONG J9 (Tyrell): Renly's death -> Loras pulls the Tyrell knights off the field ->
Littlefinger brokers the Tyrell-Lannister marriage alliance -> the Tyrell host marches
as Tywin's relief force and routs Stannis at the Blackwater.

DEDUP (from the J2+J9 dip):
  - `fighting-at-bitterbridge` EXISTS and IS the realignment locus (kept; Loras AGENT_IN
    wired to it). NOT a substitute for the two mints below.
  - `sack-of-bitterbridge` = Dance of the Dragons (130 AC) -- name-collision, NEVER wire.
  - `tyrell-plot-revealed` = the Purple-Wedding poisoning plot -- unrelated, NEVER wire.
  - `melee-at-bitterbridge` = the pre-war tourney -- irrelevant.

New beat-nodes (written as .node.md, not here):
  - stannis-absorbs-renly-s-host                  (event.incident; ACOK Catelyn IV / Tyrion VIII)
  - littlefinger-brokers-tyrell-lannister-alliance (event.conspiracy; ACOK Tyrion VIII)
The third candidate ("Tyrell forces march to join Tywin") is FOLDED into the brokering
CAUSES battle-of-the-blackwater edge -- no standalone node (over-fragmentation).

Edges (vocab-locked CAUSES/TRIGGERS/ENABLES/MOTIVATES + role AGENT_IN):
  J2:
    shadow-assassination-of-renly  --CAUSES-->   stannis-absorbs-renly-s-host        (T2)
    stannis-absorbs-renly-s-host   --ENABLES-->  battle-of-the-blackwater            (T2)
    stannis-baratheon              --AGENT_IN--> stannis-absorbs-renly-s-host        (T1)
  J9:
    shadow-assassination-of-renly  --MOTIVATES-> loras-tyrell                        (T2)
    loras-tyrell                   --AGENT_IN--> fighting-at-bitterbridge            (T1)
    shadow-assassination-of-renly  --ENABLES-->  littlefinger-brokers-...-alliance   (T2)
    tyrion-lannister               --AGENT_IN--> littlefinger-brokers-...-alliance   (T1)
    petyr-baelish                  --AGENT_IN--> littlefinger-brokers-...-alliance   (T1)
    littlefinger-brokers-...-allnc --CAUSES-->   battle-of-the-blackwater            (T2)

Edge-type rationale:
  - shadow CAUSES absorption: mediated (defections accrue over days), not an instant spark.
  - absorption ENABLES blackwater: the host is the precondition (numbers) for Stannis's
    assault -- necessary, not sufficient ("Most of Stannis's host had been Renly's to start").
  - shadow MOTIVATES loras: Renly's death drives Loras's grief-decision to quit the field
    (agency lands on the character).
  - shadow ENABLES brokering: Renly's death is the precondition that frees the Tyrells to be
    courted ("They loved Renly, clearly, but Renly is slain").
  - brokering CAUSES blackwater: the marriage pact delivers the fifty-thousand-strong Tyrell
    relief host that falls on Stannis's flank -- mediated (pact -> host marches -> battle).

HARD-STOP: no causal edge into war-of-the-five-kings. Downstream of the battle already wired.

Causal/agency edges (Tier-2) carry verified_by='pending-j2j9-verify' until a fresh
subagent confirms against the local cache.

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-j2j9-blackwater-upstream-2026-06-22.jsonl"

RUN_ID = "causal-arc-j2j9-blackwater-upstream-20260622"
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

SHADOW = "shadow-assassination-of-renly"
ABSORB = "stannis-absorbs-renly-s-host"
BROKER = "littlefinger-brokers-tyrell-lannister-alliance"
BLACKWATER = "battle-of-the-blackwater"
BITTERBRIDGE = "fighting-at-bitterbridge"
STANNIS = "stannis-baratheon"
LORAS = "loras-tyrell"
TYRION = "tyrion-lannister"
PETYR = "petyr-baelish"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified)
EDGES_SPEC = [
    # --- PRONG J2 ---
    (SHADOW, "CAUSES", ABSORB, 2, "acok", "acok-catelyn-04", 149,
     "All the power of Storm’s End and Highgarden, the power that had been Renly’s an hour ago. They belong to Stannis now ... Stannis has won all with a single evil stroke.",
     "Renly's death is the mediated cause of his host defecting to Stannis (the defections accrue over the days after Storm's End, not in an instant). CAUSES Tier-2.",
     "pending-j2j9-verify"),
    (ABSORB, "ENABLES", BLACKWATER, 2, "asos", "asos-tyrion-01", 81,
     "Most of Stannis’s host had been Renly’s to start, and they went right back over at the sight of him in that shiny green armor.",
     "The absorbed host is the precondition (numbers) for Stannis's assault on King's Landing -- his Blackwater army WAS Renly's host. Necessary but not sufficient => ENABLES Tier-2.",
     "pending-j2j9-verify"),
    (STANNIS, "AGENT_IN", ABSORB, 1, "acok", "acok-tyrion-08", 53,
     "Many serve the lords who remained at Storm’s End, and those lords now belong to Stannis.",
     "Stannis is the beneficiary-agent who gains Renly's host. Role edge => AGENT_IN Tier-1.",
     None),
    # --- PRONG J9 ---
    (SHADOW, "MOTIVATES", LORAS, 2, "acok", "acok-tyrion-08", 49,
     "It’s said the Knight of Flowers went mad when he saw his king’s body, and slew three of Renly’s guards in his wrath",
     "Renly's death drives Loras's grief-decision to quit the field with the Tyrell knights rather than serve Stannis. Event-condition -> named character => MOTIVATES Tier-2.",
     "pending-j2j9-verify"),
    (LORAS, "AGENT_IN", BITTERBRIDGE, 1, "acok", "acok-tyrion-08", 53,
     "Ser Loras is likely making for Bitterbridge",
     "Loras leads the Tyrell faction to Bitterbridge -- the realignment locus. Role edge => AGENT_IN Tier-1.",
     None),
    (SHADOW, "ENABLES", BROKER, 2, "acok", "acok-tyrion-08", 59,
     "They loved Renly, clearly, but Renly is slain. Perhaps we can give them good and sufficient reasons to prefer Joffrey to Stannis . . . if we move quickly.",
     "Renly's death is the precondition that frees the now-kingless Tyrells to be courted; without it there is no opening to broker. ENABLES Tier-2.",
     "pending-j2j9-verify"),
    (TYRION, "AGENT_IN", BROKER, 1, "acok", "acok-tyrion-08", 73,
     "It seems to me we should take a lesson from the late Lord Renly. We can win the Tyrell alliance as he did. With a marriage.",
     "Tyrion conceives and authorizes the marriage offer that becomes the alliance. Role edge => AGENT_IN Tier-1.",
     None),
    (PETYR, "AGENT_IN", BROKER, 1, "acok", "acok-tyrion-08", 139,
     "the king needs both of you here. Let me go in your stead.",
     "Littlefinger volunteers as envoy and conducts the negotiation at Bitterbridge and Highgarden. Role edge => AGENT_IN Tier-1.",
     None),
    # fresh-verify (2026-06-22) ADJUSTED CAUSES->ENABLES: the brokering enables the Lannister
    # VICTORY (Tyrell relief force), not the battle's OCCURRENCE (that is Stannis's assault,
    # the J2 chain). CAUSES-into-the-battle-node would conflate cause-of-outcome with cause-of-event.
    (BROKER, "ENABLES", BLACKWATER, 2, "acok", "acok-tyrion-08", 113,
     "Margaery Tyrell brings fifty thousand swords and all the strength of Highgarden.",
     "The brokered marriage pact delivers the fifty-thousand-strong Tyrell host, which marches as Tywin's relief force and falls on Stannis's flank -- the decisive intervention that wins the battle. Enables the Lannister VICTORY (not the battle's occurrence) => ENABLES Tier-2.",
     "pending-j2j9-verify"),
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
