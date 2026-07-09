# SESSION 203 — F&B close-out (post-bulk-apply)
> **This is Session 203.** Stamp your worklog entry `### Session 203` at endsession.
> **Recommended model:** **Sonnet** orchestrator (the judgment-heavy apply work is DONE; close-out is
> deterministic builds + triage summaries) + Haiku subagents where verdicts are orchestrator-re-verified.
> Escalate to Fable/Opus ONLY if the deferred-events minting turns out judgment-heavy.
> **PRE-REQ:** all 7 batches applied (`a9e2b2b584` = B7). If `git log` disagrees, STOP and reconcile with worklog.md.

## State (S202 close — trust worklog.md over this, CLAUDE.md rule 9)
The 35-unit F&B bulk apply is COMPLETE (batches 1–3 S201, 4–7 S202). book-fab edges 264→**1,891**
(98 disputed, all with in_universe_source), event nodes **963**, edges.jsonl **24,988**. Gate PASS,
153 tests green. Small residues (vaegon dupe, great-council mistype) fixed S202.
Live state + full batch table + residue list: `working/fire-and-blood/apply/BATCH-PROGRESS-s201.md`.

## The task — close out the F&B track (order by value)
1. **Deferred-events triage** (37 rows in per-unit `dispute-events-deferred.jsonl` + the death-of-aegon-ii
   event-residue from B6): decide create-node-or-skip per row; for creates, run the S202 rhythm
   (fresh-verify vs graph → mint via a small hand-built candidates file or `fab-dispute-inject.py`
   event path). death-of-aegon-ii gets `larys-strong SUSPECTED_OF` (tier-2, quote "we can have no doubt
   that it was done at the behest of Larys Strong", fab-short-sad-reign-of-aegon-ii-19 L277).
2. **Lineages validation diff** (design §3.4): script-builder writes the deterministic parser
   (OCR'd genealogy tables → kinship triples → diff vs edges.jsonl → confirm/new/conflict buckets;
   NEVER auto-mint from OCR; new→`working/fire-and-blood/lineages-review.jsonl`, conflict→contradictions
   report). Then triage the conflict bucket only.
3. **Review-bucket triage plan** (1,440 reconcile-review rows): deterministic Python groups rows by
   review-reason × unit → present Matt a summary table + a recommended keep/drop policy per class.
   Do NOT read rows one-by-one.
4. **F&B harvest drain** (337 rows in `working/fire-and-blood/harvest-fire-and-blood.jsonl`): the S152/S165
   drain machinery (disjoint-dir attachers). May split to its own session if context runs hot — it's the
   most separable item.
5. **Small residues** (see BATCH-PROGRESS close-out section): KNIGHTED_BY direction audit (6 edges);
   capture-of-prince-viserys date; B1 dropped PART_OF re-adds (optional); sun-chaser fold revisit (optional).
6. **Tell Matt the strip-boilerplate track un-park condition is met** (last pack applied) — his call.

## DO NOT
- Do NOT re-run extraction or touch the extraction prompt.
- Do NOT auto-mint kinship edges from the OCR'd Lineages appendix (validation corpus only, §3.4).
- Do NOT run /endsession without Matt's explicit go.
- Do NOT start the strip track or theories work unprompted (both Matt-gated).
