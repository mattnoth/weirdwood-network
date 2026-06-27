#!/usr/bin/env python3
"""Mint the ESSOS E3 "Daznak's Pit -> Drogon flees -> Dothraki sea" causal arc.

ESSOS container decomposition (working/essos-decomposition.md) juncture E3 — the
ADWD published terminus of Daenerys's arc. Three NET-NEW beat nodes were minted as
.md files alongside this script (drogon-returns-to-daznak-pit,
dany-mounts-drogon-and-flees-meereen, dany-lost-on-dothraki-sea). This script wires
the causal + role + sub-beat edges.

Built per the arc-mint machine. The causal types were ADJUDICATED by a fresh
read-only research+verify subagent (2026-06-21, working/session-results/
2026-06-21-essos-e3-research.md) BEFORE minting, and every evidence_ref line was
re-pinned against the actual chapter file by the orchestrator (0 drift found), so the
causal edges are stamped verified at mint time (no pending pass).

Causal spine (chain-as-arc, NO umbrella; Tier-2; verified at mint):
  wedding-of-hizdahr... --ENABLES--> drogon-returns-to-daznak-pit
  drogon-returns-to-daznak-pit --TRIGGERS--> dany-mounts-drogon-and-flees-meereen
  dany-mounts-drogon-and-flees-meereen --CAUSES--> dany-lost-on-dothraki-sea

ENABLES vs CAUSES on the wedding hinge: the wedding does NOT summon Drogon and is
not the mechanical cause of his descent. It is the political vehicle for the fighting-
pit reopening concession (Reznak: "it would be your wedding gift to Hizdahr"); Drogon's
descent over an open arena full of prey is his own autonomous choice. ENABLES correctly
captures the structural precondition without eliding the dragon's agency — same pattern
as E2's army-enablement waypoints. (NOTE: `--causal-chain` does NOT walk ENABLES, so the
chain reads as a segment break at the wedding hinge; that is correct, not a bug.)
TRIGGERS on drogon-returns->mount: Drogon's arrival is the precipitating spark; Dany's
mount still requires her several acts of will (running in, taking the whip, subduing him).
CAUSES on mount->lost: direct mechanical consequence (the wild dragon bears her north
and refuses to return).

Role edges (Tier-1): daenerys-targaryen AGENT_IN + drogon AGENT_IN the mount/flight.
Sub-beat edges (Tier-3): the three existing dark Daznak nodes
(unnamed-spearman-attacks-drogon, hizdahr-orders-drogon-killed, drogon-kills-more-attackers)
become SUB_BEAT_OF drogon-returns-to-daznak-pit — all occur within the single continuous
descent incident.

ROOT: E3 roots at the BUILT E2 terminus `wedding-of-hizdahr...` via the ENABLES hinge.
TERMINUS: `dany-lost-on-dothraki-sea` — the ESSOS spine's hard-stop in the 5 published
books (no downstream causal edge into TWOW territory).

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-essos-e3-arc-2026-06-21.jsonl"

RUN_ID = "causal-arc-essos-e3-daznak-20260621"
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
WEDDING = "wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen"
RETURNS = "drogon-returns-to-daznak-pit"
MOUNTS = "dany-mounts-drogon-and-flees-meereen"
LOST = "dany-lost-on-dothraki-sea"
DANY = "daenerys-targaryen"
DROGON = "drogon"
SPEARMAN = "unnamed-spearman-attacks-drogon"
HIZDAHR_ORDERS = "hizdahr-orders-drogon-killed"
KILLS_MORE = "drogon-kills-more-attackers"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified-or-None)
EDGES_SPEC = [
    # --- causal spine (verified at mint) ---
    (WEDDING, "ENABLES", RETURNS, 2, "adwd", "adwd-daenerys-06", 139,
     "To celebrate your nuptials, it would be most fitting if you would allow the fighting pits to open once again. It would be your wedding gift to Hizdahr and to your loving people, a sign that you had embraced the ancient ways and customs of Meereen.",
     "The wedding does not summon Drogon; it is the political vehicle for the fighting-pit reopening concession (Reznak frames the reopening as the wedding gift). The reopened arena -- crowd, boar, spectacle -- is the structural precondition Drogon descends upon; his arrival is his own autonomous choice. Condition, not mechanical cause => ENABLES Tier-2 (same pattern as E2 army-enablement waypoints).",
     VERIFIED),
    (RETURNS, "TRIGGERS", MOUNTS, 2, "adwd", "adwd-daenerys-09", 241,
     "Dany and Drogon screamed as one.",
     "Drogon's arrival in the pit -- and the spearman wounding him -- is the precipitating spark for Dany running into the arena and mounting him. The mount still requires her several acts of will (taking the whip, subduing the dragon, vaulting on), so the descent does not mechanically PRODUCE the mount. Immediate spark => TRIGGERS Tier-2.",
     VERIFIED),
    (MOUNTS, "CAUSES", LOST, 2, "adwd", "adwd-daenerys-10", 55,
     "North they flew, beyond the river, Drogon gliding on torn and tattered wings through clouds that whipped by like the banners of some ghostly army. ... Then there was nothing beneath them but grass rippling in the wind.",
     "The flight is the direct mechanical consequence of the mount: the wild dragon bears her north, lands on the hill, and refuses to return -- no intervening choice breaks the link. CAUSES Tier-2.",
     VERIFIED),
    # --- role edges (Tier-1) ---
    (DANY, "AGENT_IN", MOUNTS, 1, "adwd", "adwd-daenerys-09", 265,
     "Daenerys Targaryen vaulted onto the dragon's back, seized the spear, and ripped it out.",
     "Daenerys is the primary actor: she runs into the pit, tames Drogon with the whip, and mounts him. Role edge => AGENT_IN Tier-1.",
     None),
    (DROGON, "AGENT_IN", MOUNTS, 1, "adwd", "adwd-daenerys-09", 265,
     "The black wings cracked like thunder, and suddenly the scarlet sands were falling away beneath her.",
     "Drogon is the co-agent who beats his wings and carries her out of the pit. Role edge => AGENT_IN Tier-1.",
     None),
    # --- sub-beat edges (Tier-3): existing dark Daznak nodes into the descent hub ---
    (SPEARMAN, "SUB_BEAT_OF", RETURNS, 3, "adwd", "adwd-daenerys-09", 239,
     "The hero leapt onto his back and drove the iron spearpoint down at the base of the dragon's long scaled neck.",
     "The unnamed spearman's attack is the precipitating beat within the Drogon-descent incident (he is one of the men sent to drive the boar back; he wounds the dragon instead). Structural composition => SUB_BEAT_OF Tier-3.",
     None),
    (HIZDAHR_ORDERS, "SUB_BEAT_OF", RETURNS, 3, "adwd", "adwd-daenerys-09", 245,
     "“Kill it,” Hizdahr zo Loraq shouted to the other spearmen. “Kill the beast!”",
     "Hizdahr's shout occurs during the chaos of Drogon's descent, after the dragon is already present and wounded. Beat within the incident => SUB_BEAT_OF Tier-3.",
     None),
    (KILLS_MORE, "SUB_BEAT_OF", RETURNS, 3, "adwd", "adwd-daenerys-09", 251,
     "As the other spears closed in, the dragon spat fire, bathing two men in black flame. His tail lashed sideways and caught the pitmaster creeping up behind him, breaking him in two.",
     "Drogon burning and breaking the attacking spearmen happens during the same continuous descent incident. Beat within the incident => SUB_BEAT_OF Tier-3.",
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

    n_causal = sum(1 for s in EDGES_SPEC if s[1] in ("ENABLES", "TRIGGERS", "CAUSES"))
    n_role = sum(1 for s in EDGES_SPEC if s[1] == "AGENT_IN")
    n_beat = sum(1 for s in EDGES_SPEC if s[1] == "SUB_BEAT_OF")
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges ({n_causal} causal Tier-2 verified, "
          f"{n_role} role Tier-1, {n_beat} sub-beat Tier-3).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
