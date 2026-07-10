#!/usr/bin/env python3
"""s207-dedup-quotes-headers.py — merge duplicate `## Quotes` sections into one.

S205 finding: ~84 nodes carry TWO `## Quotes` headers. The chat bundle's `parse_quotes`
reads only the FIRST section, so the second is invisible — either a redundant exact copy
(39 nodes) or a genuinely different quote set the bundle silently drops (45 nodes).

Fix: for any node with 2+ `## Quotes` sections, merge them into ONE section placed where the
first one was, unioning quote lines (dedup by normalized text, preserving order + blank-line
structure), and delete the trailing sections. Every OTHER section + the frontmatter is byte-
preserved. Union is at NON-BLANK-LINE granularity — lossless except for exact-duplicate lines.

Safety: a per-file assertion guarantees the set of unique normalized quote lines in the output
equals the union across all input blocks (no unique quote is ever lost). Files are git-tracked
(git is the backup).

Usage:
  python3 scripts/s207-dedup-quotes-headers.py            # dry-run (default)
  python3 scripts/s207-dedup-quotes-headers.py --apply    # rewrite the node files
"""
import argparse
import glob
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODES = os.path.join(REPO, "graph", "nodes")

BLOCK_RE = re.compile(r'(?m)^## Quotes(?: \(continued\))?[ \t]*\n')


def norm(line):
    return re.sub(r'\s+', ' ', line.strip())


def find_blocks(text):
    """Return [(start, end, body)] for each '## Quotes' section (body excludes the header line)."""
    blocks = []
    for m in BLOCK_RE.finditer(text):
        body_start = m.end()
        nxt = re.search(r'(?m)^## ', text[body_start:])
        end = body_start + nxt.start() if nxt else len(text)
        blocks.append((m.start(), end, text[body_start:end]))
    return blocks


def union_lines(bodies):
    seen, out = set(), []
    for body in bodies:
        for line in body.split("\n"):
            k = norm(line)
            if not k:
                if out and out[-1] != "":
                    out.append("")   # collapse consecutive blanks
                continue
            if k in seen:
                continue
            seen.add(k)
            out.append(line.rstrip())
    while out and out[0] == "":
        out.pop(0)
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out), seen


def process(text):
    blocks = find_blocks(text)
    if len(blocks) < 2:
        return None
    merged, out_keys = union_lines([b[2] for b in blocks])
    # data-loss guard: every unique non-blank line across inputs survives
    in_keys = {norm(l) for _, _, b in blocks for l in b.split("\n") if norm(l)}
    assert out_keys == in_keys, "QUOTE LOST during merge"

    first_start = blocks[0][0]
    new = text
    for s, e, _ in reversed(blocks):        # remove every block region (right-to-left)
        new = new[:s] + new[e:]
    insert = "## Quotes\n\n" + merged + "\n"
    # ensure a blank line before any following section
    tail = new[first_start:]
    if tail.strip():
        insert += "\n"
    new = new[:first_start] + insert + tail
    return new, len(blocks), len(in_keys)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    changed = []
    for f in sorted(glob.glob(os.path.join(NODES, "**", "*.node.md"), recursive=True)):
        text = open(f, encoding="utf-8").read()
        res = process(text)
        if res is None:
            continue
        new, nblocks, nquotes = res
        # classify: exact-dup if every block body is identical (only redundant copies)
        blocks = find_blocks(text)
        bodies = [b[2] for b in blocks]
        is_exact = all(norm(bodies[0]) == norm(b) for b in bodies)
        changed.append((os.path.relpath(f, REPO), nblocks, nquotes, "exact-dup" if is_exact else "union"))
        if args.apply:
            open(f, "w", encoding="utf-8").write(new)

    print("=== S207 dup-Quotes dedup — %s ===" % ("APPLY" if args.apply else "DRY-RUN"))
    print("nodes with 2+ ## Quotes merged: %d" % len(changed))
    ex = [c for c in changed if c[3] == "exact-dup"]
    un = [c for c in changed if c[3] == "union"]
    print("  exact-duplicate (2nd copy dropped): %d" % len(ex))
    print("  union-merge (distinct quotes surfaced): %d" % len(un))
    print("\n-- union-merge nodes (2nd section had NEW quotes now surfaced) --")
    for path, nb, nq, _ in un:
        print("   %-60s %d blocks -> %d unique quotes" % (path.replace("graph/nodes/", ""), nb, nq))
    if not args.apply:
        print("\nDRY-RUN — no files written. Re-run with --apply.")


if __name__ == "__main__":
    main()
