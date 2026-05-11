#!/usr/bin/env python3
"""Audit prose coverage across graph nodes.

For each graph node (excluding _conflicts/ and _unclassified/) emit one JSON
row to `working/audits/wiki-prose-coverage-2026-05-12/execution/coverage.jsonl`
with these fields:

  slug                       — node slug (from frontmatter or filename)
  type                       — entity type
  pass_origin                — pass2-wiki | pass2-wiki-deterministic | other
  is_stub                    — body matches stub-only regex
  has_prose_file             — any matching `<slug>.prose.md` in pass2-buckets
  prose_byte_size            — bytes (max across all matching prose files)
  prose_bucket               — which bucket holds the largest prose file
  has_wiki_cache             — sources/wiki/_raw/<Page>.json exists
  wiki_cache_redirect_only   — cached page is only a redirect (case-collision bug)
  node_path                  — relative path

Also emits a Markdown summary at `summary.md` with counts:
  - total nodes (excluding _conflicts/ and _unclassified/)
  - by pass_origin
  - stub-only (per pass_origin)
  - stub-only nodes that could promote now (have non-empty prose ready)
  - stub-only nodes that need fresh extraction
  - stub-only nodes that hit case-collision dead-end

Read-only. Does not modify graph or buckets.

Usage:
  python3 scripts/audit-prose-coverage.py
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
NODES_DIR = PROJECT_ROOT / "graph" / "nodes"
BUCKETS_DIR = PROJECT_ROOT / "working" / "wiki" / "pass2-buckets"
WIKI_RAW = PROJECT_ROOT / "sources" / "wiki" / "_raw"
OUT_DIR = PROJECT_ROOT / "working" / "audits" / "wiki-prose-coverage-2026-05-12" / "execution"

STUB_RE = re.compile(
    r"is an? [a-z]+(\.[a-z]+)?(\s*\([^)]+\))? from the AWOIAF wiki\.",
    re.IGNORECASE,
)

# Detect a JSON cache whose only meaningful content is a "redirects to X" stub.
# The case-collision bug left these pages with only redirect HTML — they have
# no extractable prose. Matched by a tiny html field with a redirect link only.
REDIRECT_ONLY_RE = re.compile(
    r'^\s*<p[^>]*>\s*Redirect to[:]?\s*<ul[^>]*>\s*<li[^>]*>\s*<a[^>]*>[^<]+</a>\s*</li>\s*</ul>\s*</p>\s*$',
    re.IGNORECASE | re.DOTALL,
)


def parse_frontmatter(text: str) -> dict:
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm = parts[1]
    out = {}
    for line in fm.splitlines():
        m = re.match(r"^([a-zA-Z_]+):\s*(.+?)\s*$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def body_after_frontmatter(text: str) -> str:
    parts = text.split("---", 2)
    return parts[2] if len(parts) >= 3 else text


def build_prose_index() -> dict[str, list[tuple[str, int]]]:
    """slug → list of (bucket_id, prose_size). All non-empty prose files."""
    idx: dict[str, list[tuple[str, int]]] = {}
    for p in BUCKETS_DIR.glob("*/prose/*.prose.md"):
        slug = p.stem.removesuffix(".prose")
        size = p.stat().st_size
        if size == 0:
            continue
        bucket = p.parent.parent.name
        idx.setdefault(slug, []).append((bucket, size))
    return idx


def name_to_wiki_filename(name: str) -> str:
    return name.replace(" ", "_") + ".json"


def is_redirect_only_cache(path: Path) -> bool:
    """Detect a redirect-only cached wiki page (case-collision losers)."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    html = raw.get("html", "")
    # Heuristic: very small HTML payload (< 800 chars) plus a redirect div pattern.
    if len(html) > 1200:
        return False
    if "redirectMsg" in html or '<div class="redirectMsg"' in html:
        return True
    if "Redirected from" in html and len(html) < 800:
        return True
    return False


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_jsonl = OUT_DIR / "coverage.jsonl"
    out_summary = OUT_DIR / "summary.md"

    print("Building prose index...", file=sys.stderr)
    prose_index = build_prose_index()
    print(f"  {sum(len(v) for v in prose_index.values()):,} prose files indexed across {len(prose_index):,} slugs", file=sys.stderr)

    rows = []
    seen_redirect: dict[Path, bool] = {}

    counts = {
        "total": 0,
        "by_pass_origin": {},
        "stub_total": 0,
        "stub_with_prose": 0,
        "stub_without_prose": 0,
        "stub_no_wiki_cache": 0,
        "stub_redirect_only_cache": 0,
        "stub_by_pass_origin": {},
    }

    for nf in NODES_DIR.rglob("*.node.md"):
        if "_conflicts" in nf.parts or "_unclassified" in nf.parts:
            continue
        try:
            text = nf.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        fm = parse_frontmatter(text)
        body = body_after_frontmatter(text)
        slug = fm.get("slug") or nf.stem.removesuffix(".node")
        name = fm.get("name") or slug
        node_type = fm.get("type", "")
        pass_origin = fm.get("pass_origin", "other")
        prose_headers = ("## Origins", "## Narrative Arc", "## Appearances", "## Culture", "## Organization", "## Quotes", "## Aftermath")
        has_prose_section = any(h in body for h in prose_headers)
        is_stub = bool(STUB_RE.search(body)) and not has_prose_section

        # Prose lookup
        proseinfo = prose_index.get(slug, [])
        if proseinfo:
            best = max(proseinfo, key=lambda t: t[1])
            prose_bucket, prose_byte_size = best
            has_prose_file = True
        else:
            prose_bucket = None
            prose_byte_size = 0
            has_prose_file = False

        # Wiki cache lookup
        wiki_path = WIKI_RAW / name_to_wiki_filename(name)
        has_wiki_cache = wiki_path.exists()
        wiki_redirect_only = False
        if has_wiki_cache:
            if wiki_path in seen_redirect:
                wiki_redirect_only = seen_redirect[wiki_path]
            else:
                wiki_redirect_only = is_redirect_only_cache(wiki_path)
                seen_redirect[wiki_path] = wiki_redirect_only

        row = {
            "slug": slug,
            "type": node_type,
            "pass_origin": pass_origin,
            "is_stub": is_stub,
            "has_prose_file": has_prose_file,
            "prose_byte_size": prose_byte_size,
            "prose_bucket": prose_bucket,
            "has_wiki_cache": has_wiki_cache,
            "wiki_cache_redirect_only": wiki_redirect_only,
            "node_path": str(nf.relative_to(PROJECT_ROOT)),
        }
        rows.append(row)

        # Tally
        counts["total"] += 1
        counts["by_pass_origin"][pass_origin] = counts["by_pass_origin"].get(pass_origin, 0) + 1
        if is_stub:
            counts["stub_total"] += 1
            counts["stub_by_pass_origin"][pass_origin] = counts["stub_by_pass_origin"].get(pass_origin, 0) + 1
            if has_prose_file:
                counts["stub_with_prose"] += 1
            else:
                counts["stub_without_prose"] += 1
                if not has_wiki_cache:
                    counts["stub_no_wiki_cache"] += 1
                elif wiki_redirect_only:
                    counts["stub_redirect_only_cache"] += 1

    # Write jsonl
    with open(out_jsonl, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # Summary
    lines = []
    lines.append("# Wiki prose coverage audit — 2026-05-12")
    lines.append("")
    lines.append(f"Total graph nodes (excluding _conflicts/_unclassified): **{counts['total']:,}**")
    lines.append("")
    lines.append("## By pass_origin")
    for po, n in sorted(counts["by_pass_origin"].items(), key=lambda kv: -kv[1]):
        lines.append(f"- `{po}`: {n:,}")
    lines.append("")
    lines.append("## Stub-only nodes")
    lines.append(f"- Total stub-only: **{counts['stub_total']:,}**")
    for po, n in sorted(counts["stub_by_pass_origin"].items(), key=lambda kv: -kv[1]):
        lines.append(f"  - `{po}`: {n:,}")
    lines.append("")
    lines.append("## Promotion outlook")
    lines.append(f"- Stub + has non-empty prose file (READY TO PROMOTE): **{counts['stub_with_prose']:,}**")
    lines.append(f"- Stub + no prose file (needs fresh extraction or genuinely empty): **{counts['stub_without_prose']:,}**")
    lines.append(f"  - of which no wiki cache at all: {counts['stub_no_wiki_cache']:,}")
    lines.append(f"  - of which cache is redirect-only (case-collision bug): {counts['stub_redirect_only_cache']:,}")
    lines.append("")
    lines.append(f"Detail per-node JSONL: `{out_jsonl.relative_to(PROJECT_ROOT)}`")
    out_summary.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print()
    print("=" * 60)
    for line in lines:
        print(line)
    print("=" * 60)
    print(f"\nWrote: {out_jsonl}")
    print(f"Wrote: {out_summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
