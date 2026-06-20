# Worklog Archive 022 — Sessions 102–106

> Archived from `worklog.md` per CLAUDE.md rule #8 (Session Log holds 5 entries; oldest rotates out). 5 entries per archive file. This file starts at Session 102.

---

### Session 102 — Advisory board → Track 3 dating-leftovers finished + vocab-test reconcile (2026-06-16)
**Detail:** `history/session-details/session-102.md`
**Model:** Opus 4.8 (1M context) orchestrator + 4 parallel Sonnet 4.6 `general-purpose` advisors. **Commit:** this endsession commit.

**Changes made (deterministic, $0, +0 edges):**
- **5 multi-year span events dated** via existing `ac_year_end` field: `dance-of-the-dragons` 129→132, `war-of-the-five-kings` 298→300, `greyjoy-rebellion` 289→290, `regency-of-aegon-iii` 131→136; `first-blackfyre-rebellion` = single-year **196** (dropped wiki cross-link error 212). `long-night` → `ac_year:null`/`precision:relative-only` (architecture.md:476; wiki's spurious 297 AC noted+excluded). `conquest-of-dorne` **verified** (date on `event.battle` node; book is separate `texts/` node — no change). Event nodes with `occurred:` block **112 → 118**.
- **10 mistyped year-page nodes DELETED** (`{129,130,131,134,143,157,209,283,286,298}-ac.node.md`, all `character.human`/0-edges/boilerplate) + their 10 index files + alias-resolver resync (`all-node-alias-lookup.json` dropped 10 slugs) + `characters/_summary.json` `year_pages_emitted_as_characters: 10→0`. Nodes **8,528 → 8,518**; edges/orphans unchanged (21,993/62).
- **Vocab-count test reconciled 163 → 166** (`tests/test_stage4_tail_classifier.py` + `tests/test_validate_edge_jsonl.py`; +3 = reification AGENT_IN/VICTIM_IN/SUB_BEAT_OF). **pytest 1297 pass / 1 fail** (only the environmental `cwd-is-tmp`; the 2 vocab fails now green — net 3 documented fails → 1).
- Reverted **7,921 timestamp-only** `weirwood refresh` index churns; kept only real content diffs. Final staged diff: 22 files, +25/−439.

**Decisions:**
- Matt declined a direct pick and ran an **advisory board** (4 Sonnet advisors: query-value / cost-risk / schema / curatorial). **3 of 4 → Track 3 (dating leftovers); top rec won.** Board roadmap (broadly endorsed): **#3 now → #1 ordering → #2 causal pilot → #4 Fable.** Two board findings actioned: **`TRIGGERS` already in vocab** (#2 needs no vocab add); **`PRECEDES`/`FOLLOWS` absent** (#1 needs one). Year-nodes: **delete** (Matt) — aligns with chronology-extractor design ("year pages aren't nodes"); year-lookup now via `occurred.ac_year`. Vocab-test: **reconcile to 166** (Matt) — restores the drift-detector.

**What's next** (live continue prompt updated: `progress/continue-prompts/2026-06-16-next-move-decisions.md`, **Sonnet 4.6**):
- → **3 decisions remain, all Matt's:** (1) `PRECEDES`/`FOLLOWS` vocab-add (D3) + grouping basis (0 dated events share a `PART_OF` parent) · (2) causal `TRIGGERS` sign-off (Robert's Rebellion pilot; no vocab add) · (3) Fable cleanup (nomenclature scheme + repo-reorg). Track 3 (dating leftovers) is DONE.

---

### Session 103 — Fable cleanup: canonical vocabulary DECIDED (3 terms, not 6) (2026-06-16)
**Detail:** `history/session-details/session-103.md`
**Model:** Opus 4.8 (1M context) orchestrator + 4 parallel Sonnet 4.6 `general-purpose` advisors (minimalist / empirical / mechanism / ROI-skeptic). **Commit:** this endsession commit.

**Changes made (additive docs only, +33/−3, no code/graph change):**
- **NEW `reference/glossary.md`** — canonical forward vocabulary + retired-term decode + the consistency mechanism + queued follow-ups.
- `CLAUDE.md` — NEW `## Vocabulary` stub (3 terms + `step`) with the "paste terms into naming/sequencing subagents" instruction (closes the subagent-doesn't-load-CLAUDE.md gap = the "give it necessary info" answer).
- `working/nomenclature-reform-proposal.md` — superseded preamble (the 6-term scheme is no longer live).
- **NEW memory `feedback_vocabulary_canon`** (+ MEMORY.md index). `working/todos.md` — scheme marked DONE + 2 narrow follow-ups queued. Current State GATED line updated.

**Decisions:**
- Matt rejected the 2026-06-12 **six-term** scheme as overkill ("six is too many, I don't know what they mean") and ran a 4-lens advisory fan-out. Result: **3 capitalized terms + 1 lowercase word** — **Pass** (grandfathered numbered corpus sweeps) · **Track** (named workstream; lettered idiom retired) · **step** (lowercase, ordered sub-unit; replaces Stage/Plate/Phase/Wave) · **Tier** (confidence **1–5 only**, never work/process — the one rule with teeth, since Tier is stamped on edge data). Empirical advisor confirmed the famous collisions are mostly already tidied (S99/S101/S102); the only live ambiguity was Track, the only data hazard was Tier overload.
- **Full ~175–250-edit retroactive doc sweep DECLINED** as churn-for-tidiness (re-creates the S102 "timestamp diffs bury the real change" problem). History glossary decodes old docs; move forward. Two narrow follow-ups queued instead: rename live non-confidence "Tier"→class/level (the only data-error fix); pull-channel pointer in ~8 live agents. Grep linter deferred until drift recurs.
- **Mechanism** (Matt's "keep it consistent + give it necessary info"): one source of truth (`reference/glossary.md`) + CLAUDE.md stub + **push** (orchestrator pastes vocab into naming/sequencing subagent prompts) + **pull** (queued agent-def pointers). Reuses existing vocab-lockdown / drift-detection patterns, no new infra.
- **Repo-reorg half of Fable cleanup NOT taken up** (Matt's scope choice); mostly overtaken by S99/S101 hygiene anyway.

**What's next** — 2 of the 3 next-move decisions remain, both Matt's (board order #1 → #2):
- → **#1 `PRECEDES`/`FOLLOWS`** — needs vocab-add OK (D3; absent from vocab; bumps the 166 count) + grouping basis (0 dated events share a `PART_OF` parent). $0 deterministic.
- → **#2 causal `TRIGGERS`** — already in vocab; needs sign-off on the Robert's Rebellion pilot (interpretive/pollution-sensitive). Continue: `progress/continue-prompts/2026-06-16-next-move-decisions.md` (**Sonnet 4.6**).

---

*(Sessions 104–106 will be appended here as they rotate out of the live worklog. This file now holds S102–S103 (2/5); it fills to 5 entries — S102–S106 — before a new archive023 begins.)*
