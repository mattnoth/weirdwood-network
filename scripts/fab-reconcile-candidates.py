#!/usr/bin/env python3
"""fab-reconcile-candidates.py — deterministic reconciler for the Fire & Blood enrichment pass.

Turns one Opus node-first enrichment proposal (`extractions/fire-and-blood/<unit>.enrichment.md`)
into everything `mint_enrichment.py` (edges + CREATE nodes) and `fab_merge_node.py` (UPDATE prose)
need, plus review sidecars. See:
  - working/fire-and-blood/build-spec-s198.md ("Script 1" section) — the algorithm + locked interfaces.
  - working/fire-and-blood/fire-and-blood-enrichment-design.md §5.0-5.5, §7a — rationale (the R1
    confident-wrong-match mitigation is the entire point of this script).

No LLM, no network. Pure deterministic Python (`feedback_python_before_agent`).

INPUT
  A proposal markdown file with exact headers: `## Entity Roster`, `## Node Prose`,
  `## Relationships Observed`, `## Events of Note` (see prompts/fab-enrichment-v1.md OUTPUT SCHEMA).

OUTPUT (into --out-dir, default working/fire-and-blood/<unit>/)
  candidates.json           — mint_enrichment.py input (CREATE new_node_slugs + edges)
  nodes/<slug>.node.md      — CREATE node bodies
  merge-plan.json           — fab_merge_node.py input (UPDATE prose)
  contradictions-report.md  — F&B vs wiki-infobox kinship/allegiance/title/succession diffs
  run-summary.jsonl         — one observability row, appended
  reconcile-review.jsonl    — ambiguous / undecided routing cases
  quotes-review.jsonl       — quotes that failed the pre-validation grep
  quotes-repaired.jsonl     — quotes canonicalized by the trailing-punct repair (raw -> stored form)
  matched.jsonl             — every name->slug UPDATE routing (wrong-match audit surface)
  dispute-review.jsonl      — untagged artifacts held by the dispute-proximity quarantine (§7.2)
  created-nodes.jsonl       — CREATE decisions log

USAGE
  python scripts/fab-reconcile-candidates.py --proposal extractions/fire-and-blood/<unit>.enrichment.md
  python scripts/fab-reconcile-candidates.py --proposal .../<unit>.enrichment.md --smoke
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "graph" / "query"))
from weirwood_query.resolve import resolve  # noqa: E402
from weirwood_query.normalize import normalize  # noqa: E402

# ---------------------------------------------------------------------------
# Default data paths (all overridable for testing — CLI section below).
# ---------------------------------------------------------------------------
DEFAULT_EDGE_VOCAB = REPO / "working" / "wiki" / "data" / "edge-type-counts.json"
DEFAULT_BLOCKLIST = REPO / "working" / "wiki" / "data" / "disambig-node-blocklist.json"
DEFAULT_REDIRECT_MAP = REPO / "working" / "wiki" / "data" / "redirect-node-map.json"
DEFAULT_CLUSTERS = REPO / "working" / "wiki" / "data" / "same-name-clusters.json"
DEFAULT_PACKS_DIR = REPO / "working" / "fire-and-blood" / "candidate-packs"
DEFAULT_EDGES_FILE = REPO / "graph" / "edges" / "edges.jsonl"
DEFAULT_CHAPTERS_DIR = REPO / "sources" / "chapters" / "fab"
DEFAULT_NODES_ROOT = REPO / "graph" / "nodes"
DEFAULT_WORK_ROOT = REPO / "working" / "fire-and-blood"

# node `type:` prefix -> graph/nodes/ subdir (copied from mint_enrichment.py TYPE_DIR_MAP so CREATE
# node type-guess mapping matches the real mint routing exactly).
TYPE_DIR_MAP = {
    "character": "characters",
    "place": "locations",
    "object.artifact": "artifacts",
    "object.text": "texts",
    "object.food": "foods",
    "object.material": "materials",
    "event": "events",
    "faction": "factions",
    "organization.faction": "factions",
    "organization.house": "houses",
    "organization.religion": "religions",
    "house": "houses",
    "prophecy": "prophecies",
    "theory": "theories",
    "concept": "concepts",
    "custom": "customs",
    "language": "languages",
    "religion": "religions",
    "species": "species",
    "title": "titles",
    "medical": "medical",
    "meta.chapter": "chapters",
}

IN_UNIVERSE_SOURCE_ENUM = {
    "mushroom", "eustace", "munkun", "orwyle", "gyldayn-synthesis", "court-record", "unattributed",
}

# Contradiction diff only inspects these edge-type families (design §5.4).
CONTRADICTION_TYPES = {
    "PARENT_OF", "SIBLING_OF", "SPOUSE_OF", "STEP_PARENT_OF", "IN_LAW_OF",  # kinship
    "SWORN_TO", "MEMBER_OF", "ALLIES_WITH",                                 # allegiance
    "HOLDS_TITLE",                                                          # title
    "SUCCEEDS", "HEIR_TO",                                                  # succession
}

# Edge types where a single source legitimately has MANY distinct targets (a parent has
# many children; a house many members; a Targaryen many spouses under polygamy). For
# these, a DIFFERENT target is NOT a contradiction — only the disputed-vs-flat branch
# applies. (S199 fix 4 / EVAL issue 4: `valaena PARENT_OF <childA>` vs wiki
# `valaena PARENT_OF <childB>` is expected multi-child noise, not a real conflict.)
MULTI_VALUED_TYPES = {
    "PARENT_OF", "SIBLING_OF", "STEP_PARENT_OF", "IN_LAW_OF", "MEMBER_OF",
    "ALLIES_WITH", "SPOUSE_OF",
}

# Deterministic section (unit-slug) -> era map (design §5.5). Keyed by the unit's base slug (the
# `fab-<slug>-NN[-pMM]` component with numeric suffixes stripped). This mirrors unit-map.json's
# era_map comment but is baked in here so the reconciler needs no extra file for CREATE stamping —
# it also reads the unit's OWN frontmatter `era:` first (authoritative) and only falls back to this.
SECTION_ERA_FALLBACK = [
    (("aegons-conquest", "reign-of-the-dragon"), "targaryen-conquest"),
    (("heirs-of-the-dragon", "the-blacks-and-the-greens", "the-red-dragon-and-the-gold",
      "rhaenyra-overthrown", "short-sad-reign-of-aegon-ii"), "dance-of-dragons"),
]
DEFAULT_ERA_FALLBACK = "targaryen-rule"


def era_for_year(ac_year: int) -> str:
    """architecture.md era enum from a signed AC year — used to refine a CREATE
    event's era when the Events table dates it (the section map is unit-granular;
    F&B sections routinely narrate decades of backstory before their title era)."""
    if ac_year < 1:
        return "pre-conquest"
    if ac_year <= 2:
        return "targaryen-conquest"
    if ac_year < 129:
        return "targaryen-rule"
    return "dance-of-dragons"  # 129 AC through the regency aftermath — F&B ends ~136 AC


# ---------------------------------------------------------------------------
# Quote pre-validation — COPIED verbatim in spirit from mint_enrichment.py's norm()/
# authoritative_line() (single-line grep, then two-line join). Deliberately identical
# normalization so a quote that locates here is guaranteed to also locate in mint.
# ---------------------------------------------------------------------------
def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("''", "'")  # OCR artifact in fab source (e.g. `Mushroom’'s`) — collapse after curly conversion
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


QUOTE_JOIN_WINDOW = 4  # max consecutive lines to join when locating a quote (S199 fix 3)


def locate_quote(lines: list[str], quote: str, window: int = QUOTE_JOIN_WINDOW) -> int | None:
    """Return the 1-based line number the quote is found at, or None. Wrap-aware:
    single-line first, then a growing join of up to `window` consecutive lines so a
    quote that straddles a mid-paragraph line break OR a blank-line paragraph gap still
    locates (norm() collapses the whitespace, so a blank line becomes one space). This
    subsumes the old single-line + two-line-join strategy (window=2 was too small — all
    14 Stage-1 quarantines were paragraph-gap false-negatives).

    CRITICAL: the matching loop below MUST stay byte-identical to
    mint_enrichment.authoritative_line — a quote the reconciler 'locates' here has to
    also locate at mint time, or mint aborts on a quote the reconciler passed."""
    q = norm(quote)
    if not q:
        return None
    for i, ln in enumerate(lines, 1):
        if q in norm(ln):
            return i
    n = len(lines)
    for i in range(n):
        # a match whose window starts on a blank line also matches from the next
        # non-blank line (with MORE window headroom) — skipping blanks makes the
        # returned cite line point at actual text (eval fix 8).
        if not lines[i].strip():
            continue
        joined = lines[i]
        for w in range(1, window):
            if i + w >= n:
                break
            joined = joined + " " + lines[i + w]
            if q in norm(joined):
                return i + 1
    return None


SYNTHETIC_TRAILING_PUNCT_RE = re.compile(r"[.,;:!?]+$")


# ---------------------------------------------------------------------------
# Dispute-proximity quarantine (S199 — §7.2 gate FAIL response, EVAL-dispute-axis-audit.md).
# The extractor tags sentence-LOCAL hedges perfectly (0% over-tag) but is blind to
# passage-scope dispute framing ("Here is where our sources diverge" … "Of the
# aftermath, these things are certain") — unattributed sentences inside such a zone
# came out tier-1 (26.9% missed-hedge rate on the p02 stratum). Deterministic
# mitigation: an UNTAGGED artifact whose located quote line sits within ±window
# lines of a hedge-lexicon term is HELD for adjudication (dispute-review.jsonl),
# never emitted — unless a certainty marker sits at least as close (the narrator
# re-asserting flat truth clears the neighborhood). Tagged rows pass through
# unchanged. Held rows are adjudicated by the per-unit fresh-verify at apply
# (verdict-gates-apply, design §7.2) — this is a quarantine, not a demotion, so it
# cannot cause tier deflation.
# ---------------------------------------------------------------------------
# STRONG terms only — chronicler names + explicit divergence framing. Weak generic
# hedges ("rumor", "it was said", "some say") are deliberately EXCLUDED: measured on
# the 4 smoke units they contributed 100% of the false holds on audit-certified-clean
# units and 0 of the real catches (sentence-local weak hedges are the class the
# extractor already tags perfectly; the quarantine exists for PASSAGE-scope framing).
HEDGE_TERMS = [
    "mushroom", "eustace", "testimony of",
    "sources diverge", "sources differ", "dubious chroniclers",
    "tell another tale", "tells another tale", "tell a different tale",
    "in his version", "can be believed", "avers", "purportedly", "allegedly",
]
CERTAINTY_TERMS = [
    "these things are certain", "beyond dispute", "both agree",
    "all the chronicles agree", "sources concur", "all agree", "all our sources",
]
# fab chapter files store one PARAGRAPH per line — window 1 = the claim's own
# paragraph plus each adjacent one. Tuned on the 4 smoke units (scratchpad
# tune_window.py): window 1 catches the audit's entire missed-hedge cluster with
# zero holds on the audit-certified-clean units under the strong-terms lexicon.
DISPUTE_PROXIMITY_WINDOW = 1
# untagged sexual/romantic-affair edges assert more than F&B's flat euphemism
# ("favorite") states — always held absent an explicit disputed tag (audit pattern 2).
ROMANCE_EDGE_TYPES = {"LOVER_OF", "PARAMOUR_OF"}


def dispute_proximity(chapter_lines: list[str], line: int,
                      window: int = DISPUTE_PROXIMITY_WINDOW) -> tuple[str, int] | None:
    """Return (matched_hedge_term, distance) when the nearest hedge term within
    ±window lines of `line` is strictly closer than any certainty marker; else None."""
    best_hedge = None
    best_certainty = None
    n = len(chapter_lines)
    for d in range(0, window + 1):
        for ln in (line - d, line + d):
            if not (1 <= ln <= n):
                continue
            low = chapter_lines[ln - 1].lower()
            if best_hedge is None:
                for t in HEDGE_TERMS:
                    if t in low:
                        best_hedge = (t, d)
                        break
            if best_certainty is None:
                for t in CERTAINTY_TERMS:
                    if t in low:
                        best_certainty = (t, d)
                        break
        if best_hedge and best_certainty:
            break
    if best_hedge and (best_certainty is None or best_hedge[1] < best_certainty[1]):
        return best_hedge
    return None


def locate_or_repair(lines: list[str], quote: str) -> tuple[int | None, str, bool]:
    """Return (line, canonical_quote, repaired). Strict verbatim match first. If that
    misses, retry with the quote's trailing punctuation stripped: the extractor clips
    quotes mid-sentence and appends a synthetic terminal '.' where the source continues
    with ',' etc. — systematic in the Stage-2 unit (31 of 33 quarantines). On a repair
    hit, the CANONICAL quote (what downstream stores and mint re-greps) is the stripped
    strictly-verbatim form, so mint_enrichment.authoritative_line matches it unchanged —
    the repair happens to the quote, never by loosening the matcher."""
    line = locate_quote(lines, quote)
    if line is not None:
        return line, quote, False
    # repair variants, cheapest-first; the FIRST variant that strictly matches wins
    # and becomes the canonical. Enclosing-quote strip handles p02-style extractor
    # drift (the whole cell wrapped in "…" marks the source doesn't have); genuine
    # dialogue quotes match strict-first above and never reach the strip.
    variants = []
    q = quote.strip()
    dequoted = None
    if len(q) >= 2 and q[0] in "\"“" and q[-1] in "\"”":
        dequoted = q[1:-1].strip()
        variants.append(dequoted)
    trailing = SYNTHETIC_TRAILING_PUNCT_RE.sub("", q).rstrip()
    if trailing != q:
        variants.append(trailing)
    if dequoted:
        detrailed = SYNTHETIC_TRAILING_PUNCT_RE.sub("", dequoted).rstrip()
        if detrailed != dequoted:
            variants.append(detrailed)
    for v in variants:
        if v:
            line = locate_quote(lines, v)
            if line is not None:
                return line, v, True
    return None, quote, False


# ---------------------------------------------------------------------------
# Proposal parsing — exact-header parse per build-spec-s198.md.
# ---------------------------------------------------------------------------
SECTION_HEADERS = [
    "Entity Roster",
    "Node Prose",
    "Relationships Observed",
    "Events of Note",
    "Harvest sidecar",
]


def split_sections(text: str) -> dict[str, str]:
    """Split proposal body on `## <Header>` lines (exact match against SECTION_HEADERS,
    tolerant of trailing whitespace). Returns {header: body_text}."""
    pattern = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    sections: dict[str, str] = {}
    for i, m in enumerate(matches):
        header = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[header] = text[start:end].strip("\n")
    return sections


def parse_markdown_table(block: str) -> list[list[str]]:
    """Parse a GFM-style markdown table into rows of cell strings (header row excluded,
    separator row `|---|---|` excluded). Cells are stripped; empty trailing/leading
    pipes handled. Returns [] if no table found."""
    rows = []
    lines = [ln for ln in block.splitlines() if ln.strip().startswith("|")]
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        # Skip separator rows like |---|---|---|
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c != ""):
            continue
        rows.append(cells)
    if rows:
        rows = rows[1:]  # drop header row
    return rows


def parse_roster(body: str) -> list[dict]:
    rows = parse_markdown_table(body)
    out = []
    for r in rows:
        r = r + [""] * (5 - len(r))
        out.append({
            "name": r[0].strip(),
            "type_guess": r[1].strip(),
            "disambiguator": r[2].strip(),
            "new_to_me": r[3].strip(),
            "spelling_note": r[4].strip(),
        })
    return [o for o in out if o["name"]]


def parse_node_prose(body: str) -> dict[str, list[dict]]:
    """### <Name> blocks -> {name: [{text, quote}, ...]}. Each block may hold several
    ' — quote: "..."'-suffixed sentences; we split on that suffix pattern per line/clause."""
    out: dict[str, list[dict]] = {}
    blocks = re.split(r"(?m)^###\s+(.+?)\s*$", body)
    # blocks[0] is preamble (discard); then alternating name, content
    for i in range(1, len(blocks), 2):
        name = blocks[i].strip()
        content = blocks[i + 1] if i + 1 < len(blocks) else ""
        entries = []
        # Split on quote-anchor pattern; also capture a trailing anchorless clause.
        for m in re.finditer(r'([^\n]*?)\s*[—-]\s*quote:\s*"([^"]*)"', content):
            text, quote = m.group(1).strip(), m.group(2).strip()
            if text or quote:
                entries.append({"text": text, "quote": quote})
        if not entries and content.strip():
            entries.append({"text": content.strip(), "quote": ""})
        out.setdefault(name, []).extend(entries)
    return out


def parse_relationships(body: str) -> list[dict]:
    rows = parse_markdown_table(body)
    out = []
    for r in rows:
        r = r + [""] * (6 - len(r))
        source, rel, target, ius, disputed, quote = r[:6]
        rel = rel.strip()
        qualifier = None
        m = re.match(r"^([A-Z_]+)\s*\(([^)]+)\)\s*$", rel)
        etype = rel
        if m:
            etype, qualifier = m.group(1), m.group(2).strip()
        out.append({
            "source_name": source.strip(),
            "edge_type_raw": rel,
            "edge_type": etype.strip(),
            "qualifier": qualifier,
            "target_name": target.strip(),
            "in_universe_source": ius.strip() or None,
            "disputed": _truthy(disputed),
            "quote": quote.strip(),
        })
    return [o for o in out if o["source_name"] and o["target_name"] and o["edge_type"]]


def parse_events(body: str) -> list[dict]:
    rows = parse_markdown_table(body)
    out = []
    for r in rows:
        # Tolerate both the 8-col task spec shape and the 11-col real prompt shape.
        r = r + [""] * (11 - len(r))
        name, etype, year, agent, patient, instrument, location, outcome = r[:8]
        ius, disputed, quote = (r[8], r[9], r[10]) if len(r) >= 11 else ("", "", "")
        out.append({
            "name": name.strip(),
            "type": etype.strip(),
            "year": year.strip(),
            "agent": agent.strip(),
            "patient": patient.strip(),
            "instrument": instrument.strip(),
            "location": location.strip(),
            "outcome": outcome.strip(),
            "in_universe_source": ius.strip() or None,
            "disputed": _truthy(disputed),
            "quote": quote.strip(),
        })
    return [o for o in out if o["name"]]


def _truthy(cell: str) -> bool:
    return cell.strip().lower() in {"true", "yes", "y", "1"}


# ---------------------------------------------------------------------------
# Entity-name splitting + collective/composite detection (CREATE guard §5.1) — S199 fix 2
# ---------------------------------------------------------------------------
# Separators that join multiple distinct entities in one Events-table agent/patient
# cell ("Mern IX Gardener; Loren I Lannister", "Visenya Targaryen and Rhaenys Targaryen").
# Split BEFORE resolution so each individual routes on its own (two role edges, not one
# junk composite node). NOTE: no comma-split — roster/edge names never comma-join, and a
# comma inside a disambiguating name would break wrongly.
_ENTITY_SPLIT_RE = re.compile(r"\s*(?:;|/|&|\band\b)\s*", re.IGNORECASE)

# Collective / abstract military referents that are NOT graph entities ("the Targaryen
# fleet", "Aegon's host at the Field of Fire") — a head-noun stop-list. Matched anywhere
# in the name; a false positive only sends a real entity to review (never drops it).
_COLLECTIVE_NOUNS = re.compile(
    r"\b(fleet|fleets|host|hosts|army|armies|force|forces|garrison|garrisons|"
    r"vanguard|van|soldiers|troops|smallfolk|horde|column|columns)\b", re.IGNORECASE)


def split_entities(cell: str) -> list[str]:
    """Split a possibly-composite roster/event cell into individual entity names."""
    if not cell:
        return []
    parts = [p.strip() for p in _ENTITY_SPLIT_RE.split(cell)]
    return [p for p in parts if p]


def looks_composite(name: str) -> bool:
    """True if the name still splits into >1 entity (a composite that reached CREATE)."""
    return len(split_entities(name)) > 1


def is_collective(name: str) -> bool:
    """True for abstract/collective military referents that must never be minted as a
    person node — route to review instead."""
    n = name.strip().lower()
    return bool(n) and bool(_COLLECTIVE_NOUNS.search(n))


def singularize(word: str) -> str:
    """Crude de-pluralize for house-surname probing: 'Blackwoods' -> 'Blackwood'.
    Strips a single trailing 's' only (never 'ss')."""
    w = word.strip()
    if len(w) > 2 and w.lower().endswith("s") and not w.lower().endswith("ss"):
        return w[:-1]
    return w


def index_existing_nodes(nodes_root: Path) -> tuple[set[str], set[str], dict[str, str]]:
    """Return (all_slugs, house_slugs, slug->category-dir) from graph/nodes/**. One-time
    filesystem scan so the CREATE guard can reject dupes (slug-exists) and house-surname
    collisions, and so the type-agreement gate (S199 Stage-2 blocker: `Lorath` place
    resolved onto `jaqen-hghar` via a junk alias) can check a clean hit's category
    without a per-name glob."""
    all_slugs: set[str] = set()
    house_slugs: set[str] = set()
    categories: dict[str, str] = {}
    for p in nodes_root.glob("**/*.node.md"):
        slug = p.name[: -len(".node.md")]
        all_slugs.add(slug)
        categories[slug] = p.parent.name
        if p.parent.name == "houses":
            house_slugs.add(slug)
    return all_slugs, house_slugs, categories


# roster free-text 'Type guess' prefix -> graph/nodes/ category dir, for the
# type-agreement gate. None/absent = no opinion (gate inactive for that guess).
GUESS_CATEGORY = {
    "character": "characters", "person": "characters", "dragon": "characters",
    "place": "locations", "location": "locations", "region": "locations",
    "house": "houses", "event": "events", "faction": "factions",
    "ship": "artifacts", "sword": "artifacts", "artifact": "artifacts",
    "object": "artifacts", "title": "titles", "religion": "religions",
    "concept": "concepts", "species": "species", "text": "texts",
}


def expected_category(type_guess: str) -> str | None:
    tg = (type_guess or "").strip().lower()
    if not tg:
        return None
    return GUESS_CATEGORY.get(tg.split(".", 1)[0])


# ---------------------------------------------------------------------------
# Unit / chapter-file resolution
# ---------------------------------------------------------------------------
def unit_from_proposal_path(proposal_path: Path) -> str:
    name = proposal_path.name
    if not name.endswith(".enrichment.md"):
        sys.exit(f"ABORT: proposal filename must end .enrichment.md: {name}")
    return name[: -len(".enrichment.md")]


def base_slug_from_unit(unit: str) -> str:
    """fab-heirs-of-the-dragon-15 -> heirs-of-the-dragon; fab-heirs-of-the-dragon-15-p02 -> same.
    Strips a trailing NN (1-3 digits) then an optional -pMM part suffix."""
    s = unit
    if not s.startswith("fab-"):
        sys.exit(f"ABORT: unit does not start with 'fab-': {unit}")
    s = s[len("fab-"):]
    s = re.sub(r"-p\d+$", "", s)     # drop part suffix
    s = re.sub(r"-\d{1,3}$", "", s)  # drop NN
    return s


def find_candidate_pack(packs_dir: Path, slug: str) -> Path | None:
    matches = sorted(packs_dir.glob(f"fab-{slug}-*.json"))
    matches = [m for m in matches if re.fullmatch(r"fab-" + re.escape(slug) + r"-\d{2,3}\.json", m.name)]
    return matches[0] if matches else None


def find_chapter_file(chapters_dir: Path, unit: str) -> Path:
    f = chapters_dir / f"{unit}.md"
    return f


def read_chapter_frontmatter(chapter_path: Path) -> dict:
    if not chapter_path.exists():
        return {}
    text = chapter_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([a-zA-Z_]+):\s*(.*?)\s*$", line)
        if km:
            fm[km.group(1)] = km.group(2).strip().strip('"').strip("'")
    return fm


def era_for_unit(unit: str, chapter_fm: dict) -> str:
    if chapter_fm.get("era"):
        return chapter_fm["era"]
    slug = base_slug_from_unit(unit)
    for slugs, era in SECTION_ERA_FALLBACK:
        if slug in slugs:
            return era
    return DEFAULT_ERA_FALLBACK


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------
def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def build_cluster_name_index(clusters: dict) -> set[str]:
    """same-name-clusters.json is keyed by normalized 'first surname' phrases already."""
    return {normalize(k) for k in clusters.keys()}


# ---------------------------------------------------------------------------
# Bare-first-name detection (CREATE guard §5.1 step 4)
# ---------------------------------------------------------------------------
def is_bare_first_name(name: str, disambiguator: str) -> bool:
    """A 'bare first name' is a single-token name with no disambiguating text.
    Multi-word names (even without a surname match, e.g. an epithet phrase) are NOT
    bare — the roster's Disambiguator column is the authoritative signal when present
    ('bare first name — no disambiguator in text' is the prompt's own literal phrasing
    for this case, so we also recognize that string)."""
    stripped = name.strip()
    if re.search(r"no disambiguator in text", disambiguator, re.IGNORECASE):
        return True
    tokens = stripped.split()
    if len(tokens) <= 1 and not disambiguator.strip():
        return True
    return False


# ---------------------------------------------------------------------------
# Discriminator scoring (§5.1 step 3 — the R1 mitigation)
# ---------------------------------------------------------------------------
def score_candidates(name: str, disambiguator: str, unit_era: str, pack: dict | None,
                      cluster: dict) -> dict[str, dict]:
    """Score every member of a same-name cluster against the roster row's evidence.
    Returns {slug: {"score": int, "hits": [reason, ...]}} — score is the count of
    INDEPENDENT discriminators that matched (independence = distinct categories a/b/c/d
    below, not distinct matched substrings within one category)."""
    disamb_norm = normalize(disambiguator) if disambiguator else ""
    year_match = re.search(r"\b(1[0-9]{2}|[1-9][0-9]?)\s*AC\b", disambiguator, re.IGNORECASE)
    roster_year = int(year_match.group(1)) if year_match else None

    expected_slugs = set(pack.get("expected_slugs", [])) if pack else set()

    # strip punctuation before tokenizing — disambiguators are ';'-separated, and a
    # token adjacent to the separator ("Tides;") must still match its discriminator.
    d_tokens = set(re.sub(r"[^\w\s']", " ", disamb_norm).split())

    results: dict[str, dict] = {}
    for slug, member in cluster.get("members", {}).items():
        hits = []

        # (a) Disambiguator <-> parents/spouse/key_title (token-subset match — a field's
        # tokens must ALL appear in the disambiguator text; safe for multi-word slugs like
        # "aerion-targaryen-son-of-daemion" -> {aerion,targaryen,son,of,daemion}).
        disamb_fields = []
        for p in member.get("parents") or []:
            disamb_fields.append(("parent", p))
        for s in member.get("spouse") or []:
            disamb_fields.append(("spouse", s))
        if member.get("key_title"):
            disamb_fields.append(("title", member["key_title"]))
        # ALL matching (a)-fields are recorded (the accept rule compares full hit
        # sets between top and runner-up — dropping a shared hit would make the
        # runner-up's copy of it look like runner-only evidence), but category (a)
        # contributes at most 1 to the score (independence = distinct categories).
        a_hits = []
        if disamb_norm:
            for role, f in disamb_fields:
                f_tokens = set(str(f).replace("-", " ").lower().split())
                # require at least 2 tokens (or 1 token of length >=4) to avoid a single
                # short/common word spuriously "matching" via subset containment.
                if f_tokens and (len(f_tokens) >= 2 or (len(f_tokens) == 1 and len(next(iter(f_tokens))) >= 4)):
                    if f_tokens.issubset(d_tokens):
                        a_hits.append(f"disambiguator~{f}")
                        continue
                # S199 Stage-2 recall fix: parents/spouse are stored as full slugs
                # ("jaehaerys-i-targaryen") but the roster Disambiguator writes "son of
                # Jaehaerys I" — no surname, so the full-field subset above never fires.
                # Fall back to the relative's base first name (first slug token, >=4
                # chars to stay discriminating). Direction confusion (a disambiguator
                # naming a CHILD that is another candidate's PARENT) is contained by
                # the accept rule: shared/extra runner-up evidence forces review.
                if role in ("parent", "spouse"):
                    base = str(f).split("-", 1)[0].lower()
                    if len(base) >= 4 and base in d_tokens:
                        a_hits.append(f"disambiguator~{role}:{base}")
        hits.extend(a_hits)

        # (a2) Regnal number — WORD-BOUNDARY match only (never substring), since regnal
        # values are bare roman numerals ("I", "V") that would false-positive against
        # almost any prose via naive `in` containment.
        if member.get("regnal") and disamb_norm:
            regnal_pattern = r"\b" + re.escape(str(member["regnal"])) + r"\b"
            if re.search(regnal_pattern, disambiguator, flags=0):
                hits.append(f"regnal={member['regnal']}")

        # (b) unit era <-> member era
        if unit_era and member.get("era") and member["era"] == unit_era:
            hits.append(f"era={unit_era}")

        # (c) candidate-pack membership
        if slug in expected_slugs:
            anchor_count = 0
            if pack:
                anchor_count = pack.get("per_slug", {}).get(slug, {}).get("anchor_count", 0)
            hits.append(f"pack-expected(anchor_count={anchor_count})")

        # (d) born/died year vs roster-given year
        if roster_year is not None:
            for field in ("born", "died"):
                v = member.get(field)
                if v is not None and int(v) == roster_year:
                    hits.append(f"{field}={roster_year}")
                    break

        # score = distinct categories hit (a/a2/b/c/d) — category (a) caps at 1 no
        # matter how many disambiguator fields matched; the extra hits stay listed
        # for the accept rule's evidence-subset comparison and for review display.
        score = len(hits) - len(a_hits) + (1 if a_hits else 0)
        results[slug] = {"score": score, "hits": hits}
    return results


# ---------------------------------------------------------------------------
# Routing core
# ---------------------------------------------------------------------------
class Router:
    def __init__(self, blocklist, redirect_map, clusters, pack, unit_era, smoke,
                 existing_slugs=None, house_slugs=None, node_categories=None):
        self.blocklist = blocklist
        self.redirect_map = redirect_map
        self.clusters = clusters
        self.cluster_name_index = build_cluster_name_index(clusters)
        self.pack = pack
        self.unit_era = unit_era
        self.smoke = smoke
        self.existing_slugs = existing_slugs or set()
        self.house_slugs = house_slugs or set()
        self.node_categories = node_categories or {}
        self._resolve_cache: dict[str, tuple] = {}

    def _probe_candidates(self, name: str, candidates: list) -> list:
        """S199 Stage-2 (eval fix 4) — review-candidate recall: make sure the RIGHT
        answer is presentable at triage. The `Septon Eustace` row omitted the actual
        node (`eustace-dance-of-the-dragons`) because the resolver's fuzzy list missed
        it. Augment review rows with (a) candidate-pack members and (b) existing-slug
        probes that share a distinctive name token (>=4 chars, slug-word match).
        Suggestions are marked and capped; existing candidates are never removed."""
        existing = {c.get("slug") for c in (candidates or []) if isinstance(c, dict)}
        tokens = [t for t in re.sub(r"[^\w\s]", " ", name.lower()).split() if len(t) >= 4]
        if not tokens:
            return candidates or []
        suggestions = []
        pack_slugs = set(self.pack.get("expected_slugs", [])) if self.pack else set()
        for pool, tag in ((sorted(pack_slugs), "pack-probe"),
                          (sorted(self.existing_slugs), "name-token-probe")):
            for slug in pool:
                if slug in existing or any(slug == s["slug"] for s in suggestions):
                    continue
                slug_words = set(slug.split("-"))
                if any(t in slug_words for t in tokens):
                    suggestions.append({"slug": slug, "suggested": tag,
                                        "node_category": self.node_categories.get(slug)})
                if len(suggestions) >= 8:
                    break
            if len(suggestions) >= 8:
                break
        return (candidates or []) + suggestions

    def _type_gate(self, slug: str, type_guess: str):
        """S199 Stage-2 blocker fix: a clean resolver hit is TYPE-BLIND — `Lorath`
        (roster type place) resolved onto `jaqen-hghar` (a character) at 1.0 via a junk
        alias. Returns None when the hit passes (no guess, unknown category, or
        agreement), else a review dict."""
        expected = expected_category(type_guess)
        actual = self.node_categories.get(slug)
        if expected and actual and actual != expected:
            return {"decision": "review", "reason": "type-mismatch",
                    "candidates": [{"slug": slug, "node_category": actual,
                                    "expected_category": expected}]}
        return None

    def _resolve(self, name: str):
        if name not in self._resolve_cache:
            self._resolve_cache[name] = resolve(name)
        return self._resolve_cache[name]

    def _apply_redirect(self, slug: str) -> str:
        r = self.redirect_map.get(slug)
        return r["target_slug"] if r else slug

    def route(self, name: str, disambiguator: str = "", kind: str = "character",
              type_guess: str = "") -> dict:
        """Return a routing decision dict:
          {"decision": "update", "slug": <slug>}
          {"decision": "create"}
          {"decision": "review", "reason": <str>, "candidates": [...]}

        `kind` ('character' default | 'event') tunes the fuzzy-candidate branch: an
        EVENT only defers to review when a fuzzy candidate is ITSELF an existing event
        node (a real dedup risk), because the resolver's fuzzy matcher otherwise surfaces
        the persons/places an event merely involves.

        `type_guess` (roster 'Type guess' column, optional) arms the type-agreement
        gate on clean-hit UPDATEs; empty = gate inactive (edge-endpoint names carry
        no guess).
        """
        norm_name = normalize(name)
        slug, status, candidates = self._resolve(name)

        # 1. transparent redirect — a redirect page resolves to exactly ONE target by
        # construction, so it is authoritative and unconditional: it wins even when the
        # query's normalized NAME also happens to key a same-name cluster (e.g. "Aenys
        # Targaryen" is both a redirect node AND a cluster key — the redirect target,
        # aenys-i-targaryen, is the correct answer without discriminator scoring). Only
        # re-route to discrimination if the TARGET slug itself is separately blocklisted
        # (a redirect pointing at a disambiguation hub would be a data bug worth flagging).
        if slug is not None and slug in self.redirect_map:
            target = self._apply_redirect(slug)
            if target in self.blocklist:
                return self._discriminate(name, disambiguator, norm_name, target)
            mismatch = self._type_gate(target, type_guess)
            if mismatch:
                return mismatch
            return {"decision": "update", "slug": target, "route_reason": "redirect"}

        is_clean_hit = status in ("hit", "hit-character") and slug is not None

        # 2. clean hit, NOT blocklisted, NOT a same-name cluster -> UPDATE (the common case),
        #    gated on roster-type <-> node-category agreement (S199 Stage-2 blocker).
        if is_clean_hit and slug not in self.blocklist and norm_name not in self.cluster_name_index:
            mismatch = self._type_gate(slug, type_guess)
            if mismatch:
                return mismatch
            return {"decision": "update", "slug": slug, "route_reason": status}

        # blocklist hit OR same-name cluster collision -> discriminator scoring.
        if (slug is not None and slug in self.blocklist) or norm_name in self.cluster_name_index:
            return self._discriminate(name, disambiguator, norm_name, slug)

        # 3. CONFIDENTLY-EMPTY miss (no slug, and NO fuzzy candidates) -> CREATE guard.
        #    §5.1 rule 3 mints only on a confidently-empty miss. A `candidates`/`ambiguous`
        #    status means the resolver found FUZZY matches — that is NOT confidently empty
        #    and must never CREATE (S199 fix 1: `daenys`->`daenys-targaryen`,
        #    `arrec`->`arrec-durrandon` were minted because slug-None alone triggered CREATE).
        if status == "miss" and slug is None and not candidates:
            return self._create_guard(name, disambiguator, norm_name)

        # 4. fuzzy / ambiguous / candidates status.
        if kind == "event":
            # An event defers to review ONLY when a candidate is itself an existing EVENT
            # node — a real dedup risk (e.g. "Submission of Rosby" ~ `yielding-of-rosby`,
            # "Battle at the Wailing Willows" ~ `wailing-willows`, both existing
            # event.battle nodes). When every candidate is a person/place the event merely
            # involves ("Capture of Loren Lannister" -> `loren-i-lannister`), the event is
            # genuinely new -> CREATE guard.
            event_cands = [c for c in (candidates or [])
                           if isinstance(c, dict) and c.get("node_category") == "events"]
            if event_cands:
                return {"decision": "review", "reason": f"event-dedup-risk:{status}",
                        "candidates": event_cands}
            return self._create_guard(name, disambiguator, norm_name)

        # S199 Stage-2 (eval fix 5) — drain the exact-1.0 review flood: 57/85 of the
        # Stage-2 unit's review rows were a single exact-normalized-name 1.0 top with
        # clear margin. Accept ONLY on ALL of: exact 1.0 top, margin >=0.2 to #2, not
        # blocklisted, and POSITIVE type agreement (roster guess maps to a category AND
        # it equals the hit's category — a missing guess never accepts; the Merling
        # King / Cod Queen ship-rows must keep routing to review on mismatch).
        if status == "candidates" and candidates:
            ranked_c = sorted((c for c in candidates if isinstance(c, dict)),
                              key=lambda c: -(c.get("score") or 0.0))
            top_c = ranked_c[0]
            second_score = (ranked_c[1].get("score") or 0.0) if len(ranked_c) > 1 else 0.0
            expected = expected_category(type_guess)
            # the resolver reports exact-normalized-name matches as match_type
            # "fuzzy" with score 1.0 — the score IS the exactness signal.
            if ((top_c.get("score") or 0.0) >= 1.0
                    and (top_c.get("score") or 0.0) - second_score >= 0.2
                    and top_c.get("slug") and top_c["slug"] not in self.blocklist
                    and expected is not None
                    and self.node_categories.get(top_c["slug"]) == expected):
                if self.smoke:
                    return {"decision": "review", "reason": "smoke-exact-accept-disabled",
                            "candidates": candidates}
                return {"decision": "update", "slug": top_c["slug"],
                        "route_reason": "exact-1.0-type-agree"}

        # a character/other with fuzzy candidates is a dupe risk -> conservative review.
        return {"decision": "review", "reason": f"unresolved-status:{status}",
                "candidates": self._probe_candidates(name, candidates)}

    def _create_guard(self, name, disambiguator, norm_name) -> dict:
        """A confidently-empty miss still has to clear the §5.1 CREATE guards before we
        mint a net-new node. Any guard trip -> review, never CREATE. Ordering matters:
        the house/slug-exists dupe probes run BEFORE the bare-first-name check so a bare
        plural surname ("Blackwoods") surfaces its existing `house-<x>` node as the review
        candidate instead of a bare 'no disambiguator' note."""
        # composite cell that slipped through un-split -> review (don't mint a joined node).
        if looks_composite(name):
            return {"decision": "review", "reason": "composite-name",
                    "candidates": [{"name": p} for p in split_entities(name)]}
        # collective / abstract military referent -> review (never a person node).
        if is_collective(name):
            return {"decision": "review", "reason": "collective-referent"}
        # de-pluralize + "House X" probe: a bare surname ("Blackwoods") whose singular
        # already exists as house-<singular> is a dupe risk -> review, don't mint.
        house_hit = self._probe_house(name)
        if house_hit:
            return {"decision": "review", "reason": "house-surname-existing-node",
                    "candidates": [{"slug": house_hit}]}
        # slug already exists as some node -> review (final dupe backstop).
        slug = slugify(name)
        if slug in self.existing_slugs:
            return {"decision": "review", "reason": "create-slug-exists",
                    "candidates": [{"slug": slug}]}
        # bare first name -> never create (an unresolvable "Aegon" is a review case).
        if is_bare_first_name(name, disambiguator):
            return {"decision": "review", "reason": "bare-first-name-miss"}
        # same-name cluster collision even without a direct slug hit -> discriminate.
        if norm_name in self.cluster_name_index:
            return self._discriminate(name, disambiguator, norm_name, None)
        return {"decision": "create"}

    def _probe_house(self, name: str) -> str | None:
        """Return an existing `house-<slug>` node if the (optionally de-pluralized) name
        maps onto one, else None."""
        for cand in (name, singularize(name)):
            hs = "house-" + slugify(cand)
            if hs in self.house_slugs:
                return hs
        return None

    def _discriminate(self, name, disambiguator, norm_name, resolved_slug) -> dict:
        cluster = self.clusters.get(norm_name)
        if cluster is None:
            # blocklisted but not a cluster key we recognize by this exact phrase — review.
            return {"decision": "review", "reason": "blocklisted-no-cluster-entry",
                     "candidates": [{"slug": resolved_slug}] if resolved_slug else []}

        scored = score_candidates(name, disambiguator, self.unit_era, self.pack, cluster)
        ranked = sorted(scored.items(), key=lambda kv: -kv[1]["score"])
        review_payload = {
            "name": name,
            "disambiguator": disambiguator,
            "scored_candidates": [
                {"slug": s, "score": v["score"], "hits": v["hits"]} for s, v in ranked
            ],
        }

        if self.smoke:
            return {"decision": "review", "reason": "smoke-auto-accept-disabled", **review_payload}

        if not ranked:
            return {"decision": "review", "reason": "no-cluster-members", **review_payload}

        top_slug, top = ranked[0]
        runner_up = ranked[1][1] if len(ranked) > 1 else None
        runner_up_score = runner_up["score"] if runner_up else 0

        def hit_key(h: str) -> str:
            # pack-expected's anchor_count is decoration, not evidence identity —
            # normalize it away so equal pack hits compare equal across candidates.
            return re.sub(r"\(anchor_count=\d+\)", "", h)

        # Tuned S199 Stage-2 (design §5.1 bucket 2): the original margin condition
        # (runner-up must have ZERO hits) blocked correct 2-vs-1 cases where the
        # runner-up's only hit is one the top candidate ALSO carries (a shared hit
        # discriminates nothing). Accept when the top has >=2 independent
        # discriminators, STRICTLY outscores the runner-up, and the runner-up brings
        # no evidence the top lacks. Ties and runner-up-only evidence still review.
        # Tuned on the 23 scored rows of the two smoke units; MUST be validated
        # out-of-sample on >=2 fresh units before the bulk run
        # (feedback_fresh_review_and_out_of_sample).
        if top["score"] >= 2 and top["score"] > runner_up_score and (
                runner_up is None
                or {hit_key(h) for h in runner_up["hits"]} <= {hit_key(h) for h in top["hits"]}):
            return {"decision": "update", "slug": top_slug, "route_reason": "discriminator-auto-accept",
                     **review_payload}
        return {"decision": "review", "reason": "no-decisive-margin", **review_payload}


PRONOUN_OPENER_RE = re.compile(
    r"^(he|she|his|her|hers|they|their|theirs|it|its|this|these|both)\b", re.IGNORECASE)


def derive_identity_line(name: str, entries: list[dict]) -> str | None:
    """S199 (Matt: 'wire it') — book-grounded Identity line for the merge plan.
    Deterministic: take the FIRST Node-Prose bullet's text when it is identity-shaped —
    non-empty, not a pronoun continuation, sane length. Returns None (no swap; the
    boilerplate stays for the parked strip track) when no clean line exists. Supplying
    a line is always safe: fab_merge_node swaps ONLY boilerplate Identity lines
    (`^.+ is a … from the AWOIAF wiki.$`), so real curated identities are untouched."""
    for e in entries:
        text = re.sub(r"^[.\s]+", "", (e.get("text") or "").strip())
        if not text:
            continue
        if PRONOUN_OPENER_RE.match(text):
            return None  # first substantive bullet is a narrative continuation
        if not (20 <= len(text) <= 300):
            return None
        if not text.endswith((".", "!", "?")):
            text += "."
        if text.lower().startswith(name.lower()):
            return text
        return f"{name} — {text}"
    return None


# ---------------------------------------------------------------------------
# Node CREATE body composer
# ---------------------------------------------------------------------------
# extractor free-text -> canonical schema type (S199 Stage-2 eval fix 7): bare
# prefixes get their canonical default subtype; known off-vocab subtype synonyms map
# onto the graph's actual vocabulary (unknown subtypes pass through — reviewable in
# created-nodes.jsonl).
TYPE_SYNONYMS = {
    "event.tourney": "event.tournament",
    "dragon": "character.dragon",
    "person": "character.human",
    "location": "place.location",
    "region": "place.region",
}
BARE_TYPE_DEFAULTS = {
    "character": "character.human",
    "place": "place.location",
    "event": "event.incident",
    "house": "organization.house",
    "faction": "organization.faction",
    "organization": "organization.faction",
    "religion": "organization.religion",
}


def guess_node_type(type_guess: str) -> str:
    """Roster 'Type guess' column -> canonical schema type. Roster values are free text
    like 'character', 'event.battle', 'place', 'house'; default character.human (the
    overwhelmingly common F&B roster entity)."""
    tg = (type_guess or "").strip().lower()
    if not tg:
        return "character.human"
    tg = TYPE_SYNONYMS.get(tg, tg)
    if tg in BARE_TYPE_DEFAULTS:
        return BARE_TYPE_DEFAULTS[tg]
    if "." in tg and tg.split(".", 1)[0] in TYPE_DIR_MAP:
        return tg
    if tg in TYPE_DIR_MAP:
        return tg
    return "character.human"


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"['\",]", "", s)
    s = re.sub(r"[ _]+", "-", s)
    s = re.sub(r"[^a-z0-9-]", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def compose_create_node(name: str, node_type: str, identity_prose: str, era: str,
                         run_id: str, occurred: dict | None) -> str:
    slug = slugify(name)
    fm_lines = [
        "---",
        f'name: "{name}"',
        f"type: {node_type}",
        f"slug: {slug}",
        "aliases: []",
        "confidence: tier-2",
        f"era: {era}",
        "pass_origin: pass-fab-enrichment",
    ]
    if occurred:
        fm_lines.append("occurred:")
        for k, v in occurred.items():
            fm_lines.append(f"  {k}: {v}")
    fm_lines.append("---")
    body = "\n".join(fm_lines) + "\n\n"
    body += "## Identity\n\n"
    body += (identity_prose.strip() or f"{name} — introduced in Fire & Blood.") + "\n\n"
    body += "## Fire & Blood\n\n"
    body += f"<!-- fab-enriched: {run_id} -->\n\n"
    body += (identity_prose.strip() or "") + "\n"
    return slug, body


# ---------------------------------------------------------------------------
# Main reconciliation
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--proposal", required=True, type=Path)
    ap.add_argument("--smoke", action="store_true",
                    help="disable step-3 discriminator auto-accept; everything scored routes to review")
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--date", "--produced-at", dest="produced_at", default=None,
                    help="ISO date/datetime for run_id + produced_at (default: today). Deterministic override for tests.")
    ap.add_argument("--blocklist", type=Path, default=DEFAULT_BLOCKLIST)
    ap.add_argument("--redirect-map", type=Path, default=DEFAULT_REDIRECT_MAP)
    ap.add_argument("--clusters", type=Path, default=DEFAULT_CLUSTERS)
    ap.add_argument("--packs-dir", type=Path, default=DEFAULT_PACKS_DIR)
    ap.add_argument("--edges-file", type=Path, default=DEFAULT_EDGES_FILE)
    ap.add_argument("--chapters-dir", type=Path, default=DEFAULT_CHAPTERS_DIR)
    args = ap.parse_args()

    proposal_path = args.proposal
    if not proposal_path.exists():
        sys.exit(f"ABORT: proposal file not found: {proposal_path}")
    unit = unit_from_proposal_path(proposal_path)
    base_slug = base_slug_from_unit(unit)

    out_dir = args.out_dir or (DEFAULT_WORK_ROOT / unit)
    nodes_out_dir = out_dir / "nodes"
    out_dir.mkdir(parents=True, exist_ok=True)
    nodes_out_dir.mkdir(parents=True, exist_ok=True)

    produced_at = args.produced_at or f"{date.today().isoformat()}T00:00:00+00:00"
    run_date = produced_at[:10]
    # run_id="fab-<slug>-NN-<date>" (build-spec-s198.md) — NN is the unit's own numeric
    # suffix (part suffix -pMM stripped, if present) for legibility across split parts.
    nn_match = re.search(r"-(\d{1,3})(?:-p\d+)?$", unit)
    nn = nn_match.group(1) if nn_match else "NN"
    # S199 Stage-2 blocker fix: run_id keeps the FULL unit slug incl. any -pMM part
    # suffix — the old fab-<slug>-NN-<date> form gave p01/p02/p03 identical run_ids on
    # a same-day run, so fab_merge_node's idempotency marker silently dropped parts
    # 2-3's prose on every node shared across parts (R3 silent-drop class).
    run_id = f"{unit}-{run_date}"

    chapter_path = find_chapter_file(args.chapters_dir, unit)
    if not chapter_path.exists():
        print(f"WARNING: chapter file missing: {chapter_path} — all quotes will quarantine.", file=sys.stderr)
        chapter_lines: list[str] = []
        chapter_fm = {}
    else:
        chapter_lines = chapter_path.read_text(encoding="utf-8").splitlines()
        chapter_fm = read_chapter_frontmatter(chapter_path)

    unit_era = era_for_unit(unit, chapter_fm)

    blocklist = load_json(args.blocklist, {})
    redirect_map = load_json(args.redirect_map, {})
    clusters = load_json(args.clusters, {})
    pack_path = find_candidate_pack(args.packs_dir, base_slug)
    pack = load_json(pack_path, None) if pack_path else None

    existing_slugs, house_slugs, node_categories = index_existing_nodes(DEFAULT_NODES_ROOT)
    edge_vocab: set[str] = set()
    if DEFAULT_EDGE_VOCAB.exists():
        _ev = load_json(DEFAULT_EDGE_VOCAB, {})
        edge_vocab = set(_ev.get("type_counts", {}).keys()) | set(_ev.get("unpopulated_types", []))
    router = Router(blocklist, redirect_map, clusters, pack, unit_era, args.smoke,
                    existing_slugs=existing_slugs, house_slugs=house_slugs,
                    node_categories=node_categories)

    text = proposal_path.read_text(encoding="utf-8")
    sections = split_sections(text)
    roster = parse_roster(sections.get("Entity Roster", ""))
    prose = parse_node_prose(sections.get("Node Prose", ""))
    relationships = parse_relationships(sections.get("Relationships Observed", ""))
    events = parse_events(sections.get("Events of Note", ""))

    # ---- 1. Route every roster entity ----
    routes: dict[str, dict] = {}          # name -> routing decision
    disambiguators: dict[str, str] = {}
    type_guesses: dict[str, str] = {}
    for row in roster:
        disambiguators[row["name"]] = row["disambiguator"]
        type_guesses[row["name"]] = row["type_guess"]
        routes[row["name"]] = router.route(row["name"], row["disambiguator"],
                                           type_guess=row["type_guess"])

    def get_route(name: str) -> dict:
        if name not in routes:
            routes[name] = router.route(name, disambiguators.get(name, ""))
        return routes[name]

    # Route every edge/event endpoint too (roster may not cover them all).
    endpoint_names = set()
    for rel in relationships:
        endpoint_names.add(rel["source_name"])
        endpoint_names.add(rel["target_name"])
    for ev in events:
        for f in ("agent", "patient", "location"):
            # Split composite cells ("Mern IX Gardener; Loren I Lannister") so each
            # individual routes on its own (S199 fix 2).
            for person in split_entities(ev[f]):
                endpoint_names.add(person)
    for name in endpoint_names:
        get_route(name)

    reconcile_review_rows = []
    created_nodes_rows = []
    create_name_to_slug: dict[str, str] = {}
    node_bodies: dict[str, str] = {}

    entities_rostered = len(roster)
    matched = 0
    ambiguous_to_review = 0
    created = 0

    for name, route in routes.items():
        decision = route["decision"]
        if decision == "update":
            matched += 1
        elif decision == "review":
            ambiguous_to_review += 1
            reconcile_review_rows.append({
                "unit": unit,
                "name": name,
                "disambiguator": disambiguators.get(name, ""),
                "reason": route.get("reason"),
                "route_reason": route.get("route_reason"),
                "candidates": route.get("candidates", []),
                "scored_candidates": route.get("scored_candidates", []),
            })
        elif decision == "create":
            slug = slugify(name)
            # Routing bug guard: a CREATE whose slug already exists as a node.
            existing = list((DEFAULT_NODES_ROOT).glob(f"**/{slug}.node.md"))
            if existing:
                reconcile_review_rows.append({
                    "unit": unit,
                    "name": name,
                    "disambiguator": disambiguators.get(name, ""),
                    "reason": "routing-bug-create-slug-exists",
                    "existing_path": str(existing[0].relative_to(REPO)),
                })
                ambiguous_to_review += 1
                continue
            created += 1
            create_name_to_slug[name] = slug
            node_type = guess_node_type(type_guesses.get(name, ""))
            prose_entries = prose.get(name, [])
            identity_text = " ".join(e["text"] for e in prose_entries if e["text"]).strip()
            occurred = None
            _, body = compose_create_node(name, node_type, identity_text, unit_era, run_id, occurred)
            node_bodies[slug] = body
            created_nodes_rows.append({
                "unit": unit,
                "name": name,
                "slug": slug,
                "type": node_type,
            })

    def slug_for(name: str) -> str | None:
        route = get_route(name)
        if route["decision"] == "update":
            return route["slug"]
        if route["decision"] == "create":
            return create_name_to_slug.get(name)
        return None  # review — not usable as an edge endpoint yet

    # ---- 2/C. Quote pre-validation + tier/dispute invariant, build edges ----
    quotes_review_rows = []
    quotes_repaired_rows = []
    dispute_review_rows = []
    edge_candidates = []
    quotes_total = 0
    quotes_quarantined = 0
    needs_vocab_count = 0
    disputed_count = 0
    edges_by_type: dict[str, int] = defaultdict(int)

    def process_quote(quote: str, context: dict) -> tuple[bool, int | None, str]:
        """Returns (ok, line, canonical_quote) — canonical differs from the input only
        when the trailing-punct repair fired (store/mint the canonical, not the raw)."""
        nonlocal quotes_total, quotes_quarantined
        quotes_total += 1
        line, canonical, repaired = (None, quote, False)
        if quote:
            line, canonical, repaired = locate_or_repair(chapter_lines, quote)
        if line is None:
            quotes_quarantined += 1
            quotes_review_rows.append({"unit": unit, "quote": quote, **context})
            return False, None, quote
        if repaired:
            quotes_repaired_rows.append(
                {"unit": unit, "quote_raw": quote, "quote": canonical, **context})
        return True, line, canonical

    for i, rel in enumerate(relationships, 1):
        if rel["edge_type"].upper() == "NEEDS_VOCAB" or rel["edge_type_raw"].upper().startswith("NEEDS_VOCAB"):
            needs_vocab_count += 1
            reconcile_review_rows.append({
                "unit": unit, "name": rel["source_name"], "reason": "needs-vocab",
                "raw": rel["edge_type_raw"], "target": rel["target_name"],
            })
            continue
        # mechanical vocab guard (drift detection for bulk): an edge_type outside the
        # canonical 170 (architecture.md via edge-type-counts.json) is extractor drift
        # the prompt should have flagged NEEDS_VOCAB — quarantine the row, never emit.
        if edge_vocab and rel["edge_type"] not in edge_vocab:
            needs_vocab_count += 1
            reconcile_review_rows.append({
                "unit": unit, "name": rel["source_name"], "reason": "edge-type-not-in-vocab",
                "edge_type": rel["edge_type"], "target": rel["target_name"],
            })
            continue

        src_slug = slug_for(rel["source_name"])
        tgt_slug = slug_for(rel["target_name"])
        if src_slug is None or tgt_slug is None:
            # endpoint unresolved (in review) — the edge cannot be minted yet; already
            # captured in reconcile_review_rows via the endpoint's own routing.
            continue

        ok, line, quote_canonical = process_quote(rel["quote"], {
            "kind": "edge", "edge_type": rel["edge_type"],
            "source": rel["source_name"], "target": rel["target_name"],
        })
        if not ok:
            continue

        disputed = bool(rel["disputed"])
        ius = rel["in_universe_source"]
        if ius and ius not in IN_UNIVERSE_SOURCE_ENUM:
            reconcile_review_rows.append({
                "unit": unit, "reason": "in_universe_source-not-in-enum", "value": ius,
                "source": rel["source_name"], "target": rel["target_name"],
            })
            ius = None
        # dispute-proximity quarantine (§7.2 gate response): untagged edges in a
        # hedge neighborhood, and ALL untagged romance-class edges, are HELD for
        # adjudication — never emitted tier-1.
        if not disputed and not ius:
            if rel["edge_type"] in ROMANCE_EDGE_TYPES:
                hold = ("romance-class-untagged", 0)
            else:
                hold = dispute_proximity(chapter_lines, line)
            if hold:
                dispute_review_rows.append({
                    "unit": unit, "kind": "edge", "edge_type": rel["edge_type"],
                    "source": rel["source_name"], "target": rel["target_name"],
                    "quote": quote_canonical, "line": line,
                    "hedge_term": hold[0], "hedge_distance": hold[1],
                })
                continue
        tier = "tier-2" if (disputed or ius) else "tier-1"
        if disputed:
            disputed_count += 1

        eid = f"E{i}"
        edge = {
            "id": eid,
            "type": rel["edge_type"],
            "source": src_slug,
            "target": tgt_slug,
            "book": "fab",
            "chapter": unit,
            "quote": quote_canonical,
            "tier": tier,
            "note": f"Fire & Blood: {rel['source_name']} {rel['edge_type']} {rel['target_name']}",
        }
        if rel["qualifier"]:
            edge["qualifier"] = rel["qualifier"]
        if ius:
            edge["in_universe_source"] = ius
        if disputed:
            edge["disputed"] = True
        edge_candidates.append(edge)
        edges_by_type[rel["edge_type"]] += 1

    # ---- Events of Note -> candidate event CREATE/UPDATE + edges ----
    for i, ev in enumerate(events, 1):
        # dispute-proximity quarantine BEFORE any minting/edges: a single missed
        # passage-scope hedge multiplies into node + role edges + slug encoding the
        # disputed cause (audit pattern 3). Untagged event in a hedge neighborhood
        # -> the WHOLE row is held for adjudication.
        if not ev["disputed"] and ev["in_universe_source"] not in IN_UNIVERSE_SOURCE_ENUM and ev["quote"]:
            ev_line, _c, _r = locate_or_repair(chapter_lines, ev["quote"])
            if ev_line is not None:
                hold = dispute_proximity(chapter_lines, ev_line)
                if hold:
                    dispute_review_rows.append({
                        "unit": unit, "kind": "event", "name": ev["name"],
                        "quote": _c, "line": ev_line,
                        "hedge_term": hold[0], "hedge_distance": hold[1],
                    })
                    continue
        route = router.route(ev["name"], kind="event")
        routes[ev["name"]] = route  # cache so slug_for()/get_route() agree on the event
        decision = route["decision"]
        if decision == "review":
            ambiguous_to_review += 1
            reconcile_review_rows.append({
                "unit": unit, "name": ev["name"], "reason": route.get("reason"),
                "kind": "event", "candidates": route.get("candidates", []),
            })
            continue
        if decision == "create":
            existing = list(DEFAULT_NODES_ROOT.glob(f"**/{slugify(ev['name'])}.node.md"))
            if existing:
                reconcile_review_rows.append({
                    "unit": unit, "name": ev["name"], "reason": "routing-bug-create-slug-exists",
                    "existing_path": str(existing[0].relative_to(REPO)),
                })
                ambiguous_to_review += 1
                continue
            slug = slugify(ev["name"])
            created += 1
            node_type = (ev["type"].strip() or "event.incident").lower()
            if not node_type.startswith("event"):
                node_type = "event." + node_type
            if node_type == "event":
                node_type = "event.incident"
            node_type = TYPE_SYNONYMS.get(node_type, node_type)
            occurred = None
            if ev["year"]:
                ym = re.search(r"-?\d+", ev["year"])
                if ym:
                    ac_year = int(ym.group(0))
                    date_conf = "tier-2" if ev["disputed"] else "tier-1"
                    occurred = {
                        "ac_year": ac_year,
                        "precision": "year",
                        "basis_source": "narrative-prose",
                        "basis_reliability": "primary-source",
                        "date_confidence": date_conf,
                    }
            identity_text = ev["outcome"] or ev["quote"] or f"{ev['name']} — an event recorded in Fire & Blood."
            # era refinement (S199 Stage-2): a dated event beats the section map — a
            # 92 AC event in a Dance-section unit is targaryen-rule, not dance-of-dragons.
            ev_era = era_for_year(occurred["ac_year"]) if occurred else unit_era
            _, body = compose_create_node(ev["name"], node_type, identity_text, ev_era, run_id, occurred)
            node_bodies[slug] = body
            create_name_to_slug[ev["name"]] = slug
            created_nodes_rows.append({"unit": unit, "name": ev["name"], "slug": slug, "type": node_type})
        # role edges for agent/patient (best-effort, only when quote + endpoints resolve).
        # Composite agent/patient cells are split so each actor gets its own role edge
        # (S199 fix 2) instead of one edge onto a joined junk node.
        if ev["quote"]:
            ev_slug = slug_for(ev["name"])
            for role_field, role_type in (("agent", "AGENT_IN"), ("patient", "VICTIM_IN")):
                if ev_slug is None:
                    continue
                for person in split_entities(ev[role_field]):
                    person_slug = slug_for(person)
                    if person_slug is None:
                        continue
                    ok, line, ev_quote_canonical = process_quote(ev["quote"], {
                        "kind": "event-role", "role": role_field, "event": ev["name"], "person": person,
                    })
                    if not ok:
                        continue
                    disputed = bool(ev["disputed"])
                    ius = ev["in_universe_source"] if ev["in_universe_source"] in IN_UNIVERSE_SOURCE_ENUM else None
                    tier = "tier-2" if (disputed or ius) else "tier-1"
                    if disputed:
                        disputed_count += 1
                    edge = {
                        "id": f"EV{i}-{role_field}-{person_slug}",
                        "type": role_type,
                        "source": person_slug,
                        "target": ev_slug,
                        "book": "fab",
                        "chapter": unit,
                        "quote": ev_quote_canonical,
                        "tier": tier,
                        "note": f"Fire & Blood event: {person} {role_type} {ev['name']}",
                    }
                    if ius:
                        edge["in_universe_source"] = ius
                    if disputed:
                        edge["disputed"] = True
                    edge_candidates.append(edge)
                    edges_by_type[role_type] += 1

    # ---- Quote pre-validation for prose anchors (harvest-adjacent — logged, not minted as edges) ----
    prose_quotes_total = 0
    prose_quotes_located = 0
    for name, entries in prose.items():
        for e in entries:
            if not e["quote"]:
                continue
            prose_quotes_total += 1
            ok, line, _ = process_quote(e["quote"], {"kind": "prose", "entity": name})
            if ok:
                prose_quotes_located += 1

    # ---- merge-plan.json (UPDATE entries with node prose) ----
    merge_plan = []
    for name, entries in prose.items():
        route = get_route(name)
        if route["decision"] != "update":
            continue
        slug = route["slug"]
        lines_md = []
        surviving_entries = []
        for e in entries:
            # bullet hygiene (eval fix 8): strip leading orphan punctuation; skip
            # bullets with no substantive text.
            text = re.sub(r"^[.\s]+", "", (e["text"] or "").strip())
            if not e["quote"]:
                if text:
                    lines_md.append(f"- {text}")
                    surviving_entries.append(e)
                continue
            line, _canon, _repaired = locate_or_repair(chapter_lines, e["quote"])
            if line is None:
                # never write a dead cite into node prose — the quote is already
                # quarantined (quotes-review.jsonl); the bullet ships when it's fixed.
                continue
            if not text:
                continue
            # dispute-proximity quarantine: a bullet that does NOT carry its own hedge
            # ("Mushroom claims…" in the text is self-hedged and ships) but sits in a
            # hedge neighborhood is held for adjudication.
            if not any(t in text.lower() for t in HEDGE_TERMS):
                hold = dispute_proximity(chapter_lines, line)
                if hold:
                    dispute_review_rows.append({
                        "unit": unit, "kind": "prose", "entity": name, "slug": slug,
                        "text": text, "line": line,
                        "hedge_term": hold[0], "hedge_distance": hold[1],
                    })
                    continue
            # cite carries the FULL unit slug (incl. -pMM): line numbers are per
            # part-file, and the Tier-1 overlay's cites must open (eval fix 3).
            lines_md.append(f"- {text} ({unit}:{line})")
            surviving_entries.append(e)
        if not lines_md:
            continue
        mp_entry = {
            "slug": slug,
            "fab_section_md": "\n".join(lines_md),
            "run_id": run_id,
        }
        ident = derive_identity_line(name, surviving_entries)
        if ident:
            mp_entry["identity_line"] = ident
        merge_plan.append(mp_entry)

    # ---- contradictions-report.md (§5.4) ----
    contradictions = build_contradictions_report(edge_candidates, args.edges_file)

    # ---- Emit candidates.json ----
    total_edges = len(edge_candidates)
    quotes_located_pct = (
        round(100.0 * (quotes_total - quotes_quarantined) / quotes_total, 1) if quotes_total else 100.0
    )
    new_node_slugs = sorted(create_name_to_slug.values())

    candidates = {
        "_meta": {
            "unit": unit,
            "session": "fab-reconcile",
            "run_id": run_id,
            "evidence_kind": "book-fab",
            "new_node_slugs": new_node_slugs,
            "note": f"Fire & Blood reconciler output for {unit} (smoke={args.smoke}).",
            "produced_at": produced_at,
        },
        "edges": edge_candidates,
    }
    (out_dir / "candidates.json").write_text(json.dumps(candidates, indent=2, ensure_ascii=False) + "\n",
                                               encoding="utf-8")

    for slug, body in node_bodies.items():
        (nodes_out_dir / f"{slug}.node.md").write_text(body, encoding="utf-8")

    (out_dir / "merge-plan.json").write_text(json.dumps(merge_plan, indent=2, ensure_ascii=False) + "\n",
                                              encoding="utf-8")
    (out_dir / "contradictions-report.md").write_text(contradictions, encoding="utf-8")

    def write_jsonl(path: Path, rows: list[dict]):
        with path.open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    write_jsonl(out_dir / "reconcile-review.jsonl", reconcile_review_rows)
    write_jsonl(out_dir / "quotes-review.jsonl", quotes_review_rows)
    write_jsonl(out_dir / "quotes-repaired.jsonl", quotes_repaired_rows)
    write_jsonl(out_dir / "dispute-review.jsonl", dispute_review_rows)
    write_jsonl(out_dir / "created-nodes.jsonl", created_nodes_rows)
    # matched.jsonl (eval fix 8): every name->slug UPDATE routing, auditable at a
    # glance — wrong-matches on non-write-bearing names must not hide in silence.
    write_jsonl(out_dir / "matched.jsonl", [
        {"unit": unit, "name": name, "slug": r.get("slug"),
         "route_reason": r.get("route_reason")}
        for name, r in sorted(routes.items()) if r["decision"] == "update"
    ])

    summary_row = {
        "unit": unit,
        "entities_rostered": entities_rostered,
        "matched": matched,
        "ambiguous_to_review": ambiguous_to_review,
        "created": created,
        "edges_by_type": dict(edges_by_type),
        "quotes_total": quotes_total,
        "quotes_located_pct": quotes_located_pct,
        "quotes_quarantined": quotes_quarantined,
        "quotes_repaired": len(quotes_repaired_rows),
        "dispute_held": len(dispute_review_rows),
        "needs_vocab_count": needs_vocab_count,
        "disputed_rate": round(disputed_count / total_edges, 3) if total_edges else 0.0,
    }
    summary_path = DEFAULT_WORK_ROOT / "run-summary.jsonl"
    with summary_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(summary_row, ensure_ascii=False) + "\n")

    # ---- Console report ----
    print(f"Unit: {unit}  (run_id={run_id}, smoke={args.smoke})")
    print(f"Roster: {entities_rostered} entities -> matched {matched}, review {ambiguous_to_review}, created {created}")
    print(f"Edges candidates: {total_edges} ({dict(edges_by_type)})")
    print(f"Quotes: {quotes_total} total, {quotes_quarantined} quarantined ({quotes_located_pct}% located), {len(quotes_repaired_rows)} repaired (trailing-punct / enclosing-quote canonicalized)")
    print(f"Prose quotes: {prose_quotes_located}/{prose_quotes_total} located")
    print(f"needs_vocab: {needs_vocab_count}  disputed_rate: {summary_row['disputed_rate']}  dispute_held: {len(dispute_review_rows)}")
    def _display(p: Path) -> str:
        p = p.resolve()
        try:
            return str(p.relative_to(REPO))
        except ValueError:
            return str(p)

    print(f"\nWrote:")
    for p in [out_dir / "candidates.json", out_dir / "merge-plan.json",
              out_dir / "contradictions-report.md", out_dir / "reconcile-review.jsonl",
              out_dir / "quotes-review.jsonl", out_dir / "created-nodes.jsonl", summary_path]:
        print(f"  {_display(p)}")
    if node_bodies:
        print(f"  nodes/ ({len(node_bodies)} CREATE bodies) -> {_display(nodes_out_dir)}")


def build_contradictions_report(edge_candidates: list[dict], edges_file: Path) -> str:
    """Diff proposed kinship/allegiance/title/succession edges against existing
    wiki-infobox edges on the same source node. Same (source,type) DIFFERENT target,
    OR a disputed F&B tag against a flat wiki claim -> flag, grouped by node."""
    existing_by_source: dict[tuple[str, str], list[dict]] = defaultdict(list)
    if edges_file.exists():
        for line in edges_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("candidate_kind") != "wiki-infobox":
                continue
            etype = row.get("edge_type")
            if etype not in CONTRADICTION_TYPES:
                continue
            existing_by_source[(row.get("source_slug"), etype)].append(row)

    flags: dict[str, list[str]] = defaultdict(list)
    for e in edge_candidates:
        etype = e["type"]
        if etype not in CONTRADICTION_TYPES:
            continue
        key = (e["source"], etype)
        existing_rows = existing_by_source.get(key, [])
        for ex in existing_rows:
            same_target = ex.get("target_slug") == e["target"]
            if not same_target and etype not in MULTI_VALUED_TYPES:
                flags[e["source"]].append(
                    f"- **{etype}**: F&B proposes `{e['source']}` -> `{e['target']}`"
                    f" (tier {e['tier']}); existing wiki-infobox has `{e['source']}` -> `{ex.get('target_slug')}`."
                )
            elif same_target and e.get("disputed") and ex.get("confidence_tier") in (1, "1", "tier-1"):
                flags[e["source"]].append(
                    f"- **{etype}**: F&B tags `{e['source']}` -> `{e['target']}` as `disputed:true`,"
                    f" but existing wiki-infobox asserts it as flat tier-1 fact."
                )

    if not flags:
        return "# Contradictions report\n\nNo contradictions found against existing wiki-infobox edges.\n"

    lines = ["# Contradictions report", ""]
    for source in sorted(flags):
        lines.append(f"## {source}")
        lines.extend(flags[source])
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
