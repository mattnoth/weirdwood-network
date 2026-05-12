#!/usr/bin/env python3
"""
Promote 60 case-collision worker outputs into graph/nodes/.

Usage:
    python scripts/promote-case-collision.py --dry-run   # preview
    python scripts/promote-case-collision.py --apply     # write files

Reads from:
  working/missions/case-collision-top-10/worker-*/output.md  (10 files)
  working/missions/case-collision-batch-2/worker-*/output.md (50 files)

Handles:
  - Type corrections (event.conflict→event.war, event.military-expedition→event.battle, etc.)
  - CREATE vs UPDATE (existing stub gets Identity + type overwrite)
  - Multi-type policy (free-folk: factions/→concepts/, children-of-the-forest: factions/→species/)
  - Alias merges (crossroads-inn deletion, red-priest + red-priestess, valar-morghulis update)
  - Skip case (old-gods: already aliased on old-gods-of-the-forest)
"""

import os
import re
import glob
import argparse
from pathlib import Path

REPO = Path(__file__).parent.parent
GRAPH = REPO / "graph/nodes"

MISSION_DIRS = [
    REPO / "working/missions/case-collision-top-10",
    REPO / "working/missions/case-collision-batch-2",
]

TYPE_DIR_MAP = {
    "character.human": "characters",
    "character.direwolf": "characters",
    "character.dragon": "characters",
    "place.location": "locations",
    "place.region": "locations",
    "organization.house": "houses",
    "organization.faction": "factions",
    "organization.religion": "religions",
    "concept.culture": "concepts",
    "concept.magic": "concepts",
    "concept.prophecy": "concepts",
    "concept.theory": "concepts",
    "concept.language": "concepts",
    "concept.medical": "concepts",
    "concept.custom": "concepts",
    "object.artifact": "artifacts",
    "object.text": "texts",
    "object.food": "foods",
    "object.material": "materials",
    "event.battle": "events",
    "event.war": "events",
    "event.tournament": "events",
    "species": "species",
    "title": "titles",
}

# Worker drift corrections
TYPE_CORRECTIONS = {
    "event.military-expedition": "event.battle",
    "event.conflict": "event.war",
    "titles": "title",
}

# Per-slug type overrides (for bare `concept` drift cases)
SLUG_TYPE_OVERRIDES = {
    "come-into-my-castle": "concept.custom",
    "first-night": "concept.custom",
    "gender-and-sexuality": "concept.custom",
    "great-houses": "concept.custom",
    "great-voyages": "concept.custom",
    "pit-fighters": "concept.custom",
    "stallion-who-mounts-the-world": "concept.prophecy",
    "valar-morghulis": "concept.custom",
}

# Slugs to skip entirely (already resolved in the graph)
SKIP_SLUGS = {
    "old-gods",  # already aliased on old-gods-of-the-forest.node.md
}

# Nodes that must be MOVED (source_path → target_dir) + re-typed
MOVE_CASES = {
    "free-folk": {
        "from": GRAPH / "factions/free-folk.node.md",
        "to_dir": "concepts",
        "new_type": "concept.culture",
    },
    "children-of-the-forest": {
        "from": GRAPH / "factions/children-of-the-forest.node.md",
        "to_dir": "species",
        "new_type": "species",
    },
}

# Slugs where an existing stub must be deleted before creating the canonical
# (e.g., crossroads-inn stub gets deleted; its slug becomes an alias on inn-at-the-crossroads)
DELETE_STUBS_ON_PROMOTE = {
    "inn-at-the-crossroads": [GRAPH / "locations/crossroads-inn.node.md"],
}


def parse_output_md(path: Path) -> dict:
    """Parse a worker output.md into a structured dict."""
    content = path.read_text()

    # Split frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        fm_text = parts[1].strip()
        body = parts[2].strip() if len(parts) > 2 else ""
    else:
        fm_text = ""
        body = content.strip()

    # Parse frontmatter key/value (handles simple inline lists and multi-line lists)
    fm = {}
    lines = fm_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "":
                # Possible multi-line list (YAML block sequence)
                sub_items = []
                i += 1
                while i < len(lines) and lines[i].startswith("  - "):
                    sub_items.append(lines[i][4:].strip().strip('"').strip("'"))
                    i += 1
                fm[key] = sub_items
                continue
            else:
                fm[key] = val
        i += 1

    # Parse aliases from the frontmatter
    raw_aliases = fm.get("aliases", "[]")
    if isinstance(raw_aliases, list):
        aliases = raw_aliases
    elif isinstance(raw_aliases, str):
        if raw_aliases.startswith("["):
            inner = raw_aliases.strip("[]")
            aliases = [a.strip().strip('"').strip("'") for a in inner.split(",") if a.strip()]
        elif raw_aliases:
            aliases = [raw_aliases.strip('"').strip("'")]
        else:
            aliases = []
    else:
        aliases = []

    # Parse body sections
    sections = {}
    current_header = None
    current_lines: list[str] = []
    for line in body.split("\n"):
        if line.startswith("## "):
            if current_header is not None:
                sections[current_header] = "\n".join(current_lines).strip()
            current_header = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_header is not None:
        sections[current_header] = "\n".join(current_lines).strip()

    return {
        "slug": fm.get("slug", ""),
        "type": fm.get("type", ""),
        "pass_origin": fm.get("pass_origin", "pass2-wiki-reconstruction-mission"),
        "aliases": aliases,
        "identity": sections.get("Identity", ""),
        "edges": sections.get("Edges", ""),
    }


def slugify_to_name(slug: str) -> str:
    """Convert kebab-case slug to display name."""
    return " ".join(w.capitalize() for w in slug.replace("-", " ").split())


def resolve_type(slug: str, raw_type: str) -> str:
    """Apply type corrections and per-slug overrides."""
    # Per-slug override takes priority
    if slug in SLUG_TYPE_OVERRIDES:
        return SLUG_TYPE_OVERRIDES[slug]
    # General correction table
    if raw_type in TYPE_CORRECTIONS:
        return TYPE_CORRECTIONS[raw_type]
    return raw_type


def find_existing_node(slug: str, type_dir: str) -> Path | None:
    """Check if a node already exists at the expected path."""
    expected = GRAPH / type_dir / f"{slug}.node.md"
    if expected.exists():
        return expected
    # Also check all type dirs (node might be in a different dir due to past misclassification)
    for d in TYPE_DIR_MAP.values():
        p = GRAPH / d / f"{slug}.node.md"
        if p.exists():
            return p
    return None


def build_node_content(slug: str, type_: str, aliases: list[str],
                       pass_origin: str, identity: str, edges: str,
                       preserve_fm: dict | None = None) -> str:
    """Build the full node file content."""
    name = slugify_to_name(slug)
    aliases_yaml = (
        "[" + ", ".join(f'"{a}"' for a in aliases) + "]" if aliases else "[]"
    )

    if preserve_fm:
        # Keep original frontmatter but override type, aliases
        fm_lines = []
        for k, v in preserve_fm.items():
            if k == "type":
                fm_lines.append(f"type: {type_}")
            elif k == "aliases":
                fm_lines.append(f"aliases: {aliases_yaml}")
            else:
                fm_lines.append(f"{k}: {v}")
        fm_block = "\n".join(fm_lines)
    else:
        fm_block = (
            f'name: "{name}"\n'
            f"type: {type_}\n"
            f"slug: {slug}\n"
            f"aliases: {aliases_yaml}\n"
            f"confidence: tier-2\n"
            f"pass_origin: {pass_origin}"
        )

    body = f"## Identity\n\n{identity}\n\n## Edges\n\n{edges}"
    return f"---\n{fm_block}\n---\n\n{body}\n"


def read_existing_fm(node_path: Path) -> dict:
    """Parse the frontmatter of an existing node as ordered key/value pairs."""
    content = node_path.read_text()
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    fm_text = parts[1].strip()
    result = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip()
    return result


def promote_slug(worker: dict, dry_run: bool, log: list[str]) -> None:
    slug = worker["slug"]
    raw_type = worker["type"]
    aliases = worker["aliases"]
    pass_origin = worker["pass_origin"]
    identity = worker["identity"]
    edges = worker["edges"]

    # Skip?
    if slug in SKIP_SLUGS:
        log.append(f"  SKIP      {slug}  (already aliased in graph)")
        return

    # Resolve type
    type_ = resolve_type(slug, raw_type)

    if type_ not in TYPE_DIR_MAP:
        log.append(f"  ERROR     {slug}  unrecognized type after correction: {type_!r} (raw: {raw_type!r})")
        return

    type_dir = TYPE_DIR_MAP[type_]

    # Handle MOVE cases (free-folk, children-of-the-forest)
    if slug in MOVE_CASES:
        mc = MOVE_CASES[slug]
        src = mc["from"]
        type_ = mc["new_type"]
        type_dir = mc["to_dir"]
        target = GRAPH / type_dir / f"{slug}.node.md"

        if not dry_run:
            if src.exists():
                src.unlink()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(build_node_content(slug, type_, aliases, pass_origin, identity, edges))
        log.append(f"  MOVE+UPD  {slug}  {mc['from'].parent.name}/→{type_dir}/  (type: {raw_type}→{type_})")
        return

    target = GRAPH / type_dir / f"{slug}.node.md"

    # Delete obsolete stubs before writing canonical
    if slug in DELETE_STUBS_ON_PROMOTE:
        for stub_path in DELETE_STUBS_ON_PROMOTE[slug]:
            if stub_path.exists():
                if not dry_run:
                    stub_path.unlink()
                log.append(f"  DEL-STUB  {stub_path.name}")

    # Determine CREATE vs UPDATE
    existing = find_existing_node(slug, type_dir)

    if existing is not None:
        # UPDATE: preserve existing frontmatter, overwrite Identity+Edges, fix type/aliases
        preserve_fm = read_existing_fm(existing)
        content = build_node_content(slug, type_, aliases, pass_origin, identity, edges, preserve_fm=preserve_fm)
        if not dry_run:
            # If existing node is in a different dir, move it
            if existing != target:
                existing.unlink()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        log.append(f"  UPDATE    {slug}  ({existing.parent.name}/{existing.name} → {type_dir}/)")
    else:
        # CREATE: new node
        content = build_node_content(slug, type_, aliases, pass_origin, identity, edges)
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        log.append(f"  CREATE    {slug}  → {type_dir}/")


def pre_work_cleanups(dry_run: bool, log: list[str]) -> None:
    """Handle cleanups before main promotion loop."""

    # 1. Fix war-of-the-five-kings: event.battle → event.war
    wotfk = GRAPH / "events/war-of-the-five-kings.node.md"
    if wotfk.exists():
        content = wotfk.read_text()
        if "type: event.battle" in content:
            new_content = content.replace("type: event.battle", "type: event.war", 1)
            if not dry_run:
                wotfk.write_text(new_content)
            log.append(f"  TYPE-FIX  war-of-the-five-kings  event.battle → event.war")
        else:
            log.append(f"  OK        war-of-the-five-kings  (already event.war)")
    else:
        log.append(f"  MISSING   war-of-the-five-kings.node.md")

    # 2. Delete war-of-five-kings duplicate (empty, wrong slug)
    wofk_dup = GRAPH / "events/war-of-five-kings.node.md"
    if wofk_dup.exists():
        if not dry_run:
            wofk_dup.unlink()
        log.append(f"  DEL-DUP   war-of-five-kings.node.md  (wrong slug, empty content)")

    # 3. Add red-priestess to red-priest aliases
    rp = GRAPH / "titles/red-priest.node.md"
    if rp.exists():
        content = rp.read_text()
        if "red-priestess" not in content:
            new_content = content.replace(
                'aliases: []',
                'aliases: ["red-priestess", "Red Priestess"]',
                1
            )
            if 'aliases: []' not in content:
                # Try other formats
                new_content = re.sub(
                    r'(aliases:\s*\[)(\])',
                    r'\1"red-priestess", "Red Priestess"\2',
                    content,
                    count=1,
                )
            if not dry_run:
                rp.write_text(new_content)
            log.append(f"  ALIAS-ADD red-priest  ← red-priestess, Red Priestess")
        else:
            log.append(f"  OK        red-priest  (red-priestess alias already present)")

    # Note: valar-morghulis and red-priest Identity updates happen in the main loop


def main():
    parser = argparse.ArgumentParser(description="Promote case-collision outputs to graph/nodes/")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions, no writes")
    parser.add_argument("--apply", action="store_true", help="Actually write files")
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("Specify --dry-run or --apply")
        return

    dry_run = not args.apply
    log = []

    if dry_run:
        print("=== DRY RUN — no files will be written ===\n")
    else:
        print("=== APPLY — writing files ===\n")

    # Pre-work cleanups
    print("--- Pre-work cleanups ---")
    pre_work_cleanups(dry_run, log)
    for line in log:
        print(line)
    log.clear()

    # Collect all output.md files
    output_files = []
    for mission_dir in MISSION_DIRS:
        output_files.extend(sorted(mission_dir.glob("worker-*/output.md")))

    print(f"\n--- Promoting {len(output_files)} outputs ---")

    counts = {"CREATE": 0, "UPDATE": 0, "MOVE+UPD": 0, "SKIP": 0, "ERROR": 0}

    for output_path in output_files:
        worker = parse_output_md(output_path)
        if not worker["slug"]:
            print(f"  SKIP (no slug): {output_path}")
            continue

        promote_slug(worker, dry_run, log)

        for line in log:
            print(line)
            for key in counts:
                if key in line:
                    counts[key] += 1
                    break
        log.clear()

    print(f"\n--- Summary ---")
    for k, v in counts.items():
        if v:
            print(f"  {k}: {v}")
    total = sum(counts.values())
    print(f"  Total: {total} / {len(output_files)}")


if __name__ == "__main__":
    main()
