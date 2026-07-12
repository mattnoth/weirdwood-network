#!/usr/bin/env python3
"""S213 Dance arc dip — apply adjudication, run standing audits, assemble the
mint-ready edge candidates.json (W1 roles + W2 causal) and the quote-apply
plan (W3a+W3b). Decisions in ADJUDICATION-dance-s213.md."""
import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

# W1-14 (Racallio COMMANDS_IN daughters-war): verifier AMBIGUOUS on a weak
# fragment; swap to the stronger line the verifier itself identified (byte-copied
# from fab-the-hooded-hand-21.md:123).
PATCH = {
    "W1-14": {"quote": "Racallio overran the islands in a trice and put the reigning King of the Narrow Sea to death...only to decide to claim his crown for himself",
              "note": "self-proclaimed King of the Narrow Sea — led the conquest of the Stepstones himself; four-sided war, side recorded per-faction"},
}
DROP = set()

HARM = {"death","execution","murder","assassination","poisoning","maiming","torture",
        "capture","imprisonment","battle","sack","destruction","suicide","stillbirth",
        "betrayal","raid","attack","duel","deception","mutiny","massacre","abduction","wounding"}
WAR_NODES = {"dance-of-the-dragons", "daughters-war"}

edges = []
for f, key in [("proposals-w1-roles.json", "candidates"), ("proposals-w2-causal.json", "edges")]:
    d = json.loads((OUT / "proposals" / f).read_text())
    for r in d[key]:
        if r["id"] in DROP:
            continue
        r = dict(r)
        r.update(PATCH.get(r["id"], {}))
        edges.append(r)

# audits
existing = set()
with open(REPO / "graph/edges/edges.jsonl") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        e = json.loads(line)
        existing.add((e.get("source_slug"), e.get("target_slug"), e.get("edge_type")))

fails = []
seen = set()
for r in edges:
    k = (r["source"], r["target"], r["type"])
    if r["type"] == "VICTIM_IN":
        fails.append((r["id"], "VICTIM_IN present — check harm gate"))
    if r["target"] in WAR_NODES and r["type"] == "VICTIM_IN":
        fails.append((r["id"], "VICTIM_IN on war node"))
    if k in existing:
        fails.append((r["id"], f"duplicate of existing edge {k}"))
    if k in seen:
        fails.append((r["id"], f"in-batch duplicate {k}"))
    seen.add(k)
    chap = REPO / "sources/chapters" / r["book"] / (r["chapter"] + ".md")
    if not any(r["quote"] in line for line in chap.read_text().splitlines()):
        fails.append((r["id"], "quote not a single-line substring"))
if fails:
    print("AUDIT FAILURES:", fails)
    raise SystemExit(1)

(OUT / "candidates.json").write_text(json.dumps({
    "_meta": {
        "unit": "dance-arc dip (HotD-viewer coverage)",
        "session": "S213",
        "run_id": "dance-arc-s213",
        "new_node_slugs": [],
        "note": "W1 umbrella/missed-event roles + W2 causal gap-fill; Sonnet proposers, "
                "Haiku fresh-verify (W1 14C/1A, W2 6C), W1-14 quote strengthened at "
                "adjudication (ADJUDICATION-dance-s213.md).",
    },
    "edges": edges,
}, indent=1))

# quote-apply plan (deterministic; node ## Quotes appends)
quotes = []
for f in ["proposals-w3a-event-quotes.json", "proposals-w3b-entity-quotes.json"]:
    d = json.loads((OUT / "proposals" / f).read_text())
    quotes += d["quotes"]
qfails = []
for q in quotes:
    chap = REPO / "sources/chapters/fab" / (q["chapter"] + ".md")
    lines = chap.read_text().splitlines()
    ln = q.get("line", 0)
    if not (1 <= ln <= len(lines)) or q["quote"] not in lines[ln - 1]:
        qfails.append((q["id"], "quote not at stated line"))
if qfails:
    print("QUOTE AUDIT FAILURES:", qfails)
    raise SystemExit(1)
(OUT / "quotes-to-apply.json").write_text(json.dumps({"quotes": quotes}, indent=1))

print(f"edges assembled: {len(edges)}  {dict(Counter(r['type'] for r in edges))}")
print(f"quotes verified at line: {len(quotes)} across {len({q['slug'] for q in quotes})} nodes")
