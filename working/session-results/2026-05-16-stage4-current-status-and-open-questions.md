---
session_date: 2026-05-16
session_focus: Stage 4 bulk run — current status + open questions for Matt
status: PAUSED — 18 batches done, awaiting decisions before resuming
verdict: YELLOW — quality good in most cases, two recurring patterns + one regression need resolution before next 183 batches
model_used: claude-opus-4-7[1m] (orchestrator/auditor); claude-sonnet-4-6 (workers)
companion_docs:
  - 2026-05-16-stage4-bulk-run-checkpoint.md (full per-batch detail)
  - 2026-05-15-stage4-batch-0012-quality-check.md
  - 2026-05-15-stage4-haiku-smoke-verdict.md
  - 2026-05-15-stage4-edge-provenance-explained.md
---

# Stage 4 — Current Status + Open Questions

## Where we are in one paragraph

18 batches done out of 201 total (9%). Manifest: 18 done, 183 queued. Spend so far ~$27. All batches validator-CLEAN. Type discipline holding at 0-7% (most errors are graph-typing mismatches like `kingsmoot` typed as `concept.culture`, not classifier errors). KILLED_BY direction 25/27 correct across all batches (vs Haiku's 55% reversal rate). Two prompt patches landed mid-session (no CONTEMPORARY_WITH-fallback, no reverse-direction vocab gaps) — they held for 3 batches then regressed in batch-0018 (the Frey buckets — densest kinship in ASOIAF). Stopped firing after batch-0018 to ask you about how to proceed.

## What you need to decide

### Decision 1 — Vocab gap acceptances (6 items)

Reviewed and recommended:

| Proposed type | Reason it surfaced | Recommend | Notes |
|---|---|---|---|
| `COUSIN_OF` | Frey/Lannister kinship density; surfaced in batch-0018 | **ACCEPT** | One-hop shortcut, same reasoning as UNCLE_OF/NEPHEW_OF. Reverse-of itself (symmetric). |
| `MILK_BROTHER_OF` | Edric Dayne and Jon Snow; recurring Westerosi kinship | **ACCEPT** | Real cultural category; symmetric. |
| `NURSED_BY` / `WET_NURSE_OF` | Wet-nurse relationship; distinct from PARENT_OF | **ACCEPT** | Asymmetric (NURSED_BY on child, WET_NURSE_OF on nurse — both emitted). |
| `KNIGHTED_BY` / `BESTOWS_KNIGHTHOOD_ON` | Granting knighthood; recurring | **ACCEPT** | Distinct from TUTORS (skill) and APPOINTS (office). |
| `DEPICTED_IN` | Character is subject of in-world text/song (Danny Flint → "Brave Danny Flint" song) | **ACCEPT** | Captures the in-universe folklore/legacy layer ASOIAF is rich in. Distinct from WRITTEN_BY (author → work). |
| `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` | Tourney-specific | **REJECT** | Too narrow; absorb into ATTENDS with qualifier, or capture as a TRIBUTES_TO / HONORS gap if recurring. |

Accepting 5 of 6 brings the vocabulary from ~125 → ~130 types.

### Decision 2 — Approach to next 183 batches

Three paths. Recommended is A.

**A. Data-driven schema lockdown then resume (Recommended).**
- Spend one session analyzing the 18 batches' actual output
- Build empirical reports: type-usage histogram, contract-violation patterns by edge type, vocab-gap density, reject-reason frequency
- Use that to: tighten the prompt (specific examples for the top-5 violation patterns), accept the vocab gaps above, possibly RETIRE rarely-used canonical types that nobody emits in practice
- Then resume bulk firing with the tightened prompt + COUSIN_OF available
- Cost: ~$5-10 for the analysis session (mostly Python, some Opus reasoning), saves much more in cleaner downstream output
- This is what "lock down the schema and only surface truly weird ones" looks like in practice

**B. Strengthen prompt now without analysis, resume immediately.**
- Add COUSIN_OF + the 4 accepted vocab types to architecture.md
- Add explicit "never CONTEMPORARY_WITH for character pairs" top-level rule
- Add concrete examples ("attended the wedding of A and B" → ATTENDS wedding-event)
- Resume bulk
- Faster but less informed; we'd be guessing at patches rather than measuring

**C. Accept current quality, resume immediately with post-clean later.**
- Don't patch
- Run all 183 remaining batches at current quality (~5-7% real type-contract issues, occasional CONTEMPORARY_WITH-fallback regressions)
- Post-process: write a cleanup script that retracts wrong-fit CONTEMPORARY_WITH edges in dense-kinship buckets, fixes FIGHTS_IN-person and ATTENDS-person patterns, etc.
- Cheapest in upfront cost; risks compounding errors that are harder to disentangle later

### Decision 3 — batch-0018 outcome

The 132 emits include ~18 known-wrong CONTEMPORARY_WITH edges. Options:
- **Keep as-is.** Run a post-cleanup script later to retract the wrong CONTEMPORARY_WITHs in Frey buckets. (Cheapest.)
- **Quarantine + re-run after prompt strengthening.** Archive the output, reset batch-0018 to queued, re-run after Decision 2's prompt changes. (Cost: $3.42 + 25 min.)
- **Surgical correction.** Keep the 110+ good emits, manually mark the ~18 wrong CONTEMPORARY_WITHs as `_retracted` or move them to a side file for review. (Medium effort.)

Recommend: **Quarantine + re-run** if we go with Path A or B (so it benefits from the new prompt). **Keep as-is** if Path C.

### Decision 4 — Bucket density triage (optional, for Path A)

Some buckets are dramatically denser than others. Frey has ~80+ characters with mutual cross-references; small houses (Crayne, Cox) have 1-3. Worker error rate appears to scale with bucket density. We could:
- Build a quick script to compute candidates-per-bucket and rank
- For top-decile dense buckets (probably Frey, Lannister, Targaryen, Stark, Tyrell, Bolton, Tully), run them LAST after vocabulary is fully expanded
- Or process them with smaller chunks (split one bucket across multiple batches)

Not required, but would smooth the trajectory.

## Quick facts to anchor the conversation

- **Vocab usage so far:** ~30-40 of the 125 canonical types actually emitted in 18 batches (need to count exactly). Most-used: SERVES, FIGHTS_IN, ALLIES_WITH, TRAVELS_TO, ATTENDS, OPPOSES, LOCATED_AT, SIBLING_OF, KILLED_BY. Many types (FEARS, MOURNS, RESURRECTS, CURSES, WARGS_INTO, FORESHADOWS, etc.) have ZERO emits yet — they're concentrated in main-character buckets which haven't run yet.
- **Cross-identity escalations:** 4 total across 18 batches (tom-costayne pair x2 + 1 in batch-0015 + 1 in batch-0016). All well-formed. cross-identity-detector agent can process these when batches finish.
- **Vocab-gap questions filed:** ~10-15 across the session, mostly handled (3 reverse-direction noise + 5 legit pending your decision + 1 Haiku-era pre-patch).
- **Two failed historical attempts on batch-0012:** archived to `_archive/batch-0012-sonnet-pre-schema-fix-2026-05-15/` and `_archive/batch-0012-haiku-failed-2026-05-15/` — preserved for the comparison record.
- **What the validator does well:** schema enforcement, snippet-not-section-header, edge-type-in-vocab, deprecated-LOCATED_IN.
- **What the validator can't catch:** semantic correctness (wrong edge_type for the actual relationship), direction reversal on edges other than KILLED_BY, type-contract violations between valid canonical types. That's what the cross-model audit caught.

## Recommended next move

Go with Path A. Spend one focused session (probably ~3 hours of Opus + Python analysis) doing the data-driven schema lockdown. Output: refined prompt + accepted vocab + bucket-density score + maybe a few retired-canonical-types. Then resume bulk firing with a much stronger, empirically-grounded prompt. The 18 batches we already have are the calibration data — let's use them.

Continue prompt for that session: `progress/continue-prompts/2026-05-16-stage4-schema-lockdown.md`.
