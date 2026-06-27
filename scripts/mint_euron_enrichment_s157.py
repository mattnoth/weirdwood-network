#!/usr/bin/env python3
"""Mint A1.6 "Kingsmoot / Euron" enrichment (S157) — the 21st major-arc enrichment dip and the THIRD
of the 🅰 A-roundup campaign (Matt S154). Unlike the other A1s, this arc already had a spine (S116) +
one early enrichment (S116) + a Victarion-voyage wire (S132). Baseline dedup pull = 230 internal edges
but only 11 internal CAUSAL — a thin causal spine + a dense dyadic web. So this is WIRE + ENRICH with a
HEAVY dedup.

**ZERO new nodes** — every target already exists (cragorn, dunstan-drumm, red-rain, all shield-lords,
gylbert-farwynd, torwold-browntooth, victarion-greyjoys-third-wife, naggas-hill, silence, iron-victory,
dragonbinder, eurons-mongrel-sons, burning-of-the-lannister-fleet). So this dip is pure edge-wiring that
LIGHTS islanded nodes. No weirwood-refresh needed (edge-only).

37 edges (see candidates.json). KEY synthesis calls:
  - taking-of-the-shields had ZERO participant roles -> wired victarion AGENT_IN/COMMANDS_IN, euron
    COMMANDS_IN (ordered, not present), the de-island victarion-slays SUB_BEAT_OF, LOCATED_AT shield-islands,
    4 combatants (harras/nute/torwold/ragnor), + the 4 shield-lords euron APPOINTS.
  - the kingsmoot fully participated -> LOCATED_AT naggas-hill, aeron OFFICIATES (distinct from AGENT_IN),
    dragonbinder WIELDED_IN + cragorn AGENT_IN (the horn-blower the horn killed), 3 claimants + dunstan
    WIELDS red-rain (Valyrian steel), Asha's champions (Qarl/Tristifer) + Baelor PARTICIPATES_IN.
  - the Reader (rodrik-harlaw core_in=0) -> UNCLE_OF asha (maternal), ADVISES, ALLIES_WITH, PARTICIPATES_IN.
  - lit 0-edge marquee objects -> euron CAPTAIN_OF silence, victarion CAPTAIN_OF iron-victory, euron OWNS
    dragonbinder, eurons-mongrel-sons CREW_OF silence.
  - WHODUNIT done HONESTLY -> NO new SUSPECTED_OF (euron SUSPECTED_OF death-of-balon built S116; Lens B
    declined a second mechanism the text leaves unproven). The agency value is euron MANIPULATES hotho-harlaw
    via_bribe (the type-correct named-captain form, NOT MANIPULATES->the-kingsmoot-event which is a type-misfit).
  - salt-wife wound -> victarion KILLS victarion-greyjoys-third-wife. Cross-arc backstory seam -> euron+
    victarion AGENT_IN burning-of-the-lannister-fleet (lit a 0-in Greyjoy-Rebellion event).
  - HELD THE LINE: DROPPED taking-of-the-shields CAUSES anarchy-in-the-reach (the S116 TRAP — that node is a
    bare pass2-wiki stub for the HISTORICAL Gardener-era Reach anarchy, NOT the AFFC raiding); DROPPED
    dragonbinder GIFTED_TO victarion (the gift is an ADWD scene, out of AFFC scope); DROPPED euron ASSAULTS the
    salt-wife (seduction/rape ambiguous -> node-prose) + euron DECEIVES asha (over-asserts an unproven lie).
  - THEORY-GATED (node-prose, NO edges): Euron<->Bloodraven, Dragonbinder=Horn-of-Joramun, the dusky-woman
    identity, Euron-as-eldritch-herald. NO TWOW (Falia Flowers, The Forsaken). NO container tag.

Reads candidates.json; RE-GREPS each quote (FAIL-fast). Additive only. Fresh-verify drops/adjusts live in
finalize_euron_s157.py."""
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
CAND = REPO / "working" / "enrichment" / "euron" / "candidates.json"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-euron-enrichment-2026-06-27.jsonl"

RUN_ID = "euron-enrichment-s157"
PRODUCED_AT = "2026-06-27T00:00:00+00:00"

NEW_NODE_SLUGS = set()  # edge-only dip — every target already exists


def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def authoritative_line(book, chapter, quote):
    f = REPO / "sources" / "chapters" / book / f"{chapter}.md"
    if not f.exists():
        sys.exit(f"ABORT: chapter file missing: {f}")
    lines = f.read_text(encoding="utf-8").splitlines()
    q = norm(quote)
    for i, ln in enumerate(lines, 1):
        if q in norm(ln):
            return i
    for i in range(len(lines) - 1):
        if q in norm(lines[i] + " " + lines[i + 1]):
            return i + 1
    sys.exit(f"ABORT: quote not found in {chapter}.md -> {quote!r}")


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-euron-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


def make_edge_row(e):
    book, chapter = e["book"], e["chapter"]
    line = authoritative_line(book, chapter, e["quote"])
    row = {
        "edge_type": e["type"],
        "source_slug": e["source"],
        "target_slug": e["target"],
        **common(),
        "evidence_book": book,
        "evidence_chapter": chapter,
        "evidence_ref": f"sources/chapters/{book}/{chapter}.md:{line}",
        "evidence_quote": e["quote"],
        "confidence_tier": e["tier"],
        "asserted_relation": e["note"],
        "candidate_id": e["id"],
    }
    if e.get("qualifier"):
        row["qualifier"] = e["qualifier"]
    if e.get("verify"):
        row["verified_by"] = "pending"
    return row


def main():
    data = json.loads(CAND.read_text())
    edges = data["edges"]

    all_slugs = set()
    for e in edges:
        all_slugs.add(e["source"]); all_slugs.add(e["target"])
    resolved, missing = precheck_slugs(all_slugs - NEW_NODE_SLUGS)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed — non-existent: {sorted(missing)}")
    print(f"Slug pre-check OK: {len(resolved)} existing slugs resolved.")

    raw = EDGES.read_text(encoding="utf-8").splitlines()
    existing = [ln for ln in raw if ln.strip()]
    if any(RUN_ID in ln for ln in existing):
        sys.exit(f"ABORT: run_id '{RUN_ID}' already present — already minted.")
    print(f"Re-run guard OK: run_id '{RUN_ID}' not present.")

    new_rows = [make_edge_row(e) for e in edges]  # FAIL-fast on any unfound quote
    print(f"Line-check OK: all {len(new_rows)} quotes located in source.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)
    print(f"Backup written -> {BACKUP.relative_to(REPO)}")

    out = existing + [json.dumps(r, ensure_ascii=False) for r in new_rows]
    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")

    tc = {}
    for e in edges:
        tc[e["type"]] = tc.get(e["type"], 0) + 1
    print("\n── SUMMARY ──")
    print("Nodes created (0): edge-only dip")
    print(f"Edges appended ({len(new_rows)}):")
    for t, c in sorted(tc.items()):
        print(f"  {t}: {c}")


if __name__ == "__main__":
    main()
