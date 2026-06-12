# Nomenclature Reform Proposal

> **2026-06-12 — for Matt's decision. Proposal only; nothing has been renamed.**
> Companion to the project-story glossary (`history/project-story/glossary.md`), which decodes
> historical terms. This document retires the chaos *going forward*. Historical docs are never
> rewritten; the glossary maps old → new.

## 1. Canonical scheme going forward

Six term categories, fixed. Nothing else gets coined without a worklog Active Decision.

| Term | Definition | Rules |
|---|---|---|
| **Pass** | A numbered, corpus-wide extraction/analysis sweep over *source text* (Passes 1–6). | Whole numbers only — no "Pass 1.5". A smaller sweep is a Track. New Pass numbers require an Active Decision. |
| **Track** | A **named** (never lettered/numbered) multi-session workstream toward one milestone. E.g. *infobox-merge track*, *deception-edges track*. | The name is a noun phrase describing the deliverable. Tracks live in todos.md and get a continue prompt. |
| **Step** | A numbered unit of work inside one Track (Step 1, Step 2…). | Replaces Stage/Plate/Phase/Mode/Wave for all new sequencing. Steps are scoped to their Track — "infobox-merge Step 2" is unambiguous. |
| **Gate** | A measured go/no-go checkpoint with a numeric threshold and a recorded verdict (precision gate, spend gate, drift gate). | A Gate belongs to a Step. GO/NO-GO verdicts recorded in worklog. |
| **Tier** | **Reserved EXCLUSIVELY for confidence tiers 1–5** on facts/edges/claims. | The other two current uses are renamed (see §2). No new Tier systems, ever. |
| **Run** | One bounded execution of a script/agent over a defined input set, identified by `run_id`/`prompt_sha`. | Provenance lives in data (per the S65 rule), not in the run's name. |

**Version numbers attach only to artifacts** — schema v3, prompt v5, `edges.jsonl` v1.3 — never to efforts, eras, or workstreams. ("Events v2.0" as an *effort* name was the anti-pattern.)

**Retired from reuse** (historical vocabulary only — valid when citing past sessions, never for new work): **Stage, Plate, Mode, Wave, Bucket, Phase, Mission/watcher/worker, Sprint** (which, it turns out, was never actually used — its one occurrence is the glossary todo listing it), and the letter-track idiom (Track A/B/C/W).

## 2. Collision map

How to refer to each historical meaning unambiguously from now on.

| Term | Historical meanings | Say instead |
|---|---|---|
| **Stage** (worst offender) | (a) Pass 2's internal Stages 0–4 (wiki promotion pipeline, S16–S29); (b) "Stage 4" the prose-edge-classification *era* (S52+), which outlived its parent numbering and split into the deprecated wiki-comention track and the shipped Pass-1-derived pipeline | (a) "Pass 2 promotion, Stage N (historical)"; (b) "**the prose-edge era** (2026-05)" — subdivide as "the comention track (deprecated S65)" vs "the Pass-1-derived edge pipeline (shipped)". `stage4-*.py` script filenames stay as-is; the glossary notes they're era-named. |
| **Pass** | Passes 1–6 (coherent); "Pass 1.5" floated for dialogue/meals re-extraction | Keep Passes 1–6. The floated "Pass 1.5" becomes a named track (e.g. *dialogue-extraction track*) or, if truly corpus-wide, the next whole number. |
| **Tier** | THREE systems: (1) confidence tiers 1–5; (2) wiki page-promotion tiers (Tier-A/B pages, tier-secondary batch); (3) qualifier-vocab Tier-1/Tier-2 (required vs optional qualifier enums, architecture.md §Edge Schema) | (1) keeps "Tier" exclusively. (2) → "**promotion class A/B**" / "the secondary promotion batch". (3) → "**required-qualifier types**" and "**optional-qualifier types**" (collectively "qualifier requirement levels"). |
| **Track** | (a) wiki-era Track A (case-collision recovery) / Track B (infobox parser); (b) backfill Tracks A/B/C (vocab-retype / reification / head-rule); (c) Track W; (d) todos.md's new "Track 1–6" section headers; (e) "the validation track". Note todos Track 4 *contains* Tracks A/B/C — number-track nesting letter-tracks. | (a) "the case-collision recovery" / "**the infobox parser layer**" (worklog already mostly says Track B for this — highest-value rename); (b) "the **vocab-retype / reification / head-rule** backfill tracks" (use the names; letters historical); (d) todos sections keep their numbers as mere *ordering*, but each gets a name as the primary identifier (already half-true: "Track 1 — Infobox-Structural Merge"); cross-references use the name, not the number. |
| **Plate** | Plates 0–5, the reification merge sequence (S82–S87), one-off | Retire the name; keep the *pattern* as "**gated merge sequence**" (the generic shape: ordered steps, each gated, merging into a canonical artifact). Refer to the historical run as "the reification plates (S82–S87)". |
| **Mode** | Validation Modes 1–4 (graph-validation probe designs); "Mode 3" = the grounded-agent dip | "the **validation probes**"; Mode 3 specifically = "**the grounded-agent dip**" (already its natural name). Historical only after the dip lands. |
| **Phase** (unlisted collision) | (a) the history-audit's eras "Phase 0–11"; (b) "Phase 2 Mode 3 dip" in todos/continue prompts; (c) "Track A Phase 1/2" inside the backfill design — phases inside lettered tracks inside a numbered track | Eras → "**era**" ("the reification era"). All intra-track phases → **Steps**. |
| **Wave / Bucket** | Extraction batching (Pass 1 waves); wiki work units (Pass 2 buckets) | Pipeline-scoped historical jargon; fine when discussing those pipelines, never reused for new batching — new work says "**batch**" (already the prose-edge era's unit, and the most standard word). |
| **Mission / watcher / worker** | Orchestration protocol (DRAFT v0, dormant since S48) | Names stay *inside* the mission-protocol namespace only ("a mission-protocol watcher"); not general vocabulary. |
| **v1/v2/v3** | Two-plus version spaces: Pass-1 *prompt* versions v1–v3 vs *edges.jsonl* v1.0–v1.3, plus Events "v2.0/v2.1", watcher v1→v2, mission protocol v0 | Artifact-only rule (§1). Always qualify: "Pass-1 prompt v3", "edges v1.3". Effort versions ("Events v2.0") retired. |
| **spine / tail / core** | Components of the Pass-1-derived edge layer (deterministic spine, Sonnet tail, the resulting core) | Keep as proper nouns of that one layer ("the Pass-1 spine"); never reused as generic structure words. |

## 3. Naming rules for NEW work

1. **New multi-step effort → a named Track + numbered Steps.** Name = deliverable noun phrase. No letters, no bare numbers as primary identifiers (A/B/C ages badly; numbers collide on reorder).
2. **No new top-level term category** without a worklog Active Decision entry. The six in §1 are the whole vocabulary.
3. **Version numbers only on artifacts** (schema vN, prompt vN, edges vN.N) — never on efforts or eras. Artifact versions are always qualified with the artifact name.
4. **"Tier" means confidence tier 1–5, full stop.** Any new graded system gets a different word (class, level, priority).
5. **Checkpoints are Gates** and carry a number + threshold; "smoke", "audit", "review" describe *how* a gate is measured, not new categories.
6. **Retired terms (§2) are historical-only.** Citing them when discussing past sessions is fine and encouraged ("the Plate-3 incident"); coining "Plate 6" or "Stage 5" is not.
7. **Script/file names and registered skill names are exempt** — `stage4-*.py` etc. keep their names; renaming working code for vocabulary hygiene is not worth the churn. The same exemption extends to registered skill names in `.claude/commands/` and the CLAUDE.md skill list (`stage4-haiku-classify`, `worker-stage4`, etc.) — these names are functional references wired into the harness, not just labels. The glossary carries the mapping.

## 4. Adoption cost (one-time sweep of LIVING docs only)

Raw whole-word occurrence counts (grep, 2026-06-12); the **sweep estimate** is the subset actually needing rewording — most "Pass" and "Tier" hits are already-canonical uses that stay.

| Doc family | Stage | Tier | Track | Plate | Mode | Phase | Est. edits |
|---|---|---|---|---|---|---|---|
| `CLAUDE.md` | 1 | 3 | 0 | 0 | 0 | 0 | **~5** (Stage-4 skill mentions, tier wording) |
| `worklog.md` (Current State + Active Decisions only — Session Log is semi-historical) | 7 | 8 | 20 | 41 | 21 | 5 | **~40–60** |
| `working/todos.md` | 32 | 16 | 27 | 27 | 10 | 10 | **~50–70** |
| `reference/*` (architecture.md, agents.md, edge-qualifier-vocab.md) | 43 | 61 | 5 | 15 | 0 | — | **~40** (qualifier "Tier-1/2" → requirement levels is most of it; confidence tiers stay) |
| `.claude/agents/*` (28 agents; sweep only the ~8 live ones, banner the retired) | 55 | 124 | 5 | 0 | 3 | — | **~30–50 live; rest banner-only** |
| `working/runbooks/*` | 122 | 128 | 47 | 25 | 11 | — | **banner, don't sweep** — most runbooks document deprecated pipelines; add a one-line historical-vocabulary banner instead |
| Live continue prompts (`progress/continue-prompts/`, non-archived) | — | — | — | — | — | — | **~10–20** (~6–8 prompts reference old terms — Stage, Phase, Mode 3, Track A-B-C, Plate, Tier-3; see `progress/continue-prompts/README.md` for the full triage manifest) |

**Total: roughly 175–250 edits across ~15–20 living files**, plus ~25 one-line banners. One focused session (Sonnet-grade, mechanical, grep-driven, per-file review). `history/`, archives, session details, and the worklog Session Log stay untouched — the glossary decodes them.

**Note on same-day docs:** `reference/roadmap.md` (written 2026-06-12) itself uses retired meanings ("Tier-3 deferred", "Stage-4-richest-form") — same-day living docs are in the reference-sweep scope, not just older files. A parallel fix is being applied to roadmap.md as part of this critic pass.

**Suggested sequence if approved:** (1) land this scheme as a worklog Active Decision + a short "Vocabulary" section in CLAUDE.md; (2) sweep todos.md + worklog Current State/Active Decisions (highest agent traffic); (3) reference/* qualifier-tier rename; (4) live agents + live continue prompts; (5) banners on runbooks/retired agents. Steps 2–5 are one session.
