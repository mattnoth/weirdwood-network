# Continue Prompt — Wiki Pass 2: Triage Disambiguation Fix + Summary Surfacing → Scale Core

**Created:** 2026-04-26 (Session 20)
**Goal:** Fix the two findings from the direwolves smoke test (T1 + P1), re-emit `nymeria-direwolf.node.md` from a clean bundle, then scale to the remaining 41 core buckets.

## Read first

1. `worklog.md` — Sessions 20 then 19 then 18 (in that order)
2. `working/session-details/session-020.md` — full narrative of the smoke run + the bundle/source-mismatch finding
3. `working/runbooks/wiki-pass2-orchestration-build-self-review.md` § "Smoke-run findings (2026-04-26, Session 20 review)" — T1 and P1 documented in detail
4. `working/wiki-pass2/questions-for-matt.jsonl` — read it. The agent filed a disambiguation question on the direwolves run that explains the bug from the agent's perspective.

## State on disk

- Smoke run is **complete** — 6 direwolf nodes promoted to `graph/nodes/characters/`. `working/wiki-pass2/direwolves/manifest.json` is `complete`, `nodes_promoted: 6`.
- Validator + coherence both green.
- One unresolved disambiguation question in `working/wiki-pass2/questions-for-matt.jsonl` (Nymeria — historical queen vs. direwolf).
- `nymeria-direwolf.node.md` content is wiki-grounded and correct (the agent self-corrected by reading `Nymeria_(direwolf).json` directly when the bundle pointed at `Nymeria.json`). It will be re-emitted as part of this work to be reproducible from a clean bundle.
- `scripts/wiki-pass2.sh:286-290` orphan-recovery `if`-block fix is live.
- 41 other core buckets still `pending` (manifests in `working/wiki-pass2/<bucket>/manifest.json`).

## What to do

### 1. T1 — Fix triage direwolf override

**File:** `scripts/wiki-pass2-triage.py`, around line 419-427 (the direwolf override block).

The override currently matches on direwolf names without consulting the wiki page-index for disambiguators. For "Nymeria", this routes the **historical Princess Nymeria of Ny Sar** page (`sources/wiki/_raw/Nymeria.json`, 75 KB, House Martell ancestor) into the `direwolves` bucket — instead of the actual direwolf page (`sources/wiki/_raw/Nymeria_(direwolf).json`, 53 KB).

**Verify:** `grep '"page": "Nymeria' working/wiki-parsed/page-index.jsonl` shows both `"Nymeria"` and `"Nymeria (direwolf)"` as distinct entries. The direwolf page has `cite_ref_books.agot=6` (six AGOT cite_refs) — the historical queen has `cite_ref_books.agot=1`, `affc=6`. They are clearly distinct pages.

**Fix:** map known direwolf-name collisions to disambiguated wiki page names. Only Nymeria collides:

```python
DIREWOLF_PAGE_OVERRIDES = {
    "Nymeria": "Nymeria (direwolf)",
}
# When matching the direwolf override, look up the override map first;
# if the page exists in the page-index under the disambiguated name, use that.
```

The fix should be defensive — fall back to the bare name only if the disambiguated name isn't in the page-index.

**Cleaner generalization (optional, more work):** any time a direwolf override matches, query the page-index for the bucket's expected entity type (`character.direwolf`) and prefer the page whose `entity_type_guess` or category most closely matches. This will pay dividends when other overrides land (dragons, named horses, etc.).

**Re-run triage:** `weirwood wiki triage --accept` (or whatever `wiki-pass2-triage.py --accept` does in the current launcher). The direwolves bucket's fingerprint will change (input_pages set changed: "Nymeria" → "Nymeria (direwolf)"), so the bucket will be marked `version-stale` and re-queued automatically.

### 2. P1 — Surface questions/conflicts/contradictions in launcher summary

**File:** `scripts/wiki-pass2.sh`, in `cmd_run` after a bucket completes (around line 685-740, the post-validator promotion block).

**What to add:** when a bucket finishes (success OR fail), tally unresolved entries in the three append-only JSONL channels filtered by `bucket_id`:

```sh
local q_count c_count p_count
q_count=$(grep -c "\"bucket_id\": \"${bucket_id}\"" working/wiki-pass2/questions-for-matt.jsonl 2>/dev/null || echo 0)
c_count=$(grep -c "\"bucket_id\": \"${bucket_id}\"" working/wiki-pass2/conflicts.jsonl 2>/dev/null || echo 0)
p_count=$(grep -c "\"node\".*\"${bucket_id}\"" working/wiki-pass2/pass1-contradictions.jsonl 2>/dev/null || echo 0)
# ... include in per-bucket summary line
```

(The grep patterns are illustrative; `pass1-contradictions.jsonl` doesn't carry `bucket_id` directly — it's keyed by `node`. Use a join, or add `bucket_id` to that schema in §6.5 of the runbook. Easiest: just print a global count of unresolved rows added during this run, by recording the file size before/after.)

**Where to print:** the "=== Wiki Pass 2 — CORE: processed N buckets ===" summary at the end of `cmd_run`. Format:

```
=== Wiki Pass 2 — CORE: processed 42 buckets (41 ok, 0 fail, 1 skipped) ===
  Questions filed: 3 (across 2 buckets)  →  working/wiki-pass2/questions-for-matt.jsonl
  Conflicts: 0
  Pass-1 contradictions: 0
```

**Stats CSV:** add `questions_filed`, `conflicts_filed`, `pass1_contradictions_filed` columns to `working/extraction-stats/wiki-pass2-stats-core-v1.csv`.

### 3. Re-emit nymeria-direwolf

After T1 lands and triage is re-run:

```sh
weirwood wiki reset --bucket direwolves    # clears manifest status, removes promoted nodes for re-emit
weirwood wiki run core --bucket direwolves
```

Verify:
- `working/wiki-pass2/direwolves/bucket_input.json` now has `page: "Nymeria (direwolf)"` and `raw_html_path: sources/wiki/_raw/Nymeria_(direwolf).json`
- The new `nymeria-direwolf.node.md` (or `nymeria.node.md` — depends on whether you keep the disambiguator suffix in the slug after triage carries it; document the choice) has `track_b_row` data that's actually about the direwolf
- No new entry appears in `questions-for-matt.jsonl` for this bucket
- The smoke summary now reports "Questions filed: 0" (verifying P1)

If the disambiguated slug naming choice is unclear: prefer keeping `nymeria-direwolf` as the slug (matches the wiki URL form). Update triage to compute slug from the disambiguated page name, and `expected_nodes` in the manifest will line up.

### 4. Resolve the open question

Once direwolves re-emits cleanly, append a resolution to the existing question in `working/wiki-pass2/questions-for-matt.jsonl`:

```json
{... "resolved_at": "2026-04-27T...", "resolution": "Triage script updated to map direwolf-name collisions to disambiguated wiki page names. Direwolves bucket re-emitted from clean bundle. Pattern generalizable to other override types (dragons, named horses) when they're added."}
```

### 5. Scale to remaining 41 core buckets

```sh
weirwood wiki core <terms> <waves>
```

Watch the smoke summary on each wave for new questions/conflicts. Stop and triage if any single bucket fails or files a `blocking: true` question.

### Definition of done

- [ ] T1 fixed in `scripts/wiki-pass2-triage.py`; `--accept` re-run; direwolves bucket marked `version-stale`/re-queued
- [ ] P1 fixed in `scripts/wiki-pass2.sh`; smoke summary surfaces unresolved-question counts; CSV columns added
- [ ] `nymeria-direwolf.node.md` (or whatever its post-fix slug is) re-emitted from clean bundle, validator + coherence green
- [ ] Existing question in `questions-for-matt.jsonl` resolved
- [ ] No new questions filed on the direwolves re-run
- [ ] All 42 core buckets processed (41 + re-emitted direwolves), or a clear stopping point with reasons documented
- [ ] Worklog updated; this continue prompt deleted; new continue prompt for "secondary tier" if core is clean

## Out of scope this session

- Don't scale to **secondary** tier in the same session — it's 495 buckets and a wholly different cost envelope. Stop after core.
- Don't implement the "agent must file a question whenever it reaches outside the bundle" prompt change. The agent's existing structured-channel discipline is correct; the bundle isolation rule is loose by design.
- Don't add content-quality validator checks (body-cites-something, no-orphan-edges in body prose). Those are v2 — explicitly out of v1 scope per the cold review.
- Don't fix C1, C8, C9, C10 from the cold review — still post-scale calibration work.
- Don't re-fetch the wiki. Local cache only. (Memory: `feedback_no_external_wiki_fetch.md`, `project_wiki_already_local.md`.)
- Don't run extractions or smoke tests without explicit Matt confirmation. (Memory: `feedback_no_extraction_without_asking.md`.)

## Cost expectations (rough)

Direwolves ran $1.15 for 6 pages, 238 KB bundle, 4m 47s, 783k cache-read tokens (~91% of total). At sub-linear cost-per-page (driven by cache reads dominating), the **41 remaining core buckets** should be in the rough ballpark of $30-60 total — but core has variance: some buckets are 1 page (oversized solo nodes like Eddard Stark), others are 30+ (alphabetical splits of large houses). Treat the first 5 buckets of the core run as a refined cost baseline before committing to the full sweep.
