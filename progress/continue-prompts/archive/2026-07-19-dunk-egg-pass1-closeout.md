# SESSION DE-4 — Dunk & Egg Pass-1 CLOSE-OUT: adjudicate epithets, freeze the track

> **This is the Dunk & Egg track.** Read `worklog-dunk-egg.md` first; stamp your entry
> **`### Session DE-4`** there, NOT in `worklog.md`.
>
> **STATE (after DE-3, 2026-07-19):** **The extraction is COMPLETE AND VERIFIED.** 24/24 part-units in
> `extractions/mechanical/{thk,tss,tmk}/` (10,416 lines, ~$51.10); schema validator 24/24; fresh audits
> PASS (`working/dunk-egg-pass1/AUDIT-{tmk,thk-tss}-full-run.md`). Nothing extracts in this session —
> it's pure adjudication + bookkeeping.
>
> **Recommended model:** Haiku 4.5 (checklist bookkeeping; the one adjudication is small and
> Matt makes it).

## Steps

1. **Adjudicate the 4 TMK epithet-SAME_AS rows with Matt** (TMK audit item 5):
   `tmk-dunk-01-p05.extraction.md` lines 287/290 and `tmk-dunk-01-p06.extraction.md` lines 269/271 —
   rows like `Dunk | SAME_AS | the Gallows Knight`. The auditor says epithet ≠ concealed identity and
   recommends deletion; the counter-argument (DE-3 orchestrator) is that epithets are useful ALIAS
   capture for graph-build resolution. Options: (a) keep as-is (graph-build maps SAME_AS→alias),
   (b) delete the 4 rows, (c) retag in place. Matt decides; apply; note in worklog.
2. **Freeze the track** (per the `worklog-dunk-egg.md` header): add the DE-4 entry, then move the whole
   file to `history/worklog-dunk-egg.md` (git mv), update the `worklog.md` STATUS cross-track pointer
   (D&E line → "COMPLETE, frozen to history/") and the CLAUDE.md First Steps D&E branch (now moot —
   point to the frozen file for archaeology).
3. **Downstream pointers → `working/todos.md`** (do NOT execute them):
   - D&E graph-build integration: the 24 extractions emit locked-vocab relationship rows + 59 SAME_AS +
     reification-role Events tables — a Stage-4-style deterministic ingest can now wire D&E into the
     graph (the Bloodraven dip's missing substrate, `project_bloodraven_enrichment_dip`).
   - Harvest drain: `working/dunk-egg-pass1/harvest-dunk-egg.jsonl` — 372 slash-delimited rows
     (misnamed .jsonl; THK/TSS rows may duplicate the 55 smoke-era rows — dedup on drain).
   - Back-port the v4 locked-vocab prompt to the general `mechanical-extractor` (S131 decision said
     back-portable; the five-book v1–v3 corpus is free-text).
4. **Update `reference/pov-characters.md` / any chapter-count tables** if they claim D&E has no Pass 1.

## DO NOT
Extract anything · mutate the graph (`graph/`) — integration is a SEPARATE gated track ·
`/endsession` unasked · touch `worklog.md` Session Log.
