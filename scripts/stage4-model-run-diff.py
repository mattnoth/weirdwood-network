#!/usr/bin/env python3
"""Diff two Stage-4 tail-classifier runs over the SAME candidate rows.

Use case: decide which model to run the remainder of a pass on. Run model A
(baseline) and model B (candidate) over the same deterministic first-N rows,
then compare their verdicts row-by-row.

Match key = (source_slug, target_slug, evidence_chapter, hint_raw). This tuple
is present on 100% of emit / rejected / classify_failed rows (evidence_ref is
NOT — it only exists on emit rows — so it cannot be the key).

Buckets (A = baseline, B = candidate):
  agree_same_type      both emit_edge, same edge_type
  agree_both_reject    both rejected
  B_over_emit          A rejected, B emit_edge        (graph-pollution risk)
  B_miss               A emit_edge, B rejected        (recall loss)
  both_typed_diff      both emit_edge, different type
  classify_failed_*    technical failure on either side (excluded from agreement %)

Agreement % = (agree_same_type + agree_both_reject) / comparable_overlap
where comparable_overlap excludes any pair with a classify_failed on either side.
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def load_run(run_dir: Path):
    """Return dict: key -> row (last-wins), plus dup count."""
    rows = {}
    dups = 0
    for kind in ("edges", "rejected", "classify_failed"):
        for path in sorted(run_dir.glob(f"**/*.{kind}.jsonl")):
            for line in path.read_text().splitlines():
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                key = (
                    r.get("source_slug"),
                    r.get("target_slug"),
                    r.get("evidence_chapter"),
                    r.get("hint_raw"),
                )
                if key in rows:
                    dups += 1
                rows[key] = r
    return rows, dups


def decision_of(r):
    d = r.get("decision")
    if d == "emit_edge":
        return ("emit", r.get("edge_type"))
    if d == "rejected":
        return ("reject", None)
    if d == "classify_failed":
        return ("fail", None)
    return ("unknown", None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-a", required=True, help="baseline run dir (e.g. Sonnet)")
    ap.add_argument("--run-b", required=True, help="candidate run dir (e.g. Haiku)")
    ap.add_argument("--label-a", default="A")
    ap.add_argument("--label-b", default="B")
    ap.add_argument("--show", type=int, default=20, help="max rows to list per divergence bucket")
    args = ap.parse_args()

    a_rows, a_dups = load_run(Path(args.run_a))
    b_rows, b_dups = load_run(Path(args.run_b))

    A, B = args.label_a, args.label_b
    overlap = sorted(set(a_rows) & set(b_rows))

    buckets = defaultdict(list)
    for key in overlap:
        da, ta = decision_of(a_rows[key])
        db, tb = decision_of(b_rows[key])
        if da == "fail" or db == "fail":
            buckets["classify_failed_either"].append((key, da, ta, db, tb))
        elif da == "emit" and db == "emit":
            if ta == tb:
                buckets["agree_same_type"].append((key, da, ta, db, tb))
            else:
                buckets["both_typed_diff"].append((key, da, ta, db, tb))
        elif da == "reject" and db == "reject":
            buckets["agree_both_reject"].append((key, da, ta, db, tb))
        elif da == "reject" and db == "emit":
            buckets[f"{B}_over_emit"].append((key, da, ta, db, tb))
        elif da == "emit" and db == "reject":
            buckets[f"{B}_miss"].append((key, da, ta, db, tb))
        else:
            buckets["other"].append((key, da, ta, db, tb))

    n_overlap = len(overlap)
    n_fail = len(buckets["classify_failed_either"])
    comparable = n_overlap - n_fail
    n_agree = len(buckets["agree_same_type"]) + len(buckets["agree_both_reject"])
    agree_pct = (100.0 * n_agree / comparable) if comparable else 0.0

    print(f"=== {A} ({len(a_rows)} rows, {a_dups} dup-keys) vs {B} ({len(b_rows)} rows, {b_dups} dup-keys) ===")
    print(f"overlap (matched keys): {n_overlap}")
    print(f"classify_failed on either side: {n_fail} (excluded from agreement)")
    print(f"comparable overlap: {comparable}")
    print()
    print(f"AGREEMENT: {n_agree}/{comparable} = {agree_pct:.1f}%")
    print(f"  agree_same_type   : {len(buckets['agree_same_type'])}")
    print(f"  agree_both_reject : {len(buckets['agree_both_reject'])}")
    print()
    print("DIVERGENCE:")
    print(f"  {B}_over_emit ({A} reject / {B} emit) : {len(buckets[B+'_over_emit'])}   <-- graph-pollution risk")
    print(f"  {B}_miss      ({A} emit / {B} reject) : {len(buckets[B+'_miss'])}")
    print(f"  both_typed_diff (emit, diff type)    : {len(buckets['both_typed_diff'])}")
    if buckets["other"]:
        print(f"  other                                : {len(buckets['other'])}")
    print()

    # emit-rate by run over the comparable overlap
    a_emit = sum(1 for k in overlap if decision_of(a_rows[k])[0] == "emit")
    b_emit = sum(1 for k in overlap if decision_of(b_rows[k])[0] == "emit")
    print(f"emit count over overlap: {A}={a_emit}  {B}={b_emit}")
    print()

    def dump(name):
        rows = buckets.get(name, [])
        if not rows:
            return
        print(f"--- {name} (showing up to {args.show} of {len(rows)}) ---")
        for key, da, ta, db, tb in rows[: args.show]:
            src, tgt, ch, hint = key
            hint_s = (hint or "")[:90].replace("\n", " ")
            print(f"  {src} -> {tgt} @{ch} | {A}:{ta or da} {B}:{tb or db}")
            print(f"      hint: {hint_s}")
        print()

    for name in (f"{B}_over_emit", f"{B}_miss", "both_typed_diff"):
        dump(name)

    # edge_type frequency for B's emits (sanity)
    from collections import Counter
    b_types = Counter(
        b_rows[k].get("edge_type") for k in overlap if decision_of(b_rows[k])[0] == "emit"
    )
    print(f"--- {B} edge_type distribution (over overlap emits) ---")
    for t, c in b_types.most_common():
        print(f"  {t}: {c}")


if __name__ == "__main__":
    main()
