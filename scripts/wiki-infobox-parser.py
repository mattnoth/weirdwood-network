#!/usr/bin/env python3
"""Parse cached AWOIAF wiki JSON files and emit structured data for Pass 2.

Reads every JSON file in sources/wiki/_raw/ and produces three outputs in
working/wiki-parsed/:

  infobox-data.jsonl  — one object per page that has an infobox: entity type,
                        first_available, books, relationships, aliases, cite_refs
  page-index.jsonl    — L1 index: one line per page (ALL pages, not just infobox-
                        rich ones) with entity_type_guess, categories, cite_ref
                        counts, has_infobox, byte_size
  parse-stats.md      — summary: pages parsed, entity-type distribution, top
                        infobox fields, unmapped fields, failure counts

The L1 page-index is the contract between Track B and Pass 2. Every downstream
layer (triage, per-bucket manifests) builds on it without re-parsing 17k HTML.

Usage:
  python scripts/wiki-infobox-parser.py
  python scripts/wiki-infobox-parser.py --limit 50    # smoke test on 50 pages
  python scripts/wiki-infobox-parser.py --limit 50 -v # verbose output
  python scripts/wiki-infobox-parser.py --page Eddard_Stark  # single page debug

Output directories:
  working/wiki-parsed/

Source data:
  sources/wiki/_raw/*.json   — cached wiki pages with {page, html, fetched} keys
  sources/chapters/{book}/   — chapter files used to build chapter→POV mapping

Cite-ref encoding (from wiki HTML anchor IDs):
  cite_(?:ref|note)-R(agot|acok|asos|affc|adwd)(\\d+)
  Ignored: Rawoiaf, Citadel, IMDB, Calculation, and other non-book prefixes.
"""

import argparse
import html.parser
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
RAW_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
CHAPTERS_BASE = PROJECT_ROOT / "sources" / "chapters"
OUTPUT_DIR = PROJECT_ROOT / "working" / "wiki-parsed"

INFOBOX_DATA_FILE = OUTPUT_DIR / "infobox-data.jsonl"
PAGE_INDEX_FILE = OUTPUT_DIR / "page-index.jsonl"
PAGE_CATEGORIES_FILE = OUTPUT_DIR / "page-categories.jsonl"
STATS_FILE = OUTPUT_DIR / "parse-stats.md"

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]
BOOK_TITLES = {
    "A Game of Thrones": "agot",
    "A Clash of Kings": "acok",
    "A Storm of Swords": "asos",
    "A Feast for Crows": "affc",
    "A Dance with Dragons": "adwd",
}

# Cite-ref regex: captures book abbreviation + chapter number
CITE_REF_RE = re.compile(
    r'cite_(?:ref|note)-R(agot|acok|asos|affc|adwd)(\d+)',
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Infobox field → edge type mapping
#
# THIS DICT IS THE EDGE VOCABULARY LOCK FOR THE PROJECT.
#
# Every edge in every Pass 2 node (working/wiki-pass2/*/tmp/*.node.md and
# graph/nodes/**/*.node.md) traces back to a row here. Downstream scripts
# (wiki-pass2-emit-deterministic.py) and downstream agents (wiki-ingester
# in Stage 3b prose-only mode) emit edges as a faithful pass-through of
# this dict's outputs. No script and no agent invents an edge_type that
# isn't produced here.
#
# The mapping mirrors reference/architecture.md § "Wiki Infobox Fields →
# Edge Type Mapping". Updates flow architecture.md FIRST, then this dict.
#
# Currently unmapped fields (deliberately — taxonomy decisions pending):
# dynasty, written by, hatched, fathers (plural), vassal, cadet branch
# (singular). See working/todos.md "Edge taxonomy gaps surfaced by Track B".
#
# Final edge polish — collapsing semantically-equivalent variants — happens
# at a future agent-reasoning phase AFTER all wiki ingestion completes.
# Don't merge edges in this script or in Stage 3a/3b.
# ---------------------------------------------------------------------------
FIELD_EDGE_MAP = {
    # Kinship
    "father":           ("PARENT_OF",  "reverse"),
    "fathers":          ("PARENT_OF",  "reverse"),
    "mother":           ("PARENT_OF",  "reverse"),
    "mothers":          ("PARENT_OF",  "reverse"),
    "spouse":           ("SPOUSE_OF",  "symmetric"),
    "spouses":          ("SPOUSE_OF",  "symmetric"),
    "lover":            ("LOVER_OF",   "symmetric"),
    "lovers":           ("LOVER_OF",   "symmetric"),
    "issue":            ("PARENT_OF",  "forward"),
    "heir":             ("HEIR_TO",    "forward"),
    "heirs":            ("HEIR_TO",    "forward"),
    "cadet branches":   ("CADET_BRANCH_OF", "forward"),
    # Political
    "allegiance":       ("SWORN_TO",   "forward"),
    "allegiances":      ("SWORN_TO",   "forward"),
    "overlord":         ("OVERLORD_OF","reverse"),
    "overlords":        ("OVERLORD_OF","reverse"),
    "head":             ("RULES",      "forward"),
    "ruler":            ("RULES",      "forward"),
    "monarch":          ("SWORN_TO",   "forward"),
    "successor":        ("SUCCEEDS",   "forward"),
    "predecessor":      ("SUCCEEDS",   "reverse"),
    "founder":          ("FOUNDED",    "forward"),
    "title":            ("HOLDS_TITLE","forward"),
    "titles":           ("HOLDS_TITLE","forward"),
    # Spatial
    "seat":             ("SEAT_OF",    "reverse"),
    "seats":            ("SEAT_OF",    "reverse"),
    "region":           ("REGION_OF",  "forward"),
    "regions":          ("REGION_OF",  "forward"),
    "born":             ("BORN_AT",    "forward"),
    "died":             ("DIED_AT",    "forward"),
    "buried":           ("BURIED_AT",  "forward"),
    # Possession
    "ancestral weapon": ("ANCESTRAL_WEAPON_OF", "reverse"),
    "owner":            ("OWNS",       "forward"),
    "owners":           ("OWNS",       "forward"),
    # Cultural
    "culture":          ("CULTURE_OF", "forward"),
    "cultures":         ("CULTURE_OF", "forward"),
    "race":             ("CULTURE_OF", "forward"),
    "religion":         ("WORSHIPS",   "forward"),
    # Identity
    "alias":            ("ALIAS_OF",   "forward"),
    "aliases":          ("ALIAS_OF",   "forward"),
    # Battle
    "conflict":         ("FIGHTS_IN",  "forward"),
    "battles":          ("FIGHTS_IN",  "forward"),
    "result":           ("DEFEATS",    "forward"),
    # In-world texts (books, songs, decrees)
    "written by":       ("WRITTEN_BY", "forward"),
}

# Fields to skip entirely (TV, publication metadata)
SKIP_FIELDS = {
    "played by", "tv series", "episode", "seasons", "first episode", "last episode",
    "author", "publisher", "isbn", "pages", "language", "publication date",
    "media type", "illustrator", "cover artist", "preceded by", "followed by",
    "titles in pretence",
}

# Entity type classification by infobox field signatures
ENTITY_TYPE_SIGNATURES = {
    "character.human": {
        "required": set(),
        "strong": {"father", "mother", "spouse", "spouses", "born", "died",
                   "culture", "allegiance", "allegiances", "issue", "lover", "lovers",
                   "mothers"},
        "weight": 1,
    },
    "organization.house": {
        "required": set(),
        "strong": {"coat of arms", "seat", "head", "cadet branches",
                   "ancestral weapon", "overlord", "overlords", "founder"},
        "weight": 2,
    },
    "place.location": {
        "required": set(),
        "strong": {"location", "government", "ruler", "notable places",
                   "population", "founded", "religion"},
        "weight": 1,
    },
    "event.battle": {
        "required": set(),
        "strong": {"conflict", "date", "place", "result", "strength",
                   "casualties", "commanders"},
        "weight": 2,
    },
    "title": {
        "required": set(),
        "strong": {"office", "current holder", "first holder", "creator",
                   "type", "term length"},
        "weight": 2,
    },
}

# Book name normalization for the Books infobox field
BOOK_NAME_NORM = {
    "a game of thrones": "AGOT",
    "a clash of kings": "ACOK",
    "a storm of swords": "ASOS",
    "a feast for crows": "AFFC",
    "a dance with dragons": "ADWD",
}


# ---------------------------------------------------------------------------
# Build chapter-number → POV label mapping from chapter source files
# ---------------------------------------------------------------------------

def build_chapter_map():
    """Return {book: {chapter_num: pov_label}} from chapter frontmatter files."""
    chapter_map = {}
    fm_re = re.compile(r'---\n(.*?)\n---', re.DOTALL)
    chap_re = re.compile(r'chapter_number:\s*(\d+)')
    pov_re = re.compile(r'pov_label:\s*"?([^"\n]+)"?')

    for book in BOOKS:
        book_dir = CHAPTERS_BASE / book
        if not book_dir.exists():
            continue
        book_map = {}
        for chapter_file in book_dir.iterdir():
            if not chapter_file.suffix == ".md":
                continue
            try:
                content = chapter_file.read_text(encoding="utf-8")
            except OSError:
                continue
            fm_match = fm_re.search(content)
            if not fm_match:
                continue
            fm = fm_match.group(1)
            cn = chap_re.search(fm)
            pl = pov_re.search(fm)
            if cn and pl:
                chap_num = int(cn.group(1))
                pov_label = pl.group(1).strip().strip('"')
                book_map[chap_num] = pov_label
        chapter_map[book] = book_map

    return chapter_map


# ---------------------------------------------------------------------------
# HTML parsing: infobox with HTML-aware field values
# ---------------------------------------------------------------------------

class InlineTextExtractor(html.parser.HTMLParser):
    """Extract text content from an HTML fragment, handling nested tags."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._parts = []
        self._skip_depth = 0
        self.links = []  # list of (href, text) for <a> tags

    def handle_starttag(self, tag, attrs):
        if tag in ("sup", "script", "style"):
            self._skip_depth += 1
        if tag == "a" and not self._skip_depth:
            attrs_d = dict(attrs)
            self._current_link_href = attrs_d.get("title") or attrs_d.get("href", "")
            self._current_link_text = []
        if tag == "li" and not self._skip_depth:
            self._parts.append("\n")
        if tag == "br" and not self._skip_depth:
            self._parts.append("|")

    def handle_endtag(self, tag):
        if tag in ("sup", "script", "style"):
            self._skip_depth = max(0, self._skip_depth - 1)
        if tag == "a" and not self._skip_depth:
            link_text = "".join(self._current_link_text).strip()
            if link_text:
                self.links.append((self._current_link_href, link_text))
            self._current_link_href = ""
            self._current_link_text = []

    def handle_data(self, data):
        if self._skip_depth:
            return
        self._parts.append(data)
        if hasattr(self, "_current_link_text"):
            self._current_link_text.append(data)

    def get_text(self):
        raw = "".join(self._parts)
        raw = re.sub(r"\[\d+\]", "", raw)
        return raw.strip()

    def get_items(self):
        """Return list of non-empty text items split on newlines/pipes."""
        text = self.get_text()
        items = []
        for part in re.split(r"[\n|]+", text):
            part = part.strip()
            if part:
                items.append(part)
        return items


class InlineTextExtractorInit(InlineTextExtractor):
    """Same as InlineTextExtractor but initializes link tracking in __init__."""

    def __init__(self):
        super().__init__()
        self._current_link_href = ""
        self._current_link_text = []


def extract_text_and_links(html_fragment):
    """Return (items_list, links_list) from an HTML fragment."""
    parser = InlineTextExtractorInit()
    parser.feed(html_fragment)
    return parser.get_items(), parser.links


class InlineTextExtractorHTML(html.parser.HTMLParser):
    """Extract plain text + links from a <td> HTML fragment.

    Links inside <small>(...)</small> are treated as qualifiers (region scoping,
    conditional notes) rather than primary relationship targets. This prevents
    region-scoping patterns like:
        Old gods <small>(North)</small>
    from emitting "North" as a separate WORSHIPS edge target.

    self.links entries are 2-tuples (href_or_title, link_text).
    self.qualifier_links entries are also 2-tuples but are scoped qualifiers —
    callers should attach them to the preceding primary link rather than
    treating them as standalone targets.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._parts = []
        self._skip_depth = 0
        self._small_depth = 0  # tracks <small> nesting; links inside are qualifiers
        self.links = []           # primary links (outside <small>)
        self.qualifier_links = [] # qualifier links (inside <small>)
        # qualifier_for maps primary link_text → qualifier text, populated as the
        # HTML is parsed left-to-right: each qualifier is assigned to the most
        # recently completed primary link.
        self.qualifier_for = {}
        self._last_primary_text = None
        self._cur_href = ""
        self._cur_link_parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ("sup", "script", "style"):
            self._skip_depth += 1
            return
        if tag == "small" and not self._skip_depth:
            self._small_depth += 1
        if tag == "a" and not self._skip_depth:
            d = dict(attrs)
            self._cur_href = d.get("title") or d.get("href", "")
            self._cur_link_parts = []
        if tag in ("li", "br") and not self._skip_depth:
            self._parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("sup", "script", "style"):
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if tag == "small" and not self._skip_depth:
            self._small_depth = max(0, self._small_depth - 1)
        if tag == "a" and not self._skip_depth:
            link_text = "".join(self._cur_link_parts).strip()
            if link_text:
                if self._small_depth:
                    self.qualifier_links.append((self._cur_href, link_text))
                    # Attach this qualifier to the most recently seen primary link.
                    if self._last_primary_text:
                        self.qualifier_for[self._last_primary_text] = link_text
                else:
                    self.links.append((self._cur_href, link_text))
                    self._last_primary_text = link_text
            self._cur_href = ""
            self._cur_link_parts = []

    def handle_data(self, data):
        if self._skip_depth:
            return
        self._parts.append(data)
        if self._cur_href is not None and self._cur_link_parts is not None:
            self._cur_link_parts.append(data)

    def plain_text(self):
        raw = "".join(self._parts)
        raw = re.sub(r"\[\d+\]", "", raw)
        return raw.strip()

    def items(self):
        """Split on line separators (from <li>, <br>), return non-empty parts."""
        out = []
        for part in re.split(r"[\n]+", self.plain_text()):
            part = part.strip()
            if part:
                out.append(part)
        return out


# ---------------------------------------------------------------------------
# Infobox HTML parser: extracts (field, raw_html) pairs
# ---------------------------------------------------------------------------

class InfoboxFieldParser(html.parser.HTMLParser):
    """Extract (th_text, td_html) pairs from the first infobox in a page."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.fields = []          # list of (key_str, td_html_str)
        self._in_infobox = False
        self._depth = 0           # nested table depth inside infobox
        self._collecting_key = False
        self._collecting_val = False
        self._key_parts = []
        self._val_parts = []      # raw HTML of td value
        self._current_key = None
        self._raw = ""            # full source fed in

    def feed(self, data):
        self._raw += data
        super().feed(data)

    def handle_starttag(self, tag, attrs):
        raw_tag = self._get_raw_tag(tag, attrs)
        attrs_d = dict(attrs)
        cls = attrs_d.get("class", "")

        if tag == "table" and "infobox" in cls and not self._in_infobox:
            self._in_infobox = True
            self._depth = 0
            return

        if not self._in_infobox:
            return

        if tag == "table":
            self._depth += 1
            if self._collecting_val:
                self._val_parts.append(raw_tag)
            return

        if tag == "th":
            # Only collect <th scope="row"> — skip header/title rows (colspan th)
            if attrs_d.get("scope") == "row":
                self._collecting_key = True
                self._key_parts = []
            return

        if tag == "td":
            self._collecting_val = True
            self._val_parts = []
            return

        if self._collecting_val:
            self._val_parts.append(raw_tag)

    def _get_raw_tag(self, tag, attrs):
        """Reconstruct raw tag string."""
        parts = [f"<{tag}"]
        for k, v in attrs:
            if v is not None:
                parts.append(f' {k}="{v}"')
            else:
                parts.append(f" {k}")
        parts.append(">")
        return "".join(parts)

    def handle_endtag(self, tag):
        if not self._in_infobox:
            return

        if tag == "table":
            if self._depth <= 0:
                self._in_infobox = False
            else:
                self._depth -= 1
                if self._collecting_val:
                    self._val_parts.append(f"</{tag}>")
            return

        if tag == "th":
            self._collecting_key = False
            raw_key = "".join(self._key_parts)
            self._current_key = re.sub(r"\s+", " ", raw_key).strip()
            return

        if tag == "td":
            self._collecting_val = False
            if self._current_key:
                td_html = "".join(self._val_parts)
                self.fields.append((self._current_key, td_html))
            self._current_key = None
            return

        if self._collecting_val:
            self._val_parts.append(f"</{tag}>")

    def handle_data(self, data):
        if not self._in_infobox:
            return
        if self._collecting_key:
            self._key_parts.append(data)
        elif self._collecting_val:
            self._val_parts.append(data)

    def handle_entityref(self, name):
        if not self._in_infobox:
            return
        ref = f"&{name};"
        if self._collecting_key:
            self._key_parts.append(ref)
        elif self._collecting_val:
            self._val_parts.append(ref)

    def handle_charref(self, name):
        if not self._in_infobox:
            return
        ref = f"&#{name};"
        if self._collecting_key:
            self._key_parts.append(ref)
        elif self._collecting_val:
            self._val_parts.append(ref)


# ---------------------------------------------------------------------------
# Books field parsing
# ---------------------------------------------------------------------------

def parse_books_field(td_html):
    """Parse the Books infobox field into list of {book, appearance} dicts.

    Returns list of {"book": "AGOT", "appearance": "POV"} etc.
    """
    results = []
    # Pattern: <a ...>Book Name</a> ... <small>(type)</small>
    entry_re = re.compile(
        r'<a[^>]+>([^<]+)</a>.*?<small>\(([^)]+)\)</small>',
        re.DOTALL | re.IGNORECASE,
    )
    for m in entry_re.finditer(td_html):
        book_name = re.sub(r"&amp;", "&", m.group(1)).strip()
        appearance = m.group(2).strip()
        book_abbrev = BOOK_NAME_NORM.get(book_name.lower())
        if book_abbrev:
            results.append({"book": book_abbrev.upper(), "appearance": appearance})
    return results


# ---------------------------------------------------------------------------
# Entity type classification
# ---------------------------------------------------------------------------

def classify_entity_type(fields_lower):
    """Classify entity type from set of lowercase infobox field names.

    Returns best-guess entity type string, e.g. 'character.human'.
    Returns 'unknown' if no infobox or no recognizable signature.
    """
    if not fields_lower:
        return "unknown"

    scores = defaultdict(int)
    for etype, sig in ENTITY_TYPE_SIGNATURES.items():
        overlap = len(fields_lower & sig["strong"])
        scores[etype] = overlap * sig["weight"]

    if not scores or max(scores.values()) == 0:
        return "unknown"

    return max(scores, key=scores.__getitem__)


# Entity-type overrides for pages whose infobox HTML matches the {{House}}
# template (or otherwise misclassifies) but whose subject is NOT a house.
# Added 2026-04-27 (Session 25) after Stage 3a surfaced "Night's Watch typed
# as organization.house" via the test-bucket emission.
#
# v1 design choice: all overrides land at `organization.faction` regardless
# of whether the entity is technically a sworn order (Night's Watch, Kingsguard),
# a guild (Maesters, Alchemists' Guild), a sellsword company (Golden Company,
# Windblown), or a guard force (City Watch, Brazen Beasts). Finer-grained split
# (organization.order vs organization.guild vs organization.company etc.) is
# DEFERRED to the future edge-polish / entity-polish review phase, where agent
# reasoning will decide the right sub-taxonomy. Don't expand here.
ENTITY_TYPE_OVERRIDES = {
    # Sworn brotherhoods / military orders
    "Night's Watch":                "organization.faction",
    "Kingsguard":                   "organization.faction",
    "Queensguard":                  "organization.faction",
    "Rainbow Guard":                "organization.faction",
    "Kingswood Brotherhood":        "organization.faction",
    "Brotherhood of Winged Knights": "organization.faction",
    "Order of the Green Hand":      "organization.faction",
    # Religious orders
    "Faceless Men":                 "organization.faction",
    "Faith Militant":               "organization.faction",
    "Warrior's Sons":               "organization.faction",
    "Holy Hundred":                 "organization.faction",
    "Bearded priests":              "organization.faction",
    "Dragonkeepers":                "organization.faction",
    # Guilds
    "Alchemists' Guild":            "organization.faction",
    "Maesters":                     "organization.faction",
    # Sellsword companies
    "Golden Company":               "organization.faction",
    "Windblown":                    "organization.faction",
    # Guard forces
    "City Watch of King's Landing": "organization.faction",
    "Brazen Beasts":                "organization.faction",
    # Political bodies / alliances
    "Black council":                "organization.faction",
    "Band of Nine":                 "organization.faction",
    "Triarchy":                     "organization.faction",
    # Sellsword companies not covered by the regex below
    "Second Sons":                  "organization.faction",
    "Stormcrows":                   "organization.faction",
    "Long Lances":                  "organization.faction",
    "Company of the Cat":           "organization.faction",
    "Brave Companions":             "organization.faction",
    # Named artifacts without infoboxes
    "Iron Throne":                  "object.artifact",
    "Dragon egg":                   "object.artifact",
    # Mystery-knight character (Lyanna Stark's secret identity at Harrenhal —
    # R+L=J pillar). Wiki tags it as "Mystery knights" + "Terms" so
    # neither categorizer nor name-pattern catches it. Override.
    "Knight of the Laughing Tree":  "character.human",
}

# Regex patterns for page-name-based classification, evaluated AFTER the explicit
# ENTITY_TYPE_OVERRIDES dict. First match wins. Added 2026-04-30 (bug fix) to
# prevent wars and war-like conflicts from falling back to place.location.
#
# Pattern guidelines:
#   - Patterns are matched case-insensitively against the full page_name.
#   - Use ^ and $ anchors where possible to avoid accidental matches.
#   - Add a comment explaining what class of pages each pattern targets.
PAGE_NAME_TYPE_PATTERNS = [
    # Wars: "Spice War", "Salt War", "Second Turtle War", "War of Three Princes",
    # "War on Dagger Lake", "War for the Dawn", "Robert's Rebellion", etc.
    # Matches page names that end in " War" or start with "War " or contain " War ".
    (re.compile(r'\bwar\b', re.IGNORECASE), "event.war"),
    # "Rebellion" patterns: Robert's Rebellion, Blackfyre Rebellion, etc.
    (re.compile(r'\brebellion\b', re.IGNORECASE), "event.war"),
    # "Conquest" patterns: Aegon's Conquest, etc. (multi-battle campaigns)
    (re.compile(r'\bconquest\b', re.IGNORECASE), "event.war"),
    # "Invasion" patterns: Andal Invasion, etc.
    (re.compile(r'\binvasion\b', re.IGNORECASE), "event.war"),
    # "Tourney" patterns: Ashford Tourney, Tourney at Harrenhal, etc.
    # Catches pages without categories (Ashford Tourney has empty categories).
    (re.compile(r'\btourney\b', re.IGNORECASE), "event.tournament"),
    # Guards pages: "House Bolton guards", "House Stark guards", etc.
    # These are house-guard contingents, not standalone houses — classify as
    # organization.faction. Added 2026-04-30 (Bug 3 fix, session 27 audit).
    (re.compile(r'\bguards$', re.IGNORECASE), "organization.faction"),
]


def classify_by_page_name(page_name):
    """Quick classification from page name patterns and explicit overrides.

    Resolution order (first match wins):
    1. ENTITY_TYPE_OVERRIDES — explicit per-page-name override dict
    2. PAGE_NAME_TYPE_PATTERNS — regex patterns evaluated BEFORE the "House "
       prefix check, so that sub-pages like "House Bolton guards" are correctly
       classified as organization.faction rather than organization.house.
    3. "House " prefix → organization.house (catches genuine house pages after
       any more-specific patterns have had their chance to match).
    4. None (caller falls through to category-based, then infobox-based)
    """
    if page_name in ENTITY_TYPE_OVERRIDES:
        return ENTITY_TYPE_OVERRIDES[page_name]
    for pattern, entity_type in PAGE_NAME_TYPE_PATTERNS:
        if pattern.search(page_name):
            return entity_type
    if page_name.startswith("House "):
        return "organization.house"
    return None


# ---------------------------------------------------------------------------
# MediaWiki category → entity type classification
# ---------------------------------------------------------------------------
# Backfilled 2026-04-30 (Path B): the original wiki crawl stripped catlinks
# footers, leaving 70.4% of pages classified as `unknown` because the
# infobox-only path doesn't recognize swords / books / songs / castles / etc.
# The exception-fetch script `scripts/wiki-fetch-categories.py` populated
# `working/wiki-parsed/page-categories.jsonl` with MediaWiki categories for
# all 17,657 pages. This table maps those categories to project entity types.
#
# Order of precedence in process_page():
#   1. ENTITY_TYPE_OVERRIDES (explicit per-page) — always wins
#   2. PAGE_NAME_TYPE_PATTERNS (e.g. "X War" → event.war)
#   3. classify_by_categories() — MediaWiki categories, mapped via this table
#   4. classify_by_species() — Species infobox field for dragons/direwolves
#   5. classify_entity_type() — infobox-field-signature heuristics
#   6. "unknown" — fallback
#
# Rules for adding patterns:
#   - First-match-wins: order patterns from most-specific to most-general.
#   - Use anchors (^/$) to avoid accidental cross-matches.
#   - Skip-categories (Redirect, Disambiguation, TV-only) return SKIP_CATEGORY
#     so the caller can drop these from promotion entirely.
SKIP_CATEGORY = "__SKIP__"

CATEGORY_TYPE_MAP = [
    # --- Skip categories (caller filters these out of promotion) ---
    (re.compile(r"^Redirect$", re.IGNORECASE), SKIP_CATEGORY),
    (re.compile(r"^Disambiguation pages$", re.IGNORECASE), SKIP_CATEGORY),
    # Chapter-summary pages — meta-articles describing a single ASOIAF chapter
    # (e.g. "A Clash of Kings-Chapter 1"). Their infoboxes contain a "Place"
    # field which makes the field-signature classifier mistype them as
    # event.battle. They're not in-world entities; skip from promotion.
    (re.compile(r"^A Song of Ice And Fire chapters", re.IGNORECASE), SKIP_CATEGORY),
    # TV-only content — pages exist for TV episodes / seasons / cast that
    # aren't in-universe. Skip these from promotion. Real TV-vs-canon split
    # could go to a separate `tv-` namespace but that's deferred.
    (re.compile(r"^TV series$", re.IGNORECASE), SKIP_CATEGORY),
    (re.compile(r"^Episodes$", re.IGNORECASE), SKIP_CATEGORY),
    (re.compile(r"^House of the Dragon", re.IGNORECASE), SKIP_CATEGORY),
    (re.compile(r"^Game of Thrones", re.IGNORECASE), SKIP_CATEGORY),

    # --- Specific high-confidence type categories ---
    # Artifacts (swords, weapons, ships, dragon eggs, named objects)
    (re.compile(r"^(Valyrian steel blades|Swords|Weapons|Bows|Daggers|Lances|Spears|Maces|Axes|Whips|Crowns|Horns|Armor|Shields|Banners)$", re.IGNORECASE), "object.artifact"),
    (re.compile(r"^(Ships|Galleys|Cogs|Warships)$", re.IGNORECASE), "object.artifact"),
    (re.compile(r"^(Dragon eggs|Cyvasse pieces|Game pieces)$", re.IGNORECASE), "object.artifact"),

    # Texts (books, songs, decrees, letters)
    (re.compile(r"^(Books|Books and scrolls|Texts|Decrees|Letters|Documents|Manuscripts|Chronicles|Histories|Treatises)$", re.IGNORECASE), "object.text"),
    (re.compile(r"^(Songs|Ballads|Anthems|Mottoes)$", re.IGNORECASE), "object.text"),

    # Events
    (re.compile(r"^(Battles|Sieges|Skirmishes)$", re.IGNORECASE), "event.battle"),
    (re.compile(r"^(Wars|Rebellions|Conquests|Invasions|Campaigns|Conflicts|Crusades)$", re.IGNORECASE), "event.war"),
    (re.compile(r"^(Rhoynish Wars|Wars of Conquest|Dance of the Dragons)", re.IGNORECASE), "event.war"),
    (re.compile(r"^(Tournaments|Tourneys)$", re.IGNORECASE), "event.tournament"),
    (re.compile(r"^(Weddings|Assassinations|Massacres|Coronations|Funerals)$", re.IGNORECASE), "event.battle"),
    (re.compile(r"^Events$", re.IGNORECASE), "event.battle"),

    # Places
    (re.compile(r"^(Castles|Keeps|Holdfasts|Towers|Strongholds|Fortresses|Forts|Watchtowers)", re.IGNORECASE), "place.location"),
    (re.compile(r"^(Cities|Towns|Villages|Settlements|Hamlets|Holds)$", re.IGNORECASE), "place.location"),
    (re.compile(r"^(Free Cities|City states)$", re.IGNORECASE), "place.location"),
    (re.compile(r"^(Inns|Septs|Temples|Sept of)", re.IGNORECASE), "place.location"),
    (re.compile(r"^(Brothels|Taverns)$", re.IGNORECASE), "place.location"),
    (re.compile(r"^(Islands|Mountains|Rivers|Seas|Bays|Forests|Lakes|Marshes|Plains|Hills|Valleys|Caves|Tunnels|Roads|Crossings|Fords|Passes|Ruins)$", re.IGNORECASE), "place.location"),
    (re.compile(r"^(Regions|Realms|Kingdoms|Continents|Territories)$", re.IGNORECASE), "place.region"),
    (re.compile(r"^Places (in|of) ", re.IGNORECASE), "place.location"),
    # Streets, gates, halls, rooms — interior/exterior places
    (re.compile(r"^Streets in ", re.IGNORECASE), "place.location"),
    (re.compile(r"^(Halls|Gates|Squares|Plazas|Markets|Bridges|Wells|Gardens)$", re.IGNORECASE), "place.location"),

    # Organizations
    (re.compile(r"^Noble houses$", re.IGNORECASE), "organization.house"),
    (re.compile(r"^Houses ", re.IGNORECASE), "organization.house"),
    (re.compile(r"^Houses (with|without|from|of) ", re.IGNORECASE), "organization.house"),
    (re.compile(r"^(Knightly orders|Sworn brotherhoods|Sellsword companies|Mercenary companies|Guilds|Orders|Brotherhoods|Sisterhoods|Cults|Crews)$", re.IGNORECASE), "organization.faction"),
    (re.compile(r"^Mountain clans of ", re.IGNORECASE), "organization.faction"),
    (re.compile(r"^Organizations$", re.IGNORECASE), "organization.faction"),
    (re.compile(r"^(Religions|Religious orders|Faiths|Pantheons|Deities|Gods|Goddesses)$", re.IGNORECASE), "organization.religion"),
    (re.compile(r"^Cultures$", re.IGNORECASE), "concept.culture"),

    # Species (biological types — NOT individuals)
    # Trees go here too; weirwoods are first-class narrative entities,
    # and the species/ dir scope broadens to in-world flora/fauna kinds.
    # Trees take precedence over Food when both categories are present
    # (Apple, Lemon, Orange, Chestnut tree are dual-tagged).
    (re.compile(r"^(Species|Magical creatures|Magical races|Sentient species)$", re.IGNORECASE), "species"),
    (re.compile(r"^Trees$", re.IGNORECASE), "species"),

    # Food + drinks (object.food — narrative hospitality / D&E food culture).
    (re.compile(r"^(Food|Foods|Drinks|Drink|Beverages)$", re.IGNORECASE), "object.food"),

    # Concepts
    (re.compile(r"^(Magic|Magical phenomena|Magical abilities|Magical objects)$", re.IGNORECASE), "concept.magic"),
    (re.compile(r"^(Prophecies|Prophetic dreams|Visions)$", re.IGNORECASE), "concept.prophecy"),
    (re.compile(r"^(Theories|Theory)$", re.IGNORECASE), "concept.theory"),

    # Catch-all for named objects (catches "Objects" + "Merchant ships" etc.
    # that escaped the more specific Ships/Crowns/etc. patterns above)
    (re.compile(r"^Objects$", re.IGNORECASE), "object.artifact"),
    (re.compile(r"^Merchant ships$", re.IGNORECASE), "object.artifact"),

    # Titles
    (re.compile(r"^Titles$", re.IGNORECASE), "title"),

    # --- Lower-confidence / character-default patterns (fall last) ---
    # Specific character categories
    (re.compile(r"^Characters from ", re.IGNORECASE), "character.human"),
    (re.compile(r"^Character pages ", re.IGNORECASE), "character.human"),  # meta tag
    (re.compile(r"^(Nobles|Noblewomen|Smallfolk|Knights|Squires|Septons|Septas|Maesters|Grand Maesters|Bastards|Slaves|Sellswords|Hedge knights|Mercenaries)$", re.IGNORECASE), "character.human"),
    (re.compile(r"^(Casualties of |Slain in )", re.IGNORECASE), "character.human"),  # death tags imply person
    (re.compile(r"^(Kings|Queens|Princes|Princesses|Lords|Ladies|Dukes|Counts|Sers)$", re.IGNORECASE), "character.human"),
    (re.compile(r"^Unnamed characters$", re.IGNORECASE), "character.human"),
    (re.compile(r"^(Wildlings|Free folk)$", re.IGNORECASE), "character.human"),  # individual wildling pages
    (re.compile(r"birth(s|ed)?$", re.IGNORECASE), "character.human"),  # "263 AC births"
    (re.compile(r"death(s|ed)?$", re.IGNORECASE), "character.human"),  # "299 AC deaths"
]


def classify_by_categories(categories):
    """Classify entity by MediaWiki categories.

    Args:
        categories: list[str] — category names (without "Category:" prefix)

    Returns:
        - SKIP_CATEGORY string if any skip-pattern matches → caller drops page
        - Entity type string ("object.artifact", "place.location", etc.) on first match
        - None if no pattern matches → caller falls through to infobox-based
    """
    if not categories:
        return None

    # Real-world publication filter: pages categorized only as "Books"
    # (without the in-world "Books and scrolls" companion category) are
    # real-world publications — the ASOIAF novels, novellas, comics,
    # companion books, parodies. Skip them from the in-world graph.
    cat_set = {c.lower() for c in categories}
    if "books" in cat_set and "books and scrolls" not in cat_set:
        return SKIP_CATEGORY

    # First pass: skip-categories take priority (Redirect, Disambiguation, TV)
    for cat in categories:
        for pattern, etype in CATEGORY_TYPE_MAP:
            if etype == SKIP_CATEGORY and pattern.search(cat):
                return SKIP_CATEGORY

    # Second pass: type categories. First match across (category × pattern) wins.
    # Walk patterns in order so high-confidence patterns beat low-confidence
    # patterns when a page has multiple categories.
    for pattern, etype in CATEGORY_TYPE_MAP:
        if etype == SKIP_CATEGORY:
            continue
        for cat in categories:
            if pattern.search(cat):
                return etype

    return None


# Module-level cache for page-categories.jsonl (loaded once in main()).
_PAGE_CATEGORIES: dict[str, list[str]] = {}


def load_page_categories():
    """Load working/wiki-parsed/page-categories.jsonl into _PAGE_CATEGORIES dict.

    Called once from main() before processing pages. Returns count loaded.
    Returns 0 if the file doesn't exist (parser still works in legacy mode).
    """
    global _PAGE_CATEGORIES
    if not PAGE_CATEGORIES_FILE.exists():
        return 0
    n = 0
    with open(PAGE_CATEGORIES_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            page = rec.get("page")
            cats = rec.get("categories") or []
            if page:
                _PAGE_CATEGORIES[page] = cats
                n += 1
    return n


# ---------------------------------------------------------------------------
# Species-based type classification (for characters)
# ---------------------------------------------------------------------------

# Date-indicator patterns for Born/Died field filtering.
# Added 2026-04-30 (Bug 1 fix, session 27 audit).
#
# InlineTextExtractorHTML stores links as (href_or_title, link_text) where
# href_or_title is the HTML title= attribute when present (e.g. "37 AC",
# "Years after Aegon's Conquest") or href= when title= is absent (e.g.
# "/index.php/Years_after_Aegon%27s_Conquest#..."). The visible link text
# carries the date string with non-breaking spaces, e.g. "263 AC".
_DATE_TITLE_RE = re.compile(
    # title= attribute forms: year-anchor pages and era names
    r"^Years\s+(?:after|before)\s+Aegon"
    r"|^\d[\d\s\xa0–—-]*(?:AC|BC)?\s*$"
    r"|^(?:Age of Heroes|Long Night|Dawn Age"
    r"|Age of Valyria|Valyrian Freehold"
    r"|Days of the First Men)\s*$",
    re.IGNORECASE,
)
_DATE_HREF_URL_RE = re.compile(
    r'Years_(?:after|before)_Aegon|/\d+_(?:AC|BC)',
    re.IGNORECASE,
)
_DATE_TEXT_RE = re.compile(
    # Pattern A: basic year/era with optional AC/BC (e.g. "263 AC", "37", "Dawn Age")
    r'^(?:\d[\d–—–\-\s\xa0]*(?:AC|BC)?'
    r'|(?:Age of Heroes|Long Night|Dawn Age|Age of Valyria|'
    r'Valyrian Freehold|Days of the First Men)'
    r')\s*$'
    # Pattern B: "<year> AC or before/after/year" — date link stripped, plain text residue
    # e.g. "240 AC or before", "226 AC or after", "161 AC or 162 AC"
    # Also handles "X BC or Y BC", "X AC or Y AC" two-option year ranges.
    # Also handles "In or after <year> AC" / "or after <year> AC" (prose prefix variants).
    # Added 2026-04-30 (Bug 4 fix, session 27 audit — 199 date-bleed stragglers).
    r'|^\d[\d\s\xa0]*(?:AC|BC)\s+or\s+(?:before|after|\d[\d\s\xa0]*(?:AC|BC))\s*$'
    r'|^(?:In\s+)?or\s+(?:before|after)\s+\d[\d\s\xa0]*(?:AC|BC)\s*$'
    # Pattern C: "<year> BC – <year> AC" ranges — both date links stripped, plain text
    # residue contains the full range e.g. "11 BC – 1 AC"
    # Added 2026-04-30 (Bug 4 fix, session 27 audit).
    r'|^\d[\d\s\xa0]*BC[\s\xa0]*[–—\-]+[\s\xa0]*\d[\d\s\xa0]*AC\s*$',
    re.IGNORECASE,
)

# Also treat link targets that are pure-numeric (e.g. "282" from bare-year
# bleed) as date-type. Combined with the regex above in _is_date_link().


def _is_date_link(href_or_title: str, link_text: str) -> bool:
    """Return True if this link represents a temporal reference, not a place.

    Used exclusively in Born/Died/Buried field handling to separate location
    targets from date qualifiers.

    href_or_title is what InlineTextExtractorHTML stores: the HTML title=
    attribute of the <a> tag (preferred), or href= when title= is absent.
    """
    t = href_or_title.strip()
    if _DATE_TITLE_RE.match(t):
        return True
    if _DATE_HREF_URL_RE.search(t):
        return True
    # Also test the visible link text (normalise non-breaking space)
    clean = link_text.replace("\xa0", " ").strip()
    if _DATE_TEXT_RE.match(clean):
        return True
    # Pure-numeric (bare year without AC/BC suffix)
    if re.match(r'^\d{1,4}$', clean):
        return True
    return False


# Species field value → entity type override.
# The wiki "Species" infobox field is not in FIELD_EDGE_MAP (it informs node
# type, not an edge). We read it during page processing and use it to override
# the field-signature-based type guess for dragon and direwolf pages.
# Added 2026-04-30 (Bug 2 fix, session 27 audit).
_SPECIES_TYPE_MAP = {
    "dragon":   "character.dragon",
    "direwolf": "character.direwolf",
}


def classify_by_species(fields_dict: dict) -> str | None:
    """Return type override from the 'Species' infobox field, or None.

    Reads the raw td_html for the Species field, extracts the link text
    or plain text, and looks it up in _SPECIES_TYPE_MAP (case-insensitive).
    """
    # Look for the Species field (case-insensitive key lookup)
    species_html = None
    for k, v in fields_dict.items():
        if k.lower() == "species":
            species_html = v
            break
    if species_html is None:
        return None

    # Extract plain text (or link text) from the Species td HTML.
    # InlineTextExtractorInit already strips tags and returns items.
    items, links = extract_text_and_links(species_html)
    # Prefer the first link text (e.g. "Dragon"); fall back to plain text items.
    species_str = ""
    if links:
        species_str = links[0][1].strip()
    elif items:
        species_str = items[0].strip()

    if not species_str:
        return None

    return _SPECIES_TYPE_MAP.get(species_str.lower())


# ---------------------------------------------------------------------------
# Relationship extraction
# ---------------------------------------------------------------------------

def parse_relationship_field(field_name, td_html):
    """Parse a relationship infobox field into a list of relationship objects.

    Returns list of dicts: {field, target, edge_type, direction, qualifier}.
    qualifier is text in parentheses after the name, e.g. "(m. 283 AC)".
    """
    field_lower = field_name.lower()
    if field_lower not in FIELD_EDGE_MAP:
        return None

    edge_type, direction = FIELD_EDGE_MAP[field_lower]

    # Born/Died/Buried fields have special date-bleed handling (Bug 1 fix,
    # 2026-04-30). The wiki encodes these fields as:
    #   <date link><br><place link>[, secondary place link]
    # e.g. "263\xa0AC<br>Winterfell, the North"
    # We need to separate date links from place links:
    #   - Date links → stored as qualifier on the edge, NOT as a second target
    #   - Place links → emitted as the edge target (one edge per place)
    # This prevents "263 AC" and "Age of Heroes" from being emitted as
    # BORN_AT/DIED_AT targets (they're dates, not places).
    is_born_died_field = field_lower in ("born", "died", "buried")
    is_heir_field = field_lower in ("heir", "heirs")

    parser = InlineTextExtractorHTML()
    parser.feed(td_html)
    items = parser.items()
    links = parser.links

    results = []

    # qualifier_for maps primary link_text → qualifier text.
    # Populated in parse order by InlineTextExtractorHTML: each <small>-scoped
    # link is attached to the most recently completed primary link.
    qualifier_for = parser.qualifier_for

    # For Born/Died/Buried: separate date links from place links BEFORE deciding
    # whether to use the links path or the plain-text path.
    # Collect the first date link text as the edge qualifier; remove all
    # date links from the list so only place links remain.
    date_qualifier = None
    if (is_born_died_field or is_heir_field) and links:
        for href, link_text in links:
            lt = link_text.strip()
            if _is_date_link(href, lt):
                if date_qualifier is None:
                    # Use the first date link text as the qualifier
                    date_qualifier = lt.replace("\xa0", " ").strip()
        # Rebuild links to contain only place links
        links = [
            (href, lt)
            for href, lt in links
            if not _is_date_link(href, lt.strip())
        ]
        # For heir fields: discard date qualifier since dates are annotations,
        # not meaningful edge data. Keep only character-name links.
        if is_heir_field:
            date_qualifier = None

    if links:
        # Use link titles/text as primary targets (cleaner than raw text).
        # Skip targets that are bare lowercase words — these are non-proper-noun
        # wiki article names (e.g., "religions" → /index.php/Religion) that leaked
        # in through the link extractor and are not real relationship targets.
        seen = set()
        for href, link_text in links:
            link_text = link_text.strip()
            if not link_text or link_text in seen:
                continue
            # Skip non-proper-noun targets: starts with lowercase (e.g. "religions",
            # "mixed", "lords freeholder" used as a descriptor, not an entity name).
            if link_text and link_text[0].islower():
                continue
            seen.add(link_text)
            # Qualifier: for Born/Died/Buried, use the extracted date qualifier.
            # For other fields: prefer the small-scoped qualifier associated with
            # this primary target. Fall back to parenthetical patterns in items.
            if is_born_died_field:
                qualifier = date_qualifier or qualifier_for.get(link_text)
            else:
                qualifier = qualifier_for.get(link_text)
            if not qualifier:
                for item in items:
                    if link_text in item:
                        q_match = re.search(r'\(([^)]+)\)', item)
                        if q_match:
                            qualifier = q_match.group(1)
                        break
            rel = {
                "field": field_name,
                "target": link_text,
                "edge_type": edge_type,
                "direction": direction,
            }
            if qualifier:
                rel["qualifier"] = qualifier
            results.append(rel)
    else:
        # No links (or all links were date links for Born/Died/Buried) —
        # use plain text items. Split on ';' as primary separator
        # (wiki religion/allegiance fields use semicolons to separate entities).
        # Parenthesized text becomes qualifier metadata, not a separate target.
        expanded_items = []
        for item in items:
            for sub in re.split(r'\s*;\s*', item):
                sub = sub.strip()
                if sub:
                    expanded_items.append(sub)

        for item in expanded_items:
            item = item.strip()
            if not item:
                continue
            # Start with the date_qualifier already extracted from date links
            # (set when all links were filtered as dates; None otherwise).
            qualifier = date_qualifier
            q_match = re.search(r'\(([^)]+)\)', item)
            if q_match:
                if not qualifier:
                    qualifier = q_match.group(1)
                item = item[:q_match.start()].strip()
            if not item:
                continue
            # Skip non-proper-noun bare words (lowercase first character)
            if item[0].islower():
                continue

            # For Born/Died/Buried plain-text items: split "Place, Year" patterns.
            # e.g. "Winterfell, 263 AC" → target="Winterfell", qualifier="263 AC"
            # This handles Sub-pattern B from the audit where there are no links
            # and the entire "Place, Date" string is in one text item.
            if is_born_died_field or is_heir_field:
                # Match "Place, <date>" where date is year/era at end of string
                date_suffix_m = re.search(
                    r',\s*((?:\d[\d\xa0\s–—-]*(?:AC|BC)?'
                    r'|Age of Heroes|Long Night|Dawn Age'
                    r'|Age of Valyria|Valyrian Freehold'
                    r'|Days of the First Men)\s*)$',
                    item,
                    re.IGNORECASE,
                )
                if date_suffix_m:
                    # Extract date as qualifier and strip from target
                    if not qualifier:
                        qualifier = date_suffix_m.group(1).replace("\xa0", " ").strip()
                    item = item[:date_suffix_m.start()].strip()
                if not item:
                    continue
                # Skip items that are purely a date string (no place component).
                # Also skip "In <year>" form (e.g. "In 94 AC") where "In" is a
                # prose prefix from the td HTML around a date link.
                cleaned = item.replace("\xa0", " ").strip()
                if _is_date_link("", cleaned):
                    continue
                # Strip leading "In " prefix before checking again
                stripped = re.sub(r'^In\s+', '', cleaned, flags=re.IGNORECASE)
                if stripped != cleaned and _is_date_link("", stripped):
                    continue
                item = cleaned  # use normalised form as the target

            rel = {
                "field": field_name,
                "target": item,
                "edge_type": edge_type,
                "direction": direction,
            }
            if qualifier:
                rel["qualifier"] = qualifier
            results.append(rel)

    return results


# ---------------------------------------------------------------------------
# Alias extraction
# ---------------------------------------------------------------------------

def parse_aliases_field(td_html):
    """Extract list of alias strings from the Aliases infobox field."""
    parser = InlineTextExtractorHTML()
    parser.feed(td_html)
    return [item for item in parser.items() if item]


# ---------------------------------------------------------------------------
# Cite-ref extraction
# ---------------------------------------------------------------------------

def extract_cite_refs(html_str):
    """Return {book: sorted_list_of_chapter_ints} from cite_ref anchor IDs."""
    matches = CITE_REF_RE.findall(html_str)
    by_book = defaultdict(set)
    for book, chap_str in matches:
        by_book[book.lower()].add(int(chap_str))
    return {book: sorted(chaps) for book, chaps in by_book.items()}


def cite_ref_counts(cite_refs):
    """Convert {book: [chapters]} to {book: count}."""
    return {book: len(chaps) for book, chaps in cite_refs.items()}


# ---------------------------------------------------------------------------
# first_available resolution
# ---------------------------------------------------------------------------

def resolve_first_available(cite_refs, books_list, chapter_map):
    """Compute first_available from cite_refs (preferred) or books field.

    Returns {"book": "AGOT", "chapter": 2, "pov": "Bran I", "source": "cite_ref"}
    or {"book": "AGOT", "appearance": "POV", "source": "infobox_books"}
    or None if not determinable.
    """
    # Strategy 1: cite_refs — find the earliest chapter across all books.
    # Exclude chapter 0: the wiki occasionally uses 0 for front-matter or prologue
    # references that don't correspond to a real chapter in our chapter map.
    # Chapter 0 is preserved in cite_refs for completeness but excluded from
    # first_available selection to avoid false "ADWD Prologue" results for
    # entities that clearly appear first in AGOT.
    best_book = None
    best_chap = None

    for book in BOOKS:
        chapters = [c for c in cite_refs.get(book, []) if c > 0]
        if not chapters:
            continue
        min_chap = min(chapters)
        if best_chap is None or min_chap < best_chap or (
            min_chap == best_chap and BOOKS.index(book) < BOOKS.index(best_book)
        ):
            best_chap = min_chap
            best_book = book

    if best_book and best_chap is not None:
        pov_label = chapter_map.get(best_book, {}).get(best_chap)
        result = {
            "book": best_book.upper(),
            "chapter": best_chap,
            "source": "cite_ref",
        }
        if pov_label:
            result["pov"] = pov_label
        return result

    # Strategy 2: infobox Books field — first non-mentioned appearance
    for entry in books_list:
        if entry["appearance"].lower() != "mentioned":
            return {
                "book": entry["book"],
                "appearance": entry["appearance"],
                "source": "infobox_books",
            }

    # Strategy 3: first mentioned if nothing else
    if books_list:
        return {
            "book": books_list[0]["book"],
            "appearance": books_list[0]["appearance"],
            "source": "infobox_books_mentioned_only",
        }

    return None


# ---------------------------------------------------------------------------
# Per-page processing
# ---------------------------------------------------------------------------

def process_page(page_name, html_str, chapter_map, verbose=False):
    """Process one wiki page.

    Returns:
      infobox_record — dict for infobox-data.jsonl (or None if no infobox)
      index_record   — dict for page-index.jsonl (always present)
      warnings       — list of warning strings
    """
    warnings = []
    byte_size = len(html_str.encode("utf-8"))
    has_infobox = 'class="infobox"' in html_str

    # --- Cite refs (always extracted, not just for infobox pages) ---
    cite_refs = extract_cite_refs(html_str)
    cr_counts = cite_ref_counts(cite_refs)

    # Full count across all books
    total_cite_refs = sum(cr_counts.values())

    # --- Categories ---
    # Primary source: working/wiki-parsed/page-categories.jsonl, populated by
    # scripts/wiki-fetch-categories.py (Path B exception fetch, 2026-04-30).
    # The original wiki crawl stripped catlinks footers, so the inline href
    # extraction below is a fallback only.
    categories = list(_PAGE_CATEGORIES.get(page_name, []))
    if not categories:
        # Fallback: extract whatever Category: hrefs exist in the body HTML
        # (usually just gallery image links — but better than nothing if the
        # categories cache is missing for this page).
        category_hrefs = re.findall(r'href="/index\.php/Category:([^"]+)"', html_str, re.IGNORECASE)
        categories = list({
            href.replace("_", " ").split("?")[0]
            for href in category_hrefs
            if "Images_of" not in href and "images of" not in href.lower()
        })

    # Page-name hint (overrides + regex patterns + "House " prefix)
    name_hint = classify_by_page_name(page_name)

    # Category-based classification (NEW 2026-04-30; MediaWiki category mapping)
    cat_hint = classify_by_categories(categories)

    # Skip-category check: if categories say this is a Redirect / Disambiguation /
    # TV-only page, mark the page as such so callers can drop it from promotion.
    if cat_hint == SKIP_CATEGORY:
        # Surface skip status via index_record.skip_reason (not a real entity type).
        # Don't return early — still emit the page-index record so the skip is
        # visible in audits.
        skip_reason = "category-skip"
        entity_type_guess = "skip"
    elif not has_infobox:
        # Without infobox, prefer name_hint > cat_hint > unknown
        skip_reason = None
        entity_type_guess = name_hint or cat_hint or "unknown"
    else:
        skip_reason = None
        # Parse infobox fields
        field_parser = InfoboxFieldParser()
        try:
            field_parser.feed(html_str)
        except Exception as e:
            warnings.append(f"InfoboxFieldParser error: {e}")
            field_parser.fields = []

        fields_dict = {}
        for field_name, td_html in field_parser.fields:
            # Clean field name: strip HTML tags, normalize whitespace
            clean_name = re.sub(r"<[^>]+>", "", field_name).strip()
            clean_name = re.sub(r"\s+", " ", clean_name)
            if clean_name:
                fields_dict[clean_name] = td_html

        fields_lower = {k.lower() for k in fields_dict}
        # Resolution order: name_hint > cat_hint > infobox-field-signature > unknown
        entity_type_guess = name_hint or cat_hint or classify_entity_type(fields_lower)

        # Species-based type override: if the infobox has a "Species" field whose
        # value is "Dragon" or "Direwolf", override the type regardless of what
        # field-signature classification produced. This fixes the dragon-mistyping
        # bug (Bug 2, 2026-04-30 audit) where all dragons defaulted to
        # character.human because they share infobox fields with human characters.
        # Species-based overrides only apply when the page-name hint hasn't
        # already pinned a non-character type (e.g. we don't want to override an
        # event.war page that happens to have a species field).
        if not name_hint or entity_type_guess.startswith("character"):
            species_override = classify_by_species(fields_dict)
            if species_override:
                entity_type_guess = species_override

        if verbose:
            print(f"    Fields: {list(fields_dict.keys())[:12]}")
            print(f"    Entity type: {entity_type_guess}")

    # --- Build index record (every page) ---
    index_record = {
        "page": page_name,
        "entity_type_guess": entity_type_guess,
        "categories": categories,
        "cite_ref_books": {b: cr_counts.get(b, 0) for b in BOOKS},
        "has_infobox": has_infobox,
        "byte_size": byte_size,
    }
    if skip_reason:
        index_record["skip_reason"] = skip_reason

    # Skip-categorized pages don't get an infobox-data.jsonl row even if they
    # have an infobox HTML structure (Disambiguation/Redirect/TV pages have
    # infoboxes but their content isn't useful as an entity edge source).
    if skip_reason or not has_infobox:
        return None, index_record, warnings

    # --- Parse infobox fields for infobox-data.jsonl ---
    # Re-use fields_dict from above
    books_list = []
    relationships = []
    aliases = []
    unmapped_fields = []

    for field_name, td_html in fields_dict.items():
        field_lower = field_name.lower()

        # Skip TV/publication fields
        if field_lower in SKIP_FIELDS:
            continue

        # Books field
        if field_lower == "books":
            books_list = parse_books_field(td_html)
            continue

        # Alias fields
        if field_lower in ("alias", "aliases", "also known as", "epithet", "epithets"):
            aliases = parse_aliases_field(td_html)
            continue

        # Relationship fields
        rels = parse_relationship_field(field_name, td_html)
        if rels is not None:
            relationships.extend(rels)
        else:
            # Track unmapped fields (excluding known non-relationship fields)
            known_non_rel = {
                "coat of arms", "location", "government", "notable places",
                "population", "date", "place", "strength", "casualties",
                "commanders", "office", "current holder", "first holder",
                "creator", "type", "term length", "note", "species",
                "culture", "image", "caption", "status", "gender",
                "born", "died",
            }
            if field_lower not in known_non_rel:
                unmapped_fields.append(field_name)

    # Resolve first_available
    first_available = resolve_first_available(cite_refs, books_list, chapter_map)

    infobox_record = {
        "page": page_name,
        "entity_type": entity_type_guess,
        "first_available": first_available,
        "books": books_list,
        "relationships": relationships,
        "aliases": aliases,
        "cite_refs": cite_refs,
    }

    if unmapped_fields and verbose:
        print(f"    Unmapped fields: {unmapped_fields}")

    return infobox_record, index_record, warnings + (
        [f"unmapped_fields: {unmapped_fields}"] if unmapped_fields else []
    )


# ---------------------------------------------------------------------------
# Stats collection
# ---------------------------------------------------------------------------

class Stats:
    def __init__(self):
        self.total_pages = 0
        self.infobox_pages = 0
        self.cite_ref_pages = 0
        self.entity_type_counts = defaultdict(int)
        self.field_counts = defaultdict(int)
        self.unmapped_field_counts = defaultdict(int)
        self.failures = []
        self.warnings = []

    def record_index(self, rec):
        self.total_pages += 1
        if rec["has_infobox"]:
            self.infobox_pages += 1
        if any(rec["cite_ref_books"].values()):
            self.cite_ref_pages += 1
        self.entity_type_counts[rec["entity_type_guess"]] += 1

    def record_infobox(self, rec, raw_warnings):
        for w in raw_warnings:
            if w.startswith("unmapped_fields: "):
                fields_str = w[len("unmapped_fields: "):]
                try:
                    fields = eval(fields_str)  # safe: only our own output
                    for f in fields:
                        self.unmapped_field_counts[f] += 1
                except Exception:
                    pass

    def record_failure(self, page_name, error):
        self.failures.append((page_name, error))

    def record_field(self, field_name):
        self.field_counts[field_name.lower()] += 1


# ---------------------------------------------------------------------------
# Output writing helpers
# ---------------------------------------------------------------------------

def write_stats(stats, output_path, elapsed_sec=None):
    """Write parse-stats.md summary."""
    lines = [
        "# Wiki Infobox Parser — Parse Stats",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Overview",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total pages processed | {stats.total_pages:,} |",
        f"| Pages with infoboxes | {stats.infobox_pages:,} |",
        f"| Pages with cite_refs | {stats.cite_ref_pages:,} |",
        f"| Parse failures | {len(stats.failures)} |",
    ]
    if elapsed_sec is not None:
        lines.append(f"| Elapsed time | {elapsed_sec:.1f}s |")

    lines += [
        "",
        "## Entity Type Distribution",
        "",
        "| Entity Type | Count |",
        "|------------|-------|",
    ]
    for etype, count in sorted(stats.entity_type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| `{etype}` | {count:,} |")

    lines += [
        "",
        "## Top 30 Most Common Infobox Fields",
        "",
        "| Field | Count |",
        "|-------|-------|",
    ]
    # Fields that are handled specially (not via FIELD_EDGE_MAP but not truly unmapped)
    _handled_fields = set(FIELD_EDGE_MAP.keys()) | {
        "books", "book", "aliases", "alias", "also known as", "epithet", "epithets",
        "coat of arms", "location", "government", "notable places", "population",
        "date", "place", "strength", "casualties", "commanders", "office",
        "current holder", "first holder", "creator", "type", "term length",
        "note", "species", "image", "caption", "status", "gender",
    } | SKIP_FIELDS
    top_fields = sorted(stats.field_counts.items(), key=lambda x: -x[1])[:30]
    for field, count in top_fields:
        mapped = field in _handled_fields
        marker = "" if mapped else " ⚠ (unmapped)"
        lines.append(f"| `{field}`{marker} | {count:,} |")

    if stats.unmapped_field_counts:
        lines += [
            "",
            "## Unmapped Infobox Fields (schema signals)",
            "",
            "These fields appear in infoboxes but are not in FIELD_EDGE_MAP.",
            "High-count entries may indicate missing edge types.",
            "",
            "| Field | Count |",
            "|-------|-------|",
        ]
        for field, count in sorted(stats.unmapped_field_counts.items(), key=lambda x: -x[1])[:40]:
            lines.append(f"| `{field}` | {count:,} |")

    if stats.failures:
        lines += [
            "",
            "## Parse Failures",
            "",
        ]
        for page, error in stats.failures[:50]:
            lines.append(f"- `{page}`: {error}")
        if len(stats.failures) > 50:
            lines.append(f"- ... and {len(stats.failures) - 50} more")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
        help="Process a single page by its filename stem (without .json) and print result",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Print per-page progress",
    )
    args = parser.parse_args()

    # --- Single-page debug mode ---
    if args.page:
        raw_file = RAW_DIR / f"{args.page}.json"
        if not raw_file.exists():
            print(f"ERROR: Not found: {raw_file}", file=sys.stderr)
            sys.exit(1)
        chapter_map = build_chapter_map()
        n_cats = load_page_categories()
        if n_cats:
            print(f"Loaded MediaWiki categories for {n_cats:,} pages")
        else:
            print("No page-categories.jsonl found — proceeding without category data")
        data = json.loads(raw_file.read_text(encoding="utf-8"))
        html_str = data.get("html", "")
        infobox_rec, index_rec, warnings = process_page(
            data.get("page", args.page), html_str, chapter_map, verbose=True
        )
        print("\n--- infobox-data ---")
        print(json.dumps(infobox_rec, indent=2, ensure_ascii=False))
        print("\n--- page-index ---")
        print(json.dumps(index_rec, indent=2, ensure_ascii=False))
        if warnings:
            print("\n--- warnings ---")
            for w in warnings:
                print(f"  {w}")
        return

    # --- Batch processing ---
    import time
    start_time = time.monotonic()

    # Build chapter map
    print("Building chapter→POV map from chapter source files...")
    chapter_map = build_chapter_map()
    mapped_total = sum(len(v) for v in chapter_map.values())
    print(f"  Mapped {mapped_total} chapters across {len(chapter_map)} books")

    # Load MediaWiki categories (Path B exception fetch — 2026-04-30)
    print("Loading MediaWiki categories from page-categories.jsonl...")
    n_cats = load_page_categories()
    if n_cats:
        print(f"  Loaded categories for {n_cats:,} pages")
    else:
        print("  WARNING: page-categories.jsonl not found — categorization "
              "will fall back to infobox-only (legacy mode, ~70% unknown)")

    # Collect input files
    raw_files = sorted(
        f for f in RAW_DIR.iterdir()
        if f.suffix == ".json"
        and not f.name.startswith(".")
        and not f.name.startswith("CAT_")
        and not f.name.startswith("ALL_")
    )
    if args.limit:
        raw_files = raw_files[: args.limit]
        print(f"Limited to {args.limit} pages (--limit flag)")

    total = len(raw_files)
    print(f"Processing {total:,} wiki pages...")

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    stats = Stats()

    with open(INFOBOX_DATA_FILE, "w", encoding="utf-8") as ib_out, \
         open(PAGE_INDEX_FILE, "w", encoding="utf-8") as pi_out:

        for i, raw_file in enumerate(raw_files, 1):
            if args.verbose or (i % 1000 == 0):
                pct = i / total * 100
                print(f"  [{i:>6}/{total}] {pct:.1f}%  {raw_file.name}")

            # Load cached page
            try:
                data = json.loads(raw_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as e:
                stats.record_failure(raw_file.stem, f"load error: {e}")
                continue

            page_name = data.get("page", raw_file.stem)
            html_str = data.get("html", "")

            if not html_str:
                stats.record_failure(page_name, "empty html")
                continue

            # Process page
            try:
                infobox_rec, index_rec, warnings = process_page(
                    page_name, html_str, chapter_map, verbose=args.verbose
                )
            except Exception as e:
                stats.record_failure(page_name, f"process error: {e}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()
                # Emit minimal index record so page is in the L1 index
                byte_size = len(html_str.encode("utf-8"))
                index_rec = {
                    "page": page_name,
                    "entity_type_guess": "unknown",
                    "categories": [],
                    "cite_ref_books": {b: 0 for b in BOOKS},
                    "has_infobox": False,
                    "byte_size": byte_size,
                }
                pi_out.write(json.dumps(index_rec, ensure_ascii=False) + "\n")
                stats.record_index(index_rec)
                continue

            # Record field stats
            if infobox_rec:
                for field_lower in {r["field"].lower() for r in infobox_rec.get("relationships", [])}:
                    stats.field_counts[field_lower] += 1
                # Also record books, aliases, and all parsed fields
                if infobox_rec.get("books"):
                    stats.field_counts["books"] += 1
                if infobox_rec.get("aliases"):
                    stats.field_counts["aliases"] += 1

            # Collect unmapped field warnings
            if infobox_rec:
                stats.record_infobox(infobox_rec, warnings)

            # Write index record (every page)
            pi_out.write(json.dumps(index_rec, ensure_ascii=False) + "\n")
            stats.record_index(index_rec)

            # Write infobox record (only pages with infoboxes)
            if infobox_rec:
                ib_out.write(json.dumps(infobox_rec, ensure_ascii=False) + "\n")

            if warnings and args.verbose:
                for w in warnings:
                    print(f"    WARNING: {w}", file=sys.stderr)

    elapsed = time.monotonic() - start_time

    # Write stats file
    # First, collect all field counts from the infobox data for a more complete picture
    # Re-scan infobox-data.jsonl to count all fields
    print("Tallying infobox field frequencies...")
    all_field_counts = defaultdict(int)
    all_unmapped = defaultdict(int)
    with open(INFOBOX_DATA_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            # Count relationship fields
            for rel in rec.get("relationships", []):
                all_field_counts[rel["field"].lower()] += 1
            # Count books and aliases presence
            if rec.get("books"):
                all_field_counts["books"] += 1
            if rec.get("aliases"):
                all_field_counts["aliases"] += 1

    stats.field_counts = all_field_counts

    # Also rescan for unmapped — we need to re-parse to find them
    # Use the index to find infobox pages, re-parse their fields quickly
    print("Scanning for unmapped infobox fields...")
    infobox_pages = set()
    with open(PAGE_INDEX_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                if rec.get("has_infobox"):
                    infobox_pages.add(rec["page"])
            except json.JSONDecodeError:
                pass

    unmapped_field_counts = defaultdict(int)
    known_rel_fields = set(FIELD_EDGE_MAP.keys())
    known_non_rel = {
        "coat of arms", "location", "government", "notable places",
        "population", "date", "place", "strength", "casualties",
        "commanders", "office", "current holder", "first holder",
        "creator", "type", "term length", "note", "species",
        "image", "caption", "status", "gender",
        "books", "aliases", "alias", "also known as", "epithet", "epithets",
    }
    known_non_rel |= SKIP_FIELDS

    page_file_map = {
        f.stem: f for f in raw_files
    }

    # Sample infobox pages (up to 5000) to find unmapped fields efficiently
    sample_pages = list(infobox_pages)[:5000]
    for page_name in sample_pages:
        # Find the file
        safe_name = page_name.replace(" ", "_")
        raw_file = RAW_DIR / f"{safe_name}.json"
        if not raw_file.exists():
            continue
        try:
            data = json.loads(raw_file.read_text(encoding="utf-8"))
            html_str = data.get("html", "")
        except Exception:
            continue
        if not html_str:
            continue

        field_parser = InfoboxFieldParser()
        try:
            field_parser.feed(html_str)
        except Exception:
            continue

        for field_name, _ in field_parser.fields:
            clean = re.sub(r"<[^>]+>", "", field_name).strip().lower()
            if not clean:
                continue
            all_field_counts[clean] += 1
            if clean not in known_rel_fields and clean not in known_non_rel:
                unmapped_field_counts[clean] += 1

    stats.field_counts = all_field_counts
    stats.unmapped_field_counts = unmapped_field_counts

    write_stats(stats, STATS_FILE, elapsed_sec=elapsed)

    # --- Final summary ---
    print("\n" + "=" * 60)
    print("Wiki Infobox Parser — Complete")
    print("=" * 60)
    print(f"Pages processed:       {stats.total_pages:>8,}")
    print(f"Pages with infoboxes:  {stats.infobox_pages:>8,}")
    print(f"Pages with cite_refs:  {stats.cite_ref_pages:>8,}")
    print(f"Parse failures:        {stats.failures and len(stats.failures) or 0:>8}")
    print(f"Elapsed:               {elapsed:>7.1f}s")
    print()
    print("Entity type distribution:")
    for etype, count in sorted(stats.entity_type_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"  {etype:<30} {count:>6,}")
    print()
    print("Output files:")
    print(f"  {INFOBOX_DATA_FILE}")
    print(f"  {PAGE_INDEX_FILE}")
    print(f"  {STATS_FILE}")
    print()
    if stats.failures:
        print(f"Failures ({min(len(stats.failures), 10)} of {len(stats.failures)} shown):")
        for p, e in stats.failures[:10]:
            print(f"  {p}: {e}")
        print()


if __name__ == "__main__":
    main()
