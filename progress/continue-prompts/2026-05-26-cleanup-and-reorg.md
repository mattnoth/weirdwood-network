# CONTINUE — Folder reorg + repo hygiene (and optional resolver recall lever)

**Recommended model:** Sonnet 4.6 (deterministic file moves + git hygiene; mechanical). Opus 4.7 only if you also take the optional resolver-recall lever (judgment on alias aggressiveness).

**Supersedes** the deleted top-level `CONTINUE-node-recovery-and-edges.md` — that work (node-gap correction, index rebuild, edges v1.2/v1.3, resolver title-person pass) is DONE and committed (`eb3c6b18b`, `4f149f7b6`). Full record: `history/session-details/session-072.md`. Trust `worklog.md` over this doc (CLAUDE.md #9).

---

## State going in (all committed, clean tree)

- `graph/edges/edges.jsonl` = **3,811** (v1.3). Frozen unless a new edge pass is deliberately run.
- `graph/index/` covers all 21 categories (rebuilt S72).
- Node layer is whole (the S71 "7,251 unpromoted backlog" was a false alarm — verified by slug intersection; only ~8 net-new, all dups of canonical nodes → intentionally NOT promoted).
- 814 tests green.

## Primary track — folder reorg (Matt's scratch item 2: "folders are dumps")

`working/wiki/` and `scripts/` accreted with no structure. Reorganize **by epic/theme**, carefully.

1. **`scripts/`** — dozens of `stage4-*.py` + `wiki-pass2-*.py` + `build-*.py` + one-off `classify-comention-*.py`. Propose themed subdirs (e.g. `scripts/stage4/`, `scripts/wiki-pass2/`, `scripts/indexing/`, `scripts/archive/` already exists). **CRITICAL:** many scripts import each other by relative filename via `load_script()`/`importlib` (e.g. `stage4-refine-v1-edges.py` loads `stage4-type-contract-validator.py` + `stage4-quote-relevance-filter.py`; `stage4-pass1-edge-candidates.py` imports `stage4_name_resolver`). Moving files **will break these imports + the test suite's `load_script` helper**. Either (a) keep import-coupled scripts together + update path constants, or (b) update every loader. **Run the full test suite after every move** (`python3 -m unittest discover -s tests -p 'test_*.py'` — expect 814 green). Do NOT move without re-greening.
2. **`working/wiki/`** — see `working/wiki/README.md` first. `data/` (permanent products), `pass2-buckets/` (536 bucket workspaces + the gitignored `pass1-derived/` staging), `pass2-staging/`. Mostly leave `pass2-buckets/` (large, gitignored staging); focus any tidy on stray top-level files.
3. **Leftover git worktrees (clutter):** `.claude/worktrees/{mystifying-burnell-56ee9c, admiring-benz-fa26f8}` — old worktrees on branch `claude/*`. Verify nothing uncommitted in them (`git -C <path> status`), then `git worktree remove <path>` (or `--force` if clean-but-locked). The `mystifying-burnell` one carries a stale CLAUDE.md copy (says `/endsession` triages scratch — the live one says it does NOT).

## Secondary — scratch untrack (Matt's item 0.1)

Two scratch files are git-**tracked** despite the `.gitignore scratch*` rule (line 34): `scratch-do-not-delete.txt`, `scratch-stage4-considerations-haiku.txt`. Untrack WITHOUT deleting from disk:
```
git rm --cached scratch-do-not-delete.txt scratch-stage4-considerations-haiku.txt
```
(One is literally named "do-not-delete" — `--cached` only, never delete the file.) Also drop the stale `.gitignore` line-11 comment "(only /endsession triages it)" — the live rule is scratch is NEVER triaged.

## Optional — resolver RECALL lever (distinct from S72's precision pass)

S72 fixed resolver *precision* (title-person collisions). The open *recall* lever from S67: ~387 unresolved + ~651 ambiguous edge endpoints. Two measured-but-unimplemented sub-levers (Matt's "how aggressive" call): a full-surname resolution rung (~72 endpoints) and a common-leading-word index-pollution filter (~417). Reasoning-heavy → Opus, and needs Matt's aggressiveness decision. See `progress/continue-prompts/2026-05-23-stage4-pass1-finishing.md` for the original framing.

## DO NOT
- Move import-coupled scripts without updating loaders + re-greening the 814-test suite.
- Delete anything from `sources/` or `extractions/archives/` (read-only/additive; archives permanent).
- Clobber `graph/edges/edges.jsonl` (frozen v1.3) or re-run an edge build unless deliberately starting a new versioned pass.
- Refetch the wiki. Run `/endsession` without explicit permission.
