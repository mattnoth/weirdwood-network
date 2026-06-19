# Worklog Archive 021 — Sessions 97–101

> Archived from `worklog.md` per CLAUDE.md rule #8 (5 entries per archive file — now FULL, 5/5). Newest-first within the file follows the worklog convention. Session 97 archived 2026-06-16 (Session 102 endsession); Session 98 archived 2026-06-16 (Session 103 endsession); Session 99 archived 2026-06-17 (Session 104 endsession); Session 100 archived 2026-06-18 (Session 105 endsession); Session 101 archived 2026-06-19 (Session 106 worklog update).

### Session 101 — Events/time design + deterministic event dating SHIPPED + Mode-3 dip re-run (2026-06-16)
**Detail:** `history/session-details/session-101.md`
**Model:** Opus 4.8 (1M context) orchestrator + ~14 Sonnet 4.6 subagents (dip re-run; 4-lens events/time panel; era research→analysis pipeline; 4-stance next-move panel; worklog-rotation advisor; 2 script-builder runs). **Commits:** `36abaabf` (archival) + `2eacbf7c` (dating+design) + this endsession commit.

**Changes made:**
- **Event in-world dating SHIPPED (deterministic, $0, +0 edges):** 112 `event.*` nodes gained an `occurred:` block (`ac_year` + `precision:year` + `basis_source:wiki-year-page` + `basis_reliability:tertiary-fan` + `date_confidence:tier-3`) from `chronology-events.jsonl` (single attested year + exact slug match); **29 also gained `narrative_first`** (`{book}-{chapter_number}`, min reader-encounter, resolve-all-or-skip across both edge ref formats). NEW `scripts/date-event-nodes.py` + `scripts/backfill-narrative-first.py` (+64 tests; **pytest 1295 pass / 3 documented fails**). Frontmatter-only, idempotent, bodies byte-preserved, `--health` unchanged (8,528/21,993/62). `reference/architecture.md`: `occurred:` schema + sub-field table documented.
- **Mode-3 dip RE-RUN** → `working/session-results/2026-06-15-mode3-dip-rerun.md`: **4 correct / 6 partial / 0 failed** (was 4/2/4). + temporal mini-probe (4/5 time queries fail today → motivated dating).
- **Design trail:** `working/design-opinions/` (events/time 4-lens panel + SYNTHESIS; era research + analysis) · `working/next-move-decisions-2026-06-16.md` (the 4 entry points) · `working/session-results/2026-06-16-event-dating-{dryrun,APPLIED}.md` + `2026-06-16-narrative-first-dryrun.md`.
- **Repo hygiene:** 4 historic top-level markdowns `git mv` → `history/archive/` (BEFORE-LEAVE-RESUME, EDGE_MODELING_VALIDATOR_LOG, STAGE4-SMOKE-REVIEW, next.md). Top level keeps CLAUDE/worklog/README + clusters-primer + scr.

**Decisions:**
- **Re-ran the S96 Mode-3 dip (now in archive020) on the current graph** — its arc DE-PRIORITIZATION (S96 D3) CONFIRMED a 2nd time (the measured gaps are causal-edge + `ATTENDS`, not missing arcs); recent work paid off (4 fails→0; Tourney-at-Harrenhal 0→25 edges; S96 Track-7 resolver fix verified shipped). Arc wave 1 stays parked; shipped **event dating** instead (dip-driven sequencing).
- **Events/time = TWO axes** (in-world `ac_year` vs narrative `narrative_first`); time lives in node frontmatter; ordering edges DERIVED not authored. **Era schema: signed `ac_year` (negative=BC), NO `era:AC|BC`** (collides with the existing epoch `era` field, architecture.md:438); 9-invariant validator. `long-night` excluded (wiki mention-index error — prehistoric, not 297 AC).
- **`PRECEDES`/`FOLLOWS` is GATED, not mechanical:** not in the locked vocab (deferred schema decision, roadmap D3) AND 0 dated events share a `PART_OF` parent → no cluster to order within. Needs Matt's vocab + grouping call. **Causal `TRIGGERS`** = the dip's measured gap; interpretive → Matt sign-off.
- **Worklog rotation:** archived S96 normally (→ archive020, 5/5) + anchored the S96-dip reference in this entry, rather than pausing rotation (fresh-advisor call: a paused rotation silently lapses after one context reset — a documented failure mode here). Optional future safeguard logged in todos (pytest session-count guard).

**What's next — 4 decisions, ALL for Matt** (`working/next-move-decisions-2026-06-16.md`):
- → **resolve all 4:** (1) `PRECEDES`/`FOLLOWS` vocab D3 + grouping basis (0 dated events share a `PART_OF` parent) · (2) causal `TRIGGERS` sign-off (Robert's Rebellion pilot) · (3) dating leftovers (5 spans / `long-night`-as-era / `conquest-of-dorne` book-vs-event / 10 mistyped `*-ac` year nodes) · (4) Fable cleanup (nomenclature scheme + repo-reorg). Continue: `progress/continue-prompts/2026-06-16-next-move-decisions.md` (**Sonnet 4.6**) — opens by asking Matt to answer them.

### Session 100 — Historical-anchor #9 wave 2 SHIPPED (4 WO5K hubs attached) (2026-06-15)
**Detail:** none (pure-execution session — wave-2 attach via the established S97 machine; worklog entry suffices).
**Model:** Opus 4.8 (1M context) orchestrator + 4 parallel Sonnet 4.6 `general-purpose` research subagents (one per hub). Continue prompt recommended Sonnet 4.6; Opus was the active session (graph-mutating-run insurance). **Commit:** uncommitted at write time (endsession pending Matt's permission).

**Changes made:**
- `graph/edges/edges.jsonl` **21,950 → 21,993 (+43)**: historical-anchor #9 wave 2 — attached 4 isolated WO5K hubs that POV chars witnessed/recall. **siege-of-riverrun** 2→13 (AFFC Jaime POV; 11 on-page tier-1: Daven/Jaime/Ryman/Blackfish COMMANDS_IN, Edmure VICTIM_IN, Frey-parley + garrison ATTENDS), **battle-of-the-camps** 1→12 (AGOT Catelyn; Robb/Brynden/Jaime COMMANDS_IN, Tytos/Umber/Forley/Grey-Wind FIGHTS_IN, Edmure/Brax VICTIM_IN, Hoster ATTENDS), **battle-of-oxcross** 1→8 (ACOK recalled, all tier-2: Stafford/Stevron/Martyn VICTIM_IN, Karstark/Grey-Wind AGENT_IN), **melee-at-bitterbridge** 0→14 (ACOK Catelyn; Brienne/Loras/Ronnet FIGHTS_IN, Renly/Catelyn/gallery + feast-night lords ATTENDS). Provenance: 33 book-pass1 (22 tier-1 / 11 tier-2 recalled) + 10 wiki-historical-anchor (tier-2 max). Backup `graph/edges/_regrounding/edges-pre-historical-anchor-2026-06-15T23-03-00.jsonl`.
- Tooling reused unchanged (`scripts/historical-anchor-{candidates,validate,mint}.py`). Candidates+notes in `working/historical-anchor/`; **wave-1 stale candidate artifacts archived** → `working/historical-anchor/wave1-archive/` (8 hub files + wave-1 `_merged`) so validate/mint only see wave-2.
- **Quote-enrichment follow-on (same session, Matt-requested re `capture-quotes-during-research` rule):** the 4 subagents had read real chapters but only edge-grounding quotes were captured. Re-swept the already-read chapters (acok-catelyn-02 feast, AFFC Jaime siege, agot-catelyn-11, acok-sansa-03) → **48 candidate quotes** (food/physical/identity) in `working/historical-anchor/quotes/*.quotes.jsonl`, then **applied 47 to 25 node `## Quotes` sections** (1 already present) via NEW `scripts/apply-node-quotes.py` (idempotent, dry-run-default, additive/node-scoped — safe alongside concurrent agents). Highlights: Aerys II's physical description (most detailed in text), Riverrun stone-ship architecture, Bitterbridge feast menu, Hoster Tully's decline. SPEC.md gained a standing "capture incidental load-bearing quotes as you go" step so future waves do this automatically. No edges.jsonl change; pytest unchanged.

**Decisions / judgment calls:**
- **Curated 4 hubs, deferred 3.** Skipped `battle-of-oxcross`-class hubs already well-connected by the S94 infobox merge (oxcross/camps were still isolated; `battle-of-the-fords`/`ashford` pair already connected or duplicate-tangled). **Deferred `siege-of-storms-end`** — it is part of a duplicate cluster (`-299`/`-300`/`-recalled`); attaching to one risks worsening fragmentation. Needs a dedup decision before attach.
- **2 curator fixes pre-mint:** (a) `battle-of-the-camps` Robb/Brynden COMMANDS_IN quote was non-verbatim (straight-vs-curly quotes) and over-tiered — repaired to a verbatim substring + downgraded tier-1→2 (Catelyn affirms outcome after arriving, not on-page command-witness). (b) DROPPED `melee` emmon-cuy ATTENDS — its quote was from a different chapter describing Rainbow-Guard sentry duty, not melee attendance (semantic-drift failure mode the SPEC warns against).
- **Verification:** validator 0 issues (43 edges); `--health` orphans unchanged at 62 (no new orphans, all endpoints node-resolved); flagship `--neighbors` confirm all 4 hubs traversable; pytest **1231 pass / 3 documented pre-existing fails** (vocab 166≠163 ×2, cwd-is-tmp). Consumer query for these direct-attach hubs is `--neighbors` (not `--event-participants`, which traverses SUB_BEAT_OF only).

**What's next:**
- → **narrative-arc wave 1 mint** — `progress/continue-prompts/2026-06-15-arc-wave1-mint.md` (**Sonnet 4.6**) — **GATED on Matt's 3 decisions** (RW-4 role edges / arc boundaries / RECIPIENT_IN).
- → historical-anchor #9 **wave 3 (optional, low priority):** the deep-lore wiki-only set (Doom of Valyria, Blackfyre Rebellions, etc.) is approach (b) — pure `wiki-historical-anchor`, defer until a dip shows agents asking about them. `siege-of-storms-end` cluster needs dedup first.
- → Track 6 script consolidation: the 3 `historical-anchor-*.py` scripts are one-offs to fold into the `weirwood` CLI per Matt's directive.

### Session 99 — Script consolidation Session 2: archive one-offs + weirwood CLI aliasing + README refresh (2026-06-15)
**Detail:** `history/session-details/session-099.md`
**Model:** Opus 4.8 (1M context) — mechanical work (continue prompt recommended Sonnet 4.6; Opus was the active session). **Commit:** this endsession commit.

**Changes made:**
- **Archived 30 scripts** `git mv` → `scripts/archive/` (24 verified-safe early Stage-4 `classify-*`/`temp-*` one-offs + `stage4-haiku-smoke-prep.py` sibling + `migrate-stats-csv.py` + 4 shelved wrappers: `stage4-haiku-run-forever.sh`, `stage4-haiku-loop.sh`, `stage4-tail-bulk-forever.sh`, `stage4-events-bulk-run.sh`). **KEPT** `stage4-run-forever.sh` (proven ref) + `edge-reify-run-forever.sh` (registry PLANNED) + 27 comention scripts. Archive now 32 files.
- **9 frozen stats CSVs** `git mv` → `working/extraction-stats/_archive/` (Pass 1 = 344/344; nothing appends). Added `_archive/` read-fallback to `pace.py backfill`, `extract.sh status`, `wiki-pass2.sh` cost glob so nothing silently degrades; fixed 2 `test_pace.py` skip-guards (suite back to 0 skips).
- `scripts/extract.sh` — de-referenced `migrate-stats-csv.py` call (one-time migration complete; breadcrumb comment).
- **NEW** `scripts/weirwood-refresh.sh` (rebuild all 17 entity-index types + character indexes + alias resolver; `--check` staleness warn per §13 S8). Wired `weirwood graph`/`resolve`/`refresh` into `scripts/weirwood.zsh` + help text on running any script under longrun.
- `scripts/weirwood-run.sh` — 3 archived-wrapper paths → `scripts/archive/`; header rewritten.
- `scripts/README.md` — **rewritten as universal index**: Class (A/B/C/D) column + `Added` git-date provenance + invocation + §11.5 new-script checklist. Existence-truth: all 124 live + 32 archived scripts have a row.
- `working/orchestration-pacer-design-2026-06-15.md` §0 — 4 Session-2 rows flipped to **BUILT S99** (file + verification); banner → BUILT; CSV-quirk RESOLVED; corrected "484 rows" → 476 work rows + 8 wall events.

**Decisions:** Three Matt-decisions (AskUserQuestion, all "Recommended"): de-reference+archive `migrate-stats-csv.py`; archive frozen CSVs to `_archive/`; archive the 4 shelved wrappers + update registry. One cross-scope judgment call flagged: the moved CSVs are read by 3 living status commands → added read-only `_archive/` fallbacks rather than accept silent degradation. pytest **1231 pass / 3 documented pre-existing fails** (vocab 166≠163 ×2; cwd-is-tmp), 0 skips. Orchestration/pacer track (design §0) now fully BUILT.

**What's next:**
- → **historical-anchor #9 wave 2** — `progress/continue-prompts/2026-06-15-historical-anchor-wave2.md` (**Sonnet 4.6**).
- → **narrative-arc wave 1 mint** — **GATED on Matt's 3 decisions** (RW-4 role edges / arc boundaries / RECIPIENT_IN). Prompt PARKED in `continue-prompts/archive/2026-06-15-arc-wave1-mint.md` (one-live-prompt policy, Matt S99); restore when decided. (**Sonnet 4.6**)
- Loose end (todos): wire `weirwood refresh --check` into a git pre-commit hook (design §13 S8) — needs Matt's workflow buy-in.

### Session 98 — Script consolidation Session 1: orchestration/pacer BUILT + design-doc anti-drift convention (2026-06-15)
**Detail:** `history/session-details/session-098.md`
**Model:** Opus 4.8 (orchestrator + direct verification) + script-builder subagent (the build). **Commit:** this endsession commit.

**Changes made:**
- **NEW** `scripts/pace.py` (Class A-pacer; v1 report-only): `backfill` normalizes 6 heterogeneous stat schemas → per-track `working/telemetry/<track>.jsonl`; `report` prints per-`(track,model,unit_type)` baselines + conservative `LONGRUN_SLEEP_BETWEEN=600` + honest M3 wall-cadence disclaimer; `emit_telemetry_row()` importable helper. **NO ETA/headroom/concurrency in v1** (wall data too thin, §13 M3).
- **NEW** `working/telemetry/` — backfilled ledger: 484 rows / 9 tracks (pass1-{agot,acok,asos,affc,adwd}, wiki-pass2-{core,secondary}, stage4-{haiku,v1-bulk-sonnet}) + 2 `.walls.jsonl` sidecars. Dup-race deduped (`acok-davos-02` kept 247s row, dropped 6s placeholder).
- **NEW** `scripts/worker-template.py` (copy-me reference worker): §4 contract + §13 M1 (positive-wall `exit(2)` only + `next-eligible`) / M2 (atomic `os.replace` + `O_EXCL` claim) / M4 (single-worker-durable v1). **NEW** `tests/test_pace.py` (40 tests).
- `working/orchestration-pacer-design-2026-06-15.md` — Status flipped DESIGN→PARTIALLY BUILT; **NEW §0 Implementation Status table** (anti-drift seam) + CSV-quirk note.
- `progress/continue-prompts/2026-06-15-script-consolidation.md` — Session 1 marked DONE; Session-2 carryover (CSV archival decision) + anti-drift definition-of-done gate added.
- **NEW** memory `feedback_design_doc_implementation_status` (+ MEMORY.md index). S93 archived → `archive020.md` (now 2/5).

**Decisions:**
- **§11 open questions NOT re-asked** — design §12 already resolved them (per-track files / advisory-only / sequential-default / v1 report-only) after fresh review; continue-prompt step-2 instruction was stale (CLAUDE.md rule #9 → trusted updated doc).
- **Verified the build directly** (not just subagent claim): grepped worker-template for M1/M2 implementation; confirmed dedup + report output. pytest **1231 pass / 3 documented pre-existing fails** (vocab 166≠163 ×2; cwd-is-tmp), was 1191.
- **Anti-drift convention** (Matt's drift concern): design docs get a §0 Implementation Status table (BUILT/DEFERRED/DRIFT + file + test); README = existence-truth; Fable doc-truth audit checks parity; def-of-done gate. The §0 table is a convention, not code-enforced — only `weirwood refresh --check` is mechanical; Fable audit = periodic backstop.
- **Honest scope held:** Session 2 (cleanup/CLI/README) NOT started — deferred per design §14.

**What's next:**
- → **Script consolidation Session 2** — `progress/continue-prompts/2026-06-15-script-consolidation.md` steps 5–8 (**Sonnet 4.6**): archive 24 one-offs + resolve 2 blocked; legacy-wrapper disposition (do NOT archive edge-reify); `weirwood graph/resolve/refresh` aliasing; README class/provenance refresh; CSV-archival decision; reconcile §0 anti-drift table.
- → historical-anchor #9 wave 2 (`2026-06-15-historical-anchor-wave2.md`, Sonnet) + narrative-arc wave 1 mint (`2026-06-15-arc-wave1-mint.md`, Sonnet — GATED on Matt's 3 decisions).

### Session 97 — Historical-anchor #9 wave 1 SHIPPED + Orchestration/Pacer design doc (2026-06-15)
**Detail:** `history/session-details/session-097.md`
**Model:** Opus 4.8 orchestrator + Sonnet 4.6 subagents (8 historical-anchor research + 1 sequencing advisor + 1 design reviewer). **Commit:** uncommitted at endsession (Matt to decide).

**Changes made:**
- `graph/edges/edges.jsonl` **21,829 → 21,950 (+121)**: historical-anchor #9 wave 1 (+118 across 8 isolated R+L=J/Robert's-Rebellion hubs) + 3 Trident COMMANDS_IN (Robert/Rhaegar/Lewyn). Hubs: `tourney-at-harrenhal` 0→25, `the-hands-tourney` 0→33, `battle-of-the-trident` 2→16, `sack-of-kings-landing`, `combat-at-the-tower-of-joy`, `greyjoy-rebellion`, `defiance-of-duskendale`, `tragedy-at-summerhall`. **NEW evidence_kind `wiki-historical-anchor`** (Tier-2 max; 19 edges). Backups in `_regrounding/`.
- NEW scripts: `scripts/historical-anchor-{candidates,validate,mint}.py` + `working/historical-anchor/SPEC.md` + per-hub candidate/notes files. NEW `tests/test_longrun_supervisor.py` (6 tests, longrun exit-10/2/0/crash/resume verified).
- NEW `working/orchestration-pacer-design-2026-06-15.md` — design doc (supervisor/worker/pacer architecture, exit-code contract, telemetry ledger, §1.5 script taxonomy A/B/C/D, §11 Script Org Standard, §13 review amendments, §14 two-session scope). Fresh-reviewed.
- NEW memory `project_rebuild_derived_artifacts_after_node_mutation` (+ MEMORY.md index). NEW continue prompts: `2026-06-15-historical-anchor-wave2.md`, `2026-06-15-script-consolidation.md` (2-session split).
- `worklog.md` (this entry; S92 archived → `archive020.md`), `working/todos.md` (#9 wave1 done, script-consolidation pointer), `working/historical-anchor/`.

**Decisions:**
- **Pivoted from the queued arc-mint to followup #9** (fresh advisor + worklog order both said #9-first; arc mint maps to 0 dip questions). **Arc wave-1 mint stays drafted-but-unminted, still gated on Matt's 3 decisions** (RW-4 role edges / arc boundaries / RECIPIENT_IN). #9 method: curate the main-saga-recalled cluster (the ~300 deep-lore hubs are wiki-only, out of scope), per-hub Sonnet subagent → JSON attach edges → 2-stage verbatim validation → curator drop/fix (6 dropped, 4 fixed). Provenance: book-pass1 tier-1/2 earned by chapter quote; wiki-only → `wiki-historical-anchor` tier-2 max.
- **Script consolidation = design-doc-first** (Matt). Architecture: bash `longrun.sh` wraps a resumable Python worker (emits 0/2/10) + a Python `pace.py` pacer mining past run-stats; `weirwood` CLI front door; per-worker JSONL telemetry (fixes the real CSV-append race). Review found 4 must-fix spec gaps (positive wall-detect-or-crash; atomic state writes; honest thin wall-cadence backfill; shared next-eligible for concurrency → v1 single-worker). **Honest scope = TWO sessions** (pacer, then cleanup).
- **TWOIAF (6th source, on disk unextracted) + F&B (7th, not on disk) backlogged**; use wiki for deep-lore hubs now.

**What's next:**
- → **Script consolidation Session 1 (orchestration/pacer)** — `progress/continue-prompts/2026-06-15-script-consolidation.md` (Sonnet 4.6). Recommended next.
- → historical-anchor #9 wave 2 — `progress/continue-prompts/2026-06-15-historical-anchor-wave2.md` (Sonnet 4.6).
- → narrative-arc wave 1 mint — `progress/continue-prompts/2026-06-15-arc-wave1-mint.md` (Sonnet 4.6) — **GATED on Matt's 3 decisions**.
