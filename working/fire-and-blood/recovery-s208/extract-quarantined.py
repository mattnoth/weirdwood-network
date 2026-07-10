#!/usr/bin/env python3
"""extract-quarantined.py — S208 review-bucket triage support.

For every quarantined reconcile-review NAME (across the 39 applied units), pull the
proposal rows that reference it: relationship edges, Events-of-Note rows (event name
itself quarantined), and event role references (agent/patient person quarantined).
These are exactly the rows the S201/S202 bulk apply dropped.

Pure deterministic Python; reuses the reconciler's own parsers so row semantics match.

OUTPUT (into this dir):
  quarantined-rows.json    — {unit: {name: {reasons, rel_rows, event_rows, role_refs}}}
  name-summary.tsv         — one line per (name, reason-class): units, row counts, edge counts
"""
import json
import sys
import importlib.util
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
APPLY = REPO / "working" / "fire-and-blood" / "apply"
PROPOSALS = REPO / "extractions" / "fire-and-blood"

spec = importlib.util.spec_from_file_location(
    "fabrec", REPO / "scripts" / "fab-reconcile-candidates.py")
fabrec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fabrec)

# ---- load review rows ----
review = defaultdict(dict)  # unit -> name -> [reasons]
for f in sorted(APPLY.glob("*/reconcile-review.jsonl")):
    for line in f.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        name = r.get("name")
        if name is None:  # e.g. the in_universe_source enum row
            continue
        review[r["unit"]].setdefault(name, []).append(r.get("reason") or "?")

out = {}
per_name = defaultdict(lambda: {"units": set(), "reasons": set(),
                                "rel_rows": 0, "event_rows": 0, "role_refs": 0})

for unit, names in sorted(review.items()):
    proposal = PROPOSALS / f"{unit}.enrichment.md"
    if not proposal.exists():
        print(f"WARNING: proposal missing for {unit}", file=sys.stderr)
        continue
    sections = fabrec.split_sections(proposal.read_text(encoding="utf-8"))
    rels = fabrec.parse_relationships(sections.get("Relationships Observed", ""))
    events = fabrec.parse_events(sections.get("Events of Note", ""))
    qnames = set(names)
    unit_out = {}
    for name in qnames:
        entry = {"reasons": sorted(set(names[name])), "rel_rows": [], "event_rows": [], "role_refs": []}
        for rel in rels:
            if rel["source_name"] == name or rel["target_name"] == name:
                entry["rel_rows"].append({
                    "source": rel["source_name"], "type": rel["edge_type"],
                    "qualifier": rel["qualifier"], "target": rel["target_name"],
                    "quote": rel["quote"][:120]})
        for ev in events:
            persons = [p for f_ in ("agent", "patient")
                       for p in fabrec.split_entities(ev[f_])]
            if ev["name"] == name:
                entry["event_rows"].append({
                    "event": ev["name"], "type": ev["type"], "year": ev["year"],
                    "agent": ev["agent"], "patient": ev["patient"],
                    "outcome": ev["outcome"][:120], "quote": ev["quote"][:120],
                    "disputed": ev["disputed"]})
            elif name in persons:
                entry["role_refs"].append({
                    "event": ev["name"], "role": "agent" if name in fabrec.split_entities(ev["agent"]) else "patient",
                    "quote": ev["quote"][:120]})
        unit_out[name] = entry
        s = per_name[name]
        s["units"].add(unit)
        s["reasons"] |= set(names[name])
        s["rel_rows"] += len(entry["rel_rows"])
        s["event_rows"] += len(entry["event_rows"])
        s["role_refs"] += len(entry["role_refs"])
    out[unit] = unit_out

(HERE / "quarantined-rows.json").write_text(
    json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

lines = ["name\treasons\tn_units\trel_rows\tevent_rows\trole_refs"]
for name, s in sorted(per_name.items(), key=lambda kv: -(kv[1]["rel_rows"] + kv[1]["event_rows"] + kv[1]["role_refs"])):
    lines.append(f"{name}\t{';'.join(sorted(s['reasons']))}\t{len(s['units'])}"
                 f"\t{s['rel_rows']}\t{s['event_rows']}\t{s['role_refs']}")
(HERE / "name-summary.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")

n_edges = sum(s["rel_rows"] + s["role_refs"] for s in per_name.values())
n_events = sum(s["event_rows"] for s in per_name.values())
print(f"names: {len(per_name)}  units: {len(out)}")
print(f"quarantined rel-rows+role-refs (edge-shaped): {n_edges}   event rows: {n_events}")
