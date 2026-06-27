#!/usr/bin/env python3
"""Mint A1.5 "Dorne / Queenmaker" enrichment (S156) — the 20th major-arc enrichment dip and the SECOND
of the 🅰 A-roundup campaign (Matt S154). The Dorne spine was built S117 (the Queenmaker plot) with 0
enrichment dips; the baseline dedup pull found 196 unique internal edges but only 9 internal CAUSAL edges
(a thin causal spine + an under-wired conspirator web). So this is WIRE + ENRICH.

Three new nodes (NO container tag — Dorne is NOT one of the 5 approved containers):
  garin-of-the-orphans   (character.human)  -- fixes the wrong-target bug (arianne CONSPIRES_WITH
                                                garin-the-great pointed at the legendary Rhoynar prince)
  hotahs-longaxe         (object.artifact)  -- Hotah's ash-and-iron 'wife'; lit 0-edge -> 3 edges
  spear-tower            (place.location)   -- Arianne's captivity tower; lit -> the IMPRISONED_AT cluster

39 edges (see candidates.json). KEY synthesis calls (4-lens convergence + whole-file line-check, 39/39):
  - MARQUEE Arys 'soiled knight' sub-arc: arianne MANIPULATES arys via_seduction (the half-year seduction
    that turned the Kingsguard into the plot's instrument) + DECEIVES via the false marriage promise +
    arys BREAKS_VOW tommen + ATTACKS areo (the suicide charge). The LOVER_OF edge pre-existed; MANIPULATES
    adds the using-him-as-a-tool layer.
  - The conspirator web (all 4 lenses converged + the bug): minted garin-of-the-orphans; Garin/Drey/Sylva
    AGENT_IN + CONSPIRES_WITH; the dispersal (Drey->Norvos, Garin->Tyrosh, Sylva MARRIES_OFF->Greenstone).
  - The WHODUNIT done HONESTLY (the marquee Dorne lens): NO informer SUSPECTED_OF is minted. The text
    leaves 'someone always tells' (Hotah) deliberately unproven — Arianne cycles through suspects and
    reaches no conclusion, Doran refuses to name the informer. Minting an informer edge would assert what
    the published text does not prove. INSTEAD the whodunit value is the structural irony
    doran MANIPULATES arianne via_false_information (the false-suitor ploy concealing the betrothal pact —
    his concealment CAUSED the plot) + the cover-story DECEIVES balon-swann (Darkstar-killed-Arys, the
    official lie) + gerold OPPOSES the-queenmaker-plot (the saboteur-within who maimed Myrcella to spark
    the war the plot was avoiding; he is AGENT_IN the plot yet scorned its method).
  - Cross-arc seams: murder-of-elia MOTIVATES doran (Sack-of-KL -> Dorne; parallels the existing
    ...MOTIVATES oberyn — Doran's long-game had no stated root); myrcella CLAIMS iron-throne (the FIRST
    CLAIMS-iron-throne edge in the graph, the Dornish-primogeniture premise of the plot); the Sand-Snake
    forward-dispatch to KL/High-Hermitage (Obara/Nym/Tyene) wiring Dorne into the KL arc.
  - Descriptive de-islanding: hotahs-longaxe (WIELDS + WIELDED_IN + KILLED_WITH); water-gardens (was 0
    edges to the Dorne core -> LOCATED_AT/REGION_OF); ghaston-grey/sea-of-dorne/spear-tower lit.
  - THEORY-GATED (node-prose only, NO edges): Aegon-is-real / fAegon-is-a-Blackfyre; the full 'fire and
    blood' Dornish-vengeance PROPHECY reading; any R+L-adjacent Elia/Rhaegar theory. Evidence/MOTIVATES->
    character edges only.
  - HELD THE LINE: NO re-mint of the S117 Queenmaker spine / myrcella-is-maimed-by-darkstar / arianne
    WITNESS_IN the maiming (DEDUP); NO informer SUSPECTED_OF; NO maiming-MOTIVATES-doran (cOut=0 left a
    terminus — its real downstream is TWOW); NO container tag.

The bug-retire (`arianne CONSPIRES_WITH garin-the-great` -> drop) lives in finalize_dorne_s156.py, with the
fresh-verify drops/adjusts + verified_by stamps. Reads candidates.json; RE-GREPS each quote (FAIL-fast).
Additive only."""
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
NODES = REPO / "graph" / "nodes"
CAND = REPO / "working" / "enrichment" / "dorne" / "candidates.json"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-dorne-enrichment-2026-06-27.jsonl"

RUN_ID = "dorne-enrichment-s156"
PRODUCED_AT = "2026-06-27T00:00:00+00:00"

NEW_NODE_SLUGS = {
    "garin-of-the-orphans",
    "hotahs-longaxe",
    "spear-tower",
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
        "typed_by": "curator-dorne-enrichment",
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


# ════════════════════════════ NODE BODIES (no container tag — Dorne) ════════════════════════════

GARIN = """\
---
name: "Garin (orphan of the Greenblood)"
type: character.human
slug: garin-of-the-orphans
aliases: ["Garin of the orphans", "gay Garin"]
confidence: tier-1
era: current-narrative
pass_origin: s156-dorne-enrich
node_version: 1
---

# Garin (orphan of the Greenblood)

Garin is [Arianne Martell](arianne-martell)'s milk-brother — his mother was her wet nurse — and one of her
five lifelong companions: a loose-limbed, swarthy, long-nosed [orphan of the Greenblood](orphans-of-the-greenblood)
(the Rhoynar river people), with a jade stud in one ear and a golden tooth Arianne bought him. He is one of
the conspirators in [the Queenmaker plot](the-queenmaker-plot) — he gathered the firewood at the Shandystone
rendezvous, greeted [Myrcella](myrcella-baratheon) as queen, and arranged the poleboat on the Greenblood for
the planned escape. When [Areo Hotah](areo-hotah) sprang the ambush, Garin yielded with his hands in the air.
[Prince Doran](doran-martell) sentenced him to two years in Tyrosh, taking coin and hostages from his orphan kin.

**Bug-fix note (S156):** this node is the conspirator Garin, distinct from the legendary Rhoynar prince
`garin-the-great` (dead ~1,000 years). The mis-pointed edge `arianne CONSPIRES_WITH garin-the-great` was
retired and replaced by `garin-of-the-orphans CONSPIRES_WITH arianne-martell`.

## Quotes

> Here is gay Garin of the orphans, who makes me laugh. His mother was my wet nurse.

> I'm of the orphans of the Greenblood, is what my lady means.
"""

HOTAHS_LONGAXE = """\
---
name: "Areo Hotah's Longaxe"
type: object.artifact
slug: hotahs-longaxe
aliases: ["Hotah's longaxe", "the ash-and-iron wife", "the captain's longaxe"]
confidence: tier-1
era: current-narrative
pass_origin: s156-dorne-enrich
node_version: 1
---

# Areo Hotah's Longaxe

The longaxe [Areo Hotah](areo-hotah) has borne for some thirty years, since the bearded priests of Norvos
branded him and set him to guard [House Martell](house-martell). Its head sits on a shaft of mountain ash six
feet long, honed sharp enough to shave with; Hotah keeps it oiled and whetted, sleeps beside it, and calls it
his "ash-and-iron wife" (the Norvoshi custom — a novice weds his axe). It is the instrument with which he
springs the ambush on the Greenblood and beheads [Ser Arys Oakheart](arys-oakheart).

## Quotes

> Areo Hotah ran his hand along the smooth shaft of his longaxe, his ash-and-iron wife, all the while watching.

> Hotah's longaxe took his right arm off at the shoulder, spun away spraying blood, and came flashing back again in a terrible two-handed slash that removed the head of Arys Oakheart.
"""

SPEAR_TOWER = """\
---
name: "Spear Tower"
type: place.location
slug: spear-tower
aliases: ["the Spear Tower"]
confidence: tier-1
era: current-narrative
pass_origin: s156-dorne-enrich
node_version: 1
---

# Spear Tower

The slender Spear Tower is one of the three towers of the [Old Palace of Sunspear](old-palace) — a hundred
and fifty feet tall, crowned with a thirty-foot spear of gilded steel — alongside the Tower of the Sun and
the Sandship. After the Queenmaker plot collapses, [Areo Hotah](areo-hotah) confines [Arianne Martell](arianne-martell)
in an airy cell near its top (the "Princess in the Tower"), and [Prince Doran](doran-martell) orders the three
elder [Sand Snakes](sand-snakes) — [Obara](obara-sand), [Nymeria](nymeria-sand), and [Tyene](tyene-sand) —
held in the cells atop it.

## Quotes

> First the slender Spear Tower, a hundred-and-a-half feet tall and crowned with a spear of gilded steel that added another thirty feet to its height.

> You will find my brother's daughters, take them into custody, and confine them in the cells atop the Spear Tower.
"""

NODE_SPECS = [
    ("garin-of-the-orphans", NODES / "characters", GARIN),
    ("hotahs-longaxe", NODES / "artifacts", HOTAHS_LONGAXE),
    ("spear-tower", NODES / "locations", SPEAR_TOWER),
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
    for slug, node_dir, body in NODE_SPECS:
        p = node_dir / f"{slug}.node.md"
        if p.exists():
            print(f"  SKIP node (exists): {p.name}")
        else:
            node_dir.mkdir(parents=True, exist_ok=True)
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
