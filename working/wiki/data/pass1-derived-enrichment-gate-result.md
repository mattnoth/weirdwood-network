# Stage 4 enrichment gate — result + options for Matt

**Date:** 2026-05-25 (Session 70, overnight). **Verdict: NO-GO — bulk HELD, $0 spent.**
**v1 deliverable is already committed and safe** (`c3880e160`, 3,842 cited edges in `graph/edges/`).

## What happened

Decision C = "enrich with Haiku." Per the agreed ≥80% gate, I patched the typer (Rule 11:
CONTEMPORARY_WITH / COMPANION_OF / CITED_BY / CONTRADICTS gates) and re-smoked Haiku on the
same 200 rows, then had it reviewed. I did **not** launch the ~$60 bulk because the gate failed.

| Smoke | model | strict precision | note |
|---|---|---|---|
| smoke2 (pre-patch) | Haiku | 76% | baseline |
| smoke2 (pre-patch) | Sonnet | 78% | 4.4× cost; not worth 2 pts |
| **smoke3 (post-patch)** | **Haiku** | **~70%** | target biases → 0, but new drift |

Post-patch deterministic signal was great (CONTEMPORARY_WITH=0, COMPANION_OF=0, CITED_BY=0,
CONTRADICTS=0; emit 137→107, recall traded for precision). But precision did NOT clear 80%.

## Why it missed (the important part)

1. **Whack-a-mole drift:** eliminating the two biases made `RESPECTS` the new catch-all
   (~4-5 wrong/weak: Bronn/Tyrion from a brothel boast, Tom/Lady-Smallwood from a rebuke,
   Barristan/Robert from a musing). `OPPOSES` also over-applied (allies tagged as opponents).
2. **Structural candidate-noise ceiling (NOT prompt-fixable):** ~4 evidence-pairing errors
   where the cited quote doesn't name the two entities (`Littlefinger MANIPULATES Joffrey`
   should be →Catelyn; `Genna OPPOSES Faith` cited with a quote about a chin), a direction
   flip (`HEALS Bran→Luwin` backwards), wrong-target (`Cersei COURTS hand-of-the-king` title).
   These trace to the candidate generator pairing entities in a prose row + the locator
   attaching a nearby quote — **the same evidence-mis-location class already visible in the
   v1 core.** Prompt patches don't reach it.

**Honest read:** the extra-tables candidates appear to have a precision ceiling around
~70-80% because the pair+locate step is noisy. Each prompt iteration fixes some biases and
reveals others. The deterministic CORE (the spine, from Pass-1's explicit Relationships
Observed pairs) is the higher-quality layer — and it's already landed as v1.

## Over-rejection check (good news)

The patches did NOT over-reject: ~6-8% arguable false-rejects among 92 rejects (mostly
ADVISES/COMPANION_OF/REVEALS_TO swept up by the co-presence gate). Acceptable.

## Options for the morning

- **A — One more targeted iteration ($~1 + ~30min).** Add Rule-12 (RESPECTS requires explicit
  respect language) + a direction reminder, AND a DETERMINISTIC quote-relevance filter (drop
  any emit whose `evidence_quote` doesn't contain tokens of BOTH entities) + an ECHOES
  character→character type-contract drop. The quote-relevance filter is the reviewer's best
  idea — it's mechanical, and it would also clean the v1 CORE's mis-cited edges. Re-smoke;
  launch bulk only if ≥~80%. Risk: ceiling may cap it at ~75-80% regardless.
- **B — Run the bulk at ~70% + heavy post-filters + runtime verification (~$60).** Correct+weak
  was ~86%; the quote-relevance + type-contract filters lift effective precision; every edge
  carries `evidence_ref` so a runtime LLM re-verifies. Treat enrichment as noisy-but-cited
  bonus signal. Accepts a lower bar for breadth.
- **C — Ship core-only; defer enrichment ($0).** v1 (3,842 cited edges) stands as the
  deliverable. The extra-tables enrichment has a structural ceiling; revisit only when a real
  query exposes a gap. Cleanest; matches "get the graph traversable first, enrich later."

**My recommendation:** **A as a cheap one-shot** (the quote-relevance filter is worth building
regardless — it improves v1 too); **fall back to C** if A doesn't clear ~78%. **B** only if you
want maximum recall and accept the noise. The deterministic quote-relevance filter is the
single highest-value next build either way.

## Ready infrastructure (built tonight, uncommitted, tested+green)

- `scripts/stage4-tail-bulk-forever.sh` — rate-limit-surviving overnight loop wrapper.
- `stage4-tail-classifier.py`: `--abort-after-consecutive-failures` (clean exit code 42 on
  rate-limit wall), `--skip-existing`/`--output-dir` hardened, Rule 11 gates. 137 tests green.
- Launch (if you choose B, or A clears): `nohup bash scripts/stage4-tail-bulk-forever.sh >> working/wiki/data/smoke2-logs/enrich-haiku-forever.log 2>&1 &`

Smokes (gitignored staging): `_smoke2-haiku/`, `_smoke2-sonnet/`, `_smoke3-haiku/`.
Reviews: `pass1-derived-smoke2-headtohead-review.md` + this file.



  ━━━ HANDOFF — SINGLE-SESSION TASK ━━━
  Model: Opus 4.7 — the A/B/C call + reviewer reading is judgment; Sonnet for the $0 builds.
  In a fresh Claude Code session, type:
  /continue stage4-enrichment-decision
  Read first: working/wiki/data/pass1-derived-enrichment-gate-result.md (full options + numbers).
  TL;DR: v1 is landed/committed and stands regardless. Decide A (one-shot: quote-relevance filter + RESPECTS gate → re-smoke → bulk if ≥~78%) / B (run bulk at ~70% + filters) / C (ship core-only). Rec: A → fall back to C.
  Open questions for Matt: none — the decision is the task.
  DO NOT: launch the ~$60 bulk before a re-smoke clears ≥~78%; type without --output-dir; mutate committed graph/edges/edges.jsonl without showing before/after; run /endsession without permission.
  ━━━
  