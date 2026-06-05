# Step 3 — Type-contract validation on v2 candidate

> **Recommended model:** Sonnet 4.6 (mechanical contract-checking). The existing v1.2 refinement script does the heavy lifting — this step extends or re-runs it. Opus only if the contract surface needs design judgment.
>
> **Trust `worklog.md` over this prompt** if they disagree.

## Prerequisite

- **Step 2 status file** at `step-02-status.md` shows `proceed_to_step_3: yes` with Matt's sign-off.
- `_formalized/edges-v2-candidate.jsonl` exists and matches the formalize-report-v2.md counts.

## Why this step exists

v1.2 (Session 72) ran type-contract validation on v1 and caught **17 bad edges** the original merge missed (e.g., COMMANDS targeting an artifact, MOTIVATES from a character source). The new EVENTS-HAIKU source introduces edge types not heavily represented in v1 (TRAVELS_TO, TRAVELS_WITH, LOCATED_AT, REVEALS_TO, DREAMS_OF, etc.), so the contract surface needs widening.

## What to do

1. **Read** `scripts/stage4-refine-v1-edges.py` (the v1.2 producer) to understand the contract framework. Read `graph/edges/README.md` §v1.2 for the contract-failure classes it caught.

2. **Audit the v2 candidate's edge-type coverage against the contract map.** Specifically:
   - List every distinct `edge_type` in `edges-v2-candidate.jsonl`.
   - Cross-reference with the contract map in `stage4-refine-v1-edges.py`.
   - **Identify edge types with NO contract row** — write them to `working/wiki/pass2-buckets/pass1-derived/_v2-refine/missing-contracts.md`.

3. **For each missing-contract edge type, propose a contract.** The pattern from v1.2:
   - `TRAVELS_TO`: source = character, target = place ✓
   - `TRAVELS_WITH`: source = character, target = character ✓
   - `LOCATED_AT`: source = character | artifact, target = place ✓
   - `REVEALS_TO`: source = character, target = character ✓
   - `DREAMS_OF`: source = character, target = character | place | artifact | concept ✓
   - `ATTACKS`: source = character | faction, target = character | faction | place ✓
   - `SEEKS`: source = character, target = character | artifact | place | concept ✓
   - `DISTRUSTS` / `TRUSTS` / `LOVES` / `HATES` / `RESPECTS` / `RESENTS` / `FEARS` / `MOURNS`: source = character, target = character ✓
   - `MEMBER_OF`: source = character, target = faction | organization ✓
   - `RESCUES`: source = character, target = character ✓
   - `RULES` / `APPOINTS`: source = character, target = place | character | title ✓
   - (Add more as discovered; the script's existing target-category checks will catch type mismatches.)
   - **Surface the proposed contract additions to Matt** before applying them — vocabulary is locked, but contract semantics are a design decision.

4. **Run the contract validator** on the v2 candidate, outputting:
   - `_v2-refine/edges-v2-refined.jsonl` (passes contracts)
   - `_v2-refine/edges-v2-dropped.jsonl` (failed contracts; preserved for inspection)
   - `_v2-refine/edges-v2-retyped.jsonl` (retypes like v1.2's RULES→COMMANDS-when-target-is-character, if any apply)
   - `_v2-refine/v2-refinement-report.md` (drop/retype counts by edge type)

5. **Quote-relevance soft-flags.** The v1.2 pipeline also generated `_qr_warning` soft-flags on 1,944 rows for quote-relevance review. Apply the same scan to the new events-haiku rows specifically (the spine/tail rows were already scanned). Write the annotated candidate to `_v2-refine/edges-v2-refined-annotated.jsonl`; the committed graph layer keeps the clean schema (advisory `_`-fields stripped before promotion in step 6).

6. **Surface to Matt**: drop count by edge-type, retype count by edge-type, quote-relevance warning count, and any genuinely surprising contract failures (e.g., events-haiku TRAVELS_TO landing on a character — would suggest a typing error). **Wait for sign-off** before step 4.

## Gates

- **Go to step 4**: drop count is in proportion to v1.2's (v1.2 dropped 17/3,842 = 0.44%; v2 dropping >1% is a red flag warranting investigation, not a blanket block); no edge type drops >20% of its rows; Matt approves.
- **No-go**: a contract is wrong, or events-haiku introduces a class of error v1 didn't have; surface and pause.

## Deliverables for step 4

- `_v2-refine/edges-v2-refined.jsonl`
- `_v2-refine/edges-v2-refined-annotated.jsonl`
- `_v2-refine/edges-v2-dropped.jsonl`
- `_v2-refine/edges-v2-retyped.jsonl`
- `_v2-refine/v2-refinement-report.md`
- `_v2-refine/missing-contracts.md` (with the proposed-and-approved additions)
- `step-03-status.md`

## Hard rules

- **Do NOT modify** `graph/edges/edges.jsonl` or v1's `_formalized/` artifacts.
- **Do NOT delete** dropped rows — they go to `edges-v2-dropped.jsonl` for inspection and possible re-typing later.
- **Vocabulary is locked.** Contract additions are about *which categories of slug* can fill source/target, not about adding new edge_type strings.
