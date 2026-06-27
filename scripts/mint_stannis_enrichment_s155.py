#!/usr/bin/env python3
"""Mint A2.7 "Stannis Baratheon" enrichment (S155) — the 19th major-arc enrichment dip and the FIRST
of the 🅰 A-roundup campaign (Matt S154). Stannis is NOT a POV; his arc is told across Davos/Catelyn/
Jon/Asha POVs and is HEAVILY pre-wired via the Blackwater (S138) and NORTH (S125-126) spines — the
baseline dedup pull found 409 unique internal edges but only 10 internal CAUSAL edges (the Class-D
profile: dense dyadic web, causally-ISLANDED event hubs). So this is WIRE + ENRICH, and the dip's
value is the MOTIVATES/causal substrate the spine lacked.

Three new event nodes (NO container tag — Dragonstone/Renly's-war, matches the S148-S150 A2 arcs):
  burning-of-the-seven-at-dragonstone, shadow-killing-of-cortnay-penrose, leeching-of-edric-storm

31 edges (see candidates.json). KEY synthesis calls (4-lens convergence + whole-file line-check, 31/31):
  - MARQUEE conversion engine: lit lightbringer's 0-edges-graph-wide island (stannis WIELDS + WIELDED_IN
    the burning), minted the missing `stannis WORSHIPS rhllor` (only selyse had it) + `melisandre ADVISES
    stannis` (the single most-named missing edge — Mel had SERVES/COMMANDED-by/COMPANION_OF/LOVER_OF/TRUSTS
    but no ADVISES).
  - The SECOND shadow (3-lens converge A/B): shadow-killing-of-cortnay-penrose is a DISTINCT event from
    shadow-assassination-of-renly (Renly died in his tent earlier; Cortnay is killed by a shadow born in
    the sea cave beneath Storm's End). ENABLES taking-of-storms-end (de-islands it; had only 1 PART_OF).
  - The Renly-kinslaying GUILT: renly-s-death-reflection MOTIVATES stannis (de-islands the cIn=0/cOut=0
    node — the continue-prompt-named gap #3).
  - Why-march-north: davos MOTIVATES stannis ("a king protects his people") — the spine had only retreat
    ENABLES move-to-wall, no character-motive.
  - Cross-container seam: murder-of-jon-arryn MOTIVATES stannis (the RR/twincest root of his claim).
  - The leeching of Edric Storm as a TEXT EVENT (3-lens converge A/B/C): melisandre+stannis AGENT_IN,
    edric VICTIM_IN, davos WITNESS_IN -> MOTIVATES davos -> davos RESCUES edric (the counter-move).
  - WHODUNIT misdirection: brienne + catelyn SUSPECTED_OF shadow-assassination-of-renly (the FALSE
    in-world accusations; Stannis AGENT_IN is the true killer).
  - THEORY-GATED (node-prose only, NO edge): Azor Ahai / Stannis-as-the-prince-that-was-promised /
    king's-blood-magic mechanics / the stone dragon / Shireen-as-future-sacrifice. The leeching, the
    burning of the Seven, and Lightbringer-the-red-sword are minted as TEXT EVENTS (events + agency/
    possession edges); the theology/prophecy READING is not asserted. NO `leeching FORESHADOWS/CAUSES`
    the three kings' deaths.
  - HELD THE LINE: did NOT re-touch the Blackwater wildfire (S138) or the NORTH Mance-glamour thread
    (S145); excluded the wiki name-collisions flight-to/fall-of-dragonstone + shadow-war (Dance/Slaver's
    Bay, NOT Stannis); dropped a redundant march-ENABLES (the march already has 2 ENABLES inbound via
    Deepwood); dropped cersei SUSPECTED_OF death-of-robert (already minted S137); the Antler Men stay a
    future B5 dip.

Reads working/enrichment/stannis/candidates.json; RE-GREPS each quote (FAIL-fast). Additive only —
fresh-verify drops/adjusts + verified_by stamps live in the finalize script."""
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
CAND = REPO / "working" / "enrichment" / "stannis" / "candidates.json"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-stannis-enrichment-2026-06-26.jsonl"

RUN_ID = "stannis-enrichment-s155"
PRODUCED_AT = "2026-06-26T00:00:00+00:00"

NEW_NODE_SLUGS = {
    "burning-of-the-seven-at-dragonstone",
    "shadow-killing-of-cortnay-penrose",
    "leeching-of-edric-storm",
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
        "typed_by": "curator-stannis-enrichment",
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


# ════════════════════════════ NODE BODIES (no container tag — Dragonstone/Renly's-war) ════════════════════════════

BURNING_OF_THE_SEVEN = """\
---
name: "Burning of the Seven at Dragonstone"
type: event.incident
slug: burning-of-the-seven-at-dragonstone
aliases: ["Stannis burns the Seven", "the burning of the gods at Dragonstone"]
confidence: tier-1
era: current-narrative
pass_origin: s155-stannis-enrich
node_version: 1
evidence_chapters:
  - ACOK Davos I
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Burning of the Seven at Dragonstone

At Dragonstone's gates, before hundreds of the assembled host, [Melisandre](melisandre) burns the seven
wooden idols of the [Faith of the Seven](faith-of-the-seven) — Maid and Mother, Warrior and Smith, Crone,
Father and Stranger — praying once each in Asshai'i, High Valyrian, and the Common Tongue. Then
[Stannis](stannis-baratheon) plunges into the pyre and wrenches a sword free of the burning wood; the
queen's men proclaim it [Lightbringer](lightbringer), "the red sword of heroes." [Selyse](selyse-florent)
echoes the responses; [Davos](davos-seaworth), watching, "felt ill … and not only from the smoke." It is
the public act of [Stannis's conversion to R'hllor](rhllor) and his break with the Faith.

This node is the **R'hllor conversion engine** the spine entirely lacked: it lights
[Lightbringer](lightbringer)'s 0-edges-graph-wide island (`stannis WIELDS` + the sword `WIELDED_IN` the
burning) and anchors the new `stannis WORSHIPS rhllor` + `melisandre ADVISES stannis` edges.

**Theory-gated (node-prose, NOT edges):** that this sword IS the prophesied Lightbringer, that Stannis is
Azor Ahai reborn / the prince that was promised, and the whole R'hllor cosmology — all evidence-only.
Davos privately judges *"That sword was not Lightbringer"* (the heatless false-Lightbringer reading); the
text event is the burning + the drawing, not the prophecy.

## Quotes

> The red woman walked round the fire three times, praying once in the speech of Asshai, once in High Valyrian, and once in the Common Tongue.

> In ancient books of Asshai it is written that there will come a day after a long summer when the stars bleed and the cold breath of darkness falls heavy on the world. In this dread hour a warrior shall draw from the fire a burning sword.

> The Seven have never brought me so much as a sparrow. It is time I tried another hawk, Davos. A red hawk.
"""

SHADOW_KILLING_OF_CORTNAY = """\
---
name: "Shadow killing of Cortnay Penrose"
type: event.assassination
slug: shadow-killing-of-cortnay-penrose
aliases: ["the second shadow", "death of Cortnay Penrose", "the shadow at Storm's End"]
confidence: tier-1
era: current-narrative
pass_origin: s155-stannis-enrich
node_version: 1
evidence_chapters:
  - ACOK Davos II
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Shadow killing of Cortnay Penrose

The **second** shadow-birth — distinct from the [shadow that killed Renly](shadow-assassination-of-renly)
in his tent. Because [Storm's End](storms-end) is warded against shadow-magic ("Dark walls that no shadow
can pass"), [Melisandre](melisandre) must be carried inside the wards: [Davos](davos-seaworth) rows her by
night into the sea cave beneath the castle, where — naked and huge with child — she births a shadow that
slips between the portcullis bars into the castle. Davos sees it go and **knows that shadow, "as he knew
the man who'd cast it."** [Ser Cortnay Penrose](cortnay-penrose), the castellan who had refused to yield
Storm's End or surrender [Edric Storm](edric-storm), is found dead the next day (officially, fallen from a
tower); command passes to the green Lord Meadows, who yields the castle.

[Stannis](stannis-baratheon) `COMMANDS_IN` it (he foreknows and orders the mission without personally
acting); Melisandre `AGENT_IN`; Cortnay `VICTIM_IN`; Davos `PARTICIPATES_IN` (rows the boat) and
`WITNESS_IN` (the perception that turns him against Melisandre). The death `ENABLES`
[taking-of-storms-end](taking-of-storms-end).

## Quotes

> Ser Cortnay will be dead within the day. Melisandre has seen it in the flames of the future. His death and the manner of it.

> The last time it was life I brought to Storm's End, shaped to look like onions. This time it is death, in the shape of Melisandre of Asshai.

> He knew that shadow. As he knew the man who'd cast it.
"""

LEECHING_OF_EDRIC_STORM = """\
---
name: "Leeching of Edric Storm"
type: event.incident
slug: leeching-of-edric-storm
aliases: ["the king's blood leeches", "the three usurpers leeching"]
confidence: tier-1
era: current-narrative
pass_origin: s155-stannis-enrich
node_version: 1
evidence_chapters:
  - ASOS Davos IV
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Leeching of Edric Storm

In the Chamber of the Painted Table at [Dragonstone](dragonstone), [Melisandre](melisandre) presents a
covered silver dish holding three black leeches fat with the king's-blood of [Edric Storm](edric-storm)
(Robert's acknowledged bastard, taken at Storm's End and "leeched" while sick). [Stannis](stannis-baratheon)
takes each leech in turn, names it for a usurper — *"the usurper Joffrey," "the usurper Balon," "the usurper
Robb"* — and throws it into the brazier to burn. [Davos](davos-seaworth) watches, knowing *"the boy's blood
… a king's blood,"* and the horror hardens his resolve to get Edric off the island.

This wires the king's-blood thread the spine left as three islanded "queen's-men urge sacrifice" stubs:
Melisandre + Stannis `AGENT_IN`, Edric `VICTIM_IN`, Davos `WITNESS_IN`; the leeching `MOTIVATES` Davos →
[Davos `RESCUES` Edric](edric-storm) (smuggled to Lys on a Lyseni galley — the counter-move).

**Theory-gated (node-prose, NOT edges):** that king's-blood magic WORKS, that the leeching CAUSES the
subsequent deaths of Joffrey (Purple Wedding), Balon, and Robb (Red Wedding), the stone dragon, and the
Azor-Ahai / Nissa-Nissa reading of a future Shireen/Edric sacrifice — all evidence-only. The text event is
the leeching + the naming; no `FORESHADOWS`/`CAUSES` edge to the three kings' deaths is minted.

## Quotes

> The boy's blood, Davos knew. A king's blood.

> If I must sacrifice one child to the flames to save a million from the dark . . . Sacrifice . . . is never easy, Davos. Or it is no true sacrifice.
"""

NODES = [
    ("burning-of-the-seven-at-dragonstone", NODES_EVENTS, BURNING_OF_THE_SEVEN),
    ("shadow-killing-of-cortnay-penrose", NODES_EVENTS, SHADOW_KILLING_OF_CORTNAY),
    ("leeching-of-edric-storm", NODES_EVENTS, LEECHING_OF_EDRIC_STORM),
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
