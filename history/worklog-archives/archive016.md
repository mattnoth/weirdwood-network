# Worklog Archive 016

> Archived Session Log entries (oldest-first within this file). Each archive holds 5 entries.
> Sessions: 73 (1/5).

---

### Session 73 — Cleanup-and-reorg triage: worktrees removed, CLAUDE.md #9 finding, scripts KEPT (2026-05-26)

**Model:** Opus 4.7. **Detail:** `history/session-details/session-073.md`. **Commit:** this endsession commit.

**The session:** `/continue cleanup-and-reorg` — became a triage/decision session; most of the "reorg" dissolved on inspection.

**Changes made:**
- Removed both leftover worktrees (`.claude/worktrees/{admiring-benz-fa26f8, mystifying-burnell-56ee9c}`, clean) + deleted the 2 fully-merged `claude/*` branches (reversible). `.claude/worktrees/` empty.
- Fixed the stale "gitignored" claim in `progress/continue-prompts/2026-05-26-cleanup-and-reorg.md` (corrected to the tracked-files reality below).
- Scratch files untouched (Matt: "ignore scratch files"). Memory: `project_pass1_all_opus` (Pass 1 = all Opus, Matt-confirmed; not derivable from extraction files).

**Decisions:**
- **Scripts folderization DEFERRED indefinitely** — cosmetic, high-risk: `stage4-*`↔`wiki-pass2-*` cross-import via hardcoded `_REPO/"scripts"/"<name>"` paths (4 bridges), and `tests/_helpers.py:load_script` loads by flat filename (~30 call-sites). Nothing's broken; payoff is navigational only.
- **27 comention / wiki-prose-edge scripts KEPT (do NOT re-propose archiving)** — they implement the pre-S65 wiki-comention approach (**superseded, not dead**) + one-off per-house classifiers + Haiku-bulk apparatus; inert but a plausible **future recall lever** (~9% prose-only relationships, S68 recall-sample). The only driver for archiving was "cleanup" → not enough.
- **CLAUDE.md #9 finding:** the continue prompt said `pass2-buckets/` is gitignored. Reality = **23,081 TRACKED files**, incl. **7,180 stale `skeleton/*.node.md`** (~28 MB, S72-verified redundant with `graph/nodes/`). Only `pass1-derived/` is gitignored. **Skeleton-untrack DEFERRED to its own decision** (entangled — ~24 `wiki-pass2-*` promotion scripts read `skeleton/`).
- **Edge state confirmed for Matt:** 3,811 promoted (v1.3 frozen); 5,886 core candidates worked through; **27,305** extra-table candidates held at the ~$270 / ≥80%-precision spend gate (smokes ~62-66%). Strategy (deterministic spine to minimize Haiku work + validation stack + prompt hardening) confirmed correct.

**What's next:** → **edge enrichment gate-opener** = the $0 deterministic **locator quote-grounding fix** → ~$1.4 re-smoke; if ≥~75% across 2 fresh samples, enrichment unlocks, else ship core-only. Continue: `progress/continue-prompts/2026-05-25-stage4-locator-grounding.md` (**Sonnet 4.6** build/smoke; Opus review only). **NOTE both stage4 continue prompts say edges=3,842 — STALE; it's 3,811 v1.3 after S72.** Downstream framework: `2026-05-25-stage4-enrichment-decision.md` (A/B/C). Deferred levers: skeleton-untrack; S67 resolver recall levers (`2026-05-23-stage4-pass1-finishing.md`).
