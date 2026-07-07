#!/usr/bin/env python3
"""
wiki-prose-identity-composer.py — Deterministic same-name disambiguation + Identity-line composer.

Weirwood Network / ASOIAF knowledge graph. NO LLM calls, no network, no fetching.
Everything is read from local files already on disk:

  - graph/nodes/**/*.node.md            (node frontmatter + body)
  - working/wiki/data/page-categories.jsonl   (MediaWiki categories per wiki page — life-years, traps)
  - graph/edges/edges.jsonl              (wiki-infobox edges — parents, spouse, allegiance, title)
  - sources/wiki/_raw/<Page>.json        (cached page HTML — redirect-target parse only, no fetch)

Full design: working/node-enrichment-wiki-prose/design.md (v2).

SINGLETON EXTENSION (this pass): the cluster-only scope above requires >=2
real cluster members OR a real member + a trap/redirect companion — a
unique-named character (Rhaenyra Targaryen, Daemon Targaryen, ...) never
forms a cluster and so never got an Identity line from --compose/--apply.
--compose-singletons is a SEPARATE input path (same composition machinery:
build_member_discriminators, compose_member_identity_line, shape detection,
the writer) for a curated list of such singleton slugs. See
--compose-singletons below.

There are TWO junk-node trap classes handled here, both blocklisted identically
for downstream consumers (the F&B reconciler never treats either as a
CREATE/UPDATE target) but tagged distinctly so a consumer CAN tell them apart:

  - "disambiguation" traps — wiki page category `Disambiguation pages`
    (design §3.6). Get `disambiguation_hub: true` + a hub-listing Identity line.
  - "redirect" traps — wiki page category `Redirect` (NEW, this pass). Bare-name
    stub nodes (e.g. `aenys-targaryen`) whose wiki page is a MediaWiki #REDIRECT
    to the real canonical page (e.g. "Aenys I Targaryen"). Get `redirect_to:
    <target-slug>` + a one-line "Redirect — X refers to Y" Identity line instead
    of a hub listing. The target page/slug is parsed deterministically from the
    already-cached `_raw/<Page>.json` `redirectMsg` HTML block — no re-fetch,
    no LLM. See `working/wiki/data/redirect-node-map.json` (the machine-readable
    routing table a resolver hit on a redirect node should consult).

Four subcommands:

  --build-pack        Writes working/wiki/data/same-name-clusters.json,
                       working/wiki/data/disambig-node-blocklist.json, and
                       working/wiki/data/redirect-node-map.json. No node writes.

  --compose --dry-run  Writes working/node-enrichment-wiki-prose/preview.md, a human-readable
                       preview of every composed Identity line + shape/action + thin-rate.
                       Also reads the thin-sentences cache (see --enrich-thin below) and, for
                       any thin cluster member with a cached non-null sentence, appends it to
                       the composed Identity line. No node writes.

  --enrich-thin       Repeatable, self-contained step that fills
                       working/node-enrichment-wiki-prose/thin-sentences.jsonl — the committed,
                       deterministic cache the composer reads. Two parts:
                         (1) SEED: merge any working/node-enrichment-wiki-prose/thin-batch-*.jsonl
                             files into the cache (idempotent, dedup by slug).
                         (2) FILL: for thin cluster members not yet in the cache, read the local
                             wiki lead prose (sources/wiki/_raw/<Page>.json — no re-fetch) and
                             call `claude -p --model claude-haiku-4-5-20251001` (cwd=/tmp, per
                             reference_llm_pass_via_claude_p) for ONE distinguishing sentence.
                       LLM output is non-deterministic — the CACHE is the deterministic artifact;
                       --compose only ever reads the cache, never calls the LLM itself.
                       Flags: --limit N, --dry-run, --sleep SECONDS, --force-slug SLUG.

  --apply             The GATED node writer. Mutates graph/nodes/**/*.node.md in place
                       (additive-merge only — see design §5). Requires --apply explicitly;
                       every other invocation is a no-op with respect to node files. When a thin
                       member's composed Identity line carries a cached wiki sentence, the
                       applied text also carries a trailing `(wiki:<Source_Page>)` Tier-2 cite.
                       Supports --nodes-root to redirect at a scratch copy for testing.

  --compose-singletons  Composes Identity lines for a curated list of NON-clustered
                       ("singleton") character slugs — see DEFAULT_SINGLETON_SLUGS, or pass
                       --singleton-slugs-file to supply your own (one slug per line). A
                       candidate is included only if (a) a node file exists, (b) the slug is
                       NOT a member/trap/redirect of any same-name cluster, and (c) its current
                       Identity line is boilerplate or absent. Same field priority + shapes +
                       writer as cluster members, but NEVER emits the "One of N ..."
                       cross-pointer clause (a singleton has no cluster to point back to).
                         --dry-run  writes working/node-enrichment-wiki-prose/preview-singletons.md
                                    (included + skipped-with-reasons). No node writes.
                         --apply    GATED. Mutates node files (same additive-merge/atomic/
                                    idempotent writer as --apply above). DO NOT RUN without a
                                    Matt go-ahead; use --nodes-root to test on a scratch copy.

Usage:
  python3 scripts/wiki-prose-identity-composer.py --build-pack
  python3 scripts/wiki-prose-identity-composer.py --enrich-thin --dry-run
  python3 scripts/wiki-prose-identity-composer.py --enrich-thin --limit 2
  python3 scripts/wiki-prose-identity-composer.py --compose --dry-run
  python3 scripts/wiki-prose-identity-composer.py --apply               # DO NOT RUN without a Matt go-ahead
  python3 scripts/wiki-prose-identity-composer.py --compose-singletons --dry-run
  python3 scripts/wiki-prose-identity-composer.py --compose-singletons --apply  # DO NOT RUN without a Matt go-ahead
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
import os
from pathlib import Path
from urllib.parse import unquote

from bs4 import BeautifulSoup, Tag

# ---------------------------------------------------------------------------
# Repo-relative paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent

NODES_ROOT_DEFAULT = REPO_ROOT / "graph" / "nodes"
EDGES_PATH_DEFAULT = REPO_ROOT / "graph" / "edges" / "edges.jsonl"
CATEGORIES_PATH_DEFAULT = REPO_ROOT / "working" / "wiki" / "data" / "page-categories.jsonl"

RAW_WIKI_ROOT_DEFAULT = REPO_ROOT / "sources" / "wiki" / "_raw"

CLUSTERS_OUT_DEFAULT = REPO_ROOT / "working" / "wiki" / "data" / "same-name-clusters.json"
BLOCKLIST_OUT_DEFAULT = REPO_ROOT / "working" / "wiki" / "data" / "disambig-node-blocklist.json"
REDIRECT_MAP_OUT_DEFAULT = REPO_ROOT / "working" / "wiki" / "data" / "redirect-node-map.json"
PREVIEW_OUT_DEFAULT = REPO_ROOT / "working" / "node-enrichment-wiki-prose" / "preview.md"
SINGLETON_PREVIEW_OUT_DEFAULT = REPO_ROOT / "working" / "node-enrichment-wiki-prose" / "preview-singletons.md"

ENRICHMENT_DIR_DEFAULT = REPO_ROOT / "working" / "node-enrichment-wiki-prose"
THIN_SENTENCES_CACHE_DEFAULT = ENRICHMENT_DIR_DEFAULT / "thin-sentences.jsonl"
THIN_BATCH_GLOB_DEFAULT = "thin-batch-*.jsonl"

HAIKU_MODEL_DEFAULT = "claude-haiku-4-5-20251001"
HAIKU_SLEEP_DEFAULT = 3.0
HAIKU_TIMEOUT_SECONDS = 120
HAIKU_MAX_RETRIES = 2
HAIKU_MAX_SENTENCE_WORDS = 45

BOILERPLATE_RE = re.compile(r"^.+ is a [a-z][a-z.]* from the AWOIAF wiki\.$")
CATEGORY_YEAR_RE = re.compile(r"^(\d+)\s+(AC|BC)\s+(births|deaths)$")
REGNAL_TOKEN_RE = re.compile(
    r"^(X{0,3})(IX|IV|V?I{0,3})$"
)  # matches I..XIII-ish roman numerals as a standalone token
PARENTHETICAL_RE = re.compile(r"\s*\([^)]*\)")

# MediaWiki redirect stub: <div class="redirectMsg">...<a href="/index.php/Target_Page">
REDIRECT_MSG_RE = re.compile(
    r'<div class="redirectMsg">.*?<a href="/index\.php/([^"#]+)[^"]*"', re.DOTALL
)


# ---------------------------------------------------------------------------
# Tiny stdlib YAML-frontmatter mini-parser
# ---------------------------------------------------------------------------

def split_frontmatter(text: str) -> tuple[str, str, str]:
    """Split a node file's text into (frontmatter_raw, body, newline_style).

    Frontmatter is between the first two '---' lines. Returns the raw
    frontmatter block (without the '---' delimiters) and the body (everything
    after the closing '---' line, including its own leading blank line handling
    left to the caller).
    """
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("File does not start with '---' frontmatter delimiter")
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        raise ValueError("No closing '---' found for frontmatter")
    frontmatter_raw = "".join(lines[1:end_idx])
    body = "".join(lines[end_idx + 1 :])
    return frontmatter_raw, body, ""


def parse_frontmatter(raw: str) -> dict:
    """Parse simple 'key: value' frontmatter lines (scalars only — sufficient
    for this project's node schema: name, type, slug, aliases, confidence,
    wiki_source, bucket_id, prompt_version, node_version, pass_origin,
    first_available, disambiguation_hub, etc).

    Multi-line block scalars / nested maps are NOT supported (none are used
    in node frontmatter as of this writing) — such lines are preserved
    verbatim in the raw text for round-tripping but not exposed as parsed
    keys beyond their first line.
    """
    result: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        result[key] = unquote_yaml_scalar(value)
    return result


def unquote_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1]
    if len(value) >= 2 and value[0] == "'" and value[-1] == "'":
        return value[1:-1]
    return value


# ---------------------------------------------------------------------------
# Node index
# ---------------------------------------------------------------------------

class NodeRecord:
    __slots__ = ("path", "slug", "name", "frontmatter_raw", "wiki_source", "node_version")

    def __init__(self, path: Path, slug: str, name: str, frontmatter_raw: str,
                 wiki_source: str | None, node_version: int | None):
        self.path = path
        self.slug = slug
        self.name = name
        self.frontmatter_raw = frontmatter_raw
        self.wiki_source = wiki_source
        self.node_version = node_version


def build_node_index(nodes_root: Path, warnings: list[str]) -> dict[str, NodeRecord]:
    """slug -> NodeRecord, scanning ALL node dirs recursively."""
    index: dict[str, NodeRecord] = {}
    for path in sorted(nodes_root.rglob("*.node.md")):
        try:
            text = path.read_text(encoding="utf-8")
            frontmatter_raw, _body, _nl = split_frontmatter(text)
            fm = parse_frontmatter(frontmatter_raw)
        except Exception as exc:  # noqa: BLE001 - collect and continue
            warnings.append(f"WARN: could not parse frontmatter in {path}: {exc}")
            continue
        slug = fm.get("slug") or path.stem.replace(".node", "")
        name = fm.get("name") or slug
        node_version_raw = fm.get("node_version")
        try:
            node_version = int(node_version_raw) if node_version_raw is not None else None
        except ValueError:
            node_version = None
        if slug in index:
            warnings.append(f"WARN: duplicate slug '{slug}' — {path} shadows {index[slug].path}")
        index[slug] = NodeRecord(
            path=path,
            slug=slug,
            name=name,
            frontmatter_raw=frontmatter_raw,
            wiki_source=fm.get("wiki_source"),
            node_version=node_version,
        )
    return index


def wiki_source_to_page_name(wiki_source: str) -> str | None:
    """https://awoiaf.westeros.org/index.php/Aegon_Targaryen_(son_of_Baelon)
    -> "Aegon Targaryen (son of Baelon)"
    """
    if not wiki_source or "/index.php/" not in wiki_source:
        return None
    segment = wiki_source.split("/index.php/", 1)[1]
    segment = segment.split("#", 1)[0]  # strip any fragment
    decoded = unquote(segment)
    return decoded.replace("_", " ")


# ---------------------------------------------------------------------------
# page-categories.jsonl
# ---------------------------------------------------------------------------

def load_page_categories(path: Path, warnings: list[str]) -> dict[str, list[str]]:
    """page name -> list of categories."""
    result: dict[str, list[str]] = {}
    if not path.exists():
        raise FileNotFoundError(f"Missing required data file: {path}")
    with path.open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                warnings.append(f"WARN: malformed JSON at {path}:{lineno}: {exc}")
                continue
            page = obj.get("page")
            cats = obj.get("categories")
            if not page or not isinstance(cats, list):
                warnings.append(f"WARN: missing page/categories at {path}:{lineno}")
                continue
            result[page] = cats
    return result


def life_years_from_categories(categories: list[str]) -> tuple[int | None, int | None]:
    born = died = None
    for cat in categories:
        m = CATEGORY_YEAR_RE.match(cat.strip())
        if not m:
            continue
        year = int(m.group(1))
        era = m.group(2)
        kind = m.group(3)
        signed_year = -year if era == "BC" else year
        if kind == "births":
            born = signed_year
        else:
            died = signed_year
    return born, died


def is_disambiguation_page(categories: list[str]) -> bool:
    return "Disambiguation pages" in categories


def is_redirect_page(categories: list[str]) -> bool:
    return "Redirect" in categories


# ---------------------------------------------------------------------------
# Redirect-target parsing (reads sources/wiki/_raw/<Page>.json only — cached,
# no re-fetch, no LLM; see feedback_no_external_wiki_fetch)
# ---------------------------------------------------------------------------

def page_name_to_raw_path(page_name: str, raw_wiki_root: Path) -> Path:
    """"Aenys Targaryen" -> sources/wiki/_raw/Aenys_Targaryen.json

    Mirrors the MediaWiki space->underscore convention used when the crawl
    saved each page's cache file (the inverse of wiki_source_to_page_name).
    """
    return raw_wiki_root / f"{page_name.replace(' ', '_')}.json"


def parse_redirect_target_page(raw_path: Path, warnings: list[str]) -> str | None:
    """Parse the cached page's `redirectMsg` HTML block for its target page
    name. Returns None (with a warning) if the file is missing, unreadable,
    or does not actually contain a redirectMsg block — this can legitimately
    happen when a page's `page-categories.jsonl` category snapshot says
    `Redirect` but the cached HTML is a real infobox page (verified anomaly:
    `Timett (father)`, 2026-07-06) — treated as a data mismatch, not a crash.
    """
    if not raw_path.exists():
        warnings.append(f"WARN: redirect target parse — missing raw cache file {raw_path}")
        return None
    try:
        obj = json.loads(raw_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"WARN: redirect target parse — could not read/parse {raw_path}: {exc}")
        return None
    html = obj.get("html", "")
    m = REDIRECT_MSG_RE.search(html)
    if not m:
        warnings.append(
            f"WARN: redirect target parse — page-categories.jsonl says 'Redirect' but no "
            f"redirectMsg block found in {raw_path} (category/cache mismatch — not blocked "
            f"as a redirect trap; left for human review)"
        )
        return None
    target_segment = m.group(1)
    return unquote(target_segment).replace("_", " ")


# ---------------------------------------------------------------------------
# edges.jsonl discriminators
# ---------------------------------------------------------------------------

class EdgeIndex:
    """Slug-keyed indices over wiki-infobox edges, built with one linear pass."""

    def __init__(self):
        # parent_of[target_slug] -> list of source_slug (parents)
        self.parents: dict[str, list[str]] = {}
        # spouse[slug] -> list of other-slug
        self.spouse: dict[str, list[str]] = {}
        # sworn_to[source_slug] -> list of target_slug
        self.sworn_to: dict[str, list[str]] = {}
        # holds_title[source_slug] -> list of target_slug (ordered by first-seen)
        self.holds_title: dict[str, list[str]] = {}


def build_edge_index(path: Path, warnings: list[str]) -> EdgeIndex:
    idx = EdgeIndex()
    if not path.exists():
        raise FileNotFoundError(f"Missing required data file: {path}")
    with path.open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                warnings.append(f"WARN: malformed JSON at {path}:{lineno}: {exc}")
                continue
            if obj.get("evidence_kind") != "wiki-infobox":
                continue
            edge_type = obj.get("edge_type")
            source_slug = obj.get("source_slug")
            target_slug = obj.get("target_slug")
            if not edge_type or not source_slug or not target_slug:
                continue
            if edge_type == "PARENT_OF":
                idx.parents.setdefault(target_slug, [])
                if source_slug not in idx.parents[target_slug]:
                    idx.parents[target_slug].append(source_slug)
            elif edge_type == "SPOUSE_OF":
                idx.spouse.setdefault(source_slug, [])
                idx.spouse.setdefault(target_slug, [])
                if target_slug not in idx.spouse[source_slug]:
                    idx.spouse[source_slug].append(target_slug)
                if source_slug not in idx.spouse[target_slug]:
                    idx.spouse[target_slug].append(source_slug)
            elif edge_type == "SWORN_TO":
                idx.sworn_to.setdefault(source_slug, [])
                if target_slug not in idx.sworn_to[source_slug]:
                    idx.sworn_to[source_slug].append(target_slug)
            elif edge_type == "HOLDS_TITLE":
                idx.holds_title.setdefault(source_slug, [])
                if target_slug not in idx.holds_title[source_slug]:
                    idx.holds_title[source_slug].append(target_slug)
    return idx


# ---------------------------------------------------------------------------
# Cluster key derivation
# ---------------------------------------------------------------------------

ROMAN_NUMERAL_TOKEN_RE = re.compile(
    r"^(?=[MDCLXVI])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$",
    re.IGNORECASE,
)


def is_regnal_numeral_token(token: str) -> bool:
    """True if token is a standalone Roman numeral I..X-ish (bounded per spec:
    "up to X"). We accept any well-formed Roman numeral token 1-39 range
    (covers every regnal number in the setting: Aegon V, Maegor I, etc.),
    guarding against over-matching plain words ("I", "V" alone still match —
    intentional, they ARE valid single-letter regnal numerals in this corpus,
    e.g. "Aegon I").
    """
    if not token:
        return False
    if not ROMAN_NUMERAL_TOKEN_RE.match(token.upper()):
        return False
    # Reject empty match (the regex allows an all-zero-width match for "").
    return token.upper() != ""


def strip_parenthetical(name: str) -> str:
    return PARENTHETICAL_RE.sub("", name).strip()


def extract_regnal(name_no_parens: str) -> tuple[str, str | None]:
    """Return (name_without_regnal, regnal_numeral_or_None)."""
    tokens = name_no_parens.split()
    regnal = None
    kept_tokens = []
    for tok in tokens:
        cleaned = tok.strip()
        if regnal is None and is_regnal_numeral_token(cleaned):
            regnal = cleaned.upper()
            continue
        kept_tokens.append(tok)
    return " ".join(kept_tokens), regnal


def cluster_key_for_name(name: str) -> tuple[str, str | None]:
    """Return (cluster_key, regnal). Cluster key = lowercase, whitespace-
    collapsed name with parentheticals and standalone regnal numerals
    stripped.
    """
    no_parens = strip_parenthetical(name)
    no_regnal, regnal = extract_regnal(no_parens)
    key = re.sub(r"\s+", " ", no_regnal).strip().lower()
    return key, regnal


# ---------------------------------------------------------------------------
# era heuristic (best-effort, optional)
# ---------------------------------------------------------------------------

def derive_era(born: int | None, died: int | None) -> str | None:
    ref_year = died if died is not None else born
    if ref_year is None:
        return None
    if ref_year <= 37:
        return "targaryen-conquest"
    if 129 <= ref_year <= 131:
        return "dance-of-the-dragons"
    return None


# ---------------------------------------------------------------------------
# name lookup / prettification for parent & spouse slugs
# ---------------------------------------------------------------------------

def prettify_slug(slug: str) -> str:
    """Fallback: turn a slug into a readable name when it's not in the node
    index. Replace hyphens with spaces, title-case. Simplest acceptable
    per spec — does not attempt to strip qualifier suffixes.
    """
    return " ".join(part.capitalize() for part in slug.split("-"))


def slug_to_name(slug: str, node_index: dict[str, NodeRecord]) -> str:
    rec = node_index.get(slug)
    if rec is not None and rec.name:
        return rec.name
    return prettify_slug(slug)


def build_member_discriminators(rec: "NodeRecord", regnal: str | None,
                                  node_index: dict[str, NodeRecord],
                                  edge_index: EdgeIndex,
                                  page_categories: dict[str, list[str]]) -> dict:
    """The per-slug discriminator-field dict shared by cluster members
    (build_pack) AND singleton candidates (--compose-singletons). Extracted
    so both paths compute life-years/parents/spouse/allegiance/title exactly
    the same way — same field priority, same sources (page-categories.jsonl
    for life-years, edges.jsonl wiki-infobox edges for the rest).
    """
    page_name = wiki_source_to_page_name(rec.wiki_source) if rec.wiki_source else None
    cats = page_categories.get(page_name, []) if page_name else []
    born, died = life_years_from_categories(cats)

    slug = rec.slug
    parents = edge_index.parents.get(slug, [])
    spouse = edge_index.spouse.get(slug, [])
    sworn_to = edge_index.sworn_to.get(slug, [])
    allegiance = sworn_to[0] if sworn_to else None
    holds_title = edge_index.holds_title.get(slug, [])
    key_title = holds_title[0] if holds_title else None

    return {
        "regnal": regnal,
        "parents": parents,
        "spouse": spouse,
        "born": born,
        "died": died,
        "era": derive_era(born, died),
        "allegiance": allegiance,
        "key_title": key_title,
    }


# ---------------------------------------------------------------------------
# --build-pack
# ---------------------------------------------------------------------------

def build_pack(nodes_root: Path, edges_path: Path, categories_path: Path,
               clusters_out: Path, blocklist_out: Path,
               raw_wiki_root: Path = RAW_WIKI_ROOT_DEFAULT,
               redirect_map_out: Path = REDIRECT_MAP_OUT_DEFAULT) -> dict:
    warnings: list[str] = []
    node_index = build_node_index(nodes_root, warnings)
    edge_index = build_edge_index(edges_path, warnings)
    page_categories = load_page_categories(categories_path, warnings)

    # Scope for clustering: character nodes only (v1 scope per design §4).
    character_dir = nodes_root / "characters"
    character_slugs = [
        slug for slug, rec in node_index.items()
        if character_dir in rec.path.parents
    ]

    # Reverse index: wiki page name -> node slug. Used to resolve a redirect
    # node's target PAGE (parsed from cached HTML) to a target node SLUG.
    # Built once here from node_index (same wiki_source_to_page_name join the
    # blocklist loop below already does per-node).
    page_to_slug: dict[str, str] = {}
    for slug, rec in node_index.items():
        if not rec.wiki_source:
            continue
        page_name = wiki_source_to_page_name(rec.wiki_source)
        if page_name and page_name not in page_to_slug:
            page_to_slug[page_name] = slug

    # Blocklist scans ALL node dirs (not just characters). Two trap kinds:
    #   - "disambiguation": wiki page category `Disambiguation pages`.
    #   - "redirect": wiki page category `Redirect` (NEW). Also produces the
    #     separate redirect-node-map.json routing table.
    # Value shape is {"page": <wiki page name>, "trap_kind": "redirect"|"disambiguation"}
    # (richer than the old flat {slug: page_name} — the two trap kinds MUST
    # stay distinguishable for downstream consumers per this pass's brief).
    blocklist: dict[str, dict] = {}
    redirect_map: dict[str, dict] = {}
    redirect_slugs: set[str] = set()

    for slug, rec in node_index.items():
        if not rec.wiki_source:
            continue
        page_name = wiki_source_to_page_name(rec.wiki_source)
        if not page_name:
            continue
        cats = page_categories.get(page_name)
        if cats is None:
            continue
        if is_disambiguation_page(cats):
            blocklist[slug] = {"page": page_name, "trap_kind": "disambiguation"}
        elif is_redirect_page(cats):
            raw_path = page_name_to_raw_path(page_name, raw_wiki_root)
            target_page = parse_redirect_target_page(raw_path, warnings)
            if target_page is None:
                # Category/cache mismatch (verified anomaly: Timett (father))
                # — NOT blocklisted as a redirect trap; left for human review,
                # flows through as an ordinary cluster member instead.
                continue
            target_slug = page_to_slug.get(target_page)
            if target_slug is None:
                warnings.append(
                    f"WARN: redirect target page '{target_page}' (from node '{slug}') "
                    f"has no corresponding node in the graph — target_slug recorded as null"
                )
            redirect_map[slug] = {"target_page": target_page, "target_slug": target_slug}
            blocklist[slug] = {"page": page_name, "trap_kind": "redirect"}
            redirect_slugs.add(slug)

    # Cluster assembly over character nodes.
    # cluster_key -> {"real": {slug: member_dict}, "traps": [slug, ...], "redirects": [slug, ...]}
    clusters: dict[str, dict] = {}

    for slug in character_slugs:
        rec = node_index[slug]
        key, regnal = cluster_key_for_name(rec.name)
        cluster = clusters.setdefault(key, {"real": {}, "traps": [], "redirects": []})

        if slug in redirect_slugs:
            cluster["redirects"].append(slug)
            continue

        is_trap = slug in blocklist
        if is_trap:
            cluster["traps"].append(slug)
            continue

        cluster["real"][slug] = build_member_discriminators(
            rec, regnal, node_index, edge_index, page_categories,
        )

    # Filter: include a cluster when it has >=2 real members, OR >=1 real
    # member plus >=1 trap/redirect node. Redirect-only companions to a real
    # member still warrant inclusion (that's exactly the confusability this
    # pass targets — e.g. "robert baratheon": robert-i-baratheon + the
    # redirect stub robert-baratheon).
    final_clusters: dict[str, dict] = {}
    for key in sorted(clusters.keys()):
        cluster = clusters[key]
        real = cluster["real"]
        traps = sorted(cluster["traps"])
        redirects = sorted(cluster["redirects"])
        if len(real) >= 2 or (len(real) >= 1 and (len(traps) >= 1 or len(redirects) >= 1)):
            final_clusters[key] = {
                "members": {slug: real[slug] for slug in sorted(real.keys())},
                "trap_nodes": traps,
                "redirect_nodes": redirects,
            }

    clusters_out.parent.mkdir(parents=True, exist_ok=True)
    with clusters_out.open("w", encoding="utf-8") as fh:
        json.dump(final_clusters, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")

    blocklist_out.parent.mkdir(parents=True, exist_ok=True)
    blocklist_sorted = {slug: blocklist[slug] for slug in sorted(blocklist.keys())}
    with blocklist_out.open("w", encoding="utf-8") as fh:
        # Dict form {slug: {"page": ..., "trap_kind": ...}} — the F&B
        # reconciler gets the wiki page name AND the trap kind for free
        # without a second join back through node frontmatter. (Was a flat
        # {slug: page_name} map before redirect traps were added; the richer
        # shape is what keeps the two trap kinds distinguishable.)
        json.dump(blocklist_sorted, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")

    redirect_map_out.parent.mkdir(parents=True, exist_ok=True)
    redirect_map_sorted = {slug: redirect_map[slug] for slug in sorted(redirect_map.keys())}
    with redirect_map_out.open("w", encoding="utf-8") as fh:
        json.dump(redirect_map_sorted, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")

    return {
        "warnings": warnings,
        "node_index": node_index,
        "edge_index": edge_index,
        "page_categories": page_categories,
        "clusters": final_clusters,
        "blocklist": blocklist_sorted,
        "redirect_map": redirect_map_sorted,
        "character_slug_count": len(character_slugs),
        "total_node_count": len(node_index),
    }


# ---------------------------------------------------------------------------
# Identity line composition
# ---------------------------------------------------------------------------

DISCRIMINATOR_FIELD_COUNT_KEYS = (
    "life_years_present", "parents", "spouse", "allegiance", "title", "regnal",
)


def format_year_label(year: int) -> str:
    """A signed in-story year -> its era-suffixed display label, e.g.
    -27 -> '27 BC', 37 -> '37 AC'."""
    return f"{-year} BC" if year < 0 else f"{year} AC"


def format_year_range(born: int | None, died: int | None) -> str | None:
    """Render a life-year parenthetical. Handles BC/AC and cross-era spans
    correctly (never prints a bare negative number):
      both known, same era:    (84-85 AC)      -- era suffix printed ONCE
      both known, cross-era:   (27 BC-37 AC)   -- era suffix on BOTH ends
      born only:                (b. 136 AC)
      died only:                (d. 283 AC)
      neither:                  None (omit the paren entirely)
    """
    if born is None and died is None:
        return None
    if born is not None and died is not None:
        born_is_bc = born < 0
        died_is_bc = died < 0
        if born_is_bc == died_is_bc:
            # Same era: print the shared era suffix once, at the end.
            era = "BC" if born_is_bc else "AC"
            born_num = -born if born_is_bc else born
            died_num = -died if died_is_bc else died
            return f"({born_num}–{died_num} {era})"
        # Cross-era span (e.g. born 27 BC, died 37 AC): each end needs its
        # own era suffix since they differ.
        return f"({format_year_label(born)}–{format_year_label(died)})"
    if born is not None:
        return f"(b. {format_year_label(born)})"
    return f"(d. {format_year_label(died)})"


def cluster_display_name(cluster_key: str, trap_slugs: list[str],
                          node_index: dict[str, NodeRecord]) -> str:
    """The name used for the CLUSTER (not any one member) in cross-pointer
    sentences and the trap-hub line: the trap node's own `name` frontmatter
    if the cluster has a trap node (that IS the disambiguation hub's name —
    e.g. "Aegon Targaryen", not a specific regnal member like "Aegon I
    Targaryen"); else the cluster key, title-cased, as a fallback for
    trap-less clusters.
    """
    if trap_slugs:
        trap_rec = node_index.get(sorted(trap_slugs)[0])
        if trap_rec is not None and trap_rec.name:
            return trap_rec.name
    return cluster_key.title()


def page_name_to_wiki_cite(page_name: str) -> str:
    """"Wat (Standfast)" -> "Wat_(Standfast)" — matches the `(wiki:Page_Name)`
    convention already used throughout wiki-sourced node prose (see e.g.
    graph/nodes/artifacts/lightbringer.node.md): spaces become underscores,
    everything else is left as-is (no URL-encoding of parens/apostrophes —
    the existing convention doesn't encode those either).
    """
    return page_name.replace(" ", "_")


def append_wiki_sentence(composed_line: str, sentence: str | None,
                           source_page: str | None, cite: bool) -> str:
    """Append a cached Haiku-enriched distinguishing sentence to an already-
    composed Identity line (thin members only — see --enrich-thin / the
    thin-sentences.jsonl cache). No-op (returns composed_line unchanged) if
    sentence is None/empty.

    When cite=True (the --apply path), a trailing Tier-2 wiki cite marker is
    appended in the project's existing `(wiki:Page_Name)` convention so the
    new fact carries provenance like any other wiki-sourced claim (§5 of the
    design: "a new fact from wiki lead prose is Tier-2 wiki-sourced and
    cited, same as any wiki claim"). --compose's preview never cites (cite=
    False) — it's plain preview text, not the applied artifact.
    """
    if not sentence:
        return composed_line
    suffix = f" {sentence}"
    if cite and source_page:
        suffix += f" (wiki:{page_name_to_wiki_cite(source_page)})"
    return composed_line + suffix


def compose_member_identity_line(name: str, member: dict, node_index: dict[str, NodeRecord],
                                   cluster_key: str, cluster_size: int,
                                   cluster_name: str, has_trap: bool) -> tuple[str, int]:
    """Returns (composed_line, discriminator_field_count).

    cluster_name is the CLUSTER's own display name (see cluster_display_name)
    — used for the cross-pointer sentence, NOT this particular member's own
    name (a member is never its own disambiguation hub).
    """
    clauses: list[str] = []
    field_count = 0

    year_range = format_year_range(member.get("born"), member.get("died"))
    if year_range:
        field_count += 1

    parents = member.get("parents") or []
    if parents:
        field_count += 1
        parent_names = [slug_to_name(s, node_index) for s in parents]
        clauses.append(f"child of {' and '.join(parent_names)}")

    spouse = member.get("spouse") or []
    if spouse:
        field_count += 1
        spouse_names = [slug_to_name(s, node_index) for s in spouse]
        clauses.append(f"married to {' and '.join(spouse_names)}")

    allegiance = member.get("allegiance")
    if allegiance:
        field_count += 1
        allegiance_name = slug_to_name(allegiance, node_index)
        clauses.append(f"sworn to {allegiance_name}")

    key_title = member.get("key_title")
    if key_title:
        field_count += 1
        title_name = slug_to_name(key_title, node_index)
        clauses.append(title_name)

    if member.get("regnal"):
        field_count += 1

    head = name
    if year_range:
        head = f"{name} {year_range}"

    if clauses:
        body = "; ".join(clauses)
        line = f"{head} — {body}."
    else:
        line = f"{head}."

    if cluster_size > 1:
        if has_trap:
            line += (f" One of {cluster_size} {cluster_name}s — see the "
                      f"{cluster_name} disambiguation entry.")
        else:
            # No trap node in this cluster -> no hub to point to. Don't emit
            # a dangling "see the disambiguation entry" clause.
            line += f" One of {cluster_size} characters named {cluster_name}."

    return line, field_count


def compose_trap_hub_line(cluster_key: str, cluster: dict, node_index: dict[str, NodeRecord],
                            hub_display_name: str) -> str:
    members = cluster["members"]
    slugs_sorted = sorted(
        members.keys(),
        key=lambda s: (members[s].get("born") if members[s].get("born") is not None else 999999, s),
    )
    max_shown = 8
    shown = slugs_sorted[:max_shown]
    remainder = len(slugs_sorted) - len(shown)

    clauses = []
    for slug in shown:
        m = members[slug]
        name = slug_to_name(slug, node_index)
        top = top_discriminator_clause(m, node_index)
        if top:
            clauses.append(f"{name} ({top})")
        else:
            clauses.append(name)

    tail = f"; ({remainder} more)" if remainder > 0 else ""
    body = "; ".join(clauses) + tail
    return (
        f'Disambiguation entry — "{hub_display_name}" may refer to: {body} '
        f"({len(slugs_sorted)} members)."
    )


def compose_redirect_line(redirect_slug: str, redirect_map_entry: dict,
                            node_index: dict[str, NodeRecord]) -> str:
    """Compose the Identity line for a redirect-trap node (design NEW, this
    pass): distinct from a disambiguation hub line — points at exactly ONE
    canonical target rather than listing members.

      'Redirect — "Aenys Targaryen" refers to Aenys I Targaryen.'

    Uses the redirect node's own display `name` (from node_index) as the
    quoted source phrase, and the target node's display name if the target
    resolved to a node in the graph; else falls back to the raw wiki target
    page string (target_slug may be null — e.g. a redirect to a page with no
    node yet, such as House Baelish/House Leygood at time of writing).
    """
    rec = node_index.get(redirect_slug)
    source_name = rec.name if rec is not None else prettify_slug(redirect_slug)

    target_slug = redirect_map_entry.get("target_slug")
    if target_slug:
        target_display = slug_to_name(target_slug, node_index)
    else:
        target_display = redirect_map_entry.get("target_page") or "an unresolved page"

    return f'Redirect — "{source_name}" refers to {target_display}.'


def top_discriminator_clause(member: dict, node_index: dict[str, NodeRecord]) -> str | None:
    """One clause, top-priority discriminator, for the trap-hub line."""
    born, died = member.get("born"), member.get("died")
    if member.get("regnal") and (born is not None or died is not None):
        yr = format_year_range(born, died)
        return f"r. {yr.strip('()')}" if yr else f"regnal {member['regnal']}"
    if member.get("regnal"):
        return f"regnal {member['regnal']}"
    yr = format_year_range(born, died)
    if yr:
        return yr.strip("()")
    parents = member.get("parents") or []
    if parents:
        return f"child of {slug_to_name(parents[0], node_index)}"
    allegiance = member.get("allegiance")
    if allegiance:
        return f"sworn to {slug_to_name(allegiance, node_index)}"
    return None


def is_thin(field_count: int) -> bool:
    return field_count < 2


# ---------------------------------------------------------------------------
# Thin-member enrichment (--enrich-thin)
#
# The composer's own thin-set computation, extracted so --enrich-thin can
# recompute "exactly what --compose would call thin" without duplicating the
# cluster-walk logic. Returns one row per thin REAL cluster member (trap and
# redirect nodes are never thin — they don't go through
# compose_member_identity_line's field-count path).
# ---------------------------------------------------------------------------

def compute_thin_members(pack: dict) -> list[dict]:
    """Returns a list of {"slug", "name", "cluster_key"} for every thin real
    cluster member, in the same order --compose walks clusters (sorted keys,
    then sorted member slugs) so output is stable run-to-run.
    """
    node_index: dict[str, NodeRecord] = pack["node_index"]
    clusters: dict[str, dict] = pack["clusters"]

    thin: list[dict] = []
    for cluster_key in sorted(clusters.keys()):
        cluster = clusters[cluster_key]
        members = cluster["members"]
        traps = cluster["trap_nodes"]
        cluster_size = len(members)
        cluster_name = cluster_display_name(cluster_key, traps, node_index)
        has_trap = bool(traps)

        for slug in sorted(members.keys()):
            member = members[slug]
            rec = node_index.get(slug)
            name = rec.name if rec else prettify_slug(slug)
            _composed_line, field_count = compose_member_identity_line(
                name, member, node_index, cluster_key, cluster_size,
                cluster_name, has_trap,
            )
            if is_thin(field_count):
                thin.append({"slug": slug, "name": name, "cluster_key": cluster_key})

    return thin


# --- thin-sentences.jsonl cache I/O -----------------------------------------

def load_thin_sentences_cache(cache_path: Path) -> dict[str, dict]:
    """slug -> {"slug","sentence","source_page","origin","enriched_at"}."""
    cache: dict[str, dict] = {}
    if not cache_path.exists():
        return cache
    with cache_path.open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"WARN: malformed JSON at {cache_path}:{lineno}: {exc}", file=sys.stderr)
                continue
            slug = row.get("slug")
            if not slug:
                continue
            cache[slug] = row
    return cache


def write_thin_sentences_cache(cache_path: Path, cache: dict[str, dict]) -> None:
    """Rewrite the cache file in full, one row per slug, sorted by slug for a
    stable diff. Atomic write (temp + rename) — this file is committed.
    """
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_path_str = tempfile.mkstemp(
        dir=str(cache_path.parent), prefix=f".{cache_path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as fh:
            for slug in sorted(cache.keys()):
                fh.write(json.dumps(cache[slug], ensure_ascii=False) + "\n")
        os.replace(tmp_path_str, cache_path)
    finally:
        if os.path.exists(tmp_path_str):
            os.remove(tmp_path_str)


def seed_cache_from_batches(cache: dict[str, dict], enrichment_dir: Path,
                              batch_glob: str, warnings: list[str]) -> int:
    """Merge every thin-batch-*.jsonl file into `cache` (mutated in place).
    Dedup by slug — a slug already in the cache (any origin) is left alone
    (idempotent: re-running the seed step changes nothing once seeded).
    Returns the count of NEWLY seeded rows.
    """
    seeded = 0
    batch_paths = sorted(enrichment_dir.glob(batch_glob))
    for batch_path in batch_paths:
        with batch_path.open(encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    warnings.append(f"WARN: malformed JSON at {batch_path}:{lineno}: {exc}")
                    continue
                slug = row.get("slug")
                if not slug:
                    warnings.append(f"WARN: missing slug at {batch_path}:{lineno}")
                    continue
                if slug in cache:
                    continue
                cache[slug] = {
                    "slug": slug,
                    "sentence": row.get("sentence"),
                    "source_page": row.get("source_page"),
                    "origin": "subagent-batch",
                    "enriched_at": None,
                }
                seeded += 1
    return seeded


# --- lead-prose extraction (local cache only, no re-fetch) ------------------

def extract_lead_prose(raw_path: Path, warnings: list[str]) -> str | None:
    """Read sources/wiki/_raw/<Page>.json and return the plain-text lead
    prose — the first direct <p> child of the page's main content div that
    is NOT a hatnote/disambiguation notice and has non-trivial text. Strips
    the infobox (it is a sibling <table>, never inside a <p>). Returns None
    (with a warning) if the file is missing/unreadable, has no `html` key,
    is a redirect stub (no real content), or no qualifying lead <p> is found
    (e.g. an infobox-only stub with zero prose — a legitimately contentless
    page, not an error).
    """
    if not raw_path.exists():
        warnings.append(f"WARN: lead-prose extract — missing raw cache file {raw_path}")
        return None
    try:
        obj = json.loads(raw_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"WARN: lead-prose extract — could not read/parse {raw_path}: {exc}")
        return None

    html = obj.get("html", "")
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    main_div = soup.find("div", class_="mw-parser-output")
    if main_div is None:
        return None

    for child in main_div.find_all("p", recursive=False):
        if not isinstance(child, Tag):
            continue
        classes = child.get("class") or []
        if "hatnote" in classes:
            continue
        text = child.get_text(" ", strip=True)
        text = re.sub(r"\s*\[\d+\]", "", text)  # strip [1]-style cite markers
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) >= 15:  # skip empty/near-empty paragraphs
            return text

    return None


# --- prompt + claude -p invocation -------------------------------------------

ENRICH_PROMPT_TEMPLATE = """Here is the wiki lead for {name}:

{lead_text}

In ONE sentence (at most 30 words), state the single most identity-fixing fact that distinguishes this {name} from others of the same name. Wiki facts only, no speculation, no preamble, no markdown. If the text above is contentless (too short or generic to yield a distinguishing fact), output exactly NULL and nothing else.

Output ONLY the sentence (or NULL). No quotation marks, no explanation."""


def build_enrich_prompt(name: str, lead_text: str) -> str:
    return ENRICH_PROMPT_TEMPLATE.format(name=name, lead_text=lead_text)


def validate_haiku_sentence(raw_output: str) -> tuple[str | None, str | None]:
    """Validate a claude -p sentence response.

    Returns (sentence_or_None, error_or_None). sentence is None (no error)
    when the model legitimately returned NULL (contentless page). error is
    set when the output fails validation (multi-line, empty, too long,
    markdown/preamble-looking) — caller should retry or quarantine.
    """
    text = raw_output.strip()
    if not text:
        return None, "empty output"
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(lines) > 1:
        return None, f"multi-line output ({len(lines)} lines)"
    line = lines[0].strip()
    if line.upper() == "NULL":
        return None, None
    if line.startswith("```") or line.startswith("#"):
        return None, "markdown-looking output"
    word_count = len(line.split())
    if word_count > HAIKU_MAX_SENTENCE_WORDS:
        return None, f"too long ({word_count} words)"
    if not line:
        return None, "empty after stripping"
    return line, None


def call_haiku_for_sentence(name: str, lead_text: str, model: str,
                              timeout_s: int = HAIKU_TIMEOUT_SECONDS,
                              max_retries: int = HAIKU_MAX_RETRIES) -> tuple[str | None, str | None]:
    """ONE (plus bounded retries) claude -p subprocess call for a single
    distinguishing sentence. Mirrors scripts/stage4-haiku-run.py's / edge-
    reify-backfill.py's claude -p invocation conventions: cwd=/tmp (skips
    loading the project's CLAUDE.md — ~49% cheaper per
    reference_llm_pass_via_claude_p), --model flag, bounded timeout.

    Returns (sentence_or_None, error_or_None). error is set only on a
    quarantine-worthy failure (row-level — caller continues the run, never
    crashes the whole pass, per the project's other bulk-pass conventions).
    """
    prompt = build_enrich_prompt(name, lead_text)
    cmd = ["claude", "-p", "--model", model, prompt]

    last_error: str | None = None
    for attempt in range(max_retries + 1):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="/tmp",  # MUST be /tmp per reference_llm_pass_via_claude_p memory
                timeout=timeout_s,
            )
        except subprocess.TimeoutExpired:
            last_error = f"timed out after {timeout_s}s (attempt {attempt + 1})"
            continue

        if result.returncode != 0:
            stderr_snippet = (result.stderr or "").strip()[:300]
            last_error = f"claude -p exited {result.returncode}: {stderr_snippet}"
            continue

        sentence, err = validate_haiku_sentence(result.stdout)
        if err is None:
            return sentence, None
        last_error = err
        # validation failure is worth one retry (model may have added
        # preamble/markdown on a fluke) but not infinite retries.

    return None, last_error or "unknown failure"


# --- --enrich-thin runner -----------------------------------------------------

def run_enrich_thin(pack: dict, cache_path: Path, enrichment_dir: Path,
                      raw_wiki_root: Path, batch_glob: str,
                      model: str, sleep_s: float, limit: int | None,
                      dry_run: bool, force_slug: str | None) -> dict:
    """The --enrich-thin subcommand body. Returns a summary dict for the CLI
    to print. Never raises on a per-row failure — quarantines instead.
    """
    node_index: dict[str, NodeRecord] = pack["node_index"]
    warnings: list[str] = list(pack.get("warnings", []))

    cache = load_thin_sentences_cache(cache_path)
    cache_before = len(cache)

    seeded = seed_cache_from_batches(cache, enrichment_dir, batch_glob, warnings)
    if seeded and not dry_run:
        write_thin_sentences_cache(cache_path, cache)

    thin_members = compute_thin_members(pack)

    if force_slug:
        targets = [m for m in thin_members if m["slug"] == force_slug]
        if not targets:
            # Allow forcing a slug even if it's not currently thin (useful
            # for smoke-testing a known cached slug per the brief).
            rec = node_index.get(force_slug)
            if rec is not None:
                targets = [{"slug": force_slug, "name": rec.name, "cluster_key": None}]
            else:
                warnings.append(f"WARN: --force-slug {force_slug!r} not found in node index")
                targets = []
        cache_misses = targets
    else:
        cache_misses = [m for m in thin_members if m["slug"] not in cache]

    if limit is not None:
        cache_misses = cache_misses[:limit]

    called = 0
    contentless = 0
    failed = 0
    new_rows: list[dict] = []

    for member in cache_misses:
        slug = member["slug"]
        name = member["name"]
        rec = node_index.get(slug)

        if dry_run:
            print(f"  [dry-run] would call Haiku for {slug!r} ({name})")
            continue

        if rec is None or not rec.wiki_source:
            cache[slug] = {
                "slug": slug, "sentence": None, "source_page": None,
                "origin": "claude-p", "enriched_at": None,
            }
            contentless += 1
            new_rows.append(cache[slug])
            warnings.append(f"WARN: {slug!r} has no wiki_source — recorded contentless")
            continue

        page_name = wiki_source_to_page_name(rec.wiki_source)
        raw_path = page_name_to_raw_path(page_name, raw_wiki_root) if page_name else None
        lead_text = extract_lead_prose(raw_path, warnings) if raw_path else None

        if not lead_text:
            cache[slug] = {
                "slug": slug, "sentence": None, "source_page": page_name,
                "origin": "claude-p", "enriched_at": None,
            }
            contentless += 1
            new_rows.append(cache[slug])
            continue

        print(f"  Calling Haiku for {slug!r} ({name})...")
        sentence, error = call_haiku_for_sentence(name, lead_text, model)
        called += 1
        if sentence is None and error is not None:
            failed += 1
            warnings.append(f"WARN: {slug!r} — Haiku call failed after retries: {error}")
        elif sentence is None:
            contentless += 1

        cache[slug] = {
            "slug": slug,
            "sentence": sentence,
            "source_page": page_name,
            "origin": "claude-p",
            "enriched_at": None,
        }
        new_rows.append(cache[slug])

        if sleep_s > 0:
            time.sleep(sleep_s)

    if not dry_run and new_rows:
        write_thin_sentences_cache(cache_path, cache)

    for w in warnings:
        print(w, file=sys.stderr)

    return {
        "cache_before": cache_before,
        "cache_seeded": seeded,
        "cache_after": len(cache),
        "thin_members_total": len(thin_members),
        "cache_misses_found": len(cache_misses) if not force_slug else len(targets),
        "called": called,
        "contentless": contentless,
        "failed": failed,
        "dry_run": dry_run,
        "new_rows": new_rows,
    }


# ---------------------------------------------------------------------------
# Node body shape detection (shared by preview + writer)
# ---------------------------------------------------------------------------

# Sections that are structural/machine-generated on EVERY Pass-2 wiki node and
# therefore do NOT count as "rich prose" when distinguishing shape (a) from
# shape (b) — only ## Identity and ## Edges are guaranteed boilerplate
# scaffolding. Any OTHER section (Origins, Appearances & Description,
# Narrative Arc, Quotes, ...) signals a genuinely rich node.
STRUCTURAL_SECTION_HEADERS = {"## identity", "## edges"}


def detect_shape_and_identity_line(body: str) -> tuple[str, str | None, int | None]:
    """Returns (shape, boilerplate_line_or_None, boilerplate_line_index_or_None).

    shape is one of "a", "b", "c":
      a: has ## Identity whose only content is a boilerplate line, AND at
         most ONE non-structural section beyond ## Identity/## Edges (a
         plain or lightly-populated stub — e.g. lord-swyft [one short
         ## Origins paragraph], aegon-targaryen trap [no other sections])
      b: has ## Identity with boilerplate line, but the body ALSO carries
         MULTIPLE (>1) real prose sections beyond ## Identity/## Edges
         (Origins, Appearances & Description, Narrative Arc, Quotes, ...)
         — e.g. rhaenyra-targaryen (4 such sections)
      c: no ## Identity section at all — body starts at ## Origins or
         another section

    The a/b split does not change writer BEHAVIOR (both swap only the one
    boilerplate line and touch nothing else) — it exists purely so the
    dry-run preview can show Matt which nodes are thin stubs vs. already-rich
    nodes getting only a presentation touch-up.
    """
    lines = body.splitlines()
    section_starts = [i for i, ln in enumerate(lines) if ln.startswith("## ")]
    identity_idx = None
    for i in section_starts:
        header = lines[i].strip()
        if header.lower() == "## identity":
            identity_idx = i
            break

    if identity_idx is None:
        return "c", None, None

    # Find the end of the Identity section (next '## ' header or EOF).
    next_section_idx = None
    for i in section_starts:
        if i > identity_idx:
            next_section_idx = i
            break
    section_end = next_section_idx if next_section_idx is not None else len(lines)
    section_body_lines = lines[identity_idx + 1 : section_end]

    boilerplate_line = None
    boilerplate_idx = None
    non_blank_content_lines = 0
    for offset, ln in enumerate(section_body_lines):
        stripped = ln.strip()
        if not stripped:
            continue
        non_blank_content_lines += 1
        if BOILERPLATE_RE.match(stripped) and boilerplate_line is None:
            boilerplate_line = stripped
            boilerplate_idx = identity_idx + 1 + offset

    # "Rich" means MORE THAN ONE non-structural section header exists
    # (Origins/Appearances & Description/Narrative Arc/Quotes/...) beyond the
    # always-present ## Identity + ## Edges scaffolding. A single lone
    # ## Origins paragraph (common on thin stubs like lord-swyft — one short
    # wiki-cite sentence) is NOT enough to call the node "rich": the brief's
    # verified example (lord-swyft = shape a) has exactly that shape.
    # rhaenyra-targaryen (shape b) has 4 non-structural sections. Verified
    # against both named examples (2026-07-06).
    non_structural_section_count = sum(
        1
        for i in section_starts
        if i != identity_idx and lines[i].strip().lower() not in STRUCTURAL_SECTION_HEADERS
    )
    has_rich_sections = non_structural_section_count > 1

    if boilerplate_line is not None and non_blank_content_lines == 1:
        return ("b" if has_rich_sections else "a"), boilerplate_line, boilerplate_idx

    # Identity section exists but has no boilerplate line (real prose
    # already, or an empty/non-conforming section) — treat conservatively:
    # no planned change (boilerplate_line stays None so callers skip it).
    return ("b" if has_rich_sections else "a"), None, None


# ---------------------------------------------------------------------------
# --compose --dry-run
# ---------------------------------------------------------------------------

def compose_preview(pack: dict, preview_out: Path, nodes_root: Path,
                     thin_sentences_cache: dict[str, dict] | None = None) -> dict:
    node_index: dict[str, NodeRecord] = pack["node_index"]
    clusters: dict[str, dict] = pack["clusters"]
    redirect_map: dict[str, dict] = pack.get("redirect_map", {})
    thin_sentences_cache = thin_sentences_cache or {}

    lines: list[str] = []
    lines.append("# Wiki-Prose Identity Composer — Dry-Run Preview\n")
    lines.append(
        "Deterministic composition only. No node files were written by this run.\n"
    )

    total_real_members = 0
    total_thin_members = 0
    total_thin_with_sentence = 0
    total_redirect_nodes = 0
    shape_examples_seen: dict[str, str] = {}
    per_cluster_thin: list[tuple[str, list[str]]] = []

    for cluster_key in sorted(clusters.keys()):
        cluster = clusters[cluster_key]
        members = cluster["members"]
        traps = cluster["trap_nodes"]
        redirects = cluster.get("redirect_nodes", [])
        cluster_size = len(members)

        lines.append(f"\n## Cluster: \"{cluster_key}\" ({cluster_size} real member(s), "
                      f"{len(traps)} trap node(s), {len(redirects)} redirect node(s))\n")

        cluster_name = cluster_display_name(cluster_key, traps, node_index)
        has_trap = bool(traps)

        thin_in_cluster: list[str] = []

        for slug in sorted(members.keys()):
            member = members[slug]
            rec = node_index.get(slug)
            name = rec.name if rec else prettify_slug(slug)
            composed_line, field_count = compose_member_identity_line(
                name, member, node_index, cluster_key, cluster_size,
                cluster_name, has_trap,
            )
            thin = is_thin(field_count)
            total_real_members += 1
            cached_sentence_row = thin_sentences_cache.get(slug) if thin else None
            if thin:
                total_thin_members += 1
                thin_in_cluster.append(slug)
                if cached_sentence_row and cached_sentence_row.get("sentence"):
                    total_thin_with_sentence += 1
                    composed_line = append_wiki_sentence(
                        composed_line,
                        cached_sentence_row.get("sentence"),
                        cached_sentence_row.get("source_page"),
                        cite=False,
                    )

            shape, boilerplate_line, _idx = ("?", None, None)
            action = "SKIP (no node file found)"
            if rec is not None:
                try:
                    text = rec.path.read_text(encoding="utf-8")
                    _fm_raw, body, _nl = split_frontmatter(text)
                    shape, boilerplate_line, _idx = detect_shape_and_identity_line(body)
                except Exception as exc:  # noqa: BLE001
                    shape = "?"
                    action = f"SKIP (read error: {exc})"

                if shape in ("a", "b") and boilerplate_line is not None:
                    action = "swap boilerplate line"
                elif shape == "c":
                    action = "insert ## Identity section"
                elif boilerplate_line is None:
                    action = "SKIP (no boilerplate line found — treat as real prose, do not touch)"

                if shape not in shape_examples_seen:
                    shape_examples_seen[shape] = slug

            lines.append(f"- **{slug}** [shape {shape}, action: {action}]"
                          f"{'  THIN' if thin else ''} (fields={field_count})")
            lines.append(f"  - composed: {composed_line}")

        if thin_in_cluster:
            per_cluster_thin.append((cluster_key, thin_in_cluster))

        for trap_slug in traps:
            rec = node_index.get(trap_slug)
            hub_name = rec.name if rec else prettify_slug(trap_slug)
            hub_line = compose_trap_hub_line(cluster_key, cluster, node_index, hub_name)

            shape, boilerplate_line, _idx = ("?", None, None)
            action = "SKIP (no node file found)"
            if rec is not None:
                try:
                    text = rec.path.read_text(encoding="utf-8")
                    _fm_raw, body, _nl = split_frontmatter(text)
                    shape, boilerplate_line, _idx = detect_shape_and_identity_line(body)
                except Exception as exc:  # noqa: BLE001
                    shape = "?"
                    action = f"SKIP (read error: {exc})"

                if shape in ("a", "b") and boilerplate_line is not None:
                    action = "swap boilerplate line + stamp disambiguation_hub: true"
                elif shape == "c":
                    action = "insert ## Identity section + stamp disambiguation_hub: true"
                elif boilerplate_line is None:
                    action = "SKIP (no boilerplate line found)"

            lines.append(f"- **{trap_slug}** [TRAP NODE, shape {shape}, action: {action}]")
            lines.append(f"  - composed hub line: {hub_line}")

        for redirect_slug in redirects:
            rec = node_index.get(redirect_slug)
            entry = redirect_map.get(redirect_slug)
            total_redirect_nodes += 1

            if entry is None:
                lines.append(f"- **{redirect_slug}** [REDIRECT NODE, action: SKIP "
                              f"(no redirect-map entry found)]")
                continue

            redirect_line = compose_redirect_line(redirect_slug, entry, node_index)
            target_slug = entry.get("target_slug")
            target_display = target_slug if target_slug else "UNRESOLVED"

            shape, boilerplate_line, _idx = ("?", None, None)
            action = "SKIP (no node file found)"
            if rec is not None:
                try:
                    text = rec.path.read_text(encoding="utf-8")
                    _fm_raw, body, _nl = split_frontmatter(text)
                    shape, boilerplate_line, _idx = detect_shape_and_identity_line(body)
                except Exception as exc:  # noqa: BLE001
                    shape = "?"
                    action = f"SKIP (read error: {exc})"

                if shape in ("a", "b") and boilerplate_line is not None:
                    action = "swap boilerplate line + stamp redirect_to" if target_slug else \
                        "swap boilerplate line (target unresolved — no redirect_to stamped)"
                elif shape == "c":
                    action = "insert ## Identity section + stamp redirect_to" if target_slug else \
                        "insert ## Identity section (target unresolved — no redirect_to stamped)"
                elif boilerplate_line is None:
                    action = "SKIP (no boilerplate line found)"

            lines.append(f"- **{redirect_slug}** [REDIRECT NODE → {target_display}, "
                          f"shape {shape}, action: {action}]")
            lines.append(f"  - composed: {redirect_line}")

    thin_rate = (total_thin_members / total_real_members) if total_real_members else 0.0

    summary = []
    summary.append("\n---\n\n## Summary\n")
    summary.append(f"- Clusters in scope: {len(clusters)}")
    summary.append(f"- Total real cluster members: {total_real_members}")
    summary.append(f"- Total trap nodes: {sum(len(c['trap_nodes']) for c in clusters.values())}")
    summary.append(f"- Total redirect nodes: {total_redirect_nodes} "
                    f"(excluded from the real-member pool and thin-rate)")
    summary.append(f"- Thin members (< 2 discriminator fields): {total_thin_members}")
    summary.append(f"- Thin-rate: {thin_rate:.1%}"
                    f" ({'ABOVE' if thin_rate > 0.20 else 'below'} the 20% Haiku-residue threshold)")
    summary.append(f"- Thin members with a cached distinguishing sentence: "
                    f"{total_thin_with_sentence}/{total_thin_members}")
    summary.append(f"- Shape examples observed: {shape_examples_seen}")
    if per_cluster_thin:
        summary.append("\n### Clusters with thin members\n")
        for key, slugs in per_cluster_thin:
            summary.append(f"- \"{key}\": {', '.join(slugs)}")

    preview_out.parent.mkdir(parents=True, exist_ok=True)
    preview_out.write_text("\n".join(lines + summary) + "\n", encoding="utf-8")

    return {
        "total_real_members": total_real_members,
        "total_thin_members": total_thin_members,
        "total_thin_with_sentence": total_thin_with_sentence,
        "total_redirect_nodes": total_redirect_nodes,
        "thin_rate": thin_rate,
        "shape_examples_seen": shape_examples_seen,
        "cluster_count": len(clusters),
    }


# ---------------------------------------------------------------------------
# --compose-singletons — Identity composition for curated NON-clustered
# character slugs (marquee Fire & Blood figures with unique names, which the
# cluster-only scope above never touches: a cluster requires >=2 real members
# OR a real member + a trap/redirect companion; a unique-named character like
# Rhaenyra Targaryen never forms a cluster and so never got composed by v1).
#
# Reuses ALL existing machinery — build_member_discriminators (same field
# sources as cluster members), compose_member_identity_line (same field
# priority; called with cluster_size=1 so it never emits a cross-pointer
# clause), detect_shape_and_identity_line / apply_identity_to_node (same
# shape detection + writer). This block is a new INPUT/orchestration path
# only, not new composition logic.
# ---------------------------------------------------------------------------

# Curated default candidate list (Dance of the Dragons + Conquest/Jaehaerys
# marquee figures). Passed through the SAME inclusion filter as any
# --singleton-slugs-file list — candidates that turn out to be in-cluster or
# already-real-prose are reported as SKIPPED, not silently composed.
DEFAULT_SINGLETON_SLUGS: list[str] = [
    "rhaenyra-targaryen", "daemon-targaryen", "alicent-hightower", "otto-hightower",
    "criston-cole", "helaena-targaryen", "aemond-targaryen", "laenor-velaryon",
    "jacaerys-velaryon", "lucerys-velaryon", "joffrey-velaryon", "baela-targaryen",
    "daenaera-velaryon", "larys-strong", "harwin-strong", "lyonel-strong", "mysaria",
    "hugh-hammer", "ulf-white", "addam-velaryon", "alyn-velaryon", "unwin-peake",
    "cregan-stark", "borros-baratheon", "gwayne-hightower", "ormund-hightower",
    "tyland-lannister", "jason-lannister", "orys-baratheon", "septon-barth",
    "jaehaerys-i-targaryen", "alysanne-targaryen", "maegor-i-targaryen",
    "aenys-i-targaryen", "viserys-i-targaryen", "aegon-ii-targaryen",
    "aegon-iii-targaryen", "corlys-velaryon", "rhaenys-targaryen", "laena-velaryon",
    "rhaena-targaryen", "bloodraven", "brynden-rivers", "aegor-rivers",
    "daemon-blackfyre", "shiera-seastar", "aemma-arryn", "jocelyn-baratheon",
    "boremund-baratheon", "jeyne-arryn", "sabitha-frey",
]

def load_singleton_slug_candidates(default_list: list[str],
                                     slugs_file: Path | None) -> list[str]:
    """Returns the candidate slug list: --singleton-slugs-file (one slug per
    line, blank lines and '#'-comments ignored) if given, else default_list.
    """
    if slugs_file is None:
        return list(default_list)
    lines = slugs_file.read_text(encoding="utf-8").splitlines()
    slugs = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        slugs.append(stripped)
    return slugs


def collect_all_cluster_member_slugs(clusters: dict[str, dict]) -> set[str]:
    """Every slug that appears in ANY cluster's members/trap_nodes/
    redirect_nodes — the "already in a same-name cluster" exclusion set for
    --compose-singletons.
    """
    result: set[str] = set()
    for cluster in clusters.values():
        result.update(cluster.get("members", {}).keys())
        result.update(cluster.get("trap_nodes", []))
        result.update(cluster.get("redirect_nodes", []))
    return result


def classify_singleton_candidate(slug: str, node_index: dict[str, NodeRecord],
                                   cluster_member_slugs: set[str]) -> tuple[bool, str]:
    """Returns (included, reason). reason is a human-readable skip reason
    when included=False, or "" when included=True.

    Inclusion requires ALL of:
      (a) a node file exists for slug
      (b) slug is NOT in any cluster's members/trap_nodes/redirect_nodes
      (c) current Identity line is boilerplate, OR there is no ## Identity
          section at all (shape "c")
    """
    rec = node_index.get(slug)
    if rec is None:
        return False, "no-node (no node file found for this slug)"

    if slug in cluster_member_slugs:
        return False, "in-cluster (already handled by --compose / --apply, a same-name cluster member/trap/redirect)"

    try:
        text = rec.path.read_text(encoding="utf-8")
        _fm_raw, body, _nl = split_frontmatter(text)
    except Exception as exc:  # noqa: BLE001
        return False, f"read-error ({exc})"

    shape, boilerplate_line, _idx = detect_shape_and_identity_line(body)

    if shape == "c":
        return True, ""
    if boilerplate_line is not None:
        return True, ""
    return False, "already-real (## Identity exists and is not boilerplate — real prose, do not touch)"


def compose_singleton_identity_line(rec: NodeRecord, node_index: dict[str, NodeRecord],
                                      edge_index: EdgeIndex,
                                      page_categories: dict[str, list[str]],
                                      thin_sentences_cache: dict[str, dict],
                                      cite: bool) -> str:
    """Compose the Identity line for one singleton candidate. Same field
    priority as cluster members (life-years -> parents -> spouse ->
    allegiance -> title), via the SAME compose_member_identity_line — called
    with cluster_size=1 / has_trap=False so it never emits the "One of N ..."
    cross-pointer clause (a singleton has no cluster to point back to).

    If the slug has a cached thin-sentence (most marquee figures won't —
    that cache was built from THIN cluster members, and these are singletons
    with typically many discriminator fields already, so a hit here is
    incidental, not the common case), the cached sentence is appended
    exactly like the cluster path — with a Tier-2 (wiki:Page_Name) cite when
    cite=True (the --apply path), uncited in preview.
    """
    slug = rec.slug
    cluster_key, regnal = cluster_key_for_name(rec.name)
    member = build_member_discriminators(rec, regnal, node_index, edge_index, page_categories)

    composed_line, _field_count = compose_member_identity_line(
        rec.name, member, node_index, cluster_key, cluster_size=1,
        cluster_name=rec.name, has_trap=False,
    )

    cached_row = thin_sentences_cache.get(slug)
    if cached_row and cached_row.get("sentence"):
        composed_line = append_wiki_sentence(
            composed_line, cached_row.get("sentence"), cached_row.get("source_page"), cite=cite,
        )

    return composed_line


def compose_singletons_preview(candidate_slugs: list[str], node_index: dict[str, NodeRecord],
                                 edge_index: EdgeIndex, page_categories: dict[str, list[str]],
                                 clusters: dict[str, dict], thin_sentences_cache: dict[str, dict],
                                 preview_out: Path) -> dict:
    cluster_member_slugs = collect_all_cluster_member_slugs(clusters)

    included: list[tuple[str, str, str]] = []  # (slug, composed_line, action)
    skipped: list[tuple[str, str]] = []  # (slug, reason)

    for slug in candidate_slugs:
        ok, reason = classify_singleton_candidate(slug, node_index, cluster_member_slugs)
        if not ok:
            skipped.append((slug, reason))
            continue

        rec = node_index[slug]
        composed_line = compose_singleton_identity_line(
            rec, node_index, edge_index, page_categories, thin_sentences_cache, cite=False,
        )

        text = rec.path.read_text(encoding="utf-8")
        _fm_raw, body, _nl = split_frontmatter(text)
        shape, boilerplate_line, _idx = detect_shape_and_identity_line(body)
        if shape in ("a", "b") and boilerplate_line is not None:
            action = "swap boilerplate line"
        elif shape == "c":
            action = "insert ## Identity section"
        else:
            action = "SKIP (unexpected — no boilerplate line found after inclusion check)"

        included.append((slug, composed_line, action))

    lines: list[str] = []
    lines.append("# Wiki-Prose Identity Composer — Singleton Preview\n")
    lines.append(
        "Deterministic composition only, for curated NON-clustered character slugs "
        "(marquee figures that never form a same-name cluster). No node files were "
        "written by this run.\n"
    )
    lines.append(f"\n## Included ({len(included)})\n")
    for slug, composed_line, action in included:
        lines.append(f"- **{slug}** [action: {action}]")
        lines.append(f"  - composed: {composed_line}")

    lines.append(f"\n## Skipped ({len(skipped)})\n")
    for slug, reason in skipped:
        lines.append(f"- **{slug}** — {reason}")

    lines.append("\n---\n\n## Summary\n")
    lines.append(f"- Candidates: {len(candidate_slugs)}")
    lines.append(f"- Included: {len(included)}")
    lines.append(f"- Skipped: {len(skipped)}")

    preview_out.parent.mkdir(parents=True, exist_ok=True)
    preview_out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "candidates": len(candidate_slugs),
        "included": included,
        "skipped": skipped,
    }


def run_apply_singletons(candidate_slugs: list[str], node_index: dict[str, NodeRecord],
                           edge_index: EdgeIndex, page_categories: dict[str, list[str]],
                           clusters: dict[str, dict], thin_sentences_cache: dict[str, dict]) -> dict:
    """The GATED --compose-singletons --apply writer. Same
    apply_identity_to_node call as cluster members (is_trap=False,
    is_redirect=False) — additive-merge, atomic write, idempotent,
    node_version bump. Mutates whatever --nodes-root points at (a scratch
    copy during testing; graph/nodes/ only with an explicit Matt go-ahead).
    """
    cluster_member_slugs = collect_all_cluster_member_slugs(clusters)

    counts = {"updated": 0, "inserted": 0, "skipped-idempotent": 0,
              "skipped-no-boilerplate": 0, "skipped-error": 0,
              "skipped-in-cluster": 0, "skipped-already-real": 0, "skipped-no-node": 0,
              "thin-sentences-applied": 0}

    for slug in candidate_slugs:
        ok, reason = classify_singleton_candidate(slug, node_index, cluster_member_slugs)
        if not ok:
            if reason.startswith("in-cluster"):
                counts["skipped-in-cluster"] += 1
            elif reason.startswith("already-real"):
                counts["skipped-already-real"] += 1
            elif reason.startswith("no-node"):
                counts["skipped-no-node"] += 1
            else:
                counts["skipped-error"] += 1
            continue

        rec = node_index[slug]
        composed_line = compose_singleton_identity_line(
            rec, node_index, edge_index, page_categories, thin_sentences_cache, cite=True,
        )
        if thin_sentences_cache.get(slug, {}).get("sentence"):
            counts["thin-sentences-applied"] += 1

        result = apply_identity_to_node(rec.path, composed_line, is_trap=False)
        _tally(counts, result)

    return counts


# ---------------------------------------------------------------------------
# --apply (gated writer)
# ---------------------------------------------------------------------------

def apply_identity_to_node(node_path: Path, composed_line: str, is_trap: bool,
                             dry: bool = False,
                             is_redirect: bool = False,
                             redirect_target_slug: str | None = None) -> str:
    """Core writer function — additive-merge per design §5. Returns one of:
    "updated", "inserted", "skipped-idempotent", "skipped-no-boilerplate",
    "skipped-error".

    Safe to call repeatedly (idempotent): if the target Identity line already
    equals composed_line, no write occurs and node_version is not bumped.

    When dry=True, computes the result without writing (used by the preview
    path if ever needed) — in practice --compose uses detect_shape_and_identity_line
    directly; this flag exists so the same function backs a future
    --apply --dry-run combination without duplicating logic.

    is_redirect / redirect_target_slug: mutually exclusive with is_trap's
    disambiguation-hub stamping. When is_redirect=True, this node gets
    `redirect_to: <redirect_target_slug>` stamped instead of
    `disambiguation_hub: true` (skipped if redirect_target_slug is None —
    the target never resolved to a node slug; the Identity line still gets
    composed/stamped, just without a redirect_to field to point at nothing).
    is_trap is expected to be False whenever is_redirect is True (a redirect
    node is never ALSO a disambiguation hub).
    """
    try:
        text = node_path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        return f"skipped-error: {exc}"

    try:
        frontmatter_raw, body, _nl = split_frontmatter(text)
    except Exception as exc:  # noqa: BLE001
        return f"skipped-error: {exc}"

    shape, boilerplate_line, boilerplate_idx = detect_shape_and_identity_line(body)

    if shape in ("a", "b"):
        if boilerplate_line is None:
            return "skipped-no-boilerplate"
        body_lines = body.splitlines()
        current_line = body_lines[boilerplate_idx].strip()
        if current_line == composed_line:
            return "skipped-idempotent"
        # Preserve leading/trailing whitespace style of the original line
        # (node bodies use plain lines with no leading indent for prose).
        body_lines[boilerplate_idx] = composed_line
        new_body = "\n".join(body_lines)
        if body.endswith("\n") and not new_body.endswith("\n"):
            new_body += "\n"
        result_kind = "updated"
    elif shape == "c":
        # Insert immediately after frontmatter, before the first '## '
        # section. A leading blank line matches the convention every other
        # node body uses right after the closing '---' (see shape a/b
        # examples: lord-swyft, rhaenyra-targaryen).
        stripped_body = body.lstrip("\n")
        insertion = f"\n## Identity\n\n{composed_line}\n\n"
        if stripped_body.strip() == "":
            new_body = insertion.lstrip("\n") if not insertion.startswith("\n") else insertion
        else:
            new_body = insertion + stripped_body
        result_kind = "inserted"
    else:
        return "skipped-error: unknown shape"

    if dry:
        return f"would-{result_kind}"

    fm = parse_frontmatter(frontmatter_raw)
    new_frontmatter_raw = frontmatter_raw
    try:
        current_version = int(fm.get("node_version", "0"))
    except ValueError:
        current_version = 0
    new_version = current_version + 1
    if re.search(r"^node_version:\s*", frontmatter_raw, re.MULTILINE):
        new_frontmatter_raw = re.sub(
            r"^(node_version:\s*)\S+",
            lambda m: f"{m.group(1)}{new_version}",
            frontmatter_raw,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        new_frontmatter_raw = frontmatter_raw.rstrip("\n") + f"\nnode_version: {new_version}\n"

    if is_trap and "disambiguation_hub" not in fm:
        new_frontmatter_raw = new_frontmatter_raw.rstrip("\n") + "\ndisambiguation_hub: true\n"

    if is_redirect and redirect_target_slug is not None and "redirect_to" not in fm:
        new_frontmatter_raw = (
            new_frontmatter_raw.rstrip("\n") + f"\nredirect_to: {redirect_target_slug}\n"
        )

    new_text = f"---\n{new_frontmatter_raw}---\n{new_body}"

    tmp_fd, tmp_path_str = tempfile.mkstemp(
        dir=str(node_path.parent), prefix=f".{node_path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as fh:
            fh.write(new_text)
        os.replace(tmp_path_str, node_path)
    finally:
        if os.path.exists(tmp_path_str):
            os.remove(tmp_path_str)

    return result_kind


def run_apply(pack: dict, nodes_root: Path,
              thin_sentences_cache: dict[str, dict] | None = None) -> dict:
    node_index: dict[str, NodeRecord] = pack["node_index"]
    clusters: dict[str, dict] = pack["clusters"]
    redirect_map: dict[str, dict] = pack.get("redirect_map", {})
    thin_sentences_cache = thin_sentences_cache or {}

    counts = {"updated": 0, "inserted": 0, "skipped-idempotent": 0,
              "skipped-no-boilerplate": 0, "skipped-error": 0, "traps-stamped": 0,
              "redirects-stamped": 0, "thin-sentences-applied": 0}

    for cluster_key in sorted(clusters.keys()):
        cluster = clusters[cluster_key]
        members = cluster["members"]
        traps = cluster["trap_nodes"]
        redirects = cluster.get("redirect_nodes", [])
        cluster_size = len(members)
        cluster_name = cluster_display_name(cluster_key, traps, node_index)
        has_trap = bool(traps)

        for slug in sorted(members.keys()):
            member = members[slug]
            rec = node_index.get(slug)
            if rec is None:
                counts["skipped-error"] += 1
                continue
            name = rec.name
            composed_line, field_count = compose_member_identity_line(
                name, member, node_index, cluster_key, cluster_size,
                cluster_name, has_trap,
            )
            if is_thin(field_count):
                cached_row = thin_sentences_cache.get(slug)
                if cached_row and cached_row.get("sentence"):
                    composed_line = append_wiki_sentence(
                        composed_line, cached_row.get("sentence"),
                        cached_row.get("source_page"), cite=True,
                    )
                    counts["thin-sentences-applied"] += 1
            result = apply_identity_to_node(rec.path, composed_line, is_trap=False)
            _tally(counts, result)

        for trap_slug in traps:
            rec = node_index.get(trap_slug)
            if rec is None:
                counts["skipped-error"] += 1
                continue
            hub_line = compose_trap_hub_line(cluster_key, cluster, node_index, rec.name)
            result = apply_identity_to_node(rec.path, hub_line, is_trap=True)
            _tally(counts, result)
            if result in ("updated", "inserted"):
                counts["traps-stamped"] += 1

        for redirect_slug in redirects:
            rec = node_index.get(redirect_slug)
            if rec is None:
                counts["skipped-error"] += 1
                continue
            entry = redirect_map.get(redirect_slug)
            if entry is None:
                counts["skipped-error"] += 1
                continue
            redirect_line = compose_redirect_line(redirect_slug, entry, node_index)
            result = apply_identity_to_node(
                rec.path, redirect_line, is_trap=False, is_redirect=True,
                redirect_target_slug=entry.get("target_slug"),
            )
            _tally(counts, result)
            if result in ("updated", "inserted"):
                counts["redirects-stamped"] += 1

    return counts


def _tally(counts: dict, result: str) -> None:
    if result in counts:
        counts[result] += 1
    elif result.startswith("skipped-error"):
        counts["skipped-error"] += 1
    else:
        counts.setdefault(result, 0)
        counts[result] += 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Deterministic same-name disambiguation + Identity-line composer for the "
            "Weirwood Network ASOIAF knowledge graph. No LLM calls, no network access."
        ),
    )
    parser.add_argument("--build-pack", action="store_true",
                         help="Build same-name-clusters.json + disambig-node-blocklist.json. No node writes.")
    parser.add_argument("--compose", action="store_true",
                         help="Compose Identity lines and write preview.md. Requires --dry-run in v1.")
    parser.add_argument("--dry-run", action="store_true",
                         help="Meaningful with --compose (writes the human preview, no node writes) and with "
                              "--enrich-thin (print prompts/cache-miss count, make ZERO claude -p calls).")
    parser.add_argument("--apply", action="store_true",
                         help="GATED. Actually mutate node files. Do not run without an explicit go-ahead.")
    parser.add_argument("--enrich-thin", action="store_true",
                         help="Seed + fill working/node-enrichment-wiki-prose/thin-sentences.jsonl — the "
                              "committed cache --compose/--apply read for thin-cluster-member sentences. "
                              "Seeding (merging thin-batch-*.jsonl) always runs; live claude -p calls only "
                              "happen for cache misses (bounded by --limit unless omitted).")
    parser.add_argument("--compose-singletons", action="store_true",
                         help="Compose Identity lines for a curated list of NON-clustered character slugs "
                              "(marquee unique-named figures the cluster-only scope skips). Requires "
                              "--dry-run or --apply.")

    parser.add_argument("--nodes-root", type=Path, default=NODES_ROOT_DEFAULT,
                         help="Override graph/nodes root (used for scratch-copy testing).")
    parser.add_argument("--edges-path", type=Path, default=EDGES_PATH_DEFAULT,
                         help="Override graph/edges/edges.jsonl path.")
    parser.add_argument("--categories-path", type=Path, default=CATEGORIES_PATH_DEFAULT,
                         help="Override working/wiki/data/page-categories.jsonl path.")
    parser.add_argument("--clusters-out", type=Path, default=CLUSTERS_OUT_DEFAULT,
                         help="Override output path for same-name-clusters.json.")
    parser.add_argument("--blocklist-out", type=Path, default=BLOCKLIST_OUT_DEFAULT,
                         help="Override output path for disambig-node-blocklist.json.")
    parser.add_argument("--redirect-map-out", type=Path, default=REDIRECT_MAP_OUT_DEFAULT,
                         help="Override output path for redirect-node-map.json.")
    parser.add_argument("--raw-wiki-root", type=Path, default=RAW_WIKI_ROOT_DEFAULT,
                         help="Override sources/wiki/_raw root (cached page HTML for redirect-target parse "
                              "and, for --enrich-thin, lead-prose extraction).")
    parser.add_argument("--preview-out", type=Path, default=PREVIEW_OUT_DEFAULT,
                         help="Override output path for preview.md.")
    parser.add_argument("--singleton-preview-out", type=Path, default=SINGLETON_PREVIEW_OUT_DEFAULT,
                         help="Override output path for preview-singletons.md.")
    parser.add_argument("--singleton-slugs-file", type=Path, default=None,
                         help="--compose-singletons only: path to a file of candidate slugs, one per "
                              "line (blank lines and '#'-comments ignored). Defaults to the curated "
                              "DEFAULT_SINGLETON_SLUGS list baked into this script.")

    parser.add_argument("--thin-sentences-cache", type=Path, default=THIN_SENTENCES_CACHE_DEFAULT,
                         help="Override path for the thin-sentences.jsonl cache (--enrich-thin writes it; "
                              "--compose/--apply read it).")
    parser.add_argument("--enrichment-dir", type=Path, default=ENRICHMENT_DIR_DEFAULT,
                         help="Override working/node-enrichment-wiki-prose dir (thin-batch-*.jsonl seed "
                              "source + cache location).")
    parser.add_argument("--thin-batch-glob", default=THIN_BATCH_GLOB_DEFAULT,
                         help="Glob (within --enrichment-dir) for seed batch files (default: thin-batch-*.jsonl).")
    parser.add_argument("--haiku-model", default=HAIKU_MODEL_DEFAULT,
                         help=f"Model for --enrich-thin claude -p calls (default: {HAIKU_MODEL_DEFAULT}).")
    parser.add_argument("--limit", type=int, default=None, metavar="N",
                         help="--enrich-thin only: cap the number of LIVE claude -p calls this run (smoke-testing).")
    parser.add_argument("--sleep", type=float, default=HAIKU_SLEEP_DEFAULT, metavar="SECONDS",
                         help=f"--enrich-thin only: throttle sleep between claude -p calls (default: "
                              f"{HAIKU_SLEEP_DEFAULT}s).")
    parser.add_argument("--force-slug", default=None, metavar="SLUG",
                         help="--enrich-thin only: re-call for this slug even if already cached (testing).")

    args = parser.parse_args()

    if not (args.build_pack or args.compose or args.apply or args.enrich_thin or args.compose_singletons):
        parser.error("one of --build-pack, --compose, --enrich-thin, --compose-singletons, or --apply is required")

    if args.compose and not args.dry_run and not args.apply:
        print("NOTE: --compose without --dry-run still only writes preview.md "
              "(no node writes) in this version — pass --dry-run explicitly for clarity.",
              file=sys.stderr)

    if args.compose_singletons and not args.dry_run and not args.apply:
        parser.error("--compose-singletons requires --dry-run or --apply")

    for required in (args.edges_path, args.categories_path):
        if not required.exists():
            print(f"ERROR: required data file not found: {required}", file=sys.stderr)
            return 1
    if not args.nodes_root.exists():
        print(f"ERROR: nodes root not found: {args.nodes_root}", file=sys.stderr)
        return 1
    if args.build_pack and not args.raw_wiki_root.exists():
        print(f"ERROR: raw wiki cache root not found: {args.raw_wiki_root} "
              f"(needed to parse redirect targets)", file=sys.stderr)
        return 1

    if args.build_pack:
        pack = build_pack(
            nodes_root=args.nodes_root,
            edges_path=args.edges_path,
            categories_path=args.categories_path,
            clusters_out=args.clusters_out,
            blocklist_out=args.blocklist_out,
            raw_wiki_root=args.raw_wiki_root,
            redirect_map_out=args.redirect_map_out,
        )
        for w in pack["warnings"]:
            print(w, file=sys.stderr)
        disambig_count = sum(1 for v in pack["blocklist"].values() if v.get("trap_kind") == "disambiguation")
        redirect_count = sum(1 for v in pack["blocklist"].values() if v.get("trap_kind") == "redirect")
        print("\n--build-pack summary")
        print(f"  Nodes scanned (all dirs): {pack['total_node_count']}")
        print(f"  Character nodes scanned: {pack['character_slug_count']}")
        print(f"  Clusters written: {len(pack['clusters'])}  -> {args.clusters_out}")
        print(f"  Blocklist entries: {len(pack['blocklist'])}  -> {args.blocklist_out}"
              f"  ({disambig_count} disambiguation, {redirect_count} redirect)")
        print(f"  Redirect-node-map entries: {len(pack['redirect_map'])}  -> {args.redirect_map_out}")
        unresolved = [s for s, e in pack["redirect_map"].items() if e.get("target_slug") is None]
        if unresolved:
            print(f"  Redirect targets with NO node in the graph (target_slug null): {unresolved}")
        biggest = sorted(pack["clusters"].items(),
                          key=lambda kv: len(kv[1]["members"]) + len(kv[1]["trap_nodes"]),
                          reverse=True)[:5]
        print("  Largest clusters:")
        for key, cluster in biggest:
            print(f"    - \"{key}\": {len(cluster['members'])} real member(s), "
                  f"{len(cluster['trap_nodes'])} trap(s), "
                  f"{len(cluster.get('redirect_nodes', []))} redirect(s)")
        print(f"  Warnings: {len(pack['warnings'])}")
        return 0

    if args.enrich_thin:
        warnings: list[str] = []
        node_index = build_node_index(args.nodes_root, warnings)
        edge_index = build_edge_index(args.edges_path, warnings)
        page_categories = load_page_categories(args.categories_path, warnings)

        if args.clusters_out.exists():
            with args.clusters_out.open(encoding="utf-8") as fh:
                clusters = json.load(fh)
        else:
            print("NOTE: same-name-clusters.json not found — building pack in-memory "
                  "(run --build-pack first to persist it).", file=sys.stderr)
            built = build_pack(
                nodes_root=args.nodes_root, edges_path=args.edges_path,
                categories_path=args.categories_path,
                clusters_out=args.clusters_out, blocklist_out=args.blocklist_out,
                raw_wiki_root=args.raw_wiki_root, redirect_map_out=args.redirect_map_out,
            )
            clusters = built["clusters"]

        pack = {
            "node_index": node_index, "edge_index": edge_index,
            "page_categories": page_categories, "clusters": clusters,
            "warnings": warnings,
        }

        if not args.raw_wiki_root.exists():
            print(f"ERROR: raw wiki cache root not found: {args.raw_wiki_root} "
                  f"(needed for lead-prose extraction)", file=sys.stderr)
            return 1

        result = run_enrich_thin(
            pack=pack,
            cache_path=args.thin_sentences_cache,
            enrichment_dir=args.enrichment_dir,
            raw_wiki_root=args.raw_wiki_root,
            batch_glob=args.thin_batch_glob,
            model=args.haiku_model,
            sleep_s=args.sleep,
            limit=args.limit,
            dry_run=args.dry_run,
            force_slug=args.force_slug,
        )

        print("\n--enrich-thin summary")
        print(f"  Cache: {args.thin_sentences_cache}")
        print(f"  Cache size before: {result['cache_before']}")
        print(f"  Newly seeded from thin-batch-*.jsonl: {result['cache_seeded']}")
        print(f"  Thin members (recomputed from clusters): {result['thin_members_total']}")
        print(f"  Cache misses targeted this run: {result['cache_misses_found']}"
              f"{' (--limit applied)' if args.limit is not None else ''}")
        if args.dry_run:
            print("  [dry-run] No claude -p calls were made, cache not written.")
        else:
            print(f"  Live calls made: {result['called']}")
            print(f"  Contentless (sentence=null): {result['contentless']}")
            print(f"  Failed after retries (quarantined, sentence=null): {result['failed']}")
            print(f"  Cache size after: {result['cache_after']}")
        return 0

    if args.compose:
        warnings: list[str] = []
        node_index = build_node_index(args.nodes_root, warnings)
        edge_index = build_edge_index(args.edges_path, warnings)
        page_categories = load_page_categories(args.categories_path, warnings)

        if args.clusters_out.exists() and args.redirect_map_out.exists():
            with args.clusters_out.open(encoding="utf-8") as fh:
                clusters = json.load(fh)
            with args.redirect_map_out.open(encoding="utf-8") as fh:
                redirect_map = json.load(fh)
        else:
            print("NOTE: same-name-clusters.json and/or redirect-node-map.json not found — "
                  "building pack in-memory (run --build-pack first to persist it).", file=sys.stderr)
            pack = build_pack(
                nodes_root=args.nodes_root, edges_path=args.edges_path,
                categories_path=args.categories_path,
                clusters_out=args.clusters_out, blocklist_out=args.blocklist_out,
                raw_wiki_root=args.raw_wiki_root, redirect_map_out=args.redirect_map_out,
            )
            clusters = pack["clusters"]
            redirect_map = pack["redirect_map"]

        thin_sentences_cache = load_thin_sentences_cache(args.thin_sentences_cache)

        pack = {
            "node_index": node_index,
            "edge_index": edge_index,
            "page_categories": page_categories,
            "clusters": clusters,
            "redirect_map": redirect_map,
            "warnings": warnings,
        }
        stats = compose_preview(pack, args.preview_out, args.nodes_root,
                                  thin_sentences_cache=thin_sentences_cache)
        for w in warnings:
            print(w, file=sys.stderr)
        print("\n--compose --dry-run summary")
        print(f"  Preview written: {args.preview_out}")
        print(f"  Clusters in scope: {stats['cluster_count']}")
        print(f"  Real cluster members: {stats['total_real_members']}")
        print(f"  Redirect nodes previewed: {stats['total_redirect_nodes']}")
        print(f"  Thin members: {stats['total_thin_members']}")
        print(f"  Thin-rate: {stats['thin_rate']:.1%}")
        print(f"  Thin members with a cached distinguishing sentence: "
              f"{stats['total_thin_with_sentence']}/{stats['total_thin_members']}")
        print(f"  Shape examples seen: {stats['shape_examples_seen']}")
        print("  No node files were written.")
        return 0

    if args.compose_singletons:
        warnings: list[str] = []
        node_index = build_node_index(args.nodes_root, warnings)
        edge_index = build_edge_index(args.edges_path, warnings)
        page_categories = load_page_categories(args.categories_path, warnings)

        if args.clusters_out.exists():
            with args.clusters_out.open(encoding="utf-8") as fh:
                clusters = json.load(fh)
        else:
            print("NOTE: same-name-clusters.json not found — building pack in-memory "
                  "(run --build-pack first to persist it).", file=sys.stderr)
            built = build_pack(
                nodes_root=args.nodes_root, edges_path=args.edges_path,
                categories_path=args.categories_path,
                clusters_out=args.clusters_out, blocklist_out=args.blocklist_out,
                raw_wiki_root=args.raw_wiki_root, redirect_map_out=args.redirect_map_out,
            )
            clusters = built["clusters"]

        thin_sentences_cache = load_thin_sentences_cache(args.thin_sentences_cache)
        candidate_slugs = load_singleton_slug_candidates(
            DEFAULT_SINGLETON_SLUGS, args.singleton_slugs_file,
        )

        for w in warnings:
            print(w, file=sys.stderr)

        if args.dry_run:
            result = compose_singletons_preview(
                candidate_slugs, node_index, edge_index, page_categories,
                clusters, thin_sentences_cache, args.singleton_preview_out,
            )
            print("\n--compose-singletons --dry-run summary")
            print(f"  Preview written: {args.singleton_preview_out}")
            print(f"  Candidates: {result['candidates']}")
            print(f"  Included: {len(result['included'])}")
            print(f"  Skipped: {len(result['skipped'])}")
            if result["skipped"]:
                print("  Skip reasons:")
                for slug, reason in result["skipped"]:
                    print(f"    - {slug}: {reason}")
            print("  No node files were written.")
            return 0

        if args.apply:
            counts = run_apply_singletons(
                candidate_slugs, node_index, edge_index, page_categories,
                clusters, thin_sentences_cache,
            )
            print("\n--compose-singletons --apply summary")
            for k, v in sorted(counts.items()):
                print(f"  {k}: {v}")
            return 0

        return 0

    if args.apply:
        warnings = []
        node_index = build_node_index(args.nodes_root, warnings)
        edge_index = build_edge_index(args.edges_path, warnings)
        page_categories = load_page_categories(args.categories_path, warnings)

        if not args.clusters_out.exists():
            print("ERROR: same-name-clusters.json missing — run --build-pack first.",
                  file=sys.stderr)
            return 1
        with args.clusters_out.open(encoding="utf-8") as fh:
            clusters = json.load(fh)

        redirect_map = {}
        if args.redirect_map_out.exists():
            with args.redirect_map_out.open(encoding="utf-8") as fh:
                redirect_map = json.load(fh)
        else:
            print("WARN: redirect-node-map.json missing — run --build-pack first. "
                  "Redirect nodes in clusters will be skipped this run.", file=sys.stderr)

        thin_sentences_cache = load_thin_sentences_cache(args.thin_sentences_cache)

        pack = {
            "node_index": node_index, "edge_index": edge_index,
            "page_categories": page_categories, "clusters": clusters,
            "redirect_map": redirect_map,
        }
        counts = run_apply(pack, args.nodes_root, thin_sentences_cache=thin_sentences_cache)
        print("\n--apply summary")
        for k, v in sorted(counts.items()):
            print(f"  {k}: {v}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
