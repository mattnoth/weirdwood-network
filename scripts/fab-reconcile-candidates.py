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


# ---------------------------------------------------------------------------
# Quote pre-validation — COPIED verbatim in spirit from mint_enrichment.py's norm()/
# authoritative_line() (single-line grep, then two-line join). Deliberately identical
# normalization so a quote that locates here is guaranteed to also locate in mint.
# ---------------------------------------------------------------------------
def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def locate_quote(lines: list[str], quote: str) -> int | None:
    """Return the 1-based line number the quote is found at, or None. Same two-pass
    strategy as mint_enrichment.authoritative_line: single-line first, then adjacent
    two-line join (a quote can straddle the paragraph's mid-file line break)."""
    q = norm(quote)
    if not q:
        return None
    for i, ln in enumerate(lines, 1):
        if q in norm(ln):
            return i
    for i in range(len(lines) - 1):
        if q in norm(lines[i] + " " + lines[i + 1]):
            return i + 1
    return None


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

    d_tokens = set(disamb_norm.split())

    results: dict[str, dict] = {}
    for slug, member in cluster.get("members", {}).items():
        hits = []

        # (a) Disambiguator <-> parents/spouse/key_title (token-subset match — a field's
        # tokens must ALL appear in the disambiguator text; safe for multi-word slugs like
        # "aerion-targaryen-son-of-daemion" -> {aerion,targaryen,son,of,daemion}).
        disamb_fields = []
        for p in member.get("parents") or []:
            disamb_fields.append(p)
        for s in member.get("spouse") or []:
            disamb_fields.append(s)
        if member.get("key_title"):
            disamb_fields.append(member["key_title"])
        if disamb_norm:
            for f in disamb_fields:
                f_tokens = set(str(f).replace("-", " ").lower().split())
                # require at least 2 tokens (or 1 token of length >=4) to avoid a single
                # short/common word spuriously "matching" via subset containment.
                if f_tokens and (len(f_tokens) >= 2 or (len(f_tokens) == 1 and len(next(iter(f_tokens))) >= 4)):
                    if f_tokens.issubset(d_tokens):
                        hits.append(f"disambiguator~{f}")
                        break

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

        results[slug] = {"score": len(hits), "hits": hits}
    return results


# ---------------------------------------------------------------------------
# Routing core
# ---------------------------------------------------------------------------
class Router:
    def __init__(self, blocklist, redirect_map, clusters, pack, unit_era, smoke):
        self.blocklist = blocklist
        self.redirect_map = redirect_map
        self.clusters = clusters
        self.cluster_name_index = build_cluster_name_index(clusters)
        self.pack = pack
        self.unit_era = unit_era
        self.smoke = smoke
        self._resolve_cache: dict[str, tuple] = {}

    def _resolve(self, name: str):
        if name not in self._resolve_cache:
            self._resolve_cache[name] = resolve(name)
        return self._resolve_cache[name]

    def _apply_redirect(self, slug: str) -> str:
        r = self.redirect_map.get(slug)
        return r["target_slug"] if r else slug

    def route(self, name: str, disambiguator: str = "") -> dict:
        """Return a routing decision dict:
          {"decision": "update", "slug": <slug>}
          {"decision": "create"}
          {"decision": "review", "reason": <str>, "candidates": [...]}
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
            return {"decision": "update", "slug": target, "route_reason": "redirect"}

        is_clean_hit = status in ("hit", "hit-character") and slug is not None

        if is_clean_hit and slug not in self.blocklist and norm_name not in self.cluster_name_index:
            return {"decision": "update", "slug": slug, "route_reason": status}

        if (slug is not None and slug in self.blocklist) or norm_name in self.cluster_name_index:
            return self._discriminate(name, disambiguator, norm_name, slug)

        # 3. no confident hit at all -> CREATE guard
        if status == "miss" or slug is None:
            if is_bare_first_name(name, disambiguator):
                return {"decision": "review", "reason": "bare-first-name-miss", "candidates": candidates}
            # collision guard: name matches a cluster key even without a direct slug hit
            if norm_name in self.cluster_name_index:
                return self._discriminate(name, disambiguator, norm_name, slug)
            return {"decision": "create"}

        # ambiguous/candidates status with no cluster/blocklist entry -> conservative review
        return {"decision": "review", "reason": f"unresolved-status:{status}", "candidates": candidates}

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
        runner_up_score = ranked[1][1]["score"] if len(ranked) > 1 else 0
        if top["score"] >= 2 and runner_up_score == 0:
            return {"decision": "update", "slug": top_slug, "route_reason": "discriminator-auto-accept",
                     **review_payload}
        return {"decision": "review", "reason": "no-decisive-margin", **review_payload}


# ---------------------------------------------------------------------------
# Node CREATE body composer
# ---------------------------------------------------------------------------
def guess_node_type(type_guess: str) -> str:
    """Roster 'Type guess' column -> schema type. Roster values are free text like
    'character', 'event.battle', 'place', 'house' — map through TYPE_DIR_MAP's prefixes,
    default to character.human (the overwhelmingly common F&B roster entity)."""
    tg = (type_guess or "").strip().lower()
    if not tg:
        return "character.human"
    if "." in tg:
        prefix = tg.split(".", 1)[0]
        if prefix in TYPE_DIR_MAP:
            return tg
    if tg in TYPE_DIR_MAP:
        return tg + (".human" if tg == "character" else "")
    if tg.startswith("event"):
        return tg if "." in tg else "event.incident"
    if tg.startswith("character"):
        return tg if "." in tg else "character.human"
    if tg.startswith("place"):
        return tg if "." in tg else "place.location"
    if tg.startswith("house") or tg.startswith("organization.house"):
        return "organization.house"
    if tg.startswith("faction") or tg.startswith("organization.faction"):
        return "organization.faction"
    if tg.startswith("title"):
        return "title"
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
    run_id = f"fab-{base_slug}-{nn}-{run_date}"

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

    router = Router(blocklist, redirect_map, clusters, pack, unit_era, args.smoke)

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
        routes[row["name"]] = router.route(row["name"], row["disambiguator"])

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
            if ev[f]:
                endpoint_names.add(ev[f])
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
    edge_candidates = []
    quotes_total = 0
    quotes_quarantined = 0
    needs_vocab_count = 0
    disputed_count = 0
    edges_by_type: dict[str, int] = defaultdict(int)

    def process_quote(quote: str, context: dict) -> tuple[bool, int | None]:
        nonlocal quotes_total, quotes_quarantined
        quotes_total += 1
        line = locate_quote(chapter_lines, quote) if quote else None
        if line is None:
            quotes_quarantined += 1
            quotes_review_rows.append({"unit": unit, "quote": quote, **context})
            return False, None
        return True, line

    for i, rel in enumerate(relationships, 1):
        if rel["edge_type"].upper() == "NEEDS_VOCAB" or rel["edge_type_raw"].upper().startswith("NEEDS_VOCAB"):
            needs_vocab_count += 1
            reconcile_review_rows.append({
                "unit": unit, "name": rel["source_name"], "reason": "needs-vocab",
                "raw": rel["edge_type_raw"], "target": rel["target_name"],
            })
            continue

        src_slug = slug_for(rel["source_name"])
        tgt_slug = slug_for(rel["target_name"])
        if src_slug is None or tgt_slug is None:
            # endpoint unresolved (in review) — the edge cannot be minted yet; already
            # captured in reconcile_review_rows via the endpoint's own routing.
            continue

        ok, line = process_quote(rel["quote"], {
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
            "quote": rel["quote"],
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
        route = router.route(ev["name"])
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
            node_type = ev["type"].strip() or "event.incident"
            if not node_type.startswith("event"):
                node_type = "event." + node_type if node_type else "event.incident"
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
            _, body = compose_create_node(ev["name"], node_type, identity_text, unit_era, run_id, occurred)
            node_bodies[slug] = body
            create_name_to_slug[ev["name"]] = slug
            created_nodes_rows.append({"unit": unit, "name": ev["name"], "slug": slug, "type": node_type})
        # role edges for agent/patient (best-effort, only when quote + endpoints resolve)
        if ev["quote"]:
            ev_slug = slug_for(ev["name"])
            for role_field, role_type in (("agent", "AGENT_IN"), ("patient", "VICTIM_IN")):
                person = ev[role_field]
                if not person or ev_slug is None:
                    continue
                person_slug = slug_for(person)
                if person_slug is None:
                    continue
                ok, line = process_quote(ev["quote"], {
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
                    "id": f"EV{i}-{role_field}",
                    "type": role_type,
                    "source": person_slug,
                    "target": ev_slug,
                    "book": "fab",
                    "chapter": unit,
                    "quote": ev["quote"],
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
            ok, line = process_quote(e["quote"], {"kind": "prose", "entity": name})
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
        for e in entries:
            if not e["quote"]:
                if e["text"]:
                    lines_md.append(f"- {e['text']}")
                continue
            line = locate_quote(chapter_lines, e["quote"])
            cite = f"(fab-{base_slug}-{nn}:{line})" if line else "(fab-quote-unlocated)"
            lines_md.append(f"- {e['text']} {cite}".strip())
        if not lines_md:
            continue
        merge_plan.append({
            "slug": slug,
            "fab_section_md": "\n".join(lines_md),
            "run_id": run_id,
        })

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
    write_jsonl(out_dir / "created-nodes.jsonl", created_nodes_rows)

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
    print(f"Quotes: {quotes_total} total, {quotes_quarantined} quarantined ({quotes_located_pct}% located)")
    print(f"Prose quotes: {prose_quotes_located}/{prose_quotes_total} located")
    print(f"needs_vocab: {needs_vocab_count}  disputed_rate: {summary_row['disputed_rate']}")
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
            if ex.get("target_slug") != e["target"]:
                flags[e["source"]].append(
                    f"- **{etype}**: F&B proposes `{e['source']}` -> `{e['target']}`"
                    f" (tier {e['tier']}); existing wiki-infobox has `{e['source']}` -> `{ex.get('target_slug')}`."
                )
            elif e.get("disputed") and ex.get("confidence_tier") in (1, "1", "tier-1"):
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
