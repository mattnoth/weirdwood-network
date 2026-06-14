# Worklog Archive 019

> archive019 — 5/5

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

---

### Session 88 — Plate 5 recap + validation track scoped + S87 endsession gap-fill (2026-06-09 → 2026-06-10)

**Model:** Opus 4.7 (orchestrator + execution; no agents delegated). **Detail:** none (light session — wrap-up after S87 cutoff + design substance captured in the validation continue prompt). **Commits:** `cd1f362dc` (WIP gap-fill), this endsession commit.

**Context:** S87 ended abruptly mid-endsession (chat got cut off after the Plate 5 commit landed). Matt returned, asked how Plate 5 went + what the `quoted_evidence` vs `evidence_quote` field-rename was about, then asked to scope the next track ("actually using the graph to do some validation") and to make a WIP commit + push for the missed endsession steps.

**Wrap-up conversation:**
- Plate 5 recap: `edges.jsonl` 3,811 → **4,757 (+946)**; `events/` 371 → 583 (+212); validator 4,725 kept / 32 dropped (SUB_BEAT_OF empty-evidence rows remain in JSONL as read-only audit); Red Wedding 2-hop smoke passes end-to-end.
- `quoted_evidence` vs `evidence_quote`: same semantics (verbatim book quote grounding an edge); `evidence_quote` is canonical across the whole schema; `quoted_evidence` was a divergent name in Plate 4 cluster staging; fix-in-place during merge renamed 51 SUB_BEAT_OF rows (19 retained text, 32 got explanatory `plate5_evidence_note` for inference-only Pass-B/Pass-C emissions).

**Validation track scoped:** Four modes — (1) capability validation (does the new structure work; 8 probe queries on reified event hubs); (2) canonical accuracy (fact-check vs. books; partially absorbed by Track A backfill); (3) agent grounding (the real project goal — agent with `graph-query.py` as a tool answers real ASOIAF questions); (4) surprise/discovery (aggregate queries impossible pre-Plate-5). Recommendation: Mode 1 first (cheapest, isolates the graph layer; misses route cleanly to the 6 post-Plate-5 follow-up TODOs or backfill Tracks A/B/C). Mode 3 is the real test but needs Mode 1 to settle first so debugging is tractable.

**S87 endsession gap-fill (WIP commit `cd1f362dc`, pushed):**
- `working/todos.md`: EDGE/EVENT MODELING entry flipped [~]→[x] "ALL PLATES SHIPPED INCLUDING PLATE 5 (S82-S87)"; added 6 post-Plate-5 follow-up TODOs (display bullets, 32 empty-quote SUB_BEAT_OF, 109 hub-review-queue, 2 deferred collisions, donal-noye↔mag mutual-kill reverse, backfill tracks A/B/C); replaced obsolete `→ continue:` links with new validation prompt.
- `progress/continue-prompts/2026-06-09-graph-validation.md` (NEW): 4 modes, 8 Mode-1 probes, decision points listed, recommendation noted.
- `working/edge-modeling/plate3-revalidation/` (NEW): S85-era artifacts (2 minted event nodes, role-edge staging, skipped clean dyads, supersede candidates) committed for the record.
- `~/.claude/.../project_edge_modeling_reification_direction.md` (memory, outside repo): updated S84 status → S87 ship state with the 6-followup-TODO summary.

**This endsession (additional):**
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-5-merge.md` DELETED — Plate 5 shipped, prompt obsolete.
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-4-haiku-disposition.md` KEPT — its 1,617-row re-bucketing under reify lens is still part of post-Plate-5 backfill Track B; `→ continue:` link re-added under that TODO in todos.md (was accidentally removed during gap-fill edit).
- Session 83 (Edge-modeling Plates 0+1+2) archived to `history/worklog-archives/archive018.md` (archive018 now 2/5; co-located with S83-/tmp-paths).

**Out of scope (preserved untouched):** Matt's IDE edits to `progress/continue-prompts/2026-06-08-alias-and-display-design.md`; scratch deletions; `Untitled 6.rtf` deletion; `scr` untracked file at repo root.

**What's next:** → `progress/continue-prompts/2026-06-09-graph-validation.md` (**Opus 4.7** — design judgment in interpreting probe results; deterministic query work is `graph-query.py`). Matt picks Mode 1 vs straight-to-Mode-3.
### Session 89 — Mode 1 graph-validation probes complete + Phase 1 overnight kickoff (2026-06-10)

**Model:** Opus 4.7 (orchestrator + probe interpretation). 3 `script-builder` agents launched in background at end-of-session for overnight autonomous work. **Detail:** none — full narrative in `working/session-results/2026-06-09-graph-validation.md`. **Commit:** this endsession commit.

**Probes 5-8 finished:** (5) historical-events dark zone CONFIRMED — 8/10 anchors have 0 edges; 5 exist as nodes but isolated; `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` fires exactly 1× (Rhaegar→Lyanna from AGOT Eddard XV — Pass-1 caught the dyadic act but didn't attach it to the `tourney-at-harrenhal` hub; **refines NEW TODO #9 to "structural attachment" not "extraction"**). (6) Tywin↔Mountain — 4 direct + 6 2-hop, all person-mediated, zero event bridges (Sack-of-KL absent — same dark zone). (7) Red Wedding beat-union: Walder Frey 7/8 + Roose 1, Tywin absent (off-page architect); 3 NEW wrong-direction role edges for hub-review #3. (8) `robb-is-killed` has roles + structural but NO WIELDED_IN (weapon class dark — dagger, not a named sword; continue-prompt-stated "longsword" was wrong, fixed in writeup).

**Writeup landed:** `working/session-results/2026-06-09-graph-validation.md` (full 8-probe narrative + Mode 1→Mode 3 readiness call recommending **hybrid**: build #7+#8 + apply #10 first, then light Mode 3 dip drives Track B priorities). 5 NEW TODOs (#7 `--event-participants` primitive, #8 event-alias-resolver, #9 historical-anchor structural-backfill, #10 rename `joffrey-orders-execution`, #11 role-edge citation harmonization). Plus 4 NEW hub-review-queue items (S87 followup #3 grew).

**Overnight autonomous kickoff (Matt 2026-06-10, going to bed):** 3 `script-builder` agents launched in background:
- **Agent 1 — `--event-participants` primitive (#7): DONE.** `scripts/graph-query.py` extended with `cmd_event_participants()`. 4/4 smoke tests pass: red-wedding (8 beats, 29 role edges, 13 distinct participants), tourney-at-harrenhal (clean "no beats" message), nonexistent slug (clean "hub not found"), --json (valid). Results: `working/session-results/2026-06-10-overnight-event-participants.md`.
- **Agent 2 — Event-alias-resolver (#8): DONE.** `scripts/event_alias_resolver.py` + `working/wiki/data/event-alias-lookup.json` (876 phrases, 1 correct collision on `conquest-of-dorne`). 7/9 smoke tests HIT; 2 MISS are correct ("Ned's execution" auto-resolves after #10 rename + rebuild; "the Trident" needs editorial `aliases:` entry). Results: `working/session-results/2026-06-10-overnight-alias-resolver.md`.
- **Agent 3 — Rename script + DRY-RUN (#10): DONE post-commit.** `scripts/rename-event-node.py` (513 lines, `--dry-run`/`--apply`, atomic writes). Dry-run clean: 1 node file + **6 edge rows** (5 source/target + 1 superseded_by — **matches S89 probe count exactly**) + 0 reference-file hits. Action-slug audit: 29 candidates → 6 rename / 14 keep / 9 flagged for Matt. Results: `working/session-results/2026-06-10-overnight-rename-dryrun.md`. APPLY command queued in todos #10.

**Hard rules carried:** no writes to `edges.jsonl` or `graph/nodes/`, no auto-/endsession, no progression past Phase 1. All probe commands were read-only. Plate 5 state preserved: edges.jsonl=4,757, events/=583.

**What's next:**
- Matt wakes up → review 3 overnight result files → run `--apply` for #10 if dry-run is clean → fire continue prompt to start Phase 2.
- → `progress/continue-prompts/2026-06-11-phase2-mode3-dip.md` (**Opus 4.7**) — light Mode 3 grounded-agent dip (5-10 queries against the graph), failure modes drive Track B priorities. Depends on #7+#8 agents completing successfully overnight.

---
### Session 90 — S89 overnight review + primary rename applied + remaining rename decisions queued for Opus (2026-06-11)

**Model:** Opus 4.7 (orchestrator + applied the primary rename). **Detail:** none (review + small apply + handoff session). **Commit:** this endsession commit.

**What this session was:** post-overnight review of Phase 1 results from S89 + first real apply against the renamed-rebuilt graph. Matt read the 3 overnight result files, did slug-vs-victim disambiguation explainers (Ned/Eddard alias chain, "what's a hit", S89 probe count semantics, chapter→graph→dialog query chain). Then applied the **primary** rename himself (`joffrey-orders-execution` → `execution-of-eddard-stark`) — touched 7 artifacts (1 node move + 6 edge rows). Surfaced 2 #8-deliverable bugs + a #10-script gap during apply (postmortem in todos.md #10).

**Bugs found during primary apply (2026-06-11):**
1. **`event_alias_resolver.py` (Agent #8) parser bug:** only parses inline `aliases: [...]` YAML form; block-style YAML list (`aliases:\n  - "..."`) silently corrupts to a single key. Harden the parser OR enforce inline convention as the canonical form. Matt used inline form for the apply.
2. **Agent #8's "auto-resolve on rebuild" prediction was wrong:** "Ned's execution" did NOT auto-resolve from the new slug `execution-of-eddard-stark`. It needs an explicit `aliases:` frontmatter entry — which Matt added (`aliases: ["Ned's execution"]`). Lesson: the deterministic resolver is phrase-lookup only; no semantic substitution; reader-natural phrasings must be enumerated.
3. **`rename-event-node.py` (Agent #10) coverage gap:** script rewrites frontmatter + slug-form refs in JSONL/JSON/MD files, but does NOT touch (a) the renamed node's own H1 + mint-prose body text, (b) free-text `plate5_superseded_note` fields in edge rows. Matt fixed both manually post-apply. Extend the script before any batch run.

**Verification post-primary-apply:** 0 residual old-slug refs in `graph/`; `edges.jsonl` row count unchanged at 4,757; `--health` 0 new orphans; new node's 5 edges traverse; both "Ned's execution" and "execution of eddard stark" resolve to the new slug; old action phrase is dead.

**Documentation polish:** added a plain-English preamble + TL;DR + "Your decisions" scannable table to `working/session-results/2026-06-10-overnight-rename-dryrun.md` so it's not a wall of agent output. Matt filled in his per-slug yes/no/different-suggestion decisions in that same file's "Your decisions" table — for the **5 secondary clean** candidates + **9 flagged** candidates. Those remain queued.

**No further graph writes this session beyond the primary.** `edges.jsonl` 4,757; `events/` 583. The remaining ~14 rename decisions are queued for a fresh Opus session via the new continue prompt.

**What's next:**
- → `progress/continue-prompts/2026-06-11-execute-rename-decisions.md` (**Opus 4.7**) — fresh Opus reads Matt's filled-in decisions, runs per-slug dry-run-then-apply, adds curated `aliases:` (inline form only — bug #1), patches body H1 + mint-prose + plate5_superseded_note free-text per rename (bug #3), rebuilds events index + event-alias-resolver at the end, verifies alias-chain works. Hardening of bug #1 and bug #3 in-script is OPTIONAL upgrade — work-around pattern documented in the continue prompt.
- → `progress/continue-prompts/2026-06-11-phase2-mode3-dip.md` (**Opus 4.7**) — Mode 3 grounded-agent dip. **After** remaining renames land.

---

### Session 91 — Rename execution batch + DECEIVES pilot edges + structural restructures queued (2026-06-11)

**Model:** Opus 4.7 (orchestrator + applied 9 renames + minted 3 pilot edges; 9 background sub-agents delegated for rename analysis / source verification / deception-feasibility). **Detail:** none (execution-heavy; subagent decision packets reproduced into the deferred-restructures continue prompt). **Commit:** this endsession commit.

**Changes made:**
- `graph/nodes/events/` — 9 file renames + 11 files patched (H1, mint-prose, inline-form aliases): Sand Snakes, Slynt, Dontos, Symon, Kerwin, cersei→execution-of-the-blackwater-deserters, qhorin→jon-spares-ygritte, cersei→cersei-s-plot-to-assassinate-jon-snow, wyman→wyman-publicly-arrests-davos-at-white-harbor; plus aliases-only on `ned-orders-janos-slynt-to-arrest-cersei` + sibling `gold-cloaks-betray-ned` (subagent KEEP rec).
- `graph/edges/edges.jsonl` — atomic field updates across 33 rows + 3 manual `plate5_superseded_note` free-text patches (Bug 3 — Slynt, Symon, Qhorin) + **3 curator pilot edges appended**. Count: **4,757 → 4,760**.
- 3 pilot edges: BETRAYS janos-slynt→eddard-stark (accepts-bribe-then-defects, AGOT Eddard XIV); DECEIVES cersei-lannister→jon-snow (contract-assassination, AFFC Cersei IV); DECEIVES wyman-manderly→house-frey (staged-arrest, ADWD Davos IV). Tagged `candidate_kind=curator-s91-deception-pilot`, `typed_by=curator-s91`.
- `graph/index/events/` — rebuilt via `scripts/build-entity-indexes.py --type events --all`.
- `working/wiki/data/event-alias-lookup.json` — rebuilt: 876 → 922 phrases, 1 pre-existing ambiguous collision (`conquest-of-dorne` duplicate node, NOT introduced by S91).
- CREATE `working/session-results/2026-06-11-rename-execution.md` + `progress/continue-prompts/2026-06-12-deferred-structural-restructures.md`. DELETE `progress/continue-prompts/2026-06-11-execute-rename-decisions.md` (task complete).
- `working/todos.md` — closed POST-PLATE-5 followup #10.

**Decisions:** 9 renames applied + 1 aliases-only treatment per the 9 subagent decision packets (5 ambiguous-flagged subagents launched mid-session per Matt's "use fresh sub agents for open questions"). 2 structural restructures **deferred** (Wyman-execution arc + Jaime-sheathes arc) — bigger than rename: new parent events + SUB_BEAT_OF restructure + multi-edge mints + type-field decisions; subagent decision packets reproduced verbatim into the continue prompt for Matt's ratification. Side-asks verified inline: Tyrion ordered Symon (Bronn=agent, ASOS Tyrion IV); Kerwin source backed up (ADWD Iron Suitor + wiki); WIELDS longclaw→Slynt-execution edge already existed. Deception-edges feasibility: `DECEIVES` (11 live) + `BETRAYS` (38 live) already in locked vocab — zero schema cost — pilot 3 edges now, queue scripted surfacer for ~30-50 medium-confidence retypes.

**Verification:** 10/10 alias-chain probes HIT; `--neighbors` confirms full role-edge sets attached on all 9 renamed slugs; `--health` clean; final `grep -r '<old-slug>' graph/` returns only deliberate old-slug-as-alias backrefs. Bug 1 (inline-form aliases only) + Bug 3 (body-text + plate5_superseded_note manual patches) workarounds held per rename. Mid-session surprise: alias resolver doesn't auto-convert kebab→spaces; Wyman + Qhorin aliases re-spelled in space-form.

**Look-at-twice items for Matt:** (a) `jon-spares-ygritte` typed `event.execution` (execution doesn't happen); (b) `cersei-s-plot-to-assassinate-jon-snow` typed `event.death` (Jon doesn't die); (c) `execution-of-the-blackwater-deserters` missing VICTIM_IN edge; (d) stale `status: minted-plate3` + "Staging only" body notes on all renamed nodes (Plate 5 merged but script doesn't flip status); (e) pre-existing `conquest-of-dorne` duplicate; (f) `cersei-claims-ned-s-men-attacked-first` flagged as DECEIVES candidate by 2 independent subagents (not minted — not being renamed).

**What's next:**
- → `progress/continue-prompts/2026-06-12-deferred-structural-restructures.md` (**Opus 4.7**) — apply Wyman-execution + Jaime-sheathes restructures per the verbatim subagent decision packets in-prompt. Open questions enumerated for Matt's ratification.
- → `progress/continue-prompts/2026-06-11-phase2-mode3-dip.md` (**Opus 4.7**) — Phase 2 Mode 3 grounded-agent dip. Unblocked. Can run before OR after restructures (parallel-safe).
- Backlog (deception-edges scaling): 3 pilot edges done, 7 to go per subagent C rec; then build `scripts/surface-deception-candidates.py` to mine the broader 30-50 retypes from `hint_raw` markers.

---
