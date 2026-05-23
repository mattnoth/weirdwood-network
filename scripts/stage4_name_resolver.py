"""stage4_name_resolver.py — Collision-aware name resolver for the Stage 4 Pass-1 pipeline.

Importable module (note: underscore filename so it's importable via plain `import`).

Provides a five-rung resolution ladder that extends the baseline
exact/alias slug lookup with:
  c. firstname-unique:   first token maps to exactly one graph node
  d. context-present:    multiple candidates but only one is in the chapter's
                         already-present slugs
  e. context-prior:      multiple candidates, dominant one has ≥ 3x the
                         backlink count of the runner-up

Unambiguous hits (rungs c/d/e) are resolved automatically.
Ambiguous hits (rung f) are queued for human review, never guessed.

Usage (as module):
    from scripts.stage4_name_resolver import (
        build_firstname_index,
        load_importance_prior,
        resolve_name,
    )
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Minimum backlink ratio for the context-prior rung to fire
PRIOR_DOMINANT_RATIO = 3.0

# Generic role-words / bare titles that must NEVER resolve via the
# firstname-unique / context-present / context-prior rungs.  When the
# entire cleaned-and-slugified name equals one of these tokens the
# resolver returns (None, STATUS_UNRESOLVED_GENERIC) immediately after
# the exact (a) and alias (b) rungs so that e.g. "the maester" → slug
# "maester" never gets force-resolved to the graph node named "Maester".
#
# CRITICAL: the check is on the WHOLE slug, not just the first token, so
# "Maester Luwin" → "maester-luwin" (not in the set) still resolves
# normally via exact/alias/firstname.  Only a bare "maester" / "the
# maester" / "a maester" (all of which reduce to the single slug
# "maester" after article stripping) is blocked.
# Leading honorific/title tokens that PRECEDE a proper name but are NOT the name
# itself.  Used by name_key() to skip them when building the firstname index.
# CRITICAL: this stripping only affects the firstname/context fallback rungs (c/d/e).
# Rungs a (exact) and b (alias) are UNCHANGED — so "Ser Pounce" / "Maester Luwin"
# full-form slugs still resolve exactly when they exist as canonical nodes.
#
# Populate conservatively: only tokens that are reliably ONLY honorifics in ASOIAF.
# "Old" and "Young" are included because "Old Nan", "Old Bear" etc. are indexable
# by their second token (Nan, Bear) without confusion.
TITLE_PREFIXES: frozenset[str] = frozenset({
    "ser",
    "lord",
    "lady",
    "maester",
    "grand",
    "archmaester",
    "king",
    "queen",
    "prince",
    "princess",
    "septon",
    "septa",
    "khal",
    "khaleesi",
    "master",
    "captain",
    "magister",
    "messire",
    "goodwife",
    "high",
    "old",
    "young",
})

GENERIC_TERMS: frozenset[str] = frozenset({
    # Titles / rank words used as bare references
    "maester", "maesters",
    "septa", "septas",
    "septon",
    "ser",
    "lord", "lords",
    "lady", "ladies",
    "king", "kings",
    "queen", "queens",
    "prince", "princes",
    "princess",
    "squire", "squires",
    "master",
    "captain",
    "steward",
    "khal",
    "khaleesi",
    "magister",
    "bravo",
    "priest", "priests",
    "priestess",
    # Role / occupation nouns
    "knight", "knights",
    "wildling", "wildlings",
    "sailor", "sailors",
    "guard", "guards",
    "cook",
    "smith",
    "singer",
    "sellsword", "sellswords",
    "crow", "crows",
    "soldier", "soldiers",
    "servant", "servants",
    "slave", "slaves",
    "whore",
    # Generic relational nouns
    "brother", "brothers",
    "sister", "sisters",
    "mother",
    "father",
    "son", "sons",
    "daughter", "daughters",
    # Generic person nouns
    "man", "men",
    "woman", "women",
    "child", "children",
    "girl", "girls",
    "boy", "boys",
    # Common animals used as vague references
    "dragon", "dragons",
    "wolf", "wolves",
    "horse", "horses",
    "raven", "ravens",
    "dog",
})

# Slugify — must match the canonical convention used elsewhere in the pipeline
def to_slug(raw: str) -> str:
    """Convert a display name to a kebab-case slug (idempotent)."""
    s = raw.lower()
    s = re.sub(r"['\",]", "", s)            # strip apostrophes/quotes/commas
    s = re.sub(r"[ _]+", "-", s)            # spaces/underscores → hyphens
    s = re.sub(r"[^a-z0-9-]", "-", s)      # anything else → hyphen
    s = re.sub(r"-+", "-", s).strip("-")
    return s


# ---------------------------------------------------------------------------
# Preprocessing helpers
# ---------------------------------------------------------------------------

_PAREN_RE = re.compile(r"\s*\([^)]*\)")        # " (the queen)" → ""
_POSSESSIVE_RE = re.compile(r"'s?\s*$", re.IGNORECASE)  # trailing "'s" or "'"
# Leading English articles / indefinite articles to strip so "the maester"
# and "a septa" reduce to the bare term for generic-term detection.
_LEADING_ARTICLE_RE = re.compile(r"^(the|a|an)\s+", re.IGNORECASE)


def _clean_raw_name(raw: str) -> str:
    """Strip parentheticals and trailing possessives from a raw name cell.

    Examples:
        "Cersei (the queen)"     → "Cersei"
        "Lord Eddard's"          → "Lord Eddard"
        "Jorah Mormont (Ser)"    → "Jorah Mormont"
        "Tyrion"                 → "Tyrion"
    """
    s = raw.strip()
    s = _PAREN_RE.sub("", s)          # remove parentheticals
    s = _POSSESSIVE_RE.sub("", s)     # remove trailing possessive
    return s.strip()


def _first_token(name: str) -> str:
    """Return the lowercased first whitespace-delimited token of name.

    E.g. "Tyrion Lannister" → "tyrion", "Lord Commander Mormont" → "lord".
    """
    tokens = name.split()
    if not tokens:
        return ""
    return tokens[0].lower()


def name_key(name: str) -> Optional[str]:
    """Return the first non-title token of a (cleaned) display name, lowercased.

    Strips any leading TITLE_PREFIXES tokens before returning the first
    remaining token.  This is the lookup key used when building and querying
    the firstname index (rungs c/d/e) so that honorific-first names like
    "Ser Pounce" index under "pounce" and "Khal Drogo" under "drogo".

    Rungs a (exact slug match) and b (alias lookup) are NOT affected — they
    operate on the full slug and bypass this function entirely.

    Returns:
        The first non-title lowercase token, or None if the entire name
        consists only of title prefix tokens (e.g. bare "Ser" → None).

    Examples:
        name_key("Ser Pounce")        → "pounce"
        name_key("Khal Drogo")        → "drogo"
        name_key("Lord Tywin")        → "tywin"
        name_key("Maester Luwin")     → "luwin"
        name_key("Cersei")            → "cersei"
        name_key("Tyrion Lannister")  → "tyrion"
        name_key("Ser")               → None
        name_key("Lord")              → None
        name_key("Old Nan")           → "nan"
    """
    tokens = [t.lower() for t in name.split() if t]
    for tok in tokens:
        if tok not in TITLE_PREFIXES:
            return tok
    return None


# ---------------------------------------------------------------------------
# Index builders
# ---------------------------------------------------------------------------

def _display_name_from_slug(slug: str) -> str:
    """Fallback: de-kebab the slug into a display name.

    "tyrion-lannister" → "Tyrion Lannister"
    Single-token slugs like "yoren" → "Yoren"
    """
    return " ".join(part.capitalize() for part in slug.split("-"))


def build_firstname_index(
    node_slugs: set[str],
    node_names: dict[str, str],
) -> dict[str, list[str]]:
    """Build a first-name (first non-title token) → [slug, ...] index.

    Args:
        node_slugs: Complete set of canonical graph slugs (e.g. from build_graph_index).
        node_names: Mapping of slug → display name (from frontmatter `name:` field,
                    or de-kebabbed slug as fallback). Pre-supply this from
                    load_node_display_names() below.

    Returns:
        Dict where each key is a lowercased first-non-title-token and the value is
        the list of slugs whose display name has that as its first non-title token.

    Index rules:
        - Leading TITLE_PREFIXES tokens are stripped before keying:
          "Ser Pounce" → keyed under "pounce"; "Khal Drogo" → keyed under "drogo".
        - This prevents honorific-first nodes from consuming the entire title namespace.
        - Nodes whose entire display name is title tokens (e.g. bare "Ser") are
          skipped (name_key returns None) — they remain reachable only via exact
          slug match (rung a).
        - Single-token non-title names (e.g. "Yoren") are indexed under themselves.
    """
    index: dict[str, list[str]] = {}

    for slug in node_slugs:
        display = node_names.get(slug, _display_name_from_slug(slug))
        key = name_key(display)
        if key is None:
            continue
        if key not in index:
            index[key] = []
        index[key].append(slug)

    return index


def load_node_display_names(
    node_slugs: set[str],
    graph_nodes_dir: Path,
    skip_dirs: frozenset[str] | set[str] = frozenset(
        {"_conflicts", "_unclassified", "_stage3-preview"}
    ),
) -> dict[str, str]:
    """Walk graph/nodes/**/*.node.md and extract the `name:` frontmatter field.

    Returns a mapping of slug → display name. Falls back to de-kebabbed slug
    when the file lacks a name field or can't be read.
    """
    _NAME_RE = re.compile(r"^name:\s*(.+?)\s*$", re.MULTILINE)
    result: dict[str, str] = {}

    for node_file in graph_nodes_dir.rglob("*.node.md"):
        parts = node_file.relative_to(graph_nodes_dir).parts
        if any(p in skip_dirs for p in parts):
            continue

        slug = node_file.name[: -len(".node.md")]
        if slug not in node_slugs:
            continue

        try:
            text = node_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            result[slug] = _display_name_from_slug(slug)
            continue

        m = _NAME_RE.search(text)
        if m:
            name = m.group(1).strip().strip('"').strip("'")
            result[slug] = name if name else _display_name_from_slug(slug)
        else:
            result[slug] = _display_name_from_slug(slug)

    # Slugs that had no file entry (shouldn't happen, but be safe)
    for slug in node_slugs:
        if slug not in result:
            result[slug] = _display_name_from_slug(slug)

    return result


def load_importance_prior(backlink_counts_path: Path) -> dict[str, int]:
    """Load backlink-counts.json and return {slug: in_count}.

    The JSON has structure: {"backlinks": {slug: {"in_count": N, ...}, ...}, ...}
    Returns a flat dict of slug → inbound link count.  Missing slugs implicitly
    have count 0.
    """
    try:
        data = json.loads(backlink_counts_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        import sys
        print(f"WARNING: Cannot load backlink-counts from {backlink_counts_path}: {exc}",
              file=sys.stderr)
        return {}

    backlinks = data.get("backlinks", {})
    return {slug: info.get("in_count", 0) for slug, info in backlinks.items()}


# ---------------------------------------------------------------------------
# Core resolver
# ---------------------------------------------------------------------------

# Status strings (used in resolution_status field of candidate rows)
STATUS_EXACT = "resolved-exact"
STATUS_ALIAS = "resolved-alias"
STATUS_FIRSTNAME_UNIQUE = "resolved-firstname-unique"
STATUS_CONTEXT_PRESENT = "resolved-context-present"
STATUS_CONTEXT_PRIOR = "resolved-context-prior"
STATUS_AMBIGUOUS = "ambiguous-queued"
STATUS_UNRESOLVED = "unresolved"
STATUS_UNRESOLVED_GENERIC = "unresolved-generic"


def resolve_name(
    raw_name: str,
    *,
    alias_map: dict[str, str],
    node_set: set[str],
    firstname_index: dict[str, list[str]],
    prior: dict[str, int],
    present_slugs: set[str],
) -> tuple[Optional[str], str]:
    """Resolve a raw relationship-table name to a canonical graph slug.

    Resolution ladder (first hit wins):
        a. exact:              to_slug(cleaned) ∈ node_set
        b. alias:              alias_map[to_slug(cleaned)] ∈ node_set
        [generic-term gate]:   if whole slug (after article strip) ∈ GENERIC_TERMS
                               → (None, STATUS_UNRESOLVED_GENERIC); skip c–e
        c. firstname-unique:   firstname_index[first_token] has exactly one slug
                               (after filtering generic-term concept nodes)
        d. context-present:    multiple candidates, exactly one ∈ present_slugs
        e. context-prior:      top candidate by backlink count ≥ 3× runner-up
        f. ambiguous-queued:   multiple, no confident pick → (None, STATUS_AMBIGUOUS)
        g. unresolved:         no candidates → (None, STATUS_UNRESOLVED)

    Multi-name cells (comma-separated) are OUT OF SCOPE for v1: they fall
    to unresolved (the comma will survive in to_slug and almost certainly
    produce no match).

    Args:
        raw_name:        The name string exactly as it appeared in the table cell.
        alias_map:       alias_to_canonical dict from alias-resolver.json.
        node_set:        Complete set of canonical slugs (from build_graph_index).
        firstname_index: Output of build_firstname_index().
        prior:           Output of load_importance_prior().
        present_slugs:   Set of already-resolved slugs for the current chapter
                         (bootstrapped via rungs a–c only, to avoid circularity).

    Returns:
        (slug_or_None, status_string)
    """
    cleaned = _clean_raw_name(raw_name)
    if not cleaned:
        return None, STATUS_UNRESOLVED

    slug_cand = to_slug(cleaned)

    # Rung a: exact match
    if slug_cand in node_set:
        return slug_cand, STATUS_EXACT

    # Rung b: alias lookup
    alias_target = alias_map.get(slug_cand)
    if alias_target and alias_target in node_set:
        return alias_target, STATUS_ALIAS

    # Generic-term gate — applied AFTER exact (a) and alias (b) so that a node
    # literally named "Maester" (exact match) or an alias pointing to such a
    # node still resolves.  Strip leading articles first so "the maester" and
    # "a septa" reduce to the bare term slug before checking the stoplist.
    cleaned_no_article = _LEADING_ARTICLE_RE.sub("", cleaned).strip()
    generic_slug = to_slug(cleaned_no_article)
    if generic_slug in GENERIC_TERMS:
        return None, STATUS_UNRESOLVED_GENERIC

    # Rungs c–e operate on the first non-title name token (via name_key).
    # name_key strips leading TITLE_PREFIXES so "Ser Boros" → "boros",
    # "Khal Drogo" → "drogo", preventing honorific-first nodes from
    # capturing the entire title namespace in the firstname index.
    # If name_key returns None (entire name is titles, e.g. bare "Ser"),
    # treat as unresolved-generic (same effect as bare generic-term gate).
    first = name_key(cleaned)
    if first is None:
        return None, STATUS_UNRESOLVED_GENERIC

    candidates = firstname_index.get(first, [])

    # Filter out generic-term concept nodes from the candidate pool so that e.g.
    # "Maester Luwin" (whose first token is "maester") cannot resolve to the bare
    # concept node `maester` via rungs c/d/e.  Generic concept nodes may
    # legitimately exist in the graph, but they should never be picked as the
    # resolution target for a full name like "Maester Luwin".
    candidates = [c for c in candidates if c not in GENERIC_TERMS]

    if not candidates:
        return None, STATUS_UNRESOLVED

    # Rung c: unique first-name match
    if len(candidates) == 1:
        return candidates[0], STATUS_FIRSTNAME_UNIQUE

    # Multiple candidates — try context disambiguation

    # Rung d: exactly one candidate is in present_slugs
    present_candidates = [c for c in candidates if c in present_slugs]
    if len(present_candidates) == 1:
        return present_candidates[0], STATUS_CONTEXT_PRESENT

    # Rung e: dominant by backlink prior (≥ 3× runner-up)
    scored = sorted(candidates, key=lambda s: prior.get(s, 0), reverse=True)
    if len(scored) >= 2:
        top_count = prior.get(scored[0], 0)
        second_count = prior.get(scored[1], 0)
        if top_count > 0 and top_count >= PRIOR_DOMINANT_RATIO * max(second_count, 1):
            return scored[0], STATUS_CONTEXT_PRIOR
    elif len(scored) == 1:
        # Shouldn't happen (we checked len==1 above), but be safe
        return scored[0], STATUS_FIRSTNAME_UNIQUE

    # Rung f: ambiguous
    return None, STATUS_AMBIGUOUS


# ---------------------------------------------------------------------------
# Bootstrap helper (rungs a–c only, no context steps)
# ---------------------------------------------------------------------------

def resolve_name_bootstrap(
    raw_name: str,
    *,
    alias_map: dict[str, str],
    node_set: set[str],
    firstname_index: dict[str, list[str]],
) -> Optional[str]:
    """Resolve using only rungs a–c (exact/alias/firstname-unique).

    Used to bootstrap present_slugs for a chapter without circularity.
    Returns the resolved slug or None.
    """
    cleaned = _clean_raw_name(raw_name)
    if not cleaned:
        return None

    slug_cand = to_slug(cleaned)

    # Rung a
    if slug_cand in node_set:
        return slug_cand

    # Rung b
    alias_target = alias_map.get(slug_cand)
    if alias_target and alias_target in node_set:
        return alias_target

    # Rung c — use name_key to strip leading title prefixes (same as full resolver)
    first = name_key(cleaned)
    if first is None:
        return None
    candidates = [c for c in firstname_index.get(first, []) if c not in GENERIC_TERMS]
    if len(candidates) == 1:
        return candidates[0]

    return None


# ---------------------------------------------------------------------------
# Supplementary alias file writer
# ---------------------------------------------------------------------------

def write_firstname_aliases(
    firstname_index: dict[str, list[str]],
    output_path: Path,
) -> dict[str, str]:
    """Emit the auto-detected unambiguous first-name → slug mappings to a JSON file.

    Only includes entries where the firstname_index has exactly one candidate
    (rung-c hits). Does NOT modify alias-resolver.json.

    Returns the dict that was written (firstname_token → slug).
    """
    firstname_to_slug = {
        first: slugs[0]
        for first, slugs in firstname_index.items()
        if len(slugs) == 1
    }

    payload = {
        "version": "1",
        "produced_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "pass1-derived-firstname-resolver",
        "count": len(firstname_to_slug),
        "firstname_to_slug": firstname_to_slug,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return firstname_to_slug
