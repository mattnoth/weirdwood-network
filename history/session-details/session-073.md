---
session: 73
date: 2026-05-26
model: opus
title: Cleanup-and-reorg triage — most of it dissolved; worktrees removed, a CLAUDE.md #9 finding, scripts kept
---

# Session 73 — Cleanup-and-reorg triage

**Purpose:** `/continue cleanup-and-reorg` — assess and execute the repo-hygiene track (scripts/ + working/wiki/ reorg, leftover worktrees, tracked scratch files). Matt's opening question was simply "how are we sitting."

This was a **decision/triage session**, not execution. The headline: the "reorg" largely dissolved under inspection, and Matt overruled the one cleanup I proposed. What remained worth doing was small.

## What I found

**Scripts "reorg" is low-value / high-risk.** 126 entries in `scripts/`. The themes are obvious (stage4 48, wiki-pass2 41, classify 8, build 5, …), but the import-coupling is real and worse than "scripts import scripts":
- `tests/_helpers.py:load_script(filename)` loads scripts by **flat filename** via importlib (~30 call-sites across 15 test files). Any move breaks tests unless the helper searches recursively (a 1-line fix) or every call-site is updated.
- `stage4-*` and `wiki-pass2-*` are **mutually entangled** — each loads the other's edge validator/normalizer via hardcoded `_REPO/"scripts"/"<name>"` absolute paths (4 bridges). These break on move regardless of destination subdir.
- Net: folderizing the live cluster is cosmetic, carries real breakage risk, and needs Matt's layout sign-off. → **defer indefinitely.**

**The "27 dead prose-edge scripts" episode (the substance of the session).** I proposed archiving 27 `classify-*` / `stage4-classify-*` / `stage4-haiku-classify-*` / comention scripts to `scripts/archive/`, justified initially as "no importer, no test." Matt correctly challenged that — "no importer/no test" is a weak liveness signal (standalone CLI tools have neither). I re-grounded the claim on **supersession**: docstrings confirm they implement the pre-S65 wiki-**comention** edge approach (read `prose-edge-candidates-enriched` / hardcoded per-chapter relationship dicts), plus one-off per-house hand-built classifiers (`classify-ramsay-snow`, `temp-classify-glovers`, …) and the superseded Haiku-bulk apparatus. None are referenced by any wrapper/runbook/continue-prompt/pipeline. So: not dead/broken — **superseded**.
- **Matt's decision: KEEP them.** The only driver for archiving was the "cleanup" framing, and that's not reason enough. The wiki-comention approach is a plausible **future recall lever** (the S68 recall-sample found ~9% of real relationships are prose-only, not in our Pass 1 tables). Inert scripts cost nothing sitting flat. **Recommendation withdrawn.**

**CLAUDE.md #9 finding — the continue prompt was wrong about `pass2-buckets/`.** It claimed "large, gitignored staging." Reality: `working/wiki/pass2-buckets/` is **NOT gitignored** — **23,081 tracked files**, including **7,180 stale `skeleton/*.node.md`** (~28 MB) that S72 verified are already promoted into `graph/nodes/` (redundant). Only `pass1-derived/` *within* it is gitignored. Untracking the stale skeletons is a genuine repo-hygiene lever, but it's **entangled** — ~24 `wiki-pass2-*` promotion scripts read `skeleton/` dirs — so it's a deliberate decision, not a side-effect of a tidy. → **deferred to its own focused session.**

**Edge-state clarification (Matt's "~4k/20k promoted?" mental model — confirmed, one number fixed).** Promoted/frozen: `graph/edges/edges.jsonl` = **3,811** (v1.3). Core spine candidates = **5,886** Pass-1 Relationship pairs (→ the 3,811 after typing/dedup/filter). Un-promoted pool = **27,305** rows in `_extra-tables` staging (Dialogue/Events/Info/Food/Hospitality mined from the *other* Pass 1 tables) — the "~20k" ≈ the Events table, the bulk, held at the ~$270 / ≥80%-precision spend gate (smokes came in ~62–66%). Matt confirmed his strategy memory is correct: deterministic spine to minimize LLM (Haiku) work + a validation stack (type-contract validator, quote-relevance filter, endpoint/slug gates, drift-detection) + prompt hardening (tail-classifier prompt v4).

**Pass 1 = all Opus.** Matt confirmed all 5 books' mechanical extraction ran on Opus. Not derivable from extraction files (no model stamp). Saved to memory (`project_pass1_all_opus`).

## What I executed

- Removed both leftover worktrees (`.claude/worktrees/{admiring-benz-fa26f8, mystifying-burnell-56ee9c}`, both clean) + deleted the 2 `claude/*` branches (both fully merged into main → reversible). `.claude/worktrees/` now empty.
- Fixed the stale "gitignored" claim in `progress/continue-prompts/2026-05-26-cleanup-and-reorg.md` (corrected to the tracked-files reality + deferred skeleton-untrack note).
- Scratch files: **untouched**, per Matt's explicit instruction ("ignore scratch files").
- Memory: `project_pass1_all_opus` + MEMORY.md index line.

## Next move (recommended)

The edge layer (3,811 cited, ~78%, traversable) is in good shape. To grow it (~7× more candidate edges sitting un-mined), the blocker is precision below Matt's 80% gate. S71's diagnosis pinned the **root cause: locator `hint_raw`↔`evidence_quote` decoupling** (`stage4-pass1-evidence-locator.py` attaches the nearest both-named window, not the passage the hint came from). The clear next move is the **$0 deterministic locator quote-grounding fix** → cheap re-smoke (~$1.4) → if it clears ≥75% across two fresh samples, enrichment unlocks; else ship core-only. Continue: `progress/continue-prompts/2026-05-25-stage4-locator-grounding.md` (note: it says edges = 3,842; that's stale — it's 3,811 v1.3 after S72). Downstream framework: `2026-05-25-stage4-enrichment-decision.md` (A/B/C).
