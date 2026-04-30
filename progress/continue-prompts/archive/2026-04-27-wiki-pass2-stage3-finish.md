# Continue Prompt — Wiki Pass 2 Stage 3: Finish (Remaining ~40% of Stage 3 Prep)

**Created:** 2026-04-27 end-of-Session-25
**Supersedes:** `progress/continue-prompts/archive/2026-04-27-wiki-pass2-stage3-prep.md`

**Goal:** Complete the remaining DoD items from the Stage 3 prep prompt. Session 25 finished ~60% (priority script + Stage 3a script + entity-type override patches + edge vocabulary lock documentation). This session finishes the remaining 4 items: full Stage 3a `--apply`, mid-stage review, wiki-ingester v2 prose-only rewrite, validator edge byte-equality enforcement. **Then STOP for Matt's go-ahead before launching Stage 3b.**

## What is already done (Session 25 — do not redo)

- ✅ `scripts/wiki-pass2-prioritize.py` written + Tier-C-entity → Tier-B promotion patched
- ✅ Priority labels applied to all 472 secondary manifests (`priority` field added; `working/wiki-parsed/priority-summary.json` written)
- ✅ Tier distribution surfaced: A=624 (18.5%), B=2,691 (79.8%), C=57 (1.7%, all redirects)
- ✅ `scripts/wiki-pass2-emit-deterministic.py` (Stage 3a) written + tested on 1 bucket (`houses-other-h-w`, 14 nodes)
- ✅ Parser entity-type overrides (21 mistyped "houses" → `organization.faction`)
- ✅ Parser FIELD_EDGE_MAP additions: `fathers`, `cultures`, `battles` (plural variants), `written by` → new `WRITTEN_BY`
- ✅ Edge-vocabulary-lock documented in 4 places (architecture.md, parser docstring, emit-deterministic docstring, todos.md)
- ✅ Edge-polish-phase TODO recorded
- ✅ Non-ASCII normalization → graph-layer TODO recorded
- ✅ `wiki-pass2.sh cmd_run` stale-`tmp/` wipe on retry of `fail`/`validation-failed` buckets
- ✅ Redirect-detection feasibility confirmed (Playwright preserved redirect markup)

## What this session must do

### 1. Decide sequencing (5-min decision)

Two viable orderings. Surface both to Matt at session start; don't pick unilaterally:

- **Option A (sequential):** Run full Stage 3a `--apply` first → generate 3,315 skeletons → THEN do mid-stage review against concrete files → THEN rewrite wiki-ingester v2 against the skeleton format we now have.
- **Option B (parallel):** Rewrite wiki-ingester v2 prose-only IN PARALLEL with Stage 3a apply. Mid-stage review still sequential (needs files to exist).

A is safer (review reads real output); B is faster. Default to A unless Matt says otherwise.

### 2. Run full Stage 3a `--apply`

```bash
cd /Users/mnoth/source/asoiaf-chat
python3 scripts/wiki-pass2-emit-deterministic.py --apply
```

**Expected:**
- 3,315 skeletons emitted across 472 secondary buckets into `working/wiki-pass2/<bucket_id>/tmp/<slug>.node.md`
- ~few minutes wall time (no agent cost; pure local Python)
- `working/wiki-parsed/stage3a-emission-summary.json` written
- Idempotency: re-running should be byte-identical (verified on test bucket)

**Verify after run:**
- Spot-check 3-5 emitted skeletons across different bucket types (a Tier A character, a Tier B character without infobox, a battle page, a place page)
- Confirm no slug collisions
- Confirm `## Edges` section format matches `graph/nodes/characters/jon-arryn.node.md` (Stage 1 reference)
- Compare emission count against `priority.stats` in manifests (sum across all manifests should equal `tier_a + tier_b`)

### 3. Mid-stage review agent

**Spawn:** `general-purpose` subagent (no specialized agent fits this read-only review task).

**Brief the agent to:**
- Read 15-20 stratified Python-emitted skeletons from `working/wiki-pass2/*/tmp/*.node.md`. Stratify across: 5 characters (Tier A), 5 characters (Tier B), 3 battles, 3 places, 2 promoted Tier-B-from-entity (empty-edges case), 2 organization.faction (the post-override fixes).
- For each skeleton, fetch the corresponding row from `working/wiki-parsed/infobox-data.jsonl` and compare:
  - Are all `relationships[]` represented as edges in `## Edges`? (parser dropped any?)
  - Does each emitted edge cite the right `(track_b: <field>)`?
  - Does `entity_type` look right? (the agent should sanity-check post-override values)
  - Does the slug match the wiki-ingester v1 slug rule (`scripts/wiki-pass2-triage.py` slug helper)?
  - Are there any qualifier oddities (non-ASCII characters, unicode quotes, etc.)?
- For Tier B promoted-from-entity (empty-edges) cases, confirm the empty `## Edges` section is acceptable and the rest of the frontmatter is sound.
- For organization.faction cases, confirm the type override took effect.

**Output:** `working/wiki-pass2/stage3a-review.md` — issue list with severity (HIGH/MED/LOW). Read-only review; **agent does NOT modify any node files.**

**Decision after review:**
- Clean (0 HIGH issues): proceed to step 4.
- Patches needed: fix the Python script, re-run `--apply` (idempotent), repeat review.
- Escalate to Matt if anything looks structurally wrong.

### 4. Rewrite `.claude/agents/wiki-ingester.md` to v2 prose-only role

**Current state of the prompt:** the v1 prompt assumes the agent emits the entire node from scratch (frontmatter + Identity + Edges + prose body). For Stage 3b, the agent must do prose ONLY.

**The rewrite must specify:**
- **Inputs:** existing `bucket_input.json` (composed by launcher) + the Python-emitted skeleton in `tmp/<slug>.node.md` (read but do not modify frontmatter, `## Edges`, or `## Identity`).
- **What the agent FILLS:** `## Origins`, `## Allegiances` (narrative — the *story* of the structured edges, not the edges themselves), `## Appearances & Description`, `## Narrative Arc`, `## Quotes`, `## Notes`.
- **What the agent CANNOT do:** emit/modify/reorder edges; modify any frontmatter field; modify `## Identity` (Python's thin one-liner stays); touch `first_available` (deferred per 2026-04-27 decision).
- **Output contract:** the validator will enforce that frontmatter and `## Edges` are byte-identical between input skeleton and agent output. Drift = bucket failure.
- Keep the slug rule reference (`scripts/wiki-pass2-triage.py` slug helper is canonical — do NOT reinvent it in the prompt).

**Existing v1 prompt** at `.claude/agents/wiki-ingester.md`. After rewrite, version it `v2-prose-only` in the frontmatter.

### 5. Update validator for edge byte-equality

**File:** `scripts/wiki-pass2-validator.py`

**Add a check:** for each post-Stage-3b promoted node, locate the original Python skeleton in `working/wiki-pass2/<bucket>/tmp/<slug>.node.md` and confirm the `## Edges` section is byte-identical (including order, whitespace, citations). Frontmatter fields owned by Python (`name`, `type`, `slug`, `aliases`, `confidence`, `wiki_source`, `bucket_id`, `prompt_version`, `node_version`, `pass_origin`) must also be byte-identical.

The agent IS allowed to add the body sections; those new sections don't trigger the equality check.

If drift detected, the validator marks the bucket `validation-failed` so `cmd_run` re-launches it (and now wipes `tmp/` first thanks to the Session 25 fix).

### 6. Hand off cleanly to Matt for Stage 3b launch decision

After steps 2-5, prepare the Tier A bucket list (just count + filename list; no launching). Matt approves before any Stage 3b agent run.

**Cost ballpark to remind Matt:** 624 Tier-A pages × $0.111/node from Stage-1 = ~$70. Well under the "$200 / 2 days wall time" guard from the original prep prompt.

## Hard rules (project-wide; do not bend)

- **Never re-fetch the wiki.** It is local at `sources/wiki/_raw/`. See CLAUDE.md "Critical Rule: The Wiki Is Already Local."
- **Never drop anything from `sources/`.** Tier C pages stay; redirects, stubs, lists, year articles all stay. Source data is read-only and additive-only.
- **`first_available` is fully deferred.** Don't emit. Don't derive. Don't file questions. Backfill via deterministic script post-first-release.
- **Edge vocabulary is locked at the parser.** No script invents edge_types. No agent invents edge_types. Adding a new edge type requires updating `reference/architecture.md` § "Wiki Infobox Fields → Edge Type Mapping" FIRST, then `FIELD_EDGE_MAP` in the parser, then re-running the parser. See the lock callout in architecture.md.
- **Edge polish phase is FUTURE.** The agent does not merge semantically-equivalent edge variants during Stage 3b. That is a separate post-ingestion phase.
- **Python before Agent.** If a deterministic step can produce part of the output, it does. Stage 3a Python OWNS frontmatter + `## Edges` + `## Identity`. Stage 3b agent OWNS only the prose body sections.
- **Never run /endsession without Matt's explicit permission.**
- **Do not launch Stage 3b without Matt's explicit go-ahead.**
- **Do not do prose-derived edge discovery this session.** That's Stage 4 — sequential to Stage 3, never parallel. See `2026-04-27-wiki-pass2-stage4-edge-discovery.md`.

## Open questions to surface to Matt (in priority order)

1. **Sequencing decision** (see step 1 above) — A or B?
2. **Bucket-mixing rule for the 7 mixed-tier buckets** (`battles-{a-b, b, b-d, s-t}`, `houses-other-{b-h, h, h-w}`) — process the whole bucket at the highest priority tier, or split into per-tier sub-buckets? Default in current scripts is whole-bucket; Stage 3b agent will see all priority tiers in the bundle but only Tier A pages will have skeletons it should enrich.
3. **Cross-Pass-1 coverage gap** — only AGOT is Pass-1-complete. Tier A's "in Pass 1" criterion fires only against AGOT until ACOK/ASOS/AFFC/ADWD finish. Acceptable for v1?
4. **Wiki-ingester v2 sequencing** — do the prompt rewrite BEFORE Stage 3a `--apply` (so we know exactly what the skeleton looks like at write-time), or AFTER (rewrite against concrete skeletons we can inspect)? Both are defensible.

## Files in scope this session

**WRITE:**
- `working/wiki-pass2/<bucket>/tmp/<slug>.node.md` × 3,315 (Stage 3a apply)
- `working/wiki-parsed/stage3a-emission-summary.json` (auto-generated by emit script)
- `working/wiki-pass2/stage3a-review.md` (mid-stage review report)
- `.claude/agents/wiki-ingester.md` (v2 prose-only rewrite)
- `scripts/wiki-pass2-validator.py` (edge byte-equality enforcement)

**DO NOT MODIFY:**
- Any existing `graph/nodes/**/*.node.md` (those are Stage 1 promoted nodes)
- Any manifest's `priority` field or other existing fields
- The `tmp/` files this session writes (idempotent re-run is fine)
- `.claude/agents/mechanical-extractor.md` or any other agent prompt
- `scripts/wiki-infobox-parser.py` (locked; only edit if a new edge type lands in architecture.md first)

## DoD for this session

- [ ] Sequencing decision made with Matt
- [ ] Stage 3a `--apply` complete: 3,315 skeletons in `tmp/` directories
- [ ] Spot-check 3-5 skeletons; format matches Stage 1 reference
- [ ] Mid-stage review report written; 0 HIGH issues (or fixed via script patch + re-run)
- [ ] `.claude/agents/wiki-ingester.md` rewritten to v2 prose-only role
- [ ] `scripts/wiki-pass2-validator.py` enforces edge byte-equality + frontmatter byte-equality on Python-owned fields
- [ ] Tier A bucket list prepared for Stage 3b launch (read-only file or printout)
- [ ] **STOP — do not launch Stage 3b without Matt's explicit go-ahead**

## Reference

- `working/runbooks/wiki-pass2-pipeline.md` — canonical pipeline (read first)
- `working/runbooks/wiki-pass2-orchestration.md` — orchestration mechanics (bundle, validator, conflicts, fingerprints) — still applies
- `working/session-details/session-025.md` — Session 25 narrative (this session's prep work)
- `progress/continue-prompts/archive/2026-04-27-wiki-pass2-stage3-prep.md` — original prep prompt (superseded by this one)
- `progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md` — Stage 4 sequel (do not start)
- `reference/architecture.md` § "Wiki Infobox Fields → Edge Type Mapping" — vocabulary lock + 22 current edge types
- `working/wiki-parsed/parse-stats.md` — auto-generated unmapped-fields ranking (the system's gap-finder)
- `working/todos.md` — running TODO list (do not delete entries; check items off as completed)
