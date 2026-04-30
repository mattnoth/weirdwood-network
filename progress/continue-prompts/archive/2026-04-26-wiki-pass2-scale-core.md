# Continue Prompt — Wiki Pass 2: Scale to Core Tier (28 pending buckets)

**Created:** 2026-04-26 end-of-Session-21. **Updated:** 2026-04-27 end-of-Session-22.
**Goal:** Drain the remaining 28 core buckets after Session 22's rate-limit cutoff. 9 buckets complete (~136 promoted nodes); ~$25 burned so far.
**Cost envelope (remaining):** ~$20-40 ballpark for the rest. Matt has explicitly authorized launching at session start — no need to re-confirm.

## Where this fits in the chain

This is **Stage 1 of a 3-stage chain** — see `working/runbooks/wiki-pass2-tier-handoff.md` for the full spec.

- **Stage 1 (this session):** Run core. **Multi-pass is the norm.** Session 22 ran 2 passes before hitting the 7-day Anthropic cap; this session resumes after the reset window. Stage 1 is "done" when (a) every core bucket is `complete` and (b) every question filed during the run is `resolved_at != null`. Re-runs across reset windows are normal — not a sign of failure.
- **Stage 2 (next session, fresh Claude):** Cold review of core output. New session, no carry-over context.
- **Stage 3 (after stage 2 clears):** Launch tier-secondary (472 buckets).

## State at session start — what Session 22 left behind

```sh
# Expect: core complete: 9, core pending: 21, core fail: 7, secondary pending: 472
python3 -c "
import json, glob, collections
status = collections.Counter()
for f in glob.glob('working/wiki-pass2/*/manifest.json'):
    d=json.load(open(f))
    if d['tier']=='core': status[d['status']] += 1
    elif d['status']!='complete': status['secondary_pending'] += 1
print(dict(status))"

# Expect: 88 character nodes, 1 faction (Dragonkeepers), 47 house nodes — 136 total
find graph/nodes/ -mindepth 2 -name '*.node.md' -not -path '*_conflicts*' | awk -F/ '{print $3}' | sort | uniq -c

# Expect: 27 conflict files (26 from stark-h-q, 1 from stark-q-w)
ls graph/nodes/_conflicts/ | wc -l

# Expect: 3 questions, all 3 resolved
weirwood wiki questions
```

If counts disagree, stop and figure out why before launching. The 7 `fail` buckets are rate-limit skips with stale tmp/ — they MUST be wiped before relaunch (Session 22 did this manually; re-do if needed):

```sh
python3 <<'EOF'
import json, glob, os, shutil
for f in glob.glob('working/wiki-pass2/*/manifest.json'):
    d = json.load(open(f))
    if d['tier'] == 'core' and d['status'] == 'fail':
        bdir = f.rsplit('/', 1)[0]
        if os.path.isdir(f'{bdir}/tmp'): shutil.rmtree(f'{bdir}/tmp')
        if os.path.exists(f'{bdir}/validator-report.json'): os.remove(f'{bdir}/validator-report.json')
        print(f'  wiped {d["bucket_id"]}')
EOF
```

## Read first

1. **This file.** All Session 22 context lives here so you don't have to chase it.
2. `wiki-logs-` at repo root — raw iTerm tab output from Session 22 (875 lines, ~29KB). Validation reports per bucket, agent self-corrections, etc. Reference, don't re-read every line.
3. `worklog.md` Session 22 entry — concise summary of what landed.
4. `progress/scratch-notes.md` — paren-slug fix notes (Session 22 entry).
5. `working/wiki-pass2/questions-for-matt.jsonl` — 3 entries, all resolved.

## What changed in Session 22 (don't re-do)

- **Agent prompt fixes (already landed in `.claude/agents/wiki-ingester.md`):**
  - **Slug rule rewritten** (line 62): now lowercases, hyphenates spaces, then strips every non-`[a-z0-9-]` char (handles parentheses, periods, etc.) and collapses runs of `-`. Validator is canonical.
  - **`first_available` override rule:** if the agent has positive evidence the parser value is wrong (e.g., cite_refs span earlier books), set field to `"always available"` and file a question; otherwise default to `null`. Sansa Stark's node was patched manually as the seed example.
- **Bucketing finding (Matt accepted the waste, option `a`):** Multi-letter character buckets in same house overlap. `stark-h-p ∩ stark-h-q = 26/27 pages` confirmed. Same pattern likely for other multi-letter character buckets (stark-{a-b, b-h, q-w, r-w}, greyjoy-{g-r, s-w}, martell-{a-m, m-t}, tyrell-{a-l}). The launcher's collision detection routes duplicates to `graph/nodes/_conflicts/` — data integrity is fine; cost is wasted $$ on duplicate runs. **Triage-script bug deferred** to a post-Stage-1 cleanup pass.
- **Question ID collision:** parallel agents all generated `q-2026-04-26-001`. JSONL `bucket_id` is the source of truth; clean up IDs at end of Stage 1 if needed.
- **CSV `questions_filed` / `conflicts_filed` race:** snapshot delta in `cmd_run` counts other tabs' parallel JSONL writes. JSONL `bucket_id` is canonical.
- **rateLimitType is `seven_day`** (Pro Max plan, limit:100). The 5-hour daily reset Matt sees doesn't apply. Only the weekly reset clears this.

## How to launch

```sh
# Status first — read the wave plan
weirwood wiki core

# Launch — 3 terminals × 3 waves (covers up to 9 waves of 4 buckets each = 36 buckets max)
# WAVE_SIZE=4. With 28 launchable buckets = 7 waves. T1=[1,2,3], T2=[4,5,6], T3=[7].
weirwood wiki core 3 3
```

**Critical:** Verify iTerm2 has at least one window before launching. The launcher's osascript fails with "Can't get current window" if iTerm has 0 windows. If needed:
```sh
osascript -e 'tell application "iTerm2" to activate' -e 'tell application "iTerm2" to create window with default profile'
```

**Don't oversubscribe** — the 7-day cap is per-account. If all 3 tabs hit `skip-rate-limit` immediately, the cap is still active. Don't relaunch repeatedly; each round burns $3-4 in failed first-bucket attempts.

## Multi-pass expectation (revised)

Session 22 demonstrated the rate-limit pattern is severe:
- First successful pass landed 8 of 9 buckets before all 3 tabs were rate-limited mid-bucket.
- Two retry attempts within ~30 min both failed immediately on first bucket per tab.
- The cap is 7-day. Don't re-launch until clearly past the reset window.

Plan: launch once. If rate-limited, end session, write next-session continue prompt with updated counts.

## Diagnostic recipes

```sh
# Per-bucket conflicts (which buckets are duplicating into _conflicts/)
python3 -c "
import json, collections
counts = collections.Counter()
with open('working/wiki-pass2/conflicts.jsonl') as f:
    for l in f:
        if l.strip(): counts[json.loads(l)['bucket_id']] += 1
print(dict(counts))"

# Per-bucket questions
python3 -c "
import json, collections
c = collections.Counter()
with open('working/wiki-pass2/questions-for-matt.jsonl') as f:
    for l in f:
        if l.strip(): c[json.loads(l)['bucket_id']] += 1
print(dict(c))"

# Recent CSV rows
tail -10 working/extraction-stats/wiki-pass2-stats-core-v1.csv

# Inspect rate-limit JSON of last failed bucket
ls -t /tmp/wiki-pass2-*.json | head -1 | xargs grep -oE '"rateLimitType":"[^"]*"|"limit":[0-9]+|"resetsAt":"[^"]*"'
```

## Known risk areas (carry-over)

- **Slug-set validator gap** — validator now rejects bad slugs (paren fix), but does NOT enforce slug-set equality with `expected_nodes`. Silent renames still possible. Direwolves exercised this; treat new disambiguation surprises as data, not bugs.
- **Coherence script (`weirwood wiki check`)** — likely tier-filter bug; defer.
- **Question ID collision** — needs script-side ID generator (parallel-safe). Defer.

## DoD (Stage 1 → Stage 2 handoff) — unchanged

- All 37 core buckets show `status: complete` in their manifests
- Every entry in `working/wiki-pass2/questions-for-matt.jsonl` has `resolved_at != null`
- Validator passed on every promoted bucket (`validator-report.json#passed: true`)
- `working/extraction-stats/wiki-pass2-stats-core-v1.csv` has one final row per bucket (rate-limited skips can stay as historical rows)
- Worklog Session NN entry written for the final Stage-1 session
- **Stage-2 handoff prompt written** at `progress/continue-prompts/<date>-wiki-pass2-core-review.md` per the template in `working/runbooks/wiki-pass2-tier-handoff.md` §"Stage 2 prompt template"
- This prompt (Stage 1) archived to `progress/continue-prompts/archive/`

## Out of scope

- **Do not** launch tier-secondary in this session.
- **Do not** retroactively fix the 508 not-yet-run manifests' `validation_report` field.
- **Do not** rebuild the validator to enforce slug-set equality without explicit Matt direction.
- **Do not** fix the bucket-overlap triage script in this session — Matt accepted the waste; defer to post-Stage-1.
- **Do not** write the Stage-2 review prompt with carry-over context — write only the handoff.
