#!/usr/bin/env python3
"""fab-dispute-preclassify.py — deterministic pre-classifier for F&B dispute-review rows.

Fire & Blood is written as in-universe history compiled from contradictory
chroniclers (Mushroom, Septon Eustace, Grand Maester Munkun/Orwyle). The F&B
reconciler (`scripts/fab-reconcile-candidates.py`) runs a proximity quarantine:
any proposed edge/event/prose fact whose evidence sits near a hedge term (a
chronicler name or passage-scope divergence framing) is HELD, unquestioned, into
`working/fire-and-blood/apply/<unit>/dispute-review.jsonl` for human/LLM
adjudication. Most holds are FALSE POSITIVES — a flat genealogical fact held
only because a chronicler's name happens to sit in the same paragraph.

This script re-reads every dispute-review.jsonl row and PRE-CLASSIFIES it into
one of four buckets, purely from the row's own fields (chiefly `edge_type` and
its evidence text), so a human only has to hand-adjudicate the genuinely
contested minority:

  1. AUTO_CLEAR (tier-1)    — a flat genealogical/definitional fact caught only
                               by paragraph proximity; the row's own quote has
                               no hedge/rumor verb. Also covers two kind-specific
                               flat cases added S201: a `kind=="prose"` row whose
                               own text has no hedge/attribution cue (a flat
                               low-stakes node-description bullet), and a
                               `kind=="event"` row whose name+quote both lack any
                               ambiguity/hedge cue.
  2. ROMANCE_CLASS          — a LOVER_OF/PARAMOUR_OF-flavored judgment call
                               (edge_type in {LOVER_OF, PARAMOUR_OF}, or the
                               quote itself references a paramour/lover/
                               mistress/"favorite") whose language is genuinely
                               AMBIGUOUS — no flat term and no hedge/euphemism
                               cue in the quote. This is its own bucket (not
                               folded into generic NEEDS_READ) because it is a
                               distinctly-flavored small residual: a human
                               reading these is making a euphemism call, not
                               chasing a KILLS-type proximity false-hold.
                               Unambiguous romance-class rows resolve straight
                               to AUTO_CLEAR (flat term: "paramour", "his/her
                               mistress", "took ... to his/her bed", bare
                               "lover(s)") or AUTO_DISPUTED (euphemism: "the
                               groom's favorite", "close to", "intimate with",
                               "companion" — or any generic hedge verb).
  3. AUTO_DISPUTED (tier-2) — the quote ITSELF (not just its neighborhood)
                               contains a rumor/hedge verb ("it is said",
                               "some claim", "purportedly", "according to X",
                               etc.) — a genuine in-universe dispute, safe to
                               auto-tag disputed with a derived in_universe_source.
  4. NEEDS_READ             — everything else: non-genealogical, non-romance,
                               no explicit hedge verb in its own quote (e.g. a
                               KILLS/BANISHES/ALLIES_WITH edge held only by
                               paragraph proximity). This is the SMALL residual
                               bucket that actually needs a fresh primary-text
                               read (±10 lines) + orchestrator verify. For
                               `kind=="event"` rows (S201) this is also the
                               ONLY dispute-adjacent outcome besides AUTO_CLEAR —
                               an event whose name or quote contains "secret",
                               "alleged", "rumored"/"rumoured", "supposed",
                               "purported", or a hedge/attribution cue ALWAYS
                               lands here, never AUTO_DISPUTED (events are
                               higher-stakes than prose/edge rows — see
                               find_event_ambiguity_match / classify_row).

KIND DISPATCH (S201 — extends auto-resolution to kind=="prose"/"event"; was
edge-only). Originally only `kind=="edge"` rows could reach AUTO_CLEAR (bucket
1 gated on `edge_type`, which prose/event rows never carry) — the 156 prose +
37 event rows in the live corpus ALL fell to NEEDS_READ regardless of content,
overstating the human workload. `kind=="prose"` now reuses the SAME
hedge-verb lexicon (`find_dispute_signal` = find_hedge_match, extended with a
chronicler-opinion attribution check — see CHRONICLER_OPINION_RE) against its
own `text` field: a hedge/attribution cue -> AUTO_DISPUTED (tier-2); no cue ->
AUTO_CLEAR (tier-1, a flat low-stakes node-description bullet). `kind=="event"`
gets its OWN dedicated, more conservative branch (find_event_ambiguity_match):
scans BOTH `name` and `quote` for the higher-stakes ambiguity term list PLUS
the same dispute signal; any hit -> NEEDS_READ (never auto-tagged disputed —
"Secret marriage of Rhaenyra and Daemon"-class beats need a human read); no
hit -> AUTO_CLEAR. Both dispatches run AFTER the existing ROMANCE_CLASS entry
test (bucket 2, unchanged, applies uniformly across kinds).

DESIGN NOTE — reuse, not reinvention. This script imports (read-only, never
calls .main()) `scripts/fab-reconcile-candidates.py` for its LOCKED constants/
helpers: `ROMANCE_EDGE_TYPES` ({"LOVER_OF", "PARAMOUR_OF"}), the
`_CHRONICLER_NAME_TO_SOURCE` chronicler enum, and `derive_in_universe_source()`
(chronicler-in-quote-or-nearby-line -> gyldayn-synthesis fallback). This keeps
the pre-classifier's `in_universe_source` derivation byte-identical in spirit
to what the reconciler itself would compute, instead of a second driftable
copy. It does NOT modify the reconciler, mint/merge, or the extraction prompt.

SPEC DEVIATION (documented, not silent): the task brief that produced this
script named "runciter" as a third chronicler alongside mushroom/eustace.
`scripts/fab-reconcile-candidates.py`'s own locked `IN_UNIVERSE_SOURCE_ENUM`
and `_CHRONICLER_NAME_TO_SOURCE` do NOT include "runciter" — the real enum is
{mushroom, eustace, munkun, orwyle, gyldayn-synthesis, court-record,
unattributed}. "Runciter" does appear in the raw F&B text (he is a named
Grand Maester) but is not yet a mapped in_universe_source anywhere in this
pipeline. Rather than mint a fifth source value the rest of the pipeline
doesn't recognize, this script defers to the reconciler's real enum and falls
back to "gyldayn-synthesis" for any chronicler this pipeline doesn't map yet.
Also dropped for the same reason (requested but not in the locked edge-type
vocabulary per `reference/architecture.md` / `build-edge-type-counts.py`):
DESCENDANT_OF, TWIN_OF — neither edge type exists in the graph's controlled
vocabulary as of 2026-07-09.

USAGE
  python3 scripts/fab-dispute-preclassify.py
  python3 scripts/fab-dispute-preclassify.py --units fab-hour-of-the-wolf-20,fab-the-hooded-hand-21
  python3 scripts/fab-dispute-preclassify.py --units 'fab-the-long-reign*' --sample 3
  python3 scripts/fab-dispute-preclassify.py --out /tmp/preclass-summary.txt

OUTPUT
  working/fire-and-blood/apply/<unit>/dispute-preclass.jsonl  — one row per input
      row: original fields + preclass_bucket / preclass_tier /
      preclass_in_universe_source / preclass_reason.
  A summary table (per-unit + TOTAL counts of the 4 buckets), printed to stdout
      and also written to --out (default: an OS-temp scratchpad location — this
      script never assumes a specific ephemeral CLAUDE-session scratchpad path
      is still valid on a later run; pass --out explicitly to target one).

Never writes to graph/, never touches candidates.json/merge-plan.json/edges.jsonl,
never reads or mutates anything the reconciler itself owns.
"""
from __future__ import annotations

import argparse
import fnmatch
import importlib.util
import json
import re
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_APPLY_DIR = REPO / "working" / "fire-and-blood" / "apply"
DEFAULT_CHAPTERS_DIR = REPO / "sources" / "chapters" / "fab"
ARCHITECTURE_MD = REPO / "reference" / "architecture.md"

# The 4 units already applied to the graph in the S200 smoke batch (see
# working/fire-and-blood/apply/<unit>/ — their dispute-review.jsonl rows are a
# historical record of a run that already went through human adjudication and
# apply). This worklist tool never re-touches them.
EXCLUDED_UNITS = frozenset({
    "fab-aegons-conquest-03",
    "fab-heirs-of-the-dragon-15-p01",
    "fab-heirs-of-the-dragon-15-p02",
    "fab-sons-of-the-dragon-05-p01",
})


# ---------------------------------------------------------------------------
# Reuse the reconciler's locked constants/helpers (read-only import — never
# calls its main(), never writes through it).
# ---------------------------------------------------------------------------
def _load_reconciler():
    spec = importlib.util.spec_from_file_location(
        "fab_reconcile", REPO / "scripts" / "fab-reconcile-candidates.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_RECON = _load_reconciler()
ROMANCE_EDGE_TYPES: frozenset[str] = frozenset(_RECON.ROMANCE_EDGE_TYPES)
IN_UNIVERSE_SOURCE_ENUM: frozenset[str] = frozenset(_RECON.IN_UNIVERSE_SOURCE_ENUM)
derive_in_universe_source = _RECON.derive_in_universe_source
CHRONICLER_NAMES: frozenset[str] = frozenset(_RECON._CHRONICLER_NAME_TO_SOURCE.keys())


# ---------------------------------------------------------------------------
# Bucket 1 — genealogical/definitional edge-type allowlist. Requested set per
# the task spec, filtered against the LOCKED vocabulary (reference/
# architecture.md) — the same mechanical check `build-edge-type-counts.py` runs.
# ---------------------------------------------------------------------------
REQUESTED_GENEALOGICAL_TYPES = [
    "PARENT_OF", "SIBLING_OF", "SPOUSE_OF", "ANCESTOR_OF", "DESCENDANT_OF",
    "UNCLE_OF", "NEPHEW_OF", "COUSIN_OF", "IN_LAW_OF", "STEP_PARENT_OF",
    "STEP_CHILD_OF", "MILK_BROTHER_OF", "HEIR_TO", "SUCCEEDS", "NAMED_AFTER",
    "BONDED_TO", "PROPOSED_AS_BRIDE", "COURTS", "MARRIES_OFF", "TWIN_OF",
]


def load_canonical_edge_types(architecture_path: Path) -> set[str]:
    """Parse the `## Edge Types (Relationship Categories)` section of
    reference/architecture.md the same way scripts/build-edge-type-counts.py
    does: every backtick-wrapped TYPE in the first column of every table row in
    that section. Returns an empty set (never raises) if the file is missing —
    callers fall back to the full requested list rather than crash."""
    if not architecture_path.exists():
        return set()
    lines = architecture_path.read_text(encoding="utf-8").splitlines()
    in_section = False
    types: set[str] = set()
    section_start = re.compile(r"^## Edge Types \(Relationship Categories\)")
    section_end = re.compile(r"^## (?!Edge Types)")
    row_re = re.compile(r"^\|\s*`([A-Z][A-Z0-9_]*)`\s*\|")
    for line in lines:
        if section_start.match(line):
            in_section = True
            continue
        if in_section and section_end.match(line):
            break
        if in_section:
            m = row_re.match(line)
            if m:
                types.add(m.group(1))
    return types


_CANON_EDGE_TYPES = load_canonical_edge_types(ARCHITECTURE_MD)
GENEALOGICAL_TYPES: frozenset[str] = frozenset(
    t for t in REQUESTED_GENEALOGICAL_TYPES if (not _CANON_EDGE_TYPES or t in _CANON_EDGE_TYPES)
)
DROPPED_GENEALOGICAL_TYPES: frozenset[str] = (
    frozenset(REQUESTED_GENEALOGICAL_TYPES) - GENEALOGICAL_TYPES if _CANON_EDGE_TYPES else frozenset()
)


# ---------------------------------------------------------------------------
# Lexicons. Deliberately DISTINCT from (and broader than) the reconciler's own
# HEDGE_TERMS/CERTAINTY_TERMS, which are tuned to decide the QUARANTINE trigger
# itself (strong-only, to avoid over-holding good rows — see its module
# docstring). This runs one level downstream: of rows ALREADY quarantined,
# which ones self-evidently confirm the dispute in their own words?
# ---------------------------------------------------------------------------
HEDGE_VERB_PHRASES = [
    "it is said", "it was said", "some say", "some claim", "it is claimed",
    "purportedly", "reputedly", "rumored", "rumoured", "whispered", "avers",
    "avow", "alleged", "is said to", "can be believed", "would have us believe",
    "claims that", "insists",
]
HEDGE_VERB_REGEXES = [re.compile(r"\baccording to \w+", re.IGNORECASE)]

# Bucket-2 ENTRY condition: edge_type in ROMANCE_EDGE_TYPES, OR the row's own
# evidence text mentions one of these bare terms.
ROMANCE_ENTRY_TERMS = ["paramour", "mistress", "favorite"]
ROMANCE_ENTRY_LOVER_RE = re.compile(r"\blovers?\b", re.IGNORECASE)

# Bucket-2 sub-decision: EUPHEMISM (hedged claim) -> AUTO_DISPUTED.
EUPHEMISM_PHRASES = ["favorite", "close to", "intimate with", "companion"]

# Bucket-2 sub-decision: FLAT term (definite claim) -> AUTO_CLEAR.
FLAT_PHRASES = ["paramour", "his mistress", "her mistress"]
FLAT_BED_RE = re.compile(r"\btook\b.{0,40}?\bto (?:his|her) bed\b", re.IGNORECASE)
FLAT_LOVER_RE = re.compile(r"\blovers?\b", re.IGNORECASE)


def find_hedge_match(text: str) -> str | None:
    """First HEDGE_VERB_PHRASES/regex hit in `text` (case-insensitive), or None."""
    low = text.lower()
    for phrase in HEDGE_VERB_PHRASES:
        if phrase in low:
            return phrase
    for rx in HEDGE_VERB_REGEXES:
        m = rx.search(text)
        if m:
            return m.group(0)
    return None


def find_euphemism_match(text: str) -> str | None:
    low = text.lower()
    for phrase in EUPHEMISM_PHRASES:
        if phrase in low:
            return phrase
    return None


# ---------------------------------------------------------------------------
# Chronicler-opinion attribution (S201 extension — prose/event auto-resolve).
# A named chronicler paired with an opinion/claim VERB in the same clause
# ("Mushroom alone claims", "Eustace tells us", "Munkun tells it differently")
# is a genuine in-universe dispute cue even when it doesn't match the literal
# HEDGE_VERB_PHRASES list (which has "claims that" but not bare "claims";
# "according to \\w+" but not "tells us"). Gated on an ACTUAL chronicler name
# (mushroom/eustace/munkun/orwyle) being present — bare mention of a chronicler's
# BOOK TITLE ("Munkun's True Telling") or a non-chronicler character's own claim
# ("Cregan claimed her hand") never matches, since there's no opinion verb
# adjacent to a chronicler NAME token in those cases. KNOWN LIMITATION
# (documented, not silently patched): an epithet reference to a chronicler
# without their name ("the fool claims...", where "the fool" = Mushroom) is not
# resolved — that requires alias resolution out of scope for this lexicon-only
# extension.
# ---------------------------------------------------------------------------
CHRONICLER_OPINION_VERBS = [
    "claims", "tells", "avers", "aver", "insists", "insist", "maintains",
    "maintain", "believes", "believe", "writes", "says", "would have us believe",
]
CHRONICLER_OPINION_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(n) for n in sorted(CHRONICLER_NAMES)) + r")\b"
    r"[^.]{0,40}?\b(?:" + "|".join(re.escape(v) for v in CHRONICLER_OPINION_VERBS) + r")\b",
    re.IGNORECASE,
)


def find_chronicler_opinion_match(text: str) -> str | None:
    """A named chronicler + opinion/claim verb within the same clause — see
    CHRONICLER_OPINION_RE comment. Additive to find_hedge_match(); callers OR
    the two together (find_dispute_signal)."""
    m = CHRONICLER_OPINION_RE.search(text)
    return m.group(0) if m else None


def find_dispute_signal(text: str) -> str | None:
    """The composite hedge/dispute signal reused everywhere a row's own text is
    checked for an in-universe dispute cue: the SAME phrase/regex lexicon used
    for edges (find_hedge_match), extended with the chronicler-opinion
    attribution check above. A strict superset of find_hedge_match — never turns
    a previously-caught hedge into a miss, only adds catches."""
    return find_hedge_match(text) or find_chronicler_opinion_match(text)


# ---------------------------------------------------------------------------
# Event-kind ambiguity gate (S201 extension). Events are higher-stakes than
# prose bullets — the spec biases toward NEEDS_READ on ANY ambiguity and never
# auto-DISPUTES an event (only AUTO_CLEAR or NEEDS_READ; a genuinely-disputed
# event beat like "Secret marriage of Rhaenyra and Daemon" needs a human read,
# not a mechanical disputed-tag). Checks BOTH `name` and `quote`.
# ---------------------------------------------------------------------------
EVENT_AMBIGUITY_TERMS = ["secret", "alleged", "rumored", "rumoured", "supposed", "purported"]


def find_event_ambiguity_match(name: str, quote: str) -> str | None:
    for text in (name, quote):
        if not text:
            continue
        low = text.lower()
        for term in EVENT_AMBIGUITY_TERMS:
            if term in low:
                return term
        sig = find_dispute_signal(text)
        if sig:
            return sig
    return None


def find_flat_match(text: str) -> str | None:
    low = text.lower()
    for phrase in FLAT_PHRASES:
        if phrase in low:
            return phrase
    m = FLAT_BED_RE.search(text)
    if m:
        return m.group(0)
    m2 = FLAT_LOVER_RE.search(text)
    if m2:
        return m2.group(0)
    return None


def is_romance_entry(edge_type: str | None, text: str) -> bool:
    if edge_type and edge_type in ROMANCE_EDGE_TYPES:
        return True
    low = text.lower()
    if any(term in low for term in ROMANCE_ENTRY_TERMS):
        return True
    return bool(ROMANCE_ENTRY_LOVER_RE.search(text))


def source_from_hedge_term(hedge_term: str | None) -> str | None:
    """Bucket-2 in_universe_source derivation per spec: a real chronicler name
    named in the row's own `hedge_term` field. In the live corpus this rarely
    fires — the reconciler holds EVERY untagged LOVER_OF/PARAMOUR_OF edge
    unconditionally under the sentinel hedge_term "romance-class-untagged"
    (no proximity/chronicler check at all for romance edges), so this is here
    mainly for forward-compatibility / literal spec compliance."""
    if not hedge_term:
        return None
    h = hedge_term.strip().lower()
    return h if h in CHRONICLER_NAMES else None


# ---------------------------------------------------------------------------
# Chapter-line cache (for bucket-3's fuller in_universe_source derivation via
# the reconciler's own derive_in_universe_source, which also checks nearby
# lines — not just the row's own quote fragment).
# ---------------------------------------------------------------------------
_chapter_lines_cache: dict[str, list[str]] = {}


def get_chapter_lines(unit: str, chapters_dir: Path) -> list[str]:
    if unit not in _chapter_lines_cache:
        path = chapters_dir / f"{unit}.md"
        if path.exists():
            _chapter_lines_cache[unit] = path.read_text(encoding="utf-8").splitlines()
        else:
            _chapter_lines_cache[unit] = []
    return _chapter_lines_cache[unit]


# ---------------------------------------------------------------------------
# The classifier itself — pure function, no I/O, easily unit-tested.
# ---------------------------------------------------------------------------
def classify_row(row: dict, chapter_lines: list[str] | None = None) -> dict:
    """Classify one dispute-review.jsonl row. Returns a dict with keys
    preclass_bucket / preclass_tier / preclass_in_universe_source /
    preclass_reason. `chapter_lines` (optional) is the source unit's chapter
    file split on lines (1-based, matching row['line']) — supplying it lets the
    non-romance AUTO_DISPUTED path also check nearby lines for a named
    chronicler (via the reconciler's own derive_in_universe_source), not just
    the row's own quote fragment. Omitting it still classifies correctly; only
    that one in_universe_source loses its nearby-line fallback.

    kind dispatch (S201 extension — prose/event auto-resolve): the ROMANCE_CLASS
    entry test (bucket 2) runs first for every kind, unchanged. kind=="event"
    then gets its OWN dedicated branch (never AUTO_DISPUTED — NEEDS_READ or
    AUTO_CLEAR only, higher-stakes bias). kind in {"edge","prose"} continue
    through the shared hedge-in-own-text bucket (now using the composite
    find_dispute_signal, which also catches chronicler-opinion attribution like
    "Mushroom alone claims"); kind=="edge" then gets the genealogical-type
    AUTO_CLEAR gate; kind=="prose" gets its OWN flat-text AUTO_CLEAR fallback
    (low-stakes node-description bullets); anything left over (kind=="edge" with
    a non-genealogical type and no hedge cue) falls to NEEDS_READ."""
    kind = row.get("kind")
    edge_type = row.get("edge_type")
    text = row.get("quote") or row.get("text") or ""
    name = row.get("name") or ""
    line = row.get("line")
    hedge_term = row.get("hedge_term")

    # --- Bucket 2: ROMANCE_CLASS entry test (all kinds, unchanged) ---
    if is_romance_entry(edge_type, text):
        hedge_hit = find_hedge_match(text)
        euph_hit = find_euphemism_match(text)
        if hedge_hit or euph_hit:
            matched = hedge_hit or euph_hit
            source = source_from_hedge_term(hedge_term) or "gyldayn-synthesis"
            return {
                "preclass_bucket": "AUTO_DISPUTED",
                "preclass_tier": 2,
                "preclass_in_universe_source": source,
                "preclass_reason": f"romance-class hedge/euphemism cue in quote: {matched!r}",
            }
        flat_hit = find_flat_match(text)
        if flat_hit:
            return {
                "preclass_bucket": "AUTO_CLEAR",
                "preclass_tier": 1,
                "preclass_in_universe_source": None,
                "preclass_reason": f"romance-class flat term in quote: {flat_hit!r}",
            }
        return {
            "preclass_bucket": "ROMANCE_CLASS",
            "preclass_tier": None,
            "preclass_in_universe_source": None,
            "preclass_reason": (
                f"romance-class entry (edge_type={edge_type!r}) but no flat/euphemism/"
                "hedge cue found in quote — needs human read"
            ),
        }

    # --- kind == "event": dedicated higher-stakes branch. Never AUTO_DISPUTED —
    # ambiguity anywhere in name OR quote means a human read, not a mechanical tag.
    if kind == "event":
        amb = find_event_ambiguity_match(name, text)
        if amb:
            return {
                "preclass_bucket": "NEEDS_READ",
                "preclass_tier": None,
                "preclass_in_universe_source": None,
                "preclass_reason": (
                    f"event ambiguity cue in name/quote: {amb!r} — higher-stakes kind, "
                    "never auto-resolved past this gate; needs primary-text read"
                ),
            }
        return {
            "preclass_bucket": "AUTO_CLEAR",
            "preclass_tier": 1,
            "preclass_in_universe_source": None,
            "preclass_reason": "event kind: flat name+quote, no secret/alleged/rumored/hedge cue",
        }

    # --- Bucket 3: AUTO_DISPUTED via a hedge/attribution signal in the row's own
    # text (kind in {"edge","prose"} only — event already returned above) ---
    hedge_hit = find_dispute_signal(text)
    if hedge_hit:
        source = derive_in_universe_source(text, chapter_lines or [], line)
        return {
            "preclass_bucket": "AUTO_DISPUTED",
            "preclass_tier": 2,
            "preclass_in_universe_source": source,
            "preclass_reason": f"quote/text contains hedge/rumor verb or chronicler-opinion attribution: {hedge_hit!r}",
        }

    # --- Bucket 1: AUTO_CLEAR — flat genealogical/definitional fact (edge kind) ---
    if edge_type in GENEALOGICAL_TYPES:
        return {
            "preclass_bucket": "AUTO_CLEAR",
            "preclass_tier": 1,
            "preclass_in_universe_source": None,
            "preclass_reason": f"genealogical/definitional edge_type={edge_type}; no hedge verb in quote",
        }

    # --- kind == "prose" fallback: flat node-description bullet, no hedge cue ---
    if kind == "prose":
        return {
            "preclass_bucket": "AUTO_CLEAR",
            "preclass_tier": 1,
            "preclass_in_universe_source": None,
            "preclass_reason": "prose kind: flat node-description text, no hedge/attribution cue",
        }

    # --- Bucket 4: everything else (kind=="edge" non-genealogical, or unknown kind) ---
    return {
        "preclass_bucket": "NEEDS_READ",
        "preclass_tier": None,
        "preclass_in_universe_source": None,
        "preclass_reason": (
            f"kind={kind!r} edge_type={edge_type!r} not genealogical/romance and quote has "
            "no explicit hedge verb — needs primary-text read (±10 lines) + orchestrator verify"
        ),
    }


BUCKETS = ["AUTO_CLEAR", "AUTO_DISPUTED", "ROMANCE_CLASS", "NEEDS_READ"]
KNOWN_KINDS = ["edge", "prose", "event"]  # preferred display order; unknown kinds append sorted, never dropped


def build_kind_bucket_counts(per_unit_rows: dict[str, list[dict]]) -> dict[str, Counter]:
    """Aggregate preclass_bucket counts per row `kind` across ALL units (S201 —
    per-kind breakout). Returns {kind: Counter(bucket -> n)}. A row with a
    missing/unexpected kind value is still counted under its literal value (or
    "?" if absent) rather than silently dropped, so a schema surprise stays
    visible in the summary instead of vanishing from the totals."""
    counts: dict[str, Counter] = defaultdict(Counter)
    for rows in per_unit_rows.values():
        for r in rows:
            counts[r.get("kind") or "?"][r["preclass_bucket"]] += 1
    return counts


# ---------------------------------------------------------------------------
# File I/O / orchestration
# ---------------------------------------------------------------------------
def iter_unit_dirs(apply_dir: Path, units_arg: str | None) -> list[Path]:
    all_names = {p.name: p for p in sorted(apply_dir.iterdir()) if p.is_dir()}

    if units_arg and any(ch in units_arg for ch in "*?["):
        selected_names = [n for n in sorted(all_names) if fnmatch.fnmatch(n, units_arg)]
        if not selected_names:
            print(f"WARNING: --units glob {units_arg!r} matched no unit dirs under {apply_dir}",
                  file=sys.stderr)
    elif units_arg:
        wanted = [u.strip() for u in units_arg.split(",") if u.strip()]
        selected_names = []
        for w in wanted:
            if w not in all_names:
                print(f"WARNING: --units requested {w!r} but no such unit dir exists under {apply_dir}",
                      file=sys.stderr)
                continue
            selected_names.append(w)
    else:
        selected_names = sorted(all_names)

    kept = []
    for name in selected_names:
        if name in EXCLUDED_UNITS:
            print(f"NOTE: {name} is an already-applied smoke unit — permanently excluded", file=sys.stderr)
            continue
        kept.append(all_names[name])
    return kept


def process_unit(unit_dir: Path, chapters_dir: Path) -> tuple[list[dict], Counter, bool]:
    """Returns (classified_rows, bucket_counts, dispute_review_existed)."""
    src = unit_dir / "dispute-review.jsonl"
    if not src.exists():
        return [], Counter(), False

    chapter_lines = get_chapter_lines(unit_dir.name, chapters_dir)
    rows_out: list[dict] = []
    counts: Counter = Counter()
    with src.open(encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"WARNING: {src} line {lineno}: malformed JSON ({e}) — row skipped",
                      file=sys.stderr)
                continue
            result = classify_row(row, chapter_lines)
            out_row = dict(row)
            out_row.update(result)
            rows_out.append(out_row)
            counts[result["preclass_bucket"]] += 1
    return rows_out, counts, True


def default_summary_path() -> Path:
    """A generic, ALWAYS-valid default (OS temp dir) — this script never assumes
    a specific ephemeral CLAUDE-session scratchpad path is still around on a
    later run. Pass --out to target a specific session's scratchpad directory."""
    return Path(tempfile.gettempdir()) / "weirwood-scratchpad" / "p5-preclass-summary.txt"


def build_summary(per_unit_counts: dict[str, Counter], grand_counts: Counter,
                   total_rows: int, zero_row_units: list[str],
                   kind_counts: dict[str, Counter] | None = None) -> str:
    lines = []
    lines.append("Fire & Blood dispute-review pre-classification summary")
    lines.append("=" * 78)
    header = f"{'unit':<44}" + "".join(f"{b:>13}" for b in BUCKETS) + f"{'total':>7}"
    lines.append(header)
    lines.append("-" * len(header))
    for unit in sorted(per_unit_counts):
        c = per_unit_counts[unit]
        row_total = sum(c.get(b, 0) for b in BUCKETS)
        lines.append(f"{unit:<44}" + "".join(f"{c.get(b, 0):>13}" for b in BUCKETS) + f"{row_total:>7}")
    lines.append("-" * len(header))
    lines.append(f"{'TOTAL':<44}" + "".join(f"{grand_counts.get(b, 0):>13}" for b in BUCKETS)
                 + f"{total_rows:>7}")
    lines.append("")

    if kind_counts:
        lines.append("Per-kind breakdown (aggregated across all units, S201)")
        kind_header = f"{'kind':<44}" + "".join(f"{b:>13}" for b in BUCKETS) + f"{'total':>7}"
        lines.append(kind_header)
        lines.append("-" * len(kind_header))
        ordered_kinds = [k for k in KNOWN_KINDS if k in kind_counts] + \
            sorted(k for k in kind_counts if k not in KNOWN_KINDS)
        for k in ordered_kinds:
            c = kind_counts[k]
            row_total = sum(c.get(b, 0) for b in BUCKETS)
            lines.append(f"{k:<44}" + "".join(f"{c.get(b, 0):>13}" for b in BUCKETS) + f"{row_total:>7}")
        lines.append("-" * len(kind_header))
        lines.append(f"{'TOTAL':<44}" + "".join(f"{grand_counts.get(b, 0):>13}" for b in BUCKETS)
                     + f"{total_rows:>7}")
        lines.append("")

    if zero_row_units:
        lines.append(f"({len(zero_row_units)} unit(s) had 0 dispute-review rows — omitted above, "
                      f"empty dispute-preclass.jsonl still written): {', '.join(sorted(zero_row_units))}")
        lines.append("")

    needs_read_n = grand_counts.get("NEEDS_READ", 0)
    romance_n = grand_counts.get("ROMANCE_CLASS", 0)
    auto_n = grand_counts.get("AUTO_CLEAR", 0) + grand_counts.get("AUTO_DISPUTED", 0)
    human_n = needs_read_n + romance_n

    def pct(n: int) -> str:
        return f"{(100.0 * n / total_rows):.1f}%" if total_rows else "n/a"

    lines.append(f"Auto-resolved   (AUTO_CLEAR + AUTO_DISPUTED): {auto_n:>4} / {total_rows} ({pct(auto_n)})")
    lines.append(f"Human workload  (NEEDS_READ + ROMANCE_CLASS): {human_n:>4} / {total_rows} ({pct(human_n)})")
    lines.append(f"  of which NEEDS_READ (fresh primary-text read): {needs_read_n:>4} ({pct(needs_read_n)})")
    lines.append(f"  of which ROMANCE_CLASS (euphemism judgment call): {romance_n:>4} ({pct(romance_n)})")
    if DROPPED_GENEALOGICAL_TYPES:
        lines.append("")
        lines.append(f"NOTE: requested-but-not-in-locked-vocabulary genealogical types dropped: "
                     f"{sorted(DROPPED_GENEALOGICAL_TYPES)}")
    return "\n".join(lines)


def print_samples(per_unit_rows: dict[str, list[dict]], n: int) -> None:
    print(f"\n--- Sample spot-check (deterministic every-k-th, up to {n} rows per bucket) ---")
    by_bucket: dict[str, list[dict]] = defaultdict(list)
    for unit in sorted(per_unit_rows):
        for row in per_unit_rows[unit]:
            by_bucket[row["preclass_bucket"]].append(row)
    for bucket in BUCKETS:
        rows = by_bucket.get(bucket, [])
        if not rows:
            print(f"\n[{bucket}] 0 rows")
            continue
        k = max(1, len(rows) // n)
        sample = rows[::k][:n]
        print(f"\n[{bucket}] {len(rows)} total, showing {len(sample)} (every {k}-th):")
        for r in sample:
            text = r.get("quote") or r.get("text") or ""
            tag = r.get("edge_type") or r.get("name") or r.get("kind")
            print(f"  {r.get('unit', '?')} | {tag} | tier={r.get('preclass_tier')} | "
                  f"source={r.get('preclass_in_universe_source')}")
            print(f"    quote:  {text[:120]!r}")
            print(f"    reason: {r['preclass_reason']}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply-dir", type=Path, default=DEFAULT_APPLY_DIR,
                    help=f"default: {DEFAULT_APPLY_DIR.relative_to(REPO)}")
    ap.add_argument("--chapters-dir", type=Path, default=DEFAULT_CHAPTERS_DIR,
                    help=f"default: {DEFAULT_CHAPTERS_DIR.relative_to(REPO)}")
    ap.add_argument("--units", default=None,
                    help="comma-separated unit dir names, OR a glob pattern (e.g. 'fab-the-long-reign*'). "
                         "Default: every non-excluded unit under --apply-dir.")
    ap.add_argument("--out", type=Path, default=None,
                    help="override the summary text-file path (default: an OS-temp scratchpad location)")
    ap.add_argument("--sample", type=int, default=0,
                    help="print N deterministic (every-k-th) sample rows per bucket for spot-checking")
    args = ap.parse_args()

    if not args.apply_dir.exists():
        sys.exit(f"ABORT: --apply-dir not found: {args.apply_dir}")

    if DROPPED_GENEALOGICAL_TYPES:
        print(f"NOTE: dropped requested genealogical types not in the locked vocabulary: "
              f"{sorted(DROPPED_GENEALOGICAL_TYPES)}", file=sys.stderr)

    unit_dirs = iter_unit_dirs(args.apply_dir, args.units)
    if not unit_dirs:
        sys.exit("ABORT: no unit dirs selected (check --units / --apply-dir)")

    per_unit_rows: dict[str, list[dict]] = {}
    per_unit_counts: dict[str, Counter] = {}
    grand_counts: Counter = Counter()
    zero_row_units: list[str] = []
    files_written = 0
    total_rows = 0

    for unit_dir in unit_dirs:
        rows, counts, existed = process_unit(unit_dir, args.chapters_dir)
        if not existed:
            print(f"WARNING: {unit_dir.name} has no dispute-review.jsonl — skipped", file=sys.stderr)
            continue
        out_path = unit_dir / "dispute-preclass.jsonl"
        with out_path.open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        files_written += 1
        if rows:
            per_unit_rows[unit_dir.name] = rows
            per_unit_counts[unit_dir.name] = counts
            grand_counts.update(counts)
            total_rows += len(rows)
        else:
            zero_row_units.append(unit_dir.name)

    kind_counts = build_kind_bucket_counts(per_unit_rows)
    summary_text = build_summary(per_unit_counts, grand_counts, total_rows, zero_row_units, kind_counts)
    print(summary_text)

    summary_path = args.out or default_summary_path()
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(summary_text + "\n", encoding="utf-8")

    if args.sample:
        print_samples(per_unit_rows, args.sample)

    print(f"\nDone. {files_written} unit(s) processed ({len(per_unit_rows)} with rows, "
          f"{len(zero_row_units)} zero-row), {total_rows} dispute-review rows pre-classified.")
    print("Per-unit output: <unit>/dispute-preclass.jsonl")
    print(f"Summary written to: {summary_path}")


if __name__ == "__main__":
    main()
