# Stage 4 — enrichment decision (A/B/C) + commit the held infra

> **Recommended model:** **Opus 4.7** for the A/B/C decision + reviewer reading. **Sonnet 4.6**
> for the $0 builds (quote-relevance filter, RESPECTS gate). Never Opus for per-row work.
>
> **Trust `worklog.md` over this prompt if they disagree** (CLAUDE.md #9). Authoritative:
> worklog Session 70 + the `graph/edges/` Current-State line.

## State (end of Session 70, 2026-05-25)

- **`graph/edges/` v1 is LANDED + committed** (`c3880e160`): `graph/edges/edges.jsonl` =
  **3,842 cited Pass-1-derived edges**, ~78% precision, every edge carries `evidence_ref`.
  The graph is traversable. This deliverable stands regardless of what you decide below.
- **The Haiku Events+Dialogue enrichment bulk was HELD** — re-smoke gate failed (post-patch
  Haiku ~70% strict, <80%). $0 spent. Decision needed.
- **Uncommitted (tested, green):** `stage4-tail-bulk-forever.sh` + the `stage4-tail-classifier.py`
  hardening (`--abort-after-consecutive-failures`, `--skip-existing`/`--output-dir` fix, Rule 11).
  Commit these with whichever path you pick.

## The decision — READ FIRST: `working/wiki/data/pass1-derived-enrichment-gate-result.md`

That doc has the full numbers, the failure analysis (whack-a-mole drift + structural
candidate-noise ceiling), and the three options A / B / C with my recommendation. Don't
duplicate it here — read it, then:

- **A (rec, one-shot):** Sonnet builds (i) a deterministic **quote-relevance filter** (drop any
  emit whose `evidence_quote` doesn't name BOTH entities — also clean the landed v1 core with
  it), (ii) a **RESPECTS gate** + direction reminder in the prompt, (iii) ECHOES char→char
  type-contract drop. Re-smoke Haiku (same 200, seed=42). Launch the ~$60 bulk via
  `scripts/stage4-tail-bulk-forever.sh` ONLY if it clears ~78-80%. Else fall back to **C**.
- **B:** run the bulk at ~70% now + heavy post-filters + rely on runtime-LLM re-verify (~$60).
- **C:** ship core-only (v1 stands); defer enrichment until a query exposes a gap. $0.

## DO NOT
- Launch the ~$60 bulk before a re-smoke confirms ≥~78% (it's an extraction — needs Matt's OK).
- Run any typing pass without `--output-dir` to a scratch dir (never canonical `_tail-typed/`).
- Apply the quote-relevance filter to the committed `graph/edges/edges.jsonl` without showing
  Matt the before/after + a sample (it's the landed deliverable).
- Re-type / re-smoke without the Rule-11 gates (already in the prompt).
- Run `/endsession` without explicit permission.

## Pointers
- Gate result + options: `working/wiki/data/pass1-derived-enrichment-gate-result.md`
- Head-to-head review: `working/wiki/data/pass1-derived-smoke2-headtohead-review.md`
- Deliverable schema/caveats: `graph/edges/README.md`
- Formalize + filter: `scripts/stage4-formalize-edges.py` (has `--precision-filter`)
- Overnight wrapper: `scripts/stage4-tail-bulk-forever.sh`
