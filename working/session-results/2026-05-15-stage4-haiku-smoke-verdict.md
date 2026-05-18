---
session_date: 2026-05-15
session_focus: Stage 4 Haiku 4.5 head-to-head smoke test on batch-0012 (post-schema-pin)
status: complete
verdict: SYSTEMATIC FAILURE — do not use Haiku 4.5 for this task
model_used: claude-opus-4-7[1m] (audit); claude-haiku-4-5 (worker)
companion_docs:
  - 2026-05-15-stage4-batch-0012-quality-check.md (initial Sonnet schema-drift audit)
  - 2026-05-15-stage4-edge-provenance-explained.md (deep-dive on the schema-drift failure mode)
---

# Stage 4 — Haiku 4.5 Smoke Test Verdict

## Verdict

**SYSTEMATIC FAILURE.** Haiku 4.5 produces structurally clean output (validator PASS, 0 violations across 349 rows) that is semantically wrong on roughly 80%+ of emitted edges. The failure mode is consistent across all 30 files: Haiku slams most relationships into a few default edge types (SERVES, SIBLING_OF, FIGHTS_IN), ignores target type contracts entirely, reverses KILLED_BY direction, files zero vocab-gap questions, and misses the cross-identity escalation Sonnet correctly caught.

**Recommendation:** Do not use Haiku 4.5 for prose-edge classification on this task. Re-run batch-0012 on Sonnet with the new patched template + validator. Continue the bulk run on Sonnet. The cost-saving plan (Haiku-bulk + Opus-audit) is not viable: even continuous Opus auditing couldn't fix output this systematically wrong without effectively re-classifying every edge.

## Headline numbers

| Dimension | Sonnet (broken-schema, archived) | Haiku (clean-schema, this run) |
|---|---|---|
| Files processed | 30 | 30 |
| Total candidates | 353 | 349 |
| emit_edge | 102 | 252 (2.5× more) |
| reject_just_mention | 249 | 97 (60% fewer rejects) |
| escalate_cross_identity | 4 (caught tom-costayne / tommen-costayne-knight pair) | **0 (missed it; emitted nonsense edges instead)** |
| escalate_disambiguation | 0 | 0 |
| Vocab-gap questions filed | 3 (ATTENDS, UNCLE_OF/NEPHEW_OF, SLAIN_BY_WEAPON) | **0** |
| Distinct edge_types used | 25 | **9** |
| Tier distribution | 94 tier-1 / 8 tier-2 / 0 tier-3 | **0 tier-1 / 252 tier-2 / 0 tier-3** (uniform tier-2) |
| Validator | n/a (pre-validator) | PASS — 0 violations |
| Wall time | ~73 min (1 batch) | ~3 min (1 batch) |
| Estimated cost | $3.42 | ~$0.30 |

The validator passed because Haiku DID extract verbatim snippets, DID set `evidence_kind` correctly, DID use only canonical edge types. The validator is doing its job — but it can only enforce structure, not meaning.

## The failure modes — by category

### 1. SERVES as universal default (133/252 emits = 53%)

Haiku used `SERVES` for almost any character→character mention regardless of the actual relationship:
- `qarl-corbray SERVES rogar-baratheon` — They were political RIVALS who outmaneuvered each other
- `qarl-corbray SERVES barth` / `SERVES mattheus` — Septons Qarl OPPOSED on the small council
- `qarl-corbray SERVES daemon-velaryon` — Council COLLEAGUE, not master/servant
- `qarl-corbray SERVES ronnal-baratheon` — Adversary
- `lyle-crakehall SERVES edmure-tully` — Edmure was Lyle's CAPTIVE
- `lyle-crakehall SERVES amerei-frey` — Should be VOWS_TO (personal-named oath, per Sonnet's correct call)
- `lyle-crakehall SERVES jorah-mormont` — Jorah unhorsed Lyle in a tourney; that's DUELS, not SERVES
- `lyle-crakehall SERVES jon-bettley` — Jon Bettley is Lyle's SQUIRE (reverse direction)
- `clarence-crabb SERVES brienne-tarth` — Brienne discusses Clarence; he's been dead for centuries
- `clarence-crabb SERVES whispers` — Whispers is the CASTLE Clarence ruled

### 2. Type-contract violations on every spatial/event edge

Haiku ignored target type contracts wholesale. Every spatial or event edge had wrong target types:
- `qarl-corbray SERVES battle-beneath-the-gods-eye` — Battle is event; should be `FIGHTS_IN`
- `qarl-corbray FIGHTS_IN gods-eye` — Gods Eye is a LAKE, not a battle
- `qarl-corbray SERVES golden-wedding` / `SERVES storms-end` / `SPOUSE_OF house-arryn` / `SPOUSE_OF vale-of-arryn` — wedding/castle/house/region as SERVES or SPOUSE targets
- `qarl-corbray SERVES balerion` — Balerion is a DRAGON
- `qarl-corbray SERVES dragon` — generic concept node
- `qarl-corbray UNCLE_OF small-council` — Small Council is an ORGANIZATION, not a niece/nephew
- `lyle-crakehall FIGHTS_IN riverlands` / `FIGHTS_IN tywin-lannister` / `FIGHTS_IN beric-dondarrion` — region/person as battle targets
- `lyle-crakehall SPOUSE_OF jaime-lannister` / `SPOUSE_OF kings-landing` / `SPOUSE_OF margaery-tyrell` / `SPOUSE_OF tommen-baratheon` — Lyle is not married to any of these
- `clarence-crabb SERVES knight` / `SERVES lord` / `SERVES magic` — generic-concept nodes as SERVES targets
- `tom-costayne SIBLING_OF 209-ac` — 209 AC is a YEAR

The validator had no way to catch these — they're all canonical edge types with valid (existing) target slugs. The semantic check ("does the relationship actually fit the type contract?") requires understanding the prose, which Haiku didn't do reliably.

### 3. KILLED_BY direction reversal — systematic

Out of 11 KILLED_BY edges across all Haiku output files in the c-prefix buckets, 6 are direction-reversed or have wrong-type targets:
- `qarl-corbray KILLED_BY davos-darklyn` — REVERSED. Prose says "slain by Lord Corbray with Lady Forlorn" — Qarl killed Davos, not the reverse
- `qarl-corbray KILLED_BY kingsguard` — Same passage; Davos was a Kingsguard, Qarl killed him; emitted as if the Kingsguard killed Qarl
- `elinor-costayne KILLED_BY red-keep` — Red Keep is a building
- `leo-costayne KILLED_BY iron-islands` — Iron Islands is a region
- `dick-crabb KILLED_BY horse` — no horse killed Dick
- `clarent-crakehall KILLED_BY 130-ac` — year as killer
- `clarent-crakehall KILLED_BY battle-by-the-lakeshore` — should be `KILLED_AT`/event-context, not the battle as killer
- `clarent-crakehall KILLED_BY humfrey-lefford` — Humfrey was Clarent's COMMANDER, Clarent died in battle under his command, not BY him

Roughly 55% of KILLED_BY emissions are wrong direction or wrong target type — vs Sonnet which got KILLED_BY direction correct in batch-0011 and batch-0012 (0% reversal).

### 4. Cross-identity miss

Sonnet correctly escalated `tom-costayne` ↔ `tommen-costayne-knight` as a likely-same-person duplicate-node pair. Haiku missed it — instead emitting nonsense edges between them (`tommen-costayne-knight SERVES tom-costayne` with snippet "He may have been..."), treating the speculation about identity as evidence of a service relationship.

### 5. Zero vocab-gap questions

Sonnet filed 3 vocab-gap questions for ATTENDS / UNCLE_OF/NEPHEW_OF / SLAIN_BY_WEAPON. Haiku filed 0. Where Sonnet recognized "this doesn't fit any canonical type", Haiku just defaulted to SERVES or SIBLING_OF and moved on. The "default to filing a vocabulary-gap question over silent rejection" rule from the prompt was effectively ignored — but worse, Haiku didn't reject either; it emitted wrong types instead.

### 6. Tier collapse

Every single one of Haiku's 252 emit_edges is `confidence_tier: 2`. Zero tier-1, zero tier-3. The classifier prompt is explicit: "his uncle X" or "Eddard's wife Y" or "Reek and Osha join his service" are tier-1 (explicit prose statements). Haiku treated everything as tier-2 (implied but clear). This is a uniform under-tiering of explicit evidence.

### 7. Edge type vocabulary collapse

Haiku used 9 distinct edge types across 252 emissions. Sonnet used 25 distinct types across 102 emissions in the broken-schema run. The collapse to a small default vocabulary suggests Haiku stopped reasoning about which type fits each candidate and started defaulting.

| Type | Sonnet (102) | Haiku (252) |
|---|---|---|
| SERVES | 12 | **133 (52.8%)** |
| SIBLING_OF | 0 | **45 (17.9%)** |
| FIGHTS_IN | 13 | 30 |
| SPOUSE_OF | 0 | 12 |
| KILLED_BY | 3 | 9 |
| OWNS | 1 | 9 |
| PARENT_OF | 1 | 7 |
| UNCLE_OF | 0 | 5 |
| WIELDS | 1 | 2 |
| TRAVELS_TO | 15 | **0** |
| ALLIES_WITH | 12 | **0** |
| OPPOSES | 9 | **0** |
| LOCATED_AT | 8 | **0** |
| CONTEMPORARY_WITH | 4 | **0** |
| (15 other types) | 24 | 0 |

Particularly concerning: TRAVELS_TO, ALLIES_WITH, OPPOSES, LOCATED_AT all dropped to ZERO. These are common, well-defined edge types that the prose obviously supports — Haiku just didn't reach for them.

## Why this happened (hypothesis)

The patched prompt is *more demanding*, not less. It requires:
- Verbatim snippet extraction (new — adds ~15-200 chars per row, must come from the source's prose body)
- `evidence_kind` deterministic field (new)
- Type contract reasoning ("WIELDS only on artifacts; SWORN_TO targets organizations")
- Direction reasoning (KILLED_BY direction; comention direction)
- Vocab-gap default ("file a question rather than silently reject")
- Tier calibration (tier-1 vs tier-2 vs tier-3)
- 125-type vocabulary span

It looks like Haiku 4.5 prioritized the *snippet extraction* task (which the validator enforces hardest) at the expense of the *classification* task (which the validator can't enforce). The snippets ARE good — verbatim, ~100-150 chars, properly section-tagged. The edge_type assignments are not.

This matches what the Session 53b smoke verdict warned: "Haiku CONCERNS-high (5.4% issue rate) with two systematic bugs (`FORGED_BY` for materials, `TRAVELS_TO` for persons)." Today's run shows DIFFERENT systematic bugs (SERVES-on-everything, direction reversal on KILLED_BY, type-contract violations on every spatial/event edge), but the *mode* is the same: Haiku produces structurally-clean systematic semantic failures.

The validator-and-cross-model-audit plan was designed to catch this. It worked: the validator passed (so the schema rules hold), and the Opus audit caught the semantic failure on the first batch. The plan worked — what we learned is that Haiku doesn't get past the audit gate.

## Cost reframe

Original plan: Haiku-bulk ($80) + Opus-audit ($120-150) = ~$200 for 189 batches.

Reality based on this batch: Opus would have to re-derive the correct edge_type and direction for every single Haiku emission to catch the semantic errors. That's not "auditing" — that's re-classifying. Cost would balloon to ~Opus-doing-the-bulk levels (~$2000-3000), defeating the purpose. There's no productive Haiku-with-cleanup path.

Sonnet plan: ~$3.42 × 189 batches = ~$647 with the patched template + validator. This is the right number to spend.

## What I did with the artifacts

- **Sonnet broken-schema output:** archived to `working/wiki/pass2-buckets/_archive/batch-0012-sonnet-pre-schema-fix-2026-05-15/` (preserved for comparison record)
- **Haiku failed output:** archived to `working/wiki/pass2-buckets/_archive/batch-0012-haiku-failed-2026-05-15/` (preserved for comparison record)
- **batch-0012 manifest entry:** reset to `status: queued` with two `previous_run` breadcrumbs documenting both failed runs
- **Lock file:** removed

## Recommendation

1. **Re-run batch-0012 on Sonnet** with the patched template + validator. Should complete cleanly per the new contract; will give us the canonical "Sonnet-with-clean-schema" reference output for batch-0012's 30 buckets.
2. **Resume the bulk run on Sonnet** at the new cost (~$3.42/batch). 189 batches remaining ≈ $647 to bulk completion.
3. **Keep the cross-model audit cadence** for Sonnet — Opus audits every Nth Sonnet batch to catch any future schema or type-discipline drift. Lower frequency than the planned Haiku cadence (probably 1-in-20 instead of 1-in-3-to-10), since Sonnet has demonstrated stable type discipline (2.0% in batch-0012).
4. **Do not retry Haiku** under modified prompts. The failure mode is too systematic and too varied (different bugs each smoke). The cost gap doesn't justify the quality risk for this task.
5. **Update the mission spec** (`working/agent-fleet-specs/missions/2026-05-14-stage4-v1-bulk-sonnet.md`) to record the Haiku-rejection decision so future operators don't retry it. The Session 53b smoke notes already say "Decision: Sonnet" — this run reinforces that with stronger evidence.

## What's next

This session is in a good place to pause. Three independent artifacts are clean:
- Patched classifier prompt + worker template (schema pinned)
- New validator script (mechanically enforces the contract)
- 4 new vocab types added to architecture.md (Stage 4 ready to use them)

When Matt comes back, decisions:
- Approve re-running batch-0012 on Sonnet?
- Resume the bulk run on Sonnet?
- Update mission spec to formalize Haiku-rejected-twice?

## Files for the record

- This verdict: `working/session-results/2026-05-15-stage4-haiku-smoke-verdict.md`
- Sonnet archive: `working/wiki/pass2-buckets/_archive/batch-0012-sonnet-pre-schema-fix-2026-05-15/` (30 files + results JSON)
- Haiku archive: `working/wiki/pass2-buckets/_archive/batch-0012-haiku-failed-2026-05-15/` (30 files + results JSON)
- Patched prompt: `.claude/agents/prose-edge-classifier.md`
- Patched worker template: `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md`
- New validator: `scripts/wiki-pass2-validate-edge-jsonl.py`
- Architecture vocab additions: `reference/architecture.md` (UNCLE_OF, NEPHEW_OF, KILLED_WITH, ATTENDS)
