# Stage 4 — Recall expansion: merge Hospitality edges + cost decisions + finish the spine

> **Recommended model:** **Opus 4.7** — this session is mostly *decisions* (3 cost/aggressiveness levers Matt must weigh in on) + careful merge coordination, not bulk edits. Use Sonnet 4.6 for any deterministic cleanup sub-steps; never Opus for per-item work.
> **Trust worklog.md over this prompt if they differ** (CLAUDE.md #9). Authoritative state: worklog Session 68 + the Stage 4 Current-State line.
> **This prompt is the entry point.** For the resolver-lever / tail-cleanup / dedup detail, read the still-valid `progress/continue-prompts/2026-05-23-stage4-pass1-finishing.md` (Tracks 1–5) — its work is unfinished and now must ALSO cover the 529 new extra-tables edges.

## Where things stand (end of Session 68, 2026-05-24)

Stage 4 book-pass1 edges = **5,219 canonical** (2,834 deterministic `python-map` + 2,385 `sonnet` tail), still in `working/wiki/pass2-buckets/pass1-derived/{book}/` and `_tail-typed/{book}/`, **not yet merged into one set, not yet in `graph/edges/`**.

S68 added a **separate, un-merged** recall layer via `scripts/stage4-pass1-extra-tables.py` (`--extra-tables`, staging `pass1-derived/_extra-tables/{book}/`, 339 files / 4,951 rows; **canonical spine byte-for-byte untouched**):
- **529 deterministic $0 edges** from `## Hospitality & Guest Right`: 460 `GUEST_OF` (qual: shelter 211 / feast 121 / unknown 39 / gift_exchange 33 / refused 29 / safe_conduct 17 / bread_and_salt 10) + 69 `VIOLATES_GUEST_RIGHT`. Red Wedding verified correct (walder-frey → robb/catelyn VIOLATES; GUEST_OF robb/edmure/catelyn → walder-frey feast; grey-wind → walder-frey refused).
- **4,422 Dialogue tail rows** (clean Speaker→Listener; type unknown → would need LLM, ~$30 at $0.0068/row).
- **Food / Events & Actions / Information Revealed** = counted-only (prose-shaped; 1,263 / 8,384 / 5,654 rows). No edges, no regex.
- 431 tests green. Report: `working/wiki/data/pass1-derived-extra-tables-report.md`. Recall-sample: `working/wiki/data/pass1-derived-recall-sample.md`.

**Everything from S67 + S68 is UNCOMMITTED** — Matt checkpoints via his own `wip` commits. Ask before committing.

## The finding that drives the decisions

Recall-sample (7 chapters, 196 rels): **A 64% caught now / B 28% table-mineable / C 9% prose-only.** But cross-referenced with the miner:
- Bucket-B productivity ranks **Events & Actions > Information Revealed > Hospitality > Dialogue**.
- The cheap deterministic win (Hospitality) is only #3. The #1/#2 recall tables (Events/Info) are **prose-shaped → need a bounded LLM pass (~14k rows, ~$95+)**. Dialogue ($30) is **lowest-yield**.
- So 1a-as-built = A + Hospitality (~free), NOT the full ~92%. The rest of the recall is an explicit LLM cost call.
- Bucket C (~3% high-value: Gregor/Aegon, Cersei/Maggy, Dany/Viserys) → **targeted narrative-aside audit, NOT a full prose pass** (which would re-introduce the deprecated prose-hunting failure mode). Possibly fold into Pass 3 perception.

## Tracks

### Track R1 — Merge the 529 Hospitality/VIOLATES edges (deterministic; do after endpoint filter)
- **First apply an endpoint filter.** The 529 inherit the resolver's index-pollution noise — spot-check caught `walder-frey VIOLATES_GUEST_RIGHT all-for-joffrey` ("All for Joffrey" = the Freys' toast, not an entity). Drop/repair junk-node endpoints. This is the SAME fix as Track-1 in the finishing prompt (full-surname rung + index-pollution filter) — coordinate; do it once for both the spine and these edges.
- Then merge the cleaned 529 into the canonical edge set (same target as the S67 `_tail-typed/` merge — see finishing-prompt Track 4; check `reference/architecture.md` for the `graph/edges/` convention before promoting). Preserve `source_section` + `typed_by` provenance. GUEST_OF/VIOLATES carry their qualifiers per `reference/edge-qualifier-vocab.md`.
- Spot-audit a random sample of merged edges (green tests are NOT correctness proof — they missed the all-for-joffrey class and the S66/S67 misresolution bugs).

### Track R2 — Dialogue tail: SMOKE before spending (needs Matt's OK — it's an extraction)
- Do NOT blanket-type all 4,422 rows ($30) — recall sample says Dialogue is lowest-yield. Smoke ~200 rows via `scripts/stage4-tail-classifier.py`-style `claude -p` (Sonnet, cwd=/tmp). **Add the S61/S63 ENCOUNTERS Rule-6 verb-gate to the prompt first** (the tail classifier omits it). Measure the typed-vs-"just-a-mention"/rejected ratio. If most are just-conversation, skip the full run.

### Track R3 — DECISION: the bounded Events/Info LLM pass (Matt's call — ~$95+)
- This is where the real missing recall is (~14k prose-shaped rows in Events & Actions + Information Revealed). Each row is one scoped fact → far safer/cheaper than open wiki comention, but it IS an LLM extraction (pair + type both inferred). Decide: run it, defer it, or fold the high-value subset into Pass 3. If running: design a candidate shape + verb/actor heuristic + smoke first; drift-detection mandatory (cross-model audit + schema validator) per the standing rule.

### Track F (from the finishing prompt — still open) — resolver levers + tail cleanup/dedup/merge
- See `progress/continue-prompts/2026-05-23-stage4-pass1-finishing.md` Tracks 1–5. The 2 resolver levers (full-surname rung ~72; index-pollution filter ~417) are Matt's "how aggressive" call and ALSO clean the 529 edges' endpoints (Track R1). Tail-violation cleanup (21/2,385), tail dedup, and the canonical merge remain.

### Track W (optional, low-priority) — #2 fast narrow wiki layer
- The wiki's structural edges are already deterministic via `scripts/wiki-infobox-parser.py`. To get more cheaply: extend the infobox-field→edge map to the unmapped fields flagged in the worklog Track-B issues (`dynasty`, `vassal`, `cadet branch`, `fathers`, `hatched`). Python, not LLM. Scope only after the recall picture above is settled.

## Open questions for Matt (decide at start)
- **Commit S67 + S68?** (all uncommitted — scripts, tests, reports, stamped comention files, worklog/session-068/continue-prompts/todos).
- **R2:** OK to smoke ~200 Dialogue rows (~$1-2) to price the $30 decision?
- **R3:** Run / defer / Pass-3-fold the ~$95+ Events/Info pass?
- **Track-1 resolver levers** (full-surname rung + index-pollution filter): how aggressive? (Both change core resolution semantics + clean the 529 edges.)

## DO NOT
- Mutate `working/wiki/data/alias-resolver.json` (use `pass1-derived-supplementary-aliases.json` for additive aliases).
- Merge the 529 edges before the endpoint filter (you'll import `all-for-joffrey`-class junk nodes).
- Re-run any LLM tail without the ENCOUNTERS Rule-6 verb-gate in the prompt.
- Relaunch wiki comention (DEPRECATED; 133 files stamped superseded). Refetch the wiki. Use Opus for bulk/per-item edits.
- Trust green tests as correctness proof — spot-audit random samples.
- Run `/endsession` without explicit permission. Read/triage the top-level `scratch*` files.
