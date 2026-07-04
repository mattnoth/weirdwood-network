#!/usr/bin/env python3
"""build_theme_index.py — deterministic theme->members table (query-layer
Track, step 8a; design.md D-E/G4: "the trigger table's routing half").

**Not** a general tagging system, and **not** the settled 5-container axis
(`container`, event-only bag-retrieval — see `weirwood_query/traverse.py`'s
`_node_containers`). Themes are a SEPARATE, descriptive-content axis: "what do
we know about meals in the north?" needs a way to say "these ~40 nodes are
about food" without minting new edges or touching `containers:` frontmatter.

Seed themes (design.md 8a, fixed set for v1 — do not silently grow this list;
adding a theme is a deliberate edit to `THEMES` below, same discipline as the
locked edge vocabulary):
  - "meals & feasts"     — food/drink objects + custom nodes about hosting/dining
  - "hospitality"        — the guest-right/oath axis: customs + concepts about
                            hosting, guesting, and its violation
  - "dress & materials"  — clothing/textile/heraldry-adjacent materials + customs
  - "maesters & healing" — the Citadel/medical axis: `medical/` nodes + maester-
                            adjacent concepts/customs
  - "songs & tales"      — in-world texts/songs (`texts/`) + bard/singer customs

Membership rule (documented per theme below, deterministic, re-runnable):
  1. **Type rule** — every node under some `graph/nodes/<dir>/` wholesale
     qualifies for a theme (e.g. every `foods/` node -> "meals & feasts").
  2. **Keyword rule** — for node dirs that are NOT wholesale-included (customs,
     concepts, materials, religions...), a node qualifies if a theme's keyword
     list matches, as a **whole-word/whole-phrase** match (word-boundary
     regex, case-insensitive — NOT a raw substring: "harp" must not match
     inside "Harpy's" or "sharply", "host" must not match inside "Hoster"),
     against the node's `name`, `aliases`, or the `## Identity`/`## Quotes`
     text. This is a coarse recall mechanism (a routing aid, not a precision-
     guaranteed classifier) — see each theme's own keyword list below for
     exactly what it matches on.
  3. A node may belong to more than one theme (e.g. "harvest-feast" custom ->
     both "meals & feasts" and "hospitality").

No LLM in the loop. Ever. Every rule is a plain Python predicate; re-running
this script over an unchanged graph produces byte-identical output (sorted
member lists, sorted JSON keys, no embedded build timestamp in the sorted
comparison path — see `write_index`'s docstring).

Outputs (design.md 8a):
  - `working/wiki/data/theme-index.json` — the FULL profile table: per theme,
    the member list carries `{slug, category, name, matched_via}` (which rule
    fired — "type" or "keyword:<term>" — for auditability).
  - `web/data/theme-index.json` — the bundle copy consumed by `themes.py`'s
    bounded profile / `theme.ts`. Slimmed to `{slug, category, name}` per
    member (drops `matched_via` — debugging-only, not needed at query time).
    Shipped into the bundle by `build_chat_bundle.py`'s manifest measurement
    the same way `search-index.json` is (a sibling file it measures but does
    not itself regenerate) — see that module's own comment.

Usage:
    python3 graph/query/build/build_theme_index.py
    python3 graph/query/build/build_theme_index.py --working-out PATH --bundle-out PATH
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_THIS_FILE = Path(__file__).resolve()
# <repo>/graph/query/build/build_theme_index.py -> parents[0]=build,
# [1]=query, [2]=graph, [3]=<repo>
REPO_ROOT = _THIS_FILE.parents[3]

sys.path.insert(0, str(REPO_ROOT / "graph" / "query"))

from weirwood_query.load import NODES_DIR, parse_frontmatter, split_sections  # noqa: E402

WORKING_OUT = REPO_ROOT / "working" / "wiki" / "data" / "theme-index.json"
BUNDLE_OUT = REPO_ROOT / "web" / "data" / "theme-index.json"

# graph/nodes/ type-directory name -> node_type prefix, mirrors the vocabulary
# search.py/list_nodes.py already use for `category` (the directory name, NOT
# the dotted frontmatter `type:` scalar — see build_search_index.py's comment
# on why the two differ).
_EXCLUDED_DIRS = {"_conflicts", "_unclassified"}


# ---------------------------------------------------------------------------
# Theme definitions
# ---------------------------------------------------------------------------
# Each theme is: {
#   "wholesale_dirs":  [category, ...]        -> every node in these dirs qualifies
#   "keyword_dirs":    {category: [keyword, ...], ...}  -> substring match on
#                       name/aliases/identity/quotes text (lowercased)
# }
# A dir listed in wholesale_dirs is NEVER also keyword-scanned for the SAME
# theme (that would be redundant — every member already qualifies). A dir may
# be wholesale for one theme and keyword-scanned for another (e.g. "customs"
# is keyword-scanned for BOTH "meals & feasts" and "hospitality" with
# different keyword lists, since most customs nodes are neither).

THEMES: dict[str, dict[str, Any]] = {
    "meals & feasts": {
        "wholesale_dirs": ["foods"],
        "keyword_dirs": {
            "customs": ["feast", "banquet", "supper", "wedding pie", "cupbearer",
                        "harvest", "dine", "dining", "table manners"],
            "concepts": ["feast", "banquet", "cupbearer"],
        },
    },
    "hospitality": {
        "wholesale_dirs": [],
        "keyword_dirs": {
            "customs": ["guest right", "guest-right", "hospitality", "bread and salt",
                        "guestright", "hosting", "hosted", "hospitable", "fosterage"],
            "concepts": ["guest right", "guest-right", "hospitality", "bread and salt"],
        },
    },
    "dress & materials": {
        "wholesale_dirs": ["materials"],
        "keyword_dirs": {
            "customs": ["cloak", "jewelry", "tattoo", "heraldry", "tapestry",
                        "attire", "garb", "clothing", "dress"],
            "artifacts": ["cloak", "gown", "armor", "armour", "jewelry", "jewel",
                          "tapestry", "tattoo"],
        },
    },
    "maesters & healing": {
        "wholesale_dirs": ["medical"],
        "keyword_dirs": {
            "customs": ["maester", "sickroom", "healer", "healing"],
            "concepts": ["maester", "healer", "healing", "citadel"],
            "religions": ["citadel"],
        },
    },
    "songs & tales": {
        "wholesale_dirs": ["texts"],
        "keyword_dirs": {
            "customs": ["singer", "bard", "minstrel", "song", "harp"],
            "concepts": ["singer", "bard", "minstrel", "song"],
        },
    },
}


# ---------------------------------------------------------------------------
# Keyword matching — whole-word/whole-phrase, not raw substring (avoids the
# "harp" matching inside "Harpy's"/"sharply", "host" matching inside "Hoster"
# class of false positive a naive `kw in text` check produces).
# ---------------------------------------------------------------------------

_KEYWORD_PATTERN_CACHE: dict[str, re.Pattern[str]] = {}


def _keyword_pattern(keyword: str) -> re.Pattern[str]:
    pat = _KEYWORD_PATTERN_CACHE.get(keyword)
    if pat is None:
        # \b works fine around spaces too ("guest right" -> \bguest\ right\b),
        # since \b anchors on a-zA-Z0-9_ boundaries and a literal space is
        # already a non-word character on both sides.
        pat = re.compile(r"\b" + re.escape(keyword) + r"\b", re.IGNORECASE)
        _KEYWORD_PATTERN_CACHE[keyword] = pat
    return pat


def _keyword_matches(keyword: str, text: str) -> bool:
    return _keyword_pattern(keyword).search(text) is not None


# ---------------------------------------------------------------------------
# Node scan
# ---------------------------------------------------------------------------

def _iter_type_dir(category: str, nodes_dir: Path = NODES_DIR):
    d = nodes_dir / category
    if not d.is_dir():
        return
    for node_file in sorted(d.glob("*.node.md")):
        yield node_file


def _load_node_fields(node_file: Path) -> tuple[dict[str, Any], str, str]:
    """Return (frontmatter_fields, searchable_text, name)."""
    raw = node_file.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(raw)
    fallback = node_file.name.removesuffix(".node.md")
    name = str(fields.get("name") or fallback)
    aliases_raw = fields.get("aliases", [])
    if not isinstance(aliases_raw, list):
        aliases_raw = [aliases_raw] if aliases_raw else []
    sections = split_sections(body)
    # NOT lowercased here — _keyword_matches's regex is case-insensitive
    # itself (re.IGNORECASE), so keeping original case around costs nothing
    # and avoids a second normalization step.
    searchable = " ".join([
        name,
        " ".join(str(a) for a in aliases_raw),
        sections.get("identity", ""),
        sections.get("quotes", ""),
    ])
    return fields, searchable, name


def build_theme_index(nodes_dir: Path = NODES_DIR) -> dict[str, list[dict[str, Any]]]:
    """Return {theme_name: [member, ...]} — member dicts carry
    {slug, category, name, matched_via}, sorted by (category, slug) within
    each theme for determinism. A node matched by more than one rule within
    the SAME theme keeps only the first rule found (wholesale checked before
    keyword; keyword dirs walked in the dict's declared order) — one entry
    per (theme, slug), never a duplicate."""
    result: dict[str, list[dict[str, Any]]] = {}

    for theme_name, spec in THEMES.items():
        members: dict[str, dict[str, Any]] = {}  # slug -> member (dedup key)

        for category in spec.get("wholesale_dirs", []):
            for node_file in _iter_type_dir(category, nodes_dir):
                fields, _searchable, name = _load_node_fields(node_file)
                slug = fields.get("slug") or node_file.name.removesuffix(".node.md")
                if slug not in members:
                    members[slug] = {
                        "slug": slug, "category": category, "name": name,
                        "matched_via": "type",
                    }

        for category, keywords in spec.get("keyword_dirs", {}).items():
            for node_file in _iter_type_dir(category, nodes_dir):
                fields, searchable, name = _load_node_fields(node_file)
                slug = fields.get("slug") or node_file.name.removesuffix(".node.md")
                if slug in members:
                    continue  # already matched (wholesale or an earlier keyword dir)
                for kw in keywords:
                    if _keyword_matches(kw, searchable):
                        members[slug] = {
                            "slug": slug, "category": category, "name": name,
                            "matched_via": f"keyword:{kw}",
                        }
                        break

        result[theme_name] = sorted(
            members.values(), key=lambda m: (m["category"], m["slug"])
        )

    return result


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_full(index: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Full-profile table: theme -> member list with `matched_via` kept in
    (auditability — see which rule pulled a node into a theme)."""
    return {
        "format": "full",
        "themes": {
            name: {"member_count": len(members), "members": members}
            for name, members in index.items()
        },
    }


def format_bundle(index: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Bundle-profile table: same membership, `matched_via` dropped (debugging-
    only field, not needed at query time — keeps the bundle copy smaller)."""
    return {
        "format": "bundle",
        "themes": {
            name: {
                "member_count": len(members),
                "members": [
                    {"slug": m["slug"], "category": m["category"], "name": m["name"]}
                    for m in members
                ],
            }
            for name, members in index.items()
        },
    }


def write_index(index: dict[str, Any], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    # sort_keys=True + fixed separators -> byte-identical output across
    # repeated builds given an unchanged graph (determinism, verify #4).
    text = json.dumps(index, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    path.write_text(text, encoding="utf-8")
    return len(text.encode("utf-8"))


def human(nbytes: float) -> str:
    for unit in ("B", "KB", "MB"):
        if nbytes < 1024 or unit == "MB":
            return f"{nbytes:.1f}{unit}" if unit != "B" else f"{nbytes:.0f}B"
        nbytes /= 1024
    return f"{nbytes:.1f}MB"


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the theme -> members routing table.")
    ap.add_argument("--working-out", default=None, help="Override the working/wiki/data full-profile path.")
    ap.add_argument("--bundle-out", default=None, help="Override the web/data bundle-profile path.")
    args = ap.parse_args()

    print("Building theme index ...")
    index = build_theme_index()
    for name, members in index.items():
        print(f"  {name:<22} {len(members):>4} members")

    working_out = Path(args.working_out) if args.working_out else WORKING_OUT
    bundle_out = Path(args.bundle_out) if args.bundle_out else BUNDLE_OUT

    full_index = format_full(index)
    size_working = write_index(full_index, working_out)
    print(f"  wrote {working_out}  (full profile, {human(size_working)})")

    bundle_index = format_bundle(index)
    size_bundle = write_index(bundle_index, bundle_out)
    print(f"  wrote {bundle_out}  (bundle profile, {human(size_bundle)})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
