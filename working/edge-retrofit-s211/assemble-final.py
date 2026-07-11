#!/usr/bin/env python3
"""Assemble the adjudicated final candidates.json for the S211 edge-retrofit dip.

Merges the three proposal files, applies the orchestrator adjudication ledger
(drops / retypes / additions), renumbers ids, and checks no (type,source,target)
triple already exists in edges.jsonl. Read-only on the graph.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PROP = HERE / "proposals"

# ---- adjudication ledger (S211 orchestrator; see ADJUDICATION-s211.md) ----
DROP = {
    ("suspicion-a", "S4"),   # S159 fresh-verify E14 REJECT precedent (diffuse class distrust)
    ("suspicion-a", "S5"),   # S159 fresh-verify E15 REJECT precedent
    ("suspicion-b", "S2"),   # S148 retired petyr SUSPECTED_OF -> COMMANDS_IN (proven); verifier PROBLEM
    ("suspicion-b", "S10"),  # exact dup of suspicion-a S10
    ("suspicion-b", "S11"),  # exact dup of suspicion-a S11
}
# B-S5: Catelyn's suspicion is proven true in Tyrion's own POV (acok-tyrion-06) ->
# retype to COMMANDS_IN tier-1 with the proving quote (S148 Petyr-upgrade pattern).
RETYPE_B_S5 = {
    "type": "COMMANDS_IN",
    "tier": "tier-1",
    "book": "acok",
    "chapter": "acok-tyrion-06",
    "quote_line": 217,  # "…my scheme to free Jaime." (Tyrion to Varys)
    "note": "Retyped from proposed SUSPECTED_OF at orchestrator adjudication: Catelyn's "
            "suspicion (acok-catelyn-05) is proven in Tyrion's own POV — the four false "
            "guardsmen scheme is his (acok-tyrion-06). Proven agency = COMMANDS_IN "
            "(S148 Petyr precedent).",
}
# Orchestrator addition: Corlys confessed + convicted (fab-hour-of-the-wolf-20) ->
# AGENT_IN, not SUSPECTED_OF (suspicion-a flag adjudicated against the primary text).
ADD_CORLYS = {
    "type": "AGENT_IN",
    "source": "corlys-velaryon",
    "target": "death-of-aegon-ii",
    "book": "fab",
    "chapter": "fab-hour-of-the-wolf-20",
    "quote_marker": "did not attempt to deny his guilt",
    "tier": "tier-1",
    "note": "Orchestrator-added at S211 adjudication of the suspicion-a flag: Corlys "
            "confesses before Cregan Stark's tribunal and is declared guilty of murder, "
            "regicide, and high treason — proven complicity, so AGENT_IN (role edge), "
            "NOT SUSPECTED_OF. Larys Strong's existing tier-2 SUSPECTED_OF stands per "
            "the S202/S203 adjudications (he never confirmed; the administering hand "
            "is never known).",
    "qualifier": "",
}


def exact_line(book, chapter, marker):
    f = REPO / "sources" / "chapters" / book / f"{chapter}.md"
    for ln in f.read_text().splitlines():
        if marker in ln:
            return ln
    raise SystemExit(f"marker not found: {marker!r} in {f}")


def sentence_containing(line, marker, max_len=220):
    # take the sentence(s) around the marker, trimmed to a tight span
    idx = line.find(marker)
    start = max(line.rfind(". ", 0, idx), line.rfind("” ", 0, idx))
    start = start + 2 if start != -1 else 0
    end = line.find(". ", idx)
    end = end + 1 if end != -1 else len(line)
    s = line[start:end].strip()
    return s[:max_len]


def main():
    existing = set()
    for line in open(REPO / "graph/edges/edges.jsonl"):
        e = json.loads(line)
        existing.add((e["edge_type"], e["source_slug"], e["target_slug"]))

    final, adjudication_rows = [], []
    for slice_name, fname in [("knighting", "knighting-candidates.json"),
                              ("suspicion-a", "suspicion-a-candidates.json"),
                              ("suspicion-b", "suspicion-b-candidates.json")]:
        data = json.loads((PROP / fname).read_text())
        for c in data["candidates"]:
            key = (slice_name, c["id"])
            if key in DROP:
                adjudication_rows.append((slice_name, c["id"], "DROP"))
                continue
            if key == ("suspicion-b", "S5"):
                line = exact_line(RETYPE_B_S5["book"], RETYPE_B_S5["chapter"],
                                  "my scheme to free Jaime")
                c = dict(c, type=RETYPE_B_S5["type"], tier=RETYPE_B_S5["tier"],
                         book=RETYPE_B_S5["book"], chapter=RETYPE_B_S5["chapter"],
                         quote=sentence_containing(line, "my scheme to free Jaime"),
                         note=RETYPE_B_S5["note"])
                adjudication_rows.append((slice_name, "S5", "RETYPE->COMMANDS_IN"))
            c["_slice"] = slice_name
            final.append(c)

    # orchestrator addition
    line = exact_line(ADD_CORLYS["book"], ADD_CORLYS["chapter"], ADD_CORLYS["quote_marker"])
    corlys = dict(ADD_CORLYS)
    corlys["quote"] = sentence_containing(line, ADD_CORLYS["quote_marker"])
    del corlys["quote_marker"]
    corlys["_slice"] = "orchestrator"
    final.append(corlys)
    adjudication_rows.append(("orchestrator", "corlys AGENT_IN death-of-aegon-ii", "ADD"))

    # triple-level dup check vs live graph
    clashes = [(c["type"], c["source"], c["target"]) for c in final
               if (c["type"], c["source"], c["target"]) in existing]
    # intra-batch dup check
    seen, intra = set(), []
    for c in final:
        k = (c["type"], c["source"], c["target"])
        if k in seen:
            intra.append(k)
        seen.add(k)

    out = {"_meta": {"unit": "edge-vocab retrofit Part B (S211)",
                     "session": "S211",
                     "run_id": "edge-retrofit-s211",
                     "typed_by": "curator-edge-retrofit-s211",
                     "new_node_slugs": [],
                     "note": "Adjudicated merge of knighting + suspicion-a/b proposer "
                             "slices; see ADJUDICATION-s211.md."},
           "edges": []}
    for i, c in enumerate(final, 1):
        out["edges"].append({
            "id": f"R{i}", "type": c["type"], "source": c["source"],
            "target": c["target"], "book": c["book"], "chapter": c["chapter"],
            "quote": c["quote"], "tier": c["tier"],
            "note": f"[{c['_slice']}:{c.get('id','+')}] {c['note']}",
            **({"qualifier": c["qualifier"]} if c.get("qualifier") else {}),
        })
    (HERE / "candidates.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))

    print(f"final edges: {len(out['edges'])}")
    print("by type:", {t: sum(1 for e in out['edges'] if e['type'] == t)
                       for t in sorted({e['type'] for e in out['edges']})})
    print("live-graph triple clashes:", clashes or "none")
    print("intra-batch dups:", intra or "none")
    for row in adjudication_rows:
        print("adjudicated:", row)


if __name__ == "__main__":
    main()
