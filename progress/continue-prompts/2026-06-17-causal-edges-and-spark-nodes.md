# Continue — Causal edges + Robert's Rebellion spark-node minting

> **Recommended model:** Sonnet 4.6 (curatorial/deterministic) + a fresh `general-purpose` subagent for verification. Opus only if orchestration gets hairy.
>
> **Status (S104, 2026-06-17 — Robert's Rebellion DONE):** The pilot + the full Robert's Rebellion arc are now SHIPPED. Phase 1 done: 3 spark-beat nodes minted (`abduction-of-lyanna`, `execution-of-brandon-and-rickard-stark`, `aerys-demands-ned-and-robert`) + indexed + alias-resolvable. Phase 2 done: full chain wired + subagent-verified — `tourney-at-harrenhal —CAUSES→ abduction —CAUSES→ executions —TRIGGERS→ demand —TRIGGERS→ roberts-rebellion`, plus the earlier `battle-of-the-trident —CAUSES→ sack —CAUSES→ coronation`. **REMAINING WORK = SCALE to other historical hubs** (the open question for Matt below) using the exact same method.

## Goal
Make the Robert's Rebellion causal arc fully traversable, then scale the pattern to other historical hubs. Two phases:

### Phase 1 — mint the 3 missing spark-beat nodes
Create `event.*` nodes (in `graph/nodes/events/`) for the beats that currently have no node:
- `abduction-of-lyanna` (281/282 AC — Rhaegar takes Lyanna near Harrenhal; the inciting act)
- `execution-of-brandon-and-rickard-stark` (282 AC — Aerys burns Rickard, strangles Brandon)
- `aerys-demands-ned-and-robert` (282 AC — Aerys orders Jon Arryn to send Ned & Robert's heads; the direct war trigger)

For each: pull evidence from the LOCAL cache (`sources/wiki/_raw/Robert's_Rebellion.json` has the full narrative in its `html` field; cross-check `sources/chapters/` for any POV recollection, e.g. Ned's AGOT memories). Stamp `occurred.ac_year`, `era: roberts-rebellion`, `confidence`, `wiki_source`, and a `## Quotes` block with verbatim evidence ([[feedback_capture_quotes_during_research]]). Follow the node schema in `reference/architecture.md`.

**After minting (node ADD):** rebuild indexes + alias-resolver — prefer targeted ops over a full `weirwood refresh` (re-stamps ~7.9k timestamps; S102 lesson). See `project_rebuild_derived_artifacts_after_node_mutation`.

### Phase 2 — wire the causal chain
Now that beats exist, the spark chain can be `TRIGGERS` (immediate-spark granularity is finally accurate):
`tourney-at-harrenhal` (the crowning) → `abduction-of-lyanna` → `execution-of-brandon-and-rickard-stark` → `aerys-demands-ned-and-robert` → `roberts-rebellion` → … → `battle-of-the-trident` (already CAUSES `sack-of-kings-landing` → `coronation-of-robert-i-baratheon`).
Pick `TRIGGERS` vs `CAUSES` per the architecture definitions (TRIGGERS = the specific spark; CAUSES = leads-to). Both are in vocab — no vocab change. Tier-2 (wiki-attested) unless a book quote earns Tier-1.

## Verification gate (FIRM — Matt S104)
Do NOT ask Matt to review individual edges. For every interpretive/causal edge AND every minted node, run a **fresh adversarial subagent** that confirms/refutes against the LOCAL cache only (never refetch — [[feedback_no_external_wiki_fetch]]): quote-verbatim check + direction check + CONFIRM/REFUTE/UNCERTAIN verdict. Keep CONFIRMed, drop REFUTEd, surface UNCERTAIN. Stamp survivors `verified_by`. Present Matt a **summary** (counts/verdicts/drops), not an edge-list. (memory `feedback_subagent_verify_not_matt`)

## Mechanics / hard rules
- Backup `graph/edges/edges.jsonl` to `_regrounding/` before any edge write. Edge rows mirror the S104 causal-pilot shape (`candidate_kind: causal-curator-pilot` or similar, `evidence_kind: wiki-historical-anchor`, `typed_by: curator-causal-pilot`).
- Edge-only writes need no index rebuild; node ADDs do (Phase 1).
- Re-run `python3 scripts/graph-query.py --health` (orphans should not increase) + `python3 -m pytest -q` (baseline 1297 pass / 1 documented `cwd-is-tmp` fail) after changes.
- Do NOT `/endsession` without Matt's permission. Do NOT refetch the wiki.

## Context / source-of-truth
- `history/session-details/session-104.md` — the pilot, the CAUSES-vs-TRIGGERS finding, the verification method.
- `working/narrative-arcs-design-memo-2026-06-13.md` — this is the narrative-arc-reification pattern on a historical arc (`project_narrative_arc_reification`).
- Open question for Matt: how far to scale Phase 2 beyond Robert's Rebellion (which historical hubs next) — dip-driven, not mass-mint.
