#!/usr/bin/env python3
"""
event_alias_resolver.py — Deterministic event alias resolver for the Weirwood Network.

Builds a flat {alias_phrase -> canonical_slug} lookup table from three sources:
  1. working/wiki/data/event-node-aliases.json  — wiki redirect aliases (harvested S85)
  2. graph/nodes/events/*.node.md frontmatter aliases: fields
  3. Canonical name normalization of each event node's name: field

Design: reference/alias-resolver-design.md (S86)
Output: working/wiki/data/event-alias-lookup.json

Usage:
    # Build/rebuild the lookup table:
    python3 scripts/event_alias_resolver.py --build

    # Look up a phrase (builds in memory, no --build needed):
    python3 scripts/event_alias_resolver.py --lookup "Ned's execution"
    python3 scripts/event_alias_resolver.py --lookup "the Red Wedding"

    # Show stats only:
    python3 scripts/event_alias_resolver.py --stats

No LLM in the loop. Ever. (design doc, Q1)
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# --- Paths ---
REPO_ROOT = Path(__file__).parent.parent
WIKI_ALIASES_FILE = REPO_ROOT / "working/wiki/data/event-node-aliases.json"
EVENT_NODES_DIR = REPO_ROOT / "graph/nodes/events"
OUTPUT_FILE = REPO_ROOT / "working/wiki/data/event-alias-lookup.json"


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

def normalize(phrase: str) -> str:
    """
    Normalize a natural-language phrase to a lookup key.
    Steps:
      1. Lowercase
      2. Strip leading articles (a, an, the) and surrounding whitespace
      3. Collapse internal whitespace → single space
      4. Return the normalized string (NOT kebab-cased — lookup is by normalized phrase)

    The lookup table keys are all normalized forms of every alias. Input queries
    are normalized the same way before lookup, so "the Red Wedding", "Red Wedding",
    "red wedding" all resolve identically.
    """
    phrase = phrase.lower().strip()
    # Strip leading article
    phrase = re.sub(r'^(the|a|an)\s+', '', phrase)
    # Collapse whitespace
    phrase = re.sub(r'\s+', ' ', phrase).strip()
    return phrase


def name_to_normalized(name: str) -> str:
    """Normalize a node's canonical name: field for lookup."""
    return normalize(name)


def slug_to_normalized(slug: str) -> str:
    """Convert a kebab-case slug to a normalized phrase for lookup."""
    return normalize(slug.replace('-', ' '))


def alias_slug_to_normalized(alias: str) -> str:
    """Convert a wiki-redirect alias slug to a normalized phrase."""
    # Wiki redirect slugs use kebab-case (e.g. 'the-red-wedding', 'war-of-the-usurper')
    return normalize(alias.replace('-', ' '))


# ---------------------------------------------------------------------------
# Source 1: wiki redirect aliases from event-node-aliases.json
# ---------------------------------------------------------------------------

def load_wiki_redirect_aliases() -> list[dict]:
    """
    Load working/wiki/data/event-node-aliases.json.
    Returns a list of {alias, canonical_slug, source, confidence} dicts.

    The harvested file maps canonical_slug -> {aliases: [...], redirect_sources: [...]}
    Both the canonical slug and every alias slug are surfaces for the same event.
    """
    if not WIKI_ALIASES_FILE.exists():
        print(f"WARNING: {WIKI_ALIASES_FILE} not found — skipping wiki redirect source",
              file=sys.stderr)
        return []

    with WIKI_ALIASES_FILE.open() as f:
        data = json.load(f)

    entries = []
    for canonical_slug, info in data.items():
        # The slug itself is a surface (e.g. 'red-wedding' → 'Red Wedding')
        entries.append({
            "alias": slug_to_normalized(canonical_slug),
            "canonical_slug": canonical_slug,
            "source": "wiki-slug-self",
            "confidence": "high",
            "raw": canonical_slug,
        })
        # The canonical_name from the wiki page title
        # Skip noise entries where the scraper concatenated infobox "Part of..." text
        canon_name = info.get("canonical_name", "")
        if canon_name:
            norm = name_to_normalized(canon_name)
            # Filter: skip if "part of" appears mid-string (wiki scraper artifact)
            if norm and "part of" not in norm:
                entries.append({
                    "alias": norm,
                    "canonical_slug": canonical_slug,
                    "source": "wiki-canonical-name",
                    "confidence": "high",
                    "raw": canon_name,
                })
        # Each redirect alias
        for alias_slug in info.get("aliases", []):
            entries.append({
                "alias": alias_slug_to_normalized(alias_slug),
                "canonical_slug": canonical_slug,
                "source": "wiki-redirect",
                "confidence": "high",
                "raw": alias_slug,
            })
    return entries


# ---------------------------------------------------------------------------
# Source 2: event node frontmatter aliases
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---', re.DOTALL)
_SLUG_RE = re.compile(r'^slug:\s*(.+)$', re.MULTILINE)
_NAME_RE = re.compile(r'^name:\s*"?(.+?)"?\s*$', re.MULTILINE)
_ALIASES_RE = re.compile(r'^aliases:\s*(.+)$', re.MULTILINE)


def _parse_frontmatter_aliases(content: str) -> tuple[str | None, str | None, list[str]]:
    """
    Parse slug, name, and aliases list from a node file's YAML frontmatter.
    Returns (slug, name, aliases_list).
    """
    fm_match = _FRONTMATTER_RE.match(content)
    if not fm_match:
        return None, None, []

    fm = fm_match.group(1)

    slug_m = _SLUG_RE.search(fm)
    slug = slug_m.group(1).strip() if slug_m else None

    name_m = _NAME_RE.search(fm)
    name = name_m.group(1).strip().strip('"') if name_m else None

    aliases_m = _ALIASES_RE.search(fm)
    aliases = []
    if aliases_m:
        raw = aliases_m.group(1).strip()
        if raw not in ('[]', ''):
            try:
                # Try JSON parse for inline arrays: ["foo", "bar"]
                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    aliases = [str(a) for a in parsed]
            except json.JSONDecodeError:
                # Fallback: split on comma within brackets
                raw = raw.strip('[]')
                if raw:
                    aliases = [a.strip().strip('"').strip("'")
                               for a in raw.split(',') if a.strip()]

    return slug, name, aliases


def load_node_frontmatter_aliases() -> list[dict]:
    """
    Scan graph/nodes/events/*.node.md for slug, name, and aliases fields.
    Returns entries for:
      - The node's canonical name (normalized)
      - The node's slug (normalized)
      - Each alias in the frontmatter aliases: list
    """
    if not EVENT_NODES_DIR.exists():
        print(f"WARNING: {EVENT_NODES_DIR} not found — skipping node frontmatter source",
              file=sys.stderr)
        return []

    entries = []
    for node_file in sorted(EVENT_NODES_DIR.glob("*.node.md")):
        content = node_file.read_text()
        slug, name, aliases = _parse_frontmatter_aliases(content)

        if not slug:
            # Derive slug from filename
            slug = node_file.stem.replace('.node', '')

        # The slug itself as a normalized phrase
        entries.append({
            "alias": slug_to_normalized(slug),
            "canonical_slug": slug,
            "source": "node-slug",
            "confidence": "high",
            "raw": slug,
        })

        # The canonical name
        if name:
            norm = name_to_normalized(name)
            if norm:
                entries.append({
                    "alias": norm,
                    "canonical_slug": slug,
                    "source": "node-name",
                    "confidence": "high",
                    "raw": name,
                })

        # Frontmatter aliases list
        for alias_phrase in aliases:
            norm = normalize(alias_phrase)
            if norm:
                entries.append({
                    "alias": norm,
                    "canonical_slug": slug,
                    "source": "node-frontmatter-alias",
                    "confidence": "high",
                    "raw": alias_phrase,
                })

    return entries


# ---------------------------------------------------------------------------
# Merge + collision handling
# ---------------------------------------------------------------------------

PRIORITY_ORDER = [
    "node-name",           # canonical name from node = highest trust
    "node-slug",           # slug form of canonical node
    "node-frontmatter-alias",  # author-curated frontmatter aliases
    "wiki-canonical-name", # wiki page title
    "wiki-slug-self",      # wiki slug
    "wiki-redirect",       # wiki redirect chains
]


def build_lookup_table(
    entries: list[dict],
) -> tuple[dict[str, str], dict[str, list[dict]], dict]:
    """
    Merge all alias entries into a single {normalized_phrase -> canonical_slug} dict.

    Collision handling:
      - If the same normalized phrase maps to >1 slug, flag as AMBIGUOUS and exclude
        from the lookup. Neither slug is returned for an ambiguous phrase.
      - Priority order (see PRIORITY_ORDER) breaks ties when two entries from
        different sources differ — higher-priority source wins.

    Returns:
      lookup: {normalized_phrase -> canonical_slug}  (unambiguous only)
      collisions: {normalized_phrase -> [list of conflicting entries]}
      stats: summary dict
    """
    # Group all entries by normalized alias phrase
    by_phrase: dict[str, list[dict]] = {}
    for e in entries:
        phrase = e["alias"]
        if not phrase:
            continue
        by_phrase.setdefault(phrase, []).append(e)

    lookup = {}
    collisions = {}

    for phrase, candidates in by_phrase.items():
        # Collect unique target slugs
        slugs = {c["canonical_slug"] for c in candidates}

        if len(slugs) == 1:
            # Unambiguous
            lookup[phrase] = next(iter(slugs))
        else:
            # Multiple slugs — check if a priority-ordered source breaks the tie
            # Build slug -> best_priority_rank
            slug_rank: dict[str, int] = {}
            for c in candidates:
                src = c["source"]
                rank = PRIORITY_ORDER.index(src) if src in PRIORITY_ORDER else len(PRIORITY_ORDER)
                existing = slug_rank.get(c["canonical_slug"], len(PRIORITY_ORDER) + 1)
                slug_rank[c["canonical_slug"]] = min(existing, rank)

            # Find the slug with the best (lowest) rank
            best_rank = min(slug_rank.values())
            best_slugs = [s for s, r in slug_rank.items() if r == best_rank]

            if len(best_slugs) == 1:
                # Single winner by priority
                lookup[phrase] = best_slugs[0]
            else:
                # True ambiguity — exclude, record collision
                collisions[phrase] = candidates

    stats = {
        "total_entries_scanned": len(entries),
        "unique_phrases": len(by_phrase),
        "unambiguous_lookups": len(lookup),
        "ambiguous_collisions": len(collisions),
    }
    return lookup, collisions, stats


# ---------------------------------------------------------------------------
# Build and persist
# ---------------------------------------------------------------------------

def build_and_save(verbose: bool = True) -> dict:
    """
    Full build: harvest all sources, merge, save to OUTPUT_FILE.
    Returns the stats dict.
    """
    if verbose:
        print("Loading wiki redirect aliases...")
    wiki_entries = load_wiki_redirect_aliases()
    if verbose:
        print(f"  {len(wiki_entries)} entries from wiki-node-aliases.json")

    if verbose:
        print("Loading event node frontmatter aliases...")
    node_entries = load_node_frontmatter_aliases()
    if verbose:
        print(f"  {len(node_entries)} entries from {EVENT_NODES_DIR.name}/")

    all_entries = wiki_entries + node_entries

    if verbose:
        print("Merging and deduplicating...")
    lookup, collisions, stats = build_lookup_table(all_entries)

    # Count source breakdown
    source_counts: dict[str, int] = {}
    for e in all_entries:
        source_counts[e["source"]] = source_counts.get(e["source"], 0) + 1

    output = {
        "version": "v1",
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "stats": {
            **stats,
            "source_breakdown": source_counts,
        },
        "alias_to_canonical": lookup,
        "ambiguous_collisions": collisions,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w") as f:
        json.dump(output, f, indent=2, sort_keys=True)

    if verbose:
        print(f"\nSaved to: {OUTPUT_FILE}")
        print(f"  Unique phrases indexed: {stats['unique_phrases']}")
        print(f"  Unambiguous lookups:    {stats['unambiguous_lookups']}")
        print(f"  Ambiguous collisions:   {stats['ambiguous_collisions']}")
        print(f"\nSource breakdown:")
        for src, count in sorted(source_counts.items()):
            print(f"  {src:35s}: {count:5d}")

    return stats


# ---------------------------------------------------------------------------
# Lookup (in-memory)
# ---------------------------------------------------------------------------

def load_lookup() -> dict[str, str]:
    """Load the pre-built lookup table from OUTPUT_FILE. Builds if missing."""
    if not OUTPUT_FILE.exists():
        print("Lookup table not found — building now...", file=sys.stderr)
        build_and_save(verbose=False)

    with OUTPUT_FILE.open() as f:
        data = json.load(f)
    return data.get("alias_to_canonical", {})


def resolve(phrase: str, lookup: dict[str, str] | None = None) -> tuple[str | None, str]:
    """
    Resolve a natural-language phrase to a canonical event slug.
    Returns (slug, status) where status is:
      'hit'       — unambiguous match
      'miss'      — no match in lookup
      'ambiguous' — phrase is in the collision table (rare, check collisions file)
    """
    if lookup is None:
        lookup = load_lookup()

    norm = normalize(phrase)
    slug = lookup.get(norm)
    if slug is not None:
        return slug, "hit"

    # Check collisions file
    if OUTPUT_FILE.exists():
        with OUTPUT_FILE.open() as f:
            data = json.load(f)
        if norm in data.get("ambiguous_collisions", {}):
            return None, "ambiguous"

    return None, "miss"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Deterministic event alias resolver for the Weirwood Network."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--build",
        action="store_true",
        help="Build (or rebuild) the alias lookup table.",
    )
    group.add_argument(
        "--lookup",
        metavar="PHRASE",
        help="Resolve a phrase to its canonical event slug.",
    )
    group.add_argument(
        "--stats",
        action="store_true",
        help="Print statistics from the existing lookup table.",
    )
    args = parser.parse_args()

    if args.build:
        build_and_save(verbose=True)

    elif args.lookup:
        lookup = load_lookup()
        phrase = args.lookup
        slug, status = resolve(phrase, lookup)
        norm = normalize(phrase)
        print(f"Input:      {phrase!r}")
        print(f"Normalized: {norm!r}")
        if status == "hit":
            print(f"Result:     {slug}")
            print(f"Status:     HIT")
        elif status == "ambiguous":
            print(f"Result:     (ambiguous — multiple slugs match this phrase)")
            print(f"Status:     AMBIGUOUS")
        else:
            print(f"Result:     (no match)")
            print(f"Status:     MISS")

    elif args.stats:
        if not OUTPUT_FILE.exists():
            print(f"No lookup table found at {OUTPUT_FILE}")
            print("Run with --build first.")
            sys.exit(1)
        with OUTPUT_FILE.open() as f:
            data = json.load(f)
        stats = data.get("stats", {})
        print(f"Lookup table: {OUTPUT_FILE}")
        print(f"Computed at:  {data.get('computed_at', 'unknown')}")
        print(f"Version:      {data.get('version', 'unknown')}")
        print()
        for k, v in stats.items():
            if isinstance(v, dict):
                print(f"{k}:")
                for sk, sv in sorted(v.items()):
                    print(f"  {sk:35s}: {sv:5}")
            else:
                print(f"{k}: {v}")


if __name__ == "__main__":
    main()
