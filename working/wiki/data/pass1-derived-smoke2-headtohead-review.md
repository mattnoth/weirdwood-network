# Stage 4 extra-tables re-smoke — Haiku vs Sonnet head-to-head (post-lockdown)

**Date:** 2026-05-25 (Session 70). **Same 200 rows** (seed=42 stratified, Events+Dialogue),
both models run with the gated-vocab + tier-guidance prompt. Reviewer: `prose-edge-reviewer`.

## Headline

| Metric | Haiku | Sonnet |
|---|---|---|
| Strict precision | **76%** | **78%** |
| Weak / Wrong | 16% / 8% | 13% / 8% |
| emit / reject | 137 / 63 | 138 / 62 |
| distinct edge types | 55 | 49 |
| tier spread (emits) | 24 t1 / 108 t2 / 5 t3 | 17 t1 / 104 t2 / 17 t3 |
| gated leakage | 2 (ADVISES) | 2 (MANIPULATES) |
| direction errors | ~5 | ~4 |
| type-disagreement wins (15 sampled) | 5 | **8** |
| cost / 200 rows | **$0.59** | $2.60 (4.4×) |

**Both improved ~10-16 pts from the pre-lockdown ~60-66% floor.** Neither cleared 80%.
The May-2026 Haiku failure modes (SERVES-on-everything 53%, vocab collapse to 9 types,
uniform tier) are GONE — this is a different regime, driven by the lockdown + pre-paired
candidates.

## Decision

Sonnet's 2-pt edge is **not worth 4.4× the cost** (reviewer + cheapest-viable-model policy
agree). Haiku's 4-pt gap to 80% is concentrated in two **mechanically-fixable** biases:
- **CONTEMPORARY_WITH** used for scene co-presence (should be events overlapping in time).
- **COMPANION_OF** used for shared scene/meal (should require explicit friendship language).
Plus low-rate category errors: CITED_BY for a dream, CONTRADICTS for an argument, ASSAULTS
for non-sexual violence, NURSED_BY for medical care.

**Path chosen (Matt, Decision C = enrich with Haiku):** add Rule-11 anti-pattern gates for
exactly these classes → re-smoke → run the ~$25-40 Haiku bulk if it clears ~80% → apply the
deterministic precision-filter → merge as graph/edges/ v2.

## Notes
- Shared error both models made: `lysa ASSAULTS sansa` (Moon Door scene is ATTACKS, not sexual).
- Sonnet's worst single error: `jaime PARENT_OF tommen` emitted from a quote where Jaime
  *denies* paternity (world-knowledge overrode evidence). Haiku correctly used STEP_PARENT_OF.
- Haiku over-emits on thin evidence; Sonnet's rejects are slightly more disciplined.
- Full reviewer transcript: agent run 2026-05-25 (not persisted; key numbers captured here).
