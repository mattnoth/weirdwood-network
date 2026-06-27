#!/usr/bin/env python3
"""Convert the off-vocab CROWNS_QUEEN_OF_LOVE_AND_BEAUTY edge into a beat-node (S134).

Resolves the S133 open decision (Matt: "convert to beat-node"). The edge
  rhaegar-targaryen CROWNS_QUEEN_OF_LOVE_AND_BEAUTY lyanna-stark
was pre-lockdown Stage-4 tail-LLM leakage (run_id tail-llm-20260523), never a decision.

Mints:
  - 1 new event.incident node: crowning-of-lyanna-at-harrenhal (sub-beat of the Tourney at Harrenhal)
  - 4 edges:
      crowning-of-lyanna-at-harrenhal SUB_BEAT_OF tourney-at-harrenhal   (structural)
      rhaegar-targaryen               AGENT_IN     crowning-...           (the crowner / conferrer)
      lyanna-stark                    HONORED_AT   crowning-...           (the honoree — NEW edge type, S134)
      elia-martell                    WITNESS_IN   crowning-...           (the wife pointedly passed over)
  - 1 edge DROP: rhaegar-targaryen CROWNS_QUEEN_OF_LOVE_AND_BEAUTY lyanna-stark

Safeguards mirror mint_rr_enrichment_s133.py: backup, re-run guard, slug pre-check, drop-on-rewrite.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-crowning-lyanna-2026-06-23.jsonl"
NODES_EVENTS = REPO / "graph" / "nodes" / "events"

RUN_ID = "crowning-lyanna-s134"
PRODUCED_AT = "2026-06-23T00:00:00+00:00"

NEW_NODE_SLUGS = {"crowning-of-lyanna-at-harrenhal"}

# ── DROP spec: the off-vocab tail-LLM edge ───────────────────────────────────
DROP_EDGE_TYPE = "CROWNS_QUEEN_OF_LOVE_AND_BEAUTY"
DROP_SOURCE = "rhaegar-targaryen"
DROP_TARGET = "lyanna-stark"

CROWN_QUOTE = (
    "Ned remembered the moment when all the smiles died, when Prince Rhaegar Targaryen "
    "urged his horse past his own wife, the Dornish princess Elia Martell, to lay the "
    "queen of beauty’s laurel in Lyanna’s lap."
)


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "vocab-conversion-s134",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-crowns-conversion",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


# (source, edge_type, target, tier, book, chap_id, line, quote, asserted, verified_or_None)
EDGES_SPEC = [
    ("crowning-of-lyanna-at-harrenhal", "SUB_BEAT_OF", "tourney-at-harrenhal", 1,
     "agot", "agot-eddard-15", 45, CROWN_QUOTE,
     "The crowning of Lyanna as queen of love and beauty was a discrete ceremonial "
     "beat within the Tourney at Harrenhal.", None),
    ("rhaegar-targaryen", "AGENT_IN", "crowning-of-lyanna-at-harrenhal", 1,
     "agot", "agot-eddard-15", 45, CROWN_QUOTE,
     "Rhaegar Targaryen, the tourney champion, laid the queen-of-beauty's laurel in "
     "Lyanna's lap — the conferring agent of the crowning.", None),
    ("lyanna-stark", "HONORED_AT", "crowning-of-lyanna-at-harrenhal", 1,
     "agot", "agot-eddard-15", 45, CROWN_QUOTE,
     "Lyanna Stark was crowned queen of love and beauty — the honoree of the "
     "ceremony.", None),
    ("elia-martell", "WITNESS_IN", "crowning-of-lyanna-at-harrenhal", 1,
     "agot", "agot-eddard-15", 45, CROWN_QUOTE,
     "Elia Martell, Rhaegar's wife, was pointedly passed over and present as he "
     "crowned Lyanna — the load-bearing public slight she witnessed.", None),
]

CROWNING_NODE = """\
---
name: "Crowning of Lyanna at Harrenhal"
type: event.incident
slug: crowning-of-lyanna-at-harrenhal
aliases: ["crowning of Lyanna", "queen of love and beauty crowning", "Rhaegar crowns Lyanna", "the laurel of winter roses"]
confidence: tier-1
era: roberts-rebellion
pass_origin: s134-rr-enrich
node_version: 1
evidence_chapters:
  - AGOT Eddard XV
occurred:
  ac_year: 281
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-retrospective
  date_confidence: tier-2
---

## Identity

At the [Tourney at Harrenhal](tourney-at-harrenhal) in 281 AC, [Prince Rhaegar Targaryen](rhaegar-targaryen) won the joust — unhorsing Brandon Stark, Bronze Yohn Royce, Arthur Dayne, and finally Ser Barristan Selmy to claim the champion's crown. As tourney champion he chose the queen of love and beauty: he "urged his horse past his own wife, the Dornish princess [Elia Martell](elia-martell), to lay the queen of beauty's laurel in [Lyanna Stark](lyanna-stark)'s lap" — a crown of blue winter roses. The moment is one of the most charged in the saga's backstory: passing over his own wife to honor Lyanna (already betrothed to [Robert Baratheon](robert-baratheon)) is the public spark of the Rhaegar-Lyanna strand that ignites Robert's Rebellion. "All the smiles died." The deeper meaning of the choice — and what passed between Rhaegar and Lyanna afterward — is GATED (R+L theory); this node records only the on-page ceremony.

## Edges

(Role/structural edges live in `graph/edges/edges.jsonl`, S134 RR enrichment. This node is a [SUB_BEAT_OF](tourney-at-harrenhal) the Tourney at Harrenhal (Tier-1). [Rhaegar Targaryen](rhaegar-targaryen) AGENT_IN (the crowner; Tier-1); [Lyanna Stark](lyanna-stark) HONORED_AT (the honoree, queen of love and beauty; Tier-1); [Elia Martell](elia-martell) WITNESS_IN (the wife pointedly passed over; Tier-1). Replaces the retired off-vocab `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` edge.)

## Quotes

> "Ned remembered the moment when all the smiles died, when Prince Rhaegar Targaryen urged his horse past his own wife, the Dornish princess Elia Martell, to lay the queen of beauty's laurel in Lyanna's lap. He could see it still: a crown of winter roses, blue as frost."

— AGOT Eddard XV (`sources/chapters/agot/agot-eddard-15.md:45`)
"""

NODES = [("crowning-of-lyanna-at-harrenhal", CROWNING_NODE)]


def make_edge_row(spec):
    (src, etype, tgt, tier, book, chap_id, line, quote, asserted, verified) = spec
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
    if verified is not None:
        row["verified_by"] = verified
    return row


def main():
    all_slugs = set()
    for (src, _, tgt, *_rest) in EDGES_SPEC:
        all_slugs.add(src)
        all_slugs.add(tgt)
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

    kept_lines = []
    drop_count = 0
    for ln in existing_lines:
        try:
            obj = json.loads(ln)
        except json.JSONDecodeError:
            kept_lines.append(ln)
            continue
        if (obj.get("edge_type") == DROP_EDGE_TYPE
                and obj.get("source_slug") == DROP_SOURCE
                and obj.get("target_slug") == DROP_TARGET):
            drop_count += 1
            print(f"DROP confirmed: removed '{DROP_SOURCE} {DROP_EDGE_TYPE} {DROP_TARGET}'")
        else:
            kept_lines.append(ln)
    if drop_count == 0:
        print(f"WARNING: DROP target NOT FOUND — nothing dropped.")

    nodes_created = []
    for slug, body in NODES:
        node_path = NODES_EVENTS / f"{slug}.node.md"
        if node_path.exists():
            print(f"  SKIP node (already exists): {node_path.name}")
        else:
            node_path.write_text(body, encoding="utf-8")
            nodes_created.append(slug)
            print(f"  Created node: {node_path.name}")

    new_rows = [make_edge_row(spec) for spec in EDGES_SPEC]
    lines_before = len(existing_lines)
    all_out = kept_lines + [json.dumps(r, ensure_ascii=False) for r in new_rows]
    EDGES.write_text("\n".join(all_out) + "\n", encoding="utf-8")
    lines_after = len(all_out)

    type_counts = {}
    for spec in EDGES_SPEC:
        type_counts[spec[1]] = type_counts.get(spec[1], 0) + 1

    print("\n── SUMMARY ──")
    print(f"Nodes created ({len(nodes_created)}): {', '.join(nodes_created)}")
    print(f"Edges appended ({len(new_rows)}):")
    for etype, cnt in sorted(type_counts.items()):
        print(f"  {etype}: {cnt}")
    print(f"DROP: {drop_count} row(s) removed ({DROP_SOURCE} {DROP_EDGE_TYPE} {DROP_TARGET})")
    print(f"edges.jsonl: {lines_before} → {lines_after} lines (+{len(new_rows)} appended, -{drop_count} dropped)")
    print(f"Backup: {BACKUP}")


if __name__ == "__main__":
    main()
