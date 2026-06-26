# SESSION 152 — THE HARVEST PASS (dedicated, context-isolated — Matt S151)

> **This is Session 152.** Stamp your worklog entry `### Session 152` in `worklog.md` (GRAPH track, global S-number).
> **This session does ONE thing: consume the harvest queue.** Matt S151: *"we need to do the harvest pass … to save context, next session should only be that."* Do NOT bolt an enrichment dip onto it. The enrichment fork (remaining A2 arcs · the new Class-D event clusters) resumes the session AFTER this — it's parked in `working/enrichment-coverage-plan.md` (§ A2 + § Class D), not here.
> **Recommended model:** Sonnet 4.6 for the per-chapter attach subagents + the fresh-verify; Opus 4.8 for orchestration. (Mechanical attach work — keep it cheap.)
> **`/endsession` is PRE-AUTHORIZED for the harvest pass** (same standing as a dip) — but OFFER it, don't auto-run.
> **D&E Pass-1 is PARKED** — stage only graph-track files by path; never `git add -A`.

## Why now
The L1 + A2 + cheap-L2 dip streak (S133–S151) pushed breadcrumbs faster than they were consumed: the queue is at **225 open rows** (last consume pass was S118), well over the ~20–30 trigger. The load-bearing *quotes* got attached inline during each dip; what's piled up is the **food + descriptive register** (food=96, quote=37, description=33, foreshadowing=20, appearance=12, …). The arc work that was deprioritizing this is now largely done.

## The work-list is pre-grouped (prep done S151)
**Read `working/harvest-pass-s152/open-rows-by-chapter.md`** — the 225 open rows grouped into **79 chapter-buckets**, each row as `` `chapter:line` [kind] note ``. Process **chapter-by-chapter** (open each source file ONCE, attach all its rows, move on) — that's the cheapest traversal. The manifest saves you from parsing the 712-line queue. The queue itself (`working/harvest-queue.md`) remains the authoritative ledger you flip rows to `done` in.

## The consume protocol (documented at the top of `working/harvest-queue.md` — read it)
For each open row: **(1) line-check** — open the exact `chapter:line` and confirm the detail is verbatim there (cites drift; the S110/S120 passes caught several). **(2) attach to the right graph home by kind:**
- `quote` → the target node's `## Quotes` (+ navigable `sources/…:line` book-cite). Homeless quotes → the most relevant event/character node.
- `food`/`drink` → the `object.food` node (~75 exist, indexed at `graph/index/foods/`): accumulate the occurrence in the node's `## Narrative Arc` (verbatim + `chapter:line`) and/or `## Quotes`. Mint a new `object.food` dish node only when there's no home (Matt S137: capture ALL meals, maximal, incl. the grim/starvation register — those rows are tagged `GRIM REGISTER`).
- `appearance` → character node `## Appearances & Description` (book-cite overlay onto wiki prose = high value).
- `place` → `place.location` node description · `object` → `object.artifact`/`material` node · `hospitality` → feast/`GUEST_OF` custom · `foreshadowing` → a `FORESHADOWS` edge (only if a clean target event exists; else node `## Foreshadowing`) · `relationship`/`witness`/`seam`/`edge` → a typed edge (dedup first; line-check the quote; mint via a small script if >a few).
- **(3) flip the row to `done`** in `working/harvest-queue.md` (keep the row as an audit trail; append `[S152 harvest: attached to <node> …]`). `parked` rows stay parked (do NOT consume — they're blocked); there are ~46 parked, excluded from this pass.

## Method (efficient + safe)
1. **Triage the manifest** (Opus): the **real-chapter buckets** (agot/acok/asos/affc/adwd `.md`) are line-checkable; the **`wiki:…` cites** (a handful) attach from the wiki node prose, no book line. Split the 79 buckets into ~6–10 batches by book.
2. **Fan out Sonnet attach-subagents**, one per batch (a set of chapters): each opens its source files, line-checks every row, and writes the attachments. **Node `## Quotes`/description edits are direct file edits; any EDGE attachments go into a `candidates.json`** for a single mint script (`scripts/mint_harvest_s152.py`, modeled on `mint_cheap_l2_round_s151.py` — re-greps each quote, backup, re-run guard) so edges stay auditable + 0-drift-checkable. Give each subagent the consume protocol + the vocab/Tier rules + "PROPOSE edges, don't mint; you MAY directly edit node `## Quotes`/description."
3. **Independent fresh-verify** a stratified sample (the S110 pass verified 23/24 SUPPORTED) — confirm cites are real and attachments landed on the right node. Apply any fixes.
4. **Flip consumed rows to `done`** (a script that matches the row by `chapter:line`+kind and rewrites status is safest for 200+ rows — write `scripts/flip_harvest_done_s152.py`). Re-run `verify-edge-quotes.py --run-id harvest-s152` if you minted edges. `weirwood-refresh.sh` if you minted any new food/place nodes.
5. **Report** the consume tally (rows done by kind; new nodes minted; edges added) + how many rows remain open (aim: queue back under the trigger).

## OPTIONAL adjunct (only if time/context allows — else defer again)
The deferred **Python food-keyword grep** for *full-corpus* meal coverage (dish-names + eat/feast/supper/hungry/starv*/bread/meat… over all 344 chapters → seed `object.food` rows). This is a SEPARATE, larger deterministic job (`working/arc-enrichment-backlog.md` documents it). It is NOT required for this pass — consuming the 225 queued rows is the goal. If you run it, run it as a clearly-separate step AFTER the queue is drained, and log what it added.

## DO NOT
start an enrichment dip · un-park D&E · `git add -A` (stage by path) · consume `parked` rows · attach a quote without line-checking the cite first · invent edge types (locked 170 in `working/wiki/data/edge-type-counts.json`) · over-mint speculative edges from `foreshadowing`/`seam` rows (those are the judgment-heavy ones — when unsure, attach to node prose, don't force an edge).

## Read first
- `working/harvest-pass-s152/open-rows-by-chapter.md` (the grouped work-list — START HERE)
- `working/harvest-queue.md` top matter (the consumer protocol + kind→home table + the `done`/`parked` rules)
- memory `feedback_harvest_queue` · `feedback_capture_quotes_during_research` · `feedback_book_citation_overlay_value` · `feedback_python_before_agent`
- prior harvest passes for the pattern: `worklog.md`/archives S110, S113, S116, S118 (the consume-pass method)
