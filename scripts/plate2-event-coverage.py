#!/usr/bin/env python3
"""plate2-event-coverage.py — Plate 2 / 2a: Pass-1 event coverage by existing event nodes.

For every Pass-1 ``## Events & Actions`` entry across all 344 extraction files,
determine whether an existing ``event.*`` node already covers it.

Coverage signals (in priority order):
  1. **Chapter-evidence join** (exact, definitive): the event-node's
     ``graph/index/events/<slug>.index.json`` lists this chapter in
     ``chapters.in_raw_list`` or ``chapters.referenced_in``. ANY Pass-1 event
     in such a chapter MAY be covered by that node — but most Pass-1 events
     are narrative micro-beats (e.g. "Departure at daybreak"), not the named
     event the node represents. So chapter-overlap is reported as
     "chapter-covered" but does NOT imply per-event title match.
  2. **Title fuzzy match** (looser): the bold title from the Pass-1 entry
     (``1. **Title** — description``) matches an existing event slug after
     normalization. This is a stronger per-event signal.

The output is a coverage report describing how many distinct Pass-1 events
have a plausible existing hub vs how many would need a hub minted.

Distinct event de-duplication:
  Pass-1 emits per-chapter, per-line events. The Red Wedding spans 3 chapters
  (asos-catelyn-07 et al.) and produces ~5 bold-title lines per chapter — but
  it is ONE event. We de-dup distinct events by *normalized title*. This is
  approximate (different chapters may use different titles for the same event)
  but it is a *floor* for distinct-event count.

Spot-check cases (D3 motivators):
  - Bran's defenestration  (AGOT Bran I — agot-bran-01? No: Bran II / agot-bran-02)
  - Tywin's privy death    (ASOS Tyrion XI — asos-tyrion-11)
  - Purple Wedding         (ASOS Tyrion VIII — asos-tyrion-08)

Outputs:
  - working/edge-modeling/plate2-event-coverage.md   (the report)
  - working/edge-modeling/plate2-event-coverage.json (full machine-readable)
"""

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXTRACTIONS_DIR = PROJECT_ROOT / "extractions" / "mechanical"
EVENTS_INDEX_DIR = PROJECT_ROOT / "graph" / "index" / "events"
EVENTS_NODES_DIR = PROJECT_ROOT / "graph" / "nodes" / "events"

REPORT_PATH = PROJECT_ROOT / "working" / "edge-modeling" / "plate2-event-coverage.md"
JSON_PATH = PROJECT_ROOT / "working" / "edge-modeling" / "plate2-event-coverage.json"

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]

# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

_NUMBERED_BOLD_RE = re.compile(r"^\s*(\d+)\.\s+\*\*(.+?)\*\*\s*(?:[—–-]|$)")
_EVENTS_HEADING_RE = re.compile(r"^##\s+Events\s*&?\s*Actions\b", re.IGNORECASE)
_ANY_H2_RE = re.compile(r"^##\s+\S")


def parse_event_titles(text: str) -> list[tuple[int, str]]:
    """Return list of (item_number, bold_title) tuples from the ## Events & Actions section."""
    in_section = False
    items: list[tuple[int, str]] = []
    for line in text.splitlines():
        if _EVENTS_HEADING_RE.match(line):
            in_section = True
            continue
        if in_section and _ANY_H2_RE.match(line):
            # New section — stop
            in_section = False
            continue
        if not in_section:
            continue
        m = _NUMBERED_BOLD_RE.match(line)
        if m:
            num = int(m.group(1))
            title = m.group(2).strip()
            items.append((num, title))
    return items


def chapter_id_from_path(p: Path) -> str:
    """`extractions/mechanical/agot/agot-bran-01.extraction.md` -> `agot-bran-01`."""
    return p.name.replace(".extraction.md", "")


def normalize_title(s: str) -> str:
    """Lowercase, strip apostrophes/commas, collapse non-alnum to single dash."""
    s = s.lower()
    s = re.sub(r"['\",]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s


# ---------------------------------------------------------------------------
# Event-node loading
# ---------------------------------------------------------------------------


def load_event_index() -> dict[str, dict]:
    """Read all graph/index/events/*.index.json. Return {slug: index_dict}."""
    idx: dict[str, dict] = {}
    for f in EVENTS_INDEX_DIR.glob("*.index.json"):
        if f.name == "_summary.json":
            continue
        with f.open() as h:
            d = json.load(h)
        idx[d["slug"]] = d
    return idx


def build_chapter_to_events(event_index: dict[str, dict]) -> dict[str, set[str]]:
    """Reverse map: chapter_id -> {event_slug, ...} based on chapters.in_raw_list."""
    out: dict[str, set[str]] = defaultdict(set)
    for slug, d in event_index.items():
        chapters = d.get("chapters", {})
        for c in chapters.get("in_raw_list", []) + chapters.get("referenced_in", []):
            cid = c.get("chapter_id")
            if cid:
                out[cid].add(slug)
    return out


# ---------------------------------------------------------------------------
# Title fuzzy match
# ---------------------------------------------------------------------------


def title_to_slug_candidates(title: str) -> list[str]:
    """Generate plausible slug forms of a title for fuzzy matching."""
    norm = normalize_title(title)
    cands = {norm}
    # Drop leading common articles for an alt-form
    for prefix in ("the-", "a-", "an-"):
        if norm.startswith(prefix):
            cands.add(norm[len(prefix):])
    return list(cands)


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------


def main() -> int:
    if not EXTRACTIONS_DIR.exists():
        print(f"FATAL: {EXTRACTIONS_DIR} not found", file=sys.stderr)
        return 1
    if not EVENTS_INDEX_DIR.exists():
        print(f"FATAL: {EVENTS_INDEX_DIR} not found", file=sys.stderr)
        return 1

    event_index = load_event_index()
    chapter_to_events = build_chapter_to_events(event_index)

    print(f"Loaded {len(event_index)} event-node indexes.", file=sys.stderr)
    print(
        f"Chapter coverage: {len(chapter_to_events)} chapters mentioned by ≥1 event node.",
        file=sys.stderr,
    )

    all_slugs = set(event_index.keys())

    # Per-book stats
    per_book: dict[str, dict] = {}
    # Total Pass-1 event ENTRIES (every numbered item)
    total_entries = 0
    # Distinct events by normalized title
    distinct_titles: set[str] = set()
    # Distinct titles that match an existing event slug exactly (or one-of candidates)
    titles_with_node_match: set[str] = set()
    # Pass-1 entries living in a chapter touched by ANY event node (loose)
    entries_in_node_touched_chapter = 0

    # Spot-check tracking
    spot_checks: dict[str, dict] = {
        "bran-defenestration": {"chapter_candidates": ["agot-bran-02", "agot-bran-03"], "found": []},
        "tywin-privy-death": {"chapter_candidates": ["asos-tyrion-11"], "found": []},
        "purple-wedding": {"chapter_candidates": ["asos-tyrion-08", "asos-sansa-04"], "found": []},
    }

    # Build slug-set for direct match
    slug_set = set(all_slugs)

    # Walk all extraction files
    for book in BOOKS:
        bdir = EXTRACTIONS_DIR / book
        if not bdir.exists():
            print(f"WARN: {bdir} missing", file=sys.stderr)
            continue
        files = sorted(bdir.glob("*.extraction.md"))
        b_entries = 0
        b_distinct = set()
        b_title_match = set()
        b_chap_covered = 0

        for fp in files:
            cid = chapter_id_from_path(fp)
            text = fp.read_text(encoding="utf-8")
            items = parse_event_titles(text)
            if not items:
                continue

            chap_events = chapter_to_events.get(cid, set())
            chap_has_events = bool(chap_events)

            for num, title in items:
                b_entries += 1
                total_entries += 1
                norm = normalize_title(title)
                b_distinct.add(norm)
                distinct_titles.add(norm)

                # Direct slug match
                cands = title_to_slug_candidates(title)
                matched = next((c for c in cands if c in slug_set), None)
                if matched:
                    b_title_match.add(norm)
                    titles_with_node_match.add(norm)

                # Loose: chapter touched by any event node
                if chap_has_events:
                    b_chap_covered += 1
                    entries_in_node_touched_chapter += 1

                # Spot-checks
                lower_title = title.lower()
                # Bran defenestration: jaime pushes bran, fall, etc.
                if "bran" in cid and (
                    "push" in lower_title and ("bran" in lower_title or "tower" in lower_title or "window" in lower_title)
                    or "fall" in lower_title and "bran" in lower_title
                    or "jaime" in lower_title and "bran" in lower_title
                ):
                    spot_checks["bran-defenestration"]["found"].append(
                        {"chapter": cid, "num": num, "title": title}
                    )
                if cid in spot_checks["bran-defenestration"]["chapter_candidates"]:
                    # Also catch by chapter
                    if "push" in lower_title or "fall" in lower_title or "tower" in lower_title or "shove" in lower_title:
                        spot_checks["bran-defenestration"]["found"].append(
                            {"chapter": cid, "num": num, "title": title}
                        )
                # Tywin death
                if "tyrion" in cid and ("tywin" in lower_title and ("die" in lower_title or "kill" in lower_title or "shoot" in lower_title or "privy" in lower_title or "dead" in lower_title)):
                    spot_checks["tywin-privy-death"]["found"].append(
                        {"chapter": cid, "num": num, "title": title}
                    )
                # Purple Wedding / Joffrey death
                if ("joffrey" in lower_title and ("die" in lower_title or "chok" in lower_title or "dead" in lower_title or "poison" in lower_title)) or ("purple" in lower_title and "wedding" in lower_title):
                    spot_checks["purple-wedding"]["found"].append(
                        {"chapter": cid, "num": num, "title": title}
                    )

        per_book[book] = {
            "files": len(files),
            "entries": b_entries,
            "distinct_titles": len(b_distinct),
            "title_node_matches": len(b_title_match),
            "entries_in_node_touched_chapter": b_chap_covered,
        }

    # Distinct events needing mint = distinct_titles - titles_with_node_match
    distinct_needs_mint = distinct_titles - titles_with_node_match

    # Event-node-side: how many event nodes have any chapter linkage?
    events_with_chap_linkage = sum(
        1 for d in event_index.values()
        if (d.get("chapters", {}).get("in_raw_list") or d.get("chapters", {}).get("referenced_in"))
    )

    # Spot-check resolution: for each spot-check, determine if there's a node
    # whose name plausibly covers it.
    def spotcheck_node_coverage(slug_candidates: list[str]) -> list[str]:
        return [s for s in slug_candidates if s in slug_set]

    # Predict event-node names that would cover each spot-check:
    bran_node_candidates = [
        s for s in slug_set
        if "bran" in s and ("fall" in s or "defenestr" in s or "push" in s or "tower" in s)
    ]
    tywin_node_candidates = [
        s for s in slug_set
        if "tywin" in s and ("assassin" in s or "death" in s or "kill" in s)
    ]
    purple_node_candidates = [
        s for s in slug_set if "purple-wedding" in s or "joffrey" in s and "death" in s
    ]

    # ---- Build report ----
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("# Plate 2 / 2a — Event coverage report\n")
    lines.append("**Generated by:** `scripts/plate2-event-coverage.py`  ")
    lines.append("**Inputs:** 344 `extractions/mechanical/{book}/*.extraction.md` + ")
    lines.append("371 `graph/index/events/*.index.json`\n")
    lines.append("---\n")

    lines.append("## Headline numbers\n")
    lines.append(f"- **Total Pass-1 event ENTRIES** (every `1. **Title** — ...` line): `{total_entries:,}`")
    lines.append(f"- **Distinct events** (de-dup by normalized title — APPROXIMATE floor): `{len(distinct_titles):,}`")
    lines.append(f"- **Distinct titles matching an existing event slug**: `{len(titles_with_node_match):,}`")
    lines.append(f"- **Distinct titles with NO matching slug → need MINTING**: `{len(distinct_needs_mint):,}`")
    lines.append("")
    lines.append(f"- **Existing event nodes**: `{len(event_index)}`  (battle 304 + tournament 35 + war 32 per `_summary.json`)")
    lines.append(f"- **Event nodes with ANY Pass-1 chapter linkage**: `{events_with_chap_linkage} / {len(event_index)}`  ({events_with_chap_linkage * 100 // len(event_index)}%)")
    lines.append(f"- **Pass-1 entries in a chapter touched by SOME event node** (loose / upper bound): `{entries_in_node_touched_chapter:,}`")
    lines.append("")

    lines.append("**Reading these numbers:**")
    lines.append("- Title-match is *exact* but conservative — Pass-1 entries are narrative micro-beats")
    lines.append("  (\"Departure at daybreak\", \"Ride back toward Winterfell\"), not historical-event names")
    lines.append("  (\"Red Wedding\", \"Battle of the Blackwater\"). Most never match a wiki-event slug.")
    lines.append("- The chapter-touched count is a loose upper bound: it says \"this Pass-1 entry lives in")
    lines.append("  a chapter that mentions at least one event node\" — not \"this entry IS that event\".")
    lines.append("- The realistic floor for needs-minting is therefore essentially the distinct-titles count")
    lines.append("  minus the small title-slug overlap.")
    lines.append("")

    lines.append("## Per-book breakdown\n")
    lines.append("| Book | Files | Entries | Distinct titles | Title→slug matches | Entries in node-touched chapter |")
    lines.append("|------|------:|--------:|----------------:|-------------------:|-------------------------------:|")
    for b in BOOKS:
        s = per_book.get(b, {})
        lines.append(
            f"| {b.upper()} | {s.get('files', 0)} | {s.get('entries', 0):,} | "
            f"{s.get('distinct_titles', 0):,} | {s.get('title_node_matches', 0):,} | "
            f"{s.get('entries_in_node_touched_chapter', 0):,} |"
        )
    lines.append("")

    # Spot-check results
    lines.append("## Spot-check cases (D3 motivators)\n")
    lines.append("Each case asks: does an `event.*` node exist for this fine-grained narrative event?\n")

    def spot_section(name: str, plain: str, node_cands: list[str], data: dict) -> None:
        lines.append(f"### {plain}")
        if node_cands:
            lines.append(f"- **Event NODE exists?** YES — candidate slug(s): " + ", ".join(f"`{s}`" for s in node_cands))
        else:
            lines.append(f"- **Event NODE exists?** NO — no slug containing the expected keywords")
        lines.append(f"- **Pass-1 entries found in expected chapters** ({len(data['found'])}):")
        seen = set()
        for hit in data["found"][:20]:
            key = (hit["chapter"], hit["num"])
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"  - `{hit['chapter']}` #{hit['num']}: **{hit['title']}**")
        # Determine status
        if data["found"] and node_cands:
            # Check: does any candidate node list one of these chapters?
            chapters_found = {h["chapter"] for h in data["found"]}
            covered_chapters = set()
            for slug in node_cands:
                d = event_index.get(slug, {})
                node_chaps = {
                    c.get("chapter_id")
                    for c in d.get("chapters", {}).get("in_raw_list", [])
                    + d.get("chapters", {}).get("referenced_in", [])
                }
                covered_chapters |= (chapters_found & node_chaps)
            if covered_chapters:
                lines.append(f"- **Verdict:** NODE EXISTS *and* lists the matching chapter(s) {sorted(covered_chapters)} — REUSE.")
            else:
                lines.append(f"- **Verdict:** NODE EXISTS but does NOT list the matching chapter(s) — node has zero Pass-1 chapter linkage. Can REUSE the node, but the chapter→event evidence join is broken (see Discussion).")
        elif data["found"] and not node_cands:
            lines.append("- **Verdict:** NEEDS MINTING — no existing node covers this event.")
        elif not data["found"] and node_cands:
            lines.append("- **Verdict:** Node exists; Pass-1 chapters found 0 matching events. Investigate.")
        else:
            lines.append("- **Verdict:** No matching Pass-1 entries; no node. Spot-check inconclusive.")
        lines.append("")

    spot_section(
        "bran-defenestration",
        "Bran's defenestration (Jaime pushes Bran from the tower)",
        bran_node_candidates,
        spot_checks["bran-defenestration"],
    )
    spot_section(
        "tywin-privy-death",
        "Tywin's privy death (Tyrion shoots Tywin with a crossbow)",
        tywin_node_candidates,
        spot_checks["tywin-privy-death"],
    )
    spot_section(
        "purple-wedding",
        "Purple Wedding (Joffrey poisoned at his wedding)",
        purple_node_candidates,
        spot_checks["purple-wedding"],
    )

    lines.append("## Discussion — the chapter-evidence join is mostly broken\n")
    lines.append(f"Only **{events_with_chap_linkage} of {len(event_index)}** event nodes "
                 f"({events_with_chap_linkage * 100 // len(event_index)}%) have ANY linkage to a Pass-1 chapter in their `chapters.in_raw_list` "
                 "or `chapters.referenced_in` arrays. The remaining ~91% are wiki-derived nodes "
                 "(`battle-beneath-the-wall`, `regency-of-aegon-iii`, `purple-wedding`, "
                 "`assassination-of-tywin-lannister` — the very ones we'd want to reify against) "
                 "with `chapters.in_raw_list = []`. The index was built from the Pass-1 Raw Entity "
                 "List > Wars & Conflicts column, which only captures historical-event NAMES like "
                 "\"War of the Five Kings\" — not the narrative micro-events on the chapter page.\n")
    lines.append("**Consequence for Plate 3:** the chapter-evidence join cannot be the primary "
                 "binding mechanism. Plate 3 has to mine Pass-1 narrative entries directly and "
                 "match against event-node *names* (plus minting). The Pass-1 `## Events & Actions` "
                 "list is the right input — that part of the design holds — but the join key is the "
                 "bold title plus context, not the chapter ID.\n")

    lines.append("## Estimate vs exact — which numbers to trust\n")
    lines.append("- **EXACT:** Pass-1 entry count, distinct-title count, title→slug exact match count,")
    lines.append("  per-book breakdown, event-node count, event-nodes-with-any-chapter-linkage.")
    lines.append("- **APPROXIMATE:** *distinct events* is a FLOOR — different POVs use different titles")
    lines.append("  for the same event (\"The execution\" in agot-bran-01 vs \"Ned beheads the deserter\"")
    lines.append("  if another chapter described it). A more accurate distinct count needs cross-chapter")
    lines.append("  semantic clustering — out of scope for Plate 2.")
    lines.append("- **UPPER BOUND:** `entries_in_node_touched_chapter` is a loose upper bound on how many")
    lines.append("  Pass-1 rows COULD be assigned to an existing node by *some* mechanism.")
    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote: {REPORT_PATH}", file=sys.stderr)

    # JSON dump
    summary = {
        "total_pass1_entries": total_entries,
        "distinct_titles_floor": len(distinct_titles),
        "titles_matching_existing_slug": len(titles_with_node_match),
        "titles_needs_minting": len(distinct_needs_mint),
        "event_nodes_total": len(event_index),
        "event_nodes_with_any_chapter_linkage": events_with_chap_linkage,
        "entries_in_node_touched_chapter": entries_in_node_touched_chapter,
        "per_book": per_book,
        "spot_checks": {
            "bran-defenestration": {
                "node_candidates": bran_node_candidates,
                "pass1_hits": spot_checks["bran-defenestration"]["found"],
            },
            "tywin-privy-death": {
                "node_candidates": tywin_node_candidates,
                "pass1_hits": spot_checks["tywin-privy-death"]["found"],
            },
            "purple-wedding": {
                "node_candidates": purple_node_candidates,
                "pass1_hits": spot_checks["purple-wedding"]["found"],
            },
        },
    }
    JSON_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote: {JSON_PATH}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
