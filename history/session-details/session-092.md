# Session 92 — The Fable Audit: full project audit, infobox-merge greenlight, and the documentation truth-pass

```yaml
session: 92
dates: 2026-06-11 → 2026-06-12
model: Fable 5 (orchestrator) — first Fable session on this project
subagents: ~40 total (Fable for judgment/prose/adversarial critique; Sonnet for mechanical edits,
  manifests, and the merge script; one script-builder)
spend_events: monthly extra-usage cap hit TWICE mid-session (2026-06-11 night, 2026-06-12 mid-wave);
  both walls fully recovered with zero lost or broken work
commission: Matt's audit ask (chat) + working/reply-to-audit-session-2026-06-11.md (the full work order)
```

---

## 1. How this session started

Matt opened with two asks: examine where the project is after 91 sessions of aggressive growth, and
push Fable 5 to its limit doing it — "read through the worklogs, trials, failures, successes. Do an
audit." Plus the substantive question: **can the staged wiki edge work be salvaged or connected to the
book-derived edges, is that necessary, and should the next move be enrichment or dialog?**

Two read-only Fable subagents ran in parallel:

- **History auditor** — read all 18 worklog archives (~90 session entries) + spot-checked session
  details and cost CSVs. Produced the phase-by-phase arc (11 phases), the honest failures list
  (15 dead ends), the compounding-successes list, the process-pattern analysis (what repeatedly
  worked/failed, quantified), the doc-rot catalog, and the spend ledger (~$770–830 recorded;
  ~$4,400+ avoided by gates).
- **Graph deep-diver** — quantified the edge layer (4,760 rows, composition by evidence_kind/type/tier),
  the node-isolation problem (**8,261 nodes, only 14.7% touch any edge** — characters 20%, houses 4.5%,
  titles 2.6%), and the THREE latent wiki edge layers.

## 2. The central finding and the decision

The deep-dive's verdict, which became the session's headline:

| Wiki layer | Verdict |
|---|---|
| **Infobox-structural** (20,614 rows in `infobox-data.jsonl`, parsed April, typed to 23 vocab types, 92% target-resolvable, **98.4% additive** to book edges) | **MERGE** — a never-shipped deterministic product, not salvage |
| Node-file `## Edges` display bullets (21,129) | Do nothing — same data as above (track_b provenance) |
| Prose-comention/entity emits (~6k Sonnet+Haiku + 1,617 Events-Haiku) | **Stay deprecated** — wiki-prose evidence, no file:line, inconsistent schemas |

The irony, told straight: the project spent ~$150–190 and five weeks (S52–S64) trying to make LLMs
extract edges from wiki *prose*, deprecated it — while the wiki's *structured* data sat fully parsed
on disk for two months, one filter-script from taking connectivity **14.7% → ~71% for $0**.

**Matt accepted the synthesis the same day** and replied with a full work order
(`working/reply-to-audit-session-2026-06-11.md`): infobox merge greenlit (Tier 2 max,
`evidence_kind: wiki-infobox`), prose-comention stays dead, Mode 3 dip re-sequenced to AFTER the
merge, and a 15-step organize/document/spec/build program with two standing rules for the session —
**everything executes through subagents** (orchestrator coordinates and reviews only) and **every
major deliverable gets a fresh-eyes critic** "prompted to find what's wrong, missing, or unclear —
not to admire it."

Also answered from data: Matt's theories/prophecies question — 45 theory nodes / 1 connected (that
one a misresolution), 2 prophecy nodes / 0 connected, zero infobox coverage. That layer is 100% dark
and stays dark after the merge; connecting it is Pass 4/5 territory (mapped in `reference/roadmap.md`).

## 3. What was built (by wave)

**Wave 1 (six agents):** CLAUDE.md + worklog truth-fixes with the new **STATUS — at a glance** block
(the "one trustworthy where-am-I surface"); todos.md 420→232 lines with resolved blocks moved verbatim
to `history/todo-archives/`; the continue-prompt manifest (`progress/continue-prompts/README.md`);
the design-doc structure proposal (Option A: a `reference/design/` 3-doc set — Matt's pick pending);
the infobox-merge spec v1 with computed expected counts; the schema legend.

**Wave 2 (ten agents, relaunched after wall #1):** the 8-file project story at `history/project-story/`
(overview, glossary, five workstream chapters, and the required reification explainer that walks the
Red Wedding end-to-end through live graph data); the honest worth assessment; the nomenclature reform
proposal; `reference/roadmap.md` (features → capabilities → gaps, every item tagged
SCRIPT-$0 / LLM-GATED / MATT-DECISION); plus three critics on Wave 1.

**Wave 3 (nine agents):** spec v2 revision (all critic findings); legend fixes; critics for the
Wave-2 deliverables; `history/` READMEs; `scripts/README.md` (146 scripts, 6 LEGACY wrappers);
the 109-item hub-review triage; the `weirwood run` subcommand (built on `scripts/longrun.sh`,
8-scenario tested, shellcheck-clean).

**Wave 4 (six agents, relaunched after wall #2):** the three critic-fix passes (story, worth
assessment, nomenclature/roadmap); **`scripts/infobox-merge.py` + 75 tests + the dry-run report**;
the small Plate-4/5 followup proposals; the repo-reorg plan.

**Closeout:** session bookkeeping agent (worklog S92 + archive019 rotation, todos refresh, ledger
checkoffs, merge-ship continue prompt); the dry-run report rewritten to be self-explaining at Matt's
request (preamble, TL;DR, 13-term glossary incl. `direction_corrected`, rule-code mapping, per-edge
reading lines, fill-in answer lines on all 11 decisions; 275→594 lines); the graph-cleanup continue
prompt; the Olenna Tier-2 annotation (§6).

## 4. The fresh-critic loop — what it caught

Every major deliverable was reviewed by a subagent that had no part in producing it. Every critic
returned ACCEPT-WITH-FIXES, and every finding was real. The catches that mattered:

- **Merge spec (adversarial critic, the high-stakes one):** independently CONFIRMED the spec's
  biggest claim — `FIELD_EDGE_MAP` in the April infobox parser has **inverted direction on 10 fields**
  (ruler/heir/successor/predecessor/founder/owner/head/cadet-branches): "Acorn Hall · Ruler · Theomar
  Smallwood" would have minted *the castle rules the man*. Invisible for two months because nothing
  ever materialized the endpoints. The critic then found a CRITICAL leak the spec missed: quarantine
  was per-row but the wiki encodes kinship bidirectionally — **Joffrey's quarantined "Fathers" rows
  would re-enter via Robert's own "Issue" row and graph-canonize Joffrey as Robert's biological son
  at Tier 2** (likewise Ramsay·Spouses·"Arya"). Fix: quarantine by fact-key. Spec v2 applied all 9
  findings; merged count moved 17,040 → **17,006**.
- **Worth assessment (hostile critic):** the doc's own headline claim was its least-true sentence —
  "every book-derived edge carries a verbatim quote at exact file:line" (actually 3,782/4,760; 948
  reified edges cite chapter-level). Also missing: single-model-family risk (build, judge, audit all
  Claude variants; precision self-reported), and the ~$800 figure excluding the untracked
  Max-subscription time. v2 replaced the claim and added both.
- **Story critic:** a $250-vs-$150–190 spend contradiction across chapters, the misleading
  "Plate 3 actual: 2,056" row (candidate pool, not minted hubs — 217 minted), and the D&D-fleet
  failure missing from the honest-failures story. All fixed.
- **Roadmap critic:** "26 confirmed events" was wrong (the reference file has 30), and the theory
  layer's cheapest [SCRIPT-$0] item hid a vocabulary gate (ABOUT/MENTIONS aren't in the locked vocab)
  — promoted to named decision point D4.

The session also produced **new graph-defect findings** as a byproduct of writing the reification
explainer from live data: three Red Wedding beats have role edges but no SUB_BEAT_OF link (the
beat-union misses Dacey Mormont's death); `robb-is-killed SUB_BEAT_OF red-wedding` carries a wiki
display-bullet as its evidence quote; the `donal-noye KILLS mag` quote is mismatched; LOCATED_AT's
live direction (event→location) contradicts the design glossary. And the hub-review triage surfaced
a real Plate-5 leak (F1c: a live edge whose source node was never minted) and the fact that the
graph's only Purple-Wedding death signal is **Tyrion's sarcastic false confession at Tier 1**.
All routed to `curation/` + the graph-cleanup continue prompt — no graph writes this session.

## 5. The dry-run result (the gate for next session)

`scripts/infobox-merge.py --dry-run` reproduced spec v2's expected counts **exactly**:
20,614 in → **17,006 merged / 1,128 filtered / 1,037 quarantined / 1,356 deduped / 87 corroborations**;
all 22 edge-type counts ✓ (SWORN_TO 4,064, PARENT_OF 1,645…); 75 new tests green; full suite 1,031
with only 3 pre-existing failures (stale vocab-count-163 tests + cwd_is_tmp); 0.2s runtime.
If applied: edges.jsonl 4,760 → **21,766**, connectivity 14.7% → **71.0%**. `--apply` is gated behind
an explicit flag + automatic backup; **nothing touched graph/ this session.** The report ends with
11 decided-by-default questions + 2 flagged semantic remaps (lady-stoneheart→catelyn-stark,
abel→mance-rayder) awaiting Matt's marks.

## 6. The Olenna question (book canon vs show)

Matt asked whether Olenna-as-Joffrey's-poisoner is book canon or show/wiki contamination. Verified:
the proposed `olenna-tyrell AGENT_IN death-of-joffrey-baratheon` edge traces to **Pass 1 book
extractions** (ASOS Sansa chapters), not the wiki: Dontos gives Sansa the silver hairnet for the
wedding night (Sansa II), Olenna fusses with the hairnet at the feast, Sansa finds a stone missing
during the escape, Littlefinger reveals the orchestration (Sansa V). Books establish it by inference +
Littlefinger's testimony — never witnessed on-page (the show's explicit confession is show-only).
The graph-cleanup continue prompt now pins this edge at **Tier 2, never Tier 1**, with the evidence
chain attached and a Tier-3 fallback option noted.

## 7. Incident postmortem — two spend-cap walls

**Wall #1 (2026-06-11 night):** the 10-agent Wave 2 died simultaneously on the monthly extra-usage
cap. Two single-file partials survived (00-overview.md, worth-assessment.md) — both fully overwritten
on relaunch. **Wall #2 (2026-06-12):** the 6-agent final wave died; the relaunched story-fixer ran
`git diff` first and confirmed its predecessor died before writing anything. A SESSION-CHECKPOINT file
was written to disk at wall #2 so any session could resume cold. Post-session verification mapped
every changed file in the tree to an expected deliverable and tail-checked all 19 key files —
**zero stray or truncated work**.

What made the walls harmless: one-file-per-agent scoping, whole-file writes, verify-then-overwrite
on resume, checkpoint-before-wave. What Matt called out anyway, correctly: fan-out's failure mode at
a wall is N simultaneous mid-flight deaths and a window burned in one burst. **New standing rule
(saved to memory):** sequential or 2–3-agent batches when quota headroom is low/unknown; fan-out only
with fresh quota + the scoping disciplines. The closeout waves ran sequentially under this rule.

**Model-fit lesson (Matt's "push Fable" experiment, honestly scored):** Fable was genuinely load-bearing
for the audit synthesis, the adversarial spec critique, and the worth assessment; it was over-spec for
manifests, inventories, and fix passes — the project's cheapest-viable-model rule confirmed at fleet
scale. ~2.6M+ subagent tokens total.

## 8. Decision stack left for Matt

1. **Dry-run report marks** (11 questions + 2 semantic remaps) → gates the merge ship.
2. **Curation file marks** (hub-triage FIX-22 + small followups) → gates the graph cleanup.
3. **Design-doc structure** (Option A recommended) → gates the consolidation build (~3-4 sessions).
4. **Nomenclature scheme** → gates the one-time terminology sweep.
5. **archive018 judgment** — an agent appended the missing S86 entry to complete S91's recorded
   archiving (letter-violation of the no-edit rule, in-spirit completion; recommend accept).
6. **Repo-reorg P1/P2** (~64 moves, ~1–1.5 sessions) per `working/repo-reorg-plan-2026-06-12.md`.

## 9. Artifact map (everything stays in place per Matt: "keep these files until we are well and truly done")

- `working/audits/fable-audit-2026-06-11/` — audit baseline: synthesis, history-audit, graph-deep-dive,
  doc-rot punch list, worth-assessment v2, design-doc proposal, SESSION-CHECKPOINT (resolved).
- `working/infobox-merge/` — spec v2, self-explaining dry-run report, candidate/quarantine/filter JSONLs.
- `history/project-story/` — 8 chapters. `reference/{schema-legend,roadmap}.md`.
- `curation/{hub-review-triage,plate5-small-followups}-2026-06-12.md` — awaiting marks.
- `working/{nomenclature-reform-proposal,repo-reorg-plan-2026-06-12}.md` — awaiting picks.
- `scripts/{infobox-merge.py,weirwood-run.sh,README.md}` + `tests/test_infobox_merge.py`.
- `progress/continue-prompts/{README.md, 2026-06-12-infobox-merge-ship.md, 2026-06-12-graph-cleanup.md}`.
- `working/{reply-to-audit-session-2026-06-11.md, deliverables-ledger-2026-06-11.md}` — the
  cross-session correspondence pair, all [AUDIT] items checked off.
