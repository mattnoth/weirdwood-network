#!/usr/bin/env python3
"""build-entity-indexes.py

Per-entity index roll-up for non-character node types — pure Python, no LLM, no HTTP.

Mirrors the character index pattern from build-character-indexes.py but for:
  --type locations  →  graph/nodes/locations/  (place.*)     → graph/index/locations/
  --type artifacts  →  graph/nodes/artifacts/  (object.*)    → graph/index/artifacts/
  --type houses     →  graph/nodes/houses/     (organization.house) → graph/index/houses/

Output per entity: appearances_total, chapters_in_primary_section, chapters_in_raw_list,
chapters_referenced_in (union), out_edge_count, in_edge_count.

Section semantics:
  locations  — primary: {"Locations", "Location Descriptions"}
               raw_list: sections starting with "Raw Entity List > Location"
  artifacts  — primary: {"Artifacts & Objects of Significance"}
               raw_list: sections starting with "Raw Entity List > Artifact"
  houses     — no primary section (Pass 1 has no dedicated house section)
               raw_list: sections starting with "Raw Entity List > House"

Usage:
    python3 scripts/build-entity-indexes.py --type locations --all
    python3 scripts/build-entity-indexes.py --type artifacts --slug longclaw
    python3 scripts/build-entity-indexes.py --type houses --all --dry-run
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


REPO_ROOT = Path(__file__).resolve().parent.parent
GRAPH_NODES_DIR = REPO_ROOT / "graph" / "nodes"
MENTION_INDEX_DIR = REPO_ROOT / "graph" / "index" / "chapters"
EXTRACTIONS_DIR = REPO_ROOT / "extractions" / "mechanical"
ALIAS_RESOLVER_PATH = REPO_ROOT / "working" / "wiki" / "data" / "alias-resolver.json"
BACKLINK_COUNTS_PATH = REPO_ROOT / "working" / "wiki" / "data" / "backlink-counts.json"

EXCLUDED_NODE_DIRS = {"_conflicts", "_unclassified"}


# ---------------------------------------------------------------------------
# Type configuration
# ---------------------------------------------------------------------------

@dataclass
class TypeConfig:
    node_dirs: list[str]
    type_prefixes: list[str]
    output_dir: str
    primary_sections: frozenset
    raw_list_section_keywords: list[str]   # section.startswith(kw) → in_raw_list
    primary_chapter_key: Optional[str]     # None means no primary section


TYPE_CONFIGS: dict[str, TypeConfig] = {
    "locations": TypeConfig(
        node_dirs=["graph/nodes/locations"],
        type_prefixes=["place."],
        output_dir="graph/index/locations",
        primary_sections=frozenset({"Locations", "Location Descriptions"}),
        raw_list_section_keywords=["Raw Entity List > Location"],
        primary_chapter_key="in_locations_section",
    ),
    "artifacts": TypeConfig(
        node_dirs=["graph/nodes/artifacts"],
        type_prefixes=["object.", "artifact."],
        output_dir="graph/index/artifacts",
        primary_sections=frozenset({"Artifacts & Objects of Significance"}),
        raw_list_section_keywords=["Raw Entity List > Artifact"],
        primary_chapter_key="in_artifacts_section",
    ),
    "houses": TypeConfig(
        node_dirs=["graph/nodes/houses"],
        type_prefixes=["organization.house"],
        output_dir="graph/index/houses",
        primary_sections=frozenset(),
        raw_list_section_keywords=["Raw Entity List > House"],
        primary_chapter_key=None,
    ),
}


# ---------------------------------------------------------------------------
# Slug helper
# ---------------------------------------------------------------------------

def to_kebab(text: str) -> str:
    s = text.lower()
    s = re.sub(r"['\",]", "", s)
    s = re.sub(r"[ _]+", "-", s)
    s = re.sub(r"[^a-z0-9-]", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
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
        if value.startswith('"') and value.endswith('"') and len(value) >= 2:
            value = value[1:-1]
        fm[key] = value
    body = "\n".join(lines[end_idx + 1:])
    return fm, body


# ---------------------------------------------------------------------------
# Edge counting
# ---------------------------------------------------------------------------

def count_out_edges(body: str) -> int:
    count = 0
    in_edges = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            in_edges = (stripped[3:].strip() == "Edges")
            continue
        if in_edges and stripped.startswith("-"):
            count += 1
    return count


# ---------------------------------------------------------------------------
# POV resolution (lightweight — context annotation only, not critical path)
# ---------------------------------------------------------------------------

_POV_LINE_RE = re.compile(r"\*\*pov_character:\*\*\s*(.+)")
_POV_PARENS_RE = re.compile(r"^(.+?)\s*\((.+)\)\s*$")
_TITLE_PREFIXES = (
    "grand-maester-", "maester-", "lord-commander-", "lord-", "lady-",
    "king-", "queen-", "prince-", "princess-", "ser-", "septa-", "septon-",
    "khal-", "khaleesi-", "the-", "a-",
)


def _parse_pov_canonical(raw: str) -> str:
    raw = raw.strip()
    m = _POV_PARENS_RE.match(raw)
    if not m:
        return raw
    outside, inside = m.group(1).strip(), m.group(2).strip()
    inside_lower = inside.lower()
    if (inside_lower.startswith("as ")
            or " as " in inside_lower
            or inside_lower.startswith("disguised")):
        return outside
    return inside


def _resolve_slug(name: str, slug_set: set[str], alias_map: dict[str, str]) -> Optional[str]:
    slug = to_kebab(name)
    if slug in slug_set:
        return slug
    if slug in alias_map and alias_map[slug] in slug_set:
        return alias_map[slug]
    for prefix in _TITLE_PREFIXES:
        if slug.startswith(prefix):
            stripped = slug[len(prefix):]
            if stripped in slug_set:
                return stripped
            if stripped in alias_map and alias_map[stripped] in slug_set:
                return alias_map[stripped]
    return None


def build_chapter_pov_map(alias_map: dict[str, str]) -> dict[str, str]:
    """Return {chapter_id: pov_slug} for all Pass 1 chapters.

    Uses the same canonical-name extraction as build-character-indexes.py,
    but a lighter slug resolution (no prefix-match or per-chapter tiebreaking).
    Good enough for context annotation; a few edge cases may remain unresolved.
    """
    char_slugs: set[str] = set()
    for node_file in GRAPH_NODES_DIR.rglob("*.node.md"):
        try:
            rel = node_file.relative_to(GRAPH_NODES_DIR)
        except ValueError:
            continue
        if rel.parts[0] in EXCLUDED_NODE_DIRS:
            continue
        text = node_file.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        if fm.get("type", "").startswith("character"):
            char_slugs.add(fm.get("slug") or node_file.name.removesuffix(".node.md"))

    chapter_pov: dict[str, str] = {}
    if not EXTRACTIONS_DIR.exists():
        return chapter_pov
    for ext_file in EXTRACTIONS_DIR.rglob("*.extraction.md"):
        chapter_id = ext_file.name.removesuffix(".extraction.md")
        try:
            text = ext_file.read_text(encoding="utf-8")
        except OSError:
            continue
        m = _POV_LINE_RE.search(text)
        if not m:
            continue
        canonical_name = _parse_pov_canonical(m.group(1))
        slug = _resolve_slug(canonical_name, char_slugs, alias_map)
        if slug:
            chapter_pov[chapter_id] = slug
    return chapter_pov


# ---------------------------------------------------------------------------
# Support data loaders
# ---------------------------------------------------------------------------

def load_alias_resolver() -> dict[str, str]:
    if not ALIAS_RESOLVER_PATH.exists():
        return {}
    data = json.loads(ALIAS_RESOLVER_PATH.read_text(encoding="utf-8"))
    return data.get("alias_to_canonical", {})


def load_backlink_counts() -> dict[str, dict]:
    if not BACKLINK_COUNTS_PATH.exists():
        return {}
    data = json.loads(BACKLINK_COUNTS_PATH.read_text(encoding="utf-8"))
    return data.get("backlinks", {})


# ---------------------------------------------------------------------------
# Discover entity nodes for the given type config
# ---------------------------------------------------------------------------

def discover_entity_nodes(cfg: TypeConfig) -> list[tuple[str, str, str, Path]]:
    """Return [(slug, name, type, path)] for nodes matching the type config."""
    out: list[tuple[str, str, str, Path]] = []
    for node_dir_rel in cfg.node_dirs:
        node_dir = REPO_ROOT / node_dir_rel
        if not node_dir.exists():
            continue
        for node_file in node_dir.glob("*.node.md"):
            text = node_file.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(text)
            node_type = fm.get("type", "")
            if not any(node_type.startswith(p) for p in cfg.type_prefixes):
                continue
            slug = fm.get("slug") or node_file.name.removesuffix(".node.md")
            name = fm.get("name") or slug
            out.append((slug, name, node_type, node_file))
    return out


# ---------------------------------------------------------------------------
# Build mention inverse for all entity slugs of the given type
# ---------------------------------------------------------------------------

def _categorize_section(section: str, cfg: TypeConfig) -> str:
    """Categorize a mention section as 'primary', 'raw_list', or 'other'."""
    if section in cfg.primary_sections:
        return "primary"
    for kw in cfg.raw_list_section_keywords:
        if section.startswith(kw):
            return "raw_list"
    return "other"


def build_mention_inverse(
    entity_slugs: set[str],
    cfg: TypeConfig,
    chapter_pov_map: dict[str, str],
) -> dict[str, list[dict]]:
    """Walk all chapter mention files; return {slug: [chapter_record, ...]}.

    Each chapter_record:
      chapter_id, book, pov_character_slug, mention_count, sections,
      resolved_via, in_primary_section, in_raw_list
    """
    # Per slug, accumulate per-chapter data.
    # slug → chapter_id → accumulator
    per_slug_chapter: dict[str, dict[str, dict]] = defaultdict(dict)

    book_order = {"agot": 0, "acok": 1, "asos": 2, "affc": 3, "adwd": 4}

    if not MENTION_INDEX_DIR.exists():
        return {}

    for mfile in sorted(MENTION_INDEX_DIR.rglob("*.mentions.json")):
        try:
            data = json.loads(mfile.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        chapter_id = data.get("chapter_id")
        book = data.get("book")
        if not chapter_id or not book:
            continue
        pov_slug = chapter_pov_map.get(chapter_id)

        for m in data.get("mentions", []):
            slug = m.get("slug")
            if slug not in entity_slugs:
                continue
            section = m.get("section") or ""
            cat = _categorize_section(section, cfg)

            acc = per_slug_chapter[slug].setdefault(chapter_id, {
                "chapter_id": chapter_id,
                "book": book,
                "book_order": book_order.get(book, 99),
                "pov_character_slug": pov_slug,
                "mention_count": 0,
                "sections": set(),
                "resolved_via": m.get("resolved_via", "direct"),
                "in_primary_section": False,
                "in_raw_list": False,
            })
            acc["mention_count"] += 1
            acc["sections"].add(section)
            if cat == "primary":
                acc["in_primary_section"] = True
            elif cat == "raw_list":
                acc["in_raw_list"] = True

    # Flatten + sort
    result: dict[str, list[dict]] = {}
    for slug, chapters in per_slug_chapter.items():
        records = sorted(
            chapters.values(),
            key=lambda c: (c["book_order"], c["chapter_id"]),
        )
        # Convert sets to sorted lists; remove sort key
        for r in records:
            r["sections"] = sorted(r["sections"])
            del r["book_order"]
        result[slug] = records
    return result


# ---------------------------------------------------------------------------
# Build one entity index record
# ---------------------------------------------------------------------------

def build_one(
    slug: str,
    name: str,
    node_type: str,
    node_path: Path,
    chapter_records: list[dict],
    backlinks: dict[str, dict],
    cfg: TypeConfig,
) -> dict:
    body = node_path.read_text(encoding="utf-8")
    _fm, body_only = parse_frontmatter(body)
    out_edge_count = count_out_edges(body_only)

    bl = backlinks.get(slug, {})
    in_edge_count = bl.get("in_count", 0)

    appearances_total = sum(r["mention_count"] for r in chapter_records)

    # Build section-specific chapter lists
    primary_chapters = [r for r in chapter_records if r["in_primary_section"]]
    raw_list_chapters = [r for r in chapter_records if r["in_raw_list"]]
    # referenced_in = all chapters with any mention (the union)
    referenced_in = chapter_records  # already one record per chapter

    chapters_obj: dict = {}
    if cfg.primary_chapter_key:
        chapters_obj[cfg.primary_chapter_key] = primary_chapters
    chapters_obj["in_raw_list"] = raw_list_chapters
    chapters_obj["referenced_in"] = referenced_in

    stats: dict = {
        "appearances_total": appearances_total,
        "chapters_referenced_in": len(referenced_in),
        "chapters_in_raw_list": len(raw_list_chapters),
        "out_edge_count": out_edge_count,
        "in_edge_count": in_edge_count,
    }
    if cfg.primary_chapter_key:
        stats[f"chapters_{cfg.primary_chapter_key}"] = len(primary_chapters)

    return {
        "slug": slug,
        "name": name,
        "type": node_type,
        "node_path": str(node_path.relative_to(REPO_ROOT)),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stats": stats,
        "chapters": chapters_obj,
    }


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run(entity_type: str, only_slug: Optional[str], dry_run: bool) -> None:
    cfg = TYPE_CONFIGS[entity_type]
    out_dir = REPO_ROOT / cfg.output_dir

    print(f"Building {entity_type} indexes...", flush=True)
    print(f"  Output: {cfg.output_dir}", flush=True)

    print("Loading alias-resolver...", flush=True)
    alias_map = load_alias_resolver()
    print(f"  {len(alias_map):,} aliases.")

    print("Building chapter POV map from Pass 1 frontmatter...", flush=True)
    chapter_pov_map = build_chapter_pov_map(alias_map)
    print(f"  {len(chapter_pov_map):,} chapters with resolved POV slug.")

    print("Loading backlink counts...", flush=True)
    backlinks = load_backlink_counts()
    print(f"  {len(backlinks):,} slugs with backlink data.")

    print(f"Discovering {entity_type} nodes...", flush=True)
    nodes = discover_entity_nodes(cfg)
    print(f"  {len(nodes):,} nodes found.")

    if only_slug:
        nodes = [n for n in nodes if n[0] == only_slug]
        if not nodes:
            print(f"ERROR: no {entity_type} node found with slug '{only_slug}'.")
            sys.exit(1)

    entity_slugs = {slug for slug, *_ in nodes}

    print(f"Building mention inverse from chapter index...", flush=True)
    mention_inverse = build_mention_inverse(entity_slugs, cfg, chapter_pov_map)
    print(f"  {len(mention_inverse):,} slugs have at least one chapter mention.")

    print()
    print(f"Emitting per-entity index files...", flush=True)

    if not dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    type_counts: dict[str, int] = defaultdict(int)
    zero_mention_count = 0
    rolled_up: list[dict] = []

    for slug, name, node_type, node_path in nodes:
        chapter_records = mention_inverse.get(slug, [])
        if not chapter_records:
            zero_mention_count += 1
        type_counts[node_type] += 1

        record = build_one(slug, name, node_type, node_path,
                           chapter_records, backlinks, cfg)
        rolled_up.append({
            "slug": slug,
            "name": name,
            "type": node_type,
            "appearances_total": record["stats"]["appearances_total"],
            "chapters_referenced_in": record["stats"]["chapters_referenced_in"],
            "in_edge_count": record["stats"]["in_edge_count"],
            "out_edge_count": record["stats"]["out_edge_count"],
        })

        if not dry_run:
            out_path = out_dir / f"{slug}.index.json"
            out_path.write_text(
                json.dumps(record, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    print(f"  Emitted {len(rolled_up):,} {entity_type} indexes.")
    print()

    by_appearances = sorted(rolled_up, key=lambda r: -r["appearances_total"])[:20]
    by_inbound = sorted(rolled_up, key=lambda r: -r["in_edge_count"])[:20]

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "entity_type": entity_type,
        "dry_run": dry_run,
        "entity_count": len(rolled_up),
        "type_counts": dict(type_counts),
        "entities_with_zero_mentions": zero_mention_count,
        "mention_inverse_slugs": len(mention_inverse),
        "top_by_appearances": by_appearances,
        "top_by_in_edges": by_inbound,
    }

    if not dry_run:
        summary_path = out_dir / "_summary.json"
        summary_path.write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"Summary written to: {summary_path.relative_to(REPO_ROOT)}")

    print()
    print("=" * 60)
    print(f"{entity_type.upper()} INDEX BUILD SUMMARY")
    print("=" * 60)
    print(f"  Total indexes           : {len(rolled_up):,}")
    for t, c in sorted(type_counts.items()):
        print(f"    {t:<28}: {c:,}")
    print(f"  Zero-mention entities   : {zero_mention_count:,}")
    print()
    print(f"Top 15 by chapter appearances:")
    for r in by_appearances[:15]:
        print(f"  {r['slug']:<36}  appearances={r['appearances_total']:>4}  "
              f"chapters={r['chapters_referenced_in']:>3}  "
              f"in_edges={r['in_edge_count']:>4}")
    print()
    print(f"Top 10 by in-edge count:")
    for r in by_inbound[:10]:
        print(f"  {r['slug']:<36}  in_edges={r['in_edge_count']:>4}  "
              f"appearances={r['appearances_total']:>4}")
    print("=" * 60)


def main() -> None:
    p = argparse.ArgumentParser(
        description="Build per-entity index roll-ups for non-character node types."
    )
    p.add_argument("--type", required=True, choices=list(TYPE_CONFIGS),
                   metavar="TYPE",
                   help=f"Entity type to index: {', '.join(TYPE_CONFIGS)}")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--slug", metavar="SLUG",
                   help="Build only one entity (test mode).")
    g.add_argument("--all", action="store_true", dest="all_entities",
                   help="Build all entities of the given type (default).")
    p.add_argument("--dry-run", action="store_true",
                   help="Parse + compute, but don't write files.")
    args = p.parse_args()

    run(entity_type=args.type, only_slug=args.slug, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
