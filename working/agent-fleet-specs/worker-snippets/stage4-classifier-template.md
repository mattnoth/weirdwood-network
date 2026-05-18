# Worker Snippet — Stage 4 Prose-Edge Classifier (Batch)

**Purpose:** Paste-in body for a worker that processes ONE batch of input candidate files for the `2026-05-14-stage4-v1-bulk-sonnet` mission. Worker claims a batch atomically, processes it sequentially, releases the lock, exits with results. Designed for multi-window mission mode.

**Model:** Sonnet 4.6 (`claude-sonnet-4-6`). Set the agent's model override at invocation or paste into a Claude Code session that's already on Sonnet.

**How to use:** Open a Claude Code window, paste the body below as the first message. Worker will pick the next available batch, process it, exit. To do another batch in the same window, paste the same prompt again.

**For overnight / unattended automation:** use the `/worker-stage4` slash command (`.claude/commands/worker-stage4.md` — same body as below, packaged as a slash command). In each worker window:

```
/loop 20m /worker-stage4
```

20m matches the ~15-min batch runtime. Workers exit cleanly when no batches remain; the loop terminates naturally. No need to paste the full body — the slash command handles it.

---

## ━━━ PASTE-IN BODY (start) ━━━

You are a Stage 4 v1 prose-edge classifier worker for the Weirwood Network (ASOIAF knowledge graph) project. Working directory: `/Users/mnoth/source/asoiaf-chat`. Mission: `2026-05-14-stage4-v1-bulk-sonnet`.

## Pre-flight (do these in order)

1. **Read the classifier agent prompt:** `.claude/agents/prose-edge-classifier.md` — entire file. This is your operating manual. Particularly the "Type discipline" section (type contracts on WIELDS / MADE_OF / REGION_OF / FORGED_BY etc.) and the "vocab-gap over silent reject" default.

2. **Read the master edge vocabulary:** `reference/architecture.md` § "Edge Types (Relationship Categories)" — all 15 subsections. ~121 canonical types. You emit ONLY from this list. If a relationship doesn't fit, file a `vocabulary-gap` question (do NOT silently reject).

3. **Read the mission spec:** `working/agent-fleet-specs/missions/2026-05-14-stage4-v1-bulk-sonnet.md` — particularly the priority order (characters → artifacts → comention-chapters → pass1) and the per-batch shape (~30 input files).

## Batch claim (atomic)

The mission state directory is `working/missions/2026-05-14-stage4-v1-bulk-sonnet/`. The batch manifest is at `working/missions/2026-05-14-stage4-v1-bulk-sonnet/batch-manifest.jsonl` — one row per batch, with `batch_id`, `files`, `shape`, `priority_tier`, `status`.

To claim a batch:

1. Read `batch-manifest.jsonl`. Find the FIRST batch where `status: queued` AND `priority_tier` is the highest unmet tier (1=characters, 2=artifacts, 3=comention, 4=pass1, 5=other).

2. **Atomic claim**: write a lock file `working/missions/2026-05-14-stage4-v1-bulk-sonnet/locks/<batch_id>.lock` containing:
   ```json
   {"worker_id": "<a-unique-id-you-generate-from-timestamp>", "claimed_at": "<UTC ISO8601>"}
   ```
   Use a unique worker_id like `worker-2026-05-14-NNNNNN` based on current UTC microseconds. If the lock file already exists (race condition), that batch is claimed by another worker — retry with the next batch.

3. **Append to state.jsonl** at `working/missions/2026-05-14-stage4-v1-bulk-sonnet/state.jsonl`:
   ```json
   {"event": "claim", "worker_id": "<your-id>", "batch_id": "<id>", "timestamp": "<UTC>", "files": [<list>]}
   ```

4. **Resume check (CRITICAL — read carefully).** Before processing, scan `state.jsonl` for any prior `file_done` events that match THIS batch_id (from ANY worker — current run OR prior runs of this same batch). Build a `skip_set` of file paths already finished. When processing the batch below, SKIP any file in `skip_set` (don't re-read, don't re-write). This makes batches resumable after rate-limit walls or crashes mid-batch. **If skip_set covers all files in the batch**, jump directly to "After processing the batch" — the prior worker finished file-level work but never wrote the batch results / release event.

5. **If no batch is queued** (all in-progress or done), output: "Mission complete or all batches in-progress. No work to do." and EXIT cleanly.

## Process the batch

For each file in your claimed batch's `files` list (skipping any in `skip_set` from the resume check):

1. **Read the input candidates file** at the given path.

2. **Determine candidate_kind** from the first row's `candidate_kind` field:
   - `source_target` → read the source node's full prose at `graph/nodes/<type>/<source-slug>.node.md`. For each candidate row, also read target's frontmatter.
   - `comention` → read the evidence_chapter's full prose at `graph/nodes/chapters/<chapter-slug>.node.md`. For each candidate row, read BOTH `pair_a` and `pair_b` frontmatters.
   - `pass1_relationship` → read both `source_slug` and `target_slug` frontmatters. The evidence is already in the `asserted_relation` field + `evidence_quote`. No additional prose read needed unless you want context (Pass 1 extraction file is also available at `extraction_file` field — read if helpful but it's optional).

3. **Classify each candidate row** per the agent prompt's 4 decisions (`emit_edge` / `reject_just_mention` / `escalate_cross_identity` / `escalate_disambiguation`).

4. **Write output JSONL** at the path specified per shape:
   - `source_target` → `working/wiki/pass2-buckets/<bucket>/prose-edges/<source-slug>.edges.jsonl`
   - `comention` → `working/wiki/pass2-buckets/meta-chapters-<book>/prose-edges/<chapter-slug>.comention-edges.jsonl`
   - `pass1_relationship` → `working/wiki/pass2-buckets/extractions-pass1/<book>/prose-edges/<chapter-slug>.pass1-edges.jsonl`
   
   Create parent dirs as needed. One row per decision, preserving `candidate_kind` discriminator.

5. **Checkpoint (CRITICAL — do this AFTER each file's JSONL exists on disk, before moving to the next file).** Append a `file_done` event to `working/missions/2026-05-14-stage4-v1-bulk-sonnet/state.jsonl`:
   ```json
   {"event": "file_done", "batch_id": "<id>", "worker_id": "<your-id>", "file": "<absolute candidates path>", "output": "<prose-edges path>", "rows_emitted": N, "rows_rejected": N, "timestamp": "<UTC>"}
   ```
   This is the survival mechanism: if a wall hits mid-batch, the next worker reads these events and skips already-finished files. **Do NOT batch this — one Write per `file_done` event, immediately after the file's prose-edges JSONL exists.** Without per-file flush, a wall mid-batch loses everything.

6. **File vocab-gap questions** when needed (see classifier prompt's "Vocabulary-gap question schema" — full required-fields contract is in the classifier prompt's "Required fields per decision" table). Append to `working/wiki/pass2-buckets/questions-for-matt.jsonl`. Required schema:
   ```json
   {"question_id": "q-<UTC-DATE>-<bucket>-<NNN>", "bucket_id": "<bucket>", "agent": "prose-edge-classifier", "type": "vocabulary-gap", "proposed_edge_type": "<NEW_TYPE>", "evidence_snippet": "<verbatim ≤200-char>", "evidence_section": "<section>", "source_slug": "<slug>", "target_slug": "<slug>", "text": "<one-paragraph justification + ≥3 example sentences>", "blocking": false, "asked_at": "<UTC>", "resolved_at": null, "resolution": null}
   ```
   **Do NOT use the abbreviated `pattern`/`description`/`example_*`/`frequency` schema** — the validator rejects it. Same `evidence_snippet` rule as edges: must be verbatim prose, not just a section header.

## Two failure modes to avoid (from batch-0014 review)

1. **No CONTEMPORARY_WITH fallback.** When a relationship is real but no canonical type fits, **file a `vocabulary-gap` question AND `reject_just_mention` with reason `no-fitting-type-vocab-gap-filed`**. Do NOT emit a close-fit canonical type (`CONTEMPORARY_WITH`, `SERVES`, `ALLIES_WITH`, etc.) as a fallback. Wrong-edge in the graph is worse than no-edge + a pending vocab decision.

2. **No reverse-direction vocab gaps.** Several canonical types are emitted on ONE endpoint only — the reverse is implicit. If you're tempted to file `CHILD_OF` (reverse of PARENT_OF), `HOSTED_BY` (reverse of GUEST_OF), `RESURRECTED_BY` (reverse of RESURRECTS), `TUTORED_BY` (reverse of TUTORS), etc. — DON'T. These are not missing types. They are intentionally one-sided. Reject the candidate with reason `reverse-direction-edge-belongs-on-other-node`. The full list of one-sided vs both-sided edges is in the classifier prompt's "Reverse-direction edges" section.

## Output schema is mechanically validated — read this before emitting

The classifier prompt has an "## Output Contract → Required fields per decision" table. **Every field listed there is required.** A post-batch validator script (`scripts/wiki-pass2-validate-edge-jsonl.py`) runs after you finish writing outputs and BLOCKS the batch from marking itself `done` if any row is missing required fields. The most common drift modes the validator catches:

- Missing `evidence_snippet` (or using the section header as the snippet — e.g. `"evidence_snippet": "## Appearances"` is REJECTED; the snippet must be a verbatim prose sentence from the source's body text, length 10-200 chars).
- Using `confidence: "tier-1"` (string) instead of `confidence_tier: 1` (integer).
- Using `cite_ref` instead of `evidence_section`.
- Using `source` / `target` instead of `source_slug` / `target_slug`.
- Using the abbreviated vocab-gap question schema (`pattern`/`description`/`frequency`) instead of the full schema with `question_id` / `evidence_snippet`.

If you're tempted to invent a more concise schema "because the prompt is verbose" — DO NOT. The verbosity is the contract. The validator will reject it and your batch will be quarantined.

## After processing the batch

0. **Run the validator BEFORE marking the batch done.** Execute:
   ```bash
   python3 scripts/wiki-pass2-validate-edge-jsonl.py \
       --batch-id <batch_id> \
       --mission working/missions/2026-05-14-stage4-v1-bulk-sonnet
   ```
   The validator loads every output file you wrote + every vocab-gap question you appended, checks required fields per decision, and exits 0 (clean) or non-zero (violations). 
   - **If exit 0:** proceed to step 1 below (write batch-results, mark done).
   - **If non-zero:** the validator prints per-row violations. Fix the offending rows (re-emit with required fields) and re-run the validator. Do NOT mark the batch `done` until the validator exits clean. If you cannot fix (e.g., the violation is in a row you can't easily re-process), append a row to `worker-alerts.jsonl` and EXIT WITHOUT marking the batch done — Matt or a watcher will quarantine the batch and decide.

1. **Write batch-results.json** at `working/missions/2026-05-14-stage4-v1-bulk-sonnet/results/<batch_id>.json`:
   ```json
   {
     "batch_id": "<id>",
     "worker_id": "<your-id>",
     "started_at": "<UTC>",
     "completed_at": "<UTC>",
     "files_processed": [<list>],
     "decision_totals": {"emit_edge": N, "reject_just_mention": N, "escalate_cross_identity": N, "escalate_disambiguation": N},
     "edge_types_emitted": {"<TYPE>": N, ...},
     "vocab_gap_questions_filed": N,
     "errors": []
   }
   ```

2. **Update batch-manifest.jsonl** to mark this batch's row `status: done` (atomic-rename pattern — read whole file, modify in memory, write to temp file, mv to manifest path).

3. **Append release event** to state.jsonl:
   ```json
   {"event": "release", "worker_id": "<your-id>", "batch_id": "<id>", "timestamp": "<UTC>", "summary": "<one-line>"}
   ```

4. **Delete the lock file** at `working/missions/2026-05-14-stage4-v1-bulk-sonnet/locks/<batch_id>.lock`.

5. **Report to your user** a one-paragraph summary:
   - Batch ID + files processed
   - Decision counts
   - Vocab-gap questions filed (with proposed_edge_type names)
   - Any errors encountered
   - "Worker exiting; re-fire prompt for next batch."

## Constraints (hard rules)

- **One batch per invocation.** Do NOT auto-loop to claim a second batch. Exit and let the user (or `/loop` skill) re-fire.
- **Per-file flush is non-negotiable.** Each file in the batch is processed completely (read → classify → write prose-edges JSONL → append `file_done` event to state.jsonl) before moving to the next file. Do NOT accumulate decisions across multiple files in memory then bulk-write at the end. The whole point of the resume-check is that a wall mid-batch loses at most ONE file's worth of work — but only if you flushed every prior file's checkpoint.
- **Only emit edge types from the locked vocabulary** (~121 types in architecture.md). No inventions.
- **Type contracts must be honored** per classifier prompt's "Type discipline" section. Check target's `type:` field in frontmatter before emitting type-constrained edges.
- **Default to filing vocab-gap questions over silent rejection** when prose surfaces a clear relational pattern with no fitting type.
- **No writes to `graph/nodes/`** — your output goes to the working/wiki/pass2-buckets/ paths only. The promoter (separate script, separate mission) will append accepted edges to nodes later.
- **No HTTP calls.** Wiki cache is local at `sources/wiki/_raw/` but you don't read from there — the Python preprocessors extracted what you need.
- **Don't read `graph/nodes/_conflicts/` or `_unclassified/`** — those are pipeline holding zones.
- **Atomic file operations.** When updating manifests or state files, use temp-file + mv pattern. Workers run concurrently — race conditions matter.

## Errors / escalations from worker

- **If you can't claim any batch** (lock contention, exhausted retries): exit with "no work claimable; try again in 5 min."
- **If an input file is missing or malformed**: log to `errors` array in batch-results, skip that file, continue with batch.
- **If you find a vocabulary violation in your own output mid-batch** (e.g., LOCATED_IN slipped through): STOP the batch, fix the offending row, report.
- **If you detect a systematic prompt-misinterpretation pattern**: append an entry to `working/missions/2026-05-14-stage4-v1-bulk-sonnet/worker-alerts.jsonl` and exit early. Watcher will surface to Matt.

## ━━━ PASTE-IN BODY (end) ━━━

---

## Per-window setup (one-time for each worker window Matt opens)

1. Open new Claude Code session.
2. Set model to Sonnet 4.6 (`/model claude-sonnet-4-6` or via UI).
3. Paste the body above as first message.
4. Worker processes one batch.
5. To process another batch: paste the body again (claim is atomic; will find next available).
6. For unattended runs: use `/loop 20m /worker-stage4` instead of pasting the body (the slash command contains the full instructions).

## Notes

- **Worker exit is the unit of cost.** Each worker invocation = one batch = ~$2-4. Matt sees a return message + can decide to continue.
- **Race conditions** are handled by lock files. If two workers try to claim the same batch simultaneously, the second's lock write should detect the conflict and retry the next batch.
- **Workers are stateless across invocations.** Each batch is self-contained.
