#!/usr/bin/env python3
"""dunk-egg-graph-ingest.py — D&E Pass-1 graph-ingest track: deterministic candidate builder.

Parses the 24 Dunk & Egg Pass-1 extraction files (thk/tss/tmk, whole-novella
single-chapter units split into -pNN parts), resolves character names to
existing graph node slugs, grounds evidence quotes to chapter:line citations
in the whole-novella source files, dedups against live edges.jsonl, and
emits candidate edge rows + an alias-add worklist.

DRY-RUN BY DESIGN: this script never writes to graph/, sources/, or
extractions/. All outputs land under working/dunk-egg-graph-ingest/out/.

Reuses (imports, does not modify):
  - scripts/stage4_name_resolver.py   — five-rung name -> slug resolver
  - reference/architecture.md         — locked edge-type vocabulary (parsed)
  - reference/edge-qualifier-vocab.md — Tier-1/Tier-2/Tier-3 qualifier rules

No LLM calls. No network. Deterministic stdlib-only Python.

Usage:
  python3 scripts/dunk-egg-graph-ingest.py
  python3 scripts/dunk-egg-graph-ingest.py --map working/dunk-egg-graph-ingest/curated-map.csv
  python3 scripts/dunk-egg-graph-ingest.py --out-dir /tmp/de-ingest-test

Subcommands (added S222 follow-up — default dry-run ingest above is unchanged):

  --assemble-final
      Reads out/emit.jsonl + repass-verdicts-s222.jsonl + out/alias-adds.jsonl,
      applies REJECT/FIX verdicts, re-dedups, splits out anything now matching
      live graph/edges/edges.jsonl, and applies the alias reject-list +
      already-present + graph-wide-collision guards. Writes out/final-edges.jsonl,
      out/final-overlay.jsonl, out/final-aliases.jsonl, out/FINAL-STATS.md.
      Still writes only under working/ — never graph/.
      python3 scripts/dunk-egg-graph-ingest.py --assemble-final

  --apply
      Mutates the graph: backs up graph/edges/edges.jsonl, appends
      out/final-edges.jsonl rows, and inserts out/final-aliases.jsonl entries
      into each target node's `aliases:` frontmatter (idempotent). Orchestrator-
      gated — refuses to run twice (detects RUN_ID already in edges.jsonl).
      python3 scripts/dunk-egg-graph-ingest.py --apply
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Reuse: stage4_name_resolver.py (underscore filename, hyphen-safe import)
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
_RESOLVER_PATH = REPO_ROOT / "scripts" / "stage4_name_resolver.py"
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
    to_slug,
    _clean_raw_name,
    STATUS_AMBIGUOUS,
    STATUS_UNRESOLVED,
    STATUS_UNRESOLVED_GENERIC,
)

# ---------------------------------------------------------------------------
# Reuse: stage4-pass1-evidence-locator.py — sentence-level prose reader
# (hyphenated filename -> importlib, same pattern as the resolver above).
# We reuse its `read_chapter_prose` + `split_into_sentences` for tight,
# sentence-granular quote grounding rather than reinventing paragraph
# splitting; our own grounding/scoring logic (below) is D&E-specific
# (multi-fragment + ellipsis + curated-map aware) so it is not reused as-is.
# ---------------------------------------------------------------------------
_EVLOC_PATH = REPO_ROOT / "scripts" / "stage4-pass1-evidence-locator.py"
_evloc_spec = importlib.util.spec_from_file_location("stage4_pass1_evidence_locator", _EVLOC_PATH)
_evloc_mod = importlib.util.module_from_spec(_evloc_spec)
sys.modules["stage4_pass1_evidence_locator"] = _evloc_mod
_evloc_spec.loader.exec_module(_evloc_mod)

read_chapter_prose = _evloc_mod.read_chapter_prose
split_into_sentences = _evloc_mod.split_into_sentences

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
GRAPH_NODES_DIR = REPO_ROOT / "graph" / "nodes"
GRAPH_EDGES_PATH = REPO_ROOT / "graph" / "edges" / "edges.jsonl"
EXTRACTIONS_DIR = REPO_ROOT / "extractions" / "mechanical"
CHAPTERS_DIR = REPO_ROOT / "sources" / "chapters"
ALIAS_PATH = REPO_ROOT / "working" / "wiki" / "data" / "alias-resolver.json"
BACKLINKS_PATH = REPO_ROOT / "working" / "wiki" / "data" / "backlink-counts.json"
ARCH_MD = REPO_ROOT / "reference" / "architecture.md"
QUAL_VOCAB_MD = REPO_ROOT / "reference" / "edge-qualifier-vocab.md"

TRACK_DIR = REPO_ROOT / "working" / "dunk-egg-graph-ingest"
DEFAULT_CURATED_MAP = TRACK_DIR / "curated-map.csv"
DEFAULT_OUT_DIR = TRACK_DIR / "out"
DEFAULT_VERDICTS_PATH = TRACK_DIR / "repass-verdicts-s222.jsonl"

BOOKS = ["thk", "tss", "tmk"]

# ---------------------------------------------------------------------------
# --assemble-final: explicit alias reject-list (Matt/repass-directed drops)
# ---------------------------------------------------------------------------
ALIAS_REJECT_PAIRS: frozenset[tuple[str, str]] = frozenset({
    ("arlan-of-pennytree", "the old man"),
    ("arlan-of-pennytree", "old man"),
    ("aegon-v-targaryen", "aegon"),
    ("aegon-v-targaryen", "aegon targaryen"),
    ("daemon-ii-blackfyre", "the pretender"),
    ("daemon-ii-blackfyre", "pretender"),
    ("wet-wat", "the younger wat brother"),
    ("wet-wat", "younger wat brother"),
})
ALIAS_REJECT_SLUGS_ANY: frozenset[str] = frozenset({"damon-lannister"})

_SKIP_DIRS = {"_conflicts", "_unclassified", "_stage3-preview"}

RUN_ID = "dunk-egg-pass1-derived-s222"
SCHEMA_VERSION = "pass1-derived-v1"
TYPED_BY = "pass1-locked-vocab"

HONORIFICS = ["Ser ", "Lord ", "Lady ", "King ", "Prince ", "Maester "]

IDENTITY_TYPES = {"SAME_AS", "ALIAS_OF"}

MIN_FRAG_CHARS = 6
MIN_LITERAL_WORDS = 6


# ---------------------------------------------------------------------------
# Locked edge vocabulary (from architecture.md) — same extraction approach as
# scripts/stage4-pass1-edge-candidates.py's load_locked_vocab()
# ---------------------------------------------------------------------------
def load_locked_vocab(arch_path: Path) -> frozenset[str]:
    text = arch_path.read_text(encoding="utf-8", errors="replace")
    tokens = re.findall(r"`([A-Z][A-Z_]{1,})`", text)
    vocab = frozenset(
        t for t in tokens
        if len(t) >= 2 and not t.startswith("AGOT") and not t.startswith("ACOK")
        and not t.startswith("ASOS") and not t.startswith("AFFC") and not t.startswith("ADWD")
        and t not in ("POV", "ADWD")
    )
    return vocab


def load_qualifier_tiers(qual_vocab_path: Path) -> tuple[frozenset[str], frozenset[str]]:
    """Parse reference/edge-qualifier-vocab.md -> (tier1_types, tier2_types)."""
    try:
        text = qual_vocab_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"WARNING: cannot read {qual_vocab_path}: {exc}", file=sys.stderr)
        return frozenset(), frozenset()

    tier1: set[str] = set()
    tier2: set[str] = set()
    current: set[str] | None = None

    for line in text.splitlines():
        if line.startswith("## Tier 1"):
            current = tier1
            continue
        if line.startswith("## Tier 2"):
            current = tier2
            continue
        if line.startswith("## Tier 3") or (line.startswith("## ") and current is not None
                                             and not line.startswith("## Tier 1")
                                             and not line.startswith("## Tier 2")):
            current = None
            continue
        if current is None:
            continue
        m = re.search(r"`([A-Z][A-Z_]+)`", line)
        if m:
            current.add(m.group(1))

    return frozenset(tier1), frozenset(tier2)


# ---------------------------------------------------------------------------
# Graph node index (slug set + display names + alias/name meta for identity
# alias-check)
# ---------------------------------------------------------------------------
def build_graph_index() -> tuple[set[str], dict[str, dict]]:
    """Returns (node_slug_set, node_meta) where node_meta[slug] = {name, aliases}."""
    node_slug_set: set[str] = set()
    node_meta: dict[str, dict] = {}

    _NAME_RE = re.compile(r'^name:\s*(.+?)\s*$', re.MULTILINE)
    _ALIASES_RE = re.compile(r'^aliases:\s*(\[.*\])\s*$', re.MULTILINE)

    for node_file in sorted(GRAPH_NODES_DIR.rglob("*.node.md")):
        parts = node_file.relative_to(GRAPH_NODES_DIR).parts
        if any(p in _SKIP_DIRS for p in parts):
            continue
        slug = node_file.name[: -len(".node.md")]
        if not slug:
            continue
        node_slug_set.add(slug)

        try:
            text = node_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            node_meta[slug] = {"name": slug, "aliases": []}
            continue

        name_m = _NAME_RE.search(text)
        name = name_m.group(1).strip().strip('"').strip("'") if name_m else slug

        aliases: list[str] = []
        alias_m = _ALIASES_RE.search(text)
        if alias_m:
            try:
                parsed = json.loads(alias_m.group(1))
                if isinstance(parsed, list):
                    aliases = [str(a) for a in parsed]
            except json.JSONDecodeError:
                aliases = []

        node_meta[slug] = {"name": name, "aliases": aliases}

    return node_slug_set, node_meta


def build_slug_category() -> dict[str, str]:
    slug_category: dict[str, str] = {}
    for cat_dir in sorted(GRAPH_NODES_DIR.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith("_") or cat_dir.name in _SKIP_DIRS:
            continue
        for nf in cat_dir.glob("*.node.md"):
            slug_category[nf.name[: -len(".node.md")]] = cat_dir.name
    return slug_category


# ---------------------------------------------------------------------------
# Live edges index (for dedup-vs-live)
# ---------------------------------------------------------------------------
def load_live_edge_triples(path: Path) -> set[tuple[str, str, str]]:
    triples: set[tuple[str, str, str]] = set()
    if not path.exists():
        print(f"WARNING: live edges file not found: {path}", file=sys.stderr)
        return triples
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            s = row.get("source_slug")
            t = row.get("target_slug")
            e = row.get("edge_type")
            if s and t and e:
                triples.add((s, e, t))
    return triples


def load_jsonl(path: Path) -> list[dict]:
    """Read a JSONL file into a list of dicts. Missing file -> empty list."""
    if not path.exists():
        return []
    rows: list[dict] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def build_slug_path_index() -> dict[str, Path]:
    """slug -> node file Path, across all graph/nodes category subdirs (skips _-dirs)."""
    index: dict[str, Path] = {}
    for node_file in sorted(GRAPH_NODES_DIR.rglob("*.node.md")):
        parts = node_file.relative_to(GRAPH_NODES_DIR).parts
        if any(p in _SKIP_DIRS or p.startswith("_") for p in parts):
            continue
        slug = node_file.name[: -len(".node.md")]
        if slug:
            index[slug] = node_file
    return index


# ---------------------------------------------------------------------------
# Curated-map loader (--map)
# ---------------------------------------------------------------------------
def load_curated_map(path: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    if not path.exists():
        print(f"  NOTE: curated map not found at {path} (proceeding with empty map)", file=sys.stderr)
        return mapping
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            name = (row.get("name") or "").strip()
            slug = (row.get("slug") or "").strip()
            if not name:
                continue
            mapping[name.lower()] = slug
    return mapping


# ---------------------------------------------------------------------------
# Extraction file parsing — Relationships Observed table + Characters Present
# (parser logic adapted from scripts/stage4-pass1-edge-candidates.py, copied
# here rather than imported since that module's parser is tightly coupled to
# the five-book Pass 1 pipeline's file layout)
# ---------------------------------------------------------------------------
_HEADING_RE = re.compile(r"^##\s+(.+)$")
_TABLE_ROW_RE = re.compile(r"^\|(.+)\|$")


def _split_table_row(line: str) -> list[str]:
    inner = line.strip().strip("|")
    return [c.strip() for c in inner.split("|")]


def _is_separator_row(cells: list[str]) -> bool:
    return all(re.match(r"^[-: ]+$", c) for c in cells if c)


def parse_relationships_table(text: str) -> list[dict]:
    """Parse the ## Relationships Observed table. Returns list of
    {char_a, relationship, char_b, evidence} dicts."""
    in_section = False
    header_cols: list[str] = []
    idx_a = idx_rel = idx_b = idx_ev = -1
    rows: list[dict] = []

    for line in text.splitlines():
        h2 = _HEADING_RE.match(line)
        if h2:
            label = h2.group(1).strip()
            if re.search(r"relationship", label, re.IGNORECASE):
                in_section = True
                header_cols = []
                idx_a = idx_rel = idx_b = idx_ev = -1
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

        if not header_cols:
            header_cols = [c.lower() for c in cells]
            for i, h in enumerate(header_cols):
                if h in ("character a", "from"):
                    idx_a = i
                elif h in ("character b", "to"):
                    idx_b = i
                elif "relationship" in h:
                    idx_rel = i
                elif "evidence" in h:
                    idx_ev = i
            if idx_a < 0 or idx_rel < 0 or idx_b < 0:
                print(f"  WARNING: unrecognized Relationships Observed header: {cells}", file=sys.stderr)
                in_section = False
            continue

        def safe_get(i: int) -> str:
            return cells[i].strip() if 0 <= i < len(cells) else ""

        char_a = safe_get(idx_a)
        relationship = safe_get(idx_rel)
        char_b = safe_get(idx_b)
        evidence = safe_get(idx_ev)

        if not char_a or not char_b or not relationship:
            continue

        rows.append({"char_a": char_a, "relationship": relationship, "char_b": char_b, "evidence": evidence})

    return rows


_CP_HEADING_RE = re.compile(r"^##\s+Characters\s+Present", re.IGNORECASE)


def parse_characters_present(text: str) -> list[str]:
    in_section = False
    header_cols: list[str] = []
    col_idx = -1
    names: list[str] = []

    for line in text.splitlines():
        h2 = _HEADING_RE.match(line)
        if h2:
            label = h2.group(1).strip()
            if re.search(r"characters\s+present", label, re.IGNORECASE):
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
        cells = _split_table_row(line)
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
        if 0 <= col_idx < len(cells):
            name = cells[col_idx].strip()
            if name:
                names.append(name)

    return names


# ---------------------------------------------------------------------------
# Relationship cell parsing: TYPE (qualifier)
# ---------------------------------------------------------------------------
_REL_CELL_RE = re.compile(r"^([A-Z][A-Z_]*)\s*(?:\(([^)]*)\))?\s*$")


def parse_relationship_cell(raw: str) -> tuple[str | None, str | None]:
    """Returns (edge_type, qualifier_or_None). edge_type is None if malformed."""
    m = _REL_CELL_RE.match(raw.strip())
    if not m:
        return None, None
    edge_type = m.group(1)
    qualifier = m.group(2)
    if qualifier is not None:
        qualifier = re.sub(r"\s+", "_", qualifier.strip()).lower()
        if not qualifier:
            qualifier = None
    return edge_type, qualifier


# ---------------------------------------------------------------------------
# Evidence quote normalization + grounding
# ---------------------------------------------------------------------------
_QUOTE_NORM_TABLE = str.maketrans({
    "“": '"', "”": '"', "‘": "'", "’": "'",
    "′": "'", "″": '"', "«": '"', "»": '"',
    "—": "-", "–": "-", " ": " ",
})


def normalize_for_match(text: str) -> str:
    text = text.translate(_QUOTE_NORM_TABLE)
    text = text.replace("…", "...")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_quoted_fragments(evidence_text: str) -> list[str]:
    norm = normalize_for_match(evidence_text)
    frags = re.findall(r'"([^"]{3,})"', norm)
    return [f for f in frags if len(f) >= MIN_FRAG_CHARS]


def ellipsis_parts(fragment: str) -> list[str]:
    parts = re.split(r"\.\.\.+", fragment)
    parts = [p.strip(" ,;:") for p in parts]
    parts = [p for p in parts if len(p.split()) >= 2]
    return parts if parts else [fragment.strip()]


def read_sentences(path: Path) -> list[tuple[int, str]]:
    """Return (start_lineno, sentence_text) pairs for a chapter file, reusing
    stage4-pass1-evidence-locator.py's frontmatter-skipping prose reader +
    paragraph-aware sentence splitter. Sentence granularity keeps evidence
    quotes tight instead of returning whole multi-sentence paragraphs."""
    prose_lines = read_chapter_prose(path)
    if not prose_lines:
        return []
    return split_into_sentences(prose_lines)


def ground_parts(parts: list[str], prose_lines: list[tuple[int, str]]) -> tuple[int, str] | None:
    """All `parts` must appear (case-insensitive, normalized) within a single
    line, or within an adjacent 2-line window (paragraph-wrap safety net)."""
    lowered_parts = [normalize_for_match(p).lower() for p in parts]
    for lineno, line in prose_lines:
        norm_line = normalize_for_match(line).lower()
        if all(p in norm_line for p in lowered_parts):
            return lineno, line.strip()
    for i in range(len(prose_lines) - 1):
        lineno1, line1 = prose_lines[i]
        _, line2 = prose_lines[i + 1]
        combined = normalize_for_match(line1 + " " + line2).lower()
        if all(p in combined for p in lowered_parts):
            return lineno1, (line1.strip() + " " + line2.strip())
    return None


def locate_evidence(evidence_text: str, prose_lines: list[tuple[int, str]]) -> dict:
    """Returns {'grounded': True, 'lineno':N, 'quote':str, 'source':str}
    or {'grounded': False, 'reason': str}."""
    if not evidence_text.strip():
        return {"grounded": False, "reason": "empty-evidence-cell"}

    fragments = extract_quoted_fragments(evidence_text)
    for frag in fragments:
        parts = ellipsis_parts(frag)
        hit = ground_parts(parts, prose_lines)
        if hit:
            lineno, text = hit
            return {"grounded": True, "lineno": lineno, "quote": text, "source": "quoted-fragment"}

    if fragments:
        return {"grounded": False, "reason": "quoted-fragment-not-grounded"}

    # No quoted fragment at all: try the longest 6+ word literal substring
    words = normalize_for_match(evidence_text).split()
    n = len(words)
    if n >= MIN_LITERAL_WORDS:
        for length in range(n, MIN_LITERAL_WORDS - 1, -1):
            candidate = " ".join(words[0:length])
            hit = ground_parts([candidate], prose_lines)
            if hit:
                lineno, text = hit
                return {"grounded": True, "lineno": lineno, "quote": text, "source": "literal-substring-prefix"}
        for length in range(n, MIN_LITERAL_WORDS - 1, -1):
            start = n - length
            candidate = " ".join(words[start:n])
            hit = ground_parts([candidate], prose_lines)
            if hit:
                lineno, text = hit
                return {"grounded": True, "lineno": lineno, "quote": text, "source": "literal-substring-suffix"}

    return {"grounded": False, "reason": "no-quoted-fragment-ungroundable"}


# ---------------------------------------------------------------------------
# Name resolution wrapper: curated map -> resolver -> honorific-stripped retry
# ---------------------------------------------------------------------------
def strip_honorific(name: str) -> str | None:
    for h in HONORIFICS:
        if name.startswith(h):
            return name[len(h):].strip()
    return None


def resolve_full(
    raw_name: str,
    *,
    curated_map: dict[str, str],
    alias_map: dict[str, str],
    node_set: set[str],
    firstname_index: dict[str, list[str]],
    prior: dict[str, int],
    present_slugs: set[str],
    slug_category: dict[str, str],
) -> tuple[str | None, str]:
    cleaned = _clean_raw_name(raw_name)
    key = cleaned.strip().lower()

    if key in curated_map:
        slug = curated_map[key]
        if slug.upper() == "SKIP":
            return None, "curated-skip"
        if slug in node_set:
            return slug, "resolved-curated-map"
        print(f"  WARNING: curated-map slug {slug!r} for {raw_name!r} not in node set; "
              f"falling back to resolver", file=sys.stderr)

    slug, status = resolve_name(
        raw_name, alias_map=alias_map, node_set=node_set, firstname_index=firstname_index,
        prior=prior, present_slugs=present_slugs, slug_category=slug_category,
    )
    if slug is not None and status != STATUS_AMBIGUOUS:
        return slug, status

    stripped = strip_honorific(cleaned)
    if stripped and stripped != cleaned:
        slug2, status2 = resolve_name(
            stripped, alias_map=alias_map, node_set=node_set, firstname_index=firstname_index,
            prior=prior, present_slugs=present_slugs, slug_category=slug_category,
        )
        if slug2 is not None and status2 != STATUS_AMBIGUOUS:
            return slug2, f"{status2}-honorific-stripped"

    return slug, status


# ---------------------------------------------------------------------------
# Identity (SAME_AS/ALIAS_OF) alias-check
# ---------------------------------------------------------------------------
_LEADING_ARTICLE_RE = re.compile(r"^(the|a|an)\s+(.+)$", re.IGNORECASE)


def alias_variants(raw_name: str) -> list[str]:
    cleaned = _clean_raw_name(raw_name)
    variants = [cleaned]
    m = _LEADING_ARTICLE_RE.match(cleaned)
    if m:
        variants.append(m.group(2))
    return variants


def check_alias_candidates(
    slug: str, raw_name: str, node_meta: dict[str, dict], seen_pairs: set[tuple[str, str]], source_row: dict,
) -> list[dict]:
    info = node_meta.get(slug)
    if info is None:
        return []
    existing_lower = {a.lower() for a in info["aliases"]}
    existing_lower.add(info["name"].lower())

    rows = []
    for v in alias_variants(raw_name):
        key = (slug, v.lower())
        if key in seen_pairs:
            continue
        if v.lower() in existing_lower:
            continue
        seen_pairs.add(key)
        rows.append({"slug": slug, "alias": v, "source_row": source_row})
    return rows


# ---------------------------------------------------------------------------
# Main pipeline (default dry-run ingest — unchanged behavior)
# ---------------------------------------------------------------------------
def run_ingest(args) -> None:
    curated_map_path = Path(args.map)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    produced_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # -------------------------------------------------------------------
    # Load reference data
    # -------------------------------------------------------------------
    print("Loading locked edge vocabulary from architecture.md...")
    locked_vocab = load_locked_vocab(ARCH_MD)
    print(f"  {len(locked_vocab):,} locked edge types")

    print("Loading qualifier tiers from edge-qualifier-vocab.md...")
    tier1_types, tier2_types = load_qualifier_tiers(QUAL_VOCAB_MD)
    print(f"  Tier-1 (required): {sorted(tier1_types)}")
    print(f"  Tier-2 (optional): {sorted(tier2_types)}")

    print("Loading alias resolver...")
    alias_data = json.loads(ALIAS_PATH.read_text(encoding="utf-8"))
    alias_to_canonical: dict[str, str] = alias_data.get("alias_to_canonical", {})
    print(f"  {len(alias_to_canonical):,} aliases loaded")

    print("Loading curated map...")
    curated_map = load_curated_map(curated_map_path)
    print(f"  {len(curated_map):,} curated-map rows loaded from {curated_map_path}")

    print("Building graph node index...")
    node_slug_set, node_meta = build_graph_index()
    print(f"  {len(node_slug_set):,} canonical graph nodes")

    print("Loading node display names for firstname index...")
    node_names = load_node_display_names(node_slug_set, GRAPH_NODES_DIR, _SKIP_DIRS)

    print("Building firstname index...")
    firstname_index = build_firstname_index(node_slug_set, node_names)
    print(f"  {len(firstname_index):,} first-name tokens")

    print("Loading backlink-counts (importance prior)...")
    importance_prior = load_importance_prior(BACKLINKS_PATH)
    print(f"  {len(importance_prior):,} slug priors loaded")

    print("Building slug->category index...")
    slug_category = build_slug_category()
    print(f"  {len(slug_category):,} slug->category entries")

    print("Loading live edges.jsonl for dedup-vs-live...")
    live_triples = load_live_edge_triples(GRAPH_EDGES_PATH)
    print(f"  {len(live_triples):,} live (source,type,target) triples indexed")

    # -------------------------------------------------------------------
    # Enumerate extraction files
    # -------------------------------------------------------------------
    extraction_files: list[Path] = []
    for book in BOOKS:
        book_dir = EXTRACTIONS_DIR / book
        if not book_dir.exists():
            print(f"  WARNING: extraction dir not found: {book_dir}", file=sys.stderr)
            continue
        extraction_files.extend(sorted(book_dir.glob(f"{book}-*.extraction.md")))
    print(f"\n{len(extraction_files):,} D&E extraction files to process")

    # Cache sentence lists per (book, evidence_chapter)
    prose_cache: dict[str, list[tuple[int, str]]] = {}

    def get_prose(book: str, chapter: str) -> list[tuple[int, str]]:
        key = f"{book}/{chapter}"
        if key not in prose_cache:
            path = CHAPTERS_DIR / book / f"{chapter}.md"
            prose_cache[key] = read_sentences(path)
        return prose_cache[key]

    # -------------------------------------------------------------------
    # Counters / accumulators
    # -------------------------------------------------------------------
    stats = Counter()
    per_book_stats: dict[str, Counter] = {b: Counter() for b in BOOKS}
    anomalies: list[str] = []

    quarantine_reason_counts: Counter = Counter()
    needs_map_tally: dict[str, dict] = {}
    identity_flag_diff_slug: list[dict] = []

    seen_alias_pairs: set[tuple[str, str]] = set()

    # within-run dedup: (source_slug, edge_type, target_slug) -> best row dict + count
    within_run: dict[tuple[str, str, str], dict] = {}

    emit_rows: list[dict] = []
    alias_add_rows: list[dict] = []
    identity_flag_rows: list[dict] = []
    overlay_rows: list[dict] = []
    quarantine_rows: list[dict] = []

    def tally_unresolved(raw_name: str, evidence_cell: str, extraction_rel: str) -> None:
        if raw_name not in needs_map_tally:
            needs_map_tally[raw_name] = {
                "count": 0,
                "sample_evidence": evidence_cell,
                "sample_file": extraction_rel,
            }
        needs_map_tally[raw_name]["count"] += 1

    for extraction_path in extraction_files:
        book = extraction_path.parent.name.lower()
        file_stem = extraction_path.name[: -len(".extraction.md")]
        evidence_chapter = re.sub(r"-p\d+$", "", file_stem)
        extraction_rel = str(extraction_path.relative_to(REPO_ROOT))

        try:
            text = extraction_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"  WARNING: cannot read {extraction_path}: {exc}", file=sys.stderr)
            continue

        rows = parse_relationships_table(text)
        stats["files_walked"] += 1
        stats["rows_parsed"] += len(rows)
        per_book_stats[book]["rows_parsed"] += len(rows)

        if not rows:
            continue

        # Bootstrap present_slugs (rungs a-c only) from Characters Present + this table
        bootstrap_names = parse_characters_present(text)
        for row in rows:
            bootstrap_names.append(row["char_a"])
            bootstrap_names.append(row["char_b"])
        present_slugs: set[str] = set()
        for bname in bootstrap_names:
            s = resolve_name_bootstrap(
                bname, alias_map=alias_to_canonical, node_set=node_slug_set,
                firstname_index=firstname_index,
            )
            if s:
                present_slugs.add(s)

        prose_lines = get_prose(book, evidence_chapter)

        for row in rows:
            char_a_raw = row["char_a"]
            char_b_raw = row["char_b"]
            relationship_raw = row["relationship"]
            evidence_cell = row["evidence"]

            edge_type, qualifier = parse_relationship_cell(relationship_raw)

            if edge_type is None:
                stats["malformed_relationship_cell"] += 1
                anomalies.append(
                    f"{extraction_rel}: malformed relationship cell {relationship_raw!r} "
                    f"({char_a_raw} / {char_b_raw})"
                )
                quarantine_rows.append({
                    "book": book, "chapter": evidence_chapter, "extraction_file": extraction_rel,
                    "char_a_raw": char_a_raw, "char_b_raw": char_b_raw,
                    "relationship_raw": relationship_raw, "evidence": evidence_cell,
                    "reason": "malformed-relationship-cell",
                })
                quarantine_reason_counts["malformed-relationship-cell"] += 1
                continue

            # -----------------------------------------------------------
            # Identity rows (SAME_AS / ALIAS_OF) — never emitted as edges
            # -----------------------------------------------------------
            if edge_type in IDENTITY_TYPES:
                stats["identity_rows"] += 1
                per_book_stats[book]["identity_rows"] += 1

                a_slug, a_status = resolve_full(
                    char_a_raw, curated_map=curated_map, alias_map=alias_to_canonical,
                    node_set=node_slug_set, firstname_index=firstname_index,
                    prior=importance_prior, present_slugs=present_slugs, slug_category=slug_category,
                )
                b_slug, b_status = resolve_full(
                    char_b_raw, curated_map=curated_map, alias_map=alias_to_canonical,
                    node_set=node_slug_set, firstname_index=firstname_index,
                    prior=importance_prior, present_slugs=present_slugs, slug_category=slug_category,
                )

                if a_slug is None and a_status not in ("curated-skip",):
                    tally_unresolved(char_a_raw, evidence_cell, extraction_rel)
                if b_slug is None and b_status not in ("curated-skip",):
                    tally_unresolved(char_b_raw, evidence_cell, extraction_rel)

                if a_slug is not None and b_slug is not None and a_slug == b_slug:
                    stats["identity_same_slug"] += 1
                    source_row = {
                        "book": book, "chapter": evidence_chapter, "extraction_file": extraction_rel,
                        "relationship_raw": relationship_raw, "evidence": evidence_cell,
                    }
                    added = []
                    added += check_alias_candidates(a_slug, char_a_raw, node_meta, seen_alias_pairs, source_row)
                    added += check_alias_candidates(a_slug, char_b_raw, node_meta, seen_alias_pairs, source_row)
                    alias_add_rows.extend(added)
                    stats["alias_adds"] += len(added)
                else:
                    # different slugs, or one/both unresolved -> orchestrator adjudication
                    stats["identity_flags"] += 1
                    if a_slug is not None and b_slug is not None and a_slug != b_slug:
                        reason = "different-slugs"
                    elif a_slug is None and b_slug is None:
                        reason = "both-unresolved"
                    else:
                        reason = "one-unresolved"
                    flag_row = {
                        "book": book, "chapter": evidence_chapter, "extraction_file": extraction_rel,
                        "relationship_raw": relationship_raw, "evidence": evidence_cell,
                        "char_a_raw": char_a_raw, "char_a_slug": a_slug, "char_a_status": a_status,
                        "char_b_raw": char_b_raw, "char_b_slug": b_slug, "char_b_status": b_status,
                        "reason": reason,
                    }
                    identity_flag_rows.append(flag_row)
                    if reason == "different-slugs":
                        identity_flag_diff_slug.append(flag_row)
                continue

            # -----------------------------------------------------------
            # Non-identity relationship rows -> candidate edges
            # -----------------------------------------------------------
            if edge_type not in locked_vocab:
                stats["quarantine"] += 1
                quarantine_reason_counts["edge-type-not-in-locked-vocab"] += 1
                quarantine_rows.append({
                    "book": book, "chapter": evidence_chapter, "extraction_file": extraction_rel,
                    "char_a_raw": char_a_raw, "char_b_raw": char_b_raw,
                    "relationship_raw": relationship_raw, "evidence": evidence_cell,
                    "reason": "edge-type-not-in-locked-vocab",
                })
                continue

            # Qualifier tier enforcement
            if edge_type in tier1_types and not qualifier:
                stats["quarantine"] += 1
                quarantine_reason_counts["tier1-missing-qualifier"] += 1
                quarantine_rows.append({
                    "book": book, "chapter": evidence_chapter, "extraction_file": extraction_rel,
                    "char_a_raw": char_a_raw, "char_b_raw": char_b_raw,
                    "relationship_raw": relationship_raw, "evidence": evidence_cell,
                    "reason": "tier1-missing-qualifier",
                })
                continue
            if edge_type not in tier1_types and edge_type not in tier2_types and qualifier:
                anomalies.append(
                    f"{extraction_rel}: Tier-3 edge type {edge_type!r} carried a qualifier "
                    f"{qualifier!r} (dropped) — row {char_a_raw} / {char_b_raw}"
                )
                stats["tier3_qualifier_dropped"] += 1
                qualifier = None

            source_slug, source_status = resolve_full(
                char_a_raw, curated_map=curated_map, alias_map=alias_to_canonical,
                node_set=node_slug_set, firstname_index=firstname_index,
                prior=importance_prior, present_slugs=present_slugs, slug_category=slug_category,
            )
            target_slug, target_status = resolve_full(
                char_b_raw, curated_map=curated_map, alias_map=alias_to_canonical,
                node_set=node_slug_set, firstname_index=firstname_index,
                prior=importance_prior, present_slugs=present_slugs, slug_category=slug_category,
            )

            if source_slug is None:
                if source_status == "curated-skip":
                    stats["quarantine"] += 1
                    quarantine_reason_counts["curated-map-skip"] += 1
                    quarantine_rows.append({
                        "book": book, "chapter": evidence_chapter, "extraction_file": extraction_rel,
                        "char_a_raw": char_a_raw, "char_b_raw": char_b_raw,
                        "relationship_raw": relationship_raw, "evidence": evidence_cell,
                        "reason": "curated-map-skip (source)",
                    })
                else:
                    stats["quarantine"] += 1
                    reason = "unresolved-source" if source_status != STATUS_AMBIGUOUS else "ambiguous-source"
                    quarantine_reason_counts[reason] += 1
                    quarantine_rows.append({
                        "book": book, "chapter": evidence_chapter, "extraction_file": extraction_rel,
                        "char_a_raw": char_a_raw, "char_b_raw": char_b_raw,
                        "relationship_raw": relationship_raw, "evidence": evidence_cell,
                        "reason": reason,
                    })
                    tally_unresolved(char_a_raw, evidence_cell, extraction_rel)
                continue

            if target_slug is None:
                if target_status == "curated-skip":
                    stats["quarantine"] += 1
                    quarantine_reason_counts["curated-map-skip"] += 1
                    quarantine_rows.append({
                        "book": book, "chapter": evidence_chapter, "extraction_file": extraction_rel,
                        "char_a_raw": char_a_raw, "char_b_raw": char_b_raw,
                        "relationship_raw": relationship_raw, "evidence": evidence_cell,
                        "reason": "curated-map-skip (target)",
                    })
                else:
                    stats["quarantine"] += 1
                    reason = "unresolved-target" if target_status != STATUS_AMBIGUOUS else "ambiguous-target"
                    quarantine_reason_counts[reason] += 1
                    quarantine_rows.append({
                        "book": book, "chapter": evidence_chapter, "extraction_file": extraction_rel,
                        "char_a_raw": char_a_raw, "char_b_raw": char_b_raw,
                        "relationship_raw": relationship_raw, "evidence": evidence_cell,
                        "reason": reason,
                    })
                    tally_unresolved(char_b_raw, evidence_cell, extraction_rel)
                continue

            stats["resolved"] += 1
            per_book_stats[book]["resolved"] += 1

            if source_slug == target_slug:
                stats["quarantine"] += 1
                quarantine_reason_counts["self-edge-after-resolution"] += 1
                quarantine_rows.append({
                    "book": book, "chapter": evidence_chapter, "extraction_file": extraction_rel,
                    "char_a_raw": char_a_raw, "char_b_raw": char_b_raw,
                    "relationship_raw": relationship_raw, "evidence": evidence_cell,
                    "source_slug": source_slug, "target_slug": target_slug,
                    "reason": "self-edge-after-resolution",
                })
                continue

            loc = locate_evidence(evidence_cell, prose_lines)
            if not loc["grounded"]:
                stats["quarantine"] += 1
                quarantine_reason_counts[loc["reason"]] += 1
                quarantine_rows.append({
                    "book": book, "chapter": evidence_chapter, "extraction_file": extraction_rel,
                    "char_a_raw": char_a_raw, "char_b_raw": char_b_raw,
                    "relationship_raw": relationship_raw, "evidence": evidence_cell,
                    "source_slug": source_slug, "target_slug": target_slug,
                    "reason": loc["reason"],
                })
                continue

            stats["grounded_tier1"] += 1
            per_book_stats[book]["grounded_tier1"] += 1

            candidate = {
                "decision": "emit_edge",
                "candidate_kind": "pass1_relationship",
                "edge_type": edge_type,
                "source_slug": source_slug,
                "source_resolution_status": source_status,
                "target_slug": target_slug,
                "target_resolution_status": target_status,
                "evidence_kind": "book-pass1",
                "evidence_book": book,
                "evidence_chapter": evidence_chapter,
                "evidence_section": "Relationships Observed",
                "evidence_quote": loc["quote"],
                "evidence_ref": f"sources/chapters/{book}/{evidence_chapter}.md:{loc['lineno']}",
                "asserted_relation": relationship_raw,
                "hint_raw": relationship_raw,
                "extraction_file": extraction_rel,
                "confidence_tier": 1,
                "typed_by": TYPED_BY,
                "corroborates_known_edge": False,
                "wiki_edge_type": None,
                "run_id": RUN_ID,
                "schema_version": SCHEMA_VERSION,
                "produced_at": produced_at,
            }
            if qualifier:
                candidate["qualifier"] = qualifier

            key = (source_slug, edge_type, target_slug)
            if key not in within_run:
                within_run[key] = {"row": candidate, "dup_count": 1}
            else:
                within_run[key]["dup_count"] += 1
                # keep the "best-grounded" row = longest evidence_quote (more specific)
                if len(candidate["evidence_quote"]) > len(within_run[key]["row"]["evidence_quote"]):
                    within_run[key]["row"] = candidate

    # -------------------------------------------------------------------
    # Dedup: within-run collapse, then dedup-vs-live
    # -------------------------------------------------------------------
    stats["resolved_grounded_unique_triples"] = len(within_run)

    for (source_slug, edge_type, target_slug), info in within_run.items():
        row = dict(info["row"])
        if info["dup_count"] > 1:
            row["dup_count"] = info["dup_count"]
            stats["dedup_in_run_collapsed"] += info["dup_count"] - 1

        if (source_slug, edge_type, target_slug) in live_triples:
            overlay_row = dict(row)
            overlay_row["decision"] = "overlay_candidate"
            overlay_row["matches_live_edge_triple"] = True
            overlay_rows.append(overlay_row)
            stats["dedup_vs_live"] += 1
        else:
            emit_rows.append(row)
            stats["emitted"] += 1

    # -------------------------------------------------------------------
    # Write outputs
    # -------------------------------------------------------------------
    write_jsonl(out_dir / "emit.jsonl", emit_rows)
    write_jsonl(out_dir / "alias-adds.jsonl", alias_add_rows)
    write_jsonl(out_dir / "identity-flags.jsonl", identity_flag_rows)
    write_jsonl(out_dir / "overlay-candidates.jsonl", overlay_rows)
    write_jsonl(out_dir / "quarantine.jsonl", quarantine_rows)

    needs_map_sorted = sorted(needs_map_tally.items(), key=lambda kv: -kv[1]["count"])
    with (out_dir / "needs-map.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["name", "occurrence_count", "sample_evidence_cell", "sample_file"])
        for name, info in needs_map_sorted:
            writer.writerow([name, info["count"], info["sample_evidence"], info["sample_file"]])

    # -------------------------------------------------------------------
    # STATS.md
    # -------------------------------------------------------------------
    lines = [
        "# D&E Graph-Ingest — STATS",
        "",
        f"> Generated: {produced_at}  ",
        f"> run_id: {RUN_ID}  ",
        f"> schema_version: {SCHEMA_VERSION}  ",
        f"> curated_map: {curated_map_path} ({len(curated_map)} rows)  ",
        "",
        "## Pipeline counts",
        "",
        "| Stage | Count |",
        "|-------|-------|",
        f"| Extraction files walked | {stats['files_walked']:,} |",
        f"| Relationships-table rows parsed | {stats['rows_parsed']:,} |",
        f"| Malformed relationship cells | {stats['malformed_relationship_cell']:,} |",
        f"| Identity rows (SAME_AS/ALIAS_OF) | {stats['identity_rows']:,} |",
        f"|  -> resolved to same slug (alias-check) | {stats['identity_same_slug']:,} |",
        f"|  -> alias-add candidates emitted | {stats['alias_adds']:,} |",
        f"|  -> flagged for adjudication | {stats['identity_flags']:,} |",
        f"| Non-identity rows resolved (both endpoints) | {stats['resolved']:,} |",
        f"| Grounded at confidence_tier=1 | {stats['grounded_tier1']:,} |",
        f"| Unique (source,type,target) triples after in-run dedup | {stats['resolved_grounded_unique_triples']:,} |",
        f"| Duplicate rows collapsed within-run | {stats['dedup_in_run_collapsed']:,} |",
        f"| Deduped vs live edges.jsonl (-> overlay-candidates) | {stats['dedup_vs_live']:,} |",
        f"| Emitted (emit.jsonl) | {stats['emitted']:,} |",
        f"| Quarantined (total) | {stats['quarantine']:,} |",
        f"| Tier-3 qualifiers dropped (anomaly, not quarantined) | {stats['tier3_qualifier_dropped']:,} |",
        f"| Distinct unresolved names (needs-map.csv) | {len(needs_map_tally):,} |",
        "",
        "## Quarantine reasons",
        "",
        "| Reason | Count |",
        "|--------|-------|",
    ]
    for reason, cnt in quarantine_reason_counts.most_common():
        lines.append(f"| {reason} | {cnt:,} |")

    lines += [
        "",
        "## Per-book breakdown",
        "",
        "| Book | Rows Parsed | Identity Rows | Resolved (non-identity) | Grounded Tier-1 |",
        "|------|-------------|----------------|--------------------------|------------------|",
    ]
    for book in BOOKS:
        bs = per_book_stats[book]
        lines.append(
            f"| {book.upper()} | {bs.get('rows_parsed', 0):,} | {bs.get('identity_rows', 0):,} | "
            f"{bs.get('resolved', 0):,} | {bs.get('grounded_tier1', 0):,} |"
        )

    lines += [
        "",
        "## identity-flags.jsonl: different-slugs rows",
        "",
        f"{len(identity_flag_diff_slug):,} row(s) where both sides resolved but to DIFFERENT slugs "
        "(orchestrator adjudication required):",
        "",
    ]
    if identity_flag_diff_slug:
        lines.append("| Book | Char A (raw) | -> slug | Char B (raw) | -> slug | Relationship | Extraction file |")
        lines.append("|------|--------------|---------|--------------|---------|--------------|------------------|")
        for f in identity_flag_diff_slug:
            lines.append(
                f"| {f['book']} | {f['char_a_raw']} | {f['char_a_slug']} | {f['char_b_raw']} | "
                f"{f['char_b_slug']} | {f['relationship_raw']} | {f['extraction_file']} |"
            )
    else:
        lines.append("(none)")

    lines += [
        "",
        "## Top 30 unresolved names (needs-map.csv)",
        "",
        "| Name | Count | Sample evidence | Sample file |",
        "|------|-------|------------------|-------------|",
    ]
    for name, info in needs_map_sorted[:30]:
        lines.append(f"| {name} | {info['count']} | {info['sample_evidence'][:80]} | {info['sample_file']} |")

    if anomalies:
        lines += ["", "## Parsing anomalies", ""]
        for a in anomalies[:100]:
            lines.append(f"- {a}")
        if len(anomalies) > 100:
            lines.append(f"- ... and {len(anomalies) - 100} more")

    lines += [
        "",
        "## Commands run",
        "",
        "```",
        "python3 scripts/dunk-egg-graph-ingest.py "
        f"--map {curated_map_path} --out-dir {out_dir}",
        "```",
        "",
    ]

    (out_dir / "STATS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # -------------------------------------------------------------------
    # Console summary
    # -------------------------------------------------------------------
    print()
    print("=" * 70)
    print("D&E GRAPH-INGEST — RUN SUMMARY (DRY-RUN, nothing written to graph/)")
    print("=" * 70)
    print(f"  Extraction files walked:        {stats['files_walked']:>6,}")
    print(f"  Relationships rows parsed:      {stats['rows_parsed']:>6,}")
    print(f"  Identity rows (SAME_AS/ALIAS):  {stats['identity_rows']:>6,}")
    print(f"    -> alias-add candidates:      {stats['alias_adds']:>6,}")
    print(f"    -> flagged for adjudication:  {stats['identity_flags']:>6,}")
    print(f"      of which different-slugs:   {len(identity_flag_diff_slug):>6,}")
    print(f"  Non-identity resolved (both ends): {stats['resolved']:>6,}")
    print(f"  Grounded tier-1:                {stats['grounded_tier1']:>6,}")
    print(f"  Unique triples after in-run dedup: {stats['resolved_grounded_unique_triples']:>6,}")
    print(f"  Deduped vs live -> overlay:      {stats['dedup_vs_live']:>6,}")
    print(f"  Emitted (emit.jsonl):            {stats['emitted']:>6,}")
    print(f"  Quarantined:                     {stats['quarantine']:>6,}")
    print(f"  Distinct unresolved names:       {len(needs_map_tally):>6,}")
    print()
    print("Quarantine reasons:")
    for reason, cnt in quarantine_reason_counts.most_common():
        print(f"  {cnt:>5,}  {reason}")
    print()
    print(f"Outputs written to: {out_dir}")
    for fname in ["emit.jsonl", "alias-adds.jsonl", "identity-flags.jsonl",
                  "overlay-candidates.jsonl", "quarantine.jsonl", "needs-map.csv", "STATS.md"]:
        fpath = out_dir / fname
        n = sum(1 for _ in fpath.open(encoding="utf-8")) if fpath.suffix != ".md" else None
        if n is not None:
            print(f"  {fname:<28} {n:>6,} lines")
        else:
            print(f"  {fname}")


# ---------------------------------------------------------------------------
# --assemble-final: apply repass verdicts to emit.jsonl + alias-adds.jsonl.
# Still dry-run — writes only under out_dir (working/), never graph/.
# ---------------------------------------------------------------------------
def run_assemble_final(args) -> None:
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    verdicts_path = Path(args.verdicts)

    emit_path = out_dir / "emit.jsonl"
    alias_adds_path = out_dir / "alias-adds.jsonl"

    print(f"Loading {emit_path} ...")
    emit_rows = load_jsonl(emit_path)
    print(f"  {len(emit_rows):,} emit rows")
    if not emit_rows:
        print(f"ERROR: no rows in {emit_path} — run the default ingest first.", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {verdicts_path} ...")
    verdict_rows = load_jsonl(verdicts_path)
    print(f"  {len(verdict_rows):,} verdict rows")

    print(f"Loading {alias_adds_path} ...")
    alias_rows = load_jsonl(alias_adds_path)
    print(f"  {len(alias_rows):,} alias-add rows")

    print("Building graph node index (alias collision guard + dedup-vs-live)...")
    node_slug_set, node_meta = build_graph_index()
    live_triples = load_live_edge_triples(GRAPH_EDGES_PATH)
    print(f"  {len(node_slug_set):,} nodes, {len(live_triples):,} live (source,type,target) triples")

    produced_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # -------------------------------------------------------------------
    # 1. Build verdict lookup keyed on the ORIGINAL (pre-fix) triple as it
    #    appears in emit.jsonl. Duplicate verdict triples: last one wins,
    #    logged as an anomaly (should not happen — verified clean at S222).
    # -------------------------------------------------------------------
    verdict_by_triple: dict[tuple[str, str, str], dict] = {}
    dup_verdict_triples: list[tuple[str, str, str]] = []
    for v in verdict_rows:
        key = (v["source_slug"], v["edge_type"], v["target_slug"])
        if key in verdict_by_triple:
            dup_verdict_triples.append(key)
        verdict_by_triple[key] = v

    matched_triples: set[tuple[str, str, str]] = set()
    counts: Counter = Counter()
    fixes_applied: list[dict] = []
    rejected_rows: list[dict] = []
    self_edges_after_fix: list[dict] = []

    post_verdict_rows: list[dict] = []

    for row in emit_rows:
        triple = (row["source_slug"], row["edge_type"], row["target_slug"])
        verdict = verdict_by_triple.get(triple)

        if verdict is None:
            counts["kept_no_verdict"] += 1
            post_verdict_rows.append(row)
            continue

        matched_triples.add(triple)
        v = verdict.get("verdict")

        if v == "CONFIRM":
            counts["kept_confirmed"] += 1
            post_verdict_rows.append(row)

        elif v == "REJECT":
            counts["rejected"] += 1
            rejected_rows.append({
                "source_slug": row["source_slug"], "edge_type": row["edge_type"],
                "target_slug": row["target_slug"], "reason": verdict.get("reason", ""),
            })

        elif v == "FIX":
            new_row = dict(row)
            fix_src = verdict.get("fix_source_slug")
            fix_tgt = verdict.get("fix_target_slug")
            old_source, old_target = new_row["source_slug"], new_row["target_slug"]

            if fix_src:
                new_row["source_slug"] = fix_src
                new_row["source_resolution_status"] = "repass-fixed"
            if fix_tgt:
                new_row["target_slug"] = fix_tgt
                new_row["target_resolution_status"] = "repass-fixed"

            if new_row["source_slug"] == new_row["target_slug"]:
                counts["self_edge_after_fix_dropped"] += 1
                self_edges_after_fix.append({
                    "edge_type": row["edge_type"], "old_source": old_source, "old_target": old_target,
                    "new_slug": new_row["source_slug"], "reason": verdict.get("reason", ""),
                })
                continue

            counts["fixed"] += 1
            fixes_applied.append({
                "edge_type": row["edge_type"],
                "old_source": old_source, "old_target": old_target,
                "new_source": new_row["source_slug"], "new_target": new_row["target_slug"],
                "reason": verdict.get("reason", ""),
            })
            post_verdict_rows.append(new_row)

        else:
            print(f"  WARNING: unknown verdict {v!r} for triple {triple} — keeping row unchanged",
                  file=sys.stderr)
            counts["kept_unknown_verdict"] += 1
            post_verdict_rows.append(row)

    unmatched_verdicts = [
        v for v in verdict_rows
        if (v["source_slug"], v["edge_type"], v["target_slug"]) not in matched_triples
    ]

    # -------------------------------------------------------------------
    # 2. Re-dedup post-verdict rows: FIX may have made two rows collide on
    #    the same (source,type,target) triple. Keep FIRST row seen (in
    #    emit.jsonl order), bump its dup_count by the merged rows' counts.
    # -------------------------------------------------------------------
    dedup_map: dict[tuple[str, str, str], dict] = {}
    dedup_order: list[tuple[str, str, str]] = []
    dedup_merges = 0

    for row in post_verdict_rows:
        key = (row["source_slug"], row["edge_type"], row["target_slug"])
        if key not in dedup_map:
            dedup_map[key] = {"row": row, "dup_count": row.get("dup_count", 1)}
            dedup_order.append(key)
        else:
            dedup_map[key]["dup_count"] += row.get("dup_count", 1)
            dedup_merges += 1

    # -------------------------------------------------------------------
    # 3. Split vs live edges.jsonl (post-fix triples may now already exist)
    # -------------------------------------------------------------------
    final_edges: list[dict] = []
    final_overlay: list[dict] = []

    for key in dedup_order:
        entry = dedup_map[key]
        row = dict(entry["row"])
        if entry["dup_count"] > 1:
            row["dup_count"] = entry["dup_count"]
        else:
            row.pop("dup_count", None)

        if key in live_triples:
            overlay_row = dict(row)
            overlay_row["decision"] = "overlay_candidate"
            overlay_row["matches_live_edge_triple"] = True
            final_overlay.append(overlay_row)
        else:
            final_edges.append(row)

    counts["final_edges"] = len(final_edges)
    counts["final_overlay_moves"] = len(final_overlay)
    counts["dedup_merges"] = dedup_merges

    # -------------------------------------------------------------------
    # 4. Alias reject-list + already-present + graph-wide-collision guard
    # -------------------------------------------------------------------
    global_alias_owner: dict[str, set[str]] = defaultdict(set)
    for slug, info in node_meta.items():
        global_alias_owner[info["name"].strip().lower()].add(slug)
        for a in info["aliases"]:
            global_alias_owner[a.strip().lower()].add(slug)

    final_aliases: list[dict] = []
    dropped_aliases: list[dict] = []
    seen_final_pairs: set[tuple[str, str]] = set()

    for row in alias_rows:
        slug = row["slug"]
        alias = row["alias"]
        alias_key = alias.strip().lower()
        pair_key = (slug, alias_key)

        if slug in ALIAS_REJECT_SLUGS_ANY:
            dropped_aliases.append({**row, "drop_reason": "reject-list-slug-any"})
            continue
        if (slug, alias_key) in ALIAS_REJECT_PAIRS:
            dropped_aliases.append({**row, "drop_reason": "reject-list-pair"})
            continue

        info = node_meta.get(slug)
        if info is not None:
            existing_lower = {a.strip().lower() for a in info["aliases"]}
            existing_lower.add(info["name"].strip().lower())
            if alias_key in existing_lower:
                dropped_aliases.append({**row, "drop_reason": "already-present-on-node"})
                continue

        owners = global_alias_owner.get(alias_key, set())
        other_owners = owners - {slug}
        if other_owners:
            dropped_aliases.append({
                **row, "drop_reason": "collision-graph-wide",
                "colliding_slugs": sorted(other_owners),
            })
            continue

        if pair_key in seen_final_pairs:
            dropped_aliases.append({**row, "drop_reason": "duplicate-in-batch"})
            continue
        seen_final_pairs.add(pair_key)
        final_aliases.append(row)

    counts["aliases_kept"] = len(final_aliases)
    counts["aliases_dropped"] = len(dropped_aliases)

    # -------------------------------------------------------------------
    # 5. Write outputs
    # -------------------------------------------------------------------
    write_jsonl(out_dir / "final-edges.jsonl", final_edges)
    write_jsonl(out_dir / "final-overlay.jsonl", final_overlay)
    write_jsonl(out_dir / "final-aliases.jsonl", final_aliases)

    drop_reason_counts = Counter(d["drop_reason"] for d in dropped_aliases)

    lines = [
        "# D&E Graph-Ingest — FINAL-STATS (--assemble-final)",
        "",
        f"> Generated: {produced_at}  ",
        f"> run_id: {RUN_ID}  ",
        f"> source: {emit_path}  ",
        f"> verdicts: {verdicts_path}  ",
        f"> alias source: {alias_adds_path}  ",
        "",
        "## Edge verdict counts",
        "",
        "| Stage | Count |",
        "|-------|-------|",
        f"| emit.jsonl rows (input) | {len(emit_rows):,} |",
        f"| repass-verdicts.jsonl rows (input) | {len(verdict_rows):,} |",
        f"| Kept — no verdict (untouched by repass) | {counts['kept_no_verdict']:,} |",
        f"| Kept — CONFIRM | {counts['kept_confirmed']:,} |",
        f"| Kept — unknown verdict string (defensive passthrough) | {counts.get('kept_unknown_verdict', 0):,} |",
        f"| Fixed — FIX applied | {counts['fixed']:,} |",
        f"| Dropped — self-edge created by FIX (defensive) | {counts.get('self_edge_after_fix_dropped', 0):,} |",
        f"| Rejected — REJECT | {counts['rejected']:,} |",
        f"| Dedup-merged after fixes (triple collisions) | {counts['dedup_merges']:,} |",
        f"| Moved to final-overlay.jsonl (now matches live edges.jsonl) | {counts['final_overlay_moves']:,} |",
        f"| **final-edges.jsonl (emitted)** | **{counts['final_edges']:,}** |",
        f"| Verdict rows with duplicate triples in verdicts file (last-wins) | {len(dup_verdict_triples):,} |",
        f"| Verdict rows that did NOT match any emit.jsonl triple | {len(unmatched_verdicts):,} |",
        "",
        "## Alias counts",
        "",
        "| Stage | Count |",
        "|-------|-------|",
        f"| alias-adds.jsonl rows (input) | {len(alias_rows):,} |",
        f"| Kept -> final-aliases.jsonl | {counts['aliases_kept']:,} |",
        f"| Dropped (total) | {counts['aliases_dropped']:,} |",
    ]
    for reason, cnt in drop_reason_counts.most_common():
        lines.append(f"|   -> {reason} | {cnt:,} |")

    lines += ["", "## Every FIX applied", ""]
    if fixes_applied:
        lines.append("| Edge Type | Old Source | Old Target | New Source | New Target | Reason |")
        lines.append("|-----------|------------|------------|------------|------------|--------|")
        for f in fixes_applied:
            lines.append(
                f"| {f['edge_type']} | {f['old_source']} | {f['old_target']} | "
                f"{f['new_source']} | {f['new_target']} | {f['reason']} |"
            )
    else:
        lines.append("(none)")

    if self_edges_after_fix:
        lines += ["", "## Self-edges created by FIX (dropped, defensive)", ""]
        lines.append("| Edge Type | Old Source | Old Target | New (collapsed) Slug | Reason |")
        lines.append("|-----------|------------|------------|----------------------|--------|")
        for s in self_edges_after_fix:
            lines.append(
                f"| {s['edge_type']} | {s['old_source']} | {s['old_target']} | "
                f"{s['new_slug']} | {s['reason']} |"
            )

    if rejected_rows:
        lines += ["", "## Every REJECT applied", ""]
        lines.append("| Edge Type | Source | Target | Reason |")
        lines.append("|-----------|--------|--------|--------|")
        for r in rejected_rows:
            lines.append(f"| {r['edge_type']} | {r['source_slug']} | {r['target_slug']} | {r['reason']} |")

    lines += ["", "## Every dropped alias", ""]
    if dropped_aliases:
        lines.append("| Slug | Alias | Drop Reason | Colliding Slugs |")
        lines.append("|------|-------|--------------|------------------|")
        for d in dropped_aliases:
            colliding = ", ".join(d.get("colliding_slugs", []))
            lines.append(f"| {d['slug']} | {d['alias']} | {d['drop_reason']} | {colliding} |")
    else:
        lines.append("(none)")

    if unmatched_verdicts:
        lines += ["", "## Verdict rows with no matching emit.jsonl triple", ""]
        lines.append("| Source | Edge Type | Target | Verdict | Reason |")
        lines.append("|--------|-----------|--------|---------|--------|")
        for v in unmatched_verdicts:
            lines.append(
                f"| {v['source_slug']} | {v['edge_type']} | {v['target_slug']} | "
                f"{v.get('verdict','')} | {v.get('reason','')} |"
            )

    lines += [
        "",
        "## Commands run",
        "",
        "```",
        f"python3 scripts/dunk-egg-graph-ingest.py --assemble-final "
        f"--out-dir {out_dir} --verdicts {verdicts_path}",
        "```",
        "",
    ]

    (out_dir / "FINAL-STATS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print()
    print("=" * 70)
    print("D&E ASSEMBLE-FINAL — RUN SUMMARY (still dry-run, nothing written to graph/)")
    print("=" * 70)
    print(f"  emit.jsonl rows:                {len(emit_rows):>6,}")
    print(f"  verdict rows:                    {len(verdict_rows):>6,}")
    print(f"    kept (no verdict):            {counts['kept_no_verdict']:>6,}")
    print(f"    kept (CONFIRM):               {counts['kept_confirmed']:>6,}")
    print(f"    fixed (FIX):                  {counts['fixed']:>6,}")
    print(f"    rejected (REJECT):            {counts['rejected']:>6,}")
    print(f"    self-edge-after-fix (dropped):{counts.get('self_edge_after_fix_dropped', 0):>6,}")
    print(f"  dedup-merged after fixes:        {counts['dedup_merges']:>6,}")
    print(f"  moved to final-overlay.jsonl:    {counts['final_overlay_moves']:>6,}")
    print(f"  FINAL edges (final-edges.jsonl): {counts['final_edges']:>6,}")
    print(f"  Unmatched verdict rows:          {len(unmatched_verdicts):>6,}")
    if unmatched_verdicts:
        for v in unmatched_verdicts:
            print(f"    NO MATCH: {v['source_slug']} {v['edge_type']} {v['target_slug']} "
                  f"(verdict={v.get('verdict')})")
    print()
    print(f"  alias-adds.jsonl rows:           {len(alias_rows):>6,}")
    print(f"  kept -> final-aliases.jsonl:     {counts['aliases_kept']:>6,}")
    print(f"  dropped:                         {counts['aliases_dropped']:>6,}")
    for reason, cnt in drop_reason_counts.most_common():
        print(f"    {cnt:>5,}  {reason}")
    print()
    print(f"Outputs written to: {out_dir}")
    for fname in ["final-edges.jsonl", "final-overlay.jsonl", "final-aliases.jsonl", "FINAL-STATS.md"]:
        fpath = out_dir / fname
        n = sum(1 for _ in fpath.open(encoding="utf-8")) if fpath.suffix != ".md" else None
        print(f"  {fname:<22} {n:>6,} lines" if n is not None else f"  {fname}")


# ---------------------------------------------------------------------------
# --apply: mutate the live graph. Orchestrator-gated — never called by
# default. Refuses to run twice (RUN_ID sentinel check in edges.jsonl).
# ---------------------------------------------------------------------------
def upsert_node_alias(node_path: Path, new_alias: str) -> str:
    """Idempotently add `new_alias` to a node file's `aliases:` frontmatter
    list, preserving the double-quoted JSON-array style used across the
    corpus. Returns one of: 'added' | 'already-present' | 'no-frontmatter'
    | 'error'."""
    try:
        text = node_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"  ERROR: cannot read {node_path}: {exc}", file=sys.stderr)
        return "error"

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "no-frontmatter"

    close_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close_idx = i
            break
    if close_idx is None:
        return "no-frontmatter"

    alias_line_re = re.compile(r"^aliases:\s*(\[.*\])\s*$")
    for i in range(1, close_idx):
        m = alias_line_re.match(lines[i].rstrip("\n"))
        if m:
            try:
                existing = json.loads(m.group(1))
                if not isinstance(existing, list):
                    existing = []
            except json.JSONDecodeError:
                existing = []
            if any(str(a).strip().lower() == new_alias.strip().lower() for a in existing):
                return "already-present"
            existing.append(new_alias)
            newline = "\n" if lines[i].endswith("\n") else ""
            lines[i] = f"aliases: {json.dumps(existing, ensure_ascii=False)}{newline}"
            try:
                node_path.write_text("".join(lines), encoding="utf-8")
            except OSError as exc:
                print(f"  ERROR: cannot write {node_path}: {exc}", file=sys.stderr)
                return "error"
            return "added"

    # No `aliases:` line found in frontmatter -> insert one right before the
    # closing '---'.
    new_line = f'aliases: {json.dumps([new_alias], ensure_ascii=False)}\n'
    lines.insert(close_idx, new_line)
    try:
        node_path.write_text("".join(lines), encoding="utf-8")
    except OSError as exc:
        print(f"  ERROR: cannot write {node_path}: {exc}", file=sys.stderr)
        return "error"
    return "added"


def run_apply(args) -> None:
    out_dir = Path(args.out_dir)
    final_edges_path = out_dir / "final-edges.jsonl"
    final_aliases_path = out_dir / "final-aliases.jsonl"

    if not final_edges_path.exists() or not final_aliases_path.exists():
        print(
            f"ERROR: run --assemble-final first — missing "
            f"{final_edges_path if not final_edges_path.exists() else final_aliases_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    # ---- Refuse to run twice ----
    if GRAPH_EDGES_PATH.exists():
        with GRAPH_EDGES_PATH.open(encoding="utf-8") as fh:
            for line in fh:
                if f'"run_id": "{RUN_ID}"' in line or f'"run_id":"{RUN_ID}"' in line:
                    print(
                        f"ABORT: run_id {RUN_ID!r} already present in {GRAPH_EDGES_PATH} — "
                        f"this D&E apply has already run. Refusing to double-apply.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
    else:
        print(f"ERROR: {GRAPH_EDGES_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    final_edges = load_jsonl(final_edges_path)
    final_aliases = load_jsonl(final_aliases_path)
    print(f"Loaded {len(final_edges):,} final edges, {len(final_aliases):,} final aliases")

    if not final_edges and not final_aliases:
        print("Nothing to apply (both final-edges.jsonl and final-aliases.jsonl are empty). Aborting.",
              file=sys.stderr)
        sys.exit(1)

    # ---- Backup ----
    backup_path = GRAPH_EDGES_PATH.with_name(GRAPH_EDGES_PATH.name + ".bak-s222-dunk-egg")
    print(f"Backing up {GRAPH_EDGES_PATH} -> {backup_path}")
    shutil.copy2(GRAPH_EDGES_PATH, backup_path)

    # ---- Append edges ----
    print(f"Appending {len(final_edges):,} edges to {GRAPH_EDGES_PATH}...")
    with GRAPH_EDGES_PATH.open("a", encoding="utf-8") as fh:
        for row in final_edges:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    # ---- Apply aliases ----
    print(f"Applying {len(final_aliases):,} alias adds...")
    slug_path_index = build_slug_path_index()
    per_node_added: Counter = Counter()
    per_node_skipped: Counter = Counter()
    errors: list[str] = []

    for row in final_aliases:
        slug = row["slug"]
        alias = row["alias"]
        node_path = slug_path_index.get(slug)
        if node_path is None:
            errors.append(f"{slug}: node file not found (alias {alias!r} not applied)")
            continue
        result = upsert_node_alias(node_path, alias)
        if result == "added":
            per_node_added[slug] += 1
        elif result == "already-present":
            per_node_skipped[slug] += 1
        else:
            errors.append(f"{slug}: {result} ({node_path}, alias {alias!r})")

    print()
    print("=" * 70)
    print("D&E APPLY — SUMMARY")
    print("=" * 70)
    print(f"  Backup written: {backup_path}")
    print(f"  Edges appended: {len(final_edges):,}")
    print(f"  Aliases added:  {sum(per_node_added.values()):,}  across {len(per_node_added):,} nodes")
    print(f"  Aliases already-present (skipped): {sum(per_node_skipped.values()):,}")
    print(f"  Errors: {len(errors):,}")
    for e in errors[:50]:
        print(f"    {e}")
    print()
    print("Per-node alias adds:")
    for slug, n in per_node_added.most_common():
        print(f"  {slug}: +{n}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "D&E Pass-1 graph-ingest track — deterministic candidate builder.\n"
            "Parses 24 D&E extraction files, resolves names, grounds evidence, "
            "dedups vs live edges. DRY-RUN by default: writes only under working/, never graph/.\n"
            "--assemble-final and --apply are follow-up subcommands (see module docstring)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--map", default=str(DEFAULT_CURATED_MAP), metavar="CSV",
        help="Curated name->slug seed map CSV (columns: name,slug; slug=SKIP to drop). "
             f"Default: {DEFAULT_CURATED_MAP}",
    )
    parser.add_argument(
        "--out-dir", default=str(DEFAULT_OUT_DIR), metavar="DIR",
        help=f"Output directory (never graph/, except under --apply which writes to graph/edges/). "
             f"Default: {DEFAULT_OUT_DIR}",
    )
    parser.add_argument(
        "--verdicts", default=str(DEFAULT_VERDICTS_PATH), metavar="JSONL",
        help=f"Repass verdicts JSONL for --assemble-final. Default: {DEFAULT_VERDICTS_PATH}",
    )
    parser.add_argument(
        "--assemble-final", action="store_true",
        help="Apply repass-verdicts-s222.jsonl to out/emit.jsonl + out/alias-adds.jsonl; "
             "write out/final-edges.jsonl, out/final-overlay.jsonl, out/final-aliases.jsonl, "
             "out/FINAL-STATS.md. Still dry-run (writes only under working/).",
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Append out/final-edges.jsonl to graph/edges/edges.jsonl and insert "
             "out/final-aliases.jsonl into node frontmatter. MUTATES graph/. "
             "Orchestrator-gated; refuses to run twice.",
    )
    args = parser.parse_args()

    if args.apply:
        run_apply(args)
    elif args.assemble_final:
        run_assemble_final(args)
    else:
        run_ingest(args)


if __name__ == "__main__":
    main()
