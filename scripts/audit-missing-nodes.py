#!/usr/bin/env python3
"""audit-missing-nodes.py

Audits the gap between the wiki cache and the graph: wiki pages that EXIST in
`sources/wiki/_raw/` and have content, but were never promoted to a graph
node in `graph/nodes/`. Sorts candidates by Pass 1 mention frequency so the
top of the report is the most-likely-needed backfills.

Surfaces three classes:
  (A) Pass 1 mentions an entity, but no graph node exists for it.
      Highest priority — the chapter extractions know it's there.
  (B) Wiki page is heavily backlinked by other wiki pages, but no graph node.
      Medium priority — other pages reference it.
  (C) Wiki page exists with content, no graph node, no Pass 1 mention, low
      backlinks. Lowest priority — probably genuinely peripheral.

Also flags case-collision crawl bugs (the Pate-the-Novice class): wiki pages
where only the redirect variant survived the crawl due to case-insensitive
macOS filesystem.

Output: a markdown report at working/audits/missing-nodes-YYYY-MM-DD/execution/
missing-nodes.md, plus a JSON sidecar.

Usage:
    python3 scripts/audit-missing-nodes.py
    python3 scripts/audit-missing-nodes.py --top 50
"""

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_RAW_DIR = REPO_ROOT / "sources" / "wiki" / "_raw"
PAGE_INDEX_PATH = REPO_ROOT / "working" / "wiki" / "data" / "page-index.jsonl"
BACKLINK_PATH = REPO_ROOT / "working" / "wiki" / "data" / "backlink-counts.json"
GRAPH_NODES_DIR = REPO_ROOT / "graph" / "nodes"
MENTION_SUMMARY_PATH = REPO_ROOT / "graph" / "index" / "chapters" / "_summary.json"
ALIAS_RESOLVER_PATH = REPO_ROOT / "working" / "wiki" / "data" / "alias-resolver.json"


def to_kebab(text: str) -> str:
    s = text.lower()
    s = re.sub(r"['\",]", "", s)
    s = re.sub(r"[ _]+", "-", s)
    s = re.sub(r"[^a-z0-9-]", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def load_graph_slugs() -> set[str]:
    slugs: set[str] = set()
    for f in GRAPH_NODES_DIR.rglob("*.node.md"):
        if f.parts[-2] in ("_conflicts", "_unclassified"):
            continue
        slugs.add(f.name.removesuffix(".node.md"))
    return slugs


def page_name_to_slug(page_name: str) -> str:
    """Convert a wiki page title ("Pate (novice)") to our kebab slug
    ("pate-novice"). Mirrors the Stage 3 emitter convention."""
    return to_kebab(page_name)


def load_pass1_unresolved_counts() -> Counter:
    """Walk all mention-index files and tally how often each unresolved slug
    appears across the 344 chapters."""
    counts: Counter = Counter()
    for mf in (REPO_ROOT / "graph" / "index" / "chapters").rglob("*.mentions.json"):
        if mf.name == "_summary.json":
            continue
        try:
            data = json.loads(mf.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        for m in data.get("mentions", []):
            if m.get("resolved_via") == "unresolved":
                slug = m.get("slug")
                if slug:
                    counts[slug] += 1
    return counts


def load_backlinks() -> dict:
    if BACKLINK_PATH.exists():
        return json.loads(BACKLINK_PATH.read_text()).get("backlinks", {})
    return {}


def detect_case_collision_redirects() -> list[tuple[str, str]]:
    """Find wiki pages where the cached HTML is just a redirect to a same-
    spelled-but-different-case sibling. On macOS case-insensitive HFS+, the
    redirect overwrote (or precluded) the canonical content. Returns
    [(filename, redirect_target)].

    Heuristic: HTML starts with `<div class="redirectMsg">` AND the target
    differs only by case from the page title.
    """
    hits: list[tuple[str, str]] = []
    redirect_re = re.compile(
        r'<div class="redirectMsg"><p>Redirect to:.*?<a href="[^"]+" title="([^"]+)">',
        re.DOTALL,
    )
    for f in WIKI_RAW_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        html = data.get("html", "")
        if not html.startswith("<div class=\"redirectMsg\">"):
            continue
        m = redirect_re.search(html)
        if not m:
            continue
        target = m.group(1)
        page = data.get("page", "")
        # Case-collision: target equals page when both lowercased
        if page.lower() == target.lower() and page != target:
            hits.append((f.name, target))
    return hits


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--top", type=int, default=30,
                   help="Top N candidates to surface in each bucket (default 30)")
    args = p.parse_args()

    print("Loading graph slugs...", flush=True)
    graph_slugs = load_graph_slugs()
    print(f"  {len(graph_slugs):,} graph nodes")

    print("Loading wiki page-index...", flush=True)
    pages: list[dict] = []
    with PAGE_INDEX_PATH.open() as f:
        for line in f:
            pages.append(json.loads(line))
    print(f"  {len(pages):,} wiki pages indexed")

    print("Loading Pass 1 unresolved mention counts...", flush=True)
    pass1_unresolved = load_pass1_unresolved_counts()
    print(f"  {len(pass1_unresolved):,} distinct unresolved slugs across 344 chapters")

    print("Loading backlink counts...", flush=True)
    backlinks = load_backlinks()

    print("Detecting case-collision redirects...", flush=True)
    case_collisions = detect_case_collision_redirects()
    print(f"  {len(case_collisions):,} case-collision redirect pages")

    # Build the missing-nodes set: pages that exist with content but have no
    # graph node at their kebab slug.
    unpromoted: list[dict] = []
    for p_record in pages:
        # Skip pages flagged for skip (TV series, etc.)
        if p_record.get("entity_type_guess") == "skip":
            continue
        page = p_record["page"]
        slug = page_name_to_slug(page)
        if slug in graph_slugs:
            continue  # already promoted
        # Size signal: tiny pages (redirects, disambiguations) get lower priority
        byte_size = p_record.get("byte_size", 0)
        pass1_hits = pass1_unresolved.get(slug, 0)
        bl_info = backlinks.get(slug, {})
        in_count = bl_info.get("in_count", 0)
        unpromoted.append({
            "page": page,
            "slug": slug,
            "byte_size": byte_size,
            "entity_type_guess": p_record.get("entity_type_guess"),
            "categories": p_record.get("categories", []),
            "has_infobox": p_record.get("has_infobox", False),
            "pass1_mention_count": pass1_hits,
            "wiki_in_count": in_count,
        })

    print(f"  {len(unpromoted):,} unpromoted pages (excluding `skip` category)")
    print()

    # Bucket A: Pass 1 references them
    bucket_a = sorted(
        [u for u in unpromoted if u["pass1_mention_count"] > 0],
        key=lambda u: -u["pass1_mention_count"],
    )
    # Bucket B: highly backlinked but no Pass 1 mention
    bucket_b = sorted(
        [u for u in unpromoted if u["pass1_mention_count"] == 0 and u["wiki_in_count"] >= 10],
        key=lambda u: -u["wiki_in_count"],
    )
    # Bucket C: nothing
    bucket_c = sorted(
        [u for u in unpromoted if u["pass1_mention_count"] == 0 and u["wiki_in_count"] < 10],
        key=lambda u: -u["byte_size"],
    )

    # Write report
    report_dir = REPO_ROOT / "working" / "audits" / f"missing-nodes-{datetime.now().date()}" / "execution"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "missing-nodes.md"
    json_path = report_dir / "missing-nodes.json"

    def fmt_row(u: dict) -> str:
        cats = ", ".join(u["categories"][:3]) if u["categories"] else "-"
        return (
            f"| {u['page']} | `{u['slug']}` | "
            f"{u['pass1_mention_count']} | {u['wiki_in_count']} | "
            f"{u['byte_size']:,} | {u['entity_type_guess'] or '-'} | {cats} |"
        )

    lines: list[str] = []
    lines.append(f"# Missing graph-node candidates — {datetime.now().date()}")
    lines.append("")
    lines.append("> Audit of wiki pages cached in `sources/wiki/_raw/` that have no graph node at their canonical kebab slug.")
    lines.append("> Three buckets, sorted by signal strength (Pass 1 chapter mentions > wiki backlinks > nothing).")
    lines.append("")
    lines.append(f"- **Total wiki pages indexed**: {len(pages):,}")
    lines.append(f"- **Total graph nodes**: {len(graph_slugs):,}")
    lines.append(f"- **Unpromoted pages (excluding `skip` category)**: {len(unpromoted):,}")
    lines.append(f"- **Pass-1-referenced unpromoted (bucket A)**: {len(bucket_a):,}")
    lines.append(f"- **Highly-backlinked unpromoted (bucket B)**: {len(bucket_b):,}")
    lines.append(f"- **Tail unpromoted (bucket C)**: {len(bucket_c):,}")
    lines.append("")

    lines.append("## Case-collision redirect crawl bugs")
    lines.append("")
    lines.append(
        f"The case-insensitive macOS HFS+ filesystem collapsed `<Name>` and `<name>` to one disk entry "
        f"during the original wiki crawl. **{len(case_collisions)} cached pages** are redirect-only "
        f"and the canonical-content variant never made it to disk. Re-crawling these specific pages "
        f"would require a narrow exception fetch (per CLAUDE.md)."
    )
    lines.append("")
    if case_collisions:
        lines.append("| Filename | Redirect target |")
        lines.append("|---|---|")
        for fname, target in case_collisions[:50]:
            lines.append(f"| `{fname}` | {target} |")
        if len(case_collisions) > 50:
            lines.append(f"| ... | _{len(case_collisions) - 50} more_ |")
    lines.append("")

    lines.append(f"## Bucket A — Pass 1 references them ({len(bucket_a):,} pages)")
    lines.append("")
    lines.append("These wiki pages exist but Pass 1 mentions them across the chapter corpus with NO graph node to resolve to. **Highest backfill priority.**")
    lines.append("")
    lines.append("| Page | Slug | Pass 1 mentions | Wiki in-edges | Bytes | Type guess | Top categories |")
    lines.append("|---|---|---|---|---|---|---|")
    for u in bucket_a[:args.top]:
        lines.append(fmt_row(u))
    if len(bucket_a) > args.top:
        lines.append(f"| _{len(bucket_a) - args.top} more in JSON sidecar_ | | | | | | |")
    lines.append("")

    lines.append(f"## Bucket B — Heavily wiki-backlinked but Pass 1 silent ({len(bucket_b):,} pages)")
    lines.append("")
    lines.append("Other wiki pages reference these (≥10 backlinks) but no chapter mentions them. Often historical figures from D&E or TWOIAF — relevant to graph traversal but not to the main narrative arc.")
    lines.append("")
    lines.append("| Page | Slug | Pass 1 mentions | Wiki in-edges | Bytes | Type guess | Top categories |")
    lines.append("|---|---|---|---|---|---|---|")
    for u in bucket_b[:args.top]:
        lines.append(fmt_row(u))
    if len(bucket_b) > args.top:
        lines.append(f"| _{len(bucket_b) - args.top} more in JSON sidecar_ | | | | | | |")
    lines.append("")

    lines.append(f"## Bucket C — Tail ({len(bucket_c):,} pages)")
    lines.append("")
    lines.append("Low signal — no Pass 1 mention, <10 wiki backlinks. Mostly minor characters, list/disambiguation pages, and very peripheral entries. Probably fine to leave unpromoted.")
    lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")

    json_path.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "totals": {
            "wiki_pages_indexed": len(pages),
            "graph_nodes": len(graph_slugs),
            "unpromoted": len(unpromoted),
            "bucket_a": len(bucket_a),
            "bucket_b": len(bucket_b),
            "bucket_c": len(bucket_c),
            "case_collisions": len(case_collisions),
        },
        "case_collisions": case_collisions,
        "bucket_a": bucket_a,
        "bucket_b": bucket_b,
        "bucket_c_top_100": bucket_c[:100],
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Report:  {report_path.relative_to(REPO_ROOT)}")
    print(f"JSON:    {json_path.relative_to(REPO_ROOT)}")
    print()
    print(f"  Bucket A (Pass 1 referenced):       {len(bucket_a):,}")
    print(f"  Bucket B (heavily wiki-backlinked): {len(bucket_b):,}")
    print(f"  Bucket C (tail):                    {len(bucket_c):,}")
    print(f"  Case-collision redirects:           {len(case_collisions):,}")
    print()
    print("Top 10 Bucket A candidates (Pass 1 mentions):")
    for u in bucket_a[:10]:
        print(f"  {u['slug']:<40}  pass1={u['pass1_mention_count']:>3}  wiki_in={u['wiki_in_count']:>3}")


if __name__ == "__main__":
    main()
