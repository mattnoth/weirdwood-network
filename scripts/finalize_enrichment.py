#!/usr/bin/env python3
"""Parameterized enrichment finalizer — the ONE script every dip uses after fresh-verify (S158).

Replaces the ~13 disposable per-dip `finalize_<unit>_sNNN.py` scripts. Those applied the same shapes
of post-verify adjustment, varying only in DATA: which candidate_ids to drop, which notes to patch,
the verified_by stamp value, and any pre-existing-edge bug-fixes (drop / re-point). This tool reads
all of that from a `verdicts.json` and applies it. The historical per-dip finalizers are frozen in
`scripts/enrichment/archive/` (kept, never deleted).

Faithful reproduction: the mutations here are byte-identical to the per-dip finalizers (in-place note
replace, in-place pending->verified stamp, end-appended repoint_note). Validated S158 against the S157
euron finalize (note-patch E32 + 7 stamps) and the S156 dorne finalize (drop E15 + 2 note patches +
9 stamps + the garin-the-great bug drop/repoint). See `scripts/enrichment/README.md`.

DATA SCHEMA (verdicts.json):
    {
      "run_id": "euron-enrichment-s157",        # REQUIRED — the run these verdicts apply to
      "verified_by": "fresh-verify-s157",        # REQUIRED — stamp value for pending edges
      "drop": ["E15"],                           # OPTIONAL — candidate_ids (this run) to drop (fresh-verify REJECT)
      "note_patch": {"E1": "new note", ...},     # OPTIONAL — candidate_id -> replacement asserted_relation
      "bug_drop": [["src","TYPE","tgt"], ...],   # OPTIONAL — pre-existing edge triples to drop (any run)
      "bug_repoint": [                           # OPTIONAL — re-point pre-existing edges (any run)
        {"match": ["src","TYPE","tgt"], "new_target": "...", "note": "..."},
        {"match": ["src","TYPE","tgt"], "new_source": "...", "note": "..."}
      ]
    }
The verified_by stamp is applied to EVERY edge of `run_id` whose verified_by == "pending" (the edges
the mint flagged with `"verify": true`) — exactly as the per-dip finalizers did.

USAGE
  python scripts/finalize_enrichment.py --verdicts working/enrichment/<unit>/verdicts.json
  # validation:
  python scripts/finalize_enrichment.py --verdicts .../verdicts.json --edges /tmp/copy.jsonl --backup /tmp/bk.jsonl
"""
import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES_DEFAULT = REPO / "graph" / "edges" / "edges.jsonl"


def trip(r):
    return (r.get("source_slug"), r.get("edge_type"), r.get("target_slug"))


def main():
    ap = argparse.ArgumentParser(description="Parameterized enrichment finalizer (S158).")
    ap.add_argument("--verdicts", required=True, type=Path, help="path to a dip's verdicts.json")
    ap.add_argument("--edges", type=Path, default=EDGES_DEFAULT, help="edges.jsonl to mutate (override for validation)")
    ap.add_argument("--backup", type=Path, default=None, help="backup path (default: graph/edges/_regrounding/edges-pre-<unit>-finalize-<date>.jsonl)")
    args = ap.parse_args()

    v = json.loads(args.verdicts.read_text(encoding="utf-8"))
    run_id = v.get("run_id")
    verified_by = v.get("verified_by")
    if not run_id or not verified_by:
        sys.exit("ABORT: verdicts.json needs both run_id and verified_by.")

    drop_cids = set(v.get("drop", []))
    note_patch = v.get("note_patch", {})
    bug_drop = {tuple(t) for t in v.get("bug_drop", [])}
    repoints = v.get("bug_repoint", [])
    repoint_target = {tuple(r["match"]): r for r in repoints if "new_target" in r}
    repoint_source = {tuple(r["match"]): r for r in repoints if "new_source" in r}

    lines = [ln for ln in args.edges.read_text(encoding="utf-8").splitlines() if ln.strip()]
    rows = [json.loads(ln) for ln in lines]

    pending = [r for r in rows if r.get("run_id") == run_id and r.get("verified_by") == "pending"]
    bug_present = any(
        trip(r) in bug_drop or trip(r) in repoint_target or trip(r) in repoint_source for r in rows
    )
    if not pending and not bug_present:
        sys.exit("ABORT: nothing to do — finalize already applied (or mint missing).")

    backup = args.backup or (REPO / "graph" / "edges" / "_regrounding"
                             / f"edges-pre-{run_id.rsplit('-enrichment-', 1)[0]}-finalize-{date.today().isoformat()}.jsonl")
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.edges, backup)

    out = []
    n_drop = n_note = n_stamp = n_bugdrop = n_repoint = 0
    for r in rows:
        cid = r.get("candidate_id")
        rid = r.get("run_id")
        t = trip(r)

        # (A) drop fresh-verify rejects from this run
        if rid == run_id and cid in drop_cids:
            n_drop += 1
            continue

        # (B) drop pre-existing wrong-target edges
        if t in bug_drop:
            n_bugdrop += 1
            continue

        # (B) re-point pre-existing edges to a corrected node
        if t in repoint_target:
            spec = repoint_target[t]
            r["target_slug"] = spec["new_target"]
            if spec.get("note"):
                r["repoint_note"] = spec["note"]
            n_repoint += 1
        elif t in repoint_source:
            spec = repoint_source[t]
            r["source_slug"] = spec["new_source"]
            if spec.get("note"):
                r["repoint_note"] = spec["note"]
            n_repoint += 1

        # (A) note patches + verified_by stamp on this run's edges
        if rid == run_id:
            if cid in note_patch:
                r["asserted_relation"] = note_patch[cid]
                n_note += 1
            if r.get("verified_by") == "pending":
                r["verified_by"] = verified_by
                n_stamp += 1

        out.append(r)

    args.edges.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in out) + "\n", encoding="utf-8")
    print("── FINALIZE SUMMARY ──")
    print(f"  fresh-verify DROP:   {n_drop}")
    print(f"  note patches:        {n_note}")
    print(f"  verified_by stamps:  {n_stamp}")
    print(f"  bug DROP:            {n_bugdrop}")
    print(f"  bug REPOINT:         {n_repoint}")
    print(f"  rows: {len(rows)} -> {len(out)}")


if __name__ == "__main__":
    main()
