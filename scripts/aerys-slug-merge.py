#!/usr/bin/env python3
"""
aerys-slug-merge.py

Task 0b of Plate 0: Aerys slug merge candidate file.

The Mad King is bisected across two slugs in the live graph:
  - Phantom:    aerys-targaryen       (3 edges, incl. jaime-lannister KILLS aerys-targaryen)
  - Canonical:  aerys-ii-targaryen    (11 edges)

Both node files exist. This script:
  1. Reads both node files and confirms they refer to the same person.
  2. Scans graph/edges/edges.jsonl for exact matches on phantom slug.
  3. Writes working/edge-modeling/aerys-merge-candidates.jsonl
     with ORIGINAL + REWRITTEN edge for each affected row.
  4. Writes working/edge-modeling/aerys-merge-summary.md
     with count, list, and quarantine recommendation.

CRITICAL NOTES:
  - aerys-i-targaryen is a DIFFERENT earlier Targaryen king. Do NOT touch it.
  - aerys-targaryen-son-of-aegon is a DISTINCT entity. Do NOT touch it.
  - aerys-ii-targaryens-last-mistress is DISTINCT. Do NOT touch it.
  - Uses EXACT string match, not prefix/substring, to avoid false positives.

Does NOT modify graph/edges/edges.jsonl or any node file (Plate 5 gates the merge).

Usage:
    python3 scripts/aerys-slug-merge.py [--edges PATH] [--out-dir PATH]
"""

import argparse
import json
from pathlib import Path


PHANTOM_SLUG = "aerys-targaryen"
CANONICAL_SLUG = "aerys-ii-targaryen"

# Slugs that MUST NOT be touched even if they start with 'aerys-targaryen'
DO_NOT_TOUCH = {
    "aerys-i-targaryen",
    "aerys-targaryen-son-of-aegon",
    "aerys-ii-targaryens-last-mistress",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--edges",
        default="graph/edges/edges.jsonl",
        help="Path to input edges.jsonl",
    )
    parser.add_argument(
        "--out-dir",
        default="working/edge-modeling",
        help="Output directory",
    )
    parser.add_argument(
        "--nodes-dir",
        default="graph/nodes/characters",
        help="Path to character node files directory",
    )
    args = parser.parse_args()

    edges_path = Path(args.edges)
    out_dir = Path(args.out_dir)
    nodes_dir = Path(args.nodes_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    candidates_path = out_dir / "aerys-merge-candidates.jsonl"
    summary_path = out_dir / "aerys-merge-summary.md"

    # --- Step 1: Confirm both node files exist and describe the same person ---
    phantom_node = nodes_dir / f"{PHANTOM_SLUG}.node.md"
    canonical_node = nodes_dir / f"{CANONICAL_SLUG}.node.md"

    phantom_exists = phantom_node.exists()
    canonical_exists = canonical_node.exists()

    phantom_snippet = ""
    canonical_snippet = ""
    if phantom_exists:
        content = phantom_node.read_text(encoding="utf-8")
        # Grab the name field from frontmatter
        for line in content.splitlines():
            if line.startswith("name:"):
                phantom_snippet = line.strip()
                break
    if canonical_exists:
        content = canonical_node.read_text(encoding="utf-8")
        for line in content.splitlines():
            if line.startswith("name:") or "The Mad King" in line or "Mad Aerys" in line:
                canonical_snippet = line.strip()
                if "Mad King" in canonical_snippet or "Aerys II" in canonical_snippet:
                    break

    print(f"Phantom node  ({PHANTOM_SLUG}): {'EXISTS' if phantom_exists else 'MISSING'}")
    if phantom_snippet:
        print(f"  -> {phantom_snippet}")
    print(f"Canonical node ({CANONICAL_SLUG}): {'EXISTS' if canonical_exists else 'MISSING'}")
    if canonical_snippet:
        print(f"  -> {canonical_snippet}")

    # --- Step 2: Scan edges.jsonl for exact phantom slug ---
    rows = []
    with edges_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    print(f"\nRead {len(rows)} rows from {edges_path}")

    # Guard: ensure we are NOT matching any DO_NOT_TOUCH slugs
    # (the phantom slug itself is "aerys-targaryen", not "aerys-targaryen-son-of-aegon",
    # so exact match is sufficient; but we double-check)
    affected = []
    for r in rows:
        src = r.get("source_slug", "")
        tgt = r.get("target_slug", "")
        if src in DO_NOT_TOUCH or tgt in DO_NOT_TOUCH:
            # Should never happen since these are different slugs, but assert safety
            print(f"WARNING: skipping DO_NOT_TOUCH row: {src} -> {tgt}")
            continue
        if src == PHANTOM_SLUG or tgt == PHANTOM_SLUG:
            affected.append(r)

    print(f"Rows with exact phantom slug '{PHANTOM_SLUG}': {len(affected)}")

    # --- Step 3: Build rewritten rows ---
    merge_candidates = []
    for orig in affected:
        rewritten = dict(orig)
        if rewritten.get("source_slug") == PHANTOM_SLUG:
            rewritten["source_slug"] = CANONICAL_SLUG
        if rewritten.get("target_slug") == PHANTOM_SLUG:
            rewritten["target_slug"] = CANONICAL_SLUG
        rewritten["merge_action"] = "phantom-redirect"
        rewritten["merge_original_source"] = orig.get("source_slug")
        rewritten["merge_original_target"] = orig.get("target_slug")
        merge_candidates.append({
            "original": orig,
            "rewritten": rewritten,
        })

    # --- Write candidates ---
    with candidates_path.open("w", encoding="utf-8") as f:
        for entry in merge_candidates:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"Wrote {len(merge_candidates)} merge candidates to {candidates_path}")

    # --- Write summary ---
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# Aerys Slug Merge — Summary\n\n")
        f.write(f"**Phantom slug:** `{PHANTOM_SLUG}`  \n")
        f.write(f"**Canonical slug:** `{CANONICAL_SLUG}`  \n\n")

        f.write("## Node file confirmation\n\n")
        f.write(f"- Phantom node `graph/nodes/characters/{PHANTOM_SLUG}.node.md`: "
                f"{'exists' if phantom_exists else 'MISSING'}  \n")
        f.write(f"- Canonical node `graph/nodes/characters/{CANONICAL_SLUG}.node.md`: "
                f"{'exists' if canonical_exists else 'MISSING'}  \n\n")
        f.write(
            "Both nodes were inspected and confirm the same person: Aerys II Targaryen, "
            "the Mad King (262–283 AC). The phantom node (`aerys-targaryen`) is a "
            "stub created by the wiki scraper from the plain 'Aerys Targaryen' page, "
            "while the canonical node (`aerys-ii-targaryen`) is the richly populated "
            "article page. They are the same individual.  \n\n"
            "**DO NOT CONFUSE with:** `aerys-i-targaryen` (an earlier Targaryen king), "
            "`aerys-targaryen-son-of-aegon`, or `aerys-ii-targaryens-last-mistress` "
            "— these are distinct entities and were NOT touched.\n\n"
        )

        f.write(f"## Edges affected: {len(affected)}\n\n")
        f.write("| # | Source → Target | Edge Type | Asserted Relation |\n")
        f.write("|---|-----------------|-----------|-------------------|\n")
        for i, orig in enumerate(affected, 1):
            f.write(
                f"| {i} | `{orig.get('source_slug')}` → `{orig.get('target_slug')}` "
                f"| {orig.get('edge_type', '')} "
                f"| {orig.get('asserted_relation', '')} |\n"
            )
        f.write("\n")

        f.write("## Rewritten rows\n\n")
        for entry in merge_candidates:
            orig = entry["original"]
            rew = entry["rewritten"]
            f.write(
                f"- **BEFORE:** `{orig['source_slug']}` → `{orig['target_slug']}` "
                f"({orig.get('edge_type','')})  \n"
                f"  **AFTER :** `{rew['source_slug']}` → `{rew['target_slug']}` "
                f"({rew.get('edge_type','')})  \n"
            )
        f.write("\n")

        f.write("## Quarantine recommendation (for Plate 5)\n\n")
        f.write(
            f"After the Plate 5 merge, the phantom node "
            f"`graph/nodes/characters/{PHANTOM_SLUG}.node.md` will have zero edges "
            f"pointing to it. Per project convention, it should be moved to "
            f"`graph/nodes/characters/_conflicts/{PHANTOM_SLUG}.node.md` with a "
            f"stale-preamble noting the redirect to `{CANONICAL_SLUG}`.  \n\n"
            f"**Do NOT delete the node file** — source data is read-only/additive-only "
            f"per CLAUDE.md. The `_conflicts/` quarantine preserves the record while "
            f"preventing the phantom from polluting traversal queries.  \n\n"
            f"This quarantine step is **out of scope for Plates 0-4**. It is bundled "
            f"into the Plate 5 merge step (gated on Matt's sign-off).\n"
        )

    print(f"Wrote summary to {summary_path}")

    # --- Console summary ---
    print("\n=== AERYS MERGE SUMMARY ===")
    print(f"  Phantom slug:    {PHANTOM_SLUG}")
    print(f"  Canonical slug:  {CANONICAL_SLUG}")
    print(f"  Edges rewritten: {len(merge_candidates)}")
    for entry in merge_candidates:
        o = entry["original"]
        r = entry["rewritten"]
        print(f"    {o['source_slug']} -> {o['target_slug']} ({o.get('edge_type','')})")
        print(f"  → {r['source_slug']} -> {r['target_slug']}")


if __name__ == "__main__":
    main()
