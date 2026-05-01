#!/usr/bin/env python3
"""Tier 3 Pass D — Character backfill.

Promotes minor characters referenced in family-tree / kill edges
(PARENT_OF, SPOUSE_OF, SIBLING_OF, LOVER_OF, HEIR_TO, KILLS) that have
wiki pages but no existing node in graph/nodes/characters/.

Pipeline:
  1. Read character-edge orphan slugs from post-Pass-C cat1-full.tsv.
  2. Drop slugs that resolve via alias-resolver (already Cat 2).
  3. Drop slugs already present in graph/nodes/characters/.
  4. Cross-reference with working/wiki-parsed/page-index.jsonl.
     Split into: promotable (wiki page exists) vs no-wiki.
  5. Write no-wiki list to working/wiki-pass2/tier3-pass-d-no-wiki.jsonl.
  6. Build manifest at working/wiki-pass2/tier3-characters/manifest.json.
  7. Emit skeletons — type from infobox (character.human / character.dragon /
     character.direwolf); falls back to character.human.
  8. Extract prose from sources/wiki/_raw/<Page_Name>.json.
  9. Promote: skeleton + prose → graph/nodes/characters/<slug>.node.md
     (atomic rename; conflicts go to graph/nodes/_conflicts/).
 10. Slug-regression check.

Usage:
  python3 scripts/wiki-pass2-tier3-pass-d-characters.py           # dry-run
  python3 scripts/wiki-pass2-tier3-pass-d-characters.py --apply   # write nodes
  python3 scripts/wiki-pass2-tier3-pass-d-characters.py --apply --verbose
  python3 scripts/wiki-pass2-tier3-pass-d-characters.py --plan    # print slug list only
"""

import argparse
import html as html_module
import json
import os
import re
import sys
import tempfile
import urllib.parse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Use the post-Pass-C TSV
CAT1_TSV = PROJECT_ROOT / "working" / "audits" / "orphan-edges-2026-04-30c-cat1-full.tsv"
PAGE_INDEX_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "page-index.jsonl"
INFOBOX_DATA_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "infobox-data.jsonl"
ALIAS_RESOLVER_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "alias-resolver.json"
WIKI_RAW_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
GRAPH_CHARS_DIR = PROJECT_ROOT / "graph" / "nodes" / "characters"
CONFLICTS_DIR = PROJECT_ROOT / "graph" / "nodes" / "_conflicts"
PASS_D_BUCKET_DIR = PROJECT_ROOT / "working" / "wiki-pass2" / "tier3-characters"
NO_WIKI_FILE = PROJECT_ROOT / "working" / "wiki-pass2" / "tier3-pass-d-no-wiki.jsonl"
BUCKET_ID = "tier3-characters"

# Edge types that target characters
CHARACTER_EDGE_TYPES = {"PARENT_OF", "SPOUSE_OF", "SIBLING_OF", "LOVER_OF", "HEIR_TO", "KILLS"}

# Allowed character sub-types
ALLOWED_CHAR_TYPES = {"character.human", "character.dragon", "character.direwolf"}
DEFAULT_CHAR_TYPE = "character.human"


# ---------------------------------------------------------------------------
# Slug generation — must match wiki-pass2-triage.py exactly
# ---------------------------------------------------------------------------

def page_to_slug(page_name: str) -> str:
    """Convert a wiki page name to a filesystem slug."""
    slug = page_name.lower()
    slug = re.sub(r"['\",]", "", slug)
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


# ---------------------------------------------------------------------------
# Wiki URL helper
# ---------------------------------------------------------------------------

def wiki_url(page_name: str) -> str:
    """Produce the canonical AWOIAF URL for a page name."""
    encoded = urllib.parse.quote(page_name.replace(" ", "_"), safe="/:@!$&'()*+,;=")
    return f"https://awoiaf.westeros.org/index.php/{encoded}"


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_page_index() -> tuple[dict[str, str], dict[str, dict]]:
    """Return (slug_to_page_name, page_name_to_record) from page-index.jsonl.

    slug_to_page maps the first page with that slug (collision: keep first).
    """
    slug_to_page: dict[str, str] = {}
    page_records: dict[str, dict] = {}
    with open(PAGE_INDEX_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            page_name = rec["page"]
            slug = page_to_slug(page_name)
            if slug not in slug_to_page:
                slug_to_page[slug] = page_name
            page_records[page_name] = rec
    return slug_to_page, page_records


def load_infobox_data() -> dict[str, dict]:
    """Return {page_name: record} from infobox-data.jsonl."""
    data: dict[str, dict] = {}
    with open(INFOBOX_DATA_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            data[rec["page"]] = rec
    return data


def load_alias_resolver() -> set[str]:
    """Return set of slugs that resolve via alias-resolver (Cat 2 — skip these)."""
    if not ALIAS_RESOLVER_FILE.exists():
        return set()
    data = json.loads(ALIAS_RESOLVER_FILE.read_text(encoding="utf-8"))
    return set(data.get("alias_to_canonical", {}).keys())


def load_existing_character_slugs() -> set[str]:
    """Return set of slugs already present in graph/nodes/characters/."""
    existing: set[str] = set()
    if GRAPH_CHARS_DIR.is_dir():
        for f in GRAPH_CHARS_DIR.iterdir():
            if f.suffix == ".md" and f.name.endswith(".node.md"):
                slug = f.name[: -len(".node.md")]
                existing.add(slug)
    return existing


# ---------------------------------------------------------------------------
# Orphan slug extraction
# ---------------------------------------------------------------------------

def load_character_edge_orphans() -> list[tuple[str, int]]:
    """Return [(slug, in_count)] for character-edge orphans from cat1 TSV.

    Filters for rows where example_edge_type is in CHARACTER_EDGE_TYPES.
    Sorted descending by in_count (highest-impact first).
    """
    slugs: dict[str, int] = {}
    with open(CAT1_TSV, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("rank"):
                continue
            parts = line.split("\t")
            if len(parts) < 8:
                continue
            # Columns: rank, target_slug, edge_count, in_count, is_title, is_date,
            #          example_source, example_edge_type, example_target_text
            edge_type = parts[7]
            if edge_type in CHARACTER_EDGE_TYPES:
                slug = parts[1]
                try:
                    in_count = int(parts[3])
                except ValueError:
                    in_count = 0
                if slug not in slugs:
                    slugs[slug] = in_count
    return sorted(slugs.items(), key=lambda x: -x[1])


# ---------------------------------------------------------------------------
# Skeleton renderer
# ---------------------------------------------------------------------------

def render_edge_line(rel: dict) -> str:
    """Render one relationship dict into an edge bullet line."""
    edge_type = rel.get("edge_type", "UNKNOWN_EDGE")
    target = rel.get("target", "")
    field = rel.get("field", "")
    direction = rel.get("direction", "forward")
    qualifier = rel.get("qualifier", "")

    edge_label = f"{edge_type} (reverse)" if direction == "reverse" else edge_type
    line = f"- {edge_label}: {target} (track_b: {field})"
    if qualifier:
        line += f" [{qualifier}]"
    return line


def resolve_char_type(infobox_rec: dict | None) -> str:
    """Resolve character sub-type from infobox record.

    Returns one of: character.human, character.dragon, character.direwolf.
    Falls back to character.human for no-infobox or unknown types.
    """
    if infobox_rec is None:
        return DEFAULT_CHAR_TYPE
    inferred = infobox_rec.get("entity_type", "")
    if inferred in ALLOWED_CHAR_TYPES:
        return inferred
    return DEFAULT_CHAR_TYPE


def render_skeleton(
    page_name: str,
    slug: str,
    char_type: str,
    aliases: list[str],
    relationships: list[dict],
    infobox_found: bool,
) -> str:
    """Render a character skeleton node as a markdown string."""
    url = wiki_url(page_name)

    alias_items = ", ".join(f'"{a}"' for a in aliases) if aliases else ""
    aliases_yaml = f"[{alias_items}]" if aliases else "[]"

    lines = [
        "---",
        f'name: "{page_name}"',
        f"type: {char_type}",
        f"slug: {slug}",
        f"aliases: {aliases_yaml}",
        "confidence: tier-1",
        f'wiki_source: "{url}"',
        f"bucket_id: {BUCKET_ID}",
        "prompt_version: v1-python",
        "node_version: 1",
        "pass_origin: pass2-wiki-deterministic",
        "---",
        "",
        "## Identity",
        "",
        f"{page_name} is a character from the AWOIAF wiki.",
        "",
        "## Edges",
        "",
    ]

    if infobox_found and relationships:
        for rel in relationships:
            lines.append(render_edge_line(rel))

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Prose extractor (mirrors wiki-pass2-extract-prose.py conventions)
# ---------------------------------------------------------------------------

H2_HEADING_MAP: dict[str, str] = {
    "history": "Origins",
    "background": "Origins",
    "prelude": "Origins",
    "legend": "Origins",
    "appearance and character": "Appearances & Description",
    "appearance": "Appearances & Description",
    "character": "Appearances & Description",
    "character and appearance": "Appearances & Description",
    "layout": "Appearances & Description",
    "city": "Appearances & Description",
    "culture": "Culture",
    "organization": "Organization",
    "structure": "Organization",
    "recent events": "Narrative Arc",
    "battle": "Narrative Arc",
    "siege": "Narrative Arc",
    "synopsis": "Narrative Arc",
    "aftermath": "Aftermath",
    "quotes": "Quotes",
}

SKIP_H2 = {
    "family", "behind the scenes", "references", "external links",
    "contents", "members", "notable members", "notes", "see also",
    "gallery", "appendix",
}


def _strip_html_tags(text: str) -> str:
    """Remove HTML tags, expand common entities."""
    text = re.sub(r"<[^>]+>", "", text)
    text = html_module.unescape(text)
    return text


def _convert_wiki_link(match: re.Match) -> str:
    """Convert <a href="...">text</a> to (wiki:Page_Name) form."""
    href = match.group(1)
    inner = match.group(2)
    m = re.search(r"/index\.php/([^#?\"]+)", href)
    if m:
        page_raw = urllib.parse.unquote(m.group(1))
        return f"[{inner}](wiki:{page_raw})"
    return inner


def _normalize_prose_line(line: str, page_name: str) -> str:
    """Apply wiki-link and cite-ref conversions to one prose line."""
    page_name_underscored = page_name.replace(" ", "_")
    line = re.sub(
        r'<sup[^>]*\bid="(cite_ref-[^"]+)"[^>]*>.*?</sup>',
        lambda m: f"(wiki:{page_name_underscored}.{m.group(1)})",
        line,
        flags=re.DOTALL,
    )
    line = re.sub(
        r'<a[^>]+href="([^"]*)"[^>]*>(.*?)</a>',
        _convert_wiki_link,
        line,
        flags=re.DOTALL,
    )
    line = _strip_html_tags(line)
    line = re.sub(r"\s+", " ", line).strip()
    return line


def extract_prose(page_name: str) -> str | None:
    """Extract prose from sources/wiki/_raw/<Page_Name>.json.

    Returns prose markdown string (may be empty), or None if raw file missing.
    """
    safe_filename = page_name.replace(" ", "_").replace("/", "_")
    raw_path = WIKI_RAW_DIR / f"{safe_filename}.json"
    if not raw_path.exists():
        return None

    try:
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

    html_body = raw.get("html", "") or raw.get("body", "") or ""
    if not html_body:
        return None

    sections_raw = re.split(r"(<h2\b[^>]*>.*?</h2>)", html_body, flags=re.DOTALL | re.IGNORECASE)

    output_sections: list[str] = []
    current_schema_heading: str | None = None
    current_lines: list[str] = []

    def flush_section():
        nonlocal current_lines
        if current_schema_heading and current_lines:
            body = "\n".join(l for l in current_lines if l)
            if body.strip():
                output_sections.append(f"## {current_schema_heading}\n\n{body.strip()}")
        current_lines = []

    i = 0
    while i < len(sections_raw):
        chunk = sections_raw[i]
        h2_match = re.match(r"<h2\b[^>]*>(.*?)</h2>", chunk, flags=re.DOTALL | re.IGNORECASE)
        if h2_match:
            flush_section()
            heading_raw = _strip_html_tags(h2_match.group(1)).strip().lower()
            matched_schema = None
            for key, schema in H2_HEADING_MAP.items():
                if heading_raw == key or heading_raw.startswith(key):
                    matched_schema = schema
                    break
            if matched_schema is None and heading_raw.startswith("quotes"):
                matched_schema = "Quotes"
            if matched_schema is None or heading_raw in SKIP_H2:
                current_schema_heading = None
            else:
                current_schema_heading = matched_schema
            current_lines = []
        else:
            if current_schema_heading:
                sub_chunks = re.split(
                    r"(<h3\b[^>]*>.*?</h3>|<p\b[^>]*>.*?</p>|<li\b[^>]*>.*?</li>)",
                    chunk,
                    flags=re.DOTALL | re.IGNORECASE,
                )
                for sub in sub_chunks:
                    sub = sub.strip()
                    if not sub:
                        continue
                    h3_match = re.match(r"<h3\b[^>]*>(.*?)</h3>", sub, flags=re.DOTALL | re.IGNORECASE)
                    if h3_match:
                        h3_text = _strip_html_tags(h3_match.group(1)).strip()
                        if h3_text:
                            current_lines.append(f"\n### {h3_text}\n")
                    elif re.match(r"<p\b", sub, re.IGNORECASE) or re.match(r"<li\b", sub, re.IGNORECASE):
                        inner = re.sub(r"^<[^>]+>", "", sub)
                        inner = re.sub(r"</[^>]+>$", "", inner)
                        line = _normalize_prose_line(inner, page_name)
                        if line:
                            current_lines.append(line)
        i += 1

    flush_section()

    if not output_sections:
        return ""

    return "\n\n".join(output_sections) + "\n"


# ---------------------------------------------------------------------------
# Manifest builder
# ---------------------------------------------------------------------------

def build_manifest(pages: list[tuple[str, str]]) -> dict:
    """Build manifest dict for the tier3-characters bucket."""
    return {
        "bucket_id": BUCKET_ID,
        "tier": "secondary",
        "tier_default": "tier-1",
        "prompt_version": "v1-python",
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
        "status": "pending",
        "started_at": None,
        "completed_at": None,
        "validation_report": None,
        "pages": [{"page": page_name, "slug": slug} for slug, page_name in pages],
    }


# ---------------------------------------------------------------------------
# Atomic write helper
# ---------------------------------------------------------------------------

def atomic_write(dest_path: Path, content: bytes) -> str:
    """Atomically write content to dest_path. Returns 'wrote', 'skipped', or 'conflict'."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    if dest_path.exists():
        existing = dest_path.read_bytes()
        if existing == content:
            return "skipped"
        CONFLICTS_DIR.mkdir(parents=True, exist_ok=True)
        conflict_path = CONFLICTS_DIR / dest_path.name
        conflict_path.write_bytes(existing)
        result = "conflict"
    else:
        result = "wrote"

    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=dest_path.parent, prefix=f".tmp_{dest_path.name}_"
    )
    try:
        os.write(tmp_fd, content)
        os.close(tmp_fd)
        os.rename(tmp_path, dest_path)
    except Exception:
        os.close(tmp_fd)
        Path(tmp_path).unlink(missing_ok=True)
        raise

    return result


# ---------------------------------------------------------------------------
# Slug-regression check
# ---------------------------------------------------------------------------

def check_slug_regression(newly_promoted: list[str]) -> list[str]:
    """Return list of newly promoted files where slug ends in '.node' (regression bug)."""
    bad: list[str] = []
    slug_pattern = re.compile(r"^slug:\s+.*\.node\s*$", re.MULTILINE)
    if not GRAPH_CHARS_DIR.is_dir():
        return bad
    for slug in newly_promoted:
        f = GRAPH_CHARS_DIR / f"{slug}.node.md"
        if not f.exists():
            continue
        content = f.read_text(encoding="utf-8")
        if slug_pattern.search(content):
            bad.append(f.name)
    return bad


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Tier 3 Pass D: promote missing character nodes from "
            "PARENT_OF / SPOUSE_OF / SIBLING_OF / LOVER_OF / HEIR_TO / KILLS orphans."
        )
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Write files. Without this flag, dry-run only."
    )
    parser.add_argument(
        "--plan", action="store_true",
        help="Print slug list and counts, then exit (no writes)."
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Print per-page detail."
    )
    args = parser.parse_args()

    dry_run = not args.apply

    # ------------------------------------------------------------------
    # Step 1: Load orphan slugs filtered to character edge types
    # ------------------------------------------------------------------
    all_orphan_slugs = load_character_edge_orphans()
    print(f"Character-edge orphan slugs from TSV: {len(all_orphan_slugs)}")
    print(f"  (Edge types: {', '.join(sorted(CHARACTER_EDGE_TYPES))})")

    # ------------------------------------------------------------------
    # Step 2: Drop alias-resolver hits (Cat 2 cases)
    # ------------------------------------------------------------------
    alias_slugs = load_alias_resolver()
    alias_filtered = [(s, c) for s, c in all_orphan_slugs if s in alias_slugs]
    candidates = [(s, c) for s, c in all_orphan_slugs if s not in alias_slugs]
    print(f"  Alias-resolver hits (skip): {len(alias_filtered)}")
    if args.verbose and alias_filtered:
        for slug, count in alias_filtered:
            print(f"    ALIAS SKIP: {slug}")

    # ------------------------------------------------------------------
    # Step 3: Drop slugs already in graph/nodes/characters/
    # ------------------------------------------------------------------
    existing_chars = load_existing_character_slugs()
    already_exists = [(s, c) for s, c in candidates if s in existing_chars]
    candidates = [(s, c) for s, c in candidates if s not in existing_chars]
    print(f"  Already have nodes (skip): {len(already_exists)}")

    # ------------------------------------------------------------------
    # Step 4: Cross-reference with page-index
    # ------------------------------------------------------------------
    slug_to_page, _ = load_page_index()

    promotable: list[tuple[str, str, int]] = []  # (slug, page_name, in_count)
    no_wiki: list[tuple[str, int]] = []

    for slug, in_count in candidates:
        if slug in slug_to_page:
            promotable.append((slug, slug_to_page[slug], in_count))
        else:
            no_wiki.append((slug, in_count))

    print(f"  Has wiki page (promotable): {len(promotable)}")
    print(f"  No wiki page (backlog):     {len(no_wiki)}")

    if args.plan:
        print()
        print("=== Promotable slugs (sorted by in_count) ===")
        for slug, page, count in promotable:
            print(f"  {count:4d}  {slug}  ->  {page}")
        print()
        print("=== No-wiki slugs (top 50) ===")
        for slug, count in sorted(no_wiki, key=lambda x: -x[1])[:50]:
            print(f"  {count:4d}  {slug}")
        return

    # ------------------------------------------------------------------
    # Step 5: Write no-wiki list
    # ------------------------------------------------------------------
    if args.apply:
        PASS_D_BUCKET_DIR.parent.mkdir(parents=True, exist_ok=True)
        with open(NO_WIKI_FILE, "w", encoding="utf-8") as f:
            for slug, count in sorted(no_wiki, key=lambda x: -x[1]):
                rec = {"slug": slug, "in_count": count, "reason": "no-wiki-page"}
                f.write(json.dumps(rec) + "\n")
        print(f"\nWrote no-wiki backlog ({len(no_wiki)} entries) to: {NO_WIKI_FILE}")
    else:
        print(f"\n[DRY-RUN] Would write {len(no_wiki)} no-wiki entries to: {NO_WIKI_FILE}")

    # ------------------------------------------------------------------
    # Step 6: Build manifest
    # ------------------------------------------------------------------
    pages_for_manifest = [(slug, page) for slug, page, _ in promotable]
    manifest = build_manifest(pages_for_manifest)

    skeleton_dir = PASS_D_BUCKET_DIR / "skeleton"
    prose_dir = PASS_D_BUCKET_DIR / "prose"

    if args.apply:
        PASS_D_BUCKET_DIR.mkdir(parents=True, exist_ok=True)
        manifest_path = PASS_D_BUCKET_DIR / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        skeleton_dir.mkdir(parents=True, exist_ok=True)
        prose_dir.mkdir(parents=True, exist_ok=True)
        print(f"Wrote manifest: {manifest_path}")
    else:
        print(f"\n[DRY-RUN] Would write manifest with {len(promotable)} pages to:")
        print(f"  {PASS_D_BUCKET_DIR / 'manifest.json'}")

    # ------------------------------------------------------------------
    # Step 7: Load infobox data and emit skeletons
    # ------------------------------------------------------------------
    infobox_data = load_infobox_data()
    print(f"\nLoaded infobox data ({len(infobox_data)} pages)")

    print("\n--- Emitting skeletons ---")
    skeleton_count = 0
    type_counts: Counter = Counter()
    type_overrides: list[str] = []  # pages that had non-character infobox types

    for slug, page_name, in_count in promotable:
        infobox_rec = infobox_data.get(page_name)
        aliases: list[str] = []
        relationships: list[dict] = []
        infobox_found = infobox_rec is not None

        if infobox_found:
            aliases = infobox_rec.get("aliases", [])
            relationships = infobox_rec.get("relationships", [])
            inferred_type = infobox_rec.get("entity_type", "unknown")
            if inferred_type and inferred_type not in ALLOWED_CHAR_TYPES and inferred_type != "unknown":
                type_overrides.append(f"{page_name}: {inferred_type} -> {DEFAULT_CHAR_TYPE}")

        char_type = resolve_char_type(infobox_rec)
        type_counts[char_type] += 1

        skeleton_content = render_skeleton(
            page_name=page_name,
            slug=slug,
            char_type=char_type,
            aliases=aliases,
            relationships=relationships,
            infobox_found=infobox_found,
        )

        # Verify slug doesn't end in .node (regression check)
        if re.search(r"^slug:.*\.node\s*$", skeleton_content, re.MULTILINE):
            print(f"  ERROR: slug regression for {page_name}: slug contains .node suffix",
                  file=sys.stderr)

        skeleton_path = skeleton_dir / f"{slug}.node.md"
        if args.apply:
            skeleton_path.write_text(skeleton_content, encoding="utf-8")
        else:
            if args.verbose:
                print(f"  [DRY-RUN] skeleton: {slug}.node.md  type={char_type}  ({len(relationships)} edges)")

        skeleton_count += 1

    print(f"  Skeletons: {skeleton_count}")
    for t, c in type_counts.most_common():
        print(f"    {t}: {c}")
    if type_overrides:
        print(f"  Type overrides (forced to {DEFAULT_CHAR_TYPE}):")
        for msg in type_overrides[:20]:
            print(f"    {msg}")
        if len(type_overrides) > 20:
            print(f"    ... and {len(type_overrides) - 20} more")

    # ------------------------------------------------------------------
    # Step 8: Extract prose
    # ------------------------------------------------------------------
    print("\n--- Extracting prose ---")
    prose_written = 0
    prose_empty = 0
    prose_missing_raw = 0

    for slug, page_name, in_count in promotable:
        prose_content = extract_prose(page_name)

        if prose_content is None:
            prose_missing_raw += 1
            if args.verbose:
                print(f"  MISSING raw file: {page_name}")
            continue

        prose_path = prose_dir / f"{slug}.prose.md"
        if not prose_content.strip():
            prose_empty += 1
            if args.apply:
                prose_path.write_bytes(b"")
            continue

        if args.apply:
            prose_path.write_text(prose_content, encoding="utf-8")
        prose_written += 1
        if args.verbose:
            print(f"  prose: {slug}.prose.md ({len(prose_content)} bytes)")

    print(f"  Prose extracted: {prose_written}")
    print(f"  Prose empty (skeleton-only): {prose_empty}")
    print(f"  Raw file missing: {prose_missing_raw}")

    # ------------------------------------------------------------------
    # Step 9: Promote (skeleton + prose → graph/nodes/characters/)
    # ------------------------------------------------------------------
    print("\n--- Promoting nodes ---")

    if not args.apply:
        print(f"  [DRY-RUN] Would promote {skeleton_count} nodes to: {GRAPH_CHARS_DIR}")
    else:
        GRAPH_CHARS_DIR.mkdir(parents=True, exist_ok=True)

    stats: Counter = Counter()
    newly_promoted: list[str] = []

    for slug, page_name, in_count in promotable:
        skeleton_path = skeleton_dir / f"{slug}.node.md"
        prose_path = prose_dir / f"{slug}.prose.md"

        if not args.apply:
            stats["dry_run"] += 1
            continue

        if not skeleton_path.exists():
            print(f"  WARNING: skeleton missing for {slug}, skipping", file=sys.stderr)
            stats["error"] += 1
            continue

        skeleton_bytes = skeleton_path.read_bytes()

        if prose_path.exists() and prose_path.stat().st_size > 0:
            prose_bytes = prose_path.read_bytes()
            final_bytes = skeleton_bytes + b"\n" + prose_bytes
        else:
            final_bytes = skeleton_bytes

        dest_path = GRAPH_CHARS_DIR / f"{slug}.node.md"
        result = atomic_write(dest_path, final_bytes)
        stats[result] += 1
        newly_promoted.append(slug)

        if args.verbose:
            print(f"  {result}: {slug}.node.md")

    if args.apply:
        print(f"  wrote:    {stats['wrote']}")
        print(f"  skipped:  {stats['skipped']} (byte-identical)")
        print(f"  conflict: {stats['conflict']} (saved to _conflicts/)")
        print(f"  errors:   {stats['error']}")
    else:
        print(f"  [DRY-RUN] {stats['dry_run']} nodes would be promoted")

    # ------------------------------------------------------------------
    # Step 10: Slug-regression check
    # ------------------------------------------------------------------
    print("\n--- Slug regression check ---")
    if args.apply and newly_promoted:
        bad_slugs = check_slug_regression(newly_promoted)
        if bad_slugs:
            print(f"  REGRESSION: {len(bad_slugs)} nodes have slug ending in '.node':")
            for f in bad_slugs:
                print(f"    {f}")
        else:
            print(f"  OK: 0 newly promoted nodes with slug: *.node")
    else:
        print(f"  (dry-run — skipping regression check)")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n=== Summary ===")
    print(f"Character-edge orphan slugs in TSV:  {len(all_orphan_slugs)}")
    print(f"Alias-resolver hits (skipped):       {len(alias_filtered)}")
    print(f"Already had nodes (skipped):         {len(already_exists)}")
    print(f"Promotable (wiki page found):        {len(promotable)}")
    print(f"No wiki page (backlog):              {len(no_wiki)}")
    if args.apply:
        print(f"Nodes written:                       {stats['wrote']}")
        print(f"Nodes skipped (identical):           {stats['skipped']}")
        print(f"Conflicts logged:                    {stats['conflict']}")
        total_char_nodes = len(list(GRAPH_CHARS_DIR.glob("*.node.md")))
        print(f"Total character nodes after pass:    {total_char_nodes}")
        print()
        print("Type breakdown:")
        for t, c in type_counts.most_common():
            print(f"  {t}: {c}")
    else:
        print(f"\n[DRY-RUN] Run with --apply to write files.")
    print()


if __name__ == "__main__":
    main()
