# Session Details — Index

Per CLAUDE.md rule 7, detail files are written *as needed*, not for every session. Pure-execution sessions are documented only in `worklog.md`; detail files cover design discussions, incidents worth a postmortem, and novel decisions worth a long-form narrative. Gaps in the numbering are intentional.

Sessions S0–S86 appear below. S87–S91 are in the live `worklog.md` (not yet detailed).

## Files

| File | Date | Subject | Project-story chapter |
|------|------|---------|----------------------|
| [session-000.md](session-000.md) | ~Apr 13 | Project genesis — goals, architecture decisions, first direction | [01 — Scaffolding Era](../project-story/01-scaffolding-era.md) |
| [session-001.md](session-001.md) | Apr 13 | Project scaffolding and directory cleanup | [01 — Scaffolding Era](../project-story/01-scaffolding-era.md) |
| [session-002.md](session-002.md) | Apr 13 | Chapter splitter + wiki scraper built | [01 — Scaffolding Era](../project-story/01-scaffolding-era.md) |
| [session-003.md](session-003.md) | Apr 13 | Wiki crawl planning + smoke test; Cloudflare blocked | [01 — Scaffolding Era](../project-story/01-scaffolding-era.md) |
| [session-004.md](session-004.md) | Apr 13 | Playwright migration to bypass Cloudflare | [01 — Scaffolding Era](../project-story/01-scaffolding-era.md) |
| [session-005.md](session-005.md) | Apr 14 | Full wiki crawl executed (36h, 17,945 pages) | [01 — Scaffolding Era](../project-story/01-scaffolding-era.md) |
| [session-006.md](session-006.md) | Apr 16 | D&E novellas + TWOIAF integrated as sources | [02 — Book Passes](../project-story/02-book-passes.md) |
| [session-007.md](session-007.md) | Apr 22 | Extraction schema v2 + tooling | [02 — Book Passes](../project-story/02-book-passes.md) |
| [session-008.md](session-008.md) | Apr 24 | architecture.md refactor, edge type expansion, wiki discovery | [02 — Book Passes](../project-story/02-book-passes.md) |
| [session-009.md](session-009.md) | Apr 24 | `/continue` command, todo-prompt linking, session backfill | [05 — Infrastructure](../project-story/05-infrastructure-and-tooling.md) |
| [session-010.md](session-010.md) | Apr 24 | Prompt v3 update + unauthorized extraction run + revert (incident) | [02 — Book Passes](../project-story/02-book-passes.md) |
| [session-011.md](session-011.md) | Apr 24 | `extract.sh` instrumentation: worklog auto-update + versioned CSV | [05 — Infrastructure](../project-story/05-infrastructure-and-tooling.md) |
| [session-012.md](session-012.md) | Apr 25 | AGOT v3 completion + rate-limit detection + commit catchup | [02 — Book Passes](../project-story/02-book-passes.md) |
| [session-013.md](session-013.md) | Apr 25 | Remote added; Track B sequencing decision; orchestration planning | [05 — Infrastructure](../project-story/05-infrastructure-and-tooling.md) |
| [session-014.md](session-014.md) | Apr 25 | Pipeline-not-fixed note (Passes 2–6 not set in stone) | [05 — Infrastructure](../project-story/05-infrastructure-and-tooling.md) |
| [session-015.md](session-015.md) | Apr 25 | README `/continue` + `/endsession` documentation | [05 — Infrastructure](../project-story/05-infrastructure-and-tooling.md) |
| [session-016.md](session-016.md) | Apr 25 | Wiki Pass 2 orchestration plan: independent review (21 issues) | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-017.md](session-017.md) | Apr 25 | Wiki Pass 2 patch: apply 21 review decisions + prompt restructure | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-018.md](session-018.md) | Apr 26 | Wiki Pass 2 build cleanup: close the triage seam end-to-end | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-019.md](session-019.md) | Apr 26 | Wiki Pass 2 launch prep + smoke-test bug surface | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-020.md](session-020.md) | Apr 26 | Wiki Pass 2 smoke-debug fix + first-bucket smoke (direwolves, $1.15) | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-021.md](session-021.md) | Apr 26 | Triage-disambiguation fix + direwolves cleanup; mid-session crash | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-022.md](session-022.md) | Apr 26–27 | Wiki Pass 2 Stage 1 run (9/37 buckets before 7-day cap hit) | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-023.md](session-023.md) | Apr 27 | Wiki Pass 2 Stage 1 drain complete (37/37 buckets, 855 nodes) | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-024.md](session-024.md) | Apr 27 | Stage 2 cold review overturned; Python-first pivot designed | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-025.md](session-025.md) | Apr 27 | Stage 3 prep: priority script + Stage 3a + edge vocab lockdown | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-026.md](session-026.md) | Apr 27–28 | Stage 3 completion + Tier recovery + fleet architecture + chat UI design | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-027.md](session-027.md) | Apr 30 | Stage 3c audit cleanup + Tier 3 promotion (graph 4,239 → 5,008) | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-028.md](session-028.md) | Apr 30–May 1 | Path B promotion campaign + parser iteration (+2,240 nodes) | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-029.md](session-029.md) | May 1 | Promotion completion + schema-drift audit + chronology extraction | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-030.md](session-030.md) | May 2 | ACOK Pass 1 status check + wave 11–14 completion | [02 — Book Passes](../project-story/02-book-passes.md) |
| [session-033.md](session-033.md) | May 4 | `--chain` terminal-explosion + race-condition bug (incident) | [02 — Book Passes](../project-story/02-book-passes.md) |
| [session-034.md](session-034.md) | May 4 | Schema-mismatch realization + cheaper-model brainstorm | [02 — Book Passes](../project-story/02-book-passes.md) |
| [session-036.md](session-036.md) | May 6 | Hygiene pass + soft-convention hardening (chat-UI framing retired) | [05 — Infrastructure](../project-story/05-infrastructure-and-tooling.md) |
| [session-039.md](session-039.md) | May 7 | Status check + `working/wiki/` subtree reorg | [05 — Infrastructure](../project-story/05-infrastructure-and-tooling.md) |
| [session-040.md](session-040.md) | May 11 | Catch-up synthesis, surgical merges, alias backfill | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-041.md](session-041.md) | May 11 | Per-character index roll-up + POV canonicalization + missing-nodes audit | [05 — Infrastructure](../project-story/05-infrastructure-and-tooling.md) |
| [session-042.md](session-042.md) | May 12 | Wiki prose extraction backfill (Track 1) | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-045.md](session-045.md) | May 12 | Mission protocol design (watcher + workers) | [05 — Infrastructure](../project-story/05-infrastructure-and-tooling.md) |
| [session-046.md](session-046.md) | May 12 | First mission + protocol v1 + batch 2 reconstruction | [05 — Infrastructure](../project-story/05-infrastructure-and-tooling.md) |
| [session-051.md](session-051.md) | May 12 | Watcher-day orchestration + session-results convention | [05 — Infrastructure](../project-story/05-infrastructure-and-tooling.md) |
| [session-052.md](session-052.md) | May 13 | Edge vocabulary drift cleanup + Stage 4 reframing | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-053.md](session-053.md) | May 15 | Stage 4 one-tab smoke + throttle calibration | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-054.md](session-054.md) | May 15–16 | Stage 4 schema drift discovery + Haiku failure + 21-batch bulk | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-055.md](session-055.md) | May 18 | Stage 4 vocab-lock decisions + Pass-1 staleness incident | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-056.md](session-056.md) | May 18 | Stage 4 vocab applied + qualifier vocab lock-down planned | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-057.md](session-057.md) | May 18 | Stage 4 qualifier vocab lock-down (vocab 163/164) | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-058.md](session-058.md) | May 18–19 | Stage 4 lockdown completion + vocab round 2 + validator | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-059.md](session-059.md) | May 19 | Stage 4 Haiku worker built + Python re-architecture plan | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-060.md](session-060.md) | May 19 | Stage 4 Haiku: normalizer built + no-silent-drop pipeline | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-061.md](session-061.md) | May 19–20 | Stage 4 vocab 159→164 + ENCOUNTERS verb gate + overnight Haiku launch | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-062.md](session-062.md) | May 21 | Stage 4 overnight Haiku triage + LEVER 2 + test bootstrap | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-063.md](session-063.md) | May 21 | Heavy ENCOUNTERS + KNOWS deprecated + candidate enrichment pipeline | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-064.md](session-064.md) | May 22 | Stage 4 Tier-1 bulk launch + dual-run incident | [03 — Wiki Work](../project-story/03-wiki-work.md) |
| [session-065.md](session-065.md) | May 22 | S64 dual-run forensics → Pass-1-derived edge pipeline pivot | [04 — Edge Layer](../project-story/04-edge-layer.md) |
| [session-066.md](session-066.md) | May 23 | Pass-1-derived edge spine built; resolution-wall broken | [04 — Edge Layer](../project-story/04-edge-layer.md) |
| [session-067.md](session-067.md) | May 23 | Alias recovery + comention deprecation + LLM tail run | [04 — Edge Layer](../project-story/04-edge-layer.md) |
| [session-068.md](session-068.md) | May 24 | Stage 4 recall ceiling: mine all Pass 1 tables + recall-sample | [04 — Edge Layer](../project-story/04-edge-layer.md) |
| [session-069.md](session-069.md) | May 24 | Extra-tables enrichment smokes + held at $270 spend gate | [04 — Edge Layer](../project-story/04-edge-layer.md) |
| [session-071.md](session-071.md) | May 25 | Stage 4 accuracy push → unpromoted-node pivot (false alarm) | [04 — Edge Layer](../project-story/04-edge-layer.md) |
| [session-072.md](session-072.md) | May 25–26 | Node-gap false alarm corrected; index + validator + resolver fixed | [04 — Edge Layer](../project-story/04-edge-layer.md) |
| [session-073.md](session-073.md) | May 26 | Cleanup-and-reorg triage; worktrees removed; CLAUDE.md rule #9 finding | [05 — Infrastructure](../project-story/05-infrastructure-and-tooling.md) |
| [session-074.md](session-074.md) | May 26 | Locator grounding fix; enrichment NO-GO; core citations re-grounded | [04 — Edge Layer](../project-story/04-edge-layer.md) |
| [session-075.md](session-075.md) | May 26 | Graph-exercise follow-ups + conflict-pair audit + enrichment un-shelved | [04 — Edge Layer](../project-story/04-edge-layer.md) |
| [session-076.md](session-076.md) | May 27 | Events enrichment launched on Sonnet; flush-fix + ASSAULTS mis-type caught | [04 — Edge Layer](../project-story/04-edge-layer.md) |
| [session-077.md](session-077.md) | May 27 | Haiku vs Sonnet Events decision → paced runner built → bulk launched | [04 — Edge Layer](../project-story/04-edge-layer.md) |
| [session-080.md](session-080.md) | May 31 | Events Haiku bulk complete: wrapper bug fixed + v2.0 promotion chain authored | [04 — Edge Layer](../project-story/04-edge-layer.md) |
| [session-081.md](session-081.md) | May 31–Jun 1 | Events Haiku bulk drift audit → NO-GO (borderline); fresh-eyes corrected framing | [04 — Edge Layer](../project-story/04-edge-layer.md) |
| [session-082.md](session-082.md) | Jun 4 | Edge/event modeling: cleanroom decision doc + two-way synthesis | [06 — Reification](../project-story/06-reification-explained.md) |
| [session-083.md](session-083.md) | Jun 5 | Reification Plates 0+1+2 shipped; D2 resolved | [06 — Reification](../project-story/06-reification-explained.md) |
| [session-084.md](session-084.md) | Jun 6–7 | Plate 3 audit loop built + overnight rate-wall incident | [06 — Reification](../project-story/06-reification-explained.md) |
| [session-085.md](session-085.md) | Jun 7–8 | Plate 3 full sweep + Plate 4 wiki-cluster bridge (24hr autonomous) | [06 — Reification](../project-story/06-reification-explained.md) |
| [session-086.md](session-086.md) | Jun 8 | Alias resolver + display-name design + 4 structural fixes | [06 — Reification](../project-story/06-reification-explained.md) |

## Gaps (expected)

Sessions with no detail file: 031, 032, 035, 037, 038, 043, 044, 047, 048, 049, 050, 070, 078, 079. All were execution-heavy sessions whose worklog entries in [`history/worklog-archives/`](../worklog-archives/README.md) are the complete record.

## Cross-reference

The narrative companion to these session records is the project-story series at [`history/project-story/00-overview.md`](../project-story/00-overview.md). The story chapters cover the same eras thematically; these detail files cover individual sessions day-by-day.
