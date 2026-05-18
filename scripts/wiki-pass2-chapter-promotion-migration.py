#!/usr/bin/env python3
"""wiki-pass2-chapter-promotion-migration.py

Migration orchestrator for the 344 ASOIAF chapter-summary wiki pages.

These pages were either:
  - Never promoted (325 pages — classified as 'skip'/'unknown' in the old pipeline)
  - Promoted with the wrong type 'event.battle' (12 ASOS chapters in battles-a bucket)
  - Not matched by the original regex (7 prologue/epilogue pages)

After this migration every chapter page lives in graph/nodes/chapters/ as a
meta.chapter node.

Modes:
  --plan   (default)  Print everything that would be done; write nothing.
  --apply             Execute all steps.

Steps (--apply only):
  1. Create 5 per-book bucket directories + manifest files under
     working/wiki/pass2-buckets/meta-chapters-{agot,acok,asos,affc,adwd}/
  2. Emit skeleton nodes via patched wiki-pass2-emit-deterministic.py logic
     (meta.chapter type, book/chapter_number/pov_character frontmatter).
  3. Extract prose via wiki-pass2-extract-prose.py (subprocess, one bucket at a time).
  4. Delete 12 mis-typed event.battle nodes at graph/nodes/events/
     a-storm-of-swords-chapter-{8,9,71-80}.node.md  (git rm or os.unlink).
  5. Promote via wiki-pass2-promote.py (subprocess, one bucket at a time)
     → writes 344 nodes to graph/nodes/chapters/.
  6. Archive battles-a artefacts for the 12 chapter pages (skeleton + prose)
     → moved to working/wiki/pass2-buckets/battles-a/_archive/.
  6.5. Archive stale triage artefacts:
     - working/wiki/pass2-staging/triage-bucket-assignments.jsonl
       → working/wiki/pass2-staging/_archive/triage-bucket-assignments-2026-05-13-pre-chapter-migration.jsonl
     - Write MIGRATION-NOTE.md to working/wiki/pass2-buckets/battles-a/
  7. Re-run cross-references index (wiki-pass2-build-cross-refs.py --apply).
  8. Re-run alias resolver (wiki-pass2-build-alias-resolver.py --apply).
  9. Re-run edge-candidate generator (wiki-pass2-build-edge-candidates.py --apply).
  10. Print summary.

Usage:
  python3 scripts/wiki-pass2-chapter-promotion-migration.py --plan
  python3 scripts/wiki-pass2-chapter-promotion-migration.py --apply
  python3 scripts/wiki-pass2-chapter-promotion-migration.py --apply -v
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

WIKI_RAW_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
GRAPH_NODES_DIR = PROJECT_ROOT / "graph" / "nodes"
WIKI_PASS2_DIR = PROJECT_ROOT / "working" / "wiki" / "pass2-buckets"
CATEGORIES_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "page-categories.jsonl"
INFOBOX_DATA_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "infobox-data.jsonl"
PAGE_INDEX_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "page-index.jsonl"

# Step 6.5 — stale artefact paths
TRIAGE_BUCKET_ASSIGNMENTS_FILE = (
    PROJECT_ROOT / "working" / "wiki" / "pass2-staging" / "triage-bucket-assignments.jsonl"
)
TRIAGE_ARCHIVE_DIR = PROJECT_ROOT / "working" / "wiki" / "pass2-staging" / "_archive"
TRIAGE_ARCHIVE_DEST = TRIAGE_ARCHIVE_DIR / "triage-bucket-assignments-2026-05-13-pre-chapter-migration.jsonl"
BATTLES_A_NOTE_PATH = WIKI_PASS2_DIR / "battles-a" / "MIGRATION-NOTE.md"
BATTLES_A_NOTE_CONTENT = """\
Note: The `validation-failed` status in this manifest was caused by 12 mis-typed chapter pages
(a-storm-of-swords-chapter-{8,9,71-80}). Those pages were re-typed as meta.chapter and moved
to graph/nodes/chapters/ by scripts/wiki-pass2-chapter-promotion-migration.py on 2026-05-13.
The remaining 18 real battle pages in this bucket should now validate cleanly on re-run.
"""

# ---------------------------------------------------------------------------
# Chapter page definitions
# ---------------------------------------------------------------------------
CHAPTER_PAGE_RE = re.compile(
    r"^A (Game of Thrones|Clash of Kings|Storm of Swords|Feast for Crows|Dance with Dragons)"
    r"-(Chapter (\d+)|Prologue|Epilogue)$"
)
BOOK_SLUG_MAP = {
    "A Game of Thrones":    "a-game-of-thrones",
    "A Clash of Kings":     "a-clash-of-kings",
    "A Storm of Swords":    "a-storm-of-swords",
    "A Feast for Crows":    "a-feast-for-crows",
    "A Dance with Dragons": "a-dance-with-dragons",
}
BOOK_BUCKET_SUFFIX = {
    "A Game of Thrones":    "agot",
    "A Clash of Kings":     "acok",
    "A Storm of Swords":    "asos",
    "A Feast for Crows":    "affc",
    "A Dance with Dragons": "adwd",
}
BOOK_ORDERED = [
    "A Game of Thrones",
    "A Clash of Kings",
    "A Storm of Swords",
    "A Feast for Crows",
    "A Dance with Dragons",
]

# The 12 mis-typed event.battle nodes to delete
MIS_TYPED_SLUGS = [
    "a-storm-of-swords-chapter-8",
    "a-storm-of-swords-chapter-9",
    "a-storm-of-swords-chapter-71",
    "a-storm-of-swords-chapter-72",
    "a-storm-of-swords-chapter-73",
    "a-storm-of-swords-chapter-74",
    "a-storm-of-swords-chapter-75",
    "a-storm-of-swords-chapter-76",
    "a-storm-of-swords-chapter-77",
    "a-storm-of-swords-chapter-78",
    "a-storm-of-swords-chapter-79",
    "a-storm-of-swords-chapter-80",
]


# ---------------------------------------------------------------------------
# Slug helpers
# ---------------------------------------------------------------------------

def page_to_slug(page_name: str) -> str:
    """Convert a wiki page name to a filesystem slug."""
    slug = page_name.lower()
    slug = re.sub(r"['\",]", "", slug)
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def slugify(text: str) -> str:
    """Slugify a display name (e.g. 'Daenerys Targaryen' -> 'daenerys-targaryen')."""
    return page_to_slug(text)


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def chapter_sort_key(page_name: str) -> int:
    """Return a numeric sort key for a chapter page name.

    Prologues sort first (0), numbered chapters sort by their number (1..N),
    epilogues sort last (999).
    """
    m = CHAPTER_PAGE_RE.match(page_name)
    if not m:
        return 500  # fallback — should never happen
    if m.group(3) is not None:
        return int(m.group(3))
    if m.group(2) == "Prologue":
        return 0
    return 999  # Epilogue


def discover_chapter_pages() -> dict[str, list[str]]:
    """Return {book_title: [sorted page names]} by scanning sources/wiki/_raw/.

    Matches numbered chapters (Chapter N), Prologue, and Epilogue pages.
    Sort order: Prologue (0) < Chapter 1..N < Epilogue (999).
    """
    book_pages: dict[str, list[str]] = {b: [] for b in BOOK_ORDERED}
    for raw_file in WIKI_RAW_DIR.iterdir():
        if not raw_file.suffix == ".json":
            continue
        page_name = raw_file.stem.replace("_", " ")
        m = CHAPTER_PAGE_RE.match(page_name)
        if m:
            book_title = "A " + m.group(1)
            book_pages[book_title].append(page_name)
    for book_title in book_pages:
        book_pages[book_title].sort(key=chapter_sort_key)
    return book_pages


def load_categories() -> dict[str, list[str]]:
    """Return {page_name: [category, ...]} from page-categories.jsonl."""
    data: dict[str, list[str]] = {}
    if not CATEGORIES_FILE.exists():
        print(f"WARNING: {CATEGORIES_FILE} not found — POV categories unavailable", file=sys.stderr)
        return data
    with open(CATEGORIES_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            data[rec["page"]] = rec.get("categories", [])
    return data


POV_CATEGORY_RE = re.compile(
    r"^A Song of Ice And Fire chapters--POV (.+)$",
    re.IGNORECASE,
)
# Prologues and epilogues use a different category format on the wiki:
# "Chapters with the POV of <Name>" instead of the --POV <Name> subcategory.
POV_CHAPTER_WITH_RE = re.compile(
    r"^Chapters with the POV of (.+)$",
    re.IGNORECASE,
)


def get_pov(page_name: str, categories: dict[str, list[str]]) -> str | None:
    """Return slugified POV character name, or None if not in categories.

    Numbered chapters use the subcategory format:
      "A Song of Ice And Fire chapters--POV <Name>"
    Prologues and epilogues use a flat category format:
      "Chapters with the POV of <Name>"
    Both are tried in order; first match wins.
    """
    for cat in categories.get(page_name, []):
        m = POV_CATEGORY_RE.match(cat)
        if m:
            return slugify(m.group(1))
    for cat in categories.get(page_name, []):
        m = POV_CHAPTER_WITH_RE.match(cat)
        if m:
            return slugify(m.group(1))
    return None


# ---------------------------------------------------------------------------
# Broken-link analysis
# ---------------------------------------------------------------------------

def count_broken_links_that_will_resolve(chapter_slugs: set[str]) -> int:
    """Count cross-reference rows whose target is one of the chapter slugs."""
    cross_refs_file = PROJECT_ROOT / "working" / "wiki" / "data" / "cross-references.jsonl"
    if not cross_refs_file.exists():
        return 0
    count = 0
    with open(cross_refs_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("target_slug") in chapter_slugs:
                count += 1
    return count


# ---------------------------------------------------------------------------
# Wiki-URL helper
# ---------------------------------------------------------------------------

def wiki_url(page_name: str) -> str:
    import urllib.parse
    encoded = urllib.parse.quote(page_name.replace(" ", "_"), safe="/:@!$&'()*+,;=")
    return f"https://awoiaf.westeros.org/index.php/{encoded}"


# ---------------------------------------------------------------------------
# Skeleton node renderer for meta.chapter
# ---------------------------------------------------------------------------

def render_chapter_skeleton(
    page_name: str,
    slug: str,
    bucket_id: str,
    confidence: str,
    book_slug: str,
    chapter_number: int,
    pov_character: str | None,
) -> str:
    """Render a complete skeleton node for a meta.chapter page."""
    url = wiki_url(page_name)
    pov_line = pov_character if pov_character is not None else "null"

    lines = [
        "---",
        f'name: "{page_name}"',
        f"type: meta.chapter",
        f"slug: {slug}",
        f"aliases: []",
        f"confidence: {confidence}",
        f'wiki_source: "{url}"',
        f"bucket_id: {bucket_id}",
        "prompt_version: v1-python",
        "node_version: 1",
        "pass_origin: pass2-wiki-deterministic",
        f"book: {book_slug}",
        f"chapter_number: {chapter_number}",
        f"pov_character: {pov_line}",
        "---",
        "",
        "## Identity",
        "",
        f"{page_name} is a meta.chapter from the AWOIAF wiki.",
        "",
        "## Edges",
        "",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Manifest builder
# ---------------------------------------------------------------------------

def build_manifest(bucket_id: str, pages: list[str]) -> dict:
    """Build a manifest.json dict for a meta-chapters bucket."""
    import hashlib
    payload = {
        "input_pages": sorted(pages),
        "prompt_version": "v1",
        "chunk_strategy": "single-pass",
    }
    fingerprint = hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()

    return {
        "bucket_id": bucket_id,
        "tier": "secondary",
        "tier_default": "tier-1",
        "fingerprint": fingerprint,
        "prompt_version": "v1",
        "chunk_strategy": "single-pass",
        "oversized": False,
        "input_pages": sorted(pages),
        "expected_nodes": sorted(page_to_slug(p) + ".node.md" for p in pages),
        "status": "pending",
        "started_at": None,
        "completed_at": None,
        "validation_report": None,
        # Priority: all pages are Tier A (prose-rich chapter summaries)
        "priority": {
            "version": "v1",
            "computed_at": datetime.now(timezone.utc).isoformat(),
            "tier_a": sorted(pages),
            "tier_b": [],
            "tier_c": [],
            "stats": {
                "total": len(pages),
                "tier_a": len(pages),
                "tier_b": 0,
                "tier_c": 0,
            },
        },
    }


# ---------------------------------------------------------------------------
# Git-rm or unlink helper
# ---------------------------------------------------------------------------

def delete_node(path: Path, apply: bool, verbose: bool) -> str:
    """Delete a node file. Uses git rm if git-tracked, else os.unlink.

    Returns 'git-rm', 'unlink', or 'not-found'.
    """
    if not path.exists():
        return "not-found"
    if not apply:
        return "would-delete"

    # Try git rm first (preserves git history)
    result = subprocess.run(
        ["git", "rm", "--force", "-q", str(path)],
        cwd=PROJECT_ROOT,
        capture_output=True,
    )
    if result.returncode == 0:
        if verbose:
            print(f"    git rm {path.name}")
        return "git-rm"

    # Fall back to os.unlink (untracked file)
    path.unlink()
    if verbose:
        print(f"    unlink {path.name}")
    return "unlink"


# ---------------------------------------------------------------------------
# Subprocess runner
# ---------------------------------------------------------------------------

def run_script(script_name: str, extra_args: list[str], verbose: bool) -> int:
    """Run a project script via subprocess. Returns return code."""
    cmd = [sys.executable, str(SCRIPT_DIR / script_name)] + extra_args
    if verbose:
        print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    return result.returncode


# ---------------------------------------------------------------------------
# Plan mode
# ---------------------------------------------------------------------------

def run_plan(verbose: bool) -> None:
    """Print what --apply would do without writing anything."""
    print("=" * 70)
    print("wiki-pass2-chapter-promotion-migration.py  --plan")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    # Discover chapter pages
    book_pages = discover_chapter_pages()
    all_pages = [p for pages in book_pages.values() for p in pages]
    all_slugs = {page_to_slug(p) for p in all_pages}
    total = len(all_pages)

    print(f"\nStep 1: Chapter page counts from sources/wiki/_raw/")
    print(f"  {'Book':<35s}  {'Pages':>6}  {'Bucket'}")
    for book_title in BOOK_ORDERED:
        pages = book_pages[book_title]
        suffix = BOOK_BUCKET_SUFFIX[book_title]
        bucket = f"meta-chapters-{suffix}"
        print(f"  {book_title:<35s}  {len(pages):>6}  {bucket}")
    print(f"  {'TOTAL':<35s}  {total:>6}")

    # Bucket breakdown
    print(f"\nStep 2: 5 new bucket directories to create:")
    for book_title in BOOK_ORDERED:
        suffix = BOOK_BUCKET_SUFFIX[book_title]
        bucket = f"meta-chapters-{suffix}"
        bucket_dir = WIKI_PASS2_DIR / bucket
        exists = "(already exists)" if bucket_dir.exists() else "(new)"
        print(f"  working/wiki/pass2-buckets/{bucket}/  {exists}")

    # POV check
    print(f"\nStep 3: POV character derivation")
    categories = load_categories()
    pov_found = 0
    pov_missing = 0
    missing_examples: list[str] = []
    # Show prologue/epilogue POV resolutions explicitly for spot-checking
    special_pages = [p for p in all_pages
                     if CHAPTER_PAGE_RE.match(p) and CHAPTER_PAGE_RE.match(p).group(3) is None]
    print(f"  Prologue/Epilogue POV resolutions ({len(special_pages)} pages):")
    for page in sorted(special_pages, key=chapter_sort_key):
        pov = get_pov(page, categories)
        pov_display = pov if pov else "NULL (missing category)"
        print(f"    {page:<50s}  pov_character: {pov_display}")
    for page in all_pages:
        pov = get_pov(page, categories)
        if pov:
            pov_found += 1
        else:
            pov_missing += 1
            if len(missing_examples) < 5:
                missing_examples.append(page)
    print(f"  POV found: {pov_found} / {total}")
    print(f"  POV null: {pov_missing}")
    if missing_examples:
        print(f"  Pages with null POV: {missing_examples}")

    # Mis-typed nodes to delete
    print(f"\nStep 4: Mis-typed event.battle nodes to delete (12 nodes):")
    events_dir = GRAPH_NODES_DIR / "events"
    for slug in MIS_TYPED_SLUGS:
        path = events_dir / f"{slug}.node.md"
        status = "EXISTS" if path.exists() else "NOT FOUND"
        print(f"  graph/nodes/events/{slug}.node.md  [{status}]")

    # Chapters to replace (12 ASOS chapters already have prose in battles-a)
    print(f"\nStep 5: Prose reuse from battles-a bucket (12 ASOS chapters):")
    battles_a_prose = WIKI_PASS2_DIR / "battles-a" / "prose"
    reuse_count = 0
    for slug in MIS_TYPED_SLUGS:
        prose_path = battles_a_prose / f"{slug}.prose.md"
        if prose_path.exists():
            print(f"  REUSE  battles-a/prose/{slug}.prose.md")
            reuse_count += 1
        else:
            print(f"  EXTRACT battles-a/prose/{slug}.prose.md (will run extract-prose)")
    print(f"  {reuse_count}/12 prose files available for reuse")
    print(f"  Remaining 332 pages (337+7 minus 12 reused): prose extracted fresh by wiki-pass2-extract-prose.py")

    # Promotion target
    print(f"\nStep 6: Promotion target")
    chapters_dir = GRAPH_NODES_DIR / "chapters"
    if chapters_dir.exists():
        existing = list(chapters_dir.glob("*.node.md"))
        print(f"  graph/nodes/chapters/ already exists ({len(existing)} nodes)")
    else:
        print(f"  graph/nodes/chapters/  (will be created)")
    print(f"  After promotion: 344 nodes in graph/nodes/chapters/")

    # Battles-a cleanup (Step 6b in plan — same as Step 6 in apply)
    print(f"\nStep 6b: battles-a bucket cleanup")
    battles_a_skel = WIKI_PASS2_DIR / "battles-a" / "skeleton"
    skel_count = sum(1 for slug in MIS_TYPED_SLUGS
                     if (battles_a_skel / f"{slug}.node.md").exists())
    prose_count = sum(1 for slug in MIS_TYPED_SLUGS
                      if (battles_a_prose / f"{slug}.prose.md").exists())
    print(f"  Skeleton files to archive: {skel_count}/12")
    print(f"  Prose files to archive:    {prose_count}/12")
    print(f"  Destination: working/wiki/pass2-buckets/battles-a/_archive/")

    # Step 6.5 — Stale artifact archiving
    print(f"\nStep 6.5: Stale artifact archiving")
    triage_src = TRIAGE_BUCKET_ASSIGNMENTS_FILE
    triage_dst = TRIAGE_ARCHIVE_DEST
    triage_src_status = "EXISTS" if triage_src.exists() else "NOT FOUND"
    triage_dst_status = "already archived" if triage_dst.exists() else "will archive"
    print(f"  Triage assignments archive:")
    print(f"    Source: working/wiki/pass2-staging/triage-bucket-assignments.jsonl  [{triage_src_status}]")
    print(f"    Dest:   working/wiki/pass2-staging/_archive/triage-bucket-assignments-2026-05-13-pre-chapter-migration.jsonl  [{triage_dst_status}]")
    note_status = "already exists" if BATTLES_A_NOTE_PATH.exists() else "will create"
    print(f"  battles-a MIGRATION-NOTE.md  [{note_status}]:")
    print(f"    working/wiki/pass2-buckets/battles-a/MIGRATION-NOTE.md")
    print(f"  (Both steps are idempotent — safe to re-run.)")

    # Cross-reference impact (Step 8 in apply sequence, after re-run of cross-refs at Step 7)
    print(f"\nStep 7-9: Cross-reference / alias / edge-candidate impact")
    cross_refs_file = PROJECT_ROOT / "working" / "wiki" / "data" / "cross-references.jsonl"
    if cross_refs_file.exists():
        current_lines = sum(1 for _ in open(cross_refs_file, encoding="utf-8"))
        broken = count_broken_links_that_will_resolve(all_slugs)
        print(f"  Current cross-references.jsonl: {current_lines:,} rows")
        print(f"  Broken-link targets resolving after promotion: {broken}")
        print(f"  New prose sources added (337 chapter summaries): will add ~thousands")
        print(f"  Estimated new total: {current_lines:,}+ (TBD after extraction)")
    else:
        print(f"  cross-references.jsonl not found — will be rebuilt by --apply")

    # Summary
    print(f"\n{'='*70}")
    print(f"PLAN SUMMARY")
    print(f"{'='*70}")
    print(f"  New meta.chapter nodes to create:       {total}")
    print(f"    (337 numbered chapters + 7 prologue/epilogue = 344 total)")
    for book_title in BOOK_ORDERED:
        suffix = BOOK_BUCKET_SUFFIX[book_title]
        pages = book_pages[book_title]
        numbered = sum(1 for p in pages if CHAPTER_PAGE_RE.match(p).group(3) is not None)
        special = len(pages) - numbered
        print(f"    {book_title:<35s} {len(pages):>4}  ({numbered} chapters + {special} prologue/epilogue)")
    print(f"  Mis-typed event.battle nodes to delete: {len(MIS_TYPED_SLUGS)}")
    print(f"  New buckets to create:                  5")
    print(f"  Stale triage file to archive:           1")
    print(f"  Broken cross-ref targets resolved:      see cross-references step")
    if total != 344:
        print(f"\n  WARNING: Expected 344 total pages, found {total}. Check wiki _raw/ for missing files.")
    else:
        print(f"\n  PASS 1 parity check: 344 matches Pass 1 extraction count across 5 books. OK.")
    print()
    print("Run with --apply to execute.")


# ---------------------------------------------------------------------------
# Apply mode
# ---------------------------------------------------------------------------

def run_apply(verbose: bool) -> None:
    """Execute the full migration."""
    print("=" * 70)
    print("wiki-pass2-chapter-promotion-migration.py  --apply")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    categories = load_categories()
    book_pages = discover_chapter_pages()
    all_pages = [p for pages in book_pages.values() for p in pages]
    print(f"Found {len(all_pages)} chapter pages to process.")

    # ------------------------------------------------------------------
    # Step 1 + 2: Create buckets, write manifests, emit skeletons
    # ------------------------------------------------------------------
    print("\n--- Step 1-2: Create bucket directories, manifests, and skeletons ---")
    skeletons_written = 0
    skeletons_skipped = 0

    for book_title in BOOK_ORDERED:
        pages = book_pages[book_title]
        suffix = BOOK_BUCKET_SUFFIX[book_title]
        bucket_id = f"meta-chapters-{suffix}"
        book_slug = BOOK_SLUG_MAP[book_title]
        bucket_dir = WIKI_PASS2_DIR / bucket_id
        skeleton_dir = bucket_dir / "skeleton"
        prose_dir = bucket_dir / "prose"

        bucket_dir.mkdir(parents=True, exist_ok=True)
        skeleton_dir.mkdir(parents=True, exist_ok=True)
        prose_dir.mkdir(parents=True, exist_ok=True)

        # Write manifest
        manifest = build_manifest(bucket_id, pages)
        manifest_path = bucket_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        print(f"  [{bucket_id}] manifest written ({len(pages)} pages)")

        # Emit skeletons
        for page_name in pages:
            m = CHAPTER_PAGE_RE.match(page_name)
            # group(3) holds the digit string for "Chapter N"; None for Prologue/Epilogue
            if m.group(3) is not None:
                chapter_number = int(m.group(3))
            elif m.group(2) == "Prologue":
                chapter_number = 0
            else:  # Epilogue
                chapter_number = 999
            pov = get_pov(page_name, categories)
            slug = page_to_slug(page_name)

            skeleton_content = render_chapter_skeleton(
                page_name=page_name,
                slug=slug,
                bucket_id=bucket_id,
                confidence="tier-1",
                book_slug=book_slug,
                chapter_number=chapter_number,
                pov_character=pov,
            )

            skel_path = skeleton_dir / f"{slug}.node.md"
            if skel_path.exists():
                skeletons_skipped += 1
            else:
                skel_path.write_text(skeleton_content, encoding="utf-8")
                skeletons_written += 1

        print(f"  [{bucket_id}] skeletons: {sum(1 for p in pages)} total"
              f" (written={skeletons_written}, skipped-existing={skeletons_skipped})")
        skeletons_written = 0
        skeletons_skipped = 0

    # ------------------------------------------------------------------
    # Step 3: Extract prose for new buckets
    # Handle the 12 ASOS chapters specially: reuse from battles-a/prose/
    # ------------------------------------------------------------------
    print("\n--- Step 3: Extract prose ---")

    # Copy battles-a prose files to meta-chapters-asos/prose/ (reuse)
    battles_a_prose = WIKI_PASS2_DIR / "battles-a" / "prose"
    asos_prose_dir = WIKI_PASS2_DIR / "meta-chapters-asos" / "prose"
    reused = 0
    for slug in MIS_TYPED_SLUGS:
        src = battles_a_prose / f"{slug}.prose.md"
        dst = asos_prose_dir / f"{slug}.prose.md"
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)
            reused += 1
            if verbose:
                print(f"    reused prose: {slug}.prose.md")
    print(f"  Reused {reused} ASOS prose files from battles-a/")

    # Run extract-prose for all 5 new buckets
    for book_title in BOOK_ORDERED:
        suffix = BOOK_BUCKET_SUFFIX[book_title]
        bucket_id = f"meta-chapters-{suffix}"
        print(f"  Extracting prose for {bucket_id}...")
        rc = run_script(
            "wiki-pass2-extract-prose.py",
            ["--bucket", bucket_id, "--apply"],
            verbose=verbose,
        )
        if rc != 0:
            print(f"  WARNING: extract-prose returned {rc} for {bucket_id}", file=sys.stderr)

    # ------------------------------------------------------------------
    # Step 4: Delete 12 mis-typed event.battle nodes
    # ------------------------------------------------------------------
    print("\n--- Step 4: Delete 12 mis-typed event.battle nodes ---")
    events_dir = GRAPH_NODES_DIR / "events"
    deleted = 0
    not_found = 0

    for slug in MIS_TYPED_SLUGS:
        path = events_dir / f"{slug}.node.md"
        outcome = delete_node(path, apply=True, verbose=verbose)
        if outcome in ("git-rm", "unlink"):
            deleted += 1
        elif outcome == "not-found":
            not_found += 1
            print(f"  WARNING: not found: {path}", file=sys.stderr)

    print(f"  Deleted: {deleted}  Not-found: {not_found}")

    # ------------------------------------------------------------------
    # Step 5: Promote all 5 new buckets
    # ------------------------------------------------------------------
    print("\n--- Step 5: Promote meta-chapter nodes ---")
    (GRAPH_NODES_DIR / "chapters").mkdir(parents=True, exist_ok=True)

    for book_title in BOOK_ORDERED:
        suffix = BOOK_BUCKET_SUFFIX[book_title]
        bucket_id = f"meta-chapters-{suffix}"
        print(f"  Promoting {bucket_id}...")
        rc = run_script(
            "wiki-pass2-promote.py",
            ["--bucket", bucket_id, "--apply"],
            verbose=verbose,
        )
        if rc != 0:
            print(f"  WARNING: promote returned {rc} for {bucket_id}", file=sys.stderr)

    promoted_count = sum(1 for _ in (GRAPH_NODES_DIR / "chapters").glob("*.node.md"))
    print(f"  Nodes in graph/nodes/chapters/ after promotion: {promoted_count}")

    # ------------------------------------------------------------------
    # Step 6: Archive battles-a artefacts for the 12 chapter pages
    # ------------------------------------------------------------------
    print("\n--- Step 6: Archive battles-a chapter artefacts ---")
    archive_dir = WIKI_PASS2_DIR / "battles-a" / "_archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archived = 0

    battles_a_skel = WIKI_PASS2_DIR / "battles-a" / "skeleton"
    for slug in MIS_TYPED_SLUGS:
        for src_dir, kind in [(battles_a_skel, "skeleton"), (battles_a_prose, "prose")]:
            ext = ".node.md" if kind == "skeleton" else ".prose.md"
            src = src_dir / f"{slug}{ext}"
            if src.exists():
                dst = archive_dir / f"{kind}-{slug}{ext}"
                shutil.move(str(src), str(dst))
                archived += 1
                if verbose:
                    print(f"    archived: {kind}/{slug}{ext}")

    print(f"  Archived {archived} battles-a artefacts to battles-a/_archive/")

    # ------------------------------------------------------------------
    # Step 6.5: Archive stale triage artefacts
    # ------------------------------------------------------------------
    print("\n--- Step 6.5: Archive stale triage artefacts ---")

    # Archive triage-bucket-assignments.jsonl (idempotent: skip if already done)
    TRIAGE_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    if TRIAGE_ARCHIVE_DEST.exists():
        print(f"  triage-bucket-assignments archive: already exists — skipping")
    elif TRIAGE_BUCKET_ASSIGNMENTS_FILE.exists():
        shutil.copy2(str(TRIAGE_BUCKET_ASSIGNMENTS_FILE), str(TRIAGE_ARCHIVE_DEST))
        print(f"  Copied triage-bucket-assignments.jsonl → _archive/ (original preserved)")
    else:
        print(f"  WARNING: triage-bucket-assignments.jsonl not found — nothing to archive",
              file=sys.stderr)

    # Write battles-a MIGRATION-NOTE.md (idempotent: skip if already written)
    if BATTLES_A_NOTE_PATH.exists():
        print(f"  battles-a/MIGRATION-NOTE.md: already exists — skipping")
    else:
        BATTLES_A_NOTE_PATH.write_text(BATTLES_A_NOTE_CONTENT, encoding="utf-8")
        print(f"  Written: working/wiki/pass2-buckets/battles-a/MIGRATION-NOTE.md")

    # ------------------------------------------------------------------
    # Step 7: Re-run cross-references index
    # ------------------------------------------------------------------
    print("\n--- Step 7: Rebuild cross-references index ---")
    cross_refs_before = 0
    cross_refs_file = PROJECT_ROOT / "working" / "wiki" / "data" / "cross-references.jsonl"
    if cross_refs_file.exists():
        cross_refs_before = sum(1 for _ in open(cross_refs_file, encoding="utf-8"))
    rc = run_script("wiki-pass2-build-cross-refs.py", ["--apply"], verbose=verbose)
    if rc != 0:
        print(f"  WARNING: cross-refs rebuild returned {rc}", file=sys.stderr)
    cross_refs_after = 0
    if cross_refs_file.exists():
        cross_refs_after = sum(1 for _ in open(cross_refs_file, encoding="utf-8"))
    print(f"  cross-references.jsonl: {cross_refs_before:,} → {cross_refs_after:,} rows")

    # ------------------------------------------------------------------
    # Step 8: Re-run alias resolver
    # ------------------------------------------------------------------
    print("\n--- Step 8: Rebuild alias resolver ---")
    rc = run_script("wiki-pass2-build-alias-resolver.py", ["--apply"], verbose=verbose)
    if rc != 0:
        print(f"  WARNING: alias-resolver rebuild returned {rc}", file=sys.stderr)
    else:
        print(f"  Alias resolver rebuilt.")

    # ------------------------------------------------------------------
    # Step 9: Re-run edge-candidate generator (--plan only — don't apply;
    # let Matt review before committing candidate files)
    # ------------------------------------------------------------------
    print("\n--- Step 9: Edge-candidate generator (--plan only, for review) ---")
    rc = run_script("wiki-pass2-build-edge-candidates.py", ["--plan"], verbose=verbose)
    if rc != 0:
        print(f"  WARNING: edge-candidate generator --plan returned {rc}", file=sys.stderr)

    # ------------------------------------------------------------------
    # Step 10: Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("MIGRATION COMPLETE — Summary")
    print("=" * 70)

    # Node count
    chapters_dir = GRAPH_NODES_DIR / "chapters"
    final_count = sum(1 for _ in chapters_dir.glob("*.node.md")) if chapters_dir.exists() else 0
    events_chapter_nodes = list((GRAPH_NODES_DIR / "events").glob("a-storm-of-swords-chapter-*.node.md"))

    print(f"\nNode counts:")
    print(f"  graph/nodes/chapters/           : {final_count} nodes")
    print(f"  graph/nodes/events/ (chapters)  : {len(events_chapter_nodes)} (should be 0)")
    if events_chapter_nodes:
        print(f"  WARNING: Still-present chapter nodes in events/:")
        for p in events_chapter_nodes:
            print(f"    {p.name}")

    print(f"\nCross-reference delta: {cross_refs_before:,} → {cross_refs_after:,} rows"
          f" (+{cross_refs_after - cross_refs_before:,})")

    print(f"\nValidation commands:")
    print(f"  ls graph/nodes/chapters/ | wc -l       # should be 344")
    print(f"  find graph/nodes/events -name 'a-*-chapter-*'  # should be empty")
    print(f"  grep -c 'type: meta.chapter' graph/nodes/chapters/*.node.md")

    if final_count != 344:
        print(f"\nWARNING: Expected 344 nodes in chapters/, got {final_count}.", file=sys.stderr)
    if events_chapter_nodes:
        print(f"WARNING: {len(events_chapter_nodes)} chapter nodes remain in events/.", file=sys.stderr)

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
        help="Execute the migration. Without --apply, prints plan only.",
    )
    parser.add_argument(
        "--plan",
        action="store_true",
        default=False,
        help="Print plan only (default behaviour; explicit flag accepted for clarity).",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Print per-file progress.",
    )
    args = parser.parse_args()

    if args.apply:
        run_apply(verbose=args.verbose)
    else:
        run_plan(verbose=args.verbose)


if __name__ == "__main__":
    main()
