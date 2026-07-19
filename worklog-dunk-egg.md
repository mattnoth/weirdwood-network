# The Weirwood Network — Dunk & Egg Pass-1 Worklog

> **Scope:** This file is the **D&E Pass-1 track only** — mechanical Pass-1 extraction of the three *Tales of Dunk & Egg* novellas (THK / TSS / TMK), which have no Pass 1 yet. It is the **authoritative state file for D&E Pass-1 status** (a per-track re-scoping of CLAUDE.md rule #9).
>
> **Shared state lives in `worklog.md`** — the graph track, all cross-project **Active Decisions** (incl. the LOCKED Pass-1 relationship vocab), **Ideas & Backlog**, and **Principles**. A D&E session reads THIS file for its own state plus `worklog.md` for shared state; it does **not** need to load the giant graph Current State.
>
> **Numbering:** D&E sessions number **DE-1, DE-2, …** — independent of the global S-number (which is graph/meta-only). No cross-track write-order race; no `[Track:]` tag needed (this file *is* the track). The two pre-split entries below kept their original global numbers (**S131**, **S132b**) because they're referenced in the live continue prompt, commit history, and `history/worklog-archives/`. The next D&E session is **DE-1**.
>
> **Archiving:** this log does **not** rotate into `history/worklog-archives/`. It's a bounded 3-unit job; if it ever exceeds 5 Session-Log entries, spill the oldest to an `## Archived sessions` section at the foot of THIS file. When D&E Pass-1 completes, freeze the whole file into `history/`.

---

## Current State — D&E Pass-1

**Status:** **EXTRACTION COMPLETE + VERIFIED (DE-3, 2026-07-19)** — v4 promoted, full run FIRED on Matt's go ("Hit rate limit? Fire") and finished: **24/24 part-units in `extractions/mechanical/{thk,tss,tmk}/`, 10,416 extraction lines, ~$51.10, one rate-limit wall self-healed, zero crashes.** Verify pass DONE: schema validator 24/24 · THK/TSS cross-read audit **PASS clean** · TMK audit **PASS** (4 epithet-SAME_AS rows flagged for adjudication) — reports `AUDIT-{tmk,thk-tss}-full-run.md`. **Remaining: Matt's close-out** (adjudicate the 4 epithet rows · then freeze this file to `history/`) — see the close-out continue prompt.

**Unit checklist** (status ∈ not-started · smoke · extracting · done):
- [x] **THK** — 7 part-units — **done + audited PASS** (smoke also passed)
- [x] **TSS** — 8 part-units — **done + audited PASS** (smoke also passed)
- [x] **TMK** — 9 part-units — **done + audited PASS** (4 epithet-SAME_AS rows to adjudicate: p05:287/290, p06:269/271 — epithet-vs-identity call, possibly KEEP as alias capture)

**Active prompt version:** **v4 — PROMOTED, ran the full corpus.** `working/dunk-egg-pass1/prompts/pass1-prompt-v4.md`.
**Live continue prompt:** `progress/continue-prompts/2026-07-19-dunk-egg-pass1-closeout.md` (adjudicate + freeze + downstream pointers).
**Run residues (non-blocking):** (a) harvest sidecar is slash-delimited harvest-queue lines despite the `.jsonl` name — 372 rows (THK 124/TSS 115/TMK 133); THK/TSS rows may partially duplicate the 55 smoke-era rows — dedup at harvest-drain time; (b) worker wall-path lock bug FIXED in-session (wall exit now releases the lock; false "drained exit 0" now exits 10 with a warning) after it silently skipped `tss-dunk-01-p08` — recovered same night.
**Split decision:** **A (scene-split) SETTLED DE-3** — parts were built 2026-06-23 (`scripts/dunk-egg-scene-splitter.py` → 7/8/9 parts + `queue-parts.jsonl`, 24 rows); DE-3 verified lossless (delta-0 words vs originals, `unit_part` frontmatter present). Pinned via `--queue queue-parts.jsonl` in `TRACK_CMD`. Matt can veto to B at fire time (swap to `queue.jsonl`).
**Harness:** `weirwood run start dunk-egg-pass1` (READY) → generic `longrun.sh` ← worker **`scripts/dunk-egg-pass1-extraction.py`** (graduated DE-3). Run-plan: `working/dunk-egg-pass1/run-plan.md`. **Terminal trigger:** `scripts/term-launch.sh` (built DE-3) launches env-scrubbed real-terminal commands from inside a Claude Code session — authenticated `claude -p` proven (AUTH-OK probe).
**Project-wide D&E decisions** (e.g. the LOCKED Pass-1 relationship vocab, `architecture.md:687`) live in **`worklog.md` Active Decisions**, not here — so graph sessions still see them.

---

## Session Log

> Newest first. DE-N numbering. **Strict 5-entry max**, but this log **self-contains overflow** (spill the oldest to `## Archived sessions` at the foot — it does NOT archive to `history/worklog-archives/`). The S131/S132b entries are **pre-split** and kept their global numbers — see the header note. The next entry is **DE-2**.

### Session DE-3 — v4 PROMOTED + FULL RUN COMPLETE + VERIFIED: the D&E Pass-1 extraction is DONE (2026-07-18 → 07-19)
**Detail:** `history/session-details/session-de-3.md` (incident postmortem: wall-lock false-complete; env-propagation finding). **Model:** Fable 5 (orchestration); judges/auditors = Haiku subagents; worker = claude-opus-4-8. **Type:** JUDGE + PROMOTE + INFRA + EXECUTION (full run fired on Matt's explicit go). **Ledger note:** this session occupies Matt's global **S221** slot (parallel with the S220 UI-toggle session); logged here as DE-3 per the S132c track split. **Harvest-queue check at endsession:** 25 open rows — below the ~30 bar, no drain owed (the D&E harvest SIDECAR is a separate 372-row artifact, handled via the closeout/todos).
**Found on arrival:** Matt had run BOTH smokes himself via CLI on 2026-06-23 (THK ran twice — the on-disk file is from the second, longer run: 107k output tokens, $5.75; TSS single run $3.55; telemetry `exit_reason: ok`), AND the scene-split had been materialized (`dunk-egg-scene-splitter.py` → parts for all 3 novellas + `queue-parts.jsonl`, 24 rows). Neither was logged here — this entry closes that gap.
**Judging:** two fresh cold Haiku judges (checklist from the smoke continue prompt, vocab pasted) → **THK: PROMOTE-READY, 8/8 PASS** (73 relationship rows, 0 vocab violations, 5 SAME_AS reveals, 817 clean lines, no checkpoint seams) · **TSS: PROMOTE-READY, 8/8 PASS** (54/54 rows clean, Egg↔Aegon + Bloodraven↔Brynden SAME_AS, late tables full-strength). Reports: `smoke/v4/JUDGE-{thk,tss}.md`. Orchestrator spot-check: the single `(inferred)` tag is a sanctioned flag (prompt line 105), not an interpretive leak. **v4 is the winner — no v4b needed.**
**Fire-gate steps executed (run-plan §6):** (1) worker `git mv` → `scripts/dunk-egg-pass1-extraction.py` (move-safe: PROJECT_ROOT walks to CLAUDE.md; `WORK_DIR` stays `working/dunk-egg-pass1/`); (2) track registered **READY** in `weirwood-run.sh` — `TRACK_CMD` pins `--prompt-version v4 --queue queue-parts.jsonl` with absolute `$REPO_ROOT` paths (`_launch_track` doesn't cd); (3) **split A settled** — parts verified lossless (delta-0 words ×3, `unit_part` frontmatter ✓); (4) architecture.md paired doc-fix LANDED (agent principle #9 free-text fossil corrected; worklog.md S131 Active Decision updated); (5) sequencing gate satisfied (enrichment passes long since done — S133…S212).
**Bug fixed (would have sunk the full run):** `_validate_output`'s 250-line floor was calibrated on whole novellas (THK=817, TSS=715 lines) but a scene part averages ~90–117 lines → EVERY part-unit would have failed validation → crash-retry loop → longrun gives up. Floor now scales: 250 whole / 60 part (`unit_part` in queue row); headers remain the structural check.
**Infra (Matt's asks this session):** (a) "use longshell" → confirmed `longrun.sh` via the READY registry track is the run path; (b) **`scripts/term-launch.sh` BUILT + PROVEN** — triggers a real terminal from inside a Claude Code session: `open -a Terminal <snippet>` + **`env -i` + fresh zsh login shell** (critical finding: `open` PROPAGATES the session env — CLAUDECODE/OAuth/base-URL vars — into the launched app, re-creating the DE-1 401 contamination; the scrub neutralizes it). End-to-end proof: clean env (0 anthropic/claude vars) + authenticated `claude -p` **AUTH-OK** probe. `--iterm` mode exists but needs Matt's one-time macOS automation consent (TCC dialog may be pending on screen from this session's probe). Launch snippets audit-trail to `working/logs/term-launch/`.
**Cost note:** smoke spend (Matt's CLI runs) ≈ $12.40 total incl. the duplicated THK run.
**Run completed same-session (2026-07-19, Matt's go "Hit rate limit? Fire"):** fired via term-launch → longrun; 24/24 units in ~7h50m wall-clock incl. one rate-limit wall (23:10, self-healed after the 60-min sleep) — but the walled unit `tss-dunk-01-p08` was then **silently skipped on every resume and the run false-exited 0 at 23/24**: the worker's wall path returned without releasing the unit lock, and the drained check ignored pending-but-locked units. **Both bugs fixed in-session** (wall path unlinks the lock; drained check now compares the manifest and exits 10 with a warning); stale lock cleared; the missing unit re-run clean ($2.07). Totals: **$51.10, avg ~8 min/unit, 10,416 lines** (THK 3,009 vs its 817-line whole-novella smoke — split-A fidelity confirmed ~3.7×). **Verify pass (run-plan §5) DONE:** deterministic validator 24/24 (0 `NEEDS_VOCAB`, 59 `SAME_AS`); two fresh Haiku auditors — THK/TSS **PASS clean** (part-mode isolation held: Egg→Aegon only in the reveal parts), TMK **PASS** with 4 epithet-SAME_AS rows flagged (adjudication, not auto-deleted — epithets may be wanted as alias capture). Harvest sidecar grew 55→372 rows (slash-delimited format note + smoke-dup caveat in Current State).
**What's next:** Matt's close-out — adjudicate the 4 TMK epithet rows, then freeze this file to `history/` (track complete). The extractions are now the substrate for the Bloodraven enrichment dip and D&E graph-build integration. Continue prompt: `progress/continue-prompts/2026-07-19-dunk-egg-pass1-closeout.md`.

---

### Session DE-2 — Clarification: auth mechanism & smoke command ready (2026-06-23)
**Model:** Haiku 4.5. **Type:** CLARIFICATION (no changes). 
**Summary:** User asked "what API are we hitting if chapters are already local?" Clarified: the 401 is a subprocess auth issue (child `claude -p` spawned from Claude Code doesn't inherit host OAuth), not a missing-chapters problem. Confirmed smoke command is ready and provided the exact command to run from iTerm.
**What's next:** Matt runs the smoke test from a logged-in iTerm session: `python3 working/dunk-egg-pass1/dunk-egg-pass1-extraction.py --smoke --only thk --prompt-version v4`. Once `working/dunk-egg-pass1/smoke/v4/thk-dunk-01.extraction.md` is produced, fresh session judges it via `/continue 2026-06-29-dunk-egg-pass1-smoke.md` (existing continue prompt, already in place).

---

### Session DE-1 — v4 smoke: queue built, smoke blocked on nested-claude-p auth (401) (2026-06-23)
**Model:** Opus 4.8. **Type:** EXECUTION + infra finding (no extraction output produced).
**Changes made:**
- Ran `--build-queue` → `working/dunk-egg-pass1/queue.jsonl` (3 units) + created canonical empty dirs `extractions/mechanical/{thk,tss,tmk}/` (never archive — `feedback_extraction_archive_rules`).
- Pre-flight (read-only) verified the worker scaffold: `--build-queue/--smoke/--only/--prompt-version` wired; v4 prompt has the `═`×79 body delimiters + all 4 path placeholders; THK source present (~31,669 words); `claude` on PATH; `pace.py` importable.
- Fired the THK v4 smoke (`--smoke --only thk --prompt-version v4`) with Matt's explicit go → **crashed in 4.7s on `401 Invalid authentication credentials`**, 0 output tokens, no file written (smoke/v4/ empty; canonical tree untouched). Worker classified it correctly (crash, not wall/invalid). Telemetry crash row → `working/telemetry/dunk-egg-pass1.jsonl`.
**Finding (durable):** a nested `claude -p` spawned from inside a Claude Code session **cannot authenticate** — this session's host-managed OAuth (gateway `ANTHROPIC_BASE_URL`) is not inherited by a child process; 401 reproduced WITH and WITHOUT scrubbing the base-URL. This is the concrete mechanism behind `feedback_no_extraction_without_asking` (memory updated with the WHY). The canonical `claude -p` smoke must launch from a logged-in interactive CLI/iTerm. Offered an in-session Agent-tool subagent proxy as the alternative; **Matt chose to run it himself via the `claude` CLI.** Queue is pre-built, so his command is just `python3 working/dunk-egg-pass1/dunk-egg-pass1-extraction.py --smoke --only thk --prompt-version v4`.
**What's next (DE-2):** See DE-2 entry above (clarification session, then smoke runs from iTerm). Judge `smoke/v4/thk-dunk-01.extraction.md` after it's produced (DE-3? or wrapped into DE-2 judge? → use `/continue 2026-06-29-dunk-egg-pass1-smoke.md`).

---

### Session 132b — D&E v4 prompt fix: removed Bloodraven pre-flagging from harvest — [Track: D&E] (2026-06-22)
**Model:** Haiku 4.5 (lightweight fix). **Type:** REFINEMENT + HANDOFF (no extraction launched).

**Issue identified + fixed:** v4 prompt had pre-flagged "Bloodraven / Brynden Rivers" as a special harvest category, which primed the model to watch for him during mechanical extraction. This violates chapter isolation: the extraction should run CLEAN and UNBIASED; Bloodraven enrichment happens afterward as a separate dip.

**Changes made:**
- **`prompts/pass1-prompt-v4.md`** — Removed Bloodraven from the harvest sidecar (line 147–150). Harvest now generic: Targaryen history, prophecy seeds, food, hospitality, cross-identity reveals. No entity pre-flagging. Updated line 36 ("Why v4 exists") and change-log entry #2.
- **`run-plan.md`** — Updated harvest section (line 119–120) to say "generic saga-important breadcrumbs" not "aimed at Bloodraven substrate". Updated validator section (line 255) to check for generic breadcrumbs, not Bloodraven-specific. Removed Bloodraven mentions from the change-log context.
- **`worklog.md`** — Updated D&E Pass 1 line (line 86) to note: "Extraction runs CLEAN mechanical (unbiased); Bloodraven enrichment dip runs AFTER as a separate pass."

**Deferred:** 5-hour session timeout issue with `longrun.sh` wall-sleep (affects reusability of the worker template). Created `working/longrun-orchestrator-improvements.md` as a handoff document for the next session. This is infrastructure work that blocks future projects but not D&E (only 3 units, <2 hours end-to-end). Design + implementation deferred to dedicated session N+1.

**What's next:** D&E smoke-test v4 on THK. Continue prompt: `progress/continue-prompts/2026-06-29-dunk-egg-pass1-smoke.md` (already in place). Recommend: fresh Opus 4.8 session for the smoke judge + winner selection.

> **S132c follow-up (meta, in `worklog.md`):** a fresh-eyes audit graded the S132b de-bias **A** (complete — no model-visible priming survives) and **scrubbed a residual "Bloodraven/Targaryen" line from the smoke judge checklist** that would have re-leaked the bias into a v4b. Full audit + the longrun-doc fixes are in `worklog.md` S132c.

---

### Session 131 — Dunk & Egg Pass-1: unattended harness design + v4 prompt hardening — [Track: D&E] (2026-06-22)
**Detail:** `history/session-details/session-131.md`. **Model:** Opus 4.8. **Type:** DESIGN (HANDOFF B, parallel-safe with the remainders track). **Launched nothing** — extraction stays gated (`feedback_no_extraction_without_asking`).

Designed + scaffolded the unattended D&E Pass-1 harness and **substantially hardened the v3 prompt → v4**. All deliverables under `working/dunk-egg-pass1/`.
**Changes made:**
- `run-plan.md` — harness contract (generic `longrun.sh` ← `weirwood run` registry ← D&E worker payload), worker config, chapter-split decision (RECOMMEND A=split ~6–9 scene-parts; novellas are markerless continuous prose ~8× a book chapter), versioning + smoke §3.5, run/monitor/resume, ready-to-fire §6.
- `dunk-egg-pass1-extraction.py` — worker SCAFFOLD: proven `claude -p` loop from `extract.sh:494–578` (cwd=/tmp; stream-json; positive-only wall→exit 2); `--prompt-version` + `--smoke` (smoke→`smoke/<ver>/`, never canonical); per-version manifest/locks; `--build-queue` makes `extractions/mechanical/{thk,tss,tmk}/`. Runs from `working/`; compiles; inert on bare run.
- `prompts/pass1-prompt-v4.md` — hardened prompt (appendix change-table rows 1–15).
**Decisions:** (1) **LOCKED relationship vocab in Pass 1** — the Relationship column is now a forced controlled UPPER_CASE type from a curated character-to-character subset, NOT free text. This **realigns to `architecture.md:687`** (already names the Pass-1 extractor a vocab emitter) and **supersedes the stale `:161` free-text note** (predates the vocab) — a rule-#6 paired doc-fix is owed when v4 ships (logged as Active Decision in `worklog.md`). Guardrails: `NEEDS_VOCAB:` gap-hatch (`:159` "edge types cheaper than lost info"), `KNOWS` ban (deprecated S63), analytical-type ban (`FORESHADOWS`/`PARALLELS` would re-open isolation). (2) Other fold-ins, discriminated not dumped: forward-direction-only inverse rule (pruned 3 reverse types — *shrank* the prompt); deepened optional-qualifier capture (8 enums embedded); Events sub-bullets→reification roles (added Witness→WITNESS_IN); **`causal-spine` harvest breadcrumb** (point for the arc-mint pass, NOT inline `CAUSES`). **Excluded on purpose:** causal-edge emission, convergence-points, narrative-arcs (graph-layer, invisible under isolation). (3) Evidence-driven: real-extraction audit found isolation already clean (no extra rules) but interpretive-qualifier leak (`symbolic`/`ironic`/`(implicit)`) is the #1 rule-9 defect → banned-word list + "bare names only" on the Raw Entity List. Table structure stays byte-frozen (no downstream parser break). Names de-abbreviated (`de-pass1`→`dunk-egg-pass1`; `thk/tss/tmk` kept = canonical book codes). Versioning added for smoke-testing variants.
**What's next:** smoke-test v4 on THK → fresh-judge → promote or iterate to v4b → then full-run prereqs. Continue prompt: `progress/continue-prompts/2026-06-29-dunk-egg-pass1-smoke.md` (Dunk & Egg track, parallel-safe). (**Opus 4.8** for the smoke-judge session.)
