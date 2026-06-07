# Edge-Modeling — Repo Audit Reporter (in-repo agent prompt)

**What this is:** A reusable prompt for an **in-repo agent** that inspects the actual repository
state after a plate runs and writes a **factual** state report. It gathers ground truth; it does
NOT judge alignment (that's the Alignment Auditor's job — `audit-alignment-auditor-prompt.md`).

**How to use:** Open a session in the repo, fill the `SET THIS` block, paste the rest. Run it
**after each plate** from `working/edge-modeling/edge-modeling-reification-design.md` §7.
Pair it with the Alignment Auditor: Reporter establishes facts → Auditor judges them.

**Downloadable artifact** — self-contained; depends only on the repo + the design doc.

---

```markdown
# Edge-Modeling Repo Audit Report — Plate <N>

> **Recommended model:** Sonnet. This is mechanical repo inspection (counts, diffs, validator
>   runs). Delegate the validator passes to the existing audit agents where they fit
>   (`schema-drift-auditor`, `orphan-edge-finder`, `citation-validator`). Opus not needed.
> **Trust worklog.md over any prompt** (CLAUDE.md rule #9).
> **Role:** REPORT FACTS ONLY. Do not fix, do not judge "good/bad", do not edit the graph.
>   Surface numbers and diffs; the Alignment Auditor interprets them.

## SET THIS before running
- PLATE_JUST_RUN: <0 | 1 | 2 | 3 | 4 | 5>
- BASELINE: the frozen baseline counts (if captured) — else use the design-doc §1/§2 numbers:
  edges.jsonl = 3,811 rows (all tier-1); event nodes = 371 (304 battle/35 tournament/32 war);
  active edge vocab = 163; Haiku bulk = 1,617 rows.

## Read first
1. `working/edge-modeling/edge-modeling-reification-design.md` — full plan (esp. §3 decisions,
   §5 plate table, §7 the prompt that PLATE_JUST_RUN executed, §8 reversibility).
2. The most recent `worklog.md` entry.
3. Any prior `working/edge-modeling/audit-log.md` entries (so this report is comparable to the last).

## Gather (facts only — every number gets a source path)
1. **Canonical edge file integrity.**
   - `wc -l graph/edges/edges.jsonl` (current row count vs BASELINE 3,811).
   - Was it modified since the last report? (`git status`, `git diff --stat` on the file.)
   - **CRITICAL FLAG (report, don't fix):** if PLATE_JUST_RUN ∈ {0,1,2,3,4} and
     `edges.jsonl` changed, that violates staging discipline — only Plate 5 may write it.
     Report the exact diff.
2. **Backups.** Does `graph/edges/_regrounding/` contain a fresh backup if a write occurred?
3. **Schema / vocab.**
   - Current active edge-type count. **Run `scripts/build-edge-type-counts.py` and read the
     `canonical_type_count` field from `working/wiki/data/edge-type-counts.json` — never grep the
     literal "165" string in `architecture.md` (that's a human annotation, not a computed count;
     a stale annotation can read correct while the real count drifted).** Expected after Plate 1:
     `canonical_type_count: 165`, with `AGENT_IN` + `VICTIM_IN` both present. Report actual.
   - Are `AGENT_IN` / `VICTIM_IN` present? Is `COMMANDS_IN` widened? Did any UNEXPECTED new
     types appear (vocab sprawl — should be +2, not +4; no COMMANDER_OF / INSTRUMENT_IN)?
   - Is the validator contract (`AGENT_IN`/`VICTIM_IN` → `event.*`) present in
     `scripts/stage4-type-contract-validator.py`?
   - Is `architecture.md` in sync with `edge-qualifier-vocab.md` and the mechanical-extractor
     prompt (CLAUDE.md rule #6)?
4. **Staging inventory.** List `working/edge-modeling/` contents with row counts:
   `normalizer-candidates.jsonl`, `normalizer-diff.md`, `flagged-for-review.jsonl`,
   `aerys-merge-candidates.jsonl`, `role-edges-staging.jsonl`, `minted-event-nodes/`,
   `haiku-bulk-disposition.jsonl`. Report which exist and their sizes.
5. **Plate-specific facts** (only the one that ran):
   - **Plate 0:** # flipped / # left / # flagged by the normalizer. Confirm the design-doc §1
     inversions (`cressen KILLS melisandre`, `arya CAPTURES sandor`, `tyrion BETRAYS shae`) now
     resolve agent→patient in the candidate file. Bidirectional same-type pair count before vs
     after (BASELINE 232). Aerys: do the 2 `aerys-targaryen` edges now point at
     `aerys-ii-targaryen` in the candidate file? Is `aerys-i-targaryen` untouched?
   - **Plate 1:** diff of `mechanical-extractor.md` (head rule + sub-bullets present?),
     `architecture.md` (rows added?), validator (contract added?). Confirm NO Pass-1 rerun ran
     (extraction file mtimes unchanged).
   - **Plate 2:** does `plate2-findings.md` exist with (a) a node-exists-vs-needs-minting count
     and (b) a definitive `graph-query.py` person→event→person traversal answer? Is a
     "D2 RESOLVED (a/c)" note appended to the design doc AND worklog?
   - **Plate 3:** role-edge staging count by type; # event nodes minted; **Red Wedding dedup
     check** — is there exactly ONE red-wedding hub (not 3 across chapters)? Does the Red
     Wedding hub now have AGENT_IN/VICTIM_IN/COMMANDS_IN/LOCATED_AT edges (the §1 smoke test)?
     Did the D2 decision (replace vs project) get applied uniformly? Validator pass/fail on
     staged rows.
   - **Plate 4:** per-bucket counts for all 1,617 rows; confirm every promote-candidate was run
     through the Plate-0 normalizer (zero inverted rows in the promote set).
   - **Plate 5:** before/after edges.jsonl counts; all validators (schema-drift, orphan-edge,
     type-contract) results; per-node `## Edges` display regenerated? backup archived?
6. **Source-preservation check (CLAUDE.md hard rule).** Confirm nothing under `sources/`,
   `extractions/`, or `extractions/archives/` was deleted. Confirm any superseded edges were
   marked `superseded_by` (not removed) and any collided nodes went to `_conflicts/`.
7. **Scope check.** Did this plate's session modify any files OUTSIDE its declared
   "Files this session may modify" list (from the §7 prompt)? `git status` + compare.

## Output
Write the report to `working/edge-modeling/SESSION-LOG.md` — the project's canonical, **append-only**
validator log (one entry per plate; NEVER overwrite a prior entry; if a past entry was wrong,
append a correction). This is the file Matt and the Alignment Auditor read. Structure each entry:

```
## Repo Report — Plate <N> — <date> — commit <hash>
### Counts (with source paths)
| Metric | Baseline | Last report | Now | Δ |
...
### Staging inventory
...
### Plate-specific findings
...
### Flags (facts that look off — for the Auditor to judge)
- [ ] <flag> (path:line)
### Validator checks (bash a fresh agent can run to confirm THIS entry)
```bash
# every load-bearing claim above gets a one-line command that proves it
wc -l graph/edges/edges.jsonl            # expect 3811 (Plates 0-4)
python3 scripts/build-edge-type-counts.py && python3 -c "import json;print(json.load(open('working/wiki/data/edge-type-counts.json'))['canonical_type_count'])"  # expect 165
...
```
### Flag drift if…
- <tripwire condition> (e.g. edges.jsonl row count ≠ 3811 → unauthorized merge)
### Raw command outputs (appendix)
```

Keep it factual. Every claim cites a path. Put anything that "looks off" under **Flags** for
the Alignment Auditor — do not editorialize beyond noting the deviation. The **Validator checks**
and **Flag drift if** blocks are REQUIRED (borrowed from the S83 log convention) — they make the
entry self-verifying so a fresh agent can confirm it without re-deriving.

## Out of scope
- Fixing anything. Editing the graph. Judging whether the plate "succeeded" (that's the Auditor).
- Running the next plate.
```
