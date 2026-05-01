#!/usr/bin/env python3
"""wiki-pass2-pass-e-phase1.py

Pass E Phase 1 — surgical cleanup of technical debt accumulated across
Stage 3c + Tier 3 Passes A-D.

Handles four tasks:

  Task 1 — Fix 19 misclassified "title" nodes
    15 faction-like pages (city watches, religious movements, Night's Watch orders,
    paramilitary groups, guilds) are moved from titles/ to factions/ with
    type: organization.faction. 4 remain as title (bastard, hedge-knight,
    lord-of-widows-watch, sellsword).

  Task 2 — Merge culture variant duplicates
    Five variant-groups in factions/: andal/andals, dornish/dornishmen/dornishman,
    lhazareen/lhazarene, lysene/lyseni, stormlander/stormlanders.
    Canonical node gets variant slugs added to aliases[]. Variant files deleted.

  Task 3 — Re-emit 14 stale religion-bleed locations
    14 location/faction nodes still carry WORSHIPS edges with category-label
    targets (Old gods, Mixed, Dothraki) from before the Session 27 parser fix.
    Full re-emission from the corrected infobox-data.jsonl (Scope B of
    wiki-pass2-stage3-house-location-reemit.py template).

  Task 4 — Fix HEIR_TO date-bleed in parser + graph
    The wiki Heir infobox field uses year links for succession date ranges like
    "Baela Targaryen (131-134 AC)". The parser emits these year links as
    HEIR_TO targets. Fix: extend is_born_died_field logic to the heir/heirs
    field so _is_date_link() filters them out.
    Then surgically remove the 14 affected HEIR_TO edges from the 6 impacted
    character nodes.

Usage:
    python3 scripts/wiki-pass2-pass-e-phase1.py           # dry-run, all tasks
    python3 scripts/wiki-pass2-pass-e-phase1.py --apply   # write files
    python3 scripts/wiki-pass2-pass-e-phase1.py --task 1  # single task
    python3 scripts/wiki-pass2-pass-e-phase1.py --task 1 2 3 4 --apply
    python3 scripts/wiki-pass2-pass-e-phase1.py -v        # verbose

After --apply, run:
    python3 scripts/wiki-pass2-build-alias-resolver.py --apply
    python3 scripts/orphan-edges-audit.py > working/audits/orphan-edges-2026-04-30f.md
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
GRAPH_NODES_DIR = PROJECT_ROOT / "graph" / "nodes"
INFOBOX_DATA_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "infobox-data.jsonl"
WIKI_PASS2_DIR = PROJECT_ROOT / "working" / "wiki-pass2"
PARSER_SCRIPT = SCRIPT_DIR / "wiki-infobox-parser.py"

# ---------------------------------------------------------------------------
# Task 1: Misclassified title nodes
# ---------------------------------------------------------------------------

# 15 nodes to migrate to organization.faction
TO_FACTION = [
    "ancient-guild-of-spicers",   # merchants' guild
    "antler-men",                  # merchants' guild / political group
    "barefoot-lambs",              # rebel army
    "builders",                    # Night's Watch order
    "city-watch-braavos",          # city watch
    "city-watch-meereen",          # city watch
    "city-watch-of-lannisport",    # city watch
    "city-watch-pentos",           # city watch
    "city-watch-qohor",            # city watch
    "civic-guard",                 # city watch (Qarth Pureborn guard)
    "poor-fellows",                # military order (Faith Militant)
    "rangers",                     # Night's Watch order
    "sons-of-the-harpy",           # resistance organization
    "sparrows",                    # religious movement
    "stewards",                    # Night's Watch order
]

# 4 nodes legitimately kept as title
KEEP_AS_TITLE = [
    "bastard",            # social designation / name convention
    "hedge-knight",       # occupational title
    "lord-of-widows-watch",  # territorial lordship title
    "sellsword",          # occupational role / title
]

# ---------------------------------------------------------------------------
# Task 2: Culture variant merges
# ---------------------------------------------------------------------------

# (canonical_slug, [variants_to_delete_and_alias])
CULTURE_MERGES = [
    ("andals",      ["andal"]),
    ("dornishmen",  ["dornish", "dornishman"]),
    ("lhazareen",   ["lhazarene"]),
    ("lyseni",      ["lysene"]),
    ("stormlanders", ["stormlander"]),
]

# ---------------------------------------------------------------------------
# Task 3: Religion-bleed location re-emission
# (from audit orphan-edges-2026-04-30e.md — stale-data section)
# ---------------------------------------------------------------------------

RELIGION_BLEED_SLUGS = [
    "barrow-hall",
    "blackpool",
    "braavos",
    "deepwood-motte",
    "greywater-watch",
    "karhold",
    "last-hearth",
    "old-empire-of-ghis",
    "raventree-hall",
    "triarchy",
    "vaes-dothrak",
    "valyrian-freehold",
    "whitetree",
    "winterfell",
]

# ---------------------------------------------------------------------------
# Task 4: HEIR_TO date-bleed — affected nodes + their bad edge patterns
# ---------------------------------------------------------------------------

HEIR_DATE_BLEED_NODES = {
    "aerys-ii-targaryen": [r"- HEIR_TO: 283[^\n]+"],
    "daeron-ii-targaryen": [r"- HEIR_TO: 209[^\n]+"],
    "aegon-iii-targaryen": [
        r"- HEIR_TO: 134[^\n]+",
        r"- HEIR_TO: 143[^\n]+",
        r"- HEIR_TO: 157[^\n]+",
    ],
    "aerys-i-targaryen": [
        r"- HEIR_TO: 209[^\n]+",
        r"- HEIR_TO: 215[^\n]+",
        r"- HEIR_TO: 217[^\n]+",
        r"- HEIR_TO: 221[^\n]+",
    ],
    "aegon-ii-targaryen": [
        r"- HEIR_TO: 129[^\n]+",
        r"- HEIR_TO: 130[^\n]+",
        r"- HEIR_TO: 131[^\n]+",
    ],
    "robert-i-baratheon": [
        r"- HEIR_TO: 286[^\n]+",
        r"- HEIR_TO: 298[^\n]+",
    ],
}


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def atomic_write(dest_path: Path, content: str) -> None:
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    staging = dest_path.parent / f".staging-{dest_path.name}.tmp"
    try:
        staging.write_text(content, encoding="utf-8")
        os.rename(staging, dest_path)
    except Exception:
        staging.unlink(missing_ok=True)
        raise


def load_infobox_data() -> dict:
    if not INFOBOX_DATA_FILE.exists():
        print(f"ERROR: {INFOBOX_DATA_FILE} not found", file=sys.stderr)
        sys.exit(1)
    data = {}
    with open(INFOBOX_DATA_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rec = json.loads(line)
                data[rec["page"]] = rec
    return data


def load_page_to_bucket() -> dict[str, str]:
    page_to_bucket: dict[str, str] = {}
    for manifest_path in WIKI_PASS2_DIR.rglob("manifest.json"):
        bucket_id = manifest_path.parent.name
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for page in manifest.get("input_pages", []):
                page_to_bucket[page] = bucket_id
        except (json.JSONDecodeError, OSError):
            pass
    return page_to_bucket


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


def render_skeleton(page_name, slug, entity_type, aliases, confidence,
                    bucket_id, relationships, infobox_found) -> str:
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


def find_node(slug: str) -> tuple[Path | None, str | None]:
    """Find a node file across all type directories. Returns (path, dir_name)."""
    for type_dir in GRAPH_NODES_DIR.iterdir():
        if not type_dir.is_dir() or type_dir.name.startswith("_"):
            continue
        candidate = type_dir / f"{slug}.node.md"
        if candidate.exists():
            return candidate, type_dir.name
    return None, None


def slug_regression_check() -> list[str]:
    """Return list of files with slug: *.node (regression indicator)."""
    bad = []
    for p in GRAPH_NODES_DIR.rglob("*.node.md"):
        content = p.read_text(encoding="utf-8")
        if re.search(r'^slug: .*\.node\s*$', content, re.MULTILINE):
            bad.append(str(p))
    return bad


# ---------------------------------------------------------------------------
# Task 1: Migrate misclassified title nodes
# ---------------------------------------------------------------------------

def task1_migrate_titles(apply: bool, verbose: bool) -> dict:
    """Move faction-like title nodes to factions/ with type: organization.faction."""
    print("\n=== Task 1: Migrate misclassified title nodes ===")
    titles_dir = GRAPH_NODES_DIR / "titles"
    factions_dir = GRAPH_NODES_DIR / "factions"
    factions_dir.mkdir(parents=True, exist_ok=True)

    migrated = []
    kept = []
    errors = []

    for slug in TO_FACTION:
        src = titles_dir / f"{slug}.node.md"
        if not src.exists():
            errors.append(f"{slug}: not found in titles/")
            continue

        content = src.read_text(encoding="utf-8")
        # Replace type: title with type: organization.faction
        new_content = re.sub(
            r'^type: title\s*$',
            'type: organization.faction',
            content,
            flags=re.MULTILINE,
            count=1,
        )
        # Replace Identity description if it mentions "title"
        new_content = re.sub(
            r'^(\w.*) is a title from the AWOIAF wiki\.',
            r'\1 is a organization.faction from the AWOIAF wiki.',
            new_content,
            flags=re.MULTILINE,
            count=1,
        )

        dest = factions_dir / f"{slug}.node.md"
        if dest.exists():
            errors.append(f"{slug}: already exists in factions/ (collision)")
            continue

        outcome = "would_migrate"
        if apply:
            atomic_write(dest, new_content)
            src.unlink()
            outcome = "migrated"

        migrated.append(slug)
        if verbose:
            print(f"  [1] {outcome}: titles/{slug} → factions/{slug}")

    for slug in KEEP_AS_TITLE:
        src = titles_dir / f"{slug}.node.md"
        if not src.exists():
            errors.append(f"{slug}: not found in titles/ (expected to keep)")
        else:
            kept.append(slug)
            if verbose:
                print(f"  [1] kept as title: {slug}")

    print(f"  Migrated to factions: {len(migrated)}")
    print(f"  Kept as title:        {len(kept)}")
    print(f"  Errors:               {len(errors)}")
    for e in errors:
        print(f"    ERROR: {e}")

    return {"migrated": migrated, "kept": kept, "errors": errors}


# ---------------------------------------------------------------------------
# Task 2: Merge culture variant duplicates
# ---------------------------------------------------------------------------

def task2_merge_variants(apply: bool, verbose: bool) -> dict:
    """Merge culture variant slugs onto canonical nodes via aliases."""
    print("\n=== Task 2: Merge culture variant duplicates ===")
    factions_dir = GRAPH_NODES_DIR / "factions"

    merged = []
    deleted = []
    errors = []

    for canonical_slug, variants in CULTURE_MERGES:
        canonical_path = factions_dir / f"{canonical_slug}.node.md"
        if not canonical_path.exists():
            errors.append(f"{canonical_slug}: canonical node not found")
            continue

        canonical_content = canonical_path.read_text(encoding="utf-8")

        # Parse current aliases from frontmatter
        alias_match = re.search(r'^aliases:\s*(\[.*?\])\s*$', canonical_content, re.MULTILINE)
        if alias_match:
            current_aliases_str = alias_match.group(1)
            # Parse inline list ["a", "b"] or []
            inner = current_aliases_str.strip("[]")
            current_aliases = [
                a.strip().strip('"\'')
                for a in inner.split(",")
                if a.strip().strip('"\'')
            ] if inner.strip() else []
        else:
            current_aliases = []

        new_aliases = list(current_aliases)
        variants_processed = []

        for variant_slug in variants:
            variant_path = factions_dir / f"{variant_slug}.node.md"
            if not variant_path.exists():
                errors.append(f"{variant_slug}: variant not found in factions/")
                continue

            # Extract unique content from variant that might not be in canonical
            variant_content = variant_path.read_text(encoding="utf-8")

            # Get the variant name from frontmatter for alias
            name_match = re.search(r'^name:\s*"?([^"\n]+)"?\s*$', variant_content, re.MULTILINE)
            variant_name = name_match.group(1).strip() if name_match else variant_slug

            # Add variant_slug and variant_name to aliases if not already present
            if variant_slug not in new_aliases and variant_slug != canonical_slug:
                new_aliases.append(variant_slug)
            if variant_name not in new_aliases and variant_name.lower() != canonical_slug:
                # Also add the name if it's different from slug
                name_as_slug = re.sub(r'[^a-z0-9-]', '-', variant_name.lower()).strip('-')
                name_as_slug = re.sub(r'-+', '-', name_as_slug)
                if name_as_slug not in new_aliases and name_as_slug != canonical_slug:
                    new_aliases.append(variant_name)

            variants_processed.append(variant_slug)
            deleted.append(variant_slug)

        if not variants_processed:
            continue

        # Update aliases in canonical frontmatter
        if new_aliases:
            alias_items = ", ".join(f'"{a}"' for a in new_aliases)
            new_aliases_yaml = f"[{alias_items}]"
        else:
            new_aliases_yaml = "[]"

        new_canonical = re.sub(
            r'^aliases:\s*.*$',
            f'aliases: {new_aliases_yaml}',
            canonical_content,
            flags=re.MULTILINE,
            count=1,
        )

        outcome = "would_update"
        if apply:
            atomic_write(canonical_path, new_canonical)
            for variant_slug in variants_processed:
                variant_path = factions_dir / f"{variant_slug}.node.md"
                variant_path.unlink()
            outcome = "updated+deleted"

        merged.append(canonical_slug)
        if verbose:
            print(f"  [2] {outcome}: {canonical_slug} ← aliases {variants_processed}")

    print(f"  Canonicals updated: {len(merged)}")
    print(f"  Variants deleted:   {len(deleted)}")
    print(f"  Errors:             {len(errors)}")
    for e in errors:
        print(f"    ERROR: {e}")

    return {"merged_canonicals": merged, "deleted_variants": deleted, "errors": errors}


# ---------------------------------------------------------------------------
# Task 3: Re-emit stale religion-bleed locations
# ---------------------------------------------------------------------------

def task3_reemit_religion_bleed(apply: bool, verbose: bool) -> dict:
    """Full re-emission of 14 location nodes still carrying pre-fix WORSHIPS edges."""
    print("\n=== Task 3: Re-emit stale religion-bleed locations ===")

    infobox_data = load_infobox_data()
    page_to_bucket = load_page_to_bucket()

    TYPE_DIR_MAP = {
        "character.human": "characters",
        "character.direwolf": "characters",
        "character.dragon": "characters",
        "character": "characters",
        "organization.house": "houses",
        "organization.faction": "factions",
        "organization.cult": "factions",
        "organization.religion": "religions",
        "organization": "factions",
        "place.location": "locations",
        "place.region": "locations",
        "place.castle": "locations",
        "place.city": "locations",
        "place": "locations",
        "artifact": "artifacts",
        "artifact.weapon": "artifacts",
        "event.battle": "events",
        "event.war": "events",
        "event": "events",
        "title": "titles",
        "religion": "religions",
    }

    reemitted = []
    errors = []
    skipped = []

    for slug in RELIGION_BLEED_SLUGS:
        # Find existing node
        node_path, current_dir = find_node(slug)
        if node_path is None:
            errors.append(f"{slug}: node not found in graph")
            continue

        content = node_path.read_text(encoding="utf-8")

        # Check that it actually has a stale WORSHIPS edge
        has_stale_worships = bool(re.search(
            r'- WORSHIPS: (?:Old gods|Mixed|Dothraki|Mixed religions)',
            content
        ))
        if not has_stale_worships:
            # Check if it still has old-gods as target (slug form)
            has_stale_slug = bool(re.search(
                r'- WORSHIPS: (?:old-gods|mixed|dothraki)',
                content, re.IGNORECASE
            ))
            if not has_stale_slug:
                skipped.append(f"{slug}: no stale WORSHIPS edge found (already clean)")
                if verbose:
                    print(f"  [3] SKIP {slug}: already clean")
                continue

        # Get page name from frontmatter
        name_match = re.search(r'^name:\s*"?([^"\n]+)"?\s*$', content, re.MULTILINE)
        if not name_match:
            errors.append(f"{slug}: no name in frontmatter")
            continue
        page_name = name_match.group(1).strip()

        infobox_rec = infobox_data.get(page_name)
        if infobox_rec is None:
            errors.append(f"{slug}: '{page_name}' not in infobox-data.jsonl")
            continue

        bucket_id = page_to_bucket.get(page_name, "unknown")

        # Determine confidence from bucket manifest
        manifest_path = WIKI_PASS2_DIR / bucket_id / "manifest.json"
        confidence = "tier-1"
        if manifest_path.exists():
            try:
                m = json.loads(manifest_path.read_text(encoding="utf-8"))
                confidence = m.get("tier_default", "tier-1")
            except (json.JSONDecodeError, OSError):
                pass

        aliases = infobox_rec.get("aliases") or []
        relationships = infobox_rec.get("relationships") or []
        entity_type = infobox_rec.get("entity_type") or "place.location"

        target_dir_name = TYPE_DIR_MAP.get(entity_type)
        if target_dir_name is None:
            # Try parent type
            parent = entity_type.split(".")[0]
            target_dir_name = TYPE_DIR_MAP.get(parent, current_dir)

        dest_path = GRAPH_NODES_DIR / target_dir_name / f"{slug}.node.md"

        skeleton = render_skeleton(
            page_name=page_name,
            slug=slug,
            entity_type=entity_type,
            aliases=aliases,
            confidence=confidence,
            bucket_id=bucket_id,
            relationships=relationships,
            infobox_found=True,
        )

        # Append prose if it exists
        prose_path = WIKI_PASS2_DIR / bucket_id / "prose" / f"{slug}.prose.md"
        if prose_path.exists():
            final_content = skeleton + "\n" + prose_path.read_text(encoding="utf-8")
        else:
            final_content = skeleton

        old_edge_count = sum(1 for l in content.splitlines() if l.strip().startswith("- "))
        new_edge_count = len(relationships)

        outcome = "would_reemit"
        if apply:
            if dest_path != node_path:
                atomic_write(dest_path, final_content)
                node_path.unlink()
                outcome = "moved+reemitted"
            else:
                atomic_write(dest_path, final_content)
                outcome = "reemitted"

        reemitted.append(slug)
        if verbose:
            print(f"  [3] {outcome}: {slug} (edges: {old_edge_count} → {new_edge_count},"
                  f" type={entity_type}, dir={target_dir_name})")

    print(f"  Re-emitted: {len(reemitted)}")
    print(f"  Skipped:    {len(skipped)}")
    print(f"  Errors:     {len(errors)}")
    for s in skipped:
        print(f"    SKIP: {s}")
    for e in errors:
        print(f"    ERROR: {e}")

    return {"reemitted": reemitted, "skipped": skipped, "errors": errors}


# ---------------------------------------------------------------------------
# Task 4a: Patch wiki-infobox-parser.py
# ---------------------------------------------------------------------------

def task4_patch_parser(apply: bool, verbose: bool) -> dict:
    """Extend _is_date_link filtering to heir/heirs fields in the infobox parser."""
    print("\n=== Task 4a: Patch wiki-infobox-parser.py for HEIR_TO date-bleed ===")

    if not PARSER_SCRIPT.exists():
        print(f"  ERROR: {PARSER_SCRIPT} not found")
        return {"patched": False, "error": "parser not found"}

    content = PARSER_SCRIPT.read_text(encoding="utf-8")

    # Check if already patched
    if "is_heir_field" in content:
        print("  Already patched (is_heir_field found). Skipping.")
        return {"patched": False, "already_patched": True}

    # The fix: extend is_born_died_field to also cover heir/heirs fields
    old_str = '    is_born_died_field = field_lower in ("born", "died", "buried")'
    new_str = '    is_born_died_field = field_lower in ("born", "died", "buried")\n    is_heir_field = field_lower in ("heir", "heirs")'

    if old_str not in content:
        print(f"  ERROR: anchor string not found in parser. Manual patch needed.")
        return {"patched": False, "error": "anchor not found"}

    # Also need to apply date-filtering logic to heir fields.
    # In the links path: after filtering date links for born_died_field, we need
    # to do the same for heir fields. BUT for heirs, we still want the place links
    # — we just want to remove the year links (which are annotation, not targets).
    # The parallel fix: also filter date links from heir fields.
    patched = content.replace(old_str, new_str)

    # Now extend the date-link filtering block:
    # Original: `    if is_born_died_field and links:`
    old_filter_block = '    if is_born_died_field and links:'
    new_filter_block = '    if (is_born_died_field or is_heir_field) and links:'
    if old_filter_block in patched:
        patched = patched.replace(old_filter_block, new_filter_block, 1)
    else:
        print("  WARNING: could not patch date-filter block start")

    # Extend the date-links rebuild:
    # Original: `        links = [\n            (href, lt)\n            for href, lt in links\n            if not _is_date_link(href, lt.strip())\n        ]`
    old_rebuild = (
        '        links = [\n'
        '            (href, lt)\n'
        '            for href, lt in links\n'
        '            if not _is_date_link(href, lt.strip())\n'
        '        ]'
    )
    new_rebuild = (
        '        links = [\n'
        '            (href, lt)\n'
        '            for href, lt in links\n'
        '            if not _is_date_link(href, lt.strip())\n'
        '        ]\n'
        '        # For heir fields: discard date qualifier since dates are annotations,\n'
        '        # not meaningful edge data. Keep only character-name links.\n'
        '        if is_heir_field:\n'
        '            date_qualifier = None'
    )
    if old_rebuild in patched:
        patched = patched.replace(old_rebuild, new_rebuild, 1)
    else:
        print("  WARNING: could not patch date-links rebuild block")

    # Also apply to the plain-text path for heir fields:
    # Original: `        if is_born_died_field:`  (in the else/plain-text block)
    # We need the plain-text date-item skipping to apply to heir fields too.
    # The relevant block is inside `else:` after `if links:`. There are two
    # references to is_born_died_field in the plain-text path.
    old_pt1 = '            if is_born_died_field:\n                # Match "Place, <date>" where date is year/era at end of string'
    new_pt1 = '            if is_born_died_field or is_heir_field:\n                # Match "Place, <date>" where date is year/era at end of string'
    if old_pt1 in patched:
        patched = patched.replace(old_pt1, new_pt1, 1)
    else:
        print("  WARNING: could not patch plain-text date suffix check")

    if patched == content:
        print("  ERROR: no changes made — all patches failed")
        return {"patched": False, "error": "no changes"}

    outcome = "would_patch"
    if apply:
        atomic_write(PARSER_SCRIPT, patched)
        outcome = "patched"

    print(f"  Parser: {outcome}")
    print(f"  Changes: is_born_died_field extended to is_heir_field")
    return {"patched": True, "outcome": outcome}


# ---------------------------------------------------------------------------
# Task 4b: Surgically remove HEIR_TO date-bleed edges from existing nodes
# ---------------------------------------------------------------------------

def task4_fix_heir_edges(apply: bool, verbose: bool) -> dict:
    """Remove HEIR_TO date-bleed edge lines from the 6 affected character nodes."""
    print("\n=== Task 4b: Remove HEIR_TO date-bleed edges from graph nodes ===")

    fixed = []
    errors = []
    no_change = []

    for slug, patterns in HEIR_DATE_BLEED_NODES.items():
        node_path, dir_name = find_node(slug)
        if node_path is None:
            errors.append(f"{slug}: node not found in graph")
            continue

        content = node_path.read_text(encoding="utf-8")
        new_content = content

        edges_removed = 0
        for pattern in patterns:
            # Match the full line (with possible \xa0 non-breaking spaces)
            # The pattern uses raw text from the edge lines with \xa0
            line_re = re.compile(
                r'^' + pattern.replace(r'\n', '') + r'[^\n]*\n?',
                re.MULTILINE
            )
            before = new_content
            new_content = line_re.sub('', new_content)
            if new_content != before:
                edges_removed += 1

        # Clean up any double-blank lines in the Edges section
        new_content = re.sub(r'\n{3,}', '\n\n', new_content)

        if new_content == content:
            no_change.append(slug)
            if verbose:
                print(f"  [4b] no-change: {slug} (patterns may not have matched)")
            continue

        outcome = "would_fix"
        if apply:
            atomic_write(node_path, new_content)
            outcome = "fixed"

        fixed.append(slug)
        if verbose:
            print(f"  [4b] {outcome}: {slug} — removed {edges_removed} date-bleed HEIR_TO edges")

    print(f"  Fixed: {len(fixed)}")
    print(f"  No-change: {len(no_change)}")
    print(f"  Errors: {len(errors)}")
    for e in errors:
        print(f"    ERROR: {e}")

    return {"fixed": fixed, "no_change": no_change, "errors": errors}


# ---------------------------------------------------------------------------
# Final slug regression check
# ---------------------------------------------------------------------------

def run_slug_regression_check():
    print("\n=== Slug regression check ===")
    bad = slug_regression_check()
    if bad:
        print(f"  WARNING: {len(bad)} files have slug: *.node regression:")
        for b in bad:
            print(f"    {b}")
    else:
        print("  OK: No slug regressions found.")
    return bad


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
    parser.add_argument("--task", nargs="+", type=int, choices=[1, 2, 3, 4],
                        help="Run specific task(s). Default: all four.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print per-node output.")
    args = parser.parse_args()

    tasks = set(args.task) if args.task else {1, 2, 3, 4}
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"\n{'='*60}")
    print(f"Pass E Phase 1 — [{mode}] — Tasks: {sorted(tasks)}")
    print(f"{'='*60}")

    results = {}

    if 1 in tasks:
        results["task1"] = task1_migrate_titles(args.apply, args.verbose)

    if 2 in tasks:
        results["task2"] = task2_merge_variants(args.apply, args.verbose)

    if 3 in tasks:
        results["task3"] = task3_reemit_religion_bleed(args.apply, args.verbose)

    if 4 in tasks:
        results["task4_parser"] = task4_patch_parser(args.apply, args.verbose)
        results["task4_edges"] = task4_fix_heir_edges(args.apply, args.verbose)

    # Slug regression check (always run)
    run_slug_regression_check()

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    if "task1" in results:
        r = results["task1"]
        print(f"Task 1 (title migration):  {len(r['migrated'])} migrated to factions,"
              f" {len(r['kept'])} kept as title, {len(r['errors'])} errors")
        if r["migrated"]:
            print(f"  Migrated: {', '.join(r['migrated'])}")
        if r["kept"]:
            print(f"  Kept: {', '.join(r['kept'])}")

    if "task2" in results:
        r = results["task2"]
        print(f"Task 2 (culture merges):   {len(r['merged_canonicals'])} canonicals updated,"
              f" {len(r['deleted_variants'])} variants deleted, {len(r['errors'])} errors")
        if r["deleted_variants"]:
            print(f"  Deleted variants: {', '.join(r['deleted_variants'])}")

    if "task3" in results:
        r = results["task3"]
        print(f"Task 3 (religion-bleed):   {len(r['reemitted'])} re-emitted,"
              f" {len(r['skipped'])} skipped, {len(r['errors'])} errors")

    if "task4_parser" in results and "task4_edges" in results:
        rp = results["task4_parser"]
        re_ = results["task4_edges"]
        patched_str = "YES" if rp.get("patched") else ("ALREADY DONE" if rp.get("already_patched") else "FAILED")
        print(f"Task 4 (HEIR_TO date-bleed): parser patched={patched_str},"
              f" {len(re_['fixed'])} nodes fixed, {len(re_['no_change'])} no-change,"
              f" {len(re_['errors'])} errors")
        if re_["fixed"]:
            print(f"  Fixed nodes: {', '.join(re_['fixed'])}")

    if not args.apply:
        print(f"\nDry-run only. Run with --apply to write files.")
        print("After --apply, run:")
        print("  python3 scripts/wiki-pass2-build-alias-resolver.py --apply")
        print("  python3 scripts/orphan-edges-audit.py > working/audits/orphan-edges-2026-04-30f.md")

    print(f"{'='*60}")


if __name__ == "__main__":
    main()
