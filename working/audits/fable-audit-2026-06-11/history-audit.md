# The Weirwood Network — Project History Audit (Sessions 0–91, 2026-04-13 → 2026-06-11)

> Produced 2026-06-11 by a read-only Fable subagent. Sources: all 18 worklog archives
> (`history/worklog-archives/archive001-018.md`), current `worklog.md` (S87–91), `working/todos.md`,
> Pass 1 / Pass 2 cost CSVs in `working/extraction-stats/`. Nothing modified.

## A. Project arc in phases

**Phase 0 — Genesis & scaffolding (S0–S2, Apr 13).** Architecture designed (two-layer trigger-table + graph, six-pass pipeline, 5 confidence tiers, `first_available` spoiler gating declared "architectural, not optional" — a commitment later reversed). Chapter splitter built and run: 344 chapters across 5 books, all counts correct on first real run. Stdlib wiki scraper written — immediately blocked by Cloudflare.

**Phase 1 — Wiki crawl (S3–S5, Apr 13–14).** Cookie-based scraping failed (TLS fingerprinting), forced Playwright migration including a route-interceptor workaround for a Chromium cookie bug. Full crawl: 17,945/17,952 pages, 377 MB, ~36h wall (5× the estimate). Hidden defect not discovered until S41: case-insensitive HFS+ silently overwrote ~125 pages with their redirect variants. Classifier left 17,305 pages uncategorized — deferred. Cost: $0 (time only).

**Phase 2 — Pass 1 schema evolution + D&E/TWOIAF (S6–S15, Apr 16–25).** v1 AGOT (73 ch) → v2 (food/hospitality/appearance sections — Matt's design values) → v3 (12-category Raw Entity List). v1 and v2 fully discarded as extraction product (archived). Process infrastructure born here: continue prompts, `/endsession`, todos-as-authority, "no extraction without asking" (after violations).

**Phase 3 — Wiki Pass 2 orchestration + Stage 1 agent run (S16–S23, Apr 25–27).** Heavy plan-review-patch loop (21 review issues, self-acknowledged reviewer-bias problem). Direwolves smoke bucket ($1.15), then 37 core buckets → 855 agent-written nodes. **Cost blew the estimate 2–3×: $95.33 actual ($2.58/bucket vs $0.71–1.43 budgeted); secondary tier projected ~$1,200.** Hit the 7-day rate limit mid-run. Bucket-overlap bug wasted runs (accepted).

**Phase 4 — The Python-first pivot + promotion campaigns (S24–S29, Apr 27–May 1).** The project's first foundational reversal: Stage 2 cold review returned `remediate`; Matt overturned it same-session by **deferring spoiler gating entirely** and instituting **"Python before Agent"** as a project-wide rule. Stage 3 rebuilt deterministic: 3,314 nodes promoted in ~30 seconds for $0 (vs the ~$1,200 agent path). Tier-3 campaigns, the one approved exception-fetch (MediaWiki categories backfill), parser iteration. Graph: 855 → 7,563 nodes. One $50 Opus schema-drift audit (0 HIGH). This phase is where most of the graph's node mass comes from.

**Phase 5 — Pass 1 corpus completion (S30–S35, May 1–6).** Matt's "I need to get the books in then" sequenced Pass 1 before Stage 4. Marred by the `--chain` terminal-explosion + extraction-race incident (S33, ~$19 waste, feature deleted). All 5 books complete 2026-05-06 (344/344, all Opus; ASOS run by Okey as a one-off, ~$54.85). **Pass 1 v3 recorded cost: ~$234** (AGOT 50.04 / ACOK 42.33 / ASOS 54.85 / AFFC 36.39 / ADWD 50.81), plus $35 for the discarded AGOT v2.

**Phase 6 — Hygiene + index infrastructure + mission protocol (S36–S51, May 6–13).** D&D-chat-UI framing retired (S37); dialogue/meals passes exposed as agent-invented scope and killed (S38) — only the mention-index survived. Pure-Python index layer built: 344 chapter mention files (70→72.9% resolution), 3,910 character indexes, location/artifact/house indexes. Missing-node backfills (+247 nodes), case-collision reconstruction missions (70 of 125 pages recovered via the new watcher/worker mission protocol). Graph ~7,967 nodes.

**Phase 7 — Stage 4 wiki-comention era (S52–S64, May 13–22).** The long grind to make LLM edge classification safe: Sonnet bulk launched (21/201 batches, ~$50–90), schema drift discovered → mechanical validator → vocab lock rounds (96→132→149→159→163/164 types) → qualifier enums, `notes` field deleted → Haiku smoke FAILED (~80% semantic drift, S54) → full lockdown + enrichment pipeline → Haiku rehabilitated (~3-4% violations) → Tier-1 bulk launched → **S64 dual-run incident** (unexplained second `run-forever` chain, ~$15–20 waste, 24 files clobbered). Haiku-era spend ~$100. **The whole track was then deprecated.**

**Phase 8 — Pass-1-derived pivot + edges v1 (S65–S74, May 22–26).** S65 forensics concluded the project's own Pass 1 tables were a better candidate source than wiki comention (7,348 first-party relationship rows vs 29,259 noisy comentions). Deterministic spine: 2,834 cited edges at $0; Sonnet tail: +2,385 ($20.88). `graph/edges/edges.jsonl` v1 landed S70 (3,842), refined to v1.3 (3,811) through S72. **S71 false alarm** ("~7,251 unpromoted nodes") paused edges for one session on a bad file-count health check; S72 corrected it and fixed the real bugs (index coverage, validator contracts). Extra-tables enrichment (Events/Info/Food/Dialogue, 32k candidates) smoked at 60–74% precision — **NO-GO, $270 bulk never spent**; core shipped with citations re-grounded (the latent `:11` line-number bug fixed).

**Phase 9 — Events-Haiku enrichment attempts (S75–S81, May 26–Jun 1).** Enrichment un-shelved as a deferral; Events chosen as next surface. Sonnet partial run ($20.81), Haiku won the model bake-off, full Haiku bulk completed cleanly (~$50, 1,617 typed edges, 0 drift halts) — **then the S81 cross-model drift audit returned NO-GO** (triple 48% vs 70% gate), with a fresh-eyes subagent correcting both the audit's miscited smoke session and the orchestrator's framing. Borderline No-Go; nothing promoted; output parked.

**Phase 10 — Edge-modeling reification plates (S82–S87, Jun 4–9).** Cleanroom two-doc analysis converged on root cause: grammatical-subject leakage at Pass 1 + structurally empty event hubs. Plates 0–5: direction normalizer, head rule, D2/D7/D8 decisions, selective reification, audit loop (reporter + independent auditor), Plate 4 absorbed the Events-Haiku NO-GO output as cluster input (~$35). One overnight incident (rate-wall retry-burn; a silent wall cost 324 events, fully recovered) and one gate-bypass bug (`--all` minted micro-beats; contaminated output discarded). **Plate 5 shipped S87: edges.jsonl 3,811 → 4,757; event nodes 371 → 583; Red Wedding 2-hop traversal works.**

**Phase 11 — Validation & rename era (S88–S91, Jun 9–11).** Graph-validation probes (historical-events dark zone confirmed), overnight tooling agents (`--event-participants`, event-alias resolver, rename script), 10 event renames applied, 3 curator deception-pilot edges (edges 4,760). Current live track.

## B. Failures & dead ends (honest list)

1. **stdlib/cookie wiki scraper (S2–S4).** Cloudflare TLS fingerprinting killed it. Learned: browser automation or nothing. Artifact: archived cleanly at `scripts/archive/wiki-scraper.py.archive` with do-not-restore rules.
2. **Wiki crawl case-collision bug.** ~125 pages silently lost to case-insensitive filesystem overwrites; undetected for ~4 weeks (S5→S41). 70 reconstructed via missions; 55 tail dropped/aliased. Learned: verify crawl integrity against title list, not file counts. Marked in todos as resolved.
3. **Agent-does-everything Pass 2 (Stage 1).** 2–3× cost overrun; the `remediate` verdict and $1,200 secondary projection killed it. The 855 Stage-1 agent nodes remain the only agent-rich nodes — a permanent quality seam in the graph (rest are Python skeletons + extracted prose). Cleanly superseded by the Python pipeline; old runbooks archived with banners.
4. **`first_available` spoiler gating as architectural requirement.** Reversed S24 to "deferred backfill." **Not cleanly marked: worklog Principles #4 still asserts the original position** (see §E).
5. **`--chain`/`--delay` auto-advance (S31–S33).** Terminal explosion + duplicate-extraction race; ~$19 waste; deleted within 2 sessions. Learned: never let spawned workers spawn workers; later wrappers all use single-coordinator loops.
6. **Stage 4 wiki-comention (S52–S64) — the biggest dead end.** ~5 weeks of lockdown engineering and ~$150–190 spend on a candidate source (wiki chapter-summary comentions) that was structurally noisy. Deprecated S65 via in-data stamping (133 files `superseded_by: pass1-derived`) — deliberately not dir-archived. 27 scripts kept on disk as a "future recall lever" (S73 decision: do not re-propose archiving). Honest caveat: the lockdown machinery built for it (validators, vocab lock, enums, normalizer, no-silent-drop pipeline) is precisely what made every later LLM pass safe — the spend wasn't pure loss, but the candidate source was.
7. **Haiku smoke failure (S54).** ~80% semantic failure pre-lockdown (SERVES-on-everything, KILLED_BY reversals). Learned: the durable fix is locking every freestyle surface + mechanical validation, not stronger prompts. Archived as a comparison artifact (`_archive/batch-0012-haiku-failed-2026-05-15/`).
8. **KNOWS edge type.** 82.3% fallback rate; deprecated S63 (vocab 164→163). Clean.
9. **Extra-tables enrichment NO-GO (S68–S74).** Events/Info/Food/Dialogue candidates smoked at 60–74.5% against a 75–80% gate, three times. ~$11 of smokes prevented a ~$270–290 bulk. Shelved S74; reframed "deferred, not banned" S75 after Matt corrected the over-broad reading.
10. **Events-Haiku bulk NO-GO (S77–S81).** The subtlest failure: the run itself was operationally flawless (~$50, single prompt_sha, 0 drift halts, ~85-90% on hand-read smokes) but failed the *cross-model* audit on structural edge types (TRAVELS_TO 17%). Learned: hand-read precision on fresh candidates and judge-model agreement on stratified emits are different metrics — both were true. Output not wasted: absorbed as Plate 4 input in the reification era.
11. **S71 node-gap false alarm.** "~7,251 unpromoted nodes" paused edge work on a file count; slug intersection showed 7,039/7,047 already promoted. The real gaps were the index (14 categories never indexed) and validator contracts. Cleanly documented (memory + todos correction block).
12. **Chat-UI / D&D-group framing (S26→S37).** A full architecture doc (three-corpus retrieval, Netlify, friend-group auth posture) written in one expansive session and retired ten sessions later as "stale sketch, not Matt's design." Archived to `history/archive/sketches/`. Related: the 27-agent fleet roster + daemon plans (S26, budget "~$1,250–2,310") were never executed; the fleet-specs remain in `working/agent-fleet-specs/` with the mission protocol (v1, used ~3 times, dormant since S48) as the only shipped descendant. todos still carries live-looking fleet/watcher items (§E).
13. **Dialogue/meals/voice passes (S34–S38).** Agent-invented scope, never requested; killed at the design review. Only the mention index survived.
14. **S64 dual-run incident.** A second overnight chain launched from unknown origin; double quota burn, 24 clobbered files. Root cause never definitively found — mitigated structurally (provenance stamped in data; single-instance guards).
15. **Plate-3 overnight incidents (S84–S85).** Retry-loop window-burn before fail-fast existed; `--all` selective-gate bypass minted junk micro-beat hubs (output discarded); a silent rate wall dropped 324 events (recovered). All fixed; the pattern (unattended runs need fail-fast + resume + wall-detection from day one) repeated three eras in a row before sticking.

## C. Successes (what compounds)

- **The local wiki cache** (17,945 pages, one crawl, never re-fetched). Every node, alias, prose body, infobox edge, category, and cluster derives from it. The single best $0 asset.
- **Pass 1 v3 (344 Opus chapters, ~$234).** Bought as "mechanical extraction," it became the project's *primary-source candidate generator*: the winning edge spine (S65 pivot), the hospitality edges, the temporal scoping, the POV canonicalization, and the reification beats all mine Pass-1 tables. Easily the highest-ROI spend.
- **Python-first promotion + index layer.** ~7,000 of ~8,300 nodes, all indexes, the alias resolver, prose attachment — near-$0, deterministic, regenerable, and the reason the agent layer stayed affordable.
- **The deterministic, cited edge layer.** `edges.jsonl` (now 4,760): every edge carries verbatim quote + `file:line`, 0 orphans, 100% endpoint resolution, traversable. "A wrong cited edge is graph pollution" held as the governing value through three NO-GO decisions.
- **The lockdown + validation stack.** Locked vocab (~166), qualifier enums, zero-freeform schema, mechanical validators, verb gates, suspicious-edge flaggers, 1,000+ hermetic tests, drift-halt exit codes. Built painfully in the comention era; reused by every subsequent LLM pass.
- **The audit discipline.** Cross-model audits, fresh-eyes subagents, out-of-sample smokes, the S84 reporter/auditor loop. These caught: the S71 overfit claim, the S81 miscited smoke, the S66 misresolution bugs, the S67 vocab-drift, the S83 D3 factual error. The graph's precision floor exists because of this, not because any one model was good.
- **Reification (Plates 0–5).** The first structural (rather than additive) improvement: events as hubs, role edges, head rule, SUB_BEAT_OF. Validated end-to-end (Red Wedding traversal).
- **CLAUDE.md rule #9 / staleness hierarchy.** Born from the S55 incident; invoked productively at least 4 times since (S69, S72, S73, S90).

## D. Process patterns

**Repeatedly worked:**
- *Deterministic Python before LLM* — instituted S24, decisive at least 6 times (Stage 3b prose extraction, mention/entity indexes, edge spine, hospitality edges, temporal scoping, alias resolvers). Every time a pass was re-examined, more of it turned out to be deterministic.
- *Smoke + spend gate before bulk* — held at least 5 times (S69 $270, S70 overnight, S74 $75, S81 chain-halt, S84 calibration-first), and caught bugs green tests missed at least 3 times (S67 KNOWS vocab-drift, S69 generator bugs, S66 misresolutions). Stated explicitly twice: "caught by doing, not by the green tests."
- *Cross-model / fresh-context review* — ~7 instances; corrected the orchestrator's own conclusions in S71, S81, S57 (encoding choice delegated to avoid bias), S82 (cleanroom).
- *Provenance in data, not directory names* — learned from schema-mixing/archiving contention (S65); applied via supersede stamps, prompt_sha, run_id.
- *In-data deprecation, never deletion* — sources additive-only rule held for 91 sessions.

**Repeatedly failed:**
- *Unattended bulk runs launched before hardening* — ≥6 incidents (S22 rate-limit burn, S33 chain explosion, S61 wasted batches, S64 dual-run, S76 idle night, S84 retry-burn/silent wall). The fail-fast/resume/wall-detection lesson was re-learned in three separate eras before it stuck as a standing wrapper pattern.
- *Count-based health checks* — 3 false alarms (S63 "missing files" panic, S71 node gap, S80 wrapper remaining-count). Each fixed by key/slug-based reconciliation.
- *Stale state propagation* — ≥5 incidents (S39 merge status, S49 slugs, S55 Pass-1 staleness incident, S69 commit claim, S73 gitignore claim). Drove rule #9 and the memory-staleness policy; still occurring in S90 (resolver auto-resolve prediction wrong).
- *Estimate optimism* — crawl 6-8h→36h; Pass 2 $0.71–1.43→$2.58/bucket; extra-tables ~$100→$270-290; Plate 3 200-300→2,056 events. Estimates were low by 2–7× essentially every time; measured re-baselining always followed.
- *Same-author review bias* — flagged at S16 (21/21 acceptance "suspicious") and structurally mitigated only from ~S57 onward.

## E. State contradictions & doc rot

(Extracted to `doc-rot-punch-list.md` in this folder — that file is the actionable version.)

## F. Spend ledger (recorded dollars only; LLM time on Max subscription mostly untracked separately)

| Track | Recorded spend | Notes |
|---|---|---|
| Wiki crawl (S5) | $0 | 36h wall; Playwright |
| Pass 1 v2 AGOT (discarded) | $35.04 | CSV |
| Pass 1 v3, 5 books (S12–S35) | **~$234.42** | AGOT 50.04 / ACOK 42.33 / ASOS 54.85 (Okey) / AFFC 36.39 / ADWD 50.81; +~$19 S33 dup-waste |
| Wiki Pass 2 Stage 1 agent run | **$95.33** | 37 buckets, $2.58/bucket (2-3× estimate) |
| Wiki Pass 2 secondary CSV | $51.83 | recorded in `wiki-pass2-stats-secondary-v1.csv` |
| Stage 3 Python promotion | ~$0 | saved projected ~$1,200 |
| Schema-drift Opus audit (S29) | $50 | pre-approved |
| Stage 4 comention — Sonnet era (S53–54) | ~$50–90 | $50.09 cumulative at S53; S54 reports ~$37 post-archive — internally inconsistent records |
| Stage 4 comention — Haiku era (S59–64) | ~$100 | $8.50 + $38 overnight + $55.66 bulk; incl. ~$15–20 dual-run waste |
| Pass-1-derived spine + tail (S66–67) | **$20.88** + ~$1 | spine $0 |
| Extra-tables smokes (S69–74) | ~$11 | held the $270–290 bulk |
| Events — Sonnet partial (S76) | $20.81 | superseded |
| Events — Haiku bulk + comparisons (S77–80) | ~$50–55 | + ~$3.6 model bake-off |
| Events drift audit (S81) | $0.93 | |
| Reification plates (S83–85) | ~$36 | $0.81 mini + $0.57 Plate 3 + $34.74 Plate 4 cascade |
| Misc audits/smokes (batch-0020 Opus, graph exercise, etc.) | ~$10–15 | scattered |
| **Rough recorded total** | **~$770–830** | |
| **Avoided by gates/pivots** | **~$4,400+** | $1,200 secondary agents + $615 Sonnet bulk remainder + $270–290 extra-tables + $340 Sonnet Events + ~$2,000 of the projected $2,800 Sonnet month |

**Bottom line:** roughly a third of all recorded spend (~$250 of ~$800) went to the deprecated comention track, but that track funded the safety machinery everything since depends on. The two best purchases were the wiki crawl ($0) and Pass 1 ($234); the deterministic-first rule kept the other ~7,000 nodes and ~3,000 edges near-free. The graph today (8,300+ nodes, 4,760 cited edges, 0 orphans, working event reification) is real and validated — but the documentation surface lags it badly.
