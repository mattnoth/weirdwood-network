#!/usr/bin/env python3
"""fab-s200-residue-fix.py — one-shot deterministic cleanup of the S200 F&B apply residue.

The 4 Fire & Blood smoke units were applied in S200 BEFORE the P1 VICTIM_IN harm-gate and
the P4 mint edge-dedup guard existed. Two residue classes remain in graph/edges/edges.jsonl,
both `evidence_kind == "book-fab"` (this is the sweep queued in worklog S200 / working/todos.md):

  1. VICTIM_IN edges whose target event is a NON-HARM subtype -> re-type to PARTICIPATES_IN.
     (You cannot be the "victim" of a coronation/birth/appointment/surrender/migration.)
  2. Exact duplicate edges (same edge_type/source_slug/target_slug/normalized evidence_quote)
     -> keep the first, drop the rest.

Scope is STRICTLY `evidence_kind == "book-fab"`. Pre-existing book-pass1 / book-pass1-reified
residue (the AGOT narrative-arc reification) is a separate, out-of-scope dataset and is NOT touched.

Reuses (import, no divergent copies): HARM_EVENT_SUBTYPES + classify_patient_edge_type from the
reconciler, and norm() from mint_enrichment for the dedup quote normalization.

Usage:
  python3 scripts/fab-s200-residue-fix.py            # dry-run (default): report only
  python3 scripts/fab-s200-residue-fix.py --apply    # backup + rewrite edges.jsonl
"""
import argparse
import glob
import json
import os
import re
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
EDGES = os.path.join(REPO, "graph", "edges", "edges.jsonl")

# --- reuse the reconciler's harm classification (no divergent list) ---
import importlib.util


def _load(modname, filename):
    spec = importlib.util.spec_from_file_location(modname, os.path.join(REPO, "scripts", filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_recon = _load("fab_reconcile_candidates", "fab-reconcile-candidates.py")
_mint = _load("mint_enrichment", "mint_enrichment.py")
HARM = set(_recon.HARM_EVENT_SUBTYPES)
_norm = _mint.norm


def event_subtype_map():
    """slug -> event subtype, scanning ALL node dirs."""
    sub = {}
    for f in glob.glob(os.path.join(REPO, "graph", "nodes", "**", "*.node.md"), recursive=True):
        slug = os.path.basename(f)[: -len(".node.md")]
        m = re.search(r"^type:\s*[\"']?event\.([a-z_-]+)", open(f).read(), re.M)
        if m:
            sub[slug] = m.group(1)
    return sub


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="rewrite edges.jsonl (default: dry-run)")
    args = ap.parse_args()

    sub = event_subtype_map()
    rows = [json.loads(l) for l in open(EDGES) if l.strip()]

    retyped = []      # (idx, source, target, subtype)
    dropped = []      # (idx, key)
    seen = {}         # dedup key -> first idx  (book-fab only)

    for i, e in enumerate(rows):
        if e.get("evidence_kind") != "book-fab":
            continue
        # (1) VICTIM_IN on non-harm event -> PARTICIPATES_IN
        if e.get("edge_type") == "VICTIM_IN":
            st = sub.get(e.get("target_slug"))
            if st is not None and st not in HARM:
                retyped.append((i, e.get("source_slug"), e.get("target_slug"), st))

    # (2) exact-dup book-fab edges (after the retype would still be same key modulo edge_type;
    #     compute on CURRENT rows — the harren dup is a KILLS dup, unaffected by retype)
    for i, e in enumerate(rows):
        if e.get("evidence_kind") != "book-fab":
            continue
        key = (e.get("edge_type"), e.get("source_slug"), e.get("target_slug"),
               _norm(e.get("evidence_quote") or ""))
        if key in seen:
            dropped.append((i, key))
        else:
            seen[key] = i

    print("=== S200 book-fab residue cleanup — %s ===" % ("APPLY" if args.apply else "DRY-RUN"))
    print("VICTIM_IN -> PARTICIPATES_IN (non-harm targets): %d" % len(retyped))
    for i, s, t, st in retyped:
        print("   [%d] %s -> %s  [event.%s]" % (i, s, t, st))
    print("duplicate book-fab edges to drop: %d" % len(dropped))
    for i, key in dropped:
        print("   [%d] %s %s -> %s" % (i, key[0], key[1], key[2]))

    if not args.apply:
        print("\nDRY-RUN — no files written. Re-run with --apply to backup + rewrite.")
        return

    # apply: retype in place, drop dup indices
    drop_idx = {i for i, _ in dropped}
    for i, _, _, _ in retyped:
        rows[i]["edge_type"] = "PARTICIPATES_IN"
        rows[i]["_s200_residue_fix"] = "victim_in->participates_in"
    out = [r for i, r in enumerate(rows) if i not in drop_idx]

    backup = EDGES.replace(".jsonl", "-pre-s200-residue-fix.jsonl")
    shutil.copy2(EDGES, backup)
    tmp = EDGES + ".tmp"
    with open(tmp, "w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, EDGES)
    print("\nAPPLIED. backup=%s  rows %d -> %d (retyped %d, dropped %d)"
          % (backup, len(rows), len(out), len(retyped), len(dropped)))


if __name__ == "__main__":
    main()
