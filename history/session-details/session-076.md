---
session: 76
date: 2026-05-27
model: Opus 4.7 (orchestrator) + script-builder (Sonnet 4.6) ×2
track: Stage 4 — Events edge enrichment (events-enrichment continue prompt)
---

# Session 76 — Events enrichment launched on Sonnet; flush-fix + rate-limit wall; ASSAULTS mis-type caught

## Arc
`/continue events-enrichment`. Mid-session Matt said **"begin extraction enrichment batch workers, spawn one terminal with hour check with sonnet"** — which collided with his own S75 gate ("do NOT run the ~$270 Events bulk blind; precursors + re-smoke first"). I surfaced the tension and asked scope. Matt: **"run 1 [gated re-smoke first], but even if it's <75% continue, maybe update the prompt every couple batches after accuracy test"** + "I run bg workers + watch hourly." Then **"it's ok if there is some uncertainty just run it."** So the hard gate became a **monitored continuous-improvement loop**: run Events on Sonnet, accuracy-test each checkpoint, tune only on a systematic pattern, continue.

## Step 1 precursors (DONE, $0 deterministic)
- **Temporal scoping** — `scripts/stage4-edge-temporal-scope.py` + 58 tests (full suite 999 green). Every edge annotated with `(book_order, chapter_number)`. Re-ran the conflict audit temporally: **`--window chapter` → 31 of 32 flagged pairs are temporal arcs, 1 true same-window conflict** (`cersei↔tyrion` LOVES+HATES, recurs across ACOK chapters); `--window book` → 24/8. This is the "when does an edge apply" answer — the 32 conflicts are overwhelmingly *evolution over time*, not errors. Outputs: `working/wiki/data/edges-temporal-scoped.jsonl`, `graph-conflict-pairs-temporal.{md,jsonl}`. `edges.jsonl` untouched.
- **Conflict-pair mis-attribution review** — verified the agent's flagged suspects against source prose. `catelyn→tyrion` TRUSTS and `ghost↔tyrion` are **real arcs, KEEP** (the agent over-flagged them). The ONLY genuine mis-types: the **2 `cersei↔tyrion` LOVES edges** — hints literally read "sardonic affection" / "unexpected affection"; quotes are sarcasm + an accusation. Recommended drop (3,811→3,809); **awaiting Matt's OK, not applied.**
- v5 rules confirmed wired (`prompt_version=v5-precision-rules`, sha `d31ca56c4768`).

## Incident 1 — the buffering worker (caught at the 45-min mark)
First Sonnet worker launched fine (16,572 `pass1_events` candidates → 415 batches). At the 45-min checkpoint, **nothing was on disk** — `stage4-tail-classifier.py` accumulated all results in memory and only wrote at end-of-run (or rate-limit abort). Fatal for the iterative model: a tune-kill would lose everything, `--skip-existing` couldn't resume, and I couldn't accuracy-test mid-run. Killed it (~$3.45 / 12 batches sunk, memory-only).
**Fix** (script-builder): `--flush-every N` (default 5) + SIGINT/SIGTERM flush handler. **Hazard caught:** `write_output_rows` uses *append* mode, so a naive periodic full-buffer flush would duplicate every prior row — fix is cursor-based **delta** flush (append only rows since last flush). Rate-limit + end-of-run paths made cursor-safe. 1011 tests green. Relaunched with `--flush-every 5` → kill-to-tune now lossless + resumable.

## The Events run (Sonnet) — 5 clean checkpoints
75 batches (~3,000 rows) → **369 typed / 2,631 rejected / 240 classify_failed; 273 unique edges; $20.81.** Emit rate ~12% (the v5 "when in doubt REJECT" is deliberately conservative → high precision, low yield). **Strict precision held ~82-86% across all 5 checkpoints, zero drift.** The vocab lockdown worked even on the flagged-noisy types: `MANIPULATES` (cersei→sansa, target-unaware — correct), `ADVISES` (jon-arryn→robert Hand/counsel — correct), `LOVES` (dany→drogo, genuine), plus marquee specifics like `rhaegar CROWNS_QUEEN_OF_LOVE_AND_BEAUTY lyanna`. Reject sample was ~80-86% correct (fan-out, garbage slugs, single-moments); the one notable false-negative (`jaime→bran` window-push) was a **locator quote-anchor** miss, not a v5 flaw. **Only systematic emit error: `OWNS→BONDED_TO` for direwolves** (~4/21 at cp1) — deterministic merge-time fix (swords/horses correctly stay OWNS).

## Incident 2 — shared-account rate-limit wall + auto-resume miss
~05:40 the worker hit empty `claude -p` responses (batches 76-80), correctly detected the wall after 5 consecutive fails, flushed partial output, exited 42. **It then sat idle the rest of the night** — I'd launched the *bare* classifier (manual-relaunch plan) instead of an auto-resume `run-forever` wrapper. Matt woke to find usage clean (the ~5h rolling cap had reset). Lesson: a sleep-until-reset wrapper would have used the idle hours. **Quota note:** my `claude -p` worker runs on Matt's account, so the sustained Sonnet run very likely tripped the cap on his own interactive session — owned it. Empirical cap rhythm: **~75 batches per ~5-hour window.**

## The model decision (pending) — Sonnet vs Haiku for the remaining ~82%
Measured: Sonnet 4.0 min/batch → remaining 340 batches = ~23h pure compute, but **~2 days wall-clock** in ~5h cap-bursts that keep colliding with Matt's sessions. Haiku is faster + lighter on the cap (his standing bulk policy). Concern: earlier Haiku smokes were ~60-62% — **but those predate v5 + the candidate-gen fixes** (the lockdown built to make Haiku safe); Haiku is untested on the current setup. Matt asked for a **continue prompt to run a same-rows Haiku-vs-Sonnet comparison** → `progress/continue-prompts/2026-05-27-haiku-events-comparison.md` (`--smoke 600`, separate dir, diff verdicts + Haiku standalone precision; ≥~80% → switch remainder to Haiku). Not launched.

## Matt's catch — ASSAULTS is sexual-only
At endsession Matt asked "isn't ASSAULTS purely sexual assault?" — **correct** (architecture.md:233: ASSAULTS = sexual violence; ATTACKS = non-sexual physical). Audited the 32 core ASSAULTS edges: **~22 are non-sexual physical violence mis-typed → should be ATTACKS** (jaime→bran shove, cersei→eddard slap, haggo→mirri fist, joffrey→mycah, mandon→tyrion, cersei→blue-bard, victarion→ralf, duck→lorent, Sam hazing, etc.; a couple are wrong-pair too — shaggydog→luwin, grenn→jon). ~8-10 are genuinely sexual (drogo→dany, theon→kyra, rorge→arya, marillion→sansa, gregor→pia, kerwin crew, tywin→tysha). **Root cause:** the deterministic spine's phrase→type map collapsed struck/shoved/slapped/beat→ASSAULTS *before* the split was locked. The **v5 Events prompt obeys the rule** (emitted 0 ASSAULTS; routed physical → ATTACKS). Queued as a core-cleanup (fix the map + retype the ~22), gated on before/after sign-off. Task #7.

## Graph traversal — demonstrated working
`graph-query.py --neighbors jaime-lannister` → 117 outbound edges grouped by type with cited quotes; `--path arya→daenerys` → 0 direct/0 bridges (correct — they never meet; the core carries only relationship edges, so enrichment is what would bridge distant characters). S74 citation re-grounding makes the `file:line` quotes land correctly.

## Recommended core-cleanups now queued (all gated on Matt's before/after sign-off)
1. Drop 2 `cersei↔tyrion` LOVES mis-types (3,811→3,809).
2. Retype ~22 physical `ASSAULTS`→`ATTACKS` (+ fix spine type-map).
3. Merge-time: `OWNS→BONDED_TO` for direwolf/dragon targets (applies to Events output, not core).
