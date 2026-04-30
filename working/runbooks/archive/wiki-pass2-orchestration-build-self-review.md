# Wiki Pass 2 Build — Cold Script Review

> **Mode:** Fresh-agent read of the build session's scripts. Surfaces issues; **does not fix.** Created at the start of the launch-prep session per `progress/continue-prompts/2026-04-26-wiki-pass2-launch-prep.md` step 1.
>
> **Scope:** `scripts/wiki-pass2-triage.py` (Session 18 extension), `scripts/wiki-pass2.sh` (prior build), `scripts/wiki-pass2-coherence.py` (prior build). Sibling to `wiki-pass2-orchestration-review.md` (which reviewed the *plan*, not the implementation).
>
> **Verdict:** Several issues — three are blockers for the `direwolves` smoke test (B1, B2, B3 below). Most others are correctness or maintenance concerns the smoke test will not surface but a wider run will.

---

## Issues by Severity

Severity legend:
- **B** (Blocker) — smoke test cannot pass without fixing.
- **C** (Correctness) — script does the wrong thing in some path; likely visible at scale.
- **M** (Maintenance) — dead code, perf, or fragility; not user-visible today.
- **D** (Documentation/coupling) — runbook ↔ code drift to flag.

Each issue states: file:line(s), what, why it matters, suggested fix.

---

### B1. `compose_bucket_input` builds wiki cache paths with spaces; cache uses underscores
**File:** `scripts/wiki-pass2.sh:386-391` (inside `compose_bucket_input` PYEOF heredoc)
**What:** Path computed as `f"sources/wiki/_raw/{page}.json"` where `page` is the wiki page name from the manifest — e.g. `"Grey Wind"`, `"Eddard Stark"`. The on-disk cache uses underscores: `sources/wiki/_raw/Grey_Wind.json`.
**Verified:** `ls sources/wiki/_raw/Grey_Wind.json` → exists. `ls "sources/wiki/_raw/Grey Wind.json"` → No such file.
**Why it matters:** For every page whose name contains a space (most of them), `os.path.exists` returns False, the fallback to `_uncategorized` also fails (same naming), and `raw_html_path` is set to `None`. The agent then has `track_b_row` + `page_index_row` + `pass1_mentions` but no path to the raw HTML — degrading synthesis quality severely. **This is the most likely cause of a messy direwolves smoke test.**
**Suggested fix:** Normalize the page name before lookup: `page.replace(" ", "_")`. The page-index uses the space-form as canonical key, so keep `page` (space-form) in the bundle's `page` field, but compute `raw_html_path` from the underscored form.

### B2. Direwolf override matches on aliases; routes Arya Stark to direwolves
**File:** `scripts/wiki-pass2-triage.py:421-428`
**What:** `if page_name in DIREWOLF_NAMES or any(a in DIREWOLF_NAMES for a in aliases):` — Arya's wiki aliases include `"Nymeria"` (her direwolf's name), so she matches the override.
**Verified:** Current `working/wiki-pass2/direwolves/manifest.json` has 7 input pages with `"Arya Stark"` first.
**Why it matters:** Smoke test would emit a node for Arya routed to the wrong bucket; coherence check would later flag duplicate names (Arya gets a second node from `characters-house-stark-a-b` once that bucket runs).
**Suggested fix:** Drop the alias clause — match on page name only. Already in continue-prompt step 2.

### B3. Validator script does not exist; launcher silently promotes unvalidated output
**File:** `scripts/wiki-pass2.sh:692-718`
**What:** `if [[ -f "scripts/wiki-pass2-validator.py" ]]` — when the file is missing, sets `validation_ok=true` and prints `WARNING: scripts/wiki-pass2-validator.py not found — skipping validation`. Then proceeds to atomic-rename `tmp/*.node.md` into `graph/nodes/`.
**Why it matters:** Runbook §3.1 makes the validator a hard contract: "the validator is the gate; until it passes, output stays in `tmp/`." The current code violates that contract on the first run, which is precisely when output is least reliable. Smoke test would promote whatever the agent emitted, including potentially malformed frontmatter, missing `first_available`, missing `prompt_version` — exactly the fields downstream tooling depends on.
**Suggested fix:** Either (a) build a minimal validator before the smoke test (frontmatter-required-fields check is enough for v1), or (b) refuse to promote when validator missing (log `validation-failed` with note `"no validator script — output held in tmp/"`). Option (a) is preferred since the runbook treats validator as load-bearing.

### C1. Bucket fingerprint omits Track B row hashes
**File:** `scripts/wiki-pass2-triage.py:919-927` (`bucket_fingerprint`)
**What:** Hash covers `sorted(input_pages) + prompt_version + chunk_strategy`. Per runbook §3.4 the fingerprint should also cover the Track B JSONL row hashes for the bucket's pages.
**Why it matters:** Reconciliation §5.1.1 case 3 (input-change source: re-crawl changes a Track B row) cannot fire — fingerprint stays the same. A wiki re-crawl that updates Eddard's infobox would not re-queue the bucket. Not a smoke-test blocker; matters once Track B is re-run.
**Suggested fix:** Hash should include a stable digest of the relevant infobox-data rows. Cheap version: SHA-256 of the sorted JSON of each input page's `track_b_row` field, folded into the existing payload.

### C2. `compose_bucket_input` Pass 1 mention scan is substring-contains
**File:** `scripts/wiki-pass2.sh:368-369` (PYEOF) — `if page_norm in line or page in line`
**What:** For each page in the bucket, scans every line of every Pass 1 extraction looking for the literal substring of the page name.
**Why it matters:** False positives on common short names — `"Lady"` matches every line containing the word "lady". For the direwolves bucket this floods the agent context with thousands of unrelated mention rows, blowing the token budget and burying real signal.
**Suggested fix:** Match whole-word with regex `\b{page}\b`, or restrict to lines in the Raw Entity List section. Defer until after smoke if direwolves data shape is tolerable.

### C3. Coherence `edge_target_missing` check uses bidirectional prefix match
**File:** `scripts/wiki-pass2-coherence.py:197-199`
**What:** `target in known or any(s.startswith(target) or target.startswith(s) for s in known)` — bidirectional `startswith` means `"eddard"` matches `"eddard-stark"` AND `"eddard-stark"` matches `"eddard"`.
**Why it matters:** False negatives on missing edge targets. A typo or stale link reading `[[Eddar]]` would match `[[Eddard-stark]]` and pass the check.
**Suggested fix:** Exact slug match only. Allow a one-off canonicalization step (lowercase, hyphens) but no prefix wildcards.

### C4. Coherence allegiance match also uses bidirectional prefix match
**File:** `scripts/wiki-pass2-coherence.py:259-262`
**What:** Same prefix logic applied to allegiance resolution.
**Why it matters:** `"House Frey"` matches `"house-frey"` (good) but also `"house-frey-of-the-crossing"` and vice versa. Will report both as ambiguous when only one exists, or as resolved when neither does.
**Suggested fix:** Exact match; if multiple matches, produce one ambiguity row not multiple.

### C5. `cmd_status` displays `wave` column but manifests don't carry one
**File:** `scripts/wiki-pass2.sh:970-971` and the printed table at lines 960, 995
**What:** `wave_num=$(manifest_get "$mf" "wave" ...)` — the field is never written into the manifest by triage or by `cmd_run`. Always renders as `"—"`.
**Why it matters:** The wave column is dead in the status table. Either remove it or wire `cmd_run` to record the wave it ran each bucket in.
**Suggested fix:** Record wave in manifest on each run (`manifest_set "$mf" "wave" "$wave"`), or drop the column.

### C6. Reset's frontmatter-version filter is silent on missing field
**File:** `scripts/wiki-pass2.sh:1119-1126`
**What:** Regex `^prompt_version:\s*(.+)$` — if the field is absent, captures empty string, won't archive.
**Why it matters:** Any node the wiki-ingester forgets to stamp with `prompt_version` becomes un-archivable via `reset`. This makes the wiki-ingester prompt's frontmatter contract load-bearing for cleanup. Bake `prompt_version: v1` into the prompt requirements explicitly.
**Suggested fix:** No script change; document the requirement in the wiki-ingester prompt (which I'm writing in step 3).

### C7. `--limit N` opens output in `"w"` mode → silent corruption after a full run
**File:** `scripts/wiki-pass2-triage.py:1111` (`open(OUTPUT_FILE, "w")`)
**What:** Already documented in continue prompt as known issue 2.
**Why it matters:** Calling `--limit 100` after a full run rewrites `page-categories.jsonl` with only 100 rows. Already corrupted Session 18 once.
**Suggested fix:** Either (a) refuse to write to default path when `--limit` is set without `--output-path`, or (b) write to `page-categories.partial.jsonl` automatically when `--limit` is set. Low priority but a future maintainer footgun.

### C8. Direwolf `tier_default` is `tier-2` (no regex match), arguably should be `tier-1`
**File:** `scripts/wiki-pass2-triage.py:82-89` (`TIER_DEFAULT_RULES`)
**What:** `bucket_id = "direwolves"` matches none of the regex patterns; falls to fallback `tier-2`. Per architecture.md the six direwolves are named characters with verified canon facts.
**Why it matters:** Smoke-test output would tag every direwolf claim with `tier-2` by default, requiring per-claim override. Cosmetic for direwolves (a competent agent will override) but emblematic of the fallback being too low for named character buckets.
**Suggested fix:** Add `direwolves|dragons` to the tier-1 regex, or extend the rule to `character` substring (which wouldn't match `characters-house-stark` because `characters-` already matches the existing tier-1 pattern via `character`). Light touch; verify with the regex table after a substantive change.

### C9. Tripwire threshold defaults to 0.8 against the wrong denominator
**File:** `scripts/wiki-pass2-triage.py:1029-1031`
**What:** Default `--tripwire-threshold 0.8` measured against total pages. Real data shape: 12,378/17,657 (70%) are stubs without infoboxes — tripwire trivially fails.
**Why it matters:** Already documented in Session 18 details. Fails non-fatally (exit 2 after writing outputs), but creates noise.
**Suggested fix:** Either lower default to ~0.25 to match data shape, or measure against `pages-with-infoboxes` (~5,279) — the latter is more honest. Defer to a calibration session.

### C10. Oversized bucket-of-one names break CORE_TIER_RULES suffix regex
**File:** `scripts/wiki-pass2-triage.py:94, 95-103, 826-827`
**What:** When an oversized page is isolated, the sub_id is `f"{bucket_id}-{r['slug']}"` — e.g. `direwolves-grey-wind`, `characters-house-stark-eddard-stark`. The `_SPLIT_SUFFIX` regex `r"(-[a-z]([0-9]+)?(-[a-z]([0-9]+)?)?)?$"` allows at most two letter-segments. A slug like `eddard-stark` has two hyphens — does match `-[a-z]?-[a-z]?` *only* if both segments are single chars (they aren't here: `eddard` is 6 chars).
**Why it matters:** An oversized core page would land in `secondary` tier instead of `core`, delaying its processing. Not blocking direwolves (no oversized pages there) but real for `eddard-stark` if/when its bucket-of-one is created.
**Suggested fix:** Either (a) match `^direwolves(-.+)?$` (any suffix), or (b) recognize bucket-of-one suffixes explicitly. (a) is safer.

### C11. Orphan recovery has a TOCTOU-style race
**File:** `scripts/wiki-pass2.sh:239-287`
**What:** Two tabs running `cmd_run` at roughly the same time on the same orphan would both pass the staleness check, both wipe `tmp/`, both reset to `pending`. No locking.
**Why it matters:** Exposure window is small (orphan recovery runs once per `cmd_run`, before the wave starts). Worst case is double-work, not corruption (filesystem state ends up consistent).
**Suggested fix:** None for v1. Note for the runbook's "Walk-Away Safety" section if scaled-out crashes become common.

### M1. Dead code in `cmd_launch` wave numbering
**File:** `scripts/wiki-pass2.sh:894-901`
**What:** `local wave_num=$(( idx * waves_per / waves_per + j + t * waves_per + 1 ))` is computed and never used. The line below `local tw=$(( t * waves_per + j + 1 ))` is what actually drives wave assignment.
**Suggested fix:** Delete the `wave_num` line.

### M2. Triage `_SPLIT_SUFFIX` digit groups never produced
**File:** `scripts/wiki-pass2-triage.py:94`
**What:** `r"(-[a-z]([0-9]+)?(-[a-z]([0-9]+)?)?)?$"` — the `[0-9]+` parts are unreachable. `chunk_letters` only emits letters.
**Suggested fix:** Simplify to `r"(-[a-z](-[a-z])?)?$"`.

### M3. Inline Python in shell is fragile to bucket-id with quotes
**File:** `scripts/wiki-pass2.sh` — many `python3 -c "..."` blocks
**What:** Bucket IDs are interpolated directly into Python source via shell expansion. A bucket id containing `'` or `"` would break parsing. All current bucket IDs are slugs (a-z0-9-), so safe in practice.
**Suggested fix:** None for v1. If bucket IDs ever start carrying punctuation, switch to env-var-passing (`BUCKET_ID="$bid" python3 -c "import os; bid=os.environ['BUCKET_ID']; ..."`).

### M4. `compose_bucket_input` opens every Pass 1 extraction synchronously
**File:** `scripts/wiki-pass2.sh:354-381`
**What:** Nested loops: book → extraction file → for each line → for each page in the bucket. Quadratic on (pages × extractions × lines). Direwolves: 6 × ~73 × ~500 = manageable. Stark characters bucket: 30 × 344 × 500 = noticeable.
**Suggested fix:** Build a regex alternation of all page names once, scan each extraction once, group results per page. Defer until perf surfaces.

### D1. Manifest schema in triage extends runbook §5.2 silently
**What:** Triage emits `tier_default`, `chunk_strategy`, `oversized` in the per-bucket manifest. Runbook §5.2 schema lists only `bucket_id, tier, fingerprint, prompt_version, input_pages, expected_nodes, status, started_at, completed_at, validation_report`.
**Why it matters:** Future readers of the runbook will not know these fields exist. Not contradictory, but undocumented.
**Suggested fix:** Add the three fields to the §5.2 schema example with one-line descriptions. Or, alternatively, accept that the §2.1.1 input contract already documents them and rely on that.

### D2. `expected_nodes` filenames are bare; runbook §5.1 routing uses parent-type subdir
**What:** Triage writes `expected_nodes: ["ghost.node.md", ...]` — bare. Per §5.1 the actual on-disk path is `graph/nodes/characters/ghost.node.md`. Reconciliation walks them via `find graph/nodes -name "$node_file"` so it works, but two buckets emitting the same slug under different parent types (very unlikely, but possible if a character and a place share a slug) would both match the find.
**Suggested fix:** Either (a) document the find-by-name behavior in runbook §5.1.1, or (b) extend `expected_nodes` to record the parent-type subdir alongside the filename. (a) is the pragmatic choice for v1.

---

## What I checked end-to-end (`direwolves` seam test)

1. **Triage → manifest:** `working/wiki-pass2/direwolves/manifest.json` has 7 input_pages with Arya at the head. ✓ matches B2.
2. **Page-index lookup:** Each direwolf is in `working/wiki-parsed/page-index.jsonl` under its space-form name (`"Grey Wind"`, `"Ghost"`, etc.). ✓
3. **Cache disk path:** `sources/wiki/_raw/Grey_Wind.json` exists; `"sources/wiki/_raw/Grey Wind.json"` does not. ✓ matches B1.
4. **Launcher reconciliation walk:** would skip — no direwolves are `complete` yet (all `pending`). ✓
5. **Orphan recovery:** no `in-progress` manifests; would no-op. ✓
6. **bucket_input.json composition:** would set `raw_html_path: None` for every direwolf because of B1. The agent receives Track B + page-index data only, no HTML.
7. **Agent invocation:** prompt at `.claude/agents/wiki-ingester.md` is a 31-line stub — agent has no schema to follow. Step 3 of this session.
8. **Validator:** `scripts/wiki-pass2-validator.py` does not exist. Per B3, the launcher would print a warning and promote anyway.
9. **Atomic rename:** would resolve `character.direwolf` → `graph/nodes/characters/` via the `TYPE_DIR_MAP` parent-key match. ✓ assuming the agent emits `type: character.direwolf`.

---

## Recommendation

Fix B1, B2, B3 before the smoke test. C-tier issues can wait for a calibration session after smoke. Document D-tier in the runbook at a convenient moment.

**B1 fix is one line in `compose_bucket_input`** (replace spaces with underscores in path). **B2 fix is the alias clause removal** described in the continue prompt. **B3 fix needs a minimal validator script** — frontmatter-required-fields check is enough for v1; defer richer checks (no-orphan-edges, body-cites-something) to a follow-up session if smoke output is otherwise clean.

The wiki-ingester prompt I write in step 3 will explicitly require `prompt_version: v1` in frontmatter so C6 doesn't bite at first reset.

---

## Smoke-debug fix (2026-04-26, post-Session-19)

### Bug: silent exit after `--- Orphan recovery ---`

`weirwood wiki run core --bucket direwolves` exited 0 after the orphan-recovery banner with no further output, never reaching the pending-manifest collection or bundle composition.

### Root cause

`scripts/wiki-pass2.sh:286` — final line of `run_orphan_recovery`:

```sh
(( recovered > 0 )) && echo "Orphan recovery: ${recovered} bucket(s) reset to pending"
```

On a clean run with no orphans, `recovered=0`. The arithmetic `(( recovered > 0 ))` returns exit 1; the `&&` short-circuits; the whole compound returns 1. Because this is the **last** command in the function, the function returns 1. Under `set -euo pipefail`, the simple call `run_orphan_recovery "$orphan_threshold"` in `cmd_run` triggers immediate exit. No error is printed because the failing command was the function call itself, and `set -e` exits silently by design.

`run_reconciliation` doesn't hit this trap because its summary is wrapped in `if ... fi` — an `if` always returns 0 when the condition is false (no commands ran).

`bash -x` confirmed: the very last traced statement before exit was `+ (( recovered > 0 ))`.

### Fix

`scripts/wiki-pass2.sh` — wrap the recovery-summary echo in an `if`-block, matching the reconciliation pattern. Comment captures the trap so future edits don't reintroduce it. Not a `|| true` symptom suppress; the underlying contract is "this function returns 0 unless something actually went wrong," and the `&&`-chain accidentally violated it.

### Verification

Re-ran `weirwood wiki run core --bucket direwolves` (with a temporary `WIKI_PASS2_SMOKE_ABORT=1` sentinel inserted just before the `claude -p` invocation, then removed). Output:

```
--- Reconciliation pass ---
--- Orphan recovery (threshold=60min) ---
=== Wiki Pass 2 — CORE: processing all 1 pending buckets ===
--- Processing bucket: direwolves (6 pages) ---
  Composing bucket_input.json...
  Composed bucket_input.json: 6 pages
  [SENTINEL] WIKI_PASS2_SMOKE_ABORT=1 — aborting before claude -p
```

`working/wiki-pass2/direwolves/bucket_input.json` written: 6 pages (Ghost / Grey Wind / Lady / Nymeria / Shaggydog / Summer), every `raw_html_path` resolves to a real cache file under `sources/wiki/_raw/` (B1 fix confirmed working — `Grey_Wind.json` underscored form), every `track_b_row` populated with the expected key set (`page`, `entity_type`, `first_available`, `books`, `relationships`, `aliases`, …), `pass1_mentions` ranging 59–218 per page. Bundle is healthy.

Sentinel removed; manifest reset to `pending` cleanly. Ready for an actual agent-launch smoke test.

### Sibling concern (not fixed this session)

`run_reconciliation` is structurally fine today (its summary is wrapped in `if`), but there are several other places in `wiki-pass2.sh` where helper functions end on a `&&`-chain or arithmetic test — search for ` && ` near function-final lines if any future helper exits silently. Likewise, any helper that ends on `(( count > 0 ))` style needs review. Not fixing speculatively this session; flagging for the next maintenance pass.

---

## Smoke-run findings (2026-04-26, Session 20 review)

The direwolves smoke run completed: 6 nodes promoted, validator + coherence both green, $1.15, 4m 47s. But hand-inspection of the bundle and emitted nodes surfaced one substantive bug and one process gap.

### Bug T1. Triage direwolf override sends `Nymeria` (warrior queen page) instead of `Nymeria (direwolf)`
**File:** `scripts/wiki-pass2-triage.py` (direwolf override block, ~line 419-427)
**What:** The override matches on direwolf names (`{Ghost, Grey Wind, Lady, Nymeria, Shaggydog, Summer}`) and routes those pages into the `direwolves` bucket. For Nymeria, this matches the wiki page named simply `Nymeria` — which is **Princess Nymeria of Ny Sar** (Rhoynish warrior queen, ancestor of House Martell). The actual direwolf has a disambiguated wiki page name: `Nymeria (direwolf)`.
**Verified:** `working/wiki-pass2/direwolves/bucket_input.json` for page="Nymeria" has `raw_html_path: sources/wiki/_raw/Nymeria.json` (75,693-byte historical-queen page) and `track_b_row` containing `aliases: ["Nymeria of the Rhoyne"]`, `relationships: [{Titles → Princess of Dorne}, {Allegiances → House Martell}, {Issue → With Mors Martell: Four daughters}, ...]`, `first_available: ADWD chapter 6 (Tyrion II POV)`. None of this is direwolf data.
**Why it matters at scale:**
- This is the **only** case where the override hard-codes a page name without consulting a disambiguator — but the pattern is general. Any other entity whose canonical wiki page name collides with another (Aegon, Brandon, Maester ambiguities, etc.) would hit the same trap if a similar override is added.
- The agent self-corrected for direwolves (see "Agent self-correction" below). It will not always.
- The bucket fingerprint is computed from `input_pages[]`, so swapping `"Nymeria"` → `"Nymeria (direwolf)"` will trigger a re-queue of the direwolves bucket — that's correct behavior, but means the existing `nymeria-direwolf.node.md` should be re-emitted from a clean bundle once the fix lands.
**Suggested fix:** In the direwolf override, map the well-known direwolf names to canonical wiki page names: `{"Nymeria": "Nymeria (direwolf)"}` (only Nymeria has a collision; Ghost, Grey Wind, Lady, Shaggydog, Summer all canonical). Cleaner: when the override matches, look up the actual page in `working/wiki-parsed/page-index.jsonl` and prefer a `(direwolf)` / `(disambiguation-aware)` variant when one exists.
**Re-extract scope:** Once triage is fixed, only the direwolves bucket needs re-queue (set `direwolves` manifest to `pending`, delete `working/wiki-pass2/direwolves/bucket_input.json` and `nymeria-direwolf.node.md` in `graph/nodes/characters/`, re-run `weirwood wiki run core --bucket direwolves`). The existing nymeria node's content is correct (agent built from the right page) — but it's not reproducible from a clean re-run, so we want to regenerate it.

### Agent self-correction (a feature, not a bug)

When the agent saw the source mismatch, it:
1. Read `sources/wiki/_raw/Nymeria_(direwolf).json` directly (allowed under "the bundle **and the files it points at**" — and the agent inferred from the wiki URL pattern that the disambiguated file existed)
2. Filed a structured question: `working/wiki-pass2/questions-for-matt.jsonl` line 1, type `disambiguation`, blocking=false, with full context and resolution suggestion
3. Set `wiki_source` to the corrected URL (`https://awoiaf.westeros.org/index.php/Nymeria_(direwolf)`), slug to `nymeria-direwolf`, and disclosed the override in the node's `## Notes` section
4. Did **not** use any of the warrior-queen track_b_row fields in the emitted node

This is exactly the behavior the wiki-ingester prompt's "Conflict / Question / Contradiction Protocol" calls for. The agent's structured channels work. **Trust the agent to flag mismatches; verify by reading questions-for-matt.jsonl after every run.**

### Process gap P1. Smoke-summary did not surface `questions-for-matt.jsonl` entries

The prior agent's run summary reported "Coherence (weirwood wiki check) | 0 issues" and "Promoted | 6 → graph/nodes/characters/" but did not mention the disambiguation question. A reader closing the loop on smoke-test acceptance would have missed a load-bearing finding.

**Suggested fix:** When `cmd_run` finishes a bucket (or the whole `core`/`secondary` run), append to its summary line a count of unresolved entries in `working/wiki-pass2/questions-for-matt.jsonl`, `conflicts.jsonl`, and `pass1-contradictions.jsonl` for buckets touched by that run. Cheap: `wc -l` on each file, filter by `bucket_id`, print non-zero counts. Should also propagate into `working/extraction-stats/wiki-pass2-stats-*.csv` columns.

This matters more as scaling proceeds — at 42 core buckets and 495 secondary, manually grepping the question file after every run is not viable. Surface counts in the summary by default.

### Reframing the slug deviation flag

My initial Session-20 read was that the validator should enforce slug-set equality against `expected_nodes` (the `nymeria-direwolf.node.md` mismatch with `expected_nodes: [..., nymeria.node.md, ...]` had triggered this). After reading the question file, the right framing is:

- The agent's slug deviation is a **signal**, not a bug — it indicates the bundle was wrong and the agent disambiguated.
- A slug-set-equality check would have **incorrectly failed** the existing nymeria-direwolf node.
- The validator is fine as-is for v1. The launcher's smoke-summary surfacing is the correct intervention.
- A future v2 validator could optionally check that any slug deviation is paired with a `disambiguation` question — but that's a refinement, not a blocker for scaling.

### Blocker-status of T1 + P1 for scaling beyond direwolves

**Not strictly blocking, but strongly suggested before tier=core scale:**
- T1 affects only the direwolves bucket today. Other core buckets do not use the same override pattern. Could ship core without T1 fix, then re-emit nymeria afterward.
- P1 is a process+tooling gap — without it, scale-runs across 42 core buckets will silently accumulate disambiguation questions that nobody reads. **Fix P1 before scaling; T1 is a bucket-of-one re-run cost and can come after.**



