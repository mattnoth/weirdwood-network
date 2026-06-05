# Edge/Event Modeling — Cleanroom Recommendation Execution Prep

> **Recommended model:** Opus 4.7 for the verification + planning conversation (judgment-heavy, surfaces decisions for Matt). Sonnet 4.6 for any mechanical follow-up work once Matt approves a track (doc edits, filter scripts).
>
> **Trust `worklog.md` over this prompt** if they disagree (CLAUDE.md #9). This prompt was written end of S82; the cleanroom recommendation is **NOT YET DECIDED** — your job is to *prep* execution, not execute.
>
> **Supersedes (partially):** `progress/continue-prompts/2026-06-01-events-bulk-escalation-pick.md` — the cleanroom lens reshapes the A-E escalation choice; do NOT treat it as a free 5-way pick anymore. See "Track A" below.
>
> **Hard rules carried forward:** never modify `graph/edges/edges.jsonl` without Matt's before/after sign-off; never trigger a Pass-1 rerun without a separate explicit decision (it's a whole project on its own — all-Opus, 344 chapters).

## Prerequisite — read these first

1. **`worklog.md` Session 82 entry** — current state, the two-doc convergence, the recommended move.
2. **`EDGE_MODELING_DECISION-cleanroom.md`** — fresh-context decision (canonical for execution prep; the cleaner of the two docs).
   - **First line note:** the doc opens with `"I wasn't able to write the file (permission wasn't granted). Per the brief's 'write it, or print it in full,' here is the complete decision document."` — that's a Write-permission artifact, not the document. Real content starts at line 3 with the `# Edge & Event-Modeling — Diagnosis & Recommendation` header.
3. **`EDGE_MODELING_DECISION.md`** — first-pass decision with repo access; cross-check against the cleanroom on the few disagreements (see "Cleanroom-specific disagreements" in the S82 worklog entry).
4. **`EDGE_INVENTORY_ANALYSIS_PROMT.md`** — the cleanroom brief; §1.7 diagnostic heuristic is the lens, §1.8 grammatical-subject trap is the headline root cause.
5. **`EDGE_INVENTORY_REPORT.md`** — only as a reference if you need to verify a specific claim; do NOT re-read top-to-bottom (281KB).
6. **`reference/architecture.md`** — edge-type vocabulary + Directionality column; needed for Track B and Track C.

## What the cleanroom recommends (three tracks)

### Track A — Reframe the Events Haiku escalation pick (supersedes the free A-E choice)

The S81 escalation pick (`2026-06-01-events-bulk-escalation-pick.md`) presented 5 paths as a free choice. The cleanroom changes the analysis: **Haiku's measured drift concentrated on `TRAVELS_TO` / `TRAVELS_WITH` / `LOCATED_AT`, which are exactly the cleanroom's CANONICALIZE bucket, NOT the REIFY bucket.** That maps onto path (B) "promote long-tail-only" with a sharper criterion:

> **Sharpened (B):** Promote Haiku rows where the candidate already anchors to an existing `event.*` node (the reify bucket); HOLD rows where the candidate targets a person or venue (the canonicalize bucket — needs the head rule applied at extraction layer, not at typing layer).

Path (C) — Sonnet-filter the rejection-bearing types ~$2-5 — is still on the table and may compose with the sharpened (B): Sonnet-filter the held-back canonicalize rows, promote the reify rows directly. Paths (A) and (D) become less attractive under the cleanroom lens (re-running on Sonnet or v6-Haiku doesn't fix the underdetermination; it just gets more emits that still have no canonical form). Path (E) is the always-available cheap-exit.

### Track B — Backfill role edges onto the 371 existing event nodes (the high-leverage move)

The cleanroom's central claim is that **the event-node infrastructure already exists but is structurally empty.** 371 `event.*` nodes per `graph/index/events/_summary.json:1-12` (cleanroom citation; **verify before committing to it**). The canonical case: Red Wedding has 3 outbound edges (cleanroom says "§6.10", from the inventory report).

The Haiku Events bulk output is the seed for backfill: rows already carry a `**title**` field (S80 analysis noted this; cleanroom calls it "the closest thing to an event-id in any layer today"). The audit's path C costed it at ~$2-5 and flagged it as the highest-leverage move on the table.

**Role-edge schema additions** the cleanroom proposes (cleanroom §3.1):
```
AGENT_IN      person  → event   # perpetrator/actor
VICTIM_IN     person  → event   # patient/target
COMMANDER_OF  person  → event   # instigator/orderer  [or reuse COMMANDS_IN]
INSTRUMENT_IN artifact→ event   # or reuse WIELDED_IN
```
Reuse existing `LOCATED_AT` (event→location), `OFFICIATES`, `ATTENDS`, `FIGHTS_IN`. Non-participant axes go on the node frontmatter: `outcome`, `method`/`qualifier`, `time`, `recipient`/`purpose`.

### Track C — Doc changes to the Pass-1 prompt (no rerun trigger)

The cleanroom's headline root-cause finding is grammatical-subject leakage at Pass-1 (`mechanical-extractor.md:176-178`). The fix:

1. **Add an `## Events Observed` table to the prompt** with role columns: `| Event Title | Type | Agent(s) | Patient/Target(s) | Instrument | Location | Instigator | Outcome | Evidence |`. Multi-participant rows keyed by a shared **Event Title**.
2. **Add to `## Relationships Observed`:** *"Column A is always the SEMANTIC AGENT, never the grammatical subject and never the POV character; for passive sentences put the by-phrase agent in A; record orderers in the Events table's Instigator column, not in A."*

This is a doc-only change. It does NOT trigger a Pass-1 rerun. It just means the *next* time Pass-1 runs (for a sixth book, or an enrichment pass, or if Matt later decides on a full rerun) it benefits.

## Your job (this session)

**Verify first, plan second, ask Matt third, execute only with explicit go.** No spend, no `edges.jsonl` modification, no Pass-1 rerun.

### Step 1 — Verify the cleanroom's empirical claims (read-only, $0)

The cleanroom doc was written without repo access. Trust the *reasoning*, verify the *numbers* before acting:

- [ ] `graph/index/events/_summary.json` — confirm event-node count (cleanroom claims 371).
- [ ] `graph/nodes/events/red-wedding.node.md` (or wherever it lives — `find graph/nodes -name 'red-wedding*'`) — count the outbound edges in its `## Edges` section (cleanroom claims 3).
- [ ] `.claude/agents/mechanical-extractor.md` — verify the Pass-1 extractor table appears at lines 176-178 (cleanroom citation) and verify there is genuinely no head rule.
- [ ] `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/*/*.edges.jsonl` — confirm the `**title**` field exists on emit rows and is stable enough to use as an event-id (sample a few; cleanroom flagged it as worth confirming — listed as G7 in the gaps section).
- [ ] `graph/edges/edges.jsonl` — count person→person `KILLS` edges where the chapter has a known event-node match (gives the sizing for the Reify@occasion-vs-Canonicalize split for the KILLS family).
- [ ] `reference/architecture.md` — check the edge-type vocabulary table; confirm `AGENT_IN` / `VICTIM_IN` / `COMMANDER_OF` / `INSTRUMENT_IN` are NOT already in the vocabulary (the cleanroom proposes adding them).

If any claim doesn't survive verification, flag it explicitly to Matt **before** building plans on top of it (memory rule: "verify before recommending from memory" applies equally to a fresh agent's recommendation).

### Step 2 — Draft the three execution plates (no execution)

Each plate should be small enough for Matt to review at a glance and approve/reject independently. Lay them out as a single message to Matt, not as committed work.

**Plate B-doc (Track C — Pass-1 prompt doc change):**
- Identify the canonical Pass-1 prompt file (is it `.claude/agents/mechanical-extractor.md`, or does the canonical version live elsewhere — check memory `project_pass1_prompt_v3_canonical`).
- Draft the `## Events Observed` table addition + the head-rule sentence as a literal diff.
- Confirm this is purely additive and doesn't break existing Pass-1 parsers (`python-map` etc.).
- Estimated risk: low (doc-only, no live consumer until next Pass-1 invocation).

**Plate A-schema (Track B prerequisite — architecture.md role-edge additions):**
- Draft the architecture.md edits to add `AGENT_IN`, `VICTIM_IN`, `COMMANDER_OF`, `INSTRUMENT_IN` as event-attached role edges.
- Decide reuse vs new: cleanroom hedges on `COMMANDER_OF` (or reuse `COMMANDS_IN`) and `INSTRUMENT_IN` (or reuse `WIELDED_IN`). Recommendation depends on what's already in the vocabulary — verify first, then propose.
- This is a prerequisite for Plate B-backfill; do NOT propose backfill execution without this landing first.

**Plate B-backfill (Track B — role-edge population from Haiku output):**
- Specify the deterministic filter: "for each Haiku emit row, attempt to resolve the `**title**` field to an existing `event.*` slug; if resolved AND the edge_type is in the death/violence/ceremony/conspiracy/guest-right family, rewrite as a role edge to the event node; else hold for canonicalize."
- Cost: $0 if pure deterministic; ~$2-5 if a Sonnet pass is needed for title-disambiguation cases.
- This is a NEW edge writeout (not a modification of `edges.jsonl` — additive into a staging file first; merge is its own gated milestone).
- Cite the title-stability check from Step 1 in the writeup; if titles are too noisy for deterministic resolution, escalate the cost estimate.

**Plate A-pick (Track A — Events Haiku escalation pick under cleanroom lens):**
- Re-present the 5 escalation paths from `2026-06-01-events-bulk-escalation-pick.md` with the cleanroom reframe applied (sharpened B, possibly composed with C).
- Recommend a specific path; surface the tradeoff explicitly.

### Step 3 — Surface decisions, hand to Matt

Single message, plates A-doc / A-schema / B-backfill / A-pick laid out with: what the plate does, what it costs, what it depends on, what's reversible. Make it easy for Matt to say "approve plate X, hold plate Y."

Do NOT execute anything in this session beyond verification reads + drafts. The plates are *for Matt to approve*, not for you to apply.

## Out of scope (this session)

- **Pass-1 rerun.** Not in scope. The cleanroom recommendation explicitly avoids it. If you find yourself wanting to propose one, push back to a separate decision.
- **`edges.jsonl` modification.** Hard rule from S77; carries forward. Backfill writes go to a staging file first, never to `edges.jsonl` without before/after sign-off.
- **The 3 carried-forward core-cleanups** (drop 2 `cersei↔tyrion` LOVES; ~22 `ASSAULTS`→`ATTACKS`; merge-time `OWNS→BONDED_TO`). Still gated on Matt; out of scope for this session unless he raises them.
- **The dyadic-acts canonicalize sweep at scale.** The cleanroom recommends it eventually (re-invert ~232 unordered pairs carrying same type in both directions, etc.) but doesn't depend on it. Defer until after the reify track lands.

## What "done" looks like for this session

- All Step 1 verifications complete; numbers confirmed or flagged.
- Four plates drafted and presented to Matt as approve/hold/reject items.
- A revised continue prompt for the next session that picks up wherever Matt's decisions land, OR (if no decisions yet) a hand-off note explaining what's blocked on whom.
- Worklog S83 entry queued for `/endsession` (Matt's permission to run it).

## Useful background memory

- `project_stage4_pass1_derived_pivot` — Stage 4 builds edges from Pass 1; wiki-comention is deprecated.
- `project_pass1_prompt_v3_canonical` — v3 is the current Pass-1 schema (all 5 books done).
- `project_first_available_deferred` — don't touch `first_available` reasoning during agent work.
- `project_video_game_entities_excluded` / `project_impersonation_edges_redirect` — graph hygiene rules that may matter for role-edge backfill.
- `feedback_python_before_agent` — deterministic Python steps run first; agents only for genuine reasoning. The role-edge backfill is mostly deterministic (slug-resolve the `**title**`); use Python first.
- `feedback_no_extraction_without_asking` — extractions go through `weirwood` pipeline in iTerm. Backfill is not extraction, but any $$ spend still gets Matt's explicit go.

## Files this session may create / modify

**Verification reads:** all under `graph/`, `working/wiki/pass2-buckets/`, `.claude/agents/`, `reference/`.

**Drafts (do NOT commit until approved):**
- Plate B-doc: a candidate diff for `.claude/agents/mechanical-extractor.md` (or wherever).
- Plate A-schema: a candidate diff for `reference/architecture.md`.
- Plate B-backfill: a candidate Python script spec (do not write the script yet — spec it, get Matt's approval, then `script-builder` writes it).
- New continue prompt for next session reflecting Matt's decisions.

**Worklog:** Current State Events line stays as-is (S82 captured the cleanroom landing). New S83 entry queued for `/endsession` only.
