#!/usr/bin/env python3
"""Triage all 17,657 cached AWOIAF wiki pages into per-bucket manifests for Pass 2.

Two stages:

  Stage 1 — page-level triage (triage-bucket-assignments.jsonl)
  Stage 2 — bucket-level grouping + manifest emission

Reads from:
  working/wiki/data/infobox-data.jsonl   — 5,279 pages with infobox signals
  working/wiki/data/page-index.jsonl     — 17,657 pages (all)
  sources/wiki/houses/<slug>.md            — 633 pre-classified house pages
  sources/wiki/_uncategorized/<slug>.md    — 16,943 pages with derived frontmatter

Writes to:
  working/wiki/pass2-staging/triage-bucket-assignments.jsonl  — page-level row (17,657 rows)
  working/wiki/pass2-staging/triage-manifest.jsonl  — bucket membership (canonical)
  working/wiki/pass2-staging/draft-buckets.jsonl    — bucket summary (review view)

With --accept (Stage 3), additionally writes:
  working/wiki/pass2-buckets/<bucket>/manifest.json  — per-bucket lifecycle manifest

Bucket inference rules (v1, deterministic):
  - character.human + allegiance to House X  -> characters-<house-slug>
  - organization.house OR page starts 'House '  -> houses-<region-slug> or houses-other
  - place.location + region known  -> <region-slug>-locations
  - event.battle  -> battles
  - title  -> titles
  - (disambiguation) in page name  -> disambiguation
  - unknown + no signals  -> singletons-unknown
  - has_tv_only_marker AND no cite_refs  -> tv-only-skip
  - Direwolf override (Ghost, Lady, etc.)  -> direwolves

Bucket-size rules (v1, runbook §1.3):
  - Buckets >30 members are split alphabetically into chunks of <=30 each.
  - Pages with byte_size >600KB are flagged oversized and isolated as bucket-of-one
    with chunk_strategy:section-by-section.

Tier defaults (v1, runbook §1.4): bucket_id regex -> tier-1..tier-4.

Tripwire: if < 80% pages have populated signals, non-empty buckets, or
non-singleton primary_bucket, exits with code 2.

Usage:
  python3 scripts/wiki-pass2-triage.py
  python3 scripts/wiki-pass2-triage.py --accept
  python3 scripts/wiki-pass2-triage.py --limit 100 -v
  python3 scripts/wiki-pass2-triage.py --page Eddard_Stark
  python3 scripts/wiki-pass2-triage.py --tripwire-threshold 0.8
"""

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
INFOBOX_DATA_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "infobox-data.jsonl"
PAGE_INDEX_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "page-index.jsonl"
HOUSES_DIR = PROJECT_ROOT / "sources" / "wiki" / "houses"
UNCATEGORIZED_DIR = PROJECT_ROOT / "sources" / "wiki" / "_uncategorized"
OUTPUT_FILE = PROJECT_ROOT / "working" / "wiki" / "pass2-staging" / "triage-bucket-assignments.jsonl"
TRIAGE_MANIFEST_FILE = PROJECT_ROOT / "working" / "wiki" / "pass2-staging" / "triage-manifest.jsonl"
DRAFT_BUCKETS_FILE = PROJECT_ROOT / "working" / "wiki" / "pass2-staging" / "draft-buckets.jsonl"
WIKI_PASS2_DIR = PROJECT_ROOT / "working" / "wiki" / "pass2-buckets"

# Bucket-size policy (runbook §1.3)
BUCKET_SPLIT_THRESHOLD = 30          # split buckets larger than this alphabetically
OVERSIZED_PAGE_BYTES = 600_000       # ~150k tokens — bucket-of-one threshold

# Pass 2 prompt version (runbook §5.2)
PROMPT_VERSION = "v1"

# Tier-default classification (runbook §1.4) — first match wins
TIER_DEFAULT_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"theory|speculation|fan", re.I),                    "tier-4"),
    (re.compile(r"religion|magic|prophecy", re.I),                   "tier-2"),
    (re.compile(r"battle|character|house|location|castle|"
                r"region|city|kingdom|cadet|bastard|order|"
                r"quote|song|saying", re.I),                         "tier-1"),
]
TIER_DEFAULT_FALLBACK = "tier-2"

# Core vs. secondary tier assignment — drives wave order. Patterns match
# both un-split buckets (`characters-house-stark`) and alphabetical splits
# (`characters-house-stark-a-l`).
_SPLIT_SUFFIX = r"(-[a-z]([0-9]+)?(-[a-z]([0-9]+)?)?)?$"
CORE_TIER_RULES: list[re.Pattern] = [
    re.compile(r"^direwolves" + _SPLIT_SUFFIX),
    re.compile(r"^characters-house-(stark|lannister|targaryen|baratheon|"
               r"greyjoy|tully|arryn|tyrell|martell)" + _SPLIT_SUFFIX),
    re.compile(r"^houses-(north|westerlands|crownlands|riverlands|vale|"
               r"reach|stormlands|dorne|iron-islands)" + _SPLIT_SUFFIX),
    re.compile(r"^(north|westerlands|crownlands|riverlands|vale|reach|"
               r"stormlands|dorne|iron-islands)-locations" + _SPLIT_SUFFIX),
]

# Buckets to skip entirely (not eligible for Pass 2 ingestion)
SKIP_BUCKETS = {"singletons-unknown", "tv-only-skip", "disambiguation"}

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# The six canonical Stark direwolves — smoke-test seam.
# Bare names are the reader-facing names. Wiki page names sometimes need a
# disambiguator suffix because the bare name collides with another entity:
# the page "Nymeria" is the historical Rhoynar queen; the direwolf lives at
# "Nymeria (direwolf)". Override map carries known collisions so the
# direwolves bucket gets the right pages.
DIREWOLF_BARE_NAMES = {"Ghost", "Lady", "Nymeria", "Summer", "Shaggydog", "Grey Wind"}
DIREWOLF_PAGE_OVERRIDES = {
    "Nymeria": "Nymeria (direwolf)",
}
DIREWOLF_PAGE_NAMES = {
    DIREWOLF_PAGE_OVERRIDES.get(n, n) for n in DIREWOLF_BARE_NAMES
}

# Book name normalization for the Books infobox-like field in markdown
BOOK_NAME_NORM = {
    "a game of thrones": "AGOT",
    "a clash of kings": "ACOK",
    "a storm of swords": "ASOS",
    "a feast for crows": "AFFC",
    "a dance with dragons": "ADWD",
}

# Book appearance pattern for parsing markdown Books: field
# "A Game of Thrones (POV)A Clash of Kings (mentioned)..."
BOOKS_APPEARANCE_RE = re.compile(
    r'(A Game of Thrones|A Clash of Kings|A Storm of Swords|'
    r'A Feast for Crows|A Dance with Dragons)\s*\(([^)]+)\)',
    re.IGNORECASE,
)

# Region-to-slug normalization table
# Handles raw text values from ** Region: ** lines in markdown
REGION_SLUG_MAP = {
    "north": "north",
    "the north": "north",
    "westerlands": "westerlands",
    "stormlands": "stormlands",
    "the stormlands": "stormlands",
    "riverlands": "riverlands",
    "the riverlands": "riverlands",
    "crownlands": "crownlands",
    "reach": "reach",
    "the reach": "reach",
    "vale of arryn": "vale",
    "the vale of arryn": "vale",
    "vale": "vale",
    "iron islands": "iron-islands",
    "dorne": "dorne",
    "beyond the wall": "beyond-the-wall",
    "essos": "essos",
    "free cities": "free-cities",
    "braavos": "braavos",
    "pentos": "essos",
    "meereen": "essos",
    "qarth": "essos",
    "oldtown": "reach",
    "seven kingdoms": "seven-kingdoms",
    "westeros": "westeros",
    "lannisport": "westerlands",
}


# ---------------------------------------------------------------------------
# Slug generation (matches wiki-infobox-parser.py conventions)
# ---------------------------------------------------------------------------

def page_to_slug(page_name: str) -> str:
    """Convert a page name to a file-system slug.

    Matches the convention used by the original scraper (now archived):
    - Lowercase
    - Strip punctuation that doesn't separate words (apostrophes, quotes, commas)
    - Replace spaces/underscores with hyphens
    - Replace remaining non-alphanumeric chars with hyphens
    - Collapse consecutive hyphens
    """
    slug = page_name.lower()
    # Strip punctuation that merges rather than separates words
    slug = re.sub(r"['\",]", "", slug)
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def house_name_to_slug(house_name: str) -> str:
    """Convert 'House Stark' -> 'house-stark', 'House Frey' -> 'house-frey'."""
    return page_to_slug(house_name)


def region_to_slug(region_text: str) -> str | None:
    """Normalize raw region text to a slug. Returns None if unrecognized."""
    if not region_text:
        return None
    # Take the first segment before commas or conjunctions
    first = re.split(r"[,\n]", region_text)[0].strip()
    # Strip qualifiers like "(formerly)"
    first = re.sub(r"\s*\(.*?\)", "", first).strip()
    key = first.lower()
    return REGION_SLUG_MAP.get(key)


# ---------------------------------------------------------------------------
# Markdown infobox parsing (for _uncategorized and houses files)
# ---------------------------------------------------------------------------

def parse_markdown_infobox(content: str) -> dict:
    """Extract signals from a _uncategorized or houses markdown file.

    Looks for lines in the '## Infobox Data' section of the form:
      **Label:** value
    Returns a dict with normalized keys.
    """
    signals = {}
    # Find the Infobox Data section
    infobox_m = re.search(
        r"## Infobox Data\n(.*?)(?=\n## |\Z)", content, re.DOTALL
    )
    if not infobox_m:
        return signals

    infobox_text = infobox_m.group(1)

    # Parse **Label:** value lines
    field_re = re.compile(r"^\*\*([^*:]+):\*\*\s*(.*)$", re.MULTILINE)
    for m in field_re.finditer(infobox_text):
        label = m.group(1).strip().lower()
        value = m.group(2).strip()
        if value:
            signals[label] = value

    return signals


def parse_frontmatter(content: str) -> dict:
    """Extract YAML-ish frontmatter from a markdown file (naive line parser)."""
    fm = {}
    fm_m = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
    if not fm_m:
        return fm
    for line in fm_m.group(1).split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val:
                fm[key] = val
    # Parse aliases list: aliases: [Ned The quiet wolf  The Ned]
    aliases_m = re.search(r"^aliases:\s*\[([^\]]*)\]", fm_m.group(1), re.MULTILINE)
    if aliases_m:
        raw = aliases_m.group(1).strip()
        # Split on two or more spaces (the format joins aliases with double-space)
        parts = [p.strip() for p in re.split(r"\s{2,}", raw) if p.strip()]
        fm["aliases_list"] = parts
    return fm


def parse_books_field(books_text: str) -> list[str]:
    """Parse 'A Game of Thrones (POV)A Clash of Kings (mentioned)...' into list of 'AGOT-POV' etc."""
    results = []
    for m in BOOKS_APPEARANCE_RE.finditer(books_text):
        book_name = m.group(1).strip()
        appearance = m.group(2).strip()
        book_abbrev = BOOK_NAME_NORM.get(book_name.lower())
        if book_abbrev:
            results.append(f"{book_abbrev}-{appearance}")
    return results


def has_tv_only_marker(infobox_signals: dict, books_appearances: list[str]) -> bool:
    """Return True if 'played by' exists in infobox signals (TV casting marker)."""
    return "played by" in infobox_signals


# ---------------------------------------------------------------------------
# Load infobox-data.jsonl into a page-keyed dict
# ---------------------------------------------------------------------------

def load_infobox_data(limit_pages: set | None = None) -> dict:
    """Return {page_name: infobox_record} from infobox-data.jsonl."""
    data = {}
    with open(INFOBOX_DATA_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            page = rec["page"]
            if limit_pages is not None and page not in limit_pages:
                continue
            data[page] = rec
    return data


# ---------------------------------------------------------------------------
# Load per-page disk signals from _uncategorized and houses markdown files
# ---------------------------------------------------------------------------

def load_disk_signals(page_name: str) -> dict:
    """Load signals from the on-disk markdown file for a page.

    Returns dict with keys: infobox_signals, aliases, books_appearances,
    has_tv_only, region, allegiance, culture, titles, on_disk_dir.
    """
    result = {
        "on_disk_dir": None,
        "infobox_signals": {},
        "aliases": [],
        "books_appearances": [],
        "has_tv_only": False,
        "region": [],
        "allegiance": [],
        "culture": [],
        "titles": [],
    }

    slug = page_to_slug(page_name)

    # Try _uncategorized first, then houses
    candidate_paths = [
        (UNCATEGORIZED_DIR / f"{slug}.md", "_uncategorized"),
        (HOUSES_DIR / f"{slug}.md", "houses"),
    ]

    content = None
    for path, dir_name in candidate_paths:
        if path.exists():
            try:
                content = path.read_text(encoding="utf-8")
                result["on_disk_dir"] = dir_name
            except OSError:
                pass
            break

    if content is None:
        return result

    fm = parse_frontmatter(content)
    infobox = parse_markdown_infobox(content)
    result["infobox_signals"] = infobox

    # Aliases from frontmatter (parsed list) or infobox
    if "aliases_list" in fm:
        result["aliases"] = fm["aliases_list"]
    elif "aliases" in infobox:
        # Try splitting aliases text on double-space or comma
        raw = infobox["aliases"]
        parts = [p.strip() for p in re.split(r"\s{2,}|,\s*", raw) if p.strip()]
        result["aliases"] = parts

    # Books appearances
    if "books" in infobox:
        result["books_appearances"] = parse_books_field(infobox["books"])

    # TV-only marker
    result["has_tv_only"] = has_tv_only_marker(infobox, result["books_appearances"])

    # Region (may be in 'region' or 'regions')
    for key in ("region", "regions"):
        if key in infobox:
            result["region"] = [infobox[key].strip()]
            break

    # Allegiance (may be 'allegiance' or 'allegiances')
    for key in ("allegiance", "allegiances"):
        if key in infobox:
            result["allegiance"] = [infobox[key].strip()]
            break

    # Culture
    if "culture" in infobox:
        result["culture"] = [infobox["culture"].strip()]

    # Titles
    for key in ("titles", "title"):
        if key in infobox:
            result["titles"] = [infobox[key].strip()]
            break

    return result


# ---------------------------------------------------------------------------
# Bucket inference
# ---------------------------------------------------------------------------

def infer_buckets(
    page_name: str,
    entity_type: str,
    allegiances: list[str],
    regions: list[str],
    aliases: list[str],
    has_tv_only: bool,
    books_appearances: list[str],
    cite_ref_total: int,
    on_disk_dir: str | None,
) -> tuple[list[str], str, str]:
    """Return (inferred_buckets, primary_bucket, bucket_reason).

    Priority order (highest first):
      1. Disambig suffix
      2. Direwolf override
      3. TV-only with no cite_refs
      4. entity_type-based rules
      5. Page name pattern rules
      6. Fallback
    """
    page_lower = page_name.lower()

    # --- Rule 1: Disambiguation pages ---
    if "(disambiguation)" in page_lower:
        return (
            ["disambiguation"],
            "disambiguation",
            "page name contains (disambiguation)",
        )

    # --- Rule 2: Direwolf override (smoke-test seam) ---
    # Page-name match against the disambiguated direwolf page set.
    # Bare-name collisions (e.g., "Nymeria" the Rhoynar queen vs. the direwolf
    # at "Nymeria (direwolf)") are handled via DIREWOLF_PAGE_OVERRIDES so the
    # bucket only gets the actual direwolf pages.
    if page_name in DIREWOLF_PAGE_NAMES:
        return (
            ["direwolves"],
            "direwolves",
            "direwolf override: page name matches direwolf set",
        )

    # --- Rule 3: TV-only (no cite_refs and has played-by marker) ---
    if has_tv_only and cite_ref_total == 0:
        return (
            ["tv-only-skip"],
            "tv-only-skip",
            "has_tv_only_marker=True and cite_ref_total=0",
        )

    # --- Rule 4: Entity-type-based rules ---
    buckets = []
    reason_parts = []

    if entity_type == "character.human":
        # Find allegiance to a House
        house_allegiances = [
            a for a in allegiances
            if re.match(r"house\s+", a, re.IGNORECASE)
        ]
        if house_allegiances:
            for house in house_allegiances:
                # Extract just "House X" (strip trailing qualifiers like "(AGOT)")
                house_clean = re.sub(r"\s*\(.*?\)", "", house).strip()
                house_slug = house_name_to_slug(house_clean)
                buckets.append(f"characters-{house_slug}")
            reason_parts.append(
                f"allegiance:{house_allegiances[0]} + entity_type:character.human"
            )
        else:
            # Character with no house allegiance — try region or faction
            if regions:
                region_slug = region_to_slug(regions[0])
                if region_slug:
                    buckets.append(f"characters-{region_slug}")
                    reason_parts.append(
                        f"entity_type:character.human + region:{regions[0]}"
                    )
            if not buckets:
                buckets.append("characters-other")
                reason_parts.append("entity_type:character.human, no house allegiance")

    elif entity_type == "organization.house" or page_name.startswith("House "):
        # House — bucket by region if known
        if regions:
            region_slug = region_to_slug(regions[0])
            if region_slug:
                buckets.append(f"houses-{region_slug}")
                reason_parts.append(
                    f"entity_type:organization.house + region:{regions[0]}"
                )
        if not buckets:
            # Houses pre-classified dir is a direct signal too
            if on_disk_dir == "houses":
                buckets.append("houses-other")
                reason_parts.append("on_disk_dir:houses, region unknown")
            else:
                buckets.append("houses-other")
                reason_parts.append(
                    f"entity_type:organization.house or House prefix, region unknown"
                )

    elif entity_type == "place.location":
        if regions:
            region_slug = region_to_slug(regions[0])
            if region_slug:
                buckets.append(f"{region_slug}-locations")
                reason_parts.append(
                    f"entity_type:place.location + region:{regions[0]}"
                )
        if not buckets:
            buckets.append("locations-other")
            reason_parts.append("entity_type:place.location, region unknown")

    elif entity_type == "event.battle":
        buckets.append("battles")
        reason_parts.append("entity_type:event.battle")

    elif entity_type == "title":
        buckets.append("titles")
        reason_parts.append("entity_type:title")

    # --- Rule 5: Page name patterns (supplement or fallback) ---
    if not buckets:
        if re.match(r"^battle\s+of\s+", page_lower) or re.match(
            r"^siege\s+of\s+", page_lower
        ):
            buckets.append("battles")
            reason_parts.append("page_pattern:battle/siege prefix")

        elif page_name.startswith("House "):
            buckets.append("houses-other")
            reason_parts.append("page_pattern:House prefix")

        elif re.search(r"\(disambiguation\)", page_lower):
            buckets.append("disambiguation")
            reason_parts.append("page_pattern:disambiguation suffix")

    # --- Rule 6: Fallback ---
    if not buckets:
        buckets.append("singletons-unknown")
        reason_parts.append("no signals matched")

    # Primary bucket: first (most specific) wins
    primary = buckets[0]
    reason = "; ".join(reason_parts) if reason_parts else "no signals"

    return buckets, primary, reason


# ---------------------------------------------------------------------------
# Signal richness check (for tripwire)
# ---------------------------------------------------------------------------

def signals_are_populated(signals: dict) -> bool:
    """Return True if at least one meaningful signal is non-empty.

    The spec excludes 'has_infobox' and 'byte_size' as trivially present.
    We count the following as real signals:
      - entity_type != "unknown"          (infobox classification produced a type)
      - allegiance, culture, region, titles, aliases  non-empty list
      - page_pattern not None             (House prefix, battle prefix, etc.)
      - books_appearance non-empty        (entity appears in books)
      - cite_ref_total > 0                (wiki page cites at least one book chapter)
    """
    # entity_type being something other than unknown is itself a signal
    if signals.get("entity_type", "unknown") not in ("unknown", ""):
        return True
    # Non-empty list fields
    for key in ("allegiance", "culture", "region", "titles", "aliases", "books_appearance"):
        val = signals.get(key, [])
        if isinstance(val, list) and len(val) > 0:
            return True
    # page_pattern (House prefix, battle prefix, disambiguation)
    if signals.get("page_pattern") is not None:
        return True
    # cite_ref_total > 0 means the wiki cites specific book chapters about this entity
    if signals.get("cite_ref_total", 0) > 0:
        return True
    return False


# ---------------------------------------------------------------------------
# Process a single page
# ---------------------------------------------------------------------------

def process_page(
    page_name: str,
    index_rec: dict,
    infobox_rec: dict | None,
    verbose: bool = False,
) -> dict:
    """Build a page-categories row for one page."""
    # --- Entity type: prefer infobox-data over page-index (more precise) ---
    entity_type = (
        infobox_rec["entity_type"]
        if infobox_rec
        else index_rec.get("entity_type_guess", "unknown")
    )

    # --- Cite ref total ---
    cite_ref_books = index_rec.get("cite_ref_books", {})
    cite_ref_total = sum(cite_ref_books.values())

    # --- Disk signals ---
    disk = load_disk_signals(page_name)
    on_disk_dir = disk["on_disk_dir"]

    # --- Aliases: merge infobox-data (cleanest) + disk ---
    if infobox_rec and infobox_rec.get("aliases"):
        aliases = infobox_rec["aliases"]
    else:
        aliases = disk["aliases"]

    # --- Allegiance: from infobox relationships (cleanest) then disk ---
    allegiances = []
    if infobox_rec:
        for rel in infobox_rec.get("relationships", []):
            if rel.get("field", "").lower() in ("allegiance", "allegiances"):
                allegiances.append(rel["target"])
    if not allegiances and disk["allegiance"]:
        allegiances = disk["allegiance"]

    # --- Culture ---
    cultures = []
    if infobox_rec:
        for rel in infobox_rec.get("relationships", []):
            if rel.get("field", "").lower() == "culture":
                cultures.append(rel["target"])
    if not cultures and disk["culture"]:
        cultures = disk["culture"]

    # --- Region ---
    regions = []
    if infobox_rec:
        for rel in infobox_rec.get("relationships", []):
            if rel.get("field", "").lower() in ("region", "regions"):
                regions.append(rel["target"])
    if not regions and disk["region"]:
        regions = disk["region"]

    # --- Titles ---
    titles = []
    if infobox_rec:
        for rel in infobox_rec.get("relationships", []):
            if rel.get("field", "").lower() in ("titles", "title"):
                titles.append(rel["target"])
    if not titles and disk["titles"]:
        titles = disk["titles"]

    # --- Books appearances ---
    books_appearances: list[str] = []
    if infobox_rec and infobox_rec.get("books"):
        for entry in infobox_rec["books"]:
            books_appearances.append(f"{entry['book']}-{entry['appearance']}")
    if not books_appearances:
        books_appearances = disk["books_appearances"]

    # --- TV-only marker ---
    has_tv_only = disk["has_tv_only"]

    # --- Page pattern ---
    page_lower = page_name.lower()
    page_pattern = None
    if "(disambiguation)" in page_lower:
        page_pattern = "disambiguation"
    elif re.match(r"^battle\s+of\s+", page_lower) or re.match(
        r"^siege\s+of\s+", page_lower
    ):
        page_pattern = "battle-prefix"
    elif page_name.startswith("House "):
        page_pattern = "house-prefix"

    # --- Infer buckets ---
    inferred_buckets, primary_bucket, bucket_reason = infer_buckets(
        page_name=page_name,
        entity_type=entity_type,
        allegiances=allegiances,
        regions=regions,
        aliases=aliases,
        has_tv_only=has_tv_only,
        books_appearances=books_appearances,
        cite_ref_total=cite_ref_total,
        on_disk_dir=on_disk_dir,
    )

    # --- Build signals dict ---
    signals = {
        "entity_type": entity_type,
        "allegiance": allegiances,
        "culture": cultures,
        "region": regions,
        "titles": titles,
        "page_pattern": page_pattern,
        "has_tv_only_marker": has_tv_only,
        "books_appearance": books_appearances,
        "has_infobox": index_rec.get("has_infobox", False),
        "byte_size": index_rec.get("byte_size", 0),
        "cite_ref_total": cite_ref_total,
        "aliases": aliases,
    }

    # --- Build result row ---
    slug = page_to_slug(page_name)
    row = {
        "page": page_name,
        "slug": slug,
        "on_disk_dir": on_disk_dir,
        "signals": signals,
        "inferred_buckets": inferred_buckets,
        "primary_bucket": primary_bucket,
        "bucket_reason": bucket_reason,
    }

    # Disambiguation chunk strategy flag
    if primary_bucket == "disambiguation":
        row["chunk_strategy"] = "per-candidate"

    if verbose:
        print(
            f"  page={page_name!r:50s} entity_type={entity_type!r:25s} "
            f"bucket={primary_bucket!r}"
        )

    return row


# ---------------------------------------------------------------------------
# Tripwire check
# ---------------------------------------------------------------------------

def run_tripwire(rows: list[dict], threshold: float, verbose: bool = False) -> bool:
    """Check tripwire conditions. Returns True if all pass, False (exit 2) otherwise."""
    total = len(rows)
    if total == 0:
        print("TRIPWIRE: no rows to check", file=sys.stderr)
        return False

    # Metric 1: % with at least one populated signal (excl. has_infobox, byte_size)
    with_signals = sum(1 for r in rows if signals_are_populated(r["signals"]))
    pct_signals = with_signals / total

    # Metric 2: % with non-empty inferred_buckets
    with_buckets = sum(1 for r in rows if r["inferred_buckets"])
    pct_buckets = with_buckets / total

    # Metric 3: % with primary_bucket != "singletons-unknown"
    with_classified = sum(
        1 for r in rows if r["primary_bucket"] != "singletons-unknown"
    )
    pct_classified = with_classified / total

    print()
    print("=== TRIPWIRE METRICS ===")
    print(
        f"  Pages with >= 1 populated signal:          "
        f"{pct_signals*100:.1f}%  ({with_signals}/{total})"
    )
    print(
        f"  Pages with non-empty inferred_buckets:     "
        f"{pct_buckets*100:.1f}%  ({with_buckets}/{total})"
    )
    print(
        f"  Pages with primary_bucket != singletons:   "
        f"{pct_classified*100:.1f}%  ({with_classified}/{total})"
    )
    print(f"  Threshold: {threshold*100:.0f}%")

    failed = []
    for label, pct in [
        ("signals populated", pct_signals),
        ("non-empty buckets", pct_buckets),
        ("classified (non-singleton)", pct_classified),
    ]:
        if pct < threshold:
            failed.append((label, pct))

    if failed:
        print()
        print("TRIPWIRE FAILED — thresholds not met:", file=sys.stderr)
        for label, pct in failed:
            print(f"  {label}: {pct*100:.1f}% < {threshold*100:.0f}%", file=sys.stderr)
        print()
        print("Sample rows where signals are empty (up to 10):", file=sys.stderr)
        empty_samples = [
            r for r in rows if not signals_are_populated(r["signals"])
        ][:10]
        for r in empty_samples:
            print(
                f"  page={r['page']!r:50s}  on_disk_dir={r['on_disk_dir']!r}  "
                f"entity_type={r['signals']['entity_type']!r}",
                file=sys.stderr,
            )
        return False

    print("  TRIPWIRE PASSED")
    return True


# ---------------------------------------------------------------------------
# Bucket grouping (Stage 2)
# ---------------------------------------------------------------------------

def classify_tier_default(bucket_id: str) -> str:
    """Map bucket_id -> tier-1..tier-4 via runbook §1.4 regex table."""
    for pat, tier in TIER_DEFAULT_RULES:
        if pat.search(bucket_id):
            return tier
    return TIER_DEFAULT_FALLBACK


def classify_processing_tier(bucket_id: str) -> str:
    """Map bucket_id -> 'core' or 'secondary' for wave priority."""
    for pat in CORE_TIER_RULES:
        if pat.match(bucket_id):
            return "core"
    return "secondary"


def split_oversized_bucket(
    bucket_id: str, page_rows: list[dict]
) -> list[tuple[str, list[dict]]]:
    """Split a bucket of >BUCKET_SPLIT_THRESHOLD pages into alphabetical chunks.

    Returns list of (sub_bucket_id, sub_rows). Single-page oversized bytes
    (>OVERSIZED_PAGE_BYTES) are isolated as bucket-of-one regardless of count.
    """
    # First isolate any oversized-byte pages as bucket-of-one
    oversized_byte_rows = [
        r for r in page_rows
        if r["signals"].get("byte_size", 0) > OVERSIZED_PAGE_BYTES
    ]
    normal_rows = [
        r for r in page_rows
        if r["signals"].get("byte_size", 0) <= OVERSIZED_PAGE_BYTES
    ]

    result: list[tuple[str, list[dict]]] = []
    for r in oversized_byte_rows:
        result.append((f"{bucket_id}-{r['slug']}", [r]))

    if len(normal_rows) <= BUCKET_SPLIT_THRESHOLD:
        if normal_rows:
            result.append((bucket_id, normal_rows))
        return result

    # Alphabetical chunks of <= threshold
    sorted_rows = sorted(normal_rows, key=lambda r: r["page"].lower())
    chunk_count = (len(sorted_rows) + BUCKET_SPLIT_THRESHOLD - 1) // BUCKET_SPLIT_THRESHOLD
    chunk_size = (len(sorted_rows) + chunk_count - 1) // chunk_count

    def chunk_letters(rows_chunk: list[dict]) -> str:
        first = rows_chunk[0]["page"][0].lower()
        last = rows_chunk[-1]["page"][0].lower()
        return f"{first}-{last}" if first != last else first

    for i in range(0, len(sorted_rows), chunk_size):
        chunk_rows = sorted_rows[i:i + chunk_size]
        suffix = chunk_letters(chunk_rows)
        result.append((f"{bucket_id}-{suffix}", chunk_rows))

    return result


def build_buckets(rows: list[dict]) -> list[dict]:
    """Group page rows into buckets, splitting oversized ones.

    Returns list of bucket dicts:
      {bucket_id, processing_tier, tier_default, source_categories, pages,
       page_count, total_bytes, oversized, chunk_strategy, skip}
    """
    grouped: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        grouped[r["primary_bucket"]].append(r)

    buckets: list[dict] = []
    for bucket_id, page_rows in grouped.items():
        skip = bucket_id in SKIP_BUCKETS
        for sub_id, sub_rows in split_oversized_bucket(bucket_id, page_rows):
            total_bytes = sum(r["signals"].get("byte_size", 0) for r in sub_rows)
            largest_byte = max(
                (r["signals"].get("byte_size", 0) for r in sub_rows),
                default=0,
            )
            oversized = largest_byte > OVERSIZED_PAGE_BYTES
            chunk_strategy = "section-by-section" if oversized else "single-pass"
            buckets.append({
                "bucket_id": sub_id,
                "processing_tier": classify_processing_tier(sub_id),
                "tier_default": classify_tier_default(sub_id),
                "source_categories": sorted({bucket_id}),
                "pages": [r["page"] for r in sub_rows],
                "page_count": len(sub_rows),
                "total_bytes": total_bytes,
                "oversized": oversized,
                "chunk_strategy": chunk_strategy,
                "skip": skip,
            })

    buckets.sort(key=lambda b: (b["processing_tier"] != "core", b["bucket_id"]))
    return buckets


def write_triage_outputs(buckets: list[dict], rows: list[dict]) -> None:
    """Write triage-manifest.jsonl (membership) and draft-buckets.jsonl (summary)."""
    # triage-manifest.jsonl: one row per page with bucket assignment + reason
    page_to_bucket: dict[str, str] = {}
    for b in buckets:
        for p in b["pages"]:
            page_to_bucket[p] = b["bucket_id"]

    page_reasons = {r["page"]: r["bucket_reason"] for r in rows}

    with open(TRIAGE_MANIFEST_FILE, "w", encoding="utf-8") as f:
        for r in rows:
            page = r["page"]
            sub_bucket = page_to_bucket.get(page, r["primary_bucket"])
            line = {
                "page": page,
                "slug": r["slug"],
                "bucket_id": sub_bucket,
                "bucket_assignment_reason": page_reasons.get(page, ""),
            }
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

    # draft-buckets.jsonl: one row per bucket
    with open(DRAFT_BUCKETS_FILE, "w", encoding="utf-8") as f:
        for b in buckets:
            f.write(json.dumps(b, ensure_ascii=False) + "\n")


def bucket_fingerprint(b: dict) -> str:
    """SHA-256 over (sorted input_pages + prompt_version + chunk_strategy)."""
    payload = {
        "input_pages": sorted(b["pages"]),
        "prompt_version": PROMPT_VERSION,
        "chunk_strategy": b["chunk_strategy"],
    }
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def expected_node_filename(page: str) -> str:
    """Map a wiki page name -> expected node filename (slug + .node.md)."""
    return f"{page_to_slug(page)}.node.md"


def write_bucket_manifests(buckets: list[dict], verbose: bool = False) -> tuple[int, int, int]:
    """Write per-bucket manifest.json. Skip buckets in SKIP_BUCKETS.

    Preserves existing status/started_at/completed_at if a manifest already
    exists at the target path (the launcher owns those fields). Always
    rewrites input_pages, expected_nodes, fingerprint, tier_default,
    chunk_strategy.

    Returns (created, updated, skipped) counts.
    """
    created = updated = skipped = 0

    for b in buckets:
        if b["skip"]:
            skipped += 1
            continue

        bucket_dir = WIKI_PASS2_DIR / b["bucket_id"]
        bucket_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = bucket_dir / "manifest.json"

        existing: dict = {}
        if manifest_path.exists():
            try:
                existing = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                existing = {}

        new_fingerprint = bucket_fingerprint(b)
        existing_fingerprint = existing.get("fingerprint")
        existing_status = existing.get("status", "pending")

        # Fingerprint change on a previously-complete bucket → version-stale.
        # Without this, a triage rule fix (e.g., direwolf disambiguation)
        # rewrites input_pages and fingerprint but the launcher keeps treating
        # the bucket as complete and never re-runs it.
        if (existing_status == "complete"
                and existing_fingerprint
                and existing_fingerprint != new_fingerprint):
            new_status = "version-stale"
        else:
            new_status = existing_status

        manifest = {
            "bucket_id": b["bucket_id"],
            "tier": b["processing_tier"],
            "tier_default": b["tier_default"],
            "fingerprint": new_fingerprint,
            "prompt_version": PROMPT_VERSION,
            "chunk_strategy": b["chunk_strategy"],
            "oversized": b["oversized"],
            "input_pages": sorted(b["pages"]),
            "expected_nodes": sorted(expected_node_filename(p) for p in b["pages"]),
            "status": new_status,
            "started_at": existing.get("started_at"),
            "completed_at": existing.get("completed_at"),
            "validation_report": existing.get("validation_report"),
        }

        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        if existing:
            updated += 1
            if verbose:
                print(f"  updated  {b['bucket_id']:<50s} ({b['page_count']} pages)")
        else:
            created += 1
            if verbose:
                print(f"  created  {b['bucket_id']:<50s} ({b['page_count']} pages)")

    return created, updated, skipped


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Process only the first N pages (smoke test / dev mode)",
    )
    parser.add_argument(
        "--page",
        metavar="PAGE_NAME",
        help=(
            "Process a single page and print full result. "
            "Accepts wiki page name (spaces) or underscore form."
        ),
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Print per-page progress",
    )
    parser.add_argument(
        "--tripwire-threshold",
        type=float,
        default=0.8,
        metavar="FLOAT",
        help="Minimum fraction of pages that must meet each tripwire condition (default: 0.8)",
    )
    parser.add_argument(
        "--accept",
        action="store_true",
        default=False,
        help="Commit per-bucket manifest.json files at working/wiki/pass2-buckets/<bucket>/. "
             "Without --accept, only the draft (page-categories + triage-manifest + "
             "draft-buckets) is regenerated.",
    )
    args = parser.parse_args()

    # --- Single-page debug mode ---
    if args.page:
        # Accept either 'Eddard_Stark' or 'Eddard Stark'
        page_name = args.page.replace("_", " ")

        # Load infobox data for this page
        infobox_data = load_infobox_data(limit_pages={page_name})
        infobox_rec = infobox_data.get(page_name)

        # Find in page-index
        index_rec = None
        with open(PAGE_INDEX_FILE, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                if rec["page"] == page_name:
                    index_rec = rec
                    break

        if index_rec is None:
            # Build minimal fallback
            print(
                f"WARNING: page '{page_name}' not found in page-index.jsonl — "
                "using minimal record",
                file=sys.stderr,
            )
            index_rec = {
                "page": page_name,
                "entity_type_guess": "unknown",
                "cite_ref_books": {},
                "has_infobox": infobox_rec is not None,
                "byte_size": 0,
            }

        row = process_page(page_name, index_rec, infobox_rec, verbose=True)
        print()
        print(json.dumps(row, indent=2, ensure_ascii=False))
        return

    # --- Batch mode ---
    print(f"Loading page-index.jsonl...")
    page_index: list[dict] = []
    with open(PAGE_INDEX_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            page_index.append(json.loads(line))

    if args.limit:
        page_index = page_index[: args.limit]
        print(f"Limited to {args.limit} pages (--limit flag)")

    total = len(page_index)
    print(f"Processing {total:,} pages...")

    # Load infobox data (keyed by page name)
    limit_pages = {rec["page"] for rec in page_index}
    print(f"Loading infobox-data.jsonl for {total:,} pages...")
    infobox_data = load_infobox_data(limit_pages=limit_pages)
    print(f"  Found infobox records for {len(infobox_data):,} pages")

    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for i, index_rec in enumerate(page_index, 1):
            if args.verbose or (i % 2000 == 0):
                print(f"  [{i:>6}/{total}] {i/total*100:.1f}%  {index_rec['page']}")

            page_name = index_rec["page"]
            infobox_rec = infobox_data.get(page_name)

            try:
                row = process_page(
                    page_name, index_rec, infobox_rec, verbose=args.verbose
                )
            except Exception as e:
                print(
                    f"  ERROR processing {page_name!r}: {e}",
                    file=sys.stderr,
                )
                if args.verbose:
                    import traceback
                    traceback.print_exc()
                # Emit minimal row
                row = {
                    "page": page_name,
                    "slug": page_to_slug(page_name),
                    "on_disk_dir": None,
                    "signals": {
                        "entity_type": "unknown",
                        "allegiance": [],
                        "culture": [],
                        "region": [],
                        "titles": [],
                        "page_pattern": None,
                        "has_tv_only_marker": False,
                        "books_appearance": [],
                        "has_infobox": False,
                        "byte_size": 0,
                        "cite_ref_total": 0,
                        "aliases": [],
                    },
                    "inferred_buckets": ["singletons-unknown"],
                    "primary_bucket": "singletons-unknown",
                    "bucket_reason": f"processing error: {e}",
                }

            rows.append(row)
            out.write(json.dumps(row, ensure_ascii=False) + "\n")

    # --- Tripwire ---
    passed = run_tripwire(rows, args.tripwire_threshold, verbose=args.verbose)

    # --- Bucket distribution ---
    bucket_counts = Counter(r["primary_bucket"] for r in rows)
    print()
    print("=== PRIMARY BUCKET DISTRIBUTION (top 30) ===")
    for bucket, count in bucket_counts.most_common(30):
        pct = count / total * 100
        print(f"  {bucket:<50s} {count:>6,}  ({pct:.1f}%)")

    # --- Entity type x bucket summary ---
    et_bucket = Counter(
        (r["signals"]["entity_type"], r["primary_bucket"]) for r in rows
    )
    print()
    print("=== ENTITY TYPE x BUCKET (top 20 cells) ===")
    for (et, bucket), count in et_bucket.most_common(20):
        print(f"  {et:<30s} {bucket:<40s} {count:>5,}")

    # --- Stage 2: bucket grouping + draft outputs ---
    print()
    print("=== STAGE 2: Bucket grouping ===")
    buckets = build_buckets(rows)
    write_triage_outputs(buckets, rows)

    eligible = [b for b in buckets if not b["skip"]]
    skip_buckets = [b for b in buckets if b["skip"]]
    core_buckets = [b for b in eligible if b["processing_tier"] == "core"]
    secondary_buckets = [b for b in eligible if b["processing_tier"] == "secondary"]

    print(f"  Total buckets:        {len(buckets)}")
    print(f"  Eligible (not skip):  {len(eligible)}")
    print(f"    core:               {len(core_buckets)}")
    print(f"    secondary:          {len(secondary_buckets)}")
    print(f"  Skipped (singletons/tv-only/disambig): {len(skip_buckets)}")
    print(f"  Oversized buckets:    {sum(1 for b in eligible if b['oversized'])}")
    print(f"  Output: {TRIAGE_MANIFEST_FILE}")
    print(f"  Output: {DRAFT_BUCKETS_FILE}")

    # --- Stage 3: per-bucket manifests (only with --accept) ---
    if args.accept:
        print()
        print("=== STAGE 3: Writing per-bucket manifests (--accept) ===")
        WIKI_PASS2_DIR.mkdir(parents=True, exist_ok=True)
        created, updated, skipped = write_bucket_manifests(buckets, verbose=args.verbose)
        print(f"  Created: {created}")
        print(f"  Updated: {updated}")
        print(f"  Skipped: {skipped}")
        print(f"  Output dir: {WIKI_PASS2_DIR}")
    else:
        print()
        print("(Draft only — re-run with --accept to commit per-bucket manifests.)")

    # --- Final summary ---
    print()
    print("=" * 60)
    print("Wiki Pass 2 Triage — Complete")
    print("=" * 60)
    print(f"Pages processed:         {total:>8,}")
    print(f"Rows written:            {len(rows):>8,}")
    print(f"Infobox-enriched pages:  {len(infobox_data):>8,}")
    print(f"Distinct primary buckets:{len(bucket_counts):>8,}")
    print(f"Final buckets (post-split): {len(buckets):>5,}")
    print(f"Output: {OUTPUT_FILE}")

    if not passed:
        sys.exit(2)


if __name__ == "__main__":
    main()
