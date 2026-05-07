# Session 19 — Wiki Pass 2 Launch Prep + Smoke-Test Bug Surface (2026-04-26)

## Frame

Session 18 left three artifacts on disk needing review before the first wiki-ingester smoke test could fire:
- `scripts/wiki-pass2-triage.py` (Arya bug not yet fixed)
- `scripts/wiki-pass2.sh` (B1 path-mismatch bug not yet identified)
- `.claude/agents/wiki-ingester.md` (31-line stub)

The continue prompt at `progress/continue-prompts/2026-04-26-wiki-pass2-launch-prep.md` defined the work: fresh-cold script review → Arya fix → write the wiki-ingester prompt → smoke-test direwolves.

## Session shape

This was an unusual session because much of the work happened in a *separate* iTerm Claude Code session that I (the orchestrator) launched via osascript and authorized to run autonomously while Matt stepped away for a few hours. That separation worked: the autonomous agent produced the cold review, fixed the Arya bug, and wrote the wiki-ingester prompt without intervention. Hard-stop before smoke test, as instructed.

When Matt returned, we read the autonomous session's three artifacts cold, applied a couple of follow-up fixes I judgment-called (B1 path fix, validator script, `first_available` softening), and tried to run the smoke test. The smoke test surfaced a real bug — the launcher silently exits after orphan recovery, never composing the bundle.

## What the autonomous session produced

### 1. Cold script review (`working/runbooks/wiki-pass2-orchestration-build-self-review.md`)

3 blockers (B1/B2/B3), 11 correctness issues (C1-C11), 4 maintenance items (M1-M4), 2 documentation/coupling notes (D1-D2). Highlights:

- **B1** (most critical, surfaced *first* by the cold reviewer): `compose_bucket_input` builds `sources/wiki/_raw/Grey Wind.json` but the cache uses `Grey_Wind.json`. Every multi-word page would get `raw_html_path: null`. **This bug would have made the smoke test look like an agent-prompt problem when it was actually an upstream path-mismatch.**
- **B2**: Arya bug (alias-match in direwolf override).
- **B3**: validator script doesn't exist; launcher silently promotes unvalidated output, violating runbook §3.1.
- **C1**: bucket fingerprint omits Track B row hashes — wiki re-crawl wouldn't trigger re-queue.
- **C8**: direwolves `tier_default` falls to `tier-2` (no regex match); should arguably be `tier-1`.
- **C9**: triage tripwire defaults to 0.8 against the wrong denominator (already documented Session 18).
- **C10**: oversized bucket-of-one names break `_SPLIT_SUFFIX` regex — sends e.g. `eddard-stark` to secondary tier instead of core.

The cold-review approach validated its premise: an outside read finds bugs the build session wrote and missed. B1 alone justified the review session.

### 2. Arya fix (`scripts/wiki-pass2-triage.py:419-427`)

Removed the alias clause from the direwolf override. Re-ran `--accept`. `working/wiki-pass2/direwolves/manifest.json` now contains exactly: Ghost, Grey Wind, Lady, Nymeria, Shaggydog, Summer (6 entries, alphabetized). Bucket totals shifted: 42 core / 495 secondary (was 35/472 — Arya routed correctly to `characters-house-stark-a-b`, and the bucket recount cascades).

The `wiki-pass2.sh` test for "Arya isn't in direwolves" now passes.

### 3. Wiki-ingester prompt (`.claude/agents/wiki-ingester.md`)

180 lines, mechanical-extractor as structural model. Sections covered:
- Bucket isolation (read only the bundle, never the wiki domain, never `graph/nodes/`)
- Input contract (`bucket_input.json` schema, field semantics, fallback when `raw_html_path` is null)
- Output contract (required + optional frontmatter, body sections, citation format)
- Confidence-tier override protocol with explicit per-claim justification rule
- Chunk strategy (`single-pass` vs `section-by-section` for oversized pages)
- Three append-only structured channels (questions/conflicts/contradictions)
- Hard constraints + synthesis rules + definition of done

## Post-autonomous follow-ups (this session, with Matt back)

### B1 fix in `scripts/wiki-pass2.sh:386-394`

Page name normalized to underscore form before path lookup. Comment notes why the alias-style failure mode happened (preserves the lesson). One-line fix.

### Validator script (`scripts/wiki-pass2-validator.py`)

Delegated to script-builder. ~150 lines. Required-fields check, slug↔filename match, count vs `bucket_input.json::pages[]`, type prefix against architecture.md (27 valid types extracted live), `confidence` regex (`tier-[1-4]`), `bucket_id` and `prompt_version` match against bundle. `first_available` deliberately *not* enforced (see next).

Smoke-tested on a fixture: pass case green, missing-field case fails with marked JSON report on stdout, count-mismatch case fails. Cleaned up fixture.

Script-builder flagged three notes:
1. Launcher invokes with `--bucket-dir` and `--output` only (not `--bundle`/`--manifest`); validator handles via defaults.
2. Manifest's `expected_nodes[]` could be used for slug-exact matching (today only count is checked) — v2 idea.
3. Direwolves `tier_default: tier-2` — same C8 issue.

### `first_available` softening in wiki-ingester prompt

Matt: "we've had a few first_available issues and spoiler gating is becoming kind of an issue. Spoiler gating isn't a part of MVP, so maybe just add another param as to not override?"

Decision: drop `first_available` from required frontmatter for v1. It was going to be a question-floods-the-channel field — the wiki-infobox-parser only populated it for ~55% of pages. Agent now does:
- If `track_b_row.first_available` is populated, copy verbatim
- If absent, omit
- **Do not** file a question for missing values — backfill happens in a future spoiler-gating pass

Updated three places in the prompt: frontmatter table, hard constraints list, synthesis rules item 6, and the question-protocol section. Validator already deferred this check (intentional in spec).

This is a meaningful scope decision: spoiler gating was previously called "architectural, not optional" in the project principles. Reframing as a deferred backfill pass acknowledges that perfect upstream tagging would block too much production work for too little near-term value. The v1 wiki nodes will be open-canon (no spoiler gate) until a dedicated pass closes that gap.

## The smoke-test bug

Tried to run `weirwood wiki run core --bucket direwolves`. Got:

```
ERROR: Chapter directory not found: sources/chapters/wikisources/wiki
```

Followed two threads:

### Thread 1: The path is mangled because shell loaded an old `weirwood` function

Investigation: `~/.zshrc` is a symlink to `~/source/terminal-collection/zshrc`, which sources every `*.zsh` in `terminal-collection/functions/`. There were two copies of `weirwood.zsh`:
- `~/source/terminal-collection/functions/weirwood.zsh` (OLD — no `wiki` subcommand)
- `~/source/asoiaf-chat/scripts/weirwood.zsh` (NEW — what we'd been editing)

The old terminal-collection version won because it was what the shell loader picked up. `weirwood wiki run core --bucket direwolves` fell through to the default `*)` case (treating "wiki" as a book name), called `extract.sh`, which mangled the args.

Fix: replaced `terminal-collection/functions/weirwood.zsh` with a one-line forwarder that sources the asoiaf-chat version. Single source of truth in the project repo.

Saved a memory: `reference_shell_function_loader.md` documenting the loader structure (terminal-collection sources functions, project repos own the implementation, project-owned funcs forward to repo source).

### Thread 2: The smoke test silently exits after orphan recovery

After fixing the forwarder, retry produced:

```
--- Reconciliation pass ---
--- Orphan recovery (threshold=60min) ---
mnoth@... source %
```

No "No pending buckets found" message, no error, no continuation. Script exits 0 between orphan recovery and the pending-manifest collection loop.

This is a real bug. `wiki-pass2.sh` runs under `set -euo pipefail`. Some command between orphan recovery and the manifest collection (probably `ensure_stats_csv`, `list_manifests`, or something in the loop body) returns nonzero and the shell silently exits.

NOT debugged this session — captured for the next session via the new continue prompt.

## Validator considerations Matt flagged

Matt's question on the validator: would building it before smoke create risk of the validator being wrong on first encounter and rejecting good output for cosmetic reasons? Real concern, mitigated by keeping the v1 validator narrow (only structural fields, not content quality). `first_available` deferred for the same reason — would have caused mass question-flooding without near-term value.

## Memory updates

- `reference_shell_function_loader.md` (NEW) — terminal-collection loader pattern
- `MEMORY.md` index updated

## What worked / what to keep

1. **Autonomous-session pattern is good for prep work.** Cold review + bug fix + agent-prompt write was ideal autonomous fodder — non-destructive, file-bound, well-scoped. Hard-stop before agent-launch step kept blast radius bounded. Will reuse.
2. **Cold review surfaces real bugs.** B1 path-mismatch was load-bearing; the build agent missed it. Worth the review-pass overhead.
3. **iTerm trigger via osascript is unreliable.** First trigger (autonomous prep) worked. Second trigger (smoke test launch) opened a tab but didn't fully fire the command — log only got "Reconciliation" + "Orphan recovery" before stopping, identical signature to the genuine launcher bug. Hard to tell trigger-issue from launcher-bug at a glance. Future autonomous launches should verify execution by polling the log, not just by invoking osascript.
4. **MEMORY.md gets denser; the loader memory is meta-infrastructure.** It's a category of memory I hadn't been writing — system-level "where stuff lives" — and that gap caused real friction this session (had to investigate the shell function structure under time pressure).

## Coverage / deliverables

- `scripts/wiki-pass2.sh` — B1 fix applied (path-normalize before lookup)
- `scripts/wiki-pass2-triage.py` — Arya fix applied (page-name match only)
- `scripts/wiki-pass2-validator.py` — NEW (~150 lines, smoke-tested)
- `.claude/agents/wiki-ingester.md` — promoted from 31-line stub to 180-line real prompt; `first_available` softened to optional
- `working/runbooks/wiki-pass2-orchestration-build-self-review.md` — NEW (3 blockers + 11 correctness + 4 maintenance + 2 doc-coupling notes)
- `terminal-collection/functions/weirwood.zsh` — replaced with forwarder
- `memory/reference_shell_function_loader.md` — NEW

Smoke test: not passing yet. Continue prompt at `progress/continue-prompts/2026-04-26-wiki-pass2-smoke-debug.md` captures the silent-exit bug and the verification sequence for the rest of the launch readiness work.
