# Running parallel sessions safely — shared tree vs. git worktrees

**Why this exists:** the project regularly runs two tracks in parallel windows (graph-enrichment + D&E Pass-1). By default they share **one git working tree** on `main`. The S132c worklog split decoupled their *logs*; it did **not** isolate their *workspaces*. This note is how to keep parallel sessions from stepping on each other.

## Default: shared working tree (what we do now)

Both sessions edit + commit in the same checkout on `main`. This is **fine** as long as:

- **Each session stages by explicit path — never `git add -A`.** (Baked into the `endsession` skill, step 10.) This is the single rule that stops one session's commit from sweeping up the other's uncommitted work. Verify the staged set before every commit (`git diff --cached --name-only`).
- **Sessions touch disjoint files.** The tracks are file-disjoint by design: graph track = `graph/` + `working/enrichment/` + `worklog.md`; D&E track = `working/dunk-egg-pass1/` + `worklog-dunk-egg.md`. The only shared surfaces are `worklog.md` / `CLAUDE.md` — edit those in small, disjoint regions and commit promptly.
- **Whoever commits moves `HEAD` under the other.** The other session just commits on top (linear history, no merge commit). A long-running session may be working from a now-stale in-context `worklog.md`/`CLAUDE.md` — at its endsession it should **re-read both** before writing its entry.

**Verdict:** for a solo dev, shared-tree + stage-by-path is sufficient for the common case. Reach for worktrees only if a real conflict/clobber actually happens, or before a run where both sessions will write the same area.

## Full isolation: git worktrees (the escalation)

A worktree is a second checkout that shares the same `.git` history but has its own working files on its own branch — so the two sessions can't touch each other's files at all.

```
# one-time, from the repo root, per parallel track:
git worktree add ../weirwood-de de-work     # new checkout at ../weirwood-de on a new branch 'de-work'

# run the D&E session with its cwd = ../weirwood-de
#   it reads/writes/commits entirely within that tree, on de-work — main's checkout is untouched

# when the parallel work is done, merge back + clean up:
git checkout main && git merge de-work      # log-split keeps this near-conflict-free
git worktree remove ../weirwood-de
git branch -d de-work
```

- Because the D&E session only edits `worklog-dunk-egg.md` + `working/dunk-egg-pass1/` (the split did this), the merge back to `main` is near-conflict-free.
- **Cost:** disk for a second checkout + you manage a branch and a merge. Overkill unless the tracks share a write-surface.

## Recommendation

Stay on **shared-tree + stage-by-path** while the tracks remain file-disjoint (current state). Adopt a **worktree** the moment two parallel sessions need to write the same area — e.g. two concurrent `graph/` mutation runs, or running D&E extraction while a graph session also rewrites `working/` artifacts.
