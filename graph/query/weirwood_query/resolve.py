"""resolve.py — Phrase-to-slug resolution for the Weirwood query engine.

Absorbed from scripts/event_alias_resolver.py's RESOLUTION half (exact ->
ambiguous -> character -> fuzzy). The TABLE-BUILD half (harvesting aliases
from wiki redirects / node frontmatter / victim phrases / "The_*" redirects
and merging them into the on-disk lookup tables) lives in
build/build_alias_table.py — this module only CONSUMES those tables.

query-layer design.md step 4c (S190): the candidate-length de-bias described
below is now IMPLEMENTED here (previously step 1 shipped this file with a
verbatim, unfixed port — see the design doc's G10 gap). MIN_FUZZY_SCORE /
MAX_FUZZY_CANDIDATES / PRIORITY_ORDER / collision handling remain unchanged;
only `_fuzzy_candidates`'s scoring formula changed. The identical formula is
ported to `web/src/lib/resolve.ts` (see that file's own comment) — any change
here must be mirrored there or Python/TS resolution silently diverges again.

No LLM in the loop. Ever.
"""

from __future__ import annotations

from pathlib import Path

from .load import EVENT_ALIAS_LOOKUP_FILE, load_alias_collisions, load_alias_lookup, load_all_node_index
from .normalize import normalize, tokenize

# Fuzzy matching tuning — UNCHANGED from event_alias_resolver.py.
MIN_FUZZY_SCORE = 0.5
MAX_FUZZY_CANDIDATES = 5

# step 4c (G10 de-bias): a candidate phrase key much LONGER than the query
# scores no higher than `len(query_tokens) / len(candidate_tokens)` of its
# raw token-overlap score — a query can't force a 1.0 by fully overlapping a
# short slice of a much longer candidate phrase (e.g. "House Targaryen"
# (2 tokens) fully contained inside a 13-token book-title phrase). Only
# penalizes when the candidate is LONGER than the query (min(1.0, ...) is a
# no-op, never a bonus, when candidate <= query). Applied to the BASE overlap
# score, before the existing +0.05-per-slug-token bonus (so a slug-name match
# can still lift a length-penalized score back up, same as before).

# Node categories included in character-name fallback.
CHARACTER_CATEGORIES = {"characters"}


def _fuzzy_candidates(
    norm_query: str,
    lookup: dict[str, str],
    all_node_index: dict[str, list[dict]] | None = None,
    max_results: int = MAX_FUZZY_CANDIDATES,
) -> list[dict]:
    """(a) Fuzzy / token-overlap fallback.

    Score each candidate key in the lookup (and all_node_index if provided)
    against the query using an asymmetric token-overlap metric, length-
    penalized (step 4c / G10):

        base   = |query_tokens ∩ candidate_tokens| / |query_tokens|
        length_penalty = min(1.0, |query_tokens| / |candidate_tokens|)
        score  = base * length_penalty, then + slug-token bonus (below)

    `length_penalty` is 1.0 (a no-op) whenever the candidate phrase is no
    longer than the query — it only discounts a candidate phrase LONGER than
    the query, so a query can't earn a 1.0 by being a full subset of a much
    longer candidate ("House Targaryen" fully contained in a 13-token
    book-title phrase, previously a tied 1.0). Final score must clear
    MIN_FUZZY_SCORE (checked AFTER the slug bonus, so a slug-name match can
    still lift a length-penalized score back over the floor). Returns a list
    of {slug, score, match_type: 'fuzzy', node_category, ...} sorted by score
    descending, up to max_results items.
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
        base = overlap / len(query_tokens)
        if base <= 0:
            return
        length_penalty = min(1.0, len(query_tokens) / len(cand_tokens))
        score = base * length_penalty
        # Bonus: if the query tokens also appear in the slug itself,
        # boost slightly (ranks slug-named entities above nickname-
        # matched ones when both have equal phrase scores).
        slug_tokens = tokenize(slug.replace("-", " "))
        slug_overlap = len(query_tokens & slug_tokens)
        if slug_overlap > 0:
            score = min(1.0, score + 0.05 * slug_overlap)
        if score >= MIN_FUZZY_SCORE:
            existing = scored.get(slug, 0.0)
            if score > existing:
                scored[slug] = score

    for phrase, slug in lookup.items():
        _score_candidate(phrase, slug)

    if all_node_index:
        for phrase, node_list in all_node_index.items():
            for node in node_list:
                _score_candidate(phrase, node["canonical_slug"])

    if not scored:
        return []

    ranked = sorted(scored.items(), key=lambda x: -x[1])[:max_results]

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
    """(c) Character-name fallback.

    If the normalized query matches any phrase in the all-node index that
    maps to a character node, return those character slugs as candidates.
    DIRECT (not fuzzy) lookup, filtered to character category results only.
    Fires before the fuzzy pass.
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
    *,
    collisions: dict[str, list[dict]] | None = None,
    lookup_file: Path = EVENT_ALIAS_LOOKUP_FILE,
) -> tuple[str | None, str, list[dict]]:
    """Resolve a natural-language phrase to a canonical slug.

    Resolution order:
      1. Exact normalized match in event alias lookup -> HIT (event)
      2. Exact match in all-node index for a character -> HIT (character-node)
      3. Fuzzy/token-overlap fallback against event lookup + all-node index

    Returns (slug, status, candidates) where:
      slug:   the top resolved slug, or None
      status: 'hit'           — unambiguous exact match
              'hit-character' — exact match to a character node
              'candidates'    — fuzzy or ambiguous match; see candidates list
              'ambiguous'     — phrase is in the collision table
              'miss'          — no match at any level
      candidates: list of {slug, score, match_type, node_category, node_type}

    If `lookup` / `all_node_index` are not supplied they are loaded from disk
    (build/build_alias_table.py builds them if missing — this function does
    NOT trigger a build itself, unlike the legacy resolver's load_lookup()).
    `collisions` defaults to reading the same lookup_file's ambiguous_
    collisions block (mirrors the legacy CLI's inline re-read of OUTPUT_FILE).
    """
    if lookup is None:
        lookup = load_alias_lookup(lookup_file)
    if all_node_index is None:
        all_node_index = load_all_node_index()
    if collisions is None:
        collisions = load_alias_collisions(lookup_file)

    norm = normalize(phrase)

    # 1. Exact event alias lookup
    slug = lookup.get(norm)
    if slug is not None:
        return slug, "hit", []

    if norm in collisions:
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
        if (top_score >= 0.75
                and (len(fuzzy) == 1 or top_score - fuzzy[1]["score"] >= 0.2)):
            return fuzzy[0]["slug"], "candidates", fuzzy
        else:
            return None, "candidates", fuzzy

    return None, "miss", []
