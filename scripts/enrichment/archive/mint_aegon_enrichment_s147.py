#!/usr/bin/env python3
"""Mint AEGON / Golden Company enrichment pass 1 (S147) — twelfth major-arc enrichment dip;
A1.3 in the S143 reopened L1 round, the LAST spine-only heavyweight (after Dany S144 /
Jon S145 / Bran S146).

The AEGON spine (conspiracy -> reveal -> sail-west -> landing -> {Stormlands campaign, KL
assassinations}) was built S128, but the container was bare scaffolding: thin role layers,
no off-spine substrate, the assassinations hub had 0 outgoing edges, and the Golden Company's
officer corps + the Shy Maid household were almost entirely unwired. This pass (synthesis of 4
fresh Sonnet lenses over the built unit) wires the texture.

Three new nodes:
  - `illyrios-ruby-chain` (object.artifact) — Illyrio's gift to Aegon worn at the reveal,
    "three huge square-cut rubies on a chain of black iron... Red and black. Dragon colors."
  - `varys-crossbow` (object.artifact) — the ADWD-epilogue assassination weapon; Varys names
    the Tywin echo ("the crossbow fitting... you shared so much with Lord Tywin"). PARALLELS
    tywins-crossbow.
  - `kevan-reconciles-the-realm` (event.incident, [wo5k]) — Kevan's on-page regency project
    (reconcile Highgarden + Casterly Rock, bind the Faith, unite under Tommen); the thing the
    assassinations PREVENT. Minted ONLY to resolve the assassinations 0-outgoing dead-end.
    BORDERLINE — flagged for fresh-verify (re-modeling KL politics?).

The work:
  - THE MARQUEE: `jon-connington AFFLICTED_BY greyscale` (FIRST-USE of AFFLICTED_BY in graph) +
    `greyscale MOTIVATES jon-connington` (the death-clock drives his haste; routes through the
    actor, parallels maggy->cersei). Infection vector = pulling Tyrion from the Rhoyne.
  - WHODUNIT / HIDDEN AGENCY: varys DECEIVES golden-company (Connington's fake disgrace);
    varys REVEALS_TO kevan (the terminal lift of the 15-yr survival-concealment); jon-connington
    DECEIVES golden-company (the Griff identity); tyrion MANIPULATES aegon (the cyvasse goad,
    via_false_information — "I lied").
  - GC OFFICER CORPS + SIMULTANEOUS-COLUMNS COMMAND: jon-con AGENT_IN the reveal + 5 council
    participants; the column commanders (Connington/Flowers -> Griffin's Roost, Rivers -> Crow's
    Nest, Peake -> Rain House, Mandrake -> Greenstone, Edoryen/Balaq -> the landing); aegon
    COMMANDS_IN the Storm's End siege ("I mean to lead it"); strickland OPPOSES the sail-west;
    golden-company NEGOTIATES_WITH yunkai (the broken offer).
  - THE SHY MAID HOUSEHOLD: 5 TRAVELS_WITH aegon (yandry/ysilla/haldon/lemore/duck) + duck
    PROTECTS + TEACHES; yandry CAPTAIN_OF + ysilla CREW_OF the shy-maid.
  - OBJECTS: the ruby chain (GIFTED_TO + OWNS); the varys-crossbow (WIELDS + WIELDED_IN +
    PARALLELS tywins-crossbow).
  - STRUCTURAL: assassinations PREVENTS kevan-reconciles-the-realm (resolves 0-outgoing).

Theory gate: Aegon-Blackfyre / fAegon babe-swap / mummer's-dragon NOT engaged — all edges target
`aegon-targaryen-young-griff`; identity doubt is harvest-only. DROPPED at synthesis (see
candidates.json.dropped_at_synthesis): varys DISGUISED_AS rugen (no in-scope anchor),
varys MANIPULATES aegon (no qualifier fit), 2nd same-endpoint DECEIVES, griff DISGUISED_AS.

Reads working/enrichment/aegon/candidates.json; RE-GREPS each quote for the authoritative line
(FAIL-fast if a quote moved). Safeguards mirror the prior enrichment mints: backup, re-run guard,
slug pre-check (new nodes excluded).
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
NODES_ARTIFACTS = REPO / "graph" / "nodes" / "artifacts"
CAND = REPO / "working" / "enrichment" / "aegon" / "candidates.json"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-aegon-enrichment-2026-06-25.jsonl"

RUN_ID = "aegon-enrichment-s147"
PRODUCED_AT = "2026-06-25T00:00:00+00:00"

NEW_NODE_SLUGS = {"illyrios-ruby-chain", "varys-crossbow", "kevan-reconciles-the-realm"}


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
        "typed_by": "curator-aegon-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


# ════════════════════════════ NODE BODIES ════════════════════════════

RUBY_CHAIN = """\
---
name: "Illyrio's ruby chain"
type: object.artifact
slug: illyrios-ruby-chain
aliases: ["the three rubies on a chain of black iron", "Aegon's dragon-colors chain"]
confidence: tier-1
era: current-narrative
pass_origin: s147-aegon-enrich
node_version: 1
material: ruby-and-iron
evidence_chapters:
  - ADWD The Lost Lord
---

## Identity

Three huge square-cut rubies on a chain of black iron — Magister [Illyrio Mopatis](illyrio-mopatis)'s
gift to [Aegon Targaryen](aegon-targaryen-young-griff), worn at his throat when [Jon Connington](jon-connington)
reveals him to the Golden Company. "Red and black. Dragon colors." The dynastic-statement object
of the AEGON arc: the cheesemonger dressing the hidden prince in Targaryen heraldry for the moment
the long conspiracy becomes an open claim.

## Edges

(Edges in `graph/edges/edges.jsonl`, S147 AEGON enrichment. GIFTED_TO [Aegon](aegon-targaryen-young-griff)
[giver = illyrio-mopatis]; OWNS-by [Aegon](aegon-targaryen-young-griff).)

## Quotes

> With his hair washed and cut and freshly dyed a deep, dark blue, his eyes looked blue as well. At his throat he wore three huge square-cut rubies on a chain of black iron, a gift from Magister Illyrio. Red and black. Dragon colors.

— ADWD, The Lost Lord (`sources/chapters/adwd/adwd-the-lost-lord-01.md:61`)
"""

VARYS_CROSSBOW = """\
---
name: "Varys's crossbow"
type: object.artifact
slug: varys-crossbow
aliases: ["the crossbow that killed Kevan Lannister"]
confidence: tier-1
era: current-narrative
pass_origin: s147-aegon-enrich
node_version: 1
material: wood-and-iron
evidence_chapters:
  - ADWD Epilogue
---

## Identity

The crossbow [Varys](varys) uses to kill Lord Regent [Kevan Lannister](kevan-lannister) in the
ADWD epilogue, having already murdered Grand Maester [Pycelle](pycelle) with the daggers of his
little birds. Varys names the choice as a deliberate echo: "I thought the crossbow fitting. You
shared so much with Lord Tywin, why not that?" — both Lannister patriarchs, the brother and Tywin
himself, felled by a crossbow in the hand of an intimate. A distinct artifact from
[Tywin's crossbow](tywins-crossbow) (ASOS), to which it PARALLELS.

## Edges

(Edges in `graph/edges/edges.jsonl`, S147 AEGON enrichment. WIELDS-by [Varys](varys); WIELDED_IN
[the assassinations](assassinations-of-pycelle-and-kevan-lannister); PARALLELS
[Tywin's crossbow](tywins-crossbow).)

## Quotes

> He stood in a pool of shadow by a bookcase, plump, pale-faced, round-shouldered, clutching a crossbow in soft powdered hands. Silk slippers swaddled his feet.

— ADWD, Epilogue (`sources/chapters/adwd/adwd-epilogue.md:277`)

> I thought the crossbow fitting. You shared so much with Lord Tywin, why not that?

— Varys, ADWD, Epilogue (`sources/chapters/adwd/adwd-epilogue.md:293`)
"""

KEVAN_RECONCILES = """\
---
name: "Kevan Lannister reconciles the realm"
type: event.incident
slug: kevan-reconciles-the-realm
aliases: ["Kevan's regency reconciliation", "Kevan Lannister's stabilization of the realm"]
confidence: tier-2
era: war-of-the-five-kings
containers: [wo5k]
pass_origin: s147-aegon-enrich
node_version: 1
evidence_chapters:
  - ADWD Epilogue
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Kevan Lannister reconciles the realm

As Lord Regent for [Tommen](tommen-baratheon), [Kevan Lannister](kevan-lannister) sets out to undo
the damage of [Cersei](cersei-lannister)'s rule: reconcile Highgarden and Casterly Rock, bind the
Faith back to the crown, and unite the Seven Kingdoms under Tommen's reign. The stabilization is
working — which is precisely why [Varys](varys) murders him. The Spider's whole design depends on
chaos: a reconciled, governed realm would leave no opening for [Aegon](aegon-targaryen-young-griff)'s
invasion. Kevan's competence is his death warrant; the assassination cuts the project short and
seeds the "doubt, division, and mistrust" Varys wants beneath Tommen's throne.

## Edges

(Edges in `graph/edges/edges.jsonl`, S147 AEGON enrichment. [Kevan](kevan-lannister) AGENT_IN;
PREVENTED-by [the assassinations](assassinations-of-pycelle-and-kevan-lannister) — this node was
minted to resolve that hub's 0-outgoing dead-end. The realm-chaos the murder unleashes is the
AEGON container's thematic payoff.)

## Quotes

> you were threatening to undo all the queen's good work, to reconcile Highgarden and Casterly Rock, bind the Faith to your little king, unite the Seven Kingdoms under Tommen's rule. So ...

— Varys to the dying Kevan, ADWD, Epilogue (`sources/chapters/adwd/adwd-epilogue.md:285`)
"""

NODES = [
    ("illyrios-ruby-chain", NODES_ARTIFACTS, RUBY_CHAIN),
    ("varys-crossbow", NODES_ARTIFACTS, VARYS_CROSSBOW),
    ("kevan-reconciles-the-realm", NODES_EVENTS, KEVAN_RECONCILES),
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
