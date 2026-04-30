#!/usr/bin/env python3
"""wiki-pass2-stage3-house-location-reemit.py

Step 3 of the 2026-04-30 cleanup pipeline.

Scope A — Stage-1 houses (prompt_version: v1):
  259 house nodes were emitted by the Stage-1 wiki-ingester agent with an
  older edge format (cite: track_b_row.relationships.X). These need to be
  upgraded to the deterministic v1-python format. 170/259 have agent-written
  ## Notes sections that must be preserved.

  Strategy: SURGICAL edge replacement (replace ## Edges section only).
  This preserves ## Notes, ## Identity prose, and all other sections.

  Safety check: if the fresh skeleton has FEWER edges than current by >3,
  skip that house (heuristic: unusual edge-count drop may indicate the
  infobox-data is missing fields). Skipped houses are logged to
  working/wiki-pass2/stage3-house-reemit-skipped.jsonl.

Scope B — Religion-bleed location nodes (24/25 nodes):
  Location and faction nodes that were emitted before the Session 27
  religion-field parser fix. These are all Stage-3 (v1-python) so full
  re-emission is safe (bucket prose files exist for these).

  List derived from working/audits/orphan-edges-2026-04-30.md stale-data
  section, plus triarchy (in factions/).

Usage:
    python3 scripts/wiki-pass2-stage3-house-location-reemit.py          # dry-run
    python3 scripts/wiki-pass2-stage3-house-location-reemit.py --apply  # write
    python3 scripts/wiki-pass2-stage3-house-location-reemit.py --scope A  # houses only
    python3 scripts/wiki-pass2-stage3-house-location-reemit.py --scope B  # locations only
    python3 scripts/wiki-pass2-stage3-house-location-reemit.py -v       # verbose
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
INFOBOX_DATA_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "infobox-data.jsonl"
PAGE_INDEX_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "page-index.jsonl"
WIKI_PASS2_DIR = PROJECT_ROOT / "working" / "wiki-pass2"
GRAPH_NODES_DIR = PROJECT_ROOT / "graph" / "nodes"
SKIP_LOG = PROJECT_ROOT / "working" / "wiki-pass2" / "stage3-house-reemit-skipped.jsonl"
SUMMARY_LOG = PROJECT_ROOT / "working" / "wiki-pass2" / "stage3-reemit-summary.json"

# ---------------------------------------------------------------------------
# Religion-bleed location/faction slugs (Scope B)
# ---------------------------------------------------------------------------
RELIGION_BLEED_SLUGS = [
    "asshai", "barrow-hall", "barrowton", "blackpool", "braavos",
    "deepwood-motte", "dreadfort", "greywater-watch", "karhold", "last-hearth",
    "lorath", "meereen", "myr", "new-ghis", "old-empire-of-ghis",
    "raventree-hall", "valyria", "valyrian-freehold", "vaes-dothrak",
    "volantis", "white-harbor", "whitetree", "winterfell", "seven-kingdoms",
    "triarchy",
]

# ---------------------------------------------------------------------------
# Edge-count diff threshold (skip if fresh has > N fewer edges)
# ---------------------------------------------------------------------------
EDGE_COUNT_SKIP_THRESHOLD = 3


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
}


def resolve_type_dir(entity_type: str) -> str | None:
    if entity_type in TYPE_DIR_MAP:
        return TYPE_DIR_MAP[entity_type]
    parent = entity_type.split(".")[0]
    if parent in TYPE_DIR_MAP:
        return TYPE_DIR_MAP[parent]
    return None


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
    """Render just the ## Edges section for surgical replacement."""
    lines = ["## Edges", ""]
    if relationships and infobox_found:
        for rel in relationships:
            lines.append(render_edge_line(rel))
    lines.append("")
    return "\n".join(lines)


def replace_edges_section(content: str, new_edges_section: str) -> str:
    """Replace the ## Edges section, preserving all other content."""
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


def count_edges(content: str) -> int:
    """Count the number of edge lines in a node's ## Edges section."""
    edges_match = re.search(r'^## Edges\s*$', content, re.MULTILINE | re.DOTALL)
    if not edges_match:
        return 0
    # Find end of edges section
    rest = content[edges_match.end():]
    next_h = re.search(r'^## ', rest, re.MULTILINE)
    if next_h:
        edges_block = rest[:next_h.start()]
    else:
        edges_block = rest
    return sum(1 for line in edges_block.splitlines() if line.strip().startswith("- "))


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
    parser.add_argument("--scope", choices=["A", "B", "AB"], default="AB",
                        help="Scope to run: A=houses, B=locations, AB=both (default)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print per-node output.")
    args = parser.parse_args()

    run_a = args.scope in ("A", "AB")
    run_b = args.scope in ("B", "AB")
    mode = "APPLY" if args.apply else "DRY-RUN"
    scope_str = f"A={'yes' if run_a else 'no'}, B={'yes' if run_b else 'no'}"
    print(f"\n=== Stage-3 house + location re-emission [{mode}] [{scope_str}] ===\n")

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

    # --- Build manifest lookup ---
    print("Building manifest lookup...")
    page_to_bucket: dict[str, str] = {}
    bucket_confidence: dict[str, str] = {}
    for manifest_path in WIKI_PASS2_DIR.rglob("manifest.json"):
        bucket_id = manifest_path.parent.name
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            confidence = manifest.get("tier_default") or "tier-1"
            bucket_confidence[bucket_id] = confidence
            for page in manifest.get("input_pages", []):
                page_to_bucket[page] = bucket_id
        except (json.JSONDecodeError, OSError):
            pass
    print(f"  {len(page_to_bucket):,} page-to-bucket mappings loaded\n")

    results = []
    errors = []
    skipped = []

    # ==========================================================================
    # Scope A: Stage-1 houses — surgical edge replacement
    # ==========================================================================
    if run_a:
        print("--- Scope A: Stage-1 houses (surgical edge replacement) ---")
        houses_dir = GRAPH_NODES_DIR / "houses"

        v1_house_paths = []
        for p in sorted(houses_dir.glob("*.node.md")):
            content = p.read_text(encoding="utf-8")
            if "prompt_version: v1\n" in content:
                v1_house_paths.append(p)

        print(f"  Stage-1 houses found: {len(v1_house_paths)}")

        scope_a_ok = 0
        scope_a_skip = 0
        scope_a_err = 0
        scope_a_no_change = 0

        for node_path in v1_house_paths:
            slug = node_path.stem.removesuffix(".node")
            content = node_path.read_text(encoding="utf-8")
            current_edge_count = count_edges(content)

            # Get page name
            name_match = re.search(r'^name:\s*"?([^"\n]+)"?\s*$', content, re.MULTILINE)
            if not name_match:
                errors.append({"scope": "A", "slug": slug, "error": "no name in frontmatter"})
                scope_a_err += 1
                continue
            page_name = name_match.group(1)

            infobox_rec = infobox_data.get(page_name)
            if infobox_rec is None:
                # No infobox — skip (house node with no infobox entry; edges come from agent)
                skip_reason = "no infobox record"
                skipped.append({"scope": "A", "slug": slug, "page": page_name, "reason": skip_reason,
                                 "current_edges": current_edge_count, "fresh_edges": 0})
                if args.verbose:
                    print(f"  SKIP {slug}: {skip_reason}")
                scope_a_skip += 1
                continue

            relationships = infobox_rec.get("relationships") or []
            fresh_edge_count = len(relationships)

            # Safety check: skip if fresh has >3 fewer edges than current
            edge_diff = current_edge_count - fresh_edge_count
            if edge_diff > EDGE_COUNT_SKIP_THRESHOLD:
                skip_reason = f"edge-count-drop: current={current_edge_count} fresh={fresh_edge_count} diff={edge_diff}"
                skipped.append({"scope": "A", "slug": slug, "page": page_name, "reason": skip_reason,
                                 "current_edges": current_edge_count, "fresh_edges": fresh_edge_count})
                if args.verbose:
                    print(f"  SKIP {slug}: {skip_reason}")
                scope_a_skip += 1
                continue

            # Slug-regression guard
            node_slug = slug.removesuffix(".node")

            # Surgical edge replacement
            infobox_found = bool(infobox_rec.get("relationships") is not None)
            new_edges = render_edges_section(relationships, infobox_found=True)
            new_content = replace_edges_section(content, new_edges)

            # Update prompt_version to v1-python in frontmatter
            new_content = re.sub(
                r'^prompt_version: v1\s*$', 'prompt_version: v1-python',
                new_content, flags=re.MULTILINE, count=1
            )

            if new_content == content:
                outcome = "no_change"
                scope_a_no_change += 1
            else:
                outcome = "would_replace_edges"
                if args.apply:
                    atomic_write(node_path, new_content.encode("utf-8"))
                    outcome = "edges_replaced"
                scope_a_ok += 1

            results.append({
                "scope": "A", "slug": slug, "page": page_name,
                "current_edges": current_edge_count, "fresh_edges": fresh_edge_count,
                "edge_diff": edge_diff, "outcome": outcome,
            })
            if args.verbose:
                print(f"  [A] {slug}: {outcome} (curr={current_edge_count} fresh={fresh_edge_count})")

        print(f"  Processed: {scope_a_ok} ok, {scope_a_skip} skipped, "
              f"{scope_a_err} errors, {scope_a_no_change} no-change")
        print()

        # Write skip log
        if skipped and (args.apply or True):  # always write for audit trail
            SKIP_LOG.parent.mkdir(parents=True, exist_ok=True)
            with SKIP_LOG.open("w", encoding="utf-8") as f:
                for rec in skipped:
                    f.write(json.dumps(rec) + "\n")
            print(f"  Skip log: {SKIP_LOG} ({len(skipped)} entries)")
            print()

    # ==========================================================================
    # Scope B: Religion-bleed locations — full re-emission
    # ==========================================================================
    if run_b:
        print("--- Scope B: Religion-bleed locations (full re-emission) ---")
        scope_b_ok = 0
        scope_b_err = 0

        for slug in RELIGION_BLEED_SLUGS:
            # Find node across multiple dirs
            node_path = None
            current_dir = None
            for type_dir_name in ["locations", "factions", "houses", "concepts"]:
                candidate = GRAPH_NODES_DIR / type_dir_name / f"{slug}.node.md"
                if candidate.exists():
                    node_path = candidate
                    current_dir = type_dir_name
                    break

            if node_path is None:
                errors.append({"scope": "B", "slug": slug, "error": "node not found in graph"})
                scope_b_err += 1
                if args.verbose:
                    print(f"  [B] {slug}: NOT FOUND")
                continue

            content = node_path.read_text(encoding="utf-8")

            # Get page name
            name_match = re.search(r'^name:\s*"?([^"\n]+)"?\s*$', content, re.MULTILINE)
            if not name_match:
                errors.append({"scope": "B", "slug": slug, "error": "no name in frontmatter"})
                scope_b_err += 1
                continue
            page_name = name_match.group(1)

            infobox_rec = infobox_data.get(page_name)
            if infobox_rec is None:
                errors.append({"scope": "B", "slug": slug, "error": f"'{page_name}' not in infobox-data"})
                scope_b_err += 1
                continue

            bucket_id = page_to_bucket.get(page_name, "unknown")
            confidence = bucket_confidence.get(bucket_id, "tier-1")

            aliases = infobox_rec.get("aliases") or []
            relationships = infobox_rec.get("relationships") or []
            entity_type = infobox_rec.get("entity_type") or "place.location"

            # Determine correct target directory
            target_dir_name = resolve_type_dir(entity_type) or current_dir
            dest_path = GRAPH_NODES_DIR / target_dir_name / f"{slug}.node.md"

            # Slug-regression guard
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

            current_edges = count_edges(content)
            fresh_edges = len(relationships)

            outcome = "would_overwrite"
            if args.apply:
                # If directory changed, delete old file and write to new dir
                if dest_path != node_path:
                    atomic_write(dest_path, final_bytes)
                    node_path.unlink()
                    outcome = "moved+overwritten"
                else:
                    atomic_write(dest_path, final_bytes)
                    outcome = "overwritten"

            results.append({
                "scope": "B", "slug": slug, "page": page_name,
                "type": entity_type, "dir": target_dir_name,
                "current_edges": current_edges, "fresh_edges": fresh_edges,
                "outcome": outcome,
            })
            if args.verbose:
                print(f"  [B] {slug}: {outcome} (type={entity_type}, {current_edges}->{fresh_edges} edges)")
            scope_b_ok += 1

        print(f"  Processed: {scope_b_ok} ok, {scope_b_err} errors")
        print()

    # --- Slug-regression check ---
    print("--- Slug-regression check ---")
    import subprocess
    reg_result = subprocess.run(
        ["grep", "-r", "--include=*.md", "-l", r"^slug: .*\.node$",
         str(GRAPH_NODES_DIR)],
        capture_output=True, text=True
    )
    if reg_result.stdout.strip():
        print(f"  WARNING: Slug regression found in:\n{reg_result.stdout.strip()}")
    else:
        print("  OK: No slug regressions found.")
    print()

    # --- Summary ---
    print("=" * 60)
    total_ok = sum(1 for r in results if "would_overwrite" in r.get("outcome", "")
                   or "edges_replaced" in r.get("outcome", "")
                   or "overwritten" in r.get("outcome", ""))
    total_skip = len(skipped)
    total_err = len(errors)

    if run_a:
        a_ok = sum(1 for r in results if r["scope"] == "A" and
                   ("edges_replaced" in r["outcome"] or "would_replace" in r["outcome"]))
        a_no_change = sum(1 for r in results if r["scope"] == "A" and r["outcome"] == "no_change")
        print(f"Scope A (houses):  {a_ok} edges-replaced, {a_no_change} no-change, "
              f"{total_skip} skipped (logged), {sum(1 for e in errors if e['scope']=='A')} errors")

    if run_b:
        b_ok = sum(1 for r in results if r["scope"] == "B" and
                   ("overwritten" in r["outcome"] or "would_overwrite" in r["outcome"]))
        print(f"Scope B (locations): {b_ok} processed, "
              f"{sum(1 for e in errors if e.get('scope')=='B')} errors")

    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  [{e.get('scope','?')}] {e.get('slug','?')}: {e.get('error','?')}")

    # Write summary JSON
    summary = {
        "run_at": __import__("datetime").datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": mode,
        "scope_a": run_a,
        "scope_b": run_b,
        "results": results,
        "skipped": skipped,
        "errors": errors,
    }
    SUMMARY_LOG.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY_LOG.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary log: {SUMMARY_LOG}")

    if not args.apply:
        print("\nDry-run complete. Run with --apply to write files.")
    print("=" * 60)


if __name__ == "__main__":
    main()
