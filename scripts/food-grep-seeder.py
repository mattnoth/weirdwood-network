#!/usr/bin/env python3
"""food-grep-seeder.py — corpus-tool keyword sweep for food/drink mentions
(query-layer Track, step 8c; design.md D-E, "the Matt-steered Python
food-keyword grep... as a POINTER generator feeding harvest, not an LLM
sweep").

This is a CORPUS tool (grep-class, deterministic, no query engine involved),
not a `weirwood_query` op — it lives in `scripts/` alongside the other
build/ingest/harvest tooling, not under `graph/query/`.

What it does: sweeps every `sources/chapters/**/*.md` chapter file for two
keyword classes —
  1. **Named dishes** — every `object.food` node's `name` + `aliases` (from
     `graph/nodes/foods/*.node.md`), e.g. "lemon cake", "salt beef".
  2. **Generic food/eating terms** — a small fixed list (eat, feast, supper,
     dine, hungry, starv*, bread, meat, wine, ale, stew, pie, roast, ...)
     that catches food-adjacent prose even when no named dish node exists yet.

Matches are WHOLE-WORD/WHOLE-PHRASE (word-boundary regex, case-insensitive —
same discipline as `graph/query/build/build_theme_index.py`'s keyword
matcher, avoiding the "harp" inside "Harpy's" class of false positive).

**Dedup against existing graph content**: a hit is DROPPED if its exact line
text (stripped) already appears verbatim inside some food node's `## Quotes`
section (i.e. the passage is already captured on the graph) — this sweep is
for finding NEW candidate material, not re-surfacing what's already attached.

Output: `working/query-layer/food-grep-candidates.md` — one row per surviving
hit, `chapter:line / kind=food / note` format (matches the harvest-queue
row shape's cite/kind/note fields, but this is NOT `working/harvest-queue.md`
itself — see the header this script writes: rows here are a CANDIDATE POOL,
they graduate to the harvest queue only after a human/agent review pass
confirms each is load-bearing, per the project's "point, don't extract"
harvest discipline).

POINT, don't extract: this script never mints nodes/edges/quotes. It only
locates candidate lines.

Usage:
    python3 scripts/food-grep-seeder.py
    python3 scripts/food-grep-seeder.py --out PATH

No LLM in the loop. Ever.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "graph" / "query"))

from weirwood_query.load import NODES_DIR, parse_frontmatter, split_sections, parse_quotes  # noqa: E402

CHAPTERS_DIR = REPO_ROOT / "sources" / "chapters"
OUT_PATH = REPO_ROOT / "working" / "query-layer" / "food-grep-candidates.md"

BOOK_ORDER = {"agot": 0, "acok": 1, "asos": 2, "affc": 3, "adwd": 4, "tmk": 5, "tss": 6, "thk": 7}
MAIN_BOOKS = {"agot", "acok", "asos", "affc", "adwd"}

# Generic food/eating terms (design.md 8c's list, as given): eat/feast/supper/
# dine/hungry/starv*/bread/meat/wine/ale/stew/pie/roast + a few obvious
# companions kept minimal (breakfast/dinner/hungry family) to avoid silently
# growing the list past what was specified.
GENERIC_TERMS = [
    "eat", "eats", "eating", "ate", "eaten",
    "feast", "feasts", "feasting", "feasted",
    "supper", "suppers",
    "dine", "dines", "dining", "dined",
    "hungry", "hunger",
    "starving", "starved", "starve",  # covers the "starv*" wildcard intent
    "bread",
    "meat",
    "wine",
    "ale",
    "stew", "stews",
    "pie", "pies",
    "roast", "roasted",
]


# ---------------------------------------------------------------------------
# Keyword matching — whole-word/whole-phrase, case-insensitive (same
# discipline as build_theme_index.py's _keyword_matches).
# ---------------------------------------------------------------------------

_PATTERN_CACHE: dict[str, re.Pattern[str]] = {}


def _pattern(term: str) -> re.Pattern[str]:
    pat = _PATTERN_CACHE.get(term)
    if pat is None:
        pat = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
        _PATTERN_CACHE[term] = pat
    return pat


def _find_terms(line: str, terms: list[str]) -> list[str]:
    return [t for t in terms if _pattern(t).search(line)]


# ---------------------------------------------------------------------------
# Food-node keyword harvest (names + aliases)
# ---------------------------------------------------------------------------

def collect_food_keywords() -> dict[str, str]:
    """Return {keyword_lowercase: slug} for every object.food node's name +
    aliases. Longer keywords win on collision (rare; e.g. two nodes sharing
    a generic alias) by being checked first in match order — callers should
    sort by len(keyword) descending before use (see build_candidate_lists)."""
    foods_dir = NODES_DIR / "foods"
    keyword_to_slug: dict[str, str] = {}
    if not foods_dir.is_dir():
        return keyword_to_slug
    for node_file in sorted(foods_dir.glob("*.node.md")):
        raw = node_file.read_text(encoding="utf-8")
        fields, _body = parse_frontmatter(raw)
        slug = fields.get("slug") or node_file.name.removesuffix(".node.md")
        name = str(fields.get("name") or slug)
        aliases_raw = fields.get("aliases", [])
        if not isinstance(aliases_raw, list):
            aliases_raw = [aliases_raw] if aliases_raw else []
        for kw in [name, *[str(a) for a in aliases_raw]]:
            kw = kw.strip()
            if len(kw) < 3:
                continue  # skip too-short aliases (noise-prone, e.g. a 2-char stub)
            keyword_to_slug.setdefault(kw.lower(), slug)
    return keyword_to_slug


# ---------------------------------------------------------------------------
# Existing-quote dedup set — every quote already attached to a food node
# ---------------------------------------------------------------------------

def collect_existing_food_quotes() -> set[str]:
    """Return a set of normalized (lowercased, whitespace-collapsed) quote
    texts already present in some food node's `## Quotes` section — a hit
    whose line text matches one of these is dropped (already captured)."""
    foods_dir = NODES_DIR / "foods"
    seen: set[str] = set()
    if not foods_dir.is_dir():
        return seen
    for node_file in sorted(foods_dir.glob("*.node.md")):
        raw = node_file.read_text(encoding="utf-8")
        _fields, body = parse_frontmatter(raw)
        sections = split_sections(body)
        for q in parse_quotes(sections.get("quotes", "")):
            text = (q.get("text") or "").strip()
            if text:
                seen.add(_normalize_for_dedup(text))
    return seen


def _normalize_for_dedup(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _already_on_graph(line: str, existing_quotes: set[str]) -> bool:
    """A chapter line counts as "already on graph" if a curated food-node
    quote is CONTAINED in it (substring, not just exact-equal) — a node's
    `## Quotes` entry is typically one sentence lifted from a longer
    paragraph line in the source chapter file (chapter text is NOT
    line-wrapped at sentence boundaries), so exact-line equality almost
    never fires; substring containment is the check that actually matches
    the real on-disk shapes (verified this session against `acorn-paste`'s
    quote vs. acok-arya-05.md:37's full paragraph line)."""
    norm_line = _normalize_for_dedup(line)
    if not norm_line:
        return False
    return any(q and q in norm_line for q in existing_quotes)


# ---------------------------------------------------------------------------
# Chapter sweep
# ---------------------------------------------------------------------------

def chapter_cite(path: Path) -> tuple[str, str]:
    """Return (book, rel_path_str) for a chapter file, e.g.
    ('agot', 'sources/chapters/agot/agot-arya-01.md')."""
    rel = path.relative_to(REPO_ROOT)
    parts = rel.parts
    book = parts[2] if len(parts) > 2 else "?"
    return book, str(rel)


def sweep(
    food_keywords: dict[str, str],
    existing_quotes: set[str],
    chapters_dir: Path = CHAPTERS_DIR,
) -> dict[str, Any]:
    """Walk every chapter file, find lines matching a food keyword or a
    generic term, dedup against existing food-node quotes. Returns a report
    dict with `rows` (surviving candidates) + stats."""
    # Sort keywords longest-first so a substring keyword (e.g. "ham" inside
    # a longer phrase check) never masks a more specific one being reported —
    # in practice each line reports ALL matching keywords, this ordering just
    # keeps iteration deterministic.
    sorted_food_kw = sorted(food_keywords.keys(), key=len, reverse=True)

    rows: list[dict[str, Any]] = []
    total_hits = 0
    dedup_dropped = 0
    per_book: Counter[str] = Counter()
    files_scanned = 0

    if not chapters_dir.exists():
        return {"rows": [], "total_hits": 0, "dedup_dropped": 0, "per_book": {}, "files_scanned": 0}

    chapter_files = sorted(chapters_dir.rglob("*.md"))
    for cf in chapter_files:
        files_scanned += 1
        book, cite_path = chapter_cite(cf)
        try:
            lines = cf.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue

        for lineno, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue

            food_hits = _find_terms(stripped, sorted_food_kw)
            generic_hits = _find_terms(stripped, GENERIC_TERMS) if not food_hits else []
            matched = food_hits or generic_hits
            if not matched:
                continue

            total_hits += 1
            if _already_on_graph(stripped, existing_quotes):
                dedup_dropped += 1
                continue

            match_kind = "named_dish" if food_hits else "generic_term"
            matched_slugs = sorted({food_keywords[k] for k in food_hits}) if food_hits else []
            rows.append({
                "book": book,
                "cite": f"{cite_path}:{lineno}",
                "matched_terms": food_hits or generic_hits,
                "match_kind": match_kind,
                "matched_slugs": matched_slugs,
                "text": stripped,
            })
            per_book[book] += 1

    return {
        "rows": rows,
        "total_hits": total_hits,
        "dedup_dropped": dedup_dropped,
        "per_book": dict(per_book),
        "files_scanned": files_scanned,
    }


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def write_report(result: dict[str, Any], out_path: Path) -> None:
    rows = result["rows"]
    lines: list[str] = []
    lines.append("# Food-Grep Candidates (query-layer step 8c)\n")
    lines.append(
        "Deterministic keyword sweep over `sources/chapters/**/*.md` (all books incl. the "
        "D&E novellas tmk/tss/thk) for food/drink/eating mentions. This is a CANDIDATE POOL, "
        "**not** `working/harvest-queue.md` — rows here graduate to the harvest queue only "
        "after a review pass confirms each is load-bearing (POINT, don't extract; the harvest "
        "queue's own row format is `| status | kind | book | chapter:line | note | session |` — "
        "a reviewer copies a confirmed row over in that shape, they are not auto-appended here).\n"
    )
    lines.append("## Stats\n")
    lines.append(f"- Chapter files scanned: **{result['files_scanned']}**")
    lines.append(f"- Total raw hits (before dedup): **{result['total_hits']}**")
    lines.append(f"- Dropped as already-on-graph (line text matches an existing food node quote): "
                  f"**{result['dedup_dropped']}**")
    lines.append(f"- Surviving candidate rows: **{len(rows)}**")
    lines.append("")
    lines.append("### Per-book counts (surviving candidates)\n")
    lines.append("| book | count |")
    lines.append("|---|---|")
    for book in sorted(result["per_book"], key=lambda b: BOOK_ORDER.get(b, 99)):
        lines.append(f"| {book} | {result['per_book'][book]} |")
    lines.append("")

    named = [r for r in rows if r["match_kind"] == "named_dish"]
    generic = [r for r in rows if r["match_kind"] == "generic_term"]
    lines.append(f"### Match-kind breakdown\n")
    lines.append(f"- Named-dish hits (matches an `object.food` node's name/alias): **{len(named)}**")
    lines.append(f"- Generic-term hits (eat/feast/supper/bread/wine/...): **{len(generic)}**")
    lines.append("")
    lines.append(
        "**Known precision tradeoff (by design, not a bug):** several `object.food` nodes are "
        "short, generic animal/ingredient names (`rat`, `sheep`, `deer`, `quail`, `rabbit`, "
        "`meat`, `bread`...) that are also common non-food words in narrative prose (\"you're "
        "nothing but a little gutter rat\", a character's sigil, a place name). This is a "
        "RECALL-oriented seeder (POINT, don't extract) — false positives are expected and cheap "
        "to skip during the review pass; the alternative (semantic disambiguation) would require "
        "an LLM pass, which is explicitly out of scope for this deterministic tool."
    )
    lines.append("")

    lines.append("## Top 20 sample (named-dish hits first, then generic)\n")
    lines.append("| chapter:line | kind | matched | slugs | note |")
    lines.append("|---|---|---|---|---|")
    sample = (named + generic)[:20]
    for r in sample:
        note = r["text"]
        if len(note) > 140:
            note = note[:137] + "..."
        note = note.replace("|", "\\|")
        slugs = ", ".join(r["matched_slugs"]) if r["matched_slugs"] else "—"
        terms = ", ".join(r["matched_terms"])
        lines.append(f"| `{r['cite']}` | food | {terms} | {slugs} | {note} |")
    lines.append("")

    lines.append("## All surviving candidates\n")
    lines.append("<details><summary>Expand full candidate list "
                  f"({len(rows)} rows)</summary>\n")
    lines.append("")
    lines.append("| chapter:line | kind | matched | slugs | note |")
    lines.append("|---|---|---|---|---|")
    for r in rows:
        note = r["text"]
        if len(note) > 140:
            note = note[:137] + "..."
        note = note.replace("|", "\\|")
        slugs = ", ".join(r["matched_slugs"]) if r["matched_slugs"] else "—"
        terms = ", ".join(r["matched_terms"])
        lines.append(f"| `{r['cite']}` | food | {terms} | {slugs} | {note} |")
    lines.append("")
    lines.append("</details>")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Sweep chapter text for food/drink mentions (candidate pool, not harvest queue).")
    ap.add_argument("--out", default=None, help="Override output path.")
    args = ap.parse_args()

    print("Collecting object.food node keywords ...")
    food_keywords = collect_food_keywords()
    print(f"  {len(food_keywords)} keywords across foods/ nodes")

    print("Collecting existing food-node quotes (dedup set) ...")
    existing_quotes = collect_existing_food_quotes()
    print(f"  {len(existing_quotes)} existing quote lines")

    print("Sweeping sources/chapters/**/*.md ...")
    result = sweep(food_keywords, existing_quotes)
    print(f"  files scanned: {result['files_scanned']}")
    print(f"  total hits: {result['total_hits']}")
    print(f"  dedup dropped: {result['dedup_dropped']}")
    print(f"  surviving candidates: {len(result['rows'])}")
    print("  per-book:", result["per_book"])

    out_path = Path(args.out) if args.out else OUT_PATH
    write_report(result, out_path)
    print(f"\nReport written to: {out_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
