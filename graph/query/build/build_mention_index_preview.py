#!/usr/bin/env python3
"""build_mention_index_preview.py — mention-index REPAIR, preview-only
(query-layer Track, step 8b; design.md G13).

`graph/index/` is behind the project's no-graph-mutation gate (`graph/nodes|
edges|index` — see CLAUDE.md's hard gates). This script does NOT write there.
It re-runs `scripts/build-mention-index.py`'s exact resolution algorithm
(section parsing, name cleaning, title-prefix stripping — all absorbed
verbatim, see `_resolve` below) over the SAME Pass 1 extraction files, but
swaps the alias-resolution source:

  - **live** (`graph/index/chapters/`, `scripts/build-mention-index.py`):
    resolves against `working/wiki/data/alias-resolver.json` — 1,433 aliases,
    the OLDER/narrower table. Harvest-minted nodes (foods added in the S152+
    harvest drain, e.g. `acorn-paste`) were never added to this table, so
    their mentions resolve as "unresolved" even though the Pass 1 extraction
    names them ("Acorn paste" appears in acok-arya-05's Raw Entity List >
    Other section — verified this session) — the index then reports 0
    appearances for that node. This is G13.

  - **preview** (this script, `working/query-layer/mention-index-preview/`):
    resolves against `working/wiki/data/all-node-alias-lookup.json` — 27,588
    phrases / 23,031 entries, the CURRENT hardened all-node table the query
    engine's `resolve.py` and `build_alias_table.py` already use (query-layer
    step 4). This table DOES carry "acorn paste" -> `acorn-paste` (verified
    this session: `all-node-alias-lookup.json["phrase_to_nodes"]["acorn
    paste"]` = `[{"canonical_slug": "acorn-paste", "node_category": "foods",
    ...}]`), so the preview run resolves it.

Ambiguous phrases (>1 candidate in `all-node-alias-lookup.json`, e.g. "addam
of hull" naming BOTH `addam-of-hull` and `addam-velaryon`) resolve to the
FIRST candidate in that table's list (same "first-seen wins" tie-break
`build-mention-index.py`'s own alias step already uses for collisions) —
logged to the report's ambiguous-phrase sample so Matt can see the tie-break
in action, not silently hidden.

Output shape is IDENTICAL to `graph/index/chapters/` (one `<chapter_id>.
mentions.json` per chapter + a `_summary.json`) so a diff between the two
trees is a direct file-for-file comparison, and so the eventual `apply`
(copying preview -> graph/index/chapters/, Matt's go) is a straight directory
replace, not a reshape.

This script is READ-ONLY over graph/nodes, extractions/, and the alias
tables; its only write target is `working/query-layer/mention-index-preview/`.

Usage:
    python3 graph/query/build/build_mention_index_preview.py [--book agot] [--all]
    python3 graph/query/build/build_mention_index_preview.py --report-only
        (skip writing preview files; just print the before/after summary —
        used for a fast re-check without touching the preview tree)

No LLM in the loop. Ever.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_THIS_FILE = Path(__file__).resolve()
REPO_ROOT = _THIS_FILE.parents[3]  # build -> query -> graph -> repo root

sys.path.insert(0, str(REPO_ROOT / "graph" / "query"))

EXTRACTIONS_DIR = REPO_ROOT / "extractions" / "mechanical"
GRAPH_NODES_DIR = REPO_ROOT / "graph" / "nodes"
LIVE_INDEX_DIR = REPO_ROOT / "graph" / "index" / "chapters"  # READ-ONLY reference for the report
ALL_NODE_ALIAS_LOOKUP = REPO_ROOT / "working" / "wiki" / "data" / "all-node-alias-lookup.json"
PREVIEW_DIR = REPO_ROOT / "working" / "query-layer" / "mention-index-preview" / "chapters"
REPORT_PATH = REPO_ROOT / "working" / "query-layer" / "mention-index-repair-report.md"

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]
EXCLUDED_NODE_DIRS = {"_conflicts", "_unclassified"}

# ---------------------------------------------------------------------------
# Parsing constants — absorbed VERBATIM from scripts/build-mention-index.py
# (same section names, same table/bullet parsing) so the preview's mention
# EXTRACTION is identical; only the alias-resolution SOURCE differs.
# ---------------------------------------------------------------------------

TABLE_SECTIONS = {
    "Characters Present", "Character Appearances", "Characters Referenced",
    "Locations", "Location Descriptions", "Artifacts & Objects of Significance",
}
RAW_ENTITY_SUBSECTIONS = {
    "Characters", "Locations", "Houses", "Factions & Organizations",
    "Religions & Faiths", "Cultures & Peoples", "Artifacts & Objects",
    "In-world Texts & Songs", "Magic & Phenomena", "Wars & Conflicts",
    "Titles & Offices", "Other",
}
DIR_TO_NODE_TYPE = {
    "characters": "character", "locations": "place.location",
    "houses": "organization.house", "factions": "organization.faction",
    "religions": "organization.religion", "concepts": "concept",
    "customs": "concept.custom", "events": "event", "artifacts": "object.artifact",
    "texts": "object.text", "foods": "object.food", "materials": "object.material",
    "species": "species", "titles": "title", "theories": "concept.theory",
    "prophecies": "concept.prophecy", "languages": "concept.language",
    "medical": "concept.medical",
}
_PAREN_RE = re.compile(r"\s*\([^)]*\)")
_EMDASH_RE = re.compile(r"\s*[—–].*$")
_ROLE_SUFFIX_RE = re.compile(
    r"\s*(POV|deceased|dead|referenced|inferred|unnamed|historical|off-page|presumed dead"
    r"|historical referenced|historical figure|historical character)\s*$",
    re.IGNORECASE,
)
_TITLE_PREFIXES = [
    "grand-maester-", "maester-", "lord-commander-", "lord-", "lady-",
    "king-", "queen-", "prince-", "princess-", "ser-", "septa-", "septon-",
    "khal-", "khaleesi-", "the-", "a-",
]
_KNOWN_HEADERS = {
    "character", "location", "artifact", "role in chapter", "role",
    "context of reference", "context", "meal/occasion", "event", "type",
    "host", "phase", "who", "information", "speaker", "character a",
    "question", "character appearances", "hair",
}


def to_kebab(text: str) -> str:
    s = text.lower()
    s = re.sub(r"['\",]", "", s)
    s = re.sub(r"[ _]+", "-", s)
    s = re.sub(r"[^a-z0-9-]", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def clean_raw_name(raw: str) -> str:
    s = raw.strip()
    s = _PAREN_RE.sub("", s)
    s = _EMDASH_RE.sub("", s)
    s = _ROLE_SUFFIX_RE.sub("", s)
    return s.strip()


def build_node_index() -> dict[str, tuple[str, str]]:
    index: dict[str, tuple[str, str]] = {}
    for node_file in GRAPH_NODES_DIR.rglob("*.node.md"):
        try:
            rel = node_file.relative_to(GRAPH_NODES_DIR)
        except ValueError:
            continue
        type_dir = rel.parts[0]
        if type_dir in EXCLUDED_NODE_DIRS:
            continue
        slug = node_file.name.removesuffix(".node.md")
        node_type = DIR_TO_NODE_TYPE.get(type_dir, type_dir)
        rel_path = str(node_file.relative_to(REPO_ROOT))
        index.setdefault(slug, (node_type, rel_path))
    return index


def strip_title_prefix(slug: str) -> str | None:
    for prefix in _TITLE_PREFIXES:
        if slug.startswith(prefix):
            stripped = slug[len(prefix):]
            if stripped:
                return stripped
    return None


# ---------------------------------------------------------------------------
# The REPAIRED alias source — all-node-alias-lookup.json (query-layer step 4's
# hardened table), NOT the older alias-resolver.json build-mention-index.py
# reads today.
# ---------------------------------------------------------------------------

def load_all_node_alias_lookup(path: Path = ALL_NODE_ALIAS_LOOKUP) -> dict[str, list[dict]]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("phrase_to_nodes", {})


def resolve(
    raw_name: str,
    node_index: dict[str, tuple[str, str]],
    phrase_to_nodes: dict[str, list[dict]],
    ambiguous_log: Counter,
) -> tuple[str | None, str, str | None, str | None]:
    """Same resolution shape as build-mention-index.py's resolve(): returns
    (slug, resolved_via, node_type, node_path). `resolved_via` is one of
    "direct", "alias", "unresolved" (kept identical to the live builder's
    vocabulary so a before/after diff on this field is meaningful)."""
    cleaned = clean_raw_name(raw_name)
    if not cleaned:
        return None, "unresolved", None, None
    slug = to_kebab(cleaned)
    if not slug:
        return None, "unresolved", None, None

    # 1. Direct lookup (unchanged from the live builder).
    if slug in node_index:
        node_type, node_path = node_index[slug]
        return slug, "direct", node_type, node_path

    # 2. REPAIRED alias lookup — all-node-alias-lookup.json, keyed by the
    #    natural-language phrase (NOT the kebab slug — this table's keys are
    #    lowercased phrases like "acorn paste", so look up `cleaned.lower()`,
    #    matching how build_alias_table.py populates it).
    phrase_key = cleaned.lower()
    candidates = phrase_to_nodes.get(phrase_key)
    if candidates:
        if len(candidates) > 1:
            ambiguous_log[phrase_key] += 1
        chosen = candidates[0]
        canonical = chosen.get("canonical_slug")
        if canonical and canonical in node_index:
            node_type, node_path = node_index[canonical]
            return canonical, "alias", node_type, node_path
        if canonical:
            return canonical, "alias", chosen.get("node_type"), None

    # 3. Prefix-stripped direct lookup.
    stripped = strip_title_prefix(slug)
    if stripped is not None:
        if stripped in node_index:
            node_type, node_path = node_index[stripped]
            return stripped, "direct", node_type, node_path
        stripped_phrase = stripped.replace("-", " ")
        candidates = phrase_to_nodes.get(stripped_phrase)
        if candidates:
            if len(candidates) > 1:
                ambiguous_log[stripped_phrase] += 1
            chosen = candidates[0]
            canonical = chosen.get("canonical_slug")
            if canonical and canonical in node_index:
                node_type, node_path = node_index[canonical]
                return canonical, "alias", node_type, node_path
            if canonical:
                return canonical, "alias", chosen.get("node_type"), None

    return slug, "unresolved", None, None


# ---------------------------------------------------------------------------
# Extraction parsing (verbatim structure from build-mention-index.py)
# ---------------------------------------------------------------------------

def parse_table_row_col1(line: str) -> str | None:
    line = line.strip()
    if not line.startswith("|"):
        return None
    cells = [c.strip() for c in line.split("|")]
    if len(cells) < 2:
        return None
    col1 = cells[1].strip()
    if not col1:
        return None
    if re.fullmatch(r"[-:| ]+", col1):
        return None
    if col1.lower() in _KNOWN_HEADERS:
        return None
    return col1


def parse_bullet_line(line: str) -> str | None:
    stripped = line.strip()
    if not stripped.startswith("-"):
        return None
    content = stripped[1:].strip()
    if not content or content.lower() == "none":
        return None
    return content


def parse_extraction(
    extraction_path: Path,
    node_index: dict[str, tuple[str, str]],
    phrase_to_nodes: dict[str, list[dict]],
    ambiguous_log: Counter,
) -> list[dict]:
    try:
        content = extraction_path.read_text(encoding="utf-8")
    except OSError:
        return []

    lines = content.splitlines()
    mentions: list[dict] = []
    seen: set[tuple[str, str]] = set()
    current_section: str | None = None
    in_raw_entity_list = False
    current_subsection: str | None = None
    in_table_section = False

    for lineno, line in enumerate(lines, start=1):
        if line.startswith("## "):
            section_name = line[3:].strip()
            in_raw_entity_list = (section_name == "Raw Entity List")
            current_section = section_name
            current_subsection = None
            in_table_section = (section_name in TABLE_SECTIONS)
            continue
        if line.startswith("### ") and in_raw_entity_list:
            current_subsection = line[4:].strip()
            continue
        if in_table_section and "|" in line:
            col1 = parse_table_row_col1(line)
            if col1 and col1.lower() != "none":
                key = (current_section or "", col1)
                if key not in seen:
                    seen.add(key)
                    slug, resolved_via, node_type, node_path = resolve(
                        col1, node_index, phrase_to_nodes, ambiguous_log
                    )
                    if slug:
                        mentions.append({
                            "raw_name": col1, "slug": slug, "resolved_via": resolved_via,
                            "node_type": node_type, "node_path": node_path,
                            "section": current_section, "line": lineno,
                        })
            continue
        if in_raw_entity_list and current_subsection in RAW_ENTITY_SUBSECTIONS:
            item = parse_bullet_line(line)
            if item:
                section_label = f"Raw Entity List > {current_subsection}"
                key = (section_label, item)
                if key not in seen:
                    seen.add(key)
                    slug, resolved_via, node_type, node_path = resolve(
                        item, node_index, phrase_to_nodes, ambiguous_log
                    )
                    if slug:
                        mentions.append({
                            "raw_name": item, "slug": slug, "resolved_via": resolved_via,
                            "node_type": node_type, "node_path": node_path,
                            "section": section_label, "line": lineno,
                        })
    return mentions


def chapter_id_from_path(extraction_path: Path) -> str:
    return extraction_path.name.removesuffix(".extraction.md")


def pov_character_from_chapter_id(chapter_id: str) -> str:
    parts = chapter_id.split("-")
    if len(parts) < 3:
        return chapter_id
    return "-".join(parts[1:-1])


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run(books: list[str], write_files: bool) -> dict[str, Any]:
    node_index = build_node_index()
    phrase_to_nodes = load_all_node_alias_lookup()
    ambiguous_log: Counter = Counter()

    per_chapter_preview: dict[str, dict] = {}
    total_mentions = total_direct = total_alias = total_unresolved = 0
    unresolved_counter: Counter = Counter()

    for book in books:
        book_dir = EXTRACTIONS_DIR / book
        if not book_dir.exists():
            continue
        for ef in sorted(book_dir.glob("*.extraction.md")):
            chapter_id = chapter_id_from_path(ef)
            pov = pov_character_from_chapter_id(chapter_id)
            mentions = parse_extraction(ef, node_index, phrase_to_nodes, ambiguous_log)
            direct = sum(1 for m in mentions if m["resolved_via"] == "direct")
            alias = sum(1 for m in mentions if m["resolved_via"] == "alias")
            unresolved = sum(1 for m in mentions if m["resolved_via"] == "unresolved")
            for m in mentions:
                if m["resolved_via"] == "unresolved":
                    unresolved_counter[m["slug"]] += 1
            total_mentions += len(mentions)
            total_direct += direct
            total_alias += alias
            total_unresolved += unresolved

            record = {
                "chapter_id": chapter_id, "book": book, "pov_character": pov,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "extraction_path": str(ef.relative_to(REPO_ROOT)),
                "stats": {
                    "total_mentions": len(mentions), "resolved_to_node": direct + alias,
                    "direct": direct, "alias": alias, "unresolved": unresolved,
                },
                "mentions": mentions,
            }
            per_chapter_preview[chapter_id] = record

            if write_files:
                out_dir = PREVIEW_DIR / book
                out_dir.mkdir(parents=True, exist_ok=True)
                (out_dir / f"{chapter_id}.mentions.json").write_text(
                    json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8"
                )

    resolved = total_direct + total_alias
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "books_processed": books,
        "source": "all-node-alias-lookup.json (hardened table, query-layer step 4)",
        "chapters_processed": len(per_chapter_preview),
        "total_mentions": total_mentions,
        "resolved": resolved, "direct": total_direct, "alias": total_alias,
        "unresolved": total_unresolved,
        "resolution_rate_pct": round(resolved / total_mentions * 100, 1) if total_mentions else 0.0,
        "top_unresolved": [{"slug": s, "count": c} for s, c in unresolved_counter.most_common(20)],
        "top_ambiguous_phrases": [{"phrase": p, "count": c} for p, c in ambiguous_log.most_common(20)],
    }
    if write_files:
        PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
        (PREVIEW_DIR / "_summary.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    return {"summary": summary, "per_chapter": per_chapter_preview}


# ---------------------------------------------------------------------------
# Live-index comparison (for the report)
# ---------------------------------------------------------------------------

def load_live_summary() -> dict[str, Any] | None:
    p = LIVE_INDEX_DIR / "_summary.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def live_slug_appearances(slug: str) -> int | None:
    """Count appearances of `slug` across the LIVE graph/index/chapters/ tree
    (read-only) — used for the report's before/after spot-checks. Returns
    None if the live index doesn't exist at all."""
    if not LIVE_INDEX_DIR.exists():
        return None
    count = 0
    for mfile in LIVE_INDEX_DIR.rglob("*.mentions.json"):
        try:
            data = json.loads(mfile.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for m in data.get("mentions", []):
            if m.get("slug") == slug:
                count += 1
    return count


def preview_slug_appearances(preview_result: dict[str, Any], slug: str) -> int:
    count = 0
    for record in preview_result["per_chapter"].values():
        for m in record["mentions"]:
            if m.get("slug") == slug:
                count += 1
    return count


def diff_against_live(preview_result: dict[str, Any]) -> dict[str, Any]:
    """Compare the preview's per-chapter mention files against the LIVE
    graph/index/chapters/ tree (read-only comparison; live is never
    modified). Returns counts of chapters that would change + a sample."""
    changed = 0
    unchanged = 0
    missing_live = 0
    sample_diffs: list[dict[str, Any]] = []

    for chapter_id, preview_record in preview_result["per_chapter"].items():
        book = preview_record["book"]
        live_path = LIVE_INDEX_DIR / book / f"{chapter_id}.mentions.json"
        if not live_path.exists():
            missing_live += 1
            continue
        try:
            live_record = json.loads(live_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            missing_live += 1
            continue

        live_stats = live_record.get("stats", {})
        preview_stats = preview_record["stats"]
        if live_stats.get("resolved_to_node") != preview_stats["resolved_to_node"] or \
           live_stats.get("unresolved") != preview_stats["unresolved"]:
            changed += 1
            if len(sample_diffs) < 15:
                sample_diffs.append({
                    "chapter_id": chapter_id,
                    "live_resolved": live_stats.get("resolved_to_node"),
                    "preview_resolved": preview_stats["resolved_to_node"],
                    "live_unresolved": live_stats.get("unresolved"),
                    "preview_unresolved": preview_stats["unresolved"],
                })
        else:
            unchanged += 1

    return {
        "changed": changed, "unchanged": unchanged, "missing_live": missing_live,
        "sample_diffs": sample_diffs,
    }


# Spot-check slugs (query-layer step 8b) — verified this session, by tracing
# BOTH resolvers by hand (see the session notes), to have a BULLETED
# Raw-Entity-List mention (so extraction-parsing is not the confound) that
# resolves as "unresolved" under the OLD alias-resolver.json (1,433 aliases)
# but resolves via the NEW all-node-alias-lookup.json (27,588 phrases) table.
# (Earlier candidates like "guest-right"/"cupbearer" were re-checked and
# found to already resolve via DIRECT slug match under the old table too —
# not a genuine before/after; excluded from this list after verification.)
# NOTE (important caveat, see the report's own "Known extraction-format gap"
# section): `acorn-paste` itself does NOT move in this preview — its ONE
# Pass-1 mention (acok-arya-05's "Raw Entity List > Other") is written as an
# un-bulleted comma-separated prose line ("Acorn paste (...), water dancer
# (...)"), a format build-mention-index.py's bullet-only parser (and this
# preview, which absorbs that same parser verbatim) never extracts — that is
# an EXTRACTION-format gap (Pass 1 schema drift), not an alias-table gap, and
# is out of scope for this alias-table repair. It is surfaced as its own
# finding, not silently glossed over.
KNOWN_STALE_SLUGS = ["crow-cage", "lemonwater", "goat", "acorn-paste"]


_OTHER_SUBSECTION_RE = re.compile(r"^### Other\s*$")


def count_unbulleted_other_lines(books: list[str]) -> int:
    """Count non-bulleted, non-'None' content lines inside 'Raw Entity List >
    Other' subsections across the processed books — a Pass-1 EXTRACTION-
    format inconsistency (some chapters write this subsection as a
    comma-separated prose line instead of the schema's bulleted list), which
    is why some resolvable-in-principle mentions (e.g. `acorn-paste` in
    acok-arya-05) never reach the resolver at all. Out of scope for THIS
    alias-table repair (a Pass-1 prompt/extraction-quality issue) — counted
    here so the report doesn't silently claim more than the alias-table fix
    actually delivers."""
    count = 0
    for book in books:
        book_dir = EXTRACTIONS_DIR / book
        if not book_dir.exists():
            continue
        for ef in book_dir.glob("*.extraction.md"):
            lines = ef.read_text(encoding="utf-8").splitlines()
            in_raw = False
            sub = None
            for line in lines:
                if line.startswith("## "):
                    in_raw = (line[3:].strip() == "Raw Entity List")
                    sub = None
                    continue
                if line.startswith("### ") and in_raw:
                    sub = line[4:].strip()
                    continue
                if in_raw and sub in RAW_ENTITY_SUBSECTIONS and line.strip():
                    stripped = line.strip()
                    if stripped.lower() == "none" or stripped.startswith("-"):
                        continue
                    count += 1
    return count


def write_report(preview_result: dict[str, Any], diff: dict[str, Any], books: list[str]) -> None:
    live_summary = load_live_summary()
    lines: list[str] = []
    lines.append("# Mention-Index Repair Report (preview-only, query-layer step 8b)\n")
    lines.append(
        "`graph/index/` is behind the no-graph-mutation gate — this report describes a "
        "PREVIEW build at `working/query-layer/mention-index-preview/`, not a live change. "
        "Nothing under `graph/` was written by this script.\n"
    )
    lines.append("## Headline\n")
    if live_summary:
        lines.append(f"- Live index resolution rate: **{live_summary.get('resolution_rate_pct')}%** "
                      f"({live_summary.get('resolved'):,} / {live_summary.get('total_mentions'):,})")
    lines.append(f"- Preview index resolution rate: **{preview_result['summary']['resolution_rate_pct']}%** "
                  f"({preview_result['summary']['resolved']:,} / {preview_result['summary']['total_mentions']:,})")
    lines.append(f"- Chapters whose resolved/unresolved counts would CHANGE: **{diff['changed']:,}** "
                  f"(unchanged: {diff['unchanged']:,}, no live file to compare: {diff['missing_live']:,})")
    lines.append("")

    lines.append("## Known-stale spot-checks (before -> after)\n")
    lines.append(
        "Slugs verified this session to have a BULLETED Raw-Entity-List mention (so "
        "extraction-parsing is not the confound) that only resolves once the alias source "
        "is switched from `alias-resolver.json` (1,433 aliases) to `all-node-alias-lookup.json` "
        "(27,588 phrases, the query-layer step-4 hardened table).\n"
    )
    lines.append("| slug | live appearances | preview appearances |")
    lines.append("|---|---|---|")
    for slug in KNOWN_STALE_SLUGS:
        live_count = live_slug_appearances(slug)
        preview_count = preview_slug_appearances(preview_result, slug)
        live_str = str(live_count) if live_count is not None else "(no live index)"
        lines.append(f"| `{slug}` | {live_str} | {preview_count} |")
    lines.append("")

    unbulleted = count_unbulleted_other_lines(books)
    lines.append("## Known extraction-format gap (OUT OF SCOPE for this repair)\n")
    lines.append(
        f"`acorn-paste` does NOT move in this preview ({live_slug_appearances('acorn-paste')} -> "
        f"{preview_slug_appearances(preview_result, 'acorn-paste')}) despite being exactly the "
        "case design.md's step-8b card names as the motivating example. Root cause: its one "
        "Pass-1 mention (acok-arya-05, 'Raw Entity List > Other') is written as an un-bulleted, "
        "comma-separated prose line (\"Acorn paste (survival food technique taught by Kurz), "
        "water dancer (...)\"), not the schema's bulleted list — `build-mention-index.py`'s "
        "bullet-only parser (absorbed verbatim here) never extracts it as a mention candidate "
        "at all, so no alias-table fix can resolve it. This is a Pass-1 EXTRACTION-format "
        "inconsistency, not an alias-table gap — "
        f"**{unbulleted} non-bulleted 'Other'-subsection content lines** exist across the "
        "processed corpus (same class of gap). Fixing it would mean either a Pass-1 re-extraction "
        "pass or a looser (comma-splitting) parser for this one subsection — both out of scope "
        "for the alias-table repair this step delivers. Flagged here, not silently absorbed into "
        "the headline number."
    )
    lines.append("")

    lines.append("## Sample chapter diffs (up to 15)\n")
    if diff["sample_diffs"]:
        lines.append("| chapter | live resolved | preview resolved | live unresolved | preview unresolved |")
        lines.append("|---|---|---|---|---|")
        for d in diff["sample_diffs"]:
            lines.append(
                f"| {d['chapter_id']} | {d['live_resolved']} | {d['preview_resolved']} | "
                f"{d['live_unresolved']} | {d['preview_unresolved']} |"
            )
    else:
        lines.append("(none in the first 15 scanned — see the full preview tree for more)")
    lines.append("")

    lines.append("## Top unresolved slugs remaining in the preview (up to 20)\n")
    for row in preview_result["summary"]["top_unresolved"]:
        lines.append(f"- `{row['slug']}` — {row['count']}")
    lines.append("")

    lines.append("## Top ambiguous phrases (first-candidate tie-break used, up to 20)\n")
    if preview_result["summary"]["top_ambiguous_phrases"]:
        for row in preview_result["summary"]["top_ambiguous_phrases"]:
            lines.append(f"- \"{row['phrase']}\" — {row['count']} occurrence(s)")
    else:
        lines.append("(none)")
    lines.append("")

    lines.append("## Apply command (Matt's go required — NOT run by this script)\n")
    lines.append("```")
    lines.append("# Replaces graph/index/chapters/ with the reviewed preview tree.")
    lines.append("# This IS a graph/index/ write — needs Matt's explicit go per the no-mutation gate.")
    lines.append("rm -rf graph/index/chapters")
    lines.append("cp -r working/query-layer/mention-index-preview/chapters graph/index/chapters")
    lines.append("# Then re-run the per-entity rollups so graph/index/<type>/ picks up the repair:")
    lines.append("bash scripts/weirwood-refresh.sh")
    lines.append("```\n")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to: {REPORT_PATH.relative_to(REPO_ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Preview-build a repaired mention index (does NOT write graph/index/).")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--book", choices=BOOKS)
    group.add_argument("--all", action="store_true", dest="all_books")
    ap.add_argument("--report-only", action="store_true", help="Compute the report without writing preview files.")
    args = ap.parse_args()

    books = [args.book] if args.book else BOOKS
    write_files = not args.report_only

    print(f"Building mention-index PREVIEW for books: {', '.join(books)} (write_files={write_files})")
    result = run(books, write_files)
    print(f"  chapters={result['summary']['chapters_processed']}  "
          f"mentions={result['summary']['total_mentions']:,}  "
          f"resolved={result['summary']['resolved']:,} ({result['summary']['resolution_rate_pct']}%)")

    diff = diff_against_live(result)
    print(f"  vs live: changed={diff['changed']}  unchanged={diff['unchanged']}  "
          f"missing_live={diff['missing_live']}")

    write_report(result, diff, books)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
