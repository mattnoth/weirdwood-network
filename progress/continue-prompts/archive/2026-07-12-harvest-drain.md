# SESSION 216 — Harvest drain: 46 open rows → 0 (parallel-safe with theories wave 1)

> **This is Session 216.** Stamp your worklog entry `### Session 215` at endsession.
> (If theories wave 1 hasn't run yet, this can also fire as S214 — whichever fires
> second takes the higher number; coordinate via worklog.)
> **Recommended model:** any orchestrator + **Sonnet 4.6** attachers + one Haiku
> fresh-verify sampler. Mechanical track — no Fable needed.
> **PRE-REQ:** S213 committed+pushed. Parallel-safe with the theories session (disjoint
> files) EXCEPT the final mint/attach writes — if theories is mid-mint, serialize the
> apply step (edges.jsonl is monolithic; see memory `project_concurrent_enrichment_deferred`).

## Why

S213's two dips landed 42 open rows + S214's R+L=J proposer added 4 = **46 open rows** in `working/harvest-queue.md` (merged at
endsession from the per-agent harvest files) — over the ~30 bar. Endsession rule: drain
or stage; Matt directed session close, so this is the staged drain.

## Machine (proven S139/S152/S157 — see `working/arc-enrichment-backlog.md` harvest section)

1. Route the 46 open rows by target node-dir into DISJOINT batches (quotes/appearance/
   food/hospitality; ~3 batches).
2. Parallel Sonnet attachers, one per batch: open each `chapter:line`, verify the text is
   really there (S121 line-check), attach to the graph (node `## Quotes` / description
   fields / `object.food` nodes per row kind), flip the row `| open ` → `| done `.
   BYTE-COPY quotes (fab OCR mixes apostrophe styles within lines).
3. Haiku fresh-verify a ~20% sample of attachments.
4. `python3 scripts/verify_node_quotes.py` (must stay green) + `bash scripts/weirwood-refresh.sh`
   + pytest + deno. Mint-style gates apply to any new nodes.
5. Queue back to 0 open. Deploy only on Matt's go.

## DO NOT

- Do NOT drop rows to hit zero — a genuinely blocked row flips to `parked (blocked: <reason>)`.
- Do NOT rewrite others' rows; append-only discipline.
- Do NOT run /endsession without permission.
