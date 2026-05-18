---
session: 52
date: 2026-05-13
model: Opus 4.7 (1M context)
type: design + cleanup
duration_estimate: ~90 min
---

# Session 52 — Edge Vocabulary Drift Cleanup + Stage 4 Reframing

## Why this session has a detail file

Started as a "what's next?" check-in. Turned into substantive architectural cleanup once Matt pushed back on a claim I was confidently asserting. The reasoning chain that surfaced the drift — and the conceptual reframing of what Stage 4 actually buys us — both warrant a long-form record. Pure-execution sessions skip this; this one had real decisions.

## How it started

Matt opened with: *"what's next right now. bit confused. nots ure if worklog was updated last essions"*

Worklog was current — Session 51 had landed the watcher-day orchestration + session-results convention. Three sessions had landed earlier that day (49, 49b, 50). I pointed at Stage 4 prose-edge-classifier as the queued next track, citing the continue prompt at `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`.

Matt said: *"i know we are close to the prose edge thing. which i don't really understand. are we going to start codifying edge? let's be clear what this is, i'm not"*

That was the moment that opened the rest of the session. I explained edges (already exist — wiki infobox-derived, 22 locked types). Matt asked what "the 22-type lock" meant. I explained the lock concept. Matt: *"there are sooo many more that 22 different types of edges. i dont remember locking them"*

He was right.

## The drift discovery

I had been confidently citing "22 edge types" from `reference/architecture.md` § "Wiki Infobox Fields → Edge Type Mapping" without verifying. Matt's pushback forced verification.

Real numbers:

- **architecture.md actually defines 96 distinct edge types** across the `## Edge Types (Relationship Categories)` section (14 subsections: Kinship, Political, Factional, Military, Knowledge, Emotional & Perceptual, Spatial, Possession, Identity, Cultural, Narrative, Prophecy, Evidentiary, Causal, Hospitality).
- **The graph emits ~62 distinct edge types today** across 7,967 nodes (with 4,930 nodes = 62% having at least one edge populated).
- **The "22" claim was a fossil** from an earlier wiki-infobox subset count. It had propagated to 6 places: architecture.md vocab-lock callout (1), design-philosophy.md (1), schema-drift-auditor.md (1), prose-edge-classifier.md (3). None had been updated as the vocab grew.

Worse: I also discovered that the prose-edge-classifier prompt was pointing at the **wrong section** of architecture.md. It told the agent: "use the 22 edge types in § 'Wiki Infobox Fields → Edge Type Mapping'." That table is the wiki-infobox parser's `FIELD_EDGE_MAP` (~26 types) — a strict subset of the master vocabulary. The agent should have been pointed at the master `## Edge Types (Relationship Categories)` section (96 types). With the wrong section, the agent would have been *unable to emit* the very edge types prose excels at finding (perception verbs like `FEARS`, narrative verbs like `FORESHADOWS`, prophecy verbs like `FULFILLS`).

This was a real bug in the agent prompt, not just a doc-count issue.

## Cross-check: orphan emissions

Ran a `comm` between graph emissions and doc definitions to find orphans:

```
=== In graph but NOT in architecture.md (orphan emissions) ===
DECEIVED_BY    — reverse of DECEIVES, undocumented
HELD_BY        — reverse of HOLDS_TITLE, undocumented
KILLED_BY      — reverse of KILLS, undocumented
LOCATED_IN     — duplicate of LOCATED_AT, 21 instances all in _conflicts/
WRITTEN_BY     — defined in wiki-infobox subset table only, missing from master
```

Investigation:
- DECEIVED_BY / HELD_BY / KILLED_BY are legitimate reverse-direction emissions on the receiving end of the edge. Pattern is fine; just needed docs.
- LOCATED_IN was a parser-variant duplicate of LOCATED_AT. Same semantics. Normalize.
- WRITTEN_BY was already in the wiki-infobox table (line 498) but my regex `^| \`[A-Z_]\{3,\}\` ` only matched first-column edge types, so it appeared as an orphan. Real issue: it was missing from the master `## Edge Types` section's Narrative subsection.

Decision: keep the reverse pairs (document them as equivalences for query layers), normalize LOCATED_IN → LOCATED_AT in graph, add WRITTEN_BY to master Narrative section.

## The conceptual reframing

Matt's next question reframed the whole Stage 4 conversation: *"26 types is way too low. What if the prose edge discovery surfaces types that aren't in the 96? do the 96 cover every edge found on nodes?"*

I checked: yes, the 96 cover virtually every edge in the graph (only 5 orphans, all minor — reconciled above). But the more important finding: **37 of the 96 are entirely unpopulated**. These are exactly the verbs Stage 4 is designed to emit:

- Perception: `FEARS`, `RESENTS`, `MOURNS`, `TRUSTS`, `DISTRUSTS`, `HATES`, `RESPECTS`
- Identity: `IMPERSONATES`, `DISGUISED_AS`
- Prophecy: `FULFILLS`, `APPEARS_TO_FULFILL`, `SUBVERTS_PROPHECY`, `PROPHESIED_BY`, `SUBJECT_OF_PROPHECY`
- Narrative: `FORESHADOWS`, `PARALLELS`, `ECHOES`, `CONTRASTS`
- Causal: `MOTIVATES`, `TRIGGERS`, `ENABLES`, `PREVENTS`
- Hospitality: `VIOLATES_GUEST_RIGHT`, `GRANTS_SAFE_CONDUCT`

Then Matt: *"why wouldn't edges do more that just 'block any answer' wouldnt edges make this far better?"*

I had been underplaying it. He was right again. The honest framing:

- Today's graph (infobox-derived edges) answers **factual/structural** questions — genealogy, feudal hierarchy. Fine, but it's basically a structured fan wiki.
- The 37 unused edge types are what would turn it into a graph that knows the *story* — perception, identity, prophecy, parallels, causal chains. The entire narrative layer of ASOIAF.
- Even within the populated 26-type infobox subset, prose surfaces edges the infobox doesn't tag (`MANIPULATES`, `BETRAYS`, `ADVISES`, `NEGOTIATES_WITH`). Tyrion has 17 infobox edges today; prose could yield 40-60 more.

**Tier-difference, not polish.** A chat UI on today's graph = structured feudal wiki with a search bar. A chat UI on the Stage 4 graph = something that can answer "what does Tyrion fear?" or "which characters mourn Robb Stark?" with sourced edges.

## Cleanup executed

1. **`reference/architecture.md`**:
   - Rewrote vocabulary-lock callout (line 454-465) to distinguish master vocabulary (~96 types) from wiki-infobox subset (~26 types). Made explicit that "no emitter invents edge types" and the gate-with-doorbell protocol (file `vocabulary-gap` to `questions-for-matt.jsonl`).
   - Added `WRITTEN_BY` to Narrative & Literary subsection.
   - Added reverse-direction rows for `HELD_BY` (after HOLDS_TITLE), `KILLED_BY` (after KILLS), `DECEIVED_BY` (after DECEIVES) — documented as semantic equivalents with directionality flipped.
   - Added deprecation note on `LOCATED_AT` description mentioning `LOCATED_IN` as deprecated synonym to normalize on read.

2. **Graph normalization**: 21 `LOCATED_IN` instances rewritten to `LOCATED_AT` (all in `graph/nodes/_conflicts/`). Final state: 0 LOCATED_IN, 59 LOCATED_AT.

3. **`reference/design-philosophy.md`** (line 91): "22 edge types" → "~96 edge types ... ~26 derived from wiki infobox-field frequencies, the rest pre-declared for narrative/perception/prophecy passes".

4. **`.claude/agents/schema-drift-auditor.md`** (line 16): Updated to reference both master and subset tables explicitly.

5. **`.claude/agents/prose-edge-classifier.md`** — 3 spots:
   - First Steps (line 14): Repointed at master `## Edge Types (Relationship Categories)` section. Explicitly named the perception/identity/narrative/prophecy verbs the agent is now allowed to emit.
   - Vocabulary lock section (line ~74): Replaced the hardcoded 22-type list with a 14-category expansion covering all ~96 types. Made architecture.md the source of truth.
   - Definition of Done (line ~131): "locked vocabulary's 22 edge types" → "master vocabulary (~96 edge types)".

6. **`next.md`**: Added top-of-file `★ NEXT RECOMMENDATION` callout. Updated "Where we are today" with current numbers (7,967 nodes; 4,930 with edges; vocab cleanup landed). Expanded Track 5 (Stage 4 prose-edge-classifier) section with the new "tier-difference, not polish" framing + "No book passes required" clarification + Open Question on single-session vs watcher+workers run shape.

## Verification

After cleanup:
- Zero `"22 edge"` or `"22 type"` references remaining in active project files (history archives untouched).
- Zero orphan edge types in graph (graph emissions all documented in architecture.md).
- prose-edge-classifier vocabulary block matches architecture.md master section.

## Decisions captured

- **Edge vocabulary is master `## Edge Types` section in architecture.md (~96 types).** Wiki-infobox table is a subset for the parser only. Prose-edge-classifier emits from the master.
- **Reverse-direction edges are permitted** (HELD_BY ↔ HOLDS_TITLE, KILLED_BY ↔ KILLS, DECEIVED_BY ↔ DECEIVES). Documented as semantic equivalents. Query layer treats `HELD_BY(a→b)` as identical to `HOLDS_TITLE(b→a)`.
- **LOCATED_IN normalized to LOCATED_AT.** No further use of LOCATED_IN. Description on LOCATED_AT preserves the deprecated synonym note for any stragglers.
- **Stage 4 wiki-prose classifier is the next track.** Open question recorded in next.md: single-session vs watcher+workers run shape. Recommendation: single-session for the 3-bucket smoke phase; reconsider watcher+workers only at bulk-run scale (100+ buckets).

## Reflections (for future me)

- **The fossil-count problem is real.** "X edge types currently in the corpus" was true when written and rotted as the corpus grew. Doc rules that cite numbers without anchoring them to a derivation script will drift the same way. Consider: any future "N of X" claim in architecture.md should either (a) be a derived count regenerable from a script, or (b) reference a Session-N decision rather than asserting current state.
- **Confidence without verification is a worse failure mode than uncertainty.** I asserted "22 edge types" three times before Matt pushed back. The cost of verification was 3 grep commands. The cost of NOT verifying was a meaningful detour and a corrupted agent prompt.
- **Matt's pushback pattern is a signal.** When he says "I don't remember locking them" or "isn't that just too low" — verify, don't defend. Twice in this session he was right and I was wrong.

## What's next

Stage 4 wiki-prose edge classifier. Pre-flight: re-run cross-references + edge-candidates scripts (deterministic, free). Then 3-bucket smoke test on Opus classifier + Sonnet reviewer. If reviewer is CLEAN/CONCERNS-low, downgrade classifier to Sonnet for bulk. Run shape decision (single-session vs watcher+workers) deferred until candidate volume is known.
