#!/usr/bin/env python3
"""Mint the AFFC "Kingsmoot -> Euron" causal arc (S116 causal-arc track).

Major-arc backlog #20 (Euron's Kingsmoot victory) + AFFC smoke-test #2 fumble
(working/session-results/2026-06-20-affc-smoke.md) + WO5K decomposition J8.

STANDALONE arc: the prime mover is Balon Greyjoy's death (a fall from a Pyke
bridge in a storm). There is NO causal upstream by design -- Balon's death is
itself the trigger of the Iron Islands succession crisis, not a consequence of a
prior-book beat. Declared intentional in the worklog per the S115 root-check rule
(machine step 5b EXCEPTION: genuinely standalone arcs). 0-upstream here is correct.

New beat-nodes (written as .node.md, not here):
  - death-of-balon-greyjoy           (event.death; AFFC The Prophet I)
  - euron-seizes-the-seastone-chair  (event.incident; AFFC The Prophet I)
Repaired existing node:
  - kingsmoot-on-old-wyk  retyped event.battle -> event.ceremony, spaced aliases
    added, junk-bare Identity/Edges cleaned (was a near-bare Path-B wiki node).

Causal spine (chain-as-arc, NO umbrella parent; Tier-2, verified_by pending):
  death-of-balon-greyjoy --TRIGGERS--> euron-seizes-the-seastone-chair
  euron-seizes-the-seastone-chair --CAUSES--> kingsmoot-on-old-wyk
  kingsmoot-on-old-wyk --CAUSES--> taking-of-the-shields
Agency (Tier-2):
  euron-seizes-the-seastone-chair --MOTIVATES--> aeron-greyjoy

Role edges (Tier-1):
  balon-greyjoy --VICTIM_IN--> death-of-balon-greyjoy
  euron-greyjoy --AGENT_IN--> euron-seizes-the-seastone-chair
  sawane-botley --VICTIM_IN--> euron-seizes-the-seastone-chair  (drowned for objecting)
  euron-greyjoy --AGENT_IN--> kingsmoot-on-old-wyk     (chosen king)
  aeron-greyjoy --AGENT_IN--> kingsmoot-on-old-wyk     (caller / crowner)
  asha-greyjoy --AGENT_IN--> kingsmoot-on-old-wyk      (rival claimant)
  victarion-greyjoy --AGENT_IN--> kingsmoot-on-old-wyk (rival claimant)

CAUSES vs TRIGGERS: death->seizure is TRIGGERS (immediate spark -- Euron sails in
"the day after the king's death", his exile lifted the instant Balon dies).
seizure->kingsmoot is CAUSES (mediated -- Aeron's religious judgment that Euron is
godless intervenes; he deliberates, then summons the moot). kingsmoot->Shields is
CAUSES (the moot legitimizes Euron's kingship and command of the Iron Fleet, which
he then turns on the Reach -- "Your kingsmoot raised him up").

TRAP avoided: `anarchy-in-the-reach` is the HISTORICAL Gardener-era Reach
succession war (King Garth Greybeard / Manderly vs Peake), NOT Euron's invasion --
the real Reach-invasion downstream node is `taking-of-the-shields`. Not wired.
SKIP (conservative): `victarion-admits-euron-s-role-in-his-wife-s-death` is
tangential backstory (Euron impregnated Victarion's salt wife -> exile); it has no
clean causal edge into this spine and the "Euron murdered Balon" link is Tier-4/5
fan theory not stated in AFFC. Left alone (it already carries its own role edges).

HARD-STOP: arc terminates at taking-of-the-shields (Euron's Reach campaign sprawls
into many beats; staying causal-dark beyond the first conquest is correct-by-policy).

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-kingsmoot-euron-arc-2026-06-20.jsonl"

RUN_ID = "causal-arc-kingsmoot-euron-20260620"
PRODUCED_AT = "2026-06-20T00:00:00+00:00"
PENDING = "pending-s116-kingsmoot-euron-verify"
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
BALON_DEATH = "death-of-balon-greyjoy"
SEIZE = "euron-seizes-the-seastone-chair"
KINGSMOOT = "kingsmoot-on-old-wyk"
SHIELDS = "taking-of-the-shields"
BALON = "balon-greyjoy"
EURON = "euron-greyjoy"
AERON = "aeron-greyjoy"
ASHA = "asha-greyjoy"
VICTARION = "victarion-greyjoy"
SAWANE = "sawane-botley"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified)
EDGES_SPEC = [
    # --- causal spine (Tier-2, pending verify) ---
    (BALON_DEATH, "TRIGGERS", SEIZE, 2, "affc", "affc-the-prophet-01", 119,
     "He sailed into Lordsport the day after the king's death, and claimed the castle and the crown as Balon's eldest brother.",
     "Balon's death is the immediate specific spark: Euron, exiled by Balon on pain of death, sails in to seize Pyke and the Seastone Chair \"the day after the king's death\" -- the death lifts the only bar to his return with no mediation. => TRIGGERS Tier-2.",
     PENDING),
    (SEIZE, "CAUSES", KINGSMOOT, 2, "affc", "affc-the-prophet-01", 213,
     "Point your prow toward Old Wyk, where stood the Grey King's Hall. In the name of the Drowned God I summon you. I summon all of you! ... return to Nagga's hill to make a kingsmoot!",
     "Euron's godless usurpation of the chair is what drives Aeron Damphair, who deems him unworthy (\"Only a godly man may sit the Seastone Chair\"), to summon the first kingsmoot in millennia to deny him. Mediated by Aeron's religious judgment and decision => CAUSES Tier-2.",
     PENDING),
    (KINGSMOOT, "CAUSES", SHIELDS, 2, "affc", "affc-the-reaver-01", 77,
     "Euron is the king. Your kingsmoot raised him up, and you put the driftwood crown upon his head yourself!",
     "The kingsmoot legitimizes Euron's kingship and gives him command of the Iron Fleet; as king he immediately launches the conquest he promised at the moot, opening with the surprise attack on the Shield Islands. Without the moot's mandate the ironborn would not have followed him to the Reach. Mediated => CAUSES Tier-2.",
     PENDING),
    # --- agency (Tier-2, pending verify) ---
    (SEIZE, "MOTIVATES", AERON, 2, "affc", "affc-the-prophet-01", 209,
     "I was not made to sit upon the Seastone Chair . . . no more than Euron Crow's Eye. For I have heard the god, who says, No godless man may sit my Seastone Chair!",
     "Euron's seizure of the chair is the act that mobilizes Aeron the priest: his vow that no godless man may sit the Seastone Chair is the religious motive that makes him summon the kingsmoot. Event -> actor => MOTIVATES Tier-2 (distinct from the seizure->kingsmoot CAUSES edge: this carries Aeron's personal agency).",
     PENDING),
    # --- role edges (Tier-1), beat 1: death-of-balon-greyjoy ---
    (BALON, "VICTIM_IN", BALON_DEATH, 1, "affc", "affc-the-prophet-01", 69,
     "His Grace was crossing a bridge at Pyke when he fell and was dashed upon the rocks below.",
     "Balon Greyjoy is the subject who dies in the fall. Role edge => VICTIM_IN Tier-1.",
     None),
    # --- role edges (Tier-1), beat 2: euron-seizes-the-seastone-chair ---
    (EURON, "AGENT_IN", SEIZE, 1, "affc", "affc-the-prophet-01", 119,
     "He sailed into Lordsport the day after the king's death, and claimed the castle and the crown as Balon's eldest brother.",
     "Euron is the actor who sails in, claims Pyke and the Seastone Chair, and summons homage. Role edge => AGENT_IN Tier-1.",
     None),
    (SAWANE, "VICTIM_IN", SEIZE, 1, "affc", "affc-the-prophet-01", 141,
     "He had Sawane Botley drowned for saying that the Seastone Chair by rights belonged to Theon.",
     "Lord Sawane Botley is drowned by Euron for objecting to the seizure on Theon's behalf. Role edge => VICTIM_IN Tier-1.",
     None),
    # --- role edges (Tier-1), beat 3: kingsmoot-on-old-wyk ---
    (EURON, "AGENT_IN", KINGSMOOT, 1, "affc", "affc-the-drowned-man-01", 195,
     "\"EURON! EURON! CROW'S EYE! EURON KING!\" The cry swelled, became a roar.",
     "Euron wins the kingsmoot and is acclaimed king. Role edge => AGENT_IN Tier-1 (the chosen king).",
     None),
    (AERON, "AGENT_IN", KINGSMOOT, 1, "affc", "affc-the-prophet-01", 213,
     "In the name of the Drowned God I summon you. I summon all of you! ... return to Nagga's hill to make a kingsmoot!",
     "Aeron Damphair calls the kingsmoot and (per affc-the-reaver-01:77) sets the driftwood crown on the winner's head -- the convener and officiant. Role edge => AGENT_IN Tier-1.",
     None),
    (ASHA, "AGENT_IN", KINGSMOOT, 1, "affc", "affc-the-drowned-man-01", 177,
     "\"Crow's Eye,\" Asha called, \"did you leave your wits at Asshai? If we cannot hold the north—and we cannot—how can we win the whole of the Seven Kingdoms?\"",
     "Asha Greyjoy is a rival claimant who contests Euron's claim at the moot. Role edge => AGENT_IN Tier-1.",
     None),
    (VICTARION, "AGENT_IN", KINGSMOOT, 1, "affc", "affc-the-drowned-man-01", 181,
     "\"Aegon?\" Victarion crossed his arms against his armored chest. \"What has the Conqueror to do with us?\"",
     "Victarion Greyjoy is a rival claimant (offering to finish Balon's war) who contends at the moot. Role edge => AGENT_IN Tier-1.",
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
