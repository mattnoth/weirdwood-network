#!/usr/bin/env python3
"""rename-event-node.py — Rename an event node slug across the graph.

Renames a node file and updates all references to the old slug in:
  - graph/nodes/events/<old-slug>.node.md  (slug: and name: frontmatter)
  - graph/edges/edges.jsonl  (source_slug and target_slug fields)
  - working/wiki/data/alias-resolver.json  (if the slug appears as a canonical)
  - working/wiki/data/event-node-aliases.json  (if the slug is a key)
  - working/wiki/data/cross-references.jsonl  (if file exists)
  - graph/nodes/**/*.node.md  (display-bullet references in other node bodies)

In --dry-run mode: prints a full diff/preview and exits without writing anything.
In --apply mode: performs all changes atomically (temp file + rename for JSONL).

Usage:
    python3 scripts/rename-event-node.py <old-slug> <new-slug> --dry-run
    python3 scripts/rename-event-node.py <old-slug> <new-slug> --apply

Constraints:
    - --dry-run: ZERO writes, anywhere.
    - --apply: atomic JSONL rewrites via temp file + os.replace().
    - If old-slug == new-slug: prints "no-op" and exits 0.
    - If new-slug already has a node file: ABORT with collision error.
"""

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EVENTS_DIR = ROOT / "graph" / "nodes" / "events"
EDGES_PATH = ROOT / "graph" / "edges" / "edges.jsonl"
ALIAS_RESOLVER_PATH = ROOT / "working" / "wiki" / "data" / "alias-resolver.json"
EVENT_NODE_ALIASES_PATH = ROOT / "working" / "wiki" / "data" / "event-node-aliases.json"
CROSS_REFS_PATH = ROOT / "working" / "wiki" / "data" / "cross-references.jsonl"
NODES_ROOT = ROOT / "graph" / "nodes"

# Rebuild command to print at the end (informational)
REBUILD_CMD = "python3 scripts/build-entity-indexes.py"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_LOWERCASE_WORDS = {"of", "the", "a", "an", "and", "or", "but", "in", "at",
                    "by", "for", "to", "up", "as", "on", "into", "with"}


def slug_to_name(slug: str) -> str:
    """Convert kebab-case slug to Title Case display name.

    Common prepositions/articles remain lowercase (matching ASOIAF naming conventions
    like 'Execution of Eddard Stark', 'Battle of the Blackwater').
    First word is always capitalized.
    """
    words = slug.split("-")
    result = []
    for i, word in enumerate(words):
        if i == 0 or word not in _LOWERCASE_WORDS:
            result.append(word.capitalize())
        else:
            result.append(word)
    return " ".join(result)


def read_frontmatter_field(text: str, field: str) -> str | None:
    """Extract a frontmatter field value from YAML frontmatter block."""
    in_frontmatter = False
    for i, line in enumerate(text.splitlines()):
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter and line.strip() == "---":
            break
        if in_frontmatter and line.startswith(f"{field}:"):
            val = line[len(f"{field}:"):].strip()
            return val.strip('"').strip("'")
    return None


def rewrite_frontmatter(text: str, old_slug: str, new_slug: str, new_name: str) -> str:
    """Rewrite slug: and name: fields in YAML frontmatter."""
    lines = text.splitlines(keepends=True)
    in_frontmatter = False
    result = []
    fence_count = 0

    for line in lines:
        stripped = line.strip()
        if fence_count == 0 and stripped == "---":
            in_frontmatter = True
            fence_count = 1
            result.append(line)
            continue
        if in_frontmatter and stripped == "---":
            in_frontmatter = False
            fence_count = 2
            result.append(line)
            continue

        if in_frontmatter:
            if line.startswith("slug:"):
                line = f'slug: {new_slug}\n'
            elif line.startswith("name:"):
                line = f'name: "{new_name}"\n'

        result.append(line)

    return "".join(result)


def find_node_body_references(old_slug: str) -> list[tuple[Path, list[int]]]:
    """Find all node files (outside events/) that reference old_slug in their body."""
    matches = []
    for node_file in NODES_ROOT.rglob("*.node.md"):
        if node_file.parent == EVENTS_DIR:
            continue  # the event node itself is handled separately
        text = node_file.read_text(encoding="utf-8")
        hit_lines = []
        for i, line in enumerate(text.splitlines(), 1):
            if old_slug in line:
                hit_lines.append(i)
        if hit_lines:
            matches.append((node_file, hit_lines))
    return matches


def rewrite_body_references(text: str, old_slug: str, new_slug: str) -> str:
    """Replace all occurrences of old_slug in a file's body text."""
    return text.replace(old_slug, new_slug)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old_slug", help="The current slug to rename from")
    parser.add_argument("new_slug", help="The new slug to rename to")
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--dry-run", action="store_true",
                            help="Preview all changes without writing anything")
    mode_group.add_argument("--apply", action="store_true",
                            help="Apply all changes (atomic writes via temp file + rename)")
    args = parser.parse_args()

    old_slug = args.old_slug
    new_slug = args.new_slug
    dry_run = args.dry_run

    mode_label = "DRY-RUN" if dry_run else "APPLY"
    print(f"\n{'='*60}")
    print(f"rename-event-node.py  [{mode_label}]")
    print(f"  old slug: {old_slug}")
    print(f"  new slug: {new_slug}")
    print(f"{'='*60}\n")

    # --- Guard: no-op ---
    if old_slug == new_slug:
        print("NO-OP: old-slug and new-slug are identical. Nothing to do.")
        sys.exit(0)

    # --- Guard: old node must exist ---
    old_node_path = EVENTS_DIR / f"{old_slug}.node.md"
    if not old_node_path.exists():
        print(f"ERROR: Source node file not found:\n  {old_node_path}")
        print("Aborting.")
        sys.exit(1)

    # --- Guard: new slug must not already have a node file ---
    new_node_path = EVENTS_DIR / f"{new_slug}.node.md"
    if new_node_path.exists():
        print(f"ERROR: Collision — target node file already exists:\n  {new_node_path}")
        print("Aborting. Choose a different new slug or manually resolve the collision.")
        sys.exit(1)

    # -----------------------------------------------------------------------
    # Step 1: Node file inspection
    # -----------------------------------------------------------------------
    old_node_text = old_node_path.read_text(encoding="utf-8")
    current_name = read_frontmatter_field(old_node_text, "name") or slug_to_name(old_slug)
    current_slug_field = read_frontmatter_field(old_node_text, "slug") or old_slug
    new_name = slug_to_name(new_slug)

    print("STEP 1: Node file")
    print(f"  Old path: {old_node_path.relative_to(ROOT)}")
    print(f"  New path: {new_node_path.relative_to(ROOT)}")
    print(f"  Frontmatter changes:")
    print(f"    slug:  '{current_slug_field}'  ->  '{new_slug}'")
    print(f"    name:  '{current_name}'  ->  '{new_name}'")

    # -----------------------------------------------------------------------
    # Step 2: Edge rows in edges.jsonl
    # -----------------------------------------------------------------------
    print(f"\nSTEP 2: Edge rows in {EDGES_PATH.relative_to(ROOT)}")

    edge_rows_all = []
    affected_edges = []
    superseded_by_edges = []

    if not EDGES_PATH.exists():
        print("  WARNING: edges.jsonl not found — skipping edge scan.")
    else:
        with EDGES_PATH.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    edge_rows_all.append(json.loads(line))

        for i, row in enumerate(edge_rows_all):
            src = row.get("source_slug", "")
            tgt = row.get("target_slug", "")
            sup = row.get("superseded_by", "")
            in_src_tgt = (src == old_slug or tgt == old_slug)
            in_sup = (sup == old_slug)
            if in_src_tgt:
                affected_edges.append((i, row))
            elif in_sup:
                superseded_by_edges.append((i, row))

        total_affected = len(affected_edges) + len(superseded_by_edges)
        print(f"  Total edge rows scanned: {len(edge_rows_all)}")
        print(f"  Rows with '{old_slug}' in source_slug/target_slug: {len(affected_edges)}")
        print(f"  Rows with '{old_slug}' in superseded_by only:      {len(superseded_by_edges)}")
        print(f"  Total rows touching '{old_slug}': {total_affected}")
        print()

        for rank, (line_num, row) in enumerate(affected_edges, 1):
            src = row.get("source_slug", "")
            tgt = row.get("target_slug", "")
            edge_type = row.get("edge_type", "?")
            quote = row.get("evidence_quote", "")[:60]
            sup = row.get("superseded_by", "")

            new_src = new_slug if src == old_slug else src
            new_tgt = new_slug if tgt == old_slug else tgt

            flags = []
            if sup == old_slug:
                flags.append("superseded_by ALSO changes in this row")
            flag_note = f"  [NOTE: {'; '.join(flags)}]" if flags else ""
            print(f"  [{rank}] line {line_num + 1}: {edge_type}")
            print(f"       source: '{src}'  ->  '{new_src}'")
            print(f"       target: '{tgt}'  ->  '{new_tgt}'")
            if quote:
                print(f"       quote:  \"{quote}\"")
            if flag_note:
                print(f"      {flag_note}")

        if superseded_by_edges:
            print(f"\n  Rows where only superseded_by changes:")
            for rank, (line_num, row) in enumerate(superseded_by_edges, 1):
                src = row.get("source_slug", "")
                tgt = row.get("target_slug", "")
                edge_type = row.get("edge_type", "?")
                sup = row.get("superseded_by", "")
                print(f"  [S{rank}] line {line_num + 1}: {edge_type}  {src} -> {tgt}")
                print(f"        superseded_by: '{sup}'  ->  '{new_slug}'")

    # -----------------------------------------------------------------------
    # Step 3: Reference files
    # -----------------------------------------------------------------------
    print(f"\nSTEP 3: Reference files")

    # 3a: alias-resolver.json
    alias_resolver_hits = {}
    if ALIAS_RESOLVER_PATH.exists():
        with ALIAS_RESOLVER_PATH.open(encoding="utf-8") as f:
            alias_data = json.load(f)
        # Scan alias_to_canonical values and keys
        for alias_key, canonical_val in alias_data.get("alias_to_canonical", {}).items():
            if canonical_val == old_slug or alias_key == old_slug:
                alias_resolver_hits[alias_key] = canonical_val
        if alias_resolver_hits:
            print(f"  alias-resolver.json: {len(alias_resolver_hits)} entries reference '{old_slug}'")
            for k, v in alias_resolver_hits.items():
                new_k = new_slug if k == old_slug else k
                new_v = new_slug if v == old_slug else v
                print(f"    '{k}' -> '{v}'  =>  '{new_k}' -> '{new_v}'")
        else:
            print(f"  alias-resolver.json: no entries reference '{old_slug}'")
    else:
        print(f"  alias-resolver.json: not found at {ALIAS_RESOLVER_PATH.relative_to(ROOT)}")

    # 3b: event-node-aliases.json
    event_aliases_hits = {}
    if EVENT_NODE_ALIASES_PATH.exists():
        with EVENT_NODE_ALIASES_PATH.open(encoding="utf-8") as f:
            event_aliases_data = json.load(f)
        if old_slug in event_aliases_data:
            event_aliases_hits[old_slug] = event_aliases_data[old_slug]
        # Also scan values for the slug
        for k, v in event_aliases_data.items():
            if k == old_slug:
                continue  # already captured above
            if old_slug in str(v):
                event_aliases_hits[f"(value in key='{k}')"] = v
        if event_aliases_hits:
            print(f"  event-node-aliases.json: {len(event_aliases_hits)} entries reference '{old_slug}'")
            for k, v in event_aliases_hits.items():
                print(f"    key: '{k}'  ->  value: {json.dumps(v)[:80]}")
        else:
            print(f"  event-node-aliases.json: no entries reference '{old_slug}'")
    else:
        print(f"  event-node-aliases.json: not found at {EVENT_NODE_ALIASES_PATH.relative_to(ROOT)}")

    # 3c: cross-references.jsonl
    cross_ref_hits = []
    if CROSS_REFS_PATH.exists():
        with CROSS_REFS_PATH.open(encoding="utf-8") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if line and old_slug in line:
                    cross_ref_hits.append((i + 1, line))
        if cross_ref_hits:
            print(f"  cross-references.jsonl: {len(cross_ref_hits)} lines reference '{old_slug}'")
            for lineno, content in cross_ref_hits[:5]:
                print(f"    line {lineno}: {content[:80]}")
            if len(cross_ref_hits) > 5:
                print(f"    ... and {len(cross_ref_hits) - 5} more")
        else:
            print(f"  cross-references.jsonl: no entries reference '{old_slug}'")
    else:
        print(f"  cross-references.jsonl: not found (skipped)")

    # 3d: Other node files
    print()
    other_node_hits = find_node_body_references(old_slug)
    if other_node_hits:
        print(f"  Other node files referencing '{old_slug}': {len(other_node_hits)}")
        for node_path, hit_lines in other_node_hits:
            rel = node_path.relative_to(ROOT)
            text = node_path.read_text(encoding="utf-8")
            lines = text.splitlines()
            print(f"    {rel}  (lines: {hit_lines})")
            for ln in hit_lines[:3]:
                print(f"      [{ln}] {lines[ln-1].strip()[:80]}")
    else:
        print(f"  Other node files: none reference '{old_slug}'")

    # -----------------------------------------------------------------------
    # Step 4: Summary count
    # -----------------------------------------------------------------------
    total_edge_rows = len(affected_edges) + len(superseded_by_edges)
    total_changes = 0
    total_changes += 1  # node file move + frontmatter
    total_changes += total_edge_rows
    total_changes += len(alias_resolver_hits)
    total_changes += len(event_aliases_hits)
    total_changes += len(cross_ref_hits)
    total_changes += len(other_node_hits)

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"  Node file rename:           1")
    print(f"  Edge rows (source/target):  {len(affected_edges)}")
    print(f"  Edge rows (superseded_by):  {len(superseded_by_edges)}")
    print(f"  Total edge rows updated:    {total_edge_rows}")
    print(f"  alias-resolver.json:        {len(alias_resolver_hits)} entries")
    print(f"  event-node-aliases.json:    {len(event_aliases_hits)} entries")
    print(f"  cross-references.jsonl:     {len(cross_ref_hits)} lines")
    print(f"  Other node files:           {len(other_node_hits)} files")
    print(f"  ----------------------------")
    print(f"  Total artifacts changed:    {total_changes}")

    if dry_run:
        print(f"\n[DRY-RUN] No writes performed.")
        print(f"To apply: python3 scripts/rename-event-node.py {old_slug} {new_slug} --apply")
        return

    # -----------------------------------------------------------------------
    # APPLY MODE — perform all writes
    # -----------------------------------------------------------------------

    print(f"\n{'='*60}")
    print("APPLYING CHANGES")

    # Apply 1: Rewrite node file content and move
    new_node_text = rewrite_frontmatter(old_node_text, old_slug, new_slug, new_name)
    new_node_path.write_text(new_node_text, encoding="utf-8")
    old_node_path.unlink()
    print(f"  [1] Node file: moved + frontmatter updated")
    print(f"      {old_node_path.relative_to(ROOT)}")
    print(f"   -> {new_node_path.relative_to(ROOT)}")

    # Apply 2: Rewrite edges.jsonl (atomic: temp file + os.replace)
    total_edge_rows = len(affected_edges) + len(superseded_by_edges)
    if total_edge_rows > 0:
        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=EDGES_PATH.parent, prefix=".rename-tmp-", suffix=".jsonl"
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmp_f:
                for row in edge_rows_all:
                    src = row.get("source_slug", "")
                    tgt = row.get("target_slug", "")
                    sup = row.get("superseded_by", "")
                    if src == old_slug or tgt == old_slug or sup == old_slug:
                        row = dict(row)
                        if src == old_slug:
                            row["source_slug"] = new_slug
                        if tgt == old_slug:
                            row["target_slug"] = new_slug
                        if sup == old_slug:
                            row["superseded_by"] = new_slug
                    tmp_f.write(json.dumps(row, ensure_ascii=False) + "\n")
            os.replace(tmp_path, EDGES_PATH)
            print(f"  [2] edges.jsonl: {total_edge_rows} rows updated (atomic rewrite)")
        except Exception as e:
            os.unlink(tmp_path)
            print(f"  ERROR rewriting edges.jsonl: {e}")
            sys.exit(1)
    else:
        print(f"  [2] edges.jsonl: no rows affected (skipped)")

    # Apply 3: alias-resolver.json
    if alias_resolver_hits and ALIAS_RESOLVER_PATH.exists():
        with ALIAS_RESOLVER_PATH.open(encoding="utf-8") as f:
            alias_data = json.load(f)
        a2c = alias_data.get("alias_to_canonical", {})
        new_a2c = {}
        for k, v in a2c.items():
            new_k = new_slug if k == old_slug else k
            new_v = new_slug if v == old_slug else v
            new_a2c[new_k] = new_v
        alias_data["alias_to_canonical"] = new_a2c
        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=ALIAS_RESOLVER_PATH.parent, prefix=".alias-tmp-", suffix=".json"
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmp_f:
                json.dump(alias_data, tmp_f, ensure_ascii=False, indent=2)
                tmp_f.write("\n")
            os.replace(tmp_path, ALIAS_RESOLVER_PATH)
            print(f"  [3] alias-resolver.json: {len(alias_resolver_hits)} entries updated")
        except Exception as e:
            os.unlink(tmp_path)
            print(f"  ERROR rewriting alias-resolver.json: {e}")
    else:
        print(f"  [3] alias-resolver.json: no entries affected (skipped)")

    # Apply 4: event-node-aliases.json
    if event_aliases_hits and EVENT_NODE_ALIASES_PATH.exists():
        with EVENT_NODE_ALIASES_PATH.open(encoding="utf-8") as f:
            ea_data = json.load(f)
        new_ea_data = {}
        for k, v in ea_data.items():
            new_k = new_slug if k == old_slug else k
            new_ea_data[new_k] = v
        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=EVENT_NODE_ALIASES_PATH.parent, prefix=".ea-tmp-", suffix=".json"
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmp_f:
                json.dump(new_ea_data, tmp_f, ensure_ascii=False, indent=2)
                tmp_f.write("\n")
            os.replace(tmp_path, EVENT_NODE_ALIASES_PATH)
            print(f"  [4] event-node-aliases.json: {len(event_aliases_hits)} entries updated")
        except Exception as e:
            os.unlink(tmp_path)
            print(f"  ERROR rewriting event-node-aliases.json: {e}")
    else:
        print(f"  [4] event-node-aliases.json: no entries affected (skipped)")

    # Apply 5: cross-references.jsonl (line-by-line string replace)
    if cross_ref_hits and CROSS_REFS_PATH.exists():
        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=CROSS_REFS_PATH.parent, prefix=".xref-tmp-", suffix=".jsonl"
        )
        count = 0
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmp_f:
                with CROSS_REFS_PATH.open(encoding="utf-8") as src_f:
                    for line in src_f:
                        if old_slug in line:
                            line = line.replace(old_slug, new_slug)
                            count += 1
                        tmp_f.write(line)
            os.replace(tmp_path, CROSS_REFS_PATH)
            print(f"  [5] cross-references.jsonl: {count} lines updated")
        except Exception as e:
            os.unlink(tmp_path)
            print(f"  ERROR rewriting cross-references.jsonl: {e}")
    else:
        print(f"  [5] cross-references.jsonl: no entries affected (skipped)")

    # Apply 6: Other node files
    if other_node_hits:
        for node_path, _ in other_node_hits:
            text = node_path.read_text(encoding="utf-8")
            new_text = rewrite_body_references(text, old_slug, new_slug)
            node_path.write_text(new_text, encoding="utf-8")
        print(f"  [6] Other node files: {len(other_node_hits)} files updated")
    else:
        print(f"  [6] Other node files: none affected (skipped)")

    # Done
    print(f"\n{'='*60}")
    print(f"DONE. Rename complete: '{old_slug}' -> '{new_slug}'")
    print(f"\nTo rebuild graph indexes, run:")
    print(f"  {REBUILD_CMD}")
    print()


if __name__ == "__main__":
    main()
