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

4. **Resume check (CRITICAL — read this carefully).** Before processing, scan `state.jsonl` for any prior `file_done` events that match THIS batch_id (from any worker — current OR prior runs). Build a `skip_set` of file paths already finished. When processing the batch below, you will SKIP any file in `skip_set` (don't re-read, don't re-write). This makes batches resumable after rate-limit walls or crashes mid-batch. **If skip_set covers all files**, jump directly to "After processing the batch" — the prior worker did all the file-level work but never wrote the batch results / release event.

5. **If no batch is queued** (all in-progress or done), output: "Mission complete or all batches in-progress. No work to do." and EXIT cleanly.

## Process the batch

For each file in your claimed batch's `files` list (skipping any in `skip_set` from the resume check above):

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

5. **Checkpoint (CRITICAL — do this AFTER each file's JSONL is written, before moving to the next file).** Append a `file_done` event to `working/missions/2026-05-14-stage4-v1-bulk-sonnet/state.jsonl`:
   ```json
   {"event": "file_done", "batch_id": "<id>", "worker_id": "<your-id>", "file": "<absolute candidates path>", "output": "<prose-edges path>", "rows_emitted": N, "rows_rejected": N, "timestamp": "<UTC>"}
   ```
   This is the survival mechanism: if a wall hits mid-batch, the next worker resumes by reading these events. **Do NOT batch this — flush per file.** One Write tool call per `file_done` event, immediately after the file's prose-edges JSONL exists on disk.

6. **File vocab-gap questions** when needed (see classifier prompt's protocol). Append to `working/wiki/pass2-buckets/questions-for-matt.jsonl`. Use schema:
   ```json
   {"question_id": "q-<UTC-DATE>-<bucket>-<NNN>", "bucket_id": "<bucket>", "agent": "prose-edge-classifier", "type": "vocabulary-gap", "text": "...", "context": {"proposed_edge_type": "...", "examples": [...]}, "blocking": false, "asked_at": "<UTC>", "resolved_at": null, "resolution": null}
   ```

## After processing the batch

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

5. **Report** a one-paragraph summary:
   - Batch ID + files processed
   - Decision counts
   - Vocab-gap questions filed (with proposed_edge_type names)
   - Any errors encountered

## Constraints (hard rules)

- **One batch per invocation.** Do NOT auto-loop to claim a second batch. Exit and let `/loop` re-fire.
- **Per-file flush is non-negotiable.** Each file in the batch is processed completely (read → classify → write prose-edges JSONL → append `file_done` event) before moving to the next file. Do NOT accumulate decisions across multiple files in memory then bulk-write at the end. The whole point of the resume-check is that a wall mid-batch loses at most ONE file's worth of work.
- **Only emit edge types from the locked vocabulary** (~121 types in architecture.md). No inventions.
- **Type contracts must be honored** per classifier prompt's "Type discipline" section. Check target's `type:` field in frontmatter before emitting type-constrained edges.
- **Default to filing vocab-gap questions over silent rejection** when prose surfaces a clear relational pattern with no fitting type.
- **No writes to `graph/nodes/`** — output goes to working/wiki/pass2-buckets/ paths only.
- **No HTTP calls.** All data is local.
- **Don't read `graph/nodes/_conflicts/` or `_unclassified/`** — pipeline holding zones.
- **Atomic file operations.** Use temp-file + mv pattern for manifests and state files.

## Errors / escalations

- **If you can't claim any batch** (lock contention, exhausted retries): exit with "no work claimable; try again in 5 min."
- **If an input file is missing or malformed**: log to `errors` array in batch-results, skip that file, continue.
- **If you find a vocabulary violation in your own output mid-batch**: STOP, fix the offending row, report.
- **If you detect a systematic prompt-misinterpretation pattern**: append to `working/missions/2026-05-14-stage4-v1-bulk-sonnet/worker-alerts.jsonl` and exit early.
