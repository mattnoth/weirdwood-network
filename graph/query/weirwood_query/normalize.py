"""normalize.py — ONE phrase normalizer/tokenizer for the Weirwood query engine.

Absorbed VERBATIM from scripts/event_alias_resolver.py (normalize, tokenize,
slug_to_normalized, name_to_normalized, alias_slug_to_normalized). This is the
normalizer that WINS (query-layer design.md D-B / step 1): `web/src/lib/
normalize.ts` is a byte-for-byte TS port of THIS module's `normalize()` /
`tokenize()` (see that file's own header comment) — any semantic change here
must be mirrored there, or Python/TS resolution silently diverges again (G11/
G12). Do NOT "fix" anything in this pass (e.g. no plural/possessive handling,
no de-biased scoring) — that is step 4 (resolver hardening), gated separately.

No LLM in the loop. Ever.
"""

from __future__ import annotations

import re

# Stop words excluded from token-overlap scoring. Includes common
# interrogative/auxiliary words so "who killed X" and "X's death" share only
# the entity-name tokens and score correctly.
STOP_WORDS: frozenset[str] = frozenset(
    {
        "of", "the", "a", "an", "at", "in", "on", "by", "to", "and", "for", "s",
        # interrogatives / auxiliaries
        "who", "what", "where", "when", "how", "which", "whom",
        "did", "does", "do", "is", "was", "were", "are", "has", "have", "had",
    }
)


def normalize(phrase: str) -> str:
    """Normalize a natural-language phrase to a lookup key.

    Steps:
      1. Lowercase
      2. Strip ONE leading article (a, an, the) and surrounding whitespace
      3. Collapse internal whitespace -> single space
      4. Return the normalized string (NOT kebab-cased — lookup is by
         normalized phrase)

    The lookup table keys are all normalized forms of every alias. Input
    queries are normalized the same way before lookup, so "the Red Wedding",
    "Red Wedding", "red wedding" all resolve identically.
    """
    phrase = phrase.lower().strip()
    phrase = re.sub(r"^(the|a|an)\s+", "", phrase)
    phrase = re.sub(r"\s+", " ", phrase).strip()
    return phrase


def name_to_normalized(name: str) -> str:
    """Normalize a node's canonical name: field for lookup."""
    return normalize(name)


def slug_to_normalized(slug: str) -> str:
    """Convert a kebab-case slug to a normalized phrase for lookup."""
    return normalize(slug.replace("-", " "))


def alias_slug_to_normalized(alias: str) -> str:
    """Convert a wiki-redirect alias slug to a normalized phrase."""
    # Wiki redirect slugs use kebab-case (e.g. 'the-red-wedding').
    return normalize(alias.replace("-", " "))


def tokenize(phrase: str) -> set[str]:
    """Split a normalized phrase into a set of tokens (words), excluding
    stop words (see STOP_WORDS)."""
    tokens = set(re.findall(r"\w+", phrase.lower()))
    return tokens - STOP_WORDS


# ---------------------------------------------------------------------------
# Slug minting — used by load.py / traverse.py for edge-target resolution.
# Absorbed from scripts/graph-query.py::title_to_slug. A SEPARATE convention
# from the phrase-normalizers above (this produces a kebab-case slug fragment,
# not a normalized lookup phrase) — kept in this module because it is the
# other half of "how the engine turns free text into something matchable."
# ---------------------------------------------------------------------------

def title_to_slug(title: str) -> str:
    """Convert a node title/name to a filesystem slug.

    Matches the convention in wiki-pass2-emit-deterministic.py::page_to_slug
    (mirrored previously in scripts/graph-query.py::title_to_slug).
    """
    slug = title.lower()
    slug = re.sub(r"['\",]", "", slug)
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug
