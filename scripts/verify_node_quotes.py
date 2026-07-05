#!/usr/bin/env python3
"""verify_node_quotes.py — deterministic cite check for node `## Quotes` entries.

For every node (or a --slugs subset), parses the `## Quotes` section with the
REAL engine parser (`weirwood_query.load.parse_quotes` — what the bundle build
consumes) and, for each quote carrying a `sources/chapters/...md:N` cite,
verifies the normalized quote text appears in the normalized source window
(cited line .. +4 lines, blank lines dropped — handles couplets). Same norm()
family as scripts/quotecheck_enrichment.py.

Wiki-cited quotes (no navigable cite) are counted but not checked.

Usage:
    python3 scripts/verify_node_quotes.py                 # whole graph
    python3 scripts/verify_node_quotes.py --slugs a b c   # subset
    python3 scripts/verify_node_quotes.py --plan working/quote-census/s193-mint-plan.json
Exit 1 if any checked quote fails.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "graph" / "query"))
from weirwood_query.load import parse_quotes  # noqa: E402

NODES_DIR = REPO / "graph" / "nodes"
CITE_RE = re.compile(r"(sources/chapters/[a-z0-9/_-]+?\.md):(\d+)")
WINDOW = 5


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    return re.sub(r"\s+", " ", s).strip().lower()


def quotes_body(text: str) -> str:
    m = re.search(r"^## Quotes[ \t]*\n", text, re.M)
    if not m:
        return ""
    body = text[m.end():]
    nxt = re.search(r"^## ", body, re.M)
    return body[: nxt.start()] if nxt else body


def check_quote(cite: str, quote_text: str) -> tuple[bool, str]:
    m = CITE_RE.search(cite)
    if not m:
        return False, f"malformed cite {cite!r}"
    fpath, line = REPO / m.group(1), int(m.group(2))
    if not fpath.exists():
        return False, f"missing chapter file {m.group(1)}"
    src = fpath.read_text().splitlines()
    if line < 1 or line > len(src):
        return False, f"line {line} out of range ({len(src)} lines)"
    window = norm(" ".join(s for s in src[line - 1: line - 1 + WINDOW] if s.strip()))
    if norm(quote_text) in window:
        return True, ""
    # tolerate curator-added wrapping straight/curly quotes (presentation, not
    # drift — see working/quote-census/node-quote-drift-report.md class 1)
    if norm(quote_text.strip().strip('"“”').strip()) in window:
        return True, ""
    return False, "text not found at cited line"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slugs", nargs="*", default=None)
    ap.add_argument("--plan", help="mint-plan JSON; verify its slugs")
    args = ap.parse_args()

    slugs = set(args.slugs or [])
    if args.plan:
        slugs |= {r["slug"] for r in json.loads(Path(args.plan).read_text())}

    checked = passed = wiki_only = 0
    failures: list[str] = []
    for path in sorted(NODES_DIR.rglob("*.node.md")):
        if "_conflicts" in path.parts:
            continue
        slug = path.name.removesuffix(".node.md")
        if slugs and slug not in slugs:
            continue
        body = quotes_body(path.read_text())
        if not body:
            continue
        for q in parse_quotes(body):
            cite = q.get("cite")
            if not cite:
                wiki_only += 1
                continue
            checked += 1
            ok, why = check_quote(cite, q["text"])
            if ok:
                passed += 1
            else:
                failures.append(f"{slug}: {cite} — {why}: {q['text'][:80]!r}")

    print(f"checked {checked} book-cited quotes: {passed} pass, "
          f"{len(failures)} FAIL ({wiki_only} wiki-cited skipped)")
    for f in failures:
        print(f"  FAIL {f}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
