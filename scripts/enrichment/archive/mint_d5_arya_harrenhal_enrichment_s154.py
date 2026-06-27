#!/usr/bin/env python3
"""Mint D5 "Arya's flight & Harrenhal" enrichment (S154) — the SECOND Class-D event cluster
(Matt-picked over D2/D3/A2 at the S154 fork; the natural S150/S153 follow-on). The big AGOT->ACOK
Arya journey cluster: a DENSE dyadic/social layer (Arya's hate/fear/kill web) but a thin, causally-
ISLANDED event spine — the S153 Castle Black profile. `fight-at-the-holdfast` had 0 causal edges,
`needle` 0 outgoing, and the marquee beats (Needle's first kill, the iron-coin origin, Jaqen's 2nd
death, the naming-gambit, the escape) had no nodes.

Six new event nodes (NO container tag — Riverlands/journey, matches the S148-S150 A2 arcs):
  stableboy-killing, death-of-weese, arya-names-jaqen-himself,
  jaqen-gives-arya-the-iron-coin, arya-escapes-harrenhal, gold-cloaks-demand-gendry

44 edges (see candidates.json). KEY synthesis calls (4-lens + whole-file line-check):
  - MARQUEE spine: gregor-raids ENABLES holdfast -> holdfast CAUSES arya-captured -> capture ENABLES
    naming-gambit -> gambit CAUSES guards-killed -> guards ENABLES fall -> fall ENABLES iron-coin-giving
    -> iron-coin-giving ENABLES arya-departs-for-braavos. The Harrenhal->Braavos ORIGIN seam now
    threads into the S150 arc.
  - TEXT-TRAP held (3 lenses): the escape gate-guard is killed with Bolton's STOLEN DAGGER, not Needle
    -> NO `needle WIELDED_IN arya-escapes-harrenhal` (the dagger is node-prose, below artifact threshold).
  - Dropped `tywin COMMANDS_IN holdfast` (the acok-arya-07:71 quote is about destroying Roose Bolton,
    not the holdfast); Tywin->holdfast flows via existing tywin COMMANDS gregor-raids + new E1 ENABLES.
  - Dropped MANIPULATES for the naming-gambit (Jaqen is AWARE he's leveraged; MANIPULATES = unknowing).
  - THEORY-GATED (node-prose only, NO edge): FM cosmology / valar-morghulis-as-religion / Jaqen's true
    identity / the face-change-as-magic / the coin-as-magic. The coin, the words, and the face-change
    are minted as TEXT EVENTS (events + possession/agency edges); the theology is not asserted.
  - capture-of-harrenhal NODE-TANGLE (Lens D): capture-of-harrenhal (ASOS Gregor retaking) is NOT a dup
    of fall-of-harrenhal (ACOK Bolton takeover) or yielding-of-harrenhal (AGOT Whent yields) — distinct
    events, same castle. NOT touched here; alias-hygiene flag routed to todos.

Reads working/enrichment/d5-arya-harrenhal/candidates.json; RE-GREPS each quote (FAIL-fast). Additive
only — the iron-coin GIFTED_TO re-cite + verified_by stamps live in the finalize script."""
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
CAND = REPO / "working" / "enrichment" / "d5-arya-harrenhal" / "candidates.json"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-d5-arya-harrenhal-enrichment-2026-06-26.jsonl"

RUN_ID = "d5-arya-harrenhal-enrichment-s154"
PRODUCED_AT = "2026-06-26T00:00:00+00:00"

NEW_NODE_SLUGS = {
    "stableboy-killing",
    "death-of-weese",
    "arya-names-jaqen-himself",
    "jaqen-gives-arya-the-iron-coin",
    "arya-escapes-harrenhal",
    "gold-cloaks-demand-gendry",
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
        "typed_by": "curator-d5-arya-harrenhal-enrichment",
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


# ════════════════════════════ NODE BODIES (no container tag — Riverlands/journey) ════════════════════════════

STABLEBOY_KILLING = """\
---
name: "Killing of the stableboy (Needle's first kill)"
type: event.death
slug: stableboy-killing
aliases: ["Needle's first kill", "Arya kills the stableboy"]
confidence: tier-1
era: current-narrative
pass_origin: s154-d5-arya-harrenhal-enrich
node_version: 1
evidence_chapters:
  - AGOT Arya IV
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Killing of the stableboy (Needle's first kill)

Fleeing the Red Keep during the Lannister coup (after Syrio Forel falls covering her escape), [Arya
Stark](arya-stark) is cornered in the stables by a smirking stableboy with a pitchfork who means to claim
the queen's reward. In a heartbeat of terror, the only lesson she can summon is [Jon Snow](jon-snow)'s
very first — *stick him with the pointy end* — and she drives [Needle](needle) up through his belly. **It
is her first human kill.** The boy is unnamed; she carries the killing through the whole road-and-Harrenhal
arc, half-expecting his ghost in the dark.

This node fixes [Needle](needle)'s 0-outgoing dead end (`needle WIELDED_IN`). The kill is an AGOT-end
characterization beat, not on the ACOK road spine; it `MOTIVATES arya-stark` (the first blood that hardens
her). **The dagger-vs-Needle care matters elsewhere** — at the Harrenhal escape she kills with a stolen
dagger, NOT Needle (see [arya-escapes-harrenhal](arya-escapes-harrenhal)); here the weapon IS Needle.

## Quotes

> Everything Syrio Forel had ever taught her vanished in a heartbeat. In that instant of sudden terror, the only lesson Arya could remember was the one Jon Snow had given her, the very first.

> Needle went through his leather jerkin and the white flesh of his belly and came out between his shoulder blades. The boy dropped the pitchfork and made a soft noise, something between a gasp and a sigh.
"""

DEATH_OF_WEESE = """\
---
name: "Death of Weese (Jaqen's second death)"
type: event.death
slug: death-of-weese
aliases: ["Weese's death", "Jaqen's second death"]
confidence: tier-1
era: current-narrative
pass_origin: s154-d5-arya-harrenhal-enrich
node_version: 1
evidence_chapters:
  - ACOK Arya VII
  - ACOK Arya VIII
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Death of Weese (Jaqen's second death)

[Weese](weese), the cruel understeward of the Wailing Tower and [Arya](arya-stark)'s overseer at
[Harrenhal](harrenhal), is the **second** of the three deaths Arya buys from [Jaqen H'ghar](jaqen-hghar).
She finds him in the bathhouse, leans to his ear, and whispers *"Weese."* The next morning Weese's own
spotted dog — raised from a pup — tears out his throat in the ward; Jaqen acknowledges the kill with a
two-finger salute. The means are left opaque (Arya reasons *"only some dark magic could have turned the
animal against him"*) — the **method/theology stays node-prose, not an edge** (theory-gated).

Completes the three-deaths thread: death 1 = [Chiswyck](chiswyck-dies-three-days-later) (built); death 2 =
this node; death 3 = the [naming-gambit](arya-names-jaqen-himself), spent to free the dungeon northmen. All
three are repayment of the life-debt Arya created at the burning barn
([arya-frees-the-prisoners MOTIVATES jaqen-hghar](arya-frees-the-prisoners)).

## Quotes

> "I have a message." Arya eyed the serving girl uncertainly. When she did not seem likely to go away, she leaned in until her mouth was almost touching his ear. "Weese," she whispered.

> Weese was sprawled across the cobbles, his throat a red ruin, eyes gaping sightlessly up at a bank of grey cloud. His ugly spotted dog stood on his chest, lapping at the blood pulsing from his neck, and every so often ripping a mouthful of flesh out of the dead man's face.
"""

NAMING_GAMBIT = """\
---
name: "Arya names Jaqen himself (the naming-gambit)"
type: event.incident
slug: arya-names-jaqen-himself
aliases: ["the naming gambit", "Arya names Jaqen H'ghar"]
confidence: tier-1
era: current-narrative
pass_origin: s154-d5-arya-harrenhal-enrich
node_version: 1
evidence_chapters:
  - ACOK Arya IX
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Arya names Jaqen himself (the naming-gambit)

The pivot of the Harrenhal arc. With one death still owed her and the Bloody Mummers' arrival threatening
everyone, [Arya](arya-stark) needs the caged northern prisoners freed — far beyond a single whispered
name. So in the godswood she spends her last death on the assassin himself: *"It's Jaqen H'ghar."* Forced
to choose between his own death and a bargain, [Jaqen](jaqen-hghar) — more distraught than he had been in
the burning barn — offers to free the northmen if she will un-say his name. She does, and he acts at once.

The gambit is the **leverage-reversal** that `CAUSES` the weasel-soup dungeon massacre
([guards-killed](guards-killed)), which in turn enables the [fall of Harrenhal](fall-of-harrenhal). It is
the cleverest move in the arc and was previously unwired (guards-killed had no causal antecedent). NB this
is **open coercion, not MANIPULATES** (Jaqen knows exactly what she is doing); the leverage is captured by
`jaqen-hghar VICTIM_IN` + the `CAUSES guards-killed` hop, plus the existing `arya COMMANDS_IN guards-killed`.

## Quotes

> Arya put her lips to his ear. "It's Jaqen H'ghar."

> Jaqen's smile came and went. "A girl might . . . name another name then, if a friend did help?"
"""

JAQEN_GIVES_COIN = """\
---
name: "Jaqen gives Arya the iron coin"
type: event.incident
slug: jaqen-gives-arya-the-iron-coin
aliases: ["Jaqen's farewell", "the iron coin and valar morghulis"]
confidence: tier-1
era: current-narrative
pass_origin: s154-d5-arya-harrenhal-enrich
node_version: 1
evidence_chapters:
  - ACOK Arya IX
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Jaqen gives Arya the iron coin

His debt paid and [Harrenhal](harrenhal) fallen, [Jaqen H'ghar](jaqen-hghar) takes his leave of
[Arya](arya-stark) — and first changes his face entirely (fuller cheeks, hooked nose, a new scar, black
curls where the red-and-white hair had been). He presses a small [iron coin](iron-coin) into her palm and
tells her that to find him again she must give the coin to any man of Braavos and say *valar morghulis.*

**This is the ORIGIN of the iron-coin seam** the [Braavos arc](arya-departs-for-braavos) (built S150) hangs
off: the coin's existing `GIFTED_TO` edge cited the ASOS recollection, not this giving — the dip re-grounds
it here. `jaqen-gives-arya-the-iron-coin ENABLES arya-departs-for-braavos` threads the whole Harrenhal arc
forward into the Faceless-Men arc and (via S150) the terminal Braavos assassination.

**Theory-gated (node-prose, NOT edges):** the face-change as Faceless-Men magic, *valar morghulis* as a
religion/password-system, and Jaqen's true identity (the Alchemist/Pate question) are all evidence-only —
this node mints the TEXT EVENT (the giving, the words, the changed face), not the theology.

## Quotes

> Jaqen passed a hand down his face from forehead to chin, and where it went he changed. His cheeks grew fuller, his eyes closer; his nose hooked, a scar appeared on his right cheek where no scar had been before.

> "If the day comes when you would find me again, give that coin to any man from Braavos, and say these words to him—valar morghulis."
"""

ARYA_ESCAPES = """\
---
name: "Arya escapes Harrenhal"
type: event.incident
slug: arya-escapes-harrenhal
aliases: ["Arya's escape from Harrenhal", "Arya, Gendry and Hot Pie flee Harrenhal"]
confidence: tier-1
era: current-narrative
pass_origin: s154-d5-arya-harrenhal-enrich
node_version: 1
evidence_chapters:
  - ACOK Arya X
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Arya escapes Harrenhal

When [Roose Bolton](roose-bolton) prepares to leave [Harrenhal](harrenhal) to [Vargo Hoat](vargo-hoat) and
the Bloody Mummers — and to leave Arya with them — [Arya](arya-stark) acts. She steals horses by invoking
Bolton's authority, takes his map and dagger, and meets [Gendry](gendry) (in oiled mail, hammer on his
back) and [Hot Pie](hot-pie) (with bread and cheese) at the Tower of Ghosts postern. She uses [Jaqen's
iron coin](iron-coin) as a decoy — dropping it as false silver so the guard kneels — then **cuts his
throat with Bolton's stolen dagger** (NOT [Needle](needle); the dagger is below the named-artifact
threshold and stays node-prose) and whispers *"Valar morghulis"* as he dies. The three ride out into the
rain. The terminus of the Harrenhal cluster.

`fall-of-harrenhal ENABLES` this escape (Bolton's handover created the threat); Arya/Gendry/Hot-Pie all
`AGENT_IN`. The escape does NOT directly enable the Braavos departure (many ASOS legs intervene) — the
[iron coin's giving](jaqen-gives-arya-the-iron-coin) carries that seam.

## Quotes

> Cursing her softly, the man went to a knee to grope for the coin in the dirt, and there was his neck right in front of her. Arya slid her dagger out and drew it across his throat, as smooth as summer silk.

> "Valar morghulis," she whispered as he died.
"""

GOLD_CLOAKS_DEMAND_GENDRY = """\
---
name: "Gold cloaks demand Gendry from Yoren's band"
type: event.incident
slug: gold-cloaks-demand-gendry
aliases: ["the gold cloaks come for Gendry", "Cersei's warrant for Gendry"]
confidence: tier-1
era: current-narrative
pass_origin: s154-d5-arya-harrenhal-enrich
node_version: 1
evidence_chapters:
  - ACOK Arya II
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Gold cloaks demand Gendry from Yoren's band

On the kingsroad, an officer of the City Watch rides out from King's Landing with Queen
[Cersei](cersei-lannister)'s sealed warrant for *"a certain boy"* — [Gendry](gendry), one of King
Robert's bastards. (Arya, disguised as "Arry," assumes they want her; the officer's shortsword instead
jabs toward the Bull.) [Yoren](yoren) faces them down, puts his sword to the officer's throat, and sends
them back to the city — but it telegraphs the danger, and Yoren pushes the band to ride all night.

This wires Cersei's bastard-purge into the D5 cluster and gives Gendry's later peril its origin. Gendry is
ultimately taken at the [fight at the holdfast](fight-at-the-holdfast) (by Amory's foragers, not the gold
cloaks) and held as a captive smith (`gendry IMPRISONED_AT harrenhal`).

## Quotes

> The gold cloak officer dismounted. "I have a warrant for a certain boy—" Yoren stepped out of the inn, fingering his tangled black beard. "Who is it wants this boy?"

> "Fool! You think he's done with us? Next time he won't prance up and hand me no damn ribbon."
"""

NODES = [
    ("stableboy-killing", NODES_EVENTS, STABLEBOY_KILLING),
    ("death-of-weese", NODES_EVENTS, DEATH_OF_WEESE),
    ("arya-names-jaqen-himself", NODES_EVENTS, NAMING_GAMBIT),
    ("jaqen-gives-arya-the-iron-coin", NODES_EVENTS, JAQEN_GIVES_COIN),
    ("arya-escapes-harrenhal", NODES_EVENTS, ARYA_ESCAPES),
    ("gold-cloaks-demand-gendry", NODES_EVENTS, GOLD_CLOAKS_DEMAND_GENDRY),
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
