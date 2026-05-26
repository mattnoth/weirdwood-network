#!/usr/bin/env python3
"""stage4-pass1-evidence-locator.py — Stage 4 Pass-1-Derived Edge Pipeline: Script 2.

Reads the per-chapter candidate JSONL files produced by Script 1
(stage4-pass1-edge-candidates.py) and, for each candidate, locates the best
verbatim supporting passage in the corresponding chapter prose file.

The evidence_text cell from the extraction is usually PARAPHRASED (e.g.
"Yoren cut her hair, disguised her, protects her identity, disciplines her"),
so matching is fuzzy: we score sentences by overlap with entity surface forms
+ distinctive content words from the evidence_text and hint_raw.

IMPROVED QUOTE SELECTION (v3):
  The locator now FIRST tries to use the hint's own quoted/verbatim content
  before falling back to the content-scoring approach.

  Selection algorithm (A → B → C → D):
    A. hint-verbatim  — Extract quoted fragment(s) from hint_raw (straight and
       curly quote glyphs).  Normalize whitespace + quote glyphs before
       comparing.  If a fragment ≥ ~15 chars / 3 words is found in the chapter
       sentences, use the containing sentence as evidence_quote.
       quote_source="hint-verbatim".  locate_quality based on whether that
       sentence names 0/1/2 endpoints — never fabricate a both-named window
       from elsewhere.

    B. hint-fuzzy  — If no verbatim match: strip markdown lead-ins (**...**)
       and trailing [annotations], extract action verb + key content tokens
       from the remaining hint text, and fuzzy-match against sentences.
       quote_source="hint-fuzzy".  Same honest locate_quality.

    C. both-named-window  — Only if A and B both fail: fall back to the v2
       content-scoring + both-named-window search (original Steps 1–4).
       quote_source="both-named-window".

    D. nearest-fallback / chapter-level  — as before.
       quote_source="nearest-fallback" or "chapter-level".

  Critical rule: if the hint's true location does NOT name both entities, set
  locate_quality to "hint-anchored-one-named" or "hint-anchored-none" and do
  NOT fabricate a both-named quote from elsewhere.  A mismatched both-named
  quote is worse than an honest weak one.

  Coreference limit: when a character is referred to only as "she"/"he"/"my
  father" the window expansion CANNOT recover the name.  Those cases land
  as locate_quality=hint-anchored-one-named/one-named or nearest-fallback —
  this is a known, hard limit documented in the design notes.

New fields emitted:
  locate_quality ∈ {both-named, one-named, nearest-fallback, chapter-level,
                    hint-anchored-both-named, hint-anchored-one-named,
                    hint-anchored-none}
  quote_source   ∈ {hint-verbatim, hint-fuzzy, both-named-window,
                    nearest-fallback, chapter-level}

Existing fields (evidence_quote, evidence_ref, locate_status) are unchanged.

For typed candidates → emits to {chapter}.edges.jsonl (the "win" file).
For untyped candidates → emits to {chapter}.tail.jsonl (staged for future LLM pass).
Both files carry the located citation (evidence_quote + evidence_ref + locate_status).

Outputs (--apply mode):
  - Typed edges:
      working/wiki/pass2-buckets/pass1-derived/{book}/{chapter}.edges.jsonl
  - Untyped tail:
      working/wiki/pass2-buckets/pass1-derived/_tail/{book}/{chapter}.tail.jsonl
  - Locator stats (md + json):
      working/wiki/data/pass1-derived-locator-stats.md
      working/wiki/data/pass1-derived-locator-stats.json

Usage:
  python3 scripts/stage4-pass1-evidence-locator.py --plan
      Read candidate files + prose, compute stats, print to stdout. Write NOTHING.
  python3 scripts/stage4-pass1-evidence-locator.py --apply
      Same as --plan, plus write all output files.
  python3 scripts/stage4-pass1-evidence-locator.py --plan --book acok
  python3 scripts/stage4-pass1-evidence-locator.py --plan --chapter-slug acok-arya-01

No LLM calls. No network. Deterministic.
"""

import argparse
import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
CHAPTERS_DIR = REPO_ROOT / "sources" / "chapters"
PASS2_BUCKETS_DIR = REPO_ROOT / "working" / "wiki" / "pass2-buckets"
WIKI_DATA_DIR = REPO_ROOT / "working" / "wiki" / "data"

IN_BASE_DIR = PASS2_BUCKETS_DIR / "pass1-derived"
OUT_TAIL_DIR = IN_BASE_DIR / "_tail"
OUT_LOCATOR_STATS_MD = WIKI_DATA_DIR / "pass1-derived-locator-stats.md"
OUT_LOCATOR_STATS_JSON = WIKI_DATA_DIR / "pass1-derived-locator-stats.json"

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]

# ---------------------------------------------------------------------------
# Both-named window search: max sentences to span in either direction
# ---------------------------------------------------------------------------
# A window of 3 consecutive sentences (~1 ± 1) spans typical run-on paragraphs
# where Name A appears in sentence N and Name B appears in sentence N±1.
BOTH_NAMED_WINDOW_SENTENCES = 3

# ---------------------------------------------------------------------------
# Lazy-loaded alias-aware token index (module-level cache)
# ---------------------------------------------------------------------------
_FILTER_MOD = None
_CACHED_STOPLIST: Optional[frozenset] = None
_CACHED_TOKEN_INDEX: dict[str, frozenset] = {}


def _load_filter_mod():
    """Lazy-load stage4-quote-relevance-filter.py via importlib (hyphen-safe)."""
    global _FILTER_MOD
    if _FILTER_MOD is not None:
        return _FILTER_MOD
    mod_path = REPO_ROOT / "scripts" / "stage4-quote-relevance-filter.py"
    if not mod_path.exists():
        return None
    try:
        spec = importlib.util.spec_from_file_location("stage4_quote_relevance_filter", mod_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _FILTER_MOD = mod
    except Exception as exc:
        print(f"  WARNING: Could not load stage4-quote-relevance-filter: {exc}", file=sys.stderr)
        _FILTER_MOD = None
    return _FILTER_MOD


def get_filter_stoplist() -> frozenset:
    """Return (and cache) the stoplist from the filter module."""
    global _CACHED_STOPLIST
    if _CACHED_STOPLIST is not None:
        return _CACHED_STOPLIST
    mod = _load_filter_mod()
    if mod is None:
        _CACHED_STOPLIST = frozenset()
        return _CACHED_STOPLIST
    try:
        _CACHED_STOPLIST = mod.build_stoplist()
    except Exception as exc:
        print(f"  WARNING: build_stoplist() failed: {exc}", file=sys.stderr)
        _CACHED_STOPLIST = frozenset()
    return _CACHED_STOPLIST


def get_slug_tokens(slug: str) -> frozenset:
    """Return alias-aware name tokens for a slug (cached).

    Falls back to _name_forms() tokens if the filter module is unavailable.
    """
    global _CACHED_TOKEN_INDEX
    if slug in _CACHED_TOKEN_INDEX:
        return _CACHED_TOKEN_INDEX[slug]

    mod = _load_filter_mod()
    if mod is not None:
        try:
            stoplist = get_filter_stoplist()
            idx = mod.build_slug_token_index(slugs=[slug], stoplist=stoplist)
            toks = idx.get(slug, frozenset())
            # If the index returned nothing for this slug, fall back to slug parts
            if not toks:
                toks = frozenset(
                    p.lower() for p in slug.split("-")
                    if len(p) > 2 and p.lower() not in stoplist
                )
        except Exception as exc:
            print(f"  WARNING: build_slug_token_index({slug!r}) failed: {exc}", file=sys.stderr)
            toks = _name_forms_as_tokens(slug)
    else:
        toks = _name_forms_as_tokens(slug)

    _CACHED_TOKEN_INDEX[slug] = toks
    return toks


def _name_forms_as_tokens(slug: str) -> frozenset:
    """Fallback: extract tokens from slug parts (length >= 3)."""
    return frozenset(p.lower() for p in slug.split("-") if len(p) >= 3)


# ---------------------------------------------------------------------------
# English stopwords — words to exclude from content-word scoring
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


def _content_words(text: str) -> set[str]:
    """Extract lowercased non-stopword words of length >= 3 from text."""
    tokens = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    return {t for t in tokens if t not in _STOPWORDS}


# ---------------------------------------------------------------------------
# Quote-glyph normalization (for hint-verbatim matching)
# ---------------------------------------------------------------------------

# Curly/typographic quote pairs → straight equivalents
_QUOTE_NORM_TABLE = str.maketrans({
    "“": '"',  # LEFT DOUBLE QUOTATION MARK
    "”": '"',  # RIGHT DOUBLE QUOTATION MARK
    "‘": "'",  # LEFT SINGLE QUOTATION MARK
    "’": "'",  # RIGHT SINGLE QUOTATION MARK (also apostrophe)
    "′": "'",  # PRIME
    "″": '"',  # DOUBLE PRIME
    "«": '"',  # LEFT-POINTING DOUBLE ANGLE QUOTATION
    "»": '"',  # RIGHT-POINTING DOUBLE ANGLE QUOTATION
    "—": "-",  # EM DASH (normalize for comparison)
    "–": "-",  # EN DASH
    " ": " ",  # NON-BREAKING SPACE
})

# Minimum verbatim fragment length to be worth searching
_VERBATIM_MIN_CHARS = 15
_VERBATIM_MIN_WORDS = 3


def _normalize_for_match(text: str) -> str:
    """Normalize text for fuzzy-equality comparison.

    - Translate curly/typographic quotes/dashes to ASCII equivalents
    - Collapse whitespace
    - Strip leading/trailing whitespace
    """
    text = text.translate(_QUOTE_NORM_TABLE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_hint_verbatim_fragments(hint_raw: str) -> list[str]:
    """Extract quoted literal fragments from hint_raw for verbatim search.

    Handles:
    - Text inside double quotes (straight " or curly " ")
    - Ignores fragments that are too short (< _VERBATIM_MIN_CHARS chars or
      < _VERBATIM_MIN_WORDS words) — they're not discriminative enough.

    Returns a list of normalized fragment strings (longest first).
    """
    # Normalize quote glyphs before extracting
    norm = _normalize_for_match(hint_raw)

    # Pull text between double-quote pairs
    fragments: list[str] = re.findall(r'"([^"]{10,})"', norm)

    # Filter to meaningful length
    result = []
    for frag in fragments:
        frag = frag.strip()
        word_count = len(re.findall(r"\b\w+\b", frag))
        if len(frag) >= _VERBATIM_MIN_CHARS and word_count >= _VERBATIM_MIN_WORDS:
            result.append(frag)

    # Return longest first — longer fragments are more precise
    return sorted(result, key=len, reverse=True)


def _find_verbatim_in_sentences(
    fragments: list[str],
    scored: list[tuple[float, bool, bool, int, str]],
) -> Optional[tuple[int, int, str]]:
    """Search scored sentences for any fragment from hint_raw.

    Returns (sentence_index, lineno, sentence_text) of the first/best sentence
    (or merged sentence pair) containing any fragment, or None if not found.

    Matching is done after normalizing both fragment and sentence text
    (quote glyphs + whitespace).

    When a fragment spans two adjacent sentences (split at a period mid-quote),
    we also try joining sentence[i] + sentence[i+1] and return sentence[i]
    as the anchor with the merged text as evidence_quote.
    """
    for frag in fragments:
        frag_lower = _normalize_for_match(frag).lower()

        # Pass 1: single-sentence match
        for idx, (score, src_named, tgt_named, lineno, sent_text) in enumerate(scored):
            sent_norm = _normalize_for_match(sent_text).lower()
            if frag_lower in sent_norm:
                return (idx, lineno, sent_text)

        # Pass 2: adjacent pair (handles sentences split mid-quote on '.')
        for idx in range(len(scored) - 1):
            _, _, _, lineno1, sent1 = scored[idx]
            _, _, _, lineno2, sent2 = scored[idx + 1]
            merged = sent1.rstrip() + " " + sent2.lstrip()
            merged_norm = _normalize_for_match(merged).lower()
            if frag_lower in merged_norm:
                # Use the merged text as evidence_quote; scored[idx] as the anchor
                # We need to return a "virtual" sentence — patch the scored tuple in mind.
                # Return a synthetic tuple: (idx, lineno1, merged_text)
                return (idx, lineno1, merged)

        # Pass 3: try matching just the first half of the fragment (≥15 chars)
        # This handles fragments that are partially truncated in extraction.
        first_half = frag_lower[:max(15, len(frag_lower) // 2)]
        for idx, (score, src_named, tgt_named, lineno, sent_text) in enumerate(scored):
            sent_norm = _normalize_for_match(sent_text).lower()
            if first_half in sent_norm:
                return (idx, lineno, sent_text)

    return None


# Markdown bold/lead-in and trailing annotation patterns for hint cleanup
_HINT_BOLD_RE = re.compile(r"\*\*[^*]+\*\*\s*[—\-–]+\s*")   # **Bold** — or **Bold** -
_HINT_ANNOTATION_RE = re.compile(r"\[[^\]]*\]\s*$")             # trailing [annotation]
_HINT_LEAD_IN_RE = re.compile(r'^[^a-zA-Z"“”]*')      # non-alpha lead-in chars


def _extract_hint_content_words(hint_raw: str) -> set[str]:
    """Extract content words from hint_raw for fuzzy matching, stripping structural markup.

    Removes:
    - **Bold lead-in** — markup (Pass-1 extraction convention for Events)
    - Trailing [annotation] brackets
    - Quoted text already handled by verbatim path

    Returns a set of content words from the remaining text.
    """
    text = hint_raw

    # Strip **Bold lead-in** — or **Bold lead-in** -
    text = _HINT_BOLD_RE.sub("", text)

    # Strip trailing [annotation]
    text = _HINT_ANNOTATION_RE.sub("", text)

    # Strip leading non-alpha junk
    text = _HINT_LEAD_IN_RE.sub("", text)

    # Remove any remaining quoted fragments (those go via verbatim path)
    text = re.sub(r'"[^"]*"', " ", text)
    text = re.sub(r"“[^”]*”", " ", text)

    words = _content_words(text)
    return words


# Minimum fraction of hint content words that must appear in a sentence to count as fuzzy match
_FUZZY_MIN_FRACTION = 0.4
# Minimum absolute number of matching content words (avoids spurious 1/2 matches)
_FUZZY_MIN_HITS = 2


def _find_fuzzy_in_sentences(
    hint_words: set[str],
    scored: list[tuple[float, bool, bool, int, str]],
) -> Optional[tuple[int, int, str]]:
    """Find the sentence whose content words best overlap with hint content words.

    Returns (sentence_index, lineno, sentence_text) if a match clears the
    _FUZZY_MIN_FRACTION threshold, else None.

    Among candidates clearing the threshold, returns the one with the highest
    absolute hit count.
    """
    if not hint_words:
        return None

    best_idx: Optional[int] = None
    best_hits = 0

    for idx, (score, src_named, tgt_named, lineno, sent_text) in enumerate(scored):
        sent_tokens = set(re.findall(r"\b[a-zA-Z]{3,}\b", sent_text.lower()))
        hits = len(hint_words & sent_tokens)
        fraction = hits / len(hint_words)
        if hits >= _FUZZY_MIN_HITS and fraction >= _FUZZY_MIN_FRACTION and hits > best_hits:
            best_hits = hits
            best_idx = idx

    if best_idx is not None:
        _, _, _, lineno, sent_text = scored[best_idx]
        return (best_idx, lineno, sent_text)
    return None


# ---------------------------------------------------------------------------
# Name surface forms extractor (kept for backward-compat with tests)
# ---------------------------------------------------------------------------
def _name_forms(slug: str) -> set[str]:
    """Generate surface forms of a slug for name matching.

    E.g. 'arya-stark' → {'arya', 'stark', 'arya stark', 'arya-stark'}
    """
    forms: set[str] = set()
    parts = slug.split("-")
    forms.add(slug.lower())
    forms.add(slug.replace("-", " ").lower())
    for p in parts:
        if len(p) >= 3:
            forms.add(p.lower())
    return forms


# ---------------------------------------------------------------------------
# Name presence check in text
# ---------------------------------------------------------------------------

def _slug_named_in_text(tokens: frozenset, text_lower: str) -> bool:
    """Return True if any token from tokens appears as a whole word in text_lower."""
    for tok in tokens:
        if re.search(r'\b' + re.escape(tok) + r'\b', text_lower):
            return True
    return False


# ---------------------------------------------------------------------------
# Chapter prose reader
# ---------------------------------------------------------------------------
def read_chapter_prose(chapter_path: Path) -> list[tuple[int, str]]:
    """Read a chapter file, skip YAML frontmatter, return (line_number, line_text).

    YAML frontmatter = lines between opening '---' and closing '---'.
    Lines are 1-based.

    Returns list of (line_number, stripped_line) for non-empty prose lines.
    """
    try:
        raw_lines = chapter_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        print(f"  WARNING: Cannot read chapter {chapter_path}: {exc}", file=sys.stderr)
        return []

    # Skip YAML frontmatter
    in_frontmatter = False
    frontmatter_done = False
    prose_lines: list[tuple[int, str]] = []

    for lineno, line in enumerate(raw_lines, start=1):
        stripped = line.strip()
        if lineno == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
                frontmatter_done = True
            continue
        if stripped:
            prose_lines.append((lineno, line))  # Keep original line (don't strip for quote)

    return prose_lines


# ---------------------------------------------------------------------------
# Sentence splitter
# ---------------------------------------------------------------------------
# We use a simple rule: split on sentence-ending punctuation followed by whitespace.
_SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')


def split_into_sentences(prose_lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Split prose lines into sentences, tracking the line number of each sentence's start.

    Returns list of (line_number, sentence_text) where line_number is 1-based and
    refers to the source file line where the sentence began.

    Paragraph boundaries are detected two ways:
    1. A blank/empty line in prose_lines (text == "").
    2. A gap in line numbers > 1 between consecutive prose lines — this catches the
       common case where read_chapter_prose has filtered out blank lines, leaving
       a jump (e.g. line 11 → line 13) that signals a paragraph break.

    All sentences within a paragraph inherit the paragraph's START line number,
    which is the 1-based file line of the paragraph's first text line.
    """
    sentences: list[tuple[int, str]] = []

    current_start_line: int | None = None
    current_text: list[str] = []
    prev_lineno: int | None = None

    def flush_paragraph():
        nonlocal current_start_line, current_text
        if current_text:
            para_text = " ".join(current_text)
            # Split into sentences within the paragraph
            parts = _SENTENCE_SPLIT_RE.split(para_text)
            for part in parts:
                part = part.strip()
                if part:
                    sentences.append((current_start_line, part))
            current_text = []
            current_start_line = None

    for lineno, line in prose_lines:
        text = line.strip()
        if not text:
            # Explicit blank line sentinel → flush current paragraph
            flush_paragraph()
            prev_lineno = lineno
            continue
        # Detect paragraph boundary from a line-number gap (blank lines filtered upstream)
        if prev_lineno is not None and lineno > prev_lineno + 1 and current_text:
            flush_paragraph()
        if current_start_line is None:
            current_start_line = lineno
        current_text.append(text)
        prev_lineno = lineno

    flush_paragraph()
    return sentences


# ---------------------------------------------------------------------------
# Evidence locator
# ---------------------------------------------------------------------------
# Minimum score threshold to qualify as a verbatim match.
# Score = (name_hits * 2 + content_word_hits) / max(total_query_terms, 1)
# We require at least 0.15 (roughly: at least 1 content match in a 6-term query).
_MIN_SCORE_THRESHOLD = 0.15


def locate_evidence(
    candidate: dict,
    chapter_path: Path,
) -> dict:
    """Find the best verbatim passage in the chapter prose for a candidate.

    v2 algorithm:
      1. Score each sentence for source/target name presence + content words.
      2. PREFER a single sentence naming BOTH endpoints.
      3. If no single sentence names both, try a sliding window of up to
         BOTH_NAMED_WINDOW_SENTENCES consecutive sentences centred on the
         best-scoring sentence.  Emit the window text if it names both.
      4. Fall back to the best-scoring single sentence (old behaviour).
      5. If nothing clears _MIN_SCORE_THRESHOLD, chapter-level fallback.

    Returns a dict with keys added to the candidate:
      evidence_quote   — verbatim quote (or [PARAPHRASE] fallback)
      evidence_ref     — 'sources/chapters/{book}/{chapter}.md[:lineno]'
      locate_status    — 'verbatim' | 'chapter-level'  (unchanged from v1)
      locate_quality   — 'both-named' | 'one-named' | 'nearest-fallback' | 'chapter-level'

    locate_quality semantics:
      both-named      — quote window names BOTH source and target
      one-named       — best sentence names exactly ONE endpoint
      nearest-fallback — best sentence names NEITHER endpoint (content match only)
      chapter-level   — no sentence cleared the score threshold

    Known limit (coreference): when an entity appears only as a pronoun or
    relational phrase ("she", "my father") the window expansion cannot recover
    the name.  These cases land as one-named or nearest-fallback, not as
    errors.
    """
    source_slug = candidate["source_slug"]
    target_slug = candidate["target_slug"]
    hint_raw = candidate.get("hint_raw", "")
    evidence_text = candidate.get("evidence_text", "")
    chapter_id = candidate["evidence_chapter"]
    book = candidate["evidence_book"]

    chapter_rel = f"sources/chapters/{book}/{chapter_id}.md"
    chapter_ref_base = chapter_rel  # without line suffix

    # Build query terms: name surface forms + content words from evidence + hint
    source_forms = _name_forms(source_slug)
    target_forms = _name_forms(target_slug)
    evidence_content_words = _content_words(f"{evidence_text} {hint_raw}")

    all_query_terms = source_forms | target_forms | evidence_content_words
    n_query = max(len(all_query_terms), 1)

    # Alias-aware tokens for both-named preference (uses filter module if available)
    src_tokens = get_slug_tokens(source_slug)
    tgt_tokens = get_slug_tokens(target_slug)

    # Read prose
    prose_lines = read_chapter_prose(chapter_path)
    if not prose_lines:
        fallback_quote = f"[PARAPHRASE] {evidence_text}" if evidence_text else ""
        return {
            "evidence_quote": fallback_quote,
            "evidence_ref": chapter_ref_base,
            "locate_status": "chapter-level",
            "locate_quality": "chapter-level",
            "quote_source": "chapter-level",
        }

    sentences = split_into_sentences(prose_lines)
    if not sentences:
        fallback_quote = f"[PARAPHRASE] {evidence_text}" if evidence_text else ""
        return {
            "evidence_quote": fallback_quote,
            "evidence_ref": chapter_ref_base,
            "locate_status": "chapter-level",
            "locate_quality": "chapter-level",
            "quote_source": "chapter-level",
        }

    # -----------------------------------------------------------------------
    # Step 1: Score every sentence
    # -----------------------------------------------------------------------
    # Per sentence: (score, src_named, tgt_named, lineno, sent_text)
    scored: list[tuple[float, bool, bool, int, str]] = []

    for lineno, sent_text in sentences:
        sent_lower = sent_text.lower()
        sent_tokens = set(re.findall(r"\b[a-zA-Z]{2,}\b", sent_lower))

        # Name hits using legacy _name_forms (for the overall score)
        name_hits = 0
        for form in source_forms:
            if form in sent_lower:
                name_hits += 1
                break
        for form in target_forms:
            if form in sent_lower:
                name_hits += 1
                break

        # Content word hits
        content_hits = len(evidence_content_words & sent_tokens)

        score = (name_hits * 2 + content_hits) / n_query

        # Alias-aware both-named check
        src_named = _slug_named_in_text(src_tokens, sent_lower) if src_tokens else (name_hits >= 1)
        tgt_named = _slug_named_in_text(tgt_tokens, sent_lower) if tgt_tokens else (name_hits == 2)

        # Fallback: if tokens are empty (rare), use legacy _name_forms check
        if not src_tokens:
            src_named = any(form in sent_lower for form in source_forms)
        if not tgt_tokens:
            tgt_named = any(form in sent_lower for form in target_forms)

        scored.append((score, src_named, tgt_named, lineno, sent_text))

    if not scored:
        fallback_quote = f"[PARAPHRASE] {evidence_text}" if evidence_text else ""
        return {
            "evidence_quote": fallback_quote,
            "evidence_ref": chapter_ref_base,
            "locate_status": "chapter-level",
            "locate_quality": "chapter-level",
            "quote_source": "chapter-level",
        }

    # -----------------------------------------------------------------------
    # Path A: hint-verbatim — search for quoted fragments from hint_raw
    # -----------------------------------------------------------------------
    hint_fragments = _extract_hint_verbatim_fragments(hint_raw)
    if hint_fragments:
        found = _find_verbatim_in_sentences(hint_fragments, scored)
        if found is not None:
            sent_idx, match_lineno, match_sent = found
            # Re-evaluate naming from the actual match_sent (may be a merged pair)
            match_lower = match_sent.lower()
            sent_src_named = _slug_named_in_text(src_tokens, match_lower) if src_tokens \
                else any(form in match_lower for form in source_forms)
            sent_tgt_named = _slug_named_in_text(tgt_tokens, match_lower) if tgt_tokens \
                else any(form in match_lower for form in target_forms)
            if sent_src_named and sent_tgt_named:
                lq = "hint-anchored-both-named"
            elif sent_src_named or sent_tgt_named:
                lq = "hint-anchored-one-named"
            else:
                lq = "hint-anchored-none"
            return {
                "evidence_quote": match_sent.strip(),
                "evidence_ref": f"{chapter_ref_base}:{match_lineno}",
                "locate_status": "verbatim",
                "locate_quality": lq,
                "quote_source": "hint-verbatim",
            }

    # -----------------------------------------------------------------------
    # Path B: hint-fuzzy — strip markdown / annotations, fuzzy-match hint tokens
    # -----------------------------------------------------------------------
    hint_content_words = _extract_hint_content_words(hint_raw)
    if hint_content_words:
        found = _find_fuzzy_in_sentences(hint_content_words, scored)
        if found is not None:
            sent_idx, match_lineno, match_sent = found
            # Re-evaluate naming from the actual match_sent
            match_lower = match_sent.lower()
            sent_src_named = _slug_named_in_text(src_tokens, match_lower) if src_tokens \
                else any(form in match_lower for form in source_forms)
            sent_tgt_named = _slug_named_in_text(tgt_tokens, match_lower) if tgt_tokens \
                else any(form in match_lower for form in target_forms)
            if sent_src_named and sent_tgt_named:
                lq = "hint-anchored-both-named"
            elif sent_src_named or sent_tgt_named:
                lq = "hint-anchored-one-named"
            else:
                lq = "hint-anchored-none"
            return {
                "evidence_quote": match_sent.strip(),
                "evidence_ref": f"{chapter_ref_base}:{match_lineno}",
                "locate_status": "verbatim",
                "locate_quality": lq,
                "quote_source": "hint-fuzzy",
            }

    # -----------------------------------------------------------------------
    # Path C / Step 2 (fallback): Find best single sentence naming BOTH
    # -----------------------------------------------------------------------
    both_named_candidates = [
        (score, lineno, sent_text)
        for score, src_n, tgt_n, lineno, sent_text in scored
        if src_n and tgt_n and score >= _MIN_SCORE_THRESHOLD
    ]

    if both_named_candidates:
        # Pick highest-scoring both-named sentence
        best_score, best_lineno, best_sentence = max(both_named_candidates, key=lambda x: x[0])
        return {
            "evidence_quote": best_sentence.strip(),
            "evidence_ref": f"{chapter_ref_base}:{best_lineno}",
            "locate_status": "verbatim",
            "locate_quality": "both-named",
            "quote_source": "both-named-window",
        }

    # -----------------------------------------------------------------------
    # Step 3: Find best single sentence regardless of naming
    # -----------------------------------------------------------------------
    best_idx = max(range(len(scored)), key=lambda i: scored[i][0])
    best_score, best_src_named, best_tgt_named, best_lineno, best_sentence = scored[best_idx]

    # -----------------------------------------------------------------------
    # Step 4: Try window expansion around best sentence (up to
    #         BOTH_NAMED_WINDOW_SENTENCES total sentences)
    # -----------------------------------------------------------------------
    if best_score >= _MIN_SCORE_THRESHOLD:
        # Search a window centred on best_idx
        half = BOTH_NAMED_WINDOW_SENTENCES - 1  # sentences before/after
        window_start = max(0, best_idx - half)
        window_end = min(len(scored), best_idx + half + 1)

        # Try all sub-windows of size 1..BOTH_NAMED_WINDOW_SENTENCES
        # that include best_idx, checking if the combined text names both
        best_window_text: Optional[str] = None
        best_window_lineno: int = best_lineno

        for wstart in range(window_start, best_idx + 1):
            for wend in range(best_idx + 1, min(window_end + 1, len(scored) + 1)):
                window_size = wend - wstart
                if window_size > BOTH_NAMED_WINDOW_SENTENCES:
                    continue
                combined_lower = " ".join(
                    scored[i][4].lower() for i in range(wstart, wend)
                )
                window_src_named = _slug_named_in_text(src_tokens, combined_lower) if src_tokens \
                    else any(form in combined_lower for form in source_forms)
                window_tgt_named = _slug_named_in_text(tgt_tokens, combined_lower) if tgt_tokens \
                    else any(form in combined_lower for form in target_forms)

                if window_src_named and window_tgt_named:
                    # Found a window naming both — use it
                    combined_text = " ".join(
                        scored[i][4].strip() for i in range(wstart, wend)
                    )
                    window_lineno = scored[wstart][3]
                    best_window_text = combined_text
                    best_window_lineno = window_lineno
                    break
            if best_window_text is not None:
                break

        if best_window_text is not None:
            return {
                "evidence_quote": best_window_text,
                "evidence_ref": f"{chapter_ref_base}:{best_window_lineno}",
                "locate_status": "verbatim",
                "locate_quality": "both-named",
                "quote_source": "both-named-window",
            }

        # No window names both — fall back to best single sentence
        if best_src_named or best_tgt_named:
            quality = "one-named"
        else:
            quality = "nearest-fallback"

        return {
            "evidence_quote": best_sentence.strip(),
            "evidence_ref": f"{chapter_ref_base}:{best_lineno}",
            "locate_status": "verbatim",
            "locate_quality": quality,
            "quote_source": "nearest-fallback",
        }

    else:
        # Chapter-level fallback: no sentence cleared the score threshold
        fallback_quote = f"[PARAPHRASE] {evidence_text}" if evidence_text else ""
        return {
            "evidence_quote": fallback_quote,
            "evidence_ref": chapter_ref_base,
            "locate_status": "chapter-level",
            "locate_quality": "chapter-level",
            "quote_source": "chapter-level",
        }


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Stage 4 Pass-1-Derived Edge Pipeline — Script 2: evidence locator.\n"
            "Reads Script 1's candidate JSONL files, locates verbatim evidence in\n"
            "chapter prose, and emits final typed edges + untyped tail JSONL files."
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
    parser.add_argument(
        "--book",
        choices=BOOKS,
        default=None,
        metavar="BOOK",
        help="Restrict to one book.",
    )
    parser.add_argument(
        "--chapter-slug",
        default=None,
        metavar="SLUG",
        help="Restrict to one chapter slug (e.g. acok-arya-01).",
    )
    args = parser.parse_args()
    write_output = args.apply

    produced_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    run_date = datetime.now(timezone.utc).strftime("%Y%m%d")

    # -----------------------------------------------------------------------
    # Step 1: Enumerate input candidate JSONL files
    # -----------------------------------------------------------------------
    books_to_scan = [args.book] if args.book else BOOKS

    candidate_files: list[Path] = []
    for book in books_to_scan:
        book_dir = IN_BASE_DIR / book
        if not book_dir.exists():
            continue
        for f in sorted(book_dir.glob("*.candidates.jsonl")):
            chapter_slug = f.name[: -len(".candidates.jsonl")]
            if args.chapter_slug and chapter_slug != args.chapter_slug:
                continue
            candidate_files.append(f)

    print(f"  {len(candidate_files):,} candidate files to process")

    if not candidate_files:
        print("No candidate files found. Run Script 1 (--apply) first.", file=sys.stderr)
        sys.exit(1)

    # -----------------------------------------------------------------------
    # Step 2: Process each chapter
    # -----------------------------------------------------------------------
    count_candidates = 0
    count_typed = 0
    count_untyped = 0
    count_verbatim = 0
    count_chapter_level = 0

    # locate_quality distribution (extended with hint-anchored variants)
    quality_counts: dict[str, int] = {
        "both-named": 0,
        "hint-anchored-both-named": 0,
        "hint-anchored-one-named": 0,
        "hint-anchored-none": 0,
        "one-named": 0,
        "nearest-fallback": 0,
        "chapter-level": 0,
    }

    # quote_source distribution
    quote_source_counts: dict[str, int] = {
        "hint-verbatim": 0,
        "hint-fuzzy": 0,
        "both-named-window": 0,
        "nearest-fallback": 0,
        "chapter-level": 0,
    }

    # Per-book stats
    book_stats: dict[str, dict] = {
        b: {"candidates": 0, "typed": 0, "untyped": 0, "verbatim": 0, "chapter_level": 0}
        for b in BOOKS
    }

    # Per-chapter output collections
    chapter_edges: dict[str, tuple[str, list[dict]]] = {}
    chapter_tails: dict[str, tuple[str, list[dict]]] = {}

    for cand_file in candidate_files:
        chapter_slug = cand_file.name[: -len(".candidates.jsonl")]
        book_abbrev = cand_file.parent.name

        # Find corresponding chapter prose file
        chapter_path = CHAPTERS_DIR / book_abbrev / f"{chapter_slug}.md"
        chapter_exists = chapter_path.exists()
        if not chapter_exists:
            print(
                f"  WARNING: Chapter prose not found: {chapter_path}",
                file=sys.stderr,
            )

        # Read candidates
        try:
            candidates = []
            with cand_file.open(encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        candidates.append(json.loads(line))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"  WARNING: Cannot read {cand_file}: {exc}", file=sys.stderr)
            continue

        count_candidates += len(candidates)
        book_stats[book_abbrev]["candidates"] += len(candidates)

        edges_this_chapter: list[dict] = []
        tail_this_chapter: list[dict] = []

        for cand in candidates:
            is_typed = cand.get("edge_type") is not None

            # Locate evidence
            if chapter_exists:
                loc = locate_evidence(cand, chapter_path)
            else:
                # No prose file — chapter-level fallback
                evidence_text = cand.get("evidence_text", "")
                chapter_rel = f"sources/chapters/{book_abbrev}/{chapter_slug}.md"
                loc = {
                    "evidence_quote": f"[PARAPHRASE] {evidence_text}" if evidence_text else "",
                    "evidence_ref": chapter_rel,
                    "locate_status": "chapter-level",
                    "locate_quality": "chapter-level",
                    "quote_source": "chapter-level",
                }

            # Track stats
            if loc["locate_status"] == "verbatim":
                count_verbatim += 1
                book_stats[book_abbrev]["verbatim"] += 1
            else:
                count_chapter_level += 1
                book_stats[book_abbrev]["chapter_level"] += 1

            lq = loc.get("locate_quality", "chapter-level")
            quality_counts[lq] = quality_counts.get(lq, 0) + 1

            qs = loc.get("quote_source", "chapter-level")
            quote_source_counts[qs] = quote_source_counts.get(qs, 0) + 1

            if is_typed:
                count_typed += 1
                book_stats[book_abbrev]["typed"] += 1

                # Build edges row (typed only → emitted as final edge).
                # Fields named to be compatible with wiki-pass2-validate-edge-jsonl.py:
                # - candidate_kind: "pass1_relationship"
                # - evidence_kind: "book-pass1"
                # - asserted_relation: the raw hint text (validator looks for this field)
                # - extraction_file: path to source extraction
                # - confidence_tier: 1 (book-primary source; reviewer may adjust)
                # - evidence_book: book abbreviation
                # Note: v1 emits no `qualifier` field (by design — see architecture.md).
                edge_row = {
                    "decision": "emit_edge",
                    "candidate_kind": "pass1_relationship",
                    "edge_type": cand["edge_type"],
                    "source_slug": cand["source_slug"],
                    "source_resolution_status": cand.get("source_resolution_status"),
                    "target_slug": cand["target_slug"],
                    "target_resolution_status": cand.get("target_resolution_status"),
                    "evidence_kind": "book-pass1",
                    "evidence_book": cand["evidence_book"],
                    "evidence_chapter": cand["evidence_chapter"],
                    "evidence_section": "Relationships Observed",
                    "evidence_quote": loc["evidence_quote"],
                    "evidence_ref": loc["evidence_ref"],
                    "asserted_relation": cand.get("hint_raw", ""),
                    "hint_raw": cand.get("hint_raw", ""),
                    "extraction_file": cand.get("extraction_file", ""),
                    "confidence_tier": 1,
                    "typed_by": cand.get("typed_by"),
                    "corroborates_known_edge": cand.get("corroborates_known_edge", False),
                    "wiki_edge_type": cand.get("wiki_edge_type"),
                    "locate_status": loc["locate_status"],
                    "locate_quality": loc.get("locate_quality", "chapter-level"),
                    "quote_source": loc.get("quote_source", "chapter-level"),
                    "run_id": cand.get("run_id", ""),
                    "schema_version": cand.get("schema_version", ""),
                    "produced_at": cand.get("produced_at", produced_at),
                }
                edges_this_chapter.append(edge_row)

            else:
                count_untyped += 1
                book_stats[book_abbrev]["untyped"] += 1

                # Build tail row (untyped → staged for future LLM pass)
                tail_row = {
                    "decision": "needs_type",
                    "source_slug": cand["source_slug"],
                    "target_slug": cand["target_slug"],
                    "evidence_kind": "book-pass1",
                    "evidence_chapter": cand["evidence_chapter"],
                    "evidence_section": "Relationships Observed",
                    "evidence_quote": loc["evidence_quote"],
                    "evidence_ref": loc["evidence_ref"],
                    "hint_raw": cand.get("hint_raw", ""),
                    "corroborates_known_edge": cand.get("corroborates_known_edge", False),
                    "wiki_edge_type": cand.get("wiki_edge_type"),
                    "locate_status": loc["locate_status"],
                    "locate_quality": loc.get("locate_quality", "chapter-level"),
                    "quote_source": loc.get("quote_source", "chapter-level"),
                    "run_id": cand.get("run_id", ""),
                    "schema_version": cand.get("schema_version", ""),
                    "produced_at": cand.get("produced_at", produced_at),
                }
                tail_this_chapter.append(tail_row)

        if edges_this_chapter:
            chapter_edges[chapter_slug] = (book_abbrev, edges_this_chapter)
        if tail_this_chapter:
            chapter_tails[chapter_slug] = (book_abbrev, tail_this_chapter)

    # -----------------------------------------------------------------------
    # Step 3: Print summary
    # -----------------------------------------------------------------------
    verbatim_pct = 100.0 * count_verbatim / count_candidates if count_candidates else 0.0
    typed_pct = 100.0 * count_typed / count_candidates if count_candidates else 0.0

    print()
    print("=" * 70)
    print("STAGE 4 PASS-1-DERIVED EVIDENCE LOCATOR — RUN SUMMARY")
    print("=" * 70)
    print(f"  Candidate files processed:     {len(candidate_files):>8,}")
    print(f"  Total candidates:              {count_candidates:>8,}")
    print(f"  Typed candidates → edges:      {count_typed:>8,}  ({typed_pct:.1f}%)")
    print(f"  Untyped candidates → tail:     {count_untyped:>8,}  ({100 - typed_pct:.1f}%)")
    print(f"  Verbatim match:                {count_verbatim:>8,}  ({verbatim_pct:.1f}%)")
    print(f"  Chapter-level fallback:        {count_chapter_level:>8,}  ({100 - verbatim_pct:.1f}%)")
    print()

    print("locate_quality distribution:")
    all_quality_keys = [
        "hint-anchored-both-named", "hint-anchored-one-named", "hint-anchored-none",
        "both-named", "one-named", "nearest-fallback", "chapter-level",
    ]
    for q in all_quality_keys:
        n = quality_counts.get(q, 0)
        if n == 0:
            continue
        pct = 100.0 * n / count_candidates if count_candidates else 0.0
        print(f"  {q:<28}  {n:>6,}  ({pct:.1f}%)")
    print()

    print("quote_source distribution:")
    for qs in ["hint-verbatim", "hint-fuzzy", "both-named-window", "nearest-fallback", "chapter-level"]:
        n = quote_source_counts.get(qs, 0)
        if n == 0:
            continue
        pct = 100.0 * n / count_candidates if count_candidates else 0.0
        print(f"  {qs:<22}  {n:>6,}  ({pct:.1f}%)")
    print()

    print("Per-book breakdown:")
    for book in BOOKS:
        if args.book and book != args.book:
            continue
        bs = book_stats[book]
        n = bs["candidates"]
        if n == 0:
            continue
        vb_pct = 100.0 * bs["verbatim"] / n if n else 0.0
        print(
            f"  {book.upper():<6}  candidates={n:,}  "
            f"typed={bs['typed']:,}  untyped={bs['untyped']:,}  "
            f"verbatim={bs['verbatim']:,} ({vb_pct:.1f}%)"
        )
    print()

    # -----------------------------------------------------------------------
    # Step 4: Write outputs (--apply only)
    # -----------------------------------------------------------------------
    if not write_output:
        print("Plan mode — nothing written. Re-run with --apply to write outputs.")
        return

    print("Writing outputs...")

    # 4a. Per-chapter edges JSONL
    edges_files_written = 0
    edges_rows_written = 0
    for chapter_slug, (book_abbrev, edges) in sorted(chapter_edges.items()):
        out_dir = IN_BASE_DIR / book_abbrev
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{chapter_slug}.edges.jsonl"
        with out_file.open("w", encoding="utf-8") as fh:
            for row in edges:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        edges_files_written += 1
        edges_rows_written += len(edges)
    print(f"  {edges_files_written:,} edge files, {edges_rows_written:,} rows")

    # 4b. Per-chapter tail JSONL
    tail_files_written = 0
    tail_rows_written = 0
    for chapter_slug, (book_abbrev, tail_rows) in sorted(chapter_tails.items()):
        out_dir = OUT_TAIL_DIR / book_abbrev
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{chapter_slug}.tail.jsonl"
        with out_file.open("w", encoding="utf-8") as fh:
            for row in tail_rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        tail_files_written += 1
        tail_rows_written += len(tail_rows)
    print(f"  {tail_files_written:,} tail files, {tail_rows_written:,} rows")

    # 4c. Locator stats markdown
    WIKI_DATA_DIR.mkdir(parents=True, exist_ok=True)
    stats_lines = [
        "# Pass-1-Derived: Locator Stats",
        "",
        f"> Generated: {produced_at}  ",
        "",
        "## Overall",
        "",
        "| Metric | Count | % |",
        "|--------|-------|---|",
        f"| Candidate files processed | {len(candidate_files):,} | — |",
        f"| Total candidates | {count_candidates:,} | 100% |",
        f"| Typed → edges | {count_typed:,} | {typed_pct:.1f}% |",
        f"| Untyped → tail | {count_untyped:,} | {100 - typed_pct:.1f}% |",
        f"| Verbatim match | {count_verbatim:,} | {verbatim_pct:.1f}% |",
        f"| Chapter-level fallback | {count_chapter_level:,} | {100 - verbatim_pct:.1f}% |",
        "",
        "## locate_quality Distribution",
        "",
        "| Quality | Count | % |",
        "|---------|-------|---|",
    ]
    for q in ["both-named", "one-named", "nearest-fallback", "chapter-level"]:
        n = quality_counts.get(q, 0)
        pct = 100.0 * n / count_candidates if count_candidates else 0.0
        stats_lines.append(f"| {q} | {n:,} | {pct:.1f}% |")
    stats_lines += [
        "",
        "## Per-Book",
        "",
        "| Book | Candidates | Typed | Untyped | Verbatim | Verbatim% |",
        "|------|------------|-------|---------|---------|-----------|",
    ]
    for book in BOOKS:
        bs = book_stats[book]
        n = bs["candidates"]
        if n == 0:
            continue
        vb_pct = 100.0 * bs["verbatim"] / n if n else 0.0
        stats_lines.append(
            f"| {book.upper()} | {n:,} | {bs['typed']:,} | {bs['untyped']:,} | "
            f"{bs['verbatim']:,} | {vb_pct:.1f}% |"
        )
    OUT_LOCATOR_STATS_MD.write_text("\n".join(stats_lines) + "\n", encoding="utf-8")
    print(f"  Written: {OUT_LOCATOR_STATS_MD}")

    # 4d. Locator stats JSON
    locator_stats = {
        "generated_at": produced_at,
        "total_candidate_files": len(candidate_files),
        "total_candidates": count_candidates,
        "typed_to_edges": count_typed,
        "untyped_to_tail": count_untyped,
        "verbatim_match": count_verbatim,
        "chapter_level_fallback": count_chapter_level,
        "verbatim_pct": round(verbatim_pct, 2),
        "locate_quality": {q: quality_counts.get(q, 0) for q in ["both-named", "one-named", "nearest-fallback", "chapter-level"]},
        "per_book": {book: dict(book_stats[book]) for book in BOOKS},
    }
    OUT_LOCATOR_STATS_JSON.write_text(
        json.dumps(locator_stats, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"  Written: {OUT_LOCATOR_STATS_JSON}")

    print()
    print(f"Done. {edges_rows_written:,} edges written, {tail_rows_written:,} tail rows staged.")
    print(f"  Verbatim match rate: {verbatim_pct:.1f}%")


if __name__ == "__main__":
    main()
