# Continue — Execute Matt's rename decisions (S90 → S91 handoff)

> **Recommended model:** Opus 4.7 — multiple slugs to execute, each with curated `aliases:` decisions + post-rename body-text patching + alias-chain verification. Matt asked for Opus.
>
> **Read first:** `working/session-results/2026-06-10-overnight-rename-dryrun.md` — contains Matt's per-slug decisions. The "Your decisions" table for the 9 flagged slugs has his yes/no/different-suggestion calls; the "Clean rename candidates" table lists 5 low-risk renames also waiting on his per-row approval. Trust the file. If a row is ambiguous, ASK Matt (don't guess) — he's available.

## Context — what landed before this session

S88 scoped a 4-mode graph-validation track; S89 executed Mode 1 (8 capability probes) + kicked off Phase 1 overnight. Three overnight script-builder agents completed cleanly:

- **#7 — `graph-query.py --event-participants <hub>` primitive** (`scripts/graph-query.py` extended). DONE.
- **#8 — Event-alias-resolver** (`scripts/event_alias_resolver.py` + `working/wiki/data/event-alias-lookup.json`, 876 phrases). DONE — but has a parser bug (see "Known bugs" below).
- **#10 — `scripts/rename-event-node.py` (513 lines, `--dry-run`/`--apply`) + 29-slug audit.** Script built. **Primary rename `joffrey-orders-execution` → `execution-of-eddard-stark` already APPLIED by Matt in S90.** Touched 7 artifacts (1 node move + 6 edge rows). Surfaced 3 bugs (see below). The 5 secondary clean candidates + 9 flagged candidates remain queued — your job.

`edges.jsonl` = 4,757 (unchanged post-primary-apply — renames update fields in place). `events/` = 583. Backup: `graph/edges/_regrounding/edges-pre-reification-2026-06-09.jsonl`.

## Known bugs (you must work around these — fixing in-script is OPTIONAL upgrade)

Matt discovered these during S90's primary-rename apply. They affect every subsequent rename until fixed.

**Bug 1 — alias-resolver parser only reads inline YAML.** `scripts/event_alias_resolver.py` parses inline `aliases: ["Ned's execution", "..."]` correctly but silently corrupts block-style YAML lists. **Workaround: ALWAYS use the inline form** when adding aliases to renamed nodes. Do NOT write:
```yaml
aliases:
  - "Ned's execution"
  - "Ned Stark's execution"
```
Write this instead:
```yaml
aliases: ["Ned's execution", "Ned Stark's execution"]
```

**Bug 2 — alias-resolver doesn't auto-derive natural phrasings.** The deterministic resolver is pure phrase-lookup; it cannot semantically substitute "Ned" for "Eddard Stark" or recognize that `execution-of-eddard-stark` should match the natural query "Ned's execution". Every reader-natural phrasing you want to support MUST be enumerated as an explicit `aliases:` frontmatter entry. The earlier "auto-resolves on rebuild" prediction was wrong.

**Bug 3 — `rename-event-node.py` doesn't touch the renamed node's own body text or free-text edge fields.** The script rewrites:
- Frontmatter `slug:` and `name:`
- `source_slug`/`target_slug` in edges.jsonl
- `superseded_by` field references
- Reference JSON files + cross-references
- Slug-form refs in OTHER node files

But it does NOT touch:
- The renamed node's own **body H1 + mint-prose** (e.g. `# Joffrey orders execution` heading + the descriptive paragraph stays as the old slug's display text)
- Free-text `plate5_superseded_note` fields in edge rows that may contain the old slug as prose

**Workaround per rename:**
1. After `--apply`, open the new node file at `graph/nodes/events/<new_slug>.node.md` and manually rewrite the H1 + any mint-prose that uses the old display name.
2. Grep `graph/edges/edges.jsonl` for the old slug in `plate5_superseded_note` field (string match, not field-scoped): `grep '"plate5_superseded_note":.*<old-slug>' graph/edges/edges.jsonl`. If hits, edit those rows manually.
3. Final sanity grep: `grep -r '<old-slug>' graph/` should return 0 matches (excluding `_regrounding/` backup file).

If you want to fix the script before running the batch — both bugs are small upgrades — that's OPTIONAL and additive. The workaround pattern is fully documented and was applied successfully for the primary rename.

## What this session does

For each rename Matt approved, execute the rename, patch body-text, add curated inline aliases, and at the end rebuild downstream artifacts. Verify with smoke queries.

### Step 1 — Parse Matt's decisions

Read `working/session-results/2026-06-10-overnight-rename-dryrun.md`. The primary is DONE; ignore it. Build a list of rename operations from:

1. **The "Clean rename candidates" table** (5 rows: `doran-orders-arrest-of-the-sand-snakes`, `jon-orders-slynt-hanged-then-changes-to-beheading`, `littlefinger-orders-dontos-killed`, `tyrion-orders-symon-s-assassination`, `victarion-orders-kerwin-killed`). Each row has a `suggested_new_slug`. Include each ONLY if Matt explicitly approved it (look for yes/ok/✓ annotations). Unannotated = NOT approved → skip.
2. **The "Your decisions — the 9 flagged slugs" table.** Matt's yes/no/different-suggestion for each. For "yes" with a specific new slug, include it. For "no" / "skip" / "keep", skip. If any row is ambiguous, ASK before running.

Print the concrete rename list back to Matt for confirmation if there are >3 renames OR any unusual edge cases.

### Step 2 — Per-slug execution loop

For each (old_slug, new_slug):

```bash
# 2a. Re-run dry-run (sanity — file state may have shifted since overnight)
python3 scripts/rename-event-node.py <old> <new> --dry-run > /tmp/rename-dryrun-<old>.txt 2>&1
# Read it. Verify: 0 collision errors; "Other node files" hits are 0 or all expected; total edge-row count plausible (< 30 typically; flag if higher). If clean, proceed.

# 2b. Apply
python3 scripts/rename-event-node.py <old> <new> --apply

# 2c. Patch body-text (Bug 3 workaround)
# Open graph/nodes/events/<new_slug>.node.md — rewrite H1 + any mint-prose using the old display name.
# Then grep for old slug in plate5_superseded_note free-text and fix:
grep -n '<old-slug>' graph/edges/edges.jsonl
# Edit any hit rows in place.

# 2d. Add curated inline aliases (Bug 1 workaround — INLINE FORM ONLY)
# Open graph/nodes/events/<new_slug>.node.md. Add or extend:
# aliases: ["natural phrasing 1", "natural phrasing 2", "...up to ~4 entries..."]
```

**Alias guidance.** Each renamed event gets 2-4 natural-phrase aliases covering reader-natural phrasings. Be conservative — over-aliasing causes collisions. Examples (use as templates, not literal copies):

- `arrest-of-the-sand-snakes` → `aliases: ["arrest of the Sand Snakes", "the Sand Snakes arrested", "Doran arrests the Sand Snakes"]`
- `execution-of-janos-slynt` → `aliases: ["Slynt's execution", "the beheading of Janos Slynt", "Jon executes Slynt"]`
- `killing-of-dontos-hollard` → `aliases: ["Dontos's death", "the killing of Dontos", "Littlefinger has Dontos killed"]`
- `assassination-of-symon-silver-tongue` → `aliases: ["Symon's death", "the killing of Symon Silver Tongue", "Tyrion has Symon killed"]`
- `killing-of-maester-kerwin` → `aliases: ["Maester Kerwin's death", "Victarion kills Kerwin"]`

For any flagged slugs Matt OK'd with a custom new slug, derive aliases the same way — natural reader phrasings, 2-4 entries. If a phrase could plausibly point at a different node (e.g. "the execution" by itself), omit and note.

**Final per-slug sanity check:** `grep -r '<old-slug>' graph/ | grep -v _regrounding` returns 0 matches.

### Step 3 — Rebuild downstream artifacts (ONCE, after all renames complete)

```bash
python3 scripts/build-entity-indexes.py            # rebuild graph/index/events/
python3 scripts/event_alias_resolver.py --build    # rebuild alias lookup with new aliases
```

Both are idempotent.

### Step 4 — Verify alias-chain works (the actual user-facing test)

```bash
# For each renamed event, test 2-3 of its aliases resolve correctly:
python3 scripts/event_alias_resolver.py "Slynt's execution"
python3 scripts/event_alias_resolver.py "the killing of Dontos"
python3 scripts/event_alias_resolver.py "Symon's death"
# (etc.)

# Then test --event-participants on a few renamed slugs:
python3 scripts/graph-query.py --event-participants <new-slug>
```

If any expected alias miss-resolves OR `--event-participants` finds no participants for a renamed slug, STOP. Surface the issue. Don't paper over a resolver/rebuild mismatch.

### Step 5 — Update todos.md + worklog

Mark NEW TODO #10 fully done in `working/todos.md`. Update body with the full list of slugs renamed in this session (sequenced from primary → secondary clean → flagged).

Update `worklog.md` Session 91 entry with:
- How many slugs renamed (out of the ~14 candidates)
- Verbatim (old, new) list
- Aliases added per renamed node (or representative sample if many)
- Verification spot-test results
- Confirm `edges.jsonl` row count post-batch (should still be 4,757 — renames update fields, not rows)
- What's next: `progress/continue-prompts/2026-06-11-phase2-mode3-dip.md` (Phase 2 Mode 3 dip)
- Whether you fixed Bug 1 (inline parser) or Bug 3 (body-text rewriting) in the script (optional upgrades — note status)

### Step 6 — Write session results

Write `working/session-results/2026-06-11-rename-execution.md`:
- Per-slug result (renamed / skipped / failed)
- Aliases added per slug
- Spot-test outputs verbatim
- Any surprises encountered + how resolved
- Final `grep -r '<each-old-slug>' graph/ | grep -v _regrounding` results (should all be 0)

## What this session does

For each renamed slug, execute the rename, add curated aliases, and at the end rebuild downstream artifacts. Verify with a few smoke queries.

### Step 1 — Parse Matt's decisions

Read `working/session-results/2026-06-10-overnight-rename-dryrun.md`. Build a list of rename operations from:

1. **The primary rename** (always do this): `joffrey-orders-execution` → `execution-of-eddard-stark`. Already dry-run-clean.
2. **The "Clean rename candidates" table** (lines ~59-66 of the file): 5 rows with explicit `old_slug` → `suggested_new_slug` pairs. ONLY include each one if Matt has explicitly confirmed it (look for any text he added — accept marks, "yes", "ok", "skip", "no", etc.). If a row has no annotation, treat as **not yet approved** and skip it (do NOT default to yes). If Matt's annotation is ambiguous, ASK before running.
3. **The "Your decisions — the 9 flagged slugs" table** (lines ~71-89 of the file): Matt's yes/no/different-suggestion for each. For "yes" with a specific suggested slug (either his or his acceptance of mine), include it. For "no" / "skip" / "keep", do NOT rename. If a row reads ambiguously, ASK.

Build a concrete list before running any apply. Print the list back to Matt for confirmation if there are >3 renames or any unusual edge cases.

### Step 2 — Per-slug execution loop

For each (old_slug, new_slug) pair:

```bash
# 2a. Re-run dry-run (fast sanity check — files may have shifted slightly since overnight)
python3 scripts/rename-event-node.py <old> <new> --dry-run > /tmp/rename-dryrun-<old>.txt 2>&1

# 2b. Verify the dry-run is clean:
#   - 0 collision errors
#   - The "Other node files" section is 0 hits OR all hits make sense
#   - The total edge-row count is plausible (< 30 per slug, typically; flag if higher)
# If clean, proceed. If not, STOP and surface the issue.

# 2c. Apply
python3 scripts/rename-event-node.py <old> <new> --apply
```

After each `--apply`, also:

**2d. Add a curated `aliases:` entry to the renamed node's frontmatter.** The auto-derived `name:` covers display. Aliases cover discoverability for queries like "Ned's execution" or "the death of Symon Silver Tongue". Open the new node file at `graph/nodes/events/<new_slug>.node.md` and either:

- Add an `aliases:` field to the frontmatter if it doesn't exist, OR
- Append to the existing list if it does.

Use judgment. Each renamed event gets 2-4 natural-phrase aliases. Examples:

- `execution-of-eddard-stark` → `aliases: ["Ned's execution", "Ned Stark's execution", "the beheading of Ned Stark", "Ned's beheading"]`
- `arrest-of-the-sand-snakes` → `aliases: ["arrest of the Sand Snakes", "the Sand Snakes arrested", "Doran arrests the Sand Snakes"]`
- `execution-of-janos-slynt` → `aliases: ["Slynt's execution", "Jon executes Slynt", "the beheading of Janos Slynt"]`
- `killing-of-dontos-hollard` → `aliases: ["the killing of Dontos", "Dontos's death", "Littlefinger has Dontos killed"]`
- `assassination-of-symon-silver-tongue` → `aliases: ["the killing of Symon Silver Tongue", "Symon's death", "Tyrion has Symon killed"]`
- `killing-of-maester-kerwin` → `aliases: ["Maester Kerwin's death", "Victarion kills Kerwin"]`

For any flagged slugs Matt OK'd, derive 2-4 aliases that cover the natural reader phrasings (the same way you'd phrase the event aloud). Pick the aliases conservatively — over-aliasing causes resolver collisions. If a phrase could plausibly point at a different node, leave it out and note it.

### Step 3 — Rebuild downstream artifacts (do ONCE, after all renames complete)

```bash
# Rebuild the events index so graph/index/events/ reflects new slugs
python3 scripts/build-entity-indexes.py

# Rebuild the event-alias-resolver so the new aliases land in the lookup
python3 scripts/event_alias_resolver.py --build
```

Both are idempotent — running them once at the end is the right batch.

### Step 4 — Verify alias-chain works (the actual user-facing test)

After rebuild, spot-test a few queries to confirm the chain works:

```bash
# Should resolve to execution-of-eddard-stark
python3 scripts/event_alias_resolver.py "Ned's execution"
python3 scripts/event_alias_resolver.py "Ned Stark's execution"

# Should resolve to the renamed slug if applied
python3 scripts/event_alias_resolver.py "the killing of Dontos"
# (etc. — one per renamed event)

# Then test the event-participants primitive on the resolved slug
python3 scripts/graph-query.py --event-participants execution-of-eddard-stark
```

If any expected alias miss-resolves OR if `--event-participants` finds no participants for a renamed slug, STOP. Surface the issue. Don't paper over a resolver/rebuild mismatch.

### Step 5 — Update todos.md + worklog

Mark NEW TODO #10 as DONE in `working/todos.md`. Update the todo's body with the list of slugs actually renamed + counts.

Update `worklog.md` Session 91 entry with:
- How many slugs were renamed (out of the 6 clean + N flagged Matt approved)
- Verbatim list of (old, new) pairs
- Aliases added per renamed node (or a sample if there are many)
- Spot-test results
- Confirm `edges.jsonl` row count post-rename (should be unchanged from 4,757 — renames update fields in place, not add/remove rows)
- What's next: `progress/continue-prompts/2026-06-11-phase2-mode3-dip.md` (Phase 2 Mode 3 dip)

### Step 6 — Write session results

Write `working/session-results/2026-06-11-rename-execution.md`:
- Per-slug result (renamed / skipped / failed)
- Aliases added per slug
- Spot-test outputs verbatim
- Any surprises encountered + how resolved

## Hard rules

- **DO NOT** run any rename without re-running its `--dry-run` first (Step 2a). The overnight dry-run is from 2026-06-10; minor things may have shifted.
- **DO NOT** auto-/endsession. Matt grants /endsession explicitly per standing rule.
- **DO NOT** proceed to Phase 2 (Mode 3 dip) in this session. That's the next session's continue prompt.
- **DO NOT** add aliases that could plausibly resolve to a different node. When in doubt, omit and note.
- **DO** ask Matt directly if any of his decisions in the rename-dryrun file are ambiguous. He's not asleep this time.
- **DO** stop and surface issues. Don't silently work around resolver mismatches or dry-run inconsistencies.

## Files / artifacts referenced

- `working/session-results/2026-06-10-overnight-rename-dryrun.md` — Matt's decisions (this is the source of truth for what to rename)
- `scripts/rename-event-node.py` — the rename script (`--dry-run`/`--apply`)
- `scripts/build-entity-indexes.py` — rebuild events index
- `scripts/event_alias_resolver.py` — rebuild + query the event-alias-resolver
- `graph/nodes/events/<slug>.node.md` — where new aliases get added
- `graph/edges/edges.jsonl` — the canonical edge set (will be modified in place by `--apply`)
- `working/wiki/data/event-alias-lookup.json` — the alias lookup artifact (rebuilt at end)

## End-of-session checklist

- Write `working/session-results/2026-06-11-rename-execution.md`
- Update `working/todos.md` — close NEW TODO #10
- Update `worklog.md` S91 entry
- /endsession requires explicit Matt permission per standing rule
