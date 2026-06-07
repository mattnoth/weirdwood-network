# The Weirwood Network — Project Worklog

> **Purpose:** This is the living history of the project. Every Claude Code session should read this file to understand what has been done, what decisions have been made, what's in progress, and what's queued. Update this file at the end of every work session.
>
> **Convention:** Newest entries at the top. Each entry is dated and tagged with what was done.

---

## How To Use This File

### For Claude Code Agents
Load this file alongside `reference/architecture.md` at the start of every session. Before doing any work:
1. Read the **Current State** section to understand what exists
2. Read the **Active Decisions** section for unresolved design questions
3. Read the **Ideas & Backlog** section for queued work
4. Check the **Session Log** for what happened recently

After completing work, update:
- **Current State** to reflect what now exists
- **Session Log** with a new entry describing what was done
- **Active Decisions** if new questions arose
- **Ideas & Backlog** if new ideas or tasks surfaced

### For Matt
This is your project memory. When you come back after a break, read Current State and the last few Session Log entries to get back up to speed. Add ideas to the backlog whenever they occur to you, even outside of Claude Code sessions.

---

## Current State

### Infrastructure
- [x] Repository initialized
- [x] project-context.md in place (master architecture spec)
- [x] CLAUDE.md in place (orchestration guide)
- [x] Directory structure created (sources/, extractions/, graph/, index/, curation/, reference/, scripts/)
- [x] Source .txt files moved to sources/raw/
- [x] Subagent definitions in .claude/agents/ (2 full: mechanical-extractor, script-builder; 5 stubs: wiki-ingester, voice-analyzer, foreshadowing-scanner, theory-extractor, discovery-agent)
- [x] Custom slash commands (.claude/commands/endsession.md, continue.md)
- [x] Working directory with progress.md + todos.md
- [x] Reference files organized (reference/architecture.md, foreshadowing-events.md, pov-characters.md)
- [x] Chapter splitter script written (`scripts/chapter-splitter.py`)
- [x] Chapter splitter tested on one book (AGOT: 73/73)
- [x] All five books split into chapter files (344 total: AGOT 73, ACOK 70, ASOS 82, AFFC 46, ADWD 73)
- [x] Wiki scraper script written (`scripts/wiki-scraper.py`) — migrated from urllib to Playwright for Cloudflare bypass
- [x] Wiki scraper extended with `--mode all` + `--limit N` for full unattended crawl
- [x] Wiki directory structure created (`sources/wiki/`) — now fully gitignored
- [x] Full-crawl runbook drafted and updated for Playwright (`working/runbooks/wiki-full-crawl.md`)
- [x] Full wiki crawl executed (17,945/17,952 pages succeeded, 377 MB on disk)
- [x] Taxonomy candidates template created (`working/taxonomy-candidates.md`)
- [x] POV reference table corrected (6 missing chapter headings added)
- [x] D&E novellas split into chapter files (3 total: THK 1, TSS 1, TMK 1 — each novella is one continuous chapter)
- [x] TWOIAF OCR'd and extracted to plaintext (179K words, 164MB OCR'd PDF)
- [x] ocrmypdf + poppler installed (Tesseract, Ghostscript, pdftotext)

### Extraction Pipeline
- [x] Pass 1 agent prompt v1 (draft complete — `agents/pass-1-mechanical.md`)
- [x] Pass 1 v1 run on AGOT (73/73 chapters, archived to `extractions/archives/agot-v1/`)
- [x] Pass 1 agent prompt v2 — added: Physical Environment, Character Appearances, Food & Drink, Hospitality & Guest Right, Location Descriptions, Spatial Layout & Movement, time_markers, direwolves/dragons-as-characters rule
- [x] Pass 1 v2 run on AGOT (73/73, archived to `extractions/archives/agot-v2/` — 4-category Raw Entity List)
- [x] Pass 1 v2 run on ACOK (50/70, archived to `extractions/archives/acok-v2/` — 4-category Raw Entity List)
- [x] Pass 1 v3 prompt update: expanded Raw Entity List to 12 categories (10 + Other catch-all), added strict formatting rules (all headers required, no merging/renaming, "None" for empty categories)
- [x] Pass 1 v3 run on AGOT (73/73 — complete)
- [x] Pass 1 v3 run on ACOK (70/70 — complete)
- [x] Pass 1 v3 run on ASOS (82/82 — complete; Okey ran in parallel on shared Max account, branch `pass1-asos-extraction`)
- [x] Pass 1 v3 run on AFFC (46/46 — complete)
- [x] Pass 1 v3 run on ADWD (73/73 — complete)
- [ ] Pass 1 on Tales of Dunk and Egg (THK, TSS, TMK) — **deferred (enrichment pass for main-arc nodes)**. D&E content will eventually enrich existing main-arc Targaryen-prehistory nodes (Bloodraven, Egg/Aegon V, etc.) but is not on the active critical path. Not dropped, not urgent. Decision 2026-05-06 (Session 37 Q11=b).
- [x] Wiki infobox parser script (Track B) — `scripts/wiki-infobox-parser.py` produces `working/wiki/data/{infobox-data.jsonl (5,279), page-index.jsonl (17,657), parse-stats.md}`. `first_available` populated 2,888/5,279 (54.7%). **Three open issues:** (1) `categories[]` empty across all pages (parse API strips catlinks footer) — blocker for runbook §1.2.1 unless deferred to `entity_type_guess`, (2) `books` field parsed only 37 times vs 1,953 raw occurrences (parser bug), (3) unmapped infobox fields worth edge-taxonomy review (`dynasty`, `written by`, `hatched`, `fathers`, `vassal`, `cadet branch`).
- [x] AGOT/ACOK supplementary entity index — OBSOLETED 2026-04-25. v3 prompt captures all 12 categories directly; backfill index no longer needed. See `working/todos.md` line ~245.
- [ ] Pass 2 wiki ingestion agent prompt written
- [ ] Pass 2 wiki ingestion complete
- [x] Wiki Pass 2 v1 — core (37/37 buckets complete; 855 nodes; cost $95.33; per-node $0.111 healthy per Stage-2 cold review)
- [x] Wiki Pass 2 Stage 2 cold review (Session 24; decision was `remediate`, but overturned same session — see Active Decisions)
- [x] Wiki Pass 2 Stage 3 — secondary (Session 26; FULL pipeline rebuilt as Python-only after design review showed the Stage 3b agent was inertia-driven. 472 buckets / 3,315 candidate pages → 3,314 nodes promoted. Cumulative graph: 855→4,169 then →4,239 after Tier-1+Tier-2 recovery. Cost $0. Wall-clock ~30 sec total. 0 conflicts.) Canonical pipeline: `working/runbooks/wiki-pass2-pipeline.md` (rewritten as v3).
- [x] Wiki Pass 2 Stage 3c — audit cleanup (Session 27; 4 audits run, 6 parser bugs fixed, 484 nodes re-emitted across multiple targeted runs. Tier 3 promotion campaign Passes A-D + E Phase 1 added 769 new nodes. Cat 1 orphan edges 7,784→2,955 (62% drop). Stale religion-bleed 0. Edge vocabulary lock holds.)
- [x] Wiki Pass 2 Path B — categorizer extension + promotion campaign (Session 28; bounded MediaWiki categories backfill + parser CATEGORY_TYPE_MAP. `unknown` 12,434 (70.4%) → 2,118 (12.0%). +2,240 graph nodes (5,008 → 7,248). Cat 1 orphan edges 2,955 → 1,973. 5 new dirs bootstrapped: `texts/`, `theories/`, `concepts/`, `species/`, `foods/`. New entity type `object.food`.)
- [x] Wiki Pass 2 Path B promotion completion + schema-drift audit (Session 29; 4 new entity types added: `object.material`, `concept.language`, `concept.medical`, `concept.custom`. 4 new dirs: `materials/`, `languages/`, `medical/`, `customs/`. `unknown` 2,098 → 1,257. Net +315 graph nodes (7,248 → 7,563). 130 stale-dir mismatches cleaned. Full schema-drift audit on opus: 0 HIGH / 4 MED / 4 LOW. Cat 1 orphan edges 1,973 → 1,963. Edge vocabulary lock holds. Chronology data extracted from 74 year pages: 2,245 events in `working/wiki/data/chronology-events.jsonl` (awaits v2 temporal-edges schema; not graph edges yet).)
- [x] Wiki Pass 2 Stage 0 foundation — alias-resolver built + run (Session 26). 707 broken refs reclaimed via slug-mismatch fix. Empirical signal validates that most remaining "broken" refs are genuinely missing concept entities (concept-pages decision: defer).
- [~] Wiki Pass 2 Stage 4 — prose-derived edge discovery. **PIVOTED 2026-05-22 (S65) to a Pass-1-derived deterministic pipeline; wiki-chapter-summary comention DEPRECATED.** Deterministic spine BUILT + committed (S66, `047e49b3b`): `scripts/stage4-pass1-edge-candidates.py` + `stage4-pass1-evidence-locator.py` + `stage4_name_resolver.py` → **2,818 typed, ~99%-cited `book-pass1` edges at zero LLM cost** (output gitignored under `working/wiki/pass2-buckets/pass1-derived/`; audit reports under `working/wiki/data/pass1-derived-*`). S67: alias-recovery applied (spine 2,818→2,834, +16); 133 comention files deprecate-stamped in-data; **LLM tail RAN (Sonnet via `claude -p`): 2,385 typed edges (78%, $20.88) → total book-pass1 = 5,219**. Remaining: tail-violation cleanup (21/2,385, 0.88%) + 2 resolver levers (Matt's call) + tail dedup + `_tail-typed/` merge. **S68 RECALL EXPANSION:** built `scripts/stage4-pass1-extra-tables.py` (mines the OTHER relational tables; opt-in `--extra-tables`; separate `_extra-tables/` staging, canonical spine untouched) → **+529 deterministic $0 edges from Hospitality (460 GUEST_OF + 69 VIOLATES_GUEST_RIGHT)** + 4,422 Dialogue tail rows (~$30 to type) + Food/Events/Info counted-only. Recall-sample: **A 64% caught now / B 28% table-mineable / C 9% prose-only** — but the high-recall B tables (Events/Info) are prose-shaped (need ~$95+ LLM pass), Hospitality is the deterministic win, Dialogue is lowest-yield. 529 edges NOT yet merged (need endpoint filter; inherit `all-for-joffrey`-class noise). **S69 SMOKES (held at spend gate):** built Events/Info/Food candidate generators + locator-anchored all `_extra-tables` rows to `sources/chapters:line` + `--output-dir` safety flag; wrote **32,194 untyped candidate rows** (Dialogue 4,422 / Events 20,321 / Info 6,653 / Food 798); smoked Dialogue + Events/Info/Food (~$3.60, Sonnet) → both reviewer verdicts **SYSTEMATIC** (strict precision ~60-66%; reject ~90%; Events fan-out ~18% / direction-error ~7% / bare-slug ~15%). Full run re-baselined to **~$270-290 + ~3-4 days wall-clock** — **NOT launched.** 3 $0 fixes needed first: prompt vocab-restriction+anti-patterns; generator direction-validation+slug-quality gate (= endpoint filter, also cleans the 529); `candidate_kind` provenance (`stage4-tail-classifier.py:502`). `graph/edges/` still EMPTY — the FORMALIZE/merge is the milestone. Continue: `progress/continue-prompts/2026-05-25-stage4-smoke-fixes-and-formalize.md` (review doc: `STAGE4-SMOKE-REVIEW.md`). (Older wiki-comention/Haiku-bulk apparatus superseded; `prose-edge-classifier` agent at `.claude/agents/prose-edge-classifier.md` retained for the LLM-tail typing step.)
- [ ] Pass 3 voice/perception agent prompt written
- [ ] Pass 4 foreshadowing agent prompt written
- [ ] Pass 5 theory-informed agent prompt written
- [ ] Pass 6 discovery agent prompt written

### Index & Graph
- [ ] Trigger table v1
- [x] Entity index — **REBUILT to all categories (Session 72).** `graph/index/` previously covered only characters/houses/locations/artifacts/chapters; `scripts/build-entity-indexes.py` extended with 14 more `TYPE_CONFIGS` → **1,847 new `*.index.json`** (factions, titles, events, religions, species, texts, concepts, materials, foods, theories, customs, languages, medical, prophecies). This was the real "entities aren't there" gap (the nodes always existed; the index didn't cover them). Mention-stats zero for wiki-sourced entities Pass 1 never tagged (expected).
- [x] Chapter index (per-chapter `*.mentions.json` under `graph/index/chapters/`)
- [x] Graph edges formalized — **v1.3 (Session 72)** (`graph/edges/edges.jsonl` = **3,811** cited Pass-1-derived edges; v1 3,842→v1.2 3,825→v1.3 3,811). **v1.2:** type-contract re-validation vs complete node set (−17 wrong, +3 RULES→COMMANDS retype, kept 16 real `COMMANDS→faction`). **v1.3 resolver pass:** title-person disambiguation — 6 ship/artifact/title nodes named after people (`lord-tywin`=Cersei's dromond, `queen-cersei`, `lord-renly`, `princess-myrcella`, `lady-olenna`, `khal-jhaqo`) were capturing person references via exact slug-match; remapped → their characters (−12 dups) + new `CAPTAIN_OF`/`CREW_OF` target-not-character contract dropped 2 mis-typed "captain of the guard" edges. ~78% strict precision; all `evidence_ref`-carrying. **S74: core SHIPPED — citations re-grounded** (`scripts/stage4-reground-core-citations.py` corrected 3,676/3,811 `evidence_ref` line numbers; quote text + edge set byte-identical; fixed the latent `:11` locator bug — `read_chapter_prose` stripped blanks so all refs pinned to the first prose line). **Graph exercised: 100% of 898 edge endpoints resolve to a node, 0 orphans, fully traversable.** **Haiku Events+Dialogue enrichment = NO-GO, SHELVED** (post-locator-fix out-of-sample smokes 74.5%/62.5%, <75% gate; v5 precision rules authored + kept for any future revisit). Commit `63b8b461a`.
- [x] Graph query + audit tooling — **NEW (Session 75).** `scripts/graph-query.py` (S39 node-inspection EXTENDED with `--neighbors`/`--path`/`--health`/`--edges` over canonical `edges.jsonl`) + NEW `scripts/graph-conflict-pairs.py` (read-only precision-cleanup review queue → `working/wiki/data/graph-conflict-pairs.{md,jsonl}`; 32 flagged pairs, mostly temporal arcs). 920 tests green. `--health` confirms 0 orphans / 100% traversable.
- [x] Edge temporal-scoping — **NEW (Session 76).** `scripts/stage4-edge-temporal-scope.py` (+58 tests) annotates all 3,811 edges with `(book_order, chapter_number)` + temporal-aware conflict re-audit → **31/32 flagged pairs are temporal arcs** (`--window chapter`), 1 true same-window (`cersei↔tyrion`). Read-only on `edges.jsonl`. Outputs `working/wiki/data/edges-temporal-scoped.jsonl` + `graph-conflict-pairs-temporal.{md,jsonl}`.
- [~] Edge-modeling reification (Plate sequence, S82-S83) — **Plates 0+1+2+2.5 + staged cleanups + Plate-3 smoke: ALIGNMENT AUDIT 2026-06-06 = ON COURSE.** Independent fresh-session auditor recomputed all load-bearing numbers (edges.jsonl=3811 untouched, git status on graph/ empty, canonical_type_count=165, normalizer flips=10 not 11, 371 event nodes, phantom Aerys + 12 drift nodes still unmutated) — zero canonical writes, all of D1/D2/D3/D7/D8 honored in staging, Red-Wedding smoke demonstrates the "who killed/ordered X" 2-hop fix in dry-run. Next: launch full Plate 3 after Matt resolves Q1 (reify-selective) + Q2 (fuzzy reuse) and the 4 high-conf collision merges + 12 drift reclassifications are applied at the Plate-5 gate. Verdict + per-area detail in `working/edge-modeling/SESSION-LOG.md`. **Plates 0+1+2 SHIPPED; Plate 3 unblocked (HELD).** Plate 0: head-direction normalizer flipped 10/3,811 edges + Aerys slug-merge candidate (3 edges) — STAGED at `working/edge-modeling/normalizer-{candidates.jsonl,diff.md}`, `flagged-for-review.jsonl`, `aerys-merge-candidates.jsonl`. Plate 1: Pass-1 head rule + Events sub-bullets in `.claude/agents/mechanical-extractor.md`; `AGENT_IN`+`VICTIM_IN` added + `COMMANDS_IN` widened in `reference/architecture.md` (vocab 163→165); validator Contract 10 added to `scripts/stage4-type-contract-validator.py`. Plate 2: D2 RESOLVED → **option (a) Replace** (reification sufficient; `graph-query.py --path` traverses person→event→person transparently — no materialized dyad). Coverage: 8,384 Pass-1 event entries / 8,317 distinct titles / 8,316 needs-mint floor / only 38/371 (10%) event nodes have chapter linkage. Master design: `working/edge-modeling/edge-modeling-reification-design.md` (D2 resolved in §3). Plates 3+4+5 HELD; Plate 3 has 2 new design questions surfaced by Plate 2 (reify-all-vs-selective + §3 D3 correction). NOT merged into `graph/edges/edges.jsonl` (Plate 5 gate). Session log: `working/edge-modeling/SESSION-LOG.md`. **S84 UPDATE:** Q1 RESOLVED → reify-**selective** (trigger families only); Q2 → confidence-gated fuzzy reuse-before-mint; **D8** added (reify on n-ary STRUCTURE not type — clean dyads stay direct edges). Audit loop codified (Reporter + Auditor prompts + runbook); independent auditor verdict on Plates 0–2.5 = **ON COURSE**. Plate 3 pipeline `scripts/edge-reify-backfill.py` BUILT + validated (12-event mini-batch $0.81, all gates pass) + HARDENED (fail-fast + `--resume`). **Full sweep HELD/incomplete** — overnight attempt killed by rate wall (only 37 staged minted nodes + 11 review-queue; no role edges). Revised scope ~2,056 candidate events (~$50-160) → run a calibration chunk first. RESUME: `progress/continue-prompts/2026-06-07-edge-modeling-plate3-resume.md`.
- [~] Events edge enrichment (Stage 4) — **BULK RUN COMPLETE (S80), STEP-1 DRIFT AUDIT NO-GO (S81 2026-06-01, borderline).** Bulk: 16,502 → 1,617 typed + 14,884 rejected at `_events-haiku-bulk/` (gitignored), single prompt_sha `d31ca56c4768`, 0 conform_violations. Vs v1.3: 988 net-new triples *if promoted* (TRAVELS_TO/WITH 242, LOCATED_AT 90, COMMANDS 121, REVEALS_TO 66, ATTACKS 43, DREAMS_OF 36 lead). **Drift audit (50-row stratified, Sonnet 4.6 judge, $0.93) returned triple 48 % / pair 56 %** — below gates (70 %/85 %). Fresh-eyes review (S81 general-purpose subagent, cold cold-read of all 22 REJECTs) confirmed ~11 clear Haiku drifts (Rule 4a / V5-R2 / Rule 12 violations) + ~3-4 clear Sonnet over-rejections + ~7-8 ambiguous; adjusted ≈ 56-70 %, still at/below gate. **No-Go stands but borderline.** The 7-step promotion chain at `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/` is halted at step 1 awaiting Matt's escalation pick (5 paths in `cross-model-audit.md §6`; audit recommends Option C — Sonnet-filter the named-type rows only at ~$2-5). Audit script `scripts/events-drift-audit.py` (sha `576cc815649c`) is throwaway-single-purpose, uses canonical prompt code for byte-identical Haiku parity. **NOT merged into `edges.jsonl`.** Schema gap noted: rejected rows have no `reject_reason` — fix-later, Dialogue prep. Analysis: `working/audits/events-haiku-bulk-2026-05-29/analysis.md`. Prior context: S79: Matt re-launched at 240s then asked to lower to **120s** (the S78 "lower before travel" action item is DONE at 120s — NOT 600/300 as the prior plan said). Resume verified: skipped 5,239 done rows, 11,263 remaining / 282 batches at the relaunch, same `v5-precision-rules` sha. Known loose end: a recurring ~40-row acok batch fails with a JSON parse error every run because `classify_failed` is not a skip-key (non-fatal; see S79 entry + todos). As of 2026-05-28 10:26: **batch 92/411 (319 left), $11.34 spent (~$50 proj), 389 edges** (AGOT/ACOK; later books book-ordered, not yet reached). Validate@25/50/75 reject_rate ~0.90 unresolved=0 (no walls, no drift); first-flush human read ~93–96% strict. NOT merged into `edges.jsonl` (gated). Monitor log: `working/session-results/2026-05-27-events-haiku-bulk-monitor-log.md`. Haiku-vs-Sonnet comparison done on the SAME rows (AGOT 600 + ACOK 600 out-of-sample): **Haiku ~85% / ~90% strict** (vs Sonnet's 82-86%), 0 walls, ~$1.8/run → **DECISION: Haiku** for the full run (fresh all-Haiku, single provenance; Sonnet partial `_events-run-20260527/` superseded). Residual errors were **bad candidate slugs** (disambiguation, not model error) → **FIXED**: `stage4-pass1-extra-tables.py` now passes `slug_category` so the title-person rung fires (lord-tywin→tywin-lannister) + endpoint blocklist (bastard/dog/four-storms/hunt) → pass1_events **16,572→16,502 clean rows** (backup `_extra-tables.pre-slugfix-20260527/`). Runner BUILT + HARDENED: `scripts/stage4-tail-classifier.py` gained `--sleep-between` (chunked, stop-file-aware) + `--validate-every`/`--reject-rate-floor` (drift-halt exit 43); wrapper `scripts/stage4-events-bulk-run.sh` (paced auto-resume, `sleep_with_stop_check`, SIGINT-terminal, MAX_ITER, stop-file). **1072 tests green.** Comparison report: `working/session-results/2026-05-27-haiku-vs-sonnet-events.md`. Runbook: `working/runbooks/stage4-events-haiku-bulk.md`. NOT merged into `edges.jsonl` (separate gated milestone).
- [ ] Convergence maps

### Reference Materials
- [x] Foreshadowing events list (`reference/foreshadowing-events.md`)
- [ ] Theory seeds file
- [ ] Taxonomy reference doc
- [x] Architecture spec (original outline exists, needs refinement)

---

## Active Decisions

> Design questions that need resolution. Tag with status: OPEN, DECIDED, DEFERRED.

### OPEN: Events Haiku bulk — drift audit returned NO-GO (borderline); chain halted at step 1, awaiting Matt's escalation pick (2026-06-01, Session 81)
- **Bulk artifact is complete and clean** (S80): 1,617 typed edges + 14,884 rejected over 16,502 candidates at `_events-haiku-bulk/`; single prompt_sha `d31ca56c4768`, all `typed_by=haiku`, 0 conform_violations.
- **BUT step 1 drift audit (S81) returned NO-GO** — triple-level 48 % (gate 70 %), pair-level 56 % (gate 85 %); 22/50 sampled Haiku emits rejected by Sonnet judge. Failure concentrates in structural-edge types: TRAVELS_TO 17 %, TRAVELS_WITH 0 %, LOCATED_AT 20 % triple agreement.
- **Fresh-eyes pressure-test (S81) corrected the framing:** ~11 of 22 REJECTs are clear Haiku drift (Rule 4a hint-as-evidence, V5-R2 quote-doesn't-support, Rule 12 co-presence); ~3-4 are confirmed Sonnet over-rejections (judge_idx 2/6/14/16); ~7-8 ambiguous. Adjusted triple ≈ 56-70 % — at or below the gate. **No-Go stands but is borderline, not catastrophic.** The S69 vs S77 smoke-session contradiction was a misciting + a measurement-shape mismatch (S77 measured hand-read precision on fresh candidates, NOT Sonnet-judges-Haiku-emit on stratified emits) — both can be true.
- **The 3 chain-startup decisions Matt made up front still hold IF a path leads to promotion:** (1) full re-merge, not additive overlay; (2) ship Events-only as v2.0 now, Dialogue v2.1 separate; (3) `reject_reason` schema fix deferred to Dialogue prep.
- **Pick required (5 escalation paths, full discussion in `cross-model-audit.md §6` + `2026-06-01-events-bulk-escalation-pick.md`):** (A) re-run bulk on Sonnet ~$340; (B) promote long-tail-only; (C) Sonnet-filter the named-type rows only ~$2-5 (audit's recommendation); (D) tighten Haiku to v6 + re-run; (E) abandon Events for v2.0; wait for Dialogue.
- **Known loose end carried forward:** the `classify_failed`-not-a-skip-key parse-fail block from S79 still pending. Non-blocking for the escalation pick.
- **Reports:** `working/audits/events-haiku-bulk-2026-05-29/analysis.md` (S80 bulk analysis) + `cross-model-audit.md` (S81 drift audit).

### OPEN: 3 gated core-cleanups — still await Matt's before/after sign-off (carried from Session 76)
- Model decision RESOLVED (→ Haiku, see above). Still pending Matt's OK (do NOT touch `edges.jsonl` without before/after sign-off):
- **3 gated core-cleanups — await Matt's before/after sign-off (do NOT touch `edges.jsonl` without it):** (1) drop the 2 `cersei↔tyrion` LOVES mis-types (3,811→3,809); (2) retype the ~22 physical `ASSAULTS`→`ATTACKS` (`ASSAULTS`=sexual only per architecture.md:233; fix the spine phrase→type map too); (3) merge-time `OWNS→BONDED_TO` for direwolf/dragon targets (Events output, not core). The Events v5 prompt already obeys the ASSAULTS rule (emitted 0).
- **Operational:** long unattended runs MUST use a sleep-until-reset auto-resume wrapper — S76's bare worker sat idle all night after one cap wall.

### AMENDED: Enrichment is DEFERRED, not abandoned — Events is the next surface (2026-05-26, Session 75)
- **Decision (Matt):** Softens the S74 "SHELVE enrichment" below. Matt **does want to enrich the graph** — step by step, with **Events as the next surface**, but **gated behind the precision changes landing first** (the conflict-pair cleanup built this session + the kept v5 precision rules). **Not launched this session** (Matt chose to end + queue it).
- **Temporal flagging endorsed** — per-edge "when does this apply" is the right structural answer to the contradictory-edges problem, and it's largely deterministic (every edge carries `evidence_book`+`evidence_chapter`; chapter frontmatter has `chapter_number`).
- **DO NOT** run the ~$270 Events bulk blind — it failed the 75% precision gate (S74). The next Events pass must fold in the precision precursors. Continue: `progress/continue-prompts/2026-05-26-stage4-events-enrichment.md`. Memory: `project_enrichment_wanted_events_next`.

### DECIDED: Ship the deterministic core; SHELVE Events+Dialogue LLM enrichment (2026-05-26, Session 74)
- **Decision (Matt):** Ship `graph/edges/edges.jsonl` (3,811 cited deterministic edges, ~78%) as THE edge layer. **Do NOT run the ~$75 Events+Dialogue Haiku enrichment.**
- **Why:** After fixing the locator's hint↔quote decoupling (the gate-opener), two fresh out-of-sample smokes came in **74.5% / 62.5%** strict — unstable and below the 75% gate. Clear-case precision is 83-89% but the model over-emits borderline inferences. A ~70-74% enrichment layer is *noisier than the spine it sits on*, with no scheduled patcher; per the project value "a wrong cited edge is graph pollution — worse than no edge." The ~78% deterministic core is the better artifact.
- **What's kept:** the locator fix (hint-anchored grounding + `:11` line-number fix), the `quote_source` passthrough, and the **v5 precision rules** (`v5-precision-rules`) — all harmless improvements retained in case enrichment is ever revisited. The v5 re-smoke was killed mid-flight when the decision landed (~$0 extra).
- **Citation re-grounding (same session):** verifying the core revealed it carried the SAME latent `:11` bug (3,784/3,811). Re-grounded deterministically (line-numbers-only; quote text + edge set byte-identical) so the shipped core's citations are navigable. The core is **still v1.3** — same edges/types, repaired citations.
- **Next (deferred levers, NOT enrichment):** conflict-pair audit (precision cleanup), `scripts/graph-query.py`, edge temporal-scoping. See `progress/continue-prompts/2026-05-26-graph-exercise-followups.md`.

### RESOLVED/CORRECTED: The "unpromoted-node gap" was a FALSE ALARM — node layer is whole (2026-05-25, Session 72)
- **S71 claimed** ~7,251 staged `.node.md` were never promoted and PAUSED edges until "the node layer is whole." **That was a file count without a slug intersection — and it was wrong.** S72 verified three ways: (1) slug reconciliation — **7,039 of 7,047** unique staged-skeleton slugs are ALREADY in `graph/nodes/`; only **8** truly net-new. (2) `promote.py` dry-run — of ~3,730 promotable Tier-A/B pages: **43 net-new / 2,367 byte-equal / 1,307 byte-different**. (3) promoted (8,299) > staged (7,047). **No backlog. The skeletons are stale intermediate artifacts; promoted nodes are canonical (and in substantive conflicts, RICHER).**
- **What was actually wrong (all FIXED S72, $0/deterministic):** (a) **the INDEX, not the nodes** — `graph/index/` only had builder configs for characters/houses/locations/artifacts; 14 categories were never indexed → "entities weren't there." Extended `build-entity-indexes.py` + rebuilt (1,847 new index files). (b) **type-contract validator** false-dropped `COMMANDS→faction` because Contract 4 only checked `graph/nodes/characters/` (the factions existed all along). Fixed: COMMANDS accepts character OR faction/house targets. (c) **`refine-v1-edges.py` never passed `slug_category_index`** → category-based contracts never fired. Fixed.
- **Edge re-validation + v1.2 APPLIED (Matt's "re-resolve + re-validate, not re-extract"):** re-ran refine with the fixed validator → applied to **`graph/edges/edges.jsonl` = 3,825** (was v1 3,842). 16 faction-COMMANDS recovered, 17 wrong rows dropped, 3 RULES→COMMANDS retyped. Clean schema preserved. Re-resolve was a no-op (nodes never missing). **COMMITTED Session 72.**
- **Lesson for next time:** the health check is a **slug intersection** (staged-vs-promoted by slug), NOT a file count — a file count is exactly what produced this false alarm. 805 tests green.
- **Resolved this session:** ① v1.2 applied + committed. ② net-new "promotion" CANCELLED — all 8 are singular/variant **dups** of existing canonical nodes (andals/dornishmen/free-folk/war-of-the-five-kings/stormlanders/lhazareen/lyseni), not promotable. ③ `lord-tywin` = a real ship artifact (Cersei's dromond), NOT a mis-type; the bad edge referencing it was correctly dropped — no node action.
- **Resolver pass DONE (2026-05-26, edges v1.3):** title-person disambiguation in `stage4_name_resolver.py` (a title-prefixed name that exact-matches a NON-character node now prefers the character via a char-restricted ladder; `resolved-title-person` rung) + `CAPTAIN_OF`/`CREW_OF` target-not-character contract. Applied to `edges.jsonl` (3,825→3,811): remapped 6 collision slugs, dropped 2 mis-typed CAPTAIN_OF. 814 tests green.
- **Still open (updated S73):** worktrees REMOVED; scripts folderization DEFERRED (low value / high import-coupling risk); 27 comention scripts KEPT (revival recall lever — do NOT re-propose archiving); scratch left tracked per Matt. Deferred levers: **skeleton-untrack** (7,180 tracked stale `skeleton/*.node.md`, entangled w/ ~24 promotion scripts — its own decision); resolver alias completeness for S67 unresolved/ambiguous endpoints (`progress/continue-prompts/2026-05-23-stage4-pass1-finishing.md`). Edge enrichment gate-opener: `progress/continue-prompts/2026-05-25-stage4-locator-grounding.md`.

### DECIDED: Stage 4 pivots to a Pass-1-derived deterministic edge pipeline (2026-05-22, Session 65)
- **Decision:** Replace the wiki-chapter-summary **comention** pass with a pipeline built on **our own Pass 1 extractions**. The extractions already contain a `## Relationships Observed` table (pair + evidence) per chapter — use them. Python does parsing + verbatim-locating + common-hint typing; the LLM only **labels** the residual free-text hint with a locked-vocab edge type.
- **Why:** primary-text source (vs secondary wiki summaries); removes the LLM's hardest job (hunting relationships in prose — the source of the ~5% violations / ENCOUNTERS failures / KNOWS sprawl / type-invention); replaces the single biggest Stage-4 sink (29,259 wiki-summary candidates); adds traceable `file:line` citations; and **collapses LLM/API usage** to a small tail (no more rate-limit walls / heavy bulk runs).
- **Pipeline:** PARSER (tables→candidates) → LOCATOR (verbatim quote + `file:line`) → TYPER (deterministic phrase→vocab map; Haiku only for the novel tail) → CONFORM inline.
- **Wiki-comention:** DEPRECATED. 130 done files → stamp **in-data** (`status: superseded`, `superseded_by: pass1-derived`, `do_not_promote: true`) — NOT dir-archiving (archiving has been contention-prone because "archived" lives in folder names; provenance must live in the data — same root cause as the schema-mixing problem).
- **Design doc:** `working/stage4-pass1-derived-edges-design.md`. **Continue:** `progress/continue-prompts/2026-05-22-stage4-pass1-derived-edges.md`.
- **Status:** direction DECIDED + Matt-endorsed; build not started. Session-65 findings carried in the continue prompt (24 skipped files from a dual-run, run-summary.json overwrite bug, single-instance guard, provenance stamp).

### OPEN: Storage Format — Pure Markdown vs. Graph DB
- **Question:** Does the graph live as pure markdown files with edges represented as YAML/frontmatter references, or do we use a lightweight graph DB (Neo4j, SQLite with graph extensions)?
- **Leaning:** Start with pure markdown. The context base pattern works well for agentic access. Graph DB can come later if query complexity demands it.
- **Trade-off:** Markdown is portable, version-controlled, and readable by Claude Code natively. Graph DB gives real traversal queries but adds infrastructure.

### DECIDED: Wiki Ingestion Scope — Full Crawl, Then Triage
- **Decision (2026-04-13):** Scrape the entire AWOIAF wiki once (~17,952 pages, ~5–6 hrs, ~1–2 GB), store as a *reference layer* in `sources/wiki/` (gitignored). Pass 2 (wiki-ingester) decides what gets promoted into `graph/nodes/` with proper `first_available` spoiler tags.
- **Rationale:** Targeted scraping required us to predict relevance up front. Full crawl is a one-time cost (~5 hrs, ~1.5 GB) and lets us refine classification rules against a static cache for free. Cache + resume means the crawl is interruption-tolerant. The graph is still curated — only the *source layer* is exhaustive.
- **Open downstream question:** How does Pass 2 decide what to promote? Likely a combination of (a) categories the page belongs to, (b) whether the page subject appears in any chapter extraction, (c) page length / infobox richness as a quality signal. To be designed when Pass 2 prompt is written.

### OPEN: Descriptive Chapter Title Mapping
- **Question:** AFFC and ADWD use descriptive chapter titles (THE PROPHET, REEK, THE UGLY LITTLE GIRL) that map to known characters. Should the extraction system normalize these to the character's real name or preserve the title?
- **Leaning:** Preserve the title in the filename and frontmatter, but add a `real_identity` field in frontmatter. "THE UGLY LITTLE GIRL" → `real_identity: Arya Stark`. This preserves GRRM's thematic intention (Theon losing his identity as "Reek") while keeping the graph navigable.
- **Note:** This matters for the voice analysis pass — "Reek" chapters have a fundamentally different internal voice than "Theon" chapters even though it's the same character.

### DECIDED: Chapter Splitter — Source Format
- **Decision:** Source files are plain .txt (converted from EPUB). Splitter targets .txt input.
- **Location:** `sources/raw/` contains GoT.txt, ACOK.txt, ASOS.txt, AFFC.txt, ADWD.txt

### DEFERRED: Spoiler Gating to Post-First-Release (2026-04-27)
- **Decision (2026-04-27):** `first_available` field is **deferred**. Optional in v1 nodes; existing values may be wrong/missing/inconsistent. Do not invest context reasoning out individual values. Backfill via deterministic script after first release.
- **Supersedes prior DECIDED rule** ("required on every node from the start; not retrofittable") which was overturned mid-Stage-2 review when schema-correctness remediation was projected to consume too much context for too little payoff. The wiki cite_ref data is rich enough that a deterministic backfill is cheap once we stop trying to enforce per-node consistency during extraction.
- **What this changes:** wiki-ingester drops the "agent self-corrects to `always available`" rule. Validator does not enforce `first_available`. CLAUDE.md and architecture.md updated. Tyrion/Varys (Stage-2 sample bugs) nulled rather than manually patched.
- **What this preserves:** the wiki data sources (infobox Books field + cite_ref anchors) remain documented in architecture.md so the backfill script can still use them.

### DECIDED: Track B (Wiki Parser) Before v3 Schema Review
- **Decision (2026-04-25):** Build the wiki infobox parser (Track B) before doing a schema review of the v3 Pass 1 output and before scaling v3 to ACOK/ASOS/AFFC/ADWD.
- **Rationale:** Track B surfaces schema signals that an isolated v3 review cannot:
  - **Entity type boundaries** — wiki categories are an external taxonomy. Mismatch with the 12 Pass 1 categories is a schema signal.
  - **Relationship/edge shape** — infobox fields (`spouse`, `father`, `liege`, `culture`, `religion`) define the graph's relationship vocabulary. Gaps in Pass 1's relationship extraction surface here.
  - **`first_available` mechanics** — `cite_ref` chapter anchors are the spoiler-gating primitive. The parser proves whether the encoding is reliable.
  - **Schema redundancy** — if the wiki provides house words / sigils / seats reliably, Pass 1 doesn't need to extract them. Track B can *shrink* the Pass 1 schema.
- **Cost asymmetry:** Doing schema review first risks discovering Track B reshapes it → 272 chapters (ACOK + ASOS + AFFC + ADWD) re-run. Doing Track B first costs a few days of already-queued work.
- **Continue prompt:** `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md` (now includes this rationale at the top).

### DECIDED: Extraction Pass Order
- **Decision:** Six passes in sequence: Mechanical → Wiki → Voice/Perception → Foreshadowing → Theory-Informed → Discovery
- **Rationale:** Each pass builds on the structured outputs of prior passes. Cross-chapter analysis (Passes 3+) requires the chapter-level extractions from Pass 1 as input.

---

## Ideas & Backlog

> Capture every idea here, even half-formed ones. Tag with priority: HIGH, MEDIUM, LOW, SOMEDAY.

### HIGH
- [ ] Write the chapter splitter script (agent prompt ready)
- [ ] Run Pass 1 on AGOT as proof of concept
- [ ] Write Pass 2 wiki ingestion agent prompt
- [ ] Create theory seeds file (top 20-30 theories with confidence tiers)

### MEDIUM
- [ ] Design the trigger table schema (what columns, what routing logic)
- [ ] Write Pass 3 voice analysis prompt — include the cross-POV perception dimension (how Character X is perceived by Character Y's POV vs. their own self-perception)
- [ ] Write Pass 4 foreshadowing prompt — agent receives the foreshadowing events list and scans chapter extractions for matches
- [ ] Design the node file schema (what does a single entity file look like in `graph/nodes/`)
- [ ] Build convergence map for Oldtown as proof of concept

### LOW
- [ ] Explore fan fiction generation as a downstream use case — voice profiles + relationship graph + location descriptions = grounded creative generation
- [ ] Portfolio README and demo design
- [ ] Consider MCP server for programmatic graph access
- [ ] Explore cybersecurity knowledge graph as a parallel project using the same architecture

### SOMEDAY
- [ ] Graph DB migration if markdown doesn't scale
- [ ] UI for graph exploration (React app?)
- [ ] Automated theory confidence scoring based on evidence density
- [ ] Ingest theory content from YouTube transcripts (Alt Shift X, Glidus, etc.)
- [ ] Community contribution pipeline — let other ASOIAF nerds submit nodes/edges through PRs

---

## Session Log

> Newest first. One entry per work session. **Strict 5-entry max** (CLAUDE.md rule #8): when a 6th lands, the oldest archives to `history/worklog-archives/archiveNNN.md`.

### Session 84 — Edge-modeling Plate 3: audit loop built, pipeline validated, full sweep HELD (resumable) (2026-06-06 → 2026-06-07)

**Model:** Opus 4.7 orchestrator; `script-builder` (Sonnet) for all pipeline/cleanup/hardening tracks; `general-purpose` (Opus) for the independent alignment audit. **Detail:** `history/session-details/session-084.md`. **Commit:** this endsession commit.

**Audit loop (NEW, codified):** two reusable prompts — `working/edge-modeling/audit-repo-reporter-prompt.md` (in-repo agent, gathers facts → `SESSION-LOG.md`) + `audit-alignment-auditor-prompt.md` (fresh session, judges vs design intent → ON-COURSE/DRIFT/NO-GO verdict that gates the next plate). Runbook: `working/runbooks/edge-modeling-audit-loop.md`. An independent Opus auditor blessed the Plates 0–2.5 block = **ON COURSE** (independently recomputed edges.jsonl=3811, canonical_type_count=165, normalizer flips=10, 0 canonical writes).

**Staged cleanups (zero graph writes):** Track A drift-reclassify — 12 `event.battle`→`meta.chapter` candidates (TWoW/ASOS chapter articles misfiled), 0 affected edges. Track B collision-merge — 6 near-dup event groups (4 high-conf auto; `conquest-of-dorne` = book-vs-event, don't-merge → reclassify book to object.text; `tourney-at/of-maidenpool` needs wiki check), 0 affected edges. Plate 2.5 inventory — `scripts/event-node-inventory.py` → reuse lookup (1,033 keys / 359 reuse-eligible / 12 drift flagged).

**D8 (NEW design decision):** reify on n-ary STRUCTURE, not event TYPE — clean dyads (Jaime/Aerys, Tyrion/Tywin) stay direct edges; only contested/multi-participant events reify. Shrinks node-minting to near-zero. Recorded in design doc §3 (+ D3 RE-EXAMINED note: Tywin/Purple-Wedding nodes DO exist, just unlinked).

**Plate 3 pipeline:** `scripts/edge-reify-backfill.py` built + validated on a 12-event mini-batch ($0.81) — D8 gate, D7 causation, multi-chapter dedup, reuse-before-mint, group/faction AGENT_IN, Contract 10 (68/68) all pass. Found + fixed a supersede false-positive bug (added chapter-overlap requirement; mini-batch 33→12, re-validated). Runner HARDENED (code-only): fail-fast on rate wall (<~90s, no retry-burn), incremental per-event flush, `processed-events.jsonl` ledger, `--resume` (verified 0 duplicates via dry-run + mock-wall).

**Incident (postmortem in detail file):** an overnight unattended full sweep was killed ~6 min in by the rate wall, then sat in retry/backoff burning usage before the fail-fast fix existed. Lesson → fail-fast + resumability are mandatory for long `claude -p` passes.

**Revised scope/cost:** dry-run enumerated **~2,056 trigger-family candidate events** (vs the 200-300 estimate); real sweep cost ~$50-160. Recommend a cost-bounded **calibration chunk** before committing to the full run.

**Graph integrity:** `edges.jsonl`=3811, 0 nodes minted into `graph/`, `git status graph/` clean — untouched throughout.

**What's next:** → `progress/continue-prompts/2026-06-07-edge-modeling-plate3-resume.md` (**Opus 4.7** — see addendum; attended, calibration chunk first). Then Reporter → fresh Auditor → Plate 5 gated merge. Plate 5 folds in the staged cleanups + Plate 4 (Haiku bulk) + the 3 S77 core-cleanups. Full Plate 3 status report in `working/edge-modeling/SESSION-LOG.md`.

**Post-endsession addendum (2026-06-07, same session — Plate 3 agent now RUNNING in a separate window):**
- **`--all` selective-gate bug found + flagged OPEN (NOT fixed).** The overnight `--all` run minted narrative micro-beat hubs (`departure-at-daybreak`, etc.) → the D8/Q1 selective gate is not enforced in the `--all` path (it IS in `--batch`); the dry-run stub bypassed it so it was never verified. That stale partial (`plate3-full/`) was EXCLUDED from git as contaminated. Next session must fix+verify the gate, `rm -rf plate3-full/`, then run. Recommended model bumped Sonnet→**Opus 4.7** (session now leads with the gate-fix reasoning).
- **Canonical auto-resume wrapper spec** added to the resume prompt (reuse `stage4-run-forever.sh` / `stage4-events-bulk-run.sh` patterns: sleep-until-reset, stop-file, MAX_ITER, short inter-batch pacing, fail-fast + graceful exit, internal `claude -p` cap ~5). Directly prevents a repeat of the overnight retry-loop window-burn.
- **Memory entry NEW:** `project_edge_modeling_reification_direction` — captures the current edge strategy + how the dead branches (wiki-comention/Pass-1-spine/Events-Haiku/enrichment) relate, so direction can't be lost.
- **Repo audit queued (post-Plate-3):** → `progress/continue-prompts/2026-06-07-repo-audit-strategy-reconciliation.md` (**Opus 4.7**) — reconcile 84 sessions of strategy sediment, fix stale worklog checkboxes, archive superseded continue prompts, consolidate memory. Linked in todos.md (HIGH, Doc Hygiene). Run it AFTER Plate 3/5 settle.
- Commits this session-tail: `8aa595bc1` (S84 endsession), `d13fd2c8d` (gate-bug OPEN + Opus), `3b06ea0cb` (wrapper spec), `c22d1181d` (audit-session capture). The live Plate 3 agent owns `scripts/edge-reify-backfill.py` + `plate3-full/` (left uncommitted/untouched here).

### Session 83 — Edge-modeling reification Plates 0+1+2 shipped (D2 resolved) (2026-06-05)

**Model:** Opus 4.7 orchestrator. Plate 0 → `script-builder` (Sonnet). Plate 1 → `general-purpose` (Sonnet). Plate 2 → `general-purpose` (Opus, analysis + D2 decision). **Detail:** `history/session-details/session-083.md`. **Commits:** `5bc168b4d` (Plate 0+1), `03442d0a0` (Plate 2 + continue prompts), `a7046ec58` (SESSION-LOG closing summary), this endsession commit.

**Context:** Third Session-83 work-block in calendar-day 2026-06-05, following S83/path-rename (earlier). This block executed the full "safe first move" from `working/edge-modeling/edge-modeling-reification-design.md` §9 Decision #1 — Plates 0+1 in parallel, then Plate 2.

**Plate 0 (deterministic, $0):** `scripts/edge-direction-normalizer.py` + `scripts/aerys-slug-merge.py`. Normalizer flagged **10 inverted edges** out of 3,811 (cressen↔melisandre KILLS, arya↔sandor CAPTURES, tyrion↔shae BETRAYS, +7) using an edge-type-aware reverse-signal lexicon — experience/state types (PRISONER_OF, SERVES, RESENTS) explicitly excluded since their passive phrases are semantic, not inversions. 3,800 kept, 1 flagged (mutual kill). Aerys merge repointed 3 phantom `aerys-targaryen` edges to canonical `aerys-ii-targaryen`. All output staged in `working/edge-modeling/` — `graph/edges/edges.jsonl` UNTOUCHED.

**Plate 1 (doc-only, $0):** `.claude/agents/mechanical-extractor.md` line 188 head rule (Column A = semantic agent, never grammatical subject/POV); line 136 optional Events & Actions role sub-bullets (Agent/Patient/Instrument/Location/Instigator/Outcome). Parser at `scripts/stage4-pass1-extra-tables.py:521-537` VERIFIED sub-bullet-safe (only matches `^\d+\.\s+`). `reference/architecture.md`: `AGENT_IN` + `VICTIM_IN` (Person/House → event.*) added line 237-238, `COMMANDS_IN` widened to cover orderer/instigator role, vocab 163→165 at line 551. `scripts/stage4-type-contract-validator.py` Contract 10 added: AGENT_IN/VICTIM_IN with non-event target → DROP.

**Plate 2 (analysis, $0):**
- **2a Pass-1 event coverage** — `scripts/plate2-event-coverage.py` walks all 344 extraction files, parses `## Events & Actions` bold titles, joins against `graph/index/events/` chapter-evidence + slug exact-match. Output: `working/edge-modeling/plate2-event-coverage.{md,json}`. Counts: **8,384 total Pass-1 event entries** / **8,317 distinct titles (floor)** / **1 exact title→slug match** / **8,316 distinct titles needing mint (floor)**. Only **38 of 371 event nodes** (10%) have ANY Pass-1 chapter linkage — the rest are wiki-derived nodes built from the Wars & Conflicts column, which only catches historical-event names. The chapter-evidence join CAN'T be Plate 3's primary binding mechanism.
- **2b `graph-query.py` traversal check** — `working/edge-modeling/plate2-graphquery-traversal.md`. Code-read + live probes. `cmd_path()` (`scripts/graph-query.py:794-809`) computes 2-hop bridges via untyped neighbor-set intersection over `edges.jsonl`. No node-type filter, no edge-type filter. Live probes: `--path eddard-stark robb-stark` already bridges through `winterfell` (location.castle) and `house-frey` (house.*); `--path robb-stark roose-bolton` returns 12 bridges including non-character intermediates. **Person→event→person traversal will work transparently once Plate 3 role edges land.** Zero engineering changes needed.
- **D2 RESOLVED — option (a) Replace.** Recorded in `working/edge-modeling/edge-modeling-reification-design.md` §3 (new "D2 RESOLVED" subsection after D7). Reification is sufficient — `--path` traverses person→event→person via the same untyped 2-hop mechanism that already handles location/house bridges. No materialized agent→patient dyad: option (c) Project would re-introduce the underdetermination problem D2 was designed to kill (which participant becomes the canonical `source`?). Superseded person→person binaries marked `superseded_by` (NOT deleted; CLAUDE.md hard rule).
- **Spot-check verdicts:** Bran's defenestration → **NEEDS MINTING** (no node exists). Tywin's privy death → **REUSE `assassination-of-tywin-lannister`** (node exists, chapter linkage broken, re-bind needed). Purple Wedding → **REUSE `purple-wedding`** (same — node exists, chapter linkage broken). The design doc §3 D3's claim "Purple Wedding poisoning and Tywin's privy death have no hub" is FACTUALLY WRONG — both nodes exist; what's missing is the chapter→event linkage in their index. Plate 3 design needs updating for this.

**Unexpected findings:**
1. 90% of event nodes have no Pass-1 chapter linkage. The chapter-evidence index built from Raw Entity List > Wars & Conflicts catches historical names only, not narrative beats. Plate 3 must mine titles directly.
2. The "needs minting" floor of ~8,316 distinct titles is only realistic if Plate 3 reifies EVERY narrative micro-beat ("Departure at daybreak", "Ride back toward Winterfell"). A selective Plate 3 (kill/betray/attack/poisoning beats only) would be much smaller. **NEW Plate 3 design question:** reify-all vs reify-selective. Out of scope for Plate 2.

**Decisions:**
- D2 → option (a) Replace (recorded).
- Plate 3 may NOT generate canonical agent→patient dyads — events are nodes, full stop.
- Plate 3 design doc needs a §3 D3 correction (named-event coverage exists more than D3 claimed; mint-scope is narrative micro-beats + a handful of named cases).

**Files touched (this block):**
- CREATE `scripts/plate2-event-coverage.py`
- CREATE `working/edge-modeling/plate2-event-coverage.{md,json}`
- CREATE `working/edge-modeling/plate2-graphquery-traversal.md`
- APPEND `## D2 RESOLVED` subsection to `working/edge-modeling/edge-modeling-reification-design.md` §3
- APPEND Plate 2 section to `working/edge-modeling/SESSION-LOG.md`
- (this entry) `worklog.md` + archive017.md (Session 79 moved)
- Did NOT touch `graph/edges/edges.jsonl`, `graph/nodes/`, Plate 0 staged outputs, or Plate 1 doc commits.

**What's next:** Three continue prompts written, each self-contained:
- → `progress/continue-prompts/2026-06-05-edge-modeling-plate-3-backfill.md` (Sonnet; HELD on Matt Q1 reify-all-vs-selective + Q2 fuzzy-reuse-vs-mint-floor — both questions documented inline in PRE-WORK DECISION block)
- → `progress/continue-prompts/2026-06-05-edge-modeling-plate-4-haiku-disposition.md` (Opus for bucketing, Sonnet for filter pass; HELD on Matt go)
- → `progress/continue-prompts/2026-06-05-edge-modeling-plate-5-merge.md` (Sonnet for deterministic merge; HELD on Plates 3+4 staging + Matt before/after sign-off — this is the only irreversible plate)

Plate 4 (1,617 Haiku bulk re-bucketing) absorbs the S81 Events Haiku NO-GO. Plate 5 also folds in the 3 S77 core-cleanups (2 cersei↔tyrion LOVES drops, ~22 ASSAULTS→ATTACKS retypes, OWNS→BONDED_TO for direwolves/dragons). Design-doc §3 D3 needs a stale-mark before Plate 3 runs (named-event nodes mostly EXIST; what's missing is chapter linkage).

### Session 83 — Move `/tmp` paths into `~/source/claude-cwd/` hierarchy (2026-06-05)

**Model:** Opus 4.7 (orchestrator + execution; no agents delegated). **Detail:** none (pure path-rename hygiene). **Commit:** this endsession commit.

**Changes made (path refactor; no behavior change):**
- NEW dirs: `~/source/claude-cwd/` (empty `cwd=` for `claude -p` subprocesses; sibling of repo, no parent `CLAUDE.md` to defeat the cost trick) + `~/source/claude-cwd/tmp/` (for stop-files + per-run logs).
- `scripts/stage4-tail-classifier.py`: `cwd="/tmp"` → `cwd=CLAUDE_P_CWD` constant; `STOP_FILE` uses `os.path.expanduser` over the new path. `scripts/events-drift-audit.py`: cosmetic — comments / `judge_cwd` metadata / APPLY log line (inherits the cwd from `TC.invoke_claude`).
- 13 active shell scripts (`extract.sh`, `weirwood.zsh`, `launch-extraction.sh`, `run-extraction-wave.sh`, `run-extraction-all.sh`, `stage4.sh`, `stage4-run-forever.sh`, `stage4-events-bulk-run.sh`, `stage4-haiku-loop.sh`, `stage4-haiku-run-forever.sh`, `stage4-haiku-smoke-finish.sh`, `stage4-tail-bulk-forever.sh`, `wiki-pass2.sh`): every `/tmp/{extraction,stage4,wiki-pass2,haiku-smoke}-*` replaced with `$HOME/source/claude-cwd/tmp/...`.
- `tests/test_stage4_bulk_run_apparatus.py`: assertion + comments; 42/42 pass.
- `reference/extraction-commands.md`, `working/runbooks/{stage4-events-haiku-bulk, mechanical-extraction-howto, wiki-pass2-orchestration, pass1-auto-advance-mode}.md`, `progress/continue-prompts/{2026-05-17-stage4-bulk-watcher, 2026-05-16-stage4-bulk-resume}.md`, `BEFORE-LEAVE-RESUME-2026-05-28.md`, worklog S79 line, memory `reference_llm_pass_via_claude_p.md`.

**Skipped (per "except archived files" rule):** `scripts/archive/`, `working/runbooks/archive/`, `progress/continue-prompts/archive/`, `working/session-results/` (frozen historical), `EDGE_INVENTORY_REPORT.md` (one-time report). Unrelated `/tmp` references untouched: `bucket_dir/tmp` (Pass-2 bucket-internal subdir, not `/tmp`); `/tmp/test/`, `/tmp/edge-inventory/`, `/tmp/parse_rels.py` example/throwaway paths.

**Decisions:** (1) Two `/tmp` use cases share the new root: `~/source/claude-cwd/` for the `claude -p` cwd cost trick (~49% cheaper by skipping the repo CLAUDE.md cold-load); `~/source/claude-cwd/tmp/` for stop-files + per-run logs. (2) Verified nothing was in flight in `/tmp` at time of change (no processes, no stop-files, no log files) — pure code rename, nothing on disk moved. (3) Shell uses `$HOME/source/claude-cwd/tmp/...` (POSIX-portable inside quoted strings); Python uses `os.path.expanduser("~/source/claude-cwd/tmp/...")`. Test assertion now uses `os.path.expanduser` so it doesn't hard-code Matt's homedir.

**What's next:** No new track from this session — the path refactor is self-contained and complete. Queued prior-session work is unaffected: → `progress/continue-prompts/2026-06-04-edge-modeling-cleanroom-execution.md` (S82, **Opus 4.7**) is the most recent live track; `progress/continue-prompts/2026-06-01-events-bulk-escalation-pick.md` (S81) partially superseded by S82's cleanroom reframe; 3 core-cleanups still gated on Matt since S77.

### Session 82 — Edge/event modeling: cleanroom decision doc + two-way synthesis (2026-06-04)

**Model:** Opus 4.7 (orchestrator + cleanroom analyst). **Detail:** `history/session-details/session-082.md`. **Commit:** `2d971c1c9` (S82 + bundled S80/S81 backlog) + this endsession commit (continue prompt + session-details + todos linkage).

**Changes made (analysis artifacts; no code, no graph, all untracked at repo root):**
- NEW `EDGE_INVENTORY_REPORT.md` (281KB) — full inventory of current edge-modeling state; input to the analysis.
- NEW `EDGE_INVENTORY_ANALYSIS_PROMT.md` (14.8KB, typo in filename) — cleanroom brief: §0 mission, §1 conceptual foundation (relations vs events, arity, underdetermination, instigator/executor causative chain, the two fix families, §1.7 diagnostic heuristic, §1.8 grammatical-subject trap).
- NEW `EDGE_MODELING_DECISION.md` (37KB) — first decision pass, repo-access allowed.
- NEW `EDGE_MODELING_DECISION-cleanroom.md` (18.7KB) — fresh-context pass, report + brief only, no repo. First line records Write-denied; doc printed inline and captured. Empty `.err` sidecar.

**Synthesis (two-doc convergence — the most important signal of the session):** Both docs diagnose the same root cause: **grammatical-subject leakage at the Pass-1 extraction layer** (`mechanical-extractor.md:176-178`: no head rule on the `| Char A | Relationship | Char B |` table; `python-map` locks direction by column position) compounded by **structurally empty event hubs** (371 `event.*` nodes exist per `graph/index/events/_summary.json`; Red Wedding has only 3 outbound edges, the audit's canonical case). Both prescribe the same fix shape: **reify** the multi-party set-pieces (killings-at-named-occasion, sieges, sacrifices, the wedding/tourney ceremony family, `CONSPIRES_WITH`, `VIOLATES_GUEST_RIGHT`) via role edges (`AGENT_IN`/`VICTIM_IN`/`COMMANDER_OF`/`INSTRUMENT_IN`, participant→event); **canonicalize** the dyadic acts (`ATTACKS`/`DEFEATS`/`DUELS`/`HEALS`/`RESCUES`/`BETRAYS`) under one head rule (semantic agent, never grammatical subject, never POV); **leave true binaries alone** (`PARENT_OF`, kin shortcuts, emotion/perception, spatial endpoints, prophecy/narrative/evidentiary). Cleanroom-specific disagreements with the first doc: (1) `SPOUSE_OF`/`BETROTHED_TO`/`SWORN_TO` are binary STATES, not events — keep the state, reify the ceremony separately; (2) `HEALS`/`RESCUES` over-reified — canonicalize; (3) `LOCATED_AT` is binary.

**Recommended move (NOT YET DECIDED — awaits Matt's call):** Don't trigger a Pass-1 rerun (all-Opus, 344 chapters — its own project). Instead: (a) **reframe S81's Events Haiku escalation pick through the cleanroom lens** — Haiku's measured drift on `TRAVELS_TO`/`TRAVELS_WITH`/`LOCATED_AT` is the **canonicalize bucket**, NOT the reify bucket; path (B) "promote long-tail-only" sharpens to "promote rows that anchor to existing `event.*` nodes; hold rows targeting persons/venues for canonicalize work"; (b) **backfill role edges onto the 371 existing event nodes** using the Haiku run's `**title**` grouping as ready-made clustering (audit path C, ~$2-5; S80 analysis flagged as highest-leverage move on the table); (c) **add the head rule + `## Events Observed` table to the Pass-1 prompt as a doc change now** — no rerun trigger, benefits the next Pass-1 invocation whenever that happens.

**Decisions:** None binding yet — analysis-only. The Events Haiku v2.0 promotion chain (S81's open question) is now coupled to this decision: the cleanroom lens reshapes which Haiku rows promote vs. hold vs. drop.

**What's next:** → `progress/continue-prompts/2026-06-04-edge-modeling-cleanroom-execution.md` (**Opus 4.7**) — verification + planning prep, four execution plates (A-doc / A-schema / B-backfill / A-pick) to Matt as approve/hold/reject. No spend, no execution. **Partially supersedes** `2026-06-01-events-bulk-escalation-pick.md` (the S81 A-E choice is no longer free under the cleanroom lens). If Matt approves any plate → mechanical work follows on Sonnet 4.6. Still gated on Matt: 3 core-cleanups carrying since S77 (drop 2 `cersei↔tyrion` LOVES; ~22 `ASSAULTS`→`ATTACKS`; merge-time `OWNS→BONDED_TO`).

### Session 81 — Events Haiku bulk drift audit → NO-GO (borderline); fresh-eyes corrected the framing (2026-05-31 → 2026-06-01)

**Model:** Opus 4.7 (orchestrator + audit-script author) + general-purpose subagent (cold fresh-eyes review) + Sonnet 4.6 (judge via `claude -p` cwd=/tmp). **Detail:** `history/session-details/session-081.md`. **Commit:** this endsession commit.

**Changes made:**
- NEW `scripts/events-drift-audit.py` (sha `576cc815649c`, 327 lines, throwaway single-purpose) — reuses canonical `render_classify_prompt` / `invoke_claude` / `parse_batch_response` / `align_batch_output` from `stage4-tail-classifier.py` for byte-identical prompt parity with Haiku's bulk run; custom stratified sampler (≥3 of each of 6 named structural types; remainder proportional by book); seed=531; `--dry-run` default, `--apply` required for spend.
- NEW `working/audits/events-haiku-bulk-2026-05-29/{audit-sample-50.jsonl, audit-sample-50-judged.jsonl, cross-model-audit.md}` — all carry metadata header (judge_model, judge_cwd, sample_seed, prompt_sha, script_sha, timestamps, judged_count, cost). cross-model-audit.md amended with fresh-eyes banner at top.
- NEW `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/step-01-status.md` (amended with No-Go + fresh-eyes correction).
- NEW `progress/continue-prompts/2026-06-01-events-bulk-escalation-pick.md` — next-session entry point, lists 5 escalation paths.

**Audit result:** Stratified 50-row sample (seed=531); Sonnet 4.6 judge, $0.93 total. Triple-level **48 %** (24/50; floor 70 %), pair-level **56 %** (28/50; floor 85 %). 22/50 Haiku emits rejected by Sonnet. Named-type breakdown: TRAVELS_TO 17 % (1/6), TRAVELS_WITH 0 % (0/4), LOCATED_AT 20 % (1/5), COMMANDS 50 %, SERVES 67 %, REVEALS_TO 67 %. Prompt SHA byte-identical to Haiku bulk run (`d31ca56c4768`). Methodology bugs: **none** (verified by fresh-eyes subagent).

**Fresh-eyes pressure-test corrected the framing** (Matt didn't trust the 48 % number; subagent was instructed to read rules cold, then cold-judge the 22 REJECTs, then locate the smoke session):
- ~11 of 22 REJECTs **are clear Haiku drift** (Rule 4a hint-as-evidence, V5-R2 quote-doesn't-support-both-endpoints, Rule 12 co-presence) — Sonnet correct.
- **~3-4 are clear Sonnet over-rejections** (judge_idx 2 Edmure TRAVELS_WITH Lymond "on the march"; 6 Jaime TRAVELS_TO Harrenhal "when he came to Harrenhal"; 14 Ramsay REVEALS_TO Roose dispatched riders; 16 Haldon TRAVELS_WITH Duck co-riders).
- ~7-8 genuinely ambiguous, most lean V5-defensible-reject.
- **The audit's S69 smoke citation was WRONG** — actual session is **S77**, and S77 measured *hand-read precision on fresh candidates* (Matt's eye), NOT *Sonnet-judges-Haiku-emit on stratified emits-only*. Different metric on different sample shape. The apparent contradiction between the smoke (~85-90 %) and this audit (48 %) is **measurement-shape, not drift**.
- Adjusted triple agreement crediting all over-rejections + all ambiguous ≈ 56-70 % — at or below the 70 % gate.

**Decisions:** (1) **No-Go stands but is borderline**, not catastrophic. Promoting `_events-haiku-bulk/` as v2.0 would inject systematic noise into the structural-edge types (TRAVELS_TO/WITH/LOCATED_AT), where Haiku's hint-as-evidence failure mode concentrates. (2) **The 7-step promotion chain is halted at step 1** until Matt picks an escalation path. (3) **Audit script is THROWAWAY** — single-purpose, not generalized into a framework (per chain spec); reused canonical prompt code for parity. (4) **Cost discipline observed** — `--dry-run` default, `--apply` only after explicit Matt-go ($0.93 total spend).

**What's next:** Matt picks one of the 5 escalation paths in `cross-model-audit.md §6`: (A) re-run on Sonnet (~$340), (B) promote long-tail-only, (C) Sonnet-filter named-type rows only (~$2-5, **audit's recommendation**), (D) tighten Haiku prompt to v6 + re-run, (E) abandon Events for v2.0; wait for Dialogue. → `progress/continue-prompts/2026-06-01-events-bulk-escalation-pick.md` (**Opus 4.7** for the pick, then Sonnet 4.6 for whatever mechanical work follows). Stale: the 7 step prompts at `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/02-06-*.md` likely need rewrites once path is picked, or supersede the chain if (E). Still gated on Matt: 3 core-cleanups (drop 2 `cersei↔tyrion` LOVES; ~22 ASSAULTS→ATTACKS; merge-time OWNS→BONDED_TO).

---

> Session 80 archived to `history/worklog-archives/archive017.md` (archive017 now 3/5)
> Session 79 archived to `history/worklog-archives/archive017.md` (archive017 now 2/5)
> Session 78 archived to `history/worklog-archives/archive017.md` (archive017 started — 1/5)
> Session 77 archived to `history/worklog-archives/archive016.md` (archive016 now full at 5/5)
> Session 76 archived to `history/worklog-archives/archive016.md` (archive016 now 4/5)
> Session 75 archived to `history/worklog-archives/archive016.md` (archive016 now 3/5)
> Session 74 archived to `history/worklog-archives/archive016.md` (archive016 now 2/5)
> Session 73 archived to `history/worklog-archives/archive016.md` (archive016 started — 1/5)
> Session 72 archived to `history/worklog-archives/archive015.md` (archive015 now full at 5/5)
> Session 71 archived to `history/worklog-archives/archive015.md` (archive015 now 4/5)
> Session 70 archived to `history/worklog-archives/archive015.md` (archive015 now 3/5)
> Session 69 archived to `history/worklog-archives/archive015.md` (archive015 now 2/5)
> Session 68 archived to `history/worklog-archives/archive015.md`
> Session 67 archived to `history/worklog-archives/archive014.md` (archive014 now full at 5/5)
> Session 66 archived to `history/worklog-archives/archive014.md`
> Session 65 archived to `history/worklog-archives/archive014.md` (archive014 now 3/5)
> Session 64 archived to `history/worklog-archives/archive014.md` (archive014 now 2/5)
> Session 63 archived to `history/worklog-archives/archive014.md` (archive014 started — 1/5)
> Session 62 archived to `history/worklog-archives/archive013.md` (archive013 now full at 5/5)
> Sessions 58-61 archived to `history/worklog-archives/archive013.md`
> Sessions 57-56 archived to `history/worklog-archives/archive012.md` (archive012 full at 5/5 entries)
> Session 55 archived to `history/worklog-archives/archive012.md`
> Session 54 archived to `history/worklog-archives/archive012.md`
> Session 53 archived to `history/worklog-archives/archive012.md`
> Session 52 archived to `history/worklog-archives/archive011.md` (archive011 now full)
> Session 51 archived to `history/worklog-archives/archive011.md`
> Session 50 archived to `history/worklog-archives/archive011.md`
> Session 49b archived to `history/worklog-archives/archive011.md`
> Session 49 archived to `history/worklog-archives/archive011.md`
> Sessions 44-48 archived to `history/worklog-archives/archive010.md` (full at 5 entries)
> Sessions 39–43 archived to `history/worklog-archives/archive009.md` (full at 5 entries)
> Sessions 34–38 archived to `history/worklog-archives/archive008.md` (full at 5 entries)
> Sessions 30–33 in `history/worklog-archives/archive007.md` (full at 5 entries)
> Sessions 25–29 archived to `history/worklog-archives/archive006.md`
> Sessions 22–24 archived to `history/worklog-archives/archive005.md`
> Sessions 16-21 archived to `history/worklog-archives/archive004.md`

> Sessions 8–15 archived to `history/worklog-archives/archive003.md`
> Sessions 5–7 archived to `history/worklog-archives/archive002.md`
> Sessions 0–4 archived to `history/worklog-archives/archive001.md`

---

## Principles

> Guiding principles for the project. Reference these when making design decisions.

1. **The chapter text is immutable.** Source files in `sources/chapters/` never change. Everything else layers on top.
2. **Facts before interpretations.** Mechanical extraction before analytical. Tier 1 before Tier 4.
3. **Agents propose, humans decide.** Analytical findings go to the curation queue. Matt assigns confidence.
4. **Spoiler gating is architectural.** Every node has `first_available`. This is not a feature to add later.
5. **The index and the graph are complementary.** The index routes. The graph traverses. Both are needed.
6. **Each token should be productive.** Structure exists to reduce waste — agents should read relevant, trustworthy content, not re-derive known relationships.
7. **Start with the foundation, not the flashiest feature.** Chapter files → mechanical extraction → wiki → index → graph → analytical passes. In that order.
