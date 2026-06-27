#!/usr/bin/env python3
"""Mint Battle of Castle Black enrichment (S153) — D1 in the Class-D event-cluster list
(Matt-picked over D5/A2 at the S153 fork). The ASOS Wall defense: the *battle no POV arc owns*.
Build+enrich: the social/dyad layer was already dense (Jon's web), but the EVENT-HUB layer was thin —
the marquee beats (Ygritte's death, Noye & Mag's mutual death) existed only as character-dyads or not
at all, and the hub `attack-on-castle-black` had NO causal upstream.

Six new event nodes (containers: [north]):
  death-of-ygritte, noye-and-mag-die-in-the-tunnel, southern-thenn-assault-on-castle-black,
  jon-takes-command-of-the-wall, jon-sortie-to-mance-camp,
  bowen-marsh-marches-the-garrison-from-castle-black

37 edges (see candidates.json). KEY synthesis calls (4-lens + line-check):
  - NO `jon KILLS styr` (the Wall's fire-trap/stair-collapse kills him, not Jon — Lens A+C consensus).
  - NO attacker edge for Ygritte (the arrow is un-attributed in the text — node-prose only).
  - NO Grenn-holds-the-gate node (HBO-only; the book tunnel defenders are Noye + four UNNAMED men).
  - Existing Noye<->Mag KILLS dyad (both directions) KEPT; reified via the tunnel event node.
  - horn-of-winter already existed (0 edges) — lit it via `mance OWNS horn-of-winter`; Joramun
    provenance stays node-prose (theory-gated), NOT asserted by the edge.
  - Marquee upstream fix: `fight-at-the-fist ENABLES attack-on-castle-black` +
    `bowen-marsh-marches... ENABLES attack-on-castle-black` (two convergent preconditions).

Reads working/enrichment/battle-castle-black/candidates.json; RE-GREPS each quote (FAIL-fast if a
quote moved). Safeguards mirror prior enrichment mints (backup, re-run guard, slug pre-check excl.
new nodes). Additive only — retirements/adjustments live in the finalize script."""
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
NODES_EVENTS = REPO / "graph" / "nodes" / "events"
CAND = REPO / "working" / "enrichment" / "battle-castle-black" / "candidates.json"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-battle-castle-black-enrichment-2026-06-26.jsonl"

RUN_ID = "battle-castle-black-enrichment-s153"
PRODUCED_AT = "2026-06-26T00:00:00+00:00"

NEW_NODE_SLUGS = {
    "death-of-ygritte",
    "noye-and-mag-die-in-the-tunnel",
    "southern-thenn-assault-on-castle-black",
    "jon-takes-command-of-the-wall",
    "jon-sortie-to-mance-camp",
    "bowen-marsh-marches-the-garrison-from-castle-black",
}


def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def authoritative_line(book, chapter, quote):
    f = REPO / "sources" / "chapters" / book / f"{chapter}.md"
    if not f.exists():
        sys.exit(f"ABORT: chapter file missing: {f}")
    lines = f.read_text(encoding="utf-8").splitlines()
    q = norm(quote)
    for i, ln in enumerate(lines, 1):
        if q in norm(ln):
            return i
    for i in range(len(lines) - 1):
        if q in norm(lines[i] + " " + lines[i + 1]):
            return i + 1
    sys.exit(f"ABORT: quote not found in {chapter}.md -> {quote!r}")


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-battle-castle-black-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


def make_edge_row(e):
    book, chapter = e["book"], e["chapter"]
    line = authoritative_line(book, chapter, e["quote"])
    row = {
        "edge_type": e["type"],
        "source_slug": e["source"],
        "target_slug": e["target"],
        **common(),
        "evidence_book": book,
        "evidence_chapter": chapter,
        "evidence_ref": f"sources/chapters/{book}/{chapter}.md:{line}",
        "evidence_quote": e["quote"],
        "confidence_tier": e["tier"],
        "asserted_relation": e["note"],
        "candidate_id": e["id"],
    }
    if e.get("qualifier"):
        row["qualifier"] = e["qualifier"]
    if e.get("verify"):
        row["verified_by"] = "pending"
    return row


# ════════════════════════════ NODE BODIES ════════════════════════════

DEATH_OF_YGRITTE = """\
---
name: "Death of Ygritte"
type: event.death
slug: death-of-ygritte
aliases: ["Ygritte dies at Castle Black", "Ygritte's death"]
confidence: tier-1
containers: [north]
era: current-narrative
pass_origin: s153-battle-castle-black-enrich
node_version: 1
evidence_chapters:
  - ASOS Jon VII
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Death of Ygritte

During the [southern Thenn assault on Castle Black](southern-thenn-assault-on-castle-black),
[Jon Snow](jon-snow) finds [Ygritte](ygritte) beneath the Lord Commander's Tower with an arrow between
her breasts. She dies in his arms — *"You know nothing, Jon Snow,"* her last words, the recurring
phrase at its most load-bearing. Jon later [burns her body](attack-on-castle-black) north of the Wall,
as he knew she would have wanted.

**The shooter is un-attributed.** Jon sees the arrow is *"black . . . but it was fletched with white
duck feathers. Not mine . . . not one of mine,"* and later tells Tormund only *"My brother"* — a Night's
Watch man, never identified. The text deliberately leaves the attribution open; no AGENT_IN / KILLS /
SUSPECTED_OF edge is drawn (the lenses converged on node-prose). The emotional weight lives in the
existing `jon-snow MOURNS ygritte` edge.

## Quotes

> He found Ygritte sprawled across a patch of old snow beneath the Lord Commander's Tower, with an arrow between her breasts. The ice crystals had settled over her face, and in the moonlight it looked as though she wore a glittering silver mask.

> "Oh." Ygritte cupped his cheek with her hand. "You know nothing, Jon Snow," she sighed, dying.
"""

NOYE_AND_MAG = """\
---
name: "Donal Noye and Mag the Mighty kill each other in the tunnel"
type: event.death
slug: noye-and-mag-die-in-the-tunnel
aliases: ["death of Donal Noye", "death of Mag the Mighty", "Noye and Mag die in the gate tunnel"]
confidence: tier-1
containers: [north]
era: current-narrative
pass_origin: s153-battle-castle-black-enrich
node_version: 1
evidence_chapters:
  - ASOS Jon VIII
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Donal Noye and Mag the Mighty kill each other in the tunnel

When [Mag the Mighty](mag-mar-tun-doh-weg), king of the giants, forces the gate and wrenches the iron
bars apart, [Donal Noye](donal-noye) and four volunteers hold the last twenty feet of the tunnel. Mag
twists the head off Spotted Pate and crushes Noye in his massive arms; Noye drives his sword deep into
the giant's throat. They die together — *"I don't know who died first."* The one-armed blacksmith slays
the king of the giants, and the deed becomes the battle's elegy: *"I am the last of the giants."*

This node reifies the pre-existing `donal-noye KILLS mag-mar-tun-doh-weg` /
`mag-mar-tun-doh-weg KILLS donal-noye` dyad (both directions kept) as a queryable mutual-death event,
SUB_BEAT_OF [attack-on-castle-black](attack-on-castle-black). Noye and Mag each carry AGENT_IN and
VICTIM_IN roles.

## Quotes

> "Yes. Donal was the last." Noye's sword was sunk deep in the giant's throat, halfway to the hilt. The armorer had always seemed such a big man to Jon, but locked in the giant's massive arms he looked almost like a child. "The giant crushed his spine. I don't know who died first."

> "Mag." I am the last of the giants. ... "It was Mag the Mighty. The king of the giants."
"""

SOUTHERN_ASSAULT = """\
---
name: "Southern Thenn assault on Castle Black"
type: event.battle
slug: southern-thenn-assault-on-castle-black
aliases: ["Styr's attack from the south", "the Thenn assault on Castle Black"]
confidence: tier-1
containers: [north]
era: current-narrative
pass_origin: s153-battle-castle-black-enrich
node_version: 1
evidence_chapters:
  - ASOS Jon VII
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Southern Thenn assault on Castle Black

Mance Rayder's southern prong: [Styr](styr), the Magnar of [Thenn](thenn-region), scales the Wall near
Greyguard with ~120 Thenns and Jarl's raiders (and [Jon Snow](jon-snow), pretending to be a turncloak)
to take undefended Castle Black from the south while the main host hits the gate. [Jon escapes at
Queenscrown and warns the castle](jon-snow), so the surprise is lost. The Thenns burn Mole's Town and
storm the crescent barricade; [Donal Noye](donal-noye), Jon and [Satin](satin) hold the King's Tower
with Longclaw, boiling oil, and fire arrows. Noye's oil-drenched switchback stair is then set alight —
*"the whole lower third of the stair broke off, along with several tons of ice."* Styr and ~20 Thenns
die in the collapse. **The Wall defends itself.** [Ygritte dies](death-of-ygritte) in the aftermath.

SUB_BEAT_OF [attack-on-castle-black](attack-on-castle-black). Note: Styr is killed by the fire/ice
collapse, NOT by Jon's hand (`styr VICTIM_IN` this event; no `jon KILLS styr` edge).

## Quotes

> "We kill them," Jon shouted back, a black arrow in his hand.

> Jon dropped his bow, reached back over his shoulder, ripped Longclaw from its sheath, and buried the blade in the middle of the first head to pop out of the tower. Bronze was no match for Valyrian steel.

> Twenty-odd Thenns were still huddled together between the fires when the ice cracked from the heat, and the whole lower third of the stair broke off, along with several tons of ice. That was the last that Jon Snow saw of Styr, the Magnar of Thenn. The Wall defends itself, he thought.
"""

JON_TAKES_COMMAND = """\
---
name: "Jon Snow takes command of the Wall"
type: event.incident
slug: jon-takes-command-of-the-wall
aliases: ["The Wall is yours, Jon Snow", "Noye gives Jon the Wall"]
confidence: tier-1
containers: [north]
era: current-narrative
pass_origin: s153-battle-castle-black-enrich
node_version: 1
evidence_chapters:
  - ASOS Jon VIII
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Jon Snow takes command of the Wall

As [Donal Noye](donal-noye) descends to hold the tunnel against the giants, he hands [Jon
Snow](jon-snow) command of the Wall — *"Lord? I'm a blacksmith. I said, the Wall is yours."* When Noye
dies below, [Maester Aemon](aemon-targaryen-son-of-maekar-i) confirms the appointment: *"It must be you
or no one. The Wall is yours, Jon Snow."* A bastard steward with no formal rank commands the defense of
Castle Black for the rest of the battle, bypassing the absent garrison and the squabbling officers — the
proving ground that leads, two beats later, to
[Jon's election as Lord Commander](jon-elected-lord-commander).

SUB_BEAT_OF [attack-on-castle-black](attack-on-castle-black). Noye and Aemon both carry `APPOINTS jon-snow`.

## Quotes

> "Jon, you have the Wall till I return." ... "Lord? I'm a blacksmith. I said, the Wall is yours."

> "Donal chose you, and Qhorin Halfhand before him. Lord Commander Mormont made you his steward. You are a son of Winterfell, a nephew of Benjen Stark. It must be you or no one. The Wall is yours, Jon Snow."
"""

JON_SORTIE = """\
---
name: "Jon's sortie to Mance's camp"
type: event.incident
slug: jon-sortie-to-mance-camp
aliases: ["Jon sent to kill Mance", "the parley assassination sortie"]
confidence: tier-1
containers: [north]
era: current-narrative
pass_origin: s153-battle-castle-black-enrich
node_version: 1
evidence_chapters:
  - ASOS Jon X
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Jon's sortie to Mance's camp

Unable to hang Jon (Maester Aemon has written Cotter Pyke vouching for him), [Janos
Slynt](janos-slynt) and [Ser Alliser Thorne](alliser-thorne) send [Jon Snow](jon-snow) to Mance's camp
under the pretext of treating — but with secret orders to assassinate the King-beyond-the-Wall:
*"We're sending you to kill him."* It is a no-win trap (kill Mance and the free folk kill Jon; refuse and
Slynt brands him craven). Jon walks into the camp with [Longclaw](longclaw), is brought before
[Mance](mance-rayder), sees the [Horn of Winter](horn-of-winter) — and the sortie is overtaken when
[Stannis's cavalry charge](battle-beneath-the-wall) reaches the camp before Jon can act.

SUB_BEAT_OF [attack-on-castle-black](attack-on-castle-black). Slynt + Thorne carry `COMMANDS_IN`; Slynt
also `MANIPULATES jon-snow` (via_threat). The intended kill never happens, so no Mance VICTIM_IN edge.

## Quotes

> "We're not sending you to talk with Mance Rayder," Ser Alliser said. "We're sending you to kill him."

> When the cage jerked to a halt, Jon swung down onto the ground and rattled Longclaw's hilt to loosen the bastard blade in its scabbard.
"""

BOWEN_MARCHES = """\
---
name: "Bowen Marsh marches the garrison from Castle Black"
type: event.incident
slug: bowen-marsh-marches-the-garrison-from-castle-black
aliases: ["Bowen Marsh marches out", "the garrison leaves Castle Black"]
confidence: tier-1
containers: [north]
era: current-narrative
pass_origin: s153-battle-castle-black-enrich
node_version: 1
evidence_chapters:
  - ASOS Jon VI
  - ASOS Jon VII
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Bowen Marsh marches the garrison from Castle Black

Baited by [Mance](mance-rayder)'s feint raids strung all along the Wall (Harma at Woodswatch,
Rattleshirt at Long Barrow, the Weeper near Icemark), Lord Steward [Bowen Marsh](bowen-marsh) marches
out the bulk of Castle Black's fighting men, leaving *"old men, cripples, and green boys"* to hold the
castle under the blacksmith [Donal Noye](donal-noye). The dispersal is exactly what Mance planned —
*"Mance wants us to spread ourselves thin . . . And Bowen Marsh has obliged him"* — and it is the
enabling condition that lets the [southern Thenn assault](southern-thenn-assault-on-castle-black)
threaten the castle at all.

`bowen-marsh AGENT_IN`; `ENABLES attack-on-castle-black`; `mance-rayder MANIPULATES bowen-marsh`
(via_false_information). A quiet resonance with Bowen's later turn against Jon: the man who marched
*out* of the castle here is the one who, in ADWD, drives the knife in.

## Quotes

> "Feints. Mance wants us to spread ourselves thin, don't you see?" And Bowen Marsh has obliged him. "The gate is here. The attack is here."

> The brothers Bowen Marsh had left behind were old men, cripples, and green boys, just as Donal Noye had warned him.
"""

NODES = [
    ("death-of-ygritte", NODES_EVENTS, DEATH_OF_YGRITTE),
    ("noye-and-mag-die-in-the-tunnel", NODES_EVENTS, NOYE_AND_MAG),
    ("southern-thenn-assault-on-castle-black", NODES_EVENTS, SOUTHERN_ASSAULT),
    ("jon-takes-command-of-the-wall", NODES_EVENTS, JON_TAKES_COMMAND),
    ("jon-sortie-to-mance-camp", NODES_EVENTS, JON_SORTIE),
    ("bowen-marsh-marches-the-garrison-from-castle-black", NODES_EVENTS, BOWEN_MARCHES),
]


def main():
    data = json.loads(CAND.read_text())
    edges = data["edges"]

    all_slugs = set()
    for e in edges:
        all_slugs.add(e["source"]); all_slugs.add(e["target"])
    resolved, missing = precheck_slugs(all_slugs - NEW_NODE_SLUGS)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed — non-existent: {sorted(missing)}")
    print(f"Slug pre-check OK: {len(resolved)} existing slugs resolved.")

    raw = EDGES.read_text(encoding="utf-8").splitlines()
    existing = [ln for ln in raw if ln.strip()]
    if any(RUN_ID in ln for ln in existing):
        sys.exit(f"ABORT: run_id '{RUN_ID}' already present — already minted.")
    print(f"Re-run guard OK: run_id '{RUN_ID}' not present.")

    new_rows = [make_edge_row(e) for e in edges]  # FAIL-fast on any unfound quote
    print(f"Line-check OK: all {len(new_rows)} quotes located in source.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)
    print(f"Backup written -> {BACKUP.relative_to(REPO)}")

    created = []
    for slug, node_dir, body in NODES:
        p = node_dir / f"{slug}.node.md"
        if p.exists():
            print(f"  SKIP node (exists): {p.name}")
        else:
            p.write_text(body, encoding="utf-8")
            created.append(slug)
            print(f"  Created node: {p.relative_to(REPO)}")

    out = existing + [json.dumps(r, ensure_ascii=False) for r in new_rows]
    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")

    tc = {}
    for e in edges:
        tc[e["type"]] = tc.get(e["type"], 0) + 1
    print("\n── SUMMARY ──")
    print(f"Nodes created ({len(created)}): {', '.join(created) or '(none)'}")
    print(f"Edges appended ({len(new_rows)}):")
    for t, c in sorted(tc.items()):
        print(f"  {t}: {c}")


if __name__ == "__main__":
    main()
