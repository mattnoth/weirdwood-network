"""corpus_search.py — grep-class full-text search over sources/chapters/
(query-layer Track, step 5e; design.md D-C "chapter full-text search becomes
a CLI-first capability").

CLI-ONLY. No bundle exposure, no chat tool — the design doc is explicit:
"NO bundle/chat exposure, read_passage is designed-but-gated". This module
never imports/touches anything under `web/data/` and `build_chat_bundle.py`
never calls it. `sources/` is read here READ-ONLY (the standing rule — see
CLAUDE.md's "sources/ is read-only" gate).

Unlike `search()` (BM25 over the curated quote/identity layer, a build-time
index), this is a live, uncached scan over the 371 `sources/chapters/**/*.md`
files at request time — cheap enough in a local/CLI context (grep-class
string matching over ~a few MB of markdown), never meant to run inside the
50ms-CPU-budget edge function `search`/`list` serve.

Match modes:
  - whole-phrase (default): the literal phrase, case-insensitive, matched as
    a contiguous substring on each line (after collapsing internal
    whitespace in both the query and the line, so a phrase split across a
    line-wrap in the source still fails to match — a KNOWN limitation of a
    per-line scan; the corpus files are prose paragraphs, not hard-wrapped,
    so this is rare in practice).
  - all-tokens: every whitespace-token of the query (case-insensitive, exact
    word match after stripping punctuation) must appear somewhere on the
    same line, in any order — a looser recall-oriented mode for when the
    exact phrase doesn't appear verbatim but the topic does.

Cites: `sources/chapters/<book>/<file>.md:<line>` (1-indexed line number
within the file — the same `chapter:line` cite format node quotes already
carry, produced by the SAME convention `_CITE_RE` in load.py matches against).

No LLM in the loop. Ever.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .load import REPO_ROOT

CHAPTERS_DIR = REPO_ROOT / "sources" / "chapters"

DEFAULT_LIMIT = 20
_WORD_RE = re.compile(r"\w+")


def _iter_chapter_files(chapters_dir: Path, book: str | None) -> list[Path]:
    """Sorted list of chapter markdown files, optionally scoped to one book
    (a top-level subdirectory name, e.g. "agot"). Recurses (the D&E books
    nest a `parts/` subdirectory) but excludes nothing else — every chapter
    file is fair game for a corpus scan."""
    if not chapters_dir.exists():
        return []
    if book:
        book_dir = chapters_dir / book
        if not book_dir.is_dir():
            return []
        return sorted(book_dir.rglob("*.md"))
    return sorted(chapters_dir.rglob("*.md"))


def _rel_cite(path: Path, lineno: int) -> str:
    try:
        rel = path.relative_to(REPO_ROOT)
    except ValueError:
        rel = path
    return f"{rel.as_posix()}:{lineno}"


def corpus_search(
    query: str,
    *,
    book: str | None = None,
    mode: str = "phrase",
    limit: int = DEFAULT_LIMIT,
    chapters_dir: Path = CHAPTERS_DIR,
) -> dict[str, Any]:
    """Scan chapter files for `query`, line by line.

    `mode`: "phrase" (default, whole-phrase substring match, case-insensitive,
    whitespace-collapsed) or "tokens" (all whitespace/punct-stripped tokens of
    the query must appear on the line, any order).

    Returns `{query, mode, book, total, limit, matches: [{cite, book, text}]}`
    — `total` counts every matching line found (before the `limit` cap);
    `matches` holds up to `limit`, in file-then-line order (deterministic:
    the same sorted file walk `search`'s underlying index build uses).

    Empty/whitespace query returns `total: 0, matches: []` rather than
    matching every line (an empty phrase is a trivially-true substring of
    everything, which would be useless output, not a real search result).
    """
    q = query.strip()
    if not q:
        return {"query": query, "mode": mode, "book": book, "total": 0, "limit": limit, "matches": []}

    if mode == "tokens":
        want_tokens = {t.lower() for t in _WORD_RE.findall(q)}
        want_tokens = {t for t in want_tokens if t}
        if not want_tokens:
            return {"query": query, "mode": mode, "book": book, "total": 0, "limit": limit, "matches": []}

        def line_matches(line_lower: str) -> bool:
            line_tokens = set(_WORD_RE.findall(line_lower))
            return want_tokens.issubset(line_tokens)
    else:
        mode = "phrase"
        needle = re.sub(r"\s+", " ", q).strip().lower()

        def line_matches(line_lower: str) -> bool:
            collapsed = re.sub(r"\s+", " ", line_lower).strip()
            return needle in collapsed

    matches: list[dict[str, Any]] = []
    total = 0
    for path in _iter_chapter_files(chapters_dir, book):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for lineno, line in enumerate(lines, 1):
            if not line.strip():
                continue
            if line_matches(line.lower()):
                total += 1
                if len(matches) < limit:
                    try:
                        book_name = path.relative_to(chapters_dir).parts[0]
                    except (ValueError, IndexError):
                        book_name = book or ""
                    matches.append({
                        "cite": _rel_cite(path, lineno),
                        "book": book_name,
                        "text": line.strip(),
                    })

    return {
        "query": query,
        "mode": mode,
        "book": book,
        "total": total,
        "limit": limit,
        "matches": matches,
    }
