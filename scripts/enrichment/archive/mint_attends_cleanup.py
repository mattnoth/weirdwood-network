#!/usr/bin/env python3
"""ATTENDS relation cleanup (S118) — the 7 edges routed out of the S117 ATTENDS re-audit.

These are NOT WITNESS_IN reclasses of the S117 batch — they were the leftover
mistargets / wrong-relation edges deferred to "a relation-cleanup pass". A fresh
Sonnet verifier (s118-attends-verify) read each cited passage against the LOCAL
chapter cache and adjudicated the final relation. Outcome:

  (1) cersei-lannister ATTENDS robert-baratheon(CHARACTER)
        -> PARTICIPATES_IN death-of-robert-baratheon(EVENT)
        retarget + retype. WITNESS_IN was REFUTED: Cersei sits the deathbed but
        Robert dismisses her ("leads the way to the door", agot-eddard-13:53)
        BEFORE he dies — Ned alone witnesses the death, so the text-anchor gate
        fails (present-but-shielded, the Arya-at-Ned's-execution precedent).
        PARTICIPATES_IN = non-combat presence of the queen at the death-event,
        and it fixes the character->event schema violation.

  (2) ghost-of-high-heart ATTENDS summerhall(PLACE)
        -> WITNESS_IN tragedy-at-summerhall(EVENT)
        retarget + retype. First-person testimony "I gorged on grief at Summerhall"
        => she personally survived/witnessed the charged event. tragedy-at-summerhall
        ALREADY EXISTS (graph/nodes/events/) — NO new node minted (the handoff's
        tragedy-of-summerhall would have been a duplicate; dedup-check caught it).

  (3-6) emmon-frey / edwyn-frey / desmond-grell / robin-ryger ATTENDS siege-of-riverrun
        -> PARTICIPATES_IN siege-of-riverrun (retype only).
        emmon=besieger principal (designated lord, no command), edwyn=Frey envoy,
        grell+ryger=garrison defenders. The AFFC siege resolved by SURRENDER — no
        combat in-text — so FIGHTS_IN/COMMANDS_IN are not warranted. GARRISONS is
        not in the locked vocab; PARTICIPATES_IN is the vocab-legal fit (besieger
        vs defender direction is preserved in asserted_relation).

  (7) jeyne-westerling ATTENDS siege-of-riverrun
        -> PARTICIPATES_IN siege-of-riverrun (retype only).
        Verifier CONFIRMED she was physically at Riverrun (Jaime summons + interviews
        her in Hoster's solar, affc-jaime-07) — so NOT dropped — but she was held
        under the Blackfish's PROTECTION as Robb's queen-widow, not confined.
        IMPRISONED_AT was REFUTED (overstates a protected high-status hostage);
        PARTICIPATES_IN = strategic non-combat principal.

No new nodes, no new edges, no new vocab types (WITNESS_IN/PARTICIPATES_IN both
already live). Edge COUNT is unchanged (22,342) — these are in-place retypes.
Edge-type tallies shift: ATTENDS -7, PARTICIPATES_IN +6, WITNESS_IN +1.

Re-run safe: matches the CURRENT ATTENDS row by (source_slug, OLD target_slug);
if already retyped (no ATTENDS row but the post-state row exists) it skips.
"""
import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-attends-cleanup-2026-06-21.jsonl"

RECLASS_BY = "curator-attends-reclass"

# Each change keys on the CURRENT row: (source_slug, old_target, "ATTENDS").
# new_type, new_target (None = unchanged), new_asserted (None = keep), note.
CHANGES = [
    {
        "source": "cersei-lannister", "old_target": "robert-baratheon",
        "new_type": "PARTICIPATES_IN", "new_target": "death-of-robert-baratheon",
        "new_asserted": "Cersei was present at Robert's deathbed as queen during his dying; "
                        "dismissed from the chamber before the moment of death (Ned alone witnesses it). "
                        "Non-combat presence at the death-event.",
        "note": "ATTENDS->PARTICIPATES_IN + retarget robert-baratheon(character)->death-of-robert-baratheon(event) "
                "(S118 ATTENDS-cleanup; WITNESS_IN refuted — dismissed before the death, text-anchor gate fails)",
    },
    {
        "source": "ghost-of-high-heart", "old_target": "summerhall",
        "new_type": "WITNESS_IN", "new_target": "tragedy-at-summerhall",
        "new_asserted": "The Ghost of High Heart personally survived/witnessed the Tragedy of Summerhall "
                        "(\"I gorged on grief at Summerhall\") — perceiver of the charged event.",
        "note": "ATTENDS->WITNESS_IN + retarget summerhall(place)->tragedy-at-summerhall(event) "
                "(S118 ATTENDS-cleanup; first-person testimony of presence; existing node, no mint)",
    },
    {
        "source": "emmon-frey", "old_target": "siege-of-riverrun",
        "new_type": "PARTICIPATES_IN", "new_target": None, "new_asserted": None,
        "note": "ATTENDS->PARTICIPATES_IN (S118 ATTENDS-cleanup: besieger principal/designated lord, "
                "non-combat; siege resolved by surrender, no FIGHTS_IN/COMMANDS_IN)",
    },
    {
        "source": "edwyn-frey", "old_target": "siege-of-riverrun",
        "new_type": "PARTICIPATES_IN", "new_target": None, "new_asserted": None,
        "note": "ATTENDS->PARTICIPATES_IN (S118 ATTENDS-cleanup: Frey envoy/representative at the siege "
                "council, non-combat; no troop command in-scene)",
    },
    {
        "source": "desmond-grell", "old_target": "siege-of-riverrun",
        "new_type": "PARTICIPATES_IN", "new_target": None, "new_asserted": None,
        "note": "ATTENDS->PARTICIPATES_IN (S118 ATTENDS-cleanup: Riverrun garrison defender; "
                "siege ended by surrender, no combat -> not FIGHTS_IN)",
    },
    {
        "source": "robin-ryger", "old_target": "siege-of-riverrun",
        "new_type": "PARTICIPATES_IN", "new_target": None, "new_asserted": None,
        "note": "ATTENDS->PARTICIPATES_IN (S118 ATTENDS-cleanup: Riverrun captain of guards/garrison "
                "defender; siege ended by surrender, no combat -> not FIGHTS_IN)",
    },
    {
        "source": "jeyne-westerling", "old_target": "siege-of-riverrun",
        "new_type": "PARTICIPATES_IN", "new_target": None,
        "new_asserted": "Jeyne Westerling was physically present at Riverrun throughout the siege, held "
                        "under the Blackfish's protection as Robb's queen-widow (a strategic non-combat "
                        "stake); released to travel west at the surrender.",
        "note": "ATTENDS->PARTICIPATES_IN (S118 ATTENDS-cleanup: present under protection, not confinement; "
                "IMPRISONED_AT refuted — overstates a protected high-status hostage)",
    },
]


def main():
    lines = EDGES.read_text().splitlines()
    rows = [json.loads(ln) for ln in lines if ln.strip()]

    applied, skipped = [], []
    for ch in CHANGES:
        src, old_tgt = ch["source"], ch["old_target"]
        new_type, new_tgt = ch["new_type"], ch["new_target"]
        eff_new_tgt = new_tgt or old_tgt

        # find current ATTENDS row
        idx = next((i for i, r in enumerate(rows)
                    if r.get("source_slug") == src
                    and r.get("target_slug") == old_tgt
                    and r.get("edge_type") == "ATTENDS"), None)
        if idx is None:
            # already applied?
            done = any(r.get("source_slug") == src
                       and r.get("target_slug") == eff_new_tgt
                       and r.get("edge_type") == new_type for r in rows)
            skipped.append((src, old_tgt, "already-applied" if done else "NOT-FOUND"))
            continue

        r = rows[idx]
        r["edge_type"] = new_type
        if new_tgt:
            r["target_slug"] = new_tgt
        if ch["new_asserted"]:
            r["asserted_relation"] = ch["new_asserted"]
        r["typed_by"] = RECLASS_BY
        r["reclass_note"] = ch["note"]
        applied.append((src, old_tgt, f"{new_type} {eff_new_tgt}"))

    if not applied:
        print("No changes applied (all skipped):")
        for s in skipped:
            print("  SKIP", s)
        return

    # backup once (don't clobber an existing backup)
    if not BACKUP.exists():
        shutil.copy2(EDGES, BACKUP)
        print(f"backup -> {BACKUP.relative_to(REPO)}")
    else:
        print(f"backup already exists -> {BACKUP.relative_to(REPO)} (not overwritten)")

    with EDGES.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\napplied {len(applied)} retypes:")
    for a in applied:
        print("  ", a)
    if skipped:
        print("skipped:")
        for s in skipped:
            print("  ", s)


if __name__ == "__main__":
    main()
