#!/usr/bin/env python3
"""S213 roles round 2 — adjudication prep: merge proposals + verdicts, reconcile
counts, run the STANDING deterministic audits, and print every row needing an
orchestrator decision. Read-only; the orchestrator writes ADJUDICATION-s213.md."""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

HARM_EVENT_SUBTYPES = {
    "death", "execution", "murder", "assassination", "poisoning", "maiming", "torture",
    "capture", "imprisonment", "battle", "sack", "destruction", "suicide", "stillbirth",
    "betrayal", "raid", "attack", "duel", "deception", "mutiny", "massacre", "abduction",
    "wounding",
}

# node subtype per event from the packets
subtype = {}
for i in range(1, 5):
    d = json.loads((OUT / f"packets/packets-{i}.json").read_text())
    for p in d["packets"]:
        subtype[p["slug"]] = p["node_type"]

rows = {}
for i in range(1, 5):
    d = json.loads((OUT / f"proposals/proposals-chunk{i}.json").read_text())
    for r in d["candidates"]:
        rows[r["id"]] = r
    print(f"chunk{i}: {len(d['candidates'])} candidates, "
          f"{len(d.get('wiki_only', []))} wiki_only, {len(d.get('no_node', []))} no_node, "
          f"{len(d.get('flags', []))} flags")

verdicts = {}
for i in range(1, 5):
    d = json.loads((OUT / f"verify/verdicts-chunk{i}.json").read_text())
    for v in d["verdicts"]:
        verdicts[v["id"]] = v

print(f"\ncandidate rows: {len(rows)}; verdict rows: {len(verdicts)}")
missing_verdict = sorted(set(rows) - set(verdicts))
orphan_verdict = sorted(set(verdicts) - set(rows))
if missing_verdict:
    print(f"!! candidates with NO verdict: {missing_verdict}")
if orphan_verdict:
    print(f"!! verdicts with no candidate: {orphan_verdict}")

print("\n=== non-CONFIRM rows (adjudicate each) ===")
for vid, v in sorted(verdicts.items()):
    if v["verdict"] != "CONFIRM":
        r = rows.get(vid, {})
        print(f"\n{vid} [{v['verdict']}] {v.get('reason','')} — {v.get('note','')}")
        print(f"   {r.get('type')} {r.get('source')} -> {r.get('target')} "
              f"({r.get('book')}/{r.get('chapter')}) tier={r.get('tier')}")
        print(f"   quote: {r.get('quote','')[:140]}")
        print(f"   note: {r.get('note','')}")

print("\n=== STANDING AUDIT 1: kept VICTIM_IN targets must be harm subtypes ===")
bad = 0
for vid, r in sorted(rows.items()):
    if r["type"] != "VICTIM_IN":
        continue
    st = subtype.get(r["target"], "?")
    base = st.split(".", 1)[1] if "." in st else st
    ok = base in HARM_EVENT_SUBTYPES
    if not ok:
        bad += 1
    print(f"  {vid} {r['source']} VICTIM_IN {r['target']} [{st}] "
          f"{'OK' if ok else '<<< HARM-GATE FAIL'}")
print(f"  harm-gate failures: {bad}")

print("\n=== STANDING AUDIT 2: (source,target,type) vs prior adjudications + existing edges ===")
pairs = {(r["source"], r["target"], r["type"]): vid for vid, r in rows.items()}
prior_text = ""
for f in [REPO / "working/roles-slice-s212/ADJUDICATION-s212.md",
          REPO / "working/edge-retrofit-s211/ADJUDICATION-s211.md"]:
    if f.exists():
        prior_text += f.read_text()
hits = [(vid, s, t, ty) for (s, t, ty), vid in pairs.items()
        if s in prior_text and t in prior_text]
if hits:
    for vid, s, t, ty in hits:
        print(f"  CHECK MANUALLY {vid}: {s} + {t} both appear in a prior adjudication file")
else:
    print("  no (source,target) pair co-appears in prior adjudication files")

dupes = 0
with open(REPO / "graph/edges/edges.jsonl") as f:
    existing = set()
    for line in f:
        line = line.strip()
        if not line:
            continue
        e = json.loads(line)
        existing.add((e.get("source_slug"), e.get("target_slug"), e.get("edge_type")))
for (s, t, ty), vid in sorted(pairs.items(), key=lambda kv: kv[1]):
    if (s, t, ty) in existing:
        dupes += 1
        print(f"  {vid} DUPLICATE of existing edge: {s} -{ty}-> {t}")
print(f"  duplicates vs existing edges.jsonl: {dupes}")

print("\n=== STANDING AUDIT 3: in-batch duplicate (source,target,type) ===")
seen = {}
for vid, r in sorted(rows.items()):
    k = (r["source"], r["target"], r["type"])
    if k in seen:
        print(f"  {vid} duplicates {seen[k]}: {k}")
    seen[k] = vid
print("  (none above = clean)")
