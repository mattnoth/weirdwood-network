# Worklog Archive 018

> Archived Session Log entries (oldest-first within this file). Each archive holds 5 entries.
> Sessions: 83-tmp-paths, 83-edge-modeling, 84 (3/5).

---

### Session 83 — Move `/tmp` paths into `~/source/claude-cwd/` hierarchy (2026-06-05)

**Model:** Opus 4.7 (orchestrator + execution; no agents delegated). **Detail:** none (pure path-rename hygiene). **Commit:** this endsession commit.

**Changes made (path refactor; no behavior change):**
- NEW dirs: `~/source/claude-cwd/` (empty `cwd=` for `claude -p` subprocesses; sibling of repo, no parent `CLAUDE.md` to defeat the cost trick) + `~/source/claude-cwd/tmp/` (for stop-files + per-run logs).
- `scripts/stage4-tail-classifier.py`: `cwd="/tmp"` → `cwd=CLAUDE_P_CWD` constant; `STOP_FILE` uses `os.path.expanduser` over the new path. `scripts/events-drift-audit.py`: cosmetic — comments / `judge_cwd` metadata / APPLY log line (inherits the cwd from `TC.invoke_claude`).
- 13 active shell scripts (`extract.sh`, `weirwood.zsh`, `launch-extraction.sh`, `run-extraction-wave.sh`, `run-extraction-all.sh`, `stage4.sh`, `stage4-run-forever.sh`, `stage4-events-bulk-run.sh`, `stage4-haiku-loop.sh`, `stage4-haiku-run-forever.sh`, `stage4-haiku-smoke-finish.sh`, `stage4-tail-bulk-forever.sh`, `wiki-pass2.sh`): every `/tmp/{extraction,stage4,wiki-pass2,haiku-smoke}-*` replaced with `$HOME/source/claude-cwd/tmp/...`.
- `tests/test_stage4_bulk_run_apparatus.py`: assertion + comments; 42/42 pass.
- `reference/extraction-commands.md`, `working/runbooks/{stage4-events-haiku-bulk, mechanical-extraction-howto, wiki-pass2-orchestration, pass1-auto-advance-mode}.md`, `progress/continue-prompts/{2026-05-17-stage4-bulk-watcher, 2026-05-16-stage4-bulk-resume}.md`, `BEFORE-LEAVE-RESUME-2026-05-28.md`, worklog S79 line, memory `reference_llm_pass_via_claude_p.md`.

**Skipped (per "except archived files" rule):** `scripts/archive/`, `working/runbooks/archive/`, `progress/continue-prompts/archive/`, `working/session-results/` (frozen historical), `EDGE_INVENTORY_REPORT.md` (one-time report). Unrelated `/tmp` references untouched: `bucket_dir/tmp` (Pass-2 bucket-internal subdir, not `/tmp`); `/tmp/test/`, `/tmp/edge-inventory/`, `/tmp/parse_rels.py` example/throwaway paths.

**Decisions:** (1) Two `/tmp` use cases share the new root: `~/source/claude-cwd/` for the `claude -p` cwd cost trick (~49% cheaper by skipping the repo CLAUDE.md cold-load); `~/source/claude-cwd/tmp/` for stop-files + per-run logs. (2) Verified nothing was in flight in `/tmp` at time of change (no processes, no stop-files, no log files) — pure code rename, nothing on disk moved. (3) Shell uses `$HOME/source/claude-cwd/tmp/...` (POSIX-portable inside quoted strings); Python uses `os.path.expanduser("~/source/claude-cwd/tmp/...")`. Test assertion now uses `os.path.expanduser` so it doesn't hard-code Matt's homedir.

**What's next:** No new track from this session — the path refactor is self-contained and complete. Queued prior-session work is unaffected: → `progress/continue-prompts/2026-06-04-edge-modeling-cleanroom-execution.md` (S82, **Opus 4.7**) is the most recent live track; `progress/continue-prompts/2026-06-01-events-bulk-escalation-pick.md` (S81) partially superseded by S82's cleanroom reframe; 3 core-cleanups still gated on Matt since S77.

---

### Session 83 — Edge-modeling reification Plates 0+1+2 shipped (D2 resolved) (2026-06-05)

**Model:** Opus 4.7 orchestrator. Plate 0 → `script-builder` (Sonnet). Plate 1 → `general-purpose` (Sonnet). Plate 2 → `general-purpose` (Opus, analysis + D2 decision). **Detail:** `history/session-details/session-083.md`. **Commits:** `5bc168b4d` (Plate 0+1), `03442d0a0` (Plate 2 + continue prompts), `a7046ec58` (SESSION-LOG closing summary), this endsession commit.

**Context:** Third Session-83 work-block in calendar-day 2026-06-05, following S83/path-rename (earlier). This block executed the full "safe first move" from `working/edge-modeling/edge-modeling-reification-design.md` §9 Decision #1 — Plates 0+1 in parallel, then Plate 2.

**Plate 0 (deterministic, $0):** `scripts/edge-direction-normalizer.py` + `scripts/aerys-slug-merge.py`. Normalizer flagged **10 inverted edges** out of 3,811 (cressen↔melisandre KILLS, arya↔sandor CAPTURES, tyrion↔shae BETRAYS, +7) using an edge-type-aware reverse-signal lexicon — experience/state types (PRISONER_OF, SERVES, RESENTS) explicitly excluded since their passive phrases are semantic, not inversions. 3,800 kept, 1 flagged (mutual kill). Aerys merge repointed 3 phantom `aerys-targaryen` edges to canonical `aerys-ii-targaryen`. All output staged in `working/edge-modeling/` — `graph/edges/edges.jsonl` UNTOUCHED.

**Plate 1 (doc-only, $0):** `.claude/agents/mechanical-extractor.md` line 188 head rule (Column A = semantic agent, never grammatical subject/POV); line 136 optional Events & Actions role sub-bullets (Agent/Patient/Instrument/Location/Instigator/Outcome). Parser at `scripts/stage4-pass1-extra-tables.py:521-537` VERIFIED sub-bullet-safe (only matches `^\d+\.\s+`). `reference/architecture.md`: `AGENT_IN` + `VICTIM_IN` (Person/House → event.*) added line 237-238, `COMMANDS_IN` widened to cover orderer/instigator role, vocab 163→165 at line 551. `scripts/stage4-type-contract-validator.py` Contract 10 added: AGENT_IN/VICTIM_IN with non-event target → DROP.

**Plate 2 (analysis, $0):**
- **2a Pass-1 event coverage** — `scripts/plate2-event-coverage.py` walks all 344 extraction files, parses `## Events & Actions` bold titles, joins against `graph/index/events/` chapter-evidence + slug exact-match. Output: `working/edge-modeling/plate2-event-coverage.{md,json}`. Counts: **8,384 total Pass-1 event entries** / **8,317 distinct titles (floor)** / **1 exact title→slug match** / **8,316 distinct titles needing mint (floor)**. Only **38 of 371 event nodes** (10%) have ANY Pass-1 chapter linkage — the rest are wiki-derived nodes built from the Wars & Conflicts column, which only catches historical-event names. The chapter-evidence join CAN'T be Plate 3's primary binding mechanism.
- **2b `graph-query.py` traversal check** — `working/edge-modeling/plate2-graphquery-traversal.md`. Code-read + live probes. `cmd_path()` (`scripts/graph-query.py:794-809`) computes 2-hop bridges via untyped neighbor-set intersection over `edges.jsonl`. No node-type filter, no edge-type filter. Live probes: `--path eddard-stark robb-stark` already bridges through `winterfell` (location.castle) and `house-frey` (house.*); `--path robb-stark roose-bolton` returns 12 bridges including non-character intermediates. **Person→event→person traversal will work transparently once Plate 3 role edges land.** Zero engineering changes needed.
- **D2 RESOLVED — option (a) Replace.** Recorded in `working/edge-modeling/edge-modeling-reification-design.md` §3 (new "D2 RESOLVED" subsection after D7). Reification is sufficient — `--path` traverses person→event→person via the same untyped 2-hop mechanism that already handles location/house bridges. No materialized agent→patient dyad: option (c) Project would re-introduce the underdetermination problem D2 was designed to kill (which participant becomes the canonical `source`?). Superseded person→person binaries marked `superseded_by` (NOT deleted; CLAUDE.md hard rule).
- **Spot-check verdicts:** Bran's defenestration → **NEEDS MINTING** (no node exists). Tywin's privy death → **REUSE `assassination-of-tywin-lannister`** (node exists, chapter linkage broken, re-bind needed). Purple Wedding → **REUSE `purple-wedding`** (same — node exists, chapter linkage broken). The design doc §3 D3's claim "Purple Wedding poisoning and Tywin's privy death have no hub" is FACTUALLY WRONG — both nodes exist; what's missing is the chapter→event linkage in their index. Plate 3 design needs updating for this.

**Unexpected findings:**
1. 90% of event nodes have no Pass-1 chapter linkage. The chapter-evidence index built from Raw Entity List > Wars & Conflicts catches historical names only, not narrative beats. Plate 3 must mine titles directly.
2. The "needs minting" floor of ~8,316 distinct titles is only realistic if Plate 3 reifies EVERY narrative micro-beat ("Departure at daybreak", "Ride back toward Winterfell"). A selective Plate 3 (kill/betray/attack/poisoning beats only) would be much smaller. **NEW Plate 3 design question:** reify-all vs reify-selective. Out of scope for Plate 2.

**Decisions:**
- D2 → option (a) Replace (recorded).
- Plate 3 may NOT generate canonical agent→patient dyads — events are nodes, full stop.
- Plate 3 design doc needs a §3 D3 correction (named-event coverage exists more than D3 claimed; mint-scope is narrative micro-beats + a handful of named cases).

**Files touched (this block):**
- CREATE `scripts/plate2-event-coverage.py`
- CREATE `working/edge-modeling/plate2-event-coverage.{md,json}`
- CREATE `working/edge-modeling/plate2-graphquery-traversal.md`
- APPEND `## D2 RESOLVED` subsection to `working/edge-modeling/edge-modeling-reification-design.md` §3
- APPEND Plate 2 section to `working/edge-modeling/SESSION-LOG.md`
- (this entry) `worklog.md` + archive017.md (Session 79 moved)
- Did NOT touch `graph/edges/edges.jsonl`, `graph/nodes/`, Plate 0 staged outputs, or Plate 1 doc commits.

**What's next:** Three continue prompts written, each self-contained:
- → `progress/continue-prompts/2026-06-05-edge-modeling-plate-3-backfill.md` (Sonnet; HELD on Matt Q1 reify-all-vs-selective + Q2 fuzzy-reuse-vs-mint-floor — both questions documented inline in PRE-WORK DECISION block)
- → `progress/continue-prompts/2026-06-05-edge-modeling-plate-4-haiku-disposition.md` (Opus for bucketing, Sonnet for filter pass; HELD on Matt go)
- → `progress/continue-prompts/2026-06-05-edge-modeling-plate-5-merge.md` (Sonnet for deterministic merge; HELD on Plates 3+4 staging + Matt before/after sign-off — this is the only irreversible plate)

Plate 4 (1,617 Haiku bulk re-bucketing) absorbs the S81 Events Haiku NO-GO. Plate 5 also folds in the 3 S77 core-cleanups (2 cersei↔tyrion LOVES drops, ~22 ASSAULTS→ATTACKS retypes, OWNS→BONDED_TO for direwolves/dragons). Design-doc §3 D3 needs a stale-mark before Plate 3 runs (named-event nodes mostly EXIST; what's missing is chapter linkage).

---

### Session 84 — Edge-modeling Plate 3: audit loop built, pipeline validated, full sweep HELD (resumable) (2026-06-06 → 2026-06-07)

**Model:** Opus 4.7 orchestrator; `script-builder` (Sonnet) for all pipeline/cleanup/hardening tracks; `general-purpose` (Opus) for the independent alignment audit. **Detail:** `history/session-details/session-084.md`. **Commit:** this endsession commit.

**Audit loop (NEW, codified):** two reusable prompts — `working/edge-modeling/audit-repo-reporter-prompt.md` (in-repo agent, gathers facts → `SESSION-LOG.md`) + `audit-alignment-auditor-prompt.md` (fresh session, judges vs design intent → ON-COURSE/DRIFT/NO-GO verdict that gates the next plate). Runbook: `working/runbooks/edge-modeling-audit-loop.md`. An independent Opus auditor blessed the Plates 0–2.5 block = **ON COURSE** (independently recomputed edges.jsonl=3811, canonical_type_count=165, normalizer flips=10, 0 canonical writes).

**Staged cleanups (zero graph writes):** Track A drift-reclassify — 12 `event.battle`→`meta.chapter` candidates (TWoW/ASOS chapter articles misfiled), 0 affected edges. Track B collision-merge — 6 near-dup event groups (4 high-conf auto; `conquest-of-dorne` = book-vs-event, don't-merge → reclassify book to object.text; `tourney-at/of-maidenpool` needs wiki check), 0 affected edges. Plate 2.5 inventory — `scripts/event-node-inventory.py` → reuse lookup (1,033 keys / 359 reuse-eligible / 12 drift flagged).

**D8 (NEW design decision):** reify on n-ary STRUCTURE, not event TYPE — clean dyads (Jaime/Aerys, Tyrion/Tywin) stay direct edges; only contested/multi-participant events reify. Shrinks node-minting to near-zero. Recorded in design doc §3 (+ D3 RE-EXAMINED note: Tywin/Purple-Wedding nodes DO exist, just unlinked).

**Plate 3 pipeline:** `scripts/edge-reify-backfill.py` built + validated on a 12-event mini-batch ($0.81) — D8 gate, D7 causation, multi-chapter dedup, reuse-before-mint, group/faction AGENT_IN, Contract 10 (68/68) all pass. Found + fixed a supersede false-positive bug (added chapter-overlap requirement; mini-batch 33→12, re-validated). Runner HARDENED (code-only): fail-fast on rate wall (<~90s, no retry-burn), incremental per-event flush, `processed-events.jsonl` ledger, `--resume` (verified 0 duplicates via dry-run + mock-wall).

**Incident (postmortem in detail file):** an overnight unattended full sweep was killed ~6 min in by the rate wall, then sat in retry/backoff burning usage before the fail-fast fix existed. Lesson → fail-fast + resumability are mandatory for long `claude -p` passes.

**Revised scope/cost:** dry-run enumerated **~2,056 trigger-family candidate events** (vs the 200-300 estimate); real sweep cost ~$50-160. Recommend a cost-bounded **calibration chunk** before committing to the full run.

**Graph integrity:** `edges.jsonl`=3811, 0 nodes minted into `graph/`, `git status graph/` clean — untouched throughout.

**What's next:** → `progress/continue-prompts/2026-06-07-edge-modeling-plate3-resume.md` (**Opus 4.7** — see addendum; attended, calibration chunk first). Then Reporter → fresh Auditor → Plate 5 gated merge. Plate 5 folds in the staged cleanups + Plate 4 (Haiku bulk) + the 3 S77 core-cleanups. Full Plate 3 status report in `working/edge-modeling/SESSION-LOG.md`.

**Post-endsession addendum (2026-06-07, same session — Plate 3 agent now RUNNING in a separate window):**
- **`--all` selective-gate bug found + flagged OPEN (NOT fixed).** The overnight `--all` run minted narrative micro-beat hubs (`departure-at-daybreak`, etc.) → the D8/Q1 selective gate is not enforced in the `--all` path (it IS in `--batch`); the dry-run stub bypassed it so it was never verified. That stale partial (`plate3-full/`) was EXCLUDED from git as contaminated. Next session must fix+verify the gate, `rm -rf plate3-full/`, then run. Recommended model bumped Sonnet→**Opus 4.7** (session now leads with the gate-fix reasoning).
- **Canonical auto-resume wrapper spec** added to the resume prompt (reuse `stage4-run-forever.sh` / `stage4-events-bulk-run.sh` patterns: sleep-until-reset, stop-file, MAX_ITER, short inter-batch pacing, fail-fast + graceful exit, internal `claude -p` cap ~5). Directly prevents a repeat of the overnight retry-loop window-burn.
- **Memory entry NEW:** `project_edge_modeling_reification_direction` — captures the current edge strategy + how the dead branches (wiki-comention/Pass-1-spine/Events-Haiku/enrichment) relate, so direction can't be lost.
- **Repo audit queued (post-Plate-3):** → `progress/continue-prompts/2026-06-07-repo-audit-strategy-reconciliation.md` (**Opus 4.7**) — reconcile 84 sessions of strategy sediment, fix stale worklog checkboxes, archive superseded continue prompts, consolidate memory. Linked in todos.md (HIGH, Doc Hygiene). Run it AFTER Plate 3/5 settle.
- Commits this session-tail: `8aa595bc1` (S84 endsession), `d13fd2c8d` (gate-bug OPEN + Opus), `3b06ea0cb` (wrapper spec), `c22d1181d` (audit-session capture). The live Plate 3 agent owns `scripts/edge-reify-backfill.py` + `plate3-full/` (left uncommitted/untouched here).
