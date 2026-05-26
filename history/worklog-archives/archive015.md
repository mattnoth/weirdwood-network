# Worklog Archive 015

> Archived Session Log entries (oldest-first within this file). Each archive holds 5 entries.
> Sessions: 68-69 (2/5).

---

### Session 68 — Stage 4 recall ceiling: mine all Pass 1 tables + recall-sample (2026-05-24)

**Detail:** `history/session-details/session-068.md`

**Changes made:**
- Answered Matt's two S67 questions: (a) **wiki comparison** — 1,973/6,239 resolved pairs (32%) corroborate an existing wiki edge, 4,266 (68%) are NEW; vs the deprecated comention path (29,259-candidate sink, 5,723 rows from 60/222 batches @ $55.66), Pass-1-derived = 5,219 edges @ $20.88 primary-source+cited. (b) **line marking** — locator attached verbatim quote + `file:line` to **5,816/5,886 = 98.8%** (70 chapter-level fallbacks); match-rate, not verified-correct.
- NEW `scripts/stage4-pass1-extra-tables.py` (opt-in `--extra-tables`; separate staging `pass1-derived/_extra-tables/{book}/`; **canonical spine untouched**) + `tests/test_stage4_extra_tables.py` (+81 → **431 green**) + report `working/wiki/data/pass1-derived-extra-tables-report.md`. Yield: **Hospitality → 529 deterministic $0 edges** (460 GUEST_OF + 69 VIOLATES_GUEST_RIGHT; Red Wedding correct); **Dialogue → 4,422 tail rows** (~$30 to type); Food/Events/Info **counted-only** (prose-shaped: 1,263 / 8,384 / 5,654 rows).
- Recall-sample check (`working/wiki/data/pass1-derived-recall-sample.md`, 7 chapters / 196 rels): **A=64% caught now · B=28% table-mineable · C=9% prose-only** (~3% of C high-value: Gregor/Aegon, Cersei/Maggy, Dany/Viserys).
- todos.md: added "Stage 4 — Recall Expansion" block. **All S68 work uncommitted** (Matt checkpoints).

**Decisions:** **Key tension found** — recall-sample ranks bucket-B productivity Events & Actions > Information Revealed > Hospitality > Dialogue, but the miner can only emit cheap deterministic edges from **Hospitality (#3)**; the #1/#2 recall tables are **prose-shaped (counted-only)** and need a bounded LLM pass (~14k rows, ~$95+); Dialogue ($30) is the **lowest-yield**. So 1a-as-built = A + Hospitality (~free), NOT the full ~92% the sample implied — the rest is an explicit LLM cost call. Spot-check of the Red Wedding output caught `walder-frey VIOLATES all-for-joffrey` (a toast resolved to a junk node — same index-pollution class as the pending resolver levers; 529 edges inherit it → endpoint filter before merge). **Full prose reading NOT warranted; targeted narrative-aside audit recovers the ~3% high-value C.** Nothing run beyond the deterministic miner.

**What's next:** → continue: `progress/continue-prompts/2026-05-24-stage4-recall-expansion.md` (**Opus 4.7** — decisions + merge coordination; references the finishing prompt for resolver-lever/tail-cleanup detail). Tracks: (1) merge 529 Hospitality/VIOLATES edges after endpoint filter; (2) smoke ~200 Dialogue rows before the $30; (3) **Matt decides** the bounded Events/Info LLM pass (~$95+); plus the S67 finishing work (resolver levers, tail cleanup/dedup, canonical merge) now also covering the 529 edges. #2 (fast narrow wiki layer) logged in todos.

---

### Session 69 — Stage 4 recall expansion: table-mining smokes + 2 reviews, held at $270 gate (2026-05-24)

**Detail:** `history/session-details/session-069.md`

**Changes made:**
- Committed S68 (`304192ffb`) after flagging a CLAUDE.md #9 stale-prompt contradiction (S67 was already committed; only S68 was pending — not "both uncommitted" as the prompt claimed).
- script-builder (Sonnet) extended `scripts/stage4-pass1-extra-tables.py` with Events/Info/Food candidate generators (entity-match via resolver, ≥2-entity filter, first-actor fan-out) + locator-anchored ALL `_extra-tables` rows to `sources/chapters/{book}/{chapter}.md:line`; smoke-enabled `scripts/stage4-tail-classifier.py` to read `_extra-tables` rows + added ENCOUNTERS Rule-6 verb-gate to the prompt + `--sample-n` stratified smoke. `--apply` wrote **32,194 untyped candidate rows** (Dialogue 4,422 / Events 20,321 / Info 6,653 / Food 798).
- Added `--output-dir` (+ `.resolve()` + defensive `relative_to`) to the tail-classifier so smokes NEVER append into canonical `_tail-typed/`; + redirect test. 273 tests green.
- Ran 2 smokes (Sonnet `claude -p`, ~$3.60 total): Dialogue 144 typed/56 rej/$1.68; Events/Info/Food 123 typed/77 rej/$1.89. Measured ~$0.009/row → full run re-baselined to **$270-290** (not ~$100; the Events fan-out) + ~3-4 days wall-clock (needs parallel wrapper).
- 2 `prose-edge-reviewer` audits — both **SYSTEMATIC**. Strict precision Dialogue ~60% / Events ~66%; reject ~90%; Events direction-error ~7%, fan-out spurious ~18%, bare-slug ~15%.
- NEW: `STAGE4-SMOKE-REVIEW.md` (repo root, for Matt), `working/wiki/data/pass1-derived-smoke-report.md`, continue prompt `progress/continue-prompts/2026-05-25-stage4-smoke-fixes-and-formalize.md`. Deleted superseded `2026-05-24-stage4-recall-expansion.md`.

**Decisions:** Matt's call: type all 4 tables (Dialogue/Events/Info/Food; fights ∈ Events) before formalizing; **full source-chapter re-read DEFERRED** (table-mining now, enrich later — additive "build then enrich"). **HELD at the $270 spend gate** — the smokes did their job, catching 3 systematic, fixable ($0) problem classes: (1) prompt over-types `INFORMS` (~100% wrong — it's spy→handler)/`ADVISES`/`MANIPULATES`/`SUPPORTS`/`ALIAS_OF` + uniform Tier-1; (2) generator direction-heuristic/fan-out/bare-slug emission = the SAME `all-for-joffrey` endpoint-pollution class as the 529 Hospitality edges (one fix cleans both); (3) `candidate_kind` hardcoded → provenance loss. Reject discipline (~90%) + relationship-revealing types (SIBLING_OF/KILLS/VOWS_TO/DUELS/REVEALS_TO/CONSPIRES_WITH/FIGHTS_IN) are solid. Canonical `_tail-typed/` (2,385 edges) untouched all session. Two bugs caught by doing, not by the 273 green tests.

**What's next:** → continue: `progress/continue-prompts/2026-05-25-stage4-smoke-fixes-and-formalize.md` (decisions A/B/C; Sonnet for the $0 fixes). Track 1: 3 fixes (prompt vocab restriction+anti-patterns; generator direction-validation+slug-quality gate = endpoint filter; candidate_kind provenance). Track 2: re-smoke ~$4 → confirm ≥80% strict precision. Track 3: scoped full run via run-forever wrapper, drift-detection mandatory. Track 4: **FORMALIZE into `graph/edges/`**. [Superseded by S70-S74: edges formalized v1 S70; enrichment NO-GO + core shipped S74.]
