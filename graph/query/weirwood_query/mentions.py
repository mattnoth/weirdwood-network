"""mentions.py — `mentions` op (query-layer Track, step 8b; design.md G13).

Reads the LIVE `graph/index/chapters/` tree — the SAME data
`scripts/build-mention-index.py` writes today, which is real but
**partially stale** (its entity resolution predates the current hardened
alias table; harvest-minted nodes can show 0 appearances even when the
Pass-1 corpus does mention them under a resolvable phrase — see
`build/build_mention_index_preview.py` and
`working/query-layer/mention-index-repair-report.md` for the measured
gap and a preview of the repair). This module does **not** apply that
repair — it is a read-only reader of whatever is currently live, exactly
like `search.py`/`themes.py` read whatever their own builders last wrote.

Because the live data can be stale, `mentions()` proactively checks whether
a requested slug's live count differs from the PREVIEW tree's count (when
the preview happens to exist on disk) and, if so, adds a `staleness_note`
to the returned dict — so a caller (or the CLI's printed output) sees the
warning inline rather than silently trusting a possibly-wrong 0.

No LLM in the loop. Ever.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .load import REPO_ROOT

LIVE_INDEX_DIR = REPO_ROOT / "graph" / "index" / "chapters"
PREVIEW_INDEX_DIR = REPO_ROOT / "working" / "query-layer" / "mention-index-preview" / "chapters"

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]


def _scan_slug(index_dir: Path, slug: str) -> list[dict[str, Any]]:
    """Return one record per chapter where `slug` appears in that chapter's
    `.mentions.json` under `index_dir` (live or preview tree — same shape).
    Each record: {chapter_id, book, pov_character, mention_count, sections,
    resolved_via}."""
    if not index_dir.exists():
        return []
    records: list[dict[str, Any]] = []
    for mfile in sorted(index_dir.rglob("*.mentions.json")):
        if mfile.name == "_summary.json":
            continue
        try:
            data = json.loads(mfile.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        hits = [m for m in data.get("mentions", []) if m.get("slug") == slug]
        if not hits:
            continue
        sections = sorted({m.get("section") for m in hits if m.get("section")})
        resolved_via = sorted({m.get("resolved_via") for m in hits if m.get("resolved_via")})
        records.append({
            "chapter_id": data.get("chapter_id"),
            "book": data.get("book"),
            "pov_character": data.get("pov_character"),
            "mention_count": len(hits),
            "sections": sections,
            "resolved_via": resolved_via,
        })
    return records


def mentions(slug: str, *, live_dir: Path = LIVE_INDEX_DIR, preview_dir: Path = PREVIEW_INDEX_DIR) -> dict[str, Any]:
    """Return `{slug, chapter_count, appearances_total, chapters, source,
    staleness_note?}` for every chapter mentioning `slug` in the LIVE
    `graph/index/chapters/` tree.

    `staleness_note` is present only when a preview build exists on disk
    (`working/query-layer/mention-index-preview/chapters/`, built by
    `build/build_mention_index_preview.py`) AND its count for this slug
    differs from the live count — the header then names both numbers and
    points at the repair report, rather than silently returning a stale 0.

    An index that doesn't exist at all (fresh checkout, `graph/index/`
    never built) returns `chapter_count: 0, chapters: [], source: "missing"`
    — not an exception.
    """
    if not live_dir.exists():
        return {
            "slug": slug, "chapter_count": 0, "appearances_total": 0,
            "chapters": [], "source": "missing",
        }

    live_records = _scan_slug(live_dir, slug)
    appearances_total = sum(r["mention_count"] for r in live_records)

    result: dict[str, Any] = {
        "slug": slug,
        "chapter_count": len(live_records),
        "appearances_total": appearances_total,
        "chapters": live_records,
        "source": "graph/index/chapters (live — may be stale, see G13)",
    }

    if preview_dir.exists():
        preview_records = _scan_slug(preview_dir, slug)
        preview_total = sum(r["mention_count"] for r in preview_records)
        if preview_total != appearances_total:
            result["staleness_note"] = (
                f"STALE: live shows {appearances_total} appearance(s) for '{slug}', "
                f"but the mention-index preview (working/query-layer/mention-index-preview/, "
                f"the hardened-alias-table repair) shows {preview_total}. "
                "See working/query-layer/mention-index-repair-report.md for the full repair "
                "and the apply command (requires Matt's go — graph/index/ is mutation-gated)."
            )

    return result
