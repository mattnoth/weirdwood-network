# Continue Prompt — Wiki Pass 2: Pre-Secondary Remediation

**Created:** 2026-04-27 end-of-Stage-2 review (Session 24)
**Goal:** Fix 3 systemic issues found in Stage-2 sampling that would compound across 472 secondary-tier buckets. After fixes land, write a fresh Stage-2 review prompt; do **NOT** auto-proceed to Stage 3.
**Cost envelope:** Local script + small targeted re-runs (≤5 buckets if any). No new full-tier extraction in this remediation pass.

## Where this fits in the chain

Stage 2 → remediation branch → fresh Stage 2 → Stage 3. See `working/runbooks/wiki-pass2-tier-handoff.md` §"Remediation branch".

## Findings from Stage-2 sample (Session 24)

Sample: 18 nodes, stratified across high-traffic POVs (Eddard, Jon Snow, Tyrion, Cersei, Jaime, Arya, Sansa, Varys), disambiguation cases (Aegon Young Griff, Brandon variants), bucket-overlap territory (Quent from stark-h-q, Lyanna from stark-h-p), the direwolves canary (Ghost, Nymeria-direwolf), question-flagged emissions (Dragonkeepers, Nymeria, Sansa), one routine house (House Arryn, House Langward).

### Issue A — `first_available` schema drift (855 nodes; 4 different shapes)

Architecture says `first_available` is a single string `{BOOK} {POV} {CHAPTER_NUMBER}` (e.g., `AGOT Bran II`). Actual emissions across the 855 core nodes:

| Shape | Count | Example node | Sample value |
|-------|-------|--------------|--------------|
| Block-object (`book:`, `chapter:`, `source:`, `pov:`) | **453** | `eddard-stark.node.md` | `book: AGOT, chapter: 1, source: cite_ref, pov: Prologue` |
| Null / empty | **239** | many | — |
| `"always available"` (Matt's positive-suspicion rule) | **69** | `house-reed.node.md` | `"always available"` |
| `"BOOK POV-X"` (matches arch spec) | **21** | `lyanna-stark.node.md` | `"AGOT Bran I"` |
| `"BOOK chN POV-X"` (extra chapter-number prefix) | **15** | `wayn-guard.node.md` | `"AGOT 37 Daenerys IV"` |
| **Field absent entirely** | **58** | `house-langward.node.md`, `kennet-maester.node.md` | (no `first_available` key) |

The block-object shape diverges from the architecture spec but is the dominant pattern. The 58 nodes with no field at all directly violate `reference/architecture.md` rule #4 ("`first_available` is architectural, not optional"). The validator does not enforce presence or shape.

**Why this blocks Stage 3:** Spoiler gating is the entire point of `first_available`. With 4 shapes plus absences, downstream queries cannot filter consistently. At 472 secondary buckets the gap multiplies.

**Proposed fix:**
1. Pick the canonical shape. Architecture spec says single-string `"AGOT Bran II"`. The block-object shape carries more information (parser source, structured chapter number), but it isn't what the spec defines. Either (a) update architecture.md to make the block-object shape canonical and update wiki-ingester prompt to emit only that, or (b) keep the spec as-is and update prompt + a one-time normalization script that flattens block-objects → strings.
2. Add validator check: `first_available` must be present, and must match either the canonical shape or `"always available"` or `null`.
3. Update the wiki-ingester agent prompt's emission template to specify the chosen shape explicitly. (Currently the prompt's flexibility around this field is the root cause of drift.)
4. Run a one-shot normalization script over all 855 core nodes after the canonical shape is chosen. This is a mechanical rewrite, not a re-extraction.

### Issue B — Silent `first_available` parser-bug propagation (unknown count, ≥2 confirmed major characters)

The track_b parser produces wrong `first_available` values for many pages (this is the root cause of 67 of the 74 filed questions — agent noticed, set to `"always available"` per Matt's Session 22 rule). But for nodes where the agent **didn't** notice the parser was wrong, the wrong value was emitted verbatim per the agent's "default null otherwise" rule.

Confirmed silent failures in sample:
- `tyrion-lannister.node.md`: `first_available: ADWD chapter 1`. Tyrion appears from AGOT chapter 1 (Tyrion I). No self-correction note. Frontmatter contradicts the body, which describes him in AGOT events.
- `varys.node.md`: `first_available: ADWD chapter 1 / pov: Prologue`. Varys appears from AGOT (warns Eddard about Cersei's plot in AGOT). No self-correction note.

These are major POV/recurring characters. If two of eight high-traffic samples show the bug, the rate among the 591 character nodes is potentially significant.

**Why this blocks Stage 3:** Silent wrong values in spoiler gating means filtered queries return content the user shouldn't see (or hide content they should). The "agent self-corrects when it notices" rule is unreliable — relying on the agent's per-page judgment doesn't scale to 472 buckets.

**Proposed fix:**
1. Build a one-shot audit script: for each node, compare `first_available.book` against the lowest-numbered cite_ref book on the source wiki page. If `first_available` is later than the lowest cite, flip to `"always available"` (the canonical positive-suspicion fallback). This is mechanical; the wiki cache has the cite_refs.
2. After the audit, re-emit the affected node frontmatters in place (no re-extraction needed). Body text is unaffected.
3. Long-term: fix the underlying track_b parser so it doesn't produce these systematically wrong values. Out of scope for this remediation but should be in the Stage-3 prompt's "tech debt" section.

### Issue C — Validator does not enforce `first_available` presence or shape

Currently `scripts/wiki-pass2-validator.py` explicitly excludes `first_available` checks from v1 scope ("first_available format/parse validation (spoiler gating deferred)" — line 35 of the script). The validator caught zero of the 58 missing-field cases.

**Why this blocks Stage 3:** Stage 1 produced 58 nodes that violate the architecture rule. Without validator enforcement, secondary will produce ~5× more (proportional to bucket count).

**Proposed fix:** Add a validator check: `first_available` must be present in frontmatter. Acceptable values: a non-empty string, `"always available"`, or a structured block with `book` field present. Anything else fails. This is a one-liner add to the validator's `check_node` function.

## What's NOT a blocker (verified independently)

- **Cost-per-bucket vs $1 projection** — the framing was misleading. Cost-per-node is **$0.111** ($95.33 / 855), better than the direwolves baseline ($0.19/node). Per-bucket cost being higher is just bucket-size scaling. Secondary projection at this rate is real but the per-node math is healthy. Do not rebudget.
- **Slug rename rate** — 0%. The validator's slug-stem check is working. The "validator gap" flagged by the launching Claude was the manifest-`expected_nodes` gap, but in practice all 855 node-files match their slugs and only 3 expected nodes are missing (the deliberately-deleted video-game houses). No silent renames.
- **Conflict mechanism** — 52 conflict files preserved data integrity from the overlapping multi-letter character buckets (`stark-h-p` ∩ `stark-h-q` = 26 duplicates was confirmed against manifests). The wasted cost is real but small and has already been paid; this isn't a remediation prereq for secondary.
- **Type override frequency** — 2 of 855 = 0.2% (Ghost human→direwolf, Dragonkeepers house→faction). Both transparently logged in Notes. Healthy.
- **Edge yield** — mean 5.83 edges/node, zero empty-edge nodes, 17% sparse (<3 edges). Sparse cases are minor characters with thin wiki pages. Healthy.
- **Bulk question resolutions** — Spot-check of 8 resolved questions confirmed they were the same parser-bug pattern with the same correct fix. Not papered over; correctly identified as a single root cause that the upstream parser bug should eventually fix. The remediation here treats it as Issue B.

## DoD for remediation session

- [ ] Decide canonical shape for `first_available` (string vs block-object). Update `reference/architecture.md` if needed so spec and emission match.
- [ ] Edit wiki-ingester agent prompt (`.claude/agents/wiki-ingester.md`) to specify the canonical shape unambiguously. Include a worked example for `"always available"` and for normal cases.
- [ ] Add validator presence + shape check to `scripts/wiki-pass2-validator.py`.
- [ ] Build and run one-shot audit script: detect nodes where `first_available.book` > earliest cite_ref book → flip to `"always available"`.
- [ ] Build and run one-shot normalization script: rewrite the 4 emitted shapes into the chosen canonical form across all 855 nodes. Idempotent. Frontmatter-only.
- [ ] Re-run validator across all 37 core buckets with the new check. Confirm 100% pass.
- [ ] Write a fresh Stage-2 review prompt at `progress/continue-prompts/2026-04-2X-wiki-pass2-core-review-v2.md` for a fresh Claude to verify the fixes hold before authorizing Stage 3.
- [ ] Archive this remediation prompt to `progress/continue-prompts/archive/`.

## Out of scope for remediation session

- Do **not** re-run the wiki-ingester agent on any bucket. All fixes are mechanical post-processing on the emitted frontmatters.
- Do **not** fix the underlying track_b parser bug. That's a separate workstream — note it in worklog as tech debt for after Pass 2.
- Do **not** delete or re-emit any of the 855 node files beyond the in-place frontmatter rewrites.
- Do **not** auto-proceed to Stage 3. Stage 3 requires a fresh Stage-2 review.

## Verification commands at session start

```sh
# Confirm state hasn't drifted
python3 -c "
import json, glob, collections
status = collections.Counter()
for f in sorted(glob.glob('working/wiki-pass2/*/manifest.json')):
    d=json.load(open(f))
    if d['tier']=='core': status[d['status']] += 1
print(dict(status))"
# Expect: {'complete': 37}

find graph/nodes/ -mindepth 2 -name '*.node.md' -not -path '*_conflicts*' | awk -F/ '{print $3}' | sort | uniq -c
# Expect: 591 characters, 261 houses, 3 factions = 855
```

## Reference files

- `reference/architecture.md` §"Spoiler Gating" — defines `first_available` format
- `working/runbooks/wiki-pass2-tier-handoff.md` §"Remediation branch"
- `scripts/wiki-pass2-validator.py` — current validator (v1 scope explicitly excludes `first_available`)
- `.claude/agents/wiki-ingester.md` — agent prompt that emits the field
- `working/wiki-pass2/questions-for-matt.jsonl` — 67 of 74 questions are this same parser bug pattern; the resolution log shows the rule that wasn't applied to Tyrion/Varys
