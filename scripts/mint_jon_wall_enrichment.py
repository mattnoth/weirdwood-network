#!/usr/bin/env python3
"""Mint Jon Snow / the Wall enrichment pass 1 (S145) — eleventh major-arc enrichment dip;
A1.2 in the S143 reopened L1 round (the second spine-only heavyweight after Daenerys/Meereen).

The NORTH spine (N1-N6) was built S125-S126, but Jon himself was 348 edges / 0 arc-connected:
his graph presence was wiki-dyadic social web, not the causal event substrate. This pass wires
the texture the assassination spine lacked. Two new nodes:

  - `the-shieldhall-speech` (event.incident) — the missing trigger beat. The spine had
    `pink-letter-delivered TRIGGERS jon-is-stabbed-repeatedly` directly, collapsing the speech
    where Jon reads the Pink Letter aloud, calls to march on Winterfell, and the conspirators
    walk out. Now a 2-cause convergence hub: pink-letter ENABLES + hardhome ENABLES -> speech
    TRIGGERS stabbing.
  - `hardhome-catastrophe` (event.incident) — the revelation-event (Cotter Pyke's letter:
    "Dead things in the woods. Dead things in the water."). The off-page disaster known only
    through the letter; it MOTIVATES Jon and is the stated reason for the Shieldhall assembly.

The work (synthesis of 4 fresh Sonnet lenses over the built unit):
  - THE WHODUNIT (marquee): Othell Yarwyck / Left Hand Lew / Alf of Runnymudd SUSPECTED_OF the
    stabbing (Bowen's Shieldhall cluster + the joint exit; AGENT_IN reserved for the named
    stabbers Bowen+Wick who are already wired); Yarwyck CONSPIRES_WITH Bowen + the parallel
    free-folk grievance MOTIVATES edge.
  - THE GLAMOUR: mance IMPERSONATES lord-of-bones + lord-of-bones DISGUISED_AS mance (the
    double-swap; resolves the "Mance Rayder" alias collision on lord-of-bones), melisandre
    AGENT_IN + MANIPULATES (ruby fetter), lord-of-bones VICTIM_IN the burning (the real victim).
  - CROSS-CONTAINER SEAMS (lens 4): stall-at-crofters-village ENABLES pink-letter (lights a
    dead-end node); mance-execution ENABLES pink-letter (the glamour lets Mance reach Winterfell,
    which the letter taunts about); alys REVEALS the Arnolf-Bolton trap; cregan IMPRISONED_AT.
  - OBJECT/POLITICS DEPTH: jon WARGS_INTO ghost (first-use WARGS_INTO), longclaw WIELDED_IN the
    stabbing (the sword he can't draw), tormund AGENT_IN the free-folk decree, patrek COURTS val.

POST-VERIFY MODIFICATIONS (NOT in this additive mint — applied after fresh-verify, see
candidates.json.post_verify_modifications): retire the now-superseded direct
`pink-letter-delivered TRIGGERS jon-is-stabbed-repeatedly`; retire the factually-false
`mance-rayder VICTIM_IN mance-rayder-brought-to-execution` (Rattleshirt burned, Mance lived).
ALIAS hygiene: drop "Mance Rayder" from lord-of-bones.node.md.

Reads working/enrichment/jon-wall/candidates.json; RE-GREPS each quote in its chapter file for
the authoritative line (FAIL-fast if a quote moved). Safeguards mirror the prior enrichment
mints: backup, re-run guard, slug pre-check (new nodes excluded).

Theory gate: Jon's parentage / Azor Ahai NOT engaged — evidence edges only.
"""
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
CAND = REPO / "working" / "enrichment" / "jon-wall" / "candidates.json"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-jon-wall-enrichment-2026-06-25.jsonl"

RUN_ID = "jon-wall-enrichment-s145"
PRODUCED_AT = "2026-06-25T00:00:00+00:00"

NEW_NODE_SLUGS = {"the-shieldhall-speech", "hardhome-catastrophe"}


def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def authoritative_line(book, chapter, quote):
    """Grep the whole chapter file for the normalized quote; return its 1-indexed line."""
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
        "typed_by": "curator-jon-wall-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


# ════════════════════════════ NODE BODIES ════════════════════════════

SHIELDHALL = """\
---
name: "The Shieldhall speech"
type: event.incident
slug: the-shieldhall-speech
aliases: ["Shieldhall speech", "Jon's Shieldhall address", "Jon reads the Pink Letter aloud", "the march on Winterfell announcement"]
confidence: tier-1
era: war-of-the-five-kings
containers: [north]
pass_origin: s145-jon-wall-enrich
node_version: 1
evidence_chapters:
  - ADWD Jon XIII
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# The Shieldhall speech

After the [Pink Letter](pink-letter-delivered) arrives, [Jon Snow](jon-snow) summons the leading
men of Castle Black and the free folk to the [Shieldhall](shieldhall). He reads Ramsay Bolton's
letter aloud, abandons the planned ranging to the relief of [Hardhome](hardhome-catastrophe), and
announces he will ride south to Winterfell — calling for any man who will stand with him. The
wildlings, who outnumber the black brothers five to one, roar to follow; [Bowen Marsh](bowen-marsh),
[Othell Yarwyck](othell-yarwyck), and their faction slip out of the hall. Minutes later they
murder Jon outside the armory. The speech is the proximate trigger of the assassination — the
moment Jon's vow-breaking becomes public and irreversible in the conspirators' eyes.

## Edges
(Edges in `graph/edges/edges.jsonl`, S145 Jon/Wall enrichment. ENABLES-in from
[the Pink Letter](pink-letter-delivered) + [the Hardhome catastrophe](hardhome-catastrophe) +
[the free-folk decree](jon-allows-free-folk-through-the-wall) [2-cause convergence];
TRIGGERS [the stabbing](jon-is-stabbed-repeatedly); [Jon](jon-snow) AGENT_IN; LOCATED_AT
[the Shieldhall](shieldhall).)

## Quotes

> There is still much to decide. Spread the word. I want all the leading men in the Shieldhall when the evening watch begins.

— Jon Snow, ADWD Jon XIII (`sources/chapters/adwd/adwd-jon-13.md:113`)

> When Jon and Tormund entered, a sound went through the hall, like wasps stirring in a nest.

— ADWD Jon XIII (`sources/chapters/adwd/adwd-jon-13.md:279`)

> Yarwyck and Marsh were slipping out, he saw, and all their men behind them. It made no matter. He did not need them now. He did not want them. No man can ever say I made my brothers break their vows. If this is oathbreaking, the crime is mine and mine alone.

— ADWD Jon XIII (`sources/chapters/adwd/adwd-jon-13.md:299`)
"""

HARDHOME = """\
---
name: "The Hardhome catastrophe"
type: event.incident
slug: hardhome-catastrophe
aliases: ["the Hardhome disaster", "the Hardhome letter", "Cotter Pyke's letter from Hardhome", "dead things in the water"]
confidence: tier-1
era: war-of-the-five-kings
containers: [north]
pass_origin: s145-jon-wall-enrich
node_version: 1
evidence_chapters:
  - ADWD Jon XII
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-reported
---

# The Hardhome catastrophe

[Cotter Pyke](cotter-pyke)'s fleet reaches [Hardhome](hardhome) to evacuate thousands of free
folk trapped and starving on the shore, and the relief turns to disaster: ships lost in wild
seas, wildlings eating their own dead, "dead things in the woods" and "dead things in the water,"
attempts to take refugees aboard defeated with crew dead. The catastrophe is known to
[Jon Snow](jon-snow) only through the letter Cotter Pyke sends back — a revelation-event that
confirms the Others are already moving and transforms Jon's wildling policy from pragmatism into
existential urgency. It is the stated reason for the [Shieldhall assembly](the-shieldhall-speech)
that gets him killed.

## Edges
(Edges in `graph/edges/edges.jsonl`, S145 Jon/Wall enrichment. LOCATED_AT [Hardhome](hardhome);
[Cotter Pyke](cotter-pyke) AGENT_IN; MOTIVATES [Jon](jon-snow); ENABLES
[the Shieldhall speech](the-shieldhall-speech). The off-page battle is unnarrated in ADWD —
this node represents the REVELATION, i.e. the letter, not a witnessed battle.)

## Quotes

> At Hardhome, with six ships. Wild seas. Blackbird lost with all hands ... Wildlings eating their own dead. Dead things in the woods. ... Eight ravens left. Dead things in the water. Send help by land, seas wracked by storms. From Talon, by hand of Maester Harmune.

— Cotter Pyke's letter, ADWD Jon XII (`sources/chapters/adwd/adwd-jon-12.md:263`)

> Dead things in the wood. Dead things in the water. Six ships left, of the eleven that set sail. Jon Snow rolled up the parchment, frowning. Night falls, he thought, and now my war begins.

— ADWD Jon XII (`sources/chapters/adwd/adwd-jon-12.md:271`)
"""

NODES = [
    ("the-shieldhall-speech", NODES_EVENTS, SHIELDHALL),
    ("hardhome-catastrophe", NODES_EVENTS, HARDHOME),
]


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
    if e.get("verify"):
        row["verified_by"] = "pending"
    return row


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
    print(f"edges.jsonl: {len(existing)} -> {len(out)} lines (+{len(new_rows)})")


if __name__ == "__main__":
    main()
