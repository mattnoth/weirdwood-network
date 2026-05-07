# Session 030 — ACOK Pass 1 status check + wave 11-14 completion (2026-05-02)

Short execution session. Goal was to check ACOK Pass 1 status and run the missing chapters.

## What happened

Checked `extractions/mechanical/acok/` — empty. Worklog showed "Pass 1 v3 run on ACOK (0/70)" with 50 chapters sitting in `extractions/archives/acok-v2/`. Those 50 had the arya/bran/catelyn/daenerys/davos/jon/prologue/sansa/theon-01 POVs. Missing were theon-02 through theon-06 and all 15 tyrion chapters (waves 11-14 in alphabetical sort order).

Copied the 50 archive files into `extractions/mechanical/acok/`, then launched waves 11-14 (4 terminals). tyrion-10 dropped silently during wave 13 — its JSON log had no result event. Re-ran it as a single-chapter invocation. All 70 chapters confirmed present at session end.

## The schema problem

Spot-checking Raw Entity List headers revealed the 50 archived chapters use the v2 schema (4 categories: Characters, Locations, Artifacts, Houses/Factions). The 20 new chapters use v3 (12 categories). This is a real inconsistency.

Matt pushed back — he said he ran those chapters as v3. Git history settled it: commit `b801b420` on 2026-04-25 at 13:36:10 archived them as "acok-v2" in the same session-end batch that created the v3 prompt (`a317a7de` at 13:35:54). Matt ran those 50 the night before this session (burning ~28% of MAX weekly context budget), but when he ran them, v3 didn't exist yet. The v3 prompt and the archive label were both created after-the-fact in the same commit batch.

Result: 50 chapters need re-running when budget allows. Command: `weirwood-mechanical --chain acok 4 1` stopped after wave 10. The 20 theon/tyrion chapters (waves 11-14) are correct v3 and don't need to be touched.

## Other

- Confirmed friend running ASOS doesn't need a prompt update — v3 is current, no changes since AFFC completed.
- Updated worklog ACOK line to reflect 70/70 complete with schema-mix note.
- Continue prompt `2026-05-02-pass1-mechanical-remaining-books.md` still references "acok: 0/70" — updated to reflect actual state.
