#!/usr/bin/env python3
"""build_alias_table.py — Build the alias lookup tables consumed by resolve.py.

Absorbs the `--build` half of scripts/event_alias_resolver.py: harvests alias
entries from five sources (wiki redirects, event node frontmatter, all-node
frontmatter, victim-phrase generation off VICTIM_IN edges, "The_*" wiki-
redirect epithet backfill), merges them with priority-ordered collision
handling, and writes the SAME two output files at the SAME paths:

  working/wiki/data/event-alias-lookup.json
  working/wiki/data/all-node-alias-lookup.json

IMPORTANT — frontmatter parsing for THIS module: the alias-table build uses
the resolver's OWN regex-based frontmatter parser (`_parse_frontmatter_
aliases` / `_parse_aliases_from_fm` below), NOT weirwood_query.load's
pyyaml-with-fallback parser. This is deliberate, not an oversight: 5 node
files carry malformed doubled-quote aliases (design.md G18 — e.g.
`aliases: ["Blood"]` where the source alias text itself contains literal
quote characters); the two parsers extract different literal alias strings
for those 5 files ("blood" vs "\"blood\"" after normalization), which would
change the alias-table's *content*, not just its interface. The mission is
ZERO BEHAVIOR CHANGE for this build output, so this module intentionally
duplicates the regex parser rather than delegating to load.parse_frontmatter.
Elsewhere in the package (traverse.py, report.py, cli.py) the pyyaml-with-
fallback parser in load.py is used, per the step-1 design decision.

Path resolution: repo root derived from `Path(__file__).resolve()` parents,
matching weirwood_query.load's convention.

No LLM in the loop. Ever.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# --- Paths (UNCHANGED from scripts/event_alias_resolver.py) ---
_THIS_FILE = Path(__file__).resolve()
# <repo>/graph/query/build/build_alias_table.py -> parents[0]=build,
# [1]=query, [2]=graph, [3]=<repo>
REPO_ROOT = _THIS_FILE.parents[3]

WIKI_ALIASES_FILE = REPO_ROOT / "working/wiki/data/event-node-aliases.json"
EVENT_NODES_DIR = REPO_ROOT / "graph/nodes/events"
GRAPH_NODES_DIR = REPO_ROOT / "graph/nodes"
EDGES_FILE = REPO_ROOT / "graph/edges/edges.jsonl"
OUTPUT_FILE = REPO_ROOT / "working/wiki/data/event-alias-lookup.json"
ALL_NODES_OUTPUT_FILE = REPO_ROOT / "working/wiki/data/all-node-alias-lookup.json"
WIKI_RAW_DIR = REPO_ROOT / "sources/wiki/_raw"
NODES_JSON_FILE = REPO_ROOT / "web/data/nodes.json"

MIN_FUZZY_SCORE = 0.5
MAX_FUZZY_CANDIDATES = 5

CHARACTER_CATEGORIES = {"characters"}
DEATH_EVENT_TYPES = {"event.death", "event.execution", "event.assassination", "event.murder"}


# ---------------------------------------------------------------------------
# Normalization — delegate to the single normalizer (weirwood_query.normalize)
# ---------------------------------------------------------------------------

from weirwood_query.normalize import (  # noqa: E402
    alias_slug_to_normalized,
    name_to_normalized,
    normalize,
    slug_to_normalized,
    tokenize,
)


# ---------------------------------------------------------------------------
# Source 1: wiki redirect aliases from event-node-aliases.json
# ---------------------------------------------------------------------------

def load_wiki_redirect_aliases() -> list[dict]:
    """Load working/wiki/data/event-node-aliases.json. Absorbed verbatim."""
    if not WIKI_ALIASES_FILE.exists():
        print(f"WARNING: {WIKI_ALIASES_FILE} not found — skipping wiki redirect source",
              file=sys.stderr)
        return []

    with WIKI_ALIASES_FILE.open() as f:
        data = json.load(f)

    entries = []
    for canonical_slug, info in data.items():
        entries.append({
            "alias": slug_to_normalized(canonical_slug),
            "canonical_slug": canonical_slug,
            "source": "wiki-slug-self",
            "confidence": "high",
            "raw": canonical_slug,
        })
        canon_name = info.get("canonical_name", "")
        if canon_name:
            norm = name_to_normalized(canon_name)
            if norm and "part of" not in norm:
                entries.append({
                    "alias": norm,
                    "canonical_slug": canonical_slug,
                    "source": "wiki-canonical-name",
                    "confidence": "high",
                    "raw": canon_name,
                })
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
#
# Regex-based parser DELIBERATELY duplicated from scripts/event_alias_
# resolver.py rather than reusing weirwood_query.load.parse_frontmatter — see
# module docstring (G18 doubled-quote files parse differently under pyyaml).
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---', re.DOTALL)
_SLUG_RE = re.compile(r'^slug:\s*(.+)$', re.MULTILINE)
_NAME_RE = re.compile(r'^name:\s*"?(.+?)"?\s*$', re.MULTILINE)
_TYPE_RE = re.compile(r'^type:\s*(.+)$', re.MULTILINE)

_ALIASES_START_RE = re.compile(r'^aliases:\s*(.*)$', re.MULTILINE)
_ALIAS_ITEM_RE = re.compile(r'^\s+-\s+(.+)$')


def _parse_aliases_from_fm(fm: str) -> list[str]:
    """Parse the aliases list from a YAML frontmatter block. Absorbed
    verbatim from scripts/event_alias_resolver.py (regex-based, NOT pyyaml —
    see module docstring)."""
    m = _ALIASES_START_RE.search(fm)
    if not m:
        return []

    first_line = m.group(1).strip()

    if first_line.startswith('['):
        raw = first_line
        if raw in ('[]', ''):
            return []
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return [str(a) for a in parsed]
        except json.JSONDecodeError:
            pass
        raw = raw.strip('[]')
        if raw:
            return [a.strip().strip('"').strip("'")
                    for a in raw.split(',') if a.strip()]
        return []

    aliases = []

    if first_line.startswith('-'):
        item_val = re.sub(r'^-\s*', '', first_line).strip().strip('"').strip("'")
        if item_val:
            aliases.append(item_val)

    start_pos = m.end()
    rest = fm[start_pos:]
    for line in rest.split('\n'):
        item_m = _ALIAS_ITEM_RE.match(line)
        if item_m:
            val = item_m.group(1).strip().strip('"').strip("'")
            if val:
                aliases.append(val)
        elif line.strip() and not line[0].isspace() and ':' in line:
            break

    if aliases:
        return aliases

    return []


def _parse_frontmatter_aliases(content: str) -> tuple[str | None, str | None, list[str], str | None]:
    """Parse slug, name, aliases list, and type from a node file's YAML
    frontmatter. Absorbed verbatim from scripts/event_alias_resolver.py."""
    fm_match = _FRONTMATTER_RE.match(content)
    if not fm_match:
        return None, None, [], None

    fm = fm_match.group(1)

    slug_m = _SLUG_RE.search(fm)
    slug = slug_m.group(1).strip() if slug_m else None

    name_m = _NAME_RE.search(fm)
    name = name_m.group(1).strip().strip('"') if name_m else None

    type_m = _TYPE_RE.search(fm)
    node_type = type_m.group(1).strip() if type_m else None

    aliases = _parse_aliases_from_fm(fm)

    return slug, name, aliases, node_type


def load_node_frontmatter_aliases() -> list[dict]:
    """Scan graph/nodes/events/*.node.md for slug, name, and aliases fields."""
    if not EVENT_NODES_DIR.exists():
        print(f"WARNING: {EVENT_NODES_DIR} not found — skipping node frontmatter source",
              file=sys.stderr)
        return []

    entries = []
    for node_file in sorted(EVENT_NODES_DIR.glob("*.node.md")):
        content = node_file.read_text()
        slug, name, aliases, _ = _parse_frontmatter_aliases(content)

        if not slug:
            slug = node_file.stem.replace('.node', '')

        entries.append({
            "alias": slug_to_normalized(slug),
            "canonical_slug": slug,
            "source": "node-slug",
            "confidence": "high",
            "raw": slug,
        })

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
# Source 3: All-node index for character-name fallback
# ---------------------------------------------------------------------------

def load_all_node_aliases() -> list[dict]:
    """Scan ALL graph/nodes/{category}/*.node.md directories (not just
    events/). Absorbed verbatim."""
    if not GRAPH_NODES_DIR.exists():
        print(f"WARNING: {GRAPH_NODES_DIR} not found", file=sys.stderr)
        return []

    entries = []
    for category_dir in sorted(GRAPH_NODES_DIR.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith('_'):
            continue
        if category_dir.name == 'events':
            continue

        category = category_dir.name
        for node_file in sorted(category_dir.glob("*.node.md")):
            content = node_file.read_text()
            slug, name, aliases, node_type = _parse_frontmatter_aliases(content)

            if not slug:
                slug = node_file.stem.replace('.node', '')

            base = {
                "canonical_slug": slug,
                "node_category": category,
                "node_type": node_type or f"node.{category}",
                "confidence": "high",
            }

            entries.append({
                **base,
                "alias": slug_to_normalized(slug),
                "source": f"all-node-slug:{category}",
                "raw": slug,
            })

            if name:
                norm = name_to_normalized(name)
                if norm:
                    entries.append({
                        **base,
                        "alias": norm,
                        "source": f"all-node-name:{category}",
                        "raw": name,
                    })

            for alias_phrase in aliases:
                norm = normalize(alias_phrase)
                if norm:
                    entries.append({
                        **base,
                        "alias": norm,
                        "source": f"all-node-alias:{category}",
                        "raw": alias_phrase,
                    })

    return entries


# ---------------------------------------------------------------------------
# Source 5 ("the "-epithet redirect backfill): "The <Epithet>" wiki redirects
# ---------------------------------------------------------------------------

_REDIRECT_TARGET_RE = re.compile(r'redirectText.*?title="([^"]+)"', re.DOTALL)


def _unescape_html_entities(text: str) -> str:
    return (
        text.replace("&#039;", "'")
        .replace("&amp;", "&")
        .replace("&quot;", '"')
    )


def _kebab_slug_from_title(title: str) -> str:
    """Mirrors wiki-event-alias-harvester.py::slug_from_page_title."""
    slug = title.lower()
    slug = re.sub(r"[''']", "", slug)
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug


def _extract_redirect_target(html: str) -> str | None:
    if "redirectText" not in html and "redirectMsg" not in html:
        return None
    m = _REDIRECT_TARGET_RE.search(html)
    if not m:
        return None
    return _unescape_html_entities(m.group(1))


def load_the_redirect_aliases(
    all_node_slugs: set[str] | None = None,
    phrase_to_nodes: dict[str, list[dict]] | None = None,
) -> list[dict]:
    """Harvest "The <Epithet>"-titled wiki redirect pages. Absorbed verbatim."""
    if not WIKI_RAW_DIR.exists():
        print(f"WARNING: {WIKI_RAW_DIR} not found — skipping the-redirect source",
              file=sys.stderr)
        return []

    if all_node_slugs is None:
        if not NODES_JSON_FILE.exists():
            print(f"WARNING: {NODES_JSON_FILE} not found — skipping the-redirect source",
                  file=sys.stderr)
            return []
        with NODES_JSON_FILE.open() as f:
            all_node_slugs = set(json.load(f).keys())

    if phrase_to_nodes is None:
        phrase_to_nodes = {}
        if ALL_NODES_OUTPUT_FILE.exists():
            with ALL_NODES_OUTPUT_FILE.open() as f:
                phrase_to_nodes = json.load(f).get("phrase_to_nodes", {})

    node_meta_by_slug: dict[str, dict] = {}
    for candidates in phrase_to_nodes.values():
        for c in candidates:
            s = c.get("canonical_slug")
            if s and s not in node_meta_by_slug:
                node_meta_by_slug[s] = {
                    "node_category": c.get("node_category", ""),
                    "node_type": c.get("node_type", ""),
                }

    entries: list[dict] = []

    for path in sorted(WIKI_RAW_DIR.glob("The_*.json")):
        try:
            with path.open() as f:
                d = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        page_title = d.get("page", path.stem.replace("_", " "))
        html = d.get("html", "")

        target_title = _extract_redirect_target(html)
        if target_title is None:
            continue

        resolved_slugs: list[str] = []

        direct_slug = _kebab_slug_from_title(target_title)
        if direct_slug in all_node_slugs:
            resolved_slugs = [direct_slug]
        else:
            target_phrase = name_to_normalized(target_title)
            candidates = phrase_to_nodes.get(target_phrase, [])
            if candidates:
                resolved_slugs = [c["canonical_slug"] for c in candidates]

        if not resolved_slugs:
            continue

        redirect_phrase = normalize(page_title)
        if not redirect_phrase:
            continue

        for slug in resolved_slugs:
            meta = node_meta_by_slug.get(slug, {})
            entries.append({
                "alias": redirect_phrase,
                "canonical_slug": slug,
                "node_category": meta.get("node_category", ""),
                "node_type": meta.get("node_type", ""),
                "source": "wiki-the-redirect",
                "raw": page_title,
            })

    return entries


# ---------------------------------------------------------------------------
# Source 4: Victim-phrase generation for death/execution hubs
# ---------------------------------------------------------------------------

def _victim_phrases(victim_display: str) -> list[str]:
    """Generate natural-language phrases for a victim name. Absorbed verbatim."""
    v = victim_display.strip()
    v_norm = normalize(v)
    phrases = [
        f"{v_norm} death",
        f"{v_norm}'s death",
        f"death of {v_norm}",
        f"{v_norm} execution",
        f"{v_norm}'s execution",
        f"execution of {v_norm}",
        f"{v_norm} killed",
        f"{v_norm} is killed",
        f"{v_norm} murdered",
        f"killing of {v_norm}",
        f"murder of {v_norm}",
        f"assassination of {v_norm}",
        f"{v_norm} assassinated",
        f"who killed {v_norm}",
        f"who murdered {v_norm}",
    ]
    return [normalize(p) for p in phrases if normalize(p)]


_DEATH_KEYWORDS = frozenset({
    "killed", "death", "dead", "execution", "executed", "murdered", "murder",
    "assassination", "assassinated", "beheaded", "slain", "dies", "died",
})


def _event_is_primary_death_of_victim(
    victim_slug: str,
    event_slug: str,
    event_node_names: dict[str, str],
) -> bool:
    """Absorbed verbatim from scripts/event_alias_resolver.py."""
    victim_tokens = set(victim_slug.split("-"))
    event_name = event_node_names.get(event_slug, "")
    combined = f"{event_slug} {event_name}".lower()
    combined_tokens = set(re.findall(r'\w+', combined))

    has_death_keyword = bool(combined_tokens & _DEATH_KEYWORDS)
    if not has_death_keyword:
        return False

    meaningful_victim_tokens = {t for t in victim_tokens if len(t) >= 4}
    has_victim_token = bool(meaningful_victim_tokens & combined_tokens)
    return has_victim_token


def _load_character_alias_map() -> dict[str, list[str]]:
    """Absorbed verbatim from scripts/event_alias_resolver.py."""
    char_dir = GRAPH_NODES_DIR / "characters"
    if not char_dir.exists():
        return {}
    alias_map: dict[str, list[str]] = {}
    for node_file in char_dir.glob("*.node.md"):
        content = node_file.read_text()
        slug, name, aliases, _ = _parse_frontmatter_aliases(content)
        if not slug:
            slug = node_file.stem.replace('.node', '')
        all_names = []
        if name:
            all_names.append(name)
        all_names.extend(aliases)
        if all_names:
            alias_map[slug] = all_names
    return alias_map


def load_victim_aliases(
    event_node_types: dict[str, str],
    event_node_names: dict[str, str] | None = None,
    character_alias_map: dict[str, list[str]] | None = None,
) -> list[dict]:
    """Absorbed verbatim from scripts/event_alias_resolver.py."""
    if event_node_names is None:
        event_node_names = {}
    if character_alias_map is None:
        character_alias_map = {}

    if not EDGES_FILE.exists():
        print(f"WARNING: {EDGES_FILE} not found — skipping victim-index source",
              file=sys.stderr)
        return []

    entries = []
    seen: set[tuple[str, str]] = set()

    with EDGES_FILE.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                edge = json.loads(line)
            except json.JSONDecodeError:
                continue

            if edge.get("edge_type") != "VICTIM_IN":
                continue

            victim_slug = edge.get("source_slug", "")
            event_slug = edge.get("target_slug", "")
            if not victim_slug or not event_slug:
                continue

            event_type = event_node_types.get(event_slug, "")
            if event_type not in DEATH_EVENT_TYPES:
                continue

            if not _event_is_primary_death_of_victim(
                victim_slug, event_slug, event_node_names
            ):
                continue

            edge_name = edge.get("participant_name") or victim_slug.replace("-", " ").title()
            display_names = [edge_name]
            char_names = character_alias_map.get(victim_slug, [])
            for cn in char_names:
                if cn not in display_names:
                    display_names.append(cn)

            for victim_display in display_names:
                for phrase in _victim_phrases(victim_display):
                    key = (phrase, event_slug)
                    if key in seen:
                        continue
                    seen.add(key)
                    entries.append({
                        "alias": phrase,
                        "canonical_slug": event_slug,
                        "source": "victim-index",
                        "confidence": "high",
                        "raw": f"{victim_display} (VICTIM_IN → {event_slug})",
                        "node_type": event_type,
                    })

    return entries


def _collect_event_node_metadata() -> tuple[dict[str, str], dict[str, str]]:
    """Absorbed verbatim from scripts/event_alias_resolver.py."""
    if not EVENT_NODES_DIR.exists():
        return {}, {}
    types: dict[str, str] = {}
    names: dict[str, str] = {}
    for node_file in EVENT_NODES_DIR.glob("*.node.md"):
        content = node_file.read_text()
        slug, name, _, node_type = _parse_frontmatter_aliases(content)
        if not slug:
            slug = node_file.stem.replace('.node', '')
        if node_type:
            types[slug] = node_type
        if name:
            names[slug] = name
    return types, names


# ---------------------------------------------------------------------------
# Merge + collision handling
# ---------------------------------------------------------------------------

PRIORITY_ORDER = [
    "node-name",
    "node-slug",
    "node-frontmatter-alias",
    "victim-index",
    "wiki-canonical-name",
    "wiki-slug-self",
    "wiki-redirect",
]


def build_lookup_table(
    entries: list[dict],
) -> tuple[dict[str, str], dict[str, list[dict]], dict]:
    """Merge all alias entries into a single {phrase -> canonical_slug} dict.
    Absorbed verbatim from scripts/event_alias_resolver.py."""
    by_phrase: dict[str, list[dict]] = {}
    for e in entries:
        phrase = e["alias"]
        if not phrase:
            continue
        by_phrase.setdefault(phrase, []).append(e)

    lookup = {}
    collisions = {}

    for phrase, candidates in by_phrase.items():
        slugs = {c["canonical_slug"] for c in candidates}

        if len(slugs) == 1:
            lookup[phrase] = next(iter(slugs))
        else:
            slug_rank: dict[str, int] = {}
            for c in candidates:
                src = c["source"]
                src_base = src.split(":")[0] if ":" in src else src
                rank = PRIORITY_ORDER.index(src_base) if src_base in PRIORITY_ORDER else len(PRIORITY_ORDER)
                existing = slug_rank.get(c["canonical_slug"], len(PRIORITY_ORDER) + 1)
                slug_rank[c["canonical_slug"]] = min(existing, rank)

            best_rank = min(slug_rank.values())
            best_slugs = [s for s, r in slug_rank.items() if r == best_rank]

            if len(best_slugs) == 1:
                lookup[phrase] = best_slugs[0]
            else:
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

def build_and_save(
    verbose: bool = True,
    *,
    output_file: Path = OUTPUT_FILE,
    all_nodes_output_file: Path = ALL_NODES_OUTPUT_FILE,
) -> dict:
    """Full build: harvest all sources, merge, save to output_file /
    all_nodes_output_file. Returns the stats dict.

    output_file / all_nodes_output_file default to the LIVE paths (unchanged
    from event_alias_resolver.py) but can be overridden — used by the parity
    verification driver to write to a temp path without touching the live
    tables.
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

    if verbose:
        print("Building victim-phrase aliases...")
    event_types, event_names = _collect_event_node_metadata()
    char_alias_map = _load_character_alias_map()
    victim_entries = load_victim_aliases(event_types, event_names, char_alias_map)
    if verbose:
        print(f"  (loaded {len(char_alias_map)} character alias entries)")
    if verbose:
        print(f"  {len(victim_entries)} entries from VICTIM_IN edges")

    all_entries = wiki_entries + node_entries + victim_entries

    if verbose:
        print("Merging and deduplicating...")
    lookup, collisions, stats = build_lookup_table(all_entries)

    source_counts: dict[str, int] = {}
    for e in all_entries:
        source_counts[e["source"]] = source_counts.get(e["source"], 0) + 1

    output = {
        "version": "v2",
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "stats": {
            **stats,
            "source_breakdown": source_counts,
        },
        "alias_to_canonical": lookup,
        "ambiguous_collisions": collisions,
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w") as f:
        json.dump(output, f, indent=2, sort_keys=True)

    if verbose:
        print(f"\nSaved to: {output_file}")
        print(f"  Unique phrases indexed: {stats['unique_phrases']}")
        print(f"  Unambiguous lookups:    {stats['unambiguous_lookups']}")
        print(f"  Ambiguous collisions:   {stats['ambiguous_collisions']}")
        print(f"\nSource breakdown:")
        for src, count in sorted(source_counts.items()):
            print(f"  {src:35s}: {count:5d}")

    if verbose:
        print("\nBuilding all-node index (for character-name fallback)...")
    all_node_entries = load_all_node_aliases()
    all_node_entries_with_events = all_node_entries + node_entries
    _, _, all_stats = build_lookup_table(all_node_entries_with_events)

    all_node_by_phrase: dict[str, list[dict]] = {}
    for e in all_node_entries_with_events:
        phrase = e["alias"]
        if not phrase:
            continue
        entry = {
            "canonical_slug": e["canonical_slug"],
            "node_category": e.get("node_category", "events"),
            "node_type": e.get("node_type", ""),
            "source": e["source"],
        }
        all_node_by_phrase.setdefault(phrase, []).append(entry)

    all_node_collapsed: dict[str, list[dict]] = {}
    for phrase, candidates in all_node_by_phrase.items():
        seen_slugs: set[str] = set()
        deduped = []
        for c in candidates:
            if c["canonical_slug"] not in seen_slugs:
                seen_slugs.add(c["canonical_slug"])
                deduped.append(c)
        all_node_collapsed[phrase] = deduped

    if verbose:
        print("\nLoading 'The <Epithet>' wiki-redirect aliases...")
    node_slugs = set()
    if NODES_JSON_FILE.exists():
        with NODES_JSON_FILE.open() as f:
            node_slugs = set(json.load(f).keys())
    else:
        print(f"WARNING: {NODES_JSON_FILE} not found — skipping the-redirect source",
              file=sys.stderr)

    the_redirect_entries = load_the_redirect_aliases(
        all_node_slugs=node_slugs,
        phrase_to_nodes=all_node_collapsed,
    )
    if verbose:
        print(f"  {len(the_redirect_entries)} entries from sources/wiki/_raw/ 'The_*' redirects")

    new_phrase_count = 0
    for e in the_redirect_entries:
        phrase = e["alias"]
        slug = e["canonical_slug"]
        existing = all_node_collapsed.setdefault(phrase, [])
        if phrase not in all_node_by_phrase:
            new_phrase_count += 1
        if not any(c["canonical_slug"] == slug for c in existing):
            existing.append({
                "canonical_slug": slug,
                "node_category": e.get("node_category", ""),
                "node_type": e.get("node_type", ""),
                "source": e["source"],
            })
    if verbose:
        print(f"  {new_phrase_count} NEW phrases added to the all-node index")

    all_node_output = {
        "version": "v1",
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "stats": {
            "total_node_entries": len(all_node_entries_with_events) + len(the_redirect_entries),
            "unique_phrases": len(all_node_collapsed),
        },
        "phrase_to_nodes": all_node_collapsed,
    }

    all_nodes_output_file.parent.mkdir(parents=True, exist_ok=True)
    with all_nodes_output_file.open("w") as f:
        json.dump(all_node_output, f, indent=2, sort_keys=True)

    if verbose:
        print(f"Saved all-node index to: {all_nodes_output_file}")
        print(f"  Unique phrases in all-node index: {len(all_node_collapsed)}")

    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Build the Weirwood query engine's alias lookup tables."
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build (or rebuild) the alias lookup table at the live paths.",
    )
    parser.add_argument(
        "--out",
        metavar="PATH",
        default=None,
        help="Override event-alias-lookup.json output path (verification/temp use).",
    )
    parser.add_argument(
        "--all-nodes-out",
        metavar="PATH",
        default=None,
        help="Override all-node-alias-lookup.json output path (verification/temp use).",
    )
    args = parser.parse_args()

    if not args.build:
        parser.print_help()
        return

    kwargs = {}
    if args.out:
        kwargs["output_file"] = Path(args.out)
    if args.all_nodes_out:
        kwargs["all_nodes_output_file"] = Path(args.all_nodes_out)

    build_and_save(verbose=True, **kwargs)


if __name__ == "__main__":
    main()
