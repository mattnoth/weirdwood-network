#!/usr/bin/env python3
"""
apply-parent-conflation.py — apply the AUTO-APPLY (provably-safe) PARENT_OF deletes.

Reads the proposal `working/graph-cleanup/parent-edge-proposal.jsonl` and deletes ONLY
the three review-cleared, delete-only classes from the source-of-truth edge store
`graph/edges/edges.jsonl`:

  EXACT_DUP_EDGE        remove all-but-one copy of an identical (src,tgt) PARENT_OF row
  REDUNDANT_CHILD_STUB  remove edge into a bare bucket that a disambiguated variant carries
  HOUSE_AS_PARENT       remove a House-node-as-parent edge (a House can't be a parent)

Twice cold-reviewed safe (working/graph-cleanup/{cold-review-verdict,
deletion-safety-and-alias-review}.md): edge-only, no node removed, each child keeps its
correct <=2 real parents. Fully recoverable — edges.jsonl is git-tracked.

DUPLICATE_PARENT_NODE / WRONG_NAMESAKE / NODE_SPLIT are NOT touched here (they need the
deferred node-merge / node-split tracks).

Default is DRY-RUN. Pass --apply to write. Prints a per-class tally and asserts exactly
the expected number of rows are removed.

  python3 scripts/apply-parent-conflation.py            # dry run
  python3 scripts/apply-parent-conflation.py --apply    # write edges.jsonl
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph/edges/edges.jsonl"
PROPOSAL = REPO / "working/graph-cleanup/parent-edge-proposal.jsonl"

AUTO_CLASSES = {"EXACT_DUP_EDGE", "REDUNDANT_CHILD_STUB", "HOUSE_AS_PARENT"}


def load_proposal():
    """Return (full_delete_pairs, exact_dup_pairs, class_counts).

    full_delete_pairs: {(parent, child)} -> remove EVERY matching PARENT_OF row.
    exact_dup_pairs:    {(parent, child)} -> remove all-but-one matching row.
    """
    full, exact = set(), set()
    counts = Counter()
    for line in PROPOSAL.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        cls = r["edge_class"]
        if cls not in AUTO_CLASSES:
            continue
        counts[cls] += 1
        pair = (r["parent"], r["child"])
        if cls == "EXACT_DUP_EDGE":
            exact.add(pair)
        else:
            full.add(pair)
    return full, exact, counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write edges.jsonl (default: dry run)")
    args = ap.parse_args()

    full, exact, counts = load_proposal()
    expected = sum(counts.values())
    print("AUTO-APPLY classes to delete:")
    for cls in ("EXACT_DUP_EDGE", "REDUNDANT_CHILD_STUB", "HOUSE_AS_PARENT"):
        print(f"  {cls:22s} {counts[cls]}")
    print(f"  {'TOTAL rows expected':22s} {expected}\n")

    kept, removed = [], []
    exact_seen = set()
    with EDGES.open(encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            e = json.loads(s)
            if e.get("edge_type") == "PARENT_OF":
                pair = (e.get("source_slug"), e.get("target_slug"))
                if pair in full:
                    removed.append((e, "full")); continue
                if pair in exact:
                    if pair in exact_seen:
                        removed.append((e, "exact-dup")); continue
                    exact_seen.add(pair)   # keep the FIRST copy
            kept.append(line if line.endswith("\n") else line + "\n")

    rem_by = Counter(tag for _, tag in removed)
    print(f"rows removed: {len(removed)}  (full={rem_by['full']}, exact-dup={rem_by['exact-dup']})")
    print(f"rows kept:    {len(kept)}")

    # safety asserts
    if len(removed) != expected:
        print(f"\nABORT: removed {len(removed)} != expected {expected}. No write.", file=sys.stderr)
        # show any full-delete pair that matched 0 or >1 rows
        matched = Counter((e['source_slug'], e['target_slug']) for e, t in removed if t == 'full')
        for pair in full:
            if matched[pair] != 1:
                print(f"  full-delete pair {pair} matched {matched[pair]} rows", file=sys.stderr)
        sys.exit(1)

    if not args.apply:
        print("\nDRY RUN — no file written. Re-run with --apply to commit.")
        # show a few removed rows for eyeballing
        for e, tag in removed[:6]:
            print(f"  [{tag}] {e['source_slug']} -> {e['target_slug']}")
        return

    EDGES.write_text("".join(kept), encoding="utf-8")
    print(f"\nWROTE {EDGES.relative_to(REPO)} — {len(kept)} PARENT_OF+other rows retained, "
          f"{len(removed)} deleted.")
    print("Next: rebuild bundle (graph/query/build/build_chat_bundle.py) + indexes (weirwood refresh).")


if __name__ == "__main__":
    main()
