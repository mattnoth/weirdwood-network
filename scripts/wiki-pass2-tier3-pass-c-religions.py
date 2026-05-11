#!/usr/bin/env python3
"""Tier 3 Pass C — Promote missing religion / god nodes.

Builds and runs the Stage 3 pipeline for WORSHIPS orphan slugs that have
corresponding wiki pages but no existing node in graph/nodes/religions/.

Also adds alias mappings (e.g., old-gods → old-gods-of-the-forest) to
working/wiki/data/alias-resolver.json for short-form variants that should
resolve to an existing canonical node.

Pipeline:
  1. Build the Pass C target list from WORSHIPS orphan slugs in cat1-full.tsv,
     supplemented by the curated instruction list of religion/god slugs.
  2. Cross-reference with working/wiki/data/page-index.jsonl.
     Split into: promotable (wiki page exists) vs no-wiki.
  3. Filter out slugs already in graph/nodes/religions/.
  4. Write no-wiki list to working/wiki/pass2-buckets/tier3-pass-c-no-wiki.jsonl.
  5. Build manifest at working/wiki/pass2-buckets/tier3-religions/manifest.json.
  6. Emit skeletons with type: organization.religion.
  7. Extract prose from sources/wiki/_raw/<Page_Name>.json.
  8. Promote: skeleton + prose → graph/nodes/religions/<slug>.node.md
     (atomic rename; conflicts go to graph/nodes/_conflicts/).
  9. Add alias entries (old-gods → old-gods-of-the-forest, etc.) to alias-resolver.json.
 10. Slug-regression check.

Usage:
  python3 scripts/wiki-pass2-tier3-pass-c-religions.py           # dry-run
  python3 scripts/wiki-pass2-tier3-pass-c-religions.py --apply   # write nodes
  python3 scripts/wiki-pass2-tier3-pass-c-religions.py --apply --verbose
  python3 scripts/wiki-pass2-tier3-pass-c-religions.py --plan    # print slug list only
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

# Use the post-Pass-A TSV (b suffix)
CAT1_TSV = PROJECT_ROOT / "working" / "audits" / "orphan-edges-2026-04-30b-cat1-full.tsv"
PAGE_INDEX_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "page-index.jsonl"
INFOBOX_DATA_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "infobox-data.jsonl"
WIKI_RAW_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
GRAPH_RELIGIONS_DIR = PROJECT_ROOT / "graph" / "nodes" / "religions"
CONFLICTS_DIR = PROJECT_ROOT / "graph" / "nodes" / "_conflicts"
PASS_C_BUCKET_DIR = PROJECT_ROOT / "working" / "wiki" / "pass2-buckets" / "tier3-religions"
NO_WIKI_FILE = PROJECT_ROOT / "working" / "wiki" / "pass2-buckets" / "tier3-pass-c-no-wiki.jsonl"
ALIAS_RESOLVER_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "alias-resolver.json"
BUCKET_ID = "tier3-religions"

# ---------------------------------------------------------------------------
# Curated Pass C target list
# These slugs are either WORSHIPS orphans from the TSV or are mentioned in the
# Pass C plan. We promote everything with a wiki page.
#
# Slugs without a wiki page go to no-wiki backlog.
# Slugs that should map to an existing canonical node go to ALIAS_ADDITIONS.
# ---------------------------------------------------------------------------

# These slugs have no direct wiki page of their own — they need to be aliased
# to an existing canonical node rather than promoted as new nodes.
ALIAS_ADDITIONS: dict[str, str] = {
    # Short-form "Old gods" (lowercase, used by location nodes) → existing node
    "old-gods": "old-gods-of-the-forest",
    # "Mixed" and "Mixed religions" are parser artifacts, not real entities;
    # no alias target exists — they go to no-wiki backlog.
    # "Dothraki" as a WORSHIPS target means the Dothraki horse-god religion,
    # but there's no distinct religion node for it — alias to no-wiki for now.
}

# Slugs that are religion/god candidates to promote (curated + TSV-sourced).
# Any slug in ALIAS_ADDITIONS is NOT promoted (it gets aliased instead).
PASS_C_CANDIDATES: list[str] = [
    # Direct WORSHIPS orphans from TSV (post-Pass-A)
    "boash",
    "black-goat",
    # Major god/religion pages from Pass C plan
    "many-faced-god",
    "black-goat-of-qohor",
    "lion-of-night",
    "maiden-made-of-light",
    "storm-god",
    "trios",
    "crab-king",
    # The Seven (individual aspects) — simple slug form used in WORSHIPS edges
    # 'stranger', 'smith', 'maid', 'mother' have direct wiki pages
    # 'father', 'warrior', 'crone' redirect to disambiguation pages — handled below
    "stranger",
    "smith",
    "maid",
    "mother",
    # Direct wiki pages found in page-index
    "father-above",          # Father Above — canonical AWOIAF page for Father aspect
]

# Some Seven aspects have disambig pages (e.g. 'Stranger (the Seven)') but no
# simple slug. We promote using the (the Seven) slug where available, and add
# a short-slug alias pointing to the new node.
# Format: (orphan_slug_needing_alias, wiki_page_name, canonical_slug_to_create)
SEVEN_ASPECTS_WITH_DISAMBIG: list[tuple[str, str, str]] = [
    ("warrior", "Warrior (the Seven)", "warrior-the-seven"),
    ("crone",   "Crone (the Seven)",   "crone-the-seven"),
    # father: Father Above is the canonical page; father-above is in main list
    # stranger: direct page exists
    # smith: direct page exists
    # maiden/maid: 'Maid' page exists (listed as 'maid' in main list)
]

# Additional alias entries for short-form → canonical (added alongside promotion)
# These point at the nodes being created in this pass.
ADDITIONAL_ALIASES_FROM_PASS: dict[str, str] = {
    "warrior":       "warrior-the-seven",
    "crone":         "crone-the-seven",
    "father":        "father-above",
    "maiden":        "maid",          # 'Maiden' wiki page slugifies to 'maiden', 'maid' is the promoted slug
    "stranger-the-seven": "stranger", # ensure (the Seven) form resolves to simple 'stranger' node
}


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
    """Return (slug_to_page_name, page_name_to_record) from page-index.jsonl."""
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


def load_existing_religion_slugs() -> set[str]:
    """Return set of slugs already present in graph/nodes/religions/."""
    existing: set[str] = set()
    if GRAPH_RELIGIONS_DIR.is_dir():
        for f in GRAPH_RELIGIONS_DIR.iterdir():
            if f.suffix == ".md" and f.name.endswith(".node.md"):
                slug = f.name[: -len(".node.md")]
                existing.add(slug)
    return existing


# ---------------------------------------------------------------------------
# Orphan slug extraction from TSV
# ---------------------------------------------------------------------------

def load_worships_orphans_from_tsv() -> list[tuple[str, int]]:
    """Return [(slug, edge_count)] for WORSHIPS orphans from cat1 TSV.

    Sorted descending by edge_count.
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
            # Column 8 (index 7) is example_edge_type in this TSV schema
            if parts[7] == "WORSHIPS":
                slug = parts[1]
                try:
                    edge_count = int(parts[2])
                except ValueError:
                    edge_count = 0
                if slug not in slugs:
                    slugs[slug] = edge_count
    return sorted(slugs.items(), key=lambda x: -x[1])


# ---------------------------------------------------------------------------
# Skeleton renderer (religion-specific — type is always 'organization.religion')
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


def render_skeleton(
    page_name: str,
    slug: str,
    aliases: list[str],
    relationships: list[dict],
    infobox_found: bool,
) -> str:
    """Render a religion/god skeleton node as a markdown string.

    Type is always 'organization.religion' regardless of infobox classification.
    """
    url = wiki_url(page_name)

    alias_items = ", ".join(f'"{a}"' for a in aliases) if aliases else ""
    aliases_yaml = f"[{alias_items}]" if aliases else "[]"

    lines = [
        "---",
        f'name: "{page_name}"',
        "type: organization.religion",
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
        f"{page_name} is a religion or divine entity from the AWOIAF wiki.",
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
# Prose extractor (mirrors wiki-pass2-tier3-pass-a-titles.py)
# ---------------------------------------------------------------------------

H2_HEADING_MAP: dict[str, str] = {
    "history": "Origins",
    "background": "Origins",
    "prelude": "Origins",
    "legend": "Origins",
    "myths and legends": "Origins",
    "origin": "Origins",
    "appearance and character": "Appearances & Description",
    "appearance": "Appearances & Description",
    "character": "Appearances & Description",
    "character and appearance": "Appearances & Description",
    "layout": "Appearances & Description",
    "city": "Appearances & Description",
    "culture": "Culture",
    "organization": "Organization",
    "structure": "Organization",
    "religious practices": "Organization",
    "worship": "Organization",
    "clergy": "Organization",
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
    text = re.sub(r"<[^>]+>", "", text)
    text = html_module.unescape(text)
    return text


def _convert_wiki_link(match: re.Match) -> str:
    href = match.group(1)
    inner = match.group(2)
    m = re.search(r"/index\.php/([^#?\"]+)", href)
    if m:
        page_raw = urllib.parse.unquote(m.group(1))
        return f"[{inner}](wiki:{page_raw})"
    return inner


def _normalize_prose_line(line: str, page_name: str) -> str:
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
    """Build manifest dict for the tier3-religions bucket."""
    return {
        "bucket_id": BUCKET_ID,
        "tier": "tier-1",
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
# Alias-resolver updater
# ---------------------------------------------------------------------------

def update_alias_resolver(new_aliases: dict[str, str], dry_run: bool, verbose: bool) -> int:
    """Add new_aliases to alias_to_canonical in alias-resolver.json.

    Returns count of entries actually added (skipping existing ones).
    """
    data = json.loads(ALIAS_RESOLVER_FILE.read_text(encoding="utf-8"))
    alias_to_canonical = data.get("alias_to_canonical", {})

    added = 0
    for alias, canonical in sorted(new_aliases.items()):
        if alias in alias_to_canonical:
            if verbose:
                existing = alias_to_canonical[alias]
                if existing == canonical:
                    print(f"  ALIAS SKIP (already exists): {alias} -> {canonical}")
                else:
                    print(f"  ALIAS COLLISION: {alias} -> {existing} (want {canonical}); keeping existing")
            continue
        if verbose:
            print(f"  ALIAS ADD: {alias} -> {canonical}")
        alias_to_canonical[alias] = canonical
        added += 1

    if added > 0:
        data["alias_to_canonical"] = dict(sorted(alias_to_canonical.items()))
        if not dry_run:
            ALIAS_RESOLVER_FILE.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
    return added


# ---------------------------------------------------------------------------
# Slug-regression check
# ---------------------------------------------------------------------------

def check_slug_regression() -> list[str]:
    """Return list of religion node files where slug ends in '.node' (regression bug)."""
    bad: list[str] = []
    slug_pattern = re.compile(r"^slug:\s+.*\.node\s*$", re.MULTILINE)
    if not GRAPH_RELIGIONS_DIR.is_dir():
        return bad
    for f in GRAPH_RELIGIONS_DIR.iterdir():
        if not f.name.endswith(".node.md"):
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
        description="Tier 3 Pass C: promote missing religion / god nodes from WORSHIPS orphans."
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
    # Step 1: Build candidate set
    # ------------------------------------------------------------------
    tsv_orphans = load_worships_orphans_from_tsv()
    tsv_slugs = {slug for slug, _ in tsv_orphans}

    print(f"WORSHIPS orphan slugs from TSV: {len(tsv_orphans)}")
    if tsv_orphans:
        for slug, count in tsv_orphans:
            print(f"  {count:3d}e  {slug}")

    # Merge TSV orphans with curated list (deduplicate)
    all_candidates = list(dict.fromkeys(
        [s for s, _ in tsv_orphans] + PASS_C_CANDIDATES
        + [slug for slug, _, _ in SEVEN_ASPECTS_WITH_DISAMBIG]
    ))
    # Remove slugs that are alias-only (not to be promoted as new nodes)
    all_candidates = [s for s in all_candidates if s not in ALIAS_ADDITIONS]

    print(f"\nTotal unique promotion candidates (curated + TSV, excluding alias-only): {len(all_candidates)}")

    # ------------------------------------------------------------------
    # Step 2: Cross-reference with page-index
    # ------------------------------------------------------------------
    slug_to_page, _ = load_page_index()
    existing_religions = load_existing_religion_slugs()

    print(f"\nExisting religion nodes: {sorted(existing_religions)}")

    # For SEVEN_ASPECTS_WITH_DISAMBIG: the target slug to create is the disambig slug
    # (e.g. warrior-the-seven), and we add alias_from → disambig_slug
    # Build a special mapping: orphan_slug → (wiki_page, node_slug_to_create)
    seven_disambig_map: dict[str, tuple[str, str]] = {
        orphan: (page, node_slug)
        for orphan, page, node_slug in SEVEN_ASPECTS_WITH_DISAMBIG
    }

    promotable: list[tuple[str, str, str, int]] = []  # (orphan_slug, wiki_page, node_slug, edge_count)
    no_wiki: list[tuple[str, int]] = []
    already_exists: list[str] = []
    alias_only: list[str] = list(ALIAS_ADDITIONS.keys())

    tsv_edge_counts = dict(tsv_orphans)

    for slug in all_candidates:
        edge_count = tsv_edge_counts.get(slug, 0)

        # Handle disambig Seven aspects
        if slug in seven_disambig_map:
            wiki_page, node_slug = seven_disambig_map[slug]
            if node_slug in existing_religions:
                already_exists.append(slug)
            else:
                # Verify the page actually exists
                actual_page = slug_to_page.get(node_slug)
                if actual_page:
                    promotable.append((slug, actual_page, node_slug, edge_count))
                else:
                    # Try the wiki page directly
                    page_slug = page_to_slug(wiki_page)
                    if page_slug in slug_to_page:
                        promotable.append((slug, slug_to_page[page_slug], node_slug, edge_count))
                    else:
                        no_wiki.append((slug, edge_count))
            continue

        # Normal slug
        if slug in existing_religions:
            already_exists.append(slug)
        elif slug in slug_to_page:
            promotable.append((slug, slug_to_page[slug], slug, edge_count))
        else:
            no_wiki.append((slug, edge_count))

    print(f"\nAlias-only (not promoted): {len(alias_only)}")
    for a, canon in ALIAS_ADDITIONS.items():
        print(f"  {a} -> {canon}")
    print(f"Already have nodes (skip):  {len(already_exists)}")
    print(f"Has wiki page (promotable): {len(promotable)}")
    print(f"No wiki page (backlog):     {len(no_wiki)}")

    if args.plan:
        print()
        print("=== Promotable slugs ===")
        for orphan_slug, page, node_slug, count in promotable:
            disambig = f" [node: {node_slug}]" if orphan_slug != node_slug else ""
            print(f"  {count:3d}e  {orphan_slug}  ->  {page}{disambig}")
        print()
        print("=== No-wiki slugs (backlog) ===")
        for slug, count in sorted(no_wiki, key=lambda x: -x[1]):
            print(f"  {count:3d}e  {slug}")
        print()
        print("=== Alias additions ===")
        all_aliases = dict(ALIAS_ADDITIONS)
        for orphan, _, node_slug in SEVEN_ASPECTS_WITH_DISAMBIG:
            all_aliases[orphan] = node_slug
        all_aliases.update(ADDITIONAL_ALIASES_FROM_PASS)
        for a, c in sorted(all_aliases.items()):
            print(f"  {a} -> {c}")
        return

    # ------------------------------------------------------------------
    # Step 3: Write no-wiki backlog
    # ------------------------------------------------------------------
    if args.apply:
        PASS_C_BUCKET_DIR.parent.mkdir(parents=True, exist_ok=True)
        with open(NO_WIKI_FILE, "w", encoding="utf-8") as f:
            for slug, count in sorted(no_wiki, key=lambda x: -x[1]):
                rec = {"slug": slug, "edge_count": count, "reason": "no-wiki-page"}
                f.write(json.dumps(rec) + "\n")
        print(f"\nWrote no-wiki backlog to: {NO_WIKI_FILE}")
    else:
        print(f"\n[DRY-RUN] Would write {len(no_wiki)} no-wiki entries to: {NO_WIKI_FILE}")

    # ------------------------------------------------------------------
    # Step 4: Build manifest
    # ------------------------------------------------------------------
    # De-duplicate by node_slug (two orphan slugs could point to same page/node)
    seen_node_slugs: dict[str, tuple[str, str, int]] = {}
    for orphan_slug, page, node_slug, edge_count in promotable:
        if node_slug not in seen_node_slugs:
            seen_node_slugs[node_slug] = (orphan_slug, page, edge_count)

    unique_promotable = [(node_slug, page) for node_slug, (_, page, _) in seen_node_slugs.items()]
    manifest = build_manifest(unique_promotable)

    skeleton_dir = PASS_C_BUCKET_DIR / "skeleton"
    prose_dir = PASS_C_BUCKET_DIR / "prose"

    if args.apply:
        PASS_C_BUCKET_DIR.mkdir(parents=True, exist_ok=True)
        manifest_path = PASS_C_BUCKET_DIR / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        skeleton_dir.mkdir(parents=True, exist_ok=True)
        prose_dir.mkdir(parents=True, exist_ok=True)
        print(f"Wrote manifest: {manifest_path}")
    else:
        print(f"\n[DRY-RUN] Would write manifest with {len(unique_promotable)} pages to:")
        print(f"  {PASS_C_BUCKET_DIR / 'manifest.json'}")

    # ------------------------------------------------------------------
    # Step 5: Load infobox data
    # ------------------------------------------------------------------
    infobox_data = load_infobox_data()
    print(f"\nLoaded infobox data ({len(infobox_data)} pages)")

    # ------------------------------------------------------------------
    # Step 6: Emit skeletons
    # ------------------------------------------------------------------
    print("\n--- Emitting skeletons ---")
    skeleton_count = 0
    type_override_count = 0

    for node_slug, page_name in unique_promotable:
        infobox_rec = infobox_data.get(page_name)
        aliases: list[str] = []
        relationships: list[dict] = []
        infobox_found = infobox_rec is not None

        if infobox_found:
            aliases = infobox_rec.get("aliases", [])
            relationships = infobox_rec.get("relationships", [])
            inferred_type = infobox_rec.get("entity_type", "unknown")
            if inferred_type and inferred_type not in ("organization.religion", "religion", "unknown"):
                type_override_count += 1
                if args.verbose:
                    print(f"  TYPE OVERRIDE: {page_name}: {inferred_type} -> organization.religion")

        skeleton_content = render_skeleton(
            page_name=page_name,
            slug=node_slug,
            aliases=aliases,
            relationships=relationships,
            infobox_found=infobox_found,
        )

        # Verify slug doesn't end in .node (regression check)
        if re.search(r"^slug:.*\.node\s*$", skeleton_content, re.MULTILINE):
            print(f"  ERROR: slug regression for {page_name}: slug contains .node suffix", file=sys.stderr)

        skeleton_path = skeleton_dir / f"{node_slug}.node.md"
        if args.apply:
            skeleton_path.write_text(skeleton_content, encoding="utf-8")
        else:
            if args.verbose:
                print(f"  [DRY-RUN] skeleton: {node_slug}.node.md ({len(relationships)} edges, page: {page_name})")

        skeleton_count += 1

    print(f"  Skeletons: {skeleton_count} (type overrides applied: {type_override_count})")

    # ------------------------------------------------------------------
    # Step 7: Extract prose
    # ------------------------------------------------------------------
    print("\n--- Extracting prose ---")
    prose_written = 0
    prose_empty = 0
    prose_missing_raw = 0

    for node_slug, page_name in unique_promotable:
        prose_content = extract_prose(page_name)

        if prose_content is None:
            prose_missing_raw += 1
            if args.verbose:
                print(f"  MISSING raw file: {page_name}")
            continue

        prose_path = prose_dir / f"{node_slug}.prose.md"
        if not prose_content.strip():
            prose_empty += 1
            if args.apply:
                prose_path.write_bytes(b"")
            continue

        if args.apply:
            prose_path.write_text(prose_content, encoding="utf-8")
        prose_written += 1
        if args.verbose:
            print(f"  prose: {node_slug}.prose.md ({len(prose_content)} bytes)")

    print(f"  Prose extracted: {prose_written}")
    print(f"  Prose empty (skeleton-only): {prose_empty}")
    print(f"  Raw file missing: {prose_missing_raw}")

    # ------------------------------------------------------------------
    # Step 8: Promote (skeleton + prose → graph/nodes/religions/)
    # ------------------------------------------------------------------
    print("\n--- Promoting nodes ---")

    if not args.apply:
        print(f"  [DRY-RUN] Would promote {skeleton_count} nodes to: {GRAPH_RELIGIONS_DIR}")
    else:
        GRAPH_RELIGIONS_DIR.mkdir(parents=True, exist_ok=True)

    stats = Counter()

    for node_slug, page_name in unique_promotable:
        skeleton_path = skeleton_dir / f"{node_slug}.node.md"
        prose_path = prose_dir / f"{node_slug}.prose.md"

        if not args.apply:
            stats["dry_run"] += 1
            continue

        if not skeleton_path.exists():
            print(f"  WARNING: skeleton missing for {node_slug}, skipping", file=sys.stderr)
            stats["error"] += 1
            continue

        skeleton_bytes = skeleton_path.read_bytes()

        if prose_path.exists() and prose_path.stat().st_size > 0:
            prose_bytes = prose_path.read_bytes()
            final_bytes = skeleton_bytes + b"\n" + prose_bytes
        else:
            final_bytes = skeleton_bytes

        dest_path = GRAPH_RELIGIONS_DIR / f"{node_slug}.node.md"
        result = atomic_write(dest_path, final_bytes)
        stats[result] += 1

        if args.verbose:
            print(f"  {result}: {node_slug}.node.md")

    if args.apply:
        print(f"  wrote:    {stats['wrote']}")
        print(f"  skipped:  {stats['skipped']} (byte-identical)")
        print(f"  conflict: {stats['conflict']} (saved to _conflicts/)")
        print(f"  errors:   {stats['error']}")
    else:
        print(f"  [DRY-RUN] {stats['dry_run']} nodes would be promoted")

    # ------------------------------------------------------------------
    # Step 9: Update alias-resolver.json
    # ------------------------------------------------------------------
    print("\n--- Updating alias-resolver ---")

    # Build complete alias additions:
    # 1. ALIAS_ADDITIONS (old-gods → old-gods-of-the-forest, etc.)
    # 2. Disambig Seven aspects: orphan_slug → node_slug_created
    # 3. ADDITIONAL_ALIASES_FROM_PASS
    all_new_aliases: dict[str, str] = {}
    all_new_aliases.update(ALIAS_ADDITIONS)
    for orphan, _, node_slug in SEVEN_ASPECTS_WITH_DISAMBIG:
        all_new_aliases[orphan] = node_slug
    all_new_aliases.update(ADDITIONAL_ALIASES_FROM_PASS)

    if not dry_run:
        added_count = update_alias_resolver(all_new_aliases, dry_run=False, verbose=args.verbose)
        print(f"  Alias entries added: {added_count}")
    else:
        print(f"  [DRY-RUN] Would add up to {len(all_new_aliases)} alias entries:")
        for a, c in sorted(all_new_aliases.items()):
            print(f"    {a} -> {c}")

    # ------------------------------------------------------------------
    # Step 10: Slug-regression check
    # ------------------------------------------------------------------
    print("\n--- Slug regression check ---")
    bad_slugs = check_slug_regression()
    if bad_slugs:
        print(f"  REGRESSION: {len(bad_slugs)} religion nodes have slug ending in '.node':")
        for f in bad_slugs:
            print(f"    {f}")
    else:
        print(f"  OK: 0 religion nodes with slug: *.node")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n=== Summary ===")
    print(f"WORSHIPS orphan slugs in TSV:          {len(tsv_orphans)}")
    print(f"Alias-only (no node created):          {len(alias_only)}")
    print(f"Already had nodes (skipped):           {len(already_exists)}")
    print(f"Promotable (wiki page found):          {len(unique_promotable)}")
    print(f"No wiki page (backlog):                {len(no_wiki)}")
    if args.apply:
        print(f"Nodes written:                         {stats['wrote']}")
        print(f"Nodes skipped (identical):             {stats['skipped']}")
        print(f"Conflicts logged:                      {stats['conflict']}")
        total_religion_nodes = len(list(GRAPH_RELIGIONS_DIR.glob("*.node.md")))
        print(f"Total religion nodes after pass:       {total_religion_nodes}")
    else:
        print(f"\n[DRY-RUN] Run with --apply to write files.")
    print()


if __name__ == "__main__":
    main()
