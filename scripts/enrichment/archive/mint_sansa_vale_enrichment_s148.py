#!/usr/bin/env python3
"""Mint Sansa / Vale (Alayne Stone) BUILD+ENRICH pass 1 (S148) — A2.2 in the S143 plan;
the descent's first build+enrich dip (no spine existed; the Vale arc was a dark island).

The hub `littlefinger-smuggles-sansa-out-of-kings-landing` was the longest-orphaned node in
the graph (2 outgoing: LOCATED_AT red-keep, SUB_BEAT_OF purple-wedding — neither led into the
Vale). `wedding-of-petyr-baelish-and-lysa-arryn` (0 out / 1 junk PRECEDES) and
`lord-nestor-and-the-knights-call-for-marillion-s-death` (0 out, no upstream cause) were also
dead-ended, and `death-of-lysa-arryn` — the keystone — had NO node. This pass (synthesis of 4
fresh Sonnet lenses over ASOS Sansa V–VII + AFFC Sansa I / Alayne I–II) builds the spine + the
whodunit/secondary texture. Highest cross-arc payoff per dip: also builds most of the Petyr
Baelish web (C2) and lights `murder-of-jon-arryn` (the war's root, 0 outgoing graph-wide).

Three new nodes (NO container tag — Vale is not one of the 5 approved containers):
  - `death-of-lysa-arryn` (event.death) — LF pushes Lysa through the open Moon Door ('Only Cat.'
    He gave her a short, sharp shove). POV-confirmed; Sansa + Marillion witness; Marillion framed.
  - `sansa-adopts-the-alayne-stone-identity` (event.deception) — the 'natural daughter' cover.
    (alayne-baelish = LF's MOTHER, not this persona; 'Alayne Stone' is already an alias on
    sansa-stark — this node is the genesis beat, not a second character node.)
  - `lords-declarant-confront-littlefinger` (event.incident) — the six's pact + the Eyrie parley
    where Lyn Corbray bares Lady Forlorn and LF wins a one-year reprieve.

The work (34 edges):
  - SPINE (dead-end fix): smuggle ENABLES {alayne-identity, wedding}; wedding ENABLES death-of-lysa
    [BORDERLINE — fresh-verify]; death-of-lysa CAUSES {Nestor/Marillion hearing, Lords-Declarant pact}.
  - death-of-lysa roles: petyr KILLS lysa + AGENT_IN; lysa VICTIM_IN; sansa + marillion WITNESS_IN;
    moon-door WIELDED_IN (lights the 0-edge artifact).
  - WHODUNIT/REVELATION: petyr COMMANDS_IN murder-of-jon-arryn [UPGRADE of S133 SUSPECTED_OF —
    finalize retires the SUSPECTED_OF iff fresh-verify confirms]; lysa REVEALS_TO sansa (founding
    crime + false letter); petyr REVEALS_TO sansa (hairnet/Olenna, Harry plan); murder-of-jon-arryn
    ENABLES lysa-accuses-tyrion (lights the war's root dead-end).
  - HARRY BETROTHAL: harry BETROTHED_TO sansa; petyr MARRIES_OFF sansa.
  - MANIPULATION WEB: petyr CONSPIRES_WITH lyn-corbray (staged enmity); petyr DECEIVES + MANIPULATES
    (via_bribe) nestor; marillion + sansa DECEIVE nestor (the framing).
  - SECONDARY: lothor AGENT_IN smuggle + GUARDS sansa; robert-arryn WARD_OF petyr (formal).

Theory gate: no fAegon/R+L/Azor-Ahai; the sweetsleep-murder reading + 'Sansa-is-secretly-X' stay
out (harvest only). DROPPED at synthesis (see candidates.json.dropped_at_synthesis): the
harry-the-heir-plan node (forward-dangling/TWOW), the Nestor-bribe node (-> MANIPULATES edge),
petyr MANIPULATES sansa (she knows she's a piece), D-2/D-4/D-5/D-7 (over-distal / circular).

Reads working/enrichment/sansa-vale/candidates.json; RE-GREPS each quote for the authoritative
line (FAIL-fast if a quote moved). Safeguards mirror the prior enrichment mints: backup, re-run
guard, slug pre-check (new nodes excluded). Writes a structured `qualifier` only where present
(Tier-1 MANIPULATES via_bribe + WARD_OF formal)."""
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
CAND = REPO / "working" / "enrichment" / "sansa-vale" / "candidates.json"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-sansa-vale-enrichment-2026-06-25.jsonl"

RUN_ID = "sansa-vale-enrichment-s148"
PRODUCED_AT = "2026-06-25T00:00:00+00:00"

NEW_NODE_SLUGS = {
    "death-of-lysa-arryn",
    "sansa-adopts-the-alayne-stone-identity",
    "lords-declarant-confront-littlefinger",
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
        "typed_by": "curator-sansa-vale-enrichment",
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

DEATH_OF_LYSA = """\
---
name: "Death of Lysa Arryn"
type: event.death
slug: death-of-lysa-arryn
aliases: ["Lysa's fall", "the murder of Lysa Arryn", "Lysa Arryn thrown from the Moon Door"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s148-sansa-vale-enrich
node_version: 1
evidence_chapters:
  - ASOS Sansa VII
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Death of Lysa Arryn

In the High Hall of the [Eyrie](eyrie), after a jealous [Lysa Arryn](lysa-arryn) drags
[Sansa](sansa-stark) to the open [Moon Door](moon-door) to throw her out — enraged by the kiss
she saw [Littlefinger](petyr-baelish) give the girl in the snow — Petyr talks his wife back,
soothes her, and then, with the words *"Only Cat,"* gives her *"a short, sharp shove."* Lysa
stumbles backward through the Moon Door and is gone, six hundred feet to the valley floor. She
never screams. The singer [Marillion](marillion), the only other witness, gasps — and is at once
framed for the murder: Petyr tells the rushing guards *"This singer's killed my lady wife."* The
keystone of the Vale arc — it removes Sansa's protector, leaves Petyr undisputed Lord Protector
of the Vale, and triggers both the framing of Marillion and the Lords Declarant pact.

## Edges
(Edges in `graph/edges/edges.jsonl`, S148 Sansa/Vale enrichment. ENABLES-in from
[the wedding](wedding-of-petyr-baelish-and-lysa-arryn); CAUSES-out to
[the Marillion hearing](lord-nestor-and-the-knights-call-for-marillion-s-death) +
[the Lords Declarant confrontation](lords-declarant-confront-littlefinger); [Petyr](petyr-baelish)
KILLS [Lysa](lysa-arryn) + AGENT_IN; [Lysa](lysa-arryn) VICTIM_IN; [Sansa](sansa-stark) +
[Marillion](marillion) WITNESS_IN; [the Moon Door](moon-door) WIELDED_IN.)

## Quotes

> "Only Cat." He gave her a short, sharp shove.

> Lysa stumbled backward, her feet slipping on the wet marble. And then she was gone. She never screamed. For the longest time there was no sound but the wind.

> "Run let my guards in, then. Quick now, there's no time to lose. This singer's killed my lady wife."
"""

ALAYNE_IDENTITY = """\
---
name: "Sansa adopts the Alayne Stone identity"
type: event.deception
slug: sansa-adopts-the-alayne-stone-identity
aliases: ["Alayne Stone disguise", "Sansa becomes Alayne Stone", "Sansa's bastard-daughter cover"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s148-sansa-vale-enrich
node_version: 1
evidence_chapters:
  - ASOS Sansa VI
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Sansa adopts the Alayne Stone identity

Aboard the *Merling King* and at the [Fingers](fingers), [Littlefinger](petyr-baelish) constructs
a cover identity for [Sansa](sansa-stark): she is to be *"Alayne Stone,"* his natural daughter —
because *"It is not safe to be a Stark just now"* and Varys's informers watch everywhere. When
[Lysa Arryn](lysa-arryn) arrives, Petyr presents the girl: *"My lady, allow me to present you
Alayne Stone."* The persona becomes Sansa's primary self-presentation for the rest of the series
(her hair washed Tyroshi-brown over the auburn). The genesis of the *Alayne Stone* alias already
carried on [sansa-stark](sansa-stark) — distinct from [Alayne Baelish](alayne-baelish), who is
Petyr's mother, not this persona.

## Edges
(Edges in `graph/edges/edges.jsonl`, S148 Sansa/Vale enrichment. ENABLES-in from
[the smuggling](littlefinger-smuggles-sansa-out-of-kings-landing); [Sansa](sansa-stark) +
[Petyr](petyr-baelish) AGENT_IN; [Petyr](petyr-baelish) DECEIVES [Lysa](lysa-arryn) via the cover.)

## Quotes

> "It is not safe to be a Stark just now. So we shall tell Lysa's people that you are my natural daughter."

> "My daughter." Littlefinger beckoned Sansa forward with a hand. "My lady, allow me to present you Alayne Stone."
"""

LORDS_DECLARANT_CONFRONT = """\
---
name: "The Lords Declarant confront Littlefinger"
type: event.incident
slug: lords-declarant-confront-littlefinger
aliases: ["the Lords Declarant parley", "the Lords Declarant pact against Littlefinger", "Lyn Corbray draws Lady Forlorn"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s148-sansa-vale-enrich
node_version: 1
evidence_chapters:
  - AFFC Alayne I
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# The Lords Declarant confront Littlefinger

After [Lysa Arryn's fall](death-of-lysa-arryn), six of the Vale's great lords —
[Bronze Yohn Royce](yohn-royce), Benedar Belmore, Symond Templeton, Horton Redfort, Anya
Waynwood, and Young Lord Hunter — gather at Runestone and make a pact, *"vowing to defend Lord
Robert, the Vale, and one another,"* against the *"misrule"* of the Lord Protector. They march on
the [Gates of the Moon](gates-of-the-moon), [Nestor Royce](nestor-royce) lets them up, and at the
parley [Lyn Corbray](lyn-corbray) — secretly in Petyr's pay — bares Lady Forlorn (*"He drew his
longsword"*) to stage the threat. [Littlefinger](petyr-baelish), with Nestor bought and Corbray
performing, talks his way to a one-year reprieve. The political climax of the AFFC Vale arc.

## Edges
(Edges in `graph/edges/edges.jsonl`, S148 Sansa/Vale enrichment. CAUSES-in from
[Lysa's death](death-of-lysa-arryn); [the Lords Declarant](lords-declarant) AGENT_IN + OPPOSES
[Petyr](petyr-baelish); [Yohn Royce](yohn-royce) + [Lyn Corbray](lyn-corbray) +
[Nestor Royce](nestor-royce) PARTICIPATES_IN.)

## Quotes

> The six had gathered at Runestone after Lysa Arryn's fall, and there made a pact together, vowing to defend Lord Robert, the Vale, and one another.

> "All this talk makes me ill. Littlefinger will talk you out of your smallclothes if you listen long enough. The only way to settle his sort is with steel." He drew his longsword.
"""

NODES = [
    ("death-of-lysa-arryn", NODES_EVENTS, DEATH_OF_LYSA),
    ("sansa-adopts-the-alayne-stone-identity", NODES_EVENTS, ALAYNE_IDENTITY),
    ("lords-declarant-confront-littlefinger", NODES_EVENTS, LORDS_DECLARANT_CONFRONT),
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
