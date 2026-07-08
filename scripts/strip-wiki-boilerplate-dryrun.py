#!/usr/bin/env python3
"""Dry-run scope + preview for stripping "from the AWOIAF wiki" boilerplate
Identity lines from graph/nodes/. Read-only: writes only a report under
working/node-enrichment-wiki-prose/. Does NOT touch graph/nodes/.

Usage:
    python3 scripts/strip-wiki-boilerplate-dryrun.py
"""
import re
import subprocess
from collections import defaultdict
from pathlib import Path

NODES_ROOT = Path("graph/nodes")
OUT = Path("working/node-enrichment-wiki-prose/strip-boilerplate-dryrun.md")

BOILERPLATE_RE = re.compile(r"^(.*?) is an? (.+?) from the AWOIAF wiki\.$")
RICH_SECTIONS_RE = re.compile(r"## (Appearances|Origins|Narrative Arc|Quotes|Description)")


def find_files():
    out = subprocess.run(
        ["grep", "-rl", "from the AWOIAF wiki", str(NODES_ROOT)],
        capture_output=True, text=True,
    ).stdout.splitlines()
    return sorted(out)


def type_dir(path: str) -> str:
    parts = Path(path).relative_to(NODES_ROOT).parts
    return parts[0]


def main():
    files = find_files()
    thin_samples = defaultdict(list)
    rich_samples = defaultdict(list)
    thin_count = 0
    rich_count = 0
    gloss_counts = defaultdict(int)
    no_match = []

    for f in files:
        text = Path(f).read_text()
        line = None
        for l in text.splitlines():
            m = BOILERPLATE_RE.match(l.strip())
            if m:
                line = l.strip()
                name, gloss = m.group(1), m.group(2)
                gloss_counts[gloss] += 1
                break
        if line is None:
            no_match.append(f)
            continue

        is_rich = bool(RICH_SECTIONS_RE.search(text))
        td = type_dir(f)
        strip_shape = f"{name} is a {gloss}." if not gloss.startswith("an ") else line
        # Build "Shape A" (strip tail only) preserving original article word
        m2 = re.match(r"^(.*?) (is an? )(.+?) from the AWOIAF wiki\.$", line)
        shape_a = f"{m2.group(1)} {m2.group(2)}{m2.group(3)}." if m2 else None

        entry = {"file": f, "original": line, "shape_a": shape_a}
        if is_rich:
            rich_count += 1
            if len(rich_samples[td]) < 3:
                rich_samples[td].append(entry)
        else:
            thin_count += 1
            if len(thin_samples[td]) < 3:
                thin_samples[td].append(entry)

    lines = []
    lines.append("# Strip-boilerplate dry-run report (read-only, no graph writes)\n")
    lines.append(f"Total nodes with boilerplate: **{len(files)}**")
    lines.append(f"- Rich (has other body content already): **{rich_count}**")
    lines.append(f"- Thin (Identity+Edges only, nothing else): **{thin_count}**")
    if no_match:
        lines.append(f"- Unparsed (phrase present but regex didn't match — check manually): {len(no_match)}")
        for f in no_match[:10]:
            lines.append(f"  - {f}")
    lines.append("")

    lines.append("## Type-gloss variants (count)\n")
    for gloss, n in sorted(gloss_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- {n:5d}  {gloss}")
    lines.append("")

    lines.append("## RICH nodes — Shape A (strip tail only) sample rows\n")
    lines.append("These already have real body content below Identity; stripping the tail leaves a harmless one-line stub.\n")
    for td, entries in sorted(rich_samples.items()):
        lines.append(f"### {td}")
        for e in entries:
            lines.append(f"- `{e['file']}`")
            lines.append(f"  - before: {e['original']}")
            lines.append(f"  - after:  {e['shape_a']}")
        lines.append("")

    lines.append("## THIN nodes — Shape A vs alternatives (Matt's decision)\n")
    lines.append("These have NOTHING else in the node body — Identity + Edges only. Shape A leaves a contentless")
    lines.append("one-line stub; alternatives are dropping the line entirely or composing a real sentence (LLM, later).\n")
    for td, entries in sorted(thin_samples.items()):
        lines.append(f"### {td}")
        for e in entries:
            lines.append(f"- `{e['file']}`")
            lines.append(f"  - before:   {e['original']}")
            lines.append(f"  - Shape A (strip tail):  {e['shape_a']}")
            lines.append(f"  - Shape B (drop line):   *(Identity section left empty)*")
        lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines))
    print(f"Wrote {OUT}")
    print(f"Total: {len(files)}  rich: {rich_count}  thin: {thin_count}  unparsed: {len(no_match)}")


if __name__ == "__main__":
    main()
