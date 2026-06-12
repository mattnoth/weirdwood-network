# Worklog Archive 019

> archive019 started — 1/5

---

### Session 87 — Plate 5 SHIPPED — first canonical write to edges.jsonl (2026-06-09)

**Model:** Opus 4.7 (orchestrator + all execution; no agents delegated). **Detail:** none (execution-heavy, design captured in `working/edge-modeling/plate5-merge-diff.md`). **Commit:** this endsession commit.

Plate 5 — the single gated step that writes all staged edge-modeling work into the canonical graph — landed successfully. Five locked-in decisions (Q1-Q4) captured ahead of execution. Matt stepped out mid-session and explicitly delegated promotion + autonomous validation ("I won't be reviewing everything you promote anyway, so promote them. then we should talk about actually using the graph to do some validation"). Net deltas: `edges.jsonl` **3,811 → 4,757 (+946)**, `events/` nodes **371 → 583 (+212)**, `_conflicts/` **+6** (1 aerys + 5 collision losers).

**What landed (in merge order):**
- Plate 0: 10 normalizer direction-flips + 3 aerys-targaryen→aerys-ii-targaryen repoints + node quarantine. 1 mutual-kill left flagged (donal-noye↔mag) per Q4=a.
- Plate 2.5: 27 wiki schema fixes (event.battle → event.wedding/feast/coronation/trial/assassination/execution/conspiracy per S86 vocab), 12 drift retypes (10 applied + 2 already-done), 4 high-conf collision merges (5 losing nodes quarantined). 2 medium/low collisions skipped per cleanup-decisions-resolved.md.
- Plate 4 cluster: 51 SUB_BEAT_OF appended + 2/3 DUPLICATE_OF applied (7 role edges repointed to wiki nodes). 1 DUPLICATE_OF skipped (`mutiny-plan-reviewed → a-storm-of-swords-prologue`: target becoming meta.chapter would violate Contract 10).
- Plate 3: 217 of 219 mints written to `events/` (2 skipped per DUPLICATE_OF); `title:` → `name:` rewrite at mint per S86 canonical surface field. 897 of 914 role edges appended (5 dropped for fuzzy-match queue per Q1=a; 12 dropped for unresolvable LOCATED_AT; 22 LOCATED_AT remapped via small fix-map per Q2=a; 7 repointed for DUPLICATE_OF). 55/55 supersede stamps applied (1 via swapped-key fallback because Plate 0 had flipped the original direction).
- S77 carryover: 2 cersei↔tyrion LOVES rows dropped, 21 ASSAULTS → ATTACKS retyped (11 stay ASSAULTS — sexual-violence canon). OWNS→BONDED_TO no-op (0 such rows).

**Validators:**
- **Type-contract validator:** kept 4,725 / dropped 32 (0.7%). All 32 drops are SUB_BEAT_OF edges with empty `evidence_quote` (Plate 4 Pass-B/Pass-C inference-only emissions; rationale-only, no quote). Rows remain in `edges.jsonl` — validator is read-only audit. **Field-name fix applied in-place** during validator review: Plate 4 staging used `quoted_evidence` instead of canonical `evidence_quote`; renamed across all 51 SUB_BEAT_OF rows (19 retained text, 32 now have an explanatory `plate5_evidence_note` field).
- **Orphan-edges audit:** node-display bullets predate Plate 5 (display bullets are pre-merge state). Net 217 fewer cat1 orphans vs 2026-05-12 baseline. Bullets NOT regenerated this session — no canonical `build-node-display-edges.py` exists; canonical authority is edges.jsonl (graph-query.py reads from there).
- **Red Wedding smoke test PASSES.** `python3 scripts/graph-query.py --neighbors red-wedding` shows 8 SUB_BEAT_OF incoming. 2-hop traversal (red-wedding ← SUB_BEAT_OF ← catelyn-is-killed) surfaces AGENT_IN (house-frey), VICTIM_IN (catelyn-stark), COMMANDS_IN (walder-frey), LOCATED_AT (twins) — all with verbatim book quotes. Reification end-to-end working as designed.

**Decisions captured (5 ahead of execution):**
- Q1=a: hub-review-queue defaults applied (0/109 minted; 5 role edges dropped for the 2 fuzzy-match queue items).
- Q2=a: built 8-slug location alias fix-map (the-eyrie→eyrie, king-s-landing→kings-landing, etc.); 10 unresolvable slugs skipped (~12 edges).
- Q3=a: 2 LOVES drops + 21-ASSAULTS retype (11 stay) + OWNS no-op.
- Q4=a: 4 high-conf collisions only; mutual-kill left flagged.
- Mid-merge DUPLICATE_OF call: skip `mutiny-plan-reviewed` because its wiki target is being retyped to meta.chapter (would violate Contract 10).

**Files modified:** `graph/edges/edges.jsonl` (the gated write); `graph/nodes/events/` +217; `graph/nodes/_conflicts/` +6; 37 node frontmatter type retypes (27 wiki + 10 drift); `graph/edges/_regrounding/edges-pre-reification-2026-06-09.jsonl` (backup). NEW: `scripts/plate5-merge.py` (~450 lines, supports `--dry-run`/`--apply`); `working/edge-modeling/plate5-merge-diff.md` (full before/after report). NEW: `history/worklog-archives/archive018.md` (S83-/tmp moved here).

**Follow-up TODOs:** (1) Display-bullet regeneration script — `## Edges` sections in node files are pre-Plate-5 state; graph-query.py works from edges.jsonl correctly, but human readers see stale bullets. (2) The 32 SUB_BEAT_OF without quoted evidence — decide between re-emit / quote backfill / Contract-6 exemption for structural edges. (3) 109 hub-review-queue entries — still in staging, defaults applied = none minted. (4) 2 deferred collision merges (conquest-of-dorne, tourney-at-maidenpool). (5) donal-noye↔mag mutual-kill — add reverse direction. (6) Post-Plate-5 backfill tracks A/B/C (~$25-75, ~300-850 edges) per `working/edge-modeling/post-plate5-backfill-design.md`.

**What's next:** Matt's stated next track is "actually using the graph to do some validation" — use the merged graph to fact-check claims, run cross-character traversal queries, exercise the reified event hubs for the use-cases the design supported. No dedicated continue prompt yet; will draft one when Matt returns and we scope the validation conversation. The 6 follow-up TODOs above are non-blocking and can be picked up opportunistically. `graph/edges/edges.jsonl` is now LIVE at 4,757 rows; `events/` at 583 nodes.
