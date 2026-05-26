# Stage 4 — locator quote-grounding fix (the enrichment lever)

> **Recommended model:** **Sonnet 4.6** for the $0 deterministic locator build + the re-smoke ops.
> **Opus 4.7** only for a fresh-eyes review of the result. Never Opus for per-row work.
>
> **Trust `worklog.md` over this prompt if they disagree** (CLAUDE.md #9). Authoritative:
> worklog Session 71 + the `graph/edges/` Current-State line.

## State (end of Session 71, 2026-05-25)

- **`graph/edges/edges.jsonl` v1 = 3,842 cited deterministic edges. STANDS.** Committed (`c3880e160`). Not in question.
- **Events+Dialogue enrichment = NOT-YET.** Two fresh out-of-sample smokes: smoke5 (seed-4242) **72.5% raw**, smoke6 (seed-7777) **61.9% raw**. The deterministic type-contract post-filter did NOT generalize (fired ~0 on smoke6 → the earlier "~80-91%" was overfit to smoke5). Model-caused false-reject ~20%. **Do NOT run the ~$75 production run at this quality.**
- **Root cause (proven by the smoke6 reviewer): locator `hint_raw`↔`evidence_quote` DECOUPLING.** The Pass-1 relationship is stated in `hint_raw`, but `stage4-pass1-evidence-locator.py` (locator v2) attaches the nearest *both-named* window — which is often NOT the passage the hint came from. This single bug causes BOTH failure modes: wrong-emits (model trusts the hint despite a mismatched quote) AND false-rejects (model correctly rejects a TRUE edge because its attached quote is unrelated — e.g. `bowen-marsh→jon KILLS`, `lysa→sansa REVEALS_TO`).

## The task — deterministic locator quote-grounding fix ($0, no LLM)

Make `evidence_quote` carry the sentence the hint was actually extracted from, not a nearby both-named window. In `scripts/stage4-pass1-evidence-locator.py`:

1. **If `hint_raw` contains a quoted/verbatim fragment** (text in quotes, or a long literal substring), locate THAT exact text in the chapter (`sources/chapters/<book>/<chapter>.md`) and use it as `evidence_quote`. The hint frequently already carries the right quote — we are currently discarding it and re-searching. **Prioritize the hint's own quoted content.**
2. **Else fuzzy-match** the hint's action verb + key entity tokens against the chapter to find the passage the hint summarizes; take the quote *there* (expand to include both entity names only if they're adjacent).
3. **Only fall back** to the current both-named-window search if neither (1) nor (2) resolves.
4. **If the hint's true location does NOT contain both entities**, set `locate_quality` low (e.g. `hint-anchored-one-named`) and DO NOT fabricate a both-named quote from elsewhere — a mismatched quote is worse than an honest weak one. Downstream can flag/reject on it.
5. Add a field recording which path produced the quote (`quote_source` ∈ `hint-verbatim` / `hint-fuzzy` / `both-named-window` / `nearest-fallback`) so the next smoke can measure where the quote came from.

**Tractability:** HIGH for Dialogue (hints are often verbatim lines — and Dialogue was the weakest bucket at 46% in smoke6, so most to gain), MEDIUM for Events (paraphrased hints). Tests required.

## Validation (the gate)

- Re-locate a fresh out-of-sample sample with the fixed locator (use `stage4-fresh-relocate-sample.py --seed <new> --kinds pass1_events,pass1_dialogue`), re-smoke with the v4 prompt (`stage4-tail-classifier.py --model claude-haiku-4-5 --input-dir <fresh> --output-dir <scratch>` — smoke-test is pre-authorized; ~$1.4), then `prose-edge-reviewer` for strict precision + false-reject rate.
- **GO on the ~$75 production run ONLY if precision ≥~75% AND stable across TWO fresh samples** (the 72% vs 62% variance between smoke5/smoke6 is itself a not-ready signal — one good sample is not enough).
- Production plan if GO: book-sharded (AGOT-Events first, prioritized rows), output to scratch, `prose-edge-reviewer` per shard, formalize as v2 layered on v1 — never overwrite the core.

## DO NOT
- Run the ~$75 production enrichment before a re-smoke clears ≥~75% across 2 fresh samples (needs Matt's OK — it's a real spend).
- Apply the v1.1 refinement candidate (`_v1-refine/edges-v1.1-candidate.jsonl`: −10 schema errors + soft-flags) to committed `graph/edges/edges.jsonl` without showing Matt the before/after (it's the landed deliverable).
- Type/smoke without `--output-dir` to a scratch dir (never canonical `_tail-typed/`).
- Re-introduce the QR filter as a HARD gate (~50% false-drop) — it stays a SOFT flag.
- Delete anything. Run `/endsession` without explicit permission.

## Pointers
- Honest verdict + the overfitting finding: `working/wiki/data/readiness-review-fresh.md`
- Prompt reviews (converged): `working/wiki/data/prompt-review-opus-1.md` + `-2.md`
- Layer inventory (current vs superseded vs proposal): `working/wiki/data/pass1-derived-staging-manifest.md`
- Scripts (all UNCOMMITTED — Matt checkpoints): `stage4-quote-relevance-filter.py`, `stage4-type-contract-validator.py` (9 contracts, keep/drop/flip/flag), `stage4-pass1-evidence-locator.py` (locator v2 — the file to fix), `stage4-fresh-relocate-sample.py`, `stage4-refine-v1-edges.py`, modified `stage4-tail-classifier.py` (prompt v4 + prompt_sha stamping).
- Smoke outputs (gitignored scratch): `_smoke4/5/6-haiku/`, `_fresh-relocate-4242/`, `_fresh-relocate-7777/`.
