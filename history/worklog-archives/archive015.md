# Worklog Archive 015

> Archived Session Log entries (oldest-first within this file). Each archive holds 5 entries.
> Sessions: 68 (1/5).

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
