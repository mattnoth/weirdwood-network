# Vocab Completeness Audit — Launch Info

**Launched:** 2026-05-19 (Session 58 continued from 2026-05-18)
**Launched by:** Opus 4.7 orchestrator
**Worker model:** Opus 4.7
**Agent type:** general-purpose
**Run mode:** background

---

## Goal

Audit the locked edge vocabulary (149 types, Session 56) and locked qualifier vocab (17 types × enums, Sessions 57/58) for **completeness** against the Pass 1 corpus. Surface:

1. **Edge-vocabulary gaps** — relationship phrases in Pass 1 `## Relationships Observed` (and other relevant tables) that don't map cleanly to any of the 149 locked edge types. Output: proposed new edge types with rationale + corpus evidence.

2. **Sub-qualifier candidates** — for each Tier-1 and Tier-2 enum value, identify natural sub-typologies the corpus distinguishes that we collapsed into a single bucket. E.g., `SWORN_TO=former` may have natural sub-types `by_marriage` / `by_death` / `by_desertion` / `annulled`.

This is the final lockdown audit before STEP 5 Haiku smoke. Per Matt's session-close caveat in Session 57: "I feel like there may be more qualifiers that come up as we are locking this stuff down."

---

## Method

The Session 57 corpus survey was **count-driven** — top phrases by volume. This audit is **coverage-driven** — flag the long tail of phrases that don't map, and flag enum values with internal sub-typology.

---

## Output

- `working/qualifier-vocab/audit-completeness-2026-05-19.md` — primary deliverable
  - Section A: Edge vocab gaps (proposed new edge types)
  - Section B: Sub-qualifier candidates (proposed second-axis dimensions)
  - Section C: Confirmed-complete (edges + enums with no gaps surfaced — for our records that the audit checked them)

- `working/session-results/2026-05-19-vocab-completeness-audit.md` — session-results doc with brief findings summary

## Hard DO-NOTs

- Do NOT modify `reference/edge-qualifier-vocab.md`, `reference/architecture.md`, or `working/qualifier-vocab/decisions.md`. Produce candidates only — Matt verdicts each before encoding.
- Do NOT modify `.claude/agents/prose-edge-classifier.md`.
- Do NOT modify validator or any prose-edges JSONL.
- Do NOT run /endsession.

## Expected outputs

- Audit doc with both gap lists
- Brief summary (under 400 words) reporting: how many phrases surveyed total, how many flagged unmapped, how many sub-qualifier candidates surfaced, top 3 strongest recommendations.

## Expected cost / duration

~$5-15 Opus. ~20-40 min. Corpus read of 344 Pass 1 files filtered to the relevant tables (~250K input tokens) + reasoning output (~20K).

## Verification post-completion

1. Read audit doc top-to-bottom.
2. For each proposed new edge type: spot-check the corpus evidence — does the phrase actually warrant a new edge type, or could it fit an existing one?
3. For each sub-qualifier candidate: verdict whether to encode (adds vocab complexity) vs. accept the collapse (keeps the lockdown lean).
4. Decisions land in a new section appended to `working/qualifier-vocab/decisions.md` OR in a fresh `decisions-round-2.md`.
