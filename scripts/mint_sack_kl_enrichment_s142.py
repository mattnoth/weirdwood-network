#!/usr/bin/env python3
"""Mint Sack of King's Landing enrichment pass 1 (S142) — ninth major-arc enrichment dip.

The LAST L1 remnant (Matt S142 — chose the Sack double-dip over the L2-granular planning
session). The Sack hub was ALREADY partly enriched (core wired in the RR pass S133; the
Elia->Oberyn seam in the Tywin's-death pass S139), so this is a flagged LOW-MARGINAL-YIELD
double-dip. The hub had 4 sub-beats and a dense atrocity/whodunit layer; what was missing
was the WILDFIRE THREAD's integration, the pyromancer substrate, two iconic aftermath beats,
and (the marquee) two cross-arc seams. This pass builds:

  - WILDFIRE INTEGRATION: `wildfire-plot ENABLES aerys-commands-the-city-burned` (the caches
    are the precondition of the burn-order — the burn-command had only 1 inbound edge); the
    two un-wired pyromancers `belis`/`garigus` AGENT_IN wildfire-plot (Rossart already wired);
    `qarlton-chelsted VICTIM_IN wildfire-plot` + `aerys KILLS chelsted` (the Hand burned alive
    for opposing the plot).
  - THE PYROMANCER-HUNT: `jaime KILLS belis` + `jaime KILLS garigus` (he hunted them down days
    after the Sack; jaime KILLS rossart + KILLS aerys already exist — NOT re-minted).
  - TWO ICONIC AFTERMATH BEATS (new nodes):
    * `tywin-presents-bodies-to-robert` (event.incident, SUB_BEAT_OF sack) — Tywin lays the
      wrapped corpses before the throne; Robert condones ("I see no babes. Only dragonspawn.").
      De-islands Robert's complicity + the Lannister-Baratheon alliance. (Its ENABLES->coronation
      edge was DROPPED at fresh-verify — over-distal/redundant with `sack CAUSES coronation`.)
    * `jaime-found-seated-on-the-iron-throne` (event.incident, SUB_BEAT_OF the kingslaying) —
      Ned rides the length of the hall to find the Kingslayer on the throne. Carries the Ned
      WITNESS_IN that CANNOT go on the slaying node (Ned arrived after Aerys was dead — gate
      precedent). roland-crakehall WITNESS_IN the slaying itself ("burst into the hall in time
      to see the last of it").
  - TWO CROSS-ARC SEAMS:
    * MARQUEE: `wildfire-plot ENABLES wildfire-trap-on-the-blackwater` — TEXT-DIRECT via the
      Dragonpit cache (acok-tyrion-11:107: "Another cache of Lord Rossart's was found, more
      than three hundred jars. Under the Dragonpit!") + Tyrion's "King Aerys's fickle fruits"
      (acok-tyrion-13:19). S138 deliberately kept the two NODES separate (correct — distinct
      events 16 yrs apart); this ENABLES edge wires the recovered-caches causal thread WITHOUT
      conflating them.
    * `murder-of-elia... MOTIVATES doran-reveals-fire-and-blood-pact` — the 17-year Dornish
      long-game; Doran's first words at the reveal are "Vengeance." / "Justice." / "Fire and
      blood." Tier-2 interpretive (deep-motive; the proximate trigger arianne-capture CAUSES
      it already exists).

Synthesis of 4 fresh Sonnet lenses (downstream-causal / secondary-char+SUSPECTED+WITNESS /
descriptive-object-depth / existing-node<->existing-node causal-wiring) over the built
cluster. PROPOSE-only lenses -> Opus orchestrator synthesized + LINE-CHECKED every cite via
grep against the source files -> this mint set.

THE LINE-CHECK / ADJUDICATION CATCHES (orchestrator, vs the lenses):
  - DEDUP drops: `jaime KILLS rossart` + `jaime KILLS aerys-ii-targaryen` already exist (only
    belis/garigus minted); `eddard-stark DISTRUSTS jaime-lannister` already exists (Ned already
    has DISTRUSTS/ATTACKS/DECEIVES/OPPOSES/RESENTS jaime) -> dropped; `murder MOTIVATES eddard`
    + `murder MOTIVATES oberyn` + `sack CAUSES coronation` all already in graph.
  - DROPPED `wildfire WIELDED_IN aerys-commands-the-city-burned` (lens 3): semantic stretch —
    the burn never happened (Jaime stopped it); the substance's weapon-use is already wired at
    Blackwater (`wildfire WIELDED_IN battle-of-the-blackwater`). Not minted.
  - CHELSTED target: 3 lenses said VICTIM_IN wildfire-plot, 1 said aerys-commands-the-city-
    burned. Chose wildfire-plot — Chelsted opposed and died over the cache-PLAN, well before
    the during-Sack burn-command.
  - WITNESS_IN gate: `eddard WITNESS_IN slaying` REJECTED (Aerys already dead when Ned arrived
    — aftermath, fails the gate; quincy-cox S141 precedent). Ned WITNESS_IN the THRONE-scene
    beat PASSES (the tableau was ongoing as he rode down the hall). roland-crakehall WITNESS_IN
    the slaying PASSES ("burst into the hall in time to see the last of it").
  - THEORY-GATED: the Aegon babe-swap (was the smashed babe really Aegon?) NOT engaged —
    existing slugs used as-is; no swap-claim minted. Parked for the theories track.

FINAL: 2 new nodes + 17 edges (18 minted, 1 dropped at fresh-verify). Fresh-verify (independent
Sonnet) = 15 CONFIRM / 2 ADJUST / 0 REJECT: DROPPED edge 12 (tywin-presents ENABLES coronation,
over-distal/redundant); DOWNGRADED the marquee Blackwater seam T1->T2 (cross-book deduction).
Surviving interpretive ENABLES/MOTIVATES seams stamped verified=fresh-verify-confirmed-s142.

Safeguards mirror mint_brienne_stoneheart_enrichment_s141.py: backup, re-run guard, slug
pre-check (NEW_NODE_SLUGS excluded), new-node create-if-absent.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
NODES_EVENTS = REPO / "graph" / "nodes" / "events"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-sack-kl-enrichment-2026-06-24.jsonl"

RUN_ID = "sack-kl-enrichment-s142"
PRODUCED_AT = "2026-06-24T00:00:00+00:00"

NEW_NODE_SLUGS = {
    "tywin-presents-bodies-to-robert",
    "jaime-found-seated-on-the-iron-throne",
}


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-sack-kl-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


# ════════════════════════════ NODE BODIES ════════════════════════════

TYWIN_PRESENTS = """\
---
name: "Tywin presents the bodies before the throne"
type: event.incident
slug: tywin-presents-bodies-to-robert
aliases: ["Tywin presents the bodies", "the bodies before the throne", "Tywin's token of fealty", "I see no babes only dragonspawn"]
confidence: tier-1
era: roberts-rebellion
pass_origin: s142-sack-kl-enrich
node_version: 1
evidence_chapters:
  - ASOS Tyrion VI
  - ASOS Tyrion IX
  - AGOT Eddard II
occurred:
  ac_year: 283
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-recollection
---

# Tywin presents the bodies before the throne

In the aftermath of the [Sack of King's Landing](sack-of-kings-landing), [Tywin Lannister](tywin-lannister)
laid the corpses of [Princess Elia](elia-martell), [Prince Aegon](aegon-targaryen-son-of-rhaegar),
and [Princess Rhaenys](rhaenys-targaryen-daughter-of-rhaegar) — wrapped in crimson Lannister
cloaks — before the Iron Throne as a token of fealty to the newly victorious
[Robert Baratheon](robert-baratheon). Tywin's own account is unsparing about the calculation:
"It was necessary to demonstrate our loyalty. When I laid those bodies before the throne, no
man could doubt that we had forsaken House Targaryen forever." Robert condoned the killings —
"I see no babes. Only dragonspawn." — and the moment cemented the Lannister-Baratheon alliance
that underpinned the whole post-rebellion order. It also opened the rift between Robert and
[Ned Stark](eddard-stark), who named it murder where Robert called it war.

## Edges
(Edges in `graph/edges/edges.jsonl`, S142 Sack-of-KL enrichment. SUB_BEAT_OF
[the Sack](sack-of-kings-landing); [Tywin](tywin-lannister) AGENT_IN; [Robert](robert-baratheon)
WITNESS_IN; ENABLES [Robert's coronation](coronation-of-robert-i-baratheon). The murdered
children's VICTIM_IN edges live on [the murder node](murder-of-elia-martell-and-rhaegars-children).)

## Quotes

> It was necessary to demonstrate our loyalty. When I laid those bodies before the throne, no man could doubt that we had forsaken House Targaryen forever.

— Tywin to Tyrion, ASOS Tyrion VI (`sources/chapters/asos/asos-tyrion-06.md:187`)

> It was Lord Tywin who presented my sister's children to King Robert all wrapped up in crimson Lannister cloaks.

— Oberyn Martell, ASOS Tyrion IX (`sources/chapters/asos/asos-tyrion-09.md:411`)

> Ned had named that murder; Robert called it war. When he had protested that the young prince and princess were no more than babes, his new-made king had replied, "I see no babes. Only dragonspawn."

— AGOT Eddard II (`sources/chapters/agot/agot-eddard-02.md:71`)
"""

JAIME_THRONE = """\
---
name: "Jaime found seated on the Iron Throne"
type: event.incident
slug: jaime-found-seated-on-the-iron-throne
aliases: ["Jaime on the Iron Throne", "Ned finds Jaime on the throne", "the Kingslayer on the throne"]
confidence: tier-1
era: roberts-rebellion
pass_origin: s142-sack-kl-enrich
node_version: 1
evidence_chapters:
  - ASOS Jaime II
  - AGOT Eddard II
occurred:
  ac_year: 283
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-recollection
---

# Jaime found seated on the Iron Throne

Immediately after [slaying Aerys II](slaying-of-aerys-ii-the-kingslaying),
[Jaime Lannister](jaime-lannister) climbed the Iron Throne and seated himself with his gilded
sword across his knees, "to see who would come to claim the kingdom." It was
[Eddard Stark](eddard-stark) who rode the length of the throne room — between the rows of
dragon skulls, his northmen filling the hall behind him — to find the Kingslayer high above his
knights in a lion-crested helm, his sword's edge red with a king's blood. Jaime laughed, rose,
and claimed he had only been keeping the seat warm for Robert. Ned never asked, and never
forgot: the tableau seeds his lifelong contempt for Jaime. (Ned arrived AFTER Aerys was dead,
so he did not witness the killing itself — only this aftermath scene.)

## Edges
(Edges in `graph/edges/edges.jsonl`, S142 Sack-of-KL enrichment. SUB_BEAT_OF
[the kingslaying](slaying-of-aerys-ii-the-kingslaying); [Jaime](jaime-lannister) AGENT_IN;
[Ned](eddard-stark) WITNESS_IN; LOCATED_AT [the Iron Throne](iron-throne). The existing
`eddard-stark DISTRUSTS jaime-lannister` character edge is the downstream consequence.)

## Quotes

> Then he climbed the Iron Throne and seated himself with his sword across his knees, to see who would come to claim the kingdom. As it happened, it had been Eddard Stark.

— Jaime's recollection, ASOS Jaime II (`sources/chapters/asos/asos-jaime-02.md:303`)

> He was seated on the Iron Throne, high above his knights, wearing a helm fashioned in the shape of a lion's head. How he glittered!

— Ned to Robert, AGOT Eddard II (`sources/chapters/agot/agot-eddard-02.md:151`)
"""

NODES = [
    ("tywin-presents-bodies-to-robert", NODES_EVENTS, TYWIN_PRESENTS),
    ("jaime-found-seated-on-the-iron-throne", NODES_EVENTS, JAIME_THRONE),
]

# ════════════════════════════ EDGES ════════════════════════════
# (src, etype, tgt, tier, book, chap_id, line, quote, asserted, verified, qualifier)

EDGES_SPEC = [
    # ════ WILDFIRE INTEGRATION (5) ════
    ("wildfire-plot", "ENABLES", "aerys-commands-the-city-burned", 1,
     "asos", "asos-jaime-05", 53,
     "So His Grace commanded his alchemists to place caches of wildfire all over King's Landing.",
     "The placement of wildfire caches (wildfire-plot) is the necessary precondition for Aerys's burn-order to be executable — without the caches the command is empty. ENABLES, not CAUSES (Aerys's free command is the sufficient cause). Closes the gap: the burn-order had only 1 inbound edge.",
     "fresh-verify-confirmed-s142", None),
    ("belis", "AGENT_IN", "wildfire-plot", 1,
     "asos", "asos-jaime-05", 55,
     "with Rossart, Belis, and Garigus coming and going night and day, he became suspicious.",
     "Belis is one of the three named master pyromancers placing the caches for Aerys. Rossart already wired AGENT_IN; Belis (0 incoming edges) was not. On-page in Jaime's bath confession.", None, None),
    ("garigus", "AGENT_IN", "wildfire-plot", 1,
     "asos", "asos-jaime-05", 55,
     "with Rossart, Belis, and Garigus coming and going night and day, he became suspicious.",
     "Garigus is the third named master pyromancer of the wildfire-plot. Existing node, 0 incoming edges. On-page.", None, None),
    ("qarlton-chelsted", "VICTIM_IN", "wildfire-plot", 1,
     "asos", "asos-jaime-05", 55,
     "Aerys burnt him alive for that, and hung his chain about the neck of Rossart, his favorite pyromancer.",
     "Chelsted (Hand of the King) opposed the wildfire cache-plan and was burned alive by Aerys for it — the human cost of the plot's internal politics. VICTIM_IN wildfire-plot (the cache-PLAN he died over, not the during-Sack burn-command). 0 prior edges.", None, None),
    ("aerys-ii-targaryen", "KILLS", "qarlton-chelsted", 1,
     "asos", "asos-jaime-05", 55,
     "Aerys burnt him alive for that",
     "Aerys burned his own Hand alive for casting down his chain in protest of the wildfire plot. KILLS = dyadic (killer -> victim).", None, None),

    # ════ THE PYROMANCER-HUNT (2) ════
    ("jaime-lannister", "KILLS", "belis", 1,
     "asos", "asos-jaime-05", 63,
     "Days later, I hunted down the others and slew them as well. Belis offered me gold, and Garigus wept for mercy.",
     "Jaime hunted and killed Belis days after the Sack (to stop the wildfire message from reaching any surviving pyromancer). KILLS = dyadic. (jaime KILLS rossart + KILLS aerys already exist — only belis/garigus minted.)", None, None),
    ("jaime-lannister", "KILLS", "garigus", 1,
     "asos", "asos-jaime-05", 63,
     "Days later, I hunted down the others and slew them as well. Belis offered me gold, and Garigus wept for mercy.",
     "Jaime hunted and killed Garigus days after the Sack. KILLS = dyadic. Same on-page passage as Belis.", None, None),

    # ════ ROLAND CRAKEHALL WITNESS (1) ════
    ("roland-crakehall", "WITNESS_IN", "slaying-of-aerys-ii-the-kingslaying", 1,
     "asos", "asos-jaime-02", 297,
     "Ser Elys Westerling and Lord Crakehall and others of his father's knights burst into the hall in time to see the last of it",
     "Crakehall and Westerling burst into the throne room and saw the conclusion of the kingslaying — present and perceiving, passes the WITNESS_IN gate (unlike Ned, who arrived after Aerys was dead).", None, None),

    # ════ NEW NODE: tywin-presents-bodies-to-robert (3) ════
    ("tywin-presents-bodies-to-robert", "SUB_BEAT_OF", "sack-of-kings-landing", 1,
     "asos", "asos-tyrion-06", 187,
     "When I laid those bodies before the throne, no man could doubt that we had forsaken House Targaryen forever.",
     "The presentation of the murdered royals' bodies to Robert is a beat of the Sack's political aftermath. SUB_BEAT_OF the hub.", None, None),
    ("tywin-lannister", "AGENT_IN", "tywin-presents-bodies-to-robert", 1,
     "asos", "asos-tyrion-06", 187,
     "When I laid those bodies before the throne, no man could doubt that we had forsaken House Targaryen forever.",
     "Tywin himself laid the bodies before the throne — his own deliberate political act (he confesses the calculation to Tyrion). AGENT_IN.", None, None),
    ("robert-baratheon", "WITNESS_IN", "tywin-presents-bodies-to-robert", 1,
     "agot", "agot-eddard-02", 71,
     "Tywin Lannister had presented Robert with the corpses of Rhaegar's wife and children as a token of fealty.",
     "Robert received and condoned the bodies ('I see no babes. Only dragonspawn.'). WITNESS_IN = present and perceiving (he is the audience the display is staged for).", None, None),
    # NOTE: `tywin-presents-bodies-to-robert ENABLES coronation-of-robert-i-baratheon` was
    # proposed (T2) but DROPPED at fresh-verify (over-distal / redundant with the existing
    # `sack-of-kings-landing CAUSES coronation-of-robert-i-baratheon`; the bodies-presentation
    # did not mechanically enable the coronation — Robert won the war regardless). The node
    # stands on its own via SUB_BEAT_OF + tywin AGENT_IN + robert WITNESS_IN.

    # ════ NEW NODE: jaime-found-seated-on-the-iron-throne (4) ════
    ("jaime-found-seated-on-the-iron-throne", "SUB_BEAT_OF", "slaying-of-aerys-ii-the-kingslaying", 1,
     "asos", "asos-jaime-02", 303,
     "Then he climbed the Iron Throne and seated himself with his sword across his knees, to see who would come to claim the kingdom.",
     "Jaime taking the throne is the immediate aftermath tableau of the kingslaying. SUB_BEAT_OF the slaying.", None, None),
    ("jaime-lannister", "AGENT_IN", "jaime-found-seated-on-the-iron-throne", 1,
     "asos", "asos-jaime-02", 303,
     "Then he climbed the Iron Throne and seated himself with his sword across his knees, to see who would come to claim the kingdom.",
     "Jaime chose to climb and sit the Iron Throne after the killing. AGENT_IN.", None, None),
    ("eddard-stark", "WITNESS_IN", "jaime-found-seated-on-the-iron-throne", 1,
     "agot", "agot-eddard-02", 151,
     "He was seated on the Iron Throne, high above his knights, wearing a helm fashioned in the shape of a lion's head.",
     "Ned rode the length of the hall and stopped before the throne, watching Jaime seated upon it — present and perceiving the tableau (the scene was ongoing as he entered). WITNESS_IN this beat PASSES the gate, where WITNESS_IN the killing fails (Aerys already dead).", None, None),
    ("jaime-found-seated-on-the-iron-throne", "LOCATED_AT", "iron-throne", 1,
     "agot", "agot-eddard-02", 151,
     "He was seated on the Iron Throne, high above his knights, wearing a helm fashioned in the shape of a lion's head.",
     "The scene's defining location is the Iron Throne itself. LOCATED_AT = event -> place/object-as-place.", None, None),

    # ════ CROSS-ARC SEAMS (2) ════
    ("wildfire-plot", "ENABLES", "wildfire-trap-on-the-blackwater", 2,
     "acok", "acok-tyrion-11", 107,
     "Another cache of Lord Rossart's was found, more than three hundred jars. Under the Dragonpit!",
     "MARQUEE cross-arc seam (283 AC -> 299 AC). Rossart's surviving 283 wildfire caches were physically recovered (the Dragonpit find) and folded into Tyrion's Blackwater arsenal — Tyrion calls the weapons 'King Aerys's fickle fruits' at the battle (acok-tyrion-13:19). ENABLES = partial precondition (Tyrion's new production was the bulk). S138 kept the two NODES separate (correct); this edge wires the causal thread WITHOUT conflating them. Tier-2: cross-chapter/cross-book deduction (no single end-to-end statement) per fresh-verify.",
     "fresh-verify-confirmed-s142", None),
    ("murder-of-elia-martell-and-rhaegars-children", "MOTIVATES", "doran-reveals-fire-and-blood-pact", 2,
     "affc", "affc-the-princess-in-the-tower-01", 325,
     "Prince Doran pressed the onyx dragon into her palm with his swollen, gouty fingers, and whispered, “Fire and blood.”",
     "Doran's covert Targaryen pact is the Dornish answer to the murder of his sister and her children — his first words at the reveal are 'Vengeance.' / 'Justice.' / 'Fire and blood.' MOTIVATES = deep-motive routed through Doran's 17-year patience (the proximate trigger arianne-collapses-and-is-captured CAUSES it already exists). Tier-2 interpretive (long causal span).",
     "fresh-verify-confirmed-s142", None),
]


def make_edge_row(spec):
    (src, etype, tgt, tier, book, chap_id, line, quote, asserted, verified, qualifier) = spec
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
    if qualifier is not None:
        row["qualifier"] = qualifier
    if verified is not None:
        row["verified_by"] = verified
    return row


def main():
    all_slugs = set()
    for spec in EDGES_SPEC:
        all_slugs.add(spec[0])
        all_slugs.add(spec[2])
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
    for slug, node_dir, body in NODES:
        node_path = node_dir / f"{slug}.node.md"
        if node_path.exists():
            print(f"  SKIP node (already exists): {node_path.name}")
        else:
            node_path.write_text(body, encoding="utf-8")
            nodes_created.append(slug)
            print(f"  Created node: {node_path.relative_to(REPO)}")

    new_rows = [make_edge_row(spec) for spec in EDGES_SPEC]
    lines_before = len(existing_lines)
    all_out = existing_lines + [json.dumps(r, ensure_ascii=False) for r in new_rows]
    EDGES.write_text("\n".join(all_out) + "\n", encoding="utf-8")
    lines_after = len(all_out)

    type_counts = {}
    for spec in EDGES_SPEC:
        type_counts[spec[1]] = type_counts.get(spec[1], 0) + 1

    print("\n── SUMMARY ──")
    print(f"Nodes created ({len(nodes_created)}): {', '.join(nodes_created) or '(none)'}")
    print(f"Edges appended ({len(new_rows)}):")
    for etype, cnt in sorted(type_counts.items()):
        print(f"  {etype}: {cnt}")
    print(f"edges.jsonl: {lines_before} → {lines_after} lines (+{len(new_rows)})")
    print(f"Backup: {BACKUP}")


if __name__ == "__main__":
    main()
