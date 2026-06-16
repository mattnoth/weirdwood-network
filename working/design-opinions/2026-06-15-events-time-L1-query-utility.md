# Design Opinion: Temporal Representation on Event Nodes
**Lens:** Consumer-agent query utility (single-axis review)
**Date:** 2026-06-15
**Commissioned by:** Matt (S100 session)
**Status:** Independent opinion — not a worklog entry, not a commitment

---

## 0. What the dips actually told us

Two grounded-agent dips ran in the past 48 hours. Combined results: 4 correct / 6 partial
/ 0 failed on 10 questions. The partial failures break into four modes:

| Failure mode | Count | Root cause |
|---|---|---|
| `dark-vocab` | 2 | No TRIGGERS/CAUSES from historical event hubs; no ATTENDS/WITNESSES on executions |
| `slug-discoverability` | 2 | Resolver misses natural-phrase entry to known-good nodes |
| `prose-only` | 2 | Fact buried in evidence_quote, no structured edge |
| `hub-pre-mint` | 1 | Missing beat node (Joffrey/Arya fight pre-incident) |

**Zero of the 6 partials involve time.** The agent that failed on Battle of the Trident
consequences (Q10) could not find the causal TRIGGERS chain to the Sack of King's
Landing — not because it lacked a date, but because the edge does not exist. A date
field on `battle-of-the-trident` would not have helped answer "what were the
consequences." The dips have not yet asked a time-shaped question.

This is the ground state for what follows.

---

## 1. What each representation enables and blocks

### (a) In-world AC date ("283 AC", "suspected 88 AC")

**Enables:**
- "What year did the Battle of the Trident happen?" — direct field read, one hop
- "Which events happened before Robert's accession in 283 AC?" — date-range filter over
  event nodes
- "Who was alive when [event Z] happened?" — if character nodes also carry birth/death
  years (partially present via wiki infoboxes), you can compute a birth-year ≤ event-year
  ≤ death-year inclusion. This is genuinely useful for "was Rhaegar's father still king
  when Jon Snow was conceived?" type reasoning.
- "What was happening in Dorne during the War of the Five Kings (~298-300 AC)?" —
  date-range filter intersected with location. This query shape is currently impossible;
  AC dates would enable it for events that are date-stamped.
- Historical-distance questions: "How long after the Dance of the Dragons did the
  Blackfyre rebellions start?" — subtraction of two AC fields.

**Blocks or distorts:**
- Any question about events GRRM dates imprecisely. The AC calendar is notoriously
  under-specified; GRRM has not confirmed exact years for most pre-series events. An agent
  reading `date_ac: 88` will assert "88 AC" as if authoritative.
- In-series events during the five books happen over roughly 299-300 AC (disputed by
  chapters), and GRRM has been inconsistent. Stamping chapter-resident events with AC
  dates imports GRRM's own internal inconsistency into the graph.
- Pre-series events (Robert's Rebellion, Dance of the Dragons, Aegon's Conquest) have
  AC dates; in-series events have almost none that are canon-stated. The representation
  is therefore asymmetric: good for deep history, almost absent for the narrative window.

**Verdict on (a):** High value for pre-series historical events where AC dates are
wiki-canonical (Robert's Rebellion = 282-283 AC, Dance of Dragons = 129-131 AC,
Greyjoy Rebellion = 289 AC). Low/negative value for in-series events because the dates
are mostly unlocked from canon.

---

### (b) Narrative reading-position (book + chapter index)

**Enables:**
- "Is event X a spoiler if the reader is only through Book 2?" — if event nodes carry
  `first_book: agot` and `first_chapter: 15`, a spoiler gate can be a simple filter.
  The graph ALREADY stamps edges with `evidence_book` and `evidence_chapter`; the
  cheapest path is deriving an event node's first-appearance position from its earliest
  edge.
- "What does character Y know at the time of event Z?" — if event Z has a narrative
  position, you can filter all edges with `evidence_chapter < Z_chapter_in_same_book`
  and intersect with Y's POV chapters. This is the killer query for spoiler-aware agents.
  It currently requires manual reasoning; a chapter-stamp on events would make it
  mechanical.
- "What was Daenerys doing while the Red Wedding happened?" — both events have known
  narrative positions (ASOS); cross-referencing by chapter index answers this for
  the reader, even if in-world simultaneity is uncertain.
- Structural coherence: the graph already has `meta.chapter` nodes and edges carry
  `evidence_book` + `evidence_chapter`. A narrative-position stamp on event nodes
  is consistent with the existing schema and derivable deterministically from edge data
  without any LLM pass.

**Blocks or distorts:**
- "Which came first in-world, A or B?" — narrative position and in-world order diverge
  for flashback chapters, POV-delayed reveals, and prologue/epilogue events. AGOT Eddard
  chapters recall Robert's Rebellion in chronological order; the reader encounters them
  non-linearly. A chapter-stamp on the Battle of the Trident (recalled in AGOT Eddard I)
  would date it as AGOT chapter 1, which is narratively correct but in-world wrong.
- Retrospective events (Robert's Rebellion, Dance of Dragons) get their narrative
  position from the chapter that first mentions them, not the chapter where they
  happened. The Battle of the Trident first appears as recall in AGOT-Eddard-01; its
  "narrative position" by this logic is the beginning of Book 1, but it predates the
  story by 15 years.

**Verdict on (b):** High value for spoiler-gating and "what does Y know when" queries —
the use cases the project actually cares about. Derivable from edge data without new
schema fields in many cases. NOT useful for historical ordering of pre-series events;
would actively mislead for flashback-dominant events.

---

### (c) Relative ordering only (X PRECEDES Y)

**Enables:**
- "Which came first, A or B?" — a single PRECEDES edge answers this for known ordered
  pairs, without requiring either a date or a chapter stamp.
- Causal chain traversal — if Rhaegar's death PRECEDES Sack of King's Landing and
  Sack of KL PRECEDES Robert's coronation, a graph traversal recovers the chain without
  any absolute time coordinates.
- Lower precision cost: you do not need to know "283 AC" to assert "Battle of the
  Trident PRECEDES Sack of King's Landing." The relative fact is high-confidence even
  when the absolute dates are not.

**Blocks or distorts:**
- "What year did X happen?" — PRECEDES cannot answer absolute-date queries.
- "What was happening in Dorne simultaneously?" — concurrent events require CONTEMPORARY_WITH
  (already in vocab) or shared date coordinates; PRECEDES alone cannot identify overlap.
- Maintenance cost: a PRECEDES graph over 500+ events requires either a DAG (expensive
  to maintain) or sparse/selective edges. Sparse edges leave most pairs unanswerable.

**Verdict on (c):** Targeted PRECEDES/TRIGGERS edges between specific historically
adjacent events (the causal chains the dips actually failed on) are high-value. A
comprehensive PRECEDES layer is too expensive to maintain correctly. Relative ordering
works best as a by-product of causal TRIGGERS edges, not as a standalone representation.

---

### (d) Combination: AC date + narrative position

**What this enables that neither alone does:**

The two representations serve non-overlapping query classes:

| Query class | AC date | Narrative position |
|---|---|---|
| "What year did X happen?" | YES | No |
| "Which came first in-world?" | YES (for pre-series events) | Misleading (recall bias) |
| "Is X a spoiler past Book 2?" | No | YES |
| "What does Y know at time Z?" | No | YES |
| "What was happening simultaneously?" | YES (same AC year) | Approximate only |
| "How long between A and B?" | YES | Only by chapter gap (unreliable) |

The query classes do not overlap. An agent spoiler-gating answers needs narrative
position; an agent reasoning about Targaryen history needs AC dates. Both are legitimate
consumer-agent query shapes. Neither substitutes for the other.

**However:** the combination also doubles the maintenance surface and doubles the
uncertainty surface. An event can have wrong AC date AND wrong narrative position. And
"suspected 88 AC" is qualitatively different from "AGOT Chapter 5" — the former is
uncertain, the latter is a fact of the published text.

---

## 2. Rankings and positions

### 2.1 Is dating events worth it? Ranked against the causal-edge gap.

**Rank 1: Causal edges (TRIGGERS/CAUSES/ENABLES between event hubs)**

This is the gap the dips actually measured. Q10 (consequences of Battle of the Trident)
failed entirely. Q9 (Trident incident) failed partly. The Red Wedding hub works well
precisely because it has causal structure within its arc. The gap is not "what year did
this battle happen" — it's "what did this battle cause." Closing the causal-edge gap
converts real measured failures to correct answers. Expected yield: 2 of 6 partials fixed
immediately.

**Rank 2: ATTENDS/WITNESSES expansion**

Q7 (who attended Ned's execution) failed because ATTENDS has 42 graph-wide edges and
none on the execution hub. This is a dark-vocab gap, same category as causal edges but
narrower scope. Fixable by a targeted pass on key named event hubs (executions,
weddings, trials). Expected yield: 1 of 6 partials fixed.

**Rank 3: Narrative reading-position on event nodes**

No dip question tested this yet. But the spoiler-gating use case is architecturally
inevitable — if the project ever surfaces answers to readers who haven't finished the
series, this becomes critical. And it is mostly derivable from existing edge data
(`evidence_book`/`evidence_chapter` stamps on edges already exist). The cost to implement
is low; the value is deferred but real.

**Rank 4: In-world AC dates on event nodes**

Dips have not tested any date question. For pre-series historical events with wiki-canonical
dates (Robert's Rebellion, Dance of Dragons, Greyjoy Rebellion, Aegon's Conquest),
adding AC dates is a wiki-derivable mechanical step and answers "what year" cleanly. For
in-series events (the five books, ~299-300 AC), dates are mostly unavailable from canon
and the representation would be sparse and potentially wrong.

AC dates are worth adding for pre-series events during a wiki-backfill pass — they are
low-risk (canonical sources), low-cost (wiki infoboxes have date fields for these events),
and answer a real if currently unmeasured query class. They are not worth investing in
for in-series events where the answer is either wrong or absent.

**Conclusion on ranking:** Causal edges first (measured failure), ATTENDS expansion
second (measured failure), narrative position third (low-cost, future-proof), AC dates
fourth (pre-series events only, on a separate pass). Do not start with dates.

---

### 2.2 In-world date vs narrative position vs both — which does a consumer agent need?

**Take position: narrative position is primary, AC dates are secondary and bounded.**

Rationale: the graph's consumer agent is principally answering questions about the
narrative (who did what, what led to what, who knows what), not writing a Targaryen
encyclopedia. Spoiler-gating and epistemic-state queries ("what does Ned know in chapter
5 about Jon's parentage?") require narrative position. These are live use cases for the
project as built.

AC dates enable a different query class — historical-distance reasoning and
simultaneous-events reasoning — which is useful for pre-series depth but not the
dominant consumer pattern.

Both together would be ideal in a mature graph. For the next 3-6 months of development
work, prioritize narrative position because: (1) it is partially derivable from existing
edge stamps with a Python script; (2) `first_available` is already a deferred-but-planned
field in the schema; (3) it serves the spoiler-gating story that the project already
acknowledges.

Add AC dates opportunistically for pre-series events during the wiki-backfill pass
already planned (infobox-merge track), since wiki infoboxes carry date fields for named
historical events. Do not run a separate agent pass just for dates.

---

### 2.3 How "suspected 88 AC" surfaces to the agent without asserting a guess as fact

**Hard rule: uncertain dates must be typed, not just text-qualified.**

Three options, ordered by agent-safety:

**Option A (recommended): Separate field with confidence tier**
```yaml
date_ac: 88
date_ac_confidence: suspected  # one of: canonical, estimated, suspected, disputed
date_ac_source: "wiki: Dance of the Dragons article"
```
The agent is instructed to treat `date_ac_confidence: suspected` as "approximate; do not
state as fact." A consumer agent following schema rules will qualify its answer:
"around 88 AC, though this date is not canon-confirmed."

**Option B: Confidence-tier inherited from node**
Leave event node confidence as `tier-3` (inferred) when the date is not canon-stated.
Agent infers that all data on a tier-3 node is uncertain. Simpler but coarser — the
whole node inherits the uncertainty, not just the date.

**Option C: Free-text string ("~88 AC")**
Store the date as a string ("~88 AC", "c. 88 AC"). The agent reads the string and passes
uncertainty to the human. This is fragile — agents often strip qualifiers when
reformulating answers ("The event happened in 88 AC").

**Decision: Option A.** Add a `date_ac_confidence` enum field with values `canonical`
(stated in text or confirmed by GRRM), `estimated` (wiki-derived scholarly estimate,
internally consistent), `suspected` (fan-derived or highly disputed). The agent's
system prompt instructs: for any date field with confidence below `canonical`, qualify
the answer with "approximately" and do not assert year as fact. This is one additional
field per event node; the cost is trivial. The benefit is that a consumer agent does not
confidently tell a reader "the Dance of the Dragons ended in 131 AC" when the actual
wiki text says "c. 131 AC."

---

## 3. Recommendation (3 sentences)

Close the causal-edge gap before touching dates: adding `TRIGGERS` and `CAUSES` edges
between measured-failure historical event hubs (Battle of the Trident → Sack of King's
Landing, and the Trident incident's missing precipitating beat) will convert the two most
concrete dip failures to correct answers and is directly evidenced by grounded testing.
When date work begins, add narrative reading-position first (derivable from existing
edge `evidence_book`/`evidence_chapter` stamps via Python, serves spoiler-gating, no
LLM pass needed) and add AC dates opportunistically during the infobox-merge wiki pass
for pre-series historical events only, carrying a `date_ac_confidence` enum so agents
cannot assert suspected dates as canonical fact. The two temporal representations
(AC date and narrative position) serve non-overlapping query classes and neither
substitutes for the other — but neither is the bottleneck the dips found, so they
belong on the roadmap after causal edges, not before.
