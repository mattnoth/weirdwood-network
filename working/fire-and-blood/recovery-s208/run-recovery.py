#!/usr/bin/env python3
"""run-recovery.py — S208 driver. For each unit with a recover map:
  1. fab-reconcile-candidates.py --recover <map> --out-dir out/<unit>
  2. mint_enrichment.py --candidates out/<unit>/candidates.json  (skipped when empty)
  3. fab_merge_node.py --merge-plan out/<unit>/merge-plan.json    (skipped when empty)
Collects a per-unit summary to recovery-run-report.json. Any step failure stops that
unit and is recorded; the driver continues with the next unit (CLAUDE.md rule 5).

Usage: run-recovery.py [unit ...]   (no args = every unit in recover-maps/)
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
MAPS = HERE / "recover-maps"
OUT = HERE / "out"
PROPOSALS = REPO / "extractions" / "fire-and-blood"

args = sys.argv[1:]
RECONCILE_ONLY = "--reconcile-only" in args
args = [a for a in args if a != "--reconcile-only"]
units = args or sorted(p.stem for p in MAPS.glob("*.json"))
report = []
for unit in units:
    map_path = MAPS / f"{unit}.json"
    if not map_path.exists():
        report.append({"unit": unit, "status": "no-map"})
        continue
    out_dir = OUT / unit
    entry = {"unit": unit, "status": "ok", "steps": {}}
    # 1. reconcile in recovery mode
    r = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "fab-reconcile-candidates.py"),
         "--proposal", str(PROPOSALS / f"{unit}.enrichment.md"),
         "--recover", str(map_path), "--out-dir", str(out_dir)],
        capture_output=True, text=True)
    entry["steps"]["reconcile"] = {"rc": r.returncode, "tail": r.stdout.strip().splitlines()[-8:] if r.stdout else [], "err": r.stderr.strip()[-400:]}
    if r.returncode != 0:
        entry["status"] = "reconcile-failed"
        report.append(entry)
        continue
    cands = json.loads((out_dir / "candidates.json").read_text(encoding="utf-8"))
    n_edges = len(cands["edges"])
    n_nodes = len(cands["_meta"].get("new_node_slugs", []))
    merge_plan = json.loads((out_dir / "merge-plan.json").read_text(encoding="utf-8"))
    entry["candidate_edges"] = n_edges
    entry["create_nodes"] = n_nodes
    entry["merge_entries"] = len(merge_plan)
    # 2. mint
    if RECONCILE_ONLY:
        entry["steps"]["mint"] = entry["steps"]["merge"] = "skipped-reconcile-only"
        report.append(entry)
        print(f"{unit}: reconciled  edges={n_edges} creates={n_nodes} merges={len(merge_plan)}")
        continue
    if n_edges or n_nodes:
        r = subprocess.run(
            [sys.executable, str(REPO / "scripts" / "mint_enrichment.py"),
             "--candidates", str(out_dir / "candidates.json")],
            capture_output=True, text=True)
        entry["steps"]["mint"] = {"rc": r.returncode, "tail": r.stdout.strip().splitlines()[-6:] if r.stdout else [], "err": r.stderr.strip()[-400:]}
        if r.returncode != 0:
            entry["status"] = "mint-failed"
            report.append(entry)
            continue
        for ln in (entry["steps"]["mint"]["tail"] or []):
            if ln.startswith("edges_appended="):
                entry["mint_result"] = ln
    else:
        entry["steps"]["mint"] = "skipped-empty"
    # 3. prose merges
    if merge_plan:
        r = subprocess.run(
            [sys.executable, str(REPO / "scripts" / "fab_merge_node.py"),
             "--merge-plan", str(out_dir / "merge-plan.json")],
            capture_output=True, text=True)
        entry["steps"]["merge"] = {"rc": r.returncode, "tail": r.stdout.strip().splitlines()[-4:] if r.stdout else [], "err": r.stderr.strip()[-400:]}
        if r.returncode != 0:
            entry["status"] = "merge-failed"
    else:
        entry["steps"]["merge"] = "skipped-empty"
    report.append(entry)
    print(f"{unit}: {entry['status']}  edges={n_edges} creates={n_nodes} merges={len(merge_plan)} {entry.get('mint_result','')}")

(HERE / "recovery-run-report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
fails = [e for e in report if e["status"] not in ("ok", "no-map")]
print(f"\n{len(report)} units, {len(fails)} failures -> recovery-run-report.json")
for e in fails:
    print(f"  FAIL {e['unit']}: {e['status']}")
