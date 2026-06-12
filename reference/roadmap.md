# Roadmap — From the Graph We Have to the Things Matt Wants to Build

> **Status:** Written 2026-06-12 (Fable subagent, read-only session). This is a **map plus decision
> points, not a fixed plan.**
> **Edge count:** `edges.jsonl` = **4,760** as of 2026-06-12 (3 curator pilot edges added S91; older continue prompts citing 4,757 are stale on this one field). The destination features are Matt's list; the sequencing past the next
> two steps is deliberately undetermined — the Mode 3 dip's failure data decides it.
> Sources: `working/audits/fable-audit-2026-06-11/{synthesis,graph-deep-dive}.md`,
> `working/infobox-merge/spec.md`, `reference/{architecture,agents,foreshadowing-events}.md`,
> `.claude/agents/` stubs, `working/todos.md`, `worklog.md` STATUS.
> If the design-doc consolidation lands, this seeds `reference/design/features.md`; it stands alone regardless.
>
> **Execution-mode tags** (per the project's standing rules):
> **[SCRIPT-$0]** — deterministic Python, no LLM, no approval friction beyond normal review.
> **[LLM-GATED]** — costed model work; requires lockdown + smoke + gate per the drift-detection and
> model-fit rules. Rough $ given only where prior runs calibrate it; otherwise "unknown until smoked."
> **[MATT-DECISION]** — design or judgment call; no amount of scripting closes it.

---

## 1. Where the graph is now (verified 2026-06-11)

- **8,261 nodes**, **4,760 edges** with verbatim book quotes (4,728/4,760 carry evidence_quote;
  3,782 file:line verbatim-located), 0 orphans, ~78% strict precision, working event reification
  (583 event nodes, 948 role edges).
- **14.7% of nodes touch any edge.** The connected core (~1,216 entities, hubs like jon-snow at 336
  edges) is dense and high-quality; everything off-POV-screen is dark — characters 20%, houses 4.5%,
  locations 5.2%, titles 2.6%.
- The fix is parsed and sitting on disk: the wiki infobox layer (20,614 typed rows,
  `working/wiki/data/infobox-data.jsonl`), spec'd at `working/infobox-merge/spec.md`. Expected:
  **4,760 → 21,800 edges, connectivity 14.7% → 71.0%**, $0, one Python script.
- Query tooling exists: `scripts/graph-query.py` (`--neighbors`/`--path`/`--health`/`--event-participants`).
- Theories (45 nodes) and prophecies (2 nodes) are **effectively 100% dark and stay dark after the
  merge** — their wiki pages have no infoboxes.

## 2. The fixed part of the sequence (NOW → NEXT → THE FORK)

Only two steps are actually decided:

1. **NOW — Infobox merge** [SCRIPT-$0, greenlit]. Spec done; dry-run → Matt reviews
   `dry-run-report.md` → `--apply` in a later session. Folds in two hygiene fixes (115 orphan
   endpoint slugs, 948 rows missing `typed_by`/normalized refs).
2. **NEXT — Mode 3 grounded-agent dip on the MERGED graph** [LLM-GATED, small;
   continue prompt: `progress/continue-prompts/2026-06-11-phase2-mode3-dip.md`, Opus]. An agent
   actually traverses the graph answering real questions; we log where it fails.
3. **THE FORK** — everything after is decided by dip data, not by this document. The explicit
   decision points:

   - **D1 — What do the dip failures cluster on?** [MATT-DECISION]
     - *Lookup gaps / wrong-or-missing edges* → prioritize backfill Tracks A/B/C (~$25–75,
       300–850 edges, `working/edge-modeling/post-plate5-backfill-design.md`) and followup #9
       (historical-anchor structural backfill, $0 phase first).
     - *Structural confusion* (event hubs, arcs) → the 2 deferred restructures (followup #12) and
       hub-queue triage (#3).
     - *Expressiveness gaps* ("the graph can't say how Sansa FEELS about Cersei", "no theory
       evidence", "when did this happen?") → that's the signal to start a destination-feature pass
       (§3) instead of more backfill.
   - **D2 — Which destination feature first?** [MATT-DECISION] The primary goal is character dialog
     (§3.1), but theories (§3.2) are the darkest layer and the cheapest to *partially* light up
     deterministically. Dip questions that go unanswered tell us which.
   - **D3 — Temporal schema shape** [MATT-DECISION] — blocks all chronology promotion (§3.4):
     dedicated edge types (`OCCURRED_IN_YEAR`, `PRECEDES`) vs optional per-edge fields
     (`start_year`/`end_year`/`precision`/`scope`). Both designs sketched (S26/S29 todos); neither locked.
   - **D4 — ABOUT/MENTIONS vocabulary gate** [MATT-DECISION] — before any theory-page prose-link
     script runs (§3.2, Step 1), confirm that `ABOUT`, `MENTIONS`, or equivalent edge types are
     locked in `reference/architecture.md`'s vocabulary. This is a worklog Active Decision: new edge
     types go through the normal lockdown procedure (architecture.md first, then emitters) — even
     for the cheapest [SCRIPT-$0] step. No spend required, but the vocabulary gate must have a
     recorded GO verdict before the script is written.

**Explicitly shelved, and what un-shelves each:**

| Shelved item | What it is | Un-shelve trigger |
|---|---|---|
| Events-Haiku promotion | 1,617 typed rows at `_events-haiku-bulk/`, S81 cross-model NO-GO (borderline); absorbed into backfill Track B | Dip shows event-edge gaps Track B's re-bucketing would fill |
| Dialogue tail (v2.1) | Dialogue-derived edge escalation, deferred at the Events NO-GO | Dip shows interpersonal/conversational edge gaps; runs with edge-modeling lessons applied |
| Prose-comention wiki edges | ~6k Sonnet+Haiku emits, deprecated S65/S84, reaffirmed 2026-06-11 | Effectively never as a layer; at most mined as a *candidate pool* by a future curator pass |

---

## 3. The destination features

### 3.1 Talking to a character — THE primary goal

*(memory: "real project goal — graph quality for agents"; any chat layer is downstream and unstyled)*

**(a) Needs:** a graph an agent can traverse to ground dialog: factual spine (genealogy, fealty,
titles — the lookup questions users ask first), lived relationships with quotes (how the character
*feels*), a voice profile per POV (how they *talk*), POV-locked perception edges (how they see
others vs. how others see them), and chapter-evidence pointers for quoting source.

**(b) Exists:**
- The lived-relationship layer: 4,760 cited edges, affect/interaction-heavy (OPPOSES 265, SERVES 255,
  DISTRUSTS 204, HATES 173…), verbatim quotes. This is the part nobody else has.
- The factual spine arrives with the infobox merge (~17,040 new edges; characters 20%→97% connected).
- Traversal tooling (`graph-query.py`), 0-orphan health, alias resolution (1,433 entries).
- `PERCEIVED_AS` + most of the proposed perception sub-vocab (`FEARS`, `MOURNS`, `DISTRUSTS`,
  `ADMIRES`) already in the locked vocabulary — pre-declared, zero instances.
- Stubs: `voice-analyzer.md` (Sonnet), `perception-mapper.md` (Opus). Schemas not designed; never run.
- `extractions/voice/` is **empty**. Zero voice profiles, zero perception edges.

**(c) Missing:** voice-profile schema; perception-output schema + final vocab review; the actual
Pass 3 runs; chapter-evidence pointers on nodes (so the dialog agent can pull prose, not just edges).
Honest note: Pass 3 scoping is **speculative** — the stubs describe intent, not a tested design, and
per-POV full-arc reads are the biggest token sink in the whole remaining roadmap. No prior run
calibrates it.

**(d) Sequence to close:**
1. [SCRIPT-$0] Infobox merge (shared prerequisite — already greenlit).
2. [MATT-DECISION] Mode 3 dip review: does dialog grounding fail on facts, feelings, or voice?
3. [MATT-DECISION] Voice-profile schema + perception schema + identity-split handling
   (Theon/Reek, Arya/No One) + per-POV-vs-grouped batching. One design session.
4. [LLM-GATED] voice-analyzer smoke: 1 POV (e.g. a short-arc POV) on Sonnet per model-fit, judged
   before scale. Full run ≈ all POV characters across 344 chapters — cost unknown until smoked;
   the only calibration anchor is that full-corpus passes have historically run $95–$340.
5. [LLM-GATED] perception-mapper: per (POV, target) pairs, after voice profiles (blind-spot data
   informs perception reads). Cost unknown until smoked; Opus-stubbed, smoke on Sonnet first.
6. [SCRIPT-$0] Chapter-evidence backfill — "see also: agot-bran-01…" pointers per node from the
   existing mention-index (todos § Dormant — the chapter-evidence backfill component of the prose-edge era's richest-form design). Pure Python, runnable anytime.
7. [SCRIPT-$0] Display-bullet regeneration from edges.jsonl (followup #1) so node files match the
   merged graph an agent reads.

### 3.2 Theory exploration

**(a) Needs:** theory/prophecy nodes connected to the entities they discuss (so traversal *reaches*
them), SUPPORTS/CONTRADICTS evidence edges from book text, and per-theory confidence scoring.

**(b) Exists:** 45 theory nodes + 2 prophecy nodes — **1 edge total, and it looks like a
misresolution** (synthesis.md). Vocab has prophecy/evidentiary categories (`FULFILLS`,
`APPEARS_TO_FULFILL`-class, `FORESHADOWS`) pre-declared. Stubs: `theory-extractor.md` (Sonnet),
`theory-evidence-scorer.md` (Opus). `extractions/patterns/` empty.

**(c) Missing:** `reference/theory-seeds.md` was **never written** (hard blocker named in both
stubs). Prophecy nodes are undercounted — 2 nodes for a prophecy-saturated series; Azor Ahai,
valonqar, dragon-has-three-heads exist as wiki pages but weren't typed as prophecies. No ABOUT/
MENTIONS edges from theory pages to their subjects. Zero evidence extraction. Pass 5 scoping is
speculative — never smoked, costs unknown.

**(d) Sequence to close:**
1. [SCRIPT-$0, behind **D4**] Mint confidence-tier-3/4 ABOUT/MENTIONS edges from the 45 theory pages' own prose links
   (`sources/wiki/_raw/` cache → alias-resolver → existing nodes). Synthesis option (a): cheap,
   deterministic, makes the layer *reachable* even before any analysis. Prerequisite: **D4** (ABOUT/MENTIONS vocabulary gate) must have a recorded GO verdict in the worklog before this script is written.
2. [MATT-DECISION] Curate `reference/theory-seeds.md` (top 20–30 theories, descriptions, priors)
   and the prophecy-node minting list. This is Matt-taste content; agents shouldn't pick the canon
   of theories.
3. [SCRIPT-$0] Mint the missing prophecy nodes from their wiki cache pages once the list is decided
   (promotion machinery already exists).
4. [LLM-GATED] theory-extractor, per-theory corpus scan over Pass 1 extractions (not raw prose) —
   smoke 1 theory (R+L=J is the densest test), gate, then scale. Cost unknown until smoked.
5. [LLM-GATED] theory-evidence-scorer — one focused reasoning task per theory over the evidence
   dump; cheap per unit (~30 theories × single-file reasoning). Findings land in
   `curation/candidates.md` — **agents propose, Matt decides** applies with full force here.

### 3.3 Foreshadowing / Chekhov's-gun lookups

**(a) Needs:** `FORESHADOWS` edges (chapter detail → event node), gun-status tracking
(planted-but-unfired details with every reinforcement cited), `FULFILLS` edges into prophecy nodes.

**(b) Exists:** `reference/foreshadowing-events.md` — 30 confirmed events + 15 unfired Chekhov's
guns, each with location + scan-for guidance. `FORESHADOWS`/`FULFILLS`/`DREAMS_OF` locked in vocab,
zero instances. 583 event nodes (most of the 26 events likely have hubs — unverified). Pass 1
extractions for all 344 chapters as the scan surface. Stubs: `foreshadowing-scanner.md` (Sonnet),
`chekhovs-gun-tracker.md` (Opus — complementary job: absences, not confirmations).
`extractions/foreshadowing/` empty. **Zero extraction run.**

**(c) Missing:** output schema, per-event-vs-per-chapter scan strategy, confidence criteria (what
makes Tier 2 vs Tier 4 foreshadowing), the pattern-library expansion of the reference file
(todos § Future Passes: setup/payoff-shape/textual-pattern per gun — "the pattern library, not the
named-events list, is the real scanner input"). All costs unknown until smoked.

**(d) Sequence to close:**
1. [SCRIPT-$0] Map the 30 events + 15 guns to event-node slugs (event-alias-resolver, 922 phrases,
   already exists). Surfaces which anchors lack nodes — those mint first.
2. [MATT-DECISION] Expand foreshadowing-events.md into the pattern library; lock the mapping
   schema + confidence criteria; pick scan strategy.
3. [LLM-GATED] foreshadowing-scanner smoke: 1 dense event (Red Wedding) over its prior-chapter
   Pass 1 extractions; gate; scale to 26. Per-event scans re-read large prior-chapter ranges —
   expect this to be a real spend; unknown until smoked.
4. [LLM-GATED] chekhovs-gun-tracker: 15 guns, narrower corpus per gun (mention-tracking, not
   interpretation); likely the cheaper half. Output to `working/foreshadowing/`, findings → curation.

### 3.4 Timeline / chronology queries

**(a) Needs:** in-world year anchors (AC) on events, ordering edges within/across years, and
narrative-time ordering for chapter-anchored facts; a query layer that joins them.

**(b) Exists — more than any other feature:**
- **2,245 chronology events already extracted** from 74 year pages →
  `working/wiki/data/chronology-events.jsonl` (S29), awaiting a temporal-edge schema.
- **Narrative-time scoping already built** (S76): `scripts/stage4-edge-temporal-scope.py` annotates
  every edge with `(book_order, chapter_number)` from its evidence cite →
  `working/wiki/data/edges-temporal-scoped.jsonl` (+58 tests). Canonical edges.jsonl itself carries
  no temporal fields — the annotation is a sidecar.
- Pass 1 `time_markers` captured per chapter (fan-style relative reconstruction is a dormant todo).
- Stubs: `chronology-extractor.md`, `event-orderer.md` (both explicitly deferred to lower-priority work, both Opus-stubbed).

**(c) Missing:** the schema decision (D3) — `OCCURRED_IN_YEAR`/`PRECEDES`/`FOLLOWS` are NOT in the
locked vocab, and the alternative per-edge-fields design is also unlocked. Promotion of the 2,245
rows. Sub-year ordering. Also: 10 year pages mis-typed as `character.human` nodes (todos § Small Fixes).

**(d) Sequence to close:**
1. [MATT-DECISION] **D3 — lock the temporal schema** (edge types vs per-edge fields; year pages as
   string targets vs nodes). Vocabulary-lock procedure: architecture.md first, then emitters.
2. [SCRIPT-$0] Deterministic promotion of chronology-events.jsonl rows whose event resolves to an
   existing node — the extraction already happened in S29; most of chronology-extractor's stubbed
   job is *already done deterministically*. Skip-and-log the residue.
3. [SCRIPT-$0] Year-page mistype fix (10 nodes) — bundles naturally here.
4. [SCRIPT-$0] Join the S76 narrative-time sidecar into graph-query.py output ("as of ACOK…").
5. [LLM-GATED] chronology-extractor only for the unresolved residue; event-orderer
   (sub-year PRECEDES from cite_refs + causal language) after it. Both unknown until smoked; both
   both explicitly deferred as lower-priority today.

### 3.5 Spoiler-gated reading companion — ON THE MAP, deliberately deferred

**(a) Needs:** `first_available` on nodes + edges, and a query-time additive filter.

**(b) Exists:** an explicit **v1 = fully open** policy (S26, reaffirmed): no gating at query time,
backfill is NOT a blocker for anything shipping. The raw material for a deterministic backfill is
all on disk: Pass 1 mention-index (per-chapter entity lists, ~70% resolution), chapter file
ordering, infobox page-level `cite_refs` per book, book-pass1 edges carrying file:line refs.

**(c) Missing:** the backfill scripts themselves; per-row infobox chapter anchors (the parser
strips `<sup>` markers — recovering them is a targeted re-parse of infobox `<td>` HTML, logged as a
spec follow-up); the v2 gate design. Existing `first_available` values are untrusted (parser-bug
class — architecture.md says don't hand-reason them).

**(d) Sequence to close (all post-first-release by policy):**
1. [SCRIPT-$0] Node `first_available` = earliest chapter mention from the mention-index + chapter order.
2. [SCRIPT-$0] Edge `first_available` = its evidence chapter (book edges already cite file:line;
   reified rows cite chapter labels — Fix B normalizes those).
3. [SCRIPT-$0, optional] Targeted infobox `<sup>` re-parse for per-row anchors on wiki edges.
4. [MATT-DECISION] When to un-defer, and the v2 additive-gate design in the query layer.

The striking thing: this feature's road is **almost entirely free** — it's deferred by sequencing
choice, not by cost.

### 3.6 Already-shipped capabilities + the open end

**Shipped (use them, don't rebuild them):** cross-identity and disambiguation are largely DONE as
capabilities — alias-resolver (1,433 entries) + event-alias-resolver (922 phrases),
`cross-identity-detector` (full prompt) + reviewer, impersonation-edge policy, duplicate-detector /
orphan-edge-finder / schema-drift-auditor / citation-validator all at full-prompt status. Cross-
identity matching was a named design value (Theon↔Reek) and the machinery exists.

**Pass 6 — discovery-agent [LLM-GATED + MATT-DECISION]:** open-ended pattern mining across all
prior outputs. Runs LAST by design — it needs Passes 3–5 outputs to see anything the cheaper passes
wouldn't. Scoping strategy is an unsolved design problem (the stub's own TODO list says so). Output
is Tier 3–5 candidates to `curation/` only. Don't schedule it; let it stay the horizon item.

---

## 4. How much of the remaining road is free

Counts are work items from §3 sequences (shared prerequisites counted once, under 3.1).

| Feature | [SCRIPT-$0] | [LLM-GATED] | [MATT-DECISION] | Readiness one-liner |
|---|---|---|---|---|
| 3.1 Character dialog | 3 | 2 | 2 | Facts arrive with the merge; voice/perception = empty dirs + stubs, biggest unknown spend |
| 3.2 Theory exploration | 2 | 2 | 1 | 45 nodes, ~0 edges; prose-link script lights it up cheaply; seeds file never written |
| 3.3 Foreshadowing | 1 | 2 | 1 | 30 events + 15 guns in reference file; vocab ready, zero runs ever |
| 3.4 Chronology | 3 | 1 | 1 | Most data already extracted (2,245 rows); blocked only on schema decision D3 |
| 3.5 Spoiler gating | 3 | 0 | 1 | Nearly all free; deferred by policy, not cost |
| 3.6 Discovery | 0 | 1 | 1 | Horizon item, runs last, unscoped |
| **Total** | **12** | **8** | **7** | |

**The free road — [SCRIPT-$0] items runnable without any new spend or smoke gate:**

1. Infobox merge dry-run + apply (greenlit; the one true next step)
2. Theory-page prose-link ABOUT/MENTIONS edges (un-darkens theories/ for traversal)
3. Foreshadowing 26-events/15-guns → event-slug mapping
4. Chronology-events.jsonl deterministic promotion *(behind D3 schema decision)*
5. Year-page mistype fix (10 nodes)
6. Chapter-evidence backfill pointers per node
7. Display-bullet regeneration from edges.jsonl (followup #1)
8. Narrative-time sidecar joined into graph-query.py
9. `first_available` node + edge backfill scripts *(behind the post-first-release policy)*
10. Pass-1-vs-wiki coverage audit (todos [OPEN] — feeds every feature's gap analysis)

Roughly **half the remaining road is free**; the costed half (8 LLM-GATED items) is concentrated in
Passes 3–5, where every cost estimate is honest guesswork until a smoke run exists. Prior
calibration points for scale: Stage-1 wiki promotion $95 / 855 nodes ($2.58/bucket), backfill
Tracks A/B/C estimated $25–75, the abandoned Sonnet events re-run quote ~$340 — full-corpus
analytical passes will land in that order of magnitude, per pass, and the model-fit rule
(cheapest viable, smoke before upgrade) applies to every one.

## 5. The honest caveat

Passes 3–6 have never run. Their agent files are stubs with TODO lists, their schemas are
undesigned, their costs are uncalibrated, and the project's own history (wiki-comention: ~$250 and
five weeks → deprecated, while the deterministic layer sat parsed on disk) is the standing argument
for not pre-committing to them. The discipline stack — Python-before-agent, lockdown-before-long-
passes, smoke-before-spend, agents-propose-Matt-decides — is the plan; this document just maps
where it gets applied next. The dip decides; the map only shows the roads.
