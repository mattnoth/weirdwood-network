#!/usr/bin/env python3
"""
event_alias_resolver.py — COMPAT SHIM over the consolidated query engine.

The real implementation now lives in graph/query/ (query-layer Track, step 1):
  - normalize/tokenize            -> graph/query/weirwood_query/normalize.py
  - resolve (phrase -> slug)      -> graph/query/weirwood_query/resolve.py
  - table loading                 -> graph/query/weirwood_query/load.py
  - table BUILDING (--build)      -> graph/query/build/build_alias_table.py

This file keeps the exact old CLI surface (--build / --lookup / --stats) with
byte-identical stdout, and re-exports every symbol the old module defined so
existing imports keep working unchanged:
  - tests/_helpers.load_script("event_alias_resolver.py")
  - scripts/backfill-epithet-aliases.py
      (`from event_alias_resolver import normalize, name_to_normalized`)

NEW front door for lookups: `weirwood query` (the engine CLI); rebuilds run
via graph/query/build/build_alias_table.py --build (wired into
scripts/weirwood-refresh.sh).

Usage (unchanged):
    python3 scripts/event_alias_resolver.py --build
    python3 scripts/event_alias_resolver.py --lookup "the Red Wedding"
    python3 scripts/event_alias_resolver.py --stats

No LLM in the loop. Ever. (design doc, Q1)
"""

import argparse
import json
import sys
from pathlib import Path

# --- Paths ---
REPO_ROOT = Path(__file__).parent.parent

# Make the engine + builder packages importable (graph/query is NOT pip-installed).
_ENGINE_DIR = str((Path(__file__).resolve().parent.parent / "graph" / "query"))
if _ENGINE_DIR not in sys.path:
    sys.path.insert(0, _ENGINE_DIR)

from weirwood_query import resolve as _resolve_mod   # noqa: E402
from weirwood_query.normalize import (                # noqa: E402,F401
    alias_slug_to_normalized,
    name_to_normalized,
    normalize,
    slug_to_normalized,
    tokenize,
)
from build import build_alias_table as _builder       # noqa: E402

# --- Path globals (same values/paths as before; sourced from the builder) ---
WIKI_ALIASES_FILE = _builder.WIKI_ALIASES_FILE
EVENT_NODES_DIR = _builder.EVENT_NODES_DIR
GRAPH_NODES_DIR = _builder.GRAPH_NODES_DIR
EDGES_FILE = _builder.EDGES_FILE
OUTPUT_FILE = _builder.OUTPUT_FILE
ALL_NODES_OUTPUT_FILE = _builder.ALL_NODES_OUTPUT_FILE
WIKI_RAW_DIR = _builder.WIKI_RAW_DIR
NODES_JSON_FILE = _builder.NODES_JSON_FILE

# --- Tuning constants (unchanged values) ---
MIN_FUZZY_SCORE = _resolve_mod.MIN_FUZZY_SCORE
MAX_FUZZY_CANDIDATES = _resolve_mod.MAX_FUZZY_CANDIDATES
CHARACTER_CATEGORIES = _resolve_mod.CHARACTER_CATEGORIES
DEATH_EVENT_TYPES = _builder.DEATH_EVENT_TYPES
PRIORITY_ORDER = _builder.PRIORITY_ORDER
_DEATH_KEYWORDS = _builder._DEATH_KEYWORDS

# --- Build-half re-exports (graph/query/build/build_alias_table.py) ---
_parse_aliases_from_fm = _builder._parse_aliases_from_fm
_parse_frontmatter_aliases = _builder._parse_frontmatter_aliases
_victim_phrases = _builder._victim_phrases
_event_is_primary_death_of_victim = _builder._event_is_primary_death_of_victim
_load_character_alias_map = _builder._load_character_alias_map
_collect_event_node_metadata = _builder._collect_event_node_metadata
_unescape_html_entities = _builder._unescape_html_entities
_kebab_slug_from_title = _builder._kebab_slug_from_title
_extract_redirect_target = _builder._extract_redirect_target
load_wiki_redirect_aliases = _builder.load_wiki_redirect_aliases
load_node_frontmatter_aliases = _builder.load_node_frontmatter_aliases
load_all_node_aliases = _builder.load_all_node_aliases
load_the_redirect_aliases = _builder.load_the_redirect_aliases
load_victim_aliases = _builder.load_victim_aliases
build_lookup_table = _builder.build_lookup_table
build_and_save = _builder.build_and_save

# --- Resolution-half re-exports (weirwood_query.resolve) ---
_fuzzy_candidates = _resolve_mod._fuzzy_candidates
_character_candidates = _resolve_mod._character_candidates


# ---------------------------------------------------------------------------
# Loaders — thin wrappers preserving the old auto-build-if-missing behavior
# (weirwood_query.load.load_alias_lookup returns {} on a missing file; the
# legacy contract built the table instead). They read the SHIM's OUTPUT_FILE /
# ALL_NODES_OUTPUT_FILE globals at call time so monkeypatching still works.
# ---------------------------------------------------------------------------

def load_lookup() -> dict[str, str]:
    """Load the pre-built lookup table from OUTPUT_FILE. Builds if missing."""
    if not OUTPUT_FILE.exists():
        print("Lookup table not found — building now...", file=sys.stderr)
        build_and_save(verbose=False)

    with OUTPUT_FILE.open() as f:
        data = json.load(f)
    return data.get("alias_to_canonical", {})


def load_all_node_index() -> dict[str, list[dict]]:
    """Load the all-node index from ALL_NODES_OUTPUT_FILE. Builds if missing."""
    if not ALL_NODES_OUTPUT_FILE.exists():
        print("All-node index not found — building now...", file=sys.stderr)
        build_and_save(verbose=False)

    with ALL_NODES_OUTPUT_FILE.open() as f:
        data = json.load(f)
    return data.get("phrase_to_nodes", {})


def resolve(
    phrase: str,
    lookup: dict[str, str] | None = None,
    all_node_index: dict[str, list[dict]] | None = None,
) -> tuple[str | None, str, list[dict]]:
    """Resolve a natural-language phrase to a canonical slug.

    Old 3-parameter signature preserved; delegates to
    weirwood_query.resolve.resolve. When lookup/all_node_index are omitted
    they are loaded via THIS module's loaders (auto-build-if-missing, exactly
    like the legacy resolver), and the collision table is read from the shim's
    OUTPUT_FILE global.
    """
    if lookup is None:
        lookup = load_lookup()
    if all_node_index is None:
        all_node_index = load_all_node_index()
    return _resolve_mod.resolve(
        phrase, lookup, all_node_index, lookup_file=OUTPUT_FILE
    )


# ---------------------------------------------------------------------------
# CLI — old surface kept VERBATIM
# ---------------------------------------------------------------------------

def main():
    print(
        "[event_alias_resolver.py] deprecated shim — the engine lives at "
        "graph/query/; prefer `weirwood query` for lookups and "
        "graph/query/build/build_alias_table.py --build for rebuilds. "
        "Output unchanged.",
        file=sys.stderr,
    )
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
        all_node_index = load_all_node_index()
        phrase = args.lookup
        slug, status, candidates = resolve(phrase, lookup, all_node_index)
        norm = normalize(phrase)
        print(f"Input:      {phrase!r}")
        print(f"Normalized: {norm!r}")
        if status == "hit":
            print(f"Result:     {slug}")
            print(f"Status:     HIT")
        elif status == "hit-character":
            print(f"Result:     {slug}")
            print(f"Status:     HIT-CHARACTER (character node; use --neighbors {slug} to find edges)")
            if len(candidates) > 1:
                print(f"Alternates: {', '.join(c['slug'] for c in candidates[1:])}")
        elif status == "ambiguous":
            print(f"Result:     (ambiguous — multiple slugs match this phrase)")
            print(f"Status:     AMBIGUOUS")
        elif status == "candidates":
            if slug:
                print(f"Result:     {slug}  [top candidate, score={candidates[0]['score']:.2f}]")
                print(f"Status:     CANDIDATES (fuzzy match; verify before use)")
            else:
                print(f"Result:     (no confident single match)")
                print(f"Status:     CANDIDATES (fuzzy; multiple close matches)")
            if candidates:
                print(f"Ranked candidates:")
                for i, c in enumerate(candidates, 1):
                    cat = c.get('node_category', '')
                    typ = c.get('node_type', '')
                    label = f"{cat}/{typ}" if typ else cat
                    print(f"  {i}. {c['slug']}  score={c['score']:.2f}  [{label}]  match={c['match_type']}")
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
