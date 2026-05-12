# Handoff — Alias-Backfill Round 2 (Shape B: single session-task)

**Created:** 2026-05-12 (Session 45)
**Parallel-safe with:** `2026-05-12-case-collision-mission.md` (different file write-sets; can run concurrently in another window)
**Sequential prerequisite:** none
**Source todo:** `working/todos.md` "Tiny Follow-ups (Session 40 surface)" → "Second round of alias-backfill (the-vale, maester-aemon, etc.)"

This is a deterministic session-task. NOT a mission — single window, no watcher needed, no quality variance worth scaffolding for.

---

## Model

**Sonnet 4.6.** Pure frontmatter edits + script reruns; Opus wasteful here. Haiku 4.5 viable but Sonnet's better at carefully reading existing YAML before patching.

---

## Steps

1. **Verify the two Aemon canonical slugs exist:**
   ```bash
   ls graph/nodes/characters/aemon-targaryen-maester.node.md
   ls graph/nodes/characters/aemon-targaryen-dragonknight.node.md
   ```
   - If either doesn't exist: skip that one, file a follow-up todo at `working/todos.md` under "Tiny Follow-ups" noting "canonical slug X not in graph; alias-backfill for it skipped on <date>", report back to Matt at end.

2. **For each existing canonical slug, add ONE alias to its `aliases:` frontmatter list:**

   | Canonical node | Alias to add |
   |---|---|
   | `graph/nodes/locations/vale-of-arryn.node.md` | `"The Vale"` |
   | `graph/nodes/characters/aemon-targaryen-maester.node.md` | `"Maester Aemon"` |
   | `graph/nodes/characters/aemon-targaryen-dragonknight.node.md` | `"Prince Aemon the Dragonknight"` |

   Use the `Edit` tool — append to the existing `aliases:` array. Two YAML forms are common:
   - Inline: `aliases: ["Existing Alias", "The Vale"]`
   - Block:
     ```yaml
     aliases:
       - Existing Alias
       - The Vale
     ```

   Match whichever form the node currently uses. Don't change form.

3. **Rebuild the alias-resolver:**
   ```bash
   python3 scripts/wiki-pass2-build-alias-resolver.py --apply
   ```
   Expected delta in stdout: 3 new alias_to_canonical entries (or fewer if any Aemon slug was skipped).

4. **Rebuild the mention-index:**
   ```bash
   python3 scripts/build-mention-index.py --all
   ```
   Reads each chapter's Pass 1 extraction, resolves entity mentions against the alias-resolver. Writes 344 `mentions.json` files.

5. **Report the resolution-rate delta:**
   ```bash
   python3 -c "
   import json
   s = json.load(open('graph/index/chapters/_summary.json'))
   print(f\"Resolution rate: {s.get('resolution_rate_pct', 'unknown')}%\")
   "
   ```
   Expected: 70.6% → ~72-74% (these 3 aliases account for ~119 newly-resolved mentions).

6. **Update artifacts:**
   - `working/todos.md` "Tiny Follow-ups" → mark "Second round of alias-backfill" DONE with the actual delta.
   - `worklog.md` → add a Session entry (~10 lines) following the standard format.

---

## DO NOT

- Touch Stage 4 prose-edge artifacts (`working/wiki/pass2-buckets/*/prose-edges/`).
- Touch the case-collision mission scratch dirs (`working/missions/case-collision-top-10/`).
- Refetch any wiki page.
- Auto-run `/endsession`.
- Create new graph nodes — this is alias-only work.

---

## If something goes wrong

- Alias-resolver script fails: check for YAML parse errors in the 3 nodes you edited. Frontmatter-malformed nodes will crash it.
- Mention-index script reports the resolution rate didn't move: verify the 3 alias additions actually landed in frontmatter (`grep -A2 "aliases:" graph/nodes/locations/vale-of-arryn.node.md` etc.). If the YAML form was wrong, the script might silently skip.
- Either Aemon slug doesn't exist: that's fine, follow the skip-and-file-todo path in step 1.

Cheap session, expected ~15-30 min wall-clock.
