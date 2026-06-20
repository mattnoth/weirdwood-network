# Continue — Harvest pass: consume `working/harvest-queue.md`

> **Recommended model:** Sonnet 4.6 (read-and-attach + subagent-driven; Opus only for a hard judgment call).
> **Status:** LIVE — Matt's chosen next track (S109, 2026-06-20). The harvest queue has accumulated **~28 `status: open` rows** across 2 dips and is past the "worth a batched pass" threshold. This pass turns the cheap pointers into real graph, then flips rows to `done`. It also **proves the queue→graph half of the harvest mechanism** end-to-end (until a pass runs, the queue is just a promising affordance).

## What this is
`working/harvest-queue.md` is a deferred-capture ledger: any agent already reading the text drops one-line `book / chapter:line / kind / note` pointers to notable-but-not-their-task finds (homeless quotes, food, character appearance, place/object description, hospitality, foreshadowing). POINT, don't extract. **This pass is the consumer:** read each `open` row, open the cited `chapter:line` (or `wiki:Page`), attach to the graph, flip the row to `done`. Convention + rules: memory `feedback_harvest_queue` + `feedback_capture_quotes_during_research`.

## The work, in order
1. **Read `working/harvest-queue.md`** — process every `status: open` row. (Append-only file; don't rewrite others' rows — only flip `open`→`done` on rows you complete.)
2. **For each row, attach by `kind` → graph home (schema verified S109, all dirs exist):**
   - `food` → `object.food` node in `graph/nodes/foods/` (e.g. existing: `sisters-stew`, `weirwood-paste`). Bread/cheese, nut-brown ale, sweet beer, Tyrion's Dornish-pepper breakfast.
   - `quote` → attach to the relevant node's `## Quotes` block (or as `evidence_quote` on an edge). For homeless lines with no node home, attach to the nearest existing beat/character node.
   - `appearance` → the **character** node's appearance/description field or `## Description` (Renly in bloodied greens, Littlefinger's mockingbird cape, Varys in lavender). First-class for cross-identity matching ([[user_asoiaf_design_values]]).
   - `place` → the **location** node description. `object` → `object.artifact`/`object.material`. `hospitality` → `event.feast`/`GUEST_OF`/custom edges. `foreshadowing` → `FORESHADOWS` edge. `relationship` → typed edge.
   - **`concept.medical`** for "milk of the poppy" (→ `graph/nodes/medical/`; it's literally architecture.md's canonical `concept.medical` example, line 102). The quote is already on `ned-confesses-to-treason`; this just mints/links the medical node.
3. **Discipline (same as the arc machine):**
   - **Dedup before minting** — grep `graph/nodes/foods/` etc. + run the alias resolver; reuse existing nodes (e.g. an `arbor-gold` may already exist). Don't double-mint.
   - **Aliases as natural SPACED phrases, not kebab** ([[project_node_alias_spaced_phrases]]) — the resolver keeps hyphens, so kebab aliases never match natural queries.
   - **Provenance + Tier** on every attachment: cite `sources/chapters/<book>/<file>.md:<line>`; factual presence Tier-1, interpretive Tier-2.
   - **Verify the cited line before attaching** (the research agents have mis-cited before; open the file, confirm the quote sits at the line).
4. **After node ADDs: rebuild** the targeted indexes (`build-entity-indexes.py --type foods --slug <s>` etc.) + `event_alias_resolver.py --build` ([[project_rebuild_derived_artifacts_after_node_mutation]]).
5. **Surface judgment calls, don't guess** — if a find is ambiguous (is "X" a new node or just a quote? does this need a new node category?), list it for Matt rather than inventing structure. Most rows are mechanical; a few may not be.
6. **Flip completed rows to `done`** in the queue; leave anything you deferred as `open` with a note.
7. **Harvest-while-harvesting:** you'll be in the chapters — PASTE the canonical snippet (queue file § "Paste-into-every-dip/research-subagent-prompt snippet") into any text-reading subagent so new incidental finds get captured for the next pass.

## Bucket review (was due after 2 dips — Matt's smoke test)
S109's 2-dip review (in the queue file) found: push works, buckets healthy (quote 10 / appearance 8 / food 4 / rest sparse), no split/merge yet, push stays memory-only. After THIS pass, re-check whether any bucket needs splitting and whether to harden the push memory→CLAUDE.md/hook.

## Guardrails (FIRM)
- Never re-fetch the wiki — it's local at `sources/wiki/_raw/`.
- Don't run /endsession without Matt's explicit permission.
- Agents propose, Matt decides — interpretive attachments verified by a fresh subagent vs LOCAL cache; Matt gates at policy, not per-row.

## Vocabulary to paste into subagents
Pass (numbered corpus sweep) · Track (named workstream) · step (lowercase, ordered piece) · Tier (confidence 1–5 ONLY). Source: `reference/glossary.md`.

## Parked (recoverable) — the causal-arc track
The arc-execution track is at a dip-gated pause (refinements remain, none critical). Prompt parked at `progress/continue-prompts/archive/2026-06-18-causal-arc-execution.md`; restore to live when arc work resumes. Next arc gap if/when: Q12 Battle-of-the-Blackwater downstream (cheapest — `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` exists, 2–3 edges).
