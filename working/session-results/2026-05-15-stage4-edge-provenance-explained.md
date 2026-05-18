---
session_date: 2026-05-15
session_focus: Stage 4 — what "edge provenance is gutted" means, and why drift detection is now mandatory
status: complete
model_used: claude-opus-4-7[1m]
companion_doc: 2026-05-15-stage4-batch-0012-quality-check.md
---

# Stage 4 — Edge Provenance Explained

> Companion explainer to the batch-0012 quality check. Records the deep-dive on what "edge provenance is gutted" actually means, why a 2.0% type-discipline rate can still produce un-promotable output, and the operating-discipline change this drove: **drift detection + course correction is now a mandatory part of every Stage 4 bulk run, regardless of model.**

## What "edge provenance is gutted" actually means

**Provenance** = the chain of evidence that lets a reviewer answer "*why* does the graph claim this edge exists?" Specifically: the verbatim prose sentence that supports the claim + which section/paragraph of which node it came from. Without provenance, an edge in the graph is just an assertion — true-looking, but not auditable.

### The pipeline asked for three pieces of evidence per edge

The classifier prompt at `.claude/agents/prose-edge-classifier.md` lines 53-54 specifies this output shape for every emitted edge:

```json
{"decision": "emit_edge", "candidate_kind": "source_target",
 "source": "<slug>", "target": "<slug>", "edge_type": "<TYPE>",
 "evidence_snippet": "<the 75-char snippet from the candidate>",
 "evidence_section": "<which ## heading the snippet was in>",
 "confidence": "tier-1|tier-2|tier-3"}
```

Three provenance fields:
1. **`evidence_snippet`** — the actual prose sentence (verbatim, ≤75-200 chars).
2. **`evidence_section`** — which `##` heading + ideally paragraph index where the snippet lives.
3. **`confidence`** — calibrated tier with the "tier-N" prefix to make string-vs-int unambiguous.

### What batch-0011 actually produced (correct)

Take this real row:

```json
{"decision": "emit_edge", "edge_type": "MANIPULATES",
 "source_slug": "alyn-cockshaw", "target_slug": "uthor-underleaf",
 "confidence": "tier-1",
 "rationale": "He arranged for Ser Uthor Underleaf to kill Duncan
               'accidentally' in the tourney joust at Whitewalls"}
```

batch-0011 used `rationale` instead of the prompt-spec'd `evidence_snippet` — already a small drift, BUT the rationale field carries enough verbatim/paraphrased content that a reviewer can do the verification: "open `alyn-cockshaw.node.md`, search for the Whitewalls tourney passage, confirm Alyn arranged the assassination attempt, confirm `MANIPULATES` is the right type." It's a one-step audit. Not perfect, but auditable.

### What batch-0012 actually produced (gutted)

Same kind of row, the next batch:

```json
{"source_slug": "qarl-corbray", "target_slug": "lady-forlorn",
 "edge_type": "WIELDS",
 "confidence_tier": 1,
 "cite_ref": "## Appearances",
 "decision": "emit_edge"}
```

What you can do with this: confirm `qarl-corbray.node.md` has a section called `## Appearances`. That's it.

What you can't do:
- Find which paragraph supports `WIELDS lady-forlorn` — the Appearances section is dozens of paragraphs long.
- See the verb the prose actually used — was it "drew Lady Forlorn", "carried Lady Forlorn", "inherited Lady Forlorn"? The choice between `WIELDS` / `OWNS` / `INHERITED_BY` depends on this.
- Check whether the agent hallucinated — the prose might say Qarl's *son* wields Lady Forlorn, not Qarl. Without the snippet, no one can tell.
- Reconstruct the claim if the source page later changes — the section can be rewritten.

### Why `cite_ref: "## Appearances"` is not evidence

This is the most important part to understand. The candidate file the agent was given as input *already contained* the section header. The Python preprocessor at `scripts/wiki-pass2-build-edge-candidates.py` parsed the source page, found a cross-reference, and tagged each candidate with the section it came from. The candidate row the agent received looked something like:

```json
{"candidate_kind": "source_target", "source": "qarl-corbray",
 "target": "lady-forlorn", "anchor_text": "Lady Forlorn",
 "snippet": "Qarl drew Lady Forlorn from its scabbard...",
 "source_section": "## Appearances", "paragraph_index": 7}
```

The agent's job was to read the snippet (and the surrounding prose), reason about it, and emit an edge that **carries the snippet forward** so downstream tooling has provenance. Instead, the agent kept only the section name — which it didn't add, the preprocessor added — and dropped the snippet, the paragraph index, and any verbatim prose. The output field `cite_ref: "## Appearances"` is literally just echoing back input metadata. Zero new signal, zero verification value.

98 of 102 edges have `cite_ref: "## Appearances"`. Three have `## Origins`, one has `## Quotes`. The "evidence" is just the name of the section the candidate came from — the same metadata you'd get by re-running the preprocessor for free.

### The downstream consequences

Three review/promotion stages are blocked or weakened by this:

1. **prose-edge-reviewer** (the audit agent that reads a 5-10% stratified sample) can't do its job. Its whole purpose is to spot mis-classified edges by reading the evidence and disagreeing with the call. With no snippet to read, it'd have to re-derive the evidence from the source node — which means the audit becomes a re-extraction, not an audit. Audit cost balloons.

2. **wiki-pass2-promote-prose-edges.py** (the script that appends accepted edges to node files under `## Edges (prose-derived)`) is supposed to attach a citation qualifier — usually a paragraph reference and a quote so the graph-reader knows where the claim came from. With only `## Appearances` as the citation, every promoted edge would carry `[citation: appearances-section]` — true of every cross-referenced edge in the graph, useless as a discriminator.

3. **Future spoiler-gating + cross-identity work** depends on being able to trace any edge back to a specific paragraph + book + chapter. Without the snippet you can't determine which book/chapter the assertion comes from, which means `first_available` backfill (eventually) can't compute the correct value, and contradiction-surfacing (when wiki disagrees with Pass 1) can't quote either side.

### The vocab-gap question schema drift makes this worse

The vocab-gap questions in batch-0012 also dropped fields. Compare the same kind of question across batches:

```json
// batch-0009 (good)
{"question_id": "q-2026-05-15-batch-0009-vocab-gap-002",
 "evidence_snippet": "Cleyton Caswell was a suitor who sought to court Rohanne Webber",
 "evidence_section": "## Origins",
 "question": "Should COURTED be added? ..."}

// batch-0012 (gutted)
{"question_type": "vocab_gap", "pattern": "ATTENDS",
 "example_snippet": "attended the golden wedding",
 "frequency": 1}
```

The first one a reviewer can act on: read the snippet in context, decide if COURTED is real. The second one — "attended the golden wedding" — is so denuded of context that you can't tell which page it came from, who attended, what the surrounding sentence was, or whether the same pattern occurs elsewhere (it claims `frequency: 1` but the question itself says this pattern recurs broadly).

### Summary in one sentence

The agent did the *reasoning* job correctly (right edge types, right type discipline) but stripped out the *evidence* job (the verbatim prose that proves the reasoning), so the outputs read like a list of true-sounding assertions with no way to check any of them.

### Why this happened

The classifier prompt specifies `evidence_snippet` as a required field, but the worker template that wraps the classifier (`working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md`) doesn't restate the schema as a hard contract — it just says "classify each candidate row per the agent prompt's 4 decisions" and trusts the model to remember every field. When a fresh worker session starts (no prompt cache), the model re-derives an output schema from a quick re-read and tends toward the most concise valid-looking JSON. Sonnet 4.6 chose to emit the minimum-viable shape, dropping the heavy `evidence_snippet` field.

This is fixable in 30-60 minutes: pin the required fields in BOTH the worker template and the classifier prompt as a "## Output JSON contract" block, then add a Python validator (`scripts/wiki-pass2-validate-edge-jsonl.py`) that fails the batch if any emit_edge row is missing required fields. Mechanical enforcement instead of model-good-behavior.

## Operating-discipline takeaway: drift detection is mandatory now

Two things became clear from the batch-0012 audit:

1. **Models drift between sessions even when the prompt is fixed.** Same agent, same template, two different worker sessions, two different output schemas. Cache resets re-roll the model's interpretation. This is not a Sonnet defect or a Haiku defect — it's a property of using LLMs to produce structured output without mechanical post-validation.

2. **The drift was caught only because Opus did a cross-model audit.** A self-audit (Sonnet reviewing Sonnet's own output) would not have flagged this, because Sonnet considers `cite_ref: "## Appearances"` valid by its own standards. The cross-model lens — Opus reading Sonnet — surfaces "the prompt asked for X, you produced Y" where Sonnet would normalize Y as fine.

Both points apply equally to Haiku. Haiku will drift for the same structural reason; Haiku self-audit will miss it for the same structural reason. **Drift detection + course correction is now part of the standing protocol for any Stage 4 bulk run, regardless of which model is doing the bulk classification.**

Concretely, every bulk run now includes:

- **Mechanical schema validator** (post-batch, blocks merge if non-conformant).
- **Periodic cross-model audit** (every Nth batch, with a stronger model than the bulk worker, looking for type-contract violations + schema drift + the systematic bugs known for the bulk model — e.g. Haiku's FORGED_BY-on-material).
- **Verdict-gates-resumption** discipline (audit → CONCERNS-low/CLEAN allows next N batches; CONCERNS-high pauses + patches before resuming).

This applies whether the bulk worker is Sonnet, Haiku, or something else later. It's a property of the pipeline, not of any one model.

## What's next (sequenced)

1. **Pin the output schema** in the classifier prompt + worker template (`## Output JSON contract` block with required-fields list per decision type). One-shot script-builder edit.
2. **Add `scripts/wiki-pass2-validate-edge-jsonl.py`** — loads each batch's output JSONL, asserts required fields per `decision` value, exits non-zero on violation. Wire into the batch-completion step so a non-conformant batch can't mark itself `done`.
3. **Decide on batch-0011 (good) and batch-0012 (regressed) outcomes.** Two competing emits in the same graph at different schemas is itself a problem; pick a normalization (likely: re-run batch-0012 under the patched template, leave batch-0011 alone, normalize the `confidence` vs `confidence_tier` field name in a one-shot script).
4. **Decide on the 3 batch-0012 vocab gaps** (ATTENDS, UNCLE_OF/NEPHEW_OF, KILLED_WITH). All three look acceptable. Architecture.md + classifier prompt update in the same patching window.
5. **Smoke-test one batch on Haiku** under the patched template + validator. If schema holds and type-discipline issue rate stays under ~5% with no systematic bugs, switch the bulk default to Haiku for the cost win and lock in the cross-model audit cadence (Opus audits every N Haiku batches).
6. **Resume bulk run** with the new discipline.

Cost framing for step 5: if Haiku passes the smoke + holds quality across the periodic Opus audits, the remaining 189 batches drop from ~$647 (Sonnet) to ~$80 (Haiku), with maybe ~$80-150 of Opus audit cost layered on top. Net ~$430-480 saved against the bulk Sonnet plan.

## Files referenced

- `working/session-results/2026-05-15-stage4-batch-0012-quality-check.md` — the verdict this explainer expands.
- `.claude/agents/prose-edge-classifier.md` — classifier prompt, lines 53-54 are the schema spec.
- `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md` — worker template that needs the schema-contract block added.
- `scripts/wiki-pass2-build-edge-candidates.py` — the Python preprocessor that already carries `snippet` + `source_section` into each candidate row.
- `working/missions/2026-05-14-stage4-v1-bulk-sonnet/results/batch-{0011,0012}.json` — the side-by-side artifacts.
