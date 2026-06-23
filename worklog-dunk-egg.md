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

**Status:** harness + **v4 prompt** DESIGNED (S131); de-bias audited (S132c). **Queue BUILT (DE-1)**; v4/THK smoke **attempted DE-1 but blocked by a nested-`claude -p` auth wall (401)** — it runs from a logged-in CLI/iTerm only, NOT from inside a Claude Code session. Matt is running the smoke himself via the `claude` CLI. Still gated — **confirm before any extraction incl. smoke** (`feedback_no_extraction_without_asking`).

**Unit checklist** (status ∈ not-started · smoke · extracting · done):
- [ ] **THK** — `sources/chapters/thk/thk-dunk-01.md` (31,669 words) — **smoke-attempted DE-1 (auth-blocked, 0 output); re-run via logged-in CLI, then judge**
- [ ] **TSS** — `sources/chapters/tss/tss-dunk-01.md` (36,677 words) — not-started
- [ ] **TMK** — `sources/chapters/tmk/tmk-dunk-01.md` (36,808 words) — not-started

**Active prompt version:** v4 — `working/dunk-egg-pass1/prompts/pass1-prompt-v4.md` (self-contained rules, generic harvest with NO entity pre-flagging, LOCKED relationship vocab + `NEEDS_VOCAB` hatch, in-text identity→`SAME_AS`, "more room" checkpointing).
**Live continue prompt:** `progress/continue-prompts/2026-06-29-dunk-egg-pass1-smoke.md` (judge on Opus 4.8; the extraction itself runs Opus regardless — worker hardcodes `claude-opus-4-8`).
**Open decision:** chapter-split **A** (scene-split ~6–9 parts, RECOMMENDED S131) vs **B** (whole-novella). Settle at full-run prereqs.
**Harness:** `weirwood run start dunk-egg-pass1` → generic `longrun.sh` ← worker `working/dunk-egg-pass1/dunk-egg-pass1-extraction.py`. Run-plan: `working/dunk-egg-pass1/run-plan.md`.
**Project-wide D&E decisions** (e.g. the LOCKED Pass-1 relationship vocab, `architecture.md:687`) live in **`worklog.md` Active Decisions**, not here — so graph sessions still see them.

---

## Session Log

> Newest first. DE-N numbering. **Strict 5-entry max**, but this log **self-contains overflow** (spill the oldest to `## Archived sessions` at the foot — it does NOT archive to `history/worklog-archives/`). The S131/S132b entries are **pre-split** and kept their global numbers — see the header note. The next entry is **DE-2**.

### Session DE-1 — v4 smoke: queue built, smoke blocked on nested-claude-p auth (401) (2026-06-23)
**Model:** Opus 4.8. **Type:** EXECUTION + infra finding (no extraction output produced).
**Changes made:**
- Ran `--build-queue` → `working/dunk-egg-pass1/queue.jsonl` (3 units) + created canonical empty dirs `extractions/mechanical/{thk,tss,tmk}/` (never archive — `feedback_extraction_archive_rules`).
- Pre-flight (read-only) verified the worker scaffold: `--build-queue/--smoke/--only/--prompt-version` wired; v4 prompt has the `═`×79 body delimiters + all 4 path placeholders; THK source present (~31,669 words); `claude` on PATH; `pace.py` importable.
- Fired the THK v4 smoke (`--smoke --only thk --prompt-version v4`) with Matt's explicit go → **crashed in 4.7s on `401 Invalid authentication credentials`**, 0 output tokens, no file written (smoke/v4/ empty; canonical tree untouched). Worker classified it correctly (crash, not wall/invalid). Telemetry crash row → `working/telemetry/dunk-egg-pass1.jsonl`.
**Finding (durable):** a nested `claude -p` spawned from inside a Claude Code session **cannot authenticate** — this session's host-managed OAuth (gateway `ANTHROPIC_BASE_URL`) is not inherited by a child process; 401 reproduced WITH and WITHOUT scrubbing the base-URL. This is the concrete mechanism behind `feedback_no_extraction_without_asking` (memory updated with the WHY). The canonical `claude -p` smoke must launch from a logged-in interactive CLI/iTerm. Offered an in-session Agent-tool subagent proxy as the alternative; **Matt chose to run it himself via the `claude` CLI.** Queue is pre-built, so his command is just `python3 working/dunk-egg-pass1/dunk-egg-pass1-extraction.py --smoke --only thk --prompt-version v4`.
**What's next (DE-2):** judge `smoke/v4/thk-dunk-01.extraction.md` cold with a fresh `extraction-quality-auditor` (Haiku ok; paste the vocab line — subagents don't load CLAUDE.md) — locked vocab held? qualifiers? forward-only? isolation? no interpretive-qualifier leak? identity→`SAME_AS`? harvest sidecar? no skimped late tables? → SUMMARY → decide **promote v4** or **iterate v4b**. Continue prompt: `progress/continue-prompts/2026-06-29-dunk-egg-pass1-smoke.md`.

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
