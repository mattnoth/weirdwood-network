#!/usr/bin/env python3
"""wiki-pass2-fix-date-bleed-remaining.py

Fixes the 178 character nodes that still have BORN_AT/DIED_AT/BURIED_AT
date-bleed edges after the Session 27 repromote wave.

Root cause: the original DATE_BLEED_RE in wiki-pass2-repromote-targeted-2.py
did not match lines where the patched parser appended a [qualifier] bracket
after the (track_b: Born) annotation, e.g.:
    - BORN_AT: 290 AC or 291 AC (track_b: Born) [290 AC]
The presence of [290 AC] at the end caused the old regex to not fire.

Strategy (same as the previous targeted repromote):
  - Stage-3 nodes (pass_origin: pass2-wiki-deterministic): full re-emission
    from fresh infobox-data.jsonl + bucket prose.
  - Stage-1 nodes (agent-derived): surgical edge replacement only —
    preserve everything before/after ## Edges section.

CONSTRAINT: Do NOT touch Stage-1 character nodes for anything other than the
## Edges section. Type strings, prose, aliases in frontmatter are preserved.

Special case: if a node's slug matches 'arryk-cargyll' or 'erryk-cargyll',
preserve the manually-fixed aliases block (these have custom YAML).

Usage:
    python3 scripts/wiki-pass2-fix-date-bleed-remaining.py          # dry-run
    python3 scripts/wiki-pass2-fix-date-bleed-remaining.py --apply  # write
    python3 scripts/wiki-pass2-fix-date-bleed-remaining.py -v       # verbose
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
INFOBOX_DATA_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "infobox-data.jsonl"
PAGE_INDEX_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "page-index.jsonl"
WIKI_PASS2_DIR = PROJECT_ROOT / "working" / "wiki" / "pass2-buckets"
GRAPH_NODES_DIR = PROJECT_ROOT / "graph" / "nodes"

# ---------------------------------------------------------------------------
# Date-bleed detection — correct version that handles trailing [qualifier]
#
# Strategy: parse the edge line to extract the raw target text, then
# slugify it (stripping brackets and parens) and check against DATE_TARGET_RE.
# This matches the logic in orphan-edges-audit.py and is immune to trailing
# bracket qualifiers.
# ---------------------------------------------------------------------------
BORN_DIED_EDGE_RE = re.compile(
    r'^- (?:BORN_AT|DIED_AT|BURIED_AT):\s+(.+?)\s*$',
    re.IGNORECASE,
)

DATE_TARGET_RE = re.compile(
    r'^\d+(-\d+)?-ac$|^\d+(-\d+)?-bc$|^\d+(-\d+)?$|'
    r'^c-\d+-ac$|^pre-\d+-ac$|'
    r'^\d+-ac-or-\d+-ac$|^\d+-ac-or-before$|^\d+-ac-or-after$|'
    r'^\d+-bc.*\d+-ac$|'
    r'^\d+-(or|to)-\d+-ac$'
)


def to_slug(text: str) -> str:
    """Convert target text to slug, stripping [brackets] and (parens)."""
    text = re.sub(r'\[[^\]]*\]', '', text)
    text = re.sub(r'\([^)]*\)', '', text)
    text = text.strip().rstrip('.,;:')
    text = text.strip(' "\'`')
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", '-', text)
    text = text.strip('-')
    return text


def has_date_bleed(content: str) -> bool:
    """Return True if the node has any date-bleed BORN_AT/DIED_AT/BURIED_AT edge."""
    for line in content.splitlines():
        m = BORN_DIED_EDGE_RE.match(line)
        if not m:
            continue
        target_text = m.group(1)
        slug = to_slug(target_text)
        if DATE_TARGET_RE.match(slug):
            return True
    return False


# ---------------------------------------------------------------------------
# Type -> directory mapping
# ---------------------------------------------------------------------------
TYPE_DIR_MAP: dict[str, str] = {
    "character.human":       "characters",
    "character.direwolf":    "characters",
    "character.dragon":      "characters",
    "character":             "characters",
    "organization.house":    "houses",
    "organization.faction":  "factions",
    "organization.cult":     "factions",
    "organization.religion": "religions",
    "organization":          "factions",
    "place.location":        "locations",
    "place.region":          "locations",
    "place.castle":          "locations",
    "place.city":            "locations",
    "place":                 "locations",
    "artifact":              "artifacts",
    "artifact.weapon":       "artifacts",
    "object":                "artifacts",
    "object.artifact":       "artifacts",
    "object.text":           "texts",
    "event.battle":          "events",
    "event.tournament":      "events",
    "event.war":             "events",
    "event":                 "events",
    "battle":                "events",
    "war":                   "events",
    "concept":               "concepts",
    "concept.culture":       "concepts",
    "concept.magic":         "concepts",
    "concept.prophecy":      "prophecies",
    "concept.theory":        "theories",
    "species":               "species",
    "title":                 "titles",
    "prophecy":              "prophecies",
    "theory":                "theories",
    "text":                  "texts",
    # Meta (out-of-universe)
    "meta.chapter":          "chapters",
    "meta":                  "chapters",
}


# ---------------------------------------------------------------------------
# Slug generation
# ---------------------------------------------------------------------------
def page_to_slug(page_name: str) -> str:
    slug = page_name.lower()
    slug = re.sub(r"['\",]", "", slug)
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


# ---------------------------------------------------------------------------
# Atomic write
# ---------------------------------------------------------------------------
def atomic_write(dest_path: Path, data: bytes) -> None:
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    staging = dest_path.parent / f".staging-{dest_path.name}.tmp"
    try:
        staging.write_bytes(data)
        os.rename(staging, dest_path)
    except Exception:
        staging.unlink(missing_ok=True)
        raise


# ---------------------------------------------------------------------------
# Skeleton and edge renderers
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


def replace_edges_section(content: str, new_edges_section: str) -> str:
    """Replace the ## Edges section, preserving everything else."""
    edges_match = re.search(r'^## Edges\s*$', content, re.MULTILINE)
    if not edges_match:
        return content.rstrip("\n") + "\n\n" + new_edges_section

    edges_start = edges_match.start()
    next_heading_match = re.search(r'^## ', content[edges_match.end():], re.MULTILINE)
    if next_heading_match:
        edges_end = edges_match.end() + next_heading_match.start()
        return content[:edges_start] + new_edges_section + "\n" + content[edges_end:]
    else:
        return content[:edges_start] + new_edges_section


# ---------------------------------------------------------------------------
# Cargyll check — slugs that have manually-fixed aliases
# ---------------------------------------------------------------------------
CARGYLL_SLUGS = {"arryk-cargyll", "erryk-cargyll"}


def check_cargyll_aliases(slug: str, content: str) -> str | None:
    """Return the raw YAML aliases block if this is a Cargyll node, else None."""
    if slug not in CARGYLL_SLUGS:
        return None
    # Extract aliases line from frontmatter
    m = re.search(r'^aliases:.*$', content, re.MULTILINE)
    if m:
        return m.group(0)
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--apply", action="store_true",
                        help="Write files. Without --apply, dry-run only.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print per-node output.")
    args = parser.parse_args()

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"\n=== Date-bleed remaining-wave fix [{mode}] ===\n")

    # --- Load infobox-data.jsonl ---
    print(f"Loading {INFOBOX_DATA_FILE} ...")
    if not INFOBOX_DATA_FILE.exists():
        print(f"ERROR: {INFOBOX_DATA_FILE} not found.", file=sys.stderr)
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
        print(f"ERROR: {PAGE_INDEX_FILE} not found.", file=sys.stderr)
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

    # --- Scan characters dir for date-bleed nodes ---
    chars_dir = GRAPH_NODES_DIR / "characters"
    affected_stage3: list[Path] = []
    affected_stage1: list[Path] = []

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

    print(f"Stage-3 nodes with date-bleed: {len(affected_stage3)}")
    print(f"Stage-1 nodes with date-bleed: {len(affected_stage1)}")
    print(f"Total: {len(affected_stage3) + len(affected_stage1)}\n")

    results = []
    errors = []

    # --- Process Stage-3 nodes: full re-emission ---
    print("--- Processing Stage-3 nodes (full re-emission) ---")
    stage3_ok = 0
    stage3_err = 0
    for node_path in affected_stage3:
        slug = node_path.stem.removesuffix(".node")
        content = node_path.read_text(encoding="utf-8")
        name_match = re.search(r'^name:\s*"?([^"\n]+)"?\s*$', content, re.MULTILINE)
        if not name_match:
            errors.append({"slug": slug, "error": "can't extract name from frontmatter"})
            stage3_err += 1
            continue
        page_name = name_match.group(1)

        infobox_rec = infobox_data.get(page_name)
        if infobox_rec is None:
            errors.append({"slug": slug, "error": f"'{page_name}' not in infobox-data"})
            stage3_err += 1
            continue

        bucket_id = page_to_bucket.get(page_name, "unknown")
        confidence = "tier-1"
        manifest_path = WIKI_PASS2_DIR / bucket_id / "manifest.json"
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                confidence = manifest.get("tier_default") or "tier-1"
            except (json.JSONDecodeError, OSError):
                pass

        aliases = infobox_rec.get("aliases") or []
        relationships = infobox_rec.get("relationships") or []
        entity_type = infobox_rec.get("entity_type") or "character.human"

        # Slug-regression guard: ensure slug does not end with .node
        node_slug = slug.removesuffix(".node")

        skeleton_content = render_skeleton(
            page_name=page_name,
            slug=node_slug,
            entity_type=entity_type,
            aliases=aliases,
            confidence=confidence,
            bucket_id=bucket_id,
            relationships=relationships,
            infobox_found=True,
        )
        skeleton_bytes = skeleton_content.encode("utf-8")

        prose_path = WIKI_PASS2_DIR / bucket_id / "prose" / f"{node_slug}.prose.md"
        if prose_path.exists():
            final_bytes = skeleton_bytes + b"\n" + prose_path.read_bytes()
        else:
            final_bytes = skeleton_bytes

        outcome = "would_overwrite"
        if args.apply:
            atomic_write(node_path, final_bytes)
            outcome = "overwritten"

        results.append({
            "stage": "stage3", "slug": slug, "page": page_name,
            "type": entity_type, "edge_count": len(relationships),
            "outcome": outcome,
        })
        if args.verbose:
            print(f"  [s3] {slug}: {outcome} ({len(relationships)} edges)")
        stage3_ok += 1

    print(f"  Stage-3 processed: {stage3_ok} ok, {stage3_err} errors\n")

    # --- Process Stage-1 nodes: surgical edge replacement ---
    print("--- Processing Stage-1 nodes (surgical edge replacement) ---")
    stage1_ok = 0
    stage1_err = 0
    for node_path in affected_stage1:
        slug = node_path.stem.removesuffix(".node")
        content = node_path.read_text(encoding="utf-8")

        # Cargyll check — preserve manually-fixed aliases
        cargyll_aliases_line = check_cargyll_aliases(slug, content)

        name_match = re.search(r'^name:\s*"?([^"\n]+)"?\s*$', content, re.MULTILINE)
        if not name_match:
            errors.append({"slug": slug, "error": "can't extract name from frontmatter (stage1)"})
            stage1_err += 1
            continue
        page_name = name_match.group(1)

        infobox_rec = infobox_data.get(page_name)
        if infobox_rec is None:
            errors.append({"slug": slug, "error": f"'{page_name}' not in infobox-data (stage1)"})
            stage1_err += 1
            continue

        relationships = infobox_rec.get("relationships") or []
        new_edges = render_edges_section(relationships, infobox_found=True)
        new_content = replace_edges_section(content, new_edges)

        # Restore Cargyll aliases if they were present
        if cargyll_aliases_line:
            new_content = re.sub(
                r'^aliases:.*$', cargyll_aliases_line, new_content, flags=re.MULTILINE, count=1
            )

        if new_content == content:
            outcome = "no_change"
        else:
            outcome = "would_replace_edges"
            if args.apply:
                atomic_write(node_path, new_content.encode("utf-8"))
                outcome = "edges_replaced"

        results.append({
            "stage": "stage1", "slug": slug, "page": page_name,
            "type": "character.human", "edge_count": len(relationships),
            "outcome": outcome,
            "cargyll": cargyll_aliases_line is not None,
        })
        if args.verbose:
            cargyll_tag = " [CARGYLL-preserved]" if cargyll_aliases_line else ""
            print(f"  [s1] {slug}: {outcome} ({len(relationships)} edges){cargyll_tag}")
        stage1_ok += 1

    print(f"  Stage-1 processed: {stage1_ok} ok, {stage1_err} errors\n")

    # --- Slug-regression check ---
    print("--- Slug-regression check ---")
    import subprocess
    result = subprocess.run(
        ["grep", "-r", r"^slug: .*\.node$", str(GRAPH_NODES_DIR / "characters")],
        capture_output=True, text=True
    )
    slug_regressions = result.stdout.strip()
    if slug_regressions:
        print(f"  WARNING: Slug regression detected:\n{slug_regressions}")
    else:
        print("  OK: No slug regressions found.")
    print()

    # --- Summary ---
    print("=" * 60)
    total_processed = stage3_ok + stage1_ok
    total_errors = len(errors)
    print(f"Total nodes with date-bleed found: {len(affected_stage3) + len(affected_stage1)}")
    print(f"  Stage-3 (full re-emission): {stage3_ok} ok, {stage3_err} errors")
    print(f"  Stage-1 (surgical):          {stage1_ok} ok, {stage1_err} errors")
    print(f"  Total errors:                {total_errors}")

    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  {e['slug']}: {e['error']}")

    if args.apply:
        s3_written = sum(1 for r in results if r["stage"] == "stage3" and r["outcome"] == "overwritten")
        s1_written = sum(1 for r in results if r["stage"] == "stage1" and r["outcome"] == "edges_replaced")
        s1_no_change = sum(1 for r in results if r["stage"] == "stage1" and r["outcome"] == "no_change")
        cargyll_preserved = sum(1 for r in results if r.get("cargyll"))
        print(f"\nApplied:")
        print(f"  Stage-3 overwritten:       {s3_written}")
        print(f"  Stage-1 edges replaced:    {s1_written}")
        print(f"  Stage-1 no-change:         {s1_no_change}")
        if cargyll_preserved:
            print(f"  Cargyll aliases preserved: {cargyll_preserved}")
    else:
        print("\nDry-run complete. Run with --apply to write files.")
    print("=" * 60)


if __name__ == "__main__":
    main()
