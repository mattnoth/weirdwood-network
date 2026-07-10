#!/usr/bin/env python3
"""fab-lineages-diff.py — deterministic validation diff for the Fire & Blood
"Lineages and Family Tree" appendix (design §3.4, `fire-and-blood-enrichment-design.md`).

PURPOSE (design §3.4, ruling #4): the genealogy is ALREADY in the graph (the
infobox merge shipped dense PARENT_OF/SPOUSE_OF/SIBLING_OF coverage). The
appendix is OCR'd, so it is a **validation corpus**, not an edge source —
never auto-mint kinship from it. This script:
  1. PARSES the split appendix chapter file into candidate kinship triples
     (PARENT_OF / SPOUSE_OF / SIBLING_OF), deterministically, no LLM.
  2. RESOLVES each triple's endpoint names to graph slugs via
     `weirwood_query.resolve` — accepting ONLY exact/hit resolutions.
  3. DIFFS resolved triples against `graph/edges/edges.jsonl` into three
     buckets: confirm (log only) / new (review file) / conflict (PARENT_OF
     only — contradictions report).
  4. Prints a summary (counts, noisiest lines, a random 10-triple sample).

READ-ONLY against the graph — never writes to `graph/` or `sources/`. Writes
only `working/fire-and-blood/lineages-review.jsonl` and
`working/fire-and-blood/lineages-contradictions-report.md`. Pure deterministic
Python, no LLM, no network (`feedback_python_before_agent`).

VOCABULARY (locked): **step** (lowercase) = an ordered piece of work.
**Tier** = confidence 1-5 ONLY (not used by this script — it operates on raw
edge rows, not tier assignment).

WHAT THE SOURCE FILE ACTUALLY CONTAINS (verified against the raw epub —
`sources/raw/fire-and-blood.epub`, `index_split_025.html` — before writing
this parser; see this script's own final-run summary for the write-up):
the split chapter `sources/chapters/fab/fab-lineages-and-family-tree-25.md`
is NOT a set of visual family-tree diagrams (those are raster images in the
print book and were never captured as text by the epub splitter). The
genealogy content it actually holds is a short OCR'd LINE-OF-SUCCESSION LIST
("The Targaryen Succession", garbled to "—to Th Tergaryen Raccession" by the
OCR) of ~20 Targaryen monarchs, each with a one-line descent clause (e.g.
"son of Aegon I and Rhaenys", "Rhaenyra's son", "younger brother of Aegon
III"). A splitter/TOC-anchor bug (the "voodoo conversion" scrambled
`toc.ncx` noted in the design doc §2) also appended the ENTIRE "A
Conversation Between GRRM and Dan Jones" interview transcript to this same
file — that transcript is out of scope for this parser and is explicitly
excluded (bounded out by `INTERVIEW_START_RE`, never scanned for kinship).
A handful of OCR-garbage lines sit between the succession list's last
substantive sentence ("...Trident.") and the interview transcript's real
start; those are counted as `unparsed` (never turned into candidate
triples).

PARSING MODEL
  The succession list is NOT column/table-structured OCR text — it is a
  flat run of "<start>-<end> <RegnalName>[<numeral>] <descent clause>"
  entries, and (per the design doc's OCR-quirks §2) NOT reliably line-broken
  (an entry's trailing epithet clause and the NEXT entry's year-range+name
  sometimes share one physical OCR line, e.g. "the Conqueror, the Dragon
  37-42 AenysI"). So this parser does NOT split on physical lines at all —
  it joins the whole succession-list region into one character stream
  (tracking a char-offset -> original-line-number map for citation),
  regex-matches every "<NNN-NNN> <Name>" entry HEADER in that stream, and
  treats the span between one header and the next as that entry's
  descriptor text. This is robust to the physical line-break noise and
  naturally absorbs a genuinely-observed duplicated-running-header artifact
  ("A Conversation Between George R. R. Martin and / Dan Jones" injected
  mid-descriptor inside the Aegon IV entry) as harmless noise inside a
  descriptor span, rather than corrupting entry boundaries.

  Per entry, kinship clauses are extracted from the descriptor (after
  stripping `[...]`/`(...)` narrative asides and honorific titles):
    - "son/daughter of X [and Y]"           -> PARENT_OF(X, entry) [+ PARENT_OF(Y, entry)]
    - "X's [[qualifier] son/daughter]"      -> PARENT_OF(X, entry)   (possessive form)
    - "m. X"                                -> SPOUSE_OF(entry, X)  (never fires on this
                                                file — no "m." marriages appear in the
                                                actual succession-list text — kept for
                                                robustness/future lineage-appendix reuse)
    - "[younger/elder] brother/sister of X" -> SIBLING_OF(entry, X), ONLY IF X's OWN
                                                descriptor already yielded at least one
                                                explicit PARENT_OF parent (the "directly
                                                derivable from a shared explicit parent
                                                entry" rule) AND the clause is not
                                                qualified "half-" (no HALF_SIBLING_OF type
                                                exists in the locked vocab — skipped, not
                                                silently downgraded to a full sibling claim)
    - "grandson/granddaughter of X"         -> SKIPPED (not a direct PARENT_OF degree)
    - "by X or Y" (disputed second parent)  -> SKIPPED (ambiguous parentage — never guess
                                                which of two named candidates is correct;
                                                e.g. Daeron II "Naerys's son, by Aegon or
                                                Aemon" only yields the certain parent,
                                                Naerys)

RESOLUTION (weirwood_query.resolve, exact/hit ONLY — `feedback_no_graph_mutation_without_goahead`
adjacent caution: never guess for kinship)
  A bare regnal name in this OCR'd table never carries the "Targaryen"
  surname (it's implied by the table's own title) — e.g. "son of Aegon I and
  Rhaenys", not "son of Aegon I Targaryen and Rhaenys Targaryen". Verified
  (see this file's smoke output): `resolve("Aegon I")` MISSES; the graph's
  alias table only has the full "Aegon I Targaryen" phrase indexed. So this
  script tries each candidate name AS-IS, then with " Targaryen" appended,
  accepting ONLY `hit` / `hit-character` status with a SINGLE exact
  candidate. This is a name-VARIANT retry (using the appendix's own,
  stated subject — "the Targaryen Succession" — as disambiguating context),
  not a guess about who anyone's parents are.

  **Verified trap (do not remove this guard):** `resolve("Viserys
  Targaryen")` returns a CONFIDENT single hit-character onto
  `viserys-targaryen` — but that slug is Viserys III (Dany's brother, "the
  Beggar King", 276-298 AC), NOT either of this appendix's two bare-"Viserys"
  mentions (Viserys I, Aegon II's father; presumably Viserys II, Aegon IV's
  father) — a genuine same-surname cross-era collision the resolver's
  candidate-count check does NOT catch (there is exactly one exact-alias
  hit; the collision is invisible to `resolve()` itself, only visible by
  cross-checking the graph's OTHER Targaryen nodes). This script therefore
  builds its own royal-numeral collision map from `graph/nodes/characters/
  *-targaryen*.node.md` slugs (e.g. "viserys" -> {i, ii} because both
  `viserys-i-targaryen.node.md` and `viserys-ii-targaryen.node.md` exist)
  and REFUSES the "+Targaryen" retry for any BARE (non-numeralled) captured
  name whose given name has >=2 differently-numeralled slugs on record —
  routing it to `unresolved-name` instead of a silent wrong match. Non-royal
  consort names (Rhaenys, Visenya, Naerys, Rhaenyra, ...) are NOT blocked by
  this guard even though some of them ALSO have multiple same-name graph
  nodes (e.g. three "Rhaenys Targaryen"s across three eras) — those other
  nodes use disambiguated slugs (`rhaenys-targaryen-daughter-of-rhaegar`,
  not a second `-i-`/`-ii-` numeralled slug), so they never collide with the
  bare "Rhaenys Targaryen" alias the way `-i-`/`-ii-` royal slugs do; see
  the docstring above for why this is a narrower, evidence-backed guard
  rather than a blanket "block every reused name" rule.

DIFF (`graph/edges/edges.jsonl`, edge_type in PARENT_OF/SPOUSE_OF/SIBLING_OF)
  - confirm: triple already present (directed match for PARENT_OF, either-
    direction match for the symmetric SPOUSE_OF/SIBLING_OF) -> counted only.
  - new: triple absent -> full row appended to
    `working/fire-and-blood/lineages-review.jsonl` (never auto-minted).
  - conflict (PARENT_OF only): the child already has >=2 DISTINCT existing
    PARENT_OF sources on record and the appendix's parent is neither of them
    (conservative -- a child can have 2 parent slots, so a single existing
    parent that merely differs from the appendix's is `new`, not `conflict`)
    -> `working/fire-and-blood/lineages-contradictions-report.md`.

INTERFACE
  python3 scripts/fab-lineages-diff.py [--source FILE] [--edges FILE]
      [--review-out FILE] [--contradictions-out FILE] [--nodes-root DIR]
      [--limit N] [--seed N]

  --limit N   Parse only the first N succession-list entries (quick test
              runs). Default: all.
  --seed N    RNG seed for the "10 random sample triples" stdout printout
              (reproducible). Default: 42.

Never writes to `graph/` or `sources/`. Reads `graph/edges/edges.jsonl` and
`graph/nodes/characters/*.node.md` read-only, and (via `weirwood_query`)
`working/wiki/data/*-lookup.json` read-only.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = REPO / "sources" / "chapters" / "fab" / "fab-lineages-and-family-tree-25.md"
DEFAULT_EDGES = REPO / "graph" / "edges" / "edges.jsonl"
DEFAULT_REVIEW_OUT = REPO / "working" / "fire-and-blood" / "lineages-review.jsonl"
DEFAULT_CONTRADICTIONS_OUT = REPO / "working" / "fire-and-blood" / "lineages-contradictions-report.md"
DEFAULT_NODES_ROOT = REPO / "graph" / "nodes"

if str(REPO / "graph" / "query") not in sys.path:
    sys.path.insert(0, str(REPO / "graph" / "query"))
from weirwood_query.load import load_alias_collisions, load_alias_lookup, load_all_node_index  # noqa: E402
from weirwood_query.resolve import resolve as _wq_resolve  # noqa: E402

KINSHIP_TYPES = ("PARENT_OF", "SPOUSE_OF", "SIBLING_OF")
SYMMETRIC_TYPES = ("SPOUSE_OF", "SIBLING_OF")


# ---------------------------------------------------------------------------
# Region boundaries within the split chapter file (see module docstring).
# ---------------------------------------------------------------------------
HEADING_RE = re.compile(r"^#\s+Lineages and Family Tree")
GENEALOGY_START_RE = re.compile(r"^Dated by years after Aegon", re.I)
INTERVIEW_START_RE = re.compile(r"^The following questions and answers represent")
TRIDENT_RE = re.compile(r"Trident")

# Entry header: "<NNN>-<NNN> <RegnalName>[<numeral, glued or spaced>]"
ENTRY_HEADER_RE = re.compile(r"(\d{1,3})\s*-\s*(\d{1,3})\s+([A-Z][a-zA-Z|]+(?:\s?[IVXLCDM]{1,4})?)")

NAME_FRAG = r"[A-Z][a-zA-Z|]+(?:\s+(?:[IVXLCDM]{1,4}(?![a-zA-Z])|the\s+[A-Z][a-zA-Z]+))?"

PARENT_SON_OF_RE = re.compile(
    r"\b(?:eldest|youngest|elder|younger|only|second|third|fourth|fifth|sixth|seventh|\d+(?:st|nd|rd|th))?"
    r"\s*(son|daughter)\s+of\s+(" + NAME_FRAG + r")(?:\s+and\s+(" + NAME_FRAG + r"))?"
)
PARENT_POSSESSIVE_RE = re.compile(r"(" + NAME_FRAG + r")['’]s\s+(?:[a-z]+\s+)?(son|daughter)\b")
SIBLING_RE = re.compile(r"\b(younger|elder|elderly)?\s*(brother|sister)\s+of\s+(" + NAME_FRAG + r")")
AMBIGUOUS_PARENT_RE = re.compile(r"\bby\s+(" + NAME_FRAG + r")\s+or\s+(" + NAME_FRAG + r")\b")
GRANDCHILD_RE = re.compile(r"\bgrand(?:son|daughter)\s+of\s+(" + NAME_FRAG + r")")
SPOUSE_RE = re.compile(r"\bm\.\s*(" + NAME_FRAG + r")")

BRACKET_RE = re.compile(r"\[[^\]]*\]")
PAREN_RE = re.compile(r"\([^)]*\)")
TITLE_RE = re.compile(r"\b(?:Queen|King|Prince|Princess|Lord|Lady|Ser|Septon)\s+(?=[A-Z])")

# ocr_suspicion heuristics (task-specified: pipe-in-alpha-token, mixed-case
# mid-word, digit-inside-word; "name absent from graph's known-name set" is
# folded in post-resolution as an extra reason).
PIPE_IN_TOKEN_RE = re.compile(r"[A-Za-z]\s*\|\s*[A-Za-z]")
MIXED_CASE_RE = re.compile(r"\b[A-Za-z]*[a-z][A-Z][A-Za-z]*\b")
DIGIT_IN_WORD_RE = re.compile(r"\b[A-Za-z]+\d+[A-Za-z]*\b|\b[A-Za-z]*\d+[A-Za-z]+\b")

VOWELS = set("aeiouAEIOU")


# ---------------------------------------------------------------------------
# Text cleanup helpers
# ---------------------------------------------------------------------------
def clean_captured_name(raw: str) -> str:
    n = raw.replace("|", "I")
    n = re.sub(r"([a-z])([IVXLCDM]+)$", r"\1 \2", n)
    n = re.sub(r"\s+", " ", n).strip()
    return n.strip(",.;:")


def strip_asides(text: str) -> str:
    return PAREN_RE.sub(" ", BRACKET_RE.sub(" ", text))


def strip_titles(text: str) -> str:
    return TITLE_RE.sub("", text)


def ocr_heuristics(raw_text: str) -> list[str]:
    reasons = []
    if PIPE_IN_TOKEN_RE.search(raw_text):
        reasons.append("pipe-in-token")
    if MIXED_CASE_RE.search(raw_text):
        reasons.append("mixed-case-mid-word")
    if DIGIT_IN_WORD_RE.search(raw_text):
        reasons.append("digit-inside-word")
    return reasons


def is_gibberish_token(tok: str) -> bool:
    letters = [c for c in tok if c.isalpha()]
    if len(letters) < 3:
        return False
    vowel_ratio = sum(1 for c in letters if c in VOWELS) / len(letters)
    max_run, run = 0, 0
    for c in letters:
        if c not in VOWELS:
            run += 1
            max_run = max(max_run, run)
        else:
            run = 0
    return vowel_ratio < 0.2 or max_run >= 5


def line_noise_score(text: str) -> tuple[int, list[str]]:
    """Heuristic OCR-noise score for a single ORIGINAL source line (used for
    the top-10 noisiest-lines report — a softer diagnostic than the
    per-triple ocr_suspicion flag, so it also catches pure-gibberish lines
    with no digit/pipe/mixed-case signal, e.g. 'Monn ie ede SS = ...')."""
    reasons = []
    score = 0
    for reason in ocr_heuristics(text):
        reasons.append(reason)
        score += 2
    tokens = re.findall(r"[A-Za-z]+", text)
    alpha_tokens = [t for t in tokens if len(t) >= 1]
    if alpha_tokens:
        short = sum(1 for t in alpha_tokens if len(t) <= 2)
        if short / len(alpha_tokens) >= 0.25 and len(alpha_tokens) >= 3:
            reasons.append("high-short-token-ratio")
            score += 1
    gibberish = sum(1 for t in tokens if is_gibberish_token(t))
    if gibberish:
        reasons.append(f"gibberish-tokens({gibberish})")
        score += gibberish
    return score, reasons


# ---------------------------------------------------------------------------
# Region extraction + entry parsing
# ---------------------------------------------------------------------------
class Entry:
    def __init__(self, name: str, raw_name: str, start_year: str, end_year: str,
                 header_line: int, header_raw: str):
        self.name = name
        self.raw_name = raw_name
        self.start_year = start_year
        self.end_year = end_year
        self.header_line = header_line
        self.header_raw = header_raw
        self.descriptor_raw = ""
        self.descriptor_lines: list[int] = []
        self.own_parents: list[str] = []  # names, as extracted from this entry's own clause

    @property
    def lines(self) -> list[int]:
        return sorted(set([self.header_line] + self.descriptor_lines))

    @property
    def years(self) -> str:
        return f"{self.start_year}-{self.end_year}"


def build_char_line_map(lines: list[tuple[int, str]]) -> tuple[str, list[int]]:
    """Join (lineno, text) pairs with single-space separators into one blob,
    returning (blob, char_offset -> original_lineno)."""
    parts = []
    char_line: list[int] = []
    for lineno, text in lines:
        if not text.strip():
            continue
        parts.append(text)
        char_line.extend([lineno] * len(text))
        parts.append(" ")
        char_line.append(lineno)
    return "".join(parts), char_line


def lines_for_span(char_line: list[int], start: int, end: int) -> list[int]:
    start = max(0, min(start, len(char_line) - 1))
    end = max(0, min(end, len(char_line)))
    if end <= start:
        return [char_line[start]] if char_line else []
    return sorted(set(char_line[start:end]))


def load_region(source_path: Path) -> dict:
    raw_lines = source_path.read_text(encoding="utf-8").splitlines()
    numbered = list(enumerate(raw_lines, 1))  # (lineno, text)

    heading_idx = next((i for i, (_, t) in enumerate(numbered) if HEADING_RE.match(t)), None)
    if heading_idx is None:
        sys.exit(f"ABORT: could not find '# Lineages and Family Tree' heading in {source_path}")

    interview_idx = next(
        (i for i, (_, t) in enumerate(numbered) if i > heading_idx and INTERVIEW_START_RE.match(t)),
        len(numbered),
    )

    region = numbered[heading_idx + 1: interview_idx]  # (lineno, text) pairs, region of interest
    total_out_of_scope_lines = len(numbered) - len(region) - heading_idx - 1

    # Find the last "Trident" line within the region -> everything after it
    # (up to interview_idx) is trailing OCR-garbage tail, reported as unparsed.
    trident_positions = [i for i, (_, t) in enumerate(region) if TRIDENT_RE.search(t)]
    trident_idx = trident_positions[-1] if trident_positions else len(region) - 1

    genealogy_region = region[: trident_idx + 1]
    tail_region = [(ln, t) for ln, t in region[trident_idx + 1:] if t.strip()]

    return {
        "genealogy_region": genealogy_region,
        "tail_region": tail_region,
        "full_region": region,
        "interview_out_of_scope_lines": total_out_of_scope_lines,
        "interview_start_line": numbered[interview_idx][0] if interview_idx < len(numbered) else None,
    }


def parse_entries(genealogy_region: list[tuple[int, str]], limit: int | None) -> tuple[list[Entry], list[dict]]:
    blob, char_line = build_char_line_map(genealogy_region)
    header_matches = list(ENTRY_HEADER_RE.finditer(blob))

    preamble_lines: list[dict] = []
    if header_matches:
        preamble_text = blob[: header_matches[0].start()].strip()
        if preamble_text:
            preamble_line_nos = lines_for_span(char_line, 0, header_matches[0].start())
            for ln in preamble_line_nos:
                preamble_lines.append({"line": ln, "text": None, "reason": "caption/preamble (non-kinship)"})

    entries: list[Entry] = []
    for i, m in enumerate(header_matches):
        if limit is not None and i >= limit:
            break
        start_year, end_year, raw_name = m.group(1), m.group(2), m.group(3)
        name = clean_captured_name(raw_name)
        header_line = char_line[m.start()] if char_line else 0
        entry = Entry(name, raw_name, start_year, end_year, header_line, blob[m.start():m.end()])

        desc_start = m.end()
        desc_end = header_matches[i + 1].start() if i + 1 < len(header_matches) else len(blob)
        entry.descriptor_raw = blob[desc_start:desc_end].strip()
        entry.descriptor_lines = lines_for_span(char_line, desc_start, desc_end)
        entries.append(entry)

    return entries, preamble_lines


# ---------------------------------------------------------------------------
# Kinship clause extraction
# ---------------------------------------------------------------------------
def extract_clauses(entry: Entry) -> tuple[list[dict], list[dict]]:
    """Returns (triples, skips) for one entry's descriptor. `triples` are
    dicts with kinship_type/source_name/target_name/needs_chain (sibling
    only). `skips` are dicts with reason/detail for review-file transparency
    (not part of the strict PARENT_OF/SPOUSE_OF/SIBLING_OF triple schema)."""
    triples: list[dict] = []
    skips: list[dict] = []
    text = strip_titles(strip_asides(entry.descriptor_raw))

    amb = AMBIGUOUS_PARENT_RE.search(text)
    if amb:
        skips.append({
            "reason": "ambiguous-parentage",
            "detail": f"{clean_captured_name(amb.group(1))} or {clean_captured_name(amb.group(2))}",
            "target": entry.name,
        })

    for m in PARENT_POSSESSIVE_RE.finditer(text):
        parent = clean_captured_name(m.group(1))
        triples.append({"kinship_type": "PARENT_OF", "source_name": parent, "target_name": entry.name})
        entry.own_parents.append(parent)

    for m in PARENT_SON_OF_RE.finditer(text):
        p1 = clean_captured_name(m.group(2))
        triples.append({"kinship_type": "PARENT_OF", "source_name": p1, "target_name": entry.name})
        entry.own_parents.append(p1)
        if m.group(3):
            p2 = clean_captured_name(m.group(3))
            triples.append({"kinship_type": "PARENT_OF", "source_name": p2, "target_name": entry.name})
            entry.own_parents.append(p2)

    gm = GRANDCHILD_RE.search(text)
    if gm:
        skips.append({
            "reason": "non-direct-parent-degree (grandparent, not PARENT_OF)",
            "detail": clean_captured_name(gm.group(1)),
            "target": entry.name,
        })

    for m in SIBLING_RE.finditer(text):
        other_raw = m.group(3)
        window = text[max(0, m.start() - 20): m.start()]
        if "half" in window.lower():
            skips.append({
                "reason": "half-sibling-unsupported-type (no HALF_SIBLING_OF in locked vocab)",
                "detail": clean_captured_name(other_raw),
                "target": entry.name,
            })
            continue
        triples.append({
            "kinship_type": "SIBLING_OF",
            "source_name": entry.name,
            "target_name": clean_captured_name(other_raw),
            "needs_chain": True,
        })

    for m in SPOUSE_RE.finditer(text):
        triples.append({
            "kinship_type": "SPOUSE_OF",
            "source_name": entry.name,
            "target_name": clean_captured_name(m.group(1)),
        })

    return triples, skips


def resolve_sibling_chains(all_triples: list[dict], entry_by_name: dict[str, Entry]) -> list[dict]:
    """Second pass: a SIBLING_OF candidate is only kept if the REFERENCED
    entry (the 'brother of X' target) has at least one explicit parent on
    its OWN record — the 'directly derivable from a shared explicit parent
    entry' rule. Chained-away sibling rows are converted to skip notes."""
    resolved = []
    for t in all_triples:
        if t.get("kinship_type") != "SIBLING_OF" or not t.get("needs_chain"):
            resolved.append(t)
            continue
        ref_entry = entry_by_name.get(t["target_name"])
        if ref_entry is None or not ref_entry.own_parents:
            t = dict(t)
            t["kinship_type"] = None
            t["skip_reason"] = "brother-of-chain: referenced entry has no explicit parent on record"
            resolved.append(t)
            continue
        resolved.append(t)
    return resolved


# ---------------------------------------------------------------------------
# Resolution (name -> slug), with the royal-numeral-collision safety net
# ---------------------------------------------------------------------------
NUMERAL_SLUG_RE = re.compile(r"^(?P<given>[a-z]+)-(?P<numeral>i{1,3}|iv|vi{0,3}|ix|x)-targaryen(?:-.*)?$")
BARE_SLUG_RE = re.compile(r"^(?P<given>[a-z]+)-targaryen$")


def build_royal_ambiguous_givens(nodes_root: Path) -> set[str]:
    """Given names where BOTH (a) a bare `<given>-targaryen` character slug
    AND (b) at least one numeralled `<given>-<numeral>-targaryen` slug exist
    on record (e.g. 'viserys' -> viserys-targaryen (Viserys III, bare) AND
    viserys-i-targaryen/viserys-ii-targaryen both exist). The '+Targaryen'
    retry (see module docstring 'Verified trap') only ever tries the BARE
    surname-appended phrase, so it will always land on slug (a) if it
    exists -- silently, and possibly wrongly, since the appendix's bare
    mention (no numeral in the OCR'd text) is exactly the situation where we
    can't tell whether (a) or one of the (b) kings is meant. Only the
    '+Targaryen' RETRY is guarded by this set -- an AS-WRITTEN name that
    already resolves cleanly on its own (e.g. 'Aegon the Unlikely', a full
    unique epithet) is trusted without this check."""
    numbered: dict[str, set[str]] = defaultdict(set)
    bare: set[str] = set()
    char_dir = nodes_root / "characters"
    if not char_dir.exists():
        return set()
    for f in char_dir.glob("*.node.md"):
        slug = f.name[: -len(".node.md")]
        if "targaryen" not in slug:
            continue
        m = NUMERAL_SLUG_RE.match(slug)
        if m:
            numbered[m.group("given")].add(m.group("numeral"))
            continue
        m2 = BARE_SLUG_RE.match(slug)
        if m2:
            bare.add(m2.group("given"))
    return {g for g in bare if g in numbered}


def has_numeral(name: str) -> bool:
    return bool(re.search(r"\b[IVXLCDM]{1,4}\b", name))


REDIRECT_RE = re.compile(r"^redirect_to:\s*(\S+)", re.M)


def build_redirect_map(nodes_root: Path) -> dict[str, str]:
    """{slug -> canonical_slug} for character nodes that are thin redirect
    stubs (`redirect_to:` frontmatter). resolve() can return the STUB's own
    slug (a real, single, exact alias hit) when a bare/short given name
    happens to collide with a redirect page's canonical alias string (e.g.
    'Aenys Targaryen' hits the `aenys-targaryen` stub, not the real
    `aenys-i-targaryen` king) -- those stub slugs carry NO edges of their
    own in `edges.jsonl`, so diffing against them would falsely read as
    'new'/'conflict' instead of matching the real, edge-bearing canonical
    node. Always resolve through this map before diffing."""
    redirect_map: dict[str, str] = {}
    char_dir = nodes_root / "characters"
    if not char_dir.exists():
        return redirect_map
    for f in char_dir.glob("*.node.md"):
        slug = f.name[: -len(".node.md")]
        text = f.read_text(encoding="utf-8", errors="replace")
        m = REDIRECT_RE.search(text)
        if m:
            redirect_map[slug] = m.group(1).strip()
    return redirect_map


class Resolver:
    def __init__(self, nodes_root: Path):
        self.lookup = load_alias_lookup()
        self.all_node_index = load_all_node_index()
        self.collisions = load_alias_collisions()
        self.royal_ambiguous_givens = build_royal_ambiguous_givens(nodes_root)
        self.redirect_map = build_redirect_map(nodes_root)
        self._cache: dict[str, tuple[str | None, str, str]] = {}

    def resolve(self, raw_name: str) -> tuple[str | None, str, str]:
        """Returns (slug_or_None, status, reason). status in
        {'resolved', 'unresolved-name'}."""
        if raw_name in self._cache:
            return self._cache[raw_name]

        name = clean_captured_name(raw_name)
        if not name:
            result = (None, "unresolved-name", "empty-name")
            self._cache[raw_name] = result
            return result

        given = name.split()[0].lower()
        is_retry_variant = {name: False}
        variants = [name] if name.endswith("Targaryen") else [name, f"{name} Targaryen"]
        if len(variants) > 1:
            is_retry_variant[variants[1]] = True
        guard_blocked_retry = False

        for variant in variants:
            # The royal-numeral-collision guard applies ONLY to the invented
            # '+Targaryen' retry, never to the name as literally written in
            # the source text (see build_royal_ambiguous_givens docstring).
            if is_retry_variant.get(variant) and not has_numeral(name) and given in self.royal_ambiguous_givens:
                guard_blocked_retry = True
                continue
            slug, status, candidates = _wq_resolve(
                variant, lookup=self.lookup, all_node_index=self.all_node_index,
                collisions=self.collisions)
            if status in ("hit", "hit-character") and slug:
                if len(candidates) > 1:
                    result = (None, "unresolved-name", f"multi-candidate-exact-hit:{variant!r}")
                    self._cache[raw_name] = result
                    return result
                canonical = self.redirect_map.get(slug, slug)
                reason = f"matched:{variant!r}" if canonical == slug else f"matched:{variant!r}->redirect:{slug}"
                result = (canonical, "resolved", reason)
                self._cache[raw_name] = result
                return result

        reason = "bare-name-in-ambiguous-royal-cluster" if guard_blocked_retry else "no-hit"
        result = (None, "unresolved-name", reason)
        self._cache[raw_name] = result
        return result


# ---------------------------------------------------------------------------
# Edge diff
# ---------------------------------------------------------------------------
def load_kinship_edges(edges_path: Path) -> list[dict]:
    edges = []
    if not edges_path.exists():
        sys.exit(f"ABORT: --edges file not found: {edges_path}")
    with edges_path.open(encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if row.get("edge_type") in KINSHIP_TYPES:
                edges.append(row)
    return edges


class EdgeIndex:
    def __init__(self, edges: list[dict]):
        self.directed: set[tuple[str, str, str]] = set()
        self.parents_of: dict[str, set[str]] = defaultdict(set)
        self.parent_edge_rows: dict[str, list[dict]] = defaultdict(list)
        self.symmetric_pairs: dict[tuple[str, frozenset], list[dict]] = defaultdict(list)
        for e in edges:
            et, s, t = e.get("edge_type"), e.get("source_slug"), e.get("target_slug")
            if not (et and s and t):
                continue
            self.directed.add((et, s, t))
            if et == "PARENT_OF":
                self.parents_of[t].add(s)
                self.parent_edge_rows[t].append(e)
            else:
                self.symmetric_pairs[(et, frozenset((s, t)))].append(e)

    def diff(self, kinship_type: str, source_slug: str, target_slug: str) -> tuple[str, dict]:
        if kinship_type == "PARENT_OF":
            if (kinship_type, source_slug, target_slug) in self.directed:
                return "confirm", {}
            existing = self.parents_of.get(target_slug, set())
            if len(existing) >= 2 and source_slug not in existing:
                return "conflict", {
                    "existing_parents": sorted(existing),
                    "existing_parent_edges": self.parent_edge_rows.get(target_slug, []),
                }
            return "new", {}
        # symmetric: SPOUSE_OF / SIBLING_OF
        key = (kinship_type, frozenset((source_slug, target_slug)))
        if self.symmetric_pairs.get(key):
            return "confirm", {}
        return "new", {}


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------
def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def write_contradictions_report(path: Path, conflicts: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Fire & Blood Lineages appendix -- kinship contradictions",
        "",
        f"Generated by `scripts/fab-lineages-diff.py` -- {len(conflicts)} conflict(s) found.",
        "",
        "Deterministic diff of the Lineages/Family Tree appendix (section 025, the OCR'd",
        "line-of-succession list) against existing PARENT_OF kinship edges in",
        "`graph/edges/edges.jsonl`. A conflict fires ONLY when the child already has >=2",
        "DISTINCT existing parents on record and the appendix's parent is neither of them",
        "(conservative -- a child can have 2 parent slots, so one differing existing parent",
        "routes to `new`, not `conflict`). Never auto-applied -- for human review.",
        "",
    ]
    if not conflicts:
        lines.append("_No conflicts found in this run._")
    for c in conflicts:
        lines.append(f"## {c['target_name']} ({c['target_slug']})")
        lines.append("")
        lines.append(f"- **Appendix claim:** `{c['source_name']}` ({c['source_slug']}) PARENT_OF "
                      f"`{c['target_name']}` -- source line(s) {c['source_lines']}")
        lines.append(f"  - descriptor: \"{c['descriptor_raw'][:200]}\"")
        lines.append(f"- **Graph says instead:** existing parents = {', '.join(c['existing_parents'])}")
        for pe in c["existing_parent_edges"]:
            lines.append(
                f"  - `{pe.get('source_slug')}` -> `{c['target_slug']}` "
                f"(evidence_kind={pe.get('evidence_kind')}, run_id={pe.get('run_id', 'n/a')}, "
                f"evidence_ref={pe.get('evidence_ref', 'n/a')})"
            )
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    ap.add_argument("--edges", type=Path, default=DEFAULT_EDGES)
    ap.add_argument("--review-out", type=Path, default=DEFAULT_REVIEW_OUT)
    ap.add_argument("--contradictions-out", type=Path, default=DEFAULT_CONTRADICTIONS_OUT)
    ap.add_argument("--nodes-root", type=Path, default=DEFAULT_NODES_ROOT)
    ap.add_argument("--limit", type=int, default=None, help="parse only the first N succession-list entries")
    ap.add_argument("--seed", type=int, default=42, help="RNG seed for the 10-random-triple sample printout")
    args = ap.parse_args()

    if not args.source.exists():
        sys.exit(f"ABORT: --source file not found: {args.source}")

    region = load_region(args.source)
    entries, preamble_lines = parse_entries(region["genealogy_region"], args.limit)
    entry_by_name = {e.name: e for e in entries}

    all_clause_triples: list[dict] = []
    all_skips: list[dict] = []
    for e in entries:
        triples, skips = extract_clauses(e)
        for t in triples:
            t["entry_name"] = e.name
            t["entry_years"] = e.years
        for s in skips:
            s["entry_name"] = e.name
            s["entry_years"] = e.years
        all_clause_triples.extend(triples)
        all_skips.extend(skips)

    all_clause_triples = resolve_sibling_chains(all_clause_triples, entry_by_name)

    parsed_triples = [t for t in all_clause_triples if t.get("kinship_type")]
    chain_dropped = [t for t in all_clause_triples if not t.get("kinship_type")]
    for t in chain_dropped:
        all_skips.append({
            "reason": t.get("skip_reason", "sibling-chain-dropped"),
            "detail": t.get("target_name"),
            "target": t.get("entry_name"),
        })

    resolver = Resolver(args.nodes_root)
    edges = load_kinship_edges(args.edges)
    idx = EdgeIndex(edges)

    review_rows: list[dict] = []
    conflicts: list[dict] = []
    bucket_counts: Counter = Counter()
    resolved_count = 0
    unresolved_count = 0
    sample_pool: list[dict] = []

    for t in parsed_triples:
        entry = entry_by_name[t["entry_name"]]
        source_slug, source_status, source_reason = resolver.resolve(t["source_name"])
        target_slug, target_status, target_reason = resolver.resolve(t["target_name"])

        ocr_reasons = ocr_heuristics(entry.header_raw) + ocr_heuristics(entry.descriptor_raw)
        ocr_reasons = sorted(set(ocr_reasons))

        base_row = {
            "kinship_type": t["kinship_type"],
            "source_name": t["source_name"],
            "target_name": t["target_name"],
            "source_slug": source_slug,
            "target_slug": target_slug,
            "entry_name": entry.name,
            "entry_years": entry.years,
            "source_lines": entry.lines if t["kinship_type"] != "SIBLING_OF"
                            else sorted(set(entry.lines + entry_by_name.get(t["target_name"], entry).lines)),
            "descriptor_raw": entry.descriptor_raw[:300],
        }

        if source_status != "resolved" or target_status != "resolved":
            unresolved_count += 1
            unresolved_names = []
            if source_status != "resolved":
                unresolved_names.append({"name": t["source_name"], "reason": source_reason})
            if target_status != "resolved":
                unresolved_names.append({"name": t["target_name"], "reason": target_reason})
            row = dict(base_row)
            row["kind"] = "unresolved-name"
            row["unresolved_names"] = unresolved_names
            row["ocr_suspicion"] = bool(ocr_reasons) or True  # unresolved names are inherently suspect
            row["ocr_suspicion_reasons"] = sorted(set(ocr_reasons + ["name-unresolved"]))
            review_rows.append(row)
            bucket_counts["unresolved-name"] += 1
            sample_pool.append(row)
            continue

        resolved_count += 1
        bucket, extra = idx.diff(t["kinship_type"], source_slug, target_slug)
        bucket_counts[bucket] += 1

        row = dict(base_row)
        row["ocr_suspicion"] = bool(ocr_reasons)
        row["ocr_suspicion_reasons"] = ocr_reasons
        sample_pool.append(row)

        if bucket == "confirm":
            continue  # log only, never written
        if bucket == "new":
            row["kind"] = "new"
            review_rows.append(row)
        elif bucket == "conflict":
            row["kind"] = "conflict"
            conflicts.append({
                "target_name": t["target_name"],
                "target_slug": target_slug,
                "source_name": t["source_name"],
                "source_slug": source_slug,
                "source_lines": base_row["source_lines"],
                "descriptor_raw": entry.descriptor_raw,
                "existing_parents": extra["existing_parents"],
                "existing_parent_edges": extra["existing_parent_edges"],
            })

    for s in all_skips:
        row = {
            "kind": "skipped-clause",
            "reason": s["reason"],
            "detail": s.get("detail"),
            "entry_name": s["entry_name"],
            "entry_years": s["entry_years"],
        }
        review_rows.append(row)

    write_jsonl(args.review_out, review_rows)
    write_contradictions_report(args.contradictions_out, conflicts)

    # Noisiest-lines scan (diagnostic; scoped to the same genealogy region +
    # trailing garbage tail the parser actually processes).
    scored_lines = []
    for lineno, text in region["genealogy_region"] + region["tail_region"]:
        if not text.strip():
            continue
        score, reasons = line_noise_score(text)
        if score > 0:
            scored_lines.append((score, lineno, text.strip(), reasons))
    scored_lines.sort(key=lambda r: (-r[0], r[1]))

    unparsed_examples = region["tail_region"][:3]

    print_summary(
        args=args,
        entries=entries,
        preamble_lines=preamble_lines,
        parsed_triples=parsed_triples,
        all_skips=all_skips,
        resolved_count=resolved_count,
        unresolved_count=unresolved_count,
        bucket_counts=bucket_counts,
        conflicts=conflicts,
        scored_lines=scored_lines[:10],
        unparsed_tail=region["tail_region"],
        unparsed_examples=unparsed_examples,
        interview_out_of_scope_lines=region["interview_out_of_scope_lines"],
        sample_pool=sample_pool,
        review_out=args.review_out,
        contradictions_out=args.contradictions_out,
    )


def print_summary(*, args, entries, preamble_lines, parsed_triples, all_skips, resolved_count,
                   unresolved_count, bucket_counts, conflicts, scored_lines, unparsed_tail,
                   unparsed_examples, interview_out_of_scope_lines, sample_pool, review_out,
                   contradictions_out) -> None:
    print("\nFire & Blood Lineages appendix -- validation diff")
    print("=" * 78)
    print(f"source: {args.source}")
    print(f"entries parsed (succession-list monarchs): {len(entries)}"
          + (f" (--limit {args.limit})" if args.limit is not None else ""))
    print(f"candidate kinship triples parsed: {len(parsed_triples)}")
    print(f"skipped clauses (grandson-of / ambiguous-parentage / half-sibling / "
          f"unchainable brother-of): {len(all_skips)}")
    print(f"unparsed tail lines (OCR garbage after the succession list's last substantive "
          f"sentence, before the out-of-scope interview transcript): {len(unparsed_tail)}")
    if unparsed_examples:
        print("  examples:")
        for lineno, text in unparsed_examples:
            print(f"    line {lineno}: {text.strip()!r}")
    print(f"out-of-scope lines skipped entirely (the embedded GRRM/Dan Jones interview "
          f"transcript -- a splitter/TOC-anchor artifact, not genealogy content): "
          f"{interview_out_of_scope_lines}")
    print()
    print(f"resolved endpoints: {resolved_count} triple(s) -- both source+target hit/hit-character")
    print(f"unresolved endpoints: {unresolved_count} triple(s) -- routed to review, never guessed")
    print()
    print("diff buckets (resolved triples only):")
    for b in ("confirm", "new", "conflict"):
        print(f"  {b:10} {bucket_counts.get(b, 0)}")
    print(f"  unresolved-name (written to review, not diffed) {bucket_counts.get('unresolved-name', 0)}")
    print()
    print(f"conflicts found: {len(conflicts)}")
    print()

    print(f"top {len(scored_lines)} noisiest lines (OCR-noise heuristic score, diagnostic):")
    for score, lineno, text, reasons in scored_lines:
        snippet = text if len(text) <= 90 else text[:87] + "..."
        print(f"  score={score:3}  line {lineno:4}  [{','.join(reasons)}]  {snippet!r}")
    print()

    random.seed(args.seed)
    sample_n = min(10, len(sample_pool))
    sample = random.sample(sample_pool, sample_n) if sample_n else []
    print(f"spot-check sample ({sample_n} random triples, seed={args.seed}):")
    for row in sample:
        src = row.get("source_slug") or row["source_name"]
        tgt = row.get("target_slug") or row["target_name"]
        kind = row.get("kind", "confirm/other")
        print(f"  [{kind:16}] {row['source_name']!r:22} --{row['kinship_type']}--> {row['target_name']!r:22}"
              f"  (slugs: {src} -> {tgt})  lines={row['source_lines']}  ocr_suspicion={row['ocr_suspicion']}")
    print()

    print(f"wrote: {review_out} ({sum(1 for _ in review_out.open(encoding='utf-8')) if review_out.exists() else 0} rows)")
    print(f"wrote: {contradictions_out}")
    print("\nDone. Read-only against graph/ and sources/ -- both output files are for human review; "
          "nothing was auto-minted.")


if __name__ == "__main__":
    main()
