#!/usr/bin/env python3
"""Apply captured chapter quotes to node `## Quotes` sections (additive, idempotent).

Reads candidate quote files (default: working/historical-anchor/quotes/*.quotes.jsonl),
groups by target_node_slug, and appends each verbatim quote to that node's `## Quotes`
section. Creates the section at end-of-file if absent. Idempotent: a quote already present
(substring match) in the node file is skipped, so re-runs and concurrent passes are safe.

This is the reusable mechanism for the FIRM `capture-quotes-during-research` rule: any pass
over chapter/wiki text that captures load-bearing quotes lands them here.

Candidate line schema (one JSON object per line):
  {"target_node_slug","category","quote","source_ref","why","produced_at"}

Usage:
  python3 scripts/apply-node-quotes.py                 # dry run (default) over the default glob
  python3 scripts/apply-node-quotes.py --apply         # write
  python3 scripts/apply-node-quotes.py --glob 'working/foo/*.quotes.jsonl' [--apply]
"""
import json, glob, sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GLOB = 'working/historical-anchor/quotes/*.quotes.jsonl'

# slug -> node file path (one pass over the node tree)
NODE_FILES = {p.stem.replace('.node', ''): p for p in ROOT.glob('graph/nodes/**/*.node.md')}


def fmt_entry(e):
    """One markdown blockquote with provenance trailer (greppable for dedupe)."""
    q = e['quote'].strip()
    cat = e.get('category', 'other')
    ref = e.get('source_ref', '')
    why = (e.get('why') or '').strip()
    trailer = f"— {ref}" + (f" · {why}" if why else "")
    return f"> {q}\n>\n> {trailer}  _(capture: chapter-quote sweep, {cat})_\n"


def section_bounds(lines):
    """Return (start_idx, end_idx) of the body of a `## Quotes` section, or None.

    start_idx = first body line after the header; end_idx = the boundary line
    (next `## ` heading) or len(lines) at EOF.
    """
    for i, ln in enumerate(lines):
        if ln.strip().lower() == '## quotes':
            j = i + 1
            while j < len(lines) and not lines[j].startswith('## '):
                j += 1
            return (i + 1, j)
    return None


def main():
    apply = '--apply' in sys.argv
    g = DEFAULT_GLOB
    if '--glob' in sys.argv:
        g = sys.argv[sys.argv.index('--glob') + 1]

    by_slug = {}
    unresolved = []
    for fp in sorted(glob.glob(str(ROOT / g))):
        for line in open(fp, encoding='utf-8'):
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            slug = e['target_node_slug']
            if slug not in NODE_FILES:
                unresolved.append((slug, e.get('source_ref', '')))
                continue
            by_slug.setdefault(slug, []).append(e)

    added_total = skipped_total = 0
    touched = 0
    for slug, entries in sorted(by_slug.items()):
        path = NODE_FILES[slug]
        text = path.read_text(encoding='utf-8')
        new_entries = [e for e in entries if e['quote'].strip() not in text]
        skipped = len(entries) - len(new_entries)
        skipped_total += skipped
        if not new_entries:
            print(f"  {slug:32s} +0  (skip {skipped} already present)")
            continue
        block = "\n".join(fmt_entry(e) for e in new_entries)
        lines = text.splitlines(keepends=True)
        bounds = section_bounds(lines)
        if bounds:
            _, end = bounds
            insert = ("\n" if end > 0 and lines[end - 1].strip() else "") + block + "\n"
            lines.insert(end, insert)
            new_text = "".join(lines)
        else:
            sep = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
            new_text = text + sep + "## Quotes\n\n" + block + "\n"
        added_total += len(new_entries)
        touched += 1
        print(f"  {slug:32s} +{len(new_entries)}  (skip {skipped})  -> {path.relative_to(ROOT)}")
        if apply:
            path.write_text(new_text, encoding='utf-8')

    print(f"\n{'APPLIED' if apply else 'DRY RUN'}: {added_total} quotes added across {touched} nodes; "
          f"{skipped_total} already-present skipped.")
    if unresolved:
        print(f"UNRESOLVED slugs ({len(unresolved)}) — no node, skipped:")
        for s, ref in unresolved:
            print(f"  {s}  ({ref})")
    if not apply:
        print("\n(dry run — pass --apply to write node files)")


if __name__ == '__main__':
    main()
