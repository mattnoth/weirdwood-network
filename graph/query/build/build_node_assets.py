#!/usr/bin/env python3
"""build_node_assets.py — per-node static assets for the chat-UI dossier
(query-layer Track, step 6c; design.md D-F / G9).

The bundle (`build_chat_bundle.py`'s `nodes.json`) deliberately drops `##
Narrative Arc` prose (measured step 0: inlining it would grow `nodes.json`
+197.7% — nearly triple the bundle, `working/query-layer/measurements.md`).
D-F's decision: rather than inline, emit ONE static JSON asset per node that
HAS a Narrative Arc section, fetched on demand over HTTP by the edge function
(`node.ts`) and by local dev's static file server — network I/O falls outside
the Edge Function's 50ms CPU budget, unlike an inlined bundle lookup, so this
trick is what makes the extra content affordable at all.

Output: `web/public/node/<slug>.json`, one file per qualifying node:
    {"slug": ..., "name": ..., "narrative_arc": "<markdown>", "cites": [...]}
`cites` is the list of inline `sources/chapters/.../*.md:LINE` book-cite
overlay references found in the section text (the harvest-consume
book-citation convention — see feedback_book_citation_overlay_value), in
first-seen order, deduped. Omitted (key absent) when the section carries none
— most Narrative Arc prose is wiki-derived and has no book cite overlay
(87 of 4,401 as of this build).

`web/public/` is a TRACKED directory (app.js/index.html/css/fonts/portraits/
sigils all live there and are committed) but this output is DERIVED, build-
regenerated data, like `web/data/`'s bundle quartet — `web/public/node/` is
therefore added to `.gitignore` (see that edit's own note) rather than
committed.

Usage:
    python3 graph/query/build/build_node_assets.py
    python3 graph/query/build/build_node_assets.py --out-dir DIR   # verification runs
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_THIS_FILE = Path(__file__).resolve()
# <repo>/graph/query/build/build_node_assets.py -> parents[0]=build,
# [1]=query, [2]=graph, [3]=<repo>
REPO_ROOT = _THIS_FILE.parents[3]

sys.path.insert(0, str(REPO_ROOT / "graph" / "query"))

from weirwood_query.load import NODES_DIR, parse_frontmatter, split_sections  # noqa: E402

OUT_DIR = REPO_ROOT / "web" / "public" / "node"

_CITE_RE = re.compile(r"`(sources/chapters/[^`]+\.md:\d+)`")


def extract_cites(narrative_arc: str) -> list[str]:
    """Every distinct `sources/chapters/.../*.md:LINE` cite embedded in the
    section text, in first-seen order. Empty list when none (the common
    case — most Narrative Arc prose is wiki-derived with no book overlay)."""
    seen: list[str] = []
    seen_set: set[str] = set()
    for m in _CITE_RE.finditer(narrative_arc):
        cite = m.group(1)
        if cite not in seen_set:
            seen_set.add(cite)
            seen.append(cite)
    return seen


def build_node_assets(nodes_dir: Path = NODES_DIR) -> list[dict[str, Any]]:
    """Return one record per node file (under nodes_dir, excluding
    `_conflicts/`) that carries a `## Narrative Arc` section. `chapters/`
    (the per-chapter summary subsystem, a different thing from front-end
    entity nodes — see measurements.md's own scoping note) IS included here
    intentionally: a chapter dossier page benefits from its own arc prose the
    same way an entity node's does, and the size budget already accounts for
    it being small relative to the entity-node total."""
    records: list[dict[str, Any]] = []
    for path in sorted(nodes_dir.rglob("*.node.md")):
        if "_conflicts" in path.parts:
            continue
        raw = path.read_text(encoding="utf-8")
        fields, body = parse_frontmatter(raw)
        if not fields and not raw.startswith("---"):
            continue
        fallback = path.name.replace(".node.md", "")
        slug = fields.get("slug") or fallback
        name = fields.get("name") or slug

        sections = split_sections(body)
        narrative_arc = sections.get("narrative arc", "") or sections.get("narrative_arc", "")
        if not narrative_arc.strip():
            continue

        rec: dict[str, Any] = {
            "slug": str(slug),
            "name": str(name),
            "narrative_arc": narrative_arc.strip(),
        }
        cites = extract_cites(narrative_arc)
        if cites:
            rec["cites"] = cites
        records.append(rec)
    return records


def write_asset(record: dict[str, Any], out_dir: Path) -> int:
    path = out_dir / f"{record['slug']}.json"
    text = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
    path.write_text(text, encoding="utf-8")
    return len(text.encode("utf-8"))


def human(nbytes: float) -> str:
    for unit in ("B", "KB", "MB"):
        if nbytes < 1024 or unit == "MB":
            return f"{nbytes:.1f}{unit}" if unit != "B" else f"{nbytes:.0f}B"
        nbytes /= 1024
    return f"{nbytes:.1f}MB"


def main() -> int:
    ap = argparse.ArgumentParser(description="Build per-node static Narrative Arc assets.")
    ap.add_argument(
        "--out-dir", default=None,
        help="Override output directory (default: web/public/node/). Used by verification "
        "runs that must not touch the live tracked-adjacent output.",
    )
    ap.add_argument(
        "--clean", action="store_true",
        help="Remove existing *.json files in the output dir before writing (drops stale "
        "assets for nodes that lost their Narrative Arc section since the last build).",
    )
    args = ap.parse_args()

    out_dir = Path(args.out_dir) if args.out_dir else OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.clean:
        for existing in out_dir.glob("*.json"):
            existing.unlink()

    print("Building per-node Narrative Arc assets ...")
    records = build_node_assets()

    total_bytes = 0
    largest: tuple[str, int] = ("", 0)
    with_cites = 0
    for rec in records:
        size = write_asset(rec, out_dir)
        total_bytes += size
        if size > largest[1]:
            largest = (rec["slug"], size)
        if "cites" in rec:
            with_cites += 1

    print(f"  wrote {len(records)} asset(s) -> {out_dir}/")
    print(f"  with book-cite overlay: {with_cites}")
    print(f"  total size: {human(total_bytes)} ({total_bytes} bytes)")
    print(f"  largest asset: {largest[0]}.json ({human(largest[1])})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
