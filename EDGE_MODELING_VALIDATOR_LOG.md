# Edge-Modeling Validator Log

> **Purpose.** This is a **standing, append-only** record of what's actually been done against the edge-modeling reification plan, written so a fresh validator agent (with no carry-over context) can check whether execution is still aligned with the design — without needing to re-derive everything from source.
>
> **For Matt.** This is the file he reads (or hands to a validator agent) when he wants a quick "are we still on plan?" check without sitting through every session.
>
> **For the validator agent reading this file.** Your job: read this log + read `working/edge-modeling/edge-modeling-reification-design.md` + read `worklog.md` Current State, then flag any of:
>
> 1. **Drift** — execution diverged from the design without a recorded adjustment.
> 2. **Stale design** — the design doc says X but actual repo state contradicts X, and no entry below acknowledges the contradiction.
> 3. **Unresolved Matt decisions** — open questions accumulating without an answer.
> 4. **Skipped preconditions** — a plate ran without its declared preconditions being met.
> 5. **Source-data violations** — anything in `graph/` was modified outside a Plate 5 / properly-gated merge step. (CLAUDE.md hard rule: source data is read-only / additive-only.)
>
> Your output should be short (under 500 words) and reference specific entries below by plate number + date. If everything looks aligned, say so explicitly — silence is not OK; Matt needs the affirmative "looks aligned" signal.
>
> ---
>
> ## Append rules (for future Claude sessions writing here)
>
> - **APPEND-ONLY.** Never edit or overwrite earlier entries. If a prior entry turns out to be wrong, append a new entry that says so — don't rewrite history.
> - **One entry per plate completion** (or per plate-block if multiple plates ship in one session).
> - **Each entry must include:** plate number, ISO date, commit hashes that landed the work, the design-doc claim being acted on, what actually happened, surprises/divergences, adjustments to the plan, open questions for Matt, and a "validator checks" section listing concrete files/greps a fresh agent should run to verify the claims.
> - **Be honest about misalignment.** If the design doc said X and you found Y, say so. Don't paper over the gap.
> - **Cite live artifacts**, not memory: file paths + commit hashes + line numbers. The validator agent will check these.

---

## Entry 1 — Plates 0 + 1 + 2 shipped (2026-06-05, Session 83)

**Status:** Plates 0, 1, 2 all complete and committed. Plates 3, 4, 5 queued; Plate 3 is BLOCKED on two open Matt decisions.

**Commits:**
- `5bc168b4d` — Plate 0 (deterministic normalizer + Aerys merge) + Plate 1 (doc foundation)
- `03442d0a0` — Plate 2 (event-coverage + traversal probe + D2 RESOLVED) + continue prompts for Plates 3/4/5
- `a7046ec58` — SESSION-LOG closing summary
- `8427d6e74` — Session 83 endsession (worklog + todos + session-details + drop superseded continue prompt)

### Plate 0 — Head-direction normalizer + Aerys merge

**Design doc claim** (§3 D4, §4 glossary, §7.0):
- Build a deterministic, no-LLM normalizer that flips edges where `asserted_relation`/`hint_raw` self-witnesses the inversion bug.
- Repoint phantom `aerys-targaryen` slug to canonical `aerys-ii-targaryen`.
- Stage only — DO NOT touch `graph/edges/edges.jsonl`.
- Design doc predicted "232 unordered pairs carry the same edge type in both directions" as evidence of widespread inversion.

**What actually shipped:**
- `scripts/edge-direction-normalizer.py` — flagged **10 flips** out of 3,811 (kept 3,800, flagged 1 mutual-kill).
- `scripts/aerys-slug-merge.py` — repointed **3 edges** (design predicted 2) from `aerys-targaryen` → `aerys-ii-targaryen`.
- Output staged at `working/edge-modeling/normalizer-candidates.jsonl`, `normalizer-diff.md`, `flagged-for-review.jsonl`, `aerys-merge-candidates.jsonl`, `aerys-merge-summary.md`.
- **`graph/edges/edges.jsonl` was NOT modified.** ✓

**Surprises / divergences from the design:**
- **The "232 bidirectional pairs" framing was overstated.** After applying edge-type-aware filtering (excluding EXPERIENCE/STATE types like PRISONER_OF, SERVES, RESENTS — where passive phrases like "captured by" are semantic, not inversion-cues), only 10 unambiguous flips remained. The 232 bidirectional pairs are largely genuine reciprocal relations, NOT subject-leakage inversions.
- **3 Aerys edges, not 2.** Minor — design said 2 (`KILLS` + 1 SERVES), actual is 3 (`KILLS` + 2 SERVES, jaime + lord-redwyne).

**Adjustments to the plan:**
- None to the structure — the normalizer and the merge both produced staging output exactly as specified. The "smaller-than-expected scope" surprise doesn't change the plan; it just rightsizes expectations for Plate 5's merge diff.

**Open Matt questions from Plate 0:**
- The 1 flagged row (`donal-noye ↔ mag-mar-tun-doh-weg KILLS`, mutual kill at Battle of Castle Black) — leave as one edge, split into two, or use a MUTUAL_KILL convention? Defer to Plate 5 merge sign-off.

### Plate 1 — Doc foundation (head rule + schema + validator)

**Design doc claim** (§3 D1, §7.1):
- Insert head rule into `.claude/agents/mechanical-extractor.md` after the `## Relationships Observed` table (line ~178).
- Add optional role sub-bullets to `## Events & Actions` (line ~134). VERIFY parser at `scripts/stage4-pass1-extra-tables.py:522` reads only the first line.
- Add `AGENT_IN` + `VICTIM_IN` to `reference/architecture.md` (Person/House → Event). Widen `COMMANDS_IN` to cover orderer/instigator role. Vocab 163 → 165.
- Add target-type contract to `scripts/stage4-type-contract-validator.py`.
- DO NOT trigger a Pass-1 rerun.

**What actually shipped:**
- `.claude/agents/mechanical-extractor.md` line 188 — head rule inserted. Line 136 — optional role sub-bullets (Agent/Patient/Instrument/Location/Instigator/Outcome).
- Parser at `scripts/stage4-pass1-extra-tables.py:521-537` VERIFIED safe (matches `^\d+\.\s+`, silently skips indented sub-bullets).
- `reference/architecture.md` line 237 — `AGENT_IN`. Line 238 — `VICTIM_IN`. Line 214 — `COMMANDS_IN` widened. Line 240 — `WIELDED_IN` instrument-role note. Line 551 — vocab 163 → 165 with Session 83 annotation.
- `scripts/stage4-type-contract-validator.py` — Contract 10 added: AGENT_IN/VICTIM_IN with non-event target → DROP; with no-node target → FLAG; with `events` target → KEEP.
- No Pass-1 rerun. ✓

**Surprises / divergences:** None. All insertion sites matched the design's predicted locations.

**Adjustments to the plan:** None.

**Open Matt questions from Plate 1:** None.

### Plate 2 — Verify gating unknowns + resolve D2

**Design doc claim** (§3 D2, D3, §7.2):
- 2a: count Pass-1 events with-node vs. needs-mint.
- 2b: confirm whether `graph-query.py` traverses person→event→person.
- Resolve D2: (a) Replace (pure 2-hop hub) or (c) Project (materialized agent→patient dyad).
- §3 D3 predicted: "Bran's defenestration, Tywin's privy death, and the Purple Wedding poisoning have NO hub today."

**What actually shipped:**
- `scripts/plate2-event-coverage.py` — coverage join over 344 extraction files. Results in `working/edge-modeling/plate2-event-coverage.{md,json}`:
  - 8,384 total Pass-1 event entries.
  - 8,317 distinct titles.
  - **1 exact slug-match.**
  - 8,316 distinct titles needing mint (floor).
  - Only 38 of 371 event nodes (10%) have any Pass-1 chapter linkage.
- `working/edge-modeling/plate2-graphquery-traversal.md` — VERDICT: `--path` at `scripts/graph-query.py:794-809` traverses person→event→person transparently via untyped 2-hop bridge intersection. Live probes through `winterfell` (location) and `house-frey` confirmed.
- **D2 RESOLVED = (a) Replace.** Recorded as `## D2 RESOLVED` subsection in `working/edge-modeling/edge-modeling-reification-design.md` §3.

**Surprises / divergences from the design:**
- **§3 D3 is partially WRONG.** Verified against repo:
  - Bran's defenestration → NO node, NEEDS MINTING ✓ (design correct)
  - Tywin's privy death → `assassination-of-tywin-lannister` **EXISTS** (design wrong) — what's missing is chapter linkage.
  - Purple Wedding → `purple-wedding` **EXISTS** (design wrong) — what's missing is chapter linkage.
- **Coverage join is much weaker than expected.** Only 1 of 8,317 distinct titles exact-matched a slug. 90% of event nodes have no Pass-1 chapter linkage (chapter→event index was built from the Wars & Conflicts column, which only catches historical event names, not narrative beats).
- **Pass-1 events are overwhelmingly narrative micro-beats** ("Departure at daybreak", "Bran traverses rooftops"), not named historical events. A naive reify-all approach would mint ~8,300 micro-event nodes.

**Adjustments to the plan:**
- The §3 D3 correction is logged in `SESSION-LOG.md` and `worklog.md`, but the design doc itself has NOT been amended (kept as historical lineage record). A future session may want to add a `D3 RE-EXAMINED` note in §3.
- Plate 3 needs a **chapter-rebind sub-step** for existing event nodes (not just a mint step) — this was not in the original design.
- **NEW open Matt question Q1** surfaced: reify-all vs reify-selective? Documented inline in Plate 3 continue prompt's PRE-WORK DECISION block.
- **NEW open Matt question Q2** surfaced: fuzzy reuse vs slug-floor mint? Same location.

**Open Matt questions from Plate 2 (BLOCK Plate 3):**
- **Q1 — Reify-all vs reify-selective?** Reify-all = ~8,300 hubs. Reify-selective (kill/death/attack/poisoning/wedding/betrayal/capture trigger list) targets the underdetermination cases the project actually wants to fix. Recommend selective.
- **Q2 — Fuzzy reuse vs slug-floor mint?** Exact-match found 1 hit. A fuzzy-title pass (e.g. `tywin-privy-death` ≈ `assassination-of-tywin-lannister`) would likely lift existing-node reuse from 1 to several hundred. Decide: run the fuzzy pass, or accept slug-floor and mint freely.

### Carry-forward state (for the next plate's validator check)

- **`graph/edges/edges.jsonl` is BYTE-IDENTICAL to its S82 state.** 3,811 rows, no flips applied, no Aerys merge applied. Plate 5 is the only step that will modify this file.
- **`graph/nodes/` UNTOUCHED.** No event nodes minted; the phantom `aerys-targaryen.node.md` still exists at `graph/nodes/characters/`.
- **All Plate 0 outputs are staged at `working/edge-modeling/`** (not merged): normalizer-candidates.jsonl, normalizer-diff.md, flagged-for-review.jsonl, aerys-merge-candidates.jsonl, aerys-merge-summary.md.
- **D2 = (a) Replace** is binding for Plate 3 — do NOT emit materialized agent→patient dyads.
- **Vocab is locked at 165 edge types** including `AGENT_IN`/`VICTIM_IN`. Do NOT add more reification types (e.g. `INSTRUMENT_IN`) — `WIELDED_IN` covers instrument, `COMMANDS_IN` covers orderer/instigator.

### Validator checks (what a fresh agent should verify for this entry)

A validator agent should run / read these to confirm the claims above:

```bash
# Plate 0 — confirm staging outputs exist; confirm edges.jsonl untouched
ls working/edge-modeling/normalizer-candidates.jsonl working/edge-modeling/aerys-merge-candidates.jsonl
wc -l graph/edges/edges.jsonl   # should be 3811
grep -c '"flipped"' working/edge-modeling/normalizer-candidates.jsonl   # should be 10

# Plate 1 — confirm doc edits landed and vocab count is 165
grep -n "Head rule" .claude/agents/mechanical-extractor.md          # expect ~L188
grep -n "AGENT_IN\|VICTIM_IN" reference/architecture.md             # expect L237-238
grep -n "165" reference/architecture.md                              # expect L551
grep -n "_ROLE_EVENT_TYPES" scripts/stage4-type-contract-validator.py # expect Contract 10

# Plate 1 — confirm parser-safety claim
sed -n '521,537p' scripts/stage4-pass1-extra-tables.py | head -20

# Plate 2 — confirm D2 RESOLVED is in the design doc
grep -n "D2 RESOLVED" working/edge-modeling/edge-modeling-reification-design.md

# Plate 2 — confirm spot-check claims (these should ALL be true)
ls graph/nodes/events/assassination-of-tywin-lannister.node.md   # EXISTS
ls graph/nodes/events/purple-wedding.node.md                     # EXISTS
ls graph/nodes/events/brans-defenestration.node.md 2>&1 | grep -q "No such"  # SHOULD NOT EXIST

# Plate 2 — graph-query traversal claim
grep -n "def cmd_path" scripts/graph-query.py                    # should land near L794
```

**Validator should flag drift if:**
- `graph/edges/edges.jsonl` row count ≠ 3811 (means an unauthorized merge happened).
- Any file under `graph/nodes/events/` has a `created_in_session: 83` or similar (means Plate 3 minted nodes without Matt's Q1/Q2 answer).
- Vocab count in `architecture.md` ≠ 165 (means schema drifted without an entry below).
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-3-backfill.md` is missing or has been resolved without an answer to Q1/Q2.
- `working/edge-modeling/edge-modeling-reification-design.md` §3 still contains the unmarked claim "the Purple Wedding poisoning and Tywin's privy death have no hub" without a `D3 RE-EXAMINED` note (this is technical debt; flag it but don't escalate).

---

## Entry 2 — Parallel-session note: Q1/Q2 resolved, D8 added, Plate 2.5 + Plate 3 in flight (observed 2026-06-07)

**Source / authorship.** This entry was written by the orchestrator session that owns Entry 1, observing uncommitted work in another Claude Code session that ran in parallel. **The other session owns its own worklog entry + commits.** This entry exists only so the validator log doesn't fall silent during the parallel window.

**Status:** Plate 3 is no longer BLOCKED. Q1 + Q2 + a new Q1b/D8 refinement have all been answered (by Matt, in the other window). Plate 2.5 (event-node inventory) was added as a new precondition and shipped. Plate 3 has produced minibatch + revalidation + full staging outputs. None of it is committed at the time of this entry. Validator should expect a forthcoming "Entry 3" from the parallel session that records the actual Plate 3 outcome with commit hashes.

### Design-doc changes observed (uncommitted in `working/edge-modeling/edge-modeling-reification-design.md`)

- **D3 RE-EXAMINED note** added (L78-95) — directly in §3 D3, correcting the original "no hub" claim for Purple Wedding + Tywin's privy death. This closes the technical-debt flag from Entry 1's last validator-check bullet. Future validators: D3 RE-EXAMINED is in place; no further escalation.
- **D8 — Reify on n-ary STRUCTURE, not event TYPE** added (L97-114). Sharpens Q1 and the §2 disposition table. The trigger to reify is now structural (instigator ≠ executor, multiple killers/victims, or a named set-piece other edges reference), NOT event-type membership. **Clean dyads stay as direct typed edges** (`KILLS source→target`, direction-fixed by Plate 0). Empirical claim in D8: 0 of 102 current KILLS rows carry an instigator signal → almost all are clean dyads (Jaime/Aerys archetype). Reify-target collapses to "~100–200 distinct n-ary events, most of which already have nodes."
- **D2 RESOLVED + D3 RE-EXAMINED notes** were anchored at L129+ during the parallel work (line refs from `grep -n "^### D"`).

### Continue-prompt changes observed (uncommitted in `progress/continue-prompts/2026-06-05-edge-modeling-plate-3-backfill.md`)

- **Q1 — RESOLVED: reify-SELECTIVE** with explicit trigger families (death-violence / weddings & ceremonies / sieges / conspiracies / captures-imprisonments / guest-right violations). Plain travel / observations / dialogue beats are NOT reified.
- **Q2 — RESOLVED: fuzzy reuse pass BEFORE minting**, gated by confidence:
  - Auto-rebind on exact alias match or normalized-slug equality.
  - Queue for review on merely-plausible fuzzy hits (do NOT auto-rebind).
  - Mint only when no candidate clears the bar.
- **Q1b/D8 REFINEMENT** added — reify on n-ary structure (see design doc D8). Clean dyads inside the trigger families are NOT reified.
- **New precondition: Plate 2.5 Event-Node Inventory at `working/edge-modeling/event-node-reuse-lookup.json`** (normalized-title/alias → existing event-node slug). Reuse-before-mint is mandatory.

### New artifacts observed (all UNCOMMITTED at time of this entry)

**Scripts:**
- `scripts/event-node-inventory.py` — builds Plate 2.5 reuse lookup.
- `scripts/edge-reify-backfill.py` — Plate 3 backfill pipeline.
- `scripts/stage-drift-reclassify.py` — appears to be a drift-detection / reclassify pass (purpose to be confirmed by parallel session's worklog entry).
- `scripts/stage-event-collision-merge.py` — looks like an event-node de-collision step (also TBC).

**Plate 2.5 outputs:**
- `working/edge-modeling/event-node-inventory.md`
- `working/edge-modeling/event-node-reuse-lookup.json` (1,092 lines)

**Plate 3 outputs (staging only; canonical `graph/` untouched as far as I've checked):**
- `working/edge-modeling/plate3-minibatch/` — minibatch run: `role-edges-staging.jsonl`, `minted-event-nodes/`, `skipped-clean-dyads.jsonl`, `supersede-candidates.jsonl`, `hub-review-queue.jsonl`, `plate3-minibatch-summary.{md,json}`, `minibatch-config.json`.
- `working/edge-modeling/plate3-revalidation/` — revalidation pass on the same minibatch (same shape).
- `working/edge-modeling/plate3-full/` — full run: `hub-review-queue.jsonl`, `minted-event-nodes/`.
- `working/edge-modeling/plate3-smoke-red-wedding.jsonl` + `plate3-smoke-red-wedding-meta.json` — the Red Wedding smoke test called out in the design doc.

**Audit apparatus (NEW — the parallel session institutionalized the validator pattern):**
- `working/runbooks/edge-modeling-audit-loop.md` — standing procedure: each plate produces a Reporter log entry (Sonnet, in-repo agent) judged by an Auditor (Opus, FRESH session). Reporter gathers facts; Auditor renders ON-COURSE / DRIFT / NO-GO. **Separation of duties is the point.** This formalizes what this validator log was meant to do.
- `working/edge-modeling/audit-repo-reporter-prompt.md` — Reporter agent prompt.
- `working/edge-modeling/audit-alignment-auditor-prompt.md` — Auditor agent prompt.
- `working/edge-modeling/cleanup-decisions-resolved.md` — appears to capture the Q1/Q2/D8 decisions and any cleanup downstream.
- `working/edge-modeling/drift-reclassify-{candidates.jsonl,summary.md}` — drift-reclassify outputs (purpose TBC).
- `working/edge-modeling/collision-merge-{candidates.jsonl,summary.md}` — event-node collision-merge outputs (purpose TBC).

### Surprises / risks for the validator

- **The audit-loop runbook (`working/runbooks/edge-modeling-audit-loop.md`) supersedes this validator log's role in part.** Going forward, plate audits flow through the Reporter→Auditor pipeline into `SESSION-LOG.md`, not directly here. This validator log remains the **Matt-facing index**: each plate completion still gets an entry here, but the entry can cite the SESSION-LOG audit instead of re-deriving facts. Future appenders: keep this file as the high-level "are we on plan?" digest, not the audit-of-record.
- **Untracked: drift-reclassify + collision-merge scripts/outputs are NOT named in the design doc as plates.** They look like derived cleanup work the parallel session bolted on. The next validator pass should confirm they don't constitute scope creep — verify against `cleanup-decisions-resolved.md`.
- **`graph/edges/edges.jsonl` and `graph/nodes/events/` still appear untouched** at the time of this entry — Plate 3 stayed in `working/edge-modeling/plate3-*/`. Future validators must re-confirm.
- **Two scratch files (`scratch-do-not-delete.txt`, `scratch-stage4-considerations-haiku.txt`) show as deleted** in `git status`. These are Matt's private notes per memory `feedback_scratch_is_private` — the parallel session was authorized to do this OR Matt deleted them himself; **do not investigate, do not surface to Matt unless he asks.** Flagged here only so a future drift-checker doesn't read the deletions as project state.

### Validator checks for Entry 2 (what a fresh agent should run)

```bash
# Confirm the design-doc edits actually landed
grep -n "D3 RE-EXAMINED\|D8 — Reify on n-ary STRUCTURE" working/edge-modeling/edge-modeling-reification-design.md

# Confirm Plate 2.5 reuse lookup exists and is non-trivial
wc -l working/edge-modeling/event-node-reuse-lookup.json   # expect ~1092

# Confirm Plate 3 staging exists; confirm canonical graph still untouched
ls working/edge-modeling/plate3-minibatch/ working/edge-modeling/plate3-revalidation/ working/edge-modeling/plate3-full/
wc -l graph/edges/edges.jsonl   # should STILL be 3811
ls graph/nodes/events/*.node.md | wc -l   # compare against baseline (was 371)

# Confirm audit-loop runbook + agent prompts exist
ls working/runbooks/edge-modeling-audit-loop.md
ls working/edge-modeling/audit-repo-reporter-prompt.md working/edge-modeling/audit-alignment-auditor-prompt.md

# Confirm Entry 3 is forthcoming — if the parallel session committed Plate 3, there should be
# a corresponding Entry 3 here. If commits land for Plate 3 work but no Entry 3 lands, flag it.
git log --oneline --all -- working/edge-modeling/plate3-minibatch/ | head -5
```

**Validator should flag drift in this entry's terms if:**
- The parallel session's commits land but no Entry 3 is appended here within one session-cycle.
- `graph/edges/edges.jsonl` changed row count without a Plate 5 / merge entry.
- `working/edge-modeling/edge-modeling-reification-design.md` D8 was edited (not just appended-to) after this entry.
- `event-node-reuse-lookup.json` is missing or empty (means Plate 2.5 was rolled back).
- The audit-loop runbook is referenced but the Reporter→Auditor pipeline never actually ran for Plate 3 (means the institutionalized audit is bypassed).
