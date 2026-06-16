#!/usr/bin/env python3
"""Backfill `occurred:` frontmatter blocks onto event nodes from chronology year-page data.

Reads working/wiki/data/chronology-events.jsonl and deterministically assigns AC years
to event nodes where exactly one year is attested. Everything ambiguous is staged to a
report; nothing ambiguous is written.

Classification:
  CLEAN      -- node file exists + exactly one distinct year_value + not in BLOCKLIST
  MULTIYEAR  -- node exists but >1 distinct year (wars, multi-event stubs) → STAGE only
  NOMATCH    -- no node file for the slug → STAGE only
  ALREADY_DATED -- node already has occurred: block → SKIP (idempotent)

Safety:
  - Frontmatter-only, region-scoped patch — body is preserved byte-for-byte
  - Re-reads each file immediately before write (no stale buffer)
  - Idempotent — second --apply run is a no-op on already-dated nodes
  - --dry-run is DEFAULT; --apply required to write
  - Validator runs on every block before write; aborts file on violation

Usage:
  python3 scripts/date-event-nodes.py                    # dry-run (default)
  python3 scripts/date-event-nodes.py --apply            # write CLEAN nodes
  python3 scripts/date-event-nodes.py --report-only      # report only, skip node scan
"""
import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
CHRONOLOGY_FILE = ROOT / "working/wiki/data/chronology-events.jsonl"
EVENT_NODE_DIR = ROOT / "graph/nodes/events"
REPORT_DIR = ROOT / "working/session-results"
REPORT_FILE = REPORT_DIR / "2026-06-16-event-dating-dryrun.md"
EDGES_FILE = ROOT / "graph/edges/edges.jsonl"

# Hard-exclude these slugs even if they happen to appear single-year
BLOCKLIST = {"great-council", "tourney", "first-dornish-war", "long-night"}

VALID_PRECISIONS = {"exact", "year", "decade", "century", "era", "relative-only"}

# Book ordering for narrative_first computation
BOOK_ORDER = {"agot": 1, "acok": 2, "asos": 3, "affc": 4, "adwd": 5,
              "thk": 0, "tss": 0, "tmk": 0}

# Roman numeral mapping for chapter normalization
_ROMAN = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8,
    "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15,
    "XVI": 16, "XVII": 17, "XVIII": 18, "XIX": 19, "XX": 20,
    "XXI": 21, "XXII": 22, "XXIII": 23, "XXIV": 24, "XXV": 25,
}

# POV name normalization: prose form → kebab slug (reverse of pov-characters.md)
_POV_SLUG = {
    "Arya": "arya", "Bran": "bran", "Catelyn": "catelyn", "Daenerys": "daenerys",
    "Eddard": "eddard", "Ned": "eddard", "Jon": "jon", "Sansa": "sansa",
    "Tyrion": "tyrion", "Theon": "theon", "Davos": "davos", "Jaime": "jaime",
    "Samwell": "samwell", "Sam": "samwell",
    "Cersei": "cersei", "Brienne": "brienne", "Alayne": "alayne",
    "Reek": "reek", "Barristan": "barristan", "Melisandre": "melisandre",
    "Victarion": "victarion", "Quentyn": "quentyn",
    # AFFC descriptive titles
    "The Prophet": "the-prophet", "The Drowned Man": "the-drowned-man",
    "The Iron Captain": "the-iron-captain", "The Kraken's Daughter": "the-krakens-daughter",
    "The Captain of Guards": "the-captain-of-guards",
    "The Soiled Knight": "the-soiled-knight", "The Queenmaker": "the-queenmaker",
    "The Princess in the Tower": "the-princess-in-the-tower",
    "Cat of the Canals": "cat-of-the-canals", "The Reaver": "the-reaver",
    # ADWD descriptive titles
    "The Merchant's Man": "the-merchants-man", "The Turncloak": "the-turncloak",
    "The Prince of Winterfell": "the-prince-of-winterfell",
    "The Lost Lord": "the-lost-lord", "The Windblown": "the-windblown",
    "The Wayward Bride": "the-wayward-bride", "The Watcher": "the-watcher",
    "The King's Prize": "the-kings-prize", "The Dragontamer": "the-dragontamer",
    "The Griffin Reborn": "the-griffin-reborn", "The Sacrifice": "the-sacrifice",
    "The Ugly Little Girl": "the-ugly-little-girl",
    "The Discarded Knight": "the-discarded-knight",
    "The Spurned Suitor": "the-spurned-suitor", "The Queensguard": "the-queensguard",
    "The Blind Girl": "the-blind-girl", "A Ghost in Winterfell": "a-ghost-in-winterfell",
    "The Iron Suitor": "the-iron-suitor", "The Kingbreaker": "the-kingbreaker",
    "The Queen's Hand": "the-queens-hand",
    "Jon Connington": "jon-connington",
    "Prologue": "prologue", "Epilogue": "epilogue",
}

# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

_FM_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def split_frontmatter(text: str) -> tuple[dict, str, str]:
    """Return (fm_dict_raw_str, body_str, fm_delimiter_block).

    Returns the raw YAML string, the body (everything after second ---), and
    the original frontmatter block (including delimiters) for reconstruction.
    """
    m = _FM_RE.match(text)
    if not m:
        raise ValueError("No valid frontmatter block found")
    raw_yaml = m.group(1)
    body = text[m.end():]
    fm_block = m.group(0)
    return raw_yaml, body, fm_block


def body_hash(body: str) -> str:
    return hashlib.sha256(body.encode()).hexdigest()


def has_occurred_block(raw_yaml: str) -> bool:
    """Check if occurred: key already present in frontmatter."""
    for line in raw_yaml.splitlines():
        if re.match(r"^occurred\s*:", line):
            return True
    return False


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------

def validate_occurred_block(block: dict) -> None:
    """Raise ValueError if the occurred block violates schema invariants.

    block should be the dict that will be written under the 'occurred:' key.
    """
    # ac_year must be int (None is allowed to represent "unknown")
    if "ac_year" in block and block["ac_year"] is not None:
        if not isinstance(block["ac_year"], int):
            raise ValueError(
                f"ac_year must be int, got {type(block['ac_year']).__name__!r}: {block['ac_year']!r}"
            )
    # No reckoning: key allowed
    if "reckoning" in block:
        raise ValueError("'reckoning:' key must not appear in occurred: block")
    # If ac_year_end present: must be int and > ac_year
    if "ac_year_end" in block:
        if not isinstance(block["ac_year_end"], int):
            raise ValueError("ac_year_end must be int")
        if block.get("ac_year") is not None and block["ac_year_end"] <= block["ac_year"]:
            raise ValueError("ac_year_end must be > ac_year")
    # uncertainty_radius and ac_year_end are mutually exclusive
    if "uncertainty_radius" in block and "ac_year_end" in block:
        raise ValueError("uncertainty_radius and ac_year_end are mutually exclusive")
    # basis_source required when ac_year non-null
    if block.get("ac_year") is not None and not block.get("basis_source"):
        raise ValueError("basis_source required when ac_year is set")
    # tertiary-fan => date_confidence tier >= 3
    if block.get("basis_reliability") == "tertiary-fan":
        dc = block.get("date_confidence", "")
        m = re.match(r"tier-(\d+)", dc)
        if not m or int(m.group(1)) < 3:
            raise ValueError(
                f"basis_reliability=tertiary-fan requires date_confidence tier >= 3, got {dc!r}"
            )
    # precision must be in valid set
    if "precision" in block:
        if block["precision"] not in VALID_PRECISIONS:
            raise ValueError(f"precision {block['precision']!r} not in {VALID_PRECISIONS}")


# ---------------------------------------------------------------------------
# Frontmatter insertion
# ---------------------------------------------------------------------------

def build_occurred_yaml(ac_year: int) -> str:
    """Build the YAML lines for the occurred: block."""
    lines = [
        "occurred:",
        f"  ac_year: {ac_year}",
        "  precision: year",
        "  basis_source: wiki-year-page",
        "  basis_reliability: tertiary-fan",
        "  date_confidence: tier-3",
    ]
    return "\n".join(lines)


def insert_occurred_into_frontmatter(raw_yaml: str, ac_year: int) -> str:
    """Return new raw_yaml with occurred: block inserted before the first blank line
    or at end if no blank line. Appended as a clean block at the end of frontmatter."""
    occurred_yaml = build_occurred_yaml(ac_year)
    # Append at end of existing frontmatter (clean separation)
    return raw_yaml.rstrip("\n") + "\n" + occurred_yaml


def patch_node_file(path: Path, ac_year: int, apply: bool) -> tuple[bool, str]:
    """Patch a node file to add occurred: block.

    Returns (was_written: bool, message: str).
    Reads file fresh from disk immediately before patching.
    Verifies body hash before/after.
    """
    # Re-read fresh from disk
    text = path.read_text(encoding="utf-8")

    raw_yaml, body, fm_block = split_frontmatter(text)
    before_hash = body_hash(body)

    # Build occurred block dict for validation
    occurred = {
        "ac_year": ac_year,
        "precision": "year",
        "basis_source": "wiki-year-page",
        "basis_reliability": "tertiary-fan",
        "date_confidence": "tier-3",
    }
    validate_occurred_block(occurred)

    # Build new frontmatter
    new_yaml = insert_occurred_into_frontmatter(raw_yaml, ac_year)
    new_text = "---\n" + new_yaml + "\n---\n" + body

    # Verify body is preserved byte-for-byte
    _, new_body, _ = split_frontmatter(new_text)
    after_hash = body_hash(new_body)
    if before_hash != after_hash:
        raise RuntimeError(
            f"Body hash mismatch for {path.name}: {before_hash[:8]} -> {after_hash[:8]}"
        )

    if apply:
        path.write_text(new_text, encoding="utf-8")
        return True, f"wrote ac_year={ac_year}"
    else:
        return False, f"dry-run ac_year={ac_year}"


# ---------------------------------------------------------------------------
# Chapter reference normalization for narrative_first
# ---------------------------------------------------------------------------

def normalize_chapter_ref(ref: str) -> Optional[tuple[int, int]]:
    """Normalize a chapter ref to (book_order, chapter_number) or None on failure.

    Handles two formats:
      kebab: "agot-arya-01"  -> (book_order, 1)
      roman: "ASOS Catelyn VII" -> (book_order, 7)
    """
    if not ref:
        return None
    ref = ref.strip()

    # Try kebab format: {book}-{pov}-{nn}
    kebab_m = re.match(r"^(agot|acok|asos|affc|adwd|thk|tss|tmk)-(.+)-(\d+)$", ref, re.IGNORECASE)
    if kebab_m:
        book = kebab_m.group(1).lower()
        num = int(kebab_m.group(3))
        order = BOOK_ORDER.get(book)
        if order is not None:
            return (order, num)
        return None

    # Try roman format: {BOOK} {Pov} {ROMAN}
    roman_m = re.match(
        r"^(AGOT|ACOK|ASOS|AFFC|ADWD)\s+(.+?)\s+([IVXLCDM]+)$", ref, re.IGNORECASE
    )
    if roman_m:
        book = roman_m.group(1).upper()
        roman = roman_m.group(3).upper()
        book_order_map = {"AGOT": 1, "ACOK": 2, "ASOS": 3, "AFFC": 4, "ADWD": 5}
        order = book_order_map.get(book)
        num = _ROMAN.get(roman)
        if order is not None and num is not None:
            return (order, num)
        return None

    return None


# ---------------------------------------------------------------------------
# Narrative first computation
# ---------------------------------------------------------------------------

def compute_narrative_first(event_slugs: set[str]) -> dict[str, dict]:
    """For each event slug, find the minimum (book_order, chapter_number) across edges.

    Returns dict: slug -> {
        "candidate": (book_order, chapter_number) or None,
        "raw_ref": str,
        "confidence": "ok" | "mixed_formats" | "no_edges" | "no_normalizable_ref",
        "issues": [str],
    }
    """
    if not EDGES_FILE.exists():
        return {s: {"candidate": None, "raw_ref": None,
                    "confidence": "no_edges", "issues": ["edges.jsonl not found"]}
                for s in event_slugs}

    # Load edges and group by event slug
    slug_refs: dict[str, list[str]] = defaultdict(list)
    for line in EDGES_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        ch = e.get("evidence_chapter")
        src = e.get("source_slug", "")
        tgt = e.get("target_slug", "")
        if src in event_slugs and ch:
            slug_refs[src].append(ch)
        if tgt in event_slugs and ch:
            slug_refs[tgt].append(ch)

    results = {}
    for slug in event_slugs:
        refs = slug_refs.get(slug, [])
        if not refs:
            results[slug] = {
                "candidate": None, "raw_ref": None,
                "confidence": "no_edges", "issues": ["no edges found for this slug"],
            }
            continue

        # Detect format mixing
        kebab_refs = [r for r in refs if re.match(r"^(agot|acok|asos|affc|adwd)", r, re.IGNORECASE)]
        roman_refs = [r for r in refs if re.match(r"^(AGOT|ACOK|ASOS|AFFC|ADWD)\s+", r, re.IGNORECASE)]
        has_mixed = bool(kebab_refs) and bool(roman_refs)
        issues = []
        if has_mixed:
            issues.append(f"mixed formats: {len(kebab_refs)} kebab, {len(roman_refs)} roman-style")

        # Normalize all
        normalized = []
        failed = []
        for r in refs:
            n = normalize_chapter_ref(r)
            if n is not None:
                normalized.append((n, r))
            else:
                failed.append(r)
        if failed:
            issues.append(f"{len(failed)} refs not normalizable: {failed[:3]!r}")

        if not normalized:
            results[slug] = {
                "candidate": None, "raw_ref": None,
                "confidence": "no_normalizable_ref", "issues": issues,
            }
            continue

        # Find minimum
        best_tuple, best_raw = min(normalized, key=lambda x: x[0])
        confidence = "mixed_formats" if has_mixed else "ok"
        results[slug] = {
            "candidate": best_tuple,
            "raw_ref": best_raw,
            "confidence": confidence,
            "issues": issues,
        }

    return results


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_slugs(chronology_file: Path, event_node_dir: Path) -> dict:
    """Load chronology data, classify event slugs, return classification dict."""
    # Build slug -> set of years from chronology
    slug_years: dict[str, set[int]] = defaultdict(set)
    total_event_rows = 0
    for line in chronology_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        if not row.get("target_type", "").startswith("event"):
            continue
        total_event_rows += 1
        slug_years[row["target_slug"]].add(row["year_value"])

    # Build node file map
    node_files = {
        p.stem.replace(".node", ""): p
        for p in event_node_dir.glob("*.node.md")
    }

    clean = {}       # slug -> ac_year
    multiyear = {}   # slug -> sorted list of years
    nomatch = {}     # slug -> sorted list of years
    already_dated = {}  # slug -> ac_year found in file
    blocklisted = []  # slugs hard-excluded

    for slug, years in sorted(slug_years.items()):
        sorted_years = sorted(years)

        if slug in BLOCKLIST:
            blocklisted.append((slug, sorted_years))
            continue

        if slug not in node_files:
            nomatch[slug] = sorted_years
            continue

        node_path = node_files[slug]
        text = node_path.read_text(encoding="utf-8")
        raw_yaml, body, _ = split_frontmatter(text)

        if has_occurred_block(raw_yaml):
            # Extract existing year for reporting
            m = re.search(r"ac_year:\s*(\d+)", raw_yaml)
            yr = int(m.group(1)) if m else None
            already_dated[slug] = yr
            continue

        if len(years) > 1:
            multiyear[slug] = sorted_years
            continue

        # Exactly one year, node exists, not blocklisted, not already dated
        clean[slug] = sorted_years[0]

    return {
        "clean": clean,
        "multiyear": multiyear,
        "nomatch": nomatch,
        "already_dated": already_dated,
        "blocklisted": blocklisted,
        "total_event_rows": total_event_rows,
        "node_files": node_files,
    }


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def render_report(
    result: dict,
    narrative_first: dict,
    mode: str,
    applied_slugs: list[str],
    skipped_slugs: list[str],
    error_slugs: list[tuple[str, str]],
) -> str:
    clean = result["clean"]
    multiyear = result["multiyear"]
    nomatch = result["nomatch"]
    already_dated = result["already_dated"]
    blocklisted = result["blocklisted"]
    total_slugs = len(clean) + len(multiyear) + len(nomatch) + len(already_dated) + len(blocklisted)

    lines = [
        f"# Event Dating Dry-Run Report",
        f"",
        f"Generated: 2026-06-16  |  Mode: {mode}",
        f"",
        f"## Counts",
        f"",
        f"| Category | Count |",
        f"|----------|-------|",
        f"| CLEAN (single-year, node exists, will write) | {len(clean)} |",
        f"| MULTIYEAR (staged, not written) | {len(multiyear)} |",
        f"| NOMATCH (no node file, not written) | {len(nomatch)} |",
        f"| ALREADY_DATED (skipped, idempotent) | {len(already_dated)} |",
        f"| BLOCKLISTED (hard-excluded) | {len(blocklisted)} |",
        f"| **Total event-typed slugs in chronology** | **{total_slugs}** |",
        f"",
    ]

    if mode == "--apply":
        lines += [
            f"## Apply Results",
            f"",
            f"- Written: {len(applied_slugs)}",
            f"- Skipped (already dated): {len(skipped_slugs)}",
            f"- Errors: {len(error_slugs)}",
            f"",
        ]
        if error_slugs:
            lines += ["### Errors", ""]
            for slug, err in error_slugs:
                lines.append(f"- `{slug}`: {err}")
            lines.append("")

    lines += [
        f"## CLEAN — Full Table (slug → ac_year)",
        f"",
        f"These {len(clean)} nodes have exactly one attested year and will be dated.",
        f"",
        f"| slug | ac_year |",
        f"|------|---------|",
    ]
    for slug, yr in sorted(clean.items()):
        lines.append(f"| `{slug}` | {yr} |")

    lines += [
        f"",
        f"## MULTIYEAR — Staged (needs ac_year_end or split decision)",
        f"",
        f"These {len(multiyear)} slugs span multiple attested years. Not written.",
        f"",
        f"| slug | distinct years |",
        f"|------|---------------|",
    ]
    for slug, years in sorted(multiyear.items()):
        lines.append(f"| `{slug}` | {years} |")

    lines += [
        f"",
        f"## NOMATCH — Staged (event year exists, no node file)",
        f"",
        f"These {len(nomatch)} slugs appear in chronology with `target_type: event.*` but have no node file in `graph/nodes/events/`.",
        f"",
    ]
    for slug, years in sorted(nomatch.items()):
        lines.append(f"- `{slug}`: {years}")

    if already_dated:
        lines += [
            f"",
            f"## ALREADY_DATED (idempotent skips)",
            f"",
        ]
        for slug, yr in sorted(already_dated.items()):
            lines.append(f"- `{slug}`: existing ac_year={yr}")

    if blocklisted:
        lines += [
            f"",
            f"## BLOCKLISTED (hard-excluded)",
            f"",
        ]
        for slug, years in blocklisted:
            lines.append(f"- `{slug}`: {years}")

    # Narrative first section
    lines += [
        f"",
        f"## Narrative First — DRY-RUN (compute only, NOT written to nodes)",
        f"",
        f"Candidate `narrative_first` = minimum (book_order, chapter_number) across edges for each CLEAN event.",
        f"",
        f"**Format note:** edges.jsonl contains two chapter-ref formats:",
        f"  - kebab: `agot-arya-01`",
        f"  - roman-style: `ASOS Catelyn VII`",
        f"Normalization is best-effort. Mixed-format nodes are flagged.",
        f"",
        f"| slug | candidate_book_order | candidate_chapter | raw_ref | confidence | issues |",
        f"|------|---------------------|------------------|---------|------------|--------|",
    ]

    for slug in sorted(clean.keys()):
        info = narrative_first.get(slug, {})
        cand = info.get("candidate")
        raw = info.get("raw_ref", "")
        conf = info.get("confidence", "")
        issues = "; ".join(info.get("issues", []))
        if cand:
            book_ord, ch_num = cand
            lines.append(f"| `{slug}` | {book_ord} | {ch_num} | `{raw}` | {conf} | {issues} |")
        else:
            lines.append(f"| `{slug}` | — | — | — | {conf} | {issues} |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Backfill occurred: frontmatter block onto event nodes deterministically."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to node files. Default is dry-run (no writes).",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Generate report without scanning for apply status.",
    )
    args = parser.parse_args()

    mode = "--apply" if args.apply else "--dry-run"
    print(f"date-event-nodes.py | mode={mode}")
    print(f"Chronology: {CHRONOLOGY_FILE}")
    print(f"Event nodes: {EVENT_NODE_DIR}")
    print()

    if not CHRONOLOGY_FILE.exists():
        print(f"ERROR: chronology file not found: {CHRONOLOGY_FILE}", file=sys.stderr)
        sys.exit(1)
    if not EVENT_NODE_DIR.exists():
        print(f"ERROR: event node dir not found: {EVENT_NODE_DIR}", file=sys.stderr)
        sys.exit(1)

    print("Classifying slugs...")
    result = classify_slugs(CHRONOLOGY_FILE, EVENT_NODE_DIR)
    clean = result["clean"]
    multiyear = result["multiyear"]
    nomatch = result["nomatch"]
    already_dated = result["already_dated"]
    blocklisted = result["blocklisted"]
    node_files = result["node_files"]

    print(f"  CLEAN:         {len(clean)}")
    print(f"  MULTIYEAR:     {len(multiyear)}")
    print(f"  NOMATCH:       {len(nomatch)}")
    print(f"  ALREADY_DATED: {len(already_dated)}")
    print(f"  BLOCKLISTED:   {len(blocklisted)}")
    print()

    # Compute narrative_first for CLEAN slugs
    print("Computing narrative_first (dry-run, not written)...")
    narrative_first = compute_narrative_first(set(clean.keys()))
    ok_count = sum(1 for v in narrative_first.values() if v["confidence"] == "ok")
    mixed_count = sum(1 for v in narrative_first.values() if v["confidence"] == "mixed_formats")
    no_edge_count = sum(1 for v in narrative_first.values() if v["confidence"] == "no_edges")
    no_ref_count = sum(1 for v in narrative_first.values() if v["confidence"] == "no_normalizable_ref")
    print(f"  ok: {ok_count}  mixed_formats: {mixed_count}  no_edges: {no_edge_count}  no_normalizable_ref: {no_ref_count}")
    print()

    # Apply phase
    applied_slugs = []
    skipped_slugs = []
    error_slugs = []

    if args.apply:
        print(f"Applying to {len(clean)} CLEAN nodes...")
        for slug, ac_year in sorted(clean.items()):
            node_path = node_files[slug]
            try:
                written, msg = patch_node_file(node_path, ac_year, apply=True)
                if written:
                    applied_slugs.append(slug)
                    print(f"  WROTE  {slug}: ac_year={ac_year}")
                else:
                    skipped_slugs.append(slug)
                    print(f"  SKIP   {slug}: {msg}")
            except Exception as e:
                error_slugs.append((slug, str(e)))
                print(f"  ERROR  {slug}: {e}", file=sys.stderr)
    else:
        print("Dry-run: no node files written.")
        print()

    # Write report
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = render_report(
        result, narrative_first, mode, applied_slugs, skipped_slugs, error_slugs
    )
    REPORT_FILE.write_text(report, encoding="utf-8")
    print(f"Report written: {REPORT_FILE}")
    print()

    # Summary
    total = len(clean) + len(multiyear) + len(nomatch) + len(already_dated) + len(blocklisted)
    print("=== Summary ===")
    print(f"Total event-typed slugs: {total}")
    print(f"  CLEAN (writable):      {len(clean)}")
    print(f"  MULTIYEAR (staged):    {len(multiyear)}")
    print(f"  NOMATCH (staged):      {len(nomatch)}")
    print(f"  ALREADY_DATED (skip):  {len(already_dated)}")
    print(f"  BLOCKLISTED:           {len(blocklisted)}")
    if args.apply:
        print(f"  Applied:               {len(applied_slugs)}")
        print(f"  Errors:                {len(error_slugs)}")
    else:
        print("  (dry-run — pass --apply to write)")

    if error_slugs:
        print(f"\nFailed slugs ({len(error_slugs)}):")
        for s, err in error_slugs:
            print(f"  {s}: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
