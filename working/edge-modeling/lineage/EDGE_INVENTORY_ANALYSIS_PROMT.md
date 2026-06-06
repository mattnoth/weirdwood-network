# Claude Code Agent Brief: Edge / Event-Modeling Analysis & Recommendation

## 0. Mission

You are given **one input: a Markdown inventory report** describing how a knowledge graph currently models its relationships. Your job is to consume that report and produce a **decision document** that diagnoses the modeling problem and prescribes a concrete fix.

This is the *analysis* phase, not a re-inventory. You start from a deliberately fresh context: **you have the report and this brief, nothing else.** Treat the report as your only source of truth about the codebase.

- Do **not** assume access to the repo. If you have it, you may spot-check a claim, but the analysis must stand on the report alone.
- If the report lacks something your recommendation hinges on, **do not guess** — list it as an open question and state how it would change the call.
- **Be decisive.** The reader does not want a neutral menu of five options. They want a recommendation with reasoning, and the rejected alternatives noted. Hedging is the failure mode to avoid here.
- **Challenge the report.** It contains its own binary-vs-event classifications; treat those as a hypothesis to verify, not gospel. Fresh eyes are the entire point of this phase.

Deliverable: `EDGE_MODELING_DECISION.md` (write it, or print it in full).

---

## 1. Conceptual foundation (read this in full — it is the lens for the whole analysis, and it defines the terms used below)

The graph mixes two fundamentally different things that both happen to be stored as edges. They *look* like the same kind of thing — both become a line from one node to another — but they are not, and conflating them is what produces the symptom the reader is chasing.

### 1.1 Relations vs. events

**A true binary relation** is dyadic with fixed, asymmetric roles. Every instance has exactly two participants, both mandatory, each playing a determinate role, and there is an inherent direction baked into the predicate itself. There is no question of "which participant is the subject," because the predicate pins it down completely. As a result it has **exactly one correct shape** — there is literally nothing to decide. Archetype: `PARENT_OF`. A parent-of fact is always `parent → child`; you never have to choose.

**An event** is different. Archetype: `ATTACKS`. An attack has an attacker, a defender, a location, possibly an instigator distinct from the executor, an outcome, a time. "The Mountain attacks the Riverlands" — is the subject the executor (Gregor), the person who ordered it (Tywin), or the army that carried it out (the Lannister host)? Several of those are individually defensible. `PARENT_OF` has one correct shape; `ATTACKS` has roughly five.

### 1.2 What "arity" and "n-ary" mean

**Arity** is just the number of arguments (participants) a predicate takes. A *binary* predicate takes two (`PARENT_OF(parent, child)`). An **n-ary** predicate takes *n* of them, where *n* can be more than two — that's all the term means: "takes some number of arguments, possibly many." `ATTACKS(attacker, defender, location, instigator, executor, outcome, time, …)` is n-ary. The participant slots have *names* — agent, patient, instrument, location, outcome — and in linguistics these are called **thematic roles**. The specific bundle of roles a given verb licenses is its **frame** (this is "frame semantics"; e.g. an Attack frame has roles like Assailant, Victim, and Means). You don't need the linguistics jargon to use this — the operative point is just: *an event is a predicate with several distinctly-typed, often-optional participant slots.*

### 1.3 Why an event has no "canonical head"

The problem is **not** that an event is "bigger" or has more fields. The problem is structural: an edge has a built-in subject→object directionality — it points *from* one node *to* another. So the moment you flatten an event into a single edge, you are **forced to nominate one participant as the subject (the "head")** and one as the object. But an event has no natural head. Nothing in the world says an attack is "about" its attacker rather than its target; both are just roles in the frame. You're being made to pick a winner in a contest that has no winner.

### 1.4 Why this reads as inconsistency or hallucination — but actually isn't

Flattening an event into an edge is a **lossy projection**: you take a multi-slot structure and project it down onto two slots (subject, object), discarding or burying the rest. And here is the crux — **projections are not unique.** There are several individually-valid ways to do it, and there is no canonical normal form to make one of them "the" right one.

So each row, when it gets created, independently picks a projection. With no canonical form to anchor on, different rows pick *different* projections. That divergence is what surfaces downstream as "this data is inconsistent" or "the model hallucinated different answers for the same kind of event."

The precise word for this is **underdetermination**: the desired output (a single deterministic edge) is not uniquely determined by the input (an event with no natural head). It's not hallucination in the usual sense of the model inventing facts — it's the model being handed a problem that genuinely has several equally correct answers and asked to emit exactly one. The fix is therefore not "make the model more accurate"; it's "remove the underdetermination by imposing a canonical form."

### 1.5 Subproblem: the instigator-vs-executor split is a *causative chain*

This one deserves separate treatment because it isn't just a head-selection question. Ordering an act and performing it are arguably **two linked events** — a cause and its effect — with **different agents**, not one event with two agents. ("Tywin causes [the Mountain attacks the Riverlands].") Human languages mark this distinction grammatically (causative constructions), which tells you it lives *in the territory*, not merely in your schema.

So even after you decide to reify (see below), there's a sub-decision to make explicitly:
- model it as **one event node** carrying two roles (a Commander role and an Executor role), or
- model it as **two event nodes** (the ordering, the attacking) joined by a **causal edge**.

The analysis must pick one for this graph and justify it; don't leave it implicit.

### 1.6 The two families of fix

**(A) Reification.** Promote the event from an edge to a **first-class node**, and hang each participant off it as a labeled, role-typed edge (`event —agent→ Gregor`, `event —target→ Riverlands`, `event —commander→ Tywin`, `event —location→ …`, plus properties like time and outcome on the node). This is lossless — every role survives. It is the same move a software engineer already knows as the **associative entity / junction table**: when a relationship is many-to-many-to-many or carries its own attributes, you don't cram it into a foreign key, you give it its own row. The canonical example is a Prescription — doctor, patient, drug, dose, date — which is obviously a record of its own, not an edge. Reification costs structural complexity and changes how queries and visualizations traverse the graph.

**(B) Canonical head-selection.** If you can't or won't reify everywhere, keep the event as an edge but define a **single, total head-selection function** — e.g. *always* anchor on the most-agentive named participant, or *always* on the direct executor — and apply it **uniformly across every row.** This is still lossy (the non-head roles get discarded or demoted to properties), but it is **consistent**, and consistency is what kills the hallucination-look. The meta-point: consistency requires a canonical form; n-ary→binary has no unique canonical form *unless you impose one by fiat.* Imposing it by fiat is exactly what option B is.

### 1.7 The diagnostic heuristic (use this to classify every edge type)

A relationship wants to be a **node (reify it)** — or at minimum needs a canonical-form decision — if *any* of these are true:
1. it can have **more than two** meaningful participants;
2. it **carries its own properties** (time, place, instrument, outcome);
3. it can be **negated or qualified as a unit** ("the attack that never happened," "a failed attack").

It is a genuine **binary relation** (leave it alone) only if it fails all three. `PARENT_OF` fails all three. `ATTACKS` passes all three.

### 1.8 The trap to watch for

**Never anchor the head on the grammatical subject of the source sentence.** The same event is phrased many ways — "the Mountain attacked," "Tywin sent the Mountain," "the Lannister host fell upon them" — so anchoring on surface syntax pipes raw linguistic variance straight into the data model. If the report shows the subject slot tracking how sentences happened to be worded, that is very likely a **root cause** of the current inconsistency, not a symptom. Call it out wherever you see it.

---

## 2. Analysis tasks

Work through these in order; they build on each other.

### 2.1 Re-diagnose from the evidence
- Re-run the §1.7 diagnostic against each edge type the report describes. Produce your **own** binary-vs-event classification and note every place you disagree with the report's classification, with reasoning.
- For each event-like type, enumerate the **defensible collapses** (the candidate heads, as in the Mountain/Tywin/host example) and, using the sampled rows in the report, determine **which projections are actually appearing** in the live data. Name the specific inconsistency.
- Trace the inconsistency to its **origin**: schema underspecification, the extraction prompt, post-processing/dedup, manual authoring, or grammatical-subject leakage (§1.8). Cite the report.
- State plainly whether a canonical head-selection rule currently exists anywhere. If not, that's likely the headline finding.

### 2.2 Per-type disposition
Produce a table — one row per edge type:

`edge_type | your_classification | disposition | rationale | confidence | depends_on_report_gap?`

Where `disposition` is one of: **Reify**, **Canonicalize** (impose a head rule), or **Keep as binary** (already correct). Tie each rationale to the §1.7 test, not vibes. Mark confidence Low/Med/High and flag rows whose disposition would flip if a report gap were filled.

### 2.3 Target schema design
For the types you'd **reify**: specify the concrete shape — the event node type(s), their properties, and the role-typed edges connecting participants (with role names from the thematic-role inventory: agent, patient, location, instrument, outcome, time…). Show it in whatever notation the report indicates the graph uses (property-graph labels, triples, JSON shape, etc.) so it drops into the existing model. Reuse the existing node/ID conventions from the report.

For the types you'd **canonicalize**: state the exact head-selection function as an unambiguous rule a machine could apply, and specify the tie-breakers. Explicitly forbid grammatical-subject anchoring (§1.8).

### 2.4 Causation / instigator-vs-executor decision
Make the call from §1.5 for this graph: model commander-and-executor as **one event node with two roles**, or as **two event nodes joined by a causal edge**? Justify it against the project's apparent query/visualization goals as described in the report. Note what each choice makes easy vs. hard to query.

### 2.5 Pipeline remediation (so the fix doesn't erode)
Cleaning the data is pointless if the generator keeps reintroducing variance. Prescribe changes to the **creation pipeline**:
- If extraction is LLM-driven, propose concrete edits to the extraction prompt(s) the report quoted — what instructions to add so the model emits reified events, or applies the canonical head rule deterministically.
- Specify validation/normalization rules to add post-extraction (reject or repair edges that violate the canonical form).
- Note any entity-resolution interactions (reified event nodes need stable identity too).

### 2.6 Migration plan
- How existing edges transform into the target shape (the rewrite logic, at a level someone could implement).
- What is reversible vs. lossy in the migration.
- Which existing queries, traversals, or visualization behaviors **break** or change, per the report's description of how the graph is consumed.
- A suggested sequencing (e.g. schema → pipeline → backfill → validate), and whether the binary types can be left entirely untouched.

### 2.7 Tradeoffs & what would change the recommendation
- A short, honest accounting of the cost of your recommendation (complexity, query ergonomics, rendering, effort) versus the cheaper alternative you rejected.
- A bulleted list of **report gaps**: specific facts not in the report that, if known, could change the disposition — so the reader knows whether another inventory pass is warranted.

---

## 3. Output format

Produce `EDGE_MODELING_DECISION.md`:

```
# Edge & Event-Modeling — Diagnosis & Recommendation

## Recommendation in one paragraph
The headline call: reify X/Y/Z, canonicalize A/B, leave C alone — and the single
biggest root cause of the current inconsistency.

## 1. Diagnosis
What is actually causing the "hallucination-look," traced to its origin, with
report citations. Include your binary-vs-event re-classification and disagreements
with the report. Frame it in terms of underdetermination (§1.4), not "the model
is wrong."

## 2. Disposition Table
(the per-edge-type table from 2.2)

## 3. Target Schema
Reified event shapes + canonical head rules, in the graph's own notation.

## 4. Causation Modeling Decision

## 5. Pipeline Remediation
Concrete prompt edits + validation rules.

## 6. Migration Plan
Transform logic, what breaks, sequencing, reversibility.

## 7. Tradeoffs & Alternatives Rejected

## 8. Report Gaps — what would change this call
```

Every diagnostic claim should cite the report (quote the relevant line or section). Recommendations should be concrete enough to act on, not directional.

---

## 4. Done-when checklist
- [ ] Every edge type has an independent classification and a disposition.
- [ ] The specific, evidenced root cause of the inconsistency is named, and framed as underdetermination rather than mere model error.
- [ ] Reified types have a concrete node+role schema in the graph's own notation.
- [ ] Canonicalized types have an unambiguous, machine-applicable head rule that does **not** rely on grammatical subject.
- [ ] The instigator-vs-executor / causation question is decided, not deferred.
- [ ] Pipeline changes are specified, not just data fixes.
- [ ] A migration plan exists, including what breaks downstream.
- [ ] Report gaps are listed so the reader knows if another inventory pass is needed.
- [ ] The document recommends, it does not merely enumerate.