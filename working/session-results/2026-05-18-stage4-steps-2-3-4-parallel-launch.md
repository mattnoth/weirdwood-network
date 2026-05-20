# Stage 4 Haiku-Cutover STEPS 2/3/4 — Parallel Launch

**Launched:** 2026-05-18 (Session 58)
**Launched by:** Opus 4.7 orchestrator
**Worker model:** Sonnet 4.6 (all three agents)
**Agent type:** script-builder
**Run mode:** background, in parallel

---

## Three parallel agents launched

### STEP 2 — `[LINK]` substitution sub
**Goal:** when the prose-edge-classifier emits `[LINK]` as a placeholder target (because the source prose says "his brother" / "her father" without naming who), build a post-processing sub that resolves the placeholder against context.

**Investigation surface:**
- Find current `[LINK]` mentions in `working/wiki/pass2-buckets/*/prose-edges/*.edges.jsonl` (21 batches completed) — how many open, what shapes
- Determine where substitution should happen (post-processing pass on emitted JSONL? Modification to candidate generator? Sub-call from classifier?)
- Reference: `scripts/wiki-pass2-build-edge-candidates.py` for candidate generation context

### STEP 3 — Validator extension
**Goal:** extend `scripts/wiki-pass2-validate-edge-jsonl.py` with three new validation classes:
1. **Type contracts** — per-edge-type target-type constraints (FIGHTS_IN → event.battle, WIELDS → object.artifact, KILLED_WITH → object.weapon, etc.). Source: `.claude/agents/prose-edge-classifier.md` lines ~280-300.
2. **Qualifier enums** — load `reference/edge-qualifier-vocab.md`. Tier-1 reject missing/out-of-enum; Tier-2 reject out-of-enum but accept omission; Tier-3 reject any non-empty qualifier.
3. **Notes-rejection** — any edge with `notes` field → reject (field deleted from schema as of Session 57).

### STEP 4 — Suspicious-edges flagger
**Goal:** check `scripts/wiki-pass2-flag-suspicious-edges.py` (already exists) — extend with the worklist of patterns from Session 54:
- `KNOWS`-as-fallback (no explicit "knew" language)
- `ATTENDS` with non-event target
- `FIGHTS_IN` with non-event target
- `KILLED_BY` with non-person source
- `tier-3` confidence with weak evidence
- `CONTEMPORARY_WITH` on character pairs

Output: `working/wiki/data/stage4-suspicious-edges.jsonl` for later Opus review.

---

## Hard DO-NOTs (all three agents)

- Do NOT re-classify or normalize any prose-edges JSONL under `working/wiki/pass2-buckets/*/prose-edges/`.
- Do NOT modify `reference/edge-qualifier-vocab.md` (just written, locked).
- Do NOT modify `.claude/agents/prose-edge-classifier.md` schema (locked as of Session 58).
- Do NOT run /endsession.
- Do NOT modify each other's scripts (STEPS 3 and 4 touch different files; STEP 2 may touch the candidate generator).

---

## Expected outputs

- STEP 2: a script or design doc + a sample of resolved-LINK output
- STEP 3: extended validator + self-test against archived broken batch-0012 (as the original validator did)
- STEP 4: extended flagger + initial worklist JSONL
- Three session-results docs (one per step)

## Verification post-completion (orchestrator next steps)

1. STEP 2: confirm `[LINK]` resolution sub exists and has been tested against real prose-edges output.
2. STEP 3: confirm validator now rejects (a) missing Tier-1 qualifier, (b) out-of-enum Tier-2 qualifier, (c) any Tier-3 qualifier, (d) any `notes` field, (e) target-type contract violations.
3. STEP 4: confirm flagger emits the 6 pattern classes and the worklist JSONL is non-empty (it should find real patterns in the 21 completed batches).
