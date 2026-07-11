"""Regression guard (S210): the "from the AWOIAF wiki" boilerplate stays stripped.

S210 dropped this auto-generated placeholder Identity line from all 6,481 nodes
(Matt: "strip it everywhere"). ~20 dormant Pass-2 emitter scripts still contain
the f-string that once produced it (full list in working/todos.md). Rather than
patch those retired generators, we enforce the invariant at the data layer: if
anything ever reintroduces the phrase onto a node file, the suite fails loudly —
catching the whole regression class regardless of source.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NODES_ROOT = REPO / "graph" / "nodes"
PHRASE = "from the AWOIAF wiki"


def test_no_wiki_boilerplate_in_nodes():
    offenders = [
        str(p.relative_to(REPO))
        for p in NODES_ROOT.rglob("*.node.md")
        if PHRASE in p.read_text(encoding="utf-8")
    ]
    assert not offenders, (
        f"{len(offenders)} node(s) reintroduced the '{PHRASE}' boilerplate that "
        f"S210 stripped everywhere. A retired Pass-2 emitter likely ran (list in "
        f"working/todos.md) — re-run scripts/strip-wiki-boilerplate.py --apply and "
        f"patch the emitter. First offenders: {offenders[:5]}"
    )
