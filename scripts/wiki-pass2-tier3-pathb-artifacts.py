#!/usr/bin/env python3
"""Path B Sub-task 1b — Promote object.artifact nodes (named weapons, ships, etc.).

Driven by entity_type_guess == 'object.artifact' from page-index.jsonl
(post-categorizer Path B classification).

Resolves orphan WIELDS edges: jon -> Longclaw, arya -> Needle,
visenya -> Dark Sister, etc.

Glossary-page filter: 7 weapon-type concept pages (Arakh, Bastard sword,
Falchion, Greatsword, Longsword, Shortsword, Armament) are tagged with
MediaWiki's "Terms" or "Science and technology" categories — they're
glossary entries, not narrative artifacts. Skip them. (A parser-level
fix isn't appropriate because Terms is also legitimately used for
titles, events, magic concepts.)

Pipeline mirrors wiki-pass2-tier3-pathb-texts.py.

Usage:
  python3 scripts/wiki-pass2-tier3-pathb-artifacts.py           # dry-run
  python3 scripts/wiki-pass2-tier3-pathb-artifacts.py --apply
  python3 scripts/wiki-pass2-tier3-pathb-artifacts.py --plan
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

PAGE_INDEX_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "page-index.jsonl"
INFOBOX_DATA_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "infobox-data.jsonl"
WIKI_RAW_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
GRAPH_NODES_DIR = PROJECT_ROOT / "graph" / "nodes"
GRAPH_ARTIFACTS_DIR = PROJECT_ROOT / "graph" / "nodes" / "artifacts"
CONFLICTS_DIR = PROJECT_ROOT / "graph" / "nodes" / "_conflicts"
BUCKET_DIR = PROJECT_ROOT / "working" / "wiki" / "pass2-buckets" / "tier3-pathb-artifacts"
BUCKET_ID = "tier3-pathb-artifacts"

NODE_TYPE = "object.artifact"
TARGET_TYPE = "object.artifact"
DEST_DIR = GRAPH_ARTIFACTS_DIR

# Weapon-type glossary pages — skip from artifact promotion.
GLOSSARY_SKIP_PAGES = {
    "Arakh", "Bastard sword", "Falchion", "Greatsword",
    "Longsword", "Shortsword", "Armament",
}


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


def load_target_pages() -> tuple[list[tuple[str, str]], list[str]]:
    """Return (kept_pages, skipped_glossary_pages)."""
    kept: list[tuple[str, str]] = []
    skipped: list[str] = []
    with open(PAGE_INDEX_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("entity_type_guess") != TARGET_TYPE:
                continue
            page_name = rec["page"]
            if page_name in GLOSSARY_SKIP_PAGES:
                skipped.append(page_name)
                continue
            kept.append((page_to_slug(page_name), page_name))
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
    aliases: list[str],
    relationships: list[dict],
    infobox_found: bool,
) -> str:
    url = wiki_url(page_name)
    alias_items = ", ".join(f'"{a}"' for a in aliases) if aliases else ""
    aliases_yaml = f"[{alias_items}]" if aliases else "[]"

    lines = [
        "---",
        f'name: "{page_name}"',
        f"type: {NODE_TYPE}",
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
        f"{page_name} is an artifact (named weapon, ship, or object) from the AWOIAF wiki.",
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


def build_manifest(pages: list[tuple[str, str]]) -> dict:
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
        "pages": [{"page": page_name, "slug": slug} for slug, page_name in pages],
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
    bad: list[str] = []
    slug_pattern = re.compile(r"^slug:\s+.*\.node\s*$", re.MULTILINE)
    if not DEST_DIR.is_dir():
        return bad
    for f in DEST_DIR.iterdir():
        if not f.name.endswith(".node.md"):
            continue
        content = f.read_text(encoding="utf-8")
        if slug_pattern.search(content):
            bad.append(f.name)
    return bad


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Path B Sub-task 1b: promote object.artifact nodes."
    )
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    target_pages, glossary_skipped = load_target_pages()
    print(
        f"Pages with entity_type_guess == {TARGET_TYPE!r}: "
        f"{len(target_pages) + len(glossary_skipped)}"
    )
    print(f"  Glossary skips (weapon types): {len(glossary_skipped)}")
    if glossary_skipped:
        for p in sorted(glossary_skipped):
            print(f"    - {p}")
    print(f"  After glossary filter:        {len(target_pages)}")

    existing_all = load_existing_slugs_all()

    promotable: list[tuple[str, str]] = []
    already_exists: list[str] = []
    for slug, page_name in target_pages:
        if slug in existing_all:
            already_exists.append(slug)
        else:
            promotable.append((slug, page_name))

    print(f"  Already in graph (skip):  {len(already_exists)}")
    print(f"  NEW promotable:           {len(promotable)}")

    if args.plan:
        print()
        print("=== Promotable pages ===")
        for slug, page in promotable:
            print(f"  {slug:55s} <- {page}")
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

    for slug, page_name in promotable:
        infobox_rec = infobox_data.get(page_name)
        aliases: list[str] = []
        relationships: list[dict] = []
        infobox_found = infobox_rec is not None

        if infobox_found:
            aliases = infobox_rec.get("aliases", [])
            relationships = infobox_rec.get("relationships", [])
            edge_count_total += len(relationships)
            inferred_type = infobox_rec.get("entity_type", "unknown")
            if inferred_type and inferred_type != NODE_TYPE and inferred_type != "unknown":
                type_override_count += 1
                if args.verbose:
                    print(
                        f"  TYPE OVERRIDE: {page_name}: {inferred_type} -> {NODE_TYPE}"
                    )
        else:
            no_infobox += 1

        skeleton_content = render_skeleton(
            page_name=page_name,
            slug=slug,
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

    for slug, page_name in promotable:
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

    print(f"\n--- Promoting nodes to {DEST_DIR} ---")

    if not args.apply:
        print(f"  [DRY-RUN] Would promote {skeleton_count} nodes.")
    else:
        DEST_DIR.mkdir(parents=True, exist_ok=True)

    stats: Counter = Counter()

    for slug, page_name in promotable:
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

        dest_path = DEST_DIR / f"{slug}.node.md"
        result = atomic_write(dest_path, final_bytes)
        stats[result] += 1

        if args.verbose:
            print(f"  {result}: {slug}.node.md")

    if args.apply:
        print(f"  wrote:    {stats['wrote']}")
        print(f"  skipped:  {stats['skipped']} (byte-identical)")
        print(f"  conflict: {stats['conflict']} (saved to _conflicts/)")
        print(f"  errors:   {stats['error']}")

    print("\n--- Slug regression check ---")
    bad_slugs = check_slug_regression()
    if bad_slugs:
        print(f"  REGRESSION: {len(bad_slugs)} artifact nodes with slug ending in '.node':")
        for f in bad_slugs:
            print(f"    {f}")
    else:
        print(f"  OK: 0 artifact nodes with slug: *.node")

    print("\n=== Summary ===")
    print(f"object.artifact pages in index:   {len(target_pages) + len(glossary_skipped)}")
    print(f"Glossary skips:                   {len(glossary_skipped)}")
    print(f"Already had nodes (skipped):      {len(already_exists)}")
    print(f"Promotable (NEW):                 {len(promotable)}")
    print(f"Node type used:                   {NODE_TYPE}")
    print(f"Target directory:                 {DEST_DIR}")
    if args.apply:
        print(f"Nodes written:                    {stats['wrote']}")
        print(f"Nodes skipped (identical):        {stats['skipped']}")
        print(f"Conflicts logged:                 {stats['conflict']}")
        total_artifact_nodes = (
            len(list(DEST_DIR.glob("*.node.md"))) if DEST_DIR.is_dir() else 0
        )
        print(f"Total artifact nodes after pass:  {total_artifact_nodes}")
    else:
        print(f"\n[DRY-RUN] Run with --apply to write files.")
    print()


if __name__ == "__main__":
    main()
