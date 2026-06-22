#!/usr/bin/env python3
"""AEGON build A3 (S128): container retags for the Stormlands-campaign fan.

The 6 simultaneous takings + the Rhoyne stone-men incident are AEGON-internal
but were minted untagged; the Storm's End siege is an AEGON-WO5K seam. Add the
`containers:` frontmatter tag (an array tag, NOT an umbrella node) so they are
retrievable via `graph-query.py --container aegon`.

  6 takings + stone-men   -> containers: [aegon]
  siege-of-storms-end-300 -> containers: [aegon, wo5k]   (seam, dual-tag)

Inserts the field immediately after the `slug:` line (the node convention, cf.
landing-of-the-golden-company). Idempotent: skips any node that already carries a
`containers:` line. NO causal edges are added here (PART_OF is the correct + complete
structure for the sibling takings — adding CAUSES between them is a granularity overclaim).
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EVENTS = REPO / "graph" / "nodes" / "events"

AEGON_ONLY = [
    "fall-of-mistwood",
    "invasion-of-tarth",
    "taking-of-crows-nest",
    "taking-of-greenstone",
    "taking-of-griffins-roost",
    "taking-of-rain-house",
    "stone-men-attack-the-shy-maid",
]
SEAM = {"siege-of-storms-end-300": "[aegon, wo5k]"}


def retag(slug, value):
    path = EVENTS / f"{slug}.node.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    if any(ln.strip().startswith("containers:") for ln in lines):
        print(f"  SKIP (already tagged)  {slug}")
        return False
    out, inserted = [], False
    for ln in lines:
        out.append(ln)
        if not inserted and ln.strip().startswith("slug:"):
            out.append(f"containers: {value}")
            inserted = True
    if not inserted:
        print(f"  WARN no slug: line     {slug} — NOT tagged")
        return False
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"  TAGGED {value:14s}  {slug}")
    return True


def main():
    n = 0
    for slug in AEGON_ONLY:
        n += retag(slug, "[aegon]")
    for slug, value in SEAM.items():
        n += retag(slug, value)
    print(f"\nRetagged {n} nodes.")


if __name__ == "__main__":
    main()
