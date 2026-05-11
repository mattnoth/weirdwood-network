#!/usr/bin/env python3
"""build-character-indexes.py

Per-character index roll-up — pure deterministic Python, no LLM, no HTTP.

For every character.* node in graph/nodes/, emits a single
graph/index/characters/<slug>.index.json file containing:
  - which chapters the character is POV of
  - which chapters the character is mentioned in (with mention count + section provenance)
  - graph stats: out-edge count (parsed from the node's `## Edges` section),
    in-edge count (from working/wiki/data/backlink-counts.json)

This is the inverse of the per-chapter mention index
(`scripts/build-mention-index.py` → `graph/index/chapters/`).
Answers "what does the graph know about character X?" in O(1) instead of
O(344 chapter scans).

Decisions baked in (per continue-prompt 2026-05-11-per-character-index-rollup):
  - Scope: all `character.*` types (human + dragon + direwolf).
  - POV chapters are recorded in a separate list from `mentioned_in`,
    never double-counted.
  - In-edge count = backlink-counts.json (wiki cross-reference in_count).
    Out-edge count = parsed from the node's `## Edges` section bullets
    (graph-derived, not wiki-derived).
  - Year-page mis-typing (`129-ac` etc. typed as `character.human` by the
    Stage 3 emitter) is emitted faithfully; count surfaced in `_summary.json`.

Usage:
    python3 scripts/build-character-indexes.py --all
    python3 scripts/build-character-indexes.py --character eddard-stark
    python3 scripts/build-character-indexes.py --all --dry-run
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
GRAPH_NODES_DIR = REPO_ROOT / "graph" / "nodes"
MENTION_INDEX_DIR = REPO_ROOT / "graph" / "index" / "chapters"
EXTRACTIONS_DIR = REPO_ROOT / "extractions" / "mechanical"
ALIAS_RESOLVER_PATH = REPO_ROOT / "working" / "wiki" / "data" / "alias-resolver.json"
BACKLINK_COUNTS_PATH = REPO_ROOT / "working" / "wiki" / "data" / "backlink-counts.json"
OUT_DIR = REPO_ROOT / "graph" / "index" / "characters"

EXCLUDED_NODE_DIRS = {"_conflicts", "_unclassified"}

# Year-page slug pattern: e.g. "129-ac", "1-bc", "1000-ac"
# Used only for reporting (not for filtering — we emit faithfully).
YEAR_PAGE_RE = re.compile(r"^\d+-(ac|bc)$")


# ---------------------------------------------------------------------------
# Slug helper (kebab-case, matching wiki-pass2-build-alias-resolver.py)
# ---------------------------------------------------------------------------

def to_kebab(text: str) -> str:
    s = text.lower()
    s = re.sub(r"['\",]", "", s)
    s = re.sub(r"[ _]+", "-", s)
    s = re.sub(r"[^a-z0-9-]", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


# ---------------------------------------------------------------------------
# POV canonical resolution from Pass 1 extraction frontmatter
# ---------------------------------------------------------------------------

# Pass 1 records pov_character in two parenthetical idioms:
#   "Alayne (Sansa Stark)"                     → canonical is INSIDE parens
#   "Theon Greyjoy (as \"The Turncloak\" ...)" → canonical is OUTSIDE parens
# This regex captures `outside (inside)`; we then check whether `inside`
# starts with "as " to decide which side is canonical.
_POV_LINE_RE = re.compile(r"\*\*pov_character:\*\*\s*(.+)")
_POV_PARENS_RE = re.compile(r"^(.+?)\s*\((.+)\)\s*$")


def parse_pov_canonical(raw_value: str) -> str:
    """Given the raw `pov_character:` value, return the canonical character name.

    Pass 1 encodes two parenthetical idioms; we choose canonical accordingly:

      Alias-in-outside, truename-in-parens (canonical = INSIDE):
        "Alayne (Sansa Stark)"             -> "Sansa Stark"
        "Reek (Theon Greyjoy)"             -> "Theon Greyjoy"
        "The Blind Girl (Arya Stark)"      -> "Arya Stark"

      Truename-in-outside, alias-in-parens (canonical = OUTSIDE):
        "Theon Greyjoy (as \"...\")"         -> "Theon Greyjoy"
        "Arya Stark (disguised as \"Arry\")" -> "Arya Stark"

      Plain (no parens):
        "Aeron Greyjoy"                    -> "Aeron Greyjoy"
    """
    raw = raw_value.strip()
    m = _POV_PARENS_RE.match(raw)
    if not m:
        return raw
    outside, inside = m.group(1).strip(), m.group(2).strip()
    inside_lower = inside.lower()
    # Disguise / aliasing idioms → canonical is OUTSIDE parens
    if (inside_lower.startswith("as ")
        or " as " in inside_lower
        or inside_lower.startswith("disguised")):
        return outside
    # Default: canonical name is INSIDE parens (truename pattern)
    return inside


def build_chapter_pov_raw_names() -> dict[str, str]:
    """Walk Pass 1 extractions; return {chapter_id: parsed_canonical_name}.

    Returns the PARSED canonical name (still pre-slug). Slug resolution is
    deferred to `resolve_pov_slug_for_chapter()` which has access to the
    chapter's mention rows for prefix-match disambiguation.
    """
    out: dict[str, str] = {}
    if not EXTRACTIONS_DIR.exists():
        return out
    for ext_file in EXTRACTIONS_DIR.rglob("*.extraction.md"):
        chapter_id = ext_file.name.removesuffix(".extraction.md")
        try:
            text = ext_file.read_text(encoding="utf-8")
        except OSError:
            continue
        m = _POV_LINE_RE.search(text)
        if not m:
            continue
        out[chapter_id] = parse_pov_canonical(m.group(1))
    return out


# Honorific prefixes — longest-first so "grand-maester-" beats "maester-".
_TITLE_PREFIXES = (
    "grand-maester-", "maester-", "lord-commander-", "lord-", "lady-",
    "king-", "queen-", "prince-", "princess-", "ser-", "septa-", "septon-",
    "khal-", "khaleesi-", "the-", "a-",
)


def _strip_title_prefix(slug: str) -> str | None:
    for prefix in _TITLE_PREFIXES:
        if slug.startswith(prefix):
            stripped = slug[len(prefix):]
            if stripped:
                return stripped
    return None


def resolve_pov_slug_for_chapter(
    raw_name: str,
    chapter_mentions: list[dict],
    character_slugs: set[str],
    alias_map: dict[str, str],
    raw_name_to_slugs: dict[str, set[str]] | None = None,
) -> str | None:
    """Resolve a parsed POV canonical name to a character-graph slug.

    Order:
      1. kebab(name) → direct match in character_slugs.
      2. kebab(name) → alias_map → canonical slug.
      3. Strip honorific prefix (Maester-, Ser-, Lord-...) → retry direct + alias.
      4. Prefix match (kebab + "-"): unique → use it. Multiple → disambiguate
         via the chapter's own mention rows (POV is always in Characters Present).
      5. None — chapter has a POV with no graph node yet.
    """
    slug = to_kebab(raw_name)
    if not slug:
        return None
    if slug in character_slugs:
        return slug
    if slug in alias_map and alias_map[slug] in character_slugs:
        return alias_map[slug]

    stripped = _strip_title_prefix(slug)
    if stripped:
        if stripped in character_slugs:
            return stripped
        if stripped in alias_map and alias_map[stripped] in character_slugs:
            return alias_map[stripped]

    # Prefix match — use the unstripped slug (e.g., "catelyn" → catelyn-stark
    # vs catelyn-bracken). If we stripped a title, also try that.
    for candidate_slug in filter(None, [slug, stripped]):
        prefix = candidate_slug + "-"
        prefix_matches = [s for s in character_slugs if s.startswith(prefix)]
        if len(prefix_matches) == 1:
            return prefix_matches[0]
        if len(prefix_matches) > 1:
            # Tiebreaker 1: intersect with nodes that explicitly claim
            # `raw_name` as their `name:` or in their `aliases:` list.
            # Handles cases like POV "Pate" where the alias-resolver's
            # bare-disambiguation filter rightly refuses to pin "Pate" globally
            # but pate-novice is the unique node that explicitly claims it.
            if raw_name_to_slugs is not None:
                explicit = raw_name_to_slugs.get(raw_name, set())
                claimed = [s for s in prefix_matches if s in explicit]
                if len(claimed) == 1:
                    return claimed[0]
            # Tiebreaker 2: appears in this chapter's Characters Present.
            cp_slugs = {
                m.get("slug")
                for m in chapter_mentions
                if (m.get("section") or "").lower() in {
                    "characters present", "character appearances",
                }
            }
            cp_candidates = [s for s in prefix_matches if s in cp_slugs]
            if len(cp_candidates) == 1:
                return cp_candidates[0]
            # Tiebreaker 3: appears anywhere in chapter mentions.
            any_slugs = {m.get("slug") for m in chapter_mentions}
            any_candidates = [s for s in prefix_matches if s in any_slugs]
            if len(any_candidates) == 1:
                return any_candidates[0]
    return None


def load_alias_resolver() -> dict[str, str]:
    if not ALIAS_RESOLVER_PATH.exists():
        return {}
    data = json.loads(ALIAS_RESOLVER_PATH.read_text(encoding="utf-8"))
    return data.get("alias_to_canonical", {})


def load_node_slug_index() -> tuple[set[str], dict[str, set[str]]]:
    """For every character.* node, return:
      (character_slugs, raw_name_to_slugs)

    `raw_name_to_slugs[name]` is the set of slugs that explicitly claim `name`
    in either their `name:` frontmatter field or their `aliases:` list. This
    is the tiebreaker when prefix-match has multiple candidates (e.g., POV
    "Pate" → 12 pate-* slugs, but only pate-novice declares "Pate" as alias).
    """
    character_slugs: set[str] = set()
    raw_name_to_slugs: dict[str, set[str]] = defaultdict(set)

    # Match a top-level YAML list of strings on one line: aliases: ["a", "b"]
    _INLINE_LIST_RE = re.compile(r'^\s*aliases:\s*\[(.+)\]\s*$')
    _STRING_ITEM_RE = re.compile(r'"([^"]+)"|\'([^\']+)\'')

    for node_file in GRAPH_NODES_DIR.rglob("*.node.md"):
        try:
            rel = node_file.relative_to(GRAPH_NODES_DIR)
        except ValueError:
            continue
        if rel.parts[0] in EXCLUDED_NODE_DIRS:
            continue
        text = node_file.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        node_type = fm.get("type", "")
        if not node_type.startswith("character"):
            continue
        slug = fm.get("slug") or node_file.name.removesuffix(".node.md")
        character_slugs.add(slug)

        name = fm.get("name")
        if name:
            raw_name_to_slugs[name].add(slug)
        # Re-parse the aliases line — parse_frontmatter doesn't handle lists.
        for line in text.split("---", 2)[1].splitlines() if text.startswith("---") else []:
            m = _INLINE_LIST_RE.match(line)
            if m:
                for sm in _STRING_ITEM_RE.finditer(m.group(1)):
                    alias = sm.group(1) or sm.group(2)
                    if alias:
                        raw_name_to_slugs[alias].add(slug)
                break
    return character_slugs, raw_name_to_slugs


# ---------------------------------------------------------------------------
# Frontmatter parsing (minimal — no PyYAML dependency)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split a markdown file into (frontmatter_dict, body).

    Supports only the simple `key: value` and `key: "quoted value"` forms used
    in this corpus. Lists (aliases) are not parsed here — we don't need them.
    """
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if len(lines) < 2:
        return {}, text
    # Find the closing ---
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return {}, text

    fm: dict = {}
    for line in lines[1:end_idx]:
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        # Strip surrounding quotes if present
        if value.startswith('"') and value.endswith('"') and len(value) >= 2:
            value = value[1:-1]
        fm[key] = value

    body = "\n".join(lines[end_idx + 1:])
    return fm, body


# ---------------------------------------------------------------------------
# Edge counting from `## Edges` section
# ---------------------------------------------------------------------------

def count_out_edges(body: str) -> int:
    """Count bullet lines under the `## Edges` section of a node body.

    A bullet is any line whose first non-whitespace char is `-`.
    The section ends at the next `## ` heading or EOF.
    """
    count = 0
    in_edges = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            heading = stripped[3:].strip()
            in_edges = (heading == "Edges")
            continue
        if in_edges and stripped.startswith("-"):
            count += 1
    return count


# ---------------------------------------------------------------------------
# Walk character nodes
# ---------------------------------------------------------------------------

def discover_character_nodes() -> list[tuple[str, str, str, Path]]:
    """Return list of (slug, name, type, path) for every character.* node.

    Skips `_conflicts/` and `_unclassified/` directories.
    """
    out: list[tuple[str, str, str, Path]] = []
    for node_file in GRAPH_NODES_DIR.rglob("*.node.md"):
        try:
            rel = node_file.relative_to(GRAPH_NODES_DIR)
        except ValueError:
            continue
        if rel.parts[0] in EXCLUDED_NODE_DIRS:
            continue

        text = node_file.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        node_type = fm.get("type", "")
        if not node_type.startswith("character"):
            continue
        slug = fm.get("slug") or node_file.name.removesuffix(".node.md")
        name = fm.get("name") or slug
        out.append((slug, name, node_type, node_file))
    return out


# ---------------------------------------------------------------------------
# Load per-chapter mention index → build inverse maps
# ---------------------------------------------------------------------------

def load_mention_inverse(
    chapter_pov_raw_names: dict[str, str],
    character_slugs: set[str],
    alias_map: dict[str, str],
    raw_name_to_slugs: dict[str, set[str]],
    unresolved_log: list[tuple[str, str]] | None = None,
) -> tuple[dict, dict]:
    """Walk all mention-index JSON files and build inverse maps.

    POV canonical slug is taken from `chapter_pov_canonical` (built from Pass 1
    extraction frontmatter). This handles three cases the prior implementation
    missed:
      - Descriptive-title chapters (`adwd-the-prophet-01` → aeron-greyjoy)
      - Identity-fraud chapters (`affc-alayne-01` → sansa-stark)
      - Aliased POV stems (`agot-eddard-01` → eddard-stark via alias-resolver)

    Returns:
      pov_inverse: {character_slug: [{"chapter_id", "book"}, ...]}
      mention_inverse: {character_slug: [
        {"chapter_id", "book", "pov_character_slug", "mention_count",
         "sections": [...], "resolved_via": "direct"|"alias"}, ...]}
        — one entry per chapter the character appears in (non-POV).
    """
    pov_inverse: dict[str, list[dict]] = defaultdict(list)
    mention_inverse: dict[str, list[dict]] = defaultdict(list)

    if not MENTION_INDEX_DIR.exists():
        return pov_inverse, mention_inverse

    for mfile in sorted(MENTION_INDEX_DIR.rglob("*.mentions.json")):
        try:
            data = json.loads(mfile.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue

        chapter_id = data.get("chapter_id")
        book = data.get("book")
        if not chapter_id or not book:
            continue

        # Per-chapter aggregation: for each slug, collect sections + count.
        per_slug: dict[str, dict] = {}
        for m in data.get("mentions", []):
            slug = m.get("slug")
            if not slug:
                continue
            entry = per_slug.setdefault(slug, {
                "mention_count": 0,
                "sections": set(),
                "resolved_via": m.get("resolved_via", "direct"),
            })
            entry["mention_count"] += 1
            section = m.get("section")
            if section:
                entry["sections"].add(section)

        # POV: parsed canonical name from Pass 1 frontmatter, resolved to a
        # graph slug using the chapter's own mention rows for tiebreaking.
        pov_slug: str | None = None
        raw_pov_name = chapter_pov_raw_names.get(chapter_id)
        if raw_pov_name:
            pov_slug = resolve_pov_slug_for_chapter(
                raw_pov_name,
                data.get("mentions", []),
                character_slugs,
                alias_map,
                raw_name_to_slugs,
            )
            if pov_slug is None and unresolved_log is not None:
                unresolved_log.append((chapter_id, raw_pov_name))

        # Emit POV record
        if pov_slug:
            pov_inverse[pov_slug].append({
                "chapter_id": chapter_id,
                "book": book,
            })

        # Emit mention records (excluding the POV slug itself — POV chapters
        # go in the `pov` list, not `mentioned_in`)
        for slug, info in per_slug.items():
            if slug == pov_slug:
                continue
            mention_inverse[slug].append({
                "chapter_id": chapter_id,
                "book": book,
                "pov_character_slug": pov_slug,
                "mention_count": info["mention_count"],
                "sections": sorted(info["sections"]),
                "resolved_via": info["resolved_via"],
            })

    return pov_inverse, mention_inverse


# ---------------------------------------------------------------------------
# Load backlink counts (in-edge counts from wiki cross-references)
# ---------------------------------------------------------------------------

def load_backlink_counts() -> dict[str, dict]:
    if not BACKLINK_COUNTS_PATH.exists():
        return {}
    data = json.loads(BACKLINK_COUNTS_PATH.read_text(encoding="utf-8"))
    return data.get("backlinks", {})


# ---------------------------------------------------------------------------
# Per-character index emission
# ---------------------------------------------------------------------------

def build_one(
    slug: str,
    name: str,
    node_type: str,
    node_path: Path,
    pov_chapters: list[dict],
    mention_records: list[dict],
    backlinks: dict[str, dict],
) -> dict:
    body = node_path.read_text(encoding="utf-8")
    _fm, body_only = parse_frontmatter(body)
    out_edge_count = count_out_edges(body_only)

    bl = backlinks.get(slug, {})
    in_edge_count = bl.get("in_count", 0)

    # Sort POV chapters by (book order, chapter_id)
    book_order = {"agot": 0, "acok": 1, "asos": 2, "affc": 3, "adwd": 4}
    pov_chapters_sorted = sorted(
        pov_chapters,
        key=lambda c: (book_order.get(c["book"], 99), c["chapter_id"]),
    )
    mentioned_sorted = sorted(
        mention_records,
        key=lambda c: (book_order.get(c["book"], 99), c["chapter_id"]),
    )

    appearances_total = (
        len(pov_chapters_sorted)
        + sum(r["mention_count"] for r in mentioned_sorted)
    )

    return {
        "slug": slug,
        "name": name,
        "type": node_type,
        "node_path": str(node_path.relative_to(REPO_ROOT)),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stats": {
            "appearances_total": appearances_total,
            "chapters_pov": len(pov_chapters_sorted),
            "chapters_mentioned_in": len(mentioned_sorted),
            "out_edge_count": out_edge_count,
            "in_edge_count": in_edge_count,
        },
        "chapters": {
            "pov": pov_chapters_sorted,
            "mentioned_in": mentioned_sorted,
        },
    }


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run(only_slug: str | None, dry_run: bool) -> None:
    print("Building character-slug index + raw-name reverse map...", flush=True)
    character_slugs, raw_name_to_slugs = load_node_slug_index()
    print(
        f"  {len(character_slugs):,} character.* slugs in graph; "
        f"{len(raw_name_to_slugs):,} unique raw names/aliases mapped."
    )

    print("Loading alias-resolver...", flush=True)
    alias_map = load_alias_resolver()
    print(f"  {len(alias_map):,} aliases loaded.")

    print("Parsing Pass 1 pov_character frontmatter across all chapters...", flush=True)
    chapter_pov_raw_names = build_chapter_pov_raw_names()
    print(f"  {len(chapter_pov_raw_names):,} chapters with pov_character parsed.")

    print("Loading per-chapter mention index + resolving POVs to graph slugs...", flush=True)
    unresolved_pov_log: list[tuple[str, str]] = []
    pov_inverse, mention_inverse = load_mention_inverse(
        chapter_pov_raw_names, character_slugs, alias_map,
        raw_name_to_slugs, unresolved_pov_log,
    )
    if unresolved_pov_log:
        print(f"  WARN: {len(unresolved_pov_log)} chapters have a pov_character that didn't resolve to a graph slug:")
        for cid, name in unresolved_pov_log[:10]:
            print(f"    {cid}  pov_character={name!r}")
        if len(unresolved_pov_log) > 10:
            print(f"    ... ({len(unresolved_pov_log) - 10} more)")
    print(
        f"  POV inverse covers {len(pov_inverse):,} slugs; "
        f"mention inverse covers {len(mention_inverse):,} slugs."
    )

    print("Loading backlink counts...", flush=True)
    backlinks = load_backlink_counts()
    print(f"  {len(backlinks):,} slugs with backlink data.")

    print("Discovering character nodes...", flush=True)
    nodes = discover_character_nodes()
    print(f"  {len(nodes):,} character.* nodes found.")

    if only_slug:
        nodes = [n for n in nodes if n[0] == only_slug]
        if not nodes:
            print(f"ERROR: no character node found with slug '{only_slug}'.")
            sys.exit(1)

    print()
    print("Building per-character indexes...", flush=True)

    if not dry_run:
        OUT_DIR.mkdir(parents=True, exist_ok=True)

    type_counts: dict[str, int] = defaultdict(int)
    year_page_count = 0
    zero_mention_count = 0
    pov_match_count = 0
    rolled_up: list[dict] = []

    for slug, name, node_type, node_path in nodes:
        pov_chapters = pov_inverse.get(slug, [])
        mention_records = mention_inverse.get(slug, [])

        if pov_chapters:
            pov_match_count += 1
        if not pov_chapters and not mention_records:
            zero_mention_count += 1
        if YEAR_PAGE_RE.match(slug):
            year_page_count += 1
        type_counts[node_type] += 1

        record = build_one(
            slug, name, node_type, node_path,
            pov_chapters, mention_records, backlinks,
        )
        rolled_up.append({
            "slug": slug,
            "name": name,
            "type": node_type,
            "chapters_pov": record["stats"]["chapters_pov"],
            "chapters_mentioned_in": record["stats"]["chapters_mentioned_in"],
            "appearances_total": record["stats"]["appearances_total"],
            "in_edge_count": record["stats"]["in_edge_count"],
            "out_edge_count": record["stats"]["out_edge_count"],
        })

        if not dry_run:
            out_path = OUT_DIR / f"{slug}.index.json"
            out_path.write_text(
                json.dumps(record, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    print(f"  Emitted {len(rolled_up):,} character indexes.")
    print()

    # Top-N rollups for the summary
    by_appearances = sorted(rolled_up, key=lambda r: -r["appearances_total"])[:20]
    by_inbound = sorted(rolled_up, key=lambda r: -r["in_edge_count"])[:20]
    pov_chars = sorted(
        [r for r in rolled_up if r["chapters_pov"] > 0],
        key=lambda r: -r["chapters_pov"],
    )

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "character_count": len(rolled_up),
        "type_counts": dict(type_counts),
        "pov_characters_count": len(pov_chars),
        "characters_with_zero_mentions": zero_mention_count,
        "year_pages_emitted_as_characters": year_page_count,
        "pov_inverse_slugs": len(pov_inverse),
        "mention_inverse_slugs": len(mention_inverse),
        "top_by_appearances": by_appearances,
        "top_by_in_edges": by_inbound,
        "pov_characters": pov_chars,
    }

    if not dry_run:
        summary_path = OUT_DIR / "_summary.json"
        summary_path.write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"Summary written to: {summary_path.relative_to(REPO_ROOT)}")

    print()
    print("=" * 60)
    print("CHARACTER INDEX BUILD SUMMARY")
    print("=" * 60)
    print(f"  Total character indexes : {len(rolled_up):,}")
    for t, c in sorted(type_counts.items()):
        print(f"    {t:<22}: {c:,}")
    print(f"  POV characters          : {len(pov_chars):,}")
    print(f"  Zero-mention characters : {zero_mention_count:,}  "
          f"(includes ~year pages)")
    print(f"  Year-page entries       : {year_page_count:,}  "
          f"(mis-typed as character.human; see todos.md)")
    print()
    print("Top POV characters (by POV chapter count):")
    for r in pov_chars[:15]:
        print(f"  {r['slug']:<32}  POV={r['chapters_pov']:>3}  "
              f"mentioned={r['chapters_mentioned_in']:>3}  "
              f"in_edges={r['in_edge_count']:>4}")
    print()
    print("Top 10 characters by in-edge count:")
    for r in by_inbound[:10]:
        print(f"  {r['slug']:<32}  in_edges={r['in_edge_count']:>4}  "
              f"appearances={r['appearances_total']:>3}")
    print("=" * 60)


def main() -> None:
    p = argparse.ArgumentParser(
        description="Build per-character index roll-ups from the mention index."
    )
    g = p.add_mutually_exclusive_group()
    g.add_argument("--character", metavar="SLUG",
                   help="Build only one character (test mode).")
    g.add_argument("--all", action="store_true", dest="all_chars",
                   help="Build all character.* nodes (default).")
    p.add_argument("--dry-run", action="store_true",
                   help="Parse + compute, but don't write files.")
    args = p.parse_args()

    run(only_slug=args.character, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
