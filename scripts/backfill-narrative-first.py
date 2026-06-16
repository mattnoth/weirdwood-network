#!/usr/bin/env python3
"""Backfill `narrative_first` sub-field into the `occurred:` block of dated event nodes.

For each event node that already carries an `occurred:` block (the 112 nodes written
by scripts/date-event-nodes.py), this script computes WHERE IN THE NARRATIVE the reader
first encounters that event — i.e. the minimum absolute chapter position across all
edges that cite this event as source or target.

The result is stored as:
    occurred:
      ...existing fields...
      narrative_first: "asos-52"   # {book}-{absolute_chapter_number}

Design principles:
  - ADDITIVE and FRONTMATTER-ONLY: body is preserved byte-for-byte (hash-checked).
  - IDEMPOTENT: if narrative_first is already present under occurred:, skip + log.
  - RESOLVE-ALL-OR-SKIP: if ANY chapter ref for an event fails to resolve, skip that
    event entirely and log as `unresolved`. Better null than a wrong minimum.
  - Chapter index is built from sources/chapters/<book>/*.md frontmatter — the
    authoritative source for (book, pov_character, pov_chapter_number) -> chapter_number.
  - Both ref formats are supported:
      kebab:  "agot-eddard-01"  -> book=agot, pov_index=1 -> absolute chapter_number
      roman:  "AGOT Eddard I"   -> book=AGOT, pov=Eddard, pov_index=1 -> absolute chapter_number
  - Events with zero chapter-cited edges -> `no_edges`, nothing written.

Usage:
    python3 scripts/backfill-narrative-first.py              # dry-run (default)
    python3 scripts/backfill-narrative-first.py --apply      # write node files
    python3 scripts/backfill-narrative-first.py --dry-run    # explicit dry-run

Output:
    Report -> working/session-results/2026-06-16-narrative-first-dryrun.md
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
CHAPTERS_DIR = ROOT / "sources" / "chapters"
EVENT_NODE_DIR = ROOT / "graph" / "nodes" / "events"
EDGES_FILE = ROOT / "graph" / "edges" / "edges.jsonl"
REPORT_DIR = ROOT / "working" / "session-results"
REPORT_FILE = REPORT_DIR / "2026-06-16-narrative-first-dryrun.md"

# Book ordering for narrative position: agot=1, acok=2, asos=3, affc=4, adwd=5
BOOK_ORDER = {"agot": 1, "acok": 2, "asos": 3, "affc": 4, "adwd": 5}

# Roman numeral -> int mapping
_ROMAN = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8,
    "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15,
    "XVI": 16, "XVII": 17, "XVIII": 18, "XIX": 19, "XX": 20,
    "XXI": 21, "XXII": 22, "XXIII": 23, "XXIV": 24, "XXV": 25,
    "XXVI": 26, "XXVII": 27, "XXVIII": 28, "XXIX": 29, "XXX": 30,
}

# Frontmatter delimiter pattern
_FM_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


# ---------------------------------------------------------------------------
# Chapter index builder (authority: sources/chapters/ frontmatter)
# ---------------------------------------------------------------------------

class ChapterIndex:
    """Index mapping chapter refs to (book_order, absolute_chapter_number).

    Two lookup paths:
      (book_lower, pov_character_prose, pov_chapter_number_int) -> (book_order, chapter_number)
      (book_lower, pov_chapter_number_int) -> set of (book_order, chapter_number)

    For kebab refs "agot-eddard-01": maps (agot, <pov_slug_from_filename>, 1)
      where the file stem encodes the pov slug directly.
    For roman refs "AGOT Eddard I": maps (agot, "Eddard", 1) via pov_character field.
    """

    def __init__(self, chapters_dir: Path):
        # Primary: (book_lower, pov_character_prose_lower, pov_index) -> (book_order, chapter_number)
        self._by_pov_name: dict[tuple[str, str, int], tuple[int, int]] = {}
        # Secondary: (book_lower, file_pov_slug, pov_index) -> (book_order, chapter_number)
        # where file_pov_slug is the middle segment of the filename
        self._by_file_slug: dict[tuple[str, str, int], tuple[int, int]] = {}
        self._available = False
        self._build(chapters_dir)

    def _build(self, chapters_dir: Path) -> None:
        if not chapters_dir.exists():
            return
        count = 0
        for book_lower in BOOK_ORDER:
            book_dir = chapters_dir / book_lower
            if not book_dir.exists():
                continue
            book_ord = BOOK_ORDER[book_lower]
            for f in book_dir.glob("*.md"):
                text = f.read_text(encoding="utf-8")
                m = _FM_RE.match(text)
                if not m:
                    continue
                raw_yaml = m.group(1)
                fm = _parse_simple_yaml(raw_yaml)
                chapter_number = fm.get("chapter_number")
                pov_character = fm.get("pov_character")
                pov_chapter_number = fm.get("pov_chapter_number")
                if chapter_number is None or pov_character is None or pov_chapter_number is None:
                    continue
                try:
                    ch_num = int(chapter_number)
                    pov_idx = int(pov_chapter_number)
                except (ValueError, TypeError):
                    continue

                # By prose POV name (for roman-style refs)
                key_pov = (book_lower, pov_character.strip().lower(), pov_idx)
                self._by_pov_name[key_pov] = (book_ord, ch_num)

                # By file slug (middle segment of filename, for kebab refs)
                # e.g. "asos-catelyn-07.md" -> file_slug="catelyn", pov_idx=7
                stem = f.stem  # "asos-catelyn-07"
                # Strip book prefix and numeric suffix
                # Pattern: {book}-{pov_slug}-{NN}  or {book}-{pov_slug} (prologue/epilogue)
                slug_m = re.match(
                    r"^(?:agot|acok|asos|affc|adwd)-(.+?)(?:-(\d+))?$", stem, re.IGNORECASE
                )
                if slug_m:
                    file_pov_slug = slug_m.group(1).lower()
                    file_idx_str = slug_m.group(2)
                    file_idx = int(file_idx_str) if file_idx_str else 1
                    key_slug = (book_lower, file_pov_slug, file_idx)
                    self._by_file_slug[key_slug] = (book_ord, ch_num)

                count += 1
        self._available = count > 0

    @property
    def available(self) -> bool:
        return self._available

    def lookup_kebab(self, book_lower: str, file_pov_slug: str, pov_idx: int) -> Optional[tuple[int, int]]:
        """Look up a kebab-style ref by file slug components."""
        return self._by_file_slug.get((book_lower, file_pov_slug.lower(), pov_idx))

    def lookup_roman(self, book_lower: str, pov_name_prose: str, pov_idx: int) -> Optional[tuple[int, int]]:
        """Look up a roman-style ref by prose POV name."""
        return self._by_pov_name.get((book_lower, pov_name_prose.strip().lower(), pov_idx))


def _parse_simple_yaml(raw_yaml: str) -> dict:
    """Parse a simple flat YAML block (no lists, no nesting) into a dict.

    Only handles top-level scalar key: value pairs.
    Returns numeric values as strings — caller converts.
    """
    result = {}
    for line in raw_yaml.splitlines():
        # Top-level keys only (no leading space)
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)', line)
        if m:
            key = m.group(1)
            val = m.group(2).strip().strip('"').strip("'")
            result[key] = val
    return result


# ---------------------------------------------------------------------------
# Frontmatter helpers (mirroring date-event-nodes.py)
# ---------------------------------------------------------------------------

def split_frontmatter(text: str) -> tuple[str, str, str]:
    """Return (raw_yaml, body, fm_block_with_delimiters)."""
    m = _FM_RE.match(text)
    if not m:
        raise ValueError("No valid frontmatter block found")
    return m.group(1), text[m.end():], m.group(0)


def body_hash(body: str) -> str:
    return hashlib.sha256(body.encode()).hexdigest()


def has_occurred_block(raw_yaml: str) -> bool:
    for line in raw_yaml.splitlines():
        if re.match(r"^occurred\s*:", line):
            return True
    return False


def has_narrative_first_in_occurred(raw_yaml: str) -> bool:
    """Check if narrative_first sub-field already exists under occurred:."""
    in_occurred = False
    for line in raw_yaml.splitlines():
        if re.match(r"^occurred\s*:", line):
            in_occurred = True
            continue
        if in_occurred:
            # sub-field under occurred: (has leading spaces)
            if re.match(r"^\s+narrative_first\s*:", line):
                return True
            # Hit next top-level key — end of occurred block
            if line and not line[0].isspace():
                break
    return False


# ---------------------------------------------------------------------------
# Chapter ref normalization (using chapter index as authority)
# ---------------------------------------------------------------------------

def normalize_chapter_ref(ref: str, index: ChapterIndex) -> Optional[tuple[int, int]]:
    """Normalize a chapter ref string to (book_order, absolute_chapter_number).

    Handles two formats:
      kebab:  "agot-arya-01"            -> (1, 4)   [absolute AGOT chapter 4]
      roman:  "ASOS Catelyn VII"        -> (3, 52)  [absolute ASOS chapter 52]
      roman:  "ADWD The Prince of Winterfell I" -> (5, 38)

    Returns None if the ref cannot be resolved.
    """
    if not ref:
        return None
    ref = ref.strip()

    # --- Kebab format: {book}-{pov_slug}-{NN} ---
    kebab_m = re.match(
        r"^(agot|acok|asos|affc|adwd)-(.*?)-(\d+)$", ref, re.IGNORECASE
    )
    if kebab_m:
        book_lower = kebab_m.group(1).lower()
        file_pov_slug = kebab_m.group(2).lower()
        pov_idx = int(kebab_m.group(3))
        if index.available:
            result = index.lookup_kebab(book_lower, file_pov_slug, pov_idx)
            if result is not None:
                return result
        # Fallback: use pov_idx as chapter_number proxy (less accurate, logs warn)
        book_ord = BOOK_ORDER.get(book_lower)
        if book_ord is not None:
            return None  # Don't guess; treat as unresolvable without index
        return None

    # --- Roman format: {BOOK} {Pov Name} {ROMAN} ---
    # The pov name can be multi-word (e.g. "The Prince of Winterfell")
    # Roman numeral must be the final token.
    roman_m = re.match(
        r"^(AGOT|ACOK|ASOS|AFFC|ADWD)\s+(.+?)\s+([IVXLCDM]+)$", ref, re.IGNORECASE
    )
    if roman_m:
        book_upper = roman_m.group(1).upper()
        pov_name = roman_m.group(2)
        roman_str = roman_m.group(3).upper()
        book_lower = book_upper.lower()
        pov_idx = _ROMAN.get(roman_str)
        if pov_idx is None:
            return None  # Unknown roman numeral
        if index.available:
            result = index.lookup_roman(book_lower, pov_name, pov_idx)
            if result is not None:
                return result
        # If index not available, we cannot resolve roman refs accurately
        return None

    return None


# ---------------------------------------------------------------------------
# Per-event narrative_first computation
# ---------------------------------------------------------------------------

class RefResult:
    """Classification of a single event's chapter refs."""
    def __init__(self, status: str, value: Optional[tuple[int, int]] = None,
                 human_ref: str = "", unresolved_refs: Optional[list[str]] = None):
        self.status = status          # "will_write" | "no_edges" | "unresolved" | "already_set"
        self.value = value            # (book_order, chapter_number) or None
        self.human_ref = human_ref    # The raw ref string that produced the minimum
        self.unresolved_refs = unresolved_refs or []

    @property
    def narrative_first_str(self) -> Optional[str]:
        """Format value as "{book}-{chapter_number}" string."""
        if self.value is None:
            return None
        book_ord, ch_num = self.value
        # Reverse-map book_order to name
        book_name = {v: k for k, v in BOOK_ORDER.items()}.get(book_ord, "unknown")
        return f"{book_name}-{ch_num}"


def compute_narrative_first_for_events(
    event_slugs: set[str],
    index: ChapterIndex,
    edges_file: Optional[Path] = None,
) -> dict[str, RefResult]:
    """For each dated event slug, compute narrative_first from edges.jsonl.

    Args:
        event_slugs: Set of event node slugs to process.
        index: ChapterIndex built from sources/chapters/ frontmatter.
        edges_file: Path to edges.jsonl. Defaults to EDGES_FILE constant.
                    Passed explicitly in tests to avoid reading real graph data.

    Returns dict: slug -> RefResult
    """
    ef = edges_file if edges_file is not None else EDGES_FILE
    if not ef.exists():
        return {
            s: RefResult("no_edges", unresolved_refs=["edges.jsonl not found"])
            for s in event_slugs
        }

    # Collect chapter refs per event slug
    slug_refs: dict[str, list[str]] = defaultdict(list)
    with ef.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                edge = json.loads(line)
            except json.JSONDecodeError:
                continue
            ch = edge.get("evidence_chapter") or ""
            if not ch:
                continue
            src = edge.get("source_slug", "")
            tgt = edge.get("target_slug", "")
            if src in event_slugs:
                slug_refs[src].append(ch)
            if tgt in event_slugs:
                slug_refs[tgt].append(ch)

    results: dict[str, RefResult] = {}
    for slug in event_slugs:
        refs = slug_refs.get(slug, [])

        if not refs:
            results[slug] = RefResult("no_edges")
            continue

        # RESOLVE-ALL-OR-SKIP: attempt to resolve every ref
        resolved: list[tuple[tuple[int, int], str]] = []  # ((book_ord, ch_num), raw_ref)
        unresolved: list[str] = []

        for raw_ref in refs:
            normalized = normalize_chapter_ref(raw_ref, index)
            if normalized is not None:
                resolved.append((normalized, raw_ref))
            else:
                unresolved.append(raw_ref)

        if unresolved:
            # Safety rule: any unresolved ref -> skip this event
            results[slug] = RefResult("unresolved", unresolved_refs=unresolved)
            continue

        if not resolved:
            results[slug] = RefResult("no_edges")
            continue

        # Find minimum (book_order, chapter_number)
        best_tuple, best_raw = min(resolved, key=lambda x: x[0])
        results[slug] = RefResult("will_write", value=best_tuple, human_ref=best_raw)

    return results


# ---------------------------------------------------------------------------
# Frontmatter patcher: insert narrative_first under occurred: block
# ---------------------------------------------------------------------------

def insert_narrative_first_into_yaml(raw_yaml: str, value_str: str) -> str:
    """Insert `  narrative_first: "<value>"` at the end of the occurred: block.

    Finds the occurred: key and appends the sub-field after the last
    existing sub-field within that block (before the next top-level key or EOF).

    Returns the modified raw_yaml string.
    Raises ValueError if occurred: block not found.
    """
    lines = raw_yaml.splitlines()
    occurred_end_idx = None  # index of last line in the occurred: block

    in_occurred = False
    for i, line in enumerate(lines):
        if re.match(r"^occurred\s*:", line):
            in_occurred = True
            occurred_end_idx = i
            continue
        if in_occurred:
            if line == "" or line[0].isspace():
                # Still in occurred block (empty lines within block, or indented sub-fields)
                if line.strip():  # non-empty indented line
                    occurred_end_idx = i
                # empty line might be trailing — keep tracking
            else:
                # Hit the next top-level key
                break

    if occurred_end_idx is None:
        raise ValueError("occurred: block not found in frontmatter")

    # Insert new sub-field after occurred_end_idx
    new_line = f'  narrative_first: "{value_str}"'
    new_lines = lines[:occurred_end_idx + 1] + [new_line] + lines[occurred_end_idx + 1:]
    return "\n".join(new_lines)


def patch_node_file_narrative_first(
    path: Path,
    value_str: str,
    apply: bool,
) -> tuple[bool, str]:
    """Patch a node file to add narrative_first sub-field under occurred:.

    Returns (was_written, message).
    Re-reads file fresh from disk. Checks body hash before/after.
    """
    # Re-read fresh from disk
    text = path.read_text(encoding="utf-8")
    raw_yaml, body, _ = split_frontmatter(text)

    # Idempotency check
    if has_narrative_first_in_occurred(raw_yaml):
        return False, "already has narrative_first"

    if not has_occurred_block(raw_yaml):
        return False, "no occurred: block found"

    before_hash = body_hash(body)

    # Build new frontmatter
    new_yaml = insert_narrative_first_into_yaml(raw_yaml, value_str)
    new_text = "---\n" + new_yaml + "\n---\n" + body

    # Verify body preserved byte-for-byte
    _, new_body, _ = split_frontmatter(new_text)
    after_hash = body_hash(new_body)
    if before_hash != after_hash:
        raise RuntimeError(
            f"Body hash mismatch for {path.name}: {before_hash[:8]} -> {after_hash[:8]}"
        )

    if apply:
        path.write_text(new_text, encoding="utf-8")
        return True, f"wrote narrative_first={value_str!r}"
    else:
        return False, f"dry-run: would write narrative_first={value_str!r}"


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def render_report(
    results: dict[str, RefResult],
    mode: str,
    applied: list[str],
    skipped_idempotent: list[str],
    errors: list[tuple[str, str]],
) -> str:
    will_write = {s: r for s, r in results.items() if r.status == "will_write"}
    no_edges = {s: r for s, r in results.items() if r.status == "no_edges"}
    unresolved = {s: r for s, r in results.items() if r.status == "unresolved"}
    already_set = {s: r for s, r in results.items() if r.status == "already_set"}
    total = len(results)

    lines = [
        "# Narrative First Backfill Report",
        "",
        f"Generated: 2026-06-16  |  Mode: {mode}",
        "",
        "## Counts",
        "",
        "| Category | Count |",
        "|----------|-------|",
        f"| will_write (has edges, all refs resolved, narrative_first absent) | {len(will_write)} |",
        f"| no_edges (zero chapter-cited edges) | {len(no_edges)} |",
        f"| unresolved (one or more refs failed to resolve) | {len(unresolved)} |",
        f"| already_set (idempotent skip) | {len(already_set)} |",
        f"| **Total dated events examined** | **{total}** |",
        "",
    ]

    if mode == "--apply":
        lines += [
            "## Apply Results",
            "",
            f"- Written: {len(applied)}",
            f"- Skipped (already set): {len(skipped_idempotent)}",
            f"- Errors: {len(errors)}",
            "",
        ]
        if errors:
            lines += ["### Errors", ""]
            for slug, err in errors:
                lines.append(f"- `{slug}`: {err}")
            lines.append("")

    # Will-write table
    lines += [
        "## Will-Write Table (slug → narrative_first → min human ref)",
        "",
        f"These {len(will_write)} events will receive `narrative_first` under their `occurred:` block.",
        "",
        "| slug | narrative_first | min human ref | (book_order, chapter_number) |",
        "|------|----------------|---------------|------------------------------|",
    ]
    for slug in sorted(will_write):
        r = will_write[slug]
        nf = r.narrative_first_str or "—"
        hr = r.human_ref or "—"
        val = str(r.value) if r.value else "—"
        lines.append(f"| `{slug}` | `{nf}` | `{hr}` | {val} |")

    # Unresolved list
    lines += [
        "",
        "## Unresolved (skipped — one or more refs failed to resolve)",
        "",
        f"These {len(unresolved)} events have chapter-cited edges but at least one ref could not be"
        " resolved to an absolute chapter number. Nothing written.",
        "",
    ]
    if unresolved:
        lines += [
            "| slug | failing refs |",
            "|------|-------------|",
        ]
        for slug in sorted(unresolved):
            r = unresolved[slug]
            failing = ", ".join(f"`{x}`" for x in r.unresolved_refs[:5])
            lines.append(f"| `{slug}` | {failing} |")
    else:
        lines.append("*(none)*")

    # No-edges section (brief)
    lines += [
        "",
        f"## No-Edges ({len(no_edges)} events — pure backstory, no chapter citations)",
        "",
        "These events have `occurred:` but no chapter-cited edges. No `narrative_first` written.",
        "",
    ]
    for slug in sorted(no_edges):
        lines.append(f"- `{slug}`")

    # Already-set section
    if already_set:
        lines += [
            "",
            f"## Already Set ({len(already_set)} — idempotent skips)",
            "",
        ]
        for slug in sorted(already_set):
            lines.append(f"- `{slug}`")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backfill narrative_first into occurred: blocks of dated event nodes."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to node files. Default is dry-run.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Dry-run (default). No node files written.",
    )
    args = parser.parse_args()
    apply = args.apply
    mode = "--apply" if apply else "--dry-run"

    print(f"backfill-narrative-first.py | mode={mode}")
    print(f"Event nodes: {EVENT_NODE_DIR}")
    print(f"Edges:       {EDGES_FILE}")
    print(f"Chapters:    {CHAPTERS_DIR}")
    print()

    # --- Build chapter index ---
    print("Building chapter index from sources/chapters/...")
    index = ChapterIndex(CHAPTERS_DIR)
    if not index.available:
        print("WARNING: Chapter index unavailable — falling back to pov_index (less accurate).")
        print("  Check that sources/chapters/ exists and contains .md files.")
    else:
        by_pov = len(index._by_pov_name)
        by_slug = len(index._by_file_slug)
        print(f"  Index built: {by_pov} POV-name entries, {by_slug} file-slug entries")
    print()

    # --- Find all dated event nodes ---
    if not EVENT_NODE_DIR.exists():
        print(f"ERROR: Event node dir not found: {EVENT_NODE_DIR}", file=sys.stderr)
        sys.exit(1)

    dated_slugs: set[str] = set()
    already_set_slugs: set[str] = set()
    node_paths: dict[str, Path] = {}

    for f in sorted(EVENT_NODE_DIR.glob("*.node.md")):
        slug = f.stem.replace(".node", "")
        text = f.read_text(encoding="utf-8")
        if not has_occurred_block(text):
            continue
        node_paths[slug] = f
        if has_narrative_first_in_occurred(text.split("---\n", 2)[1] if "---\n" in text else text):
            already_set_slugs.add(slug)
        else:
            dated_slugs.add(slug)

    print(f"Dated event nodes found:    {len(dated_slugs) + len(already_set_slugs)}")
    print(f"  Already have narrative_first: {len(already_set_slugs)} (idempotent skip)")
    print(f"  Need processing:              {len(dated_slugs)}")
    print()

    # --- Compute narrative_first ---
    print(f"Computing narrative_first for {len(dated_slugs)} events...")
    results = compute_narrative_first_for_events(dated_slugs, index)

    # Add already_set to results
    for slug in already_set_slugs:
        results[slug] = RefResult("already_set")

    will_write_count = sum(1 for r in results.values() if r.status == "will_write")
    no_edges_count = sum(1 for r in results.values() if r.status == "no_edges")
    unresolved_count = sum(1 for r in results.values() if r.status == "unresolved")

    print(f"  will_write:   {will_write_count}")
    print(f"  no_edges:     {no_edges_count}")
    print(f"  unresolved:   {unresolved_count}")
    print(f"  already_set:  {len(already_set_slugs)}")
    print()

    # --- Apply phase ---
    applied: list[str] = []
    skipped_idempotent: list[str] = []
    errors: list[tuple[str, str]] = []

    if apply:
        print(f"Applying to {will_write_count} events...")
        for slug, result in sorted(results.items()):
            if result.status != "will_write":
                continue
            path = node_paths[slug]
            value_str = result.narrative_first_str
            try:
                written, msg = patch_node_file_narrative_first(path, value_str, apply=True)
                if written:
                    applied.append(slug)
                    print(f"  WROTE  {slug}: {value_str}")
                else:
                    skipped_idempotent.append(slug)
                    print(f"  SKIP   {slug}: {msg}")
            except Exception as e:
                errors.append((slug, str(e)))
                print(f"  ERROR  {slug}: {e}", file=sys.stderr)
    else:
        print("Dry-run: no node files written.")
        print()

    # --- Write report ---
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_text = render_report(results, mode, applied, skipped_idempotent, errors)
    REPORT_FILE.write_text(report_text, encoding="utf-8")
    print(f"Report written: {REPORT_FILE}")
    print()

    # --- Summary ---
    print("=== Summary ===")
    print(f"Total dated events examined: {len(results)}")
    print(f"  will_write:   {will_write_count}")
    print(f"  no_edges:     {no_edges_count}")
    print(f"  unresolved:   {unresolved_count}")
    print(f"  already_set:  {len(already_set_slugs)}")
    if apply:
        print(f"  Applied:      {len(applied)}")
        print(f"  Errors:       {len(errors)}")
    else:
        print("  (dry-run — pass --apply to write)")

    if errors:
        print(f"\nFailed slugs ({len(errors)}):")
        for s, err in errors:
            print(f"  {s}: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
