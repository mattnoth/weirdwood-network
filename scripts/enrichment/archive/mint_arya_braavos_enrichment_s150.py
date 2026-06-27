#!/usr/bin/env python3
"""Mint Arya / Braavos BUILD+ENRICH pass 1 (S150) — A2.3 in the S143 plan; the descent's THIRD
build+enrich dip (Matt-picked over the cheaper B1 L2 round). The most-isolated A2 arc: Arya's
House-of-Black-and-White identity-dissolution journey had ZERO event nodes despite Arya being a
saturated 153-edge character. This dip BUILDS the spine from scratch (8 event nodes across 6
chapters: ASOS XIII -> AFFC Arya I/II/Cat -> ADWD Blind-Girl/Ugly-Little-Girl) + the two missing
keystone artifacts (the iron coin, the finger knife), and wires the few genuine cross-arc seams.

Ten new nodes (NO container tag — Braavos is not one of the 5 approved containers):
  events:  arya-departs-for-braavos, arya-arrives-at-the-house-of-black-and-white,
           arya-becomes-cat-of-the-canals, arya-hides-needle-beneath-the-temple-steps,
           killing-of-dareon, blinding-of-arya, arya-trains-blind-and-regains-her-sight,
           arya-assassinates-the-insurance-broker
  objects: iron-coin, finger-knife

44 edges (see candidates.json). Identity layers handled by arya-stark's EXISTING aliases
(Salty/Cat/Blind Beth/...) + the event.deception nodes — NO persona character nodes (the
Sansa-Alayne + Theon-Reek convention). Marquee seams: the iron coin ENABLES the departure
(Harrenhal -> Braavos, the only edge that makes the arc reachable); dareon MOTIVATES arya
(the Ned's-justice execution of a deserter); the kill-list CONTRASTS the Faceless Men.

Reads working/enrichment/arya-braavos/candidates.json; RE-GREPS each quote for the authoritative
line (FAIL-fast if a quote moved). Safeguards mirror prior enrichment mints: backup, re-run guard,
slug pre-check (new nodes excluded). Additive only — retirements/adjustments live in finalize."""
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
NODES_ARTIFACTS = REPO / "graph" / "nodes" / "artifacts"
CAND = REPO / "working" / "enrichment" / "arya-braavos" / "candidates.json"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-arya-braavos-enrichment-2026-06-26.jsonl"

RUN_ID = "arya-braavos-enrichment-s150"
PRODUCED_AT = "2026-06-26T00:00:00+00:00"

NEW_NODE_SLUGS = {
    "arya-departs-for-braavos",
    "arya-arrives-at-the-house-of-black-and-white",
    "arya-becomes-cat-of-the-canals",
    "arya-hides-needle-beneath-the-temple-steps",
    "killing-of-dareon",
    "blinding-of-arya",
    "arya-trains-blind-and-regains-her-sight",
    "arya-assassinates-the-insurance-broker",
    "iron-coin",
    "finger-knife",
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
        "typed_by": "curator-arya-braavos-enrichment",
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

DEPARTS = """\
---
name: "Arya departs for Braavos"
type: event.incident
slug: arya-departs-for-braavos
aliases: ["Arya boards the Titan's Daughter", "Arya sails for Braavos"]
confidence: tier-1
era: current-narrative
pass_origin: s150-arya-braavos-enrich
node_version: 1
evidence_chapters:
  - ASOS Arya XIII
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Arya departs for Braavos

At [Saltpans](saltpans), having left [Sandor](sandor-clegane) dying and her old life behind,
[Arya](arya-stark) buys passage on the Braavosi galleas *Titan's Daughter* under
[Captain Ternesio Terys](ternesio-terys). When her silver proves too little, she presses into his
hand the small black [iron coin](iron-coin) that [Jaqen H'ghar](jaqen-hghar) gave her at
[Harrenhal](harrenhal) and speaks the words — **"Valar morghulis."** The captain answers *"Valar
dohaeris"* and grants her a cabin. The coin is the precondition that opens the entire Braavos arc:
the Harrenhal three-deaths gift, redeemed. (The departure node anchors the
[iron coin](iron-coin) ENABLES seam wiring the ACOK Harrenhal cluster forward into Braavos.)

## Quotes

> "It's not silver." Her fingers closed on it. "It's iron. Here." She pressed it into his hand, the small black iron coin that Jaqen H'ghar had given her, so worn the man whose head it bore had no features.

> Arya crossed her arms against her chest. "Valar morghulis," she said, as loud as if she'd known what it meant.
"""

ARRIVES = """\
---
name: "Arya arrives at the House of Black and White"
type: event.incident
slug: arya-arrives-at-the-house-of-black-and-white
aliases: ["Arya comes to the House of Black and White", "the skull test"]
confidence: tier-1
era: current-narrative
pass_origin: s150-arya-braavos-enrich
node_version: 1
evidence_chapters:
  - AFFC Arya I
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Arya arrives at the House of Black and White

The *Titan's Daughter* passes beneath the [Titan of Braavos](titan-of-braavos) into the lagoon;
Yorko rows [Arya](arya-stark) to the covered dock of the [House of Black and White](house-of-black-and-white),
the windowless grey temple on its rocky knoll. She climbs to the weirwood-and-ebony doors, shows the
[iron coin](iron-coin), and says *"Valar morghulis."* Inside, among the statues of a hundred gods and
the black pool, the [kindly man](kindly-man) tests her courage: he lowers his cowl to a worm-eaten
**skull** — *"Kiss me, child"* — and she kisses it and tries to eat the grave-worm. The skull melts
into a gentle old face. The [waif](waif) watches. Asked her name, Arya cycles Salty -> Squab ->
Nan/Weasel -> Arry -> **Arya of House Stark** — and is told the House is no place for Arya of House Stark.

## Quotes

> The left-hand door was made of weirwood pale as bone, the right of gleaming ebony. In their center was a carved moon face; ebony on the weirwood side, weirwood on the ebony.

> The priest lowered his cowl. Beneath he had no face; only a yellowed skull with a few scraps of skin still clinging to the cheeks, and a white worm wriggling from one empty eye socket. "Kiss me, child," he croaked, in a voice as dry and husky as a death rattle.
"""

BECOMES_CAT = """\
---
name: "Arya becomes Cat of the Canals"
type: event.deception
slug: arya-becomes-cat-of-the-canals
aliases: ["Arya becomes a novice of the Faceless Men", "Arya takes the Cat of the Canals identity", "Cat of the Canals"]
confidence: tier-1
era: current-narrative
pass_origin: s150-arya-braavos-enrich
node_version: 1
evidence_chapters:
  - AFFC Arya II
  - AFFC Cat of the Canals
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Arya becomes Cat of the Canals

To serve the Many-Faced God, [Arya](arya-stark) must surrender everything she is. She throws her
Westeros things — fork, hat, boots, coins, swordbelt, clothes — into the canal, keeping only
[Needle](needle), which she [hides beneath a loose temple step](arya-hides-needle-beneath-the-temple-steps).
She answers *"No one"* when the [kindly man](kindly-man) asks who she is, and becomes a novice. He
sends her into the city under a cover identity — *Cat, an orphan of King's Landing* — to push
[Brusco](brusco)'s barrow and sell cockles and oysters at Ragman's Harbor. The textbook
identity-assumption beat of the arc (the `event.deception` sibling of
[sansa-adopts-the-alayne-stone-identity](sansa-adopts-the-alayne-stone-identity)) — but the kill-list
she still whispers each night marks the surrender as incomplete.

## Quotes

> "Cat." He considered. "Yes. Braavos is full of cats. One more will not be noticed. You are Cat, an orphan of . . ."

> "from that moment she was a novice in the House of Black and White."
"""

HIDES_NEEDLE = """\
---
name: "Arya hides Needle beneath the temple steps"
type: event.deception
slug: arya-hides-needle-beneath-the-temple-steps
aliases: ["Arya keeps Needle", "Needle hidden on the House of Black and White steps"]
confidence: tier-1
era: current-narrative
pass_origin: s150-arya-braavos-enrich
node_version: 1
evidence_chapters:
  - AFFC Arya II
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Arya hides Needle beneath the temple steps

Commanded to give up all she owns, [Arya](arya-stark) discards everything into the canal — except
[Needle](needle), [Jon Snow](jon-snow)'s gift and the synecdoche of her whole Stark self (*"Needle
was Robb and Bran and Rickon, her mother and her father, even Sansa"*). She cannot make herself throw
it away. Instead she hides the sword behind a loose stone on the temple stair, counting the steps so
she can find it again. The moral seam of the arc: at the moment of maximum identity-surrender,
something Stark-core survives. The Many-Faced God can have the rest, *but he can't have this*.
(SUB_BEAT of [Arya becomes Cat of the Canals](arya-becomes-cat-of-the-canals).)

## Quotes

> Needle was Robb and Bran and Rickon, her mother and her father, even Sansa. Needle was Winterfell's grey walls, and the laughter of its people. ... Needle was Jon Snow's smile.

> "You'll be safe here," she told Needle. "No one will know where you are but me." She pushed the sword and sheath behind the step, then shoved the stone back into place, so it looked like all the other stones.
"""

KILLING_DAREON = """\
---
name: "The killing of Dareon"
type: event.incident
slug: killing-of-dareon
aliases: ["Arya kills Dareon", "the death of Dareon the singer"]
confidence: tier-1
era: current-narrative
pass_origin: s150-arya-braavos-enrich
node_version: 1
evidence_chapters:
  - AFFC Cat of the Canals
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# The killing of Dareon

At the Happy Port, Cat finds [Dareon](dareon) — the [Night's Watch](nights-watch) singer who deserted
his vows, abandoning [Sam](samwell-tarly) and Maester Aemon in Braavos — living fat and brazen as a
singer. *"He is a man of the Night's Watch... the singer should be on the Wall."* The old Stark
justice fires: [Arya](arya-stark) walks him into a twisty alley, says *"Just so,"* slits his throat,
and pushes him into a canal, keeping his boots. It is an **unauthorized** kill — she chose the target
herself, out of her own judgment, not by the Faceless Men's assignment — and that is exactly why it
costs her her eyes. (Reifies the existing `arya-stark KILLS dareon` dyad with the desertion-motive
and the blinding-consequence.)

## Quotes

> "Just so," said Cat as they stepped into the gloom of a twisty little alley.

> "Dareon is dead. The black singer who was sleeping at the Happy Port. He was really a deserter from the Night's Watch. Someone slit his throat and pushed him into a canal, but they kept his boots."
"""

BLINDING = """\
---
name: "The blinding of Arya"
type: event.incident
slug: blinding-of-arya
aliases: ["Arya is blinded", "the warm milk", "Arya loses her sight"]
confidence: tier-1
era: current-narrative
pass_origin: s150-arya-braavos-enrich
node_version: 1
evidence_chapters:
  - AFFC Cat of the Canals
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# The blinding of Arya

When Cat reports that she killed [Dareon](dareon) — for her own reasons, judging him as a deserter
rather than killing on the god's behalf — the [kindly man](kindly-man) calls it a lie that she is
"no one" and orders the [waif](waif) to bring her warm milk. *"When you slew the singer, you took
god's powers on yourself. We kill men, but we do not presume to judge them."* The milk smells burnt
and tastes bitter; [Arya](arya-stark) wakes the next morning **blind**. The blinding is at once a
punishment and the next stage of training — by her own account it came half a year early because she
killed the singer.

## Quotes

> "My throat is dry. Do me a kindness and bring a cup of wine for me and warm milk for our friend Arya, who has returned to us so unexpectedly."

> When she woke the next morning, she was blind.
"""

BLIND_TRAINING = """\
---
name: "Arya trains blind and regains her sight"
type: event.incident
slug: arya-trains-blind-and-regains-her-sight
aliases: ["Blind Beth", "the blind girl's training", "Arya recovers her sight"]
confidence: tier-1
era: current-narrative
pass_origin: s150-arya-braavos-enrich
node_version: 1
evidence_chapters:
  - ADWD The Blind Girl
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Arya trains blind and regains her sight

Sightless, [Arya](arya-stark) is trained to see without eyes. By day she begs through Braavos as
**"Blind Beth"** (a mummer's disguise the [waif](waif) builds with pox-scars and a mole); by night
the waif drills her to navigate by sound, scent and touch, and the [kindly man](kindly-man), in a
harsh disguised voice, beats her with a stick until she learns to feel the blows coming. Her warging
sharpens in the dark — at Pynto's she sees three Lyseni sailors *through the slitted yellow eyes of a
one-eared tomcat*. When she finally strikes the stick from the kindly man's hand and names him as her
attacker — proving mastery of her other senses — the bitter night-cup changes, and she wakes to see a
tallow candle burning. *She had never seen anything so beautiful.*

## Quotes

> And for a time it seemed that she could see them too, through the slitted yellow eyes of the tomcat purring in her lap.

> And come the morning, when the night wolf left her and she opened her eyes, she saw a tallow candle burning where no candle had been the night before ... She had never seen anything so beautiful.
"""

ASSASSINATION = """\
---
name: "Arya assassinates the insurance broker"
type: event.assassination
slug: arya-assassinates-the-insurance-broker
aliases: ["the coin-swap assassination", "Arya kills the insurance underwriter", "Arya earns her face"]
confidence: tier-1
era: current-narrative
pass_origin: s150-arya-braavos-enrich
node_version: 1
evidence_chapters:
  - ADWD The Ugly Little Girl
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Arya assassinates the insurance broker

Given the face of a dead ugly girl, [Arya](arya-stark) is sent to give the gift of death to an old
Braavosi maritime-insurance underwriter — a stranger she neither loves nor hates — at the
[kindly man](kindly-man)'s direction, after some wronged petitioner prayed for his death. She does
not stab him: she follows a shipowner who deals with him, slits the man's purse with her
[finger knife](finger-knife), and swaps in a poisoned Westerosi gold dragon. The shipowner pays it to
the underwriter; *"soon after that man's heart gave out."* Her first kill **for the god** rather than
for herself — the inverse of [Dareon](killing-of-dareon). For it she is given back the face of Arya
Stark and an acolyte's robe, and sent on to Izembaro. (The published arc ends here; *Mercy* is a TWOW
preview, not minted.)

## Quotes

> Her blade flashed out, smooth and quick, one deep slash through the velvet and he never felt a thing. ... She slipped her hand through the gap, slit the purse open with the finger knife, filled her fist with gold ...

> "And with that coin and the others in his purse, he paid a certain man. Soon after that man's heart gave out. Is that the way of it? Very sad."
"""

IRON_COIN = """\
---
name: "Iron coin"
type: object.artifact
slug: iron-coin
aliases: ["the iron coin", "Jaqen's coin", "the coin of the Faceless Men"]
confidence: tier-1
era: current-narrative
pass_origin: s150-arya-braavos-enrich
node_version: 1
wiki_source: "https://awoiaf.westeros.org/index.php/Iron_coin"
---

# Iron coin

A small, worn black [iron](iron) coin bearing a head whose features have rubbed away, given by
[Jaqen H'ghar](jaqen-hghar) to [Arya Stark](arya-stark) at [Harrenhal](harrenhal) as a token of the
[Faceless Men](faceless-men): *"give that coin to any man from Braavos, and say these words to
him—valar morghulis."* It is not currency but a key. Arya uses it to buy passage on the
[Titan's Daughter](titan-of-braavos) when her silver runs short, and again at the doors of the
[House of Black and White](house-of-black-and-white) to gain entry. The single object that wires the
ACOK Harrenhal arc forward into the Braavos arc.

## Quotes

> She pressed it into his hand, the small black iron coin that Jaqen H'ghar had given her, so worn the man whose head it bore had no features.

> "Jaqen told me to come. I have the iron coin." She pulled it from her pouch and held it up. "See? Valar morghulis."
"""

FINGER_KNIFE = """\
---
name: "Finger knife"
type: object.artifact
slug: finger-knife
aliases: ["the finger knife", "Cat's finger knife"]
confidence: tier-1
era: current-narrative
pass_origin: s150-arya-braavos-enrich
node_version: 1
---

# Finger knife

A small concealed blade [Arya Stark](arya-stark) carries as Cat of the Canals, kept very sharp and
hidden up her sleeve. Red Roggo taught her to use it at the Happy Port — how to slip it out at need
and *"slice a purse so smooth and quick the coins would all be spent before their owner ever missed
them."* The skill is the mechanism of her first Faceless-Men kill: at the
[assassination of the insurance broker](arya-assassinates-the-insurance-broker) she uses the finger
knife not to kill the target but to slit a shipowner's purse and plant the poisoned coin.

## Quotes

> Once in a great while that would make somebody angry, but when it did she had her finger knife. She kept it very sharp, and knew how to use it too.

> Her blade flashed out, smooth and quick, one deep slash through the velvet and he never felt a thing. ... slit the purse open with the finger knife, filled her fist with gold ...
"""

NODES = [
    ("arya-departs-for-braavos", NODES_EVENTS, DEPARTS),
    ("arya-arrives-at-the-house-of-black-and-white", NODES_EVENTS, ARRIVES),
    ("arya-becomes-cat-of-the-canals", NODES_EVENTS, BECOMES_CAT),
    ("arya-hides-needle-beneath-the-temple-steps", NODES_EVENTS, HIDES_NEEDLE),
    ("killing-of-dareon", NODES_EVENTS, KILLING_DAREON),
    ("blinding-of-arya", NODES_EVENTS, BLINDING),
    ("arya-trains-blind-and-regains-her-sight", NODES_EVENTS, BLIND_TRAINING),
    ("arya-assassinates-the-insurance-broker", NODES_EVENTS, ASSASSINATION),
    ("iron-coin", NODES_ARTIFACTS, IRON_COIN),
    ("finger-knife", NODES_ARTIFACTS, FINGER_KNIFE),
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
