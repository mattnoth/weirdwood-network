#!/usr/bin/env python3
"""
Filter the 65 case-collision tail slugs into:
  - DROP: real-world books, disambig pages, list articles, meta concepts, hound names, too-generic
  - ALREADY_EXISTS: node already in graph (exact slug or as alias)
  - CANONICAL: canonical in-world entities needing reconstruction
  - UNCERTAIN: needs manual check

Outputs a report + a canonicals.txt for the mission file.
"""

import json
import os
import re
from pathlib import Path

BASE = Path("/Users/mnoth/source/asoiaf-chat")
GRAPH = BASE / "graph" / "nodes"
WIKI_RAW = BASE / "sources" / "wiki" / "_raw"

# The 65 remaining tail slugs (from continue prompt)
TAIL_SLUGS = [
    "god-emperor",
    "dragon-horn",
    "conflict-beyond-the-wall",
    "chief-undergaoler",
    "across-the-narrow-sea",
    "wine-of-courage",
    "trade-talk",
    "timeline-of-major-events",
    "rolfe-the-dwarf",
    "list-of-rivers",
    "grazdan-mo-ullhor",
    "grand-master",
    "ghost-grass",
    "fat-fellow",
    "willow-(hound)",
    "the-song-of-ice-and-fire",
    "the-princess-and-the-queen,-or,-the-blacks-and-the-greens",
    "the-princess-and-the-queen",
    "stern-face",
    "starved-man",
    "rule-of-thumb",
    "roone-(maester)",
    "ronnel-arryn-(king)",
    "roland-crakehall-(lord)",
    "robert-brax-(disambiguation)",
    "rickard-stark-(king)",
    "red-raven-(free-folk)",
    "pov-character",
    "pate-(ranger)",
    "pate-(novice)",
    "lyonel-tyrell-(lord)",
    "lymond-(disambiguation)",
    "lyman-(disambiguation)",
    "lyman-(archmaester)",
    "lucerys-velaryon-(master-of-ships)",
    "luceon-(disambiguation)",
    "list-of-characters",
    "kyra-(hound)",
    "ice-dragon",
    "house-words",
    "house-towers-(north)",
    "house-lake-(north)",
    "house-holt-(north)",
    "house-brownhill-(stormlands)",
    "horse-god",
    "high-septon-(fat-one)",
    "high-king",
    "henly-(maester)",
    "helicent-(hound)",
    "harmune-(archmaester)",
    "handsome-man",
    "gerold-(archmaester)",
    "garin-(orphan)",
    "fowler-twins",
    "erryk-(guard)",
    "damon-lannister-(lord)",
    "damon-dance-for-me",
    "dake-(guard)",
    "beyond-the-wall-(book)",
    "bethany-fair-fingers",
    "bellegere-otherys-(courtesan)",
    "arryn-succession-conflict-(134-ac)",
    "arryk-(guard)",
    "all-for-joffrey",
    "a-feast-for-crows",
]

# ── Drop rules ──────────────────────────────────────────────────────────────

def is_drop(slug):
    """Returns (True, reason) or (False, None)."""

    # Real-world publications
    REAL_WORLD = {
        "a-feast-for-crows": "real-world book",
        "beyond-the-wall-(book)": "real-world book anthology",
        "across-the-narrow-sea": "real-world short story collection (GRRM)",
        "the-princess-and-the-queen,-or,-the-blacks-and-the-greens": "real-world GRRM novella",
        "the-princess-and-the-queen": "real-world GRRM novella (short title; same work)",
    }
    if slug in REAL_WORLD:
        return True, REAL_WORLD[slug]

    # Disambiguation pages
    if slug.endswith("-(disambiguation)"):
        return True, "disambiguation page"

    # List / timeline / index articles
    if slug.startswith("list-of-") or slug.startswith("timeline-of-"):
        return True, "list/timeline article"

    # Meta-wiki concepts
    META_WIKI = {
        "pov-character": "meta-wiki concept (not in-universe)",
        "rule-of-thumb": "too-generic phrase / meta-wiki",
        "house-words": "meta-wiki list page, not a concept node",
    }
    if slug in META_WIKI:
        return True, META_WIKI[slug]

    # Hound names (animals, no narrative agency)
    HOUND_NAMES = {
        "willow-(hound)": "hound/dog name — no narrative agency",
        "kyra-(hound)":   "hound/dog name — no narrative agency",
        "helicent-(hound)": "hound/dog name — no narrative agency",
        "fat-fellow":     "one of Joffrey's named hounds — no narrative agency",
    }
    if slug in HOUND_NAMES:
        return True, HOUND_NAMES[slug]

    # Too-generic phrases / non-discrete in-universe entities
    TOO_GENERIC = {
        "trade-talk": "too-generic phrase (trade pidgin concept; no discrete wiki page entity)",
        "horse-god":  "too-generic deity reference (Dothraki Great Stallion); already covered via Dothraki concept.culture node",
    }
    if slug in TOO_GENERIC:
        return True, TOO_GENERIC[slug]

    return False, None


# ── Existing-node check ──────────────────────────────────────────────────────

def _load_alias_map():
    """Returns slug→canonical_slug map by reading all node frontmatters."""
    alias_map = {}
    for node_path in GRAPH.rglob("*.node.md"):
        canonical = node_path.stem.removesuffix(".node")
        alias_map[canonical] = canonical
        text = node_path.read_text(errors="replace")
        m = re.search(r"^aliases:\s*\[([^\]]*)\]", text, re.MULTILINE)
        if m:
            raw = m.group(1)
            for alias in re.findall(r'"([^"]+)"|\'([^\']+)\'|([^,\s]+)', raw):
                alias_str = alias[0] or alias[1] or alias[2]
                if alias_str:
                    alias_key = alias_str.lower().replace(" ", "-")
                    alias_map[alias_key] = canonical
    return alias_map

def node_exists(slug, alias_map):
    """Returns (True, found_slug, path) or (False, None, None)."""
    # Exact match
    for d in GRAPH.iterdir():
        if not d.is_dir():
            continue
        node = d / f"{slug}.node.md"
        if node.exists():
            return True, slug, str(node.relative_to(BASE))

    # Alias match (normalize slug)
    norm = slug.lower().replace(" ", "-")
    # Strip parenthetical suffix to find canonical
    base_slug = re.sub(r"-\([^)]+\)$", "", norm)

    for candidate in [norm, base_slug]:
        if candidate in alias_map and alias_map[candidate] != candidate:
            # alias points to a different canonical
            canonical = alias_map[candidate]
            for d in GRAPH.iterdir():
                if not d.is_dir():
                    continue
                node = d / f"{canonical}.node.md"
                if node.exists():
                    return True, f"alias→{canonical}", str(node.relative_to(BASE))
        elif candidate in alias_map:
            for d in GRAPH.iterdir():
                if not d.is_dir():
                    continue
                node = d / f"{candidate}.node.md"
                if node.exists():
                    return True, candidate, str(node.relative_to(BASE))

    return False, None, None


# ── Wiki source check ─────────────────────────────────────────────────────────

def wiki_page_exists(slug):
    """Returns the wiki JSON filename (Title_Case) if found."""
    # Try to reconstruct wiki title from slug
    candidates = []

    # 1. Direct kebab→Title_Case conversion
    title = slug.replace("-", "_").title()
    candidates.append(title)

    # 2. Parenthetical suffix
    m = re.match(r"^(.+)-\((.+)\)$", slug)
    if m:
        base = m.group(1).replace("-", "_").title()
        suffix = m.group(2).replace("-", " ").title()
        candidates.append(f"{base}_({suffix})")

    for cand in candidates:
        p = WIKI_RAW / f"{cand}.json"
        if p.exists():
            return str(p)
    return None


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Loading alias map from graph nodes...")
    alias_map = _load_alias_map()
    print(f"  {len(alias_map)} alias entries")

    results = {
        "DROP": [],
        "ALREADY_EXISTS": [],
        "CANONICAL": [],
        "UNCERTAIN": [],
    }

    for slug in TAIL_SLUGS:
        dropped, reason = is_drop(slug)
        if dropped:
            results["DROP"].append((slug, reason))
            continue

        exists, found_slug, node_path = node_exists(slug, alias_map)
        if exists:
            results["ALREADY_EXISTS"].append((slug, found_slug, node_path))
            continue

        # Check if wiki page exists to help assess confidence
        wiki = wiki_page_exists(slug)

        # Classify as canonical or uncertain
        # Parenthetical-suffix patterns → canonical characters/houses
        if re.search(r"-\((maester|archmaester|king|lord|guard|ranger|novice|courtesan|free-folk|master-of-ships)\)$", slug):
            results["CANONICAL"].append((slug, "parenthetical-suffix character/title", wiki))
        elif re.match(r"^house-[a-z]+-\(", slug):
            results["CANONICAL"].append((slug, "minor house with parenthetical disambiguation", wiki))
        elif slug in {
            "dragon-horn",
            "ice-dragon",
            "ghost-grass",
            "grazdan-mo-ullhor",
            "conflict-beyond-the-wall",
            "arryn-succession-conflict-(134-ac)",
            "grand-master",
            "chief-undergaoler",
            "high-king",
            "stern-face",
            "starved-man",
            "handsome-man",
            "garin-(orphan)",
            "fowler-twins",
            "damon-dance-for-me",
            "all-for-joffrey",
            "red-raven-(free-folk)",
            "wine-of-courage",
        }:
            results["CANONICAL"].append((slug, "named in-world entity", wiki))
        elif slug in {
            "the-song-of-ice-and-fire",
            "high-septon-(fat-one)",
        }:
            # Ambiguous: real-world vs in-world
            results["UNCERTAIN"].append((slug, "may be real-world publication or in-world concept — check wiki"))
        else:
            results["UNCERTAIN"].append((slug, "unclassified — needs manual review"))

    # ── Print report ────────────────────────────────────────────────────────

    print("\n" + "="*72)
    print("CASE-COLLISION TAIL FILTER REPORT")
    print("="*72)

    print(f"\n🚫 DROP ({len(results['DROP'])} slugs):")
    for slug, reason in sorted(results["DROP"]):
        print(f"  {slug}")
        print(f"    reason: {reason}")

    print(f"\n✅ ALREADY EXISTS ({len(results['ALREADY_EXISTS'])} slugs):")
    for slug, found, path in sorted(results["ALREADY_EXISTS"]):
        print(f"  {slug}")
        print(f"    → {found} at {path}")

    print(f"\n🔨 CANONICAL — needs reconstruction ({len(results['CANONICAL'])} slugs):")
    for slug, note, wiki in sorted(results["CANONICAL"]):
        wiki_status = f"wiki:{wiki.split('/')[-1]}" if wiki else "wiki:NOT_FOUND"
        print(f"  {slug}")
        print(f"    {note} | {wiki_status}")

    print(f"\n❓ UNCERTAIN — manual review needed ({len(results['UNCERTAIN'])} slugs):")
    for slug, note in sorted(results["UNCERTAIN"]):
        print(f"  {slug}")
        print(f"    {note}")

    total = (len(results["DROP"]) + len(results["ALREADY_EXISTS"]) +
             len(results["CANONICAL"]) + len(results["UNCERTAIN"]))
    print(f"\nTotal: {total}/65  "
          f"(DROP:{len(results['DROP'])}  EXISTS:{len(results['ALREADY_EXISTS'])}  "
          f"CANONICAL:{len(results['CANONICAL'])}  UNCERTAIN:{len(results['UNCERTAIN'])})")

    # ── Write canonicals list for mission file ──────────────────────────────
    out = BASE / "working" / "missions" / "case-collision-tail"
    out.mkdir(parents=True, exist_ok=True)

    canonical_slugs = [s for s, _, _ in results["CANONICAL"]]
    (out / "canonical-slugs.txt").write_text("\n".join(canonical_slugs) + "\n")
    print(f"\nWrote {len(canonical_slugs)} canonical slugs → working/missions/case-collision-tail/canonical-slugs.txt")

    uncertain_slugs = [s for s, _ in results["UNCERTAIN"]]
    (out / "uncertain-slugs.txt").write_text("\n".join(uncertain_slugs) + "\n")
    print(f"Wrote {len(uncertain_slugs)} uncertain slugs → working/missions/case-collision-tail/uncertain-slugs.txt")


if __name__ == "__main__":
    main()
