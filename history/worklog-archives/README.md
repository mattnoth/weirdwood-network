# Worklog Archives — Index

These files hold worklog session entries that were rotated out of `worklog.md` under CLAUDE.md rule #8: the live worklog keeps at most 5 sessions; when a 6th lands, the oldest is moved here.

**Convention:** each archive file holds exactly 5 sessions in reverse-chronological order (newest first). Entries are moved verbatim — no edits, no summaries. The two non-archive files below are explained at the bottom.

## Archive files

| File | Sessions covered | Date range | Era label |
|------|-----------------|------------|-----------|
| [archive001.md](archive001.md) | S0–S4 | ~Apr 13 | Phase 0–1: Genesis, scaffolding, and Cloudflare fight |
| [archive002.md](archive002.md) | S5–S7 | Apr 14–22 | Phase 1–2: Wiki crawl completion + schema v2 |
| [archive003.md](archive003.md) | S8–S15 | Apr 24–25 | Phase 2: Pass 1 v3 schema, process infrastructure, AGOT complete |
| [archive004.md](archive004.md) | S16–S21 | Apr 25–26 | Phase 3: Wiki Pass 2 orchestration plan + Stage 1 smoke runs |
| [archive005.md](archive005.md) | S22–S24 | Apr 26–27 | Phase 3: Stage 1 drain complete + Stage 2/3 pivot decision |
| [archive006.md](archive006.md) | S25–S29 | Apr 27–May 1 | Phase 4: Stage 3 pipeline redesign + Python-first promotion campaigns |
| [archive007.md](archive007.md) | S30–S33 | May 1–4 | Phase 5: ACOK Pass 1 + `--chain` terminal-explosion incident |
| [archive008.md](archive008.md) | S34–S38 | May 4–6 | Phase 5: All 5 books complete; hygiene + schema review |
| [archive009.md](archive009.md) | S39–S43 | May 7–12 | Phase 6: Index infrastructure + missing-node backfills |
| [archive010.md](archive010.md) | S44–S48 | May 11–12 | Phase 6: Mission protocol design (watcher/worker) |
| [archive011.md](archive011.md) | S49–S52 | May 12–13 | Phase 6: Alias backfill, orphan edge recovery, vocab drift cleanup |
| [archive012.md](archive012.md) | S53–S57 | May 15–18 | Phase 7: Stage 4 smoke + 21-batch bulk + vocab lockdown rounds |
| [archive013.md](archive013.md) | S58–S62 | May 18–21 | Phase 7: Lockdown completion + Haiku worker + overnight bulk + triage |
| [archive014.md](archive014.md) | S63–S67 | May 21–23 | Phase 7–8: KNOWS deprecated + S64 dual-run incident + Pass-1-derived pivot |
| [archive015.md](archive015.md) | S68–S72 | May 24–26 | Phase 8: edges.jsonl v1 landed + S71 false-alarm corrected |
| [archive016.md](archive016.md) | S73–S77 | May 26–27 | Phase 8–9: Enrichment NO-GO + Events-Haiku bulk launched |
| [archive017.md](archive017.md) | S78–S82 | May 28–Jun 4 | Phase 9–10: Events Haiku bulk done + NO-GO audit + reification design |
| [archive018.md](archive018.md) | S83–S86 | Jun 5–8 | Phase 10: Reification plates 0–5 shipped; edges 3,811 → 4,757 |

Sessions S87–S91 are in the live `worklog.md`.

### Anomalies in the archive files

- **archive006** and **archive007**: the `### Session NN` line appears at line 1 (no `# Worklog Archive NNN` title preamble). These files were created before the title-preamble convention was established. Content is intact.
- **archive006**: contains a duplicate `### Session 29` header — the entry was archived across two sessions and appears twice. The content beneath each is the same session (the second is a continuation); this is a worklog-tooling artifact, not a data error.
- **archive007**: `### Session 30` appears twice (two different sub-sessions entered as S30 in the live worklog before rotation). Same pattern as archive006.
- **archive009, archive010**: no title-preamble line (same as archive006/007). Session entries are complete.

## Non-archive files

**`extraction-progress.md`** — Wave-by-wave log of AGOT Pass 1 extraction runs (timestamps, chapter batches, token counts, costs). Referenced by live runbooks at `working/runbooks/pass1-auto-advance-mode.md` and `mechanical-extraction-howto.md`. Landed here during a S36 hygiene pass. It is a data file, not a worklog archive — the name explains its origin.

**`session-32-handoff.md`** — A cross-session handoff note written at the end of Session 31/32 to stage the ACOK re-extraction launch. Moved to this directory during the S36 hygiene pass (see `history/session-details/session-036.md`); it was stale before it arrived. Not a worklog archive entry.

## Cross-reference

The project-story chapter series at [`history/project-story/`](../project-story/00-overview.md) covers the same eras in narrative form. The phase labels in the table above align with phases A–11 of that series. For a complete phase-by-session mapping see the timeline table in [`00-overview.md`](../project-story/00-overview.md).
