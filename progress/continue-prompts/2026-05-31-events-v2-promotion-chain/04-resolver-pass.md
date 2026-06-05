# Step 4 — Resolver pass: title-person disambiguation on v2 candidate

> **Recommended model:** Sonnet 4.6 (mechanical; the resolver does the work). Opus only if a new collision class appears that needs design judgment.
>
> **Trust `worklog.md` over this prompt** if they disagree.

## Prerequisite

- **Step 3 status file** shows `proceed_to_step_4: yes` with Matt's sign-off.
- `_v2-refine/edges-v2-refined.jsonl` exists.

## Why this step exists

v1.3 (Session 72) ran title-person disambiguation and caught **12+ bad edges** where ship/artifact/title nodes named after a person were catching the person's references (e.g., `lord-tywin` the dromond, `princess-myrcella` the artifact, `khal-jhaqo` the title vs the khal). The events-haiku output uses the same candidate generator (`stage4-pass1-edge-candidates.py`) which already threads through `stage4_name_resolver.py` — but the `resolved-title-person` rung needs to be re-validated against the v2 candidate because new context patterns (especially TRAVELS-WITH chains) can introduce collisions the original resolver didn't see.

## What to do

1. **Read** `scripts/stage4_name_resolver.py` and the v1.3 README section in `graph/edges/README.md` to understand the existing resolver behavior and the v1.3 fix list.

2. **Audit v2-refined for known v1.3 collision slugs.** Run a check across `edges-v2-refined.jsonl`:
   - List every distinct `source_slug` and `target_slug` whose slug matches the v1.3 fix list (`lord-tywin`, `queen-cersei`, `lord-renly`, `princess-myrcella`, `lady-olenna`, `khal-jhaqo`, the `lady-marya` ship, the `CAPTAIN_OF`-misuse pattern from `hallis-mollen`/`areo-hotah`).
   - Confirm the v2-refined rows have these resolved correctly (i.e., the character slug, not the title-prefixed artifact). If any survived, the resolver isn't running on events-haiku rows — investigate.

3. **Look for NEW title-person collisions.** Cross-reference v2 slugs with `graph/nodes/` to find every node whose name starts with a title (`lord-*`, `lady-*`, `prince-*`, `princess-*`, `queen-*`, `king-*`, `khal-*`, `ser-*`, `maester-*`) AND has a corresponding non-character node sharing the slug or stem.
   - Write the candidates to `_v2-refine/title-person-candidates.md`.
   - For each candidate, decide: remap → character / keep as artifact / drop the edge / surface to Matt.

4. **Look for new collision classes** that v1.3 didn't see. Specifically:
   - `CAPTAIN_OF` target-not-character is a contract from v1.3 — re-validate it on v2.
   - `MEMBER_OF` target-not-faction (could surface from events with "X joined the brotherhood" style hints typing to a person).
   - `WIELDS` target-not-artifact (events sometimes describe wielding a person figuratively).
   - Any contract-passed but slug-stuffed edges should be flagged here, not at step 3.

5. **Apply the resolver remaps to v2.** Output:
   - `_v2-refine/edges-v2-resolved.jsonl` (post-resolver)
   - `_v2-refine/resolver-remap-log.md` (what changed, with before/after slugs)
   - `_v2-refine/edges-v2-resolver-dropped.jsonl` (anything dropped vs. remapped)

6. **Surface to Matt**: remap count, drop count, new collision classes (if any), the title-person-candidates list with the decision per row. **Wait for sign-off** before step 5.

## Gates

- **Go to step 5**: remap count is bounded (single digits expected, given the candidate generator already runs the resolver); no new collision class introduces >10 edges; Matt approves the candidate list.
- **No-go**: a new collision class introduces a structural issue (e.g., a whole edge-type pattern is mis-resolving). Surface and pause.

## Deliverables for step 5

- `_v2-refine/edges-v2-resolved.jsonl` (this is the input to step 5)
- `_v2-refine/resolver-remap-log.md`
- `_v2-refine/title-person-candidates.md`
- `_v2-refine/edges-v2-resolver-dropped.jsonl`
- `step-04-status.md`

## Hard rules

- **Do NOT modify** the v1.3 resolver behavior in `stage4_name_resolver.py` without a separate Matt design conversation — this step is about *applying* the resolver, not changing it.
- **Do NOT delete** any v2-refined rows; remapped rows update the slug, dropped rows go to `edges-v2-resolver-dropped.jsonl`.
- **Do NOT promote** v2-resolved to `graph/` — that's step 6.
