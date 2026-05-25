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
  3. ## Food & Drink — entity-matched candidate pairs (candidate_kind=pass1_food).
  4. ## Events & Actions — entity-matched candidate pairs (candidate_kind=pass1_events).
  5. ## Information Revealed — entity-matched candidate pairs (candidate_kind=pass1_info).

All new candidates are written to a separate staging path so they are fully
separable from the canonical spine outputs:
  working/wiki/pass2-buckets/pass1-derived/_extra-tables/{book}/{chapter}.extra-tables.jsonl

All candidates now carry evidence_ref (sources/chapters/{book}/{chapter}.md:LINE)
+ locate_status (verbatim | chapter-level), anchored via the same locator logic
as the canonical spine.

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
from typing import Optional

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
CHAPTERS_DIR = REPO_ROOT / "sources" / "chapters"

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
# Evidence locator helpers (Task 2)
# Mirrors stage4-pass1-evidence-locator.py's logic; read-only, no imports needed.
# ---------------------------------------------------------------------------
_STOPWORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "must", "shall", "can",
    "not", "no", "nor", "so", "yet", "both", "either", "neither",
    "he", "she", "it", "they", "we", "you", "i", "his", "her", "its",
    "their", "our", "your", "my", "him", "them", "us", "me",
    "that", "this", "these", "those", "which", "who", "whom", "whose",
    "what", "when", "where", "why", "how", "all", "each", "every",
    "any", "some", "more", "most", "other", "then", "than", "too",
    "just", "up", "out", "about", "after", "before", "while", "also",
    "into", "through", "during", "between", "against", "over", "under",
    "again", "there", "here", "even", "down", "only", "very", "still",
    "back", "now", "always", "never", "once",
})
_MIN_SCORE_THRESHOLD = 0.15
_SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')


def _loc_content_words(text: str) -> set[str]:
    tokens = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    return {t for t in tokens if t not in _STOPWORDS}


def _loc_name_forms(slug: str) -> set[str]:
    forms: set[str] = set()
    parts = slug.split("-")
    forms.add(slug.lower())
    forms.add(slug.replace("-", " ").lower())
    for p in parts:
        if len(p) >= 3:
            forms.add(p.lower())
    return forms


def _read_chapter_prose(chapter_path: Path) -> list[tuple[int, str]]:
    """Read chapter file, skip YAML frontmatter, return (lineno, line) pairs."""
    try:
        raw_lines = chapter_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []

    in_frontmatter = False
    prose_lines: list[tuple[int, str]] = []
    for lineno, line in enumerate(raw_lines, start=1):
        stripped = line.strip()
        if lineno == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue
        if stripped:
            prose_lines.append((lineno, line))
    return prose_lines


def _split_into_sentences(prose_lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Split prose lines into (lineno, sentence) pairs."""
    sentences: list[tuple[int, str]] = []
    current_start: Optional[int] = None
    current_text: list[str] = []

    def _flush():
        nonlocal current_start, current_text
        if current_text:
            para_text = " ".join(current_text)
            parts = _SENTENCE_SPLIT_RE.split(para_text)
            for part in parts:
                part = part.strip()
                if part:
                    sentences.append((current_start, part))
            current_text = []
            current_start = None

    for lineno, line in prose_lines:
        text = line.strip()
        if not text:
            _flush()
            continue
        if current_start is None:
            current_start = lineno
        current_text.append(text)
    _flush()
    return sentences


def locate_evidence_for_candidate(
    source_slug: str,
    target_slug: str,
    hint_text: str,
    chapter_path: Path,
    chapter_rel: str,
) -> dict:
    """Find best verbatim passage in chapter prose for (source, target, hint).

    Returns dict with keys: evidence_quote, evidence_ref, locate_status.
    locate_status: 'verbatim' | 'chapter-level'.

    This is the same algorithm as stage4-pass1-evidence-locator.py's
    locate_evidence(), inlined here to avoid import cross-dependency.
    """
    source_forms = _loc_name_forms(source_slug)
    target_forms = _loc_name_forms(target_slug)
    hint_content = _loc_content_words(hint_text)

    all_query_terms = source_forms | target_forms | hint_content
    n_query = max(len(all_query_terms), 1)

    prose_lines = _read_chapter_prose(chapter_path)
    if not prose_lines:
        return {
            "evidence_quote": f"[PARAPHRASE] {hint_text}" if hint_text else "",
            "evidence_ref": chapter_rel,
            "locate_status": "chapter-level",
        }

    sentences = _split_into_sentences(prose_lines)
    if not sentences:
        return {
            "evidence_quote": f"[PARAPHRASE] {hint_text}" if hint_text else "",
            "evidence_ref": chapter_rel,
            "locate_status": "chapter-level",
        }

    best_score = -1.0
    best_sentence = ""
    best_lineno = 0

    for lineno, sent_text in sentences:
        sent_lower = sent_text.lower()
        sent_tokens = set(re.findall(r"\b[a-zA-Z]{2,}\b", sent_lower))

        name_hits = 0
        for form in source_forms:
            if form in sent_lower:
                name_hits += 1
                break
        for form in target_forms:
            if form in sent_lower:
                name_hits += 1
                break

        content_hits = len(hint_content & sent_tokens)
        score = (name_hits * 2 + content_hits) / n_query

        if score > best_score:
            best_score = score
            best_sentence = sent_text.strip()
            best_lineno = lineno

    if best_score >= _MIN_SCORE_THRESHOLD:
        return {
            "evidence_quote": best_sentence,
            "evidence_ref": f"{chapter_rel}:{best_lineno}",
            "locate_status": "verbatim",
        }
    else:
        return {
            "evidence_quote": f"[PARAPHRASE] {hint_text}" if hint_text else "",
            "evidence_ref": chapter_rel,
            "locate_status": "chapter-level",
        }


# ---------------------------------------------------------------------------
# Entity scanner: scan free text for resolved entity slugs.
# Used by the Events, Info, and Food candidate generators.
# ---------------------------------------------------------------------------

def _scan_text_for_entities(
    text: str,
    alias_map: dict,
    node_set: set,
    firstname_index: dict,
    importance_prior: dict,
    present_slugs: set,
) -> list[str]:
    """Scan text for entity name-forms, return list of resolved slugs in reading order.

    Uses resolve_name with full context. Deduplicates while preserving first-occurrence
    order. Applies GENERIC_TERMS check via STATUS_UNRESOLVED_GENERIC guard.

    Greedy multi-word matching: tries 3-word → 2-word → 1-word spans for each
    Title-cased token. A multi-word span is consumed (advances the cursor) ONLY
    when it resolves via a full-name match (EXACT or ALIAS status). FIRSTNAME_UNIQUE
    matches are accepted only for single-word spans — this prevents "Jon" from eating
    "Snow" into an "Arya Jon Snow" ghost span.

    Returns list of unique resolved slugs (AMBIGUOUS and UNRESOLVED excluded).
    """
    # Multi-word spans consumed only on these statuses (full-name match):
    _FULL_MATCH_STATUSES = (STATUS_EXACT, STATUS_ALIAS)

    all_tokens = re.findall(r"\b[A-Z][a-zA-Z'-]+\b", text)
    seen_slugs: dict[str, int] = {}  # slug → first occurrence position
    position = 0
    i = 0

    while i < len(all_tokens):
        resolved_slug = None
        advance_extra = 0  # how many extra positions to skip after this token

        # Try 3-word, 2-word, 1-word spans
        for span_len in (3, 2, 1):
            if i + span_len > len(all_tokens):
                continue
            candidate_name = " ".join(all_tokens[i:i + span_len])
            slug, status = resolve_name(
                candidate_name,
                alias_map=alias_map,
                node_set=node_set,
                firstname_index=firstname_index,
                prior=importance_prior,
                present_slugs=present_slugs,
            )
            if slug and status not in (STATUS_AMBIGUOUS, STATUS_UNRESOLVED, STATUS_UNRESOLVED_GENERIC):
                # For multi-word spans: only advance cursor on full-name matches.
                # For single-word spans: accept any non-ambiguous status.
                if span_len > 1 and status not in _FULL_MATCH_STATUSES:
                    # Firstname-unique on a multi-word span — fall through to shorter spans.
                    continue
                resolved_slug = slug
                advance_extra = span_len - 1  # outer loop adds 1 more
                break

        if resolved_slug and resolved_slug not in seen_slugs:
            seen_slugs[resolved_slug] = position
            position += 1
        i += 1 + advance_extra

    # Return in reading order
    return sorted(seen_slugs, key=lambda s: seen_slugs[s])


# ---------------------------------------------------------------------------
# Slug-quality gate (reusable / importable — also called by formalize step)
# ---------------------------------------------------------------------------

# Bare titles that should never be standalone endpoints (they are forms of
# address, not resolvable individuals).
_BARE_TITLE_SLUGS: frozenset[str] = frozenset({
    "ser", "lord", "lady", "king", "queen", "prince", "princess",
    "maester", "grand-maester", "septon", "septa", "high-septon",
    "father", "mother", "brother", "sister", "uncle", "aunt",
    "knight", "commander", "captain", "steward", "squire",
    "lord-commander", "high-septon",
})

# Known national/regional demonyms that appear as entity slugs but are not
# specific individuals.
_DEMONYM_PATTERN = re.compile(
    r"^(westerosi|dothraki|wildling|free-folk|unsullied|ironborn|"
    r"northerner|southron|valyrian|andal|first-men|"
    r"braavosi|lyseni|myrish|pentoshi|volantene|qartheen|"
    r"dornish|riverlander|stormlander|westerlander|crownlander)s?$",
    re.IGNORECASE,
)

# Known aliases that should route to cross-identity path rather than emit edges.
# These are in-universe identity aliases (not just titles), e.g. Arya's cover
# names, Sansa's alias identity.
_KNOWN_ALIAS_SLUGS: frozenset[str] = frozenset({
    "alayne",           # Sansa Stark alias
    "alayne-stone",     # Sansa Stark alias
    "nan",              # Arya Stark alias
    "arry",             # Arya Stark alias
    "weasel",           # Arya Stark alias
    "mercy",            # Arya Stark alias
    "cat-of-the-canals",  # Arya Stark alias
    "the-blind-girl",   # Arya Stark alias
    "reek",             # Theon Greyjoy alias (also a node for the alter-ego)
    "lord-reaper",      # Balon Greyjoy title-alias
    "no-one",           # Arya faceless alias
    "the-kindly-man",   # Faceless Man alias
    "the-waif",         # Faceless Man alias
})

# Toasts / phrases that look like names but aren't individuals.
# Pattern: all-for-X, long-may-X-reign, etc.
_TOAST_PHRASE_PATTERN = re.compile(
    r"^(all-for-|long-may-|glory-to-|praise-|for-the-)",
    re.IGNORECASE,
)


def is_low_quality_endpoint(slug: str) -> bool:
    """Return True if a slug should be routed to escalation rather than emitting an edge.

    Gates:
    1. Bare title slugs (ser, lord, king, maester, etc.) — forms of address, not individuals.
    2. Known aliases (alayne, reek, arry, etc.) — cross-identity paths handle these.
    3. National/regional demonyms (dothraki, wildling, etc.) — groups, not individuals.
    4. Toast/phrase patterns (all-for-joffrey, etc.) — not people.

    This function is intentionally importable and reusable for the formalize step
    that applies the same gate to already-computed edge sets.
    """
    if not slug:
        return True
    slug_lower = slug.lower().strip()

    # 1. Bare titles
    if slug_lower in _BARE_TITLE_SLUGS:
        return True

    # 2. Known aliases
    if slug_lower in _KNOWN_ALIAS_SLUGS:
        return True

    # 3. Demonyms
    if _DEMONYM_PATTERN.match(slug_lower):
        return True

    # 4. Toast/phrase patterns
    if _TOAST_PHRASE_PATTERN.match(slug_lower):
        return True

    return False


# ---------------------------------------------------------------------------
# Passive voice detection (direction-validation)
# ---------------------------------------------------------------------------

# Passive constructions that indicate the SUBJECT is the receiver, not actor.
# Used to flag direction-uncertain rows for escalation.
_PASSIVE_PATTERNS = re.compile(
    r"\b(was|were|is|are|been|being)\s+"
    r"(killed|told|informed|warned|threatened|betrayed|"
    r"manipulated|used|deceived|tricked|threatened|coerced|"
    r"advised|helped|saved|rescued|captured|arrested|imprisoned|"
    r"sent|given|shown|brought|taken|led|escorted|guarded|"
    r"named|called|appointed|crowned|knighted|wed|married|"
    r"revealed to|known to)\b",
    re.IGNORECASE,
)


def _has_passive_voice(text: str) -> bool:
    """Return True if the text contains a passive construction.

    Passive voice indicates the grammatical subject may be the receiver of the
    action rather than the actor, which means the direction heuristic
    "first-named entity = actor" is unreliable.
    """
    return bool(_PASSIVE_PATTERNS.search(text))


def _emit_entity_pair_candidates(
    slugs: list[str],
    candidate_kind: str,
    source_section: str,
    hint_raw: str,
    evidence_quote: str,
    evidence_context: str,
    chapter_slug: str,
    book_abbrev: str,
    pov_slug: str,
    extraction_rel: str,
    run_id: str,
    schema_version: str,
    produced_at: str,
    chapter_path: Path,
    chapter_rel: str,
) -> tuple[list[dict], list[dict]]:
    """Emit candidate pair rows from a resolved slug list.

    Direction heuristic v1: first slug = actor/source, each subsequent = target.
    Cap at first-actor → others fan-out (no full cartesian product).
    Requires >=2 distinct slugs to emit anything.

    Quality gates applied before emission:
    - is_low_quality_endpoint(): bare titles, known aliases, demonyms, toasts
      → routed to escalation (not emitted as candidates).
    - Passive voice in hint_raw → routed to escalation (direction uncertain).

    Returns (emit_rows, escalation_rows).
    Callers that previously expected only a list[dict] should unpack the tuple.
    """
    if len(slugs) < 2:
        return [], []

    actor = slugs[0]
    targets = slugs[1:]  # fan-out from first actor

    emit_rows: list[dict] = []
    escalation_rows: list[dict] = []

    # Check for passive voice in the hint — direction unreliable
    passive_flag = _has_passive_voice(hint_raw) or _has_passive_voice(evidence_quote)

    for target in targets:
        if target == actor:
            continue

        # Slug-quality gate
        low_quality_reason: str | None = None
        if is_low_quality_endpoint(actor):
            low_quality_reason = f"low-quality source slug: {actor!r}"
        elif is_low_quality_endpoint(target):
            low_quality_reason = f"low-quality target slug: {target!r}"
        elif passive_flag:
            low_quality_reason = "passive voice — direction uncertain"

        if low_quality_reason:
            escalation_rows.append({
                "decision": "escalate",
                "escalation_reason": low_quality_reason,
                "candidate_kind": candidate_kind,
                "source_section": source_section,
                "evidence_chapter": chapter_slug,
                "evidence_book": book_abbrev,
                "evidence_pov": pov_slug,
                "source_slug": actor,
                "target_slug": target,
                "hint_raw": hint_raw,
                "run_id": run_id,
                "schema_version": schema_version,
                "produced_at": produced_at,
            })
            continue

        # Locate evidence
        loc = locate_evidence_for_candidate(
            source_slug=actor,
            target_slug=target,
            hint_text=hint_raw,
            chapter_path=chapter_path,
            chapter_rel=chapter_rel,
        )
        cand = {
            "candidate_kind": candidate_kind,
            "source_section": source_section,
            "evidence_chapter": chapter_slug,
            "evidence_book": book_abbrev,
            "evidence_pov": pov_slug,
            "source_slug": actor,
            "source_resolution_status": "scan",
            "target_slug": target,
            "target_resolution_status": "scan",
            "edge_type": None,
            "typed_by": None,
            "qualifier": None,
            "hint_raw": hint_raw,
            "evidence_quote": loc["evidence_quote"],
            "evidence_context": evidence_context,
            "evidence_ref": loc["evidence_ref"],
            "locate_status": loc["locate_status"],
            "extraction_file": extraction_rel,
            "run_id": run_id,
            "schema_version": schema_version,
            "produced_at": produced_at,
        }
        emit_rows.append(cand)
    return emit_rows, escalation_rows


# ---------------------------------------------------------------------------
# Task 1: Events & Actions candidate generator
# ---------------------------------------------------------------------------

def generate_events_candidates(
    event_items: list[str],
    chapter_slug: str,
    book_abbrev: str,
    pov_slug: str,
    extraction_rel: str,
    alias_map: dict,
    node_set: set,
    firstname_index: dict,
    importance_prior: dict,
    present_slugs: set,
    chapter_path: Path,
    chapter_rel: str,
    run_id: str,
    schema_version: str,
    produced_at: str,
) -> tuple[list[dict], int, int, int, list[dict]]:
    """Generate pass1_events candidate pairs from Events & Actions numbered items.

    Returns (candidates, rows_with_2plus_entities, rows_dropped, rows_escalated,
             escalation_rows).
    """
    candidates: list[dict] = []
    escalation_rows: list[dict] = []
    rows_with_2plus = 0
    rows_dropped = 0
    rows_escalated = 0

    for item_text in event_items:
        # Strip leading number + bold marker: "1. **Name** — prose"
        # hint_raw = the full item text (no number prefix)
        hint_raw = re.sub(r"^\d+\.\s+", "", item_text).strip()

        slugs = _scan_text_for_entities(
            hint_raw, alias_map, node_set, firstname_index, importance_prior, present_slugs
        )

        if len(slugs) < 2:
            rows_dropped += 1
            continue

        rows_with_2plus += 1
        pairs, escals = _emit_entity_pair_candidates(
            slugs=slugs,
            candidate_kind="pass1_events",
            source_section="Events & Actions",
            hint_raw=hint_raw,
            evidence_quote=hint_raw,
            evidence_context="",
            chapter_slug=chapter_slug,
            book_abbrev=book_abbrev,
            pov_slug=pov_slug,
            extraction_rel=extraction_rel,
            run_id=run_id,
            schema_version=schema_version,
            produced_at=produced_at,
            chapter_path=chapter_path,
            chapter_rel=chapter_rel,
        )
        candidates.extend(pairs)
        escalation_rows.extend(escals)
        rows_escalated += len(escals)

    return candidates, rows_with_2plus, rows_dropped, rows_escalated, escalation_rows


# ---------------------------------------------------------------------------
# Task 1: Information Revealed candidate generator
# ---------------------------------------------------------------------------

def generate_info_candidates(
    info_rows: list[dict],
    chapter_slug: str,
    book_abbrev: str,
    pov_slug: str,
    extraction_rel: str,
    alias_map: dict,
    node_set: set,
    firstname_index: dict,
    importance_prior: dict,
    present_slugs: set,
    chapter_path: Path,
    chapter_rel: str,
    run_id: str,
    schema_version: str,
    produced_at: str,
) -> tuple[list[dict], int, int, int, list[dict]]:
    """Generate pass1_info candidate pairs from Information Revealed table rows.

    Scans: Information column + Known To (Characters) column.
    How Revealed column → evidence_context.
    Returns (candidates, rows_with_2plus_entities, rows_dropped, rows_escalated,
             escalation_rows).
    """
    candidates: list[dict] = []
    escalation_rows: list[dict] = []
    rows_with_2plus = 0
    rows_dropped = 0
    rows_escalated = 0

    for row in info_rows:
        # Identify columns by partial key match (headers may vary slightly)
        info_text = ""
        known_to = ""
        how_revealed = ""
        for k, v in row.items():
            kl = k.lower()
            if "information" in kl and not info_text:
                info_text = v or ""
            elif "known to" in kl or ("known" in kl and "character" in kl):
                known_to = v or ""
            elif "how" in kl:
                how_revealed = v or ""

        # Scan: info_text + known_to together for entity names
        combined_scan = f"{info_text} {known_to}"
        hint_raw = info_text.strip() if info_text.strip() else combined_scan.strip()
        evidence_context = how_revealed.strip()

        slugs = _scan_text_for_entities(
            combined_scan, alias_map, node_set, firstname_index, importance_prior, present_slugs
        )

        if len(slugs) < 2:
            rows_dropped += 1
            continue

        rows_with_2plus += 1
        pairs, escals = _emit_entity_pair_candidates(
            slugs=slugs,
            candidate_kind="pass1_info",
            source_section="Information Revealed",
            hint_raw=hint_raw,
            evidence_quote=info_text,
            evidence_context=evidence_context,
            chapter_slug=chapter_slug,
            book_abbrev=book_abbrev,
            pov_slug=pov_slug,
            extraction_rel=extraction_rel,
            run_id=run_id,
            schema_version=schema_version,
            produced_at=produced_at,
            chapter_path=chapter_path,
            chapter_rel=chapter_rel,
        )
        candidates.extend(pairs)
        escalation_rows.extend(escals)
        rows_escalated += len(escals)

    return candidates, rows_with_2plus, rows_dropped, rows_escalated, escalation_rows


# ---------------------------------------------------------------------------
# Task 1: Food & Drink candidate generator
# ---------------------------------------------------------------------------

def generate_food_candidates(
    food_rows: list[dict],
    chapter_slug: str,
    book_abbrev: str,
    pov_slug: str,
    extraction_rel: str,
    alias_map: dict,
    node_set: set,
    firstname_index: dict,
    importance_prior: dict,
    present_slugs: set,
    chapter_path: Path,
    chapter_rel: str,
    run_id: str,
    schema_version: str,
    produced_at: str,
) -> tuple[list[dict], int, int, int, list[dict]]:
    """Generate pass1_food candidate pairs from Food & Drink table rows.

    Primary source: "Who Is Eating/Drinking" column (most entity-rich).
    Also scans Meal/Occasion column.
    Returns (candidates, rows_with_2plus_entities, rows_dropped, rows_escalated,
             escalation_rows).
    """
    candidates: list[dict] = []
    escalation_rows: list[dict] = []
    rows_with_2plus = 0
    rows_dropped = 0
    rows_escalated = 0

    for row in food_rows:
        # Find "Who Is Eating/Drinking" column
        who_text = ""
        meal_text = ""
        for k, v in row.items():
            kl = k.lower()
            if _WHO_EATING_PATTERNS.search(kl):
                who_text = v or ""
            elif "meal" in kl or "occasion" in kl:
                meal_text = v or ""

        # Scan the "who" column primarily; fall back to whole row if who is empty
        scan_text = who_text if who_text.strip() else " ".join(v for v in row.values() if v)
        # hint_raw = who column (or meal desc as fallback)
        hint_raw = who_text.strip() if who_text.strip() else meal_text.strip()

        slugs = _scan_text_for_entities(
            scan_text, alias_map, node_set, firstname_index, importance_prior, present_slugs
        )

        if len(slugs) < 2:
            rows_dropped += 1
            continue

        rows_with_2plus += 1
        pairs, escals = _emit_entity_pair_candidates(
            slugs=slugs,
            candidate_kind="pass1_food",
            source_section="Food & Drink",
            hint_raw=hint_raw,
            evidence_quote=who_text,
            evidence_context=meal_text,
            chapter_slug=chapter_slug,
            book_abbrev=book_abbrev,
            pov_slug=pov_slug,
            extraction_rel=extraction_rel,
            run_id=run_id,
            schema_version=schema_version,
            produced_at=produced_at,
            chapter_path=chapter_path,
            chapter_rel=chapter_rel,
        )
        candidates.extend(pairs)
        escalation_rows.extend(escals)
        rows_escalated += len(escals)

    return candidates, rows_with_2plus, rows_dropped, rows_escalated, escalation_rows


# ---------------------------------------------------------------------------
# Task 2: Locator anchoring for Dialogue + Hospitality rows
# (Events/Info/Food already anchored inside their generators above.)
# ---------------------------------------------------------------------------

def _anchor_candidate_locator(
    cand: dict,
    chapter_path: Path,
    chapter_rel: str,
) -> dict:
    """Attach evidence_ref + locate_status to an existing candidate dict (in-place).

    Uses hint_raw + evidence_quote as the hint text for content-word matching.
    Only sets fields if they are not already present.
    Returns the modified candidate.
    """
    if "evidence_ref" in cand and cand["evidence_ref"]:
        return cand  # already anchored

    hint_text = " ".join(filter(None, [
        cand.get("hint_raw", ""),
        cand.get("evidence_quote", ""),
        cand.get("evidence_context", ""),
        cand.get("evidence_event", ""),
        cand.get("evidence_type_raw", ""),
        cand.get("evidence_details", ""),
    ]))

    source_slug = cand.get("source_slug", "")
    target_slug = cand.get("target_slug", "")

    if not chapter_path.exists():
        cand["evidence_ref"] = chapter_rel
        cand["locate_status"] = "chapter-level"
        return cand

    loc = locate_evidence_for_candidate(
        source_slug=source_slug,
        target_slug=target_slug,
        hint_text=hint_text,
        chapter_path=chapter_path,
        chapter_rel=chapter_rel,
    )
    cand["evidence_ref"] = loc["evidence_ref"]
    cand["locate_status"] = loc["locate_status"]
    # Update evidence_quote with the located sentence if we found a verbatim match
    # and the candidate didn't already have a substantive quote.
    if loc["locate_status"] == "verbatim" and not cand.get("evidence_quote"):
        cand["evidence_quote"] = loc["evidence_quote"]
    return cand


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
    f_rows_with_2plus = 0
    f_rows_dropped = 0
    f_candidates_emitted = 0
    f_verbatim = 0
    f_chapter_level = 0

    # Events counters
    ev_rows_seen = 0
    ev_examples: list[str] = []
    ev_rows_with_2plus = 0
    ev_rows_dropped = 0
    ev_candidates_emitted = 0
    ev_verbatim = 0
    ev_chapter_level = 0

    # Info counters
    i_rows_seen = 0
    i_examples: list[dict] = []
    i_rows_with_2plus = 0
    i_rows_dropped = 0
    i_candidates_emitted = 0
    i_verbatim = 0
    i_chapter_level = 0

    # Locator stats for Dialogue + Hospitality (anchored retroactively)
    d_verbatim = 0
    d_chapter_level = 0
    h_verbatim = 0
    h_chapter_level = 0

    # Per-book stats
    book_stats: dict[str, dict] = {b: collections.Counter() for b in BOOKS}

    # Escalation counters (direction-uncertain + low-quality endpoint rows)
    f_escalated = 0
    ev_escalated_total = 0
    i_escalated_total = 0

    # Per-chapter output collections
    # {chapter_slug: (book, [candidate_row_dict, ...])}
    chapter_extra: dict[str, tuple[str, list[dict]]] = {}
    # {chapter_slug: (book, [escalation_row_dict, ...])}  — written separately
    chapter_escalations: dict[str, tuple[str, list[dict]]] = {}

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

        # Chapter prose path (for locator anchoring)
        chapter_path = CHAPTERS_DIR / book_abbrev / f"{chapter_slug}.md"
        chapter_rel = f"sources/chapters/{book_abbrev}/{chapter_slug}.md"

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
                            # Task 2: anchor locator
                            _anchor_candidate_locator(cand, chapter_path, chapter_rel)
                            if cand.get("locate_status") == "verbatim":
                                h_verbatim += 1
                            else:
                                h_chapter_level += 1
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
                    # Task 2: anchor locator
                    _anchor_candidate_locator(cand, chapter_path, chapter_rel)
                    if cand.get("locate_status") == "verbatim":
                        h_verbatim += 1
                    else:
                        h_chapter_level += 1
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
            # Task 2: anchor locator
            _anchor_candidate_locator(cand, chapter_path, chapter_rel)
            if cand.get("locate_status") == "verbatim":
                d_verbatim += 1
            else:
                d_chapter_level += 1
            chapter_rows.append(cand)

        # -----------------------------------------------------------------
        # 4c. Food & Drink — entity-matched candidate pairs (Task 1)
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

        food_cands, food_2plus, food_dropped, food_escalated, food_escals = generate_food_candidates(
            food_rows=food_rows,
            chapter_slug=chapter_slug,
            book_abbrev=book_abbrev,
            pov_slug=pov_slug,
            extraction_rel=extraction_rel,
            alias_map=alias_to_canonical,
            node_set=node_slug_set,
            firstname_index=firstname_index,
            importance_prior=importance_prior,
            present_slugs=present_slugs,
            chapter_path=chapter_path,
            chapter_rel=chapter_rel,
            run_id=run_id,
            schema_version=schema_version,
            produced_at=produced_at,
        )
        f_rows_with_2plus += food_2plus
        f_rows_dropped += food_dropped
        f_candidates_emitted += len(food_cands)
        for c in food_cands:
            if c.get("locate_status") == "verbatim":
                f_verbatim += 1
            else:
                f_chapter_level += 1
        chapter_rows.extend(food_cands)
        book_stats[book_abbrev]["food_candidates"] += len(food_cands)
        book_stats[book_abbrev]["food_escalated"] += food_escalated
        if food_escals:
            if chapter_slug not in chapter_escalations:
                chapter_escalations[chapter_slug] = (book_abbrev, [])
            chapter_escalations[chapter_slug][1].extend(food_escals)

        # -----------------------------------------------------------------
        # 4d. Events & Actions — entity-matched candidate pairs (Task 1)
        # -----------------------------------------------------------------
        ev_rows_seen += len(event_items)
        if len(ev_examples) < 5:
            for item in event_items[:5]:
                if len(ev_examples) >= 5:
                    break
                ev_examples.append({"chapter": chapter_slug, "text": item})

        events_cands, ev_2plus, ev_dropped, ev_escalated, ev_escals = generate_events_candidates(
            event_items=event_items,
            chapter_slug=chapter_slug,
            book_abbrev=book_abbrev,
            pov_slug=pov_slug,
            extraction_rel=extraction_rel,
            alias_map=alias_to_canonical,
            node_set=node_slug_set,
            firstname_index=firstname_index,
            importance_prior=importance_prior,
            present_slugs=present_slugs,
            chapter_path=chapter_path,
            chapter_rel=chapter_rel,
            run_id=run_id,
            schema_version=schema_version,
            produced_at=produced_at,
        )
        ev_rows_with_2plus += ev_2plus
        ev_rows_dropped += ev_dropped
        ev_candidates_emitted += len(events_cands)
        for c in events_cands:
            if c.get("locate_status") == "verbatim":
                ev_verbatim += 1
            else:
                ev_chapter_level += 1
        chapter_rows.extend(events_cands)
        book_stats[book_abbrev]["events_candidates"] += len(events_cands)
        book_stats[book_abbrev]["events_escalated"] += ev_escalated
        if ev_escals:
            if chapter_slug not in chapter_escalations:
                chapter_escalations[chapter_slug] = (book_abbrev, [])
            chapter_escalations[chapter_slug][1].extend(ev_escals)

        # -----------------------------------------------------------------
        # 4e. Information Revealed — entity-matched candidate pairs (Task 1)
        # -----------------------------------------------------------------
        i_rows_seen += len(info_rows)
        if len(i_examples) < 5:
            for r in info_rows[:5]:
                if len(i_examples) >= 5:
                    break
                i_examples.append({"chapter": chapter_slug, "row": r})

        info_cands, info_2plus, info_dropped, info_escalated, info_escals = generate_info_candidates(
            info_rows=info_rows,
            chapter_slug=chapter_slug,
            book_abbrev=book_abbrev,
            pov_slug=pov_slug,
            extraction_rel=extraction_rel,
            alias_map=alias_to_canonical,
            node_set=node_slug_set,
            firstname_index=firstname_index,
            importance_prior=importance_prior,
            present_slugs=present_slugs,
            chapter_path=chapter_path,
            chapter_rel=chapter_rel,
            run_id=run_id,
            schema_version=schema_version,
            produced_at=produced_at,
        )
        i_rows_with_2plus += info_2plus
        i_rows_dropped += info_dropped
        i_candidates_emitted += len(info_cands)
        for c in info_cands:
            if c.get("locate_status") == "verbatim":
                i_verbatim += 1
            else:
                i_chapter_level += 1
        chapter_rows.extend(info_cands)
        book_stats[book_abbrev]["info_candidates"] += len(info_cands)
        book_stats[book_abbrev]["info_escalated"] += info_escalated
        if info_escals:
            if chapter_slug not in chapter_escalations:
                chapter_escalations[chapter_slug] = (book_abbrev, [])
            chapter_escalations[chapter_slug][1].extend(info_escals)

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
    total_untyped_new = d_tail_emitted + ev_candidates_emitted + i_candidates_emitted + f_candidates_emitted

    # Dialogue LLM cost estimate at S67 observed rate: $0.0068/row
    tail_cost_estimate = total_untyped_new * 0.0068

    emitted_violations = [r for r in h_violation_rows_detail if r["emitted"]]
    unemitted_violations = [r for r in h_violation_rows_detail if not r["emitted"]]

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
    h_total_anchored = h_verbatim + h_chapter_level
    h_verbatim_pct = 100.0 * h_verbatim / h_total_anchored if h_total_anchored else 0.0
    print(f"  Locator verbatim:              {h_verbatim:>8,}  ({h_verbatim_pct:.1f}% of anchored)")
    print()
    print("  GUEST_OF qualifier distribution:")
    for qual, cnt in sorted(h_qualifier_dist.items(), key=lambda x: -x[1]):
        print(f"    {cnt:>6,}  {qual}")
    print()
    print("  VIOLATES_GUEST_RIGHT candidates (flagged violations, emitted where resolvable):")
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
    d_total = d_verbatim + d_chapter_level
    d_vb_pct = 100.0 * d_verbatim / d_total if d_total else 0.0
    print(f"  Locator verbatim:              {d_verbatim:>8,}  ({d_vb_pct:.1f}% of emitted)")
    print()
    print("--- Food & Drink (Task 1 — entity-matched pairs) ---")
    print(f"  Rows seen:                     {f_rows_seen:>8,}")
    print(f"  Rows with >=2 named referents: {f_multi_named:>8,}  (heuristic, pre-resolver)")
    print(f"  Rows with >=2 resolved slugs:  {f_rows_with_2plus:>8,}")
    print(f"  Rows dropped (<2 resolved):    {f_rows_dropped:>8,}")
    print(f"  Candidate pairs emitted:       {f_candidates_emitted:>8,}")
    total_f_escalated = sum(bs.get("food_escalated", 0) for bs in book_stats.values())
    print(f"  Escalated (slug/passive gate): {total_f_escalated:>8,}")
    f_total = f_verbatim + f_chapter_level
    f_vb_pct = 100.0 * f_verbatim / f_total if f_total else 0.0
    print(f"  Locator verbatim:              {f_verbatim:>8,}  ({f_vb_pct:.1f}% of emitted)")
    print("  Examples (first 5 rows):")
    for ex in f_examples[:5]:
        who = ex.get("who", "")[:80]
        print(f"    [{ex['chapter']}] who={who!r}")
    print()
    print("--- Events & Actions (Task 1 — entity-matched pairs) ---")
    print(f"  Numbered items:                {ev_rows_seen:>8,}")
    print(f"  Items with >=2 resolved slugs: {ev_rows_with_2plus:>8,}")
    print(f"  Items dropped (<2 resolved):   {ev_rows_dropped:>8,}")
    print(f"  Candidate pairs emitted:       {ev_candidates_emitted:>8,}")
    total_ev_escalated = sum(bs.get("events_escalated", 0) for bs in book_stats.values())
    print(f"  Escalated (slug/passive gate): {total_ev_escalated:>8,}")
    ev_total = ev_verbatim + ev_chapter_level
    ev_vb_pct = 100.0 * ev_verbatim / ev_total if ev_total else 0.0
    print(f"  Locator verbatim:              {ev_verbatim:>8,}  ({ev_vb_pct:.1f}% of emitted)")
    print("  Examples (first 5):")
    for ex in ev_examples[:5]:
        print(f"    [{ex['chapter']}] {ex['text'][:100]}")
    print()
    print("--- Information Revealed (Task 1 — entity-matched pairs) ---")
    print(f"  Rows seen:                     {i_rows_seen:>8,}")
    print(f"  Rows with >=2 resolved slugs:  {i_rows_with_2plus:>8,}")
    print(f"  Rows dropped (<2 resolved):    {i_rows_dropped:>8,}")
    print(f"  Candidate pairs emitted:       {i_candidates_emitted:>8,}")
    total_i_escalated = sum(bs.get("info_escalated", 0) for bs in book_stats.values())
    print(f"  Escalated (slug/passive gate): {total_i_escalated:>8,}")
    i_total = i_verbatim + i_chapter_level
    i_vb_pct = 100.0 * i_verbatim / i_total if i_total else 0.0
    print(f"  Locator verbatim:              {i_verbatim:>8,}  ({i_vb_pct:.1f}% of emitted)")
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
    print(f"  New TAIL rows — Dialogue:      {d_tail_emitted:>8,}")
    print(f"  New TAIL rows — Events:        {ev_candidates_emitted:>8,}")
    print(f"  New TAIL rows — Info:          {i_candidates_emitted:>8,}")
    print(f"  New TAIL rows — Food:          {f_candidates_emitted:>8,}")
    print(f"  Total new untyped tail rows:   {total_untyped_new:>8,}")
    print(f"  Total extra candidates:        {total_deterministic + total_untyped_new:>8,}")
    print(f"  LLM cost if typed (S67 rate):  ${tail_cost_estimate:>7.2f}")
    print()

    per_book_header = (
        f"{'Book':<6}  {'GUEST_OF':>10}  {'violation':>10}  "
        f"{'diag_tail':>10}  {'events':>8}  {'info':>8}  {'food':>8}"
    )
    print("Per-book breakdown:")
    print(f"  {per_book_header}")
    for book in BOOKS:
        if args.book and book != args.book:
            continue
        bs = book_stats[book]
        print(
            f"  {book.upper():<6}  {bs.get('guest_of_emitted', 0):>10,}  "
            f"{bs.get('violation_emitted', 0):>10,}  "
            f"{bs.get('dialogue_tail', 0):>10,}  "
            f"{bs.get('events_candidates', 0):>8,}  "
            f"{bs.get('info_candidates', 0):>8,}  "
            f"{bs.get('food_candidates', 0):>8,}"
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

    # 6a-ii. Per-chapter escalation JSONL (low-quality endpoints + passive voice)
    OUT_ESCALATE_DIR = OUT_EXTRA_BASE_DIR.parent / "_extra-tables-escalated"
    escal_files_written = 0
    escal_rows_written = 0
    for chapter_slug, (book_abbrev, rows) in sorted(chapter_escalations.items()):
        if not rows:
            continue
        out_dir = OUT_ESCALATE_DIR / book_abbrev
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{chapter_slug}.escalated.jsonl"
        with out_file.open("w", encoding="utf-8") as fh:
            for row in sorted(rows, key=lambda r: (r["source_slug"], r["target_slug"])):
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        escal_files_written += 1
        escal_rows_written += len(rows)
    if escal_rows_written:
        print(f"  {escal_files_written:,} escalation files, {escal_rows_written:,} escalated rows → {OUT_ESCALATE_DIR.name}/")

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
        f"| Locator verbatim match | {d_verbatim:,} ({d_vb_pct:.1f}%) |",
        f"| LLM cost if typed (S67 rate ≈ $0.0068/row) | ${d_tail_emitted * 0.0068:.2f} |",
        "",
        "Edge type is NOT deterministic from the Dialogue table — the quote/context",
        "is the hint for a future LLM tail step. All rows carry evidence_ref.",
        "",
        "---",
        "",
        "## 3. Food & Drink (Task 1 — entity-matched pairs)",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Rows seen | {f_rows_seen:,} |",
        f"| Rows with >=2 named referents (heuristic) | {f_multi_named:,} |",
        f"| Rows with >=2 resolved slugs | {f_rows_with_2plus:,} |",
        f"| Rows dropped (<2 resolved) | {f_rows_dropped:,} |",
        f"| **Candidate pairs emitted** | **{f_candidates_emitted:,}** |",
        f"| Locator verbatim match | {f_verbatim:,} ({f_vb_pct:.1f}%) |",
        "",
        "The Food & Drink table is medium-noise for edges. The 'Who Is Eating/Drinking'",
        "column is the primary entity source; group cells (e.g. 'All guests') are",
        "filtered by the resolver's GENERIC_TERMS stoplist.",
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
        "## 4. Events & Actions (Task 1 — entity-matched pairs)",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Numbered items corpus-wide | {ev_rows_seen:,} |",
        f"| Items with >=2 resolved slugs | {ev_rows_with_2plus:,} |",
        f"| Items dropped (<2 resolved) | {ev_rows_dropped:,} |",
        f"| **Candidate pairs emitted** | **{ev_candidates_emitted:,}** |",
        f"| Locator verbatim match | {ev_verbatim:,} ({ev_vb_pct:.1f}%) |",
        "",
        "Events & Actions is a numbered prose list with actor/action embedded in",
        "free text. The >=2-entity filter is the primary noise cut. Direction heuristic:",
        "first-resolved entity = actor/source; subsequent distinct entities = targets.",
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
        "## 5. Information Revealed (Task 1 — entity-matched pairs)",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Rows seen | {i_rows_seen:,} |",
        f"| Rows with >=2 resolved slugs | {i_rows_with_2plus:,} |",
        f"| Rows dropped (<2 resolved) | {i_rows_dropped:,} |",
        f"| **Candidate pairs emitted** | **{i_candidates_emitted:,}** |",
        f"| Locator verbatim match | {i_verbatim:,} ({i_vb_pct:.1f}%) |",
        "",
        "The 'Known To (Characters)' column is the primary entity source, combined",
        "with the Information column. The edge direction is: first entity in reading",
        "order → subsequent entities (actor = information holder or revealer).",
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
        report_lines.append(f"- `[{ex['chapter']}]` how=*{how[:80]}*")

    report_lines += [
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Table | Rows Seen | Deterministic Edges | Tail Rows (untyped) | Verbatim% |",
        "|-------|-----------|--------------------:|--------------------:|----------:|",
        f"| Hospitality & Guest Right | {h_rows_seen:,} | "
        f"{h_guest_of_emitted + h_violation_emitted:,} (GUEST_OF + VIOLATES) | — | {h_verbatim_pct:.1f}% |",
        f"| Dialogue of Note | {d_rows_seen:,} | — | {d_tail_emitted:,} | {d_vb_pct:.1f}% |",
        f"| Food & Drink | {f_rows_seen:,} | — | {f_candidates_emitted:,} | {f_vb_pct:.1f}% |",
        f"| Events & Actions | {ev_rows_seen:,} | — | {ev_candidates_emitted:,} | {ev_vb_pct:.1f}% |",
        f"| Information Revealed | {i_rows_seen:,} | — | {i_candidates_emitted:,} | {i_vb_pct:.1f}% |",
        "",
        f"**Total new deterministic edges: {total_deterministic:,}** (GUEST_OF + VIOLATES_GUEST_RIGHT)",
        f"**Total new untyped tail rows: {total_untyped_new:,}** "
        f"(Dialogue {d_tail_emitted:,} + Events {ev_candidates_emitted:,} + Info {i_candidates_emitted:,} + Food {f_candidates_emitted:,})",
        f"**Tail LLM cost estimate (S67 rate $0.0068/row): ${tail_cost_estimate:.2f}**",
        "",
        "All candidates carry `evidence_ref` (sources/chapters/{book}/{chapter}.md:LINE) + `locate_status`.",
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
    print(
        f"Done. {total_deterministic:,} deterministic + {total_untyped_new:,} untyped tail rows "
        f"across {files_written:,} chapter files."
    )
    print(f"  GUEST_OF:             {h_guest_of_emitted:,}")
    print(f"  VIOLATES_GUEST_RIGHT: {h_violation_emitted:,}")
    print(f"  Dialogue tail:        {d_tail_emitted:,}")
    print(f"  Events tail:          {ev_candidates_emitted:,}")
    print(f"  Info tail:            {i_candidates_emitted:,}")
    print(f"  Food tail:            {f_candidates_emitted:,}")
    print(f"  LLM cost (all untyped, S67 rate): ${tail_cost_estimate:.2f}")
    print(f"  Report: {OUT_REPORT_MD}")


if __name__ == "__main__":
    main()
