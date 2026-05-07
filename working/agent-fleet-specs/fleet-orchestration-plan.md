# Fleet Orchestration Plan — Weirwood Network

**Created:** Session 26 (2026-04-28)
**Purpose:** Master plan for running the 24-agent fleet across the remaining work, with Python-driven orchestration borrowing the mechanical-extraction stats/rate-limit infrastructure. Includes self-review agents (orchestrator-invoked, sample-based) for quality control.

**Why this plan exists:** The agent fleet plan (`working/agent-fleet-specs/agent-pipeline-plan.md`) lists 24 agents and their roles. This document specifies HOW to run them — concurrency, dependencies, stats, rate-limit handling, peer review, graceful failure. Without this, "run the fleet" is hand-wavy; with it, the orchestrator has a concrete operational model.

**Work queue:** This is an operating manual. The live queue of WHAT to work on is `working/todos.md`. The fleet was designed to tackle that queue automatically.

---

## Design principles

1. **Python orchestrates; agents execute.** The orchestrator is a Python script (or a Claude Code skill that drives one). Agents are subagent invocations from that orchestrator. Composition is via on-disk files (JSONL/markdown), never via direct agent-to-agent calls.

2. **Stats from Day 1.** Every agent invocation logs to a per-stage CSV with the same shape as the mechanical-extraction stats. This lets us answer "did Stage 4 run cleanly?", "what's the cost trend?", "which buckets failed?" without re-deriving from scratch each time.

3. **Wave-based parallelism with concurrency caps.** Borrowed from mechanical-extraction: spawn N agents at once, wait for the wave to complete, gather stats, advance. Cap N per agent type to respect rate limits.

4. **Rate-limit detection and graceful recovery.** Borrowed from `wiki-pass2.sh:684-688`: detect the `"rateLimitType"` JSON marker in agent failure responses; back off; retry. If the rate limit blocks the whole wave, pause until reset.

5. **Sample-based peer review.** A reviewer agent reads a stratified 5-10% sample of a classifier's output and writes a quality verdict. Orchestrator surfaces verdicts; doesn't auto-action them. Reviewers are CHEAP — they read JSONL and produce a short report, not full nodes.

6. **Idempotent re-runs.** Every stage is re-runnable. If Stage 4 completes 80% then crashes, re-running picks up where it stopped (manifest-driven, like wiki-pass2.sh). No double-emission, no double-cost.

7. **Graceful failure isolation.** One agent's failure doesn't crash the orchestrator. Failures get logged to the stats CSV with `status=fail` + `error_message`. The orchestrator continues with the next agent.

---

## Stage diagram (the master DAG)

```
                              FOUNDATION (deterministic Python, $0)
                                          │
              ┌───────────────────────────┼───────────────────────────┐
              ▼                           ▼                           ▼
     [build-alias-resolver.py]  [re-build-cross-refs.py     [build-edge-candidates.py
        — alias index             — applies alias-resolver    — Stage 4 candidate
        from frontmatter]         drops broken-link rate]     generation per bucket]

                                          │ (all 3 must complete)
                                          │
                              ┌───────────┴───────────┐
                              ▼                       ▼
              QUALITY AUDITS (parallel — read-only)    STAGE 4 CLASSIFICATION
              ─ schema-drift-auditor                  ─ prose-edge-classifier
              ─ citation-validator                       (per-bucket parallel,
              ─ duplicate-detector                        wave size 5)
              ─ orphan-edge-finder                     ─ cross-identity-detector
                                                          (one global run)
                                                       ─ disambiguation-resolver
                                                          (after prose-edge runs,
                                                           consumes escalations)
                              │                       │
                              ▼                       ▼
              QUALITY REPORTS (one .md each)    STAGE 4 REVIEW (sample-based)
              ─ working/audits/                 ─ prose-edge-reviewer
                schema-drift-<date>.md             (5% sample per bucket)
                citation-issues-<date>.md       ─ cross-identity-reviewer
                orphan-edges-<date>.md             (100% — rarer + higher-stakes)
                duplicate-candidates.jsonl
                                                       │
                                                       ▼
                                       STAGE 4 PROMOTE (deterministic Python)
                                       ─ promote-prose-edges.py
                                       ─ promote-cross-identity.py
                                       (atomic-rename; updates graph/nodes/)

                                          │
              ┌───────────────────────────┼───────────────────────────┐
              ▼                           ▼                           ▼
       PASS 1 CATCH-UP             FLEET-STATS-REVIEWER          (on-demand
       (parallel across books;     (after each major stage:        cleanup
        wave-based per book)        synthesizes CSVs into a        reruns
       ─ mechanical-extractor       human-readable status)         as needed)
         on ACOK / ASOS / AFFC /
         ADWD chapters

                                          │
                                          ▼
                        PASS 1 PER-BOOK QUALITY (after each book completes)
                        ─ extraction-quality-auditor (one per book)
                        ─ cross-book-entity-reconciler (after ≥2 books)
                        ─ contradiction-surfacer (after ≥2 books)

                                          │
                                          ▼
                              PASS 3 (Voice & Perception)
                              ─ voice-analyzer (per POV)
                              ─ perception-mapper (per POV-target pair)
                              [requires perception edge vocabulary expansion]

                                          │
                                          ▼
                              PASS 4 (Foreshadowing)
                              ─ foreshadowing-scanner (full corpus)
                              ─ chekhovs-gun-tracker (full corpus)

                                          │
                                          ▼
                              PASS 5 (Theory-Informed)
                              ─ theory-extractor (per theory)
                              ─ theory-evidence-scorer (per theory)
                              [requires reference/theory-seeds.md]

                                          │
                                          ▼
                              PASS 6 (Open-Ended Discovery)
                              ─ discovery-agent (full corpus, runs LAST)

                                          │
                                          ▼
                              TIER 3 DEFERRED (chronology)
                              ─ chronology-extractor
                              ─ event-orderer
                              [requires temporal edge vocabulary expansion]

                                          │
                                          ▼
                              POST-RELEASE BACKFILL
                              ─ first-available backfill (deterministic Python)
                              ─ trigger table build
                              ─ entity index build
```

---

## Stages in detail

### Stage 0 — Foundation (deterministic Python, $0)

Three scripts, run sequentially:

| Script | Purpose | Output |
|--------|---------|--------|
| `wiki-pass2-build-alias-resolver.py` | Walk all `graph/nodes/**/*.node.md` frontmatter `aliases`; build canonical wiki-form-slug → canonical-slug map | `working/wiki-parsed/alias-resolver.json` |
| `wiki-pass2-build-cross-refs.py --apply` (re-run with alias resolution) | Re-extract cross-refs using alias-resolver to drop slug-mismatch noise | Updates `cross-references.jsonl`, `backlink-counts.json`, `cross-refs-summary.md`. Expect broken-link rate to drop ~50% (slug-mismatch noise → real gaps). |
| `wiki-pass2-build-edge-candidates.py` | For each bucket, walk prose, extract `[anchor](wiki:Page)` cross-references, filter against existing edges, emit per-source-slug candidate JSONL | `working/wiki-pass2/<bucket>/prose-edge-candidates/<slug>.candidates.jsonl` |

**Total cost:** $0
**Total wall-clock:** <2 minutes
**Failure mode:** script crashes — fix and re-run, idempotent
**Stats logged:** `working/fleet-stats/stage-0-foundation.csv` — one row per script with start/end/duration/output_size

### Stage 1 — Quality audits (4 agents, parallel)

Run all four read-only audit agents simultaneously. Each produces a markdown report.

| Agent | Wave size | Scope | Output |
|-------|-----------|-------|--------|
| `schema-drift-auditor` | 1 (single global pass) | full graph | `working/audits/schema-drift-<date>/execution/schema-drift.md` |
| `citation-validator` | 1 | full graph | `working/audits/citation-issues-<date>/execution/citation-issues.md` |
| `duplicate-detector` | 1 | full graph | `working/wiki-pass2/duplicate-candidates.jsonl` + `working/audits/duplicate-detector-<date>/execution/duplicate-detector-stats.md` |
| `orphan-edge-finder` | 1 | full graph | `working/audits/orphan-edges-<date>/execution/orphan-edges.md` |

**Concurrency:** All 4 launched in parallel via 4 Agent tool calls in a single message. They're read-only — no file conflicts.
**Cost:** ~$5-15 each = $20-60 total
**Wall-clock:** ~30-60 minutes (longest single agent)
**Stats logged:** `working/fleet-stats/stage-1-quality-audits.csv`
**Failure handling:** If one agent fails (rate limit, error), others continue. Failed agent gets `status=fail` row; orchestrator re-runs the failed one after the wave completes.

### Stage 2 — Stage 4 classification (3 agents, varied parallelism)

Three agents, different shapes:

#### 2a. `prose-edge-classifier` — bucket-parallel

- One invocation per bucket with prose-edge-candidates files (typically 472 secondary buckets + recovery buckets)
- Wave size: 5 buckets at a time (concurrency cap to respect rate limits)
- Each invocation reads `working/wiki-pass2/<bucket>/prose-edge-candidates/*.candidates.jsonl`, emits `working/wiki-pass2/<bucket>/prose-edges/*.edges.jsonl`
- Resume-able: orchestrator checks bucket manifest for `stage4_classified_at` field; skips done buckets

**Estimated cost:** ~$50-100 across all buckets
**Wall-clock:** 3-5 hours with 5-tab parallelism
**Stats:** `working/fleet-stats/stage-2a-prose-edge-classifier.csv` — one row per bucket invocation

#### 2b. `cross-identity-detector` — single global run

- One invocation reading the full duplicate-candidates.jsonl + alias-resolver.json + redirect graph
- Wave size: 1 (global, not parallel)
- Output: `working/wiki-pass2/cross-identity-decisions.jsonl`

**Estimated cost:** ~$10-20
**Wall-clock:** ~1 hour
**Stats:** `working/fleet-stats/stage-2b-cross-identity-detector.csv`

#### 2c. `disambiguation-resolver` — after 2a

- One invocation per bucket with disambiguation escalations from 2a
- Wave size: 3 (smaller; this agent is reasoning-heavy)
- Resume-able

**Estimated cost:** ~$10-30 (depends on escalation volume)
**Stats:** `working/fleet-stats/stage-2c-disambiguation-resolver.csv`

### Stage 3 — Stage 4 peer review (sample-based)

This is the new addition. Reviewer agents read a stratified sample of classifier output and write quality verdicts.

| Agent | Sample strategy | Output |
|-------|-----------------|--------|
| `prose-edge-reviewer` | Random 5% sample per bucket of `prose-edges/*.edges.jsonl` rows | `working/audits/prose-edge-review-<date>/execution/prose-edge-review.md` per bucket |
| `cross-identity-reviewer` | 100% of `cross-identity-decisions.jsonl` (rarer + higher-stakes) | `working/audits/cross-identity-review-<date>/execution/cross-identity-review.md` |

**Sample-based not full-pass because:**
- Full-pass cost ~= classifier cost (defeats the point)
- 5% catches systematic biases — the kind of error that affects many decisions consistently
- 5% misses one-off errors — but the cost calculus favors fast and cheap over comprehensive
- Cross-identity at 100% because each decision is high-stakes (a `SAME_AS` edge is structurally important; ~50-100 candidates total, not thousands)

**Concurrency:** prose-edge-reviewer is per-bucket parallel (wave size 5). Cross-identity-reviewer is single-pass.

**Cost:** ~$10-20 total (cheap because reviewers read structured JSONL, not full prose)
**Wall-clock:** ~30-60 minutes total
**Stats:** `working/fleet-stats/stage-3-peer-review.csv`

**What reviewers DO:**
- Check that classifier outputs respect the locked vocabulary
- Spot-check edge_type assignments against the snippet
- Flag patterns: "this bucket has 30% `SPOUSE_OF` decisions where the snippet says 'lover'" — possible mis-classification
- Surface cases where escalation seems warranted but classifier didn't escalate

**What reviewers DON'T DO:**
- Re-classify (don't redo the classifier's work)
- Modify any output files
- Override decisions
- Recurse into other agents

### Stage 4 — Stage 4 promote (deterministic Python)

Two scripts:

| Script | Purpose |
|--------|---------|
| `wiki-pass2-promote-prose-edges.py --apply` | Walk all `prose-edges/*.edges.jsonl`; append accepted edges to nodes under `## Edges (prose-derived)` subheading. Atomic-rename. Conflict-detect. |
| `wiki-pass2-promote-cross-identity.py --apply` | Walk `cross-identity-decisions.jsonl`; append `SAME_AS` edges to alias nodes. Same atomic-rename pattern. |

**Cost:** $0
**Wall-clock:** <5 minutes total

### Stage 5 — Pass 1 catch-up

Mechanical-extractor on ACOK / ASOS / AFFC / ADWD chapters. Already-existing wave-based infrastructure (`scripts/mechanical-extract.sh` or whatever's named). Per-book parallelism.

**Per-book cost:** ~$95 (per AGOT precedent)
**Per-book wall-clock:** 4-8 hours with 3-5 parallel tabs
**Stats:** existing `working/extraction-stats/extraction-stats-<book>-pass1-v3.csv`

This stage runs INDEPENDENTLY of Stage 1-4 (no graph dependency). Can be background-running during Stage 1-4 work.

### Stage 6 — Pass 1 per-book quality

After each book completes Pass 1:

| Agent | Trigger | Output |
|-------|---------|--------|
| `extraction-quality-auditor` | Book complete | `working/audits/extraction-quality-<book>-<date>.md` |
| `cross-book-entity-reconciler` | ≥2 books complete | `working/curation/alias-additions.jsonl` |
| `contradiction-surfacer` | ≥2 books complete | Append to `working/wiki-pass2/pass1-contradictions.jsonl` |

### Stage 7-9: Pass 3-6, Tier 3, Post-release backfill

Each Pass is its own multi-session work block. Detailed orchestration plans get drafted as we approach them. Skeletons exist; full prompts come into focus when prerequisites are met.

---

## Stats schema

Every agent invocation writes a row to its stage's CSV. Schema:

```csv
agent_name,run_id,target,started_at,completed_at,duration_seconds,input_tokens,output_tokens,cost_usd,status,retries,rate_limit_hits,output_path,error_message,reviewer_verdict
```

Columns:
- `agent_name` — e.g., `prose-edge-classifier`
- `run_id` — UTC timestamp of the orchestration run, used to group rows from one fleet-orchestrator invocation
- `target` — what the agent processed (bucket name, chapter file, etc.)
- `started_at` / `completed_at` — UTC ISO 8601
- `duration_seconds` — wall-clock
- `input_tokens` / `output_tokens` — for cost computation + bucket-size-relative analysis
- `cost_usd` — computed at row-write time using the agent's model rate
- `status` — `pass` / `fail` / `partial` / `rate-limit-skipped`
- `retries` — number of retries this row represents
- `rate_limit_hits` — number of rate-limit responses encountered
- `output_path` — where the agent wrote its output (for forensic recovery)
- `error_message` — populated when `status != pass`
- `reviewer_verdict` — populated by Stage 3 review pass: `clean` / `concerns` / `not-reviewed`

Per-stage CSV files live at `working/fleet-stats/stage-<N>-<stage-name>.csv`.

A summary CSV `working/fleet-stats/fleet-summary-<run-id>.csv` aggregates one row per stage with: stage_name, agents_run, success_count, fail_count, total_cost, total_duration, reviewer_concerns_count.

---

## Rate-limit handling

Adapted from `wiki-pass2.sh:684-688`'s detection logic.

**Detection:** when an agent invocation fails, the orchestrator parses the failure response. If it contains `"rateLimitType"`, it's a rate-limit failure (not a true error).

**Backoff strategy:**
1. **Per-agent within-wave**: if one agent in a wave hits rate limit, that agent gets `status=rate-limit-skipped` for now; the wave continues with other agents
2. **Whole-wave**: if the orchestrator sees ≥3 rate-limit hits in one wave, pause the whole wave for the rate-limit reset duration (parsed from the error if available, else 5 minutes default)
3. **Whole-stage**: if rate limits persist after backoff, the orchestrator pauses the stage and emits a `rate-limit-blocked` summary; user resumes manually

**Resume:** because every stage is idempotent + manifest-driven, resuming after a rate-limit-pause means re-running the orchestrator on the same stage. Already-completed agents are skipped (manifest checks); rate-limit-skipped agents are retried.

**Tracking:** the stats CSV's `rate_limit_hits` column lets us see whether a particular agent consistently hits rate limits (might need a smaller wave size for that agent's stage).

---

## Self-review pattern (clarification)

This pattern is COMPATIBLE with the no-recursive-subagent rule:

```
Orchestrator (Python or main Claude Code session)
  ├── invokes  prose-edge-classifier  →  writes prose-edges/*.edges.jsonl
  ├── invokes  prose-edge-reviewer    →  reads prose-edges/*.edges.jsonl
  │                                       writes audits/prose-edge-review-*.md
  └── parses reviewer's report; if "concerns", surfaces to user
```

The reviewer is a SECOND subagent invoked by the orchestrator (one level deep). It reads the first subagent's text-stream output. No recursive call. Same Unix-pipe pattern.

**Why this is different from the "no peer review" position I took earlier:**
- Earlier I rejected `theory-extractor → theory-extractor-reviewer` as a chain. That would be recursive (one agent invoking another).
- The pattern here is `orchestrator → A`, then `orchestrator → B reading A's output`. That's composition, not recursion.
- Convergence-bias risk is real but mitigated by sample-based review (catches systematic biases, accepts some single-decision noise) and by the reviewer being framed differently from the classifier ("find suspicious patterns" vs "classify each candidate").

**Reviewer agent design pattern:**
- Tools: `Read, Glob, Grep` — read-only on the output being reviewed
- Output: a single markdown report (not JSONL — humans read these)
- Cost target: <$5 per reviewer run (cheap because they read structured data, not full prose)
- Length: <500 tokens of output per reviewed file
- Forbidden: re-classifying, overriding, modifying any source files

---

## New agents this plan adds (3 reviewers)

| Agent | File | Status | Role |
|-------|------|--------|------|
| `prose-edge-reviewer` | `.claude/agents/prose-edge-reviewer.md` | Stub | Reviews 5% sample of `prose-edge-classifier` output per bucket. Spots systematic biases, malformed entries, mis-classified edge types. |
| `cross-identity-reviewer` | `.claude/agents/cross-identity-reviewer.md` | Stub | Reviews 100% of `cross-identity-detector` output (low volume, high stakes). Verifies each `SAME_AS` proposal against the source nodes. |
| `fleet-stats-reviewer` | `.claude/agents/fleet-stats-reviewer.md` | Stub | After each major stage, reads the stage's stats CSV + the audit reports + the reviewer reports; produces a one-page synthesis: "Stage 2 complete. 472 buckets, 95% pass rate, 3 buckets escalated, $89 cost. Recommended action: review the 3 escalated buckets before promoting." |

Total fleet now: 27 agents (24 from prior plan + 3 reviewers).

---

## Implementation roadmap

The orchestrator itself doesn't exist yet. Build order:

| Step | Deliverable | When |
|------|-------------|------|
| 1 | Stats schema implementation — Python helper `scripts/fleet_stats.py` with `record_invocation(...)` and `aggregate_stage(...)` functions | Before first orchestrated run |
| 2 | Wave-based agent dispatcher — Python helper `scripts/fleet_dispatcher.py` that takes a list of agent invocations and a wave size, runs them with rate-limit-aware concurrency | Before first multi-agent stage |
| 3 | Stage 0 foundation scripts (alias-resolver, re-cross-refs, edge-candidate-generator) | Before Stage 4 work |
| 4 | Stage 1 audits — manual orchestration first, then via orchestrator if pattern proves out | Standalone — can run today on existing graph |
| 5 | Stage 2 prose-edge-classifier — manual first, then orchestrated; gets stats infrastructure proven | After Stage 0 + Stage 1 |
| 6 | `fleet-stats-reviewer` — first run after Stage 2 completes | Validates the stats infrastructure |
| 7 | Full orchestrator script `scripts/fleet-orchestrator.py` driven by `fleet-config.yaml` | Once 4-6 manual orchestrations validate the pattern |

**Pre-orchestrator phase:** Stages 0-2 can run via direct Agent tool calls from the main session, with stats manually appended to CSVs. This validates the schema before automating.

**Post-orchestrator phase:** YAML config defines stages, agents, dependencies, parallelism. `fleet-orchestrator.py --stage 2 --bucket-glob 'houses-*'` runs a stage. `--resume` picks up after a crash.

---

## What this plan deliberately doesn't include

- **Auto-promote on review pass.** Reviewer "clean" verdicts don't auto-trigger promotion. Matt or the orchestrator looks at the verdicts and decides.
- **Per-decision dispute resolution.** If a reviewer disagrees with the classifier, the disagreement gets logged but no third agent adjudicates. Surface; don't auto-resolve.
- **Cross-stage peer review.** Stage 4's prose-edge-classifier output isn't reviewed by a Stage 5 theory agent. Each stage's reviews stay within the stage.
- **Continuous integration / always-on monitoring.** This is a batch orchestration plan, not a streaming system. Nothing runs continuously.
- **Predictive cost estimates beyond order-of-magnitude.** Real costs come from actual runs. The estimates here are calibration-quality only.

---

## Cost / time summary across the full plan

| Stage | Agents | Cost | Wall-clock |
|-------|--------|------|------------|
| Stage 0 — Foundation | (none — Python only) | $0 | <2 min |
| Stage 1 — Quality audits | 4 | $20-60 | ~30-60 min (parallel) |
| Stage 2 — Stage 4 classification | 3 | $70-150 | ~5-7 hours |
| Stage 3 — Stage 4 peer review | 2 | $10-20 | ~30-60 min |
| Stage 4 — Stage 4 promote | (none — Python only) | $0 | <5 min |
| Stage 5 — Pass 1 catch-up (4 books) | 1 (mechanical-extractor) | ~$380 | ~16-32 hours over multiple sessions |
| Stage 6 — Pass 1 per-book quality | 3 | $30-60 per book | ~2-4 hours per book |
| Stage 7 — Pass 3 (Voice & Perception) | 2 | $200-400 | Multi-session |
| Stage 8 — Pass 4 (Foreshadowing) | 2 | $100-200 | Multi-session |
| Stage 9 — Pass 5 (Theory-Informed) | 2 | $200-400 | Multi-session |
| Stage 10 — Pass 6 (Discovery) | 1 | $200-500 | Multi-session |
| Stage 11 — Tier 3 (Chronology) | 2 | $20-40 | TBD |
| Stage 12 — Post-release backfill | (none — Python only) | $0 | <30 min |
| `fleet-stats-reviewer` runs (across stages) | 1 (multiple invocations) | $20-50 cumulative | ~10 min per invocation |

**Total remaining-work budget: ~$1,250-2,310** for all 27 agents across all 12 stages, with stats + peer review + rate-limit handling baked in.

---

## Files this plan ties into

- `working/agent-fleet-specs/agent-pipeline-plan.md` — agent fleet roster (this plan adds 3 reviewers to bring total to 27)
- `reference/design-philosophy.md` — Unix philosophy, soft-corrected on peer review (orchestrator-invoked sample-based review is fine; recursive-subagent peer review is not)
- `reference/agents.md` — canonical roster (sync with this plan when reviewers' stubs land)
- `working/runbooks/wiki-pass2-pipeline.md` — Stage 3 done; Stage 4 spec lives in this plan
- `progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md` — gets superseded by this fleet plan; archive when Stage 4 starts
