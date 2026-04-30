#!/usr/bin/env python3
"""wiki-pass2-build-alias-resolver.py

Stage 0 of the fleet orchestration plan — pure deterministic Python, no agents,
no HTTP calls, read-only on graph/nodes/.

Scans all node files in graph/nodes/**/*.node.md (excluding _conflicts/ and
_unclassified/), extracts frontmatter fields (slug, name, aliases), and builds
an alias-to-canonical slug map. Output: working/wiki-parsed/alias-resolver.json.

Usage:
    python3 scripts/wiki-pass2-build-alias-resolver.py          # dry-run; print stats
    python3 scripts/wiki-pass2-build-alias-resolver.py --apply  # write the JSON
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
GRAPH_NODES_DIR = REPO_ROOT / "graph" / "nodes"
OUTPUT_PATH = REPO_ROOT / "working" / "wiki-parsed" / "alias-resolver.json"

# Directories to exclude (relative to GRAPH_NODES_DIR)
EXCLUDED_DIRS = {"_conflicts", "_unclassified"}


# ---------------------------------------------------------------------------
# Slug computation — matches wiki-pass2-emit-deterministic.py::page_to_slug
# ---------------------------------------------------------------------------

def to_kebab(text: str) -> str:
    """Convert an alias string to the canonical kebab slug format.

    Rules:
    1. Lowercase
    2. Strip apostrophes, quotes, commas (these merge words, not separate them)
    3. Replace spaces and underscores with hyphens
    4. Replace remaining characters not in [a-z0-9-] with hyphens
    5. Collapse runs of hyphens into single hyphen
    6. Strip leading/trailing hyphens
    """
    s = text.lower()
    s = re.sub(r"['\",]", "", s)
    s = re.sub(r"[ _]+", "-", s)
    s = re.sub(r"[^a-z0-9-]", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from a markdown file.

    Returns a dict with string values for 'slug', 'name', and a list for
    'aliases'. Returns empty dict if no frontmatter found.
    Only reads the block between the first two '---' delimiters.
    """
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    # Find closing delimiter
    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        return {}

    fm_lines = lines[1:end]
    result = {}

    # Simple key-value parser — handles:
    #   key: "quoted string"
    #   key: unquoted string
    #   aliases: ["item1", "item2"]
    #   aliases:
    #     - item1
    #     - item2
    #   aliases: []

    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        m = re.match(r'^(\w+):\s*(.*)', line)
        if not m:
            i += 1
            continue

        key = m.group(1)
        raw_value = m.group(2).strip()

        if key == "aliases":
            aliases = []
            if raw_value.startswith("["):
                # Inline YAML list: ["a", "b", "c"] or []
                inner = raw_value.strip("[]")
                if inner:
                    # Split on commas, strip quotes and whitespace
                    for item in inner.split(","):
                        item = item.strip().strip('"\'')
                        if item:
                            aliases.append(item)
            elif raw_value == "":
                # Block list — gather subsequent "- item" lines
                i += 1
                while i < len(fm_lines):
                    item_line = fm_lines[i]
                    item_m = re.match(r'^\s+-\s+(.*)', item_line)
                    if item_m:
                        val = item_m.group(1).strip().strip('"\'')
                        if val:
                            aliases.append(val)
                        i += 1
                    else:
                        break
                result["aliases"] = aliases
                continue
            result["aliases"] = aliases
        elif key in ("slug", "name"):
            # Strip surrounding quotes if present
            value = raw_value.strip('"\'')
            result[key] = value

        i += 1

    return result


# ---------------------------------------------------------------------------
# Node scanning
# ---------------------------------------------------------------------------

def collect_nodes(graph_nodes_dir: Path) -> list[dict]:
    """Walk graph/nodes/, skipping excluded directories.

    Returns list of dicts with keys: slug, name, aliases, path.
    """
    nodes = []
    warnings = []

    for node_path in sorted(graph_nodes_dir.rglob("*.node.md")):
        # Check if any path component is in EXCLUDED_DIRS
        rel = node_path.relative_to(graph_nodes_dir)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue

        try:
            content = node_path.read_text(encoding="utf-8")
        except OSError as e:
            warnings.append(f"WARNING: Could not read {node_path}: {e}")
            continue

        fm = parse_frontmatter(content)

        # slug is required; fall back to stem
        slug = fm.get("slug", "")
        if not slug:
            # Derive from filename as fallback
            slug = node_path.stem.replace(".node", "")
            warnings.append(f"WARNING: No slug in frontmatter, derived '{slug}' from filename: {node_path.name}")

        name = fm.get("name", "")
        aliases = fm.get("aliases", [])

        nodes.append({
            "slug": slug,
            "name": name,
            "aliases": aliases,
            "path": str(node_path),
        })

    for w in warnings:
        print(w, file=sys.stderr)

    return nodes


# ---------------------------------------------------------------------------
# Alias resolver builder
# ---------------------------------------------------------------------------

# Title-words filter (Step 1 patch): aliases that are single honorific or
# generic title words should NEVER bridge to a specific node — "Ser" is held by
# every knight, not just Gregor Clegane.  These are the known problem cases;
# extend the set if new title-word aliases are discovered.
TITLE_WORD_SLUGS: frozenset[str] = frozenset({
    "ser", "lord", "lady", "prince", "princess", "king", "queen",
    "khal", "khaleesi", "septon", "septa", "maester", "archmaester",
    "castellan", "captain", "bastard", "sellsword", "magister",
    "seeker",
})

# Disambiguation threshold: if alias-as-prefix matches this many or more
# distinct canonical slugs (alias + "-" + ...), the alias is a bare
# disambiguation form and must not be pinned to any single referent.
BARE_DISAMBIGUATION_THRESHOLD = 3


def _count_disambiguation_matches(alias_kebab: str, canonical_slugs: set[str]) -> int:
    """Count how many canonical slugs have alias_kebab as a hyphen-prefix.

    E.g. 'aegon-targaryen' matches 'aegon-targaryen-son-of-rhaegar' etc.
    Returns the count of such matches.
    """
    prefix = alias_kebab + "-"
    return sum(1 for s in canonical_slugs if s.startswith(prefix))


def build_resolver(nodes: list[dict]) -> dict:
    """Build the alias-to-canonical map and detect collisions.

    Returns a dict with keys:
        alias_to_canonical: {kebab_alias -> canonical_slug}
        alias_collisions: [{alias_kebab, candidates, resolution}]
        filtered: [{alias_kebab, canonical, reason}]   (new — for audit trail)
        stats: {nodes_scanned, total_aliases, alias_to_canonical_count,
                alias_collisions, alias_is_self, alias_already_canonical,
                filtered_title_words, filtered_bare_disambiguation}
    """
    # Build the full set of canonical slugs for fast lookup
    canonical_slugs = {node["slug"] for node in nodes}

    # Map: kebab_alias -> list of canonical slugs that claim it
    alias_map: dict[str, list[str]] = defaultdict(list)

    total_aliases = 0
    alias_is_self = 0
    alias_already_canonical = 0

    for node in nodes:
        canonical = node["slug"]
        for raw_alias in node["aliases"]:
            # Skip non-string or empty aliases
            if not isinstance(raw_alias, str) or not raw_alias.strip():
                continue

            total_aliases += 1
            kebab = to_kebab(raw_alias)

            if not kebab:
                continue  # degenerate alias that collapses to empty string

            # Edge case 1: alias kebab == node's own canonical slug → skip
            if kebab == canonical:
                alias_is_self += 1
                continue

            # Edge case 2: alias kebab == another node's canonical slug →
            # the target already exists in the graph by that slug; no resolver
            # entry needed. Log to stats.
            if kebab in canonical_slugs and kebab != canonical:
                alias_already_canonical += 1
                continue

            alias_map[kebab].append(canonical)

    # Separate unambiguous resolutions from collisions
    alias_to_canonical: dict[str, str] = {}
    alias_collisions: list[dict] = []
    filtered: list[dict] = []
    filtered_title_words = 0
    filtered_bare_disambiguation = 0

    for kebab, candidates in sorted(alias_map.items()):
        # --- Filter 1: title-word aliases ---
        if kebab in TITLE_WORD_SLUGS:
            for c in candidates:
                filtered.append({
                    "alias_kebab": kebab,
                    "would_have_resolved_to": c,
                    "reason": "title-word",
                })
                filtered_title_words += 1
            continue

        # --- Filter 2: bare disambiguation forms ---
        # If alias-as-prefix matches BARE_DISAMBIGUATION_THRESHOLD or more
        # canonical slugs, this alias is too ambiguous to pin.
        disambig_count = _count_disambiguation_matches(kebab, canonical_slugs)
        if disambig_count >= BARE_DISAMBIGUATION_THRESHOLD:
            for c in candidates:
                filtered.append({
                    "alias_kebab": kebab,
                    "would_have_resolved_to": c,
                    "reason": f"bare-disambiguation ({disambig_count} matches)",
                })
                filtered_bare_disambiguation += 1
            continue

        if len(candidates) == 1:
            alias_to_canonical[kebab] = candidates[0]
        else:
            # Deduplicate candidates while preserving order
            seen = []
            deduped = []
            for c in candidates:
                if c not in seen:
                    seen.append(c)
                    deduped.append(c)
            alias_collisions.append({
                "alias_kebab": kebab,
                "candidates": sorted(deduped),
                "resolution": "ambiguous-do-not-resolve",
            })

    stats = {
        "nodes_scanned": len(nodes),
        "total_aliases": total_aliases,
        "alias_to_canonical_count": len(alias_to_canonical),
        "alias_collisions": len(alias_collisions),
        "alias_is_self": alias_is_self,
        "alias_already_canonical": alias_already_canonical,
        "filtered_title_words": filtered_title_words,
        "filtered_bare_disambiguation": filtered_bare_disambiguation,
    }

    return {
        "alias_to_canonical": alias_to_canonical,
        "alias_collisions": alias_collisions,
        "filtered": filtered,
        "stats": stats,
    }


# ---------------------------------------------------------------------------
# Cross-ref impact estimate
# ---------------------------------------------------------------------------

def estimate_broken_link_recovery(
    alias_to_canonical: dict[str, str],
    cross_refs_path: Path,
) -> dict:
    """Count how many broken cross-ref links can be resolved via the alias map.

    Returns a dict with counts and top broken slugs.
    """
    if not cross_refs_path.exists():
        return {"error": f"cross-references.jsonl not found at {cross_refs_path}"}

    broken_slugs: dict[str, int] = defaultdict(int)

    with cross_refs_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not rec.get("target_in_graph", True):
                broken_slugs[rec.get("target_slug", "")] += 1

    total_broken_refs = sum(broken_slugs.values())
    total_unique_broken = len(broken_slugs)

    # How many refs are resolvable via alias map?
    resolvable_refs = 0
    resolvable_unique = 0
    for slug, count in broken_slugs.items():
        if slug in alias_to_canonical:
            resolvable_refs += count
            resolvable_unique += 1

    return {
        "total_broken_refs": total_broken_refs,
        "total_unique_broken_slugs": total_unique_broken,
        "resolvable_refs": resolvable_refs,
        "resolvable_unique_slugs": resolvable_unique,
        "recovery_pct": round(100 * resolvable_refs / total_broken_refs, 1) if total_broken_refs else 0,
        "top_broken_by_freq": sorted(broken_slugs.items(), key=lambda x: -x[1])[:20],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Build alias-to-canonical slug resolver for the Weirwood graph."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write the output JSON to working/wiki-parsed/alias-resolver.json",
    )
    args = parser.parse_args()

    print(f"Scanning nodes in: {GRAPH_NODES_DIR}")
    nodes = collect_nodes(GRAPH_NODES_DIR)
    print(f"Nodes found: {len(nodes)}")

    result = build_resolver(nodes)
    alias_to_canonical = result["alias_to_canonical"]
    alias_collisions = result["alias_collisions"]
    stats = result["stats"]

    # Cross-ref impact estimate
    cross_refs_path = REPO_ROOT / "working" / "wiki-parsed" / "cross-references.jsonl"
    impact = estimate_broken_link_recovery(alias_to_canonical, cross_refs_path)

    # --- Print report ---
    print()
    print("=" * 60)
    print("ALIAS RESOLVER — DRY RUN STATS")
    print("=" * 60)
    print(f"  Nodes scanned:              {stats['nodes_scanned']:,}")
    print(f"  Total alias strings read:   {stats['total_aliases']:,}")
    print(f"    - Alias == own slug:       {stats['alias_is_self']:,}  (skipped)")
    print(f"    - Alias already canonical: {stats['alias_already_canonical']:,}  (skipped)")
    print(f"  Resolver map entries:       {stats['alias_to_canonical_count']:,}")
    print(f"  Collision entries:          {stats['alias_collisions']:,}")
    print()
    print("BROKEN LINK RECOVERY ESTIMATE")
    print("-" * 60)
    if "error" in impact:
        print(f"  {impact['error']}")
    else:
        print(f"  Total broken refs:          {impact['total_broken_refs']:,}")
        print(f"  Unique broken target slugs: {impact['total_unique_broken_slugs']:,}")
        print(f"  Resolvable via alias map:   {impact['resolvable_refs']:,} refs "
              f"({impact['recovery_pct']}% of broken)")
        print(f"  Unique slugs resolved:      {impact['resolvable_unique_slugs']:,}")
        print()
        print("  Top 20 broken slugs by frequency:")
        for slug, count in impact["top_broken_by_freq"]:
            resolved = alias_to_canonical.get(slug, "")
            tag = f" → {resolved}" if resolved else ""
            print(f"    {count:5d}  {slug}{tag}")

    print()
    print("TOP 10 COLLISION CASES")
    print("-" * 60)
    # Sort collisions by number of candidates descending, then alphabetically
    sorted_collisions = sorted(alias_collisions, key=lambda x: (-len(x["candidates"]), x["alias_kebab"]))
    for col in sorted_collisions[:10]:
        print(f"  '{col['alias_kebab']}' → candidates: {col['candidates']}")

    print()
    if args.apply:
        payload = {
            "version": "v1",
            "computed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "stats": stats,
            "alias_to_canonical": alias_to_canonical,
            "alias_collisions": sorted_collisions,  # sorted for stable diff
        }

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Write to a temp path then rename for atomicity
        tmp_path = OUTPUT_PATH.with_suffix(".tmp")
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
            f.write("\n")
        tmp_path.rename(OUTPUT_PATH)

        print(f"Written: {OUTPUT_PATH}")
        print(f"  {OUTPUT_PATH.stat().st_size:,} bytes")
    else:
        print("Dry run complete. Pass --apply to write alias-resolver.json.")


if __name__ == "__main__":
    main()
