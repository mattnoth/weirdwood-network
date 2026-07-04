#!/usr/bin/env python3
"""build-chat-export.py — COMPAT SHIM.

Moved to graph/query/build/build_chat_bundle.py (query-layer Track, step 1,
S189/S190). This file just prints a deprecation pointer to stderr and delegates
to the new module's main() so any existing callers (docs, print-string
references in apply-parent-conflation.py / apply-node-merge-and-namesake.py /
backfill-epithet-aliases.py) keep working unchanged.

No behavior change: same CLI flags, same output files, same content.
"""

import sys
from pathlib import Path

print(
    "[deprecated] moved to graph/query/build/build_chat_bundle.py",
    file=sys.stderr,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "graph" / "query"))

from build.build_chat_bundle import main  # noqa: E402

if __name__ == "__main__":
    main()
