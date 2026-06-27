#!/usr/bin/env python3
"""Mint Red Wedding enrichment pass 1 (S134) — second major-arc enrichment dip.

Synthesis of 4 fresh Sonnet lenses (downstream-causal / secondary-char+witness /
descriptive-depth / NEW existing-node↔existing-node causal-wiring) over the built
Red Wedding cluster. PROPOSE-only lenses → orchestrator synthesized + line-checked
every cite → this mint set.

Mints:
  - 2 new event.incident nodes:
      grey-wind-killed-at-the-twins
      edmure-taken-hostage-at-the-twins
  - 23 edges:
      6 causal/cross-arc (verified=pending → fresh-verify):
        the-rains-of-castamere TRIGGERS red-wedding
        ser-wendel-manderly-is-killed MOTIVATES wyman-manderly-stages-fake-execution-of-davos
        roose-named-warden-of-the-north ENABLES wedding-of-ramsay-bolton-and-arya-stark
        roose-named-warden-of-the-north MOTIVATES stannis-march-on-winterfell
        red-wedding ENABLES siege-of-riverrun
        edmure-taken-hostage-at-the-twins ENABLES siege-of-riverrun
      10 role edges on existing beats/hub
      7 role/structural edges for the 2 new nodes

Rejected at synthesis (logged, not minted):
  - blackfish-escapes-the-twins NODE — factually wrong (the Blackfish held Riverrun;
    he was never at the Twins; Tywin confirms he is at Riverrun, asos-tyrion-06:53).
  - red-wedding CAUSES guest-right(concept) — novel event→concept pattern; done as ATTACH_QUOTE instead.
  - roslin-frey SUSPECTED_OF red-wedding-conspiracy — overclaims a coerced victim's agency.
  - arya-stark WITNESS_IN grey-wind-attacks — warg-howl perception fails the visual-sight gate.
  - robb-is-killed MOTIVATES kill-list — wrong node instance (kill-list predates the RW).

Safeguards mirror mint_rr_enrichment_s133.py: backup, re-run guard, slug pre-check.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-red-wedding-enrichment-2026-06-23.jsonl"
NODES_EVENTS = REPO / "graph" / "nodes" / "events"

RUN_ID = "red-wedding-enrichment-s134"
PRODUCED_AT = "2026-06-23T00:00:00+00:00"

NEW_NODE_SLUGS = {
    "grey-wind-killed-at-the-twins",
    "edmure-taken-hostage-at-the-twins",
}


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-rw-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


# (source, edge_type, target, tier, book, chap_id, line, quote, asserted, verified_or_None)
EDGES_SPEC = [
    # ════════ CAUSAL / CROSS-ARC (6) — verified=pending → fresh-verify ════════
    ("the-rains-of-castamere", "TRIGGERS", "red-wedding", 1,
     "asos", "asos-catelyn-07", 99,
     "No one sang the words, but Catelyn knew “The Rains of Castamere” when she heard it.",
     "The Rains of Castamere was the pre-arranged massacre signal — the moment the players "
     "in the gallery struck it up, the crossbowmen revealed themselves and the slaughter began "
     "(the first quarrel sprouts from Robb seconds later, :103).",
     "pending"),
    ("ser-wendel-manderly-is-killed", "MOTIVATES", "wyman-manderly-stages-fake-execution-of-davos", 1,
     "adwd", "adwd-davos-04", 125,
     "My son Wendel came to the Twins a guest. He ate Lord Walder’s bread and salt, and hung "
     "his sword upon the wall to feast with friends. And they murdered him. … The north remembers, "
     "Lord Davos. The north remembers, and the mummer’s farce is almost done.",
     "Wendel Manderly's murder at the Red Wedding is the explicit motive Wyman names for his "
     "covert anti-Frey revenge — the staged Davos execution is part of that 'mummer's farce.'",
     "pending"),
    ("roose-named-warden-of-the-north", "ENABLES", "wedding-of-ramsay-bolton-and-arya-stark", 1,
     "adwd", "adwd-the-prince-of-winterfell-01", 127,
     "In her children our two ancient houses will become as one, he said, and the long enmity "
     "between Stark and Bolton will be ended.",
     "Roose's Wardenship (the RW's reward) is the political scaffold that makes the fArya-Stark "
     "marriage the instrument of Bolton's consolidation of the North.",
     "pending"),
    ("roose-named-warden-of-the-north", "MOTIVATES", "stannis-march-on-winterfell", 1,
     "adwd", "adwd-the-kings-prize-01", 69,
     "Roose Bolton is feared, but little loved. And his friends the Freys … the north has not "
     "forgotten the Red Wedding. … Stannis need only bloody Bolton, and the northmen will abandon him.",
     "Stannis marches to dislodge the Bolton regime that the RW elevated; the northern resentment of "
     "Bolton-as-Warden is both his motive and his opening.",
     "pending"),
    ("red-wedding", "ENABLES", "siege-of-riverrun", 1,
     "affc", "affc-jaime-06", 89,
     "Harrenhal has fallen. Seagard and Maidenpool. … Piper, Vance, Mooton, all your bannermen "
     "have yielded. Only Riverrun remains.",
     "The Red Wedding annihilated Robb's host and command structure, isolating Riverrun as the last "
     "Tully holdout — which is what made the later siege viable (cf. Tywin, asos-tyrion-06:53).",
     "pending"),
    ("edmure-taken-hostage-at-the-twins", "ENABLES", "siege-of-riverrun", 1,
     "asos", "asos-tyrion-06", 53,
     "Riverrun remains, but so long as Walder Frey holds Edmure Tully hostage, the Blackfish dare "
     "not mount a threat.",
     "Edmure's captivity (taken at the Twins) is the lever that neutralizes the Blackfish, enabling "
     "the siege to proceed to surrender — Tywin names the mechanism explicitly.",
     "pending"),

    # ════════ ROLE EDGES on existing beats/hub (10) ════════
    ("lothar-frey", "AGENT_IN", "red-wedding-conspiracy", 1,
     "asos", "asos-epilogue", 31,
     "it had been Lame Lothar who had plotted it out with Roose Bolton, all the way down to which "
     "songs would be played.",
     "Lame Lothar Frey was the operational architect of the Red Wedding conspiracy — he plotted it "
     "with Roose Bolton.",
     None),
    ("lothar-frey", "COMMANDS_IN", "red-wedding", 1,
     "asos", "asos-epilogue", 165,
     "Lothar rigged the tents to collapse and put the crossbowmen in the gallery with the musicians",
     "Lothar Frey directed the two key tactical preparations of the massacre — the collapsing tents "
     "and the crossbow gallery.",
     None),
    ("catelyn-stark", "WITNESS_IN", "robb-is-killed", 1,
     "asos", "asos-catelyn-07", 135,
     "A man in dark armor and a pale pink cloak spotted with blood stepped up to Robb. “Jaime "
     "Lannister sends his regards.” He thrust his longsword through her son’s heart, and twisted.",
     "Catelyn (the POV) watches Roose Bolton deliver the killing blow to Robb — the chapter's "
     "central witnessed moment.",
     None),
    ("jon-umber-son-of-jon", "AGENT_IN", "robb-is-killed", 1,
     "asos", "asos-catelyn-07", 103,
     "She saw Smalljon Umber wrestle a table off its trestles. Crossbow bolts thudded into the wood, "
     "one two three, as he flung it down on top of his king.",
     "The Smalljon shields Robb with a table against the crossbow volley — an agent (defender) in "
     "the kill beat.",
     None),
    ("jon-umber", "VICTIM_IN", "red-wedding", 1,
     "asos", "asos-epilogue", 47,
     "It had taken eight of them to get him into chains, and the effort had left two men wounded, one "
     "dead … When he couldn’t fight with his hands any longer, Umber had fought with his teeth.",
     "The Greatjon was overpowered and captured (not killed) at the Red Wedding after fighting eight "
     "men into chains.",
     None),
    ("merrett-frey", "ATTENDS", "red-wedding", 1,
     "asos", "asos-epilogue", 45,
     "Lame Lothar had summoned him to discuss his role in Roslin’s wedding.",
     "Merrett Frey was present at the Red Wedding with an assigned role.",
     None),
    ("merrett-frey", "AGENT_IN", "red-wedding-conspiracy", 2,
     "asos", "asos-epilogue", 45,
     "You shall have one task and one task only, Merrett … I want you to see to it that Greatjon "
     "Umber is so bloody drunk that he can hardly stand, let alone fight.",
     "Merrett was assigned a conspiracy sub-task — incapacitating the Greatjon with drink (Tier-2: a "
     "minor, knowingly-assigned role he attempted and failed).",
     None),
    ("edwyn-frey", "AGENT_IN", "red-wedding", 1,
     "asos", "asos-catelyn-07", 99,
     "She grabbed Edwyn by the arm to turn him and went cold all over when she felt the iron rings "
     "beneath his silken sleeve.",
     "Edwyn Frey wore concealed mail and was moving to clear the hall as the signal struck — an agent "
     "in the massacre's opening.",
     None),
    ("arya-stark", "WITNESS_IN", "the-camp-becomes-a-battlefield", 1,
     "asos", "asos-arya-11", 21,
     "she saw that there were only two of the huge feast tents where once there had been three. The "
     "one in the middle had collapsed. … A flight of fire arrows streaked through the air.",
     "Arya, outside the Twins, is the only on-page witness to the camp slaughter — she sees the tents "
     "collapse and burn and the riders ride men down.",
     None),
    ("walder-rivers", "AGENT_IN", "the-camp-becomes-a-battlefield", 1,
     "asos", "asos-epilogue", 165,
     "Bastard Walder led the attack on the camps",
     "Walder Rivers ('Bastard Walder') commanded the assault on the soldiers' camp outside the Twins.",
     None),

    # ════════ NEW-NODE role/structural edges (7) ════════
    ("grey-wind", "VICTIM_IN", "grey-wind-killed-at-the-twins", 1,
     "asos", "asos-epilogue", 161,
     "Stark’s direwolf killed four of our wolfhounds and tore the kennelmaster’s arm off his "
     "shoulder, even after we’d filled him full of quarrels",
     "Grey Wind was shot full of crossbow quarrels and killed during the Red Wedding.",
     None),
    ("house-frey", "AGENT_IN", "grey-wind-killed-at-the-twins", 1,
     "asos", "asos-epilogue", 161,
     "even after we’d filled him full of quarrels",
     "Frey men killed Grey Wind with crossbows during the massacre.",
     None),
    ("grey-wind-killed-at-the-twins", "SUB_BEAT_OF", "red-wedding", 1,
     "asos", "asos-epilogue", 163,
     "So you sewed his head on Robb Stark’s neck after both o’ them were dead",
     "The killing and desecration of Grey Wind is a distinct beat of the Red Wedding.",
     None),
    ("edmure-tully", "VICTIM_IN", "edmure-taken-hostage-at-the-twins", 1,
     "asos", "asos-tyrion-06", 53,
     "so long as Walder Frey holds Edmure Tully hostage, the Blackfish dare not mount a threat.",
     "Edmure Tully was taken captive at the Twins and held hostage by Walder Frey.",
     None),
    ("walder-frey", "AGENT_IN", "edmure-taken-hostage-at-the-twins", 1,
     "asos", "asos-tyrion-06", 53,
     "so long as Walder Frey holds Edmure Tully hostage",
     "Walder Frey took and held Edmure Tully as hostage.",
     None),
    ("house-frey", "AGENT_IN", "edmure-taken-hostage-at-the-twins", 1,
     "asos", "asos-tyrion-06", 53,
     "Walder Frey holds Edmure Tully hostage",
     "House Frey took Edmure captive at the Twins.",
     None),
    ("edmure-taken-hostage-at-the-twins", "SUB_BEAT_OF", "red-wedding", 1,
     "asos", "asos-catelyn-07", 119,
     "Keep me for a hostage, Edmure as well if you haven’t killed him.",
     "Edmure's capture is a beat of the Red Wedding (Catelyn's plea names him as a hostage target).",
     None),
]

# ── Node bodies ───────────────────────────────────────────────────────────────

GREY_WIND_KILLED_NODE = """\
---
name: "Grey Wind killed at the Twins"
type: event.incident
slug: grey-wind-killed-at-the-twins
aliases: ["death of Grey Wind", "killing of Grey Wind", "Grey Wind's head sewn on Robb"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s134-rw-enrich
node_version: 1
evidence_chapters:
  - ASOS Catelyn VII
  - ASOS Arya XI
  - ASOS Epilogue
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

During the Red Wedding, [Robb Stark](robb-stark)'s direwolf [Grey Wind](grey-wind) — penned away from the hall on Lord Walder's pretext — was shot full of crossbow quarrels by Frey men after he killed four of their wolfhounds and tore the kennelmaster's arm off. In the massacre's most infamous desecration, the Freys then sewed Grey Wind's severed head onto Robb's headless corpse and paraded it. [Arya Stark](arya-stark), outside the walls, hears his death-howl "sharp with rage and grief" through her latent warg-bond. A distinct beat of the [Red Wedding](red-wedding).

## Edges

(Role/structural edges live in `graph/edges/edges.jsonl`, S134 RW enrichment. [Grey Wind](grey-wind) VICTIM_IN (Tier-1); [House Frey](house-frey) AGENT_IN (Tier-1); SUB_BEAT_OF [Red Wedding](red-wedding) (Tier-1).)

## Quotes

> "Stark's direwolf killed four of our wolfhounds and tore the kennelmaster's arm off his shoulder, even after we'd filled him full of quarrels . . ." / "So you sewed his head on Robb Stark's neck after both o' them were dead," said yellow cloak.

— ASOS Epilogue (`sources/chapters/asos/asos-epilogue.md:161-163`)
"""

EDMURE_HOSTAGE_NODE = """\
---
name: "Edmure taken hostage at the Twins"
type: event.incident
slug: edmure-taken-hostage-at-the-twins
aliases: ["capture of Edmure Tully", "Edmure taken captive at the Twins", "Edmure Tully held hostage"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s134-rw-enrich
node_version: 1
evidence_chapters:
  - ASOS Catelyn VII
  - ASOS Tyrion VI
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

[Edmure Tully](edmure-tully) — the bridegroom whose wedding to [Roslin Frey](roslin-frey) was the bait for the Red Wedding — was taken captive rather than killed during the massacre and held hostage by [Walder Frey](walder-frey). His captivity became the lever that paralysed the Tully war effort: as [Tywin Lannister](tywin-lannister) notes, "so long as Walder Frey holds Edmure Tully hostage, the Blackfish dare not mount a threat." Edmure's hostage status is what later ENABLES the [siege of Riverrun](siege-of-riverrun) to end in surrender. A beat of the [Red Wedding](red-wedding).

## Edges

(Role/causal edges live in `graph/edges/edges.jsonl`, S134 RW enrichment. [Edmure Tully](edmure-tully) VICTIM_IN (Tier-1); [Walder Frey](walder-frey) AGENT_IN + [House Frey](house-frey) AGENT_IN (Tier-1); SUB_BEAT_OF [Red Wedding](red-wedding) (Tier-1); ENABLES [siege-of-riverrun](siege-of-riverrun) (Tier-1, fresh-verify).)

## Quotes

> "Riverrun remains, but so long as Walder Frey holds Edmure Tully hostage, the Blackfish dare not mount a threat."

— Tywin Lannister, ASOS Tyrion VI (`sources/chapters/asos/asos-tyrion-06.md:53`)
"""

NODES = [
    ("grey-wind-killed-at-the-twins", GREY_WIND_KILLED_NODE),
    ("edmure-taken-hostage-at-the-twins", EDMURE_HOSTAGE_NODE),
]


def make_edge_row(spec):
    (src, etype, tgt, tier, book, chap_id, line, quote, asserted, verified) = spec
    row = {
        "edge_type": etype,
        "source_slug": src,
        "target_slug": tgt,
        **common(),
        "evidence_book": book,
        "evidence_chapter": chap_id,
        "evidence_ref": f"sources/chapters/{book}/{chap_id}.md:{line}",
        "evidence_quote": quote,
        "confidence_tier": tier,
        "asserted_relation": asserted,
    }
    if verified is not None:
        row["verified_by"] = verified
    return row


def main():
    all_slugs = set()
    for (src, _, tgt, *_rest) in EDGES_SPEC:
        all_slugs.add(src)
        all_slugs.add(tgt)
    check_slugs = all_slugs - NEW_NODE_SLUGS
    resolved, missing = precheck_slugs(check_slugs)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed — non-existent targets: {missing}")
    print(f"Slug pre-check OK: {len(resolved)} existing slugs resolved.")

    raw_lines = EDGES.read_text(encoding="utf-8").splitlines()
    existing_lines = [ln for ln in raw_lines if ln.strip()]
    if any(RUN_ID in ln for ln in existing_lines):
        sys.exit(f"ABORT: run_id '{RUN_ID}' already present — already minted.")
    print(f"Re-run guard OK: run_id '{RUN_ID}' not present.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)
    print(f"Backup written → {BACKUP}")

    nodes_created = []
    for slug, body in NODES:
        node_path = NODES_EVENTS / f"{slug}.node.md"
        if node_path.exists():
            print(f"  SKIP node (already exists): {node_path.name}")
        else:
            node_path.write_text(body, encoding="utf-8")
            nodes_created.append(slug)
            print(f"  Created node: {node_path.name}")

    new_rows = [make_edge_row(spec) for spec in EDGES_SPEC]
    lines_before = len(existing_lines)
    all_out = existing_lines + [json.dumps(r, ensure_ascii=False) for r in new_rows]
    EDGES.write_text("\n".join(all_out) + "\n", encoding="utf-8")
    lines_after = len(all_out)

    type_counts = {}
    for spec in EDGES_SPEC:
        type_counts[spec[1]] = type_counts.get(spec[1], 0) + 1

    print("\n── SUMMARY ──")
    print(f"Nodes created ({len(nodes_created)}): {', '.join(nodes_created)}")
    print(f"Edges appended ({len(new_rows)}):")
    for etype, cnt in sorted(type_counts.items()):
        print(f"  {etype}: {cnt}")
    print(f"edges.jsonl: {lines_before} → {lines_after} lines (+{len(new_rows)})")
    print(f"Backup: {BACKUP}")


if __name__ == "__main__":
    main()
