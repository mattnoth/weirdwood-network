#!/usr/bin/env python3
"""Path B Sub-task 6 — Promote long-tail (titles + magic + cultures + species).

Driven by entity_type_guess in {'title', 'concept.magic', 'concept.culture', 'species'} from
page-index.jsonl (post-categorizer Path B classification).

place.region (7 pages — Sothoryos, White Waste, Grey Waste, Cannibal
Sands, etc.) is folded into graph/nodes/locations/ per the existing
TYPE_DIR_MAP convention; a future migration can split if a regions/
directory is formally adopted.

Pipeline mirrors wiki-pass2-tier3-pathb-texts.py.

Usage:
  python3 scripts/wiki-pass2-tier3-pathb-longtail.py           # dry-run
  python3 scripts/wiki-pass2-tier3-pathb-longtail.py --apply
  python3 scripts/wiki-pass2-tier3-pathb-longtail.py --plan
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

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

PAGE_INDEX_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "page-index.jsonl"
INFOBOX_DATA_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "infobox-data.jsonl"
WIKI_RAW_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
GRAPH_NODES_DIR = PROJECT_ROOT / "graph" / "nodes"
GRAPH_TITLES_DIR = PROJECT_ROOT / "graph" / "nodes" / "titles"
GRAPH_CONCEPTS_DIR = PROJECT_ROOT / "graph" / "nodes" / "concepts"
GRAPH_FACTIONS_DIR = PROJECT_ROOT / "graph" / "nodes" / "factions"
GRAPH_SPECIES_DIR = PROJECT_ROOT / "graph" / "nodes" / "species"
GRAPH_THEORIES_DIR = PROJECT_ROOT / "graph" / "nodes" / "theories"
GRAPH_FOODS_DIR = PROJECT_ROOT / "graph" / "nodes" / "foods"

# concept.culture routes to factions/ per Pass B precedent (existing
# culture nodes: first-men, ironborn, free-folk, dornishmen, etc.).
# A future migration can split if a cultures/ directory is adopted.
TYPE_TO_DIR = {
    "title":           GRAPH_TITLES_DIR,
    "concept.magic":   GRAPH_CONCEPTS_DIR,
    "concept.culture": GRAPH_FACTIONS_DIR,
    "concept.theory":  GRAPH_THEORIES_DIR,
    "species":         GRAPH_SPECIES_DIR,
    "object.food":     GRAPH_FOODS_DIR,
}
CONFLICTS_DIR = PROJECT_ROOT / "graph" / "nodes" / "_conflicts"
BUCKET_DIR = PROJECT_ROOT / "working" / "wiki-pass2" / "tier3-pathb-longtail"
BUCKET_ID = "tier3-pathb-longtail"

# Default node type written into skeletons; the per-page type from
# page-index.jsonl overrides this (place.location vs place.region).
NODE_TYPE_DEFAULT = "title"
TARGET_TYPES = set(TYPE_TO_DIR.keys())

# No glossary skip pages for locations — leave the set empty so the
# pipeline shape stays identical to artifacts.
# Dragon page is categorized as Magic but is the species page; should be
# species/Dragon. Skip from this batch — will need a parser-level override.
GLOSSARY_SKIP_PAGES: set[str] = {"Dragon"}


def page_to_slug(page_name: str) -> str:
    slug = page_name.lower()
    slug = re.sub(r"['\",]", "", slug)
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def wiki_url(page_name: str) -> str:
    encoded = urllib.parse.quote(
        page_name.replace(" ", "_"), safe="/:@!$&'()*+,;="
    )
    return f"https://awoiaf.westeros.org/index.php/{encoded}"


def load_target_pages() -> tuple[list[tuple[str, str, str]], list[str]]:
    """Return (kept_pages, skipped_glossary_pages).

    Each kept page is (slug, page_name, entity_type) so per-page type
    (place.location vs place.region) flows through to the skeleton.
    """
    kept: list[tuple[str, str, str]] = []
    skipped: list[str] = []
    with open(PAGE_INDEX_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            etype = rec.get("entity_type_guess")
            if etype not in TARGET_TYPES:
                continue
            page_name = rec["page"]
            if page_name in GLOSSARY_SKIP_PAGES:
                skipped.append(page_name)
                continue
            kept.append((page_to_slug(page_name), page_name, etype))
    return kept, skipped


def load_infobox_data() -> dict[str, dict]:
    data: dict[str, dict] = {}
    with open(INFOBOX_DATA_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            data[rec["page"]] = rec
    return data


def load_existing_slugs_all() -> set[str]:
    existing: set[str] = set()
    if GRAPH_NODES_DIR.is_dir():
        for f in GRAPH_NODES_DIR.rglob("*.node.md"):
            slug = f.name[: -len(".node.md")]
            existing.add(slug)
    return existing


def render_edge_line(rel: dict) -> str:
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
    entity_type: str,
    aliases: list[str],
    relationships: list[dict],
    infobox_found: bool,
) -> str:
    url = wiki_url(page_name)
    alias_items = ", ".join(f'"{a}"' for a in aliases) if aliases else ""
    aliases_yaml = f"[{alias_items}]" if aliases else "[]"

    if entity_type == "title":
        identity_line = f"{page_name} is a title from the AWOIAF wiki."
    elif entity_type == "concept.magic":
        identity_line = f"{page_name} is a magical concept/practice from the AWOIAF wiki."
    elif entity_type == "concept.culture":
        identity_line = f"{page_name} is a culture/people from the AWOIAF wiki."
    elif entity_type == "concept.theory":
        identity_line = f"{page_name} is a fan theory / interpretive framework from the AWOIAF wiki."
    elif entity_type == "object.food":
        identity_line = f"{page_name} is a food or drink from the AWOIAF wiki."
    else:
        identity_line = f"{page_name} is a species from the AWOIAF wiki."

    lines = [
        "---",
        f'name: "{page_name}"',
        f"type: {entity_type}",
        f"slug: {slug}",
        f"aliases: {aliases_yaml}",
        "confidence: tier-2",
        f'wiki_source: "{url}"',
        f"bucket_id: {BUCKET_ID}",
        "prompt_version: v1-python",
        "node_version: 1",
        "pass_origin: pass2-wiki-deterministic",
        "---",
        "",
        "## Identity",
        "",
        identity_line,
        "",
        "## Edges",
        "",
    ]

    if infobox_found and relationships:
        for rel in relationships:
            lines.append(render_edge_line(rel))

    lines.append("")
    return "\n".join(lines)


# --- Prose extraction (identical to texts script) ---
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
    safe_filename = (
        page_name.replace(":", "_").replace(" ", "_").replace("/", "_")
    )
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

    sections_raw = re.split(
        r"(<h2\b[^>]*>.*?</h2>)", html_body, flags=re.DOTALL | re.IGNORECASE
    )

    output_sections: list[str] = []
    current_schema_heading: str | None = None
    current_lines: list[str] = []

    def flush_section():
        nonlocal current_lines
        if current_schema_heading and current_lines:
            body = "\n".join(l for l in current_lines if l)
            if body.strip():
                output_sections.append(
                    f"## {current_schema_heading}\n\n{body.strip()}"
                )
        current_lines = []

    for chunk in sections_raw:
        h2_match = re.match(
            r"<h2\b[^>]*>(.*?)</h2>", chunk, flags=re.DOTALL | re.IGNORECASE
        )
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
                    h3_match = re.match(
                        r"<h3\b[^>]*>(.*?)</h3>",
                        sub,
                        flags=re.DOTALL | re.IGNORECASE,
                    )
                    if h3_match:
                        h3_text = _strip_html_tags(h3_match.group(1)).strip()
                        if h3_text:
                            current_lines.append(f"\n### {h3_text}\n")
                    elif re.match(r"<p\b", sub, re.IGNORECASE) or re.match(
                        r"<li\b", sub, re.IGNORECASE
                    ):
                        inner = re.sub(r"^<[^>]+>", "", sub)
                        inner = re.sub(r"</[^>]+>$", "", inner)
                        line = _normalize_prose_line(inner, page_name)
                        if line:
                            current_lines.append(line)

    flush_section()

    if not output_sections:
        return ""

    return "\n\n".join(output_sections) + "\n"


def build_manifest(pages: list[tuple[str, str, str]]) -> dict:
    return {
        "bucket_id": BUCKET_ID,
        "tier": "secondary",
        "tier_default": "tier-2",
        "prompt_version": "v1-python",
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
        "status": "pending",
        "started_at": None,
        "completed_at": None,
        "validation_report": None,
        "pages": [
            {"page": page_name, "slug": slug, "type": etype}
            for slug, page_name, etype in pages
        ],
    }


def atomic_write(dest_path: Path, content: bytes) -> str:
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


def check_slug_regression() -> list[str]:
    """Check all three target dirs (houses/religions/factions) for slug bugs."""
    bad: list[str] = []
    slug_pattern = re.compile(r"^slug:\s+.*\.node\s*$", re.MULTILINE)
    for dest in TYPE_TO_DIR.values():
        if not dest.is_dir():
            continue
        for f in dest.iterdir():
            if not f.name.endswith(".node.md"):
                continue
            content = f.read_text(encoding="utf-8")
            if slug_pattern.search(content):
                bad.append(f"{dest.name}/{f.name}")
    return bad


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Path B Sub-task 2: promote long-tail nodes (titles, concepts, species)."
    )
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    target_pages, glossary_skipped = load_target_pages()
    type_breakdown = Counter(t for _, _, t in target_pages)
    print(
        f"Pages with entity_type_guess in {sorted(TARGET_TYPES)}: "
        f"{len(target_pages) + len(glossary_skipped)}"
    )
    for t, n in sorted(type_breakdown.items()):
        print(f"    {t}: {n}")
    if glossary_skipped:
        print(f"  Glossary skips: {len(glossary_skipped)}")
        for p in sorted(glossary_skipped):
            print(f"    - {p}")

    existing_all = load_existing_slugs_all()

    promotable: list[tuple[str, str, str]] = []
    already_exists: list[str] = []
    for slug, page_name, etype in target_pages:
        if slug in existing_all:
            already_exists.append(slug)
        else:
            promotable.append((slug, page_name, etype))

    print(f"  Already in graph (skip):  {len(already_exists)}")
    print(f"  NEW promotable:           {len(promotable)}")

    if args.plan:
        print()
        print("=== Promotable pages ===")
        for slug, page, etype in promotable:
            print(f"  [{etype:<14}] {slug:55s} <- {page}")
        return

    manifest = build_manifest(promotable)
    skeleton_dir = BUCKET_DIR / "skeleton"
    prose_dir = BUCKET_DIR / "prose"

    if args.apply:
        BUCKET_DIR.mkdir(parents=True, exist_ok=True)
        manifest_path = BUCKET_DIR / "manifest.json"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        skeleton_dir.mkdir(parents=True, exist_ok=True)
        prose_dir.mkdir(parents=True, exist_ok=True)
        print(f"\nWrote manifest: {manifest_path}")
    else:
        print(f"\n[DRY-RUN] Would write manifest with {len(promotable)} pages.")

    infobox_data = load_infobox_data()
    print(f"Loaded infobox data ({len(infobox_data)} pages)")

    print("\n--- Emitting skeletons ---")
    skeleton_count = 0
    type_override_count = 0
    no_infobox = 0
    edge_count_total = 0

    for slug, page_name, etype in promotable:
        infobox_rec = infobox_data.get(page_name)
        aliases: list[str] = []
        relationships: list[dict] = []
        infobox_found = infobox_rec is not None

        if infobox_found:
            aliases = infobox_rec.get("aliases", [])
            relationships = infobox_rec.get("relationships", [])
            edge_count_total += len(relationships)
            inferred_type = infobox_rec.get("entity_type", "unknown")
            if inferred_type and inferred_type != etype and inferred_type != "unknown":
                type_override_count += 1
                if args.verbose:
                    print(
                        f"  TYPE OVERRIDE: {page_name}: {inferred_type} -> {etype}"
                    )
        else:
            no_infobox += 1

        skeleton_content = render_skeleton(
            page_name=page_name,
            slug=slug,
            entity_type=etype,
            aliases=aliases,
            relationships=relationships,
            infobox_found=infobox_found,
        )

        if re.search(r"^slug:.*\.node\s*$", skeleton_content, re.MULTILINE):
            print(
                f"  ERROR: slug regression detected for {page_name}", file=sys.stderr
            )

        if args.apply:
            (skeleton_dir / f"{slug}.node.md").write_text(
                skeleton_content, encoding="utf-8"
            )

        skeleton_count += 1

    print(
        f"  Skeletons: {skeleton_count} "
        f"(no-infobox: {no_infobox}, type overrides: {type_override_count}, "
        f"total edges: {edge_count_total})"
    )

    print("\n--- Extracting prose ---")
    prose_written = 0
    prose_empty = 0
    prose_missing_raw = 0

    for slug, page_name, etype in promotable:
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

    print(f"  Prose extracted: {prose_written}")
    print(f"  Prose empty (skeleton-only): {prose_empty}")
    print(f"  Raw file missing: {prose_missing_raw}")

    print(f"\n--- Promoting nodes (per-type routing) ---")

    if not args.apply:
        print(f"  [DRY-RUN] Would promote {skeleton_count} nodes.")
    else:
        for d in TYPE_TO_DIR.values():
            d.mkdir(parents=True, exist_ok=True)

    stats: Counter = Counter()
    per_dir_stats: Counter = Counter()

    for slug, page_name, etype in promotable:
        skeleton_path = skeleton_dir / f"{slug}.node.md"
        prose_path = prose_dir / f"{slug}.prose.md"

        if not args.apply:
            stats["dry_run"] += 1
            continue

        if not skeleton_path.exists():
            print(f"  WARNING: skeleton missing for {slug}", file=sys.stderr)
            stats["error"] += 1
            continue

        skeleton_bytes = skeleton_path.read_bytes()
        if prose_path.exists() and prose_path.stat().st_size > 0:
            prose_bytes = prose_path.read_bytes()
            final_bytes = skeleton_bytes + b"\n" + prose_bytes
        else:
            final_bytes = skeleton_bytes

        dest_dir = TYPE_TO_DIR[etype]
        dest_path = dest_dir / f"{slug}.node.md"
        result = atomic_write(dest_path, final_bytes)
        stats[result] += 1
        per_dir_stats[dest_dir.name] += 1

        if args.verbose:
            print(f"  {result}: {dest_dir.name}/{slug}.node.md")

    if args.apply:
        print(f"  wrote:    {stats['wrote']}")
        print(f"  skipped:  {stats['skipped']} (byte-identical)")
        print(f"  conflict: {stats['conflict']} (saved to _conflicts/)")
        print(f"  errors:   {stats['error']}")

    print("\n--- Slug regression check ---")
    bad_slugs = check_slug_regression()
    if bad_slugs:
        print(f"  REGRESSION: {len(bad_slugs)} long-tail nodes with slug ending in '.node':")
        for f in bad_slugs:
            print(f"    {f}")
    else:
        print(f"  OK: 0 long-tail nodes with slug: *.node")

    print("\n=== Summary ===")
    print(f"Long-tail pages in index:                {len(target_pages) + len(glossary_skipped)}")
    print(f"Glossary skips:                   {len(glossary_skipped)}")
    print(f"Already had nodes (skipped):      {len(already_exists)}")
    print(f"Promotable (NEW):                 {len(promotable)}")
    promotable_breakdown = Counter(t for _, _, t in promotable)
    for t, n in sorted(promotable_breakdown.items()):
        print(f"    {t}: {n}")
    print(f"Target dirs:                      {sorted(d.name for d in TYPE_TO_DIR.values())}")
    if args.apply:
        print(f"Nodes written:                    {stats['wrote']}")
        print(f"Nodes skipped (identical):        {stats['skipped']}")
        print(f"Conflicts logged:                 {stats['conflict']}")
        for dname, n in sorted(per_dir_stats.items()):
            print(f"    -> {dname}: {n}")
        total_longtail_nodes = sum(
            len(list(d.glob("*.node.md"))) for d in TYPE_TO_DIR.values() if d.is_dir()
        )
        print(f"Total long-tail nodes after pass:      {total_longtail_nodes}")
    else:
        print(f"\n[DRY-RUN] Run with --apply to write files.")
    print()


if __name__ == "__main__":
    main()
