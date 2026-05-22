# Worklog Archive 013

> Sessions 58-59 (archived from main worklog). Format identical to live worklog Session Log entries.

---

### Session 59 — Stage 4 Haiku Worker Built + Smoke (2026-05-19)

**Detail:** `history/session-details/session-059.md`

**Changes made:**
- `scripts/stage4-haiku-run.py` — NEW. Haiku Stage 4 orchestrator: batch selection (`--batches`/`--all-done`), `--chunk-size`, `--concurrency` (parallel chunks), rate-limit detection, provenance snapshot, results + `run-summary.json`. Output → `prose-edges-haiku/` (separate from Sonnet's `prose-edges/`).
- `.claude/commands/stage4-haiku-classify.md` — NEW. Thin classify-only Haiku prompt; hardened with a `## CRITICAL RULES` section (Tier-1 qualifier-enum table, KNOWS STOP, qualifier≠direction, no-invented-types, type contracts).
- `.claude/agents/prose-edge-classifier.md` — R1/R2/R3 applied (Pattern 5 KNOWS STOP rule + KNOWS type-contract row; co-presence centralized rule; qualifier self-check).
- `scripts/stage4-haiku-smoke-prep.py` / `-cleanup.py` / `-finish.sh` — NEW (smoke scaffolding).
- `working/session-results/2026-05-19-batch-0020-opus-audit.md` — NEW (audit re-run; verdict "needs prompt change first" → R1).
- New Haiku mission dir `working/missions/2026-05-19-stage4-haiku/`; batch-0020 Sonnet control + Haiku-v1 output archived under `working/wiki/pass2-buckets/_archive/`.
- Memory `project_stage4_haiku_not_sonnet.md` — NEW.
- Continue prompt `2026-05-19-stage4-haiku-run-batches.md` — NEW. `2026-05-19-stage4-haiku-smoke-fire.md` + `2026-05-19-batch-0020-opus-audit.md` — DELETED (completed).

**Decisions:** Haiku is the Stage 4 bulk worker; **Sonnet is off the table** (cost — ~1017 batches; memory `project_stage4_haiku_not_sonnet`). The Haiku worker is built SEPARATE from the Sonnet worker (own scripts, output dir, mission dir) — never co-mingle. Haiku cannot drive the Sonnet worker harness's batch-bookkeeping (claimed wrong batch, early-exited, asked human mid-task) → a Python orchestrator does all bookkeeping; Haiku only classifies. Prompt hardening works when rules are inlined WITH their data (qualifier-missing 38→0, KNOWS 60→16) — proven twice. Speed-first; imperfect output acceptable (Opus watcher + later mechanical-extraction enrichment backstop). batch-0020 Haiku chunk-10 parallel = $1.86/5.7min vs chunk-3 = $2.99/28.5min — under Sonnet's $3.42. Remaining ~17.5% drift = invented type-name variants + type-contract → next: Python normalizer + inline-vocab + pre-loading re-architecture.

**What's next:**
- **Opus conductor — optimize Haiku pass speed, run batches, compare vs Sonnet, harden, iterate, scale** → continue: `progress/continue-prompts/2026-05-19-stage4-haiku-run-batches.md` (**Opus 4.7** conductor).
- 8-batch Haiku wave (queued batches, chunk-15, concurrency-8) completed at session close — next session reads its `run-summary.json` as STEP 0.
- **/endsession was explicitly authorized this session.**

---

### Session 58 — Stage 4 Lockdown Completion + Vocab Round 2 (2026-05-18 → 2026-05-19)

**Detail:** `history/session-details/session-058.md`

**Changes made:**
- `reference/edge-qualifier-vocab.md` — NEW. 18 enum-bearing types (8 Tier-1 + 10 Tier-2). IN_LAW_OF added Round 2 with `{by_marriage_of_*}` enum.
- `reference/architecture.md` — `## Edge Types` intro cross-ref to qualifier-vocab; 10 new edge type rows across 6 subsections (Kinship/Political/Factional/Military/Knowledge/Cultural); vocab callout 149 → 159; Session-58 audit history line added.
- `.claude/agents/prose-edge-classifier.md` — `notes` field DELETED from emit_edge schema; `qualifier` field added with tier-dependent behavior; qualifier-lookup workflow step (step 4); Pattern 4 prohibition; 5 vocab-count refs bumped 149 → 159; reverse-direction lists extended (STEP_PARENT_OF/STEP_CHILD_OF one-sided pair; IN_LAW_OF/CONSPIRES_WITH symmetric).
- `scripts/stage4-resolve-link-placeholders.py` — NEW. 4,744 queued candidate files rewritten (121,310 `[LINK]` → `«anchor»` substitutions). Inline patch in `scripts/wiki-pass2-build-edge-candidates.py` for future generations.
- `scripts/wiki-pass2-validate-edge-jsonl.py` — extended with 3 new check classes (type contracts / qualifier enums / notes-rejection). Self-test on 21 Sonnet control-arm batches surfaces 2,528 new violations (1,757 tier-3 qualifier emission dominant; 380 not-in-enum; 193 notes; 149 missing required; 49 type-contract).
- `scripts/wiki-pass2-flag-suspicious-edges.py` — extended with 6 pattern classes. Full run across 72 done batches / 4,075 emits: 288 flagged (7.1%). KNOWS-as-fallback dominates at 82.3% of KNOWS emits; batch-0020 alone has 140 of 163.
- `working/qualifier-vocab/audit-completeness-2026-05-19.md` — NEW. 229-line audit deliverable; 8 STRONG ADOPT edges + 0 sub-qualifiers + 8 MEDIUM DEFER + 11 REJECT + 3 borderlines.
- `working/qualifier-vocab/decisions.md` — `## Round 2` section appended (Round 1 untouched).
- `progress/continue-prompts/2026-05-19-batch-0020-opus-audit.md` — NEW (Opus audit running in iTerm2 at session close).
- `progress/continue-prompts/2026-05-19-stage4-haiku-smoke-fire.md` — NEW.
- `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-encode.md` — DELETED (STEP 1.6 completed).
- `progress/continue-prompts/2026-05-18-stage4-haiku-cutover.md` — DELETED (superseded by smoke-fire prompt).
- `working/todos.md` — HAIKU-CUTOVER STEPS 1.6/1.7/2/3/4 marked [x]; entity-linking-Pass-1-to-nodes item added under Ideas & Backlog (Matt's session-58 follow-up).
- `history/session-details/session-058.md` — NEW.
- `history/worklog-archives/archive012.md` — NEW. Session 53 archived (archive012 holds 1/5 entries).

**Decisions:** **Vocab FINAL at 159 types / 18 enumerable** (8 Tier-1 + 10 Tier-2 + ~141 Tier-3). **Sub-qualifier dimension NOT adopted** — audit confirmed enum value IS the leaf. 10 new edge types adopted from vocab-completeness audit: SPIES_ON, INFORMS, NAMED_AFTER, STEP_PARENT_OF, STEP_CHILD_OF, IN_LAW_OF (Tier-2), RESCUES, BANISHES, TORTURES, CONSPIRES_WITH. **Pass-1 deterministic harvester deferred** — architecture settled (markdown-parse + Haiku closed-vocab + Opus stratified audit), not built; revisit after Haiku smoke. **batch-0020 chosen as canonical Haiku smoke target** (hot zone: 153/437 flagged, KNOWS-fallback concentration). **Haiku smoke fires via watcher pattern** (Matt's call) — watcher Opus 4.7, worker Haiku 4.5, verdict-gating mandatory per drift-detection rule. **Entity-linking via extractions surfaced as follow-up** (Matt's session-close add) — Pass 1 mentions ("Jon Snow", "the bastard of Winterfell") need to resolve to canonical node slugs so extractions can enrich graph-node edges. Deferred to post-smoke. **Mid-session reframe:** Matt's three probing questions — "could you have recorded relationships on that same pass?" → "python might miss what the word means... does that lock in our edges?" → "did we miss anything?" — reshaped the harvester architecture (candidate + verify, not deterministic emit) and triggered the completeness audit that produced Round 2.

**What's next:**
- **Verify batch-0020 Opus audit completion** (running in fresh iTerm2 separate process at session close; verify `working/session-results/2026-05-19-batch-0020-opus-audit.md` exists before firing smoke).
- **STEP 5 Haiku smoke fire** → continue: `progress/continue-prompts/2026-05-19-stage4-haiku-smoke-fire.md` (**Opus 4.7 watcher + Haiku 4.5 worker** per mission-protocol). Gated on audit verdict.
- After smoke: revisit Pass-1 deterministic harvester; decide Stage 4 bulk Haiku resume; begin Pass-1-mention → graph-node entity-linking work (Matt's session-58 add).
- **Per Matt's standing rule, /endsession was explicitly authorized this session — not auto-triggered.**
