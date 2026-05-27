# Worklog Archive 015

> Archived Session Log entries (oldest-first within this file). Each archive holds 5 entries.
> Sessions: 68-71 (4/5).

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

---

### Session 70 — graph/edges/ v1 LANDED + Haiku enrichment gate (NO-GO) (2026-05-25)

**Detail:** `working/wiki/data/pass1-derived-enrichment-gate-result.md` + `pass1-derived-smoke2-headtohead-review.md` serve as the detail (no separate session file).

**Changes made:**
- **graph/edges/ v1 COMMITTED (`c3880e160`)** — `graph/edges/edges.jsonl` (3,842 cited Pass-1-derived edges) + `graph/edges/README.md`. First populated edge layer; graph is now traversable.
- NEW `scripts/stage4-formalize-edges.py` (+test, 99 green): merge spine(2,834 emit)+S67 tail(2,385 emit)+Hospitality(529)=5,748 → endpoint-gate −109, tail-violation quarantine −10, dedup −1,543 → 4,086 → `--precision-filter` (gated-type −234, CONTEMPORARY_WITH person↔person −10) → **3,842**. Quarantines preserved in `_formalized/` (gitignored).
- 3 $0 fixes to `stage4-tail-classifier.py` + `stage4-pass1-extra-tables.py` (+tests): vocab gating (5 types)+tier guidance; generator direction-validation + reusable `is_low_quality_endpoint()`; provenance (candidate_kind preserved, typed_by from `--model`). Rule-11 anti-pattern patches (CONTEMPORARY_WITH/COMPANION_OF/CITED_BY/CONTRADICTS/ASSAULTS/NURSED_BY). `--abort-after-consecutive-failures` (exit 42) + `--skip-existing`/`--output-dir` hardening.
- NEW `scripts/stage4-tail-bulk-forever.sh` (rate-limit-surviving overnight loop). **UNCOMMITTED** (classifier hardening + wrapper; 137 cls tests green) — commit with whichever path Matt picks.
- NEW reviews: `pass1-derived-smoke2-headtohead-review.md`, `pass1-derived-enrichment-gate-result.md`. Deleted continue prompt `2026-05-25-stage4-smoke-fixes-and-formalize.md` (executed).

**Decisions:** Matt: **deliverable-first** + head-to-head re-smoke (not Sonnet-only). Head-to-head (same 200 rows, post-lockdown): **Haiku 76% / Sonnet 78% strict** — neither cleared 80%; Sonnet's 2pt edge NOT worth 4.4× cost → **Decision C = enrich with Haiku**. Rule-11 patches cleanly eliminated the 2 target biases (CONTEMPORARY_WITH/COMPANION_OF→0) but post-patch precision = **~70%** (new RESPECTS drift + structural candidate-noise: evidence-mis-pairing, direction flips — the same ceiling as the v1 core; prompt can't reach it). **Bulk HELD overnight, $0 spent** — honored the agreed ≥80% gate. The deterministic core (explicit Pass-1 Relationships pairs) is the higher-quality layer; the extra-tables enrichment has a ~70-80% ceiling.

**What's next:** → continue: `progress/continue-prompts/2026-05-25-stage4-enrichment-decision.md` (**Opus 4.7** — A/B/C decision + review; Sonnet for the $0 builds). Options: **A** one iteration (RESPECTS gate + direction reminder + deterministic quote-relevance filter — also cleans v1) then re-smoke; **B** run bulk at ~70% + heavy filters + runtime verify (~$60); **C** ship core-only, defer enrichment. Rec: **A one-shot → fall back to C**. [Superseded by S74: C taken — enrichment NO-GO, core shipped 3,811 v1.3.]

---

### Session 71 — Stage 4 accuracy suite + prompt overhaul → PIVOT: unpromoted-node gap found, edges PAUSED (2026-05-25)

**Detail:** `history/session-details/session-071.md` + tracked docs: `working/wiki/data/readiness-review-fresh.md`, `prompt-review-opus-1.md`/`-2.md`, `pass1-derived-staging-manifest.md`, `pass1-derived-v1.1-applied.md`.

**Changes made (all $0/deterministic except 3 smokes ~$3.4 Haiku; NOTHING committed; `graph/edges/edges.jsonl` untouched):**
- **Deterministic accuracy suite (NEW, tested):** `stage4-{quote-relevance-filter,type-contract-validator,fresh-relocate-sample,refine-v1-edges,produce-v1-1-candidate}.py`; improved `stage4-pass1-evidence-locator.py` (locator v2 + `locate_quality`); `stage4-tail-classifier.py` prompt v4 (GOVERNING PRINCIPLE + GATE1/2/3, evidence-grounding, gated types 5→13, `prompt_version`/`prompt_sha` stamping). 119+ tests green.
- **Smokes:** smoke4 (60%), smoke5 (seed-4242, **72.5% raw**; post-filter looked ~80-91% but OVERFIT), **smoke6 (seed-7777 OUT-OF-SAMPLE = ~62% raw)**. v1.1 refinement candidate built (`_v1-refine/edges-v1.1-candidate.jsonl`) — **NOT applied.**
- NEW top-level continue prompt `CONTINUE-node-recovery-and-edges.md` + staging manifest.

**Decisions:** **PIVOT — edge formalization PAUSED.** Edge work surfaced that a large chunk of the wiki Pass-2 entity schema was **never promoted**: `graph/nodes/` = **8,299** nodes but **~7,251 staged `.node.md` sit unpromoted in `working/wiki/pass2-buckets/*/skeleton/`** (the "staging nodes ready" Matt remembered — NOT lost). Smoking gun: the type-contract validator false-dropped real `COMMANDS→faction` edges (stone-crows/second-sons/iron-fleet/brotherhood) because those factions aren't in `graph/nodes/characters/` — the node gap producing false edge-drops. So edges can't be finalized until nodes are whole. **Enrichment (Events+Dialogue Haiku) separately = NOT-YET** (~62% out-of-sample; root cause = locator hint↔quote decoupling; fresh-Opus-review caught my ~80-91% overfit claim). **Will edges be fully redone? No** — re-resolve + re-type-check (deterministic, $0) over existing candidates, NOT re-extract. Core v1 (3,842) FROZEN.

**What's next:** → **PRIMARY: `CONTINUE-node-recovery-and-edges.md`** (top-level; **Opus 4.7** "fixer & finder"). Stream 1 = node accounting + promote the ~7,251 staged skeletons; Stream 2 = edge re-validation against complete nodes; Stream 3 = folder reorg (wiki/scripts are dumps); Stream 4 = scratch-check (no project hook found — IDE-selection surfacing). SECONDARY (gated behind nodes): `progress/continue-prompts/2026-05-25-stage4-locator-grounding.md`. All Stage-4 scripts UNCOMMITTED.

---

### Session 72 — CORRECTION: "unpromoted-node gap" was a false alarm; index + validator + resolver FIXED; edges v1→v1.3 (2026-05-25→26)

**Model:** Opus 4.7 (autonomous stretches — Matt stepped away mid-session with "do all of this"). **Detail:** `history/session-details/session-072.md`. **Commits:** `eb3c6b18b`, `4f149f7b6`.

**The correction (CLAUDE.md #9 in action):** S71 handed off "~7,251 staged nodes never promoted → edges PAUSED." **Verified false this session** — it was a file count without a slug check. Slug reconciliation: **7,039/7,047** staged-skeleton slugs ALREADY in `graph/nodes/`; only **8** net-new. `promote.py` dry-run: 43 net-new / 2,367 byte-equal / 1,307 byte-diff. Promoted (8,299) > staged (7,047). **No backlog; node layer whole.** Did NOT mass-promote on the false premise.

**What was actually wrong — all FIXED ($0/deterministic):**
- **The index, not the nodes** (what Matt actually saw). `graph/index/` only had configs for characters/houses/locations/artifacts; 14 categories never indexed. script-builder extended `scripts/build-entity-indexes.py` + rebuilt → **1,847 new `*.index.json`** (factions 191, titles 542, events 371, …).
- **Type-contract validator** false-dropped `COMMANDS→faction` (Contract 4 only checked `graph/nodes/characters/`; the factions existed all along). Fixed `stage4-type-contract-validator.py`: COMMANDS accepts character OR commandable unit (faction/house); drops place(two-hop)/object; flags unknown. `TestCommandsContract` rewritten.
- **`refine-v1-edges.py` never passed `slug_category_index`** → category-based contracts never fired (latent bug). Fixed (builds + passes index; test stub updated). **805 tests green.**

**Edge re-validation (Matt's "re-resolve + re-validate, not re-extract"):** re-ran refine with the fixed validator over READ-ONLY `edges.jsonl` → **corrected v1.2 candidate 3,825 rows** (`_v1-refine/edges-v1.1-candidate.jsonl`); **16 faction-COMMANDS recovered** (gunthor→stone-crows, victarion→iron-fleet, …), 17 hard-drops (13 wrong COMMANDS + 1 MOTIVATES + 3 VIOLATES_GUEST_RIGHT). Pre-fix v1.1 preserved in `_v1-refine/superseded-2026-05-25-preCommandsFix/`. **`graph/edges/edges.jsonl` = 3,842 FROZEN/untouched** (md5 `9617c73b…`).

**Decisions/findings:** 1,307 skeleton↔node "conflicts" = stale staging vs canonical (richer) nodes → **NO ACTION** (re-promoting would downgrade). Data-smell tail: `lord-tywin` resolves to `graph/nodes/artifacts/` (alias/mis-type). 0.1 scratch: `endsession.md` already says don't triage scratch + `.gitignore scratch*` covers it, BUT 2 scratch files are git-tracked (`git rm --cached`). **Nothing committed; did NOT run /endsession** (no permission). Health-check lesson: use a **slug intersection**, not a file count.

**Then (same session, Matt back — "go for 1,2,3, commit"):** ① **applied v1.2 → `edges.jsonl` = 3,825 + committed.** ② net-new promotion CANCELLED (all 8 are dups of canonical nodes). ③ `lord-tywin` = real ship artifact, bad edge already dropped — no-op. Answered Matt's Q: fixing `graph/index/` does NOT help the edge scripts (they read `graph/nodes/`, not the index); the next real edge-quality lever is the **resolver/name-disambiguation** layer (the `lord-tywin` ship-vs-man class), a scoped follow-up.

**Resolver pass (2026-05-26, continued same session → edges v1.3 = 3,811):** title-person disambiguation in `stage4_name_resolver.py` + `CAPTAIN_OF`/`CREW_OF` validator guard. Measured 42 collision edges, simulated to de-risk (6 clean wins, ship `lady-marya` protected), applied to `edges.jsonl`. 814 tests green. Answered Matt's Q on whether the index helps edge scripts: no (decoupled) — the resolver is the lever.

**What's next:** → `CONTINUE-node-recovery-and-edges.md`. Open: folder reorg (wiki/scripts dumps + leftover worktrees); scratch untrack (`git rm --cached` 2 files); optional deeper resolver work (alias completeness for S67 unresolved/ambiguous endpoints).
