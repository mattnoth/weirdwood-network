# Deliverables Ledger — 2026-06-11

Everything Matt asked for across the 2026-06-11 orchestrator conversation, in one place.
Owner key: **[DONE]** shipped · **[AUDIT]** commissioned to the audit session via `working/reply-to-audit-session-2026-06-11.md` · **[NEXT]** confirmed deliverable, not yet built · **[GATED]** sequenced behind something.

## Infrastructure / tooling

- [x] **[DONE] `scripts/longrun.sh`** — central long-run supervisor (exit contract 0=done / 2=wall / 10=more-work / other=crash; LONGRUN_* env vars; tested, shellcheck-clean). Replaces six divergent run-forever wrappers' loop logic.
- [x] **[DONE] `weirwood run` subcommand** — built on longrun.sh; `scripts/weirwood-run.sh` + weirwood.zsh case + .gitignore working/logs/; tested, shellcheck-clean. No READY tracks yet — custom-only until a runner adopts exit-10 contract.
- [ ] **[GATED] Legacy wrapper migration** — the six wrappers become thin `longrun.sh`/`weirwood run` call-throughs, one per track, only after each track's current run finishes; underlying runners must adopt the exit-code contract first (notably exit 10). Tracked in todos.md → Extraction Infrastructure.

## Documentation / organization (audit session executes)

- [x] **[DONE] Step 0** — audit package persisted to `working/audits/fable-audit-2026-06-11/` (synthesis, history-audit, graph-deep-dive, doc-rot punch list, SESSION-CHECKPOINT).
- [x] **[DONE] Step 1** — CLAUDE.md + worklog truth-fixes + STATUS block; agent-count 28, dip-prompt gate, node count 8,263 applied per critic.
- [x] **[DONE] Step 1b** — todos.md 420→232; resolved blocks archived to `history/todo-archives/`.
- [x] **[DONE] Step 1c** — `progress/continue-prompts/README.md` manifest, every prompt tagged LIVE/DONE/STALE/MERGED.
- [x] **[DONE] Step 1d** — design-doc proposal at `working/audits/fable-audit-2026-06-11/design-doc-proposal.md` (Option A recommended). Consolidation build gated on Matt's pick (~3-4 sessions).
- [x] **[DONE] Step 2** — `history/project-story/` 8 chapters incl. the reification explainer with a live Red Wedding walkthrough. Critic-verified content-complete.
- [x] **[DONE] Step 2c** — `reference/schema-legend.md` (critic fixes applied — dual count columns).
- [x] **[DONE] Step 2d** — `working/audits/fable-audit-2026-06-11/worth-assessment.md` v2. Fresh-critic mandatory; applied.
- [x] **[DONE] Step 2b** — `working/nomenclature-reform-proposal.md` v1. Matt picks; sweep runs after.
- [x] **[DONE] Step 3** — infobox-merge spec v2 at `working/infobox-merge/spec.md`. Adversarial critic confirmed direction-inversion on 10 fields; all 9 findings applied.
- [x] **[DONE] Step 3b** — `reference/roadmap.md` v1 (destination features → graph capability → what exists/missing → remaining work tagged).
- [x] **[DONE] Step 4 fan-out** — (1) `scripts/infobox-merge.py` + 75 tests + dry-run report `working/infobox-merge/dry-run-report-2026-06-12.md`; (2) `history/` READMEs ×3; (2b) `scripts/README.md` (146 scripts, 6 LEGACY wrappers); (3) `curation/plate5-small-followups-2026-06-12.md`; (4) `curation/hub-review-triage-2026-06-12.md` (FIX 22 / QUARANTINE 10 / KEEP 81); (5) `working/repo-reorg-plan-2026-06-12.md`.
- [x] **[DONE] Question** — theories/prophecies connectivity: answered in synthesis.md (45 nodes + 2 nodes, effectively 0 real edges; infobox merge contributes nothing; options documented in todos.md § Dormant).

## Project knowledge

- [x] **[DONE] todos.md updates** — longrun consolidation entry (with DONE marker + migration remainder); project-story entry under Doc Hygiene.
- [x] **[DONE] Memory rule** — cross-session replies go through markdown files in working/ ("read X and execute it"), never clipboard.
- [x] **[DONE] Reply file** — `working/reply-to-audit-session-2026-06-11.md`, send-ready.

## Gated / later (deliberately NOT lost, just sequenced)

- [ ] **[GATED] Merge ship to graph/** — after Matt reviews the dry-run report.
- [ ] **[GATED] Mode 3 validation dip** — after the merge lands, on the merged graph; its failures decide whether backfill Tracks A/B/C matter.
- [ ] **[GATED] Nomenclature sweep of living docs** — after Matt picks the Step 2b scheme.
- [ ] **[GATED] Repo reorganization execution** — off the Step 4 plan draft + 2026-06-07 repo-audit continue prompt.
- [ ] **[GATED] Matt's articles/papers** — Matt writes; Step 2 project-story is the input.

## Open question for Matt

Anything wanted tonight that is NOT on this page?
