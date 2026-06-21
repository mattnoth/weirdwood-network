#!/usr/bin/env python3
"""Mint the S116 ENRICHMENT pass on the Kingsmoot -> Euron cluster.

This is the second pass on an already-spine-built arc (the "spine -> enrich"
cadence, smoke-tested S116). It adds the braided side-plots that occur WITHIN the
arc but were not on the causal spine: Asha's doomed claim, Aeron's resistance vow,
the Victarion revelation's agency link, and the (unproven) Balon-murder suspicion.

New beat-nodes (written as .node.md, not here):
  - asha-claims-the-kingsmoot                    (event.incident; AFFC The Drowned Man I)
  - aeron-vows-to-raise-the-ironborn-smallfolk   (event.incident; AFFC The Reaver I)

Edges:
  asha-claims-the-kingsmoot --SUB_BEAT_OF--> kingsmoot-on-old-wyk           (Tier-1 structural)
  asha-greyjoy --AGENT_IN--> asha-claims-the-kingsmoot                       (Tier-1 role)
  kingsmoot-on-old-wyk --CAUSES--> aeron-vows-to-raise-the-ironborn-smallfolk (Tier-2, pending)
  aeron-greyjoy --AGENT_IN--> aeron-vows-to-raise-the-ironborn-smallfolk      (Tier-1 role)
  victarion-admits-euron-s-role-in-his-wife-s-death --MOTIVATES--> victarion-greyjoy (Tier-2, pending)
  euron-greyjoy --SUSPECTED_OF--> death-of-balon-greyjoy                     (Tier-2, pending)

The SUSPECTED_OF edge is the FIRST instance of a new edge type (architecture.md
Causal & Plot, S116): models the Euron-killed-Balon suspicion WITHOUT asserting it
as fact (published canon leaves it speculation; Euron's confession is in the TWOW
preview "The Forsaken", which we hold only as a wiki summary). Node stays event.death.

DEFERRED to the Essos/ADWD container (forward-dangling, would stub into a void now):
  - euron-weds-asha-to-erik-ironmaker-in-absentia  (learned in ADWD "The Wayward Bride")
  - euron-commissions-victarion-to-fetch-daenerys  (AFFC seed -> ADWD/Essos payoff)
These attach cleanly in a SECOND Kingsmoot enrichment pass once the Essos spine exists.

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-kingsmoot-enrichment-2026-06-20.jsonl"

RUN_ID = "causal-arc-kingsmoot-enrichment-20260620"
PRODUCED_AT = "2026-06-20T00:00:00+00:00"
PENDING = "pending-s116-kingsmoot-enrichment-verify"
COMMON = {
    "decision": "emit_edge",
    "candidate_kind": "causal-curator-arc",
    "evidence_kind": "book-pass1",
    "typed_by": "curator-causal-arc",
    "schema_version": "pass1-derived-v1",
    "produced_at": PRODUCED_AT,
    "run_id": RUN_ID,
}

ASHA_CLAIMS = "asha-claims-the-kingsmoot"
AERON_VOWS = "aeron-vows-to-raise-the-ironborn-smallfolk"
KINGSMOOT = "kingsmoot-on-old-wyk"
ASHA = "asha-greyjoy"
AERON = "aeron-greyjoy"
VIC_ADMITS = "victarion-admits-euron-s-role-in-his-wife-s-death"
VICTARION = "victarion-greyjoy"
EURON = "euron-greyjoy"
BALON_DEATH = "death-of-balon-greyjoy"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified)
EDGES_SPEC = [
    (ASHA_CLAIMS, "SUB_BEAT_OF", KINGSMOOT, 1, "affc", "affc-the-drowned-man-01", 107,
     "But it was not Euron who put an end to the shouting, it was the woman. ... \"Nuncle! Nuncle!\" Bending, she snatched up a twisted golden collar and bounded up the steps.",
     "Asha's claim is a discrete beat within the kingsmoot assembly. Structural composition => SUB_BEAT_OF Tier-1.",
     None),
    (ASHA, "AGENT_IN", ASHA_CLAIMS, 1, "affc", "affc-the-drowned-man-01", 113,
     "\"Ah, but my claim is better still.\" Asha set the collar on her head at a jaunty angle ... \"Balon's brother cannot come before Balon's son!\"",
     "Asha is the actor staking the claim. Role edge => AGENT_IN Tier-1.",
     None),
    (KINGSMOOT, "CAUSES", AERON_VOWS, 2, "affc", "affc-the-reaver-01", 87,
     "\"Not mine,\" the priest declared. ... \"If you will not bestir yourself to remove the Crow's Eye from the Seastone Chair, I must take the task upon myself.\"",
     "Euron's victory at the kingsmoot is what drives Aeron, who crowned him but deems him godless, to vow a smallfolk uprising against the new king. Mediated by Aeron's refusal-and-decision => CAUSES Tier-2.",
     PENDING),
    (AERON, "AGENT_IN", AERON_VOWS, 1, "affc", "affc-the-reaver-01", 95,
     "\"The ironborn shall be waves,\" the Damphair said. \"Not the great and lordly, but the simple folk ... the common folk shall tear him down ...\"",
     "Aeron is the actor making the vow. Role edge => AGENT_IN Tier-1.",
     None),
    (VIC_ADMITS, "MOTIVATES", VICTARION, 2, "affc", "affc-the-iron-captain-01", 269,
     "He put a baby in her belly and made me do the killing. I would have killed him too, but Balon would have no kinslaying in his hall. He sent Euron into exile, never to return . . .",
     "The revelation event (Victarion admitting Euron fathered the child on his salt wife, forcing the killing) crystallizes the standing grudge that drives Victarion's posture at the kingsmoot and his later vulnerability to Euron's manipulation (\"He stole my wife and he stole my throne\", affc-the-reaver-01:57). Event -> actor => MOTIVATES Tier-2. The revelation occurs en route to the moot (\"Balon had commanded them not to speak of it, but Balon was dead\") — contemporaneous with the arc, not loose backstory.",
     PENDING),
    (EURON, "SUSPECTED_OF", BALON_DEATH, 2, "affc", "affc-the-iron-captain-01", 165,
     "You know his name as well as I. Three years you were gone from us, and yet Silence returns within a day of my lord father's death.",
     "Asha openly accuses Euron of murdering Balon (the timing of his return + the storm-portents); Euron offers a hollow alibi (a crew of mutes who cannot speak, affc-the-iron-captain-01:179). The published books leave this SPECULATION — never proven. Euron confesses to causing Balon's death only in the TWOW preview chapter \"The Forsaken\" (we hold this as a wiki summary, not primary text). Modeled as SUSPECTED_OF (NOT KILLS/AGENT_IN), capped Tier-2; the node stays event.death, NOT event.assassination. First instance of the SUSPECTED_OF type.",
     PENDING),
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

    n_causal = sum(1 for s in EDGES_SPEC if s[1] in ("CAUSES", "TRIGGERS", "MOTIVATES", "SUSPECTED_OF"))
    n_role = len(EDGES_SPEC) - n_causal
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} enrichment edges ({n_causal} causal/interpretive + {n_role} role/structural).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
