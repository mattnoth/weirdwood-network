### Session 45 — Mission Protocol Design (Watcher + Workers) (2026-05-12)
**Detail:** `history/session-details/session-045.md`

**Changes made:**
- `working/agent-fleet-specs/mission-protocol.md` — NEW. DRAFT v0 (NOT locked). Defines "mission" as bounded, isolated orchestration between session-task and full fleet. Sections: mission-vs-session distinction, two-role model (watcher + worker), mission file schema, worker emission contract (per-worker `status.json` + optional `questions-for-matt.jsonl` + `conflicts.jsonl`; mission-wide `_dashboard.json` + `_admiral-log.md`), watcher behavior (v1 = Matt-as-admiral, no daemon), lifecycle (queued → running → done → archived), what v1 deliberately doesn't have, daemon-deferral triggers, 5 open questions.
- `working/agent-fleet-specs/missions/` — NEW directory.
- `working/agent-fleet-specs/missions/2026-05-12-case-collision-top-10.md` — NEW. First concrete mission file, worked example of the protocol schema. Scope: top-10 case-collision pages by backlink count (small-council 215, king-in-the-north 195, free-folk 141, brotherhood-without-banners 141, narrow-sea 120, great-ranging 64, warden-of-the-north 62, old-gods 61, hedge-knight 60, master-of-coin 57). Path (a) reconstruction-from-cross-references only; refetch deferred. Queued, not started.
- `.claude/commands/watcher.md` — NEW slash command. `.claude/commands/worker.md` — NEW slash command. `.claude/README.md` — NEW index. `.claude/agents/watcher.md` — NEW v1 watcher (admiral) agent prompt (briefing-assistant model).
- Memory: `feedback_session_purpose_discipline.md` + `project_mission_protocol_v0.md`. MEMORY.md index updated.

**Decisions:** Watcher = briefing-assistant, NOT dispatcher. Mission = unit of v1 orchestration; daemon deferred. Watcher always Opus 4.7. Captain → worker rename.

**What's next:**
- Case-collision top-10 mission. Alias-backfill round 2. Year-page type fix.
- **Per Matt's standing rule, /endsession was invoked explicitly.**

---

### Session 44 — Per-LOCATION + per-ARTIFACT index roll-ups (2026-05-11)

**Changes made:**
- `scripts/build-entity-indexes.py` — NEW. Pure-Python (no LLM, no HTTP) script that builds per-entity index files for non-character node types. `--type locations` → `graph/index/locations/` (1,056 files); `--type artifacts` → `graph/index/artifacts/` (265 files); `--type houses` → `graph/index/houses/` (556 files). Section-aware for locations (in_locations_section vs in_raw_list) and artifacts (in_artifacts_section vs in_raw_list); flat in_raw_list for houses (no dedicated Pass-1 section). Per-entity stats: appearances_total, chapters_referenced_in, chapters_in_primary_section, chapters_in_raw_list, out_edge_count (from `## Edges` section bullets), in_edge_count (from backlink-counts.json). Per-chapter records carry pov_character_slug (resolved from Pass 1 frontmatter), mention_count, sections, resolved_via. Runs in <0.5s per type.
- `graph/index/locations/` — NEW. 1,056 index files + `_summary.json`. Top by appearances: kings-landing/304 (217 chapters), winterfell/300 (191), wall/205 (121).
- `graph/index/artifacts/` — NEW. 265 index files + `_summary.json`. Top: iron-throne/95 (59 chapters), longclaw/35 (25), needle/34 (22).
- `graph/index/houses/` — NEW. 556 index files + `_summary.json`. Top: house-stark/77 (77 chapters), house-lannister/71 (70), house-baratheon/52 (52).
- `working/todos.md` — marked Per-LOCATION + per-ARTIFACT index roll-ups DONE.

**Smoke-test results:** winterfell 191 chapters ✓, kings-landing 217 ✓, wall 121 ✓ (slug is `wall` not `the-wall`), meereen 38 ✓, oldtown 59 ✓; iron-throne 59 chapters ✓, heartsbane 7 ✓, longclaw 25 ✓, oathkeeper 7 ✓; house-lannister 70 ✓, house-frey 25 ✓. Zero-mention counts: locations 434/1,056 (historical/peripheral nodes), artifacts 145/265, houses 395/556.

**Decisions:** One parameterized script (not three clones) with a `TYPE_CONFIGS` dict — locations/artifacts/houses each get their own section keywords and primary_chapter_key. Houses have no `primary_chapter_key` (no dedicated Pass-1 section exists for houses; `Raw Entity List > Houses` is their main section). Section-aware field naming: `in_locations_section` / `in_artifacts_section` as type-specific keys; `in_raw_list` and `referenced_in` (union) shared across all types. POV resolution reuses the same Pass-1-frontmatter parsing approach from `build-character-indexes.py` but with lighter slug resolution (no prefix-match tiebreaking chain — sufficient for context annotation). Chapter records include `in_primary_section` and `in_raw_list` boolean flags for downstream filtering.

**What's next:**
- **Stage 4 component (b) — chapter-evidence backfill — is now fully met** for all primary node types (characters + locations + artifacts + houses). Stage 4 prose-edge-classifier can now ground edge classifications in per-entity chapter context for all primary types. Continue prompt: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`.
- **Missing-node backfill (Bucket A, 138 pages) — DONE** (Session 43 below).
- **Per Matt's standing rule, /endsession is NOT auto-run.**

---

### Session 46 — First Mission + Protocol v1 + Batch 2 Reconstruction (2026-05-12)
**Detail:** `history/session-details/session-046.md`

**Changes made:**
- `working/agent-fleet-specs/mission-protocol.md` — v0 → v1. Added "Lessons from first mission" section at top (4 findings). Rewrote Worker role: wave-sized default + dual execution modes (multi-window + subagent-orchestrated). Added mandatory schema-validation block to Worker emission contract (locked field types: status enum `{pass,partial,fail}`, numeric confidence 0.0-1.0, ISO 8601 timestamps via `datetime.utcnow().isoformat()+"Z"` with explicit "NOT placeholder" guard). "Next steps for this doc" checked 3 boxes.
- `working/agent-fleet-specs/missions/done/2026-05-12-case-collision-top-10.md` — mission moved from `missions/` to `missions/done/`; Outcome + Postmortem sections filled in.
- `working/todos.md` — first-mission todo marked DONE; HIGH case-collision item updated from "125 pages" to "10/125 reconstructed, 115 remaining"; `→ continue:` line added linking to close prompt.
- `working/missions/case-collision-top-10/worker-<slug>/` — 10 dirs (mission 1 outputs, NOT YET PROMOTED).
- `working/missions/case-collision-batch-2/worker-<slug>/` — 50 dirs (batch 2 outputs, NOT YET PROMOTED).
- `working/agent-fleet-specs/worker-snippets/case-collision-template.md` — NEW dir + NEW file. Reusable worker snippet inlining TYPE_DIR_MAP, edge vocab, v1 schema, alias-merge check, reverse-lookup default.
- `history/session-details/session-046.md` — NEW. Full session narrative.
- `progress/continue-prompts/2026-05-12-case-collision-mission.md` — DELETED (mission complete).
- `progress/continue-prompts/2026-05-12-case-collision-close.md` — NEW. Two-track handoff for closing case-collision (promotion mandatory; tail optional, multi-window+watcher).

**Decisions:** First mission ran end-to-end (10/10 returned, 0 fail, avg 0.89 conf, ~6 min wall-clock). Postmortem surfaced 4 lessons: workers wave-sized not slug-sized; task strategies must be in worker template upfront not added mid-mission; schema validation is mandatory (every worker drifted on at least one field); watcher is optional, not required. Mission protocol v1 baked these in. Batch 2 (next 50 slugs) ran subagent-orchestrated in 5 parallel waves, all schema-PASS, ~8 min total. Multi-type entity policy decided (single node + primary type + edges capture other facets, NOT split-into-multiple-nodes). War-vs-battle clarification: `event.war` already exists in architecture.md (worker drift, not missing type). Subagent vs multi-window trigger rule drafted (lands in mission-protocol.md next session).

**What's next (at time of archiving):** Close case-collision, alias-backfill round 2, Stage 4 prose-edge classifier.

---

### Session 47 — Case-Collision Promotion + Type Fixes + Protocol Edits (2026-05-12)

**Changes made:**
- `scripts/promote-case-collision.py` — NEW. Promotion script for 60 case-collision worker outputs → `graph/nodes/`. Handles CREATE (36 new nodes), UPDATE (21 existing stubs), MOVE+UPD (2 type relocations), SKIP (old-gods, already aliased). Applies locked type corrections inline (event.conflict→event.war, event.military-expedition→event.battle, bare `concept`→per-slug overrides, `titles`→`title`).
- **36 CREATE** — notable new nodes: `small-council` (factions/), `tower-of-joy` (locations/), `ghiscari-wars` (events/, typed event.war not event.conflict), `dothraki-sea` (locations/), `haunted-forest` (locations/), `hammer-of-the-waters` (concepts/), `first-night` (concepts/), `stallion-who-mounts-the-world` (concepts/, typed concept.prophecy), `children-of-the-forest` moved from factions/ to species/.
- **21 UPDATE** — stubs replaced with worker Identity: `brotherhood-without-banners`, `hedge-knight`, `king-in-the-north`, `master-of-coin`, `warden-of-the-north`, `king-beyond-the-wall`, `master-of-laws`, `master-of-ships`, `master-of-whisperers`, `red-priest`, `red-waste`, `ruby-ford`, `valar-morghulis`, `war-of-the-first-men-and-the-children-of-the-forest`, and others.
- **2 MOVE+UPD** — `free-folk`: factions/→concepts/, type organization.faction→concept.culture. `children-of-the-forest`: factions/→species/, type organization.faction→species. Both: old files deleted, new files written with worker Identity.
- **Pre-work cleanups:** `war-of-the-five-kings.node.md` type-fixed event.battle→event.war; `war-of-five-kings.node.md` deleted (empty duplicate, wrong slug); `red-priest` aliases updated to include `red-priestess` + `Red Priestess`; `crossroads-inn.node.md` stub deleted (merged into `inn-at-the-crossroads` aliases).
- **`small-council` edges** — uncommented MEMBER_OF edges from worker's narrative-evidence comments (petyr-baelish, stannis-baratheon, janos-slynt, daemon-targaryen, corlys-velaryon) + LOCATED_AT: red-keep. Infobox-data.jsonl had no entries (redirect page); reverse-lookup returned 0 results.
- `reference/architecture.md` — NEW section "Multi-type entities" under Hierarchy Query Rules. Policy: one node per real-world entity, primary type in `type` field, other facets via edges. Examples: Free Folk → concept.culture (faction-ness via edges), Children of the Forest → species (ancient-people-ness via edges).
- `working/agent-fleet-specs/mission-protocol.md` — NEW section "Choosing execution mode (subagent vs multi-window)" under Roles. Documents the trigger rule: subagent OK when self-contained + stateless + <10 min; multi-window+watcher when TYPE_DIR_MAP awareness, context loading, or drift-potential is high. Notes case-collision-batch-2 as a cautionary example.
- `working/todos.md` — case-collision HIGH item (60/125 promoted, 65 remaining) → downgraded to LOW (optional Track B, tail slugs, multi-window mission when wanted).
- Graph total: 7,915 → 7,949 nodes (+34 net).

**Decisions:** All 60 outputs promoted (36 CREATE + 21 UPDATE + 2 MOVE + 1 SKIP). Type corrections applied inline from locked vocab — no new types invented. Multi-type policy ratified: free-folk as concept.culture (not faction), children-of-the-forest as species (not faction). War-of-the-five-kings canonical slug confirmed; empty duplicate deleted. Red-priestess absorbed as alias, not separate node.

**What's next:**
- **Case-collision tail (65 slugs, optional)** — LOW priority. Track B: Python filter to classify canonical (~15) vs droppable (~50), then multi-window+watcher mission. → continue: `progress/continue-prompts/2026-05-12-case-collision-close.md` (Track B section)
- **Alias-backfill round 2** — parallel-safe. → continue: `progress/continue-prompts/2026-05-12-alias-backfill-round-2.md`
- **Stage 4 prose-edge-classifier** — next major track. → continue: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`
- **Per Matt's standing rule, /endsession is NOT auto-run.**

