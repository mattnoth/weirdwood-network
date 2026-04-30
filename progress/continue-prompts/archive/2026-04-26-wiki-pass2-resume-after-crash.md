# Continue Prompt — Resume Wiki Pass 2 Triage Disambiguation (post-crash)

**Created:** 2026-04-26 (mid-session, Claude Code crashed before re-emit could run)
**Supersedes (do not delete):** `2026-04-26-wiki-pass2-triage-disambiguation.md` — that prompt is the authoritative spec; this one is a thin "where I left off" overlay.

## What's already done in the prior session

T1 + P1 code is **landed and verified** but **not committed**. The 6 promoted direwolf nodes have **not** been archived yet, and the bucket has **not** been re-emitted yet.

### Diffs on disk (uncommitted)

- `scripts/wiki-pass2-triage.py`
  - `DIREWOLF_NAMES` → split into `DIREWOLF_BARE_NAMES` + `DIREWOLF_PAGE_OVERRIDES` + `DIREWOLF_PAGE_NAMES` (computed)
  - `DIREWOLF_PAGE_OVERRIDES = {"Nymeria": "Nymeria (direwolf)"}`
  - Rule 2 in `classify_page` now matches `DIREWOLF_PAGE_NAMES` (disambiguated set)
  - `write_bucket_manifests` flips `status: complete` → `status: version-stale` when fingerprint changes
- `scripts/wiki-pass2.sh`
  - `version-stale` added to runnable statuses in `cmd_run` and `cmd_launch`
  - `append_stats_row` extended with `questions_filed,conflicts_filed,pass1_contradictions_filed` (3 trailing args, default 0)
  - `ensure_stats_csv` writes the 3 new columns into the header
  - `cmd_run` snapshots `working/wiki-pass2/{questions-for-matt,conflicts,pass1-contradictions}.jsonl` line counts before each bucket and computes deltas after — passed to stats row + per-bucket `OK:` line + wave summary footer
  - New `cmd_reset_bucket` (invoked via `reset --bucket <id>`): finds nodes by `expected_nodes` + by `bucket_id` frontmatter scan, moves them to `graph/archives/wiki-pass2-<bucket>-<ts>/nodes/...`, wipes `tmp/`, flips manifest to `pending`
  - Usage block + dispatcher updated for `reset --bucket`
  - `jsonl_linecount` helper added
- `working/extraction-stats/wiki-pass2-stats-core-v1.csv`
  - Header + existing direwolves row migrated to include the 3 new columns (existing row: `q=1,c=0,p=0` — the open Nymeria question)

### Triage already re-run with `--accept`

```sh
python3 scripts/wiki-pass2-triage.py --accept
```

Result: only `working/wiki-pass2/direwolves/manifest.json` flipped to `version-stale` (verified by grep — no other manifest changed status). New manifest has:
- `fingerprint: f9b4904db6acca8d504b3916c83ef1b5e0c3dbb11f6d1009102e15c1b47bd153` (was `699410...`)
- `input_pages` includes `"Nymeria (direwolf)"` (was `"Nymeria"`)
- `expected_nodes` includes `"nymeria-direwolf.node.md"` (was `"nymeria.node.md"`)

A `reset --bucket direwolves --dry-run` confirmed the 6 nodes the reset would archive: ghost, grey-wind, lady, nymeria-direwolf, shaggydog, summer.

### Tasks completed in prior session

- T1 fix in triage — done
- P1 summary surfacing in launcher — done
- Triage `--accept` re-run — done

### Tasks remaining (this session)

1. `./scripts/wiki-pass2.sh reset --bucket direwolves` (no `--dry-run`) — archives the 6 nodes, wipes tmp/, flips manifest to pending
2. `weirwood wiki run core --bucket direwolves` — re-emit from clean bundle. Expected ~$1.15, ~5 min, 6 nodes promoted. Watch the new wave summary for `Questions filed: 0`.
3. Verify `working/wiki-pass2/direwolves/bucket_input.json` has `page: "Nymeria (direwolf)"` and `raw_html_path: sources/wiki/_raw/Nymeria_(direwolf).json` for the Nymeria entry
4. Verify validator + coherence are green
5. Append `resolved_at` + `resolution` to the existing question in `working/wiki-pass2/questions-for-matt.jsonl` (q-2026-04-26-001)
6. Update `worklog.md` Session 21 entry, archive the original continue prompt + this one (DoD met)
7. Ask Matt before scaling to remaining 41 core buckets — that's the second cost envelope (~$30-60 ballpark)

## Read first (in this order)

1. `progress/continue-prompts/2026-04-26-wiki-pass2-triage-disambiguation.md` — full spec for T1/P1/re-emit/scale
2. This file (overlay of what's already done)
3. `worklog.md` Session 20
4. `working/wiki-pass2/questions-for-matt.jsonl` — the open question that should resolve cleanly
5. `working/wiki-pass2/direwolves/manifest.json` — confirm the version-stale state is still on disk

## Context recovery checks before doing anything

```sh
# 1. Confirm code edits survived
grep -n DIREWOLF_PAGE_OVERRIDES scripts/wiki-pass2-triage.py
grep -n cmd_reset_bucket scripts/wiki-pass2.sh
grep -n questions_filed scripts/wiki-pass2.sh
head -1 working/extraction-stats/wiki-pass2-stats-core-v1.csv

# 2. Confirm direwolves manifest is version-stale with the new fingerprint
cat working/wiki-pass2/direwolves/manifest.json | python3 -m json.tool | head -25

# 3. Confirm the 6 nodes are still on disk (reset hasn't run yet)
ls graph/nodes/characters/
```

If any check fails, the prior session's work was lost — re-run starting from the original continue prompt's "What to do" §1.

## Out of scope this session
Same as the original continue prompt — don't scale to secondary, don't run extractions without explicit Matt confirmation.
