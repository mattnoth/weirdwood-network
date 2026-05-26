# Session 74 — Locator grounding, enrichment NO-GO, core citation re-grounding, graph exercised (2026-05-26)

**Model:** Opus 4.7 (orchestrator) + script-builder (Sonnet) for the deterministic builds + prose-edge-reviewer ×2 (smoke reviews).
**Commit:** `63b8b461a`.

## Purpose

Open the Stage-4 edge-enrichment gate per `2026-05-25-stage4-locator-grounding.md`: fix the locator's hint↔quote decoupling, smoke fresh out-of-sample, refine the prompt, and decide GO/NO-GO on the ~$75 Events+Dialogue Haiku enrichment run. Matt's standing direction: "ship the core" if enrichment doesn't cleanly clear the bar.

## What happened, in order

### 1. Locator quote-grounding fix (the original task)
`stage4-pass1-evidence-locator.py` `locate_evidence` was re-scoring chapter sentences by name+content overlap and grabbing the nearest both-named window — discarding the hint's own quoted text. Worked example: `timeon→brienne` hint *contained* the verbatim line `"You did for Vargo with that bite…"` but the locator attached an unrelated both-named sentence. Fixed with a priority chain: **hint-verbatim → hint-fuzzy → both-named-window → nearest-fallback**, emitting a new `quote_source` field + honest `hint-anchored-*` `locate_quality` values (never fabricate a both-named quote when the true location names only one endpoint). 74 tests. quote_source distributions stable across seeds (Dialogue ~64-67% hint-verbatim, Events ~12% — Events are paraphrases).

### 2. Smokes (v4 prompt, post-locator-fix) → NO-GO
Two fresh out-of-sample seeds (1111, 2718), Haiku, ~$1.25 each. The first `--kinds` typo errored at arg-parse → **$0 wasted** (real flag is `--candidate-kinds`; `--apply` required).
- **seed-2718: 74.5% strict** (41/55, 5 wrong, 9 borderline). Events 78% / Dialogue 64%.
- **seed-1111: 62.5% strict** (35/56, 7 wrong, 14 borderline). Events 69% / Dialogue 54%.
- False-reject ~4-7% (healthy); **clear-case** precision 83-89% — the model is decisive-and-right but **over-emits borderline inferences**. The two samples diverge 12 pts → unstable, below the 75% gate.

### 3. Two bugs the reviewers surfaced
- **`evidence_ref` line number always `:11`.** Root cause: `read_chapter_prose` strips blank lines, so `split_into_sentences` never sees paragraph breaks → every sentence inherits the first prose line (11). The quote *text* was correct; only the line number was wrong. Reviewer initially mis-read this as "quotes pinned to chapter-start" — verified against chapter files it's line-number-only. Fixed via gap-detection in `split_into_sentences`.
- **Classifier dropped `quote_source`/`locate_quality`.** Passed them through into all four output-row builders (emit / rejected / needs-qualifier / classify-failed).
- 89 tests after both fixes; fresh seeds 3141, 9265 regenerated with correct line numbers + quote_source.

### 4. v5 precision rules
Authored 6 reject-harder rules from the shared error taxonomy (both reviewers agree): R1 direction-lock (LOCATED_AT/TRAVELS_TO/PARTICIPATES_IN/GIFTED_TO), R2 evidence-must-support-both-endpoints (the biggest sink — `jorah LOVES daenerys` where the quote is Jorah mourning his wife), R3 target-category (PRACTICES≠language, CLAIMS≠person, WORSHIPS≠ancestor, HOLDS_TITLE≠garbage-slug), R4 state-not-moment (ATTACKS/COMMANDS/ALLIES_WITH), R5 temporal phase (BETROTHED_TO vs SPOUSE_OF), R6 no-analytical-from-a-single-moment (PARALLELS). prompt_version → `v5-precision-rules`, sha `d31ca56c4768`, 217 tests.

### 5. DECISION: ship the core, shelve enrichment
v5 re-smokes were launched (seeds 3141/9265) then **Matt called "ship the core"** — killed them mid-flight (exit 144), ~$0 wasted beyond 2 in-flight batches. The deterministic core (~78%) is the better artifact than a noisy ~70% LLM layer with no scheduled patcher; per the project value "a wrong cited edge is graph pollution." v5 rules are kept (harmless improvement) in case enrichment is ever revisited.

### 6. INCIDENT — the shipped core had the same `:11` citation bug
Verifying the core before declaring it shipped: **3,784/3,811 committed edges had `evidence_ref` ending in `:11`** — the same latent locator bug, present since the core was built (predates the S72/S73 commit). Quote text correct, line numbers wrong (e.g. `arya→jon LOVES` cited line 11 but the quote is at 35). A cited graph whose citations point to the wrong line undercuts its whole value.
- Built `scripts/stage4-reground-core-citations.py`: for each edge, find the line where its EXISTING quote actually appears, rewrite ONLY the `evidence_ref` line suffix. Hard safety contract (every other field byte-identical; abort otherwise; 3,811→3,811).
- Result: **3,676 regrounded, 99 already correct, 27 skipped (paraphrase/no-quote), 9 unresolved** (quotes starting with a bare `."`/`?"`/em-dash — left honest, not fabricated). git diff = exactly 3,676 insertions / 3,676 deletions (1:1). 183 distinct line numbers now.

### 7. Exercised the graph (the payoff)
Walked a real query across nodes→edges→index:
- **8,297 nodes / 3,811 edges; 100% of 898 distinct edge endpoints resolve to a node — 0 orphans.** Structurally sound and fully traversable (exact-slug).
- Cersei (141 out/88 in) & Tyrion (186 out/129 in) returned rich neighborhoods; 18 direct edges, 27 two-hop bridges (Jaime densest connector).
- **Findings (now adjudicable thanks to the citation fix):** `cersei LOVES tyrion` cites a Varys/Sandor line (mis-typed); `tyrion LOVES cersei` cites the sarcastic *"Cersei is my own sweet sister"* (mis-typed); `cersei ALLIES_WITH tyrion` cites Cersei *"reared up like a viper"* (grudging submission, not alliance). `tyrion SIBLING_OF cersei` correct-but-weak-evidence (generic chapter-opener at :11). And the structural gap: **no temporal scoping → contradictory edges coexist** (LOVES + HATES both directions on the same pair).

## Takeaways
- The architecture (nodes + edges + index) **composes** and is gap-free structurally. The quality ceiling is edge *typing* (~78%), and exercising the graph concentrated the errors into a findable signal: **conflicting-type pairs are where mis-types cluster.**
- The citation re-grounding is the session's quiet win — it turned "the core has ~22% mis-types somewhere" into "click the cite and see exactly which ones are wrong."
- Health-check lesson reinforced: the orphan audit (slug intersection) is the right structural check; it came back clean.

## Spend
~$2.5 (two v4 smokes). Everything else $0/deterministic. v5 smokes killed before completing.
