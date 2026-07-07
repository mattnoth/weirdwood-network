#!/usr/bin/env python3
"""fab-build-candidate-packs.py

Deterministic (no-LLM) builder of per-unit "candidate packs" for the Fire &
Blood enrichment Track.

The wiki prose already tells us which existing graph nodes each F&B section
touches: node files carry cite anchors of the form
`cite_ref-Rfab<section_slug>...`. This script inverts that relationship:

    section slug  -->  nodes citing it  -->  extraction unit(s) covering it

Vocabulary note (paste-in): "Pass" = numbered corpus sweep; "Track" = named
workstream; "step" (lowercase) = ordered piece of a Track; "Tier" = confidence
1-5 ONLY. This script does not mint any new capitalized process words.

Inputs (all local, read-only):
  - graph/nodes/**/*.node.md      (~8.7k node files; `_conflicts/` excluded --
                                    those are superseded duplicate artifacts,
                                    not canonical graph nodes)
  - working/fire-and-blood/unit-map.json   (section-slug -> unit crosswalk)

Outputs (working/fire-and-blood/candidate-packs/ by default):
  - fab-<unit-slug>-<nn>.json     one pack per unit with >=1 citing node
  - _index.md                     human-readable summary table
  - _unmapped-sections.md         section slugs that matched no unit

This script never touches graph/, edges.jsonl, or unit-map.json.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

ANCHOR_RE = re.compile(r"cite_ref-Rfab([A-Za-z0-9._-]*)")

# MediaWiki percent-escape-style codes (dot-hex, as they appear in these
# anchors instead of true %-escapes) that show up inside Rfab section slugs.
# Decode longest-match-first so multi-byte UTF-8 sequences (em/en dash) don't
# get mangled by a shorter prefix match.
_HEX_ESCAPE_RE = re.compile(r"(?:\.[0-9A-Fa-f]{2})+")


def _decode_hex_escape_run(run: str) -> str:
    """Decode a run of `.XX` dot-hex escapes (concatenated, MediaWiki-anchor
    style) into raw bytes, then UTF-8 decode. Falls back to stripping on any
    error since these are cosmetic anchor artifacts, not load-bearing data."""
    hex_bytes = bytes(int(h, 16) for h in re.findall(r"\.([0-9A-Fa-f]{2})", run))
    try:
        return hex_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return ""


def decode_anchor_escapes(raw: str) -> str:
    """Replace all dot-hex escape runs in a raw Rfab anchor suffix with their
    decoded characters (apostrophes, dashes, commas, braces, etc.)."""
    return _HEX_ESCAPE_RE.sub(lambda m: _decode_hex_escape_run(m.group(0)), raw)


def strip_trailing_ref_suffix(s: str) -> str:
    """Strip trailing MediaWiki cite_ref numeric suffixes: `_N-M`, `-N`, or a
    lone trailing `.` left over from decoding. Applied AFTER `{{{3}}}{{{4}}}`
    template junk (the `{...}` template-braces block) has already been cut."""
    s = re.sub(r"_[0-9]+-[0-9]+$", "", s)
    s = re.sub(r"-[0-9]+$", "", s)
    s = s.rstrip(".")
    return s


def extract_section_slug(anchor_suffix: str) -> str:
    """Given the raw suffix captured after `cite_ref-Rfab`, produce the best-
    effort section slug: decode MediaWiki dot-hex escapes, cut everything
    from the `{{{3}}}{{{4}}}` template-braces junk onward, strip trailing
    numeric ref suffixes. Returns "" for anchors with no recoverable slug
    (bare `Rfab`, `Rfab-1`, or purely-numeric `Rfab1`/`Rfab10`/...)."""
    if not anchor_suffix:
        return ""

    decoded = decode_anchor_escapes(anchor_suffix)

    # Cut at the template-braces junk: decoded "{{{3}}}{{{4}}}" or the raw
    # ".7B" sequences if decoding left any un-consumed (shouldn't happen, but
    # be defensive).
    for marker in ("{{{", ".7B"):
        idx = decoded.find(marker)
        if idx != -1:
            decoded = decoded[:idx]

    decoded = strip_trailing_ref_suffix(decoded)

    # Purely numeric suffix (e.g. "1", "10", "23") is a footnote counter, not
    # a section slug -- these correspond to the bare `Rfab` / `Rfab-1` family.
    if decoded.isdigit():
        return ""

    return decoded


def normalize_slug(s: str) -> str:
    """Normalize a section slug for fuzzy comparison: lowercase, decode any
    remaining unicode punctuation to ASCII where reasonable, collapse
    hyphens/underscores/spaces/em-dashes/en-dashes to a single underscore,
    drop everything that isn't [a-z0-9_], collapse repeats, strip ends."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = s.lower()
    # unify all dash/space/underscore variants to underscore
    s = re.sub(r"[\s\-‐-―_]+", "_", s)
    # drop apostrophes/commas/semicolons/brackets/periods entirely
    s = re.sub(r"[^a-z0-9_]", "", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def strip_leading_article(s: str) -> str:
    for article in ("the_", "a_"):
        if s.startswith(article):
            return s[len(article):]
    return s


def token_set(s: str) -> set:
    return set(t for t in s.split("_") if t)


def load_unit_map(map_path: Path) -> list[dict]:
    with map_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data["units"]


def build_section_lookup(units: list[dict]) -> tuple[dict, dict]:
    """Build two lookup dicts keyed by normalized section slug:
      - exact:   normalize_slug(raw_slug) -> set of unit nn
      - fuzzy:   (article-stripped, token-set-based) for fallback matching
    Returns (exact_lookup, unit_by_nn) where unit_by_nn maps nn -> unit dict,
    and exact_lookup maps normalized wiki_section_slug -> set of nn strings.
    Also attaches a `_fuzzy_keys` list per unit for the second-pass matcher.
    """
    exact_lookup: dict[str, set] = defaultdict(set)
    unit_by_nn = {}
    for unit in units:
        nn = unit["nn"]
        unit_by_nn[nn] = unit
        fuzzy_keys = []
        for raw in unit.get("wiki_section_slugs", []):
            norm = normalize_slug(raw)
            if not norm:
                continue
            exact_lookup[norm].add(nn)
            fuzzy_keys.append(norm)
        unit["_fuzzy_keys"] = fuzzy_keys
    return exact_lookup, unit_by_nn


def fuzzy_match_units(norm_slug: str, exact_lookup: dict, unit_by_nn: dict) -> set:
    """Fallback fuzzy match when exact normalized match fails:
    1. Try stripping a leading article (the_/a_) from both sides.
    2. Try token-subset match: does the anchor's token set contain (or get
       contained by) a unit section's token set, with enough overlap to be
       confident (>=2 shared tokens, or one is a full subset of the other and
       both have >=2 tokens)?
    This exists to absorb the observed OCR/typo drift (e.g.
    'a_surfeit_or_rulers' vs 'a_surfeit_of_rulers', 'aftermath_-_the_house_of_the_wolf'
    vs 'aftermath_-_the_hour_of_the_wolf', 'reign_of_the_dragons_...' vs
    'reign_of_the_dragon_...') without requiring an exhaustive alias table.
    """
    stripped = strip_leading_article(norm_slug)
    if stripped != norm_slug and stripped in exact_lookup:
        return set(exact_lookup[stripped])
    # also try: does article-stripped anchor match an article-stripped unit key?
    candidates = set()
    anchor_tokens = token_set(stripped)
    if not anchor_tokens:
        return candidates
    for unit in unit_by_nn.values():
        for key in unit["_fuzzy_keys"]:
            key_stripped = strip_leading_article(key)
            key_tokens = token_set(key_stripped)
            if not key_tokens:
                continue
            overlap = anchor_tokens & key_tokens
            # Require a strong overlap: either one token set is a subset of
            # the other (handles truncated/expanded titles) with >=2 tokens,
            # or at least 3 shared tokens (handles typo'd single tokens in a
            # longer compound title) and the shared tokens are the majority
            # of the smaller set.
            smaller = min(len(anchor_tokens), len(key_tokens))
            if smaller == 0:
                continue
            is_subset = anchor_tokens <= key_tokens or key_tokens <= anchor_tokens
            strong_overlap = len(overlap) >= 3 and len(overlap) >= 0.6 * smaller
            if (is_subset and smaller >= 2) or strong_overlap:
                candidates.add(unit["nn"])
    return candidates


def iter_node_files(nodes_dir: Path):
    for path in sorted(nodes_dir.rglob("*.node.md")):
        if "_conflicts" in path.parts:
            continue
        yield path


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm_text = text[3:end]
    try:
        data = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Build per-unit Fire & Blood candidate packs from Rfab cite anchors in graph nodes."
    )
    parser.add_argument(
        "--nodes-dir",
        type=Path,
        default=REPO_ROOT / "graph" / "nodes",
        help="Directory containing *.node.md files (default: graph/nodes/)",
    )
    parser.add_argument(
        "--map",
        type=Path,
        default=REPO_ROOT / "working" / "fire-and-blood" / "unit-map.json",
        help="Path to unit-map.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "working" / "fire-and-blood" / "candidate-packs",
        help="Output directory for candidate packs (default: working/fire-and-blood/candidate-packs/)",
    )
    parser.add_argument("--verbose", action="store_true", help="Print per-node match diagnostics")
    args = parser.parse_args()

    nodes_dir: Path = args.nodes_dir
    map_path: Path = args.map
    output_dir: Path = args.output_dir

    if not nodes_dir.exists():
        print(f"ERROR: nodes dir not found: {nodes_dir}", file=sys.stderr)
        sys.exit(1)
    if not map_path.exists():
        print(f"ERROR: unit map not found: {map_path}", file=sys.stderr)
        sys.exit(1)

    units = load_unit_map(map_path)
    exact_lookup, unit_by_nn = build_section_lookup(units)

    # unit_nn -> slug -> {anchor_count, name, aliases, type}
    unit_slug_data: dict[str, dict] = defaultdict(dict)
    unmapped_sections: dict[str, int] = defaultdict(int)  # normalized section slug -> node count citing it
    unmapped_raw_examples: dict[str, str] = {}

    total_nodes_scanned = 0
    total_nodes_with_anchor = 0
    total_nodes_mapped = 0
    fuzzy_hits = 0
    exact_hits = 0

    for path in iter_node_files(nodes_dir):
        total_nodes_scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            print(f"WARNING: could not read {path}: {e}", file=sys.stderr)
            continue

        anchor_matches = ANCHOR_RE.findall(text)
        if not anchor_matches:
            continue
        total_nodes_with_anchor += 1

        fm = parse_frontmatter(text)
        slug = fm.get("slug") or path.stem.replace(".node", "")
        name = fm.get("name") or slug
        aliases = fm.get("aliases") or []
        if not isinstance(aliases, list):
            aliases = [aliases]
        node_type = fm.get("type") or "unknown"

        # Count anchors per matched unit for THIS node.
        node_unit_counts: dict[str, int] = defaultdict(int)
        node_had_recoverable_slug = False

        for raw_suffix in anchor_matches:
            section_slug = extract_section_slug(raw_suffix)
            if not section_slug:
                continue  # bare Rfab / numeric-only footnote ref -- not a section anchor
            node_had_recoverable_slug = True
            norm = normalize_slug(section_slug)
            matched_nns = set(exact_lookup.get(norm, set()))
            if matched_nns:
                exact_hits += 1
            else:
                matched_nns = fuzzy_match_units(norm, exact_lookup, unit_by_nn)
                if matched_nns:
                    fuzzy_hits += 1

            if matched_nns:
                for nn in matched_nns:
                    node_unit_counts[nn] += 1
            else:
                unmapped_sections[norm] += 1
                if norm not in unmapped_raw_examples:
                    unmapped_raw_examples[norm] = section_slug

        if node_unit_counts:
            total_nodes_mapped += 1
            for nn, count in node_unit_counts.items():
                entry = unit_slug_data[nn].get(slug)
                if entry is None:
                    unit_slug_data[nn][slug] = {
                        "name": name,
                        "aliases": aliases,
                        "type": node_type,
                        "anchor_count": count,
                    }
                else:
                    entry["anchor_count"] += count

        if args.verbose:
            status = "MAPPED" if node_unit_counts else ("NO-SLUG" if not node_had_recoverable_slug else "UNMAPPED")
            print(f"[{status}] {path.relative_to(REPO_ROOT)} -> units={sorted(node_unit_counts)}")

    # --- write packs ---
    output_dir.mkdir(parents=True, exist_ok=True)
    # clean any stale packs from a previous run so removed units don't linger
    for stale in output_dir.glob("fab-*-*.json"):
        stale.unlink()

    index_rows = []
    packs_written = 0

    for unit in units:
        nn = unit["nn"]
        per_slug_raw = unit_slug_data.get(nn, {})
        if not per_slug_raw:
            continue

        expected_slugs = sorted(
            per_slug_raw.keys(), key=lambda s: per_slug_raw[s]["anchor_count"], reverse=True
        )
        per_slug = {
            s: {
                "name": per_slug_raw[s]["name"],
                "aliases": per_slug_raw[s]["aliases"],
                "type": per_slug_raw[s]["type"],
                "anchor_count": per_slug_raw[s]["anchor_count"],
            }
            for s in expected_slugs
        }

        pack = {
            "nn": nn,
            "slug": unit["slug"],
            "section_title": unit["ncx_title"],
            "expected_slugs": expected_slugs,
            "per_slug": per_slug,
        }

        out_path = output_dir / f"fab-{unit['slug']}-{nn}.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(pack, f, indent=2, ensure_ascii=False)
            f.write("\n")
        packs_written += 1

        top5 = expected_slugs[:5]
        index_rows.append(
            {
                "nn": nn,
                "slug": unit["slug"],
                "section_title": unit["ncx_title"],
                "node_count": len(expected_slugs),
                "top5": top5,
            }
        )

    # --- _index.md ---
    index_path = output_dir / "_index.md"
    lines = [
        "# Fire & Blood candidate packs — index",
        "",
        "Built by `scripts/fab-build-candidate-packs.py`. One row per unit with >=1 citing node.",
        "",
        "| nn | slug | section title | node count | top-5 expected_slugs |",
        "|----|------|---------------|-----------|----------------------|",
    ]
    for row in sorted(index_rows, key=lambda r: r["nn"]):
        top5_str = ", ".join(row["top5"]) if row["top5"] else "—"
        lines.append(
            f"| {row['nn']} | {row['slug']} | {row['section_title']} | {row['node_count']} | {top5_str} |"
        )
    lines.append("")
    index_path.write_text("\n".join(lines), encoding="utf-8")

    # --- _unmapped-sections.md ---
    unmapped_path = output_dir / "_unmapped-sections.md"
    unmapped_lines = [
        "# Fire & Blood candidate packs — unmapped sections",
        "",
        "Normalized section slugs extracted from node `cite_ref-Rfab...` anchors that matched",
        "NO unit in `unit-map.json`'s `wiki_section_slugs`. High node-citing-counts here likely",
        "indicate a real section the map is missing (or a section-title variant worth adding as",
        "an alias); one-off counts are more likely OCR/typo noise in the source wiki markup.",
        "",
        "| normalized slug | example raw section slug | citing node count |",
        "|------------------|---------------------------|--------------------|",
    ]
    if unmapped_sections:
        for norm, count in sorted(unmapped_sections.items(), key=lambda kv: -kv[1]):
            example = unmapped_raw_examples.get(norm, "")
            unmapped_lines.append(f"| {norm or '(empty)'} | {example} | {count} |")
    else:
        unmapped_lines.append("| _none_ | | |")
    unmapped_lines.append("")
    unmapped_path.write_text("\n".join(unmapped_lines), encoding="utf-8")

    # --- summary ---
    print("=" * 72)
    print("fab-build-candidate-packs.py — summary")
    print("=" * 72)
    print(f"Nodes scanned (excluding _conflicts/):      {total_nodes_scanned}")
    print(f"Nodes carrying >=1 Rfab anchor:              {total_nodes_with_anchor}")
    print(f"Nodes mapped to >=1 unit:                    {total_nodes_mapped}")
    print(f"  exact section-slug matches:                {exact_hits}")
    print(f"  fuzzy section-slug matches:                {fuzzy_hits}")
    print(f"Packs written:                               {packs_written}  -> {output_dir}")
    print(f"Unmapped distinct normalized section slugs:  {len(unmapped_sections)}")
    print(f"Index:                                       {index_path}")
    print(f"Unmapped report:                              {unmapped_path}")
    print()

    # 015 acceptance check
    smoke_pack_path = output_dir / "fab-heirs-of-the-dragon-015.json"
    if smoke_pack_path.exists():
        with smoke_pack_path.open("r", encoding="utf-8") as f:
            smoke = json.load(f)
        expected = smoke["expected_slugs"]
        must_have = ["rhaenyra-targaryen", "daemon-targaryen", "criston-cole"]
        missing = [s for s in must_have if s not in expected]
        print(f"Acceptance check — {smoke_pack_path.name}:")
        print(f"  expected_slugs count: {len(expected)}")
        if missing:
            print(f"  FAIL — missing required slugs: {missing}")
        else:
            print(f"  PASS — contains {must_have}")
        print(f"  expected_slugs: {expected}")
    else:
        print(f"WARNING: smoke pack not found: {smoke_pack_path}")
    print()


if __name__ == "__main__":
    main()
