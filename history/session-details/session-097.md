# Session 97 — Historical-anchor #9 wave 1 + Orchestration/Pacer design doc (2026-06-15)

**Model:** Opus 4.8 orchestrator + Sonnet 4.6 subagents (8 historical-anchor research agents, 1 sequencing advisor, 1 design-doc reviewer).
**Entry point:** `/continue arc-wave1-mint` — but the session pivoted twice on Matt's steer.

---

## 1. The pivot: arc-mint → historical-anchor #9

The continue prompt queued the narrative-arc wave-1 mint (Red Wedding + Joffrey conspiracies), gated on 3 of Matt's design decisions (RW-4 parent role edges, arc boundaries, RECIPIENT_IN vocab). Matt declined to answer cold and asked what prior agents had said + whether we were even at the right stage. Honest accounting surfaced a **contradiction**: the worklog's NEXT-TRACK order put followup #9 (historical-anchor) *before* the arc mint, while the arc continue prompt queued #9 *after* — per CLAUDE.md rule #9 the worklog wins.

A fresh general-purpose advisor (read-only, uninfluenced by the continue prompt) independently recommended **B-first**: the S96 Mode-3 dip's measured #2 gap was the isolated historical hubs, the arc mint maps to *zero* of the 10 dip questions, and #9 is the structural back-half of the discoverability work (Track 7 resolver = front-half, already shipped). Matt chose #9. Arc mint stays drafted-but-unminted, still gated on his 3 decisions.

## 2. Historical-anchor #9 wave 1 — SHIPPED

**The gap:** major pre-series historical event hubs (`tourney-at-harrenhal` etc.) sat isolated (0–2 edges) even though their facts already exist — in the hub's own wiki node body (Known Attendees / joust results) and, for some participants, as cited Pass-1 dyads. Dip §6 Q5 is the prototype: the `rhaegar→lyanna CROWNS` edge exists, cited with a Harrenhal-naming quote, but the hub had 0 edges because the dyad wasn't attached.

**Method (after a false start):** the blind quote-matcher (`historical-anchor-candidates.py`) proved too noisy over 300 hubs — descriptive event names share common words with unrelated prose (advisor predicted exactly this). Pivoted to: **curate the high-value cluster by hand** (8 Robert's-Rebellion / R+L=J hubs, the only ones with real main-saga POV coverage; the other ~300 are deep-lore wiki-only, out of scope for the cheap pass), then **one Sonnet subagent per hub** reads the node body + wiki cache + chapters and emits JSON attach edges (FIGHTS_IN/ATTENDS/AGENT_IN/VICTIM_IN/COMMANDS_IN/LOCATED_AT).

**Two-stage validation caught the failure modes the advisor warned about.** `historical-anchor-validate.py` checks every book quote verbatim-in-chapter AND every wiki quote verbatim-in-node-body-or-raw-json (stripping `[x](wiki:)` markup — without that strip, 16 false positives masked the 7 real ones). Curator dispositions: **6 dropped** (Theon FIGHTS_IN — he was a child *hostage*, not a combatant; Jon Arryn COMMANDS_IN trident — grounded on a *wedding* quote; 2 meta-description "quotes"; 2 speculative Summerhall attendees) + **4 quote-fixes**.

**Shipped:** +118 edges (21,829→21,947) across 8 hubs + a 3-edge Trident follow-up (Robert/Rhaegar/Lewyn COMMANDS_IN, →21,950). Provenance discipline held: 99 book-pass1 (tier-1/2) / 19 `wiki-historical-anchor` (NEW evidence_kind, tier-2 max). `--health` 62 orphans unchanged (0 new); pytest clean (3 documented pre-existing fails). `tourney-at-harrenhal` 0→25, `the-hands-tourney` 0→33, `battle-of-the-trident` 2→16. Dip Q5/Q10 now answerable.

## 3. Source discussion: TWOIAF (6th) + F&B (7th)

For the ~300 deep-lore wiki-only hubs, the real primary text is Fire & Blood / TWOIAF. Confirmed on disk: **TWOIAF is present** (`sources/raw/TWOIAF.txt`, 179K-word OCR) but never Pass-1-extracted; **F&B is NOT on disk** (only wiki pages *about* it). So TWOIAF = 6th source (cheaper, text already here), F&B = 7th (needs acquiring). Both are non-POV history register (Yandel/Gyldayn), closer to the wiki than a chapter, and the wiki was largely derived from them — unique value is verbatim primary-text tier-1 quotes. Backlogged; use wiki for those hubs now.

## 4. The design session: orchestration & pacing

Matt asked to take on the long-overdue **script consolidation** (151 scripts, 2 archived; the Fable-audit cleanup plan never executed). Started mechanically (wrote `tests/test_longrun_supervisor.py` — 6 tests proving longrun.sh's exit-10/2/0/crash/resume machinery; grep-guarded 24 archive candidates, catching a **zsh word-splitting bug** in my own guard that had produced a false all-clean). Then Matt redirected to a design discussion.

**The teaching arc** (Matt asked "what does bash-wraps/python-paces mean — can a shell script call a python script?"): explained the supervisor/worker pattern through the **exit code as the universal cross-language seam** — bash is the dumb durable relaunch loop, Python is the worker + brain that emits 0/2/10, and the split exists because the supervisor must outlive the worker dying. Then the four-class **script taxonomy** (A=long-run job / B=one-shot mutation / C=standing tool / D=resolver-library) clarified that the orchestration governs only class A; resolvers (D) are load-bearing libraries that rebuild derived artifacts, not one-offs.

**Decision: design-doc-first** (Matt). Wrote `working/orchestration-pacer-design-2026-06-15.md` — architecture, exit-code contract, worker/resumability contract, per-worker JSONL telemetry ledger (the fix for the CSV-append race Matt remembered — confirmed real: `acok-davos-02` appears twice in the agot-v3 CSV from two terminals), the pacer (`pace.py`, mines past stats for sleep/headroom), concurrency model, the `weirwood` CLI surface, the §11 Script Organization Standard, and `weirwood refresh` (one command rebuilding all derived artifacts post-mutation; memory entry written so it isn't forgotten).

**Fresh review** (skeptical subagent that read the *actual* stage4.sh wall-detection + stats schemas) found 4 real spec gaps → applied as §13 binding amendments: (M1) exit-2 needs a positive wall signal else exit-crash + a shared `next-eligible` file; (M2) atomic tmp-then-rename state writes vs SIGTERM corruption; (M3) honest backfill — wall-cadence data is thin (~4 events), so v1 reports duration baselines only; (M4) concurrent workers must share one next-eligible timestamp → v1 is single-worker, burst is v2. §12 open questions resolved (advisory pacer, sequential-default, per-track ledger, v1 report-only). §14: **scope is honestly TWO sessions** (pacer build, then cleanup), not one — the heterogeneous-CSV backfill normalizer is the time-sink.

## 5. State at session close
- Graph: edges.jsonl 21,950 (committable). 2 new backups in `_regrounding/`.
- Nothing committed (Matt ran /endsession without answering the commit question).
- Open threads preserved: script-consolidation Session 1 (pacer) = recommended next; historical-anchor #9 wave 2; narrative-arc wave 1 mint (still gated on Matt's 3 decisions).
