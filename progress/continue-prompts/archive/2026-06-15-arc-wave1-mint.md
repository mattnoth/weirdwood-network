# Continue — Narrative-Arc Wave 1 MINT (Red Wedding + Joffrey conspiracies)

> **Recommended model:** Sonnet 4.6 — deterministic mint + verification (same shape as the S96 graph-cleanup; JSON edges are pre-drafted + fresh-reviewed). Opus only if Matt wants insurance on a graph-mutating run.
>
> **Status (2026-06-14, S96):** Two wave-1 arc drafts written + fresh-reviewed. **Both verdict = MINT-WITH-FIXES.** Nothing minted yet. This session applies them AFTER Matt resolves the open decisions below.

## What this is
Wave 1 of the narrative-arc reification track (memo: `working/narrative-arcs-design-memo-2026-06-13.md`; memory: `project_narrative_arc_reification`). Reify two causal arcs as `event.conspiracy` parent hubs wrapping the already-reified event hubs. Prototype = the shipped `incident-at-the-trident` (S95 Q5).

## Source-of-truth files (read all four)
- `curation/narrative-arc-wave1-red-wedding-draft-2026-06-14.md` — proposes `red-wedding-conspiracy` parent; 5 new mints + 22 edges.
- `curation/narrative-arc-wave1-joffrey-draft-2026-06-14.md` — proposes `joffrey-poisoning-conspiracy` parent; 4 new nodes + 18 edges.
- `curation/narrative-arc-wave1-review-2026-06-14.md` — the fresh review; **apply its must-fixes (below) during mint.**
- `curation/s95-quarantine-resolutions-2026-06-13.md` § Q5 — the gold-standard shape + JSON style to match.

## SETTLED design rule (Matt-confirmed S96) — parent shape
Arc parent = a NEW `event.conspiracy` hub that WRAPS the existing event hub. The event (`red-wedding` / `purple-wedding`) is ONE sub-beat of the conspiracy parent and keeps its own in-feast sub-beats. Pre-event plotting + post-event consequences attach to the CONSPIRACY parent; in-feast moments attach to the EVENT hub. Scope test: a beat is `SUB_BEAT_OF X` only if it genuinely happened within X's scope.

## OPEN DECISIONS — Matt must resolve before mint (do NOT guess)
1. **RW-4 (parent role edges):** the Red Wedding draft puts `COMMANDS_IN` (Tywin, Walder) + `AGENT_IN` (Roose) DIRECTLY on the `red-wedding-conspiracy` parent — a deliberate deviation from the memo's "parent has zero direct role edges." Reviewer recommends SANCTIONING this for `event.conspiracy` hubs (conspirators act at arc level, not a single beat) + updating the memo. **Matt: approve arc-level role edges for conspiracy hubs, or push them down to beats?**
2. **Red Wedding terminus:** include the `catelyn-is-resurrected-as-lady-stoneheart` beat (reviewer recommends YES — the conspiracy's most consequential downstream node) or close at Robb's death (drops 1 mint + ~4 edges)?
3. **Joffrey boundary:** include `sansa-s-escape-from-kings-landing` (reviewer recommends YES — Littlefinger commissioned escape + poison-delivery in one instruction) or close tighter?
4. **Vocab additions** (reviewer-recommended): add `RECIPIENT_IN` to `reference/architecture.md` edge vocab (clean, reusable — use `VICTIM_IN` for Sansa on the stone-removal beat in the meantime); use existing `event.incident` for the escape node (NOT a new `event.escape`); defer `UNWITTING_INSTRUMENT_IN`. **Matt: approve the `RECIPIENT_IN` add, or use `VICTIM_IN` and skip it?**

## MUST-FIX before/during mint (from the review — apply these)
**Red Wedding:**
- RW-1: TRIGGERS `frey-bolt-offer-edmure-roslin → red-wedding` — change `evidence_ref` `asos-catelyn-04.md:219` → `:251` (the "It must happen" quote is at 251; 219 is a different line).
- RW-2: `death-of-grey-wind` SUB_BEAT_OF must point at `red-wedding` (the EVENT — it happened at the Twins during the massacre), NOT the conspiracy parent. (Its TRIGGERS edge is already correct.)
- RW-3: drop the circular `robb-breaks-frey-marriage-pact TRIGGERS red-wedding-conspiracy` (a sub-beat can't trigger its own parent); if cross-beat causation wanted, use `robb-breaks… TRIGGERS frey-bolt-offer-edmure-roslin`.
- Slug-naming nit: `frey-bolt-offer-edmure-roslin` reads like "crossbow bolt" → consider `frey-offer-edmure-roslin-marriage` or `lothar-delivers-roslin-offer`.

**Joffrey:**
- JF-1: 3 edges have `evidence_chapter:"asos-sansa-05"` but `evidence_ref` → `asos-sansa-06.md` (quotes are verbatim-correct in sansa-06). Fix the chapter labels to `asos-sansa-06`. (`COMMANDS_IN petyr→dontos-delivers-hairnet` :145, `TRIGGERS death-of-joffrey→killing-of-dontos` :145, `AGENT_IN lothor-brune→sansa-s-escape` :55 — for Lothor consider the stronger `asos-sansa-05.md:117` instead.)
- JF-2: Sansa "unwitting instrument" role → use `VICTIM_IN` (or `RECIPIENT_IN` if Matt approves the vocab add).
- JF-3: `sansa-s-escape-from-kings-landing` → type `event.incident` (not `event.escape`).
- Olenna corroboration (bonus capture, per the firm quote rule): the review CONFIRMED Olenna is shown touching the hairnet on-page in Tyrion's POV — `asos-tyrion-08.md:101` ("The little old woman reached up and fussed at the loose strands… straightening Sansa's hair net"). Add this as a corroborating `evidence_quote` (Tier-2 stands — touching is shown, stone-removal still needs Littlefinger's testimony) on the relevant beat/edge or the `death-of-joffrey-baratheon` `## Quotes` block.

## Mint procedure (S95 / graph-cleanup style)
1. **Backup** `graph/edges/edges.jsonl` → `graph/edges/_regrounding/edges-pre-arc-wave1-<timestamp>.jsonl`.
2. If Matt approved vocab adds: edit `reference/architecture.md` (RECIPIENT_IN row) FIRST.
3. Apply the reviewed+fixed JSON edges (append) + mint the new node files (frontmatter from the drafts). Build as a script with `--dry-run` if volume warrants, else direct append with a count check.
4. Rebuild indexes (`build-entity-indexes.py --all`) + alias resolver (`event_alias_resolver.py --build`).
5. **Verify:** `--health` clean (orphan count not worse); `--event-participants red-wedding-conspiracy` and `--event-participants joffrey-poisoning-conspiracy` traverse the full arcs; `--lookup` resolves the arc names (resolver was fixed in Track 7); pytest green except the 3 documented pre-existing failures.
6. Mark drafts `[MINTED YYYY-MM-DD]`; update `working/todos.md` HIGH + `worklog.md`.

## Hard rules
- No writes to `sources/`. Backup before any `edges.jsonl` write. Do NOT auto-`/endsession`.
- Every edge carries a verbatim `evidence_quote` + `evidence_ref` (already in the drafts; verify the fixed refs).
- If a `[NEW: slug]` already exists, STOP and report (don't duplicate).

## Downstream queue (Matt's sequence: A done → C this → then B)
- After this mint: **followup #9 — historical structural-attachment** (`working/todos.md` Track 3; Sonnet 4.6; $0 deterministic — attach existing dyads like Rhaegar→Lyanna to isolated historical hubs e.g. `tourney-at-harrenhal`).
- Then: **B — script consolidation / hygiene** (`working/todos.md` Track 6, MATT DIRECTIVE 2026-06-14; own session; standardize long-runs onto `longrun.sh` + `weirwood run`, archive dead one-offs).
