#!/usr/bin/env python3
"""apply-verify-verdicts.py — S208. Fold the Haiku fresh-verify verdicts back into
events-decisions.json: REJECT-DUPE:<slug> flips the CREATE to MAP:<slug> (role edges
attach to the existing node); REJECT-UNGROUNDED / REJECT-WRONG flips to DROP.
Rerun compile-recover-maps.py afterwards.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

verdicts = []
for f in sorted(HERE.glob("verify-verdicts-*.json")):
    verdicts.extend(json.loads(f.read_text(encoding="utf-8")))

# slug -> (unit, name) from the reconcile outputs
slug_to_key = {}
for cn in HERE.glob("out/*/created-nodes.jsonl"):
    for line in cn.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        slug_to_key[(r["unit"], r["slug"])] = (r["unit"], r["name"])

existing = {p.name[: -len(".node.md")] for p in (REPO / "graph" / "nodes").glob("**/*.node.md")}

dec_path = HERE / "events-decisions.json"
decisions = json.loads(dec_path.read_text(encoding="utf-8"))
by_key = {(d["unit"], d["name"]): d for d in decisions}

changed, problems = [], []
for v in verdicts:
    verdict = v["verdict"]
    if verdict == "CONFIRM":
        continue
    key = slug_to_key.get((v["unit"], v["slug"]))
    if key is None or key not in by_key:
        problems.append(f"verdict for unknown create: {v}")
        continue
    d = by_key[key]
    if verdict.startswith("REJECT-DUPE:"):
        slug = verdict.split(":", 1)[1].strip()
        if slug not in existing:
            problems.append(f"REJECT-DUPE target missing: {v}")
            continue
        d["decision"] = f"MAP:{slug}"
    else:
        d["decision"] = f"DROP:fresh-verify {verdict[:50]}"
    d["note"] = (v.get("note", "") + " [fresh-verify]").strip()
    changed.append(f"{key[0]}|{key[1]} -> {d['decision']}")

dec_path.write_text(json.dumps(decisions, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"verdicts: {len(verdicts)}  confirmed: {sum(1 for v in verdicts if v['verdict']=='CONFIRM')}  changed: {len(changed)}")
for c in changed:
    print(" ", c)
if problems:
    print("PROBLEMS:")
    for p in problems:
        print(" ", p)
    sys.exit(1)
