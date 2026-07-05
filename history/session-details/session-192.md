---
session: 192
date: 2026-07-04
model: Fable 5 (solo — no subagents; spend-ceiling caution from S191)
track: meta/graph
---

# Session 192 — Class-5 dup-slug apply + hardening + next-steps planning

The Matt-proposed "short Fable cleanup + next-steps planning" half-session that grew a
graph-mutation apply in the middle — because Matt answered the class-5 questions
in-session ("apply this session", all recommendations accepted) instead of re-parking.

## Part 1 — cleanup as planned

- **`cwd_is_tmp` was never environmental.** The failing test asserted `cwd == "/tmp"`
  but S83 (`149e32129d`) moved `claude -p`'s working dir to `~/source/claude-cwd` and
  the test was never updated. Fixed the test to assert `tc.CLAUDE_P_CWD` + an
  outside-the-repo check (the actual invariant). Suite fully green for the first time
  in memory: **pytest 1447 passed / 1 skip / 0 fail**.
- **Mini-fixture doubled-article alias keys:** five stored keys (not two — the continue
  prompt undercounted) carried a literal leading "the "/"a ", unreachable because
  `normalize()` strips one article from the query side. Dropped the stored articles,
  rewrote the test comment, added a real hit case (`"The Salt Debt"` → `salt-debt-massacre`).

## The class-5 apply (Matt-approved via AskUserQuestion, all recommendations)

Approval surface = the S190 checkboxes + the reconciliation file's 3 amendments.
Matt's picks: apply this session (incl. deploy) · 5a **medical/ canonical** ·
amendments 1&3 accepted (5g `concept.prophecy`, 5b species/ canonical) · 5d
**character → `porridge-gaoler`** (the lamprey-gaoler precedent; bare "porridge" now
resolves to the food — verified). The character was renamed `Porridge (gaoler)`
following the wiki's own disambiguation style; 4 edges rewritten.

**Two things the apply surfaced that neither scan had:**

1. **An 8th dup:** the 5c rename target `renlys-peach` already existed as a
   wiki-promoted `artifacts/` node (the wiki has a literal "Renly's peach" page).
   Same entity as the harvest food node → merged with the exact fold-content pattern
   Matt had just approved three times. Graph-wide dup slugs now **zero**.
2. **The `_conflicts/` bundle leak (the session's real find):** the new fail-loud
   guard in `load_nodes()` tripped instantly on `graph/nodes/_conflicts/` — the
   builder's `rglob` had been walking the unresolved-duplicate stash all along
   (`build_search_index.py` excludes it; the bundle builder didn't). Impact measured:
   **7 phantom slugs with no live counterpart were shipping in the live bundle**
   (incl. `aerys-targaryen` and `battle-of-the-green-fork` — stale wiki promotions
   whose live equivalents have different slugs). Sorted-walk luck (`_conflicts` sorts
   first, live copies overwrote) kept the damage to phantom-only. Excluded + guarded.

Hardening (ungated, per the reconciliation): `load_nodes` + `build_search_index`
fail loudly on dup slugs; `find_node_file` + `build_node_index` sorted walk with
deterministic first-wins + stderr collision warning (engine warns, builders die).

Close-out: `weirwood refresh` clean; 8,119 timestamp-only index restamps reverted
(S165 rule); 8 orphaned index files of deleted nodes removed; bundle rebuilt;
**prod deployed + live-verified** (`porridge`→food, `porridge-gaoler`→character,
`renlys-peach`→merged node, phantoms 404, `aerys-ii-targaryen` intact). Worktree
`vigilant-chebyshev` landed (its scan record → `curation/`) and removed with its branch.

## Part 2 — planning

Ranked the parked queue; Matt engaged the **side-window receipts + node UX** track
with concrete design steer (neighbors card's `▶ details` pattern inconsistent with
click-opens-dossier; "styling needs a big boost"; modals showing node markdown fine;
prose entity-linking — assessed as 3 tiers, tier 1 client-only is cheap). Then his
"one more Fable session" question re-opened the pick: recommended **quote minting +
dossier substance** (S188 census: quotes ~73% characters vs ~3% descriptive; theme
tool now routes users at empty dossiers) as the better Fable spend vs granular dips
or front-end-on-Fable. **Matt picked it.** Final sequence: **S193 quotes (Fable) →
S194 receipts/node-UX (Opus)** — fill the dossiers, then make them reachable. His
"good for the about" note became S194 step 6 (About-page provenance story, also
closing the S187 About-copy carry-over).

Deferred/noted: 8d SERVED_AT stays gated (live evidence ~1 day old); the
`stallion who mounts the world` → `rhaego` character-alias precedence quirk observed
(pre-existing, not a regression — left alone).
