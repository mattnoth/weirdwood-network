---
session: 42
date: 2026-05-12
title: Wiki prose extraction backfill (Track 1)
model: claude-opus-4-7 (1M context)
duration: ~1 session
cost: $0 (pure Python)
worklog_entry: yes
---

# Session 42 — Wiki prose extraction backfill (Track 1 of three parallel-runnable tracks)

## What this session was

Track 1 of three tracks queued in `next.md` after Session 41. Goal: close the apparent 79% stub-only depth gap on graph nodes by re-running prose attachment against `pass_origin: pass2-wiki-deterministic` nodes. The continue prompt (`progress/continue-prompts/2026-05-12-wiki-prose-extraction-backfill.md`) was explicit that the first step should be a 15-minute investigation — don't just trust the premise — because the gap could be:
- prose was extracted but never promoted (in which case: re-run promote)
- prose was never extracted (in which case: run extractor first)
- prose was extracted and promoted but a later script overwrote the body (in which case: figure out what overwrote it)

## The investigation step

Sampled 10 stub-only nodes (non-Stage-1, by frontmatter `pass_origin`) and checked whether each had a corresponding `.prose.md` file in any `working/wiki/pass2-buckets/*/prose/` directory. Quick probe via inline Python — counted **4,726 stub-only deterministic nodes**, of which **3,939 (83%) had non-empty prose files already in their buckets**. Only 787 lacked prose entirely.

So the gap shape was clear: most of the work was just "concatenate skeleton + prose into the graph node, which somebody/something did once but the result didn't stick."

### Why the prose didn't stick (theory)

Tried to nail down a root cause. Walked through the scripts:
- `wiki-pass2-extract-prose.py` → emits prose files to bucket. ✅ Ran in Session 26.
- `wiki-pass2-promote.py` → concatenates skeleton + prose → graph node. ✅ Ran in Session 26.
- `wiki-pass2-fix-date-bleed-remaining.py` → Session 27 corrective pass. Re-rendered skeleton + concatenates prose if `prose_path.exists()`. ✅ Same shape.
- `wiki-pass2-repromote-targeted.py` → same shape.
- `wiki-pass2-tier3-pathb-*.py` → emits skeleton + extracts prose + concatenates. ✅

Picked `walgrave` as the test case (one of the AFFC prologue Citadel novices/archmaesters from the continue prompt's suggested smoke-test set). Findings:
- Skeleton at `working/wiki/pass2-buckets/characters-other-v-w/skeleton/walgrave.node.md`: pre-date-bleed-fix form (`BORN_AT: 198 AC`).
- Prose at `working/wiki/pass2-buckets/characters-other-v-w/prose/walgrave.prose.md`: 4,168 bytes of real content.
- Graph node at `graph/nodes/characters/walgrave.node.md`: 519 bytes, stub-only. BUT the `BORN_AT` field reads `After 198 AC (track_b: Born) [198 AC]` — the **post-fix** form.

So `wiki-pass2-fix-date-bleed-remaining.py` did touch walgrave's graph node (skeleton got the date-bleed correction) but somehow the prose-concat step didn't land on disk. Ran the fixer's logic in dry-run today — all the lookups (page_to_bucket, infobox_data, prose_path.exists) return correctly. So either:
- The prose file didn't exist *at the time the fixer ran* (i.e., extraction ran in a later commit), OR
- The fixer had a bug in that prior version that's since been fixed, OR
- The fixer's atomic-write was preceded by another write that won the race.

Couldn't reproduce. Stopped chasing — the fix is mechanical regardless of why the failure happened, and re-running cleanly resolves it.

## The over-count surprise

Continue prompt cited "5,975 (79%) have stub-only Identity" from Session 41's per-character-index audit. When I ran my fresh audit with the same regex, I got 4,726, then 2,030 after a tightened detector. After running the attach script: 1,086, then 1,019 after a final tightening.

Why the over-count? My initial stub regex matched any body containing `"X is a Y from the AWOIAF wiki."` — but **nodes that already had prose ALSO had that line** (the Identity section's intro line). The original 5,975 count was probably from a similar permissive regex. The accurate stub-detector needs to check for the *absence* of prose-section headers (`## Origins`, `## Narrative Arc`, `## Appearances`, `## Culture`, `## Organization`, `## Quotes`, `## Aftermath`).

This is worth flagging because the next agent reading the worklog might believe "5,975 nodes were stubs and got prose" — but it was always 2,030 real stubs, of which 1,011 were closable here. The other 1,019 are genuinely empty-prose wiki pages (very short stubs, disambiguation pages, list articles, short title pages).

## Design decision: append vs rebuild

The bucket's skeleton (older form, pre-date-bleed-fix) is NOT what we want to write back. The current graph node carries late-stage parser-fix Edges that the bucket skeleton doesn't have. Options:

**(A)** Re-render skeleton from `working/wiki/data/infobox-data.jsonl` (today's freshest data) + concatenate prose. Like the existing fixers do.

**(B)** Take the current graph node body verbatim + append `\n + prose_bytes`. Preserves whatever the current state is, ignores the bucket skeleton entirely.

Chose **(B)** because:
- The current node already has Stage 3c corrections (date-bleed, religion-bleed, etc.) baked in.
- Re-rendering would re-run the parser on the infobox-data, and if any new parser bugs landed after Session 27 (none known), they'd flow into the result.
- (B) is strictly additive — the only thing that changes is the body grows with prose. No fields are rewritten.
- Idempotent: secondary check is "does the current body contain any prose section header? If yes, skip."

This is the design encoded in `scripts/wiki-pass2-attach-prose.py`.

## Walgrave before/after

**Before** (519 bytes):
```
---
name: "Walgrave"
type: character.human
slug: walgrave
...
pass_origin: pass2-wiki-deterministic
---

## Identity

Walgrave is a character.human from the AWOIAF wiki.

## Edges

- HOLDS_TITLE: Archmaester (track_b: Title)
- SWORN_TO: Citadel (track_b: Allegiance)
- CULTURE_OF: Reach (track_b: Culture)
- BORN_AT: After 198 AC (track_b: Born) [198 AC]
```

**After** (4,688 bytes): same frontmatter and Edges, plus:

- `## Origins` (paragraphs on Walgrave's reputation in ravencraft, his book *Black Wings, Swift Words*, his decline into senility, his strongbox containing a key that opens any door in the Citadel)
- `## Appearances & Description` (his ring/rod/mask are black iron — denoting ravencraft expertise)
- `## Narrative Arc` with `### A Feast for Crows` subheading (Pate's theft of his archmaester's key, the alchemist plot, Walgrave's selection as Seneschal of the Citadel)
- All cite_refs preserved as `(wiki:Walgrave.cite_ref-X)` for downstream resolution.

## Why dependent-index rebuilds yielded zero content changes

Re-ran the alias-resolver, mention-index, and character-index builders. All three regenerated 5,000+ files but the only diff was the `generated_at` timestamps.

Reasoning:
- **alias-resolver** reads frontmatter `aliases:[...]` fields. Prose attachment didn't touch frontmatter. → No change.
- **mention-index** reads Pass-1 chapter extractions, slugifies entity names, and resolves via the alias-resolver. None of those inputs changed. → No change.
- **character-index** reads `## Edges` from each node for `out_edge_count` + `backlink-counts.json` for `in_edge_count`. Prose attachment didn't touch ## Edges blocks; backlink-counts.json derives from wiki HTML cross-references, not node bodies. → No change.

So the rebuilds confirmed correctness (nothing broke) but produced only timestamp churn. Reverted the timestamp-only diffs to keep this session's commit focused on the actual prose attachments.

This is a useful confirmation for the next agent: **rebuilding dependent indexes after a body-only graph-node change is a no-op for content but useful for verifying nothing downstream broke.**

## The 1,019 remaining stub-only nodes

Type breakdown:
- 361 character.human (mostly minor named characters with very short wiki entries)
- 223 place.location (one-line geographic references)
- 126 title (short title definitions; "Paymaster", "Lord of the Red Dunes")
- 27 species
- 30 event.* (battles and wars without expanded wiki articles)
- 23 concept.* (medical/custom/language) — these are dictionary-style stubs
- 8 organization.house (cadet/minor houses)
- ~10 misc

Sampled 10 of these and confirmed: their wiki cache files are 1-2 KB of HTML, contain an infobox + a single sentence definition + maybe a "See also" — no mappable H2 sections like History/Background/Recent Events. The prose extractor correctly emits no file (or an empty file) for these.

206 of the 1,019 are the case-collision redirect-only caches (separate todo since Session 41).

## What was discarded

- **Track 4 (run extractor for missing-prose nodes)** from the task list was closed-as-unnecessary after sampling confirmed the 813 non-case-collision missing-prose nodes are genuinely empty pages, not extraction gaps.
- The audit's initial loose stub regex was used twice (once for the over-count, once before tightening). Both were instructive but not load-bearing.

## Mid-session asides from Matt

- **"possibly has something to do with our concept pages we didnt do? or did we i think"** — Concept-type nodes (concepts/, theories/, prophecies/, languages/, medical/, customs/, species/) all got prose. Only 23 concept.* nodes remain stub-only, and they're genuinely-short dictionary-style entries.
- **"quotes are great, esp if we can find them to surface in the chat, idk just a thought"** — `## Quotes` sections on the newly-attached nodes carry chapter cite_refs (`(wiki:NodeName.cite_ref-Rasos27)` etc.). These could feed a future query-UI evidence pane. Filed as a "Defer / low priority" entry in next.md.

## Next-session handoff

Tracks 2 and 3 from next.md are now the natural next steps, both independent. Track 2 (138 Bucket A missing-node backfill) and Track 3 (per-LOCATION + per-ARTIFACT index roll-ups) can run in parallel. Continue prompts written to `progress/continue-prompts/` this session.

## Files changed this session

- NEW: `scripts/audit-prose-coverage.py` (read-only audit, ~200 LOC)
- NEW: `scripts/wiki-pass2-attach-prose.py` (in-place attacher, ~210 LOC)
- NEW: `working/audits/wiki-prose-coverage-2026-05-12/execution/{coverage.jsonl, summary.md, attach-prose-summary.json}`
- MODIFIED: 990 graph nodes across 10 type directories (character, title, location, event, species, custom, language, faction, artifact, medical)
- MODIFIED: `worklog.md` (Session 42 entry, Session 37 archived)
- MODIFIED: `working/todos.md` (wiki-prose todo marked DONE)
- MODIFIED: `history/worklog-archives/archive008.md` (Session 37 appended)
- NEW: `progress/continue-prompts/2026-05-12-missing-node-backfill-bucket-a.md`
- NEW: `progress/continue-prompts/2026-05-12-location-artifact-index-rollup.md`
- DELETED: `progress/continue-prompts/2026-05-12-wiki-prose-extraction-backfill.md`
- MODIFIED: `next.md` (gitignored; Track 1 marked done, Tracks 2 & 3 expanded)

No agent calls. No external fetches. Pure Python. Cost $0.
