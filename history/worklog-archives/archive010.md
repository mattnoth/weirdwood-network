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
