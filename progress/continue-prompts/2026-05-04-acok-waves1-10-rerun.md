---
title: ACOK remaining-waves re-run (BLOCKED on chain/race bug fix)
date: 2026-05-04
model: opus (extraction) / sonnet (orchestrator)
focus: execution
blocked_by: progress/continue-prompts/2026-05-04-urgent-fix-chain-and-race-bug.md
---

# ACOK Re-Run: Remaining V2 Chapters → V3 Schema

> **⚠️ BLOCKED — DO NOT LAUNCH YET.** The auto-advance feature (`--chain`) has a terminal-explosion bug + a race condition on parallel extraction. Both must be fixed before any further launches. See the urgent prompt linked above.

---

## Status as of Session 33 end

**Re-run was attempted in Session 33 with `weirwood acok 2 1 claude-opus-4-6 --delay 2h --chain`. Aborted mid-run when the chain bug + race fired** — 5 simultaneous tabs ended up running, racing on overlapping waves, overwriting each other's outputs. See `working/session-details/session-033.md`.

**Current state of `extractions/mechanical/acok/`:**
- ✅ Waves 1–4 (chapters 1–20: arya-01..05, arya-06..10, bran-01..05, bran-06..07 + catelyn-01..03) — re-extracted to v3 in Session 33 (some duplicated, but all valid v3).
- ❌ Waves 5–10 (chapters 21–50) — STILL v2 in `extractions/archives/acok-v2-original-2026-05-04/`.
- ✅ Waves 11–14 (chapters 51–70) — already v3 from Session 30.

**30 chapters remaining** to convert from v2 → v3.

---

## Prerequisite — fix the chain + race bugs first

Before launching anything: complete `progress/continue-prompts/2026-05-04-urgent-fix-chain-and-race-bug.md`.

That prompt:
1. Removes (or single-masters) the `--chain` re-launch behavior.
2. Adds per-chapter atomic claim files to prevent parallel-write collisions.
3. Smoke-tests the fix before re-launch.

After the fix lands, this prompt becomes safe to execute.

---

## Launch (post-fix)

**Recommended command** (no `--chain`, no `--delay`):

```bash
weirwood acok 2 3 claude-opus-4-6
# 2 terminals × 3 waves each = 30 chapters in one batch
# ~3-4 hrs wall-clock
# When done, run again if any waves remain
```

**Pre-launch sanity check:**

```bash
weirwood acok
# Expect: 40/70 done. Waves 5..10 listed as missing.
# If it shows waves 1..4 missing, STOP — Session 33's re-extractions didn't land.
```

**Why no chain?** Even with the fix, chain adds complexity for marginal benefit. Manual re-launch every ~3 hours is fine for 30 remaining chapters. If chain returns, it should be a single coordinator process — not every terminal launching more.

**Why Opus?** AGOT v3 used Opus; ACOK waves 11–14 used Opus; AFFC used Opus. Consistency matters for downstream comparison until/unless a Sonnet smoke-test proves equivalent v3 quality (a separate TODO).

---

## Acceptance criteria

- [ ] Both bugs in extract.sh fixed and smoke-tested (gated by urgent prompt).
- [ ] `weirwood acok` shows 70/70 complete.
- [ ] Sample 5 random newly-extracted chapters → all have 12 Raw Entity List headers + all v3 sections.
- [ ] No `_FAILED` markers / truncated files / zero-byte outputs.
- [ ] `working/extraction-stats/extraction-stats-acok-pass1-v3.csv` has stats rows for all 70 chapters.
- [ ] Worklog Session N entry updated with cost, duration, any anomalies.
- [ ] This continue prompt deleted; todos.md `→ continue:` line removed.

---

## What's next after ACOK 70/70

1. **ASOS** (0/82) and **ADWD** (0/73) — single-pass v3 each. Continue prompt: `progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md`. **Open question:** can Sonnet 4.6 produce equivalent v3 output? Worth a 1-wave smoke test before committing Opus to 155 more chapters. See todos.md "Pass 1 model-fit smoke test."
2. **Stage 4** prose-edge-classifier — once all 344 chapters land. Continue prompt: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`.

---

## Hard rules

- **DO NOT** launch this until `2026-05-04-urgent-fix-chain-and-race-bug.md` is fully complete.
- **DO NOT** use `--chain` even after the fix unless the fix specifically addresses both bugs and is smoke-tested.
- **DO NOT** delete the v2 archive at `extractions/archives/acok-v2-original-2026-05-04/`. Archives are permanent.
- **DO NOT** run `/endsession` without explicit Matt permission.
