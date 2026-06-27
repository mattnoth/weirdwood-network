#!/usr/bin/env python3
"""Mint Theon Greyjoy / Reek BUILD+ENRICH pass 1 (S149) — A2.1 in the S143 plan; the descent's
second build+enrich dip (the last big cross-identity arc). Unlike Sansa/Vale, much of the spine
already existed (Theon is a POV; the chapters were Pass-1'd) — so this is WIRE + ENRICH: the
marquee is the flagged three-bearer 'Reek' identity tangle + the previously-unbuilt fake-deaths
beat + the dead-ended escape wired forward into the pink-letter -> Jon-stabbing seam.

Four new event nodes (NO container tag — A2 arcs are not one of the 5 approved containers; the
events the dip touches may already carry NORTH/wo5k tags from prior builds — those are untouched):
  - theon-fakes-the-deaths-of-bran-and-rickon (event.deception) — architecture.md's named example
  - breaking-of-theon-greyjoy (event.incident) — the Dreadfort captivity hub
  - the-winterfell-murders (event.incident) — the snowbound 'ghost' killings whodunit
  - theon-and-jeyne-escape-winterfell (event.incident) — the redemption turn; wires the old dead-end

35 edges (see candidates.json). Reek tangle modeled `ramsay-snow IMPERSONATES reek` (FIRST-USE
IMPERSONATES) — NOT SAME_AS (would transitively imply Theon=Ramsay=servant). Theon's ADWD 'Reek'
handled by an alias-add + disambiguation note (done OUTSIDE this script, then weirwood-refresh).

Reads working/enrichment/theon-reek/candidates.json; RE-GREPS each quote for the authoritative
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
CAND = REPO / "working" / "enrichment" / "theon-reek" / "candidates.json"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-theon-reek-enrichment-2026-06-25.jsonl"

RUN_ID = "theon-reek-enrichment-s149"
PRODUCED_AT = "2026-06-25T00:00:00+00:00"

NEW_NODE_SLUGS = {
    "theon-fakes-the-deaths-of-bran-and-rickon",
    "breaking-of-theon-greyjoy",
    "the-winterfell-murders",
    "theon-and-jeyne-escape-winterfell",
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
        "typed_by": "curator-theon-reek-enrichment",
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

FAKE_DEATHS = """\
---
name: "Theon fakes the deaths of Bran and Rickon"
type: event.deception
slug: theon-fakes-the-deaths-of-bran-and-rickon
aliases: ["the false deaths of Bran and Rickon", "the miller's boys charade", "Theon's burned Stark boys"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s149-theon-reek-enrich
node_version: 1
evidence_chapters:
  - ACOK Theon V
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Theon fakes the deaths of Bran and Rickon

After [Bran](bran-stark) and [Rickon](rickon-stark) escape [Winterfell](winterfell) and the hunt
through the wolfswood fails to recover them, [Theon](theon-greyjoy) — unable to admit he has lost
the Stark boys — has *"Reek"* (in fact [Ramsay](ramsay-snow) in the dead servant's guise) murder the
two sons of the miller at the Acorn Water, **flay the skin from their faces and dip their heads in
tar**, and mounts the unrecognizable heads on Winterfell's walls as proof that the heirs of
[Ned Stark](eddard-stark) are dead. It is the moral nadir of Theon's ACOK arc and the textbook
`event.deception` (named as such in the data model). The false deaths propagate north as the news
that breaks [Robb](robb-stark). Only [Maester Luwin](luwin) has the stomach to come near and begs to
sew the heads back on for the crypts.

## Edges
(Edges in `graph/edges/edges.jsonl`, S149 Theon/Reek enrichment. CAUSES-in from
[the failed hunt](trail-followed-north-northwest); CAUSES-out to
[Robb's false news](robb-receives-false-news-of-brans-death); [Theon](theon-greyjoy) +
[Reek](reek) AGENT_IN; [the miller's sons](millers-sons) + [Bran](bran-stark) + [Rickon](rickon-stark)
VICTIM_IN; [Luwin](luwin) WITNESS_IN.)

## Quotes

> The miller's boys had been of an age with Bran and Rickon, alike in size and coloring, and once Reek had flayed the skin from their faces and dipped their heads in tar, it was easy to see familiar features in those misshapen lumps of rotting flesh. People were such fools. If we'd said they were rams' heads, they would have seen horns.

> Only Maester Luwin had the stomach to come near. Stone-faced, the small grey man had begged leave to sew the boys' heads back onto their shoulders, so they might be laid in the crypts below with the other Stark dead.
"""

BREAKING = """\
---
name: "The breaking of Theon Greyjoy"
type: event.incident
slug: breaking-of-theon-greyjoy
aliases: ["the breaking of Theon", "Theon becomes Reek", "the Dreadfort captivity of Theon"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s149-theon-reek-enrich
node_version: 1
evidence_chapters:
  - ADWD Reek I
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# The breaking of Theon Greyjoy

Captured at the [sack of Winterfell](sack-of-winterfell), [Theon](theon-greyjoy) is taken to the
[Dreadfort](dreadfort), where [Ramsay](ramsay-snow) imprisons, starves, flays, and mutilates him —
fingers, toes, and teeth taken one at a time — and beats a new identity into him: **"Reek."** The
self that was Theon Greyjoy dissolves under months of torment in the dark (*"It had been scourged
from him, starved from him, flayed from him"*), until only the cringing creature remains. A staged
false-escape with the kennel-girl [Kyra](kyra) — a cruel hunt-game — is one beat of the breaking;
[Skinner](skinner) and the Bastard's Boys are its instruments. The captivity hub of the ADWD arc.
(For the three-bearer "Reek" name, see the [Reek](reek) node — Reek (I) is the original servant;
Ramsay-as-Reek is the ACOK disguise; Theon is "Reek (III)".)

## Edges
(Edges in `graph/edges/edges.jsonl`, S149 Theon/Reek enrichment. ENABLES-in from
[the sack](sack-of-winterfell); [Ramsay](ramsay-snow) AGENT_IN; [Theon](theon-greyjoy) +
[Kyra](kyra) VICTIM_IN; [Skinner](skinner) PARTICIPATES_IN; [Theon](theon-greyjoy) IMPRISONED_AT
[the Dreadfort](dreadfort). Theon's torture is also carried on the existing `ramsay-snow TORTURES
theon-greyjoy` dyad.)

## Quotes

> Reek. My name is Reek, it rhymes with bleak. ... It had been scourged from him, starved from him, flayed from him. When Little Walder pulled him up and Big Walder waved the torch at him to herd him from the cell, he went along as docile as a dog.

> "My name is Reek. It rhymes with leek." In the dark he did not need a name, so it was easy to forget. Reek, Reek, my name is Reek. He had not been born with that name.
"""

WINTERFELL_MURDERS = """\
---
name: "The Winterfell murders"
type: event.incident
slug: the-winterfell-murders
aliases: ["the ghost in Winterfell", "the snowbound killings at Winterfell", "the Winterfell murder spree"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s149-theon-reek-enrich
node_version: 1
evidence_chapters:
  - ADWD A Ghost in Winterfell
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# The Winterfell murders

During the snowbound Bolton occupation of [Winterfell](winterfell), a string of killings empties
the castle of [Ramsay](ramsay-snow)'s men one by one — Yellow Dick (genitals stuffed in his mouth),
Roger Ryswell's groom thrown from the battlements, a Flint, Ser Aenys's squire — each waved away as
accident until the bodies will no longer be ignored. The garrison blames *"a ghost."* The hidden
hand is [Abel](mance-rayder)'s six spearwives, infiltrated to steal "Arya" away; the killings sow the
demoralization and the Frey–Manderly mistrust that will erupt. [Theon](theon-greyjoy), the literal
ghost of the castle he once took, is suspected and interrogated — and cleared by [Lady Dustin](barbrey-dustin)
on the grounds he could not hold a dagger. **The murder of Little Walder Frey is the one death the
spearwives explicitly disclaim** — it remains a genuine open mystery.

## Edges
(Edges in `graph/edges/edges.jsonl`, S149 Theon/Reek enrichment. [Yellow Dick](yellow-dick) VICTIM_IN;
[Abel/Mance](mance-rayder) + [Rowan](rowan) AGENT_IN (the spearwives' covert work — fresh-verify
weighs AGENT_IN vs SUSPECTED_OF); [Theon](theon-greyjoy) SUSPECTED_OF + WITNESS_IN; ENABLES-out to
[the escape](theon-and-jeyne-escape-winterfell).)

## Quotes

> This one could not be waved away as some drunken tumble or the kick of a horse. ... someone had sliced it off and stuffed it into his mouth so forcefully they had broken three of his teeth.

> "Are all Freys such fools? Look at him. Hold a dagger? He hardly has the strength to hold a spoon."
"""

ESCAPE = """\
---
name: "Theon and Jeyne escape Winterfell"
type: event.incident
slug: theon-and-jeyne-escape-winterfell
aliases: ["the leap from the battlements", "Theon rescues Jeyne Poole", "Theon and Jeyne flee Winterfell"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s149-theon-reek-enrich
node_version: 1
evidence_chapters:
  - ADWD Theon I
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Theon and Jeyne escape Winterfell

Under cover of the Frey–Manderly brawl and the order to march on [Stannis](stannis-baratheon),
[Abel](mance-rayder)'s spearwives spring their plan. [Theon](theon-greyjoy) — answering a guard with
his own name, *"Theon Greyjoy,"* for the first time since the Dreadfort, reclaiming the self Ramsay
broke — leads [Jeyne Poole](jeyne-poole) (the false "Arya") through the castle. [Holly](holly) knifes
the gate guard and [Frenya](frenya) holds the drawbridge, both dying to cover them; at the wall Theon
**grabs Jeyne about the waist and jumps** into the snowdrift below. The redemption turn of the arc —
and the act that triggers Ramsay's [pink letter](pink-letter-delivered) demanding the bride and "his
Reek" back, the seam that wires Theon's arc into [Jon](jon-snow)'s.

## Edges
(Edges in `graph/edges/edges.jsonl`, S149 Theon/Reek enrichment. ENABLES-in from
[the murders](the-winterfell-murders); TRIGGERS-out [the pink letter](pink-letter-delivered);
[Theon](theon-greyjoy) + [Abel/Mance](mance-rayder) + [Rowan](rowan) + [Holly](holly) + [Frenya](frenya)
AGENT_IN; [Jeyne](jeyne-poole) + [Holly](holly) VICTIM_IN;
[the carry up the stairs](theon-carries-jeyne-up-battlements-stairs) SUB_BEAT_OF. Theon's rescue of
Jeyne is also carried on the existing `theon-greyjoy RESCUES jeyne-poole` dyad.)

## Quotes

> Yes, he meant to say. Instead he heard himself reply, "Theon Greyjoy. I … I have brought some women for you."

> Theon grabbed Jeyne about the waist and jumped.
"""

NODES = [
    ("theon-fakes-the-deaths-of-bran-and-rickon", NODES_EVENTS, FAKE_DEATHS),
    ("breaking-of-theon-greyjoy", NODES_EVENTS, BREAKING),
    ("the-winterfell-murders", NODES_EVENTS, WINTERFELL_MURDERS),
    ("theon-and-jeyne-escape-winterfell", NODES_EVENTS, ESCAPE),
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
    print(f"edges.jsonl: {len(existing)} -> {len(out)} lines (+{len(new_rows)})")


if __name__ == "__main__":
    main()
