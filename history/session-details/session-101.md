# Session 101 — Events/time design + deterministic event dating (2026-06-16)

**Model:** Opus 4.8 (1M context) orchestrator + ~14 Sonnet 4.6 subagents.
**Outcome:** re-tested the graph, decided the events/time + era schema, and SHIPPED deterministic
in-world event dating (112 nodes) + narrative reading-position (29 nodes). All deterministic, $0, reversible.

---

## How the session opened: arcs vs. testing, and a Fable-cleanup discrepancy

Matt opened with the parked handoff (narrative-arc wave 1 mint, gated on 3 decisions) and asked the real
question: should we mint arcs, do more graph-traversal testing, or does arc/clustering work make testing
unnecessary? Plus a second observation — he thought the "Fable cleanup" was done, but the working-dir and
verbiage ("track", "plate") hadn't changed.

**Findings:**
- The project's own **Mode-3 dip (S96)** had already de-prioritized arcs (D3): "the dominant problem is a
  lookup bug sitting on correct data, not missing arcs." The arc track's governing rule is *dip-driven, not
  mass-mint* — testing is what's supposed to prioritize arc-minting, so arcs don't make testing unnecessary;
  it's the reverse.
- The **Fable cleanup** wasn't fully done because the script-consolidation slice (S98/S99) was a separate
  track. The working-dir reorg (`working/repo-reorg-plan-2026-06-12.md`) and the nomenclature/"track-plate"
  sweep (`working/nomenclature-reform-proposal.md`) were delivered by the audit as **plans/proposals only**,
  both gated on Matt's picks, neither executed. Matt's instinct was correct.

## The re-dip (decision: test before minting)

A fresh evaluator re-ran the exact S96 10-question dip on the current graph, blind to the prior scores (to
avoid anchoring). Result: **4 correct / 6 partial / 0 failed** vs S96's 4/2/4. Verified independently:
Tourney-at-Harrenhal 0→25 edges (historical-anchor wave 1), "who ordered the Red Wedding" now names Tywin,
the S96 Track-7 resolver fix is live (natural phrasings hit). The remaining gaps shifted to **causal/
consequence edges** (`TRIGGERS`; Battle of the Trident has 16 participant edges, 0 causal) and **`ATTENDS`**.
The evaluator explicitly said arc reification is NOT the bottleneck — "the failures are vocabulary gaps, not
missing hub layers." Two independent dips now agree.

## Events/time: should events have dates?

Matt proposed dating events (sketch schema: `ac_year`/`precision`/`basis`/`confidence`) and raised a dual
axis — in-world date ("suspected 88 AC") vs narrative position ("Book 2 Ch 5"). A temporal mini-probe showed
the graph fails 4/5 time queries today, but `chronology-events.jsonl` (2,245 rows) already holds the answers.

A **4-lens opinion panel** (query-utility / data-cost / canon-uncertainty / graph-modeling) plus the parallel
historical-anchor agent's coordination note converged:
- **Two separate axes**, not one — they diverge maximally for historical events (Trident happened 283 AC but
  is narrated as Book-1 backstory).
- Time in **node frontmatter**; ordering edges DERIVED, not authored. Don't mint `OCCURRED_IN_YEAR`.
- **Relative ordering is the safe primary; absolute AC dates are the risky, tiered, gated layer.** Uncertainty
  must be structured (typed fields), never a string an agent can strip.
- Cheap: narrative axis ~95% derivable, in-world ~44% deterministic + a small LLM tail.
- Chronology ≠ causation: dating doesn't fill the causal-edge gap, it complements it (makes ordering free).

## The era question (research → analysis pipeline)

Matt flagged a possible naming collision around `era`. A research subagent produced an evidence dossier; an
analysis subagent decided. Findings: **`era:` is already a documented frontmatter field** (architecture.md:438)
meaning *narrative epoch* (`pre-conquest`…`current-narrative`), forward-only, on 0 live nodes. So `era: AC|BC`
is **disqualified** (overloads the epoch field). Decision: **signed `ac_year` integer (negative = BC)**, no
separate reckoning field — unambiguous, sort-correct, drift-resistant. Plus a 9-invariant validator (type
contract, no `reckoning:` key, span-vs-uncertainty mutual exclusion, no naked dates, tertiary-fan tier cap,
age-of-heroes guard, epoch-enum guard).

## Next-move panel → execute

Matt: "spawn a panel to weigh the correct move and then do it." A 4-stance panel (cheapest-win / measured-value
/ risk-auditor / sequencing) unanimously chose **deterministic event dating**. The risk auditor (Panel C) drew
the apply/dry-run line, catching two things: (a) `narrative_first` isn't safe to auto-write naively (edge
chapter-refs come in two formats), (b) multi-event noise stubs (`great-council` = 3 councils) must be excluded
— and the "exactly one distinct year" rule auto-excludes them.

**Executed (deterministic, additive, reversible):**
- `scripts/date-event-nodes.py`: 112 clean event nodes dated (single attested year + exact slug match),
  tier-3/wiki-year-page. Reviewed all 113 candidates; excluded `long-night → 297 AC` (a wiki mention-index
  error — the Long Night is prehistoric, on the 297 page because its *return* is discussed). 5 multi-year
  spans + 1 no-match staged.
- `scripts/backfill-narrative-first.py`: 29 events with chapter-cited edges got `narrative_first`
  (`{book}-{chapter_number}`), via a normalizer resolving both ref formats (`agot-eddard-01` ≡ `AGOT Eddard I`)
  to absolute chapter via the chapter-file index, with resolve-all-or-skip → 0 unresolved. Red Wedding → asos-52
  (ASOS Catelyn VII), verified.
- 64 new tests; pytest 1295 pass / 3 documented pre-existing fails. `--health` unchanged. `architecture.md`
  amended with the `occurred:` schema. Frontmatter-only, idempotent, bodies preserved.

**Stopped at `PRECEDES`/`FOLLOWS`** — recon found it's NOT a mechanical step: the edge types aren't in the
locked vocab (deferred schema decision, roadmap D3), and 0 dated events share a `PART_OF` parent (no cluster
structure). Correctly left as a Matt decision.

## Wrap-up

- 4 historic top-level markdowns archived to `history/archive/` (Matt request).
- Two commits staged the work (`36abaabf` archival, `2eacbf7c` dating + design trail), committed to main.
- Worklog rotation: a fresh advisor recommended archiving S96 normally + anchoring the S96-dip reference in the
  S101 entry, rather than pausing rotation (a paused rotation silently lapses after one context reset — a
  documented failure mode in this project). Matt chose that. Optional future safeguard (pytest session-count
  guard) logged in todos.
- The 4 open decisions captured in `working/next-move-decisions-2026-06-16.md` + a continue prompt that opens
  next session by asking Matt to resolve them.
