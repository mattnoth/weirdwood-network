#!/usr/bin/env python3
"""stage4-pass1-edge-candidates.py — Stage 4 Pass-1-Derived Edge Pipeline: Script 1.

Walks all 344 Pass 1 extraction files under extractions/mechanical/{book}/.
For every row in each chapter's "## Relationships Observed" table:

  1. Parses char_a (source), relationship (hint), char_b (target), evidence text,
     plus chapter_id, book, and POV slug.
  2. Slugifies + alias-resolves source and target via a five-rung collision-aware
     resolver (stage4_name_resolver.py):
       a. exact slug match
       b. alias lookup (alias-resolver.json)
       c. firstname-unique: first token maps to exactly one graph node
       d. context-present: multiple candidates, one is in chapter's present_slugs
       e. context-prior: dominant by backlink count (≥ 3× runner-up)
       f. ambiguous-queued → review file (no edge emitted)
       g. unresolved → needs-node tally
  3. RESOLUTION gate: both endpoints must resolve (rungs a–e). Ambiguous endpoints
     go to pass1-derived-ambiguous-review.md. Unresolved go to needs-node tally.
  4. TYPER: maps hint → locked-vocab edge type using the three-layer deterministic
     map from stage4-pass1-hint-inventory.py (exact → prefix → keyword).
     typed_by = "python-map" when non-None, else null.
  5. CORROBORATION: checks existing-edges index for (source→target) or
     (target→source). Sets corroborates_known_edge=True + wiki_edge_type when found.
  6. CONFORM step: asserts every non-null edge_type is in the locked vocab from
     architecture.md. Drift bugs → conform report + stderr, not crash.
  7. QUALIFIER routing: Tier-1 edge types (qualifier REQUIRED) without a qualifier
     are routed to a separate needs-qualifier tail instead of the main output.

Outputs (--apply mode):
  - Per-chapter candidate JSONL:
      working/wiki/pass2-buckets/pass1-derived/{book}/{chapter}.candidates.jsonl
  - Needs-node report:
      working/wiki/data/pass1-derived-needs-node.md
  - Ambiguous-review report:
      working/wiki/data/pass1-derived-ambiguous-review.md
  - Supplementary firstname-alias map:
      working/wiki/data/pass1-derived-firstname-aliases.json
  - Conform report:
      working/wiki/data/pass1-derived-conform-report.md
  - Summary markdown + JSON:
      working/wiki/data/pass1-derived-candidates-summary.md
      working/wiki/data/pass1-derived-candidates-stats.json
  - Per-chapter needs-qualifier tail JSONL:
      working/wiki/pass2-buckets/pass1-derived/_needs-qualifier/{book}/{chapter}.needs-qualifier.jsonl

Usage:
  python3 scripts/stage4-pass1-edge-candidates.py --plan
      Compute all stats, print to stdout. Write NOTHING.
  python3 scripts/stage4-pass1-edge-candidates.py --apply
      Same as --plan, plus write all output files.
  python3 scripts/stage4-pass1-edge-candidates.py --plan --book acok
      Restrict to one book (smoke test).
  python3 scripts/stage4-pass1-edge-candidates.py --plan --chapter-slug acok-arya-01
      Restrict to one chapter (debugging).

No LLM calls. No network. Deterministic.
"""

import argparse
import collections
import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# stage4_name_resolver is in scripts/ with underscore name — importable directly
_RESOLVER_PATH = Path(__file__).parent / "stage4_name_resolver.py"
_resolver_spec = importlib.util.spec_from_file_location("stage4_name_resolver", _RESOLVER_PATH)
_resolver_mod = importlib.util.module_from_spec(_resolver_spec)
sys.modules["stage4_name_resolver"] = _resolver_mod
_resolver_spec.loader.exec_module(_resolver_mod)

from stage4_name_resolver import (  # noqa: E402 (after dynamic load)
    build_firstname_index,
    load_importance_prior,
    load_node_display_names,
    resolve_name,
    resolve_name_bootstrap,
    write_firstname_aliases,
    GENERIC_TERMS,
    STATUS_EXACT,
    STATUS_ALIAS,
    STATUS_FIRSTNAME_UNIQUE,
    STATUS_CONTEXT_PRESENT,
    STATUS_CONTEXT_PRIOR,
    STATUS_AMBIGUOUS,
    STATUS_UNRESOLVED,
    STATUS_UNRESOLVED_GENERIC,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
GRAPH_NODES_DIR = REPO_ROOT / "graph" / "nodes"
EXTRACTIONS_DIR = REPO_ROOT / "extractions" / "mechanical"
WIKI_DATA_DIR = REPO_ROOT / "working" / "wiki" / "data"
PASS2_BUCKETS_DIR = REPO_ROOT / "working" / "wiki" / "pass2-buckets"
CHAPTERS_DIR = REPO_ROOT / "sources" / "chapters"

IN_ALIAS = WIKI_DATA_DIR / "alias-resolver.json"
IN_BACKLINKS = WIKI_DATA_DIR / "backlink-counts.json"
ARCH_MD = REPO_ROOT / "reference" / "architecture.md"
QUAL_VOCAB_MD = REPO_ROOT / "reference" / "edge-qualifier-vocab.md"

OUT_BASE_DIR = PASS2_BUCKETS_DIR / "pass1-derived"
OUT_NEEDS_QUAL_DIR = OUT_BASE_DIR / "_needs-qualifier"
OUT_NEEDS_NODE_MD = WIKI_DATA_DIR / "pass1-derived-needs-node.md"
OUT_AMBIGUOUS_MD = WIKI_DATA_DIR / "pass1-derived-ambiguous-review.md"
OUT_FIRSTNAME_ALIASES_JSON = WIKI_DATA_DIR / "pass1-derived-firstname-aliases.json"
OUT_CONFORM_MD = WIKI_DATA_DIR / "pass1-derived-conform-report.md"
OUT_SUMMARY_MD = WIKI_DATA_DIR / "pass1-derived-candidates-summary.md"
OUT_SUMMARY_JSON = WIKI_DATA_DIR / "pass1-derived-candidates-stats.json"

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]

# Skip these graph subdirectories (special/conflict folders)
_SKIP_DIRS = {"_conflicts", "_unclassified", "_stage3-preview"}


# ---------------------------------------------------------------------------
# Load the typer from stage4-pass1-hint-inventory.py via importlib
# (filename has hyphens → can't use regular import)
# ---------------------------------------------------------------------------
def _load_typer_module():
    """Load stage4-pass1-hint-inventory.py and return the module."""
    path = Path(__file__).parent / "stage4-pass1-hint-inventory.py"
    if not path.exists():
        print(f"ERROR: typer module not found at {path}", file=sys.stderr)
        sys.exit(1)
    mod_name = "stage4_pass1_hint_inventory"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


_typer = _load_typer_module()
normalize_hint = _typer.normalize_hint
map_hint_to_edge = _typer.map_hint_to_edge


# ---------------------------------------------------------------------------
# Locked edge vocabulary from architecture.md
# ---------------------------------------------------------------------------
def load_locked_vocab(arch_path: Path) -> frozenset[str]:
    """Extract all backtick-quoted ALL_CAPS_UNDERSCORE tokens from architecture.md.

    These are the canonical locked edge types. Used for CONFORM checking.
    """
    text = arch_path.read_text(encoding="utf-8", errors="replace")
    # Match tokens like `KILLS`, `PARENT_OF`, etc. — all-caps + underscores, len >= 2
    tokens = re.findall(r"`([A-Z][A-Z_]{1,})`", text)
    # Filter out obvious non-edge-type tokens (single-letter, or known non-edge acronyms)
    vocab = frozenset(
        t for t in tokens
        if len(t) >= 2 and not t.startswith("AGOT") and not t.startswith("ACOK")
        and not t.startswith("ASOS") and not t.startswith("AFFC") and not t.startswith("ADWD")
        and t not in ("POV", "ADWD")
    )
    return vocab


# ---------------------------------------------------------------------------
# Tier-1 edge types (qualifier REQUIRED) — from edge-qualifier-vocab.md
# ---------------------------------------------------------------------------
def load_tier1_edge_types(qual_vocab_path: Path) -> frozenset[str]:
    """Parse reference/edge-qualifier-vocab.md and return the set of Tier-1 edge types.

    Tier-1 section starts with '## Tier 1 — REQUIRED qualifier'.
    Parses table rows like: | `SIBLING_OF` | ... until the next ## heading.
    """
    try:
        text = qual_vocab_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"WARNING: Cannot read qualifier vocab {qual_vocab_path}: {exc}", file=sys.stderr)
        return frozenset()

    tier1_types: set[str] = set()
    in_tier1 = False

    for line in text.splitlines():
        if line.startswith("## Tier 1"):
            in_tier1 = True
            continue
        if in_tier1 and line.startswith("## "):
            in_tier1 = False
            continue
        if not in_tier1:
            continue
        # Table rows like: | `SIBLING_OF` | ...
        m = re.search(r"`([A-Z][A-Z_]+)`", line)
        if m:
            tier1_types.add(m.group(1))

    return frozenset(tier1_types)


# ---------------------------------------------------------------------------
# Slugify — copied verbatim from wiki-pass2-build-pass1-relationship-candidates.py
# ---------------------------------------------------------------------------
def to_slug(raw: str) -> str:
    """Convert a display name to a kebab-case slug.

    Must match the canonical convention:
    - Lowercase
    - Strip apostrophes, quotes, commas
    - Replace spaces/underscores with hyphens
    - Replace remaining non-alphanumeric chars with hyphens
    - Collapse consecutive hyphens, strip leading/trailing hyphens
    """
    s = raw.lower()
    s = re.sub(r"['\",]", "", s)           # strip possessives/quotes/commas
    s = re.sub(r"[ _]+", "-", s)           # spaces and underscores → hyphens
    s = re.sub(r"[^a-z0-9-]", "-", s)     # anything else → hyphen
    s = re.sub(r"-+", "-", s).strip("-")
    return s


# ---------------------------------------------------------------------------
# Extraction file metadata parser — copied from old script
# ---------------------------------------------------------------------------
_METADATA_KEY_RE = re.compile(r"^\s*-\s+\*\*([^*]+)\*\*:\s*(.+)$")
_HEADING_RE = re.compile(r"^##\s+(.+)$")


def parse_extraction_metadata(text: str) -> dict:
    """Parse the ## Chapter Metadata section from an extraction file body."""
    meta: dict = {}
    in_metadata = False

    for line in text.splitlines():
        h2_match = _HEADING_RE.match(line)
        if h2_match:
            section_name = h2_match.group(1).strip()
            in_metadata = section_name.lower() == "chapter metadata"
            continue
        if not in_metadata:
            continue
        m = _METADATA_KEY_RE.match(line)
        if m:
            key = m.group(1).strip().lower().replace(" ", "_")
            val = m.group(2).strip()
            if key and key not in meta:
                meta[key] = val

    return meta


def derive_chapter_slug(extraction_path: Path) -> str:
    """Derive chapter slug from the extraction filename."""
    return extraction_path.name[: -len(".extraction.md")]


def derive_pov_slug(pov_character: str) -> str:
    """Slugify the pov_character value from metadata."""
    return to_slug(pov_character)


# ---------------------------------------------------------------------------
# Relationships Observed table parser — copied from old script (proven)
# ---------------------------------------------------------------------------
_RELATIONSHIP_HEADING_RE = re.compile(r"^##\s+.*relationship", re.IGNORECASE)
_TABLE_ROW_RE = re.compile(r"^\|(.+)\|$")


def _split_table_row(line: str) -> list[str]:
    inner = line.strip().strip("|")
    cells = [c.strip() for c in inner.split("|")]
    return cells


def _is_separator_row(cells: list[str]) -> bool:
    return all(re.match(r"^[-: ]+$", c) for c in cells if c)


def parse_relationships_table(text: str) -> list[dict]:
    """Parse the ## Relationships Observed table from an extraction file.

    Returns a list of dicts with keys: char_a, relationship, char_b, evidence.
    """
    in_relationships_section = False
    header_cols: list[str] = []
    col_index_char_a = -1
    col_index_relationship = -1
    col_index_char_b = -1
    col_index_evidence = -1
    rows: list[dict] = []

    for line in text.splitlines():
        h2_match = _HEADING_RE.match(line)
        if h2_match:
            section_label = h2_match.group(1).strip()
            if re.search(r"relationship", section_label, re.IGNORECASE):
                in_relationships_section = True
                header_cols = []
                col_index_char_a = col_index_relationship = col_index_char_b = col_index_evidence = -1
            else:
                in_relationships_section = False
            continue

        if not in_relationships_section:
            continue
        if not _TABLE_ROW_RE.match(line.strip()):
            continue

        cells = _split_table_row(line)
        if not cells:
            continue
        if _is_separator_row(cells):
            continue

        # Header row detection
        if not header_cols:
            header_cols = [c.lower() for c in cells]
            for i, h in enumerate(header_cols):
                if h in ("character a", "from"):
                    col_index_char_a = i
                elif h in ("character b", "to"):
                    col_index_char_b = i
                elif "relationship" in h:
                    col_index_relationship = i
                elif "evidence" in h:
                    col_index_evidence = i
            if col_index_char_a < 0 or col_index_relationship < 0 or col_index_char_b < 0:
                print(
                    f"  WARNING: Unrecognized Relationships Observed header: {cells}",
                    file=sys.stderr,
                )
                in_relationships_section = False
            continue

        def safe_get(idx: int) -> str:
            if idx < 0 or idx >= len(cells):
                return ""
            return cells[idx].strip()

        char_a = safe_get(col_index_char_a)
        relationship = safe_get(col_index_relationship)
        char_b = safe_get(col_index_char_b)
        evidence = safe_get(col_index_evidence)

        if not char_a or not char_b or not relationship:
            continue

        rows.append({
            "char_a": char_a,
            "relationship": relationship,
            "char_b": char_b,
            "evidence": evidence,
        })

    return rows


# ---------------------------------------------------------------------------
# Characters Present table parser
# ---------------------------------------------------------------------------
_CP_HEADING_RE = re.compile(r"^##\s+Characters\s+Present", re.IGNORECASE)


def parse_characters_present(text: str) -> list[str]:
    """Parse the ## Characters Present table to extract character name strings.

    Returns the raw string in the first column (Character / Name) for each
    data row. Callers are responsible for resolving these names to slugs.
    """
    in_section = False
    header_cols: list[str] = []
    col_idx: int = -1
    names: list[str] = []

    for line in text.splitlines():
        h2_match = _HEADING_RE.match(line)
        if h2_match:
            section_label = h2_match.group(1).strip()
            if re.search(r"characters\s+present", section_label, re.IGNORECASE):
                in_section = True
                header_cols = []
                col_idx = -1
            else:
                in_section = False
            continue

        if not in_section:
            continue
        if not _TABLE_ROW_RE.match(line.strip()):
            continue

        inner = line.strip().strip("|")
        cells = [c.strip() for c in inner.split("|")]
        if not cells:
            continue
        if _is_separator_row(cells):
            continue

        if not header_cols:
            header_cols = [c.lower() for c in cells]
            for i, h in enumerate(header_cols):
                if h in ("character", "character name", "name"):
                    col_idx = i
            continue

        if col_idx >= 0 and col_idx < len(cells):
            name = cells[col_idx].strip()
            if name:
                names.append(name)

    return names


# ---------------------------------------------------------------------------
# Existing-edges parser — extended from old script to also capture edge_type
# ---------------------------------------------------------------------------
_EDGE_LINE_RE = re.compile(r"^- ([A-Z_]+)(?: \([^)]+\))?:\s+(.+)$")


def parse_existing_edges_with_types(node_path: Path) -> dict[str, str]:
    """Parse ## Edges sections from a node file.

    Returns dict of {target_slug: edge_type} for every edge listed.
    If multiple edges to the same target, the last one wins (rare edge case).
    """
    try:
        text = node_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}

    result: dict[str, str] = {}
    in_edges_section = False

    for line in text.splitlines():
        if line.startswith("## Edges"):
            in_edges_section = True
            continue
        if line.startswith("## ") and not line.startswith("## Edges"):
            in_edges_section = False
            continue
        if not in_edges_section:
            continue

        m = _EDGE_LINE_RE.match(line.strip())
        if not m:
            continue

        edge_type = m.group(1)
        rest = m.group(2).strip()

        # Extract target: everything before first ( or [
        paren = rest.find("(")
        bracket = rest.find("[")
        delimiters = [p for p in (paren, bracket) if p != -1]
        if delimiters:
            end = min(delimiters)
            target_raw = rest[:end].strip()
        else:
            target_raw = rest.strip()

        if target_raw:
            result[to_slug(target_raw)] = edge_type

    return result


# ---------------------------------------------------------------------------
# Graph index builder
# ---------------------------------------------------------------------------
def build_graph_index() -> tuple[set[str], dict[str, dict[str, str]]]:
    """Walk graph/nodes/**/*.node.md and return:
      - node_slug_set: set of all canonical slugs
      - existing_edges: {slug: {target_slug: edge_type}}
    """
    node_slug_set: set[str] = set()
    existing_edges_raw: dict[str, dict[str, str]] = {}

    for node_file in sorted(GRAPH_NODES_DIR.rglob("*.node.md")):
        parts = node_file.relative_to(GRAPH_NODES_DIR).parts
        if any(p in _SKIP_DIRS for p in parts):
            continue

        slug = node_file.name[: -len(".node.md")]
        if not slug:
            continue

        node_slug_set.add(slug)
        existing_edges_raw[slug] = parse_existing_edges_with_types(node_file)

    return node_slug_set, existing_edges_raw


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Stage 4 Pass-1-Derived Edge Pipeline — Script 1: candidate generator.\n"
            "Walks all Pass 1 extraction Relationships Observed tables → emits typed, "
            "citation-bearing graph edge candidates at ZERO LLM cost."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--plan",
        action="store_true",
        default=True,
        help="Dry-run: compute stats, print to stdout. Write NOTHING (default).",
    )
    mode_group.add_argument(
        "--apply",
        action="store_true",
        help="Compute + write all output files.",
    )
    parser.add_argument(
        "--book",
        choices=BOOKS,
        default=None,
        metavar="BOOK",
        help="Restrict to one book (agot|acok|asos|affc|adwd).",
    )
    parser.add_argument(
        "--chapter-slug",
        default=None,
        metavar="SLUG",
        help="Restrict to one chapter slug (e.g. acok-arya-01).",
    )
    args = parser.parse_args()
    write_output = args.apply

    run_date = datetime.now(timezone.utc).strftime("%Y%m%d")
    run_id = f"pass1-derived-{run_date}"
    schema_version = "pass1-derived-v1"
    produced_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # -----------------------------------------------------------------------
    # Step 0: Load locked vocab + qualifier tiers
    # -----------------------------------------------------------------------
    print("Loading locked edge vocabulary from architecture.md...")
    locked_vocab = load_locked_vocab(ARCH_MD)
    print(f"  {len(locked_vocab):,} locked edge types")

    print("Loading qualifier tiers from edge-qualifier-vocab.md...")
    tier1_types = load_tier1_edge_types(QUAL_VOCAB_MD)
    print(f"  {len(tier1_types):,} Tier-1 (qualifier-required) types: {sorted(tier1_types)}")

    # -----------------------------------------------------------------------
    # Step 1: Load alias resolver
    # -----------------------------------------------------------------------
    print("Loading alias resolver...")
    try:
        alias_data = json.loads(IN_ALIAS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: Cannot load {IN_ALIAS}: {exc}", file=sys.stderr)
        sys.exit(1)
    alias_to_canonical: dict[str, str] = alias_data.get("alias_to_canonical", {})
    print(f"  {len(alias_to_canonical):,} aliases loaded")

    # -----------------------------------------------------------------------
    # Step 2: Build graph index
    # -----------------------------------------------------------------------
    print("Building graph node index...")
    node_slug_set, existing_edges_raw = build_graph_index()
    print(f"  {len(node_slug_set):,} canonical graph nodes")

    # Alias-resolve existing edge targets
    print("  Alias-resolving existing edge targets...")
    existing_edges: dict[str, dict[str, str]] = {}
    for slug, raw_targets in existing_edges_raw.items():
        resolved: dict[str, str] = {}
        for t_slug, t_etype in raw_targets.items():
            canonical = alias_to_canonical.get(t_slug, t_slug)
            resolved[canonical] = t_etype
        existing_edges[slug] = resolved

    # -----------------------------------------------------------------------
    # Step 2b: Build firstname index + load importance prior
    # -----------------------------------------------------------------------
    print("Loading node display names for firstname index...")
    node_names = load_node_display_names(node_slug_set, GRAPH_NODES_DIR, _SKIP_DIRS)
    print(f"  {len(node_names):,} display names loaded")

    print("Building firstname index...")
    firstname_index = build_firstname_index(node_slug_set, node_names)
    unique_count = sum(1 for slugs in firstname_index.values() if len(slugs) == 1)
    ambiguous_count = sum(1 for slugs in firstname_index.values() if len(slugs) > 1)
    print(f"  {len(firstname_index):,} first-name tokens ({unique_count:,} unique, {ambiguous_count:,} ambiguous)")

    print("Loading backlink-counts (importance prior)...")
    importance_prior = load_importance_prior(IN_BACKLINKS)
    print(f"  {len(importance_prior):,} slug priors loaded")

    # -----------------------------------------------------------------------
    # Step 3: Enumerate extraction files
    # -----------------------------------------------------------------------
    books_to_scan = [args.book] if args.book else BOOKS

    extraction_files: list[Path] = []
    for book in books_to_scan:
        book_dir = EXTRACTIONS_DIR / book
        if not book_dir.exists():
            print(f"  WARNING: extraction dir not found: {book_dir}", file=sys.stderr)
            continue
        for f in sorted(book_dir.glob("*.extraction.md")):
            chapter_slug = derive_chapter_slug(f)
            if args.chapter_slug and chapter_slug != args.chapter_slug:
                continue
            extraction_files.append(f)

    print(f"  {len(extraction_files):,} extraction files to process")

    # -----------------------------------------------------------------------
    # Step 4: Process each extraction file
    # -----------------------------------------------------------------------
    # Counters
    count_files_walked = 0
    count_rows_seen = 0
    count_drop_unresolved_source = 0
    count_drop_unresolved_target = 0
    count_drop_generic_source = 0
    count_drop_generic_target = 0
    count_drop_ambiguous_source = 0
    count_drop_ambiguous_target = 0
    count_drop_self = 0
    count_resolved = 0
    count_typed = 0
    count_untyped = 0
    count_corroborating = 0
    count_new = 0
    count_needs_qualifier = 0

    # Resolution-status histogram: {status: count}
    resolution_status_hist: dict[str, int] = collections.Counter()

    # Unresolved entity tracking: {raw_name: {"count": N, "example_chapter": slug}}
    unresolved_tally: dict[str, dict] = {}

    # Ambiguous-queued tracking: list of dicts for the review file
    ambiguous_review_rows: list[dict] = []

    # Conform drift tracking: {edge_type: {"count": N, "example_hint": str}}
    conform_drift: dict[str, dict] = {}

    # Per-book stats
    book_stats: dict[str, dict] = {b: collections.Counter() for b in BOOKS}

    # Edge type distribution
    edge_type_dist: dict[str, int] = collections.Counter()

    # Per-chapter output collections
    # {chapter_slug: (book, [candidate_row_dict, ...])}
    chapter_candidates: dict[str, tuple[str, list[dict]]] = {}
    # {chapter_slug: (book, [needs_qualifier_row_dict, ...])}
    chapter_needs_qualifier: dict[str, tuple[str, list[dict]]] = {}

    for extraction_path in extraction_files:
        count_files_walked += 1

        chapter_slug = derive_chapter_slug(extraction_path)
        book_abbrev = extraction_path.parent.name.lower()

        try:
            text = extraction_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"  WARNING: Cannot read {extraction_path}: {exc}", file=sys.stderr)
            continue

        meta = parse_extraction_metadata(text)
        pov_character_raw = meta.get("pov_character", "")
        if pov_character_raw:
            pov_slug = derive_pov_slug(pov_character_raw)
        else:
            parts = chapter_slug.split("-")
            pov_slug = "-".join(parts[1:-1]) if len(parts) >= 3 else ""

        rows = parse_relationships_table(text)

        if not rows:
            continue

        count_rows_seen += len(rows)
        extraction_rel = str(extraction_path.relative_to(REPO_ROOT))

        # -------------------------------------------------------------------
        # Bootstrap present_slugs for this chapter (rungs a–c only).
        # Sources: Characters Present names + Relationships table names.
        # This avoids circularity (we don't use context in bootstrapping).
        # -------------------------------------------------------------------
        bootstrap_names: list[str] = parse_characters_present(text)
        for row in rows:
            bootstrap_names.append(row["char_a"])
            bootstrap_names.append(row["char_b"])

        present_slugs: set[str] = set()
        for bname in bootstrap_names:
            s = resolve_name_bootstrap(
                bname,
                alias_map=alias_to_canonical,
                node_set=node_slug_set,
                firstname_index=firstname_index,
            )
            if s:
                present_slugs.add(s)

        candidates_this_chapter: list[dict] = []
        needs_qual_this_chapter: list[dict] = []

        for row in rows:
            char_a_raw = row["char_a"]
            char_b_raw = row["char_b"]
            relationship_raw = row["relationship"]
            evidence = row["evidence"]

            # RESOLVE source
            source_slug, source_status = resolve_name(
                char_a_raw,
                alias_map=alias_to_canonical,
                node_set=node_slug_set,
                firstname_index=firstname_index,
                prior=importance_prior,
                present_slugs=present_slugs,
            )

            # RESOLVE target
            target_slug, target_status = resolve_name(
                char_b_raw,
                alias_map=alias_to_canonical,
                node_set=node_slug_set,
                firstname_index=firstname_index,
                prior=importance_prior,
                present_slugs=present_slugs,
            )

            # Track resolution statuses for histogram (only successful endpoints)
            # We count each endpoint independently only when both resolve.
            # We process drops first.

            # Handle ambiguous endpoints → review queue
            if source_status == STATUS_AMBIGUOUS or target_status == STATUS_AMBIGUOUS:
                # Collect the candidate slugs for the ambiguous endpoint(s).
                # For non-ambiguous endpoint: use resolved slug if available, else [].
                from stage4_name_resolver import _clean_raw_name as _cnr, name_key as _nk

                def _ambig_candidates(raw):
                    """First-name candidates for an ambiguous endpoint."""
                    cleaned = _cnr(raw)
                    first = _nk(cleaned)
                    if first is None:
                        return []
                    return list(firstname_index.get(first, []))

                if source_status == STATUS_AMBIGUOUS:
                    a_cands = _ambig_candidates(char_a_raw)
                else:
                    a_cands = [source_slug] if source_slug is not None else []

                if target_status == STATUS_AMBIGUOUS:
                    b_cands = _ambig_candidates(char_b_raw)
                else:
                    b_cands = [target_slug] if target_slug is not None else []

                ambiguous_review_rows.append({
                    "chapter": chapter_slug,
                    "book": book_abbrev,
                    "pov": pov_slug,
                    "char_a_raw": char_a_raw,
                    "char_a_status": source_status,
                    "char_a_candidates": a_cands,
                    "char_b_raw": char_b_raw,
                    "char_b_status": target_status,
                    "char_b_candidates": b_cands,
                    "hint_raw": relationship_raw,
                })
                if source_status == STATUS_AMBIGUOUS:
                    count_drop_ambiguous_source += 1
                if target_status == STATUS_AMBIGUOUS:
                    count_drop_ambiguous_target += 1
                continue

            # Handle unresolved endpoints → needs-node tally
            # unresolved-generic is counted separately but also goes to the tally.
            if source_slug is None:
                if source_status == STATUS_UNRESOLVED_GENERIC:
                    count_drop_generic_source += 1
                else:
                    count_drop_unresolved_source += 1
                if char_a_raw not in unresolved_tally:
                    unresolved_tally[char_a_raw] = {"count": 0, "example_chapter": chapter_slug}
                unresolved_tally[char_a_raw]["count"] += 1
                continue

            if target_slug is None:
                if target_status == STATUS_UNRESOLVED_GENERIC:
                    count_drop_generic_target += 1
                else:
                    count_drop_unresolved_target += 1
                if char_b_raw not in unresolved_tally:
                    unresolved_tally[char_b_raw] = {"count": 0, "example_chapter": chapter_slug}
                unresolved_tally[char_b_raw]["count"] += 1
                continue

            # Self-edge gate
            if source_slug == target_slug:
                count_drop_self += 1
                continue

            # Both endpoints resolved — track status histogram
            resolution_status_hist[source_status] += 1
            resolution_status_hist[target_status] += 1

            count_resolved += 1

            # TYPE the hint
            hint_norm = normalize_hint(relationship_raw)
            edge_type = map_hint_to_edge(hint_norm)
            typed_by = "python-map" if edge_type is not None else None

            # CONFORM check: if edge_type is not None, must be in locked vocab
            if edge_type is not None and edge_type not in locked_vocab:
                if edge_type not in conform_drift:
                    conform_drift[edge_type] = {"count": 0, "example_hint": relationship_raw}
                conform_drift[edge_type]["count"] += 1
                print(
                    f"  CONFORM DRIFT: typer returned '{edge_type}' (not in locked vocab) "
                    f"for hint '{relationship_raw}' in {chapter_slug}",
                    file=sys.stderr,
                )
                edge_type = None
                typed_by = None

            # CORROBORATION check: look for existing edge in either direction
            corroborates = False
            wiki_edge_type = None
            fwd_edges = existing_edges.get(source_slug, {})
            rev_edges = existing_edges.get(target_slug, {})
            if target_slug in fwd_edges:
                corroborates = True
                wiki_edge_type = fwd_edges[target_slug]
            elif source_slug in rev_edges:
                corroborates = True
                wiki_edge_type = rev_edges[source_slug]

            if corroborates:
                count_corroborating += 1
            else:
                count_new += 1

            # QUALIFIER routing: Tier-1 edge types without qualifier go to separate tail
            if edge_type is not None and edge_type in tier1_types:
                # v1 emits no qualifier field → route to needs-qualifier tail
                count_needs_qualifier += 1
                count_typed += 1
                edge_type_dist[edge_type] += 1

                nq_row = {
                    "candidate_kind": "pass1_relationship",
                    "evidence_chapter": chapter_slug,
                    "evidence_book": book_abbrev,
                    "evidence_pov": pov_slug,
                    "source_slug": source_slug,
                    "source_resolution_status": source_status,
                    "target_slug": target_slug,
                    "target_resolution_status": target_status,
                    "hint_raw": relationship_raw,
                    "edge_type": edge_type,
                    "typed_by": typed_by,
                    "evidence_text": evidence,
                    "evidence_section": "Relationships Observed",
                    "corroborates_known_edge": corroborates,
                    "wiki_edge_type": wiki_edge_type,
                    "extraction_file": extraction_rel,
                    "needs_qualifier_reason": f"Tier-1 type {edge_type!r} requires qualifier; deferred",
                    "run_id": run_id,
                    "schema_version": schema_version,
                    "produced_at": produced_at,
                }
                needs_qual_this_chapter.append(nq_row)
                book_stats[book_abbrev]["needs_qualifier"] += 1
                book_stats[book_abbrev]["typed"] += 1
                continue  # Do NOT put in main candidates

            # Build candidate row
            if edge_type is not None:
                count_typed += 1
                edge_type_dist[edge_type] += 1
            else:
                count_untyped += 1

            book_stats[book_abbrev]["resolved"] += 1
            if edge_type is not None:
                book_stats[book_abbrev]["typed"] += 1
            else:
                book_stats[book_abbrev]["untyped"] += 1
            if corroborates:
                book_stats[book_abbrev]["corroborating"] += 1
            else:
                book_stats[book_abbrev]["new"] += 1

            candidate = {
                "candidate_kind": "pass1_relationship",
                "evidence_chapter": chapter_slug,
                "evidence_book": book_abbrev,
                "evidence_pov": pov_slug,
                "source_slug": source_slug,
                "source_resolution_status": source_status,
                "target_slug": target_slug,
                "target_resolution_status": target_status,
                "hint_raw": relationship_raw,
                "edge_type": edge_type,
                "typed_by": typed_by,
                "evidence_text": evidence,
                "evidence_section": "Relationships Observed",
                "corroborates_known_edge": corroborates,
                "wiki_edge_type": wiki_edge_type,
                "extraction_file": extraction_rel,
                "run_id": run_id,
                "schema_version": schema_version,
                "produced_at": produced_at,
            }
            candidates_this_chapter.append(candidate)

        if candidates_this_chapter:
            candidates_this_chapter.sort(key=lambda r: (r["source_slug"], r["target_slug"]))
            chapter_candidates[chapter_slug] = (book_abbrev, candidates_this_chapter)

        if needs_qual_this_chapter:
            needs_qual_this_chapter.sort(key=lambda r: (r["source_slug"], r["target_slug"]))
            chapter_needs_qualifier[chapter_slug] = (book_abbrev, needs_qual_this_chapter)

    # -----------------------------------------------------------------------
    # Step 5: Print summary
    # -----------------------------------------------------------------------
    # Compute top unresolved
    top_unresolved = sorted(
        unresolved_tally.items(), key=lambda x: -x[1]["count"]
    )[:50]

    count_main_candidates = sum(len(v[1]) for v in chapter_candidates.values())
    count_main_typed = sum(1 for v in chapter_candidates.values() for r in v[1] if r["edge_type"] is not None)
    count_main_untyped = count_main_candidates - count_main_typed
    count_ambiguous_queued = len(ambiguous_review_rows)

    print()
    print("=" * 70)
    print("STAGE 4 PASS-1-DERIVED EDGE CANDIDATES — RUN SUMMARY")
    print("=" * 70)
    print(f"  Extraction files walked:       {count_files_walked:>8,}")
    print(f"  Total Relationships rows seen: {count_rows_seen:>8,}")
    print(f"  Drop (source unresolved):      {count_drop_unresolved_source:>8,}")
    print(f"  Drop (target unresolved):      {count_drop_unresolved_target:>8,}")
    print(f"  Drop (source generic-term):    {count_drop_generic_source:>8,}")
    print(f"  Drop (target generic-term):    {count_drop_generic_target:>8,}")
    print(f"  Drop (source ambiguous):       {count_drop_ambiguous_source:>8,}")
    print(f"  Drop (target ambiguous):       {count_drop_ambiguous_target:>8,}")
    print(f"  Ambiguous-queued rows:         {count_ambiguous_queued:>8,}")
    print(f"  Drop (self-edge):              {count_drop_self:>8,}")
    print(f"  Resolved pairs:                {count_resolved:>8,}")
    print(f"    → Routed to needs-qualifier: {count_needs_qualifier:>8,}")
    print(f"    → Main candidates:           {count_main_candidates:>8,}")
    print(f"      of which typed:            {count_main_typed:>8,}")
    print(f"      of which untyped:          {count_main_untyped:>8,}")
    print(f"  Corroborating (wiki-known):    {count_corroborating:>8,}")
    print(f"  New (not in existing edges):   {count_new:>8,}")
    print(f"  Conform drift issues:          {len(conform_drift):>8,}")
    print()

    # Resolution-status histogram
    print("Resolution-status histogram (endpoint count for successfully resolved pairs):")
    for status in [
        STATUS_EXACT, STATUS_ALIAS, STATUS_FIRSTNAME_UNIQUE,
        STATUS_CONTEXT_PRESENT, STATUS_CONTEXT_PRIOR,
    ]:
        cnt = resolution_status_hist.get(status, 0)
        print(f"  {cnt:>8,}  {status}")
    count_generic_total = count_drop_generic_source + count_drop_generic_target
    print(f"  {count_generic_total:>8,}  {STATUS_UNRESOLVED_GENERIC}  (dropped before rungs c–e)")
    print()

    # Per-book
    print("Per-book breakdown:")
    for book in BOOKS:
        if args.book and book != args.book:
            continue
        bs = book_stats[book]
        print(
            f"  {book.upper():<6}  resolved={bs.get('resolved', 0):,}  "
            f"typed={bs.get('typed', 0):,}  untyped={bs.get('untyped', 0):,}  "
            f"corroborating={bs.get('corroborating', 0):,}  new={bs.get('new', 0):,}"
        )
    print()

    # Edge type distribution (top 20)
    print("Top 20 edge types by frequency:")
    for etype, cnt in sorted(edge_type_dist.items(), key=lambda x: -x[1])[:20]:
        print(f"  {cnt:>6,}  {etype}")
    print()

    # Conform drift
    if conform_drift:
        print(f"CONFORM DRIFT (typer output NOT in locked vocab) — {len(conform_drift)} type(s):")
        for etype, info in sorted(conform_drift.items()):
            print(f"  {info['count']:>5,}x  {etype!r}  example hint: {info['example_hint']!r}")
        print()
    else:
        print("Conform: no drift issues (all typer outputs are in locked vocab).")
        print()

    # Top unresolved
    print("Top 20 unresolved entity names (needs-node tally):")
    for name, info in top_unresolved[:20]:
        print(f"  {info['count']:>5,}  {name!r}  (e.g. {info['example_chapter']})")
    print(f"  Total distinct unresolved names: {len(unresolved_tally):,}")
    print()

    # -----------------------------------------------------------------------
    # Step 6: Write outputs (--apply only)
    # -----------------------------------------------------------------------
    if not write_output:
        print("Plan mode — nothing written. Re-run with --apply to write outputs.")
        return

    print("Writing outputs...")

    # 6a. Per-chapter candidate JSONL
    candidates_written = 0
    candidates_rows_written = 0
    for chapter_slug, (book_abbrev, candidates) in sorted(chapter_candidates.items()):
        out_dir = OUT_BASE_DIR / book_abbrev
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{chapter_slug}.candidates.jsonl"
        with out_file.open("w", encoding="utf-8") as fh:
            for row in candidates:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        candidates_written += 1
        candidates_rows_written += len(candidates)
    print(f"  {candidates_written:,} candidate files, {candidates_rows_written:,} rows")

    # 6b. Needs-qualifier tail JSONL
    nq_written = 0
    nq_rows_written = 0
    for chapter_slug, (book_abbrev, nq_rows) in sorted(chapter_needs_qualifier.items()):
        out_dir = OUT_NEEDS_QUAL_DIR / book_abbrev
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{chapter_slug}.needs-qualifier.jsonl"
        with out_file.open("w", encoding="utf-8") as fh:
            for row in nq_rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        nq_written += 1
        nq_rows_written += len(nq_rows)
    print(f"  {nq_written:,} needs-qualifier files, {nq_rows_written:,} rows")

    # 6c. Needs-node report
    WIKI_DATA_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Pass-1-Derived: Needs-Node Report",
        "",
        f"> Generated: {produced_at}  ",
        f"> run_id: {run_id}  ",
        f"> Total distinct unresolved names: {len(unresolved_tally):,}  ",
        "",
        "Entities that appeared in Relationships Observed tables but could not be",
        "resolved to a graph node slug even with the firstname resolver. These are",
        "candidates for new node files or alias-resolver additions.",
        "",
        "| Entity Name (raw) | Count | Example Chapter |",
        "|-------------------|-------|----------------|",
    ]
    for name, info in sorted(unresolved_tally.items(), key=lambda x: -x[1]["count"]):
        lines.append(f"| {name} | {info['count']:,} | {info['example_chapter']} |")
    lines += ["", "---", ""]
    OUT_NEEDS_NODE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Written: {OUT_NEEDS_NODE_MD}")

    # 6d. Ambiguous-review report
    ambig_lines = [
        "# Pass-1-Derived: Ambiguous Name Review",
        "",
        f"> Generated: {produced_at}  ",
        f"> run_id: {run_id}  ",
        f"> Total ambiguous-queued rows: {count_ambiguous_queued:,}  ",
        "",
        "Relationship rows where one or both endpoints had multiple firstname candidates",
        "and no confident disambiguation was possible. Human review needed.",
        "",
        "| Chapter | Book | POV | Char A (raw) | A Status | A Candidates | Char B (raw) | B Status | B Candidates | Hint |",
        "|---------|------|-----|--------------|----------|-------------|--------------|----------|-------------|------|",
    ]
    for ar in ambiguous_review_rows:
        a_cands = ", ".join(ar["char_a_candidates"][:5])
        b_cands = ", ".join(ar["char_b_candidates"][:5])
        ambig_lines.append(
            f"| {ar['chapter']} | {ar['book']} | {ar['pov']} | "
            f"{ar['char_a_raw']} | {ar['char_a_status']} | {a_cands} | "
            f"{ar['char_b_raw']} | {ar['char_b_status']} | {b_cands} | "
            f"{ar['hint_raw']} |"
        )
    ambig_lines += ["", "---", ""]
    OUT_AMBIGUOUS_MD.write_text("\n".join(ambig_lines) + "\n", encoding="utf-8")
    print(f"  Written: {OUT_AMBIGUOUS_MD}")

    # 6e. Supplementary firstname-aliases JSON (additive, does NOT modify alias-resolver.json)
    write_firstname_aliases(firstname_index, OUT_FIRSTNAME_ALIASES_JSON)
    print(f"  Written: {OUT_FIRSTNAME_ALIASES_JSON}")

    # 6f. Conform report
    conform_lines = [
        "# Pass-1-Derived: CONFORM Report",
        "",
        f"> Generated: {produced_at}  ",
        f"> run_id: {run_id}  ",
        "",
    ]
    if not conform_drift:
        conform_lines += [
            "**No drift issues found.** All typer outputs are in the locked edge vocabulary.",
            "",
        ]
    else:
        conform_lines += [
            f"**{len(conform_drift)} edge type(s)** produced by the typer are NOT in the locked vocabulary.",
            "These indicate a bug in the hint map — the typer's HINT_EXACT_MAP or HINT_PREFIX_MAP",
            "maps to a name not listed in reference/architecture.md.",
            "",
            "| Spurious Edge Type | Count | Example Hint |",
            "|--------------------|-------|-------------|",
        ]
        for etype, info in sorted(conform_drift.items(), key=lambda x: -x[1]["count"]):
            conform_lines.append(
                f"| {etype} | {info['count']:,} | {info['example_hint']!r} |"
            )
        conform_lines += ["", "**Action:** Fix HINT_EXACT_MAP / HINT_PREFIX_MAP to use canonical vocab names.", ""]
    OUT_CONFORM_MD.write_text("\n".join(conform_lines) + "\n", encoding="utf-8")
    print(f"  Written: {OUT_CONFORM_MD}")

    # 6g. Summary markdown
    summary_lines = [
        "# Pass-1-Derived Edge Candidates Summary",
        "",
        f"> Generated: {produced_at}  ",
        f"> run_id: {run_id}  ",
        f"> schema_version: {schema_version}  ",
        "",
        "## Counts",
        "",
        "| Stage | Count |",
        "|-------|-------|",
        f"| Extraction files walked | {count_files_walked:,} |",
        f"| Total Relationships rows seen | {count_rows_seen:,} |",
        f"| Drop: source unresolved | {count_drop_unresolved_source:,} |",
        f"| Drop: target unresolved | {count_drop_unresolved_target:,} |",
        f"| Drop: source generic-term | {count_drop_generic_source:,} |",
        f"| Drop: target generic-term | {count_drop_generic_target:,} |",
        f"| Drop: source ambiguous-queued | {count_drop_ambiguous_source:,} |",
        f"| Drop: target ambiguous-queued | {count_drop_ambiguous_target:,} |",
        f"| Ambiguous-queued rows | {count_ambiguous_queued:,} |",
        f"| Drop: self-edge | {count_drop_self:,} |",
        f"| Resolved pairs (total) | {count_resolved:,} |",
        f"| → Routed to needs-qualifier tail | {count_needs_qualifier:,} |",
        f"| → Main candidates | {count_main_candidates:,} |",
        f"|    of which typed | {count_main_typed:,} |",
        f"|    of which untyped | {count_main_untyped:,} |",
        f"| Corroborating (wiki-known) | {count_corroborating:,} |",
        f"| New (not in existing edges) | {count_new:,} |",
        f"| Conform drift issues | {len(conform_drift):,} |",
        f"| Total distinct unresolved names | {len(unresolved_tally):,} |",
        "",
        "## Resolution-Status Histogram",
        "",
        "Counts are per-endpoint (each edge has two endpoints).",
        "",
        "| Status | Endpoint Count |",
        "|--------|---------------|",
    ]
    for status in [
        STATUS_EXACT, STATUS_ALIAS, STATUS_FIRSTNAME_UNIQUE,
        STATUS_CONTEXT_PRESENT, STATUS_CONTEXT_PRIOR,
    ]:
        summary_lines.append(f"| {status} | {resolution_status_hist.get(status, 0):,} |")
    count_generic_total = count_drop_generic_source + count_drop_generic_target
    summary_lines.append(f"| {STATUS_UNRESOLVED_GENERIC} (dropped) | {count_generic_total:,} |")

    summary_lines += [
        "",
        "## Per-Book Breakdown",
        "",
        "| Book | Resolved | Typed | Untyped | Corroborating | New |",
        "|------|----------|-------|---------|--------------|-----|",
    ]
    for book in BOOKS:
        bs = book_stats[book]
        summary_lines.append(
            f"| {book.upper()} | {bs.get('resolved',0):,} | {bs.get('typed',0):,} | "
            f"{bs.get('untyped',0):,} | {bs.get('corroborating',0):,} | {bs.get('new',0):,} |"
        )

    summary_lines += [
        "",
        "## Edge Type Distribution",
        "",
        "| Edge Type | Count |",
        "|-----------|-------|",
    ]
    for etype, cnt in sorted(edge_type_dist.items(), key=lambda x: -x[1]):
        summary_lines.append(f"| {etype} | {cnt:,} |")

    summary_lines += [
        "",
        "## Top 50 Unresolved Entity Names",
        "",
        "| Entity Name (raw) | Count | Example Chapter |",
        "|-------------------|-------|----------------|",
    ]
    for name, info in top_unresolved:
        summary_lines.append(f"| {name} | {info['count']:,} | {info['example_chapter']} |")

    OUT_SUMMARY_MD.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print(f"  Written: {OUT_SUMMARY_MD}")

    # 6h. Stats JSON
    stats = {
        "generated_at": produced_at,
        "run_id": run_id,
        "schema_version": schema_version,
        "counts": {
            "extraction_files_walked": count_files_walked,
            "total_rows_seen": count_rows_seen,
            "drop_source_unresolved": count_drop_unresolved_source,
            "drop_target_unresolved": count_drop_unresolved_target,
            "drop_source_generic": count_drop_generic_source,
            "drop_target_generic": count_drop_generic_target,
            "drop_source_ambiguous": count_drop_ambiguous_source,
            "drop_target_ambiguous": count_drop_ambiguous_target,
            "ambiguous_queued_rows": count_ambiguous_queued,
            "drop_self_edge": count_drop_self,
            "resolved": count_resolved,
            "needs_qualifier": count_needs_qualifier,
            "main_candidates": count_main_candidates,
            "typed": count_main_typed,
            "untyped": count_main_untyped,
            "corroborating": count_corroborating,
            "new": count_new,
            "conform_drift_types": len(conform_drift),
            "distinct_unresolved_names": len(unresolved_tally),
        },
        "resolution_status_histogram": dict(resolution_status_hist),
        "per_book": {
            book: dict(book_stats[book])
            for book in BOOKS
        },
        "edge_type_distribution": dict(sorted(edge_type_dist.items(), key=lambda x: -x[1])),
        "top_unresolved": [
            {"name": name, "count": info["count"], "example_chapter": info["example_chapter"]}
            for name, info in top_unresolved
        ],
        "conform_drift": {
            etype: info
            for etype, info in sorted(conform_drift.items())
        },
    }
    OUT_SUMMARY_JSON.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"  Written: {OUT_SUMMARY_JSON}")

    print()
    print(
        f"Done. {count_main_candidates:,} main candidates + {count_needs_qualifier:,} "
        f"needs-qualifier rows written."
    )
    print(f"  Typed + emitted: {count_main_typed:,}  (corroborating: {count_corroborating:,} | new: {count_new:,})")
    print(f"  Untyped tail:    {count_main_untyped:,}")
    print(f"  Needs-qualifier: {count_needs_qualifier:,}")
    print(f"  Ambiguous-queued:{count_ambiguous_queued:,} rows → {OUT_AMBIGUOUS_MD.name}")
    print(f"  Needs-node:      {len(unresolved_tally):,} distinct names")
    print()
    print("Resolution-status histogram (endpoints in resolved pairs):")
    for status in [
        STATUS_EXACT, STATUS_ALIAS, STATUS_FIRSTNAME_UNIQUE,
        STATUS_CONTEXT_PRESENT, STATUS_CONTEXT_PRIOR,
    ]:
        cnt = resolution_status_hist.get(status, 0)
        print(f"  {cnt:>8,}  {status}")


if __name__ == "__main__":
    main()
