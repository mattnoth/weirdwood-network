# Session 18 — Wiki Pass 2 Build Cleanup: Close the Triage Seam

**Date:** 2026-04-26
**Mode:** Cleanup + script extension. Came in cold to "last session lost it's mind" — meaning the prior unstructured build session left scripts on disk that didn't fully match the runbook.

## Goal

Get `weirwood wiki triage` / `status` / `run` working end-to-end against the local wiki cache, without making architectural changes. Don't fetch externally. Verify all scripts run. Categorize the 17,657 cached pages.

## What was on disk coming in

Three new uncommitted scripts from a prior unwritten-up session:
- `scripts/wiki-pass2-categorize.py` (921 lines) — page-level categorization
- `scripts/wiki-pass2-coherence.py` (431 lines) — graph/nodes/ coherence checker
- `scripts/wiki-pass2.sh` (1423 lines) — full orchestration launcher

Plus output: `working/wiki-parsed/page-categories.jsonl` (17,657 rows, ~30% classified into real buckets, ~70% into `singletons-unknown`).

Three new runbooks: `wiki-pass2-orchestration.md`, `wiki-pass2-orchestration-review.md`, `archive-wiki-full-crawl-DONE.md`.

The runbook + wiki-pass2.sh expected `scripts/wiki-pass2-triage.py` (with `--accept` to commit per-bucket manifests). What got built was `wiki-pass2-categorize.py` — does the page-level work but stops before bucket-manifest emission. `wiki-pass2.sh triage` dead-ended on "ERROR: scripts/wiki-pass2-triage.py not found." The seam was open.

## Audit (Stage 1)

Verified all scripts syntax-clean. Smoke-tested:
- `wiki-infobox-parser.py --page Eddard_Stark` → produces full record with cite_refs, books, relationships
- `wiki-pass2-categorize.py --page Eddard_Stark` → routes to `characters-house-stark` correctly
- `wiki-pass2-coherence.py` → "0 nodes to check" (graph/nodes/ empty, expected)
- `wiki-pass2.sh status` → "no triage manifest found" (correct: no manifests yet)
- `wiki-pass2.sh triage` → ERROR (the seam)

No test suite exists. Smoke tests substitute.

Re-ran `wiki-pass2-categorize.py` end-to-end: 17,657 rows, 437 buckets, 12,328 (69.8%) in `singletons-unknown`. Found that `--limit N` clobbers the full output (script opens `OUTPUT_FILE` in `"w"` mode); regenerated full file. Of the 12,328 singletons: 12,266 have ZERO populated signals — these are stubs/redirects/calendar pages without infoboxes. The 5,279 infobox-rich pages do get real bucket assignments.

The 80% tripwire fails (only 30% classified non-singleton). This is a threshold/data-shape mismatch, not a script bug — the runbook's whole point of triage is to filter stubs.

## Decision: extend categorize → triage (close the seam)

Matt asked "yes" to extending the script. I renamed `wiki-pass2-categorize.py` → `wiki-pass2-triage.py` (matching what `wiki-pass2.sh` calls) and added Stages 2 + 3:

**Stage 2 — bucket grouping + draft outputs:**
- Group rows by `primary_bucket`
- Split buckets >30 members alphabetically (`characters-house-stark` → `characters-house-stark-{a-b, b-h, h-q, r-w}`)
- Isolate pages with `byte_size > 600KB` as bucket-of-one with `chunk_strategy: section-by-section` (per runbook §1.3)
- Apply `tier_default` regex table from runbook §1.4 (theory→tier-4, religion/magic→tier-2, character/house/location→tier-1, fallback tier-2)
- Apply `processing_tier` (core vs. secondary): nine houses (Stark, Lannister, Targaryen, Baratheon, Greyjoy, Tully, Arryn, Tyrell, Martell) + nine regions + direwolves → core; everything else secondary
- Skip `singletons-unknown`, `tv-only-skip`, `disambiguation`
- Emit `working/wiki-parsed/triage-manifest.jsonl` (membership canonical) and `draft-buckets.jsonl` (review view)

**Stage 3 — `--accept` writes per-bucket manifests:**
- For each non-skip bucket, write `working/wiki-pass2/<bucket>/manifest.json` with the schema from runbook §5.2: `bucket_id`, `tier`, `tier_default`, `fingerprint` (sha256 of input_pages + prompt_version + chunk_strategy), `prompt_version`, `chunk_strategy`, `oversized`, `input_pages`, `expected_nodes`, `status` (preserved from existing manifest if any, else `pending`), `started_at`, `completed_at`, `validation_report`
- Idempotent: re-running with `--accept` rewrites membership but preserves status fields the launcher owns

Result of accept run: **507 buckets created**, 35 core / 472 secondary, 2 oversized.

## Bug found: pipefail + find/grep

`wiki-pass2.sh status` printed "no triage manifest found" even with 507 manifests on disk. Traced via `bash -x`: the dir-existence check `[[ ! -d "$WIKI_STATE_DIR" ]] || ! find "$WIKI_STATE_DIR" -name "manifest.json" -maxdepth 2 2>/dev/null | grep -q .` interacts with `set -euo pipefail`. When `grep -q` finds a match it exits 0 immediately, `find` gets SIGPIPE (status 141), pipefail propagates that, the `!` inverts to "not zero" → enters the if-block → prints the wrong message.

Fix (3 occurrences): replace `! find ... | grep -q .` with `[[ -z "$(find ... -print -quit 2>/dev/null)" ]]`. `-print -quit` makes find exit on first match, no pipe, no SIGPIPE.

After fix, `weirwood wiki status` produces the expected table.

## Known issue surfaced (NOT fixed this session)

`direwolves` bucket includes "Arya Stark" alongside Ghost/Lady/Nymeria/Summer/Shaggydog/Grey Wind/(missing Robb's Grey Wind is there too). The direwolf override matches on alias, and Arya's wiki aliases include "Nymeria" (her direwolf's name). This is existing behavior of `infer_buckets()`, not introduced by this session. Flagged in todos for the smoke-test session — Arya should land in `characters-house-stark-a-b`, not `direwolves`.

Direwolves' `tier_default` is `tier-2` (no regex match). Arguably should be tier-1 (named Tier-1 characters per architecture). Left as default until the smoke test reveals if it matters.

## What's actually broken before agents can launch

The user's stated next intent is "spin off agents at once similar to book parser" — i.e., `weirwood wiki core 2 3` to launch parallel iTerm tabs.

**Blocker:** `.claude/agents/wiki-ingester.md` is a 31-line **stub** with TODOs only. No schema, no node template, no extraction rules. The launcher's `cmd_run` will invoke `claude -p` with a thin "read your spec, process bucket_input.json, write to tmp/" wrapper — but the spec referenced is the stub. Output would be unstructured.

The runbook's agreed sequence (Session 17) is:
1. ✅ Track B (wiki-infobox-parser)
2. ✅ Build session: scripts + manifests (this session, completing what the lost session started)
3. **fresh-agent script-review session** — read scripts cold, find bugs (e.g., the Arya-in-direwolves bug)
4. **wiki-ingester prompt session** — write the actual prompt
5. **smoke-test direwolves bucket** — first real agent run
6. Scale beyond smoke

The user's "spin off agents at once" jumps from step 2 directly to step 6. Honest read: cannot launch productively until step 4 is done. The next-prompt at end of this session lays that out.

## Files touched

- `scripts/wiki-pass2-categorize.py` → renamed to `scripts/wiki-pass2-triage.py`
- `scripts/wiki-pass2-triage.py` — extended with Stage 2 (bucket grouping/split) + Stage 3 (--accept manifest emission); added `import hashlib`; added `TIER_DEFAULT_RULES`, `CORE_TIER_RULES`, `SKIP_BUCKETS`, `BUCKET_SPLIT_THRESHOLD`, `OVERSIZED_PAGE_BYTES`, `PROMPT_VERSION` constants; added `classify_tier_default`, `classify_processing_tier`, `split_oversized_bucket`, `build_buckets`, `write_triage_outputs`, `bucket_fingerprint`, `expected_node_filename`, `write_bucket_manifests` functions; wired into `main()`
- `scripts/wiki-pass2.sh` — fixed 3× pipefail/SIGPIPE bug in dir-existence checks (lines 471, 845, 946)
- `working/wiki-parsed/page-categories.jsonl` — regenerated (17,657 rows; was clobbered earlier by `--limit` smoke test)
- `working/wiki-parsed/triage-manifest.jsonl` — NEW (17,657 rows, page → bucket)
- `working/wiki-parsed/draft-buckets.jsonl` — NEW (961 rows, post-split bucket summary)
- `working/wiki-pass2/<bucket>/manifest.json` — NEW (507 manifest files)

## Surprises / process notes

- **The lost session wasn't catastrophic.** Three scripts on disk are mostly correct — they just leave the seam at the boundary between page-level and bucket-level, plus a pipefail bug. Cleanup was extension, not rewrite.
- **The categorize-vs-triage distinction was real but small.** The lost-session agent wrote `categorize.py` because the page-level work IS most of the script. The bucket emission is ~150 lines added on top. Renaming + extending was the right move.
- **70% singletons-unknown is fine.** It looks like a failure (tripwire fails at 80%), but the data shape is correct: 12,378 of 17,657 wiki pages don't have infoboxes (stubs, redirects, calendar pages, lists). The runbook explicitly says triage filters these out. The tripwire threshold needs a calibration in a future session — should probably be measured against `pages-with-infoboxes`, not `total-pages`.
- **`--limit N` is destructive.** The script opens output in `"w"` mode and writes only the limited rows. Calling `--limit` after a full run silently corrupts the output file. Non-blocking but worth noting in a future cleanup.
- **wiki-pass2.sh references runbook sections that depend on its own outputs.** The sh script and runbook are tightly coupled — pipefail bug aside, the sh script is well-structured, and the cmd_run / cmd_status / cmd_check / cmd_unstick / cmd_reset / cmd_questions all share the same bucket directory contract. The build session got the sh skeleton right.
- **`/endsession` requires explicit permission per memory.** User explicitly asked for it this turn — invoking is appropriate.

## What's next

Per the user's stated intent: launch parallel wiki agents. But honest sequence is:

1. **Fresh-agent script review** — read `wiki-pass2-triage.py` (this session's extension) + `wiki-pass2.sh` (last session's build) cold, surface bugs (Arya-in-direwolves, tripwire calibration, etc.)
2. **Write the wiki-ingester prompt** — currently a 31-line stub. Needs schema, node template, extraction rules, validator-aware output.
3. **Smoke test on direwolves bucket** (after the Arya bug is fixed). Single bucket, single agent invocation, verify the cmd_run pipeline (compose bucket_input.json → claude -p → validator → atomic rename).
4. **THEN** scale via `weirwood wiki core <terminals> <waves>`.

Continue prompt at `progress/continue-prompts/2026-04-26-wiki-pass2-launch-prep.md` covers steps 1-3 in one self-contained prompt.
