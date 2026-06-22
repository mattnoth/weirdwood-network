#!/usr/bin/env python3
"""Shared helpers for arc/edge mint scripts — the slug pre-check floor.

The S120 advisory board (process-hardening lens) asked for a slug-existence +
alias-resolution pre-check in the mint-script template, to catch the
`daznak-s-pit` vs `daznaks-pit` class of dedup-miss BEFORE edges land. Call
`precheck_slugs(...)` in any mint script before appending edges:

    from mint_arc_lib import precheck_slugs
    resolved, missing = precheck_slugs({src, tgt for every edge})
    if missing:
        sys.exit(f"ABORT: slug pre-check failed: {missing}")

A slug "resolves" if EITHER (a) a node file `graph/nodes/**/<slug>.node.md`
exists, OR (b) the event alias resolver maps it (as slug or normalized phrase)
to a real canonical node. NOTE (calibration, per the board): this catches
non-existent targets only — it does NOT catch a *wrong-but-existing* target
(the S116 `anarchy-in-the-reach` mis-apply). That stays the research/verify
subagent's job. This is a cheap floor, not a cure-all.

CLI:  python scripts/mint_arc_lib.py <slug> [<slug> ...]   # exit 1 if any missing
"""
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

REPO_DEFAULT = Path(__file__).resolve().parent.parent
ALIAS_LOOKUP_REL = "working/wiki/data/event-alias-lookup.json"


def _normalize(phrase: str) -> str:
    """Lowercase + collapse whitespace. Keeps hyphens (matches resolver keys,
    which store both spaced and kebab variants)."""
    return re.sub(r"\s+", " ", phrase.strip().lower())


@lru_cache(maxsize=8)
def _node_slugs(repo_root: str) -> frozenset[str]:
    nodes = Path(repo_root) / "graph" / "nodes"
    return frozenset(
        p.name[: -len(".node.md")] for p in nodes.glob("**/*.node.md")
    )


@lru_cache(maxsize=8)
def _alias_index(repo_root: str) -> tuple[frozenset[str], dict]:
    """Return (canonical_slugs, alias_to_canonical) from the event alias lookup.
    Missing file → empty (node-file check still works)."""
    path = Path(repo_root) / ALIAS_LOOKUP_REL
    if not path.exists():
        return frozenset(), {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return frozenset(), {}
    a2c = data.get("alias_to_canonical", {}) if isinstance(data, dict) else {}
    canon = frozenset(a2c.values())
    return canon, a2c


def resolve_slug(slug: str, *, repo_root=None) -> tuple[bool, str | None]:
    """Return (resolved, canonical_or_None). `canonical` is the slug the input
    maps to (== slug itself for a direct node-file hit)."""
    root = str(repo_root or REPO_DEFAULT)
    if slug in _node_slugs(root):
        return True, slug
    canon, a2c = _alias_index(root)
    if slug in canon:
        return True, slug
    norm = _normalize(slug)
    if norm in a2c:
        return True, a2c[norm]
    return False, None


def precheck_slugs(slugs, *, repo_root=None) -> tuple[list[str], list[str]]:
    """Validate an iterable of slugs. Returns (resolved, missing), both sorted."""
    resolved, missing = [], []
    for s in sorted(set(slugs)):
        ok, _ = resolve_slug(s, repo_root=repo_root)
        (resolved if ok else missing).append(s)
    return resolved, missing


def main() -> None:
    args = sys.argv[1:]
    if not args:
        sys.exit("usage: mint_arc_lib.py <slug> [<slug> ...]")
    resolved, missing = precheck_slugs(args)
    for s in resolved:
        _, canon = resolve_slug(s)
        note = "" if canon == s else f"  (resolves -> {canon})"
        print(f"  OK       {s}{note}")
    for s in missing:
        print(f"  MISSING  {s}")
    print(f"\n{len(resolved)} resolved · {len(missing)} missing")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
