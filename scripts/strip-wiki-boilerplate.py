#!/usr/bin/env python3
"""Strip "from the AWOIAF wiki" boilerplate Identity lines from graph/nodes/.

Decision (Matt, S210 — supersedes the 2026-07-06 board synthesis):
  DROP the boilerplate Identity line entirely for EVERY node, leaving the
  `## Identity` section empty. Rationale: the live chat-UI already suppresses
  the wiki-tail form (`web/public/app.js` `isWikiBoilerplate`) so the phrase is
  invisible today — it lives only in the data. The board's original "rich nodes
  keep a stripped `<Name> is a <type>.` stub" would NEWLY SURFACE ~5,300
  contentless stubs (some with raw types like `organization.house`) into the
  dossier, a regression. An empty identity renders as nothing (the node's type
  is already shown via the card subtitle), so dropping cleans the data with zero
  UI change. The rich/thin split is kept for REPORTING only (how many nodes had
  real content elsewhere vs. were Identity+Edges-only).

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
# A node is THIN iff its ONLY top-level sections are Identity + Edges (docstring
# intent). Classify RICH by the presence of ANY other `## ` section — a complete,
# future-proof test that supersedes the old hardcoded allowlist (which missed
# Culture / Aftermath / Heraldry & Sigil / Fire & Blood / Organization / … — the
# "46-node misclassification nit" and then some). "(continued)" suffixes and the
# Identity/Edges base headings are excluded.
SECTION_HEADING_RE = re.compile(r"^## (.+?)\s*$", re.M)
_STRUCTURAL_HEADINGS = {"Identity", "Edges"}


def _base_heading(h: str) -> str:
    return re.sub(r"\s*\(cont.*?\)\s*$", "", h).strip()


def has_content_section(text: str) -> bool:
    for m in SECTION_HEADING_RE.finditer(text):
        if _base_heading(m.group(1)) not in _STRUCTURAL_HEADINGS:
            return True
    return False


def find_files():
    out = subprocess.run(
        ["grep", "-rl", "from the AWOIAF wiki", str(NODES_ROOT)],
        capture_output=True, text=True,
    ).stdout.splitlines()
    return sorted(out)


def process(path: str, apply: bool):
    """Drop the boilerplate Identity line entirely (S210 decision). Returns
    (kind, before_line, None) — kind is 'rich'/'thin' for reporting only; the
    action is the same (drop) for both."""
    text = Path(path).read_text()
    is_rich = has_content_section(text)

    lines = text.splitlines(keepends=True)
    out_lines = []
    before = None
    changed = False

    for line in lines:
        stripped = line.rstrip("\n")
        m = BOILERPLATE_LINE_RE.match(stripped)
        if m and before is None:
            before = stripped
            changed = True
            continue  # drop the line entirely, for EVERY node
        out_lines.append(line)

    if not changed:
        return ("unmatched", None, None)

    new_text = "".join(out_lines)
    # normalize the now-empty Identity section: exactly one blank line between the
    # `## Identity` heading and the next `## ` heading (or EOF) — no stray blanks.
    new_text = re.sub(r"(## Identity\n)\n+(?=(## |\Z))", r"\1\n", new_text)

    if apply:
        Path(path).write_text(new_text)

    return ("rich" if is_rich else "thin", before, None)


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
    print(f"[{mode}] total files: {len(files)}   (action: DROP the line for all)")
    print(f"  rich (had content, line dropped, section left empty):  {counts['rich']}")
    print(f"  thin (Identity+Edges only, line dropped):              {counts['thin']}")
    print(f"  unmatched:                                             {counts['unmatched']}")

    if not args.apply:
        for kind in ("rich", "thin"):
            print(f"\n--- sample: {kind} (line removed, Identity section left empty) ---")
            for f, before, _ in samples[kind]:
                print(f"{f}")
                print(f"  before: {before}")
                print(f"  after:  (line removed)")


if __name__ == "__main__":
    main()
