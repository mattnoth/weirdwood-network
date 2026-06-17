#!/usr/bin/env python3
"""Build deterministic PRECEDES ordering edges between dated event nodes.

Decision lineage (S104, 2026-06-17, next-move decision #1):
  - Vocab: PRECEDES only (FOLLOWS is its inverse; graph-query traverses PRECEDES
    in reverse). Added to reference/architecture.md "Temporal & Sequencing".
  - Basis: GLOBAL YEAR-CHAIN. Order events by occurred.ac_year. Within a same-year
    cluster, order by narrative_first (a chapter slug -> (book_order, chapter));
    leave same-year siblings WITHOUT narrative_first mutually unordered.
  - Floater policy: P2 "floater-bridged", refined S104 to SAME-BOOK narrative
    ordering only. narrative_first is a reading-order proxy and is reliable for
    in-world order only WITHIN one book — cross-book same-year pairs can invert
    (an event narrated retrospectively in a later book). So:
      * a "unit" = a maximal same-(year,book) run of narrative_first events
        (internally chained by chapter), OR a single event without nf.
      * units within a year are mutually unordered (no cross-book/floater order).
      * every year gets ONE representative event rep(Y); each unit's endpoints
        bridge by cross-year edge to rep(prev occupied year) / rep(next).
    This positions every dated event in the timeline, asserts no cross-book or
    same-year-sibling order, and (because every year has a rep) preserves
    ordering between consecutive all-floater historical years.

Confidence: every edge is tier-3 — it can be no more certain than the
date_confidence: tier-3 (wiki-year-page) dating it is derived from.

Edge shape mirrors the historical-anchor derived-edge rows already in edges.jsonl
(curator/derived provenance, no book quote). New evidence_kind: derived-chronology.

Every emitted edge carries `order_basis`:
  - "narrative"  : same-year pair, both have narrative_first (reading-order proxy)
  - "cross-year" : different years (rock-solid given the year dating)

Usage:
  python3 scripts/build-precedes-edges.py            # dry-run -> working file + summary
  python3 scripts/build-precedes-edges.py --apply    # backup + append to edges.jsonl
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_DIR = os.path.join(REPO, "graph", "nodes", "events")
EDGES = os.path.join(REPO, "graph", "edges", "edges.jsonl")
BACKUP_DIR = os.path.join(REPO, "graph", "edges", "_regrounding")
DRYRUN_OUT = os.path.join(REPO, "working", "wiki", "data", "precedes-edges-dryrun.jsonl")

BOOK_ORDER = {"agot": 1, "acok": 2, "asos": 3, "affc": 4, "adwd": 5}
RUN_ID = "precedes-chain-20260617"
SCHEMA_VERSION = "chronology-v1"


def parse_nf(nf: str | None):
    """Return (book_order, chapter, book_code) or (None, None, None)."""
    if not nf:
        return (None, None, None)
    book, _, chap = nf.partition("-")
    return (BOOK_ORDER.get(book, 9), int(chap), book)


def load_events():
    """Return list of dicts: {slug, yr, nf(tuple|None), book(str|None)} for dated
    events with a concrete ac_year (null-year events like long-night excluded)."""
    events = []
    occ_re = re.compile(r"^occurred:\s*\n((?:[ \t]+\w+:.*\n)+)", re.M)
    for f in sorted(glob.glob(os.path.join(EVENTS_DIR, "*.md"))):
        text = open(f, encoding="utf-8").read()
        m = occ_re.search(text)
        if not m:
            continue
        block = m.group(1)
        ym = re.search(r"ac_year:\s*(-?\d+|null)", block)
        if not ym or ym.group(1) == "null":
            continue
        nfm = re.search(r'narrative_first:\s*"?([a-z]+-\d+)"?', block)
        bo, chap, bk = parse_nf(nfm.group(1) if nfm else None)
        events.append({
            "slug": os.path.basename(f).replace(".node.md", ""),
            "yr": int(ym.group(1)),
            "nf": (bo, chap) if bo is not None else None,
            "book": bk,
        })
    return events


def build_edges(events):
    by_year: dict[int, list] = {}
    for e in events:
        by_year.setdefault(e["yr"], []).append(e)
    years = sorted(by_year)

    def rep(y):
        """One deterministic representative event of a year. Any event of Y is a
        valid cross-year endpoint (cross-year order is certain regardless), so we
        pick nf-first when available, else the lexicographically-first slug."""
        nfs = [e for e in by_year[y] if e["nf"]]
        if nfs:
            return min(nfs, key=lambda e: e["nf"])
        return min(by_year[y], key=lambda e: e["slug"])

    def units(y):
        """Partition a year into ordered units. A unit is either a same-(year,book)
        narrative run (sorted by chapter) or a singleton event without nf."""
        nf_by_book: dict[str, list] = {}
        singletons = []
        for e in by_year[y]:
            if e["nf"]:
                nf_by_book.setdefault(e["book"], []).append(e)
            else:
                singletons.append([e])
        segs = [sorted(g, key=lambda e: e["nf"]) for g in nf_by_book.values()]
        return segs + singletons

    edges = []  # (src, dst, basis)

    # (1) within-(year, book) narrative chains
    for y in years:
        for seg in units(y):
            if len(seg) > 1:
                for a, b in zip(seg, seg[1:]):
                    edges.append((a["slug"], b["slug"], "narrative"))

    # (2) cross-year unit bridges: each unit's head/tail to the adjacent year's rep
    for i, y in enumerate(years):
        prv = rep(years[i - 1]) if i > 0 else None
        nxt = rep(years[i + 1]) if i < len(years) - 1 else None
        for seg in units(y):
            head, tail = seg[0], seg[-1]
            if prv:
                edges.append((prv["slug"], head["slug"], "cross-year"))
            if nxt:
                edges.append((tail["slug"], nxt["slug"], "cross-year"))

    # de-dup directed pairs; drop self-loops
    seen = set()
    uniq = []
    for src, dst, basis in edges:
        if src == dst or (src, dst) in seen:
            continue
        seen.add((src, dst))
        uniq.append((src, dst, basis))
    return uniq, {e["slug"]: e["yr"] for e in events}


def to_row(src, dst, basis, year_of):
    return {
        "edge_type": "PRECEDES",
        "source_slug": src,
        "target_slug": dst,
        "decision": "emit_edge",
        "candidate_kind": "event-chronology",
        "evidence_kind": "derived-chronology",
        "confidence_tier": 3,
        "typed_by": "python-chronology-chain",
        "order_basis": basis,
        "source_ac_year": year_of[src],
        "target_ac_year": year_of[dst],
        "asserted_relation": (
            f"{src} ({year_of[src]} AC) occurs before {dst} ({year_of[dst]} AC)"
            if basis == "cross-year"
            else f"{src} precedes {dst} (same-year, narrative reading order)"
        ),
        "schema_version": SCHEMA_VERSION,
        "run_id": RUN_ID,
        "produced_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="backup + append edges to graph/edges/edges.jsonl")
    args = ap.parse_args()

    events = load_events()
    edges, year_of = build_edges(events)
    rows = [to_row(s, d, b, year_of) for s, d, b in edges]

    n_nar = sum(1 for r in rows if r["order_basis"] == "narrative")
    n_cross = len(rows) - n_nar
    print(f"dated events (concrete ac_year): {len(events)}")
    print(f"PRECEDES edges: {len(rows)}  (narrative={n_nar}, cross-year={n_cross})")

    # node-existence guard: every endpoint must be a real event node
    node_slugs = {os.path.basename(f).replace(".node.md", "")
                  for f in glob.glob(os.path.join(EVENTS_DIR, "*.md"))}
    bad = [r for r in rows if r["source_slug"] not in node_slugs
           or r["target_slug"] not in node_slugs]
    if bad:
        print(f"ERROR: {len(bad)} edges reference a missing node slug", file=sys.stderr)
        sys.exit(1)
    print("endpoint check: all slugs resolve to event nodes ✓")

    os.makedirs(os.path.dirname(DRYRUN_OUT), exist_ok=True)
    with open(DRYRUN_OUT, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    print(f"dry-run rows written: {DRYRUN_OUT}")

    if not args.apply:
        print("\n--- sample (5 narrative, 5 cross-year) ---")
        for kind in ("narrative", "cross-year"):
            for r in [x for x in rows if x["order_basis"] == kind][:5]:
                print(f"  [{kind}] {r['source_slug']} -> {r['target_slug']}")
        print("\nDRY RUN. Re-run with --apply to backup + append to edges.jsonl.")
        return

    os.makedirs(BACKUP_DIR, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    backup = os.path.join(BACKUP_DIR, f"edges-pre-precedes-{stamp}.jsonl")
    shutil.copy2(EDGES, backup)
    print(f"backup: {backup}")
    with open(EDGES, "a", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    total = sum(1 for _ in open(EDGES, encoding="utf-8"))
    print(f"appended {len(rows)} edges -> edges.jsonl now {total} lines")


if __name__ == "__main__":
    main()
