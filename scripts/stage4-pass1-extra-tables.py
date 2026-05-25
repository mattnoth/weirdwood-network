#!/usr/bin/env python3
"""stage4-pass1-extra-tables.py — Stage 4 Pass-1-Derived Edge Pipeline: Extra Tables.

Supplements stage4-pass1-edge-candidates.py by mining additional relational
tables from Pass 1 extraction files. This script is opt-in via --extra-tables
in the main candidates script (or run standalone).

Tables mined:
  1. ## Hospitality & Guest Right  — emits GUEST_OF (deterministic) and flags
     VIOLATES_GUEST_RIGHT (counted; violator/victim emitted where cleanly parseable).
  2. ## Dialogue of Note — emits Speaker→Listener pairs routed to the untyped
     tail (type not deterministic from columns).
  3. ## Food & Drink — counted only; ~5 example rows in report.
  4. ## Events & Actions — counted only (prose-shaped).
  5. ## Information Revealed — counted only (prose-shaped).

All new candidates are written to a separate staging path so they are fully
separable from the canonical spine outputs:
  working/wiki/pass2-buckets/pass1-derived/_extra-tables/{book}/{chapter}.extra-tables.jsonl

The existing canonical outputs are NEVER mutated.

Usage:
  python3 scripts/stage4-pass1-extra-tables.py --plan
      Compute all stats, print to stdout. Write NOTHING.
  python3 scripts/stage4-pass1-extra-tables.py --apply
      Same as --plan, plus write output files and report.
  python3 scripts/stage4-pass1-extra-tables.py --plan --book acok
      Restrict to one book (smoke test).
  python3 scripts/stage4-pass1-extra-tables.py --plan --chapter-slug acok-arya-01
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

# ---------------------------------------------------------------------------
# Load stage4_name_resolver (dynamic import, filename has underscores OK)
# ---------------------------------------------------------------------------
_RESOLVER_PATH = Path(__file__).parent / "stage4_name_resolver.py"
_resolver_spec = importlib.util.spec_from_file_location("stage4_name_resolver", _RESOLVER_PATH)
_resolver_mod = importlib.util.module_from_spec(_resolver_spec)
sys.modules["stage4_name_resolver"] = _resolver_mod
_resolver_spec.loader.exec_module(_resolver_mod)

from stage4_name_resolver import (  # noqa: E402
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
# Load stage4-pass1-edge-candidates.py for shared parsers / helpers
# (dynamic import — filename has hyphens)
# ---------------------------------------------------------------------------
def _load_hyphen_module(filename: str, mod_name: str):
    path = Path(__file__).parent / filename
    if not path.exists():
        print(f"ERROR: module not found at {path}", file=sys.stderr)
        sys.exit(1)
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


_candidates_mod = _load_hyphen_module(
    "stage4-pass1-edge-candidates.py",
    "stage4_pass1_edge_candidates",
)

# Re-export shared helpers from the candidates module so tests can import them
# from this module too.
to_slug = _candidates_mod.to_slug
parse_extraction_metadata = _candidates_mod.parse_extraction_metadata
derive_chapter_slug = _candidates_mod.derive_chapter_slug
derive_pov_slug = _candidates_mod.derive_pov_slug
parse_characters_present = _candidates_mod.parse_characters_present
build_graph_index = _candidates_mod.build_graph_index
load_locked_vocab = _candidates_mod.load_locked_vocab
load_tier1_edge_types = _candidates_mod.load_tier1_edge_types

_TABLE_ROW_RE = re.compile(r"^\|(.+)\|$")
_HEADING_RE = re.compile(r"^##\s+(.+)$")


def _split_table_row(line: str) -> list[str]:
    inner = line.strip().strip("|")
    return [c.strip() for c in inner.split("|")]


def _is_separator_row(cells: list[str]) -> bool:
    return all(re.match(r"^[-: ]+$", c) for c in cells if c)


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
GRAPH_NODES_DIR = REPO_ROOT / "graph" / "nodes"
EXTRACTIONS_DIR = REPO_ROOT / "extractions" / "mechanical"
WIKI_DATA_DIR = REPO_ROOT / "working" / "wiki" / "data"
PASS2_BUCKETS_DIR = REPO_ROOT / "working" / "wiki" / "pass2-buckets"

IN_ALIAS = WIKI_DATA_DIR / "alias-resolver.json"
IN_SUPP_ALIAS = WIKI_DATA_DIR / "pass1-derived-supplementary-aliases.json"
IN_BACKLINKS = WIKI_DATA_DIR / "backlink-counts.json"
ARCH_MD = REPO_ROOT / "reference" / "architecture.md"
QUAL_VOCAB_MD = REPO_ROOT / "reference" / "edge-qualifier-vocab.md"

OUT_EXTRA_BASE_DIR = PASS2_BUCKETS_DIR / "pass1-derived" / "_extra-tables"
OUT_REPORT_MD = WIKI_DATA_DIR / "pass1-derived-extra-tables-report.md"

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]


# ---------------------------------------------------------------------------
# Group stoplists: listener values that are clearly groups, not individuals.
# The resolver drops most of them naturally (unresolved), but we explicitly
# skip these common patterns to avoid noise.
# ---------------------------------------------------------------------------
_GROUP_LISTENER_PATTERNS = re.compile(
    r"^(the\s+)?(recruits?|men|soldiers?|lords?|ladies|crowd|council|"
    r"boys?|girls?|knights?|rangers?|brothers?|sisters?|servants?|"
    r"smallfolk|people|all|everyone|all present|assembled|"
    r"companions?|guards?|sworn swords?|household|bannermen|retainers?"
    r"|\w+s \(group\)|\w+s \(plural\))$",
    re.IGNORECASE,
)


def _looks_like_group(name: str) -> bool:
    """Return True if the raw name string looks like a group, not an individual."""
    return bool(_GROUP_LISTENER_PATTERNS.match(name.strip()))


# ---------------------------------------------------------------------------
# Hospitality qualifier normalization
# ---------------------------------------------------------------------------
_HOSP_QUAL_MAP: list[tuple[re.Pattern, str]] = [
    # NOTE: order matters — more-specific patterns must precede generic ones.
    # "shelter_denied" contains "shelter" so it must be checked first.
    (re.compile(r"refus|denied|denial|decline|reject", re.IGNORECASE), "refused"),
    (re.compile(r"shelter", re.IGNORECASE), "shelter"),
    (re.compile(r"feast", re.IGNORECASE), "feast"),
    (re.compile(r"bread.?and.?salt|bread\s*&\s*salt", re.IGNORECASE), "bread_and_salt"),
    (re.compile(r"safe.?conduct", re.IGNORECASE), "safe_conduct"),
    (re.compile(r"gift.?exchange|gift_exchange", re.IGNORECASE), "gift_exchange"),
]


def normalize_hospitality_qualifier(type_cell: str) -> str:
    """Map the raw Type column value to the GUEST_OF qualifier enum.

    Returns one of: shelter, feast, bread_and_salt, safe_conduct,
    gift_exchange, refused, unknown.
    """
    raw = type_cell.strip()
    for pattern, qual in _HOSP_QUAL_MAP:
        if pattern.search(raw):
            return qual
    return "unknown"


# ---------------------------------------------------------------------------
# Violation / special-type detection for Hospitality rows
# ---------------------------------------------------------------------------
_VIOLATION_TYPE_RE = re.compile(
    r"violat|broken|betrayal|massacre|murder|killed|slaughter|"
    r"hospitality_violated|shelter_denied.*violat|invoked.*negat|custom",
    re.IGNORECASE,
)
_VIOLATION_EVENT_RE = re.compile(
    r"red\s+wedding|violat|broken.*guest|betray.*guest|murder.*guest|"
    r"massacr|slaughter",
    re.IGNORECASE,
)
_SKIP_ROW_RE = re.compile(
    r"^(none|—|-|n/a|no\s|not\s)",
    re.IGNORECASE,
)
_REFUSAL_TYPE_RE = re.compile(
    r"shelter_denied|refusal|refused|hostage|captiv|detention|ward",
    re.IGNORECASE,
)
_GUEST_RIGHT_INVOKED_RE = re.compile(
    r"guest_right_invoked",
    re.IGNORECASE,
)


def _is_violation_row(event: str, typ: str, details: str) -> bool:
    """Return True if this hospitality row describes a violation."""
    combined = f"{event} {typ} {details}"
    return bool(_VIOLATION_TYPE_RE.search(combined) or _VIOLATION_EVENT_RE.search(event))


def _is_refusal_row(typ: str) -> bool:
    """Return True if this row is a refusal (shelter_denied / refusal_to_host)."""
    return bool(_REFUSAL_TYPE_RE.search(typ))


def _is_guest_right_invoked(typ: str) -> bool:
    """Return True if this row is guest-right-invoked (not a GUEST_OF edge)."""
    return bool(_GUEST_RIGHT_INVOKED_RE.search(typ))


# ---------------------------------------------------------------------------
# Parser: ## Hospitality & Guest Right
# ---------------------------------------------------------------------------
_HOSP_HEADING_RE = re.compile(r"^##\s+Hospitality", re.IGNORECASE)


def parse_hospitality_table(text: str) -> list[dict]:
    """Parse ## Hospitality & Guest Right from an extraction file.

    Returns list of dicts with keys:
        event, type_raw, host, guests_raw, details

    Empty / None tables return [].
    """
    in_section = False
    header_seen = False
    col_event = col_type = col_host = col_guests = col_details = -1
    rows: list[dict] = []

    for line in text.splitlines():
        h2_match = _HEADING_RE.match(line)
        if h2_match:
            section_label = h2_match.group(1).strip()
            if re.search(r"hospitality", section_label, re.IGNORECASE):
                in_section = True
                header_seen = False
                col_event = col_type = col_host = col_guests = col_details = -1
            else:
                in_section = False
            continue

        if not in_section:
            continue

        # Skip "None" prose lines
        stripped = line.strip()
        if _SKIP_ROW_RE.match(stripped) and not stripped.startswith("|"):
            continue

        if not _TABLE_ROW_RE.match(stripped):
            continue

        cells = _split_table_row(line)
        if not cells:
            continue
        if _is_separator_row(cells):
            continue

        if not header_seen:
            header_lower = [c.lower() for c in cells]
            for i, h in enumerate(header_lower):
                if "event" in h:
                    col_event = i
                elif "type" in h:
                    col_type = i
                elif "host" in h and "guest" not in h:
                    col_host = i
                elif "guest" in h:
                    col_guests = i
                elif "detail" in h:
                    col_details = i
            header_seen = True
            continue

        def _get(idx: int) -> str:
            if idx < 0 or idx >= len(cells):
                return ""
            return cells[idx].strip()

        event = _get(col_event)
        type_raw = _get(col_type)
        host = _get(col_host)
        guests_raw = _get(col_guests)
        details = _get(col_details)

        # Skip fully-empty data rows (e.g., "None" placeholder as table row)
        if not event and not host and not guests_raw:
            continue
        if _SKIP_ROW_RE.match(event) and not host and not guests_raw:
            continue

        rows.append({
            "event": event,
            "type_raw": type_raw,
            "host": host,
            "guests_raw": guests_raw,
            "details": details,
        })

    return rows


# ---------------------------------------------------------------------------
# Split guest cell on commas / "and" / semicolons
# ---------------------------------------------------------------------------
_GUEST_SPLIT_RE = re.compile(r"\s*[,;]\s*|\s+and\s+", re.IGNORECASE)


def split_guests(guests_raw: str) -> list[str]:
    """Split the Guest(s) cell into individual guest names.

    Handles: "Robb Stark, Catelyn, Edmure" or "Robb and Catelyn".
    Returns cleaned non-empty strings.
    """
    if not guests_raw:
        return []
    parts = _GUEST_SPLIT_RE.split(guests_raw)
    result = []
    for p in parts:
        p = p.strip()
        # Strip parenthetical notes like "(and their retainers)"
        p = re.sub(r"\s*\([^)]*\)", "", p).strip()
        if p and not _SKIP_ROW_RE.match(p):
            result.append(p)
    return result


# ---------------------------------------------------------------------------
# Parser: ## Dialogue of Note
# ---------------------------------------------------------------------------
_DIALOGUE_HEADING_RE = re.compile(r"^##\s+Dialogue", re.IGNORECASE)


def parse_dialogue_table(text: str) -> list[dict]:
    """Parse ## Dialogue of Note from an extraction file.

    Returns list of dicts with keys: speaker, listener, quote, context.
    """
    in_section = False
    header_seen = False
    col_speaker = col_listener = col_quote = col_context = -1
    rows: list[dict] = []

    for line in text.splitlines():
        h2_match = _HEADING_RE.match(line)
        if h2_match:
            section_label = h2_match.group(1).strip()
            if re.search(r"dialogue", section_label, re.IGNORECASE):
                in_section = True
                header_seen = False
                col_speaker = col_listener = col_quote = col_context = -1
            else:
                in_section = False
            continue

        if not in_section:
            continue
        if not _TABLE_ROW_RE.match(line.strip()):
            continue

        cells = _split_table_row(line)
        if not cells:
            continue
        if _is_separator_row(cells):
            continue

        if not header_seen:
            header_lower = [c.lower() for c in cells]
            for i, h in enumerate(header_lower):
                if "speaker" in h:
                    col_speaker = i
                elif "listener" in h:
                    col_listener = i
                elif "quote" in h or "paraphrase" in h:
                    col_quote = i
                elif "context" in h:
                    col_context = i
            header_seen = True
            continue

        def _get(idx: int) -> str:
            if idx < 0 or idx >= len(cells):
                return ""
            return cells[idx].strip()

        speaker = _get(col_speaker)
        listener = _get(col_listener)
        quote = _get(col_quote)
        context = _get(col_context)

        if not speaker or not listener:
            continue

        rows.append({
            "speaker": speaker,
            "listener": listener,
            "quote": quote,
            "context": context,
        })

    return rows


# ---------------------------------------------------------------------------
# Parser: ## Food & Drink (count + examples only)
# ---------------------------------------------------------------------------
_FOOD_HEADING_RE = re.compile(r"^##\s+Food\s*&?\s*Drink", re.IGNORECASE)
# Column index for "Who Is Eating/Drinking"
_WHO_EATING_PATTERNS = re.compile(r"who.*(eat|drink)", re.IGNORECASE)


def parse_food_table(text: str) -> list[dict]:
    """Parse ## Food & Drink table. Returns rows as dicts with all columns.

    We don't emit edges from this table; just count and provide examples.
    """
    in_section = False
    header_seen = False
    header_cols: list[str] = []
    rows: list[dict] = []

    for line in text.splitlines():
        h2_match = _HEADING_RE.match(line)
        if h2_match:
            section_label = h2_match.group(1).strip()
            if re.search(r"food", section_label, re.IGNORECASE):
                in_section = True
                header_seen = False
                header_cols = []
            else:
                in_section = False
            continue

        if not in_section:
            continue
        if not _TABLE_ROW_RE.match(line.strip()):
            continue

        cells = _split_table_row(line)
        if not cells:
            continue
        if _is_separator_row(cells):
            continue

        if not header_seen:
            header_cols = [c.lower() for c in cells]
            header_seen = True
            continue

        row = dict(zip(header_cols, cells))
        rows.append(row)

    return rows


def count_food_multi_named(rows: list[dict]) -> int:
    """Count Food rows that appear to have >=2 cleanly-parseable named referents.

    Heuristic: if 'who' column has >=2 comma/and-separated tokens each starting
    with a capital letter, count it as a potential co-dining pair.
    """
    count = 0
    for row in rows:
        who = ""
        for k, v in row.items():
            if _WHO_EATING_PATTERNS.search(k):
                who = v
                break
        if not who:
            # Fall back to any value that looks like a list of names
            for v in row.values():
                if v and re.search(r"[A-Z]\w+\s*,\s*[A-Z]\w+|[A-Z]\w+\s+and\s+[A-Z]\w+", v):
                    who = v
                    break
        if not who:
            continue
        # Split and count capitalized tokens
        parts = re.split(r"\s*[,;]\s*|\s+and\s+", who)
        named = [p.strip() for p in parts if p.strip() and p.strip()[0].isupper()]
        if len(named) >= 2:
            count += 1
    return count


# ---------------------------------------------------------------------------
# Parser: ## Events & Actions (count only — numbered prose list)
# ---------------------------------------------------------------------------
_EVENTS_HEADING_RE = re.compile(r"^##\s+Events\s*&?\s*Actions", re.IGNORECASE)
_NUMBERED_ITEM_RE = re.compile(r"^\d+\.\s+")


def parse_events_section(text: str) -> list[str]:
    """Parse ## Events & Actions — return list of item strings (numbered lines)."""
    in_section = False
    items: list[str] = []

    for line in text.splitlines():
        h2_match = _HEADING_RE.match(line)
        if h2_match:
            section_label = h2_match.group(1).strip()
            in_section = re.search(r"events", section_label, re.IGNORECASE) is not None
            continue
        if not in_section:
            continue
        if _NUMBERED_ITEM_RE.match(line.strip()):
            items.append(line.strip())

    return items


# ---------------------------------------------------------------------------
# Parser: ## Information Revealed (count only — table)
# ---------------------------------------------------------------------------
_INFO_HEADING_RE = re.compile(r"^##\s+Information\s+Revealed", re.IGNORECASE)


def parse_info_table(text: str) -> list[dict]:
    """Parse ## Information Revealed table. Returns rows as dicts."""
    in_section = False
    header_seen = False
    header_cols: list[str] = []
    rows: list[dict] = []

    for line in text.splitlines():
        h2_match = _HEADING_RE.match(line)
        if h2_match:
            section_label = h2_match.group(1).strip()
            if re.search(r"information\s+revealed", section_label, re.IGNORECASE):
                in_section = True
                header_seen = False
                header_cols = []
            else:
                in_section = False
            continue

        if not in_section:
            continue
        if not _TABLE_ROW_RE.match(line.strip()):
            continue

        cells = _split_table_row(line)
        if not cells:
            continue
        if _is_separator_row(cells):
            continue

        if not header_seen:
            header_cols = [c.lower() for c in cells]
            header_seen = True
            continue

        row = dict(zip(header_cols, cells))
        rows.append(row)

    return rows


# ---------------------------------------------------------------------------
# Bootstrap present_slugs (reuse same approach as main pipeline)
# ---------------------------------------------------------------------------
def _build_present_slugs(
    text: str,
    hosp_rows: list[dict],
    diag_rows: list[dict],
    alias_map: dict,
    node_set: set,
    firstname_index: dict,
) -> set[str]:
    """Build a set of probable-present slugs for context-resolution.

    Seeds from Characters Present + Hospitality host/guests + Dialogue speakers/listeners.
    """
    raw_names: list[str] = parse_characters_present(text)
    for row in hosp_rows:
        if row["host"]:
            raw_names.append(row["host"])
        for g in split_guests(row["guests_raw"]):
            raw_names.append(g)
    for row in diag_rows:
        raw_names.append(row["speaker"])
        raw_names.append(row["listener"])

    present: set[str] = set()
    for name in raw_names:
        s = resolve_name_bootstrap(
            name,
            alias_map=alias_map,
            node_set=node_set,
            firstname_index=firstname_index,
        )
        if s:
            present.add(s)
    return present


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Stage 4 Pass-1-Derived Edge Pipeline — Extra Tables miner.\n"
            "Mines Hospitality, Dialogue, Food, Events, Information Revealed tables\n"
            "from 344 Pass 1 extraction files. GUEST_OF edges are deterministic ($0).\n"
            "Dialogue Speaker→Listener pairs route to the untyped tail.\n"
            "Food/Events/Info are counted only (no edges emitted).\n"
            "\n"
            "NEVER mutates existing canonical spine outputs."
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
    parser.add_argument("--book", choices=BOOKS, default=None, metavar="BOOK")
    parser.add_argument("--chapter-slug", default=None, metavar="SLUG")
    args = parser.parse_args()
    write_output = args.apply

    run_date = datetime.now(timezone.utc).strftime("%Y%m%d")
    run_id = f"pass1-extra-tables-{run_date}"
    schema_version = "pass1-extra-tables-v1"
    produced_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # ------------------------------------------------------------------
    # Step 0: Load alias resolver
    # ------------------------------------------------------------------
    print("Loading alias resolver...")
    try:
        alias_data = json.loads(IN_ALIAS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: Cannot load {IN_ALIAS}: {exc}", file=sys.stderr)
        sys.exit(1)
    alias_to_canonical: dict[str, str] = alias_data.get("alias_to_canonical", {})
    print(f"  {len(alias_to_canonical):,} aliases loaded")

    # Supplementary aliases (additive, fill-only — same guard as main pipeline)
    if IN_SUPP_ALIAS.exists():
        try:
            supp_data = json.loads(IN_SUPP_ALIAS.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"  WARNING: cannot load supplementary aliases: {exc}", file=sys.stderr)
            supp_data = {}
        supp_map: dict[str, str] = supp_data.get("alias_to_canonical", {})
        added = conflicts = 0
        for k, v in supp_map.items():
            existing = alias_to_canonical.get(k)
            if existing is not None and existing != v:
                conflicts += 1
                continue
            if existing is None:
                alias_to_canonical[k] = v
                added += 1
        print(f"  +{added} supplementary aliases merged ({conflicts} conflicts skipped)")

    # ------------------------------------------------------------------
    # Step 1: Build graph index
    # ------------------------------------------------------------------
    print("Building graph node index...")
    node_slug_set, _existing_edges_raw = build_graph_index()
    print(f"  {len(node_slug_set):,} canonical graph nodes")

    print("Loading node display names for firstname index...")
    _SKIP_DIRS = {"_conflicts", "_unclassified", "_stage3-preview"}
    node_names = load_node_display_names(node_slug_set, GRAPH_NODES_DIR, _SKIP_DIRS)
    print(f"  {len(node_names):,} display names loaded")

    print("Building firstname index...")
    firstname_index = build_firstname_index(node_slug_set, node_names)

    print("Loading backlink-counts (importance prior)...")
    importance_prior = load_importance_prior(IN_BACKLINKS)
    print(f"  {len(importance_prior):,} slug priors loaded")

    # ------------------------------------------------------------------
    # Step 2: Enumerate extraction files
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Step 3: Counters and accumulators
    # ------------------------------------------------------------------
    # Hospitality counters
    h_rows_seen = 0
    h_none_tables = 0
    h_guest_of_emitted = 0
    h_violation_flagged = 0
    h_violation_emitted = 0
    h_refusal_emitted = 0
    h_invoked_skipped = 0
    h_guest_drop_unresolved = 0
    h_guest_drop_self = 0
    h_qualifier_dist: dict[str, int] = collections.Counter()
    h_violation_rows_detail: list[dict] = []  # for report

    # Dialogue counters
    d_rows_seen = 0
    d_tail_emitted = 0
    d_drop_group_listener = 0
    d_drop_unresolved = 0
    d_drop_self = 0

    # Food counters
    f_rows_seen = 0
    f_multi_named = 0
    f_examples: list[dict] = []

    # Events counters
    ev_rows_seen = 0
    ev_examples: list[str] = []

    # Info counters
    i_rows_seen = 0
    i_examples: list[dict] = []

    # Per-book stats
    book_stats: dict[str, dict] = {b: collections.Counter() for b in BOOKS}

    # Per-chapter output collections
    # {chapter_slug: (book, [candidate_row_dict, ...])}
    chapter_extra: dict[str, tuple[str, list[dict]]] = {}

    # ------------------------------------------------------------------
    # Step 4: Process each extraction file
    # ------------------------------------------------------------------
    for extraction_path in extraction_files:
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

        extraction_rel = str(extraction_path.relative_to(REPO_ROOT))

        hosp_rows = parse_hospitality_table(text)
        diag_rows = parse_dialogue_table(text)
        food_rows = parse_food_table(text)
        event_items = parse_events_section(text)
        info_rows = parse_info_table(text)

        # Build present_slugs for context resolution
        present_slugs = _build_present_slugs(
            text, hosp_rows, diag_rows,
            alias_to_canonical, node_slug_set, firstname_index,
        )

        chapter_rows: list[dict] = []

        # -----------------------------------------------------------------
        # 4a. Hospitality table
        # -----------------------------------------------------------------
        if not hosp_rows:
            h_none_tables += 1
        else:
            h_rows_seen += len(hosp_rows)

            for row in hosp_rows:
                event = row["event"]
                type_raw = row["type_raw"]
                host = row["host"]
                guests_raw = row["guests_raw"]
                details = row["details"]

                # Skip guest_right_invoked rows — these don't produce GUEST_OF edges
                if _is_guest_right_invoked(type_raw):
                    h_invoked_skipped += 1
                    continue

                # Detect violations — flag for report, attempt edge if host/guest clear
                if _is_violation_row(event, type_raw, details):
                    h_violation_flagged += 1
                    # Attempt: violator = host, victim(s) = guests
                    # Only emit if both resolve cleanly
                    violator_slug, violator_status = resolve_name(
                        host,
                        alias_map=alias_to_canonical,
                        node_set=node_slug_set,
                        firstname_index=firstname_index,
                        prior=importance_prior,
                        present_slugs=present_slugs,
                    )
                    for guest_raw in split_guests(guests_raw):
                        victim_slug, victim_status = resolve_name(
                            guest_raw,
                            alias_map=alias_to_canonical,
                            node_set=node_slug_set,
                            firstname_index=firstname_index,
                            prior=importance_prior,
                            present_slugs=present_slugs,
                        )
                        detail_entry = {
                            "chapter": chapter_slug,
                            "book": book_abbrev,
                            "event": event,
                            "type_raw": type_raw,
                            "host": host,
                            "guest_raw": guest_raw,
                            "violator_slug": violator_slug,
                            "victim_slug": victim_slug,
                            "emitted": False,
                        }
                        if (violator_slug and victim_slug
                                and violator_slug != victim_slug
                                and violator_status not in (STATUS_AMBIGUOUS, STATUS_UNRESOLVED, STATUS_UNRESOLVED_GENERIC)
                                and victim_status not in (STATUS_AMBIGUOUS, STATUS_UNRESOLVED, STATUS_UNRESOLVED_GENERIC)):
                            h_violation_emitted += 1
                            detail_entry["emitted"] = True
                            cand = {
                                "candidate_kind": "pass1_hospitality_violation",
                                "source_section": "Hospitality & Guest Right",
                                "evidence_chapter": chapter_slug,
                                "evidence_book": book_abbrev,
                                "evidence_pov": pov_slug,
                                "source_slug": violator_slug,
                                "source_resolution_status": violator_status,
                                "target_slug": victim_slug,
                                "target_resolution_status": victim_status,
                                "edge_type": "VIOLATES_GUEST_RIGHT",
                                "typed_by": "hospitality-table-violation",
                                "qualifier": None,
                                "evidence_event": event,
                                "evidence_type_raw": type_raw,
                                "evidence_details": details,
                                "extraction_file": extraction_rel,
                                "run_id": run_id,
                                "schema_version": schema_version,
                                "produced_at": produced_at,
                            }
                            chapter_rows.append(cand)
                            book_stats[book_abbrev]["violation_emitted"] += 1
                        h_violation_rows_detail.append(detail_entry)
                    continue  # Do not also emit GUEST_OF for violation rows

                # Skip refusal rows — these map to qualifier=refused on GUEST_OF
                # (refusal still has a guest_of direction: guest attempted → host refused)
                if _is_refusal_row(type_raw):
                    qualifier = "refused"
                else:
                    qualifier = normalize_hospitality_qualifier(type_raw)

                # Resolve host
                if not host or _SKIP_ROW_RE.match(host):
                    continue
                host_slug, host_status = resolve_name(
                    host,
                    alias_map=alias_to_canonical,
                    node_set=node_slug_set,
                    firstname_index=firstname_index,
                    prior=importance_prior,
                    present_slugs=present_slugs,
                )
                if not host_slug or host_status in (STATUS_AMBIGUOUS, STATUS_UNRESOLVED, STATUS_UNRESOLVED_GENERIC):
                    if host:
                        h_guest_drop_unresolved += 1
                    continue

                # Each guest → host edge
                for guest_raw in split_guests(guests_raw):
                    if not guest_raw or _SKIP_ROW_RE.match(guest_raw):
                        continue

                    guest_slug, guest_status = resolve_name(
                        guest_raw,
                        alias_map=alias_to_canonical,
                        node_set=node_slug_set,
                        firstname_index=firstname_index,
                        prior=importance_prior,
                        present_slugs=present_slugs,
                    )
                    if not guest_slug or guest_status in (STATUS_AMBIGUOUS, STATUS_UNRESOLVED, STATUS_UNRESOLVED_GENERIC):
                        h_guest_drop_unresolved += 1
                        continue

                    if guest_slug == host_slug:
                        h_guest_drop_self += 1
                        continue

                    h_guest_of_emitted += 1
                    h_qualifier_dist[qualifier] += 1
                    book_stats[book_abbrev]["guest_of_emitted"] += 1

                    if qualifier == "refused":
                        h_refusal_emitted += 1

                    cand = {
                        "candidate_kind": "pass1_hospitality",
                        "source_section": "Hospitality & Guest Right",
                        "evidence_chapter": chapter_slug,
                        "evidence_book": book_abbrev,
                        "evidence_pov": pov_slug,
                        # GUEST_OF direction: Guest → Host
                        "source_slug": guest_slug,
                        "source_resolution_status": guest_status,
                        "target_slug": host_slug,
                        "target_resolution_status": host_status,
                        "edge_type": "GUEST_OF",
                        "typed_by": "hospitality-table",
                        "qualifier": qualifier,
                        "evidence_event": event,
                        "evidence_type_raw": type_raw,
                        "evidence_details": details,
                        "extraction_file": extraction_rel,
                        "run_id": run_id,
                        "schema_version": schema_version,
                        "produced_at": produced_at,
                    }
                    chapter_rows.append(cand)

        # -----------------------------------------------------------------
        # 4b. Dialogue table — Speaker → Listener, untyped tail
        # -----------------------------------------------------------------
        d_rows_seen += len(diag_rows)

        for row in diag_rows:
            speaker_raw = row["speaker"]
            listener_raw = row["listener"]
            quote = row["quote"]
            context = row["context"]

            # Group listener check — let resolver drop most; explicit fast-path for common patterns
            if _looks_like_group(listener_raw):
                d_drop_group_listener += 1
                continue

            speaker_slug, speaker_status = resolve_name(
                speaker_raw,
                alias_map=alias_to_canonical,
                node_set=node_slug_set,
                firstname_index=firstname_index,
                prior=importance_prior,
                present_slugs=present_slugs,
            )
            listener_slug, listener_status = resolve_name(
                listener_raw,
                alias_map=alias_to_canonical,
                node_set=node_slug_set,
                firstname_index=firstname_index,
                prior=importance_prior,
                present_slugs=present_slugs,
            )

            if not speaker_slug or speaker_status in (STATUS_AMBIGUOUS, STATUS_UNRESOLVED, STATUS_UNRESOLVED_GENERIC):
                d_drop_unresolved += 1
                continue
            if not listener_slug or listener_status in (STATUS_AMBIGUOUS, STATUS_UNRESOLVED, STATUS_UNRESOLVED_GENERIC):
                d_drop_unresolved += 1
                continue

            if speaker_slug == listener_slug:
                d_drop_self += 1
                continue

            d_tail_emitted += 1
            book_stats[book_abbrev]["dialogue_tail"] += 1

            # Tail row: edge_type is None (untyped), hint is quote + context
            hint = f"{quote} [{context}]".strip(" []")
            cand = {
                "candidate_kind": "pass1_dialogue",
                "source_section": "Dialogue of Note",
                "evidence_chapter": chapter_slug,
                "evidence_book": book_abbrev,
                "evidence_pov": pov_slug,
                "source_slug": speaker_slug,
                "source_resolution_status": speaker_status,
                "target_slug": listener_slug,
                "target_resolution_status": listener_status,
                "edge_type": None,
                "typed_by": None,
                "qualifier": None,
                "hint_raw": hint,
                "evidence_quote": quote,
                "evidence_context": context,
                "extraction_file": extraction_rel,
                "run_id": run_id,
                "schema_version": schema_version,
                "produced_at": produced_at,
            }
            chapter_rows.append(cand)

        # -----------------------------------------------------------------
        # 4c. Food & Drink — count only
        # -----------------------------------------------------------------
        f_rows_seen += len(food_rows)
        multi = count_food_multi_named(food_rows)
        f_multi_named += multi
        if len(f_examples) < 5:
            for r in food_rows:
                if len(f_examples) >= 5:
                    break
                who = ""
                for k, v in r.items():
                    if _WHO_EATING_PATTERNS.search(k):
                        who = v
                        break
                f_examples.append({"chapter": chapter_slug, "row": r, "who": who})

        # -----------------------------------------------------------------
        # 4d. Events & Actions — count only
        # -----------------------------------------------------------------
        ev_rows_seen += len(event_items)
        if len(ev_examples) < 5:
            for item in event_items[:5]:
                if len(ev_examples) >= 5:
                    break
                ev_examples.append({"chapter": chapter_slug, "text": item})

        # -----------------------------------------------------------------
        # 4e. Information Revealed — count only
        # -----------------------------------------------------------------
        i_rows_seen += len(info_rows)
        if len(i_examples) < 5:
            for r in info_rows[:5]:
                if len(i_examples) >= 5:
                    break
                i_examples.append({"chapter": chapter_slug, "row": r})

        # -----------------------------------------------------------------
        # Collect chapter rows
        # -----------------------------------------------------------------
        if chapter_rows:
            chapter_extra[chapter_slug] = (book_abbrev, chapter_rows)

    # ------------------------------------------------------------------
    # Step 5: Print summary
    # ------------------------------------------------------------------
    total_hosp_emitted = h_guest_of_emitted + h_violation_emitted
    total_deterministic = h_guest_of_emitted + h_violation_emitted  # both typed
    total_tail = d_tail_emitted

    # Dialogue LLM cost estimate at S67 observed rate: $0.0068/row
    tail_cost_estimate = d_tail_emitted * 0.0068

    print()
    print("=" * 70)
    print("STAGE 4 PASS-1 EXTRA TABLES — RUN SUMMARY")
    print("=" * 70)
    print()
    print("--- Hospitality & Guest Right ---")
    print(f"  Rows seen (non-None):          {h_rows_seen:>8,}")
    print(f"  None/empty tables:             {h_none_tables:>8,}")
    print(f"  guest_right_invoked skipped:   {h_invoked_skipped:>8,}")
    print(f"  Violation rows flagged:        {h_violation_flagged:>8,}")
    print(f"  VIOLATES_GUEST_RIGHT emitted:  {h_violation_emitted:>8,}")
    print(f"  Drop (unresolved host/guest):  {h_guest_drop_unresolved:>8,}")
    print(f"  Drop (self-edge):              {h_guest_drop_self:>8,}")
    print(f"  GUEST_OF edges emitted:        {h_guest_of_emitted:>8,}  (deterministic, $0)")
    print(f"    of which qualifier=refused:  {h_refusal_emitted:>8,}")
    print()
    print("  GUEST_OF qualifier distribution:")
    for qual, cnt in sorted(h_qualifier_dist.items(), key=lambda x: -x[1]):
        print(f"    {cnt:>6,}  {qual}")
    print()
    print("  VIOLATES_GUEST_RIGHT candidates (flagged violations, emitted where resolvable):")
    emitted_violations = [r for r in h_violation_rows_detail if r["emitted"]]
    unemitted_violations = [r for r in h_violation_rows_detail if not r["emitted"]]
    print(f"    Emitted: {len(emitted_violations):,}  |  Counted-only (unresolved): {len(unemitted_violations):,}")
    if emitted_violations[:5]:
        print("    Notable emitted violations:")
        for rv in emitted_violations[:5]:
            print(f"      [{rv['chapter']}] {rv['event'][:60]!r}")
    print()
    print("--- Dialogue of Note ---")
    print(f"  Rows seen:                     {d_rows_seen:>8,}")
    print(f"  Drop (group listener):         {d_drop_group_listener:>8,}")
    print(f"  Drop (unresolved endpoint):    {d_drop_unresolved:>8,}")
    print(f"  Drop (self-edge):              {d_drop_self:>8,}")
    print(f"  Tail rows emitted (untyped):   {d_tail_emitted:>8,}")
    print(f"  LLM cost if typed (S67 rate):  ${tail_cost_estimate:>7.2f}  (~${tail_cost_estimate/1:.2f} at $0.0068/row)")
    print()
    print("--- Food & Drink (counted only) ---")
    print(f"  Rows seen:                     {f_rows_seen:>8,}")
    print(f"  Rows with >=2 named referents: {f_multi_named:>8,}")
    print("  Examples (first 5 rows):")
    for ex in f_examples[:5]:
        who = ex.get("who", "")[:80]
        print(f"    [{ex['chapter']}] who={who!r}")
    print()
    print("--- Events & Actions (counted only) ---")
    print(f"  Numbered items:                {ev_rows_seen:>8,}")
    print("  Examples (first 5):")
    for ex in ev_examples[:5]:
        print(f"    [{ex['chapter']}] {ex['text'][:100]}")
    print()
    print("--- Information Revealed (counted only) ---")
    print(f"  Rows seen:                     {i_rows_seen:>8,}")
    print("  Examples (first 5 'How Revealed' values):")
    for ex in i_examples[:5]:
        how = ""
        for k, v in ex["row"].items():
            if "how" in k:
                how = v
                break
        print(f"    [{ex['chapter']}] how={how[:80]!r}")
    print()
    print("--- Totals ---")
    print(f"  New DETERMINISTIC edges:       {total_deterministic:>8,}  (GUEST_OF + VIOLATES_GUEST_RIGHT)")
    print(f"  New TAIL rows:                 {total_tail:>8,}  (Dialogue, untyped)")
    print(f"  Total extra candidates:        {total_deterministic + total_tail:>8,}")
    print()

    per_book_header = f"{'Book':<6}  {'GUEST_OF':>10}  {'violation':>10}  {'diag_tail':>10}"
    print("Per-book breakdown:")
    print(f"  {per_book_header}")
    for book in BOOKS:
        if args.book and book != args.book:
            continue
        bs = book_stats[book]
        print(
            f"  {book.upper():<6}  {bs.get('guest_of_emitted', 0):>10,}  "
            f"{bs.get('violation_emitted', 0):>10,}  "
            f"{bs.get('dialogue_tail', 0):>10,}"
        )
    print()

    if not write_output:
        print("Plan mode — nothing written. Re-run with --apply to write outputs.")
        return

    # ------------------------------------------------------------------
    # Step 6: Write outputs (--apply only)
    # ------------------------------------------------------------------
    print("Writing outputs...")

    # 6a. Per-chapter extra-tables JSONL
    files_written = 0
    rows_written = 0
    for chapter_slug, (book_abbrev, rows) in sorted(chapter_extra.items()):
        out_dir = OUT_EXTRA_BASE_DIR / book_abbrev
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{chapter_slug}.extra-tables.jsonl"
        with out_file.open("w", encoding="utf-8") as fh:
            for row in sorted(rows, key=lambda r: (r["source_slug"], r["target_slug"])):
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        files_written += 1
        rows_written += len(rows)
    print(f"  {files_written:,} extra-tables files, {rows_written:,} rows")

    # 6b. Report
    report_lines = [
        "# Pass-1-Derived Extra Tables: Recall Headroom Report",
        "",
        f"> Generated: {produced_at}  ",
        f"> run_id: {run_id}  ",
        f"> schema_version: {schema_version}  ",
        "",
        "This report answers: **how much recall headroom do the extra Pass 1 tables add**",
        "beyond the existing Relationships Observed spine?",
        "",
        "Sections: Hospitality & Guest Right | Dialogue of Note | Food & Drink | Events & Actions | Information Revealed",
        "",
        "---",
        "",
        "## 1. Hospitality & Guest Right",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Rows seen (non-None tables) | {h_rows_seen:,} |",
        f"| None/empty tables | {h_none_tables:,} |",
        f"| guest_right_invoked skipped | {h_invoked_skipped:,} |",
        f"| Violation rows flagged | {h_violation_flagged:,} |",
        f"| VIOLATES_GUEST_RIGHT emitted (resolvable violator+victim) | {h_violation_emitted:,} |",
        f"| VIOLATES_GUEST_RIGHT counted-only (unresolved) | {len(unemitted_violations):,} |",
        f"| Drop (unresolved host/guest) | {h_guest_drop_unresolved:,} |",
        f"| Drop (self-edge) | {h_guest_drop_self:,} |",
        f"| **GUEST_OF edges emitted (deterministic, $0)** | **{h_guest_of_emitted:,}** |",
        f"| of which qualifier=refused | {h_refusal_emitted:,} |",
        "",
        "**GUEST_OF qualifier distribution:**",
        "",
        "| Qualifier | Count |",
        "|-----------|-------|",
    ]
    for qual, cnt in sorted(h_qualifier_dist.items(), key=lambda x: -x[1]):
        report_lines.append(f"| {qual} | {cnt:,} |")

    report_lines += [
        "",
        "**VIOLATES_GUEST_RIGHT — notable emitted violations:**",
        "",
        "| Chapter | Event | Violator (slug) | Victim (slug) |",
        "|---------|-------|----------------|--------------|",
    ]
    for rv in sorted(emitted_violations, key=lambda r: r["chapter"]):
        report_lines.append(
            f"| {rv['chapter']} | {rv['event'][:60]} "
            f"| {rv.get('violator_slug', '?')} | {rv.get('victim_slug', '?')} |"
        )

    report_lines += [
        "",
        "---",
        "",
        "## 2. Dialogue of Note",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Rows seen | {d_rows_seen:,} |",
        f"| Drop (group listener) | {d_drop_group_listener:,} |",
        f"| Drop (unresolved endpoint) | {d_drop_unresolved:,} |",
        f"| Drop (self-edge) | {d_drop_self:,} |",
        f"| **Tail rows emitted (untyped, Speaker→Listener)** | **{d_tail_emitted:,}** |",
        f"| LLM cost if typed (S67 rate ≈ $0.0068/row) | ${tail_cost_estimate:.2f} |",
        "",
        "Edge type is NOT deterministic from the Dialogue table — the quote/context",
        "is the hint for a future LLM tail step. These are NOT $0 edges.",
        "",
        "---",
        "",
        "## 3. Food & Drink (counted only — no edges emitted)",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Rows seen | {f_rows_seen:,} |",
        f"| Rows with >=2 named referents (potential co-dining pairs) | {f_multi_named:,} |",
        "",
        "The Food & Drink table is high-noise / low-signal for edges. The 'Who Is",
        "Eating/Drinking' column is free-text and frequently describes groups rather",
        "than clean named pairs. Recommend deferred to a bounded LLM tail if food",
        "hospitality edges become a priority.",
        "",
        "**5 example rows (Who Is Eating/Drinking cell):**",
        "",
    ]
    for ex in f_examples[:5]:
        who = ex.get("who", "")
        report_lines.append(f"- `[{ex['chapter']}]` {who[:100]}")

    report_lines += [
        "",
        "---",
        "",
        "## 4. Events & Actions (counted only — prose-shaped)",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Numbered items corpus-wide | {ev_rows_seen:,} |",
        "",
        "Events & Actions is a numbered prose list with actor/action embedded in",
        "free text. Building a fragile regex to extract actor→target would be noisy.",
        "Recommendation: feed to a bounded LLM tail (estimated cost at S67 rate:",
        f"${ev_rows_seen * 0.0068:,.0f} if every item is an edge candidate, likely",
        "much lower after filtering to items with ≥2 named entities).",
        "",
        "**5 representative examples:**",
        "",
    ]
    for ex in ev_examples[:5]:
        report_lines.append(f"- `[{ex['chapter']}]` {ex['text'][:120]}")

    report_lines += [
        "",
        "---",
        "",
        "## 5. Information Revealed (counted only — table with free-text How Revealed)",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Rows seen | {i_rows_seen:,} |",
        "",
        "The 'How Revealed' column is free-text prose. The 'Known To (Characters)'",
        "column names characters but the relationship is 'knows fact X', not a direct",
        "binary graph edge. Recommendation: defer or feed to LLM with an INFORMED_OF",
        "edge type if this layer is needed for the knowledge graph.",
        "",
        "**5 representative examples (How Revealed column):**",
        "",
    ]
    for ex in i_examples[:5]:
        how = ""
        for k, v in ex["row"].items():
            if "how" in k:
                how = v
                break
        info_text = ""
        for k, v in ex["row"].items():
            if "information" in k or k == "information":
                info_text = v
                break
        report_lines.append(f"- `[{ex['chapter']}]` how=*{how[:80]}*")

    report_lines += [
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Table | Rows Seen | Deterministic Edges | Tail Rows | Counted Only |",
        "|-------|-----------|--------------------:|----------:|-------------|",
        f"| Hospitality & Guest Right | {h_rows_seen:,} | "
        f"{h_guest_of_emitted + h_violation_emitted:,} (GUEST_OF + VIOLATES) | — | — |",
        f"| Dialogue of Note | {d_rows_seen:,} | — | {d_tail_emitted:,} | — |",
        f"| Food & Drink | {f_rows_seen:,} | — | — | {f_rows_seen:,} |",
        f"| Events & Actions | {ev_rows_seen:,} | — | — | {ev_rows_seen:,} |",
        f"| Information Revealed | {i_rows_seen:,} | — | — | {i_rows_seen:,} |",
        "",
        f"**Total new deterministic edges: {total_deterministic:,}** (all GUEST_OF + VIOLATES_GUEST_RIGHT)",
        f"**Total new tail rows: {total_tail:,}** (Dialogue Speaker→Listener, untyped)",
        f"**Tail LLM cost estimate (S67 rate $0.0068/row): ${tail_cost_estimate:.2f}**",
        "",
        "Output path: `working/wiki/pass2-buckets/pass1-derived/_extra-tables/{book}/`",
        "",
        "---",
        "",
        f"> Generated by `scripts/stage4-pass1-extra-tables.py` on {produced_at}",
    ]

    WIKI_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_REPORT_MD.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(f"  Written: {OUT_REPORT_MD}")

    print()
    print(f"Done. {total_deterministic:,} deterministic + {total_tail:,} tail rows across {files_written:,} chapter files.")
    print(f"  GUEST_OF:             {h_guest_of_emitted:,}")
    print(f"  VIOLATES_GUEST_RIGHT: {h_violation_emitted:,}")
    print(f"  Dialogue tail:        {d_tail_emitted:,}  (est. ${tail_cost_estimate:.2f} to type at S67 rate)")
    print(f"  Report: {OUT_REPORT_MD}")


if __name__ == "__main__":
    main()
