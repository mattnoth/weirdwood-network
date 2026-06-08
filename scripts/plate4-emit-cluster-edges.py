#!/usr/bin/env python3
"""plate4-emit-cluster-edges.py — emit SUB_BEAT_OF / DUPLICATE_OF edges from cluster decisions.

Reads the Pass-A → Pass-B → Pass-C cascade outputs and produces a staged edge
JSONL ready for Plate 5 to merge into graph/edges/edges.jsonl.

Reconciliation order (later overrides earlier):
  1. Pass A (Haiku, all 219 mints): working/edge-modeling/plate4-wiki-cluster/wiki-cluster-assignments.jsonl
  2. Pass B (Opus, 71 inference-only): working/edge-modeling/plate4-wiki-cluster-passb/wiki-cluster-assignments.jsonl
  3. Pass C (Sonnet, 167 distinct): working/edge-modeling/plate4-wiki-cluster-passc/wiki-cluster-assignments.jsonl

For each reconciled mint:
  - suggested_action == "sub-beat-of" → emit SUB_BEAT_OF edge: mint → wiki_event
  - suggested_action == "duplicate-of" → emit DUPLICATE_OF edge: mint → wiki_event
  - suggested_action == "distinct" → no edge emitted
  - equivalence_evidence_strength == "direct-textual" → confidence_tier 1
  - equivalence_evidence_strength == "inference-only" → confidence_tier 2

Outputs (STAGING ONLY — Plate 5 is the merge):
  - working/edge-modeling/plate4-wiki-cluster/cluster-edges-staging.jsonl
  - working/edge-modeling/plate4-wiki-cluster/cluster-edges-summary.md
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_PASS_A = _REPO / "working" / "edge-modeling" / "plate4-wiki-cluster" / "wiki-cluster-assignments.jsonl"
_PASS_B = _REPO / "working" / "edge-modeling" / "plate4-wiki-cluster-passb" / "wiki-cluster-assignments.jsonl"
_PASS_C = _REPO / "working" / "edge-modeling" / "plate4-wiki-cluster-passc" / "wiki-cluster-assignments.jsonl"
_HUMAN = _REPO / "working" / "edge-modeling" / "plate4-wiki-cluster" / "human-triage-assignments.jsonl"
_OUT_DIR = _REPO / "working" / "edge-modeling" / "plate4-wiki-cluster"
_EDGES_OUT = _OUT_DIR / "cluster-edges-staging.jsonl"
_RECONCILED = _OUT_DIR / "wiki-cluster-RECONCILED.jsonl"
_SUMMARY = _OUT_DIR / "cluster-edges-summary.md"


def load_assignments(path: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not path.exists():
        return out
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            slug = row.get("mint_slug", "")
            if slug:
                out[slug] = row
    return out


def reconcile() -> dict[str, dict]:
    """Build final per-mint classification. Later passes override earlier.

    Priority order (highest wins):
      1. human-triage  (Matt's manual decisions)
      2. opus-pass-b   (Opus on inference-only)
      3. sonnet-pass-c (Sonnet on distinct)
      4. haiku-pass-a  (initial LLM pass)
    """
    pa = load_assignments(_PASS_A)
    pb = load_assignments(_PASS_B)
    pc = load_assignments(_PASS_C)
    human = load_assignments(_HUMAN)
    print(f"Pass A:       {len(pa)} mints")
    print(f"Pass B:       {len(pb)} mints (overrides Pass A)")
    print(f"Pass C:       {len(pc)} mints (overrides Pass A; Pass B has priority)")
    print(f"Human-triage: {len(human)} mints (overrides everything)")
    final: dict[str, dict] = {}
    for slug, row in pa.items():
        final[slug] = dict(row)
        final[slug]["reconciled_model"] = "haiku-pass-a"
    for slug, row in pc.items():
        final[slug] = dict(row)
        final[slug]["reconciled_model"] = "sonnet-pass-c"
    for slug, row in pb.items():
        final[slug] = dict(row)
        final[slug]["reconciled_model"] = "opus-pass-b"
    # Human-triage is highest authority — preserve Pass A's title/chapter context
    for slug, row in human.items():
        merged = dict(final.get(slug, {}))
        merged.update(row)
        merged["reconciled_model"] = "human-triage"
        final[slug] = merged
    return final


def emit_edges(reconciled: dict[str, dict]) -> list[dict]:
    """Convert reconciled cluster decisions into JSONL-ready edge dicts."""
    edges: list[dict] = []
    now = datetime.now(timezone.utc).isoformat()
    for slug, row in reconciled.items():
        action = row.get("suggested_action", "")
        best = row.get("best_match", "")
        strength = row.get("equivalence_evidence_strength", "")
        if action not in ("sub-beat-of", "duplicate-of"):
            continue
        if not best or best == "none":
            continue
        edge_type = "SUB_BEAT_OF" if action == "sub-beat-of" else "DUPLICATE_OF"
        tier = 1 if strength == "direct-textual" else 2
        edges.append({
            "edge_type": edge_type,
            "source_slug": slug,                   # the Plate-3 mint
            "target_slug": best,                   # the wiki event-node
            "confidence_tier": tier,
            "evidence_kind": "plate4-wiki-cluster",
            "evidence_book": row.get("source_book", ""),
            "evidence_chapter": (row.get("source_chapter_labels") or [""])[0],
            "rationale": row.get("rationale", ""),
            "quoted_evidence": row.get("quoted_evidence", ""),
            "classifier_model": row.get("model", ""),
            "reconciled_model": row.get("reconciled_model", ""),
            "produced_at": now,
            "schema_version": "plate4-v1",
            "stage": "STAGED — DO NOT promote to graph/edges/edges.jsonl until Plate 5 gated merge",
        })
    return edges


def write_summary(reconciled: dict[str, dict], edges: list[dict]) -> None:
    action_counts: dict[str, int] = {}
    strength_counts: dict[str, int] = {}
    target_counts: dict[str, int] = {}
    model_provenance: dict[str, int] = {}
    for slug, row in reconciled.items():
        a = row.get("suggested_action") or "n/a"
        s = row.get("equivalence_evidence_strength") or "n/a"
        action_counts[a] = action_counts.get(a, 0) + 1
        strength_counts[s] = strength_counts.get(s, 0) + 1
        m = row.get("reconciled_model", "n/a")
        model_provenance[m] = model_provenance.get(m, 0) + 1
        if a in ("sub-beat-of", "duplicate-of") and row.get("best_match"):
            target_counts[row["best_match"]] = target_counts.get(row["best_match"], 0) + 1

    with open(_SUMMARY, "w", encoding="utf-8") as fh:
        fh.write("# Plate 4 Cluster Edges — Summary\n\n")
        fh.write(f"**Generated:** {datetime.now().isoformat(timespec='seconds')}\n\n")
        fh.write(f"**Total mints classified:** {len(reconciled)}\n")
        fh.write(f"**Total cluster edges emitted:** {len(edges)}\n")
        fh.write(f"**Output:** `{_EDGES_OUT.relative_to(_REPO)}` (STAGED — not in graph/)\n\n")
        fh.write("## Action distribution\n\n| Action | Count |\n|---|---|\n")
        for k, v in sorted(action_counts.items(), key=lambda x: -x[1]):
            fh.write(f"| {k} | {v} |\n")
        fh.write("\n## Strength distribution\n\n| Strength | Count |\n|---|---|\n")
        for k, v in sorted(strength_counts.items(), key=lambda x: -x[1]):
            fh.write(f"| {k} | {v} |\n")
        fh.write("\n## Reconciled-by-model provenance\n\n| Final model | Count |\n|---|---|\n")
        for k, v in sorted(model_provenance.items(), key=lambda x: -x[1]):
            fh.write(f"| {k} | {v} |\n")
        fh.write("\n## Top 25 wiki events absorbing sub-beats\n\n| Wiki event | Sub-beats | |\n|---|---:|---|\n")
        for k, v in sorted(target_counts.items(), key=lambda x: -x[1])[:25]:
            fh.write(f"| `{k}` | {v} | |\n")
        fh.write("\n## Edge-type breakdown\n\n| Edge type | Count | Confidence tier 1 | Confidence tier 2 |\n|---|---|---|---|\n")
        by_et: dict[str, dict] = {}
        for e in edges:
            et = e["edge_type"]
            by_et.setdefault(et, {"total": 0, "t1": 0, "t2": 0})
            by_et[et]["total"] += 1
            if e["confidence_tier"] == 1:
                by_et[et]["t1"] += 1
            else:
                by_et[et]["t2"] += 1
        for et, c in sorted(by_et.items()):
            fh.write(f"| {et} | {c['total']} | {c['t1']} | {c['t2']} |\n")


def main() -> None:
    print("Reconciling Pass A + Pass B + Pass C...")
    reconciled = reconcile()
    print(f"  Reconciled: {len(reconciled)} mints")

    # Write the reconciled file
    with open(_RECONCILED, "w", encoding="utf-8") as fh:
        for slug, row in reconciled.items():
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"  Wrote reconciled: {_RECONCILED.relative_to(_REPO)}")

    edges = emit_edges(reconciled)
    print(f"  Emitted {len(edges)} cluster edges")

    with open(_EDGES_OUT, "w", encoding="utf-8") as fh:
        for e in edges:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"  Wrote edges: {_EDGES_OUT.relative_to(_REPO)}")

    write_summary(reconciled, edges)
    print(f"  Wrote summary: {_SUMMARY.relative_to(_REPO)}")


if __name__ == "__main__":
    main()
