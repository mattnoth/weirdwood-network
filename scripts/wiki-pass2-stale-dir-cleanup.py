#!/usr/bin/env python3
"""Stale-dir cleanup — migrate nodes whose entity_type_guess no longer
matches the directory they were promoted to.

Today's parser updates (Step 1-4 of 2026-05-02 session) reclassify some
already-in-graph pages: castles formerly typed as `title` now classify as
`place.location`; ships formerly typed as `title` now classify as
`object.artifact`; deities formerly typed as `character.human` now
classify as `organization.religion`; etc.

This script:
  1. Reads working/wiki-parsed/page-index.jsonl + the canonical TYPE_DIR_MAP.
  2. For each existing graph/nodes/<dir>/<slug>.node.md, checks whether
     <dir> matches the expected dir from page-index.jsonl[entity_type_guess].
  3. Reports mismatches in --plan mode; deletes stale files in --apply mode
     so the dedicated promotion scripts can re-emit them in the correct dir.

Re-run dedicated promotion scripts AFTER this:
  python3 scripts/wiki-pass2-tier3-pathb-locations.py --apply
  python3 scripts/wiki-pass2-tier3-pathb-events.py --apply
  python3 scripts/wiki-pass2-tier3-pathb-orgs.py --apply
  python3 scripts/wiki-pass2-tier3-pathb-artifacts.py --apply
  python3 scripts/wiki-pass2-tier3-pathb-texts.py --apply
  python3 scripts/wiki-pass2-tier3-pathb-characters.py --apply
  python3 scripts/wiki-pass2-tier3-pathb-longtail.py --apply
"""

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

PAGE_INDEX_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "page-index.jsonl"
GRAPH_NODES_DIR = PROJECT_ROOT / "graph" / "nodes"

# Mirror scripts/wiki-pass2-promote.py TYPE_DIR_MAP
TYPE_DIR_MAP = {
    "character.human": "characters", "character.direwolf": "characters",
    "character.dragon": "characters", "character": "characters",
    "organization.house": "houses",
    "organization.faction": "factions", "organization.cult": "factions",
    "organization.religion": "religions", "organization": "factions",
    "place.location": "locations", "place.region": "locations",
    "place.castle": "locations", "place.city": "locations", "place": "locations",
    "object.artifact": "artifacts", "object": "artifacts",
    "object.text": "texts", "object.food": "foods",
    "object.material": "materials",
    "event.battle": "events", "event.tournament": "events",
    "event.war": "events", "event": "events",
    "concept": "concepts", "concept.culture": "factions",
    "concept.magic": "concepts", "concept.prophecy": "prophecies",
    "concept.theory": "theories", "concept.language": "languages",
    "concept.medical": "medical", "concept.custom": "customs",
    "species": "species", "title": "titles",
    "prophecy": "prophecies", "theory": "theories", "text": "texts",
}


def slug(name: str) -> str:
    n = re.sub(r"['\",]", "", name.lower())
    n = re.sub(r"[ _]+", "-", n)
    n = re.sub(r"[^a-z0-9-]", "-", n)
    return re.sub(r"-+", "-", n).strip("-")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true",
                    help="Delete stale files (default: report only)")
    args = ap.parse_args()

    # Build slug → expected_dir, slug → page_name
    slug_to_expected = {}
    slug_to_page = {}
    with open(PAGE_INDEX_FILE) as f:
        for line in f:
            r = json.loads(line)
            et = r.get("entity_type_guess")
            if et in TYPE_DIR_MAP:
                s = slug(r["page"])
                slug_to_expected[s] = TYPE_DIR_MAP[et]
                slug_to_page[s] = (r["page"], et)

    # Walk graph/nodes/, find mismatches.
    # Stage-1 carve-out: nodes with `prompt_version: v1` (Stage-1 agent-emitted)
    # are preserved verbatim — Stage 4 prose-edge-classifier handles their
    # type/edge re-classification later. v1-python (Stage-3 deterministic)
    # nodes are eligible for migration.
    mismatches = []
    stage1_protected = []
    for d in sorted(GRAPH_NODES_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith("_"):
            continue
        for f in d.glob("*.node.md"):
            s = f.name[: -len(".node.md")]
            if s in slug_to_expected and slug_to_expected[s] != d.name:
                page, et = slug_to_page[s]
                head = f.read_text(encoding="utf-8")[:2000]
                if "prompt_version: v1\n" in head:
                    stage1_protected.append((s, d.name, slug_to_expected[s], page, et))
                    continue
                mismatches.append((s, d.name, slug_to_expected[s], page, et, f))

    if stage1_protected:
        print(f"\nStage-1 carve-out (preserved verbatim, NOT migrated): "
              f"{len(stage1_protected)}")
        for s, cur, exp, p, et in stage1_protected[:30]:
            print(f"  [STAGE-1] {s} ({p!r}) {cur} → {exp} (would-be type={et})")

    print(f"Stale-dir mismatches: {len(mismatches)}")
    if not mismatches:
        return

    from collections import Counter
    buckets = Counter()
    for s, cur, exp, p, et, f in mismatches:
        buckets[(cur, exp)] += 1
    print("=== By transition ===")
    for (cur, exp), n in buckets.most_common():
        print(f"  {cur:15s} → {exp:15s}: {n}")

    if not args.apply:
        print("\n(--plan mode; pass --apply to delete stale files)")
        print("=== First 30 ===")
        for s, cur, exp, p, et, f in mismatches[:30]:
            print(f"  {s} ({p!r}) {cur} → {exp} (type={et})")
        return

    # Delete stale files
    deleted = 0
    for s, cur, exp, p, et, f in mismatches:
        f.unlink()
        deleted += 1
    print(f"\nDeleted {deleted} stale files. Re-run dedicated promotion "
          f"scripts to recreate them in correct dirs.")


if __name__ == "__main__":
    main()
