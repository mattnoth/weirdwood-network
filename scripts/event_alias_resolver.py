#!/usr/bin/env python3
"""
event_alias_resolver.py — Deterministic event alias resolver for the Weirwood Network.

Builds a flat {alias_phrase -> canonical_slug} lookup table from three sources:
  1. working/wiki/data/event-node-aliases.json  — wiki redirect aliases (harvested S85)
  2. graph/nodes/events/*.node.md frontmatter aliases: fields
  3. Canonical name normalization of each event node's name: field

Additionally builds three fallback mechanisms (S96):
  (a) Fuzzy / substring fallback — when exact lookup misses, falls back to
      token-overlap scoring against the full slug+alias index and returns ranked
      candidates. Requires >= MIN_FUZZY_SCORE to return anything (conservative
      threshold: wrong confident match is worse than MISS).
  (b) Victim-indexing — builds alias phrases for event.death / event.execution /
      event.assassination hubs keyed on their VICTIM_IN edges. Generates phrase
      variants like "{victim}'s death", "death of {victim}", etc.
  (c) Character-name fallback — when a phrase names a character node, returns
      that character node slug as a candidate so consumers can call --neighbors
      on it to find outgoing relationship edges.

Design: reference/alias-resolver-design.md (S86)
Output: working/wiki/data/event-alias-lookup.json
        working/wiki/data/all-node-alias-lookup.json  (extended index, S96)

Usage:
    # Build/rebuild the lookup table:
    python3 scripts/event_alias_resolver.py --build

    # Look up a phrase (builds in memory, no --build needed):
    python3 scripts/event_alias_resolver.py --lookup "Ned's execution"
    python3 scripts/event_alias_resolver.py --lookup "the Red Wedding"

    # Show stats only:
    python3 scripts/event_alias_resolver.py --stats

No LLM in the loop. Ever. (design doc, Q1)
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# --- Paths ---
REPO_ROOT = Path(__file__).parent.parent
WIKI_ALIASES_FILE = REPO_ROOT / "working/wiki/data/event-node-aliases.json"
EVENT_NODES_DIR = REPO_ROOT / "graph/nodes/events"
GRAPH_NODES_DIR = REPO_ROOT / "graph/nodes"
EDGES_FILE = REPO_ROOT / "graph/edges/edges.jsonl"
OUTPUT_FILE = REPO_ROOT / "working/wiki/data/event-alias-lookup.json"
ALL_NODES_OUTPUT_FILE = REPO_ROOT / "working/wiki/data/all-node-alias-lookup.json"
WIKI_RAW_DIR = REPO_ROOT / "sources/wiki/_raw"
NODES_JSON_FILE = REPO_ROOT / "web/data/nodes.json"

# Fuzzy matching tuning
# A candidate must have at least this fraction of the query tokens present in
# the candidate's token set (Jaccard-like but asymmetric on query side).
# 0.5 means half the query words must appear in the candidate.
MIN_FUZZY_SCORE = 0.5
# Maximum number of candidates to return from fuzzy fallback
MAX_FUZZY_CANDIDATES = 5

# Node categories included in character-name fallback
CHARACTER_CATEGORIES = {"characters"}

# Event subtypes whose VICTIM_IN edges drive victim-phrase generation
DEATH_EVENT_TYPES = {"event.death", "event.execution", "event.assassination", "event.murder"}


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

def normalize(phrase: str) -> str:
    """
    Normalize a natural-language phrase to a lookup key.
    Steps:
      1. Lowercase
      2. Strip leading articles (a, an, the) and surrounding whitespace
      3. Collapse internal whitespace → single space
      4. Return the normalized string (NOT kebab-cased — lookup is by normalized phrase)

    The lookup table keys are all normalized forms of every alias. Input queries
    are normalized the same way before lookup, so "the Red Wedding", "Red Wedding",
    "red wedding" all resolve identically.
    """
    phrase = phrase.lower().strip()
    # Strip leading article
    phrase = re.sub(r'^(the|a|an)\s+', '', phrase)
    # Collapse whitespace
    phrase = re.sub(r'\s+', ' ', phrase).strip()
    return phrase


def name_to_normalized(name: str) -> str:
    """Normalize a node's canonical name: field for lookup."""
    return normalize(name)


def slug_to_normalized(slug: str) -> str:
    """Convert a kebab-case slug to a normalized phrase for lookup."""
    return normalize(slug.replace('-', ' '))


def alias_slug_to_normalized(alias: str) -> str:
    """Convert a wiki-redirect alias slug to a normalized phrase."""
    # Wiki redirect slugs use kebab-case (e.g. 'the-red-wedding', 'war-of-the-usurper')
    return normalize(alias.replace('-', ' '))


def tokenize(phrase: str) -> set[str]:
    """
    Split a normalized phrase into a set of tokens (words), excluding stop words.

    Stop words include common interrogative/auxiliary words so that "who killed X"
    and "X's death" share only the entity-name tokens and score correctly.
    """
    STOP = {
        'of', 'the', 'a', 'an', 'at', 'in', 'on', 'by', 'to', 'and', 'for', 's',
        # interrogatives / auxiliaries — stripped so "who crowned Lyanna" scores
        # on "lyanna" only, not on "who"
        'who', 'what', 'where', 'when', 'how', 'which', 'whom',
        'did', 'does', 'do', 'is', 'was', 'were', 'are', 'has', 'have', 'had',
    }
    tokens = set(re.findall(r'\w+', phrase.lower()))
    return tokens - STOP


# ---------------------------------------------------------------------------
# Source 1: wiki redirect aliases from event-node-aliases.json
# ---------------------------------------------------------------------------

def load_wiki_redirect_aliases() -> list[dict]:
    """
    Load working/wiki/data/event-node-aliases.json.
    Returns a list of {alias, canonical_slug, source, confidence} dicts.

    The harvested file maps canonical_slug -> {aliases: [...], redirect_sources: [...]}
    Both the canonical slug and every alias slug are surfaces for the same event.
    """
    if not WIKI_ALIASES_FILE.exists():
        print(f"WARNING: {WIKI_ALIASES_FILE} not found — skipping wiki redirect source",
              file=sys.stderr)
        return []

    with WIKI_ALIASES_FILE.open() as f:
        data = json.load(f)

    entries = []
    for canonical_slug, info in data.items():
        # The slug itself is a surface (e.g. 'red-wedding' → 'Red Wedding')
        entries.append({
            "alias": slug_to_normalized(canonical_slug),
            "canonical_slug": canonical_slug,
            "source": "wiki-slug-self",
            "confidence": "high",
            "raw": canonical_slug,
        })
        # The canonical_name from the wiki page title
        # Skip noise entries where the scraper concatenated infobox "Part of..." text
        canon_name = info.get("canonical_name", "")
        if canon_name:
            norm = name_to_normalized(canon_name)
            # Filter: skip if "part of" appears mid-string (wiki scraper artifact)
            if norm and "part of" not in norm:
                entries.append({
                    "alias": norm,
                    "canonical_slug": canonical_slug,
                    "source": "wiki-canonical-name",
                    "confidence": "high",
                    "raw": canon_name,
                })
        # Each redirect alias
        for alias_slug in info.get("aliases", []):
            entries.append({
                "alias": alias_slug_to_normalized(alias_slug),
                "canonical_slug": canonical_slug,
                "source": "wiki-redirect",
                "confidence": "high",
                "raw": alias_slug,
            })
    return entries


# ---------------------------------------------------------------------------
# Source 2: event node frontmatter aliases
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---', re.DOTALL)
_SLUG_RE = re.compile(r'^slug:\s*(.+)$', re.MULTILINE)
_NAME_RE = re.compile(r'^name:\s*"?(.+?)"?\s*$', re.MULTILINE)
_TYPE_RE = re.compile(r'^type:\s*(.+)$', re.MULTILINE)

# Matches the start of an aliases: field — captures inline array or empty
_ALIASES_START_RE = re.compile(r'^aliases:\s*(.*)$', re.MULTILINE)
# Matches a YAML block-sequence item: "  - value" or '  - "value"'
_ALIAS_ITEM_RE = re.compile(r'^\s+-\s+(.+)$')


def _parse_aliases_from_fm(fm: str) -> list[str]:
    """
    Parse the aliases list from a YAML frontmatter block (the text between ---).
    Handles both inline arrays and YAML block sequences:
      Inline:  aliases: ["Ned Stark", "Ned"]
      Block:   aliases:
                 - "Ned Stark"
                 - Ned

    Note: the regex `^aliases:\\s*(.*)$` with MULTILINE will greedily eat the
    newline+indentation before the first block item because \\s* matches \\n,
    so `first_line` may start with `- ` even for block sequences.

    Returns a list of alias strings (stripped of quotes).
    """
    m = _ALIASES_START_RE.search(fm)
    if not m:
        return []

    first_line = m.group(1).strip()

    # Case 1: inline array (JSON-compatible)
    if first_line.startswith('['):
        raw = first_line
        if raw in ('[]', ''):
            return []
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return [str(a) for a in parsed]
        except json.JSONDecodeError:
            pass
        # Manual fallback for inline arrays
        raw = raw.strip('[]')
        if raw:
            return [a.strip().strip('"').strip("'")
                    for a in raw.split(',') if a.strip()]
        return []

    # Case 2: block sequence item on same "line" as aliases: (due to \s* greediness)
    # OR actual block sequence with items on subsequent lines.
    # Collect ALL block-sequence items from the match position onward.
    # We re-scan from the `aliases:` keyword position in the fm text.
    # `m.start()` is where `aliases:` starts; items begin after `aliases:\n` or inline.
    aliases = []

    # If first_line is already a "- item" form, parse it
    if first_line.startswith('-'):
        item_val = re.sub(r'^-\s*', '', first_line).strip().strip('"').strip("'")
        if item_val:
            aliases.append(item_val)

    # Now scan forward from m.end() for more "  - item" lines
    start_pos = m.end()
    rest = fm[start_pos:]
    for line in rest.split('\n'):
        item_m = _ALIAS_ITEM_RE.match(line)
        if item_m:
            val = item_m.group(1).strip().strip('"').strip("'")
            if val:
                aliases.append(val)
        elif line.strip() and not line[0].isspace() and ':' in line:
            # Hit a non-indented YAML key — stop parsing aliases block
            break

    if aliases:
        return aliases

    # Case 3: empty or unrecognized
    return []


def _parse_frontmatter_aliases(content: str) -> tuple[str | None, str | None, list[str], str | None]:
    """
    Parse slug, name, aliases list, and type from a node file's YAML frontmatter.
    Returns (slug, name, aliases_list, node_type).
    """
    fm_match = _FRONTMATTER_RE.match(content)
    if not fm_match:
        return None, None, [], None

    fm = fm_match.group(1)

    slug_m = _SLUG_RE.search(fm)
    slug = slug_m.group(1).strip() if slug_m else None

    name_m = _NAME_RE.search(fm)
    name = name_m.group(1).strip().strip('"') if name_m else None

    type_m = _TYPE_RE.search(fm)
    node_type = type_m.group(1).strip() if type_m else None

    aliases = _parse_aliases_from_fm(fm)

    return slug, name, aliases, node_type


def load_node_frontmatter_aliases() -> list[dict]:
    """
    Scan graph/nodes/events/*.node.md for slug, name, and aliases fields.
    Returns entries for:
      - The node's canonical name (normalized)
      - The node's slug (normalized)
      - Each alias in the frontmatter aliases: list
    """
    if not EVENT_NODES_DIR.exists():
        print(f"WARNING: {EVENT_NODES_DIR} not found — skipping node frontmatter source",
              file=sys.stderr)
        return []

    entries = []
    for node_file in sorted(EVENT_NODES_DIR.glob("*.node.md")):
        content = node_file.read_text()
        slug, name, aliases, _ = _parse_frontmatter_aliases(content)

        if not slug:
            # Derive slug from filename
            slug = node_file.stem.replace('.node', '')

        # The slug itself as a normalized phrase
        entries.append({
            "alias": slug_to_normalized(slug),
            "canonical_slug": slug,
            "source": "node-slug",
            "confidence": "high",
            "raw": slug,
        })

        # The canonical name
        if name:
            norm = name_to_normalized(name)
            if norm:
                entries.append({
                    "alias": norm,
                    "canonical_slug": slug,
                    "source": "node-name",
                    "confidence": "high",
                    "raw": name,
                })

        # Frontmatter aliases list
        for alias_phrase in aliases:
            norm = normalize(alias_phrase)
            if norm:
                entries.append({
                    "alias": norm,
                    "canonical_slug": slug,
                    "source": "node-frontmatter-alias",
                    "confidence": "high",
                    "raw": alias_phrase,
                })

    return entries


# ---------------------------------------------------------------------------
# Source 3 (S96 new): All-node index for character-name fallback
# ---------------------------------------------------------------------------

def load_all_node_aliases() -> list[dict]:
    """
    Scan ALL graph/nodes/{category}/*.node.md directories (not just events/).
    Returns entries for slug + name + frontmatter aliases for every node, tagged
    with node_type and node_category.

    Used to power the character-name fallback: if a phrase names a character,
    return that character node slug as a candidate.
    """
    if not GRAPH_NODES_DIR.exists():
        print(f"WARNING: {GRAPH_NODES_DIR} not found", file=sys.stderr)
        return []

    entries = []
    for category_dir in sorted(GRAPH_NODES_DIR.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith('_'):
            continue
        # Skip events — already handled by load_node_frontmatter_aliases
        if category_dir.name == 'events':
            continue

        category = category_dir.name
        for node_file in sorted(category_dir.glob("*.node.md")):
            content = node_file.read_text()
            slug, name, aliases, node_type = _parse_frontmatter_aliases(content)

            if not slug:
                slug = node_file.stem.replace('.node', '')

            base = {
                "canonical_slug": slug,
                "node_category": category,
                "node_type": node_type or f"node.{category}",
                "confidence": "high",
            }

            # The slug itself
            entries.append({
                **base,
                "alias": slug_to_normalized(slug),
                "source": f"all-node-slug:{category}",
                "raw": slug,
            })

            # The canonical name
            if name:
                norm = name_to_normalized(name)
                if norm:
                    entries.append({
                        **base,
                        "alias": norm,
                        "source": f"all-node-name:{category}",
                        "raw": name,
                    })

            # Frontmatter aliases
            for alias_phrase in aliases:
                norm = normalize(alias_phrase)
                if norm:
                    entries.append({
                        **base,
                        "alias": norm,
                        "source": f"all-node-alias:{category}",
                        "raw": alias_phrase,
                    })

    return entries


# ---------------------------------------------------------------------------
# Source 5 ("the "-epithet redirect backfill): "The <Epithet>" wiki redirects
# ---------------------------------------------------------------------------

_REDIRECT_TARGET_RE = re.compile(r'redirectText.*?title="([^"]+)"', re.DOTALL)


def _unescape_html_entities(text: str) -> str:
    return (
        text.replace("&#039;", "'")
        .replace("&amp;", "&")
        .replace("&quot;", '"')
    )


def _kebab_slug_from_title(title: str) -> str:
    """
    Kebab-case a wiki page title the same way the project's node slugs are
    minted (mirrors wiki-event-alias-harvester.py::slug_from_page_title).
    """
    slug = title.lower()
    slug = re.sub(r"[''']", "", slug)
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug


def _extract_redirect_target(html: str) -> str | None:
    """Return the redirect TARGET page title, or None if not a redirect page."""
    if "redirectText" not in html and "redirectMsg" not in html:
        return None
    m = _REDIRECT_TARGET_RE.search(html)
    if not m:
        return None
    return _unescape_html_entities(m.group(1))


def load_the_redirect_aliases(
    all_node_slugs: set[str] | None = None,
    phrase_to_nodes: dict[str, list[dict]] | None = None,
) -> list[dict]:
    """
    Harvest "The <Epithet>"-titled wiki redirect pages from sources/wiki/_raw/
    and resolve each to a node slug, closing the "0 phrases start with 'the '"
    alias gap (backfill-epithet-aliases.py, working/graph-cleanup/epithet-backfill-report.md).

    For every "The_*.json" page in the local wiki cache that is a genuine
    MediaWiki redirect (most are; ~121/792 are real content pages and are
    skipped), resolves the redirect TARGET title to a node slug:
      a. kebab-slug(target title) is itself a node slug in web/data/nodes.json, OR
      b. the normalized target phrase already resolves in the all-node index
         (transitively resolves chains like "The Hound" -> "Hound" -> sandor-clegane)
    Unresolved targets are skipped (no guessing).

    Returns entries in the same shape as the other all-node sources:
      {alias, canonical_slug, node_category, node_type, source, raw}

    all_node_slugs / phrase_to_nodes may be passed in to avoid re-reading the
    same files this function would otherwise load itself (used by
    build_and_save(), which already has both in hand).
    """
    if not WIKI_RAW_DIR.exists():
        print(f"WARNING: {WIKI_RAW_DIR} not found — skipping the-redirect source",
              file=sys.stderr)
        return []

    if all_node_slugs is None:
        if not NODES_JSON_FILE.exists():
            print(f"WARNING: {NODES_JSON_FILE} not found — skipping the-redirect source",
                  file=sys.stderr)
            return []
        with NODES_JSON_FILE.open() as f:
            all_node_slugs = set(json.load(f).keys())

    if phrase_to_nodes is None:
        phrase_to_nodes = {}
        if ALL_NODES_OUTPUT_FILE.exists():
            with ALL_NODES_OUTPUT_FILE.open() as f:
                phrase_to_nodes = json.load(f).get("phrase_to_nodes", {})

    # slug -> {node_category, node_type} lookup, built from whatever
    # phrase_to_nodes candidates are available, for annotating direct hits.
    node_meta_by_slug: dict[str, dict] = {}
    for candidates in phrase_to_nodes.values():
        for c in candidates:
            s = c.get("canonical_slug")
            if s and s not in node_meta_by_slug:
                node_meta_by_slug[s] = {
                    "node_category": c.get("node_category", ""),
                    "node_type": c.get("node_type", ""),
                }

    entries: list[dict] = []

    for path in sorted(WIKI_RAW_DIR.glob("The_*.json")):
        try:
            with path.open() as f:
                d = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        page_title = d.get("page", path.stem.replace("_", " "))
        html = d.get("html", "")

        target_title = _extract_redirect_target(html)
        if target_title is None:
            continue  # not a redirect — a real content page, out of scope

        resolved_slugs: list[str] = []

        direct_slug = _kebab_slug_from_title(target_title)
        if direct_slug in all_node_slugs:
            resolved_slugs = [direct_slug]
        else:
            target_phrase = name_to_normalized(target_title)
            candidates = phrase_to_nodes.get(target_phrase, [])
            if candidates:
                resolved_slugs = [c["canonical_slug"] for c in candidates]

        if not resolved_slugs:
            continue  # unresolved — skip, don't guess

        redirect_phrase = normalize(page_title)
        if not redirect_phrase:
            continue

        for slug in resolved_slugs:
            meta = node_meta_by_slug.get(slug, {})
            entries.append({
                "alias": redirect_phrase,
                "canonical_slug": slug,
                "node_category": meta.get("node_category", ""),
                "node_type": meta.get("node_type", ""),
                "source": "wiki-the-redirect",
                "raw": page_title,
            })

    return entries


# ---------------------------------------------------------------------------
# Source 4 (S96 new): Victim-phrase generation for death/execution hubs
# ---------------------------------------------------------------------------

def _victim_phrases(victim_display: str) -> list[str]:
    """
    Generate natural-language phrases for a victim name:
      "{victim} death"
      "{victim}'s death"
      "death of {victim}"
      "{victim} execution"
      "{victim}'s execution"
      "execution of {victim}"
      "{victim} killed"
      "{victim} is killed"
      "{victim} murdered"
      "killing of {victim}"
      "murder of {victim}"
      "assassination of {victim}"
    Returns all as normalized strings.
    """
    v = victim_display.strip()
    v_norm = normalize(v)  # normalized victim name (no leading article)
    # Also build a version without leading "Lord", "Ser", etc. for matching
    # We generate from the raw name, normalization strips leading "the/a/an"
    phrases = [
        f"{v_norm} death",
        f"{v_norm}'s death",
        f"death of {v_norm}",
        f"{v_norm} execution",
        f"{v_norm}'s execution",
        f"execution of {v_norm}",
        f"{v_norm} killed",
        f"{v_norm} is killed",
        f"{v_norm} murdered",
        f"killing of {v_norm}",
        f"murder of {v_norm}",
        f"assassination of {v_norm}",
        f"{v_norm} assassinated",
        f"who killed {v_norm}",
        f"who murdered {v_norm}",
    ]
    # normalize each phrase (strips leading 'the/a/an' again; collapses spaces)
    return [normalize(p) for p in phrases if normalize(p)]


# Keywords in an event slug/name that confirm the event is about the victim's death.
# We only generate victim-death alias phrases when BOTH the victim's name tokens
# AND at least one death keyword appear in the event's slug+name.
#
# Critically: "kill" (bare infinitive) is EXCLUDED because it appears in phrases
# like "theon-urges-robb-to-kill-jaime" (kill Jaime, not Robb). We require the
# past tense ("killed") or noun forms ("death", "execution", etc.) to avoid
# false-positive matches where a third party is the actual target.
_DEATH_KEYWORDS = frozenset({
    "killed",                       # past tense — "robb-is-killed"
    "death", "dead",                # noun/adj
    "execution", "executed",        # for execution hubs
    "murdered", "murder",           # murder events
    "assassination", "assassinated",
    "beheaded",
    "slain",
    "dies", "died",
})


def _event_is_primary_death_of_victim(
    victim_slug: str,
    event_slug: str,
    event_node_names: dict[str, str],
) -> bool:
    """
    Return True only when:
      1. The event node type is a death type (checked by caller), AND
      2. The event slug or canonical name contains the victim's first name or
         a meaningful subset of the victim's slug tokens, AND
      3. The event slug or canonical name contains a death keyword.

    This prevents generating "Robb Stark's death" → theon-urges-robb-to-kill-jaime
    (Robb appears as VICTIM_IN there but that hub is an urging event, even if
    mis-typed as event.death; its slug/name doesn't contain a death keyword
    with Robb as the subject).

    Conservative: false negatives (don't generate a phrase) are acceptable;
    false positives (generate conflicting phrases) break resolution.
    """
    victim_tokens = set(victim_slug.split("-"))
    # Build a combined text from the event slug and its name (if any)
    event_name = event_node_names.get(event_slug, "")
    combined = f"{event_slug} {event_name}".lower()
    combined_tokens = set(re.findall(r'\w+', combined))

    # Check death keyword present
    has_death_keyword = bool(combined_tokens & _DEATH_KEYWORDS)
    if not has_death_keyword:
        return False

    # Check at least one victim token (min 4 chars to skip noise like "of", "the")
    meaningful_victim_tokens = {t for t in victim_tokens if len(t) >= 4}
    has_victim_token = bool(meaningful_victim_tokens & combined_tokens)
    return has_victim_token


def _load_character_alias_map() -> dict[str, list[str]]:
    """
    Build a map {character_slug -> [alias1, alias2, ...]} from character node
    frontmatter. Used to augment victim-phrase generation with common aliases
    (e.g. eddard-stark → ["Ned Stark", "Ned", ...]).

    Returns empty dict if characters directory doesn't exist.
    """
    char_dir = GRAPH_NODES_DIR / "characters"
    if not char_dir.exists():
        return {}
    alias_map: dict[str, list[str]] = {}
    for node_file in char_dir.glob("*.node.md"):
        content = node_file.read_text()
        slug, name, aliases, _ = _parse_frontmatter_aliases(content)
        if not slug:
            slug = node_file.stem.replace('.node', '')
        all_names = []
        if name:
            all_names.append(name)
        all_names.extend(aliases)
        if all_names:
            alias_map[slug] = all_names
    return alias_map


def load_victim_aliases(
    event_node_types: dict[str, str],
    event_node_names: dict[str, str] | None = None,
    character_alias_map: dict[str, list[str]] | None = None,
) -> list[dict]:
    """
    Read graph/edges/edges.jsonl and collect VICTIM_IN edges where the target
    event node is a death/execution/assassination type AND the event hub's slug
    or name confirms the victim is the subject of the death (not just a bystander
    VICTIM_IN on a mis-typed hub).

    Generates victim phrases for:
      - The participant_name in the edge (e.g. "Eddard Stark")
      - All aliases of the victim character node (e.g. "Ned Stark", "Ned")

    event_node_types: {slug -> node_type} for all event nodes.
    event_node_names: {slug -> canonical name} for all event nodes (optional).
    character_alias_map: {char_slug -> [names/aliases]} (optional).

    Returns alias entries: {alias (normalized victim phrase), canonical_slug
    (the event hub), source: 'victim-index', node_type, ...}
    """
    if event_node_names is None:
        event_node_names = {}
    if character_alias_map is None:
        character_alias_map = {}

    if not EDGES_FILE.exists():
        print(f"WARNING: {EDGES_FILE} not found — skipping victim-index source",
              file=sys.stderr)
        return []

    entries = []
    seen: set[tuple[str, str]] = set()  # (phrase, slug) — avoid duplicates

    with EDGES_FILE.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                edge = json.loads(line)
            except json.JSONDecodeError:
                continue

            if edge.get("edge_type") != "VICTIM_IN":
                continue

            victim_slug = edge.get("source_slug", "")
            event_slug = edge.get("target_slug", "")
            if not victim_slug or not event_slug:
                continue

            # Only for death/execution/assassination event types
            event_type = event_node_types.get(event_slug, "")
            if event_type not in DEATH_EVENT_TYPES:
                continue

            # Confirm this event is specifically about this victim's death
            # (not just a hub where they appear as a tangential victim)
            if not _event_is_primary_death_of_victim(
                victim_slug, event_slug, event_node_names
            ):
                continue

            # Collect all names to generate phrases for:
            # 1) participant_name from the edge (or slug-derived)
            # 2) canonical name + aliases from the character node (if known)
            edge_name = edge.get("participant_name") or victim_slug.replace("-", " ").title()
            display_names = [edge_name]
            char_names = character_alias_map.get(victim_slug, [])
            for cn in char_names:
                if cn not in display_names:
                    display_names.append(cn)

            for victim_display in display_names:
                for phrase in _victim_phrases(victim_display):
                    key = (phrase, event_slug)
                    if key in seen:
                        continue
                    seen.add(key)
                    entries.append({
                        "alias": phrase,
                        "canonical_slug": event_slug,
                        "source": "victim-index",
                        "confidence": "high",
                        "raw": f"{victim_display} (VICTIM_IN → {event_slug})",
                        "node_type": event_type,
                    })

    return entries


def _collect_event_node_metadata() -> tuple[dict[str, str], dict[str, str]]:
    """
    Scan event nodes and return:
      ({slug -> type}, {slug -> canonical_name})
    """
    if not EVENT_NODES_DIR.exists():
        return {}, {}
    types: dict[str, str] = {}
    names: dict[str, str] = {}
    for node_file in EVENT_NODES_DIR.glob("*.node.md"):
        content = node_file.read_text()
        slug, name, _, node_type = _parse_frontmatter_aliases(content)
        if not slug:
            slug = node_file.stem.replace('.node', '')
        if node_type:
            types[slug] = node_type
        if name:
            names[slug] = name
    return types, names


# ---------------------------------------------------------------------------
# Merge + collision handling
# ---------------------------------------------------------------------------

PRIORITY_ORDER = [
    "node-name",           # canonical name from node = highest trust
    "node-slug",           # slug form of canonical node
    "node-frontmatter-alias",  # author-curated frontmatter aliases
    "victim-index",        # generated victim-phrase aliases (S96)
    "wiki-canonical-name", # wiki page title
    "wiki-slug-self",      # wiki slug
    "wiki-redirect",       # wiki redirect chains
]


def build_lookup_table(
    entries: list[dict],
) -> tuple[dict[str, str], dict[str, list[dict]], dict]:
    """
    Merge all alias entries into a single {normalized_phrase -> canonical_slug} dict.

    Collision handling:
      - If the same normalized phrase maps to >1 slug, flag as AMBIGUOUS and exclude
        from the lookup. Neither slug is returned for an ambiguous phrase.
      - Priority order (see PRIORITY_ORDER) breaks ties when two entries from
        different sources differ — higher-priority source wins.

    Returns:
      lookup: {normalized_phrase -> canonical_slug}  (unambiguous only)
      collisions: {normalized_phrase -> [list of conflicting entries]}
      stats: summary dict
    """
    # Group all entries by normalized alias phrase
    by_phrase: dict[str, list[dict]] = {}
    for e in entries:
        phrase = e["alias"]
        if not phrase:
            continue
        by_phrase.setdefault(phrase, []).append(e)

    lookup = {}
    collisions = {}

    for phrase, candidates in by_phrase.items():
        # Collect unique target slugs
        slugs = {c["canonical_slug"] for c in candidates}

        if len(slugs) == 1:
            # Unambiguous
            lookup[phrase] = next(iter(slugs))
        else:
            # Multiple slugs — check if a priority-ordered source breaks the tie
            # Build slug -> best_priority_rank
            slug_rank: dict[str, int] = {}
            for c in candidates:
                src = c["source"]
                # Strip the "all-node-*:category" prefix for priority ordering
                src_base = src.split(":")[0] if ":" in src else src
                rank = PRIORITY_ORDER.index(src_base) if src_base in PRIORITY_ORDER else len(PRIORITY_ORDER)
                existing = slug_rank.get(c["canonical_slug"], len(PRIORITY_ORDER) + 1)
                slug_rank[c["canonical_slug"]] = min(existing, rank)

            # Find the slug with the best (lowest) rank
            best_rank = min(slug_rank.values())
            best_slugs = [s for s, r in slug_rank.items() if r == best_rank]

            if len(best_slugs) == 1:
                # Single winner by priority
                lookup[phrase] = best_slugs[0]
            else:
                # True ambiguity — exclude, record collision
                collisions[phrase] = candidates

    stats = {
        "total_entries_scanned": len(entries),
        "unique_phrases": len(by_phrase),
        "unambiguous_lookups": len(lookup),
        "ambiguous_collisions": len(collisions),
    }
    return lookup, collisions, stats


# ---------------------------------------------------------------------------
# Build and persist
# ---------------------------------------------------------------------------

def build_and_save(verbose: bool = True) -> dict:
    """
    Full build: harvest all sources, merge, save to OUTPUT_FILE.
    Also builds the all-node index to ALL_NODES_OUTPUT_FILE.
    Returns the stats dict.
    """
    if verbose:
        print("Loading wiki redirect aliases...")
    wiki_entries = load_wiki_redirect_aliases()
    if verbose:
        print(f"  {len(wiki_entries)} entries from wiki-node-aliases.json")

    if verbose:
        print("Loading event node frontmatter aliases...")
    node_entries = load_node_frontmatter_aliases()
    if verbose:
        print(f"  {len(node_entries)} entries from {EVENT_NODES_DIR.name}/")

    if verbose:
        print("Building victim-phrase aliases...")
    event_types, event_names = _collect_event_node_metadata()
    char_alias_map = _load_character_alias_map()
    victim_entries = load_victim_aliases(event_types, event_names, char_alias_map)
    if verbose:
        print(f"  (loaded {len(char_alias_map)} character alias entries)")
    if verbose:
        print(f"  {len(victim_entries)} entries from VICTIM_IN edges")

    all_entries = wiki_entries + node_entries + victim_entries

    if verbose:
        print("Merging and deduplicating...")
    lookup, collisions, stats = build_lookup_table(all_entries)

    # Count source breakdown
    source_counts: dict[str, int] = {}
    for e in all_entries:
        source_counts[e["source"]] = source_counts.get(e["source"], 0) + 1

    output = {
        "version": "v2",
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "stats": {
            **stats,
            "source_breakdown": source_counts,
        },
        "alias_to_canonical": lookup,
        "ambiguous_collisions": collisions,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w") as f:
        json.dump(output, f, indent=2, sort_keys=True)

    if verbose:
        print(f"\nSaved to: {OUTPUT_FILE}")
        print(f"  Unique phrases indexed: {stats['unique_phrases']}")
        print(f"  Unambiguous lookups:    {stats['unambiguous_lookups']}")
        print(f"  Ambiguous collisions:   {stats['ambiguous_collisions']}")
        print(f"\nSource breakdown:")
        for src, count in sorted(source_counts.items()):
            print(f"  {src:35s}: {count:5d}")

    # --- Build all-node index ---
    if verbose:
        print("\nBuilding all-node index (for character-name fallback)...")
    all_node_entries = load_all_node_aliases()
    # Also include event entries in the all-node index
    all_node_entries_with_events = all_node_entries + node_entries
    _, _, all_stats = build_lookup_table(all_node_entries_with_events)

    # Build a simple {normalized -> [{slug, node_category, node_type, source}]} map
    # (not collapsed to single winner — we want all candidates for character lookups)
    all_node_by_phrase: dict[str, list[dict]] = {}
    for e in all_node_entries_with_events:
        phrase = e["alias"]
        if not phrase:
            continue
        entry = {
            "canonical_slug": e["canonical_slug"],
            "node_category": e.get("node_category", "events"),
            "node_type": e.get("node_type", ""),
            "source": e["source"],
        }
        all_node_by_phrase.setdefault(phrase, []).append(entry)

    # Deduplicate within each phrase's list by slug
    all_node_collapsed: dict[str, list[dict]] = {}
    for phrase, candidates in all_node_by_phrase.items():
        seen_slugs: set[str] = set()
        deduped = []
        for c in candidates:
            if c["canonical_slug"] not in seen_slugs:
                seen_slugs.add(c["canonical_slug"])
                deduped.append(c)
        all_node_collapsed[phrase] = deduped

    # --- Source 5: "The <Epithet>" wiki-redirect backfill (additive) ---
    # Resolves against the all-node index just built above (in-memory, not the
    # on-disk file — this makes the resolution transitive within a single build:
    # e.g. "The Hound" -> "Hound" -> sandor-clegane, where "hound" -> sandor-clegane
    # was itself just computed a few lines up).
    if verbose:
        print("\nLoading 'The <Epithet>' wiki-redirect aliases...")
    node_slugs = set()
    if NODES_JSON_FILE.exists():
        with NODES_JSON_FILE.open() as f:
            node_slugs = set(json.load(f).keys())
    else:
        print(f"WARNING: {NODES_JSON_FILE} not found — skipping the-redirect source",
              file=sys.stderr)

    the_redirect_entries = load_the_redirect_aliases(
        all_node_slugs=node_slugs,
        phrase_to_nodes=all_node_collapsed,
    )
    if verbose:
        print(f"  {len(the_redirect_entries)} entries from sources/wiki/_raw/ 'The_*' redirects")

    new_phrase_count = 0
    for e in the_redirect_entries:
        phrase = e["alias"]
        slug = e["canonical_slug"]
        existing = all_node_collapsed.setdefault(phrase, [])
        if phrase not in all_node_by_phrase:
            new_phrase_count += 1
        if not any(c["canonical_slug"] == slug for c in existing):
            existing.append({
                "canonical_slug": slug,
                "node_category": e.get("node_category", ""),
                "node_type": e.get("node_type", ""),
                "source": e["source"],
            })
    if verbose:
        print(f"  {new_phrase_count} NEW phrases added to the all-node index")

    all_node_output = {
        "version": "v1",
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "stats": {
            "total_node_entries": len(all_node_entries_with_events) + len(the_redirect_entries),
            "unique_phrases": len(all_node_collapsed),
        },
        "phrase_to_nodes": all_node_collapsed,
    }

    with ALL_NODES_OUTPUT_FILE.open("w") as f:
        json.dump(all_node_output, f, indent=2, sort_keys=True)

    if verbose:
        print(f"Saved all-node index to: {ALL_NODES_OUTPUT_FILE}")
        print(f"  Unique phrases in all-node index: {len(all_node_collapsed)}")

    return stats


# ---------------------------------------------------------------------------
# Lookup (in-memory)
# ---------------------------------------------------------------------------

def load_lookup() -> dict[str, str]:
    """Load the pre-built lookup table from OUTPUT_FILE. Builds if missing."""
    if not OUTPUT_FILE.exists():
        print("Lookup table not found — building now...", file=sys.stderr)
        build_and_save(verbose=False)

    with OUTPUT_FILE.open() as f:
        data = json.load(f)
    return data.get("alias_to_canonical", {})


def load_all_node_index() -> dict[str, list[dict]]:
    """Load the all-node index from ALL_NODES_OUTPUT_FILE. Builds if missing."""
    if not ALL_NODES_OUTPUT_FILE.exists():
        print("All-node index not found — building now...", file=sys.stderr)
        build_and_save(verbose=False)

    with ALL_NODES_OUTPUT_FILE.open() as f:
        data = json.load(f)
    return data.get("phrase_to_nodes", {})


def _fuzzy_candidates(
    norm_query: str,
    lookup: dict[str, str],
    all_node_index: dict[str, list[dict]] | None = None,
    max_results: int = MAX_FUZZY_CANDIDATES,
) -> list[dict]:
    """
    (a) Fuzzy / token-overlap fallback.

    Score each candidate key in the lookup (and all_node_index if provided)
    against the query using an asymmetric token-overlap metric:

        score = |query_tokens ∩ candidate_tokens| / |query_tokens|

    This measures what fraction of the QUERY's meaningful words appear in the
    candidate. We require score >= MIN_FUZZY_SCORE.

    Returns a list of {slug, score, match_type: 'fuzzy', node_category, ...}
    sorted by score descending, up to max_results items.
    """
    query_tokens = tokenize(norm_query)
    if not query_tokens:
        return []

    scored: dict[str, float] = {}  # slug -> best score

    def _score_candidate(phrase: str, slug: str) -> None:
        cand_tokens = tokenize(phrase)
        if not cand_tokens:
            return
        overlap = len(query_tokens & cand_tokens)
        score = overlap / len(query_tokens)
        if score >= MIN_FUZZY_SCORE:
            # Bonus: if the query tokens also appear in the slug itself, boost
            # slightly. This ranks slug-named entities above nickname-matched ones
            # when both have equal phrase scores (e.g. lyanna-stark beats
            # balon-greyjoy when the query contains "lyanna").
            slug_tokens = tokenize(slug.replace('-', ' '))
            slug_overlap = len(query_tokens & slug_tokens)
            if slug_overlap > 0:
                score = min(1.0, score + 0.05 * slug_overlap)
            existing = scored.get(slug, 0.0)
            if score > existing:
                scored[slug] = score

    # Score event-alias lookup
    for phrase, slug in lookup.items():
        _score_candidate(phrase, slug)

    # Score all-node index (if provided)
    if all_node_index:
        for phrase, node_list in all_node_index.items():
            for node in node_list:
                _score_candidate(phrase, node["canonical_slug"])

    if not scored:
        return []

    # Sort by score desc
    ranked = sorted(scored.items(), key=lambda x: -x[1])[:max_results]

    # Annotate with node_category and node_type where available
    slug_meta: dict[str, dict] = {}
    if all_node_index:
        for phrase, node_list in all_node_index.items():
            for node in node_list:
                sl = node["canonical_slug"]
                if sl not in slug_meta:
                    slug_meta[sl] = {
                        "node_category": node.get("node_category", ""),
                        "node_type": node.get("node_type", ""),
                    }

    results = []
    for slug, score in ranked:
        meta = slug_meta.get(slug, {})
        results.append({
            "slug": slug,
            "score": round(score, 3),
            "match_type": "fuzzy",
            "node_category": meta.get("node_category", "events"),
            "node_type": meta.get("node_type", ""),
        })
    return results


def _character_candidates(
    norm_query: str,
    all_node_index: dict[str, list[dict]],
) -> list[dict]:
    """
    (c) Character-name fallback.

    If the normalized query matches any phrase in the all-node index that maps
    to a character node, return those character slugs as candidates.

    This is a DIRECT (not fuzzy) lookup in the all-node index, filtered to
    character category results only. It fires before the fuzzy pass.

    Returns list of {slug, match_type: 'character-node', node_category, node_type}.
    """
    candidates = all_node_index.get(norm_query, [])
    char_candidates = [
        {
            "slug": c["canonical_slug"],
            "match_type": "character-node",
            "node_category": c.get("node_category", ""),
            "node_type": c.get("node_type", ""),
            "score": 1.0,
        }
        for c in candidates
        if c.get("node_category") in CHARACTER_CATEGORIES
    ]
    return char_candidates


def resolve(
    phrase: str,
    lookup: dict[str, str] | None = None,
    all_node_index: dict[str, list[dict]] | None = None,
) -> tuple[str | None, str, list[dict]]:
    """
    Resolve a natural-language phrase to a canonical slug.

    Resolution order:
      1. Exact normalized match in event alias lookup → HIT (event)
      2. Exact match in all-node index for a character → HIT (character-node)
      3. Fuzzy/token-overlap fallback against event lookup + all-node index

    Returns (slug, status, candidates) where:
      slug:   the top resolved slug, or None
      status: 'hit'        — unambiguous exact match
              'hit-character' — exact match to a character node (phrase = full character name)
              'candidates' — fuzzy or ambiguous match; see candidates list
              'ambiguous'  — phrase is in the collision table
              'miss'       — no match at any level
      candidates: list of {slug, score, match_type, node_category, node_type}
                  (populated for 'candidates' status; may also be populated for
                  'hit' to show alternates when scores are close)

    BACKWARD COMPATIBILITY: callers that only unpack (slug, status) still work.
    The third element is new; existing code using `slug, status = resolve(...)` will
    raise ValueError — update callers to use `slug, status, candidates = resolve(...)`.
    """
    if lookup is None:
        lookup = load_lookup()
    if all_node_index is None:
        all_node_index = load_all_node_index()

    norm = normalize(phrase)

    # 1. Exact event alias lookup
    slug = lookup.get(norm)
    if slug is not None:
        return slug, "hit", []

    # Check collisions file
    if OUTPUT_FILE.exists():
        with OUTPUT_FILE.open() as f:
            data = json.load(f)
        if norm in data.get("ambiguous_collisions", {}):
            return None, "ambiguous", []

    # 2. Character-name exact lookup
    char_candidates = _character_candidates(norm, all_node_index)
    if char_candidates:
        top = char_candidates[0]
        return top["slug"], "hit-character", char_candidates

    # 3. Fuzzy fallback
    fuzzy = _fuzzy_candidates(norm, lookup, all_node_index)
    if fuzzy:
        top_score = fuzzy[0]["score"]
        # If top score is decisive (>= 0.75) and at least 0.2 better than #2,
        # treat as a single confident candidate. Otherwise return all candidates.
        if (top_score >= 0.75
                and (len(fuzzy) == 1 or top_score - fuzzy[1]["score"] >= 0.2)):
            return fuzzy[0]["slug"], "candidates", fuzzy
        else:
            return None, "candidates", fuzzy

    return None, "miss", []


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Deterministic event alias resolver for the Weirwood Network."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--build",
        action="store_true",
        help="Build (or rebuild) the alias lookup table.",
    )
    group.add_argument(
        "--lookup",
        metavar="PHRASE",
        help="Resolve a phrase to its canonical event slug.",
    )
    group.add_argument(
        "--stats",
        action="store_true",
        help="Print statistics from the existing lookup table.",
    )
    args = parser.parse_args()

    if args.build:
        build_and_save(verbose=True)

    elif args.lookup:
        lookup = load_lookup()
        all_node_index = load_all_node_index()
        phrase = args.lookup
        slug, status, candidates = resolve(phrase, lookup, all_node_index)
        norm = normalize(phrase)
        print(f"Input:      {phrase!r}")
        print(f"Normalized: {norm!r}")
        if status == "hit":
            print(f"Result:     {slug}")
            print(f"Status:     HIT")
        elif status == "hit-character":
            print(f"Result:     {slug}")
            print(f"Status:     HIT-CHARACTER (character node; use --neighbors {slug} to find edges)")
            if len(candidates) > 1:
                print(f"Alternates: {', '.join(c['slug'] for c in candidates[1:])}")
        elif status == "ambiguous":
            print(f"Result:     (ambiguous — multiple slugs match this phrase)")
            print(f"Status:     AMBIGUOUS")
        elif status == "candidates":
            if slug:
                print(f"Result:     {slug}  [top candidate, score={candidates[0]['score']:.2f}]")
                print(f"Status:     CANDIDATES (fuzzy match; verify before use)")
            else:
                print(f"Result:     (no confident single match)")
                print(f"Status:     CANDIDATES (fuzzy; multiple close matches)")
            if candidates:
                print(f"Ranked candidates:")
                for i, c in enumerate(candidates, 1):
                    cat = c.get('node_category', '')
                    typ = c.get('node_type', '')
                    label = f"{cat}/{typ}" if typ else cat
                    print(f"  {i}. {c['slug']}  score={c['score']:.2f}  [{label}]  match={c['match_type']}")
        else:
            print(f"Result:     (no match)")
            print(f"Status:     MISS")

    elif args.stats:
        if not OUTPUT_FILE.exists():
            print(f"No lookup table found at {OUTPUT_FILE}")
            print("Run with --build first.")
            sys.exit(1)
        with OUTPUT_FILE.open() as f:
            data = json.load(f)
        stats = data.get("stats", {})
        print(f"Lookup table: {OUTPUT_FILE}")
        print(f"Computed at:  {data.get('computed_at', 'unknown')}")
        print(f"Version:      {data.get('version', 'unknown')}")
        print()
        for k, v in stats.items():
            if isinstance(v, dict):
                print(f"{k}:")
                for sk, sv in sorted(v.items()):
                    print(f"  {sk:35s}: {sv:5}")
            else:
                print(f"{k}: {v}")


if __name__ == "__main__":
    main()
