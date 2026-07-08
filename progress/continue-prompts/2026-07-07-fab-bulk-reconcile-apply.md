# SESSION 201 — F&B BULK reconcile + apply (after Matt's 35-unit extraction run finishes)
> **This is Session 201.** Stamp your worklog entry `### Session 201` at endsession.
> **Recommended model:** **Fable** for the first bulk-apply session (per-unit judgment: CREATE
> fresh-verify dispositions + dispute adjudication overrides — S200 proved both need real reads).
> Later sessions may drop to Sonnet once the per-unit pattern is boringly mechanical.
> **PRE-REQ: the bulk extraction run is COMPLETE (or a coherent batch of units is).** Check
> `ls extractions/fire-and-blood/*.enrichment.md | wc -l` (39 = all done; 4 were done pre-bulk)
> and `working/fire-and-blood/logs/`. If the run is still going, STOP — nothing to do yet.

## State (S200 close — trust worklog.md over this, CLAUDE.md rule 9)
The 4 smoke units are APPLIED (S200: +264 book-fab edges → edges.jsonl 23,363, +18 nodes,
76 merges, schema batch landed, tests 63/63). The proven per-unit §8 pattern + all tooling exist.
S200 records: worklog S200 entry + `working/fire-and-blood/apply/ADJUDICATION-s200.md`.

## The task — batch the remaining 35 units through the S200 pattern
Work in unit batches (suggest 5–8 units per batch; one git checkpoint per batch is fine, but
keep mint→merge per-unit). For each unit:
1. **Reconcile (non-smoke):** `python3 scripts/fab-reconcile-candidates.py --proposal extractions/fire-and-blood/<unit>.enrichment.md --out-dir working/fire-and-blood/apply/<unit>`
2. **Gate on the run-summary row (§7a):** located% ≥90 (below → check `ocr-scan.md`, quarantine is row-level, never re-extract); `disputed_rate ≈ 0` on a Dance unit = prompt failure → STOP and tell Matt; `created` spike = resolver failure → STOP.
3. **CREATE fresh-verify (MANDATORY per unit — caught a semantic dupe in 3 of 4 smoke units):** fresh subagent adversarially checks each CREATE against the graph (semantic dupes under different slugs, `birth-of-<canonical-char-slug>` convention, granular-event PART_OF/CAUSES parents). Apply folds/renames as deterministic surgery on candidates.json + nodes/ BEFORE mint (S200 pattern: scratchpad surgery script; re-verify quotes locate via `mint_enrichment.authoritative_line` after).
4. **Dispute adjudication per unit (rows in `dispute-review.jsonl`):** fresh subagent verdicts clear / tag-as-disputed(+`in_universe_source`) / drop — BUT verify tags against the primary text yourself before feeding back (S200: 2 subagent clears were wrong; the exile-decree class — divergence zones where one chronicler's version lacks the claim entirely → `gyldayn-synthesis`). Euphemistic "favorite" LOVER_OF = disputed/unattributed; flat "paramour" = tier-1. Skip redundant weaker duplicates of same-triple flat rows. Append verdicted edges to candidates.json; cleared prose bullets back into merge-plan; record everything in an ADJUDICATION file.
5. **Apply:** git checkpoint → `python3 scripts/mint_enrichment.py --candidates .../candidates.json` → `python3 scripts/fab_merge_node.py --merge-plan .../merge-plan.json` (summary MUST show 0 skipped / 0 not-found) → commit.
6. **After each batch:** `weirwood refresh`; spot queries; `python3 scripts/test-fab-reconcile.py` (fixtures can collide with newly-minted nodes — S200 had to move one; fix the fixture, not the router).

## Close-out (after the LAST unit applies)
- Deterministic Lineages-appendix validation diff (design §3.4/§10.10) → contradictions triage.
- Review-bucket triage plan (S200 left 161 rows; bulk adds more — present a triage summary, not row-by-row).
- Harvest-queue drain (`working/fire-and-blood/harvest-fire-and-blood.jsonl` + main queue — don't let it re-balloon; S153–S156 lesson).
- Un-park check: the strip-boilerplate track un-parks ONLY after the LAST pack applies (todos.md ★CURRENT).
- Residue sweeps queued in worklog S200: VICTIM_IN-on-non-harm-events re-type (deterministic, filter `evidence_kind: book-fab` + event type); `vaegon`/`vaegon-targaryen` dupe; `great-council-of-101-ac` mistype; chat-bundle rebuild rides the next deploy.

## DO NOT
- Do NOT re-run extraction for quote failures (row-level quarantine exists) or touch the extraction prompt.
- Do NOT skip the per-unit CREATE fresh-verify or the dispute adjudication.
- Do NOT touch the parked strip track. Do NOT auto-run /endsession.
