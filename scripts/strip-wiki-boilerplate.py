#!/usr/bin/env python3
"""Strip "from the AWOIAF wiki" boilerplate Identity lines from graph/nodes/.

Decision (advisory board synthesis, 2026-07-06):
  - RICH nodes (real content elsewhere in the body): strip the tail only,
    keep the sentence as "<Name> is a/an <type-gloss>." — cheap, reversible,
    no new claim, doesn't touch the type-gloss wording itself.
  - THIN nodes (Identity + Edges only, nothing else): drop the boilerplate
    line entirely, leaving the Identity section empty rather than a fake
    contentless stub. Humanizing the type-gloss and an LLM composer pass for
    thin nodes are explicitly OUT of scope here — parked as separate tracks.

Default is --dry-run (prints a sample + counts, writes nothing). Use --apply
to write changes. Never touches wiki_source/tier/cite_refs or any frontmatter.

Usage:
    python3 scripts/strip-wiki-boilerplate.py --dry-run
    python3 scripts/strip-wiki-boilerplate.py --apply
"""
import argparse
import re
import subprocess
from pathlib import Path

NODES_ROOT = Path("graph/nodes")

BOILERPLATE_LINE_RE = re.compile(r"^(.*?) (is an? )(.+?) from the AWOIAF wiki\.$")
RICH_SECTIONS_RE = re.compile(r"## (Appearances|Origins|Narrative Arc|Quotes|Description)")


def find_files():
    out = subprocess.run(
        ["grep", "-rl", "from the AWOIAF wiki", str(NODES_ROOT)],
        capture_output=True, text=True,
    ).stdout.splitlines()
    return sorted(out)


def process(path: str, apply: bool):
    """Returns (kind, before_line, after_line_or_None) — after=None means the
    line was dropped entirely (thin case)."""
    text = Path(path).read_text()
    is_rich = bool(RICH_SECTIONS_RE.search(text))

    lines = text.splitlines(keepends=True)
    out_lines = []
    before = after = None
    changed = False

    for line in lines:
        stripped = line.rstrip("\n")
        m = BOILERPLATE_LINE_RE.match(stripped)
        if m and before is None:
            before = stripped
            if is_rich:
                after = f"{m.group(1)} {m.group(2)}{m.group(3)}."
                out_lines.append(after + "\n")
            else:
                after = None
                # drop the line; also drop one adjacent blank line if this
                # leaves the ## Identity section with just blank lines
                changed = True
                continue
            changed = True
            continue
        out_lines.append(line)

    if not changed:
        return ("unmatched", None, None)

    new_text = "".join(out_lines)

    if not is_rich:
        # collapse the now-possibly-double-blank-line left where the
        # dropped sentence used to sit, right under "## Identity"
        new_text = re.sub(r"(## Identity\n)\n+(\n## )", r"\1\n\2", new_text)

    if apply:
        Path(path).write_text(new_text)

    return ("rich" if is_rich else "thin", before, after)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (default is dry-run)")
    ap.add_argument("--sample", type=int, default=15, help="how many sample rows to print in dry-run")
    args = ap.parse_args()

    files = find_files()
    counts = {"rich": 0, "thin": 0, "unmatched": 0}
    samples = {"rich": [], "thin": []}

    for f in files:
        kind, before, after = process(f, apply=args.apply)
        counts[kind] += 1
        if kind in samples and len(samples[kind]) < args.sample:
            samples[kind].append((f, before, after))

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode}] total files: {len(files)}")
    print(f"  rich (strip tail):  {counts['rich']}")
    print(f"  thin (drop line):   {counts['thin']}")
    print(f"  unmatched:          {counts['unmatched']}")

    if not args.apply:
        print("\n--- sample: rich (strip tail) ---")
        for f, before, after in samples["rich"]:
            print(f"{f}")
            print(f"  before: {before}")
            print(f"  after:  {after}")
        print("\n--- sample: thin (drop line) ---")
        for f, before, after in samples["thin"]:
            print(f"{f}")
            print(f"  before: {before}")
            print(f"  after:  (line removed, Identity section left empty)")


if __name__ == "__main__":
    main()
