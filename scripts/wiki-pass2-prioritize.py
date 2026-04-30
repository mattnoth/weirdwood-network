#!/usr/bin/env python3
"""Compute priority_tier (A/B/C) for every page in secondary-tier wiki Pass 2 manifests.

This is Stage 3 prep for Wiki Pass 2 — pure metadata labeling, no node emission.
Stage 3a emission (Python deterministic skeletons) happens in a separate later script.

IMPORTANT: The existing wiki-pass2-triage.py uses a field called `tier_default` with
values `tier-1` through `tier-4`. That is a CONFIDENCE tier (canon-quality grade),
NOT the axis this script computes. This script computes a separate 3-value PRIORITY
tier (A/B/C) stored in the field `priority_tier`. Both fields live side-by-side in
each manifest. The field name `tier` is never used here as a variable to avoid confusion.

Priority tier definitions
--------------------------
A  Page name appears in any AGOT Pass 1 raw entity list OR sum of cite_ref_books >= 5
B  Has infobox in infobox-data.jsonl but does NOT meet Tier A criteria
C  No infobox AND cite_ref_books sum is 0

Page-kind labels (Tier C only, first match wins)
-------------------------------------------------
1. redirect        - HTML contains class="redirectMsg" or class="redirectText"
2. disambiguation  - HTML contains "may refer to:" within 500 chars of a <ul>
3. list_article    - page name starts with "List of "
4. year_article    - page name matches \\d+ AC / \\d+ BC / Year \\d+
5. stub            - byte_size < 500 AND has_infobox False AND none above
6. entity          - fallback

Inputs
------
- working/wiki-parsed/page-index.jsonl       (17,657 rows)
- working/wiki-parsed/infobox-data.jsonl     (5,279 rows)
- extractions/mechanical/agot/*.extraction.md (73 files)
- sources/wiki/_raw/<Page_Name>.json          (Tier C redirect detection only)
- working/wiki-pass2/*/manifest.json          (only secondary-tier manifests modified)

Outputs (--apply only)
-------
- Writes `priority` field into each secondary manifest (additive, no existing fields touched)
- Writes working/wiki-parsed/priority-summary.json

Usage
-----
  python3 scripts/wiki-pass2-prioritize.py             # dry-run
  python3 scripts/wiki-pass2-prioritize.py --apply     # write manifests + summary
  python3 scripts/wiki-pass2-prioritize.py --reapply   # alias for --apply (idempotent)
  python3 scripts/wiki-pass2-prioritize.py --bucket battles-a          # dry-run one bucket
  python3 scripts/wiki-pass2-prioritize.py --bucket battles-a --apply  # apply one bucket
  python3 scripts/wiki-pass2-prioritize.py -v          # verbose per-bucket stats
"""

import argparse
import json
import re
import sys
import urllib.parse
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

PAGE_INDEX_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "page-index.jsonl"
INFOBOX_DATA_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "infobox-data.jsonl"
AGOT_EXTRACTIONS_DIR = PROJECT_ROOT / "extractions" / "mechanical" / "agot"
WIKI_RAW_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
WIKI_PASS2_DIR = PROJECT_ROOT / "working" / "wiki-pass2"
PRIORITY_SUMMARY_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "priority-summary.json"

# Threshold for cite_ref_books sum to qualify for Tier A
CITE_REF_THRESHOLD = 5

# Threshold for stub detection (byte_size)
STUB_BYTE_THRESHOLD = 500

# Year article patterns
YEAR_AC_RE = re.compile(r"^\d+ AC$")
YEAR_BC_RE = re.compile(r"^\d+ BC$")
YEAR_WORD_RE = re.compile(r"^Year \d+$")


# ---------------------------------------------------------------------------
# Pass 1 entity set — build once at startup
# ---------------------------------------------------------------------------

def _normalize_entity_name(raw: str) -> str:
    """Normalize a Pass 1 bullet item to a comparable lowercase string.

    Steps:
    1. Strip leading '- ' and trailing whitespace.
    2. Strip everything from first '(' onward.
    3. Strip leading article: 'The ' or 'the ' -> ''.
    4. Lowercase.
    5. Trim whitespace.
    """
    name = raw.strip()
    # Strip bullet marker
    if name.startswith("- "):
        name = name[2:]
    name = name.strip()
    # Strip parenthetical suffix
    paren_idx = name.find("(")
    if paren_idx >= 0:
        name = name[:paren_idx]
    name = name.strip()
    # Strip leading article
    name = re.sub(r"^[Tt]he\s+", "", name)
    # Lowercase and trim
    return name.lower().strip()


def load_pass1_entity_set(verbose: bool = False) -> set:
    """Parse all AGOT extraction files and return a normalized set of entity names."""
    entity_set: set[str] = set()
    extraction_files = sorted(AGOT_EXTRACTIONS_DIR.glob("*.extraction.md"))
    if not extraction_files:
        print(
            f"WARNING: No extraction files found at {AGOT_EXTRACTIONS_DIR}",
            file=sys.stderr,
        )
        return entity_set

    for ef in extraction_files:
        try:
            text = ef.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"WARNING: Cannot read {ef}: {exc}", file=sys.stderr)
            continue

        # Find ## Raw Entity List section
        section_match = re.search(r"## Raw Entity List\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
        if not section_match:
            continue

        section_text = section_match.group(1)
        # Collect all bullet items (lines starting with '- ')
        for line in section_text.splitlines():
            line = line.strip()
            if not line.startswith("- "):
                continue
            normalized = _normalize_entity_name(line)
            if normalized and normalized != "none":
                entity_set.add(normalized)

    if verbose:
        print(f"  Pass 1 entity set: {len(entity_set):,} normalized names from {len(extraction_files)} files")
    return entity_set


def page_in_pass1(page_name: str, pass1_set: set) -> bool:
    """Return True if the wiki page name normalizes to something in the Pass 1 set."""
    normalized = _normalize_entity_name(page_name)
    return bool(normalized) and normalized in pass1_set


# ---------------------------------------------------------------------------
# Load page-index.jsonl
# ---------------------------------------------------------------------------

def load_page_index(verbose: bool = False) -> dict:
    """Return {page_name: record} from page-index.jsonl."""
    index: dict[str, dict] = {}
    with open(PAGE_INDEX_FILE, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            index[rec["page"]] = rec
    if verbose:
        print(f"  page-index.jsonl: {len(index):,} records")
    return index


# ---------------------------------------------------------------------------
# Load infobox-data.jsonl
# ---------------------------------------------------------------------------

def load_infobox_set(verbose: bool = False) -> set:
    """Return a set of page names that appear in infobox-data.jsonl."""
    pages: set[str] = set()
    with open(INFOBOX_DATA_FILE, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            pages.add(rec["page"])
    if verbose:
        print(f"  infobox-data.jsonl: {len(pages):,} pages with infoboxes")
    return pages


# ---------------------------------------------------------------------------
# Tier C page-kind detection
# ---------------------------------------------------------------------------

def _load_raw_html(page_name: str) -> str | None:
    """Load body HTML for a wiki page from the local cache.

    Filename mapping: 'Foo Bar' -> 'Foo_Bar.json'. Falls back to None if not found.
    """
    fname = page_name.replace(" ", "_") + ".json"
    fpath = WIKI_RAW_DIR / fname
    if not fpath.exists():
        return None
    try:
        data = json.loads(fpath.read_text(encoding="utf-8"))
        return data.get("html") or ""
    except (OSError, json.JSONDecodeError) as exc:
        print(f"WARNING: Cannot read raw HTML for {page_name!r}: {exc}", file=sys.stderr)
        return None


def _extract_redirect_target(html: str) -> str | None:
    """Extract redirect target from redirectText block.

    Looks for: <a href="/index.php/<TARGET>" ...>
    inside the redirectText block. Returns the decoded page name (underscores -> spaces)
    or None if extraction fails.
    """
    # Find the redirectText block
    rt_match = re.search(
        r'class="redirectText"[^>]*>.*?<a href="/index\.php/([^"?#]+)"',
        html,
        re.DOTALL,
    )
    if not rt_match:
        return None
    raw_target = rt_match.group(1)
    # URL-decode and convert underscores to spaces
    decoded = urllib.parse.unquote(raw_target).replace("_", " ")
    return decoded if decoded else None


def detect_page_kind(page_name: str, byte_size: int) -> tuple[str, str | None]:
    """Determine Tier C page_kind. Returns (kind, redirect_target_or_None).

    Order: redirect -> disambiguation -> list_article -> year_article -> stub -> entity
    Only reads raw HTML for redirect/disambiguation checks (expensive I/O).
    """
    # 1. list_article — cheap check first (no I/O needed)
    if page_name.startswith("List of "):
        return "list_article", None

    # 2. year_article — cheap check (no I/O needed)
    if YEAR_AC_RE.match(page_name) or YEAR_BC_RE.match(page_name) or YEAR_WORD_RE.match(page_name):
        return "year_article", None

    # 3. stub — cheap check (no I/O needed)
    if byte_size < STUB_BYTE_THRESHOLD:
        # Read HTML to rule out redirect (redirect pages are very small too)
        html = _load_raw_html(page_name)
        if html is None:
            # Can't read — assume stub
            return "stub", None
        if 'class="redirectMsg"' in html or 'class="redirectText"' in html:
            target = _extract_redirect_target(html)
            return "redirect", target
        return "stub", None

    # 4. Need HTML for redirect / disambiguation
    html = _load_raw_html(page_name)
    if html is None:
        # Fallback — can't read raw file
        return "entity", None

    # redirect check
    if 'class="redirectMsg"' in html or 'class="redirectText"' in html:
        target = _extract_redirect_target(html)
        return "redirect", target

    # disambiguation check: "may refer to:" within 500 chars of a <ul>
    refer_idx = html.find("may refer to:")
    if refer_idx >= 0:
        window = html[refer_idx: refer_idx + 500]
        if "<ul>" in window:
            return "disambiguation", None

    # entity fallback
    return "entity", None


# ---------------------------------------------------------------------------
# Priority tier assignment for a single page
# ---------------------------------------------------------------------------

def assign_priority_tier(
    page_name: str,
    index_rec: dict | None,
    infobox_pages: set,
    pass1_set: set,
) -> tuple[str, str | None, str | None]:
    """Return (priority_tier, page_kind, redirect_target).

    priority_tier: 'A', 'B', or 'C'
    page_kind: only set for Tier C; None for A/B
    redirect_target: only set for Tier C redirect; None otherwise
    """
    # Compute inputs
    has_infobox = page_name in infobox_pages
    cite_ref_books = (index_rec or {}).get("cite_ref_books") or {}
    cite_ref_sum = sum(cite_ref_books.values()) if isinstance(cite_ref_books, dict) else 0
    byte_size = (index_rec or {}).get("byte_size") or 0

    in_pass1 = page_in_pass1(page_name, pass1_set)

    # Tier A: in Pass 1 OR cite_ref_sum >= threshold
    if in_pass1 or cite_ref_sum >= CITE_REF_THRESHOLD:
        return "A", None, None

    # Tier B: has infobox but didn't meet Tier A
    if has_infobox:
        return "B", None, None

    # Tier C: no infobox and cite_refs == 0
    page_kind, redirect_target = detect_page_kind(page_name, byte_size)
    # Promotion rule (v1, 2026-04-27): real-content pages that fall through to
    # the entity catch-all are too valuable to defer. Promote to Tier B so they
    # get a Stage 3a Python skeleton (frontmatter + Identity one-liner only;
    # Edges section will be empty since they have no infobox to mine).
    if page_kind == "entity":
        return "B", None, None
    return "C", page_kind, redirect_target


# ---------------------------------------------------------------------------
# Process a single bucket
# ---------------------------------------------------------------------------

def process_bucket(
    manifest_path: Path,
    page_index: dict,
    infobox_pages: set,
    pass1_set: set,
    verbose: bool = False,
) -> dict | None:
    """Compute priority labels for all pages in a secondary-tier manifest.

    Returns a result dict with keys:
      bucket_id, tier_a, tier_b, tier_c, stats, manifest_path

    Returns None if the manifest is not secondary-tier or has no input_pages.
    """
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"WARNING: Cannot read {manifest_path}: {exc}", file=sys.stderr)
        return None

    # Skip core buckets
    if manifest.get("tier") != "secondary":
        return None

    input_pages: list[str] = manifest.get("input_pages") or []
    if not input_pages:
        print(f"WARNING: {manifest_path} has no input_pages — skipping", file=sys.stderr)
        return None

    bucket_id = manifest.get("bucket_id", manifest_path.parent.name)

    tier_a: list[str] = []
    tier_b: list[str] = []
    tier_c: list[dict] = []

    for page_name in input_pages:
        index_rec = page_index.get(page_name)
        priority_tier, page_kind, redirect_target = assign_priority_tier(
            page_name, index_rec, infobox_pages, pass1_set
        )

        if priority_tier == "A":
            tier_a.append(page_name)
        elif priority_tier == "B":
            tier_b.append(page_name)
        else:  # C
            entry: dict = {"page": page_name, "page_kind": page_kind or "entity"}
            if redirect_target is not None:
                entry["redirect_target"] = redirect_target
            tier_c.append(entry)

    # Invariant: all pages accounted for exactly once
    total_classified = len(tier_a) + len(tier_b) + len(tier_c)
    if total_classified != len(input_pages):
        print(
            f"ERROR: Invariant violated in bucket {bucket_id!r}: "
            f"{total_classified} classified != {len(input_pages)} input_pages — skipping",
            file=sys.stderr,
        )
        return None

    result = {
        "bucket_id": bucket_id,
        "manifest_path": manifest_path,
        "manifest": manifest,
        "tier_a": tier_a,
        "tier_b": tier_b,
        "tier_c": tier_c,
        "stats": {
            "total": len(input_pages),
            "tier_a": len(tier_a),
            "tier_b": len(tier_b),
            "tier_c": len(tier_c),
        },
    }

    if verbose:
        print(
            f"  {bucket_id:<55s} "
            f"A={len(tier_a):>3}  B={len(tier_b):>3}  C={len(tier_c):>4}  "
            f"total={len(input_pages):>4}"
        )

    return result


# ---------------------------------------------------------------------------
# Write priority field back into a manifest
# ---------------------------------------------------------------------------

def write_priority_to_manifest(result: dict) -> None:
    """Write the priority field into the manifest JSON, preserving all existing fields."""
    manifest = result["manifest"]
    manifest_path = result["manifest_path"]

    computed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    priority_block = {
        "version": "v1",
        "computed_at": computed_at,
        "tier_a": result["tier_a"],
        "tier_b": result["tier_b"],
        "tier_c": result["tier_c"],
        "stats": result["stats"],
    }

    # Additive — do not remove or overwrite existing fields
    manifest["priority"] = priority_block

    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Global summary
# ---------------------------------------------------------------------------

def build_summary(
    results: list[dict],
    computed_at: str,
) -> dict:
    """Build the global priority-summary.json structure."""
    totals_a = 0
    totals_b = 0
    totals_c = 0
    c_by_kind: dict[str, int] = {
        "redirect": 0,
        "disambiguation": 0,
        "list_article": 0,
        "year_article": 0,
        "stub": 0,
        "entity": 0,
    }

    tier_a_samples: list[str] = []
    tier_b_samples: list[str] = []
    tier_c_redirect_samples: list[str] = []
    tier_c_stub_samples: list[str] = []
    tier_c_entity_samples: list[str] = []

    mixed_buckets: list[dict] = []

    for r in results:
        a_count = r["stats"]["tier_a"]
        b_count = r["stats"]["tier_b"]
        c_count = r["stats"]["tier_c"]

        totals_a += a_count
        totals_b += b_count
        totals_c += c_count

        for entry in r["tier_c"]:
            kind = entry.get("page_kind", "entity")
            c_by_kind[kind] = c_by_kind.get(kind, 0) + 1

        # Accumulate samples
        if len(tier_a_samples) < 20:
            tier_a_samples.extend(r["tier_a"][: 20 - len(tier_a_samples)])
        if len(tier_b_samples) < 20:
            tier_b_samples.extend(r["tier_b"][: 20 - len(tier_b_samples)])
        for entry in r["tier_c"]:
            kind = entry.get("page_kind", "entity")
            if kind == "redirect" and len(tier_c_redirect_samples) < 10:
                tier_c_redirect_samples.append(entry["page"])
            elif kind == "stub" and len(tier_c_stub_samples) < 10:
                tier_c_stub_samples.append(entry["page"])
            elif kind == "entity" and len(tier_c_entity_samples) < 10:
                tier_c_entity_samples.append(entry["page"])

        # Mixed buckets: all three tiers non-empty
        if a_count > 0 and b_count > 0 and c_count > 0:
            mixed_buckets.append({
                "bucket_id": r["bucket_id"],
                "a": a_count,
                "b": b_count,
                "c": c_count,
            })

    return {
        "version": "v1",
        "computed_at": computed_at,
        "buckets_processed": len(results),
        "totals": {
            "tier_a": totals_a,
            "tier_b": totals_b,
            "tier_c_total": totals_c,
            "tier_c_by_kind": c_by_kind,
        },
        "samples": {
            "tier_a_first_20": tier_a_samples[:20],
            "tier_b_first_20": tier_b_samples[:20],
            "tier_c_redirect_first_10": tier_c_redirect_samples[:10],
            "tier_c_stub_first_10": tier_c_stub_samples[:10],
            "tier_c_entity_first_10": tier_c_entity_samples[:10],
        },
        "buckets_with_mixed_tiers": sorted(
            mixed_buckets, key=lambda x: x["bucket_id"]
        ),
    }


def print_summary(summary: dict, apply_mode: bool) -> None:
    """Print human-readable summary to stdout."""
    mode_label = "APPLY" if apply_mode else "DRY RUN"
    t = summary["totals"]
    ck = t["tier_c_by_kind"]

    print()
    print("=" * 66)
    print(f"  wiki-pass2-prioritize.py  [{mode_label}]")
    print("=" * 66)
    print(f"  Buckets processed:  {summary['buckets_processed']:>5,}")
    print(f"  Computed at:        {summary['computed_at']}")
    print()
    print("  Priority tier totals:")
    total_pages = t["tier_a"] + t["tier_b"] + t["tier_c_total"]
    print(f"    Tier A (emit + agent):  {t['tier_a']:>5,}  ({t['tier_a']/max(total_pages,1)*100:.1f}%)")
    print(f"    Tier B (emit only):     {t['tier_b']:>5,}  ({t['tier_b']/max(total_pages,1)*100:.1f}%)")
    print(f"    Tier C (defer):         {t['tier_c_total']:>5,}  ({t['tier_c_total']/max(total_pages,1)*100:.1f}%)")
    print(f"    Total pages:            {total_pages:>5,}")
    print()
    print("  Tier C breakdown by kind:")
    for kind in ("redirect", "disambiguation", "list_article", "year_article", "stub", "entity"):
        n = ck.get(kind, 0)
        print(f"    {kind:<18s}  {n:>5,}")
    print()
    mixed = summary["buckets_with_mixed_tiers"]
    print(f"  Buckets with all three tiers non-empty: {len(mixed)}")
    if mixed:
        for bm in mixed[:10]:
            print(f"    {bm['bucket_id']:<55s}  A={bm['a']}  B={bm['b']}  C={bm['c']}")
        if len(mixed) > 10:
            print(f"    ... and {len(mixed) - 10} more")
    print()
    print("  Sample Tier A pages:")
    for p in summary["samples"]["tier_a_first_20"][:10]:
        print(f"    {p}")
    print()
    print("  Sample Tier B pages:")
    for p in summary["samples"]["tier_b_first_20"][:10]:
        print(f"    {p}")
    print()
    print("  Sample Tier C redirect pages:")
    for p in summary["samples"]["tier_c_redirect_first_10"][:5]:
        print(f"    {p}")
    print()
    print("  Sample Tier C stub pages:")
    for p in summary["samples"]["tier_c_stub_first_10"][:5]:
        print(f"    {p}")
    print()
    print("  Sample Tier C entity pages:")
    for p in summary["samples"]["tier_c_entity_first_10"][:5]:
        print(f"    {p}")
    if apply_mode:
        print()
        print(f"  Manifests updated:  {summary['buckets_processed']:,}")
        print(f"  Summary written:    {PRIORITY_SUMMARY_FILE}")
    else:
        print()
        print("  (DRY RUN — no files written. Re-run with --apply to write.)")
    print("=" * 66)
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help="Write priority field into each secondary manifest and write priority-summary.json",
    )
    parser.add_argument(
        "--reapply",
        action="store_true",
        default=False,
        help="Alias for --apply (intent: idempotent re-run)",
    )
    parser.add_argument(
        "--bucket",
        metavar="BUCKET_ID",
        default=None,
        help="Process only the named bucket (dry-run or --apply for that bucket only)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Print per-bucket stats",
    )
    args = parser.parse_args()

    apply_mode = args.apply or args.reapply

    # --- Load shared data once ---
    print("Loading Pass 1 entity set...")
    pass1_set = load_pass1_entity_set(verbose=args.verbose)
    print(f"  {len(pass1_set):,} normalized entity names")

    print("Loading page-index.jsonl...")
    page_index = load_page_index(verbose=args.verbose)
    print(f"  {len(page_index):,} pages")

    print("Loading infobox-data.jsonl...")
    infobox_pages = load_infobox_set(verbose=args.verbose)
    print(f"  {len(infobox_pages):,} pages with infoboxes")

    # --- Collect manifest paths ---
    if args.bucket:
        bucket_dir = WIKI_PASS2_DIR / args.bucket
        if not bucket_dir.exists():
            print(f"ERROR: Bucket directory not found: {bucket_dir}", file=sys.stderr)
            sys.exit(1)
        manifest_paths = [bucket_dir / "manifest.json"]
    else:
        manifest_paths = sorted(
            WIKI_PASS2_DIR.glob("*/manifest.json"),
            key=lambda p: p.parent.name,
        )

    print(f"\nProcessing {len(manifest_paths):,} manifest(s)...")
    if args.verbose:
        print(f"  {'Bucket':<55s}  {'A':>3}  {'B':>3}  {'C':>4}  {'total':>5}")
        print(f"  {'-'*55}  {'-'*3}  {'-'*3}  {'-'*4}  {'-'*5}")

    # --- Process each manifest ---
    results: list[dict] = []
    skipped_core = 0
    errors = 0

    for manifest_path in manifest_paths:
        result = process_bucket(
            manifest_path=manifest_path,
            page_index=page_index,
            infobox_pages=infobox_pages,
            pass1_set=pass1_set,
            verbose=args.verbose,
        )
        if result is None:
            # Could be core (not secondary) or an error
            try:
                m = json.loads(manifest_path.read_text(encoding="utf-8"))
                if m.get("tier") == "core":
                    skipped_core += 1
            except Exception:
                errors += 1
            continue
        results.append(result)

    print(f"\n  Secondary buckets processed: {len(results):,}")
    print(f"  Core buckets skipped:        {skipped_core:,}")
    if errors:
        print(f"  Errors:                      {errors:,}", file=sys.stderr)

    if not results:
        print("WARNING: No secondary manifests found or processed.", file=sys.stderr)
        sys.exit(1)

    # --- Build summary ---
    computed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    summary = build_summary(results, computed_at)

    # --- Print human-readable summary ---
    print_summary(summary, apply_mode)

    # --- Apply: write manifests + summary ---
    if apply_mode:
        print(f"Writing priority field into {len(results):,} manifests...")
        for result in results:
            write_priority_to_manifest(result)

        print(f"Writing {PRIORITY_SUMMARY_FILE}...")
        PRIORITY_SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
        PRIORITY_SUMMARY_FILE.write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Done. {len(results):,} manifests updated.")
    else:
        print("Dry run complete. Re-run with --apply to write changes.")


if __name__ == "__main__":
    main()
