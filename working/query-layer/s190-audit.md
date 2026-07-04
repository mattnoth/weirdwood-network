# S190 Post-Session Audit

**Auditor pass, 2026-07-04, read-only except this file.** Scope: 9 commits `adae223e00..0408819e20`
(query-layer engine build + retrieval + close-out + the Matt-approved class-1/mention-index applies).

## Verdict: CLEAN

No gate violations, no misplaced writes, no debris to delete, all four suites at expected
tallies, docs consistent modulo the one pre-flagged worklog lag (which is expected and will
be closed by endsession, not a new finding).

---

## 1. Gates held

- `graph/nodes/` — exactly the 5 approved class-1 alias repairs touched (`blood-butcher`,
  `cheese-ratcatcher`, `jacaerys-velaryon`, `shepherd-reborn`, `tyrion-tanner`). Diffed each:
  every change is `aliases: [""X""]` → `aliases: ["\"X\""]` (inner-quote escaping only) — alias
  **content** unchanged, confirms the "class 1 = YAML-parse repair, not a data edit" claim.
- `graph/edges/` — only `README.md` touched (doc text: edge-count note, "since grown" framing).
  Zero rows in `edges.jsonl` changed.
- `graph/convergence-maps/` — untouched (git log empty for the path across the range).
- `sources/` — untouched (git log empty for the path across the range).
- Everything else in the 1,505-line stat is `graph/index/` (chapters/artifacts/characters
  mention-data regen — the approved mention-index apply), `graph/query/` (the new engine),
  `working/query-layer/`, `web/src/lib` + `web/netlify/edge-functions/lib` (TS port),
  `CLAUDE.md`/`.gitignore` (doc/config), `worklog.md`, and one `history/worklog-archives/`
  rotation. No surprises.

## 2. Working tree state

`git status --porcelain`:
```
 M working/query-layer/design.md
 M working/query-layer/variant-collisions-s190.md
?? scr
?? working/query-layer/hygiene-proposal-s190-reconciliation.md
```
- `scr` — Matt's private file. Not read, not touched. Correctly untracked/gitignored-by-convention.
- `working/query-layer/design.md` diff — Matt's live in-session ruling on the 3 open persona
  knobs (flat register deliberate / tool-grounded reasoning / no A/B eval). Legitimate close-out
  annotation, not drift.
- `working/query-layer/variant-collisions-s190.md` diff — re-run after the cheese-ratcatcher
  class-1 fix landed (156→155 collisions, the `the cheese` collision resolved). Expected,
  matches the apply.
- `working/query-layer/hygiene-proposal-s190-reconciliation.md` — new file reconciling the S190
  hygiene proposal against the parallel dup-slug worktree session's independent scan. Read it:
  legitimate cross-session reconciliation (both scans cross-validate on 7 collisions), not debris.
- **Dup-slug worktree check:** `git worktree list` confirms `.claude/worktrees/vigilant-chebyshev-9cacb3`
  is a separate, still-checked-out worktree (branch `claude/vigilant-chebyshev-9cacb3`,
  `f8c30f2886`). None of the 7 named dup-slug node pairs (sweetsleep/peach/porridge/sourleaf/
  stallion-who-mounts-the-world/ASOS-prologue/ASOS-epilogue — 15 files found on disk) show up in
  `git status` here — confirmed NOT locally modified in this working tree. No flag needed.
- `.claude/settings.local.json`, `.DS_Store` files, `__pycache__`, `.netlify/`, `web/data/`,
  `web/public/data/`, `web/public/node/` — all pre-existing/gitignored derived output, none
  session-created debris (`settings.local.json` mtime is 2026-06-10, well before S190).

## 3. Consistency spot-checks

- **`graph/query/README.md`** — directory map + module list verified against the actual tree
  (`find graph/query -maxdepth 3`): every file it names exists, nothing extra/missing.
- **`worklog.md` S190 entry** — accurate for what it narrates ("no graph writes anywhere" was
  true at the time it was written), but predates the class-1 + mention-index APPLIES that
  landed after in `0408819e20`. This is the one known/pre-flagged lag from the task brief —
  endsession will amend it. No OTHER staleness found in the entry.
- **`working/todos.md` Track 7 block** — S190 sub-bullet matches reality: engine shipped,
  resolver hardening numbers match (10/20→17/21 in todos vs 10/20→16/20 exact in worklog — todos
  says "17/21" combining a later count; not a contradiction, just a different snapshot moment,
  both internally cited). Continue-prompt pointer and Matt-gated-applies list both correct.
- **`spec/operations.md` op table** — all 16 rows checked against shipped files: every ✅ Python
  cell names a real module in `weirwood_query/` or `build/` (verified all exist), every status
  tag ("SHIPPED — step N") is internally consistent with the README's session log. No rows
  claim a module that isn't on disk.
- **`progress/continue-prompts/`** — exactly two live prompts:
  `2026-07-04-query-layer-final-pytest-suite.md` and `2026-06-29-dunk-egg-pass1-smoke.md`
  (the parked D&E smoke), plus `README.md` and `archive/` (104 files). Matches spec.

## 4. Suites

| Suite | Result | Expected | Match |
|---|---|---|---|
| `pytest tests/ -q` | 1322 passed, 3 failed | 1322/3 pre-existing | YES |
| — failures | `test_vocab_count_is_167` ×2, `test_cwd_is_tmp` | vocab-167-vs-170 ×2 + cwd-is-tmp | YES |
| `cd web && deno task test` | 98 passed, 0 failed, 1 ignored | 98/0/1 | YES |
| `PYTHONPATH=graph/query python3 graph/query/spec/run_cases.py` | 37 passed, 0 failed, 1 skipped | 37/0/1 | YES |
| `scripts/weirwood-refresh.sh --check` | "derived artifacts newer than every node — no refresh needed"; "mention-index newer than every node" | fresh (mention-index just applied) | YES |

Note: vocab-count failure is now 170 (not 167) — the test docstring's own history table already
tracks this drift lineage (163→166→167); this is the pre-existing, documented failure, not new.

## 5. Leftover-file sweep

`working/query-layer/` — every file is a deliberate S190 artifact: `design.md`, `measurements.md`,
`alias-table-diff-s190.md`, `variant-collisions-s190.md`, `resolve-misses.md`,
`hygiene-proposal-s190.md` + its reconciliation, `mention-index-repair-report.md`,
`mention-index-preview/` (KEEP, apply provenance), `food-grep-candidates.md` (4,865-row pointer
pool, step 8c), `boards/` (5 files, matches the 5 named board decisions), `evals/` (baseline +
3 post-step eval snapshots + harness script). Nothing orphaned.

Repo root + `scripts/`: files newer than today 00:00 are all legitimate (worklog.md,
CLAUDE.md, GRAPH-STATE.md, GRAPH-QUERY-ROADMAP.md, .gitignore; scripts/weirwood-refresh.sh,
weirwood.zsh, food-grep-seeder.py, graph-query.py + event_alias_resolver.py shims,
build-chat-export.py, README.md) — all already accounted for in the commit range. No stray
script or scratch file found. Nothing was found written to `/tmp` outside the session's own
scratchpad usage.

## 6. Harvest queue

`working/harvest-queue.md`: **1 open row**, 86 parked (excluded from trigger count), 843 done.
Nowhere near the 20-row drain threshold.
