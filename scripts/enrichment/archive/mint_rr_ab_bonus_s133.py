#!/usr/bin/env python3
"""S133 RR-enrichment A/B BONUS: 2 genuine net-new causal edges surfaced by the max-effort Opus
blind pass that the 3-Sonnet-lens board missed (lens-division coverage seam: no lens owned
existing-node->existing-node causal links). Both reference pre-existing nodes; both quotes are
byte-clean (no internal quote chars) and line-verified by the orchestrator.

  C9  MOTIVATES roberts-rebellion -> robert-orders-daenerys-assassination
      (gives the RR hub its FIRST real outgoing edge — fixes the dead-end at the cluster head;
       also a clean Tier-1 RR->Essos seam)
  C1  MOTIVATES wildfire-plot -> slaying-of-aerys-ii-the-kingslaying
      (Jaime's stated motive for the kingslaying)
"""
import json, shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph/edges/edges.jsonl"
BACKUP = REPO / "graph/edges/_regrounding/edges-pre-rr-ab-bonus-2026-06-22.jsonl"
RUN = "rr-enrichment-s133-ab"

NEW = [
    {"edge_type": "MOTIVATES", "source_slug": "roberts-rebellion", "target_slug": "robert-orders-daenerys-assassination",
     "evidence_book": "agot", "evidence_chapter": "agot-eddard-08",
     "evidence_ref": "sources/chapters/agot/agot-eddard-08.md:13",
     "evidence_quote": "I want them dead, mother and child both, and that fool Viserys as well.",
     "confidence_tier": 1,
     "asserted_relation": "Robert's hatred of the Targaryens, born of the rebellion, motivates his standing order to assassinate the exiled Targaryens — the RR hub's causal continuation into the present (a clean RR->Essos seam)."},
    {"edge_type": "MOTIVATES", "source_slug": "wildfire-plot", "target_slug": "slaying-of-aerys-ii-the-kingslaying",
     "evidence_book": "asos", "evidence_chapter": "asos-jaime-05",
     "evidence_ref": "sources/chapters/asos/asos-jaime-05.md:63",
     "evidence_quote": "Then I slew Aerys, before he could find someone else to carry his message to the pyromancers.",
     "confidence_tier": 1,
     "asserted_relation": "Jaime slew Aerys specifically to stop the king's wildfire message reaching the pyromancers — the wildfire plot is the stated motive for the kingslaying."},
]
COMMON = {"decision": "emit_edge", "candidate_kind": "causal-curator-arc", "evidence_kind": "book-pass1",
          "typed_by": "curator-causal-arc", "schema_version": "pass1-derived-v1",
          "produced_at": "2026-06-22T00:00:00+00:00", "run_id": RUN,
          "verified_by": "orchestrator-linecheck-opus-ab-2026-06-22"}

rows = [json.loads(l) for l in EDGES.read_text(encoding="utf-8").splitlines() if l.strip()]
if any(r.get("run_id") == RUN for r in rows):
    raise SystemExit("ABORT: run_id already present (idempotent guard).")
# slug existence + edge-absence guard
slugs = {p.name[:-len(".node.md")] for p in (REPO/"graph/nodes").glob("**/*.node.md")}
for e in NEW:
    for k in ("source_slug", "target_slug"):
        if e[k] not in slugs:
            raise SystemExit(f"ABORT: missing node {e[k]}")
    if any(r.get("source_slug")==e["source_slug"] and r.get("target_slug")==e["target_slug"] and r.get("edge_type")==e["edge_type"] for r in rows):
        raise SystemExit(f"ABORT: edge already exists {e['source_slug']}->{e['target_slug']}")

shutil.copy2(EDGES, BACKUP)
with EDGES.open("a", encoding="utf-8") as f:
    for e in NEW:
        f.write(json.dumps({**COMMON, **e}, ensure_ascii=False) + "\n")
print(f"appended {len(NEW)} A/B bonus edges; backup {BACKUP}; edges.jsonl now {len(rows)+len(NEW)} rows")
