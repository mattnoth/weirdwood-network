#!/usr/bin/env python3
"""build_alias_table.py — Build the alias lookup tables consumed by resolve.py.

Absorbs the `--build` half of scripts/event_alias_resolver.py: harvests alias
entries from five sources (wiki redirects, event node frontmatter, all-node
frontmatter, victim-phrase generation off VICTIM_IN edges, "The_*" wiki-
redirect epithet backfill), merges them with priority-ordered collision
handling, and writes the SAME two output files at the SAME paths:

  working/wiki/data/event-alias-lookup.json
  working/wiki/data/all-node-alias-lookup.json

IMPORTANT — frontmatter parsing for THIS module: the alias-table build uses
the resolver's OWN regex-based frontmatter parser (`_parse_frontmatter_
aliases` / `_parse_aliases_from_fm` below), NOT weirwood_query.load's
pyyaml-with-fallback parser. This is deliberate, not an oversight: 5 node
files carry malformed doubled-quote aliases (design.md G18 — e.g.
`aliases: ["Blood"]` where the source alias text itself contains literal
quote characters); the two parsers extract different literal alias strings
for those 5 files ("blood" vs "\"blood\"" after normalization), which would
change the alias-table's *content*, not just its interface. The mission is
ZERO BEHAVIOR CHANGE for this build output, so this module intentionally
duplicates the regex parser rather than delegating to load.parse_frontmatter.
Elsewhere in the package (traverse.py, report.py, cli.py) the pyyaml-with-
fallback parser in load.py is used, per the step-1 design decision.

Path resolution: repo root derived from `Path(__file__).resolve()` parents,
matching weirwood_query.load's convention.

No LLM in the loop. Ever.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# --- Paths (UNCHANGED from scripts/event_alias_resolver.py) ---
_THIS_FILE = Path(__file__).resolve()
# <repo>/graph/query/build/build_alias_table.py -> parents[0]=build,
# [1]=query, [2]=graph, [3]=<repo>
REPO_ROOT = _THIS_FILE.parents[3]

WIKI_ALIASES_FILE = REPO_ROOT / "working/wiki/data/event-node-aliases.json"
EVENT_NODES_DIR = REPO_ROOT / "graph/nodes/events"
GRAPH_NODES_DIR = REPO_ROOT / "graph/nodes"
EDGES_FILE = REPO_ROOT / "graph/edges/edges.jsonl"
OUTPUT_FILE = REPO_ROOT / "working/wiki/data/event-alias-lookup.json"
ALL_NODES_OUTPUT_FILE = REPO_ROOT / "working/wiki/data/all-node-alias-lookup.json"
WIKI_RAW_DIR = REPO_ROOT / "sources/wiki/_raw"
NODES_JSON_FILE = REPO_ROOT / "web/data/nodes.json"

MIN_FUZZY_SCORE = 0.5
MAX_FUZZY_CANDIDATES = 5

CHARACTER_CATEGORIES = {"characters"}
DEATH_EVENT_TYPES = {"event.death", "event.execution", "event.assassination", "event.murder"}


# ---------------------------------------------------------------------------
# Normalization — delegate to the single normalizer (weirwood_query.normalize)
# ---------------------------------------------------------------------------

from weirwood_query.normalize import (  # noqa: E402
    alias_slug_to_normalized,
    name_to_normalized,
    normalize,
    slug_to_normalized,
    tokenize,
)


# ---------------------------------------------------------------------------
# Source 1: wiki redirect aliases from event-node-aliases.json
# ---------------------------------------------------------------------------

def load_wiki_redirect_aliases() -> list[dict]:
    """Load working/wiki/data/event-node-aliases.json. Absorbed verbatim."""
    if not WIKI_ALIASES_FILE.exists():
        print(f"WARNING: {WIKI_ALIASES_FILE} not found — skipping wiki redirect source",
              file=sys.stderr)
        return []

    with WIKI_ALIASES_FILE.open() as f:
        data = json.load(f)

    entries = []
    for canonical_slug, info in data.items():
        entries.append({
            "alias": slug_to_normalized(canonical_slug),
            "canonical_slug": canonical_slug,
            "source": "wiki-slug-self",
            "confidence": "high",
            "raw": canonical_slug,
        })
        canon_name = info.get("canonical_name", "")
        if canon_name:
            norm = name_to_normalized(canon_name)
            if norm and "part of" not in norm:
                entries.append({
                    "alias": norm,
                    "canonical_slug": canonical_slug,
                    "source": "wiki-canonical-name",
                    "confidence": "high",
                    "raw": canon_name,
                })
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
#
# Regex-based parser DELIBERATELY duplicated from scripts/event_alias_
# resolver.py rather than reusing weirwood_query.load.parse_frontmatter — see
# module docstring (G18 doubled-quote files parse differently under pyyaml).
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---', re.DOTALL)
_SLUG_RE = re.compile(r'^slug:\s*(.+)$', re.MULTILINE)
_NAME_RE = re.compile(r'^name:\s*"?(.+?)"?\s*$', re.MULTILINE)
_TYPE_RE = re.compile(r'^type:\s*(.+)$', re.MULTILINE)

_ALIASES_START_RE = re.compile(r'^aliases:\s*(.*)$', re.MULTILINE)
_ALIAS_ITEM_RE = re.compile(r'^\s+-\s+(.+)$')


def _parse_aliases_from_fm(fm: str) -> list[str]:
    """Parse the aliases list from a YAML frontmatter block. Absorbed
    verbatim from scripts/event_alias_resolver.py (regex-based, NOT pyyaml —
    see module docstring)."""
    m = _ALIASES_START_RE.search(fm)
    if not m:
        return []

    first_line = m.group(1).strip()

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
        raw = raw.strip('[]')
        if raw:
            return [a.strip().strip('"').strip("'")
                    for a in raw.split(',') if a.strip()]
        return []

    aliases = []

    if first_line.startswith('-'):
        item_val = re.sub(r'^-\s*', '', first_line).strip().strip('"').strip("'")
        if item_val:
            aliases.append(item_val)

    start_pos = m.end()
    rest = fm[start_pos:]
    for line in rest.split('\n'):
        item_m = _ALIAS_ITEM_RE.match(line)
        if item_m:
            val = item_m.group(1).strip().strip('"').strip("'")
            if val:
                aliases.append(val)
        elif line.strip() and not line[0].isspace() and ':' in line:
            break

    if aliases:
        return aliases

    return []


def _parse_frontmatter_aliases(content: str) -> tuple[str | None, str | None, list[str], str | None]:
    """Parse slug, name, aliases list, and type from a node file's YAML
    frontmatter. Absorbed verbatim from scripts/event_alias_resolver.py."""
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
    """Scan graph/nodes/events/*.node.md for slug, name, and aliases fields."""
    if not EVENT_NODES_DIR.exists():
        print(f"WARNING: {EVENT_NODES_DIR} not found — skipping node frontmatter source",
              file=sys.stderr)
        return []

    entries = []
    for node_file in sorted(EVENT_NODES_DIR.glob("*.node.md")):
        content = node_file.read_text()
        slug, name, aliases, _ = _parse_frontmatter_aliases(content)

        if not slug:
            slug = node_file.stem.replace('.node', '')

        entries.append({
            "alias": slug_to_normalized(slug),
            "canonical_slug": slug,
            "source": "node-slug",
            "confidence": "high",
            "raw": slug,
        })

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
# Source 3: All-node index for character-name fallback
# ---------------------------------------------------------------------------

def load_all_node_aliases() -> list[dict]:
    """Scan ALL graph/nodes/{category}/*.node.md directories (not just
    events/). Absorbed verbatim."""
    if not GRAPH_NODES_DIR.exists():
        print(f"WARNING: {GRAPH_NODES_DIR} not found", file=sys.stderr)
        return []

    entries = []
    for category_dir in sorted(GRAPH_NODES_DIR.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith('_'):
            continue
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

            entries.append({
                **base,
                "alias": slug_to_normalized(slug),
                "source": f"all-node-slug:{category}",
                "raw": slug,
            })

            if name:
                norm = name_to_normalized(name)
                if norm:
                    entries.append({
                        **base,
                        "alias": norm,
                        "source": f"all-node-name:{category}",
                        "raw": name,
                    })

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
    """Mirrors wiki-event-alias-harvester.py::slug_from_page_title."""
    slug = title.lower()
    slug = re.sub(r"[''']", "", slug)
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug


def _extract_redirect_target(html: str) -> str | None:
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
    """Harvest "The <Epithet>"-titled wiki redirect pages. Absorbed verbatim."""
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
            continue

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
            continue

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
# Source 4: Victim-phrase generation for death/execution hubs
# ---------------------------------------------------------------------------

def _victim_phrases(victim_display: str) -> list[str]:
    """Generate natural-language phrases for a victim name. Absorbed verbatim."""
    v = victim_display.strip()
    v_norm = normalize(v)
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
    return [normalize(p) for p in phrases if normalize(p)]


_DEATH_KEYWORDS = frozenset({
    "killed", "death", "dead", "execution", "executed", "murdered", "murder",
    "assassination", "assassinated", "beheaded", "slain", "dies", "died",
})


def _event_is_primary_death_of_victim(
    victim_slug: str,
    event_slug: str,
    event_node_names: dict[str, str],
) -> bool:
    """Absorbed verbatim from scripts/event_alias_resolver.py."""
    victim_tokens = set(victim_slug.split("-"))
    event_name = event_node_names.get(event_slug, "")
    combined = f"{event_slug} {event_name}".lower()
    combined_tokens = set(re.findall(r'\w+', combined))

    has_death_keyword = bool(combined_tokens & _DEATH_KEYWORDS)
    if not has_death_keyword:
        return False

    meaningful_victim_tokens = {t for t in victim_tokens if len(t) >= 4}
    has_victim_token = bool(meaningful_victim_tokens & combined_tokens)
    return has_victim_token


def _load_character_alias_map() -> dict[str, list[str]]:
    """Absorbed verbatim from scripts/event_alias_resolver.py."""
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
    """Absorbed verbatim from scripts/event_alias_resolver.py."""
    if event_node_names is None:
        event_node_names = {}
    if character_alias_map is None:
        character_alias_map = {}

    if not EDGES_FILE.exists():
        print(f"WARNING: {EDGES_FILE} not found — skipping victim-index source",
              file=sys.stderr)
        return []

    entries = []
    seen: set[tuple[str, str]] = set()

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

            event_type = event_node_types.get(event_slug, "")
            if event_type not in DEATH_EVENT_TYPES:
                continue

            if not _event_is_primary_death_of_victim(
                victim_slug, event_slug, event_node_names
            ):
                continue

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
    """Absorbed verbatim from scripts/event_alias_resolver.py."""
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
# step 4b — deterministic variant expansion (plurals / possessives / leading
# article) at BUILD time. Generates NEW alias entries from existing resolved
# (phrase -> slug) pairs; never touches node frontmatter (variants live only
# in this derived table). Lowest merge priority of all sources — a generated
# variant never displaces a real alias/name/slug entry; if a variant phrase
# collides with an already-claimed phrase for a DIFFERENT slug, it is logged
# (not guessed) to working/query-layer/variant-collisions-s190.md.
# ---------------------------------------------------------------------------

VARIANT_COLLISIONS_LOG = REPO_ROOT / "working/query-layer/variant-collisions-s190.md"

# A small set of common irregular plurals seen in ASOIAF food/object naming
# (kept intentionally short — this is a deterministic RULES pass, not a
# lemmatizer; anything not covered here just doesn't get a plural variant).
_IRREGULAR_PLURALS = {
    "loaf": "loaves",
    "knife": "knives",
    "wife": "wives",
    "life": "lives",
    "leaf": "leaves",
    "half": "halves",
    "shelf": "shelves",
    "wolf": "wolves",
    "man": "men",
    "woman": "women",
    "child": "children",
    "tooth": "teeth",
    "foot": "feet",
    "goose": "geese",
    "mouse": "mice",
    "person": "people",
}
# Reverse map for singularizing a plural variant candidate.
_IRREGULAR_SINGULARS = {v: k for k, v in _IRREGULAR_PLURALS.items()}


def _pluralize_word(word: str) -> str | None:
    """Return the plural form of a single lowercase word, or None if no
    deterministic rule applies. Rules (in order): irregular table; -y -> -ies
    (consonant+y only); -s/-x/-z/-ch/-sh -> +es; default +s. Does not touch
    words already ending in a plural-looking form (best-effort only)."""
    if not word or not word.isalpha():
        return None
    if word in _IRREGULAR_PLURALS:
        return _IRREGULAR_PLURALS[word]
    if word in _IRREGULAR_SINGULARS.values():
        return None  # already plural, per the irregular table
    if len(word) > 1 and word.endswith("y") and word[-2] not in "aeiou":
        return word[:-1] + "ies"
    if word.endswith(("s", "x", "z", "ch", "sh")):
        return word + "es"
    return word + "s"


def _singularize_word(word: str) -> str | None:
    """Inverse of _pluralize_word for a single lowercase word, best-effort."""
    if not word or not word.isalpha():
        return None
    if word in _IRREGULAR_SINGULARS:
        return _IRREGULAR_SINGULARS[word]
    if word in _IRREGULAR_PLURALS:
        return None  # already singular
    if word.endswith("ies") and len(word) > 3:
        return word[:-3] + "y"
    if word.endswith(("ses", "xes", "zes", "ches", "shes")) and len(word) > 4:
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss") and len(word) > 1:
        return word[:-1]
    return None


def _plural_variants(phrase: str) -> list[str]:
    """Generate plural/singular variants of a normalized phrase by
    transforming ONLY its final word (the common case: 'lemon cake' <->
    'lemon cakes'). Returns both directions since the source phrase may
    already be singular or plural."""
    words = phrase.split(" ")
    if not words or not words[-1]:
        return []
    last = words[-1]
    out = []
    plural = _pluralize_word(last)
    if plural and plural != last:
        out.append(" ".join(words[:-1] + [plural]))
    singular = _singularize_word(last)
    if singular and singular != last:
        out.append(" ".join(words[:-1] + [singular]))
    return out


def _possessive_variants(phrase: str) -> list[str]:
    """Generate "X's Y" <-> "Y of X" possessive variants for a TWO-OR-MORE-
    word phrase whose last word is a recognized possessable-noun-ish tail
    (kept simple: only handles the "<subject> <tail>" -> "<subject>'s <tail>"
    direction plus stripping an existing possessive). Natural-language only —
    does not fire on single-word phrases (no possessor to attach)."""
    out = []
    # "X's Y" -> "X Y" (strip the possessive) and vice versa, when the
    # phrase already contains "'s " as a whole-word marker.
    if "'s " in phrase:
        out.append(phrase.replace("'s ", " ", 1))
    else:
        words = phrase.split(" ")
        if len(words) >= 2:
            # Insert possessive after the first word (covers the common
            # "<name> <noun-phrase>" shape, e.g. "robb stark death" would not
            # occur as a stored phrase, but "tywin death" -> "tywin's death").
            out.append(words[0] + "'s " + " ".join(words[1:]))
    return out


def _article_variants(phrase: str) -> list[str]:
    """Generate "the X" <-> "X" leading-article variants. normalize() already
    strips a leading article from QUERY input, so this mainly matters for
    matching an alias TABLE KEY that itself starts with a bare noun the user
    might type with "the" in front (defense in depth / explicit coverage —
    the fuzzy/exact path already benefits from normalize() doing this at
    query time, but an explicit table entry means an EXACT hit either way)."""
    out = []
    if phrase.startswith("the "):
        out.append(phrase[4:])
    else:
        out.append("the " + phrase)
    return out


# Sources whose phrases are short, name-shaped strings (character/object/food/
# location names, node slugs) — the genuine target of plural/possessive/
# article expansion ("lemon cake" <-> "lemon cakes"). EXCLUDES "victim-index"
# deliberately: those phrases are already-generated multi-word sentence
# TEMPLATES ("X is killed", "assassination of X" — 5-15 words), and running
# a naive last-word pluralizer/possessive-inserter over a verb-phrase produces
# garbage ("... is killeds", "... with teats assassinateds"). Victim phrases
# already cover their own possessive form explicitly (_victim_phrases emits
# both "X death" and "X's death"), so they don't need this pass at all.
_VARIANT_ELIGIBLE_SOURCE_PREFIXES = (
    "node-name", "node-slug", "node-frontmatter-alias",
    "wiki-canonical-name", "wiki-slug-self", "wiki-redirect", "wiki-the-redirect",
    "all-node-name", "all-node-slug", "all-node-alias",
)

# Cap on phrase length (words) eligible for variant generation. Short,
# name-shaped phrases only — this is a deliberate, conservative bound so the
# generator can't run away over long templated/descriptive phrases that
# happen to slip through the source-prefix filter.
_VARIANT_MAX_WORDS = 4

# Proper-noun/titled-phrase node categories where PLURAL/POSSESSIVE transforms
# produce nonsense ("Dagmer" -> "Dagmers"; "Crake the Boarkiller" -> "Crake's
# the Boarkiller"; event titles like "Defenestration of Sunspear" -> "end of
# stannis's hope"-shaped garbage) rather than a phrase a real user would type.
# LEADING-ARTICLE variants ("the Red Witch" <-> "Red Witch") stay universal —
# that transform is safe for any name and is the one the misses log actually
# shows value for (epithets, house names). Plural/possessive are scoped down
# ONLY to node categories where the underlying noun is a common noun a user
# might legitimately pluralize/possessive-ize (food/object/material/text/
# title-shaped things). "" (unset — the shape event-table entries carry, since
# EVENT_NODES_DIR-sourced entries never set node_category) is treated as
# proper-noun/titled and EXCLUDED too — event/chapter titles are names, not
# common nouns, and the ambiguity of an unset category is itself a reason to
# be conservative.
_PROPER_NOUN_CATEGORIES = {
    "characters", "houses", "locations", "chapters", "factions", "events", "",
}
# Explicit allowlist is the safer inverse for this pass: only these categories
# get plural/possessive. (Kept alongside the exclusion set above for
# readability — an entry must be in the allowlist AND not in the exclusion
# set, but since they're complementary within the categories we've observed,
# the allowlist is the one actually consulted.)
_COMMON_NOUN_CATEGORIES = {
    "foods", "objects", "artifacts", "materials", "texts", "titles",
    "customs", "concepts", "religions",
}


def _variant_eligible(phrase: str, source: str, node_category: str = "") -> tuple[bool, bool]:
    """Returns (article_eligible, plural_possessive_eligible)."""
    src_base = source.split(":")[0] if ":" in source else source
    if src_base not in _VARIANT_ELIGIBLE_SOURCE_PREFIXES:
        return False, False
    if not phrase or len(phrase.split(" ")) > _VARIANT_MAX_WORDS:
        return False, False
    plural_possessive_ok = (
        node_category in _COMMON_NOUN_CATEGORIES
        and node_category not in _PROPER_NOUN_CATEGORIES
    )
    return True, plural_possessive_ok


def generate_variants(source_entries: list[dict]) -> list[dict]:
    """Generate plural/possessive/article variant entries at the LOWEST merge
    priority, from short name-shaped alias entries only (see
    _VARIANT_ELIGIBLE_SOURCE_PREFIXES / _VARIANT_MAX_WORDS above — this
    deliberately excludes the long victim-phrase sentence templates).

    Returns a list of NEW alias entries (same shape as every other source's
    entries) tagged source="variant-plural" / "variant-possessive" /
    "variant-article". Callers merge these back through build_lookup_table
    alongside the real sources so real data always outranks a generated
    variant on collision (PRIORITY_ORDER unchanged — variant sources sort
    after every real source, see PRIORITY_ORDER below).
    """
    new_entries: list[dict] = []
    seen: set[tuple[str, str, str]] = set()  # (phrase, slug, source) dedupe

    def _emit(phrase: str, slug: str, kind: str, raw: str, meta: dict) -> None:
        if not phrase or phrase == raw:
            return
        key = (phrase, slug, kind)
        if key in seen:
            return
        seen.add(key)
        new_entries.append({
            "alias": phrase,
            "canonical_slug": slug,
            "node_category": meta.get("node_category", ""),
            "node_type": meta.get("node_type", ""),
            "source": kind,
            "raw": f"variant of {raw!r}",
        })

    for e in source_entries:
        phrase = e.get("alias", "")
        slug = e.get("canonical_slug")
        source = e.get("source", "")
        node_category = e.get("node_category", "")
        if not phrase or not slug:
            continue
        article_ok, plural_possessive_ok = _variant_eligible(phrase, source, node_category)
        if not article_ok:
            continue
        meta = {"node_category": node_category, "node_type": e.get("node_type", "")}
        if plural_possessive_ok:
            for v in _plural_variants(phrase):
                _emit(v, slug, "variant-plural", phrase, meta)
            for v in _possessive_variants(phrase):
                _emit(v, slug, "variant-possessive", phrase, meta)
        for v in _article_variants(phrase):
            _emit(v, slug, "variant-article", phrase, meta)

    return new_entries


def _filter_variant_collisions(collisions: dict[str, list[dict]]) -> dict[str, list[dict]]:
    """Filter a collisions dict down to phrases involving at least one
    generated variant entry. A phrase that collides for reasons unrelated to
    variant generation (e.g. two real wiki aliases clashing) is left out —
    that's pre-existing collision noise the build already tracked separately."""
    variant_sources = {"variant-plural", "variant-possessive", "variant-article"}
    return {
        phrase: cands
        for phrase, cands in collisions.items()
        if any(c["source"] in variant_sources for c in cands)
    }


def write_variant_collisions_log(
    sections: list[tuple[str, dict[str, list[dict]]]],
    path: Path = VARIANT_COLLISIONS_LOG,
) -> int:
    """Write ONE combined review file (working/query-layer/, NOT graph/ or
    node frontmatter) covering every collision section (event table,
    all-node index, ...). `sections` is a list of (label, relevant_collisions)
    pairs, already filtered by _filter_variant_collisions. Returns the total
    count of colliding phrases logged across all sections."""
    total = sum(len(rel) for _, rel in sections)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Variant-generation collisions — step 4b (S190)\n",
        f"Generated: {datetime.now(timezone.utc).isoformat()}\n",
    ]
    if total == 0:
        lines.append(
            "\nNo collisions involving a generated plural/possessive/article "
            "variant were found in this build.\n"
        )
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return 0

    lines.append(
        f"\n{total} phrase(s) (across {len(sections)} table(s)) where a "
        "deterministically-generated plural/possessive/article variant "
        "collided with an existing alias for a DIFFERENT slug. Logged for "
        "review, not auto-resolved — the existing PRIORITY_ORDER means a "
        "real alias/name/slug always wins over a generated variant; these "
        "are cases where TWO OR MORE real slugs are already tied to the "
        "target phrase, so no single winner exists even before the variant "
        "arrived.\n"
    )
    for label, relevant in sections:
        if not relevant:
            continue
        lines.append(f"\n## Table: {label} ({len(relevant)} phrase(s))\n")
        for phrase, cands in sorted(relevant.items()):
            lines.append(f"\n### `{phrase}`\n")
            for c in cands:
                lines.append(
                    f"- slug=`{c['canonical_slug']}` source=`{c['source']}` "
                    f"raw={c.get('raw', '')!r}"
                )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return total


# ---------------------------------------------------------------------------
# Merge + collision handling
# ---------------------------------------------------------------------------

PRIORITY_ORDER = [
    "node-name",
    "node-slug",
    "node-frontmatter-alias",
    "victim-index",
    "wiki-canonical-name",
    "wiki-slug-self",
    "wiki-redirect",
    "variant-plural",
    "variant-possessive",
    "variant-article",
]


def build_lookup_table(
    entries: list[dict],
) -> tuple[dict[str, str], dict[str, list[dict]], dict]:
    """Merge all alias entries into a single {phrase -> canonical_slug} dict.
    Absorbed verbatim from scripts/event_alias_resolver.py."""
    by_phrase: dict[str, list[dict]] = {}
    for e in entries:
        phrase = e["alias"]
        if not phrase:
            continue
        by_phrase.setdefault(phrase, []).append(e)

    lookup = {}
    collisions = {}

    for phrase, candidates in by_phrase.items():
        slugs = {c["canonical_slug"] for c in candidates}

        if len(slugs) == 1:
            lookup[phrase] = next(iter(slugs))
        else:
            slug_rank: dict[str, int] = {}
            for c in candidates:
                src = c["source"]
                src_base = src.split(":")[0] if ":" in src else src
                rank = PRIORITY_ORDER.index(src_base) if src_base in PRIORITY_ORDER else len(PRIORITY_ORDER)
                existing = slug_rank.get(c["canonical_slug"], len(PRIORITY_ORDER) + 1)
                slug_rank[c["canonical_slug"]] = min(existing, rank)

            best_rank = min(slug_rank.values())
            best_slugs = [s for s, r in slug_rank.items() if r == best_rank]

            if len(best_slugs) == 1:
                lookup[phrase] = best_slugs[0]
            else:
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

def build_and_save(
    verbose: bool = True,
    *,
    output_file: Path = OUTPUT_FILE,
    all_nodes_output_file: Path = ALL_NODES_OUTPUT_FILE,
) -> dict:
    """Full build: harvest all sources, merge, save to output_file /
    all_nodes_output_file. Returns the stats dict.

    output_file / all_nodes_output_file default to the LIVE paths (unchanged
    from event_alias_resolver.py) but can be overridden — used by the parity
    verification driver to write to a temp path without touching the live
    tables.
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
        print("Generating deterministic variants (step 4b: plural/possessive/article)...")
    variant_entries = generate_variants(all_entries)
    if verbose:
        print(f"  {len(variant_entries)} candidate variant entries generated")

    if verbose:
        print("Merging and deduplicating...")

    all_entries_with_variants = all_entries + variant_entries
    lookup, collisions, stats = build_lookup_table(all_entries_with_variants)

    event_variant_collisions = _filter_variant_collisions(collisions)

    source_counts: dict[str, int] = {}
    for e in all_entries_with_variants:
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

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w") as f:
        json.dump(output, f, indent=2, sort_keys=True)

    if verbose:
        print(f"\nSaved to: {output_file}")
        print(f"  Unique phrases indexed: {stats['unique_phrases']}")
        print(f"  Unambiguous lookups:    {stats['unambiguous_lookups']}")
        print(f"  Ambiguous collisions:   {stats['ambiguous_collisions']}")
        print(f"\nSource breakdown:")
        for src, count in sorted(source_counts.items()):
            print(f"  {src:35s}: {count:5d}")

    if verbose:
        print("\nBuilding all-node index (for character-name fallback)...")
    all_node_entries = load_all_node_aliases()
    # step 4a (G19): fold victim-phrase entries in here too. Without this, the
    # all-node index (the table build_chat_bundle.py's build_alias_map() reads
    # to produce web/data/alias-map.json) never carries phrases like "robb
    # stark's death" — they existed only in the EVENT-alias lookup above
    # (event-alias-lookup.json), which the bundle build does NOT consume. The
    # event-alias-lookup.json output above is unchanged (still wiki+node+victim);
    # this is additive: victim phrases now ALSO land in the all-node index.
    all_node_entries_with_events = all_node_entries + node_entries + victim_entries
    _, _, all_stats = build_lookup_table(all_node_entries_with_events)

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

    all_node_collapsed: dict[str, list[dict]] = {}
    for phrase, candidates in all_node_by_phrase.items():
        seen_slugs: set[str] = set()
        deduped = []
        for c in candidates:
            if c["canonical_slug"] not in seen_slugs:
                seen_slugs.add(c["canonical_slug"])
                deduped.append(c)
        all_node_collapsed[phrase] = deduped

    # step 4b (all-node index side): generate the SAME plural/possessive/
    # article variants from every (phrase -> slug) pair already present,
    # then merge them in with the SAME "real entries win" rule used above —
    # a generated variant is only added to a phrase bucket that doesn't
    # already carry that slug, and if the phrase bucket already resolves to
    # OTHER slug(s), the collision (variant phrase implies a different node
    # than what's already there) is logged for review rather than silently
    # added as a second candidate.
    all_node_variant_collisions: dict[str, list[dict]] = {}
    all_node_variant_new_phrases = 0
    for phrase, candidates in list(all_node_collapsed.items()):
        for cand in candidates:
            slug = cand["canonical_slug"]
            article_ok, plural_possessive_ok = _variant_eligible(
                phrase, cand.get("source", ""), cand.get("node_category", "")
            )
            if not article_ok:
                continue
            variant_kinds = [("variant-article", _article_variants(phrase))]
            if plural_possessive_ok:
                variant_kinds = [
                    ("variant-plural", _plural_variants(phrase)),
                    ("variant-possessive", _possessive_variants(phrase)),
                ] + variant_kinds
            for kind, variants in variant_kinds:
                for v in variants:
                    if not v or v == phrase:
                        continue
                    existing = all_node_collapsed.get(v)
                    if existing is None:
                        all_node_collapsed[v] = [{
                            "canonical_slug": slug,
                            "node_category": cand.get("node_category", ""),
                            "node_type": cand.get("node_type", ""),
                            "source": kind,
                        }]
                        all_node_variant_new_phrases += 1
                    elif not any(c["canonical_slug"] == slug for c in existing):
                        # phrase already resolves to (a) different slug(s) —
                        # log, don't guess which one is "right".
                        all_node_variant_collisions.setdefault(v, []).extend(existing)
                        all_node_variant_collisions[v].append({
                            "canonical_slug": slug,
                            "node_category": cand.get("node_category", ""),
                            "node_type": cand.get("node_type", ""),
                            "source": kind,
                        })
    if verbose:
        print(f"  {all_node_variant_new_phrases} NEW phrases added via variant generation (all-node index)")

    total_variant_collisions = write_variant_collisions_log([
        ("event-alias-lookup.json", event_variant_collisions),
        ("all-node-alias-lookup.json", all_node_variant_collisions),
    ])
    if verbose:
        print(f"  {total_variant_collisions} total variant collision(s) logged to "
              f"{VARIANT_COLLISIONS_LOG}")

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

    all_nodes_output_file.parent.mkdir(parents=True, exist_ok=True)
    with all_nodes_output_file.open("w") as f:
        json.dump(all_node_output, f, indent=2, sort_keys=True)

    if verbose:
        print(f"Saved all-node index to: {all_nodes_output_file}")
        print(f"  Unique phrases in all-node index: {len(all_node_collapsed)}")

    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Build the Weirwood query engine's alias lookup tables."
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build (or rebuild) the alias lookup table at the live paths.",
    )
    parser.add_argument(
        "--out",
        metavar="PATH",
        default=None,
        help="Override event-alias-lookup.json output path (verification/temp use).",
    )
    parser.add_argument(
        "--all-nodes-out",
        metavar="PATH",
        default=None,
        help="Override all-node-alias-lookup.json output path (verification/temp use).",
    )
    args = parser.parse_args()

    if not args.build:
        parser.print_help()
        return

    kwargs = {}
    if args.out:
        kwargs["output_file"] = Path(args.out)
    if args.all_nodes_out:
        kwargs["all_nodes_output_file"] = Path(args.all_nodes_out)

    build_and_save(verbose=True, **kwargs)


if __name__ == "__main__":
    main()
