---
session: 39
date: 2026-05-07
model: claude-opus-4-7 (1M context)
type: design + reorg
duration: ~1.5 hr
---

# Session 39 — Status check, naming reorg, working/wiki/ subtree

## Frame

Matt opened with: "Status update. How are we doing? I'm a bit overwhelmed. The repo looks much cleaner but still, overwhelmed. Can you help me think of better names for wiki-parsed & wiki-pass2." Two threads in one message — a stocktake request and a naming-clarity request.

## Status synthesis Matt got

The honest read: **the project is in good shape**, the overwhelm is from menu-width, not from broken state.

- Pass 1 v3 = 344/344 across all 5 books (foundation done)
- Wiki Pass 2 = 7,563 graph nodes across Stages 1, 3, Path B; edge vocab clean; citation audit clean
- Mention-index built Session 38 = 70% chapter-mention resolution (graph-traversal infrastructure now exists)
- Two cleanup scrubs landed in Session 37 (D&D framing, copyright textual rule)
- Working tree is clean before this session — last 5 commits all hygiene/structure

Why it feels heavy: three live continue prompts + model-fit recommendations awaiting approval + an Okey ASOS branch that I claimed was unmerged.

## Correction: ASOS was already merged

I told Matt the Okey ASOS branch was unmerged. He pushed back. Verified: commit `2eaf5c71 "Merge ASOS Pass 1 v3 from Okey's parallel run"` did the merge. Worklog Session 35's "Branch not yet merged to main" was true at that session but was overtaken by a subsequent merge commit, and I read the entry without checking git log.

**Lesson:** when a worklog entry makes a forward claim ("not yet merged"), check `git log` for what came after that session, not just the entry.

Worklog Session 35 patched on the spot to record the merge commit.

## Naming-rename progression

Walked through three options:

**Option A** — minimum effort: `wiki-parsed/` → `wiki-derived/`, `wiki-pass2/` → `wiki-pass2-buckets/`. Two `git mv`s. Lowest churn.

**Option B** — split-and-rename: separate permanent reference layer (`wiki-data/`) from run artifacts (`wiki-pass2-buckets/` absorbing the staging files). Clearer mental model, more script-path edits.

**Option C** — role-not-stage names: `wiki-tables/` and `wiki-promotion-runs/`. Most accurate to what the contents *are*; biggest churn.

I recommended Option A initially (overwhelm-conservative). Matt's pushback surfaced two things I hadn't weighed:

1. He was honest: "Why don't you like option C?" — I was being overcautious. I admitted Option C was actually stronger on the merits, just bigger churn.
2. **He proposed `working/wiki/` as a parent directory** — pass-numbers become *children* of the wiki domain rather than top-level siblings. This is the cleanest framing: "pass2" is scoped to the wiki pipeline, not to the whole project.

That became **Option D**:

```
working/wiki/
  ├── data/           # alias-resolver, infobox-data, page-index, page-categories,
  │                   # cross-references, chronology-events, backlink-counts, etc.
  ├── pass2-buckets/  # 536 per-bucket workspaces from Stages 1+3
  └── pass2-staging/  # triage-*, draft-buckets, stage3*-summary, priority-summary
```

Option D was approved. Future passes get a natural home (`pass4-prose-edges/`, etc.).

## Food/dialogue cost question (design discussion, no code)

Matt asked: "will [the food/dialogue/events pass] be as bad as the full book passes, or does the python help us be more discrete about this?"

Answer I gave (preserved here for future reference):

The mention-index changes the math substantially. Pass 1 had to scan every chapter blind looking for *everything*. The mention-index changes the question from "is there food in this chapter?" to "this chapter has 7 Food & Drink entries — extract the meal scenes around them."

Concrete savings:
- **Targeting**: LLM only opens chapters where mention-index already flags ≥N food references. Solo "she ate bread" mentions get skipped; the Wedding feast scenes get focus.
- **Scoping the prompt**: instead of 12-category extraction, prompts become single-purpose ("for this scene, extract: who's at table, what's served, who hosts, was guest-right invoked, what gets discussed"). Tighter prompt = fewer output tokens.
- **Scene-level chunking**: LLM operates on scenes (~hundreds of lines), not whole chapters (1500-4000 lines). Fewer input tokens per call.
- **Sampling oracle pattern** (already in dialogue/meals continue prompt): Opus on small validation sample, Sonnet/Haiku on bulk run.

Order-of-magnitude: meals + dialogue + events on Pass-1-augmented corpus = **~$10-25/book on Sonnet**, vs ~$50/book for blind Pass 1 on Opus. Mention-index earned its keep.

But: still need an LLM pass to verify. Python made name-level decisions only. It never decided whether "she gnawed a heel of bread" is a meal scene vs. a memory-of-food vs. a passing reference. Reasoning is irreducible there.

## "Mentions" naming

Matt: "the readme should probably make this clear, the directory i mean - like 'mentions' is not just for people."

Confirmed: the actual directory is `graph/index/chapters/` (Session 38), not `mentions/`. Each file lists every named entity surfaced in the chapter — characters, locations, artifacts, food, etc. The word "mention" only shows up in concept docs, not the path.

Decided: **don't rename, but write a README**. The technical "mention" term is fine once explained. Renaming would collide with the existing `reference/` directory. Added to todos.

## Reorg execution

Matt approved Option D. Executed across 6 tracked tasks:

1. **Move 9 permanent files** to `working/wiki/data/` via `git mv`.
2. **Move 7 staging files** to `working/wiki/pass2-staging/` via `git mv`.
3. **Move all 536 buckets** via `git mv working/wiki-pass2 working/wiki/pass2-buckets`.
4. **Update script paths** — three-step targeted sed:
   - First fix Python `Path` concat for staging files (`"wiki-parsed" / "<staging>"` → `"wiki" / "pass2-staging" / "<staging>"`)
   - Catch-all for remaining `"wiki-parsed"` → `"wiki" / "data"`
   - `"wiki-pass2"` → `"wiki" / "pass2-buckets"` (quoted form only, won't break filenames like `wiki-pass2-triage.py`)
5. **Update doc paths** — same three-step sed against 33 live `.md` and `.zsh` files.
6. **Write `working/wiki/README.md`** explaining the data/staging/buckets split.

**Frozen records left untouched** (per the spirit of Matt's "don't edit historical archives" hook idea): `history/**`, `progress/continue-prompts/archive/**`, `working/audits/**`, `working/runbooks/archive/**`, `scripts/archive/**`. README explicitly notes that historical paths are preserved as-written.

## Verification

- `python3 scripts/build-mention-index.py --book agot --dry-run` runs cleanly against new paths
- Final grep check: only remaining live refs are script *filenames* (correct — those scripts haven't moved) plus one doc reference to the named "wiki-pass2 pipeline" of scripts (also correct)
- `git status --short`: 14,141 renames + 65 modifications + 1 untracked (the new README)

## Sed pitfall (lesson learned mid-execution)

The first sed pass only matched slash-form paths (`working/wiki-parsed/`). Python scripts use `Path` concatenation with quoted components (`"working" / "wiki-parsed" / "alias-resolver.json"`) which the slash pattern missed. Caught when grep showed remaining hits in `scripts/build-mention-index.py:50`.

The naive fix — bare `wiki-parsed` → `wiki/data` — would have broken script *filenames* like `wiki-pass2-triage.py` (becoming `wiki/pass2-buckets-triage.py`).

The fix that worked: only match the **quoted form** `"wiki-parsed"` and `"wiki-pass2"`. That matches Path components but not bare filenames.

## What didn't get done

- **No commit.** /endsession doesn't auto-commit, and Matt didn't explicitly authorize one. The reorg sits in the working tree as 14,141 renames + 65 modifications + 1 new README.
- **`graph/index/chapters/README.md`** — agreed it should be written; not done. Added to todos.
- **The food/dialogue/events pass itself** — design discussion only, no execution.

## Files changed

**New:**
- `working/wiki/README.md`
- `working/wiki/data/` (9 files, all renamed in)
- `working/wiki/pass2-staging/` (7 files, renamed in)
- `working/wiki/pass2-buckets/` (536 buckets, all renamed in)

**Modified (65 files):**
- `CLAUDE.md` (directory structure diagram + path refs)
- `worklog.md` (Session 35 ASOS-merge correction + path refs)
- 14 `.claude/agents/*.md`
- 2 `.claude/commands/*.md`
- 4 `reference/*.md`
- 3 `working/runbooks/` (live, non-archive)
- 3 `working/agent-fleet-specs/`
- `working/todos.md`, `working/tier3-promotion-plan.md`
- 2 active `progress/continue-prompts/*.md`
- ~32 `scripts/*.py|*.sh|*.zsh` (excluding archive/)

**Deleted:**
- `working/wiki-parsed/` (now-empty after moves)

## Next session decision menu (what's actually queued)

1. **Commit the reorg.** Single commit, suggested message in the conversation.
2. **Alias-backfill from Session 38 mention-index** — top-20 unresolved patterns; expected to lift resolution past 75%. Cheap.
3. **Stage 4 prose-edge-classifier** (continue prompt: `2026-05-02-stage4-v1-prose-edge-classifier.md`).
4. **Dialogue/meals/mention-index design** continue prompt — design pass + smoke test. (`2026-05-05-dialogue-meals-mention-index-design.md`).
5. **Model-fit recommendations** queued for Matt's review before agent prompt frontmatter changes.
6. **Two PreToolUse hooks** queued: block edits to historical archives, block edits under sources/.

Smallest unit-of-work that finishes a thread: option 2 (alias-backfill).
