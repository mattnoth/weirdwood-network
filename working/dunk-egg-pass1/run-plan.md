# Dunk & Egg Pass-1 — Unattended Run Plan (DESIGN; launches nothing)

> **Session:** S131/132 (stamp at endsession per worklog). **Model for the run:** Opus 4.8 (all Pass 1
> was Opus — `project_pass1_all_opus`; D&E is the substrate for theory-heavy Bloodraven work, so it gets
> the strongest model). **This doc launches NOTHING** — run-plan + scaffold + hardened prompt, gated on
> Matt's explicit go-ahead (`feedback_no_extraction_without_asking`).
>
> **Deliverables (all under `working/dunk-egg-pass1/`):**
> - `run-plan.md` (this file)
> - `prompts/pass1-prompt-v4.md` — the hardened v4 extraction prompt (the prompt-improvement prereq).
>   **Versioned** — smoke variants are sibling files `prompts/pass1-prompt-v4b.md`, `…-v4c.md`, … (see §3.5)
> - `dunk-egg-pass1-extraction.py` — the worker **scaffold** (proven `claude -p` loop wired in;
>   `--prompt-version` + `--smoke` aware; NOT production-placed, NOT run)

---

## 0. The shape, in one picture

```
weirwood run start dunk-egg-pass1                         ← what Matt types (named, aliased)
        │  (scripts/weirwood-run.sh: log + symlink + pidfile, then…)
        ▼
bash scripts/longrun.sh  python3 scripts/dunk-egg-pass1-extraction.py --resume
     └─ GENERIC supervisor ┘ └─ Dunk & Egg-specific payload (the worker) ────┘
        (0/2/10/crash contract)   (queue · prompt · claude -p · validate · telemetry)
```

The reorg's whole dividend: **a new pass = write one worker + add one registry line.** The supervisor
is written once and never touched again.

---

## 1. Harness contract — how a pass gets "passed into" the unattended harness

There are **two** extraction harnesses. The unattended run uses the **new** one.

| | `extract.sh` (OLD, the 5 books) | `weirwood run` → `longrun.sh` → worker (NEW, S97–99) |
|--|--|--|
| Attendance | Interactive iTerm tabs (osascript) | **Unattended**, backgrounded, survives walls/crashes |
| Unit | wave of 5 chapters | whatever the worker's queue defines |
| Resume | CSV claim-rows + soft-stop file | manifest `done[]` + `O_CREAT\|O_EXCL` lock files |
| Rate-limit | halts the wave, writes `retry_at` | worker **exit(2)** → supervisor sleeps `LONGRUN_WALL_SLEEP`, relaunches |
| `claude -p` call | **proven, `extract.sh:494–578`** | placeholder in template — **we ported the proven call in** |
| cwd | repo root (loads CLAUDE.md) | **`/tmp`** for the subprocess (~49% cheaper; `reference_llm_pass_via_claude_p`) |
| Launch | `weirwood agot 2 3` | `weirwood run start <track>` |

**Contract `longrun.sh` enforces (the only thing the worker must honor):** exit `0`=done · `2`=wall
(supervisor sleeps `LONGRUN_WALL_SLEEP`=3600s) · `10`=more-remains (sleeps `LONGRUN_SLEEP_BETWEEN`=1200s) ·
other=crash (sleeps 300s, gives up after `LONGRUN_MAX_CRASHES`=5).

`longrun.sh` is **generic** — it relaunches the same argv on the contract; there is **nothing
D&E-specific in it.** All specificity is in the worker we hand it.

### The aliasing — `weirwood run` registry (this is what makes it a named track)
`scripts/weirwood-run.sh` is a declarative track registry over `longrun.sh`: each track gets a
timestamped log, a `*-latest.log` symlink, and a pidfile under `working/logs/longrun/`. Two ways to run:
- `weirwood run start custom -- <cmd…>` — escape hatch, any command (works today, unregistered).
- `weirwood run start <track>` — a **registered READY track** (the clean way). Add this entry to the
  registry's track table (the worker must be graduated to `scripts/` first):

  ```bash
  TRACK_NAMES+=("dunk-egg-pass1")
  TRACK_STATUS+=("READY")
  TRACK_DESC+=("Dunk & Egg Pass-1 full extraction (THK/TSS/TMK) — scripts/dunk-egg-pass1-extraction.py")
  TRACK_CMD+=("python3 scripts/dunk-egg-pass1-extraction.py --resume --prompt-version v4")
  ```
  (Pin the **winning** prompt version in `TRACK_CMD` once smoke-testing picks it — §3.5.)

  Then: `weirwood run start dunk-egg-pass1` · `… logs dunk-egg-pass1` · `… status …` · `… stop …`.
  Logs auto-land at `working/logs/longrun/dunk-egg-pass1-latest.log`.

> **Why not register it now?** A `READY` track pointing at a script that doesn't exist yet (the worker
> is still a scaffold in `working/`) would fail on launch. So the registry edit is bundled with the
> "graduate the worker to `scripts/`" step at the fire-gate (section 6). Until then, `weirwood run start
> custom -- python3 working/dunk-egg-pass1/dunk-egg-pass1-extraction.py --resume` would work for a smoke
> test, but we don't smoke-test live extraction without Matt's go.

### Gaps that blocked an unattended run (all closed in the scaffold)
1. Template did fake work → replaced `_do_real_work()` with the `extract.sh` `claude -p` call.
2. Template wall-detection was simulated → ported the real grep (`"status":"rejected"` +
   `"rateLimitType"`); exit(2) ONLY on that positive signal, else crash (ambiguous failure must not burn
   a wall-sleep).
3. No queue → `--build-queue` builds it + creates `extractions/mechanical/{thk,tss,tmk}/` (canonical,
   never archive — `feedback_extraction_archive_rules`).
4. Telemetry track is `dunk-egg-pass1` (new ledger, no collision).

---

## 2. The worker (scaffolded in `dunk-egg-pass1-extraction.py`, not run)

- **TRACK / telemetry / weirwood name** = `dunk-egg-pass1`.
- **Queue** `working/dunk-egg-pass1/queue.jsonl`, one row/unit:
  `{"unit_id":"thk","book":"THK","source":"<abs>/sources/chapters/thk/thk-dunk-01.md","out":"<abs>/extractions/mechanical/thk/thk-dunk-01.extraction.md"}`
- **Manifest** `working/dunk-egg-pass1/manifest-<version>.json` (`done[]`, per prompt version so a v4
  full run and a later v4b full run never cross-mark each other). **Locks** `…/locks-<version>/<unit>.lock`.
- **`_do_real_work(unit)`** runs, subprocess **cwd=/tmp**:
  `claude -p --dangerously-skip-permissions --model claude-opus-4-8 --verbose --output-format stream-json "<v4 prompt, absolute paths filled>"`
  → stream to `working/dunk-egg-pass1/logs/<unit>.json`; usage parsed from the `type:result` event
  (exactly `extract.sh:536–556`).
- **Per-unit validation** before `done`: file exists, ≥250 lines, the 4 anchor headers
  (`## Characters/Events/Locations/Relationships`) + all 12 Raw-Entity-List headers present. Fail =
  crash (retry), not done.
- **Chunk size 1** — one novella/iteration → exit 10 → supervisor sleeps → next. Long units, lose ≤1 on
  crash, each `claude -p` call bounded.
- **`thk/tss/tmk` are canonical book codes** (collection frontmatter + chapter dirs use them) — kept
  as-is; not abbreviations to expand.

### Cost / time (order-of-magnitude — NOT a budget gate)
A ~4K-word AGOT chapter → ~300-line extraction. A D&E unit is ~32–37K words (~8×). Whole-novella:
~1.5–2.5K output lines, ~20–35 min wall-clock per novella on Opus, 3 total. Small. The constraint we
optimize is **completeness**, not spend ("we have considerably more room" — Matt).

---

## 3. Prompt-improvement prereq — DONE (draft) this session

Drafted: `working/dunk-egg-pass1/prompts/pass1-prompt-v4.md`. Headlines (full change table in its appendix):
- **Self-contains every rule** (`claude -p` in /tmp loads no CLAUDE.md/architecture).
- **Harvest + capture-quote pointers baked in** ("drop pointers like the harvester") — generic
  saga-important breadcrumbs for downstream harvest passes (`feedback_harvest_queue`).
- **In-text identity-reveal → `SAME_AS`** (Egg→Aegon, the old man→Ser Arlan) — D&E's engine.
- **"More room"**: section-checkpointing + a final self-audit to beat the long-generation
  skimped-late-tables failure.
- **Evidence-driven (real-extraction audit):** banned the interpretive-qualifier leak
  (`symbolic`/`ironic`/`foreshadows`/`(implicit)`) — the #1 recurring rule-9 defect; isolation audited
  clean, so no extra isolation rules.
- **LOCKED relationship vocabulary (the big one — Matt S131):** Relationship column is now a forced
  controlled type from the curated character-to-character edge set (free text → pseudo-labels like
  `implicit_hostility` banned), with a `NEEDS_VOCAB:` gap-hatch, required-qualifier capture, `KNOWS`/
  analytical-type bans, and Events sub-bullets aligned to the reification roles (AGENT_IN…WITNESS_IN).
  Folds in the whole post-pass infrastructure (controlled vocab + normalizers + vocab-gap tooling).
- **Table structure still byte-frozen vs v3** (no downstream parser break) — but the vocab-lock is a
  **rule-#6 paired change**: it realigns to `architecture.md:687` (already names Pass-1 a vocab emitter)
  and **supersedes the stale `:161` free-text note**, which must be corrected when v4 ships (see §6 +
  the Active Decision below).

**This is the gate.** Nothing launches until Matt signs off on a version.

> **ACTIVE DECISION (record in worklog at endsession):** *Pass-1 relationships now emit the controlled
> edge vocabulary (curated character-to-character subset) rather than free text.* Rationale: the
> controlled vocab + normalizers + vocab-gap tooling all postdate `architecture.md:161`; `:687` already
> declares Pass-1 a vocab emitter; hard closed-set > soft "prefer" for model compliance (Matt). Paired
> doc fix: correct/withdraw the stale `:161` free-text sentence. Guardrail: `NEEDS_VOCAB:` hatch so
> forcing never drops a real relation (`:159` "edge types cheaper than lost information").

---

## 3.5 Prompt versions & smoke-testing

We won't commit the full batch to a single guess — we **smoke-test a few prompt variants on one unit,
diff the outputs, then promote a winner.** The worker is built for this.

**Layout.** Each version is one file; the version id IS the filename suffix:
```
working/dunk-egg-pass1/prompts/
  pass1-prompt-v4.md     ← the current draft (the baseline)
  pass1-prompt-v4b.md    ← a variant (copy v4, tweak one axis, bump the suffix)
  pass1-prompt-v4c.md    ← another variant
```
Make a variant by copying the baseline and changing **one thing** (so the diff is attributable) — e.g.
v4b = more aggressive harvest pointers, v4c = a worked identity-reveal example. Each file's header
carries a `Version:` line for humans; the filename is authoritative for the worker.

**Smoke (attended, one unit, no supervisor, no canonical writes).** Output routes to a scratch dir
keyed by version, so variants never clobber the canonical tree **or each other**:
```
python3 dunk-egg-pass1-extraction.py --smoke --only thk --prompt-version v4
python3 dunk-egg-pass1-extraction.py --smoke --only thk --prompt-version v4b
# →  smoke/v4/thk-dunk-01.extraction.md   vs   smoke/v4b/thk-dunk-01.extraction.md
diff smoke/v4/thk-dunk-01.extraction.md smoke/v4b/thk-dunk-01.extraction.md
```
Pick THK (or, under split-option A, one scene-part) as the fixed smoke unit so every version is judged
on identical input. Each smoke run stamps `prompt_version` + `mode=smoke` into the `dunk-egg-pass1`
telemetry ledger, so cost/length per version is logged.

**Judge on:** section completeness (no skimped late tables — count rows per section), Head-rule
correctness in `## Relationships Observed`, identity-reveal capture, isolation (no cross-unit leakage),
and harvest-sidecar yield. A fresh `extraction-quality-auditor` subagent can diff two version outputs
and report which is better and why (summary, not an edge-list — `feedback_subagent_verify_not_matt`).

**Promote.** The winning version is **pinned in the weirwood track command** (`--prompt-version <winner>`,
§1) and recorded in the worklog. Losing variants stay in `prompts/` as smoke history (not deleted — they
document why the winner won). Smoke outputs under `smoke/` are scratch; clear them when done.

> Smoke runs call `claude -p` too → they are **also gated** on Matt's go (`feedback_no_extraction_without_asking`).
> The scaffold stays inert until then.

---

## 4. Chapter-split decision — RECOMMENDATION + the fork for Matt

**Finding:** the 3 novellas are **single continuous-prose files with NO scene-break markers** (no
`* * *`, no headers) — only YAML frontmatter divides them. Each is ~32–37K words, ~8× a book chapter.
`scripts/chapter-splitter.py` keys on book-style markers D&E lacks → **cannot split them as-is.**

**Recommendation: SPLIT each novella into ~6–9 scene-sized parts.** Why: the biggest documented Pass-1
failure mode is **long generations skimping late tables** (a ~2K-line single extraction sits squarely
there); book-chapter-scale units (~4–5K words) are what the prompt/schema are tuned for; **cite
granularity is high-value** (`feedback_book_citation_overlay_value`) for the Bloodraven overlay; the
budget absorbs the extra units.

**Split method (no markers exist):** a one-time **scene-boundary step** — one cheap pass (Opus, or Matt
eyeballing) emits paragraph-boundary line numbers at narrative seams; a tiny splitter writes
`thk-dunk-01.md … thk-dunk-0N.md` with inherited frontmatter + `unit_part: "k of N"`. Splits only at
paragraph boundaries → scenes stay intact. This is its own small prereq step, gated like the rest.

**The fork (Matt decides at the fire-gate):**
- **A — Split (recommended):** higher fidelity + cite granularity; costs the one-time scene-boundary
  step; queue has ~18–27 part-units.
- **B — Whole-novella:** simplest; 3 units; matches the existing `chapter_number: 1` frontmatter; relies
  on v4's "section-checkpoint + self-audit" to hold fidelity over the long generation.

> I lean **A**; **B** is a legit "ship it simply" choice and v4 is written to make B as safe as
> possible (`unit_part: "whole"`). No scene-boundary work happens until Matt picks.

---

## 5. Run / monitor / resume

**Launch (after Matt's go + v4 sign-off + split decision + worker graduated/registered):**
```
# one-time setup
python3 scripts/dunk-egg-pass1-extraction.py --build-queue     # dirs + queue.jsonl

# (optional) smoke a few prompt versions on THK first, pick a winner — see §3.5
#   python3 scripts/dunk-egg-pass1-extraction.py --smoke --only thk --prompt-version v4
#   python3 scripts/dunk-egg-pass1-extraction.py --smoke --only thk --prompt-version v4b

# launch the named track (backgrounded, supervised, logged, pidfiled)
# the registry's TRACK_CMD pins the winning --prompt-version
LONGRUN_SLEEP_BETWEEN=600 weirwood run start dunk-egg-pass1

# monitor / control
weirwood run logs   dunk-egg-pass1     # tail
weirwood run status dunk-egg-pass1     # alive? last 10 lines?
weirwood run stop   dunk-egg-pass1     # graceful SIGTERM
```
- `LONGRUN_SLEEP_BETWEEN=600` (10 min) is plenty — only 3–27 units; we are not pacing 344 chapters. Wall
  sleep stays at the 3600s default (`project_stage4_sleep_defaults`).
- **Logs/telemetry:** `working/logs/longrun/dunk-egg-pass1-latest.log` (supervisor) +
  `working/dunk-egg-pass1/logs/<unit>.json` (per-unit stream) + the `dunk-egg-pass1` telemetry ledger.

**Wall survival / resume:** worker exits 2 on a *positive* wall → supervisor sleeps → relaunches →
worker reads `manifest-<version>.json`, skips `done[]`, re-claims the rest. Idempotent; safe to stop/restart.
`longrun.sh` IS the generic run-forever supervisor — the legacy `stage4-run-forever.sh` wrapper is not
needed.

**Verify output (drift-detection mandatory even at 3 units — `feedback_drift_detection_mandatory`):**
1. **Schema validator** — reuse the worker's `_validate_output` logic standalone for the record.
2. **Cross-read audit** — one fresh `extraction-quality-auditor` subagent (Haiku ok) checks isolation
   leakage, meta-commentary in cells, Head-rule violations, and that every in-text identity reveal
   became a `same_as`. Summary to Matt, not an edge-list (`feedback_subagent_verify_not_matt`). PASTE
   the vocab line into its prompt (Pass/Track/step/Tier — subagents don't load CLAUDE.md).
3. **Harvest sidecar review** — confirm `working/dunk-egg-pass1/harvest-dunk-egg.jsonl` accumulated
   generic saga-important breadcrumbs (Targaryen history, prophecy seeds, etc. for later harvest passes).

**On success:** worker exits 0; update worklog + the "Pass 1 on Tales of Dunk and Egg" checklist line;
the new extractions are now structured nodes for the Bloodraven enrichment unit (until now D&E links came
only via book-cite overlay).

---

## 6. STOP — ready-to-fire checklist (Matt confirms each; nothing launches until then)

- [ ] **Prompt approved** (`prompts/pass1-prompt-v4.md`, + any variants) — the prereq gate. ← primary review
- [ ] **Smoke-test versions** on the fixed unit (THK), diff, **pick a winner**; pin it in `TRACK_CMD`
      (`--prompt-version <winner>`) and record in worklog (§3.5).
- [ ] **Split decision:** A (split, recommended) or B (whole-novella). If A → run the scene-boundary
      step first.
- [ ] **Model confirmed:** Opus 4.8.
- [ ] **Worker graduated** `working/dunk-egg-pass1/dunk-egg-pass1-extraction.py` → `scripts/` (a
      deliberate `git mv`).
- [ ] **Track registered** — add the 4-line `READY` entry (section 1) to `scripts/weirwood-run.sh`;
      confirm with `weirwood run list`.
- [ ] **architecture.md §161 corrected** (rule #6 paired change) — withdraw/replace the stale "Pass 1
      records relationships in free-text" sentence to match §687 + v4's locked vocab; log the Active
      Decision (above) in the worklog. Do this when v4 is approved (not while it's still a draft).
- [ ] **Output dirs** created via `--build-queue`: `extractions/mechanical/{thk,tss,tmk}/` (canonical,
      never archive).
- [ ] **Sequencing** — worklog says D&E runs **after the first enrichment passes**. Confirm we're past
      that gate, or that Matt wants it concurrent/now.
- [ ] **Then, and only then:** `weirwood run start dunk-egg-pass1`.

> Per `feedback_no_extraction_without_asking`, the launch is a separate explicit Matt go-ahead. This
> session ends at the checklist.
