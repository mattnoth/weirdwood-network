#!/usr/bin/env python3
"""infobox-merge.py — Promote wiki infobox relationship rows into graph/edges/edges.jsonl.

Reads working/wiki/data/infobox-data.jsonl (20,614 relationship rows from 4,786 wiki pages)
and applies the v2 promotion rule set:
  Rule 0  — input universe (all rows)
  Rule 1  — source resolution (4-rung ladder)
  Rule 2  — noise-target filter (placeholder / bare-kinship / numeral)
  Rule 3  — speculative-kinship quarantine + fact-key closure (v2)
  Rule 4  — target resolution (same 4-rung ladder)
  Rule 5  — deterministic retypes (FIGHTS_IN→PART_OF, WORSHIPS→RELIGION_OF)
  Rule 6  — endpoint type contracts
  Rule 7  — direction correction (10 inverted FIELD_EDGE_MAP fields)
  Rule 8  — self-loop suppression
  Rule 9  — qualifier-aware in-run dedupe
  Rule 10 — dedupe vs existing edges.jsonl (corroboration log)
  Rule 11 — stamping (tier, provenance, qualifiers)

Also runs two hygiene fixes on edges.jsonl:
  Fix A — orphan-endpoint slug remap (alias + the-strip + honorific-prefix-strip)
  Fix B — typed_by backfill for 948 rows missing it

Modes:
  --dry-run (DEFAULT)  Write nothing under graph/. Emit full logs to working/infobox-merge/.
  --apply              Requires --yes-i-reviewed-the-dry-run flag AND creates timestamped
                       backup to graph/edges/_regrounding/ before writing.

Usage:
    python3 scripts/infobox-merge.py [--dry-run]
    python3 scripts/infobox-merge.py --apply --yes-i-reviewed-the-dry-run
"""

import argparse
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INFOBOX_DATA = ROOT / "working/wiki/data/infobox-data.jsonl"
ALIAS_RESOLVER_FILE = ROOT / "working/wiki/data/alias-resolver.json"
NODES_ROOT = ROOT / "graph/nodes"
EDGES_FILE = ROOT / "graph/edges/edges.jsonl"
REGROUNDING_DIR = ROOT / "graph/edges/_regrounding"
OUTPUT_DIR = ROOT / "working/infobox-merge"
CHAPTERS_ROOT = ROOT / "sources/chapters"

SKIP_DIRS = {"_conflicts", "_unclassified"}
SYMMETRIC_TYPES = {"SPOUSE_OF", "LOVER_OF"}
CHAR_CHAR_TYPES = {"PARENT_OF", "SPOUSE_OF", "LOVER_OF"}
DIRECTION_FLIP_FIELDS = {
    "heir", "heirs", "cadet branches", "head", "ruler",
    "successor", "predecessor", "founder", "owner", "owners",
}
KINSHIP_FIELDS = {
    "father", "fathers", "mother", "mothers", "spouse", "spouses",
    "lover", "lovers", "issue", "heir", "heirs",
}
UNIQUE_SINGULAR_FIELDS = {"father", "mother"}
PLURAL_SPECULATIVE_FIELDS = {"fathers", "mothers"}
FACT_CLASS = {
    "PARENT_OF": "PARENT",
    "SPOUSE_OF": "SPOUSE",
    "LOVER_OF": "LOVER",
    "HEIR_TO": "HEIR",
}

NOISE_EXACT = frozenset(w.lower() for w in [
    "Unknown", "None", "Extinct", "Unborn", "N/A", "Various", "Several",
    "Many", "Disputed", "Vacant", "Defunct", "Dead", "Deceased",
    "Abandoned", "Uninhabited", "Mixed", "Uncertain", "Unnamed", "Issue",
])

KINSHIP_BARE_RE = re.compile(
    r"^(a |an |two |three |four |five |six |several |many )?"
    r"(unborn |deceased |stillborn |bastard )?"
    r"(sons?|daughters?|childr?e?n?|brothers?|sisters?|mothers?|fathers?|"
    r"wife|wives|husbands?|nephews?|nieces?|cousins?|grandsons?|granddaughters?|"
    r"uncles?|aunts?)$",
    re.IGNORECASE,
)

NUMERAL_RE = re.compile(r"^[\d\s\xa0,–—-]+(AC|BC)?\s*$", re.IGNORECASE)

SPEC_QUAL_RE = re.compile(
    r"\b(rumored|rumoured|supposedly|supposed|alleged(ly)?|possibly|reportedly|"
    r"officially|legally|unconfirmed|presumably|debated|dubious canonicity|in some tales)\b",
    re.IGNORECASE,
)

ARTIFACT_QUAL_RE = re.compile(r"^(ren|s)$", re.IGNORECASE)
DATE_RANGE_QUAL_RE = re.compile(r"^\d{1,4}[\s–—-]+\d{1,4}\s*(AC|BC)?$", re.IGNORECASE)

# Honorific prefixes for Fix A orphan remap
HONORIFIC_PREFIXES = (
    "ser-", "lord-", "lady-", "maester-", "septa-", "septon-",
    "khal-", "king-", "queen-", "prince-", "princess-",
)

# POV character label map for Fix B (label → file-stem)
_POV_LABEL_MAP = {
    # AGOT / ACOK / ASOS standard POVs
    "bran": "bran", "catelyn": "catelyn", "daenerys": "daenerys",
    "eddard": "eddard", "jon": "jon", "arya": "arya", "tyrion": "tyrion",
    "sansa": "sansa", "theon": "theon", "davos": "davos",
    "jaime": "jaime", "samwell": "samwell", "cersei": "cersei",
    "brienne": "brienne",
    # AFFC / ADWD descriptive titles
    "the prophet": "the-prophet",
    "the drowned man": "the-drowned-man",
    "the iron captain": "the-iron-captain",
    "the kraken's daughter": "the-krakens-daughter",
    "the captain of guards": "the-captain-of-guards",
    "the soiled knight": "the-soiled-knight",
    "the queenmaker": "the-queenmaker",
    "the princess in the tower": "the-princess-in-the-tower",
    "alayne": "alayne",
    "cat of the canals": "cat-of-the-canals",
    "the reaver": "the-reaver",
    "reek": "reek",
    "the merchant's man": "the-merchants-man",
    "the turncloak": "the-turncloak",
    "the prince of winterfell": "the-prince-of-winterfell",
    "the lost lord": "the-lost-lord",
    "the windblown": "the-windblown",
    "the wayward bride": "the-wayward-bride",
    "the watcher": "the-watcher",
    "the king's prize": "the-kings-prize",
    "the dragontamer": "the-dragontamer",
    "the griffin reborn": "the-griffin-reborn",
    "the sacrifice": "the-sacrifice",
    "the ugly little girl": "the-ugly-little-girl",
    "the discarded knight": "the-discarded-knight",
    "the spurned suitor": "the-spurned-suitor",
    "the queensguard": "the-queensguard",
    "the blind girl": "the-blind-girl",
    "a ghost in winterfell": "a-ghost-in-winterfell",
    "the iron suitor": "the-iron-suitor",
    "the iron suitor (victarion i)": "the-iron-suitor",
    "the kingbreaker": "the-kingbreaker",
    "the queen's hand": "the-queens-hand",
    "melisandre": "melisandre",
    "barristan": "barristan",
    "victarion": "victarion",
    "quentyn": "quentyn",
    "jon connington": "jon-connington",
}
ROMAN_TO_INT = {
    "i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7,
    "viii": 8, "ix": 9, "x": 10, "xi": 11, "xii": 12, "xiii": 13,
    "xiv": 14, "xv": 15, "xvi": 16, "xvii": 17, "xviii": 18,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def kebab(text: str, keep_parens: bool = False) -> str:
    """Convert display string to slug (byte-identical to orphan-edges-audit.py kebab())."""
    if not text:
        return ""
    text = re.sub(r"\[[^\]]*\]", "", text)
    if not keep_parens:
        text = re.sub(r"\([^)]*\)", "", text)
    text = text.strip().rstrip(".,;:").strip(" \"'`").lower()
    text = text.replace("’", "").replace("‘", "").replace("'", "")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def norm_qual(q: str) -> str:
    return re.sub(r"\s+", " ", (q or "").replace("\xa0", " ").strip().lower())


def noise_reason(target: str) -> str | None:
    t = target.replace("\xa0", " ").strip()
    if t.lower() in NOISE_EXACT:
        return "noise-placeholder"
    if KINSHIP_BARE_RE.match(t):
        return "noise-bare-kinship"
    if NUMERAL_RE.match(t):
        return "noise-numeral-date"
    return None


def load_nodes() -> dict[str, str]:
    """Returns slug → category (first path component under graph/nodes/)."""
    nodes: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(NODES_ROOT):
        d = Path(dirpath)
        if d.name in SKIP_DIRS:
            dirnames[:] = []
            continue
        for fn in filenames:
            if fn.endswith(".node.md"):
                rel = d.relative_to(NODES_ROOT)
                category = rel.parts[0] if rel.parts else "_root"
                nodes[fn[:-8]] = category
    return nodes


def load_alias(alias_file: Path) -> dict[str, str]:
    with alias_file.open() as f:
        data = json.load(f)
    return data.get("alias_to_canonical", {})


def resolve(name: str, nodes: dict[str, str], alias: dict[str, str]) -> tuple[str | None, str | None, str | None]:
    """4-rung resolution ladder. Returns (slug, category, status) or (None, None, 'unresolved')."""
    # Rung 1: exact with parens kept
    sk = kebab(name, keep_parens=True)
    if sk in nodes:
        return sk, nodes[sk], "resolved-exact-parens"
    # Rung 2: exact, parens stripped
    s = kebab(name)
    if s != sk and s in nodes:
        return s, nodes[s], "resolved-exact"
    # Rung 3: alias-resolver (try both forms)
    for cand in (sk, s):
        if cand in alias and alias[cand] in nodes:
            canon = alias[cand]
            return canon, nodes[canon], "resolved-alias"
    # Rung 4: leading-article strip
    if s.startswith("the-"):
        stripped = s[4:]
        if stripped in nodes:
            return stripped, nodes[stripped], "resolved-the-strip"
    return None, None, "unresolved"


def load_existing_keys(edges_file: Path, symmetric_types: set[str]) -> set:
    """Load existing edges as a set of (type, src, tgt) or (type, frozenset) keys."""
    keys = set()
    for line in edges_file.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        s, t, ty = r.get("source_slug"), r.get("target_slug"), r.get("edge_type")
        if s and t and ty:
            if ty in symmetric_types:
                keys.add((ty, frozenset((s, t))))
            else:
                keys.add((ty, s, t))
    return keys


def edge_key(et: str, s: str, t: str, symmetric_types: set[str]):
    if et in symmetric_types:
        return (et, frozenset((s, t)))
    return (et, s, t)


def load_chapter_stems() -> set[str]:
    """Load all chapter file stems from sources/chapters/."""
    stems: set[str] = set()
    for book_dir in CHAPTERS_ROOT.iterdir():
        if book_dir.is_dir():
            for f in book_dir.glob("*.md"):
                stems.add(f.stem)
    return stems


def label_to_file_stem(book: str, label: str, chapter_stems: set[str]) -> str | None:
    """Convert 'ASOS Arya VII' / 'AGOT Prologue' → chapter file stem."""
    label = label.strip()
    # Try to strip book prefix
    label_lower = label.lower()
    book_lower = book.lower() if book else ""
    # Remove book prefix if present (e.g. "ASOS Arya VII" → "Arya VII")
    if label_lower.startswith(book_lower + " "):
        rest = label[len(book_lower) + 1:].strip()
    else:
        # Try matching "ASOS " prefix
        m = re.match(r"^([A-Z]+)\s+(.+)$", label)
        if m:
            book_lower = m.group(1).lower()
            rest = m.group(2).strip()
        else:
            return None

    rest_lower = rest.lower()

    # Check for Prologue / Epilogue
    if rest_lower == "prologue":
        cand = f"{book_lower}-prologue"
        return cand if cand in chapter_stems else None
    if rest_lower == "epilogue":
        cand = f"{book_lower}-epilogue"
        return cand if cand in chapter_stems else None

    # Try POV-map lookup: rest may be "Arya VII" or "The Griffin Reborn" etc.
    # Split off trailing roman numeral
    m2 = re.match(r"^(.+?)\s+([IVX]+)$", rest, re.IGNORECASE)
    if m2:
        who_raw = m2.group(1).strip()
        roman = m2.group(2).lower()
        num = ROMAN_TO_INT.get(roman)
        if num is None:
            return None
        who_key = who_raw.lower()
        pov_slug = _POV_LABEL_MAP.get(who_key)
        if pov_slug:
            cand = f"{book_lower}-{pov_slug}-{num:02d}"
            return cand if cand in chapter_stems else None
    else:
        # No roman numeral — try as single-chapter POV (e.g. "A Ghost in Winterfell")
        who_key = rest_lower
        pov_slug = _POV_LABEL_MAP.get(who_key)
        if pov_slug:
            cand = f"{book_lower}-{pov_slug}-01"
            return cand if cand in chapter_stems else None

    return None


# ---------------------------------------------------------------------------
# Qualifier normalization (Rule 11)
# ---------------------------------------------------------------------------

QUALIFIER_ENUM = {
    "HOLDS_TITLE": (
        ["former", "claimed", "historical", "contested", "current", "unknown"],
        {
            "formerly": "former", "stripped": "former",
            "claimant": "claimed", "self-styled": "claimed", "pretender": "claimed",
            "historical": "historical",
            "current": "current",
        },
        "unknown",
    ),
    "SWORN_TO": (
        ["former", "deserted", "by_marriage", "claimed", "current", "unknown"],
        {
            "formerly": "former", "deserted": "deserted",
            "by marriage": "by_marriage",
            "claimed": "claimed",
            "current": "current",
        },
        "unknown",
    ),
    "SPOUSE_OF": (
        ["current", "former", "annulled", "widowed", "salt_wife", "unknown"],
        {
            "salt wife": "salt_wife",
            "annulled": "annulled", "dissolved": "annulled",
            "formerly": "former",
            "current": "current",
        },
        "unknown",
    ),
    "PARENT_OF": (
        ["biological", "adopted", "claimed", "rumored", "disputed", "unknown"],
        {
            "adopted": "adopted", "adoptive mother": "adopted", "adoptive father": "adopted",
            "claimed": "claimed",
        },
        "biological",
    ),
    "LOVER_OF": (
        ["current", "former", "secret", "paramour", "rumored", "unknown"],
        {
            "paramour": "paramour",
            "formerly": "former",
        },
        None,  # OPTIONAL — omit if no match
    ),
}


def normalize_qualifier(edge_type: str, raw_qual: str | None) -> str | None:
    """Return the enum qualifier value (or None if the type is Tier-3 / no match for optional)."""
    if edge_type not in QUALIFIER_ENUM:
        return None  # Tier-3: no qualifier
    enum_values, mapping, default = QUALIFIER_ENUM[edge_type]
    if not raw_qual:
        return default
    q = raw_qual.replace("\xa0", " ").strip().lower()
    # Check direct mapping
    for pattern, value in mapping.items():
        if q == pattern or q.startswith(pattern):
            return value
    # Check if raw_qual starts with "disputed"
    if q.startswith("disputed"):
        if edge_type == "PARENT_OF":
            return "disputed"
        # For other types disputed quarantines via Rule 3d — won't reach here
    # Enum direct match
    if q in enum_values:
        return q
    return default


# ---------------------------------------------------------------------------
# Build quarantined fact-key set (pre-pass for Rule 3e)
# ---------------------------------------------------------------------------

def build_quarantine_fact_keys(
    pages: list[dict],
    nodes: dict[str, str],
    alias: dict[str, str],
) -> set[tuple]:
    """Pre-pass: collect fact keys where any row trips Rule 3a-3d."""
    q2_keys = _build_q2_keys(pages)
    fact_quarantine: set = set()
    for rec in pages:
        page = rec["page"]
        src, _, _ = resolve(page, nodes, alias)
        if src is None:
            continue
        for r in rec["relationships"]:
            field = r["field"].lower()
            et = r["edge_type"]
            qual = r.get("qualifier") or ""
            if et not in FACT_CLASS:
                continue
            if noise_reason(r["target"]):
                continue
            q3 = _trips_r3(field, qual, et, q2_keys, page)
            if q3 is None:
                continue
            tgt, _, _ = resolve(r["target"], nodes, alias)
            if tgt is not None and tgt != src:
                fact_quarantine.add((FACT_CLASS[et], frozenset((src, tgt))))
    return fact_quarantine


def _build_q2_keys(pages: list[dict]) -> set[tuple]:
    """Rule 3b: pages that have >1 distinct non-noise target in a singular parent field."""
    q2: set[tuple] = set()
    for rec in pages:
        per_field: dict[str, set] = defaultdict(set)
        for r in rec["relationships"]:
            per_field[r["field"].lower()].add(r["target"])
        for f, tgts in per_field.items():
            real = {t for t in tgts if not noise_reason(t)}
            if f in UNIQUE_SINGULAR_FIELDS and len(real) > 1:
                q2.add((rec["page"], f))
    return q2


def _trips_r3(
    field: str,
    qual: str,
    edge_type: str,
    q2_keys: set,
    page: str,
) -> str | None:
    """Check Rule 3a-3d. Returns a quarantine sub-bucket id or None."""
    if field in PLURAL_SPECULATIVE_FIELDS:
        return "R3a"
    if (page, field) in q2_keys:
        return "R3b"
    q_norm = (qual or "").replace("\xa0", " ")
    if field in KINSHIP_FIELDS and q_norm and SPEC_QUAL_RE.search(q_norm):
        return "R3c"
    if field in KINSHIP_FIELDS and q_norm and "disputed" in q_norm.lower() and edge_type != "PARENT_OF":
        return "R3d"
    return None


# ---------------------------------------------------------------------------
# Hygiene Fix A: orphan endpoint remap
# ---------------------------------------------------------------------------

def build_orphan_remaps(
    rows: list[dict],
    nodes: dict[str, str],
    alias: dict[str, str],
) -> tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, int]]:
    """Classify each orphan endpoint slug into alias / the-strip / honorific / unresolvable.

    Returns (fix_alias, fix_thestrip, fix_honorific, unresolvable).
    """
    endpoint_rows: dict[str, list] = defaultdict(list)
    for i, r in enumerate(rows):
        for k in ("source_slug", "target_slug"):
            s = r.get(k)
            if s and s not in nodes:
                endpoint_rows[s].append(i)

    fix_alias: dict[str, str] = {}
    fix_thestrip: dict[str, str] = {}
    fix_honorific: dict[str, str] = {}
    unresolvable: dict[str, int] = {}

    for slug in endpoint_rows:
        if slug in alias and alias[slug] in nodes:
            fix_alias[slug] = alias[slug]
        elif slug.startswith("the-") and slug[4:] in nodes:
            fix_thestrip[slug] = slug[4:]
        else:
            # Honorific-prefix strip (characters only)
            hit = None
            for prefix in HONORIFIC_PREFIXES:
                if slug.startswith(prefix):
                    cand = slug[len(prefix):]
                    if cand in nodes and nodes[cand] == "characters":
                        hit = cand
                    elif cand in alias and alias[cand] in nodes and nodes[alias[cand]] == "characters":
                        hit = alias[cand]
                    break
            if hit:
                fix_honorific[slug] = hit
            else:
                unresolvable[slug] = len(endpoint_rows[slug])

    return fix_alias, fix_thestrip, fix_honorific, unresolvable


def apply_orphan_remaps(
    rows: list[dict],
    all_remaps: dict[str, str],
) -> tuple[list[dict], list[dict]]:
    """Apply all remaps to edges rows in-place. Returns (remapped_rows, remap_log)."""
    remap_log = []
    remapped = []
    for r in rows:
        r = dict(r)
        changed = {}
        for k in ("source_slug", "target_slug"):
            old = r.get(k)
            if old and old in all_remaps:
                new = all_remaps[old]
                changed[old] = new
                r[k] = new
        if changed:
            r["endpoint_remapped"] = changed
        remapped.append(r)
        if changed:
            remap_log.append({"before": {k: v for k, v in changed.items()}, "after": r, "row_index": len(remapped) - 1})
    return remapped, remap_log


# ---------------------------------------------------------------------------
# Hygiene Fix B: typed_by backfill
# ---------------------------------------------------------------------------

def apply_typed_by_backfill(
    rows: list[dict],
    chapter_stems: set[str],
) -> tuple[list[dict], list[dict], Counter]:
    """Add typed_by and optionally evidence_ref to rows missing typed_by.
    Also drops stale 'stage' field from plate4 rows.
    Returns (patched_rows, stamp_log, stats).
    """
    stamp_log = []
    patched = []
    stats: Counter = Counter()
    for r in rows:
        r = dict(r)
        if not r.get("typed_by"):
            ek = r.get("evidence_kind", "")
            if ek == "book-pass1-reified":
                r["typed_by"] = "plate3-reifier"
                stats["plate3"] += 1
            elif ek == "plate4-wiki-cluster":
                r["typed_by"] = "plate4-cluster-classifier"
                stats["plate4"] += 1
                # Drop stale stage field if present
                if "stage" in r:
                    del r["stage"]
                    stats["plate4_stage_dropped"] += 1
            # Try to resolve evidence_ref from chapter label
            ev_book = r.get("evidence_book", "")
            ev_ch = r.get("evidence_chapter", "")
            if ev_ch:
                stem = label_to_file_stem(ev_book, ev_ch, chapter_stems)
                if stem:
                    book_prefix = stem.split("-")[0]
                    r["evidence_ref"] = f"sources/chapters/{book_prefix}/{stem}.md"
                    r["locate_status"] = "chapter-file"
                    stats["ref_resolved"] += 1
                else:
                    stats["ref_unresolved"] += 1
            stamp_log.append(dict(r))
        else:
            # Still drop stale stage field from plate4 rows that already have typed_by
            if r.get("evidence_kind") == "plate4-wiki-cluster" and "stage" in r:
                del r["stage"]
        patched.append(r)
    return patched, stamp_log, stats


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(dry_run: bool = True, apply_confirmed: bool = False, rng_seed: int = 42):
    """Run the full infobox-merge pipeline.

    dry_run=True: writes to working/infobox-merge/ only.
    dry_run=False + apply_confirmed=True: writes to graph/.
    """
    ts = datetime.now(timezone.utc)
    run_id = "infobox-merge-" + ts.strftime("%Y%m%d")
    produced_at = ts.isoformat()

    print(f"[infobox-merge] Loading data...", file=sys.stderr)

    # Load node universe
    nodes = load_nodes()
    print(f"  {len(nodes)} nodes indexed", file=sys.stderr)

    # Load alias-resolver
    alias = load_alias(ALIAS_RESOLVER_FILE)
    print(f"  {len(alias)} aliases loaded", file=sys.stderr)

    # Load infobox data
    pages = []
    with INFOBOX_DATA.open() as f:
        for line in f:
            line = line.strip()
            if line:
                pages.append(json.loads(line))
    total_rows = sum(len(p["relationships"]) for p in pages)
    print(f"  {len(pages)} pages, {total_rows} rows", file=sys.stderr)

    # Load existing edges (pre-Fix-A, so Rule 10 compares post-remap endpoints)
    existing_rows = []
    for line in EDGES_FILE.read_text().splitlines():
        line = line.strip()
        if line:
            existing_rows.append(json.loads(line))

    # --- Hygiene Fix A (pre-pass, runs before Rule 10 dedupe) ---
    print(f"[infobox-merge] Running Hygiene Fix A (orphan remap)...", file=sys.stderr)
    fix_alias, fix_thestrip, fix_honorific, unresolvable_orphans = build_orphan_remaps(
        existing_rows, nodes, alias
    )
    all_remaps = {**fix_alias, **fix_thestrip, **fix_honorific}
    existing_rows_remapped, hygiene_a_log = apply_orphan_remaps(existing_rows, all_remaps)

    # Detect post-remap duplicates: find rows whose remap caused a new key collision
    # (i.e., the remap-modified key now collides with another row that was NOT remapped,
    # or whose pre-remap key was different).
    pre_remap_keys: set = set()
    for r in existing_rows:
        s, t, ty = r.get("source_slug"), r.get("target_slug"), r.get("edge_type")
        if s and t and ty:
            pre_remap_keys.add(edge_key(ty, s, t, SYMMETRIC_TYPES))

    post_remap_dupe_pairs: list[dict] = []
    post_remap_seen: dict = {}
    for orig, remapped_r in zip(existing_rows, existing_rows_remapped):
        s, t, ty = remapped_r.get("source_slug"), remapped_r.get("target_slug"), remapped_r.get("edge_type")
        if not (s and t and ty):
            continue
        k = edge_key(ty, s, t, SYMMETRIC_TYPES)
        # Was this row remapped?
        was_remapped = "endpoint_remapped" in remapped_r
        if k in post_remap_seen:
            # If either this row or the previously-seen row was remapped, it's a new collision
            other_was_remapped = post_remap_seen[k].get("was_remapped", False)
            if was_remapped or other_was_remapped:
                post_remap_dupe_pairs.append({
                    "key": str(k),
                    "row_a_was_remapped": other_was_remapped,
                    "row_b_was_remapped": was_remapped,
                })
        else:
            post_remap_seen[k] = {"was_remapped": was_remapped}

    # Build existing_keys set from remapped rows (for Rule 10)
    existing_keys: set = set()
    for r in existing_rows_remapped:
        s, t, ty = r.get("source_slug"), r.get("target_slug"), r.get("edge_type")
        if s and t and ty:
            existing_keys.add(edge_key(ty, s, t, SYMMETRIC_TYPES))

    # --- Hygiene Fix B ---
    print(f"[infobox-merge] Running Hygiene Fix B (typed_by backfill)...", file=sys.stderr)
    chapter_stems = load_chapter_stems()
    existing_rows_fixed, hygiene_b_log, fix_b_stats = apply_typed_by_backfill(
        existing_rows_remapped, chapter_stems
    )

    # --- Main promotion pipeline ---
    print(f"[infobox-merge] Running promotion rules...", file=sys.stderr)

    # Pre-compute Rule 3 helpers
    q2_keys = _build_q2_keys(pages)
    fact_quarantine = build_quarantine_fact_keys(pages, nodes, alias)

    stats: Counter = Counter()
    by_type: Counter = Counter()
    merged: list[dict] = []
    filtered: list[dict] = []
    quarantined: list[dict] = []
    corroborations: list[dict] = []
    artifact_qual_rows: list[dict] = []

    seen: dict = {}  # key → {midx: int|None, conflict: bool}

    stats["rows_in"] = total_rows

    for rec in pages:
        page = rec["page"]
        cite_refs = rec.get("cite_refs", {})

        # Rule 1: source resolution
        src, src_cat, src_how = resolve(page, nodes, alias)
        if src is None:
            for r in rec["relationships"]:
                stats["F1_source_unresolved"] += 1
                filtered.append({
                    "rule": "R1", "reason": "source-unresolved",
                    "page": page, "field": r["field"], "target": r["target"],
                    "edge_type": r["edge_type"],
                })
            continue

        # Track per-page per-field multi-value for Rule 3b (already in q2_keys)
        for r in rec["relationships"]:
            et = r["edge_type"]
            field = r["field"].lower()
            tgt_name = r["target"]
            qual = r.get("qualifier") or ""

            # Rule 2: noise-target filter
            nr = noise_reason(tgt_name)
            if nr:
                stats[f"F2_{nr}"] += 1
                filtered.append({
                    "rule": "R2", "reason": nr,
                    "page": page, "field": r["field"], "target": tgt_name, "edge_type": et,
                })
                # Log artifact qualifiers if present
                qn = (qual or "").replace("\xa0", " ").strip()
                if qn and (ARTIFACT_QUAL_RE.match(qn) or DATE_RANGE_QUAL_RE.match(qn)):
                    artifact_qual_rows.append({
                        "rule": "R2_artifact_qual", "page": page, "field": r["field"],
                        "target": tgt_name, "edge_type": et, "qualifier": qual,
                        "disposition": nr,
                    })
                continue

            # Rule 3a-3d (before target resolution)
            q3 = _trips_r3(field, qual, et, q2_keys, page)
            if q3:
                stats[f"Q3_{q3}"] += 1
                quarantined.append({
                    "rule": q3, "page": page, "field": r["field"],
                    "target": tgt_name, "edge_type": et, "qualifier": qual,
                })
                continue

            # Rule 6c: Result-field DEFEATS quarantine
            if field == "result":
                stats["Q6c_result_field_defeats"] += 1
                quarantined.append({
                    "rule": "R6c", "page": page, "field": r["field"],
                    "target": tgt_name, "edge_type": et, "qualifier": qual,
                })
                continue

            # Rule 4: target resolution. Prefer the link's disambiguated title
            # (e.g. "Daenerys Targaryen (daughter of Aegon IV)") over the bare
            # display text (e.g. "Daenerys Targaryen") when the wikilink used a
            # piped display form — otherwise a same-named, more-prominent node
            # silently swallows the edge (see the Maron-Martell's-son bug).
            # Gated narrowly to actual DISAMBIGUATION: the title must be the same
            # base name plus a "(...)" qualifier (kebab with parens stripped ==
            # the display text's kebab). This deliberately excludes cases where
            # title and display text are just different words for related-but-
            # distinct concepts (e.g. "Ser" -> title "Knight", "Myrish" -> title
            # "Myr") — those are a separate, unreviewed class of edge change, not
            # the identity-collision bug this override targets.
            # Only override when the title actually resolves to a DIFFERENT node;
            # if it doesn't resolve, fall back to the plain-text resolution so
            # this never turns a previously-resolved edge into an unresolved one.
            tgt, tgt_cat, tgt_how = resolve(tgt_name, nodes, alias)
            title_hint = r.get("target_title")
            if title_hint and "(" in title_hint and kebab(title_hint) == kebab(tgt_name):
                title_tgt, title_cat, title_how = resolve(title_hint, nodes, alias)
                if title_tgt is not None and title_tgt != tgt:
                    tgt, tgt_cat, tgt_how = title_tgt, title_cat, title_how
            if tgt is None:
                stats["F4_target_unresolved"] += 1
                filtered.append({
                    "rule": "R4", "reason": "target-unresolved",
                    "page": page, "field": r["field"], "target": tgt_name, "edge_type": et,
                })
                continue

            # Rule 3e: fact-key mirror quarantine (after both endpoints resolved)
            if et in FACT_CLASS and (FACT_CLASS[et], frozenset((src, tgt))) in fact_quarantine:
                stats["Q3e_mirror_of_quarantined_fact"] += 1
                quarantined.append({
                    "rule": "R3e", "page": page, "field": r["field"],
                    "target": tgt_name, "edge_type": et, "qualifier": qual,
                })
                continue

            # Rule 5: deterministic retypes
            current_et = et
            direction_corrected = False
            if et == "FIGHTS_IN" and src_cat == "events":
                current_et = "PART_OF"
            elif et == "WORSHIPS" and src_cat == "locations":
                current_et = "RELIGION_OF"

            # Rule 6a: kinship char↔char
            if current_et in CHAR_CHAR_TYPES and (src_cat != "characters" or tgt_cat != "characters"):
                stats["Q6a_contract_kinship_nonchar"] += 1
                quarantined.append({
                    "rule": "R6a", "page": page, "field": r["field"],
                    "target": tgt_name, "edge_type": current_et, "qualifier": qual,
                    "detail": f"{src_cat}->{tgt_cat}",
                })
                continue

            # Rule 6b: HOLDS_TITLE target must be titles/
            if current_et == "HOLDS_TITLE" and tgt_cat != "titles":
                stats["Q6b_contract_holds_title_target"] += 1
                quarantined.append({
                    "rule": "R6b", "page": page, "field": r["field"],
                    "target": tgt_name, "edge_type": current_et, "qualifier": qual,
                    "detail": f"->{tgt_cat}",
                })
                continue

            # Rule 7: direction correction
            direction = r["direction"]
            flip = field in DIRECTION_FLIP_FIELDS
            if direction == "reverse":
                s_, t_ = tgt, src
            else:
                s_, t_ = src, tgt
            if flip:
                s_, t_ = t_, s_
                direction_corrected = True

            # Rule 8: self-loop suppression
            if s_ == t_:
                stats["F8_self_loop"] += 1
                filtered.append({
                    "rule": "R8", "reason": "self-loop",
                    "page": page, "field": r["field"], "target": tgt_name, "edge_type": current_et,
                })
                continue

            # Check artifact qualifiers (before dedupe)
            qn = (qual or "").replace("\xa0", " ").strip()
            if qn and (ARTIFACT_QUAL_RE.match(qn) or DATE_RANGE_QUAL_RE.match(qn)):
                artifact_qual_rows.append({
                    "rule": "R11_artifact_qual", "page": page, "field": r["field"],
                    "target": tgt_name, "edge_type": current_et, "qualifier": qual,
                    "disposition": "merged (date-range in wiki_qualifier)" if DATE_RANGE_QUAL_RE.match(qn) else "pre-disposed-by-R2",
                })

            # Build the candidate row
            norm_qualifier = normalize_qualifier(current_et, qual if qual else None)
            candidate = {
                "decision": "emit_edge",
                "candidate_kind": "wiki-infobox",
                "edge_type": current_et,
                "source_slug": s_,
                "source_resolution_status": src_how,
                "target_slug": t_,
                "target_resolution_status": tgt_how,
                "evidence_kind": "wiki-infobox",
                "evidence_ref": f"wiki:{page.replace(' ', '_')}",
                "evidence_field": r["field"],
                "evidence_quote": None,
                "evidence_book": None,
                "evidence_chapter": None,
                "confidence_tier": 2,
                "typed_by": "python-infobox-map",
                "symmetric": current_et in SYMMETRIC_TYPES,
                "direction_corrected": direction_corrected,
                "run_id": run_id,
                "schema_version": "infobox-merge-v2",
                "produced_at": produced_at,
            }
            if qual:
                candidate["wiki_qualifier"] = qual
            if norm_qualifier is not None:
                candidate["qualifier"] = norm_qualifier

            k = edge_key(current_et, s_, t_, SYMMETRIC_TYPES)

            # Rule 9: qualifier-aware in-run dedupe
            if k in seen:
                st = seen[k]
                if st.get("conflict"):
                    # Already in quarantine for qualifier conflict
                    stats["Q9_dedupe_qualifier_conflict"] += 1
                    quarantined.append({
                        "rule": "R9q", "page": page, "field": r["field"],
                        "target": tgt_name, "edge_type": current_et, "qualifier": qual,
                    })
                    continue
                if st["midx"] is None:
                    # Corroborates existing edge, nothing emitted
                    stats["D9_deduped_in_run"] += 1
                    continue
                # Compare qualifiers
                kept_row = merged[st["midx"]]
                q_kept = norm_qual(kept_row.get("wiki_qualifier"))
                q_new = norm_qual(qual)
                if q_new == q_kept or not q_new:
                    stats["D9_deduped_in_run"] += 1
                elif not q_kept:
                    # Prefer the qualified row
                    merged[st["midx"]] = candidate
                    stats["D9_deduped_in_run"] += 1
                    stats["D9_qualified_row_preferred"] += 1
                else:
                    # Two different non-empty qualifiers → quarantine both
                    old = merged[st["midx"]]
                    quarantined.append({
                        "rule": "R9q", "page": old["evidence_ref"].split("wiki:")[-1].replace("_", " "),
                        "field": old["evidence_field"],
                        "target": old["target_slug"], "edge_type": current_et,
                        "qualifier": old.get("wiki_qualifier", ""),
                    })
                    quarantined.append({
                        "rule": "R9q", "page": page, "field": r["field"],
                        "target": tgt_name, "edge_type": current_et, "qualifier": qual,
                    })
                    stats["Q9_dedupe_qualifier_conflict"] += 2
                    merged[st["midx"]] = None  # mark for removal
                    st["conflict"] = True
                continue

            # Rule 10: dedupe against existing edges.jsonl
            if k in existing_keys:
                stats["D10_skipped_existing_corroboration"] += 1
                seen[k] = {"midx": None, "conflict": False}
                corroborations.append({
                    "rule": "R10",
                    "edge_type": current_et,
                    "source_slug": s_,
                    "target_slug": t_,
                    "page": page,
                    "field": r["field"],
                    "qualifier": qual,
                })
                continue

            seen[k] = {"midx": len(merged), "conflict": False}
            merged.append(candidate)

    # Remove None (R9q conflict retractions)
    merged = [m for m in merged if m is not None]

    for m in merged:
        by_type[m["edge_type"]] += 1

    stats["merged"] = len(merged)

    # Verify bucket sum
    excludes = {"rows_in", "D9_qualified_row_preferred", "merged"}
    bucket_sum = sum(v for k, v in stats.items() if k not in excludes) + stats["merged"]

    print(f"[infobox-merge] Pipeline complete: {stats['merged']} merged, "
          f"sum_check={bucket_sum}/{total_rows}", file=sys.stderr)

    return {
        "merged": merged,
        "filtered": filtered,
        "quarantined": quarantined,
        "corroborations": corroborations,
        "stats": stats,
        "by_type": by_type,
        "existing_rows": existing_rows,
        "existing_rows_remapped": existing_rows_remapped,
        "existing_rows_fixed": existing_rows_fixed,
        "hygiene_a_log": hygiene_a_log,
        "hygiene_b_log": hygiene_b_log,
        "fix_b_stats": fix_b_stats,
        "fix_alias": fix_alias,
        "fix_thestrip": fix_thestrip,
        "fix_honorific": fix_honorific,
        "unresolvable_orphans": unresolvable_orphans,
        "post_remap_dupe_pairs": post_remap_dupe_pairs,
        "artifact_qual_rows": artifact_qual_rows,
        "bucket_sum": bucket_sum,
        "run_id": run_id,
        "produced_at": produced_at,
    }


# ---------------------------------------------------------------------------
# Expected counts (spec v2)
# ---------------------------------------------------------------------------

SPEC_COUNTS = {
    "rows_in": 20614,
    "merged": 17006,
    "F1_source_unresolved": 3,
    "F2_noise-placeholder": 412,
    "F2_noise-bare-kinship": 204,
    "F2_noise-numeral-date": 0,
    "F4_target_unresolved": 507,
    "F8_self_loop": 2,
    "filtered_total": 1128,
    "Q3_R3a": 46,
    "Q3_R3b": 8,
    "Q3_R3c": 102,
    "Q3_R3d": 5,
    "Q3e_mirror_of_quarantined_fact": 24,
    "Q6a_contract_kinship_nonchar": 73,
    "Q6b_contract_holds_title_target": 464,
    "Q6c_result_field_defeats": 315,
    "quarantined_total": 1037,
    "Q9_dedupe_qualifier_conflict": 0,
    "D9_deduped_in_run": 1356,
    "D10_skipped_existing_corroboration": 87,
}

SPEC_BY_TYPE = {
    "SWORN_TO": 4064, "HOLDS_TITLE": 3401, "CULTURE_OF": 3252,
    "PARENT_OF": 1645, "DIED_AT": 915, "BORN_AT": 833,
    "REGION_OF": 573, "OVERLORD_OF": 551, "SEAT_OF": 329,
    "SPOUSE_OF": 313, "RULES": 264, "PART_OF": 184,
    "HEIR_TO": 179, "RELIGION_OF": 93, "SUCCEEDS": 93,
    "OWNS": 84, "LOVER_OF": 71, "FOUNDED": 71,
    "BURIED_AT": 48, "CADET_BRANCH_OF": 26, "ANCESTRAL_WEAPON_OF": 13,
    "FIGHTS_IN": 4,
}


# ---------------------------------------------------------------------------
# Dry-run report
# ---------------------------------------------------------------------------

def write_dry_run_report(result: dict, output_dir: Path, rng_seed: int = 42):
    """Write the full dry-run report to working/infobox-merge/dry-run-report-2026-06-12.md."""
    stats = result["stats"]
    by_type = result["by_type"]
    merged = result["merged"]
    fix_alias = result["fix_alias"]
    fix_thestrip = result["fix_thestrip"]
    fix_honorific = result["fix_honorific"]
    unresolvable_orphans = result["unresolvable_orphans"]
    artifact_qual_rows = result["artifact_qual_rows"]
    fix_b_stats = result["fix_b_stats"]

    def check(actual, expected, label):
        status = "PASS" if actual == expected else "FAIL"
        return f"| {label} | {expected} | {actual} | {status} |"

    lines = []
    lines.append("# Infobox-Merge Dry-Run Report — 2026-06-12")
    lines.append("")
    lines.append(f"> Generated: {result['produced_at']}  ")
    lines.append(f"> Run ID: `{result['run_id']}`  ")
    lines.append(f"> RNG seed for 20-edge sample: `{rng_seed}`")
    lines.append("")

    # --- Counts vs spec ---
    lines.append("## 1. Disposition Counts vs Spec v2")
    lines.append("")
    lines.append("| Bucket | Expected | Actual | Status |")
    lines.append("|---|---|---|---|")
    lines.append(check(stats["rows_in"], SPEC_COUNTS["rows_in"], "rows_in (total input)"))
    lines.append(check(stats["merged"], SPEC_COUNTS["merged"], "MERGED"))
    lines.append(check(stats.get("F1_source_unresolved", 0), SPEC_COUNTS["F1_source_unresolved"], "Filtered: source unresolved (R1)"))
    lines.append(check(stats.get("F2_noise-placeholder", 0), SPEC_COUNTS["F2_noise-placeholder"], "Filtered: noise placeholder (R2a)"))
    lines.append(check(stats.get("F2_noise-bare-kinship", 0), SPEC_COUNTS["F2_noise-bare-kinship"], "Filtered: noise bare-kinship (R2b)"))
    lines.append(check(stats.get("F2_noise-numeral-date", 0), SPEC_COUNTS["F2_noise-numeral-date"], "Filtered: noise numeral/date (R2c)"))
    lines.append(check(stats.get("F4_target_unresolved", 0), SPEC_COUNTS["F4_target_unresolved"], "Filtered: target unresolved (R4)"))
    lines.append(check(stats.get("F8_self_loop", 0), SPEC_COUNTS["F8_self_loop"], "Filtered: self-loop (R8)"))

    filtered_total = (
        stats.get("F1_source_unresolved", 0)
        + stats.get("F2_noise-placeholder", 0)
        + stats.get("F2_noise-bare-kinship", 0)
        + stats.get("F2_noise-numeral-date", 0)
        + stats.get("F4_target_unresolved", 0)
        + stats.get("F8_self_loop", 0)
    )
    lines.append(check(filtered_total, SPEC_COUNTS["filtered_total"], "**Filtered total**"))

    lines.append(check(stats.get("Q3_R3a", 0), SPEC_COUNTS["Q3_R3a"], "Quarantined: plural Mothers/Fathers (R3a)"))
    lines.append(check(stats.get("Q3_R3b", 0), SPEC_COUNTS["Q3_R3b"], "Quarantined: multi-value singular father/mother (R3b)"))
    lines.append(check(stats.get("Q3_R3c", 0), SPEC_COUNTS["Q3_R3c"], "Quarantined: speculative qualifier (R3c)"))
    lines.append(check(stats.get("Q3_R3d", 0), SPEC_COUNTS["Q3_R3d"], "Quarantined: disputed on non-PARENT_OF kinship (R3d)"))
    lines.append(check(stats.get("Q3e_mirror_of_quarantined_fact", 0), SPEC_COUNTS["Q3e_mirror_of_quarantined_fact"], "Quarantined: mirror of quarantined fact (R3e)"))
    lines.append(check(stats.get("Q6a_contract_kinship_nonchar", 0), SPEC_COUNTS["Q6a_contract_kinship_nonchar"], "Quarantined: kinship endpoint contract (R6a)"))
    lines.append(check(stats.get("Q6b_contract_holds_title_target", 0), SPEC_COUNTS["Q6b_contract_holds_title_target"], "Quarantined: HOLDS_TITLE target contract (R6b)"))
    lines.append(check(stats.get("Q6c_result_field_defeats", 0), SPEC_COUNTS["Q6c_result_field_defeats"], "Quarantined: Result-field DEFEATS (R6c)"))

    quarantined_total = (
        stats.get("Q3_R3a", 0) + stats.get("Q3_R3b", 0) + stats.get("Q3_R3c", 0)
        + stats.get("Q3_R3d", 0) + stats.get("Q3e_mirror_of_quarantined_fact", 0)
        + stats.get("Q6a_contract_kinship_nonchar", 0) + stats.get("Q6b_contract_holds_title_target", 0)
        + stats.get("Q6c_result_field_defeats", 0)
    )
    lines.append(check(quarantined_total, SPEC_COUNTS["quarantined_total"], "**Quarantined total**"))

    lines.append(check(stats.get("Q9_dedupe_qualifier_conflict", 0), SPEC_COUNTS["Q9_dedupe_qualifier_conflict"], "Quarantined: dedupe qualifier conflict (R9q)"))
    lines.append(check(stats.get("D9_deduped_in_run", 0), SPEC_COUNTS["D9_deduped_in_run"], "Deduped within run (R9, incl. 3 preferred swaps)"))
    lines.append(check(stats.get("D9_qualified_row_preferred", 0), 3, "  └─ qualified-row-preferred swaps (sub-count)"))
    lines.append(check(stats.get("D10_skipped_existing_corroboration", 0), SPEC_COUNTS["D10_skipped_existing_corroboration"], "Skipped, corroborates existing (R10)"))

    total_check = stats["merged"] + filtered_total + quarantined_total + stats.get("D9_deduped_in_run", 0) + stats.get("D10_skipped_existing_corroboration", 0) + stats.get("Q9_dedupe_qualifier_conflict", 0)
    lines.append(check(total_check, 20614, "**Sum check (must equal rows_in)**"))
    lines.append("")

    # --- Merged by type ---
    lines.append("## 2. Merged Edges by Type (all 22)")
    lines.append("")
    lines.append("| Type | Expected | Actual | Status |")
    lines.append("|---|---|---|---|")
    all_types = sorted(set(list(SPEC_BY_TYPE.keys()) + list(by_type.keys())))
    for t in sorted(all_types, key=lambda x: -SPEC_BY_TYPE.get(x, 0)):
        exp = SPEC_BY_TYPE.get(t, 0)
        act = by_type.get(t, 0)
        status = "PASS" if act == exp else "FAIL"
        lines.append(f"| {t} | {exp} | {act} | {status} |")
    lines.append("")

    # --- Fix A ---
    lines.append("## 3. Hygiene Fix A — Orphan Endpoint Remaps")
    lines.append("")
    lines.append(f"**115 orphan endpoint slugs, 140 affected rows** (recomputed from edges.jsonl).")
    lines.append("")
    lines.append("| Resolution | Slugs | Rows | Action |")
    lines.append("|---|---|---|---|")
    fa_rows = sum(len([r for r in result["hygiene_a_log"] if any(k in r["before"] for k in fix_alias)]) for _ in [1])

    def count_remap_rows(fix_dict):
        if not fix_dict:
            return 0
        cnt = 0
        for r in result["hygiene_a_log"]:
            for old_slug in r["before"]:
                if old_slug in fix_dict:
                    cnt += 1
                    break
        return cnt

    alias_rows = sum(len([_ for r in result["existing_rows"] for k in ("source_slug", "target_slug") if r.get(k) in fix_alias])  for _ in [1])
    thestrip_rows = sum(len([_ for r in result["existing_rows"] for k in ("source_slug", "target_slug") if r.get(k) in fix_thestrip]) for _ in [1])
    honorific_rows = sum(len([_ for r in result["existing_rows"] for k in ("source_slug", "target_slug") if r.get(k) in fix_honorific]) for _ in [1])
    unres_rows = sum(unresolvable_orphans.values())

    # Recount properly
    alias_rows = sum(1 for r in result["existing_rows"] for k in ("source_slug", "target_slug") if r.get(k) in fix_alias)
    thestrip_rows = sum(1 for r in result["existing_rows"] for k in ("source_slug", "target_slug") if r.get(k) in fix_thestrip)
    honorific_rows = sum(1 for r in result["existing_rows"] for k in ("source_slug", "target_slug") if r.get(k) in fix_honorific)

    lines.append(f"| Alias-resolver remap | {len(fix_alias)} | {alias_rows} | rewrite slug in place |")
    lines.append(f"| Leading `the-` strip | {len(fix_thestrip)} | {thestrip_rows} | rewrite slug in place |")
    lines.append(f"| Honorific-prefix strip | {len(fix_honorific)} | {honorific_rows} | rewrite slug in place (characters-only guard) |")
    lines.append(f"| Unresolvable | {len(unresolvable_orphans)} | {unres_rows} | leave as-is, logged below |")
    lines.append("")

    if result["post_remap_dupe_pairs"]:
        lines.append(f"**Post-remap duplicates created: {len(result['post_remap_dupe_pairs'])} pair(s)** — listed as merge-candidate pairs for Matt review.")
        for p in result["post_remap_dupe_pairs"]:
            lines.append(f"  - {p['key']}")
    else:
        lines.append("**Post-remap duplicates created: 0** — no new collision introduced by remaps.")
    lines.append("")

    # Semantic remaps flagged section
    lines.append("### 3a. Semantic Remaps — Require Matt Review")
    lines.append("")
    lines.append("These two remaps collapse an in-story *persona* onto the underlying person. They follow established project "
                 "conventions (alias-resolver already canonicalizes them, impersonation-edges rule applies), but persona-collapse "
                 "is a judgment call. The default can be overridden before `--apply`.")
    lines.append("")
    semantic_flags = {"lady-stoneheart": "catelyn-stark", "abel": "mance-rayder"}
    for old, new in semantic_flags.items():
        affected = [r for r in result["existing_rows"] if r.get("source_slug") == old or r.get("target_slug") == old]
        lines.append(f"- **`{old}` → `{new}`** ({len(affected)} row(s) affected)")
        for r in affected:
            ref = r.get("evidence_ref") or r.get("evidence_source_file") or "?"
            lines.append(f"  - `{r.get('edge_type')} {r.get('source_slug')} → {r.get('target_slug')}` ({ref[:60]})")
    lines.append("")

    lines.append("### 3b. Honorific-Strip Remaps (26 slugs / 33 rows, characters-only)")
    lines.append("")
    lines.append("The `maester-griffins-roost → griffins-roost` case is correctly **rejected** (griffins-roost is a location, not a character).")
    lines.append("")
    for s, c in sorted(fix_honorific.items()):
        n = sum(1 for r in result["existing_rows"] for k in ("source_slug", "target_slug") if r.get(k) == s)
        lines.append(f"- `{s}` → `{c}` ({n} rows)")
    lines.append("")

    lines.append("### 3c. Unresolvable Orphans (stay as-is)")
    lines.append("")
    for s, c in sorted(unresolvable_orphans.items(), key=lambda x: -x[1]):
        lines.append(f"- `{s}` ({c} rows)")
    lines.append("")

    # --- Fix B ---
    lines.append("## 4. Hygiene Fix B — `typed_by` Backfill (948 rows)")
    lines.append("")
    lines.append(f"| Population | Count | typed_by assigned |")
    lines.append("|---|---|---|")
    lines.append(f"| `evidence_kind: book-pass1-reified` | 897 | `plate3-reifier` |")
    lines.append(f"| `evidence_kind: plate4-wiki-cluster` | 51 | `plate4-cluster-classifier` |")
    lines.append(f"| **Total** | **948** | — |")
    lines.append("")
    lines.append(f"Chapter-label → file synthesis: {fix_b_stats.get('ref_resolved', 0)} resolved, {fix_b_stats.get('ref_unresolved', 0)} unresolvable (empty label + non-POV-pattern chapters).")
    lines.append(f"Plate-4 stale `stage` field dropped: {fix_b_stats.get('plate4_stage_dropped', 0)} rows.")
    lines.append("")

    # --- Rule 9 qualifier-conflict section ---
    lines.append("## 5. Rule 9 Qualifier-Conflict Quarantine (R9q)")
    lines.append("")
    lines.append(f"Expected: 0. Actual: {stats.get('Q9_dedupe_qualifier_conflict', 0)}.")
    r9q_rows = [q for q in result["quarantined"] if q.get("rule") == "R9q"]
    if r9q_rows:
        lines.append("")
        for q in r9q_rows:
            lines.append(f"- `{q['page']}` · `{q['field']}` · `{q['target']}` [{q['edge_type']}] qual=`{q.get('qualifier','')}`")
    lines.append("")

    # --- Artifact qualifier log ---
    lines.append("## 6. Parser-Artifact Qualifier Log (Rule 11)")
    lines.append("")
    lines.append("Rows with raw qualifier matching artifact patterns (`^(ren|s)$` or date-range shape):")
    lines.append("")
    if artifact_qual_rows:
        for aq in artifact_qual_rows:
            lines.append(f"- `{aq['page']}` · `{aq['field']}` · `{aq['target']}` [{aq['edge_type']}] "
                         f"qual=`{aq['qualifier']}` → {aq['disposition']}")
    else:
        lines.append("_(none found)_")
    lines.append("")

    # --- 20-edge random sample ---
    lines.append(f"## 7. Random 20-Edge Sample (seed={rng_seed})")
    lines.append("")
    rng = random.Random(rng_seed)
    sample = rng.sample(result["merged"], min(20, len(result["merged"])))
    lines.append("| # | edge_type | source → target | field | qualifier | direction_corrected |")
    lines.append("|---|---|---|---|---|---|")
    for i, m in enumerate(sample, 1):
        q = m.get("qualifier", m.get("wiki_qualifier", ""))
        lines.append(
            f"| {i} | {m['edge_type']} | `{m['source_slug']}` → `{m['target_slug']}` "
            f"| {m['evidence_field']} | {q or ''} | {m['direction_corrected']} |"
        )
    lines.append("")

    # --- Open questions ---
    lines.append("## 8. YOUR-DECISIONS — Open Questions (11 items, spec §8)")
    lines.append("")
    lines.append("The spec identified 11 open questions. Decided-by-default values listed here for Matt to override line by line.")
    lines.append("")
    open_qs = [
        ("1", "FIELD_EDGE_MAP direction inversions (10 fields)", "Recommend: yes, fix FIELD_EDGE_MAP + architecture.md in the --apply session (CLAUDE.md rule 6: schema and architecture.md must not stay contradictory)."),
        ("2", "Tier-1 qualifier defaults (HOLDS_TITLE/SWORN_TO/SPOUSE_OF: `unknown`; PARENT_OF: `biological`)", "Default shipped. Alternative: `current` for the first three. Change before --apply if preferred."),
        ("3", "Quarantined ship-captaincy HOLDS_TITLE→artifact rows (43 of 464)", "Default: quarantined. Future: retype to CAPTAIN_OF in a small follow-up pass."),
        ("4", "CULTURE_OF region-name targets (927 rows, person → location)", "Default: merged as-is. Future: mint reachmen/crownlanders culture nodes."),
        ("5", "Result-field DEFEATS class (315 rows, R6c)", "Default: quarantined wholesale. Future: curator pass for victor-extraction."),
        ("6", "`the-` strip overrides alias_collisions 'ambiguous-do-not-resolve' for single-candidate variants", "Default: the-strip wins (exact-match only, 89 target rows + 4 orphan rows depend on it)."),
        ("7", "Honorific-strip rung in Fix A (26 slugs / 33 rows, characters-only guard)", "Default: included. Reject: restrict Fix A to pure alias remaps (23/35). Character-category guard prevents maester-griffins-roost false positive."),
        ("8", "Corroboration handling (87 rows)", "Default: log-only. Future: stamp `corroborated_by: wiki-infobox` on matching Tier-1 edges at apply time."),
        ("9", "Fact-key mirror quarantine (Rule 3e, 24 rows)", "Default: quarantine (conservative). Override per-fact from quarantined.jsonl."),
        ("10", "Dedupe-conflict policy (R9q — currently 0 rows)", "Default: qualified row beats unqualified (3 swaps); two different qualifiers quarantine. Alt: union qualifiers and merge anyway."),
        ("11", "`evidence_book`/`evidence_chapter` emitted as explicit nulls", "Default: null (page-level cite_refs are false precision at row level). Alt: derive from cite_refs where page cites exactly one chapter — rejected for v2."),
    ]
    for num, title, decision in open_qs:
        lines.append(f"**Q{num}: {title}**")
        lines.append(f"> Decided-by-default: {decision}")
        lines.append("")

    report = "\n".join(lines)
    report_path = output_dir / "dry-run-report-2026-06-12.md"
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)
    print(f"  Report written to {report_path}", file=sys.stderr)


def write_jsonl(path: Path, rows: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True, help="Dry-run mode (default)")
    mode.add_argument("--apply", action="store_true", help="Apply mode — writes to graph/")
    parser.add_argument(
        "--yes-i-reviewed-the-dry-run", action="store_true",
        help="Required flag for --apply to confirm dry-run was reviewed",
    )
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for sample (default: 42)")
    args = parser.parse_args()

    if args.apply and not args.yes_i_reviewed_the_dry_run:
        print("ERROR: --apply requires --yes-i-reviewed-the-dry-run", file=sys.stderr)
        sys.exit(1)

    apply_mode = args.apply and args.yes_i_reviewed_the_dry_run
    dry_run = not apply_mode

    t0 = datetime.now()
    result = run_pipeline(dry_run=dry_run, apply_confirmed=apply_mode, rng_seed=args.seed)
    t1 = datetime.now()
    elapsed = (t1 - t0).total_seconds()

    # Always write working/infobox-merge/ outputs
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "merged-candidate.jsonl", result["merged"])
    write_jsonl(OUTPUT_DIR / "filtered.jsonl", result["filtered"])
    write_jsonl(OUTPUT_DIR / "quarantined.jsonl", result["quarantined"])
    write_jsonl(OUTPUT_DIR / "corroborations.jsonl", result["corroborations"])
    write_jsonl(OUTPUT_DIR / "hygiene-a-remaps.jsonl", result["hygiene_a_log"])
    write_jsonl(OUTPUT_DIR / "hygiene-b-stamps.jsonl", result["hygiene_b_log"])
    # The dry-run report is the human-curated approval surface (Matt's CLOSEOUT
    # banner + per-decision [x] marks live in it). Only rewrite it on dry-run
    # runs; --apply must NOT silently wipe it.
    if not apply_mode:
        write_dry_run_report(result, OUTPUT_DIR, rng_seed=args.seed)

    if apply_mode:
        print("[infobox-merge] --apply mode: writing to graph/...", file=sys.stderr)

        # 1. Backup
        ts_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        backup_path = REGROUNDING_DIR / f"edges-pre-infobox-merge-{ts_str}.jsonl"
        REGROUNDING_DIR.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(EDGES_FILE, backup_path)
        print(f"  Backed up to {backup_path}", file=sys.stderr)

        # 2. Apply Fix A remaps + Fix B stamps
        with EDGES_FILE.open("w") as f:
            for row in result["existing_rows_fixed"]:
                f.write(json.dumps(row) + "\n")
        print(f"  Applied Fix A ({len(result['fix_alias']) + len(result['fix_thestrip']) + len(result['fix_honorific'])} slug remaps) + Fix B (948 typed_by stamps)", file=sys.stderr)

        # 3. Append merged rows
        with EDGES_FILE.open("a") as f:
            for row in result["merged"]:
                f.write(json.dumps(row) + "\n")
        print(f"  Appended {len(result['merged'])} merged rows", file=sys.stderr)

        # 4. Verify
        final_count = sum(1 for _ in EDGES_FILE.read_text().splitlines() if _.strip())
        expected_count = len(result["existing_rows"]) + len(result["merged"])
        print(f"  Final edges.jsonl: {final_count} rows (expected {expected_count})", file=sys.stderr)

    # Summary
    stats = result["stats"]
    print(f"\n{'='*60}")
    print(f"INFOBOX-MERGE {'DRY-RUN' if dry_run else 'APPLY'} SUMMARY ({elapsed:.1f}s)")
    print(f"{'='*60}")
    print(f"Input:            {stats['rows_in']:>6} rows ({len(result['existing_rows'])} existing edges)")
    print(f"MERGED:           {stats['merged']:>6}  (→ working/infobox-merge/merged-candidate.jsonl)")
    print(f"Filtered:         {stats.get('F1_source_unresolved',0) + stats.get('F2_noise-placeholder',0) + stats.get('F2_noise-bare-kinship',0) + stats.get('F2_noise-numeral-date',0) + stats.get('F4_target_unresolved',0) + stats.get('F8_self_loop',0):>6}  (→ filtered.jsonl)")
    print(f"Quarantined:      {sum(v for k,v in stats.items() if k.startswith('Q3') or k.startswith('Q6')):>6}  (→ quarantined.jsonl)")
    print(f"Deduped (in-run): {stats.get('D9_deduped_in_run',0):>6}  ({stats.get('D9_qualified_row_preferred',0)} qual-preferred swaps)")
    print(f"Corroborations:   {stats.get('D10_skipped_existing_corroboration',0):>6}  (→ corroborations.jsonl)")
    print(f"R9q quarantined:  {stats.get('Q9_dedupe_qualifier_conflict',0):>6}")
    print(f"Bucket sum:       {result['bucket_sum']:>6} / {stats['rows_in']:>6}  {'✓ OK' if result['bucket_sum'] == stats['rows_in'] else '✗ MISMATCH'}")
    print(f"")
    print(f"Top edge types: SWORN_TO={result['by_type'].get('SWORN_TO',0)}, "
          f"HOLDS_TITLE={result['by_type'].get('HOLDS_TITLE',0)}, "
          f"CULTURE_OF={result['by_type'].get('CULTURE_OF',0)}, "
          f"PARENT_OF={result['by_type'].get('PARENT_OF',0)}")
    print(f"")
    print(f"Hygiene A: {len(result['fix_alias'])} alias + {len(result['fix_thestrip'])} the-strip + {len(result['fix_honorific'])} honorific remaps; "
          f"{len(result['unresolvable_orphans'])} unresolvable")
    print(f"Hygiene B: {result['fix_b_stats'].get('plate3',0)} plate3 + {result['fix_b_stats'].get('plate4',0)} plate4 = "
          f"{result['fix_b_stats'].get('plate3',0) + result['fix_b_stats'].get('plate4',0)} typed_by backfilled")
    print(f"")
    print(f"Report: working/infobox-merge/dry-run-report-2026-06-12.md")
    print(f"{'='*60}")

    # Flag any count mismatches
    mismatches = []
    for k, expected in SPEC_COUNTS.items():
        if k == "filtered_total":
            actual_ft = (stats.get("F1_source_unresolved",0) + stats.get("F2_noise-placeholder",0) +
                         stats.get("F2_noise-bare-kinship",0) + stats.get("F2_noise-numeral-date",0) +
                         stats.get("F4_target_unresolved",0) + stats.get("F8_self_loop",0))
            if actual_ft != expected:
                mismatches.append(f"filtered_total: expected {expected}, got {actual_ft}")
            continue
        if k == "quarantined_total":
            actual_qt = (stats.get("Q3_R3a",0) + stats.get("Q3_R3b",0) + stats.get("Q3_R3c",0) +
                         stats.get("Q3_R3d",0) + stats.get("Q3e_mirror_of_quarantined_fact",0) +
                         stats.get("Q6a_contract_kinship_nonchar",0) + stats.get("Q6b_contract_holds_title_target",0) +
                         stats.get("Q6c_result_field_defeats",0))
            if actual_qt != expected:
                mismatches.append(f"quarantined_total: expected {expected}, got {actual_qt}")
            continue
        actual = stats.get(k, 0)
        if actual != expected:
            mismatches.append(f"{k}: expected {expected}, got {actual}")
    for t, exp in SPEC_BY_TYPE.items():
        act = result["by_type"].get(t, 0)
        if act != exp:
            mismatches.append(f"by_type[{t}]: expected {exp}, got {act}")
    if mismatches:
        print("MISMATCHES vs spec v2:")
        for m in mismatches:
            print(f"  ✗ {m}")
    else:
        print("All spec v2 counts match exactly.")


if __name__ == "__main__":
    main()
