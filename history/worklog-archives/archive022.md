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

### Session 104 — PRECEDES ordering edges + causal CAUSES pilot (the 2 remaining next-move decisions) (2026-06-17)
**Detail:** `history/session-details/session-104.md`
**Model:** Opus 4.8 orchestrator + 1 fresh `general-purpose` verification subagent. **Commit:** this endsession commit.

**Changes made (edges + vocab + docs; +176 edges):**
- **Decision #1 — `PRECEDES` ordering edges SHIPPED.** Added `PRECEDES` only to the locked vocab (new "Temporal & Sequencing" subsection in `architecture.md`; `FOLLOWS`/`OCCURRED_IN_YEAR` deliberately NOT added); vocab **166 → 167**, both count-tests updated. New `scripts/build-precedes-edges.py` → **174 edges** (17 same-book narrative + 157 cross-year), Tier-3, `evidence_kind: derived-chronology` (7th kind), `typed_by: python-chronology-chain`, each tagged `order_basis`. Basis: global year-chain by `occurred.ac_year`; same-year tiebreak by `narrative_first` but **restricted to same-book** (reading-order proxy inverts cross-book — caught + fixed the wrong `red-wedding→renly-wedding` edge). Unit model (each `(year,book)` nf-run = a unit, bridged cross-year to adjacent-year reps) keeps all 117 events in one connected timeline; also fixed consecutive-floater-year ordering.
- **Decision #2 — causal pilot SHIPPED (small).** 2 `CAUSES` edges (Tier-2, `candidate_kind: causal-curator-pilot`): `battle-of-the-trident → sack-of-kings-landing → coronation-of-robert-i-baratheon`. Typed `CAUSES` not `TRIGGERS` (coarse battle-node granularity; the specific spark = Tywin's gate-opening, no node). Both `verified_by` a fresh subagent against the local cache; EDGE 2 re-cited to `Coronation_of_Robert_I_Baratheon` per the verdict.
- `edges.jsonl`: **21,993 → 22,169**; edge types 125 → **127**; orphans **62 unchanged**. Backups: `_regrounding/edges-pre-{precedes,causal-pilot,recite}-2026-06-17.jsonl`. pytest 1297 pass / 1 documented `cwd-is-tmp` fail.

**Decisions:**
- Matt picked **#1 first**, then **#2**. #1 sub-calls: PRECEDES-only / global-year-chain / P2-floater-bridged / **same-book narrative only** (chosen after a fresh-eyes case showed `narrative_first` inverts across books). #2: emit as **CAUSES** (not TRIGGERS — overclaims at this granularity); **defer** minting the 3 Rebellion spark-beat nodes (abduction/executions/demand) to a dedicated track. **NEW standing method (Matt):** interpretive/causal edges are verified by **fresh subagents against the LOCAL wiki/book cache** — Matt gates at policy level, not per-edge (memory `feedback_subagent_verify_not_matt`). Unblocks scaling causal work.

**Post-endsession continuation (same day, S104):** Matt asked for unattended follow-up work; a background agent died to a network error so this ran inline.
- **Inverted `PART_OF` fix SHIPPED** (commit `e6c031015`): dropped 16 war→battle inversions graph-wide (15 with correct forward edge + 1 malformed `roberts-rebellion→tower-of-joy`, target is a location); left 1 flagged (`shadow-war→targaryen-campaign-in-slavers-bay`, ambiguous war-vs-campaign). Root cause = S94 infobox merge (no direction guard on conflict/part-of field). edges 22,169→22,153.
- **Causal track Phase 1+2 for Robert's Rebellion DONE** (was "deferred"): minted **3 spark-beat nodes** (`abduction-of-lyanna`, `execution-of-brandon-and-rickard-stark`, `aerys-demands-ned-and-robert`; `event.incident`/`event.execution`, tier-1, 282 AC, local-source `## Quotes`) + targeted index + alias rebuild (nodes 8,518→8,521). Wired the full spark chain **verified by a fresh subagent** (all CONFIRM): `tourney-at-harrenhal —CAUSES→ abduction —CAUSES→ executions —TRIGGERS→ demand —TRIGGERS→ roberts-rebellion` (E1/E2 CAUSES not TRIGGERS per verifier — mediated). edges 22,153→22,157. All `verified_by: subagent-local-source-check-20260617`.
- State now: **8,521 nodes / 22,157 edges**, 62 orphans, pytest 1297 pass / 1 documented fail.

**What's next:**
- → **NEXT = a PURE-ANALYSIS session (Matt's call, S104)** on the strategy for causal/narrative-arc edges across the WHOLE graph (scaling beyond Robert's Rebellion). No graph writes — produce a prioritized plan. `progress/continue-prompts/2026-06-17-causal-edges-and-spark-nodes.md`.
- `shadow-war→targaryen-campaign-in-slavers-bay` **RESOLVED S104** (subagent vs local wiki): KEEP as-is — the shadow war (Sons of the Harpy insurgency in Meereen) is a wiki-attested component of the broader Slaver's Bay campaign.
- Small-fix backlog (subagent-surfaced S104): `shadow-war` + `targaryen-campaign-in-slavers-bay` carry junk `DEFEATS`/`FIGHTS_IN` edges (misparsed infobox fields) and are mistyped `event.battle`. → todos § Small Fixes.

---

### Session 105 — Causal-arc scaling strategy + Bran's-fall smoke test #2 + advisory board (2026-06-18)
**Detail:** `history/session-details/session-105.md`
**Model:** Opus 4.8 (1M context) orchestrator + 5 Sonnet 4.6 `general-purpose` subagents (2 edge-verification + 4-lens advisory board). **Commit:** this endsession commit.

**Changes made:**
- **NEW `working/causal-arc-strategy-2026-06-18.md`** — the causal/narrative-arc scaling plan (rubric + prioritized arc list + cost model + 7 policy Qs + the smoke-test analysis + advisory-board outcome + the agency-collapse lesson). This is the deliverable of the continue prompt.
- **Built the "Bran's fall" causal arc (smoke test #2)** — `edges.jsonl` **22,157 → 22,174**, nodes 8,521 → **8,525**, edge types **127 → 128** (`MOTIVATES` now live). Chain: `bran-witnesses-jaime-and-cersei →TRIGGERS→ jaime-pushes-bran-from-the-tower →CAUSES→ bran-s-direwolf-kills-the-assassin →CAUSES→ littlefinger-names-the-dagger-as-tyrion-s →CAUSES→ catelyn-seizes-the-moment-and-arrests-tyrion →CAUSES→ gregor-raids-the-riverlands` (HARD STOP, no edge to WO5K). Plus role edges on all new beats + `capture MOTIVATES tywin` + `petyr DECEIVES catelyn`. 5 new nodes minted (`bran-witnesses…`, `jaime-pushes…`, `littlefinger-names-the-dagger…` [event.deception], `gregor-raids-the-riverlands` [event.incident]; 1 dup `catelyn-captures-tyrion-at-the-crossroads-inn` minted-then-deleted). 2 pre-existing beats enriched (`bran-s-direwolf-kills-the-assassin`, `catelyn-seizes-the-moment-and-arrests-tyrion`). All causal edges Tier-2 + fresh-subagent-verified; role edges Tier-1.
- Backups: `_regrounding/edges-pre-bran-arc-2026-06-18.jsonl`, `…-littlefinger-fix-2026-06-18.jsonl`. Targeted index builds (`--slug`) + alias rebuild. 62 orphans unchanged; pytest 1297 pass / 1 documented `cwd-is-tmp` fail.

**Decisions:**
- Session started as pure-analysis (per continue prompt); Matt expanded scope to a live smoke test + a 4-lens advisory board (narrative-craft / graph-modeling / canon / skeptic). **Parent-node recommendation (awaits Matt's ratification): causal-chain-as-arc, NO umbrella parent nodes** — deliver "show me the whole arc" via a `--causal-chain` traversal primitive, not a parent hub (dissolves the multi-parent-ownership trap; supersedes the umbrella-vs-chain fork in the parked arc-wave1 prompt). **Tier policy:** causal edges capped Tier-2 (interpretive). **Three reusable lessons banked:** (1) **pre-mint dedup lookup** is mandatory (a dup was minted this session); (2) **agency-collapse check** — before `A CAUSES B`, model the human decision between them (insert a beat node OR `MOTIVATES`→actor + COMMANDS_IN); (3) cost model is "patchwork mint," not "pure wiring."

**What's next:**
- → **Matt ratifies the parent-node rec**, then: build the `--causal-chain` directed-traversal primitive (Track 7 prerequisite), then run the first Tier-A arc batch (Sack of KL, Purple Wedding) dip-gated. Continue: `progress/continue-prompts/2026-06-18-causal-arc-execution.md`.

---

*(Session 106 will be appended here as it rotates out of the live worklog. This file now holds S102–S105 (4/5); it fills to 5 entries — S102–S106 — before a new archive023 begins.)*

### Session 106 — Causal-arc execution: `--causal-chain` primitive + Sack-of-KL & Purple-Wedding arcs (2026-06-19)
**Detail:** `history/session-details/session-106.md`
**Model:** Opus 4.8 orchestrator + 1 background `general-purpose` doc agent + 4 `general-purpose` subagents (2 arc-research + 2 fresh edge-verification). **Commit:** this endsession commit.

**Changes made:**
- **Step 1 — `--causal-chain <slug>` traversal primitive SHIPPED** in `scripts/graph-query.py` (walks CAUSES/TRIGGERS/MOTIVATES transitively, both directions; PRECEDES deliberately excluded as pure-chronology). +10 tests (`tests/test_graph_query_edges.py`). The Track-7 prerequisite that makes causal arcs queryable from any beat — and what made the chain-as-arc decision real ("show me the whole arc" without an umbrella node).
- **NEW `reference/narrative-arc-glossary.md`** (~28 terms, 5 sections) — data-model/method companion to `glossary.md` (process vocab) + `architecture.md` (schema). Written by a background agent.
- **Sack of King's Landing arc** — 4 new beat nodes (`pycelle-opens-the-gates-of-kings-landing` [event.deception], `aerys-commands-the-city-burned` [event.incident], `slaying-of-aerys-ii-the-kingslaying` [event.assassination], `murder-of-elia-martell-and-rhaegars-children` [event.assassination]) + **21 edges** (14 role Tier-1 + 4 SUB_BEAT_OF + 3 causal Tier-2). Mint script `scripts/mint_sack_kl_arc.py`; backup `_regrounding/edges-pre-sack-kl-arc-2026-06-19.jsonl`.
- **Purple Wedding arc** — 4 new beat nodes (`sansa-receives-the-poisoned-hairnet` [event.deception], `tyrion-accused-of-poisoning-joffrey` [event.incident], `trial-of-tyrion-lannister` [event.trial], `littlefinger-smuggles-sansa-out-of-kings-landing` [event.deception]) + **20 edges** (14 role + 3 SUB_BEAT_OF + 3 causal Tier-2). Mint script `scripts/mint_purple_wedding_arc.py`; backup `_regrounding/edges-pre-purple-wedding-arc-2026-06-19.jsonl`.
- **Totals:** nodes **8,525 → 8,533** (+8 beats); edges **22,174 → 22,215** (+41); orphans **62 unchanged**; edge types **128** (no new types); **0 pending** verified_by (all 6 causal edges fresh-subagent CONFIRMED). pytest **1307 pass / 1 documented `cwd-is-tmp` fail**.

**Decisions:**
- **Parent-node rec ratified by Matt → chain-as-arc, NO `event.arc` umbrella nodes** (the `--causal-chain` primitive delivers the whole-arc query; supersedes the umbrella-vs-chain fork in the parked arc-wave1 prompt).
- **Scope = 2 Tier-A arcs as one validating batch** (Matt), NOT a minting fleet — a fleet was considered and rejected as wrong-shaped (arc-minting is low-volume + judgment-heavy + write-conflicting; the agency-collapse check and pre-mint dedup don't parallelize). **D&E noted as main-arc in priority** (Bloodraven-in-the-flesh seeds theory anchors); it stays after in-saga arcs only because its chapters aren't Pass-1-extracted yet.
- **Discipline held end-to-end:** pre-mint dedup gate caught 2 real collisions (`fall-of-kings-landing` = the Dance-era fall, kept distinct; the existing flat role-layer on the sack hub + the existing Littlefinger/Olenna conspiracy on the death node — NOT duplicated). Agency-collapse modeled (Tywin COMMANDS_IN vs Gregor/Amory AGENT_IN; PW whodunnit = zero `tyrion POISONS joffrey`, Tyrion VICTIM_IN only). Causal edges Tier-2-capped; role Tier-1. All 8 beats natural-phrase discoverable (closes the S105 Track-7 gap). Both fresh verifiers returned ALL-CONFIRM.

**What's next:**
- → **Per the strategy's dip-driven cadence: re-run an arc-weighted Mode-3 dip before committing Tier B** (Catelyn-frees-Jaime→Red-Wedding-feed; Greyjoy→Theon-hostage→Northern-invasion). Don't mass-mint. Strategy: `working/causal-arc-strategy-2026-06-18.md`; continue prompt `progress/continue-prompts/2026-06-18-causal-arc-execution.md` (Step 1 done; Step 2 ongoing, dip-gated). (**Sonnet 4.6**)
- Small cleanups surfaced by verifiers (→ todos § Small Fixes): duplicate `robert-baratheon` vs `robert-i-baratheon` node; sack hub's junk `DEFEATS: Elia of Dorne` infobox edge.
