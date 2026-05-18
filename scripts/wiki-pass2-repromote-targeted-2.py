#!/usr/bin/env python3
"""Targeted re-promotion for three parser-bug fixes from Session 27 audit.

Bug 1 — BORN_AT/DIED_AT date-bleed (~1,235 character nodes):
  Parser was emitting date strings ("263 AC", "Age of Heroes", bare "282") as
  edge targets in BORN_AT/DIED_AT/BURIED_AT edges instead of as qualifiers.
  Fix: these date strings are now stripped and stored as qualifier metadata.
  Affected: Stage-3 deterministic nodes in graph/nodes/characters/ (1,137)
  and Stage-1 agent nodes (98). Stage-3 nodes are fully re-emitted; Stage-1
  nodes get only their ## Edges section surgically replaced (preserving prose).

Bug 2 — Dragon mistyping (~19 existing nodes, 9 not yet in graph):
  All dragon pages emitted type: character.human instead of character.dragon.
  Fix: Species infobox field now correctly drives type classification.
  Affected: 19 Stage-3 nodes in graph/nodes/characters/. No directory move
  needed (character.dragon also lives in characters/). 9 pages not yet
  promoted are skipped (they have no existing node to update).

Bug 3 — guards pages mistyped as organization.house (~6 nodes):
  House *_guards sub-pages are guard contingents, not standalone houses.
  Fix: page-name pattern now routes them to organization.faction.
  Affected: 6 nodes in graph/nodes/houses/ → move to graph/nodes/factions/.

Strategy for each group:
  Stage-3 nodes (bugs 1+2+3): re-emit skeleton from fresh infobox-data.jsonl,
    append prose from bucket prose/ directory (if exists), atomic-rename to
    correct destination. Delete old wrong-directory file for Bug 3.
  Stage-1 nodes (bug 1 only): surgically replace only the ## Edges section.
    Everything before ## Edges (frontmatter, ## Identity, prose) is preserved.
    Edges are regenerated from fresh infobox-data.jsonl. Type string is also
    updated in frontmatter when needed (not applicable for bug-1 Stage-1 nodes
    since their type is already character.human — the date-bleed is in edges only).

Usage:
  python3 scripts/wiki-pass2-repromote-targeted-2.py           # dry-run
  python3 scripts/wiki-pass2-repromote-targeted-2.py --apply   # write files
  python3 scripts/wiki-pass2-repromote-targeted-2.py -v        # verbose
  python3 scripts/wiki-pass2-repromote-targeted-2.py --bug 1   # one bug at a time
  python3 scripts/wiki-pass2-repromote-targeted-2.py --bug 2 --apply
  python3 scripts/wiki-pass2-repromote-targeted-2.py --bug 3 --apply
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
INFOBOX_DATA_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "infobox-data.jsonl"
PAGE_INDEX_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "page-index.jsonl"
WIKI_PASS2_DIR = PROJECT_ROOT / "working" / "wiki" / "pass2-buckets"
GRAPH_NODES_DIR = PROJECT_ROOT / "graph" / "nodes"

# ---------------------------------------------------------------------------
# Bug 2: Dragon page names (all 28 pages with Species: Dragon infobox field)
# ---------------------------------------------------------------------------
DRAGON_PAGES = [
    "Arrax", "Balerion", "Cannibal (dragon)", "Caraxes",
    "Dragon that died in the Red Waste", "Dreamfyre", "Drogon", "Grey Ghost",
    "Last dragon", "Meleys", "Meraxes", "Moondancer", "Morghul", "Morning",
    "Quicksilver", "Rhaegal", "Seasmoke", "Sheepstealer", "Shrykos", "Silverwing",
    "Sunfyre", "Terrax", "Tessarion", "Tyraxes", "Vermax", "Vermithor",
    "Vhagar", "Viserion",
]

# ---------------------------------------------------------------------------
# Bug 3: Guards page names (all 6 pages to retype + move)
# ---------------------------------------------------------------------------
GUARDS_PAGES = [
    "House Bolton guards",
    "House Stark guards",
    "House Tully guards",
    "House Tyrell guards",
    "House Arryn guards",
    "House Targaryen guards",
]

# ---------------------------------------------------------------------------
# Date-bleed detection patterns (mirrors the parser fix for identification)
# ---------------------------------------------------------------------------
DATE_BLEED_RE = re.compile(
    r'^- (?:BORN_AT|DIED_AT|BURIED_AT):\s+'
    # Date-only targets: year strings, era names
    r'(?:\d[\d\s\xa0–—-]*(?:AC|BC)?'
    r'|Age of Heroes|Long Night|Dawn Age'
    r'|Age of Valyria|Valyrian Freehold'
    r'|Days of the First Men'
    r')\s*(?:\(track_b:.*\))?\s*$',
    re.IGNORECASE,
)
# Sub-pattern B: composite "Place, Year" in one line
PLACE_DATE_BLEED_RE = re.compile(
    r'^- (?:BORN_AT|DIED_AT|BURIED_AT):\s+[A-Z].+,\s*\d+\s*(?:AC|BC)?'
    r'\s*(?:\(track_b:.*\))?\s*$',
)


def has_date_bleed(content: str) -> bool:
    """Return True if the node file has any date-bleed BORN_AT/DIED_AT edges."""
    for line in content.splitlines():
        if DATE_BLEED_RE.match(line) or PLACE_DATE_BLEED_RE.match(line):
            return True
    return False


# ---------------------------------------------------------------------------
# Type -> directory mapping (mirrors wiki-pass2-promote.py)
# ---------------------------------------------------------------------------
TYPE_DIR_MAP: dict[str, str] = {
    "character.human":      "characters",
    "character.direwolf":   "characters",
    "character.dragon":     "characters",
    "character":            "characters",
    "organization.house":   "houses",
    "organization.faction": "factions",
    "organization.cult":    "factions",
    "organization.religion": "religions",
    "organization":         "factions",
    "place.location":       "locations",
    "place.region":         "locations",
    "place.castle":         "locations",
    "place.city":           "locations",
    "place":                "locations",
    "artifact":             "artifacts",
    "artifact.weapon":      "artifacts",
    "object":               "artifacts",
    "object.artifact":      "artifacts",
    "object.text":          "texts",
    "event.battle":         "events",
    "event.tournament":     "events",
    "event.war":            "events",
    "event":                "events",
    "battle":               "events",
    "war":                  "events",
    "concept":              "concepts",
    "concept.culture":      "concepts",
    "concept.magic":        "concepts",
    "concept.prophecy":     "prophecies",
    "concept.theory":       "theories",
    "species":              "species",
    "title":                "titles",
    "prophecy":             "prophecies",
    "theory":               "theories",
    "text":                 "texts",
    # Meta (out-of-universe)
    "meta.chapter":         "chapters",
    "meta":                 "chapters",
}


def resolve_type_dir(entity_type: str) -> str | None:
    if entity_type in TYPE_DIR_MAP:
        return TYPE_DIR_MAP[entity_type]
    parent = entity_type.split(".")[0]
    if parent in TYPE_DIR_MAP:
        return TYPE_DIR_MAP[parent]
    return None


# ---------------------------------------------------------------------------
# Slug generation (matches wiki-pass2-emit-deterministic.py exactly)
# ---------------------------------------------------------------------------

def page_to_slug(page_name: str) -> str:
    slug = page_name.lower()
    slug = re.sub(r"['\",]", "", slug)
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


# ---------------------------------------------------------------------------
# Atomic write helper
# ---------------------------------------------------------------------------

def atomic_write(dest_path: Path, data: bytes) -> None:
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    staging = dest_path.parent / f".staging-{dest_path.name}.tmp"
    try:
        staging.write_bytes(data)
        os.rename(staging, dest_path)
    except Exception:
        try:
            staging.unlink(missing_ok=True)
        except Exception:
            pass
        raise


# ---------------------------------------------------------------------------
# Skeleton renderer (mirrors wiki-pass2-emit-deterministic.py::render_node)
# ---------------------------------------------------------------------------

def wiki_url(page_name: str) -> str:
    import urllib.parse
    encoded = urllib.parse.quote(page_name.replace(" ", "_"), safe="/:@!$&'()*+,;=")
    return f"https://awoiaf.westeros.org/index.php/{encoded}"


def render_edge_line(rel: dict) -> str:
    edge_type = rel.get("edge_type", "UNKNOWN_EDGE")
    target = rel.get("target", "")
    field = rel.get("field", "")
    direction = rel.get("direction", "forward")
    qualifier = rel.get("qualifier", "")

    edge_label = f"{edge_type} (reverse)" if direction == "reverse" else edge_type
    line = f"- {edge_label}: {target} (track_b: {field})"
    if qualifier:
        line += f" [{qualifier}]"
    return line


def render_skeleton(
    page_name: str,
    slug: str,
    entity_type: str,
    aliases: list,
    confidence: str,
    bucket_id: str,
    relationships: list,
    infobox_found: bool,
) -> str:
    url = wiki_url(page_name)

    if aliases:
        alias_items = ", ".join(f'"{a}"' for a in aliases)
        aliases_yaml = f"[{alias_items}]"
    else:
        aliases_yaml = "[]"

    lines = [
        "---",
        f'name: "{page_name}"',
        f"type: {entity_type}",
        f"slug: {slug}",
        f"aliases: {aliases_yaml}",
        f"confidence: {confidence}",
        f'wiki_source: "{url}"',
        f"bucket_id: {bucket_id}",
        "prompt_version: v1-python",
        "node_version: 1",
        "pass_origin: pass2-wiki-deterministic",
        "---",
        "",
        "## Identity",
        "",
        f"{page_name} is a {entity_type} from the AWOIAF wiki.",
        "",
        "## Edges",
        "",
    ]

    if relationships and infobox_found:
        for rel in relationships:
            lines.append(render_edge_line(rel))

    lines.append("")
    return "\n".join(lines)


def render_edges_section(relationships: list, infobox_found: bool) -> str:
    """Render just the ## Edges section (for surgical Stage-1 replacement)."""
    lines = ["## Edges", ""]
    if relationships and infobox_found:
        for rel in relationships:
            lines.append(render_edge_line(rel))
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Surgical Stage-1 edge replacement
# ---------------------------------------------------------------------------

def replace_edges_section(content: str, new_edges_section: str) -> str:
    """Replace the ## Edges section in a node file, preserving surrounding content.

    Finds ## Edges and replaces everything from that heading up to (but not
    including) the next ## heading, or to end of file if Edges is the last section.
    """
    # Find the ## Edges heading
    edges_match = re.search(r'^## Edges\s*$', content, re.MULTILINE)
    if not edges_match:
        # No Edges section found — append it
        return content.rstrip("\n") + "\n\n" + new_edges_section

    edges_start = edges_match.start()

    # Find the next ## heading after Edges
    next_heading_match = re.search(r'^## ', content[edges_match.end():], re.MULTILINE)
    if next_heading_match:
        edges_end = edges_match.end() + next_heading_match.start()
        # Preserve the content from next heading onward
        return content[:edges_start] + new_edges_section + "\n" + content[edges_end:]
    else:
        # Edges is the last section
        return content[:edges_start] + new_edges_section


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help="Write new nodes and delete old wrong-type files. Without --apply, dry-run only.",
    )
    parser.add_argument(
        "--bug",
        type=int,
        choices=[1, 2, 3],
        default=None,
        help="Process only the specified bug number (default: all three bugs).",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Print detailed per-page output.",
    )
    args = parser.parse_args()

    run_bug1 = args.bug is None or args.bug == 1
    run_bug2 = args.bug is None or args.bug == 2
    run_bug3 = args.bug is None or args.bug == 3

    mode = "APPLY" if args.apply else "DRY-RUN"
    bugs_running = [b for b, r in [(1, run_bug1), (2, run_bug2), (3, run_bug3)] if r]
    print(f"\n=== Targeted re-promotion (bugs {bugs_running}) [{mode}] ===\n")

    # --- Load infobox-data.jsonl ---
    print(f"Loading {INFOBOX_DATA_FILE} ...")
    if not INFOBOX_DATA_FILE.exists():
        print(f"ERROR: {INFOBOX_DATA_FILE} not found. Re-run wiki-infobox-parser.py first.",
              file=sys.stderr)
        sys.exit(1)
    infobox_data: dict[str, dict] = {}
    with open(INFOBOX_DATA_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            infobox_data[rec["page"]] = rec
    print(f"  {len(infobox_data):,} infobox records loaded")

    # --- Load page-index.jsonl ---
    print(f"Loading {PAGE_INDEX_FILE} ...")
    if not PAGE_INDEX_FILE.exists():
        print(f"ERROR: {PAGE_INDEX_FILE} not found. Re-run wiki-infobox-parser.py first.",
              file=sys.stderr)
        sys.exit(1)
    page_index: dict[str, dict] = {}
    with open(PAGE_INDEX_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            page_index[rec["page"]] = rec
    print(f"  {len(page_index):,} page-index records loaded")

    # --- Build manifest lookup: page_name → bucket_id ---
    print("Building manifest lookup...")
    page_to_bucket: dict[str, str] = {}
    for manifest_path in WIKI_PASS2_DIR.rglob("manifest.json"):
        bucket_id = manifest_path.parent.name
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for page in manifest.get("input_pages", []):
                page_to_bucket[page] = bucket_id
        except (json.JSONDecodeError, OSError):
            pass
    print(f"  {len(page_to_bucket):,} page-to-bucket mappings loaded\n")

    results = []
    errors = []

    # ==========================================================================
    # Bug 1: BORN_AT/DIED_AT date-bleed — fix edges in character nodes
    # ==========================================================================
    if run_bug1:
        print("--- Bug 1: BORN_AT/DIED_AT date-bleed ---")
        chars_dir = GRAPH_NODES_DIR / "characters"

        # Find all character nodes with date-bleed edges
        affected_stage3 = []
        affected_stage1 = []
        for node_path in sorted(chars_dir.iterdir()):
            if node_path.suffix != ".md":
                continue
            try:
                content = node_path.read_text(encoding="utf-8")
            except OSError:
                continue
            if not has_date_bleed(content):
                continue
            if "pass_origin: pass2-wiki-deterministic" in content:
                affected_stage3.append(node_path)
            else:
                affected_stage1.append(node_path)

        print(f"  Stage-3 nodes with date-bleed: {len(affected_stage3)}")
        print(f"  Stage-1 nodes with date-bleed: {len(affected_stage1)}")

        # Process Stage-3 nodes: full re-emission
        stage3_ok = 0
        stage3_err = 0
        for node_path in affected_stage3:
            slug = node_path.stem.removesuffix(".node")
            # Find page name from node frontmatter
            content = node_path.read_text(encoding="utf-8")
            name_match = re.search(r'^name:\s*"?([^"\n]+)"?\s*$', content, re.MULTILINE)
            if not name_match:
                errors.append({"bug": 1, "slug": slug, "error": "can't extract page name from frontmatter"})
                stage3_err += 1
                continue
            page_name = name_match.group(1)

            # Get fresh infobox data
            infobox_rec = infobox_data.get(page_name)
            if infobox_rec is None:
                errors.append({"bug": 1, "slug": slug, "error": f"page '{page_name}' not in infobox-data"})
                stage3_err += 1
                continue

            bucket_id = page_to_bucket.get(page_name, "unknown")
            # Get bucket confidence tier
            manifest_path = WIKI_PASS2_DIR / bucket_id / "manifest.json"
            confidence = "tier-1"
            if manifest_path.exists():
                try:
                    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                    confidence = manifest.get("tier_default") or "tier-1"
                except (json.JSONDecodeError, OSError):
                    pass

            aliases = infobox_rec.get("aliases") or []
            relationships = infobox_rec.get("relationships") or []
            entity_type = infobox_rec.get("entity_type") or "character.human"

            skeleton_content = render_skeleton(
                page_name=page_name,
                slug=slug,
                entity_type=entity_type,
                aliases=aliases,
                confidence=confidence,
                bucket_id=bucket_id,
                relationships=relationships,
                infobox_found=True,
            )
            skeleton_bytes = skeleton_content.encode("utf-8")

            # Append prose from bucket if exists
            prose_path = WIKI_PASS2_DIR / bucket_id / "prose" / f"{slug}.prose.md"
            if prose_path.exists():
                prose_bytes = prose_path.read_bytes()
                final_bytes = skeleton_bytes + b"\n" + prose_bytes
            else:
                final_bytes = skeleton_bytes

            outcome = "would_overwrite"
            if args.apply:
                atomic_write(node_path, final_bytes)
                outcome = "overwritten"

            results.append({
                "bug": 1, "stage": "stage3", "slug": slug,
                "page": page_name, "type": entity_type,
                "edge_count": len(relationships), "outcome": outcome,
            })
            if args.verbose:
                print(f"  [bug1/s3] {slug}: {outcome} ({len(relationships)} edges)")
            stage3_ok += 1

        # Process Stage-1 nodes: surgical edge replacement only
        stage1_ok = 0
        stage1_err = 0
        for node_path in affected_stage1:
            slug = node_path.stem.removesuffix(".node")
            content = node_path.read_text(encoding="utf-8")

            # Find page name from frontmatter
            name_match = re.search(r'^name:\s*"?([^"\n]+)"?\s*$', content, re.MULTILINE)
            if not name_match:
                errors.append({"bug": 1, "slug": slug, "error": "can't extract page name from frontmatter (stage1)"})
                stage1_err += 1
                continue
            page_name = name_match.group(1)

            # Get fresh infobox data
            infobox_rec = infobox_data.get(page_name)
            if infobox_rec is None:
                errors.append({"bug": 1, "slug": slug, "error": f"page '{page_name}' not in infobox-data (stage1)"})
                stage1_err += 1
                continue

            relationships = infobox_rec.get("relationships") or []
            new_edges = render_edges_section(relationships, infobox_found=True)
            new_content = replace_edges_section(content, new_edges)

            if new_content == content:
                outcome = "no_change"
            else:
                outcome = "would_overwrite_edges"
                if args.apply:
                    atomic_write(node_path, new_content.encode("utf-8"))
                    outcome = "edges_replaced"

            results.append({
                "bug": 1, "stage": "stage1", "slug": slug,
                "page": page_name, "type": "character.human",
                "edge_count": len(relationships), "outcome": outcome,
            })
            if args.verbose:
                print(f"  [bug1/s1] {slug}: {outcome} ({len(relationships)} edges, surgical)")
            stage1_ok += 1

        print(f"  Stage-3 processed: {stage3_ok} ok, {stage3_err} errors")
        print(f"  Stage-1 processed: {stage1_ok} ok, {stage1_err} errors")
        print()

    # ==========================================================================
    # Bug 2: Dragon mistyping — retype character.human → character.dragon
    # ==========================================================================
    if run_bug2:
        print("--- Bug 2: Dragon mistyping ---")
        chars_dir = GRAPH_NODES_DIR / "characters"
        dragon_ok = 0
        dragon_skip = 0
        dragon_err = 0

        for page_name in DRAGON_PAGES:
            slug = page_to_slug(page_name)
            node_path = chars_dir / f"{slug}.node.md"

            if not node_path.exists():
                if args.verbose:
                    print(f"  [bug2] {slug}: SKIP (not in graph)")
                dragon_skip += 1
                results.append({"bug": 2, "slug": slug, "page": page_name,
                                 "outcome": "skipped_no_node"})
                continue

            content = node_path.read_text(encoding="utf-8")
            is_stage3 = "pass_origin: pass2-wiki-deterministic" in content

            if not is_stage3:
                # Stage-1 node: surgically update type string in frontmatter
                if "type: character.dragon" in content:
                    results.append({"bug": 2, "slug": slug, "page": page_name,
                                     "outcome": "already_correct"})
                    dragon_skip += 1
                    continue
                new_content = content.replace("type: character.human",
                                               "type: character.dragon", 1)
                outcome = "would_overwrite_type"
                if args.apply:
                    atomic_write(node_path, new_content.encode("utf-8"))
                    outcome = "type_replaced"
                results.append({"bug": 2, "stage": "stage1", "slug": slug,
                                 "page": page_name, "outcome": outcome})
                if args.verbose:
                    print(f"  [bug2/s1] {slug}: {outcome}")
                dragon_ok += 1
                continue

            # Stage-3 node: full re-emission
            infobox_rec = infobox_data.get(page_name)
            if infobox_rec is None:
                errors.append({"bug": 2, "slug": slug, "error": f"not in infobox-data"})
                dragon_err += 1
                continue

            bucket_id = page_to_bucket.get(page_name, "unknown")
            manifest_path = WIKI_PASS2_DIR / bucket_id / "manifest.json"
            confidence = "tier-1"
            if manifest_path.exists():
                try:
                    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                    confidence = manifest.get("tier_default") or "tier-1"
                except (json.JSONDecodeError, OSError):
                    pass

            aliases = infobox_rec.get("aliases") or []
            relationships = infobox_rec.get("relationships") or []
            entity_type = infobox_rec.get("entity_type") or "character.dragon"
            if entity_type != "character.dragon":
                errors.append({"bug": 2, "slug": slug,
                                "error": f"parser returned type={entity_type!r}, expected character.dragon"})
                dragon_err += 1
                continue

            skeleton_content = render_skeleton(
                page_name=page_name,
                slug=slug,
                entity_type=entity_type,
                aliases=aliases,
                confidence=confidence,
                bucket_id=bucket_id,
                relationships=relationships,
                infobox_found=True,
            )
            skeleton_bytes = skeleton_content.encode("utf-8")
            prose_path = WIKI_PASS2_DIR / bucket_id / "prose" / f"{slug}.prose.md"
            if prose_path.exists():
                final_bytes = skeleton_bytes + b"\n" + prose_path.read_bytes()
            else:
                final_bytes = skeleton_bytes

            outcome = "would_overwrite"
            if args.apply:
                atomic_write(node_path, final_bytes)
                outcome = "overwritten"

            results.append({"bug": 2, "stage": "stage3", "slug": slug,
                             "page": page_name, "type": entity_type,
                             "edge_count": len(relationships), "outcome": outcome})
            if args.verbose:
                print(f"  [bug2/s3] {slug}: {outcome} (type={entity_type})")
            dragon_ok += 1

        print(f"  Dragon nodes updated: {dragon_ok}, skipped: {dragon_skip}, errors: {dragon_err}")
        print()

    # ==========================================================================
    # Bug 3: Guards pages — retype + move houses/ → factions/
    # ==========================================================================
    if run_bug3:
        print("--- Bug 3: Guards page mistyping ---")
        houses_dir = GRAPH_NODES_DIR / "houses"
        factions_dir = GRAPH_NODES_DIR / "factions"
        guards_ok = 0
        guards_err = 0

        for page_name in GUARDS_PAGES:
            slug = page_to_slug(page_name)
            old_path = houses_dir / f"{slug}.node.md"
            new_path = factions_dir / f"{slug}.node.md"

            if not old_path.exists():
                if args.verbose:
                    print(f"  [bug3] {slug}: SKIP (not in houses/)")
                results.append({"bug": 3, "slug": slug, "page": page_name,
                                 "outcome": "skipped_no_old_node"})
                guards_err += 1
                continue

            content = old_path.read_text(encoding="utf-8")
            is_stage3 = "pass_origin: pass2-wiki-deterministic" in content

            if is_stage3:
                # Full re-emission with corrected type
                infobox_rec = infobox_data.get(page_name)
                bucket_id = page_to_bucket.get(page_name, "unknown")
                manifest_path = WIKI_PASS2_DIR / bucket_id / "manifest.json"
                confidence = "tier-1"
                if manifest_path.exists():
                    try:
                        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                        confidence = manifest.get("tier_default") or "tier-1"
                    except (json.JSONDecodeError, OSError):
                        pass

                if infobox_rec:
                    aliases = infobox_rec.get("aliases") or []
                    relationships = infobox_rec.get("relationships") or []
                    infobox_found = True
                else:
                    aliases = []
                    relationships = []
                    infobox_found = False

                skeleton_content = render_skeleton(
                    page_name=page_name,
                    slug=slug,
                    entity_type="organization.faction",
                    aliases=aliases,
                    confidence=confidence,
                    bucket_id=bucket_id,
                    relationships=relationships,
                    infobox_found=infobox_found,
                )
                skeleton_bytes = skeleton_content.encode("utf-8")
                prose_path = WIKI_PASS2_DIR / bucket_id / "prose" / f"{slug}.prose.md"
                if prose_path.exists():
                    final_bytes = skeleton_bytes + b"\n" + prose_path.read_bytes()
                else:
                    final_bytes = skeleton_bytes
            else:
                # Stage-1: update type string, keep prose
                final_content = content.replace(
                    "type: organization.house",
                    "type: organization.faction", 1,
                )
                final_bytes = final_content.encode("utf-8")

            outcome = "would_promote+would_delete_old"
            if args.apply:
                atomic_write(new_path, final_bytes)
                old_path.unlink()
                outcome = "promoted+deleted_old"

            results.append({"bug": 3, "slug": slug, "page": page_name,
                             "old_dir": "houses", "new_dir": "factions",
                             "outcome": outcome})
            if args.verbose:
                print(f"  [bug3] {slug}: {outcome}")
            guards_ok += 1

        print(f"  Guards nodes moved: {guards_ok} ok, {guards_err} not found")
        print()

    # --- Summary ---
    print("=" * 60)
    total_ok = sum(1 for r in results if "would" not in r["outcome"]
                   and "skipped" not in r["outcome"] and "no_change" not in r["outcome"])
    total_skipped = sum(1 for r in results if "skipped" in r["outcome"])
    total_no_change = sum(1 for r in results if "no_change" in r["outcome"])
    total_errors = len(errors)

    print(f"Total results:   {len(results)}")
    print(f"Errors:          {total_errors}")
    print()

    if args.apply:
        b1_s3 = sum(1 for r in results if r.get("bug") == 1 and r.get("stage") == "stage3" and "overwritten" in r["outcome"])
        b1_s1 = sum(1 for r in results if r.get("bug") == 1 and r.get("stage") == "stage1" and "replaced" in r["outcome"])
        b2 = sum(1 for r in results if r.get("bug") == 2 and "overwritten" in r.get("outcome", "") or "replaced" in r.get("outcome", ""))
        b3 = sum(1 for r in results if r.get("bug") == 3 and "promoted" in r.get("outcome", ""))
        print(f"Bug 1 — Stage-3 nodes overwritten:        {b1_s3}")
        print(f"Bug 1 — Stage-1 nodes (edges replaced):   {b1_s1}")
        print(f"Bug 2 — Dragon nodes retyped:             {b2}")
        print(f"Bug 3 — Guards nodes moved houses→factions: {b3}")
    else:
        b1_s3 = sum(1 for r in results if r.get("bug") == 1 and r.get("stage") == "stage3")
        b1_s1 = sum(1 for r in results if r.get("bug") == 1 and r.get("stage") == "stage1")
        b2 = sum(1 for r in results if r.get("bug") == 2 and "skip" not in r.get("outcome", "") and "already" not in r.get("outcome", ""))
        b3 = sum(1 for r in results if r.get("bug") == 3 and "would" in r.get("outcome", ""))
        print(f"Bug 1 — Stage-3 nodes would overwrite:     {b1_s3}")
        print(f"Bug 1 — Stage-1 nodes (edges would replace): {b1_s1}")
        print(f"Bug 2 — Dragon nodes would retype:          {b2}")
        print(f"Bug 3 — Guards nodes would move:            {b3}")

    if errors:
        print()
        print("Errors:")
        for e in errors:
            print(f"  Bug {e.get('bug')}: {e.get('slug', '?')}: {e.get('error', '?')}")

    if not args.apply:
        print()
        print("Dry-run complete. Run with --apply to write files.")
    print("=" * 60)


if __name__ == "__main__":
    main()
