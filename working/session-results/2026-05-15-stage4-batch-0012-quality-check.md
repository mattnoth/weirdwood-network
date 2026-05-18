I ---
session_date: 2026-05-15
session_focus: Stage 4 batch-0012 quality check + Sonnet vs Haiku verdict
status: complete
verdict: CONCERNS-high
model_used: claude-opus-4-7[1m]
---

# Stage 4 — batch-0012 Quality Check

## Verdict

**CONCERNS-high.** **Pause the bulk run.** Edge *content* is good (clean vocabulary, correct type discipline, no Haiku-style systematic bugs); edge *provenance* is gutted by a schema regression between batch-0011 and batch-0012. Outputs in their current form will not survive downstream review or promotion-with-citation.

## Headline numbers

- **30 files audited** (6 empty = 20%, agent correctly rejected when nothing to emit)
- **102 emit_edge / 353 candidates = 28.9% emit rate** (vs batch-0011's 8.5% — 3.4× higher; possible over-permissive drift, but emitted edges look reasonable so this may just be bucket variance)
- **2 escalate_cross_identity** (both well-formed, both about the tom-costayne / tommen-costayne-knight duplicate-node pair)
- **3 vocab-gap questions filed** (ATTENDS, UNCLE_OF/NEPHEW_OF, SLAIN_BY_WEAPON)
- **0 escalate_disambiguation**
- **2/102 type-contract concerns = 2.0%** (low — see Type Discipline section)
- **0 deprecated `LOCATED_IN` emissions** ✓
- **0 invented edge types** ✓ (every emit is from the canonical 121-type vocabulary)
- **0 Haiku-style FORGED_BY-on-material bugs** found across all 362 prose-edges files in the graph
- **0 string-tier confidence values** (`confidence_tier: 1` integers used — but see schema-drift below)
- **94 tier-1 / 8 tier-2 / 0 tier-3** — agent never used tier-3, possible under-use signal but not a defect

## ⚠️ Headline issue: schema regression batch-0011 → batch-0012

Side-by-side of the same emit_edge decision:

```
# batch-0011 (good)
{"decision":"emit_edge","edge_type":"MANIPULATES","source_slug":"alyn-cockshaw",
 "target_slug":"uthor-underleaf","confidence":"tier-1",
 "rationale":"He arranged for Ser Uthor Underleaf to kill Duncan 'accidentally' in the tourney joust at Whitewalls"}

# batch-0012 (regressed)
{"source_slug":"qarl-corbray","target_slug":"lady-forlorn","edge_type":"WIELDS",
 "confidence_tier":1,"cite_ref":"## Appearances","decision":"emit_edge"}
```

**What was lost:**
1. **`rationale` field dropped.** No verbatim or paraphrased evidence accompanies the edge. Downstream `prose-edge-reviewer` cannot verify edges; promoter cannot attach a meaningful qualifier.
2. **`cite_ref: "## Appearances"` is not evidence.** 98/102 emits cite this section header (3 cite `## Origins`, 1 cites `## Quotes`). The cross-reference candidates were *generated from* the Appearances section by the Python preprocessor, so this field reproduces the section header it was already given — zero new signal.
3. **`confidence` schema changed**: `"tier-1"` (string) → `confidence_tier: 1` (integer). Both are valid against the auditor checklist, but inconsistency between batches breaks any downstream tooling that branches on shape.
4. **`evidence_snippet` and `evidence_section`** specified by the classifier prompt at lines 53-54 of `.claude/agents/prose-edge-classifier.md` are absent from batch-0012 output. The agent prompt was not followed.
5. **Vocab-gap question schema also drifted.** Earlier batches (0008-0011) used `{question_id, bucket_id, agent, type, text, context}`; batch-0012 used `{question_type, worker_id, batch_id, pattern, description, example_*, frequency}`. Two different question schemas in `questions-for-matt.jsonl` — review tooling will need both readers.

**Cause (inferred):** the worker template at `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md` does not pin the output JSON shape with required fields. Each worker session is improvising. The new worker (`worker-20260515-143200000`) chose a more concise schema. Without a contract-validating post-batch step, this drift will keep happening at every model/cache reset.

## Type discipline audit

Programmatic check against `target_slug`'s frontmatter `type:` field across all 102 emit_edge rows. **Only 2 concerns surfaced:**

1. **`leo-costayne` COMMANDS `house-hightower` (organization.house)** — `COMMANDS` per architecture targets persons or military forces, not the abstract House. Likely should be `SERVES leyton-hightower` (whoever was Lord at the time) or a new `LEADS_FORCES_OF` gap. Borderline-acceptable as-is because a fleet-commander may be said to "command" the house's fleet.

2. **`tommen-costayne` SWORN_TO `leyton-hightower` (character.human)** — Per the new disambiguation guidance: structural feudal allegiance to a *house* = `SWORN_TO`; personal-named oath to a person = `VOWS_TO` or `SERVES`. Should be `SERVES leyton-hightower` or `SWORN_TO house-hightower`. Minor.

Two issues out of 102 edges = **2.0%**, well below the Session 53b Sonnet baseline of 3.9%. Type discipline is **clean**.

Spot-check of borderline emits Opus also examined manually:
- `clarence-crabb OWNS aurochs` ✓ (animal — OWNS correct, not WIELDS)
- `qarl-corbray WIELDS lady-forlorn` ✓ (Lady Forlorn is the Corbray Valyrian sword)
- `dick-crabb LOCATED_AT stinking-goose` ✓ (assuming Stinking Goose has a `place.location` node; tavern-as-location is reasonable)
- `merlon-crakehall LOCATED_AT kings-landing` — would prefer `TRAVELS_TO`; LOCATED_AT implies seated/resident. Marginal.
- `lord-costayne-aerys-i OPPOSES lord-shawney` AND `CONTEMPORARY_WITH lord-shawney` — duplicate edge between same pair from two sections. Acceptable; promoter will dedupe or keep both.

## Vocab-gap recommendations

Three questions filed. My judgment per question:

### 1. ATTENDS (person → event, non-combatant)
**Recommendation: ACCEPT as new canonical type.**
- The `qarl-corbray` ATTENDED `golden-wedding` case is real — the wedding has its own event node and Qarl was a guest, not a fighter or organizer. No existing type covers passive event attendance.
- Existing `FIGHTS_IN` is only for combatants; `COMMANDS_IN` only for commanders. There's a gap for guests, attendees, audience members, witnesses.
- ASOIAF has many such pages: who-attended-what-tourney, who-was-at-what-feast, who-sat-where at the Purple Wedding, etc. This will recur many times.
- Proposed contract: `ATTENDS(character.* → event.*)` — tier-1 when explicit, tier-2 when implied by presence in the room.
- Add to architecture.md "Spatial & Temporal" or a new "Social & Ceremonial" subsection alongside `GUEST_OF`.

### 2. UNCLE_OF / NEPHEW_OF
**Recommendation: ACCEPT both (or at least UNCLE_OF — NEPHEW_OF as reverse-of).**
- Prose constantly says "his uncle Corwyn" / "his nephew Bran". The current vocab forces these to be modeled as `PARENT_OF` chains (Corwyn's brother → Quenton's father → Quenton), which is slow to traverse and brittle when the parent isn't in the graph.
- Direct uncle/nephew edges are queryable in one hop; the chain reconstruction is multi-hop and fragile.
- Pattern: `UNCLE_OF(character → character)`, reverse `NEPHEW_OF`. Treat like `SIBLING_OF` (one-generation kinship shortcut).
- Add to "Kinship & Family" subsection.

### 3. SLAIN_BY_WEAPON / KILLED_WITH
**Recommendation: ACCEPT as `KILLED_WITH`** (mirror of existing `EXECUTED_WITH`).
- The vocab already has `EXECUTED_WITH(character → object.artifact)` for *judicial* execution-by-weapon. The classifier correctly noted there's no combat equivalent.
- `KILLS` and `KILLED_BY` only handle person-as-agent. When prose says "slain by Orphan-Maker" the artifact is the named agent of death and there's no slot for it.
- Proposed contract: `KILLED_WITH(character → object.artifact)` — analogous to `EXECUTED_WITH`. Doesn't replace `KILLED_BY person`; coexists with it (Owen Costayne KILLED_BY Jon Roxton + KILLED_WITH Orphan-Maker).
- Add to "Possession & Ownership" or "Military & Conflict".

All three gaps are legitimate and recurrent. None are covered by an existing type.

## Cross-identity escalation review

4 escalations were claimed in the results JSON; only 2 found in actual output files (both in the costayne bucket, mutual escalations of the same pair).

**`tom-costayne` ↔ `tommen-costayne-knight`** (mutual):
- Rationale field present and meaningful: "appear to be the same person under two different name forms; mutual wiki cross-references and matching context suggest duplicate nodes"
- This is plausible. "Tom" is a common nickname for "Tommen". The fact that both nodes cross-reference each other in their respective `## Appearances` sections is signal.
- Note however: both nodes also point to a third node `tommen-costayne` (without the `-knight` suffix), which is a *third* costayne with the same name. So we may have 2-of-3 duplicates plus a true distinct third person. The cross-identity-detector should evaluate all three together.
- Schema concern: escalation rows use `note` field instead of `rationale` per the prompt. Same schema-drift problem.

The other 2 escalations promised by the results JSON (`files_with_escalations: 2`) appear in the count metadata but not in any output file I could find — possibly miscounted. The cross-identity-detector pipeline will only see what's in the JSONL files, so the 2 above are what gets handed off.

## Sonnet vs Haiku — comparison verdict

The Session 53b smoke compared Sonnet (3.9% issues) vs Haiku (5.4% with two systematic bugs: FORGED_BY-on-material and TRAVELS_TO-on-non-traveler).

**Searched all 362 prose-edges files in the graph for FORGED_BY-on-material. Zero hits.** The Haiku bug pattern is absent from the bulk-Sonnet output. Sonnet's type discipline is holding at 2.0% in batch-0012 — better than the 3.9% smoke baseline.

**Sonnet IS worth the cost.** Edge content is high-quality; vocabulary discipline is strict; type contracts are honored. The current $3.42/batch is reasonable for what's produced.

The reason to pause is NOT model quality — it's the schema regression that makes outputs un-reviewable. Fixing that doesn't require a model change.

## Comparison: batch-0011 vs batch-0012 schema (full)

| Dimension | batch-0011 | batch-0012 |
|---|---|---|
| Worker | worker-2026-05-14-141623 | worker-20260515-143200000 |
| Edges emitted | 71 | 102 |
| Emit rate | 8.5% (71/835) | 28.9% (102/353) |
| Schema fields | `decision, edge_type, source_slug, target_slug, confidence, rationale` | `decision, edge_type, source_slug, target_slug, confidence_tier, cite_ref` |
| Confidence type | string `"tier-1"` | int `1` |
| Evidence | `rationale` field with verbatim/paraphrased justification | `cite_ref: "## Appearances"` only — no quote, no paragraph |
| Vocab-gap question schema | `question_id, bucket_id, agent, type, text, context.examples` | `question_type, worker_id, batch_id, pattern, description, example_*, frequency` |
| Reviewability | Auditable per-edge | Not auditable per-edge |

batch-0011 (and the 8 vocab-gap questions filed during 0009-0011) used the prompt-conformant schema. batch-0012 invented its own. Both worker sessions ran the same `/worker-stage4` slash command; the prompt didn't pin the schema tightly enough.

## Recommendation

**Do not resume `weirwood stage4 1` until the schema is pinned.** The output content is good but the form is not durable.

Concrete fixes (do these before resuming, in roughly ~30-60 min):

1. **Pin output schema in worker template.** Add a `## Output JSON contract — required fields` section to `.claude/agents/prose-edge-classifier.md` (lines 53-61 area) and to `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md`. Required fields:
   ```
   emit_edge: decision, candidate_kind, source_slug, target_slug, edge_type,
              confidence_tier (int 1|2|3), evidence_snippet (verbatim ≤200 chars),
              evidence_section (heading + paragraph index)
   reject_just_mention: decision, candidate_kind, source_slug, target_slug, reason
   escalate_cross_identity: decision, candidate_kind, source_slug, target_slug,
              evidence_snippet, evidence_section, rationale
   escalate_disambiguation: decision, candidate_kind, source_slug,
              target_candidates, evidence_snippet, anchor_text
   ```
   Pick `confidence_tier: int` over `confidence: "tier-N"` since auditor docs already use the int form.

2. **Add a post-batch validator script.** `scripts/wiki-pass2-validate-edge-jsonl.py` that loads each output file and asserts every row has the required fields for its `decision`. Run after each batch; fail the batch if rows are non-conformant. Forces the schema into mechanical enforcement instead of model-good-behavior.

3. **Decide what to do with batch-0012's 102 emit_edge rows.**
   - **Option A (recommended):** Quarantine batch-0012 outputs. Mark the batch `status: needs-rerun` in the manifest. Re-run with the patched template. Cost: ~$3.42 to redo + ~30 min wall time.
   - **Option B:** Keep them as-is, mark them `evidence_kind: section_header_only`, and let the promoter attach them with that lower confidence. Avoids cost, accepts unverifiable edges.
   - **Option C:** Run a separate Python pass to back-fill `evidence_snippet` from the original candidate JSONL files (which carry the snippet from the cross-reference). Cheap but doesn't catch agent-side reasoning errors.

4. **Decide on the 3 vocab gaps.** All three look acceptable to me. Adding ATTENDS + UNCLE_OF/NEPHEW_OF + KILLED_WITH would bring the vocabulary to 117/15-categories. Per the standing process: update `reference/architecture.md` § Edge Types + the classifier prompt + re-run `build-edge-type-counts.py` to confirm zero drift.

5. **Resume bulk run** with patched template + validator wired in. Sonnet quality is good; volume is the only thing left to grind.

## What's next

- Matt review: pick A/B/C for batch-0012 quarantine, accept/reject the 3 vocab gaps.
- If the vocab gaps are accepted, update architecture.md + prompt before bulk resumes (so the classifier can emit the new types instead of filing them as gaps again).
- Pin output schema + add validator (separate small script-builder task, ~30-60 min).
- Then `weirwood stage4 1` resumes — 12/201 batches done, 189 remaining at $3.42/batch ≈ $647 to bulk completion.

## Files inspected

- 30 batch-0012 output JSONLs (all read; aggregated)
- batch-0011 sample for comparison (alyn-cockshaw, dagon-codd)
- All 362 prose-edges files (Haiku-bug regex search)
- `working/missions/2026-05-14-stage4-v1-bulk-sonnet/results/batch-{0011,0012}.json`
- `working/wiki/pass2-buckets/questions-for-matt.jsonl` (last 10 entries)
- `.claude/agents/prose-edge-classifier.md`
- `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md`
- Frontmatter `type:` field of every emit's source + target slug
