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
- [x] Edge-modeling reification (Plate sequence, S82-S87) — **ALL PLATES SHIPPED including Plate 5 (2026-06-09, S87).** `graph/edges/edges.jsonl` **3,811 → 4,757 (+946)**; `graph/nodes/events/` **371 → 583 (+212)**; `graph/nodes/_conflicts/` **+6** (1 aerys + 5 collision losers). Backup: `graph/edges/_regrounding/edges-pre-reification-2026-06-09.jsonl`. Phases: Plate 0 normalizer 10 flips + 3 aerys repoints; Plate 2.5 27 wiki schema retypes + 12 drift retypes + 4 high-conf collision merges; Plate 4 51 SUB_BEAT_OF + 2 DUPLICATE_OF (1 skipped — meta.chapter target); Plate 3 217 mints (`title:`→`name:` rewrite) + 897 role edges + 55 supersede stamps; S77 carryover 2 LOVES drops + 21 ASSAULTS→ATTACKS retypes. Validators: 4,725 kept / 32 dropped (all SUB_BEAT_OF empty-evidence — read-only audit, rows remain). Red Wedding smoke test ✓ (8 SUB_BEAT_OF, 2-hop participant traversal works). Followups: display-bullet regen, 32 SUB_BEAT_OF empty-quote backfill, 109 hub-review-queue triage, post-Plate-5 tracks A/B/C ($25-75). Diff doc: `working/edge-modeling/plate5-merge-diff.md`. Script: `scripts/plate5-merge.py`.

  *(historical S82-S84 detail compressed; see history/session-details/session-082.md through session-085.md.)* Plates 0+1+2+2.5 cleanups, D2 RESOLVED (Replace), D8 added (reify on n-ary structure not type), vocab 163→165 (`AGENT_IN`+`VICTIM_IN`+`COMMANDS_IN` widened), Contract 10 validator, audit loop codified.

- [~] Edge-modeling reification (HISTORICAL, S82-S84 detail) — superseded by line above; kept for archival reference of original sequence.
  Original entry: Plates 0+1+2+2.5 + staged cleanups + Plate-3 smoke: ALIGNMENT AUDIT 2026-06-06 = ON COURSE. Independent fresh-session auditor recomputed all load-bearing numbers (edges.jsonl=3811 untouched, git status on graph/ empty, canonical_type_count=165, normalizer flips=10 not 11, 371 event nodes, phantom Aerys + 12 drift nodes still unmutated) — zero canonical writes, all of D1/D2/D3/D7/D8 honored in staging, Red-Wedding smoke demonstrates the "who killed/ordered X" 2-hop fix in dry-run. Next: launch full Plate 3 after Matt resolves Q1 (reify-selective) + Q2 (fuzzy reuse) and the 4 high-conf collision merges + 12 drift reclassifications are applied at the Plate-5 gate. Verdict + per-area detail in `working/edge-modeling/SESSION-LOG.md`. **Plates 0+1+2 SHIPPED; Plate 3 unblocked (HELD).** Plate 0: head-direction normalizer flipped 10/3,811 edges + Aerys slug-merge candidate (3 edges) — STAGED at `working/edge-modeling/normalizer-{candidates.jsonl,diff.md}`, `flagged-for-review.jsonl`, `aerys-merge-candidates.jsonl`. Plate 1: Pass-1 head rule + Events sub-bullets in `.claude/agents/mechanical-extractor.md`; `AGENT_IN`+`VICTIM_IN` added + `COMMANDS_IN` widened in `reference/architecture.md` (vocab 163→165); validator Contract 10 added to `scripts/stage4-type-contract-validator.py`. Plate 2: D2 RESOLVED → **option (a) Replace** (reification sufficient; `graph-query.py --path` traverses person→event→person transparently — no materialized dyad). Coverage: 8,384 Pass-1 event entries / 8,317 distinct titles / 8,316 needs-mint floor / only 38/371 (10%) event nodes have chapter linkage. Master design: `working/edge-modeling/edge-modeling-reification-design.md` (D2 resolved in §3). Plates 3+4+5 HELD; Plate 3 has 2 new design questions surfaced by Plate 2 (reify-all-vs-selective + §3 D3 correction). NOT merged into `graph/edges/edges.jsonl` (Plate 5 gate). Session log: `working/edge-modeling/SESSION-LOG.md`. **S84 UPDATE:** Q1 RESOLVED → reify-**selective** (trigger families only); Q2 → confidence-gated fuzzy reuse-before-mint; **D8** added (reify on n-ary STRUCTURE not type — clean dyads stay direct edges). Audit loop codified (Reporter + Auditor prompts + runbook); independent auditor verdict on Plates 0–2.5 = **ON COURSE**. Plate 3 pipeline `scripts/edge-reify-backfill.py` BUILT + validated (12-event mini-batch $0.81, all gates pass) + HARDENED (fail-fast + `--resume`). **Full sweep HELD/incomplete** — overnight attempt killed by rate wall (only 37 staged minted nodes + 11 review-queue; no role edges). Revised scope ~2,056 candidate events (~$50-160) → run a calibration chunk first. RESUME: `progress/continue-prompts/2026-06-07-edge-modeling-plate3-resume.md`.
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

### Session 88 — Plate 5 recap + validation track scoped + S87 endsession gap-fill (2026-06-09 → 2026-06-10)

**Model:** Opus 4.7 (orchestrator + execution; no agents delegated). **Detail:** none (light session — wrap-up after S87 cutoff + design substance captured in the validation continue prompt). **Commits:** `cd1f362dc` (WIP gap-fill), this endsession commit.

**Context:** S87 ended abruptly mid-endsession (chat got cut off after the Plate 5 commit landed). Matt returned, asked how Plate 5 went + what the `quoted_evidence` vs `evidence_quote` field-rename was about, then asked to scope the next track ("actually using the graph to do some validation") and to make a WIP commit + push for the missed endsession steps.

**Wrap-up conversation:**
- Plate 5 recap: `edges.jsonl` 3,811 → **4,757 (+946)**; `events/` 371 → 583 (+212); validator 4,725 kept / 32 dropped (SUB_BEAT_OF empty-evidence rows remain in JSONL as read-only audit); Red Wedding 2-hop smoke passes end-to-end.
- `quoted_evidence` vs `evidence_quote`: same semantics (verbatim book quote grounding an edge); `evidence_quote` is canonical across the whole schema; `quoted_evidence` was a divergent name in Plate 4 cluster staging; fix-in-place during merge renamed 51 SUB_BEAT_OF rows (19 retained text, 32 got explanatory `plate5_evidence_note` for inference-only Pass-B/Pass-C emissions).

**Validation track scoped:** Four modes — (1) capability validation (does the new structure work; 8 probe queries on reified event hubs); (2) canonical accuracy (fact-check vs. books; partially absorbed by Track A backfill); (3) agent grounding (the real project goal — agent with `graph-query.py` as a tool answers real ASOIAF questions); (4) surprise/discovery (aggregate queries impossible pre-Plate-5). Recommendation: Mode 1 first (cheapest, isolates the graph layer; misses route cleanly to the 6 post-Plate-5 follow-up TODOs or backfill Tracks A/B/C). Mode 3 is the real test but needs Mode 1 to settle first so debugging is tractable.

**S87 endsession gap-fill (WIP commit `cd1f362dc`, pushed):**
- `working/todos.md`: EDGE/EVENT MODELING entry flipped [~]→[x] "ALL PLATES SHIPPED INCLUDING PLATE 5 (S82-S87)"; added 6 post-Plate-5 follow-up TODOs (display bullets, 32 empty-quote SUB_BEAT_OF, 109 hub-review-queue, 2 deferred collisions, donal-noye↔mag mutual-kill reverse, backfill tracks A/B/C); replaced obsolete `→ continue:` links with new validation prompt.
- `progress/continue-prompts/2026-06-09-graph-validation.md` (NEW): 4 modes, 8 Mode-1 probes, decision points listed, recommendation noted.
- `working/edge-modeling/plate3-revalidation/` (NEW): S85-era artifacts (2 minted event nodes, role-edge staging, skipped clean dyads, supersede candidates) committed for the record.
- `~/.claude/.../project_edge_modeling_reification_direction.md` (memory, outside repo): updated S84 status → S87 ship state with the 6-followup-TODO summary.

**This endsession (additional):**
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-5-merge.md` DELETED — Plate 5 shipped, prompt obsolete.
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-4-haiku-disposition.md` KEPT — its 1,617-row re-bucketing under reify lens is still part of post-Plate-5 backfill Track B; `→ continue:` link re-added under that TODO in todos.md (was accidentally removed during gap-fill edit).
- Session 83 (Edge-modeling Plates 0+1+2) archived to `history/worklog-archives/archive018.md` (archive018 now 2/5; co-located with S83-/tmp-paths).

**Out of scope (preserved untouched):** Matt's IDE edits to `progress/continue-prompts/2026-06-08-alias-and-display-design.md`; scratch deletions; `Untitled 6.rtf` deletion; `scr` untracked file at repo root.

**What's next:** → `progress/continue-prompts/2026-06-09-graph-validation.md` (**Opus 4.7** — design judgment in interpreting probe results; deterministic query work is `graph-query.py`). Matt picks Mode 1 vs straight-to-Mode-3.

### Session 87 — Plate 5 SHIPPED — first canonical write to edges.jsonl (2026-06-09)

**Model:** Opus 4.7 (orchestrator + all execution; no agents delegated). **Detail:** none (execution-heavy, design captured in `working/edge-modeling/plate5-merge-diff.md`). **Commit:** this endsession commit.

Plate 5 — the single gated step that writes all staged edge-modeling work into the canonical graph — landed successfully. Five locked-in decisions (Q1-Q4) captured ahead of execution. Matt stepped out mid-session and explicitly delegated promotion + autonomous validation ("I won't be reviewing everything you promote anyway, so promote them. then we should talk about actually using the graph to do some validation"). Net deltas: `edges.jsonl` **3,811 → 4,757 (+946)**, `events/` nodes **371 → 583 (+212)**, `_conflicts/` **+6** (1 aerys + 5 collision losers).

**What landed (in merge order):**
- Plate 0: 10 normalizer direction-flips + 3 aerys-targaryen→aerys-ii-targaryen repoints + node quarantine. 1 mutual-kill left flagged (donal-noye↔mag) per Q4=a.
- Plate 2.5: 27 wiki schema fixes (event.battle → event.wedding/feast/coronation/trial/assassination/execution/conspiracy per S86 vocab), 12 drift retypes (10 applied + 2 already-done), 4 high-conf collision merges (5 losing nodes quarantined). 2 medium/low collisions skipped per cleanup-decisions-resolved.md.
- Plate 4 cluster: 51 SUB_BEAT_OF appended + 2/3 DUPLICATE_OF applied (7 role edges repointed to wiki nodes). 1 DUPLICATE_OF skipped (`mutiny-plan-reviewed → a-storm-of-swords-prologue`: target becoming meta.chapter would violate Contract 10).
- Plate 3: 217 of 219 mints written to `events/` (2 skipped per DUPLICATE_OF); `title:` → `name:` rewrite at mint per S86 canonical surface field. 897 of 914 role edges appended (5 dropped for fuzzy-match queue per Q1=a; 12 dropped for unresolvable LOCATED_AT; 22 LOCATED_AT remapped via small fix-map per Q2=a; 7 repointed for DUPLICATE_OF). 55/55 supersede stamps applied (1 via swapped-key fallback because Plate 0 had flipped the original direction).
- S77 carryover: 2 cersei↔tyrion LOVES rows dropped, 21 ASSAULTS → ATTACKS retyped (11 stay ASSAULTS — sexual-violence canon). OWNS→BONDED_TO no-op (0 such rows).

**Validators:**
- **Type-contract validator:** kept 4,725 / dropped 32 (0.7%). All 32 drops are SUB_BEAT_OF edges with empty `evidence_quote` (Plate 4 Pass-B/Pass-C inference-only emissions; rationale-only, no quote). Rows remain in `edges.jsonl` — validator is read-only audit. **Field-name fix applied in-place** during validator review: Plate 4 staging used `quoted_evidence` instead of canonical `evidence_quote`; renamed across all 51 SUB_BEAT_OF rows (19 retained text, 32 now have an explanatory `plate5_evidence_note` field).
- **Orphan-edges audit:** node-display bullets predate Plate 5 (display bullets are pre-merge state). Net 217 fewer cat1 orphans vs 2026-05-12 baseline. Bullets NOT regenerated this session — no canonical `build-node-display-edges.py` exists; canonical authority is edges.jsonl (graph-query.py reads from there).
- **Red Wedding smoke test PASSES.** `python3 scripts/graph-query.py --neighbors red-wedding` shows 8 SUB_BEAT_OF incoming. 2-hop traversal (red-wedding ← SUB_BEAT_OF ← catelyn-is-killed) surfaces AGENT_IN (house-frey), VICTIM_IN (catelyn-stark), COMMANDS_IN (walder-frey), LOCATED_AT (twins) — all with verbatim book quotes. Reification end-to-end working as designed.

**Decisions captured (5 ahead of execution):**
- Q1=a: hub-review-queue defaults applied (0/109 minted; 5 role edges dropped for the 2 fuzzy-match queue items).
- Q2=a: built 8-slug location alias fix-map (the-eyrie→eyrie, king-s-landing→kings-landing, etc.); 10 unresolvable slugs skipped (~12 edges).
- Q3=a: 2 LOVES drops + 21-ASSAULTS retype (11 stay) + OWNS no-op.
- Q4=a: 4 high-conf collisions only; mutual-kill left flagged.
- Mid-merge DUPLICATE_OF call: skip `mutiny-plan-reviewed` because its wiki target is being retyped to meta.chapter (would violate Contract 10).

**Files modified:** `graph/edges/edges.jsonl` (the gated write); `graph/nodes/events/` +217; `graph/nodes/_conflicts/` +6; 37 node frontmatter type retypes (27 wiki + 10 drift); `graph/edges/_regrounding/edges-pre-reification-2026-06-09.jsonl` (backup). NEW: `scripts/plate5-merge.py` (~450 lines, supports `--dry-run`/`--apply`); `working/edge-modeling/plate5-merge-diff.md` (full before/after report). NEW: `history/worklog-archives/archive018.md` (S83-/tmp moved here).

**Follow-up TODOs:** (1) Display-bullet regeneration script — `## Edges` sections in node files are pre-Plate-5 state; graph-query.py works from edges.jsonl correctly, but human readers see stale bullets. (2) The 32 SUB_BEAT_OF without quoted evidence — decide between re-emit / quote backfill / Contract-6 exemption for structural edges. (3) 109 hub-review-queue entries — still in staging, defaults applied = none minted. (4) 2 deferred collision merges (conquest-of-dorne, tourney-at-maidenpool). (5) donal-noye↔mag mutual-kill — add reverse direction. (6) Post-Plate-5 backfill tracks A/B/C (~$25-75, ~300-850 edges) per `working/edge-modeling/post-plate5-backfill-design.md`.

**What's next:** Matt's stated next track is "actually using the graph to do some validation" — use the merged graph to fact-check claims, run cross-character traversal queries, exercise the reified event hubs for the use-cases the design supported. No dedicated continue prompt yet; will draft one when Matt returns and we scope the validation conversation. The 6 follow-up TODOs above are non-blocking and can be picked up opportunistically. `graph/edges/edges.jsonl` is now LIVE at 4,757 rows; `events/` at 583 nodes.

### Session 86 — Alias resolver + display-name design + 4 structural fixes (2026-06-08)

**Model:** Opus 4.7 (design session, no agents delegated). **Detail:** none (design-only session; no incidents, no novel infrastructure). **Commit:** this endsession commit.

Design session resolving the two open questions queued by S85: (1) event-alias-resolver scope/integration, (2) chat-UI slug-vs-name display policy, plus 4 structural fixes from Matt's 23-mint triage. **No code, no `graph/` writes, no Plate 5 work.** Decisions captured in `reference/alias-resolver-design.md` (NEW, ~1,200 words) + 5 surgical edits to `reference/architecture.md`: (a) 7 new event sub-types (`event.wedding/feast/coronation/trial/assassination/execution/conspiracy`) added to type hierarchy + Type Reference Table — fixes the missing-enum bug that caused S85's 27 wiki schema misclassifications; (b) `SUB_BEAT_OF` formalized as canonical edge type (Beat → Parent Event, distinct from `PART_OF`'s event-in-war scope; vocab 165 → 166) — per Matt's call this session, NOT normalized to `PART_OF`; (c) `ALIAS_OF` row gains the canonical substitution test ("two strings are aliases iff substitution preserves truth value"); (d) NEW "Node Frontmatter Conventions" section with the `name`/`slug`/`aliases`/`era` field spec — `era:` is forward-only (no backfill), with 7-value enum (`pre-conquest` → `current-narrative`); (e) NEW "Display Names: slug as identifier, name as surface" section — both fields stored, rendering belongs to UI, no prompt-time enforcement; mint schema renames `title:` → `name:` at Plate 5 merge.

**Decisions:**
- `scripts/event_alias_resolver.py` to be built (follow-on, NOT this session) — separate from `stage4_name_resolver.py` (events don't have person/house/location collision shape; deterministic lookup-only is sufficient). Harvest broad across all node types; apply as O(1) lookup. No Haiku/LLM layer — not because of any blanket enrichment ban, but because a ~70% LLM tail over a ~95% deterministic lookup has no precision-gate math to win. Standing rule remains S75's: LLM enrichment is wanted, gated on precision.
- Sub-beat is NOT an alias. Granularity-collapse loses temporal queryability inside an event. `SUB_BEAT_OF` canonical.
- 4 structural fixes folded into Plate 5 / follow-on: 27 wiki schema-fix corrections (apply at Plate 5; `working/edge-modeling/plate2.5-schema-fixes/event-type-corrections.jsonl`), `scripts/wiki-pass2-triage.py` entity-type map update + new `scripts/wiki-event-type-validator.py` (follow-on prevention; would have caught all 27), IDF weighting in `scripts/plate4-wiki-cluster.py` narrowing function (follow-on; before next re-cluster), `era:` field on new mints (forward-only, narrowing function weights `era=current-narrative` higher), chapter-beat tier accepted (no separate canonical-promotion workflow for 2-3 genuinely missing event-pages like Robert's boar-hunt assassination).
- Stannis-approach-to-Winterfell and Winterfell-murders-during-Stannis-approach confirmed as two distinct events (related, link via `CONTEMPORARY_WITH` if both mint).

**Files touched:**
- CREATE `reference/alias-resolver-design.md` (NEW, ~1,200 words; the canonical design memo).
- EDIT `reference/architecture.md` — 5 surgical inserts (event sub-types in hierarchy diagram + Type Reference Table; `SUB_BEAT_OF` row near `PART_OF`; `ALIAS_OF` row substitution-test note; vocab count note 165→166; new "Node Frontmatter Conventions" + "Display Names" sections before Edge Metadata).
- ARCHIVE Session 82 from worklog → `history/worklog-archives/archive017.md` (archive017 now full at 5/5).

**Graph state:** `edges.jsonl` still **3,811** (unchanged since S76). `graph/nodes/events/` still 371. `git status graph/` clean.

**What's next:** → `progress/continue-prompts/2026-06-05-edge-modeling-plate-5-merge.md` (**Opus 4.7** — upgraded from Sonnet S86; the first plate to write to canonical `edges.jsonl`, backup-recoverable but high-friction to undo). Plate 5 folds in the staged 219 mints + 914 role edges + 54 cluster edges + 27 schema fixes + 3 S77 core cleanups + this session's mint-schema `title:`→`name:` rewrite. `SUB_BEAT_OF`-now-canonical means the 51 staged cluster edges land directly without re-emission. Matt before/after sign-off required. Follow-on (NOT blocking Plate 5): build `scripts/event_alias_resolver.py`, extend the wiki-redirect harvester to non-event types, IDF rewrite of `plate4-wiki-cluster.py`.

**Late-session fork — post-Plate-5 backfill design (S86 end):** Matt pushed back on my over-narrow "no backfill" framing for SUB_BEAT_OF and surfaced the bigger question: the edge-modeling lessons (head rule, reification, vocab additions) should be applied to the existing 3,811-edge graph, not just to future emissions. **Matt also corrected my misreading of S74 mid-fork** — S74 was a precision-gate failure on the specific Events+Dialogue Haiku run (74.5%/62.5% vs 75% gate), NOT a blanket "no LLM enrichment" ban. S75 explicitly amended to "enrichment wanted, gated on precision changes." Standing rule for any LLM-touching work: pass the precision gate. Empirical scan of edges.jsonl confirmed 25+ deterministic vocab-drift candidates at a sample floor across 6 of ~12 newer-vocab types (full sweep likely 100-200+). Designed 3 backfill tracks sequenced after Plate 5, each with its own precision gate per S75: (A) vocab-drift retype $0-15, 100-200 retypes; (B) reification of existing edges into event hubs $20-50, 200-600 reifications (cleanroom's main carry-over); (C) head-rule retroactive cleanup beyond Plate 0's 10 flips $0-10. Total ~$25-75 for ~300-850 edges touched (6-17× Plate 5's retroactive scope). Pass 1 chapter re-extraction stays OFF the table. Full design: `working/edge-modeling/post-plate5-backfill-design.md`. New HIGH todo added. **Plate 5 still proceeds as scoped — no scope creep.**

### Session 85 — Plate 3 full sweep + Plate 4 wiki-cluster bridge (2026-06-07 → 2026-06-08)

**Model:** Opus 4.7 orchestrator. Plate 3 reify per-event LLM = Sonnet 4.6 via `claude -p`. Plate 4 cluster cascade: Haiku 4.5 (Pass A) → Opus 4.7 (Pass B inference-only) → Sonnet 4.6 (Pass C distinct). 5 sub-agents (cold-read review, wrapper audit, gate stress-test, cluster validation, alias harvester). **Detail:** `history/session-details/session-085.md`. **Cost:** ~$35 ($0.57 Plate 3 + $34.74 Plate 4-cluster).

**Plate 3 (reify) SHIPPED:** Gate bug fixed (bold-title-only matching + clean slugs); Gate E v1+v2 dialogue/recall deny-list (33.6% kill rate); new wrapper `scripts/edge-reify-run-forever.sh` (5hr-wall-safe); empty-stderr-as-wall + ledger-no-error-write fixes (load-bearing — first sweep silently lost 324 events to a silent wall, full recovery). Final: **413/413 events processed, 0 errors, 219 minted event-nodes, 914 role edges, 55 supersede candidates, 109 hub-review-queue, 213 Gate-E pre-rejected.** 18/18 validation spot-check = 100% precision.

**Plate 4-cluster (NEW track) — wiki-vs-chapter bridge:** discovered only 1/220 Plate-3 mints matched a wiki event-node via slug overlap (wiki uses formal canonical names like `red-wedding`; mints use chapter-beat narrative names like `lord-walder-calls-for-the-bedding` — different taxonomies). Built `scripts/plate4-wiki-cluster.py` hybrid classifier (deterministic narrow + LLM judge). 3-pass cascade: Pass A Haiku $5 (50 sub-beat-of, 167 distinct), Pass B Opus on 71 inference-only $22 (DOWNGRADED 52% to distinct), Pass C Sonnet on 167 distinct partial $7 (144/167 before wall, 10 new sub-beat-of). Human triage of remaining 23: 2 sub-beat-of, 18 distinct, 3 deferred. **Final: 54 cluster edges staged** (51 SUB_BEAT_OF + 3 DUPLICATE_OF). 18/18 spot-check = 100% precision.

**Wiki alias harvest** ($0 deterministic via subagent): 176 aliases from 88 wiki event-nodes (e.g. `red-wedding` ← `wedding-at-the-twins`). 0/219 Plate-3 mints retro-matched (confirms granularity gap can't be bridged by aliases alone — they need LLM judgment).

**4 structural issues surfaced by Matt's triage, all STAGED for follow-on:** (1) 27 wiki schema misclassifications — root cause is wiki ingestion only knew `event.battle/.tournament/.war`, all weddings/coronations/feasts/trials defaulted to event.battle (missing-enum bug); corrections at `working/edge-modeling/plate2.5-schema-fixes/event-type-corrections.jsonl`. (2) IDF-style downweighting needed in narrowing function (mass-participant events like `feast-in-honor` over-score). (3) Era property to add going forward (no backfill). (4) 2-3 genuinely missing wiki nodes (Robert's boar-hunt assassination, Winterfell murders during Stannis approach).

**Graph state:** `edges.jsonl` still **3,811** (unchanged since S76). `graph/nodes/events/` still 371. `git status graph/` clean across all 24+ hours.

**What's next:**
- → `progress/continue-prompts/2026-06-08-alias-and-display-design.md` (Opus 4.7) — alias resolver extension + chat-UI slug-vs-name display policy + 4 structural fixes including the 27-event schema-bug root-cause analysis
- → `progress/continue-prompts/2026-06-05-edge-modeling-plate-5-merge.md` (Sonnet) — UPDATED with new staging items (54 cluster edges, 27 schema fixes, etc). Single irreversible step — Matt sign-off required.
- Plate 5 prerequisite: Matt picks dual-taxonomy vs single-tier for chapter-beat mints
- Plate 5 readiness inventory: `working/edge-modeling/PLATE5-READINESS.md`

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

> Session 83 (Edge-modeling Plates 0+1+2) archived to `history/worklog-archives/archive018.md` (archive018 now 2/5)
> Session 83 (Move /tmp paths) archived to `history/worklog-archives/archive018.md` (archive018 started — 1/5)
> Session 82 archived to `history/worklog-archives/archive017.md` (archive017 now full at 5/5)
> Session 81 archived to `history/worklog-archives/archive017.md` (archive017 now 4/5)
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
