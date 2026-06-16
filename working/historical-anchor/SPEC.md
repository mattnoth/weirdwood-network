# Historical-Anchor Structural Attachment — Subagent Spec (POST-PLATE-5 followup #9, wave 1)

**Goal:** A major historical event hub (e.g. `tourney-at-harrenhal`) sits ISOLATED in the
graph (0–2 edges) even though the underlying facts already exist — in the node's own
wiki body (Known Attendees / joust / melee / battle results) and, for some participants,
as cited book dyads. Your job: produce JSON-ready edges that **attach the participants,
location, and parent-event** to the hub so it becomes traversable. You are NOT extracting
new facts — you are connecting facts that already exist to their parent hub.

You will be told ONE hub slug. Work only on that hub.

## Read these (local only — NEVER fetch over the network)
1. `graph/nodes/events/<hub>.node.md` — the hub node. Its body usually already contains the
   authoritative participant list, joust/melee/battle results, and book quotes. This is your
   primary source.
2. `sources/wiki/_raw/<PageName>.json` — the raw wiki cache page (the node's `wiki_source`
   gives the page name). Use for anything the node body abbreviates.
3. Chapter files under `sources/chapters/<book>/` — ONLY to grab a verbatim book quote when a
   participant's involvement is narrated on-page (so you can tier the edge as book-grounded).
   grep for the participant + event terms.

## What edges to emit (per hub)

Emit one JSON object per line to your output file. Use these edge types:

- **`LOCATED_AT`**  `<hub> → <place-slug>` — the event happened at a place. Emit ONLY if a
  place node exists (you'll be told which place slugs are valid). One per hub.
- **`PART_OF`**  `<hub> → <war-slug>` — if the hub is a battle/event that belongs to a named
  war already in the graph (e.g. `battle-of-the-trident → roberts-rebellion`) AND that edge
  doesn't already exist. One per hub at most.
- **Participant attach edges** (Person/House → hub):
  - `FIGHTS_IN` — combatants: jousters, melee fighters, named battle combatants, champions.
  - `ATTENDS` — non-combatant attendees: spectators, guests, witnesses, the host.
  - `COMMANDS_IN` — for battles only: a commander/orderer who directed but didn't personally fight.
  - `VICTIM_IN` — for battles/sacks: someone killed or victimized in the event (e.g. Elia
    Martell in the Sack of King's Landing).
  - `AGENT_IN` — for battles/sacks: someone who performed a signature act (e.g. Jaime killing
    Aerys; Gregor killing Rhaenys).
  Pick the SINGLE best-fitting type per participant. Do not emit two role edges for the same
  person on the same hub.

Resolve every participant to an existing node slug. You'll be given a way to check slugs
(`python3 scripts/graph-query.py <slug>` prints the node if it exists; non-zero/empty = no
node). If a participant has NO node, SKIP them and list them under `unresolved` in your notes —
do NOT invent nodes.

## Provenance + tier (STRICT — this is the project's core quality rule)

Every edge carries an `evidence_kind` + `confidence_tier`:

- **Book-grounded** (you found a verbatim chapter quote narrating this participant's
  involvement): `evidence_kind: "book-pass1"`, `evidence_book`, `evidence_chapter`,
  `evidence_ref: "sources/chapters/<book>/<file>.md:<line>"`, `confidence_tier: 1` (or `2` if
  the involvement is recalled/second-hand). Quote must be VERBATIM from the file.
- **Wiki-only** (the fact is in the wiki node body / attendee list but you found no on-page
  book quote): `evidence_kind: "wiki-historical-anchor"`, `evidence_ref: "wiki:<PageName>"`,
  `confidence_tier: 2` MAX (never tier-1 for wiki-only). `evidence_quote` = the relevant
  sentence from the wiki node body.

Tier-1 is earned ONLY by a real book quote. When in doubt, tier down.

## Output (write these files; do not touch the graph)

1. `working/historical-anchor/<hub>.candidates.jsonl` — one edge object per line. Schema per edge:
```json
{"edge_type":"FIGHTS_IN","source_slug":"rhaegar-targaryen","target_slug":"tourney-at-harrenhal","decision":"emit_edge","candidate_kind":"historical-anchor-w1","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-eddard-15","evidence_quote":"<verbatim>","evidence_ref":"sources/chapters/agot/agot-eddard-15.md:45","confidence_tier":1,"typed_by":"curator-historical-anchor","asserted_relation":"Rhaegar was champion of the joust at Harrenhal","schema_version":"pass1-derived-v1","produced_at":"2026-06-15T00:00:00+00:00"}
```
   For wiki-only edges, drop `evidence_book`/`evidence_chapter`, set `evidence_ref":"wiki:<Page>"`, `evidence_kind":"wiki-historical-anchor"`, `confidence_tier":2`.

2. `working/historical-anchor/<hub>.notes.md` — short: which place/war you attached, count of
   FIGHTS_IN vs ATTENDS vs role edges, book-grounded vs wiki-only counts, any `unresolved`
   participants (named, no node), and anything you deliberately skipped + why.

3. `working/historical-anchor/quotes/<hub>.quotes.jsonl` — see "Capture incidental quotes" below.
   (Skip the file only if the chapters you read yielded zero load-bearing quotes beyond your edges.)

## Capture incidental load-bearing quotes as you go (FIRM project rule)

While you are already inside the chapter/wiki text grounding your edges, you WILL pass other
load-bearing verbatim quotes. The project rule (`capture-quotes-during-research`): **every pass
over the text must enrich the graph — do not let a quote you found go uncaptured.** Beyond the
quotes you use as edge evidence, watch especially for the project's first-class targets:

- **Food / hospitality / feast detail** (bowls of brown, what was served, guest-right moments)
- **Physical descriptions** of characters/places (appearance, sigils-in-scene, the look of a castle)
- **Cross-identity / disguise tells** (a character recognized, a name slipping, an alias moment)
- Any other quote that is the BEST direct-text evidence for a fact about an existing node.

For each such quote, append one line to `working/historical-anchor/quotes/<hub>.quotes.jsonl`:
```json
{"target_node_slug":"<existing node slug>","category":"food|physical|identity|other","quote":"<verbatim substring>","source_ref":"sources/chapters/<book>/<file>.md:<line>","why":"<one line: what node fact this evidences>","produced_at":"..."}
```
Rules: quote must be a VERBATIM substring; `target_node_slug` must resolve via
`python3 scripts/graph-query.py <slug>` (skip + omit if no node); these are CANDIDATES for a
node `## Quotes` section — do NOT edit node files yourself. Bound it (the strongest few per
chapter, not every line). This is additive and node-scoped, so it is safe to run alongside
other agents.

## Rules
- Do NOT modify `graph/`, `edges.jsonl`, `sources/`, or any node file. Output is candidates only.
- Do NOT duplicate an edge that already touches the hub (check `python3 scripts/graph-query.py --neighbors <hub>` first; if it's 0/0 there's nothing to dedupe).
- Every `evidence_quote` must be a real substring of its cited source. No paraphrase in quotes.
- Bound it: attach the named, node-resolved participants the wiki lists. Don't invent minor
  unnamed attendees ("House Mormont members") unless a specific named node exists.
- Your final message: a 4–6 line summary (hub, # edges by type, book vs wiki split, unresolved count).
