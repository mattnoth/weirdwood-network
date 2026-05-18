# Stage 4 Vocab Lock — Apply Phase + Haiku Smoke Prep

> **Recommended model:** Opus 4.7 — apply work is mechanical, but the same session also designs the Haiku smoke-test plan on already-done batches (architecture-level decisions). Opus is justified for the planning portion.
>
> **Parent context:** `progress/continue-prompts/2026-05-18-stage4-haiku-cutover.md` (the 3-step Haiku cutover plan; this is Step 1's apply phase + groundwork for Step 3 Haiku smoke).
>
> **What was decided last session (Session 55, 2026-05-18):** **17 new edge types** approved + 2 description modifications. Vocab grows 132 → 149. All open questions locked at session-end:
> - `CREW_OF` ACCEPTED (Path B) — sibling to `CAPTAIN_OF`; both target `object.artifact` (vessel). Qualifier carries role detail ("first mate", "oarsman").
> - `AFFLICTED_BY` + `DIED_OF` placed in **Knowledge & Information** subsection (sits next to existing `HEALS`, which is medical-adjacent).
> - `CAPTAIN_OF` placed in **Possession & Ownership** subsection.
>
> Decisions are in `working/agent-fleet-specs/stage4-vocab-lock-2026-05-18.md`. Full session narrative + agent's architecture-diff text in `history/session-details/session-055.md`.

---

## Goal

Apply the locked vocab to the durable files so the classifier prompt switches to "vocab FINAL — do not file vocab-gap questions" before the Sonnet bulk worker resumes or the Haiku smoke runs.

Decisions are made. This session is **mechanical apply** — no judgment calls except CREW_OF.

---

## Step 1 — Apply architecture.md diffs

**File:** `reference/architecture.md`. The full diff text is in `working/agent-fleet-specs/stage4-vocab-lock-2026-05-18.md` Buckets B + D verdicts, **PLUS** the second-opinion agent's revised diffs (in `history/session-details/session-055.md` Phase 6 — the agent provided ready-to-paste table rows).

**17 new types to add** (all locked Session 55):

| Type | Subsection in architecture.md |
|---|---|
| `AFFLICTED_BY` | Knowledge & Information (next to HEALS) |
| `DIED_OF` | Knowledge & Information (next to AFFLICTED_BY) |
| `COMPANION_OF` | Emotional & Perceptual (symmetric) |
| `PARTICIPATES_IN` | Military & Conflict |
| `OFFICIATES` | Cultural & Religious |
| `ATTACKS` | Military & Conflict |
| `ASSAULTS` | Military & Conflict |
| `COURTS` | Kinship & Family |
| `CONTRACTED_WITH` | Factional & Diplomatic |
| `PROPOSED_AS_BRIDE` | Kinship & Family |
| `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` | Hospitality & Custom |
| `PRACTICES` | Magic & Supernatural |
| `PURCHASED_FROM` | Possession & Ownership |
| `BUILT` | Possession & Ownership |
| `CAPTAIN_OF` | Possession & Ownership |
| `CREW_OF` | Possession & Ownership (sibling to CAPTAIN_OF) |
| `REPUTED_AS` | Emotional & Perceptual |

**2 description modifications:**
- `FIGHTS_IN` — change "Participates in a battle or war" to "Participates in a battle, war, or tournament as a combatant." Target column: "Person → Event (battle/war/tournament)."
- `MANIPULATES` — add to description: "Note mechanism in `notes` when known (e.g., `via bribe`, `via flattery`, `via false information`)."

**Vocab count bump:**
- Locate the master-vocabulary callout (above the wiki-infobox table, around architecture.md line 512). Currently says "~132 distinct edge types." Change to **149 distinct edge types**.
- Update the "Session 53/54/55 added X, Y, Z" historical note to add Session 55 additions (the 17 new types). Keep prior sessions' notes intact.

**Read the second-opinion agent's full diff text in `history/session-details/session-055.md` Phase 6** — it has ready-to-paste table rows for ATTACKS, ASSAULTS, PURCHASED_FROM, BUILT, CAPTAIN_OF, REPUTED_AS, CROWNS_QUEEN_OF_LOVE_AND_BEAUTY, PROPOSED_AS_BRIDE, CONTRACTED_WITH, plus the MANIPULATES + FIGHTS_IN modifications. Use those verbatim where present; draft fresh rows for the others (AFFLICTED_BY, DIED_OF, COMPANION_OF, PARTICIPATES_IN, OFFICIATES, COURTS, PRACTICES) matching the existing markdown table style.

---

## Step 2 — Update the classifier prompt

**File:** `.claude/agents/prose-edge-classifier.md`

Three edits required:

### 2a. Switch gap-filing default to FINAL

Find the "Vocabulary lock — read twice" section (around line 208). Currently says: "If a candidate represents a relationship that doesn't fit any of the ~125, **default to filing a `vocabulary-gap` question over silent rejection.**"

Replace with: "**The vocabulary is FINAL as of Session 55 (2026-05-18).** If a candidate represents a relationship that doesn't fit any of the ~148 canonical types, **reject_just_mention with reason `no-fitting-type-vocab-locked`. Do NOT file vocabulary-gap questions for the remaining batches.** The bulk run cannot pause for vocab review at this stage; the classifier must work the closed surface."

Also update the numbered list directly below (currently 1. File a vocab-gap; 2. Don't fall back; 3. reject as no-fitting-edge-type) — collapse to: "**reject_just_mention with reason `no-fitting-type-vocab-locked`** — this is the only correct action for relationships that don't fit the locked vocab. Do NOT fall back on a near-fit type (CONTEMPORARY_WITH, KNOWS, ATTENDS on persons, FIGHTS_IN on persons) — those produce wrong edges that pollute the graph. The vocab is intentionally closed."

### 2b. Bump vocabulary count + add new types to category expansions

Find references to "~125 edge types" and update to "~149". Locations:
- First Steps section line 20: "all 15 subsections... ~125 edge types"
- Vocabulary lock section line 210
- Definition of Done section: "locked master vocabulary (~125 edge types in architecture.md)"

In the "Concretely, the categories your prose-derived edges may emit from" bullet list (around line 212-228), add the new types to the appropriate categories:
- Kinship & Family: add `COURTS`, `PROPOSED_AS_BRIDE`
- Factional & Diplomatic: add `CONTRACTED_WITH`
- Military & Conflict: add `ATTACKS`, `ASSAULTS`, `PARTICIPATES_IN`
- Knowledge & Information: add `AFFLICTED_BY`, `DIED_OF`
- Emotional & Perceptual: add `COMPANION_OF`, `REPUTED_AS`
- Possession & Ownership: add `PURCHASED_FROM`, `BUILT`, `CAPTAIN_OF`, `CREW_OF`
- Magic & Supernatural: add `PRACTICES`
- Cultural & Religious: add `OFFICIATES`
- Hospitality & Custom: add `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY`

### 2c. Update reverse-direction edges section

Find the "Reverse-direction edges" section (around line 247). Currently lists 7 one-sided types + a "both-sided" list of 3 pairs (KILLS/KILLED_BY, UNCLE_OF/NEPHEW_OF, WARD_OF/FOSTERED_BY).

**Add to both-sided list:** KNIGHTED_BY/BESTOWS_KNIGHTHOOD_ON, NURSED_BY/WET_NURSE_OF.

**Add to one-sided list (do NOT emit reverse):** CHILD_OF (use PARENT_OF), HOST_OF/HOSTED_BY (use GUEST_OF on guest), RESURRECTED_BY (use RESURRECTS on resurrector), SERVED_BY/EMPLOYS (use SERVES on server), DEFEATED_BY (use DEFEATS on victor), GUARDIAN_OF (use FOSTERED_BY).

This makes the most-common-mistakes explicit in the prompt so the classifier doesn't even contemplate filing them as vocab gaps.

---

## Step 3 — Close the gap rows in questions-for-matt.jsonl

Write a Python script `scripts/stage4-close-vocab-gaps.py` that:

1. Reads `working/wiki/pass2-buckets/questions-for-matt.jsonl` (68 rows).
2. For each row, determines its disposition from the decision doc lookup:
   - **Stale-resolved (12 rows)** — proposed type now in canonical vocab. Resolution: `"resolved-pre-adopted; type X added Session N"`.
   - **Hard-rejected (9 rows; Bucket C)** — reverse-direction or too-generic. Resolution: `"rejected-reverse-direction-use-X"` or `"rejected-too-generic-use-X"`.
   - **D-bucket rejected (6 rows)** — NAMED_AFTER, GREAT_UNCLE_OF/DAUGHTER_IN_LAW_OF/STEP_PARENT_OF, BRIBES standalone, CREW_OF (if Path C), USES_AS_SIGIL. Resolution: per the doc.
   - **D-bucket accepted (varies)** — accepted into vocab. Resolution: `"accepted-as-X; added Session 55"`.
   - **Bucket B accepted (6 rows)** — AFFLICTED_BY/DIED_OF/COMPANION_OF/PARTICIPATES_IN/OFFICIATES. Resolution: `"accepted-as-X; added Session 55"`.
3. Appends `resolved_at: "2026-05-18T..."` and `resolution: "<text>"` fields to each row.
4. Re-writes the JSONL.
5. Prints summary: "Closed N rows: A stale, B accept, C reject."

The 7 untyped (deprecated abbreviated schema) rows: tag with `resolution: "stale-schema; superseded by Session-55 decisions; see history/session-details/session-055.md"` if their gap is covered by a Session-55 verdict, or `resolution: "stale-schema; needs manual triage"` otherwise. Eight of the 16 distinct schemas in the JSONL are deprecated — the script should map every row regardless of source schema.

---

## Step 4 — Update working/todos.md

Mark `HAIKU-CUTOVER STEP 1` as `[x]` DONE. Add `→ continue: progress/continue-prompts/2026-05-18-stage4-burn-link-substitution.md` (or similar) under STEP 2 if you want to queue the next Haiku-cutover step immediately.

---

## Step 5 — Optional: Add backlog item for vocab-decision-reviewer agent

Matt skipped writing this agent during Session 55 but the design was sketched. Add a one-line backlog item under "Agent Improvements" or similar in `working/todos.md`:

```
- [ ] **FUTURE — `vocab-decision-reviewer` agent** — Surfaced 2026-05-18 (Session 55). Reusable second-opinion agent for vocab decisions. Pre-loaded reads of architecture.md + classifier prompt + questions-jsonl + rollup. Sonnet model. Tools: Read/Glob/Grep (advisory, never writes architecture.md). Per-invocation prompt passes specific items needing verdicts. See session-055.md Phase 10 for full design sketch. Apply when next vocab-lock round surfaces.
```

---

## Step 6 — Haiku smoke-test prep (the architecture-level part of the session)

After the apply work lands, design the Haiku smoke. The plan:

**Goal:** re-run Haiku 4.5 on already-done Sonnet batches, write to a parallel `haiku-smoke/` directory, then diff. Matt's session resumes the bulk run on Haiku ONLY if the diff passes thresholds.

**Constraints (from the parent continue prompt):**
- Never overwrite Sonnet output. Haiku writes to `working/missions/2026-05-14-stage4-v1-bulk-sonnet/haiku-smoke/<batch_id>/`.
- Smoke batches must be complex/diverse — not 3 trivial ones.
- Use the locked vocab (Step 1-3 above must be done first).
- Drift detection mandatory: schema validator + cross-model diff + verdict gates resumption.

**Candidate done batches identified (from mission manifest, verified at end of Session 55):**

All 72 done batches are `source_target` shape. The 5 hot-page batches the parent continue prompt called out are all present in the done pool:

| batch | shape | file_count | notable page(s) | candidate volume |
|---|---|---|---|---|
| `batch-0065` | source_target | 5 | wylis-manderly | ~112 candidates |
| `batch-0066` | source_target | 5 | wyman-manderly | ~168 candidates (biggest known) |
| `batch-0068` | source_target | 5 | bowen-marsh | ~66 candidates |
| `batch-0072` | source_target | 5 | taena-merryweather + hallis-mollen | ~53 + 71 candidates |

For diversity, also include 1-2 large-file-count batches from early in the run (broader page mix):
| `batch-0001` | source_target | 30 | mixed (daemon-sand, ryon-allyrion, etc.) | ~varied |
| `batch-0002` | source_target | 30 | mixed | ~varied |

**Recommended smoke set:** batches **0066, 0068, 0072, 0001** (4 batches). Covers: one mega-page, one mid-page, one multi-page mix, one early-batch broad-mix. Skip 0065 (similar to 0066 — both Manderly).

**What's NOT in the done pool:** `pass1_relationship` and `comention` shapes. Those still need their candidate files generated. **Defer those shapes to a later smoke round** — the source_target-only smoke is the priority because all the Sonnet baseline lives in that shape.

**Steps for the smoke design (write a smoke-spec file at `working/agent-fleet-specs/stage4-haiku-smoke-spec-2026-05-18.md`):**

1. Specify the 4 batch IDs + their input files.
2. Document the Haiku invocation command (the existing `worker-stage4` machinery should accept a `--model` flag, or document the override path).
3. Specify the output directory pattern: `working/missions/2026-05-14-stage4-v1-bulk-sonnet/haiku-smoke/<batch_id>/<source_slug>.edges.jsonl`.
4. Specify the diff metrics:
   - Per-candidate decision agreement (emit / reject / escalate).
   - Edge-type agreement on matched-emit rows (confusion matrix).
   - Confidence-tier agreement.
   - Snippet capture rate (Haiku vs Sonnet's 84%).
   - Cost + wall-clock per batch.
5. Specify pass thresholds (default proposed: ≥90% emit/reject agreement, ≥85% edge-type agreement on matched emits, ≥80% snippet capture — final call is Matt's).
6. Write a diff script `scripts/stage4-haiku-smoke-diff.py` that compares Sonnet output (in `working/wiki/pass2-buckets/<bucket>/prose-edges/<slug>.edges.jsonl`) against the Haiku parallel output and emits the metrics above.

**DO NOT run the actual Haiku invocation in this session** — that's launched from the iTerm pipeline per Matt's `feedback_no_extraction_without_asking.md` rule. The smoke spec defines what gets run; Matt fires it.

---

## Definition of done

- [ ] architecture.md has all 17 new rows + 2 description mods + vocab count bumped (132 → 149) + Session 55 historical note added
- [ ] classifier prompt has gap-filing default flipped to FINAL + vocab count bumped + new types in category list + reverse-direction sections updated
- [ ] `scripts/stage4-close-vocab-gaps.py` written + run + 68 rows closed with `resolved_at`/`resolution` fields
- [ ] `working/agent-fleet-specs/stage4-haiku-smoke-spec-2026-05-18.md` written with batch IDs, output dir, metrics, thresholds
- [ ] `scripts/stage4-haiku-smoke-diff.py` written (the diff tool itself; not the runner)
- [ ] `working/todos.md` shows HAIKU-CUTOVER STEP 1 as `[x]` done; STEP 5 (Haiku smoke) now has its prep done — STEP 5's actual smoke run is Matt-fired
- [ ] Session-results file written at `working/session-results/<date>-stage4-vocab-applied-and-smoke-prepped.md`

After: STEP 2 ([LINK] substitution) + STEP 3 (validator type-contract extension) + STEP 4 (suspicious-edges flagger) still pending. Matt's call whether they happen alongside the smoke or before.

---

## DO NOTs

- Do NOT touch the running Sonnet worker prompt scaffolding (`.claude/commands/worker-stage4.md`). The worker prompt loads the agent prompt; only the agent prompt changes.
- Do NOT run the Sonnet bulk worker yet — stop file in `/tmp/stage4-stop` should stay set until at least HAIKU-CUTOVER STEP 4 is also done. The vocab lock alone doesn't justify resumption.
- Do NOT auto-run `/endsession` without permission.
- Do NOT delete any gap rows — append-only JSONL convention.
