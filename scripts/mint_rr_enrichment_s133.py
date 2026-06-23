#!/usr/bin/env python3
"""Mint Robert's Rebellion enrichment pass 1 (S133).

Mints:
  - 3 new event.incident nodes:
      knight-of-the-laughing-tree-incident
      exile-of-jon-connington
      murder-of-jon-arryn
  - 23 edges (E1–E23) per synthesis.md locked mint set
  - 1 edge DROP: roberts-rebellion GUEST_OF winterfell (junk row)

Source of truth: working/enrichment/rr/synthesis.md
Template: graph/nodes/events/euron-commissions-victarion-to-fetch-daenerys.node.md

Safeguards:
  1. Backs up edges.jsonl before any write.
  2. Re-run guard: aborts if run_id already present.
  3. Slug pre-check: aborts if any non-new slug is missing.
  4. Drops the GUEST_OF junk row on rewrite.
  5. Prints summary + counts.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-rr-enrichment-2026-06-22.jsonl"
NODES_EVENTS = REPO / "graph" / "nodes" / "events"

RUN_ID = "rr-enrichment-s133"
PRODUCED_AT = "2026-06-22T00:00:00+00:00"

# ── 3 New node slugs (created in this run; excluded from missing-abort) ──────
NEW_NODE_SLUGS = {
    "knight-of-the-laughing-tree-incident",
    "exile-of-jon-connington",
    "murder-of-jon-arryn",
}

# ── DROP spec ────────────────────────────────────────────────────────────────
DROP_EDGE_TYPE = "GUEST_OF"
DROP_SOURCE = "roberts-rebellion"
DROP_TARGET = "winterfell"


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "causal-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-causal-arc",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


# Each tuple: (source_slug, edge_type, target_slug, tier, book, chapter_id, line,
#              quote, asserted_relation, verified_by_or_None)
# verified_by="pending" → causal/enabling edges (CAUSES, ENABLES, SUSPECTED_OF)
# verified_by=None       → role/structural edges (AGENT_IN, VICTIM_IN, COMMANDS_IN,
#                          WITNESS_IN, FIGHTS_IN, SUB_BEAT_OF)
EDGES_SPEC = [
    # ── Causal / structural (5) ────────────────────────────────────────────
    # E1
    ("battle-of-the-bells", "CAUSES", "exile-of-jon-connington", 1,
     "adwd", "adwd-the-griffin-reborn-01", 57,
     "After the Battle of the Bells, when Aerys Targaryen had stripped him of his titles "
     "and sent him into exile in a mad fit of ingratitude and suspicion",
     "Connington's defeat at the Battle of the Bells caused Aerys to strip and exile him.",
     "pending"),
    # E2
    ("exile-of-jon-connington", "ENABLES", "aegon-revealed-to-the-golden-company", 1,
     "adwd", "adwd-the-griffin-reborn-01", 71,
     "I failed the father, he said, but I will not fail the son.",
     "Connington's exile and subsequent joining of the Golden Company enabled the later "
     "reveal of Young Griff as Aegon Targaryen.",
     "pending"),
    # E3
    ("coronation-of-robert-i-baratheon", "ENABLES",
     "wedding-of-robert-i-baratheon-and-cersei-lannister", 1,
     "agot", "agot-eddard-07", 101,
     "I had no wish to marry after Lyanna was taken from me, but Jon said the realm needed "
     "an heir. Cersei Lannister would be a good match, he told me, she would bind Lord Tywin "
     "to me should Viserys Targaryen ever try to win back his father's throne",
     "Robert's coronation and new kingship made the Cersei-Lannister match politically "
     "necessary, enabling the marriage.",
     "pending"),
    # E4
    ("wedding-of-robert-i-baratheon-and-cersei-lannister", "ENABLES",
     "death-of-robert-baratheon", 2,
     "agot", "agot-eddard-07", 101,
     "Cersei Lannister would be a good match, he told me, she would bind Lord Tywin to me "
     "should Viserys Targaryen ever try to win back his father's throne",
     "Robert's marriage to Cersei placed her at court; her later role in the boar-hunt "
     "wine manipulation was the distal enabler of his death.",
     "pending"),
    # E5
    ("knight-of-the-laughing-tree-incident", "SUB_BEAT_OF", "tourney-at-harrenhal", 1,
     "asos", "asos-bran-02", 179,
     "The little crannogman was walking across the field, enjoying the warm spring day and "
     "harming none, when he was set upon by three squires.",
     "The Knight of the Laughing Tree incident was a discrete episode within the Tourney "
     "at Harrenhal.",
     None),

    # ── Role edges — KotLT incident (4) ───────────────────────────────────
    # E6
    ("knight-of-the-laughing-tree", "FIGHTS_IN", "knight-of-the-laughing-tree-incident", 1,
     "asos", "asos-bran-02", 225,
     "The porcupine knight fell first, then the pitchfork knight, and lastly the knight "
     "of the two towers.",
     "The mystery knight fought in and was the central combatant of the KotLT incident.",
     None),
    # E7
    ("howland-reed", "VICTIM_IN", "knight-of-the-laughing-tree-incident", 1,
     "asos", "asos-bran-02", 179,
     "he was set upon by three squires. They were none older than fifteen, yet even so "
     "they were bigger than him, all three.",
     "Howland Reed was beaten by the three squires — the victim whose mistreatment "
     "prompted the mystery knight's intervention.",
     None),
    # E8
    ("aerys-ii-targaryen", "WITNESS_IN", "knight-of-the-laughing-tree-incident", 1,
     "asos", "asos-bran-02", 229,
     "The king was wroth, and even sent his son the dragon prince to seek the man, but "
     "all they ever found was his painted shield, hanging abandoned in a tree.",
     "Aerys witnessed the incident and was angered enough to dispatch Rhaegar to unmask "
     "the mystery knight.",
     None),
    # E9
    ("rhaegar-targaryen", "AGENT_IN", "knight-of-the-laughing-tree-incident", 1,
     "asos", "asos-bran-02", 229,
     "the king himself urged men to challenge him",
     "Rhaegar was sent by Aerys to seek and unmask the mystery knight — acting agent "
     "in the royal response.",
     None),

    # ── Role edges — Connington exile (2) ─────────────────────────────────
    # E10
    ("jon-connington", "VICTIM_IN", "exile-of-jon-connington", 1,
     "adwd", "adwd-the-griffin-reborn-01", 57,
     "Aerys Targaryen had stripped him of his titles and sent him into exile in a mad "
     "fit of ingratitude and suspicion",
     "Jon Connington was the victim of the stripping and exile ordered by Aerys.",
     None),
    # E11
    ("aerys-ii-targaryen", "COMMANDS_IN", "exile-of-jon-connington", 1,
     "adwd", "adwd-the-griffin-reborn-01", 57,
     "Aerys Targaryen had stripped him of his titles and sent him into exile in a mad "
     "fit of ingratitude and suspicion",
     "Aerys ordered the stripping of titles and exile — the commanding instigator.",
     None),

    # ── Role edges — Battle of the Bells (fill bare node) (2) ────────────
    # E12
    ("jon-connington", "COMMANDS_IN", "battle-of-the-bells", 1,
     "asos", "asos-jaime-05", 53,
     "After dancing griffins lost the Battle of the Bells, Aerys exiled him.",
     "Jon Connington commanded the Targaryen forces at the Battle of the Bells.",
     None),
    # E13
    ("robert-baratheon", "AGENT_IN", "battle-of-the-bells", 1,
     "asos", "asos-jaime-05", 53,
     "He had finally realized that Robert was no mere outlaw lord to be crushed at whim, "
     "but the greatest threat House Targaryen had faced since Daemon Blackfyre.",
     "Robert Baratheon was the primary acting opponent at the Battle of the Bells.",
     None),

    # ── Role edges — Wildfire-plot overlays (2) ───────────────────────────
    # E14
    ("rossart", "AGENT_IN", "wildfire-plot", 1,
     "asos", "asos-jaime-05", 55,
     "Aerys burnt him alive for that, and hung his chain about the neck of Rossart, "
     "his favorite pyromancer.",
     "Rossart was Aerys's favorite pyromancer and the lead agent executing the wildfire "
     "plot.",
     None),
    # E15
    ("aerys-ii-targaryen", "COMMANDS_IN", "wildfire-plot", 1,
     "asos", "asos-jaime-05", 53,
     "So His Grace commanded his alchemists to place caches of wildfire all over "
     "King's Landing. Beneath Baelor's Sept and the hovels of Flea Bottom, under stables "
     "and storehouses, at all seven gates, even in the cellars of the Red Keep itself.",
     "Aerys commanded the placement of wildfire caches throughout King's Landing — the "
     "orderer of the wildfire plot.",
     None),

    # ── Jon Arryn murder reification (4) ──────────────────────────────────
    # E16
    ("jon-arryn", "VICTIM_IN", "murder-of-jon-arryn", 1,
     "agot", "agot-eddard-07", 311,
     "The tears of Lys, they call it. A rare and costly thing, clear and sweet as water, "
     "and it leaves no trace.",
     "Jon Arryn was poisoned with the tears of Lys — the victim of the murder.",
     None),
    # E17
    ("lysa-arryn", "AGENT_IN", "murder-of-jon-arryn", 1,
     "asos", "asos-sansa-07", 287,
     "You told me to put the tears in Jon's wine, and I did. For Robert, and for us!",
     "Lysa Arryn administered the poison to Jon Arryn — the direct agent of the murder.",
     None),
    # E18
    ("petyr-baelish", "SUSPECTED_OF", "murder-of-jon-arryn", 2,
     "asos", "asos-sansa-07", 287,
     "You told me to put the tears in Jon's wine, and I did. For Robert, and for us!",
     "Lysa's confession implicates Littlefinger as the instigator who told her to poison "
     "Jon Arryn.",
     "pending"),
    # E19
    ("cersei-lannister", "SUSPECTED_OF", "murder-of-jon-arryn", 2,
     "agot", "agot-catelyn-07", 87,
     "but whether it was Tyrion, or Ser Jaime, or the queen, or all of them together, "
     "I could not begin to say.",
     "Cersei was the in-world suspect named in Lysa's false accusatory letter, making "
     "her the dominant false-misdirection target.",
     "pending"),

    # ── SUSPECTED_OF / WITNESS_IN substrate (5) ───────────────────────────
    # E20
    ("rhaegar-targaryen", "SUSPECTED_OF", "abduction-of-lyanna", 2,
     "agot", "agot-bran-07", 79,
     "Robert was betrothed to marry her, but Prince Rhaegar carried her off and raped her,"
     " Bran explained.",
     "Rhaegar is the in-world-named abductor/rapist of Lyanna Stark, per Robert's "
     "war-narrative framing.",
     "pending"),
    # E21
    ("lyanna-stark", "SUSPECTED_OF", "knight-of-the-laughing-tree-incident", 2,
     "asos", "asos-bran-02", 233,
     "Are you certain you never heard this tale before, Bran? asked Jojen. "
     "Your lord father never told it to you?",
     "Lyanna Stark is the in-world-suspected identity of the mystery Knight of the "
     "Laughing Tree; Jojen's pointed question implies Ned and Howland knew.",
     "pending"),
    # E22
    ("howland-reed", "WITNESS_IN", "combat-at-the-tower-of-joy", 1,
     "agot", "agot-eddard-10", 93,
     "They had been seven against three, yet only two had lived to ride away; Eddard "
     "Stark himself and the little crannogman, Howland Reed.",
     "Howland Reed was one of only two survivors of the combat at the Tower of Joy — "
     "a direct witness.",
     None),
    # E23
    ("eddard-stark", "WITNESS_IN", "combat-at-the-tower-of-joy", 1,
     "agot", "agot-eddard-10", 45,
     "he could hear Lyanna screaming. 'Eddard!' she called. A storm of rose petals blew "
     "across a blood-streaked sky, as blue as the eyes of death.",
     "Eddard Stark witnessed the combat at the Tower of Joy firsthand as the other "
     "surviving participant.",
     None),
]


# ── Node bodies ───────────────────────────────────────────────────────────────

KOTLT_NODE = """\
---
name: "Knight of the Laughing Tree incident"
type: event.incident
slug: knight-of-the-laughing-tree-incident
aliases: ["Knight of the Laughing Tree incident", "the mystery knight at Harrenhal", "Laughing Tree incident"]
confidence: tier-1
era: roberts-rebellion
pass_origin: s133-rr-enrich
node_version: 1
evidence_chapters:
  - ASOS Bran II
occurred:
  ac_year: 281
  precision: year
  basis_source: book-chapter
  basis_reliability: second-hand-oral
  date_confidence: tier-2
---

## Identity

At the [Tourney at Harrenhal](tourney-at-harrenhal) a mystery knight appeared in mismatched patchwork armour bearing a shield painted with a weirwood-faced laughing tree. The [little crannogman Howland Reed](howland-reed) had been set upon and beaten by three squires the day before; the mystery knight challenged the three knights those squires served, unhorsed all three, and demanded only "teach your squires honor" as ransom for their armour and horses. [King Aerys II](aerys-ii-targaryen) was furious and dispatched his son [Prince Rhaegar](rhaegar-targaryen) to unmask the knight, but when Rhaegar came he found only the painted shield hanging abandoned in a tree. The knight's identity remains ungated in the published text, though the surrounding narrative strongly implies insider knowledge among the Stark-Reed circle. The incident is a direct sub-beat of the Tourney at Harrenhal and seeds the Lyanna-Rhaegar strand of the Robert's Rebellion arc.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S133 RR enrichment pass. The incident is a [SUB_BEAT_OF](tourney-at-harrenhal) the Tourney at Harrenhal (Tier-1). [Knight of the Laughing Tree](knight-of-the-laughing-tree) FIGHTS_IN (Tier-1); [Howland Reed](howland-reed) VICTIM_IN (the beaten crannogman; Tier-1); [Aerys II](aerys-ii-targaryen) WITNESS_IN (angered spectator who orders the unmasking; Tier-1); [Rhaegar Targaryen](rhaegar-targaryen) AGENT_IN (sent to unmask; Tier-1). [Lyanna Stark](lyanna-stark) SUSPECTED_OF the mystery-knight identity (Tier-2, GATED — identity not confirmed in published canon).)

## Quotes

> "The little crannogman was walking across the field, enjoying the warm spring day and harming none, when he was set upon by three squires. They were none older than fifteen, yet even so they were bigger than him, all three."

— ASOS Bran II (`sources/chapters/asos/asos-bran-02.md:179`)

> "The king was wroth, and even sent his son the dragon prince to seek the man, but all they ever found was his painted shield, hanging abandoned in a tree."

— ASOS Bran II (`sources/chapters/asos/asos-bran-02.md:229`)
"""

EXILE_CONNINGTON_NODE = """\
---
name: "Exile of Jon Connington"
type: event.incident
slug: exile-of-jon-connington
aliases: ["exile of Jon Connington", "Connington stripped and exiled", "Aerys exiles Jon Connington"]
confidence: tier-1
era: roberts-rebellion
pass_origin: s133-rr-enrich
node_version: 1
evidence_chapters:
  - ADWD The Griffin Reborn I
occurred:
  ac_year: 283
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-retrospective
  date_confidence: tier-2
---

## Identity

After [Jon Connington](jon-connington) led the Targaryen host at the [Battle of the Bells](battle-of-the-bells) and failed to kill Robert Baratheon, [Aerys II Targaryen](aerys-ii-targaryen) stripped him of his titles and exiled him — an act the king framed as punishment for failure but which Connington's later retrospective characterizes as "a mad fit of ingratitude and suspicion." The exile is the causal hinge of the AEGON container arc: a disgraced Connington later finds his way to the Golden Company and raises [Young Griff](aegon-revealed-to-the-golden-company), making his own exile the precondition of Young Aegon's comeback. The exile is the direct effect of the Battle of the Bells (CAUSES, Tier-1) and in turn ENABLES the reveal of Young Aegon to the Golden Company.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S133 RR enrichment pass. [Battle of the Bells](battle-of-the-bells) CAUSES exile-of-jon-connington (Tier-1). exile-of-jon-connington ENABLES [aegon-revealed-to-the-golden-company](aegon-revealed-to-the-golden-company) (Tier-1; the exile is what puts Connington in position to serve as Aegon's guardian in exile). [Jon Connington](jon-connington) VICTIM_IN (Tier-1); [Aerys II](aerys-ii-targaryen) COMMANDS_IN as orderer (Tier-1).)

## Quotes

> "After the Battle of the Bells, when Aerys Targaryen had stripped him of his titles and sent him into exile in a mad fit of ingratitude and suspicion"

— ADWD The Griffin Reborn I (`sources/chapters/adwd/adwd-the-griffin-reborn-01.md:57`)

> "I failed the father," he said, "but I will not fail the son."

— Jon Connington, ADWD The Griffin Reborn I (`sources/chapters/adwd/adwd-the-griffin-reborn-01.md:71`)
"""

MURDER_JON_ARRYN_NODE = """\
---
name: "Murder of Jon Arryn"
type: event.incident
slug: murder-of-jon-arryn
aliases: ["murder of Jon Arryn", "death of Jon Arryn", "poisoning of Jon Arryn"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s133-rr-enrich
node_version: 1
evidence_chapters:
  - AGOT Eddard VII
  - ASOS Sansa VII
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

The inciting mystery of the entire saga. [Jon Arryn](jon-arryn), Hand of the King, was poisoned with the tears of Lys — a rare, clear, traceless poison. A letter from [Lysa Arryn](lysa-arryn) to her sister Catelyn blamed the Lannisters, pulling [Eddard Stark](eddard-stark) to King's Landing and triggering the whole chain of events in AGOT. The ASOS reveal (Lysa's confession to Littlefinger at the Eyrie) exposes [Lysa Arryn](lysa-arryn) as the direct administrator of the poison, acting at the instigation of [Petyr Baelish](petyr-baelish). [Cersei Lannister](cersei-lannister) was the prominent false-misdirection target named in Lysa's letter. This event is NOT part of Robert's Rebellion (it occurs 298 AC, roughly 15 years after RR's close); it is a standalone hub anchoring the War of the Five Kings' proximate trigger-chain.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S133 RR enrichment pass. [Jon Arryn](jon-arryn) VICTIM_IN (Tier-1); [Lysa Arryn](lysa-arryn) AGENT_IN (direct poisoner, per her own confession; Tier-1); [Petyr Baelish](petyr-baelish) SUSPECTED_OF as instigator (Tier-2 — confession implicates him but the full degree of his role is contested/inference); [Cersei Lannister](cersei-lannister) SUSPECTED_OF as false-misdirection target (Tier-2 — the in-world suspicion was real even though she is innocent).)

## Quotes

> "The tears of Lys, they call it. A rare and costly thing, clear and sweet as water, and it leaves no trace."

— AGOT Eddard VII (`sources/chapters/agot/agot-eddard-07.md:311`)

> "You told me to put the tears in Jon's wine, and I did. For Robert, and for us!"

— Lysa Arryn, ASOS Sansa VII (`sources/chapters/asos/asos-sansa-07.md:287`)
"""

NODES = [
    ("knight-of-the-laughing-tree-incident", KOTLT_NODE),
    ("exile-of-jon-connington", EXILE_CONNINGTON_NODE),
    ("murder-of-jon-arryn", MURDER_JON_ARRYN_NODE),
]


def make_edge_row(spec):
    (src, etype, tgt, tier, book, chap_id, line,
     quote, asserted, verified) = spec
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
    # ── 1. Slug pre-check ─────────────────────────────────────────────────
    all_slugs = set()
    for (src, _, tgt, *_rest) in EDGES_SPEC:
        all_slugs.add(src)
        all_slugs.add(tgt)

    # Exclude the 3 new nodes (don't exist yet — created in this run)
    check_slugs = all_slugs - NEW_NODE_SLUGS
    resolved, missing = precheck_slugs(check_slugs)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed — non-existent targets: {missing}")
    print(f"Slug pre-check OK: {len(resolved)} existing slugs resolved.")

    # ── 2. Re-run guard ───────────────────────────────────────────────────
    raw_lines = EDGES.read_text(encoding="utf-8").splitlines()
    existing_lines = [ln for ln in raw_lines if ln.strip()]
    if any(RUN_ID in ln for ln in existing_lines):
        sys.exit(f"ABORT: run_id '{RUN_ID}' already present in edges.jsonl — already minted.")
    print(f"Re-run guard OK: run_id '{RUN_ID}' not present.")

    # ── 3. Backup ─────────────────────────────────────────────────────────
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)
    print(f"Backup written → {BACKUP}")

    # ── 4. DROP: filter junk GUEST_OF row ─────────────────────────────────
    kept_lines = []
    drop_count = 0
    for ln in existing_lines:
        try:
            obj = json.loads(ln)
        except json.JSONDecodeError:
            kept_lines.append(ln)
            continue
        if (obj.get("edge_type") == DROP_EDGE_TYPE
                and obj.get("source_slug") == DROP_SOURCE
                and obj.get("target_slug") == DROP_TARGET):
            drop_count += 1
            print(f"DROP confirmed: removed '{DROP_SOURCE} {DROP_EDGE_TYPE} {DROP_TARGET}'")
        else:
            kept_lines.append(ln)

    if drop_count == 0:
        print(f"WARNING: DROP target '{DROP_SOURCE} {DROP_EDGE_TYPE} {DROP_TARGET}' "
              "NOT FOUND in edges.jsonl — nothing dropped.")
    elif drop_count > 1:
        print(f"WARNING: found {drop_count} copies of the DROP target — all removed.")

    # ── 5. Mint new nodes ─────────────────────────────────────────────────
    nodes_created = []
    for slug, body in NODES:
        node_path = NODES_EVENTS / f"{slug}.node.md"
        if node_path.exists():
            print(f"  SKIP node (already exists): {node_path.name}")
        else:
            node_path.write_text(body, encoding="utf-8")
            nodes_created.append(slug)
            print(f"  Created node: {node_path.name}")

    # ── 6. Build new edge rows ─────────────────────────────────────────────
    new_rows = [make_edge_row(spec) for spec in EDGES_SPEC]

    # ── 7. Rewrite edges.jsonl (drop removed, new appended) ───────────────
    lines_before = len(existing_lines)
    all_out = kept_lines + [json.dumps(r, ensure_ascii=False) for r in new_rows]
    EDGES.write_text("\n".join(all_out) + "\n", encoding="utf-8")
    lines_after = len(all_out)

    # ── 8. Summary ────────────────────────────────────────────────────────
    type_counts: dict[str, int] = {}
    for spec in EDGES_SPEC:
        etype = spec[1]
        type_counts[etype] = type_counts.get(etype, 0) + 1

    print("\n── SUMMARY ─────────────────────────────────────────────────────")
    print(f"Nodes created ({len(nodes_created)}): {', '.join(nodes_created)}")
    print(f"Edges appended (23):")
    for etype, cnt in sorted(type_counts.items()):
        print(f"  {etype}: {cnt}")
    print(f"DROP: {drop_count} row(s) removed "
          f"({DROP_SOURCE} {DROP_EDGE_TYPE} {DROP_TARGET})")
    print(f"edges.jsonl: {lines_before} → {lines_after} lines "
          f"(+{len(new_rows)} appended, -{drop_count} dropped)")
    print(f"Backup: {BACKUP}")


if __name__ == "__main__":
    main()
