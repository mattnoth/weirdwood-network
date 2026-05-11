#!/usr/bin/env python3
"""Stage 3a: Deterministic skeleton node emitter for Wiki Pass 2.

Reads every secondary-tier bucket manifest, extracts Tier A and Tier B pages
(skips Tier C entirely), and emits a skeleton .node.md file for each page into
working/wiki/pass2-buckets/<bucket_id>/skeleton/<slug>.node.md.

The `skeleton/` directory is the immutable Python record of what the parser
produced. `tmp/` is reserved for the agent's working augmentation in Stage 3b
(Tier A) and the launcher's pre-promotion staging copy (Tier B). The validator
diffs `tmp/` against `skeleton/` on Python-owned frontmatter fields and the
`## Edges` section to enforce that the agent does not silently mutate
deterministic data.

Node content is derived entirely from:
  - working/wiki/data/infobox-data.jsonl  (entity_type, aliases, relationships)
  - working/wiki/data/page-index.jsonl    (entity_type_guess fallback)
  - Per-bucket manifest.json                (tier_default, bucket_id)

No agent involvement. No HTTP calls. No writes outside tmp/ directories.

Edge vocabulary lock
--------------------
Every edge emitted in `## Edges` sections is a verbatim pass-through of what
`scripts/wiki-infobox-parser.py` produced in `infobox-data.jsonl` under the
`relationships[].edge_type` field. This script does NOT translate, rename,
merge, or invent edge types. The vocabulary is locked at the parser level
(its `FIELD_EDGE_MAP` dict). See `reference/architecture.md` § "Wiki Infobox
Fields → Edge Type Mapping" for the canonical table and the rationale for
keeping it locked. The future "edge polish" phase (post-ingestion) is where
semantically-equivalent variants get merged by agent reasoning — never here.

Usage:
  python3 scripts/wiki-pass2-emit-deterministic.py             # dry-run
  python3 scripts/wiki-pass2-emit-deterministic.py --apply     # write files
  python3 scripts/wiki-pass2-emit-deterministic.py --bucket houses-other-h-w
  python3 scripts/wiki-pass2-emit-deterministic.py --bucket houses-other-h-w --apply
  python3 scripts/wiki-pass2-emit-deterministic.py -v          # verbose per-bucket
  python3 scripts/wiki-pass2-emit-deterministic.py --tier-a-only --apply
  python3 scripts/wiki-pass2-emit-deterministic.py --tier-b-only --apply
"""

import argparse
import json
import re
import sys
import urllib.parse
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
INFOBOX_DATA_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "infobox-data.jsonl"
PAGE_INDEX_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "page-index.jsonl"
WIKI_PASS2_DIR = PROJECT_ROOT / "working" / "wiki" / "pass2-buckets"
STAGE3A_SUMMARY_FILE = PROJECT_ROOT / "working" / "wiki" / "pass2-staging" / "stage3a-emission-summary.json"

# Core bucket patterns — these are already processed and must be skipped
_SPLIT_SUFFIX = r"(-[a-z]([0-9]+)?(-[a-z]([0-9]+)?)?)?$"
CORE_TIER_PATTERNS = [
    re.compile(r"^direwolves" + _SPLIT_SUFFIX),
    re.compile(r"^characters-house-(stark|lannister|targaryen|baratheon|"
               r"greyjoy|tully|arryn|tyrell|martell)" + _SPLIT_SUFFIX),
    re.compile(r"^houses-(north|westerlands|crownlands|riverlands|vale|"
               r"reach|stormlands|dorne|iron-islands)" + _SPLIT_SUFFIX),
    re.compile(r"^(north|westerlands|crownlands|riverlands|vale|reach|"
               r"stormlands|dorne|iron-islands)-locations" + _SPLIT_SUFFIX),
]


def is_core_bucket(bucket_id: str) -> bool:
    """Return True if this bucket is a core (Stage 1) bucket that should be skipped."""
    for pat in CORE_TIER_PATTERNS:
        if pat.match(bucket_id):
            return True
    return False


# ---------------------------------------------------------------------------
# Slug generation — must match wiki-pass2-triage.py exactly
# ---------------------------------------------------------------------------

def page_to_slug(page_name: str) -> str:
    """Convert a wiki page name to a filesystem slug.

    Matches the convention in wiki-pass2-triage.py::page_to_slug:
    - Lowercase
    - Strip punctuation that merges words (apostrophes, quotes, commas)
    - Replace spaces/underscores with hyphens
    - Replace remaining non-alphanumeric chars with hyphens
    - Collapse consecutive hyphens, strip leading/trailing hyphens
    """
    slug = page_name.lower()
    slug = re.sub(r"['\",]", "", slug)
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


# ---------------------------------------------------------------------------
# Load infobox-data.jsonl and page-index.jsonl into lookup dicts
# ---------------------------------------------------------------------------

def load_infobox_data() -> dict[str, dict]:
    """Return {page_name: record} from infobox-data.jsonl."""
    data: dict[str, dict] = {}
    with open(INFOBOX_DATA_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            data[rec["page"]] = rec
    return data


def load_page_index() -> dict[str, dict]:
    """Return {page_name: record} from page-index.jsonl."""
    data: dict[str, dict] = {}
    with open(PAGE_INDEX_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            data[rec["page"]] = rec
    return data


# ---------------------------------------------------------------------------
# Node rendering
# ---------------------------------------------------------------------------

def wiki_url(page_name: str) -> str:
    """Produce the canonical AWOIAF URL for a page name."""
    # Replace spaces with underscores for the URL (wiki convention)
    encoded = urllib.parse.quote(page_name.replace(" ", "_"), safe="/:@!$&'()*+,;=")
    return f"https://awoiaf.westeros.org/index.php/{encoded}"


def render_edge_line(rel: dict) -> str:
    """Render one relationship dict into an edge bullet line.

    Forward:  - EDGE_TYPE: Target (track_b: FieldName)
    Reverse:  - EDGE_TYPE (reverse): Target (track_b: FieldName)
    Qualifier appended as bracketed note when present.
    """
    edge_type = rel.get("edge_type", "UNKNOWN_EDGE")
    target = rel.get("target", "")
    field = rel.get("field", "")
    direction = rel.get("direction", "forward")
    qualifier = rel.get("qualifier", "")

    if direction == "reverse":
        edge_label = f"{edge_type} (reverse)"
    else:
        edge_label = edge_type

    line = f"- {edge_label}: {target} (track_b: {field})"
    if qualifier:
        line += f" [{qualifier}]"
    return line


def render_node(
    page_name: str,
    slug: str,
    entity_type: str,
    aliases: list,
    confidence: str,
    bucket_id: str,
    relationships: list,
    infobox_found: bool,
) -> str:
    """Render a complete skeleton node markdown string."""
    url = wiki_url(page_name)

    # Aliases: YAML inline list
    if aliases:
        alias_items = ", ".join(f'"{a}"' for a in aliases)
        aliases_yaml = f"[{alias_items}]"
    else:
        aliases_yaml = "[]"

    # Frontmatter
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
    # If no relationships (or no infobox), section is intentionally empty

    # Ensure file ends with a newline
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Per-bucket processing
# ---------------------------------------------------------------------------

def process_bucket(
    manifest_path: Path,
    infobox_data: dict[str, dict],
    page_index: dict[str, dict],
    apply: bool,
    tier_a_only: bool,
    tier_b_only: bool,
    verbose: bool,
) -> dict:
    """Process one secondary bucket. Returns stats dict.

    Stats keys:
      bucket_id, tier_a_pages, tier_b_pages, emitted, skipped_tier_c,
      no_infobox_count, total_edges, pages_emitted (list of dicts)
    """
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"  ERROR reading {manifest_path}: {e}", file=sys.stderr)
        return {"bucket_id": str(manifest_path.parent.name), "error": str(e)}

    bucket_id = manifest["bucket_id"]
    confidence = manifest.get("tier_default") or "tier-2"

    # Extract priority tiers
    priority = manifest.get("priority", {})
    tier_a_pages: list[str] = priority.get("tier_a", [])
    tier_b_pages: list[str] = priority.get("tier_b", [])

    # Apply tier filters
    if tier_a_only:
        pages_to_emit = [(p, "A") for p in tier_a_pages]
    elif tier_b_only:
        pages_to_emit = [(p, "B") for p in tier_b_pages]
    else:
        pages_to_emit = [(p, "A") for p in tier_a_pages] + [(p, "B") for p in tier_b_pages]

    stats = {
        "bucket_id": bucket_id,
        "tier_a_count": len(tier_a_pages),
        "tier_b_count": len(tier_b_pages),
        "emitted": 0,
        "no_infobox_count": 0,
        "total_edges": 0,
        "type_counts": Counter(),
        "field_counts": Counter(),
        "pages_emitted": [],
    }

    if not pages_to_emit:
        if verbose:
            print(f"  {bucket_id}: no Tier A/B pages to emit")
        return stats

    # Slug uniqueness check within this bucket
    slug_to_page: dict[str, str] = {}

    skeleton_dir = manifest_path.parent / "skeleton"
    if apply:
        skeleton_dir.mkdir(parents=True, exist_ok=True)

    for page_name, tier in pages_to_emit:
        slug = page_to_slug(page_name)

        # Assert slug uniqueness within bucket
        if slug in slug_to_page:
            print(
                f"  ERROR: slug collision in {bucket_id}: "
                f"'{slug}' maps to both '{slug_to_page[slug]}' and '{page_name}'",
                file=sys.stderr,
            )
            print(
                f"  Aborting bucket {bucket_id} — slug uniqueness violated.",
                file=sys.stderr,
            )
            stats["error"] = f"slug_collision: {slug}"
            return stats
        slug_to_page[slug] = page_name

        # Look up infobox record
        infobox_rec = infobox_data.get(page_name)
        page_idx_rec = page_index.get(page_name)

        # Determine entity_type
        if infobox_rec and infobox_rec.get("entity_type"):
            entity_type = infobox_rec["entity_type"]
        elif page_idx_rec and page_idx_rec.get("entity_type_guess"):
            entity_type = page_idx_rec["entity_type_guess"]
        else:
            entity_type = "unknown"

        # Aliases
        aliases: list[str] = []
        if infobox_rec and infobox_rec.get("aliases"):
            aliases = infobox_rec["aliases"]

        # Relationships
        relationships: list[dict] = []
        infobox_found = infobox_rec is not None
        if infobox_rec and infobox_rec.get("relationships"):
            relationships = infobox_rec["relationships"]

        if not infobox_found:
            stats["no_infobox_count"] += 1

        stats["total_edges"] += len(relationships)
        stats["type_counts"][entity_type] += 1
        for rel in relationships:
            stats["field_counts"][rel.get("field", "")] += 1

        # Render node content
        node_content = render_node(
            page_name=page_name,
            slug=slug,
            entity_type=entity_type,
            aliases=aliases,
            confidence=confidence,
            bucket_id=bucket_id,
            relationships=relationships,
            infobox_found=infobox_found,
        )

        out_path = skeleton_dir / f"{slug}.node.md"

        if apply:
            out_path.write_text(node_content, encoding="utf-8")

        stats["emitted"] += 1
        stats["pages_emitted"].append({
            "page": page_name,
            "tier": tier,
            "slug": slug,
            "entity_type": entity_type,
            "infobox_found": infobox_found,
            "edge_count": len(relationships),
            "path": str(out_path),
        })

        if verbose:
            infobox_tag = "infobox" if infobox_found else "NO-INFOBOX"
            print(
                f"    [{tier}] {page_name!r:50s} → {slug}.node.md "
                f"({infobox_tag}, {len(relationships)} edges, type={entity_type})"
            )

    return stats


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
        help="Write skeleton nodes to tmp/ directories. Without --apply, prints stats only.",
    )
    parser.add_argument(
        "--bucket",
        metavar="BUCKET_ID",
        default=None,
        help="Process a single bucket only (by bucket_id).",
    )
    parser.add_argument(
        "--tier-a-only",
        action="store_true",
        default=False,
        help="Emit only Tier A pages (skip Tier B).",
    )
    parser.add_argument(
        "--tier-b-only",
        action="store_true",
        default=False,
        help="Emit only Tier B pages (skip Tier A).",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Print per-page stats within each bucket.",
    )
    args = parser.parse_args()

    if args.tier_a_only and args.tier_b_only:
        print("ERROR: --tier-a-only and --tier-b-only are mutually exclusive.", file=sys.stderr)
        sys.exit(1)

    # Load reference data
    print("Loading infobox-data.jsonl...")
    infobox_data = load_infobox_data()
    print(f"  {len(infobox_data):,} infobox records loaded")

    print("Loading page-index.jsonl...")
    page_index = load_page_index()
    print(f"  {len(page_index):,} page-index records loaded")

    # Discover bucket manifests
    if args.bucket:
        bucket_dir = WIKI_PASS2_DIR / args.bucket
        manifest_path = bucket_dir / "manifest.json"
        if not manifest_path.exists():
            print(f"ERROR: No manifest found at {manifest_path}", file=sys.stderr)
            sys.exit(1)
        manifest_paths = [manifest_path]
    else:
        manifest_paths = sorted(WIKI_PASS2_DIR.glob("*/manifest.json"))

    # Filter to secondary buckets only (skip core, which are already done)
    secondary_manifests: list[Path] = []
    skipped_core = 0
    for mpath in manifest_paths:
        bucket_id = mpath.parent.name
        try:
            manifest = json.loads(mpath.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if manifest.get("tier") == "core" or is_core_bucket(bucket_id):
            skipped_core += 1
            continue
        secondary_manifests.append(mpath)

    tier_label = ""
    if args.tier_a_only:
        tier_label = " (Tier A only)"
    elif args.tier_b_only:
        tier_label = " (Tier B only)"

    mode_label = "APPLY" if args.apply else "DRY-RUN"
    print(f"\n=== Stage 3a deterministic emission [{mode_label}]{tier_label} ===")
    print(f"Secondary buckets found: {len(secondary_manifests)}")
    if skipped_core and not args.bucket:
        print(f"Core buckets skipped:    {skipped_core}")

    # Process all secondary buckets
    all_stats: list[dict] = []
    total_errors = 0

    for mpath in secondary_manifests:
        bucket_id = mpath.parent.name
        if args.verbose:
            print(f"\n  Bucket: {bucket_id}")

        stats = process_bucket(
            manifest_path=mpath,
            infobox_data=infobox_data,
            page_index=page_index,
            apply=args.apply,
            tier_a_only=args.tier_a_only,
            tier_b_only=args.tier_b_only,
            verbose=args.verbose,
        )

        if "error" in stats and "slug_collision" in stats.get("error", ""):
            total_errors += 1

        all_stats.append(stats)

    # Aggregate stats
    total_buckets = len(all_stats)
    total_emitted = sum(s.get("emitted", 0) for s in all_stats)
    total_tier_a = sum(s.get("tier_a_count", 0) for s in all_stats)
    total_tier_b = sum(s.get("tier_b_count", 0) for s in all_stats)
    total_no_infobox = sum(s.get("no_infobox_count", 0) for s in all_stats)
    total_edges_all = sum(s.get("total_edges", 0) for s in all_stats)

    # Tier A / B emitted counts
    tier_a_emitted = 0
    tier_b_emitted = 0
    for s in all_stats:
        for p in s.get("pages_emitted", []):
            if p["tier"] == "A":
                tier_a_emitted += 1
            else:
                tier_b_emitted += 1

    mean_edges = total_edges_all / total_emitted if total_emitted else 0.0

    # Aggregate type counts
    type_dist: Counter = Counter()
    field_dist: Counter = Counter()
    for s in all_stats:
        type_dist.update(s.get("type_counts", {}))
        field_dist.update(s.get("field_counts", {}))

    # No-infobox sample (pages where infobox was missing)
    no_infobox_sample: list[str] = []
    for s in all_stats:
        for p in s.get("pages_emitted", []):
            if not p["infobox_found"]:
                no_infobox_sample.append(p["page"])
                if len(no_infobox_sample) >= 10:
                    break
        if len(no_infobox_sample) >= 10:
            break

    # Print summary
    print()
    print(f"Buckets processed:    {total_buckets}")
    print(f"Skeletons emitted:    {total_emitted} total (A={tier_a_emitted}, B={tier_b_emitted})")
    print(f"Tier A total (across buckets): {total_tier_a}")
    print(f"Tier B total (across buckets): {total_tier_b}")
    print(f"Tier B without infobox (empty edges section): {total_no_infobox}")
    print(f"Pages with no infobox match: {total_no_infobox}")
    if no_infobox_sample:
        print("  Sample (up to 10):")
        for pg in no_infobox_sample:
            print(f"    - {pg}")
    print(f"Mean edges/skeleton:  {mean_edges:.2f}")
    print()
    print("Type-guess distribution (top 15):")
    for type_name, count in type_dist.most_common(15):
        print(f"  {type_name:<40s} {count:>6,}")
    print()
    print("Top 10 fields by edge count:")
    for field_name, count in field_dist.most_common(10):
        print(f"  {field_name:<30s} {count:>6,}")

    if total_errors:
        print(f"\nWARNING: {total_errors} bucket(s) had slug collision errors.")

    print("=" * 50)

    # Write summary JSON on --apply runs
    if args.apply and not args.bucket:
        per_bucket = []
        for s in all_stats:
            per_bucket.append({
                "bucket_id": s.get("bucket_id", "?"),
                "tier_a_count": s.get("tier_a_count", 0),
                "tier_b_count": s.get("tier_b_count", 0),
                "emitted": s.get("emitted", 0),
                "no_infobox_count": s.get("no_infobox_count", 0),
                "total_edges": s.get("total_edges", 0),
            })

        summary = {
            "buckets_processed": total_buckets,
            "skeletons_emitted": total_emitted,
            "tier_a_emitted": tier_a_emitted,
            "tier_b_emitted": tier_b_emitted,
            "tier_b_without_infobox": total_no_infobox,
            "mean_edges_per_skeleton": round(mean_edges, 4),
            "type_distribution": dict(type_dist.most_common()),
            "top_fields_by_edge_count": field_dist.most_common(20),
            "per_bucket": per_bucket,
        }
        STAGE3A_SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
        STAGE3A_SUMMARY_FILE.write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"\nSummary written to: {STAGE3A_SUMMARY_FILE}")

    if total_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
