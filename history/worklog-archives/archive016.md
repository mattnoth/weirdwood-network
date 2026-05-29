# Worklog Archive 016

> Archived Session Log entries (oldest-first within this file). Each archive holds 5 entries.
> Sessions: 73, 74 (2/5).

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

---

### Session 74 — Locator grounding fix, enrichment NO-GO, core citations re-grounded, graph exercised (2026-05-26)

**Model:** Opus 4.7 + script-builder (Sonnet) + prose-edge-reviewer ×2. **Detail:** `history/session-details/session-074.md`. **Commit:** `63b8b461a`.

**Changes made:**
- `scripts/stage4-pass1-evidence-locator.py` — hint-anchored quote grounding (hint-verbatim→hint-fuzzy→both-named-window) + new `quote_source` field; **fixed `:11` line-number bug** (`read_chapter_prose` stripped blanks → `split_into_sentences` never saw paragraph breaks → all refs pinned to first prose line; fixed via gap-detection).
- `scripts/stage4-tail-classifier.py` — `quote_source`/`locate_quality` passthrough into all 4 output builders; **v5 precision rules** (`prompt_version=v5-precision-rules`, sha `d31ca56c4768`): R1 direction-lock, R2 evidence-supports-both-endpoints, R3 target-category, R4 state-not-moment, R5 temporal-phase, R6 no-analytical-from-moment.
- NEW `scripts/stage4-reground-core-citations.py` (+test) — re-grounded the SHIPPED core: **`graph/edges/edges.jsonl` 3,676/3,811 `evidence_ref` line numbers corrected** (quote text + edge set byte-identical, 3,811→3,811, safety-asserted; 9 left honestly unresolved). Edges are still v1.3 — same edges/types, citations now navigable.
- `.gitignore` — ignore regrounding backup/candidate (report tracked). 883 tests green.

**Decisions:** **Enrichment NO-GO → ship core-only.** Post-locator-fix out-of-sample smokes = **74.5% / 62.5%** strict (unstable, <75% gate; clear-case 83-89% but borderline over-emits sink it). The ~78% deterministic core is the better artifact than a ~70% LLM layer with no scheduled patcher (project value: a wrong cited edge is graph pollution). v5 rules authored + kept for any future revisit; v5 smokes killed mid-flight on Matt's "ship the core" call (~$0 extra). **Then discovered the committed core carried the SAME latent `:11` citation bug** (3,784/3,811) → re-grounded deterministically before declaring shipped.

**Graph exercised (the payoff):** nodes+edges+index **compose; 100% of 898 edge endpoints resolve to a node, 0 orphans, fully traversable.** Cersei/Tyrion query returned rich neighborhoods + 18 direct + 27 two-hop. Surfaced: mis-typed edges now *clickable* via the fixed citations (`cersei LOVES tyrion`=Varys-line; `tyrion LOVES cersei`=sarcasm; `ALLIES_WITH`=grudging submission); structural gap = **no temporal scoping → contradictory edges coexist** (LOVES+HATES same pair). Conflicting-type pairs concentrate the mis-types.

**What's next:** → `progress/continue-prompts/2026-05-26-graph-exercise-followups.md` (**Sonnet 4.6** builds; Opus review). (1) $0 **conflict-pair audit** — flag pairs with incompatible edge types as a precision-cleanup queue (attacks the ~22%). (2) Formalize the ad-hoc traversal into reusable `scripts/graph-query.py`. (3) Deferred: temporal/chapter scoping on edges; SIBLING_OF-class weak-evidence backfill. Spend: ~$2.5.
