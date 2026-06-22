#!/usr/bin/env python3
"""Stamp a `containers:` array tag onto node frontmatter (idempotent).

Usage:
    python scripts/stamp_containers.py <container-name> <slug> [<slug> ...]
    python scripts/stamp_containers.py --dry-run essos drogo-westward-vow ...

Adds <container-name> to each node's `containers:` frontmatter array. Idempotent: if the name is
already present it's a no-op for that node; if the key is absent it's inserted (after `era:` if present,
else after `confidence:`, else before the closing `---`). Never writes `[]`. Inline-flow style:
    containers: [essos]            (one value)
    containers: [wo5k, essos]      (seam node, multiple values)

A node not found is reported and skipped (does not abort the batch). Built S121 for the containers:
field rollout; reusable for WO5K + any retro-tagging.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NODES = REPO / "graph" / "nodes"


def find_node(slug):
    hits = list(NODES.glob(f"**/{slug}.node.md"))
    return hits[0] if hits else None


def parse_containers(line):
    """Parse a `containers: [a, b]` (or `containers: null`) line -> list of names."""
    m = re.match(r"\s*containers:\s*(.*)$", line)
    if not m:
        return None
    val = m.group(1).strip()
    if val in ("", "null", "~", "[]"):
        return []
    val = val.strip("[]")
    return [x.strip().strip("'\"") for x in val.split(",") if x.strip()]


def stamp(path, name, dry_run=False):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ("no-frontmatter", None)
    # locate frontmatter bounds
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return ("no-frontmatter", None)

    # existing containers line?
    cont_idx = None
    for i in range(1, end):
        if re.match(r"\s*containers:", lines[i]):
            cont_idx = i
            break

    if cont_idx is not None:
        current = parse_containers(lines[cont_idx]) or []
        if name in current:
            return ("already", current)
        new = current + [name]
        lines[cont_idx] = f"containers: [{', '.join(new)}]"
        result = ("merged", new)
    else:
        # insert after era: or confidence:, else just before closing ---
        insert_at = end
        for i in range(1, end):
            if re.match(r"\s*era:", lines[i]):
                insert_at = i + 1
                break
        else:
            for i in range(1, end):
                if re.match(r"\s*confidence:", lines[i]):
                    insert_at = i + 1
                    break
        lines.insert(insert_at, f"containers: [{name}]")
        result = ("inserted", [name])

    if not dry_run:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def main():
    args = [a for a in sys.argv[1:]]
    dry = False
    if args and args[0] == "--dry-run":
        dry = True
        args = args[1:]
    if len(args) < 2:
        sys.exit("usage: stamp_containers.py [--dry-run] <container-name> <slug> [<slug> ...]")
    name, slugs = args[0], args[1:]
    counts = {"inserted": 0, "merged": 0, "already": 0, "missing": 0, "no-frontmatter": 0}
    for slug in slugs:
        path = find_node(slug)
        if path is None:
            print(f"  MISSING  {slug}")
            counts["missing"] += 1
            continue
        status, vals = stamp(path, name, dry_run=dry)
        counts[status] = counts.get(status, 0) + 1
        print(f"  {status:9} {slug}  -> containers: {vals}")
    tag = " (dry-run)" if dry else ""
    print(f"\nDONE{tag}: " + " · ".join(f"{k}={v}" for k, v in counts.items() if v))
    if counts["missing"] or counts["no-frontmatter"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
