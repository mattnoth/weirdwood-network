---
session_date: 2026-05-15 → 2026-05-16
session_number: 54
session_focus: Stage 4 prose-edge classifier — schema drift discovery, Haiku failure, 21-batch bulk run with two prompt-patch iterations
model_used: claude-opus-4-7[1m]
worklog_entry: worklog.md § Session 54
---

# Session 54 — Stage 4 Schema Lockdown + 21-Batch Bulk Run

## What happened (narrative)

This session compressed three logically distinct phases into one continuous wall-clock session. The phases:

### Phase 1 — Schema drift discovery + Haiku rejection (2026-05-15)

Matt asked for a quality audit of batch-0012 (the first batch under the new 1-tab + 90-min throttle configuration). The audit revealed that batch-0012's output looked semantically reasonable but had **regressed the output schema** — the `rationale`/`evidence_snippet` field that batch-0011 produced was gone, replaced by `cite_ref: "## Appearances"` (just the section header the Python preprocessor had already attached). Every emit_edge row had been gutted of provenance. The validator-less pipeline didn't catch it because the schema was technically valid; cross-model audit (Opus reading Sonnet) caught it on the first read.

The deep-dive explanation went into `working/session-results/2026-05-15-stage4-edge-provenance-explained.md` — the headline insight being that the prompt's required-fields list wasn't pinned as a hard contract, so each worker session re-derived the output schema from its prompt reading and tended toward the most concise valid-looking JSON.

Matt agreed: pin the schema in the prompt + add a mechanical validator. We did that:
- `.claude/agents/prose-edge-classifier.md`: added an "## Output Contract → Required fields per decision" table with explicit required-fields per (decision, candidate_kind), shape rules (`confidence_tier` int 1-3, `evidence_snippet` verbatim ≥10 chars not section-header), and a forbidden-vocab callout (`cite_ref` rejected, `notes`-instead-of-`reason` rejected).
- `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md`: added a "Two failure modes to avoid" section + a step-0 in the post-processing flow that runs the validator BEFORE marking the batch done. If validator fails, fix rows + re-run until clean.
- `scripts/wiki-pass2-validate-edge-jsonl.py`: new mechanical validator. Loads architecture.md vocab (127 canonical types found via regex), checks each row against the required-fields contract, surfaces violations with file:line + slug context. Self-tested against the archived broken batch-0012 (caught 14/14 violations on the qarl-corbray.edges.jsonl file).

Per the discussion, we also:
- Added 4 new edge types to architecture.md: UNCLE_OF, NEPHEW_OF, KILLED_WITH, ATTENDS (Session-54-marked).
- Added `evidence_kind` discriminator field on emit_edge rows: `wiki-entity` / `wiki-chapter-summary` / `book-pass1`. This is the provenance discriminator — downstream queries can filter on authority (which corpus the edge came from).
- Documented the third candidate shape (`pass1_relationship`) in the classifier prompt. It was already wired in the candidate generator but the prompt had only documented two shapes.

Then we ran a Haiku 4.5 smoke test on batch-0012 to validate Matt's "Haiku bulk + Opus audit" cost-saving idea. Result: **systematic failure**. Validator passed (Haiku produces structurally-clean output) but the semantic content was ~80% wrong:
- 53% of emits (133/252) collapsed to `SERVES` regardless of actual relationship
- KILLED_BY direction reversed (qarl-corbray KILLED_BY davos-darklyn when the prose says Qarl killed Davos)
- Type-contract violations on every spatial/event edge (regions, dragons, years, generic concepts as SERVES/SPOUSE_OF targets)
- Cross-identity escalation missed (Sonnet caught the tom-costayne/tommen-costayne-knight pair; Haiku emitted nonsense edges between them)
- 0 vocab-gap questions filed (Haiku just slammed everything into 9 default types)

Verdict in `working/session-results/2026-05-15-stage4-haiku-smoke-verdict.md`: Haiku 4.5 not viable for this task. The cost-saving plan dies — Opus would have to re-classify every Haiku edge, not just audit. Stick with Sonnet.

Both failed batches preserved as archives for the comparison record:
- `working/wiki/pass2-buckets/_archive/batch-0012-sonnet-pre-schema-fix-2026-05-15/`
- `working/wiki/pass2-buckets/_archive/batch-0012-haiku-failed-2026-05-15/`

Memory rule saved: `feedback_drift_detection_mandatory.md` — every Stage 4+ bulk run includes mechanical schema validator + cross-model audit + verdict-gates-resumption, regardless of model. Cache resets re-roll the model's interpretation of any field the prompt doesn't pin.

### Phase 2 — Canonical batch-0012 + initial bulk firing (2026-05-15)

Re-ran batch-0012 on Sonnet with the patched template. Result: CLEAN. 63 emit / 282 reject / 2 escalate, 1.6% type-contract concerns, all 4 KILLED_BY directions correct, cross-identity caught. Locked this as the canonical reference for these 30 buckets.

Then fired batches 0013, 0014, 0015 sequentially with ~60s sleeps. All CLEAN per validator. Trajectory:
- batch-0013: 152 emits, 0.0% type-contract, 7/7 KILLED_BY correct
- batch-0014: 170 emits, 2.9% type-contract, 5/5 KILLED_BY correct, **but two new failure modes surfaced**:
  - **CONTEMPORARY_WITH-as-fallback** at 14 emits where the actual relationship was milk-brother, wet-nurse, knighting, hosting. The worker also correctly filed vocab-gap questions for these, but ADDITIONALLY emitted a wrong-fit edge as fallback.
  - **Reverse-direction vocab gaps**: CHILD_OF (reverse of PARENT_OF), HOSTED_BY (reverse of GUEST_OF), RESURRECTED_BY (reverse of RESURRECTS). These are not missing types — they're one-sided by design. Worker filed them as gaps because it didn't understand directionality.

Both patches added to the next batch's prompt:
- Patch A: "Do NOT emit a wrong-fit canonical type as a 'fallback' when a vocab gap is filed. Specifically, do not use CONTEMPORARY_WITH as a catch-all..."
- Patch B: "Reverse-direction edges — do NOT file as vocab gaps." Listed PARENT_OF/CHILD_OF, GUEST_OF/HOSTED_BY, RESURRECTS/RESURRECTED_BY, TUTORS/TUTORED_BY, WIELDS/WIELDED_BY, OWNS/OWNED_BY, FORGED_BY/FORGED. Listed exceptions (both-sided): KILLS/KILLED_BY, UNCLE_OF/NEPHEW_OF, WARD_OF/FOSTERED_BY.

batch-0015 ran under these inline patches: **0 CONTEMPORARY_WITH, 0 reverse-direction vocab gaps**. Patches worked. Codified into the canonical classifier prompt + worker template so future workers benefit automatically.

batch-0016 (first under codified patches): 119 emits, 0 CONTEMPORARY_WITH, 1 legit new vocab gap (DEPICTED_IN — character-as-subject-of-in-world-text). Pattern held.

### Phase 3 — Regression + new patches + parallel bulk (2026-05-16)

batch-0017 ran clean. Then batch-0018 (Frey buckets) regressed: CONTEMPORARY_WITH back to 21 emits. Frey is the densest kinship cluster in ASOIAF (Walder Frey has 100+ descendants); the patch reduced rate but didn't survive high-cognitive-load conditions. Worker also filed COUSIN_OF as a vocab gap (legit — same reasoning as UNCLE_OF/NEPHEW_OF for one-hop kinship shortcut).

Audit of all 21 CONTEMPORARY_WITH emits in batch-0018:
- ~18 were clearly fallback misuse (cersei-frey CONTEMPORARY_WITH robb-stark = OFFERED_AS_BRIDE; hosteen-frey CONTEMPORARY_WITH wyman-manderly = OPPOSES; lothar-frey CONTEMPORARY_WITH roose-bolton = ALLIES_WITH/CONSPIRES_WITH; etc.)
- ~3 were borderline
- 0 were genuine peer-of-era assertions

Stopped firing. Surfaced to Matt with the three-paths decision (continue with post-clean / pause for data-driven schema lockdown / strengthen prompt now and resume). Matt picked: keep firing, accept the baseline, fold improvements as we discover them. Don't over-engineer.

Quick wins implemented:
- Added 7 new edge types to architecture.md: COUSIN_OF, MILK_BROTHER_OF, NURSED_BY, WET_NURSE_OF, KNIGHTED_BY, BESTOWS_KNIGHTHOOD_ON, DEPICTED_IN. Vocab now ~132 types.
- Added a top-level "## Common failure patterns" section to the classifier prompt with three concrete from-the-data examples: (1) CONTEMPORARY_WITH-fallback with 6 example cases; (2) FIGHTS_IN-with-person-target with corrective restatement ("X fought against Y" = two edges: FIGHTS_IN-battle + OPPOSES-person); (3) ATTENDS-with-person-target ("attended wedding of A and B" = ATTENDS-wedding-event, not ATTENDS-bride).

Then fired 3 parallel Sonnet workers in background (batches 0019, 0020, 0021). Lock files coordinate; workers retry next-queued if collision. Results:
- batch-0021: 60 emits, 0.0% type-contract, 0 CONTEMPORARY_WITH, 1/1 KILLED_BY correct. **Best batch yet** — strengthened prompt working perfectly.
- batch-0019: 74 emits (after schema-repair episode where worker initially emitted with missing required fields + wrong field names, validator caught it, worker wrote post-hoc Python repair). Validated CLEAN post-repair. 0/74 type-contract, 5/5 KILLED_BY correct, 0 CONTEMPORARY_WITH.
- batch-0020: 437 emits (huge — Frey-t-z + Glover buckets are dense). **NEW soft-fallback discovered: KNOWS at 163 emits / 37%**. CONTEMPORARY_WITH stayed at 0, but KNOWS became the new catch-all. Also 6 ATTENDS-with-person-target violations recurring, and 3 KILLED_BY over-attributed (Ethan Glover at Tower of Joy ascribed to each of 3 Kingsguard individually instead of as a group). 27 COUSIN_OF emits — new vocab being used correctly. Validator CLEAN.

The pattern that emerged: **soft-fallback whack-a-mole**. Plug CONTEMPORARY_WITH, KNOWS opens. Each new worker session is creative in finding broadest still-allowed canonical type. The prompt patches reduce severity but don't eliminate fundamental behavior.

## Key insight that emerged

You can't 100% lock down the schema via prompts alone. Each worker session re-derives understanding from its prompt reading + finds new soft-fallbacks. The asymptotic best we can do via prompts is "low single-digit error rate with bounded patterns we know how to detect." The **durable answer is to lock the audit, not the prompt**:

- Validator catches structural drift (schema violations)
- Cross-model audit catches semantic drift (wrong edge type for the actual relationship)
- **NEW: suspicious-edges worklist** flags schema-clean but semantically-suspicious patterns (KNOWS without "knew/known/learned of" in snippet, ATTENDS-with-non-event-target, FIGHTS_IN-with-non-event-target, KILLED_BY-with-non-person-target, confidence_tier-3 rows, CONTEMPORARY_WITH-with-character-target). These don't block emission but produce a worklist for later Opus review.

This is the answer Matt asked about ("have a parameter where it marks an edge not in the schema for Opus to review later"). Implementation deferred to the resume continue prompt — straightforward extension to the validator script.

## Cost + state at session end

- Spend this session: ~$37 across 11 Sonnet batches (1 canonical re-run + 10 bulk) + 1 Haiku smoke + Opus audit time
- Manifest: 21 done / 180 queued
- Per-batch quality holding at validator-CLEAN with 0-7% type-contract concerns (mostly bounded patterns)
- 4-5 vocab-gap candidates pending review (CROWNS_QUEEN_OF_LOVE_AND_BEAUTY recommended REJECT; rest already accepted Session-54)
- Two failed batches archived for record
- Schema patches all codified in canonical files (not just inline prompts)
- 7 new edge types added to vocab

## What's next

Continue prompt at `progress/continue-prompts/2026-05-16-stage4-bulk-resume.md`. Recommended: one terminal running `/loop 20m /worker-stage4` to grind the remaining 180 batches sequentially. Build the suspicious-edges worklist extension to the validator BEFORE resuming if possible (it's described in the continue prompt's Step 4). 5-7% baseline error is acceptable; post-cleanup via the worklist is the answer.

## Files written this session

- Patched: `.claude/agents/prose-edge-classifier.md` (output contract + evidence_kind + pass1_relationship shape + Common failure patterns + 7 new vocab type orientation)
- Patched: `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md` (validator step + failure-mode warnings)
- Patched: `reference/architecture.md` (11 new edge types across Session-54+55)
- Created: `scripts/wiki-pass2-validate-edge-jsonl.py`
- Created: `working/session-results/2026-05-15-stage4-batch-0012-quality-check.md`
- Created: `working/session-results/2026-05-15-stage4-edge-provenance-explained.md`
- Created: `working/session-results/2026-05-15-stage4-haiku-smoke-verdict.md`
- Created: `working/session-results/2026-05-16-stage4-bulk-run-checkpoint.md`
- Created: `working/session-results/2026-05-16-stage4-current-status-and-open-questions.md`
- Created: `progress/continue-prompts/2026-05-16-stage4-bulk-resume.md`
- Created: `~/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/feedback_drift_detection_mandatory.md` (+ MEMORY.md pointer)
- Archived: 2 failed batch-0012 attempts (Sonnet broken-schema + Haiku failed)
- Bulk output: 21 batches × ~30 prose-edges JSONL files = ~600+ output files under `working/wiki/pass2-buckets/<bucket>/prose-edges/`
- Manifest updates: batch-0012 through batch-0021 marked done with previous_run breadcrumbs where applicable
