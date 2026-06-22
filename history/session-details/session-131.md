# Session 131 — Dunk & Egg Pass-1: unattended harness design + v4 prompt hardening

**Date:** 2026-06-22
**Model:** Opus 4.8
**Type:** Design / planning (HANDOFF B, parallel-safe with the low-value-remainders track). **Launched nothing.**
**Track:** Dunk & Egg Pass-1 (THK/TSS/TMK mechanical extraction)

---

## Purpose

Two goals from the handoff: (1) plan running the Dunk & Egg full-Opus Pass-1 batch **unattended**, to
get D&E off the critical path *and* exercise the post-Fable-audit unified-script harness; (2) **harden
the v3 extraction prompt** before any run — Matt's explicit ask ("we can def make those prompts better…
drop pointers like the harvester… learn from the mistakes of the initial book opus passes. as these are
short stories we have considerably more room").

Output: a run-plan + worker scaffold + a substantially-rewritten v4 prompt, all under
`working/dunk-egg-pass1/`. Nothing fired — extraction stays gated on Matt's explicit go
(`feedback_no_extraction_without_asking`).

## The harness (the easy part — the reorg paid off)

`longrun.sh` is the **generic** supervisor: it relaunches any argv on the exit-code contract
(0=done/2=wall/10=more/crash) and knows nothing D&E-specific. `weirwood run` (`weirwood-run.sh`) is the
declarative track registry over it — log + latest-symlink + pidfile + start/logs/status/stop by name.
So a new pass = **write one worker + add one registry line.** The worker is the D&E-specific payload;
the supervisor is written once.

`worker-template.py` ships with a fake `_do_real_work()`. The scaffold
(`dunk-egg-pass1-extraction.py`) replaces it with the **proven** `claude -p` call lifted from
`extract.sh:494–578` (stream-json, token parse from the `type:result` event, the real
`"status":"rejected"`+`"rateLimitType"` wall-detect → exit 2 on a *positive* signal only). Subprocess
runs **cwd=/tmp** (~49% cheaper — skips CLAUDE.md; `reference_llm_pass_via_claude_p`), so all prompt
paths are absolute. Per-version manifest/locks; output validated (≥250 lines + 4 anchor headers + 12
Raw-List headers) before `done`.

## Chapter-split decision (flagged, not decided)

The 3 novellas are **continuous prose, no scene-break markers** — `chapter-splitter.py` can't touch
them. Each is ~32–37K words, ~8× a book chapter; a whole-novella single generation would be ~2K lines,
squarely in the "late tables get skimped" failure zone. Recommended **A (split into ~6–9 scene-sized
parts via a one-time scene-boundary step)** for fidelity + cite granularity; **B (whole-novella)** is the
simpler "ship it" path and v4's section-checkpointing makes it as safe as it can be. Left as a fire-gate
fork for Matt.

## Naming + versioning (Matt-driven iterations)

Matt: "enough with the abbreviations." Renamed `de-pass1*` → `dunk-egg-pass1*` throughout (kept
`thk/tss/tmk` — those are canonical book codes, not abbreviations). Confirmed the run is launched by the
**named** `weirwood run start dunk-egg-pass1` (flagless; the winning prompt version is pinned in
`TRACK_CMD`) — Matt won't type flags.

Matt then flagged that we'll smoke-test multiple prompt variants → added **prompt versioning**: prompts
live in `prompts/pass1-prompt-<version>.md`; the worker takes `--prompt-version` + a `--smoke` mode that
routes output to `smoke/<version>/` (never the canonical tree or another variant), with per-version
manifest/locks and `prompt_version` stamped into telemetry. Smoke → diff → promote-winner workflow
documented in run-plan §3.5.

## Prompt hardening — the substance (rows 1–15 of the v4 appendix)

### First pass (rule-archaeology + memory)
Self-contained every rule (no CLAUDE.md in a /tmp run); baked in the **harvest + capture-quote**
pointers aimed at the **Bloodraven** evidence substrate; added the **in-text identity-reveal → `SAME_AS`**
rule (Egg→Aegon, the old man→Ser Arlan); a "more room" block (section-checkpointing + final self-audit
vs the long-generation skimp); front-loaded the reactively-patched v3 rules; frontmatter-driven
`first_available` (no inference).

### Evidence-driven pass (audited the actual 5-book extractions)
- **Isolation audited clean** — the strict leakage scan came back essentially empty; nearly all
  "reader learns X" hits are the legitimate "Known To (Reader Only?)" column. So **no extra isolation
  rules added** (would've been wasted strictness).
- **Qualifier-leak is the #1 recurring rule-9 defect** — `symbolic`/`ironic`/`(implicit)`/`representing`
  slip into cells and the Raw Entity List (`blood oranges (pervasive symbolic object)`, Iron Throne
  "symbolic center of power struggle"). Added a concrete banned-word list + "bare names only" on the
  Raw Entity List.

### The big one — LOCKED relationship vocabulary (Matt pushed; the audit proved him right)
I initially deferred to `architecture.md:161` ("Pass 1 records relationships in free-text"). Matt
challenged it as stale, and correctly: that line predates the controlled vocab (written when v1 produced
"~127 ad-hoc labels"), and **`architecture.md:687` — maintained through S116 — already names the
"Pass-1 mechanical extractor" a vocab emitter.** The doc contradicts itself; §161 is the fossil. So
forcing the vocab *realigns* to §687, it doesn't invent a new policy. Matt also noted (empirically true)
that models follow a hard closed-set far better than soft "prefer these."

Implemented: the Relationship column is **forced to one controlled UPPER_CASE type** from a **curated
character-to-character subset** (kinship/authority/factional/conflict/knowledge/emotional/identity/magic).
Critical curation: did NOT force from all ~168 types — excluded spatial/possession/event-role (belong in
other tables) and especially the **analytical** types (`FORESHADOWS`/`PARALLELS`) whose use would re-open
the isolation hole. Guardrails: `NEEDS_VOCAB: <desc>` gap-hatch (honors `:159` "edge types cheaper than
lost info" → feeds the vocab-gap tooling instead of inventing pseudo-labels); `KNOWS` banned (deprecated
S63). Recorded as an **Active Decision** with a paired doc-fix: correct stale `:161` when v4 ships.

### Further fold-ins (Matt: "there's a lot we've learned… but I don't want to overload it")
Discriminated rather than dumped:
- **Inverse edges → yes, and it SHRANK the prompt.** Right lesson = "emit the forward/agent direction
  only; the graph derives reverses by traversal." Pruned 3 reverse types (`NEPHEW_OF`/`STEP_CHILD_OF`/
  `WET_NURSE_OF`), added a forward-only rule tied to the Head rule, prevents double-emission.
- **Causal edges → NO graph emission, YES a pointer.** Causal typing is the heart of the arc machine
  *because* it needs fresh-verify + L1/L2 + agency-collapse checks; asserting `CAUSES` inline would
  manufacture the exact unverified junk that machine exists to prevent. But a single novella is
  self-contained, so its within-unit causal spine is real → added a **`causal-spine` harvest
  breadcrumb** (point for the later arc-mint pass, don't type/assert).
- **Convergence points / narrative arcs → EXCLUDED.** Graph-layer, multi-event, often cross-book;
  invisible under chapter-isolation; the arc machine owns them post-hoc. "Small novellas" buys
  thoroughness + a verify pass, not a license to do graph reasoning in a mechanical pass.
- **Events sub-bullets aligned to reification roles** (Agent→AGENT_IN … added **Witness**→WITNESS_IN,
  the S117 role) so Stage 4 reifies straight from them.
- **Qualifier capture deepened** — embedded the 8 optional-qualifier enums with active-capture
  instructions (`KILLS (by_ambush)`, `DECEIVES (by_disguise)`, `REVEALS_TO (under_torture)`,
  `LOVER_OF (paramour)` …); high D&E mystery-signal, text-evident, cheap given "more room".

Net: a ~360-line prompt body that folds three years of post-pass learning in, with the **table
structure still byte-frozen** (no downstream parser break). The single paired change is the §161
doc-fix.

## Why a new session for the smoke

Recommended the smoke test runs in a **fresh** session, not this one: (1) this is the design handoff
("launches nothing") — bolting a live `claude -p` extraction on violates `feedback_session_purpose_discipline`;
(2) the fresh `extraction-quality-auditor` judge should read THK's output cold, not soaked in the
rationale for every prompt choice; (3) the deliverables are self-documenting so handoff is cheap. Wrote
the smoke continue-prompt (`2026-06-29-dunk-egg-pass1-smoke.md`), tagged as the Dunk & Egg track,
parallel-safe, no hardcoded session number.

## Open for Matt (the fire-gate)
v4 sign-off (or smoke→iterate to v4b) · split A vs B · then graduate worker to `scripts/` + register the
track + correct `architecture.md:161` + `--build-queue` + confirm sequencing (worklog: D&E runs after
the first enrichment passes). All in run-plan §6.
