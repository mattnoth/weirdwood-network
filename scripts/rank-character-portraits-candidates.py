#!/usr/bin/env python3
"""Rank character nodes by graph degree for portrait-fetch prioritization.

Part A of the "portrait smoke test" bounded exception task (2026-06-30).

For every `character.human` / `character.direwolf` / `character.dragon` node
under `graph/nodes/characters/`, this script:

  1. Computes graph DEGREE = count of edges (from `web/data/edges.json`, the
     built bundle derived 1:1 from `graph/edges/edges.jsonl`) where the
     node's `slug` appears as either `source` or `target`.
  2. Flags whether the character is a POV character (cross-referenced against
     `reference/pov-characters.md`'s POV_CHARACTERS table + node name/aliases
     matching, since that table keys on chapter-heading tokens, not slugs).
  3. Emits one ranked JSONL row per character to
     `working/wiki/data/portrait-candidates.jsonl`, sorted by degree
     descending:
       {slug, name, degree, is_pov, wiki_page, wiki_source,
        portrait_filename, portrait_url}
     (portrait_filename/portrait_url are populated by the companion Part B
     step — see resolve_portraits() — and are null until then.)

Read-only against sources/wiki (no fetching). Never writes to sources/.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
NODES_DIR = PROJECT_ROOT / "graph" / "nodes" / "characters"
EDGES_JSON = PROJECT_ROOT / "web" / "data" / "edges.json"
POV_REF = PROJECT_ROOT / "reference" / "pov-characters.md"
RAW_WIKI_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
OUTPUT = PROJECT_ROOT / "working" / "wiki" / "data" / "portrait-candidates.jsonl"

CHARACTER_TYPES = {"character.human", "character.direwolf", "character.dragon"}

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

INFOBOX_IMG_RE = re.compile(
    r'infobox-image.*?<img[^>]+src="([^"]+)"', re.DOTALL
)
BASE_URL = "https://awoiaf.westeros.org"


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML frontmatter parser sufficient for these node files
    (name, type, slug, aliases, wiki_source — all simple scalars/lists)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm_text = m.group(1)
    data: dict = {}
    lines = fm_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        kv = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if not kv:
            i += 1
            continue
        key, val = kv.group(1), kv.group(2).strip()
        if val == "":
            # possible block list on following lines
            items = []
            j = i + 1
            while j < len(lines) and re.match(r"^\s*-\s*", lines[j]):
                item = re.sub(r"^\s*-\s*", "", lines[j]).strip()
                item = item.strip('"').strip("'")
                items.append(item)
                j += 1
            if items:
                data[key] = items
                i = j
                continue
            else:
                data[key] = None
                i += 1
                continue
        else:
            val = val.strip('"').strip("'")
            data[key] = val
            i += 1
    return data


def load_pov_names() -> set:
    """Extract the POV_CHARACTERS dict values (normalized slug-ish tokens)
    from reference/pov-characters.md, plus derive a set of plausible full
    given-names for matching against character node `name` / `aliases`."""
    text = POV_REF.read_text(encoding="utf-8")
    # Pull the python dict block
    m = re.search(r"POV_CHARACTERS = \{(.*?)\n\}", text, re.DOTALL)
    tokens = set()
    if m:
        for line in m.group(1).split("\n"):
            kv = re.match(r'\s*"([^"]+)":\s*"([^"]+)"', line)
            if kv:
                heading, norm = kv.group(1), kv.group(2)
                tokens.add(norm.lower())
                tokens.add(heading.lower())
    return tokens


def node_matches_pov(name: str, slug: str, aliases: list, pov_tokens: set) -> bool:
    """A character node counts as POV if its slug's leading token, or its
    first given name (lowercased), appears in the POV_CHARACTERS token set.
    Handles multi-word POV labels like "the-prophet" / "jon-connington" and
    single-given-name POV labels like "jon" / "bran" / "arya"."""
    first_token = slug.split("-")[0]
    if first_token in pov_tokens:
        return True
    if slug in pov_tokens:
        return True
    name_lower = name.lower()
    first_name = name_lower.split(" ")[0]
    if first_name in pov_tokens:
        return True
    # full multi-word descriptive POV labels (AFFC/ADWD) match by full name
    if name_lower.replace(" ", "-") in pov_tokens:
        return True
    for alias in aliases or []:
        if alias.lower().replace(" ", "-") in pov_tokens:
            return True
    return False


def wiki_page_from_source(wiki_source: str) -> str:
    """'https://awoiaf.westeros.org/index.php/Jon_Snow' -> 'Jon_Snow'"""
    if not wiki_source:
        return ""
    page = wiki_source.rstrip("/").split("/")[-1]
    return unquote(page)


def extract_portrait(html: str):
    """Find the portrait <img> inside the infobox-image cell. Returns
    (thumb_src, original_url_or_none) or (None, None) if not found."""
    m = INFOBOX_IMG_RE.search(html)
    if not m:
        return None, None
    thumb_src = m.group(1)
    orig_m = re.match(r"^/images/thumb/(.+)/[0-9]+px-[^/]+$", thumb_src)
    original_url = None
    if orig_m:
        original_url = BASE_URL + f"/images/{orig_m.group(1)}"
    return thumb_src, original_url


REDIRECT_RE = re.compile(
    r'<div class="redirectMsg">.*?href="/index\.php/([^"]+)"', re.DOTALL
)


def resolve_portrait_for_node(wiki_page: str, _redirected: bool = False):
    """Read sources/wiki/_raw/<page>.json and locate the portrait image.
    Follows a single level of MediaWiki redirect (the raw cache stores the
    redirect stub under the original page name; the real infobox lives on
    the target page's own cached JSON file). Returns
    (portrait_filename, portrait_url, status) — status is one of
    'ok', 'no-raw-json', 'no-infobox-image', 'redirect-target-missing'."""
    if not wiki_page:
        return None, None, "no-wiki-page"
    raw_path = RAW_WIKI_DIR / f"{wiki_page}.json"
    if not raw_path.exists():
        return None, None, "no-raw-json"
    try:
        with open(raw_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return None, None, f"parse-error: {e}"
    html = data.get("html", "")
    thumb_src, original_url = extract_portrait(html)
    if not thumb_src:
        if not _redirected:
            redirect_m = REDIRECT_RE.search(html)
            if redirect_m:
                target_page = unquote(redirect_m.group(1))
                filename, url, status = resolve_portrait_for_node(target_page, _redirected=True)
                if status == "no-raw-json":
                    return None, None, "redirect-target-missing"
                return filename, url, status
        return None, None, "no-infobox-image"
    url = original_url or (BASE_URL + thumb_src)
    filename = unquote(url.split("/")[-1])
    return filename, url, "ok"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument(
        "--resolve-top", type=int, default=100,
        help="Resolve portrait availability (Part B) for the top-N by degree (default 100). Pass 0 to skip Part B.",
    )
    ap.add_argument("--output", type=Path, default=OUTPUT)
    args = ap.parse_args()

    if not EDGES_JSON.exists():
        print(f"ERROR: edges file not found: {EDGES_JSON}", file=sys.stderr)
        return 1

    with open(EDGES_JSON, encoding="utf-8") as f:
        edges = json.load(f)
    print(f"Loaded {len(edges):,} edges from {EDGES_JSON}")

    degree: dict = {}
    for e in edges:
        src = e.get("source")
        tgt = e.get("target")
        if src:
            degree[src] = degree.get(src, 0) + 1
        if tgt:
            degree[tgt] = degree.get(tgt, 0) + 1

    pov_tokens = load_pov_names()

    node_files = sorted(NODES_DIR.glob("*.node.md"))
    print(f"Found {len(node_files)} node files in {NODES_DIR}")

    rows = []
    skipped_non_character = 0
    for nf in node_files:
        text = nf.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        ntype = fm.get("type", "")
        if ntype not in CHARACTER_TYPES:
            skipped_non_character += 1
            continue
        slug = fm.get("slug") or nf.stem.replace(".node", "")
        name = fm.get("name", slug)
        aliases = fm.get("aliases") or []
        wiki_source = fm.get("wiki_source")
        wiki_page = wiki_page_from_source(wiki_source) if wiki_source else ""
        is_pov = node_matches_pov(name, slug, aliases, pov_tokens)
        deg = degree.get(slug, 0)
        rows.append({
            "slug": slug,
            "name": name,
            "degree": deg,
            "is_pov": is_pov,
            "wiki_page": wiki_page or None,
            "wiki_source": wiki_source,
            "portrait_filename": None,
            "portrait_url": None,
            "portrait_status": None,
        })

    rows.sort(key=lambda r: (-r["degree"], r["slug"]))

    # Part B: resolve portrait availability for the top N
    resolved_count = 0
    available_count = 0
    if args.resolve_top > 0:
        for row in rows[: args.resolve_top]:
            filename, url, status = resolve_portrait_for_node(row["wiki_page"])
            row["portrait_filename"] = filename
            row["portrait_url"] = url
            row["portrait_status"] = status
            resolved_count += 1
            if status == "ok":
                available_count += 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    pov_count = sum(1 for r in rows if r["is_pov"])
    no_wiki_source = sum(1 for r in rows if not r["wiki_source"])

    print()
    print("=== Summary ===")
    print(f"Character nodes (human/direwolf/dragon): {len(rows)}")
    print(f"Skipped non-character-typed nodes in dir: {skipped_non_character}")
    print(f"POV-flagged characters: {pov_count}")
    print(f"Nodes missing wiki_source: {no_wiki_source}")
    if args.resolve_top > 0:
        print(f"Portrait availability resolved for top {resolved_count}: {available_count} available, {resolved_count - available_count} not available")
    print(f"Manifest written: {args.output}")
    if rows:
        print()
        print("Top 15 by degree:")
        for r in rows[:15]:
            print(f"  {r['degree']:>4}  {r['slug']:<30} pov={r['is_pov']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
