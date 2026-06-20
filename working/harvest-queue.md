# Harvest Queue — deferred-capture ledger

> **Purpose.** A cheap breadcrumb log for anything *notable but not your current task* that an agent
> notices **while already reading a passage** (a dip, arc research, an audit — any pass over the text).
> You **point**, you do **not** extract. One line per find. A later **harvest pass** batches the
> pointers and does the context-expensive part (slug resolution, dedup, minting node `## Quotes` /
> `object.food` nodes / appearance & description fields / edges).
>
> **Why it exists.** Attaching a find inline mid-task costs real context (resolve the slug, dedup against
> the graph, mint the edge). Dropping a `book / chapter:line / kind / one-liner` pointer costs almost
> nothing and you're already in the text. The graph still gets enriched — just batched, later, by a pass
> whose *whole job* is harvesting. Companion to the FIRM `feedback_capture_quotes_during_research` rule.
>
> **Consumer.** A future "harvest pass" (own track / todo) reads `status: open` rows, opens each
> `chapter:line`, attaches to the graph, and flips the row to `done`. Until then this is a queue, not
> graph state — nothing here is authoritative. Append-only; don't rewrite others' rows.

## `kind` enum (kept tight — split where the graph home differs)

| kind | use for | likely graph home |
|------|---------|-------------------|
| `quote` | a homeless load-bearing line with no beat-node home yet | node `## Quotes` / edge `evidence_quote` |
| `food` | food, drink, or a consumable served (lemon cakes, Arbor gold, sweet beer) | `object.food` node |
| `appearance` | a **character's** physical look — face, body, hair, scars, dress, sigil-worn (first-class for cross-identity matching) | character node appearance field / `## Description` |
| `place` | a **location's** look, layout, or atmosphere (a hall, a godswood, a ruin) | `place.location` node description |
| `object` | an **artifact/material's** look, material, or provenance (a sword's blade, a crown) | `object.artifact` / `object.material` node |
| `hospitality` | guest-right, host-guest custom, a feast-as-event, bread-and-salt | `event.feast` / `GUEST_OF` / custom edges |
| `foreshadowing` | a planted detail / Chekhov's gun | `FORESHADOWS` edge → event |
| `relationship` | an asserted tie worth an edge that isn't your task | typed edge |
| `other` | notable but none of the above — say what in `note` | triage at harvest |

> **Bucket evolution — smoke test, don't pre-engineer (Matt, S108):** this enum is a starting point.
> **Review gate: after the next ~2 dips' worth of rows**, check (a) which buckets actually filled,
> (b) whether any need splitting/merging (e.g. `place` dividing into layout-vs-atmosphere), and
> (c) whether to harden the push from memory → CLAUDE.md/hook. Until then: leave the enum and the
> memory-only push as-is. Don't pre-engineer buckets nobody is filling.

## Paste-into-every-dip/research-subagent-prompt snippet (canonical — copy verbatim)

> While you read these chapters/passages for your task, ALSO drop one-line pointers to anything
> *notable-but-not-your-task* into `working/harvest-queue.md` — append a row:
> `| open | <kind> | <book> | <chapter:line> | <short note or verbatim snippet> | <this session/track> |`.
> Kinds: `quote` (homeless load-bearing line) · `food` (food/drink/hospitality consumable) · `appearance`
> (a character's physical look/dress) · `place` (a location's look/atmosphere) · `object` (an
> artifact/material's look or provenance) · `hospitality` (guest-right/host-guest custom) ·
> `foreshadowing` · `relationship` · `other`. POINT, don't extract; don't stop your task to attach it;
> don't pre-dedup. If nothing notable comes up, add nothing.

## Queue

| status | kind | book | chapter:line | note | found during |
|--------|------|------|--------------|------|--------------|
| open | appearance | agot | agot-eddard-13:35 | Renly in bloodied hunting greens just after the boar kills Robert | S108 B3 research |
| open | quote | agot | agot-eddard-13:169 | Ned refuses to seize Cersei's children while Robert dies: "I will not dishonor his last hours on earth by shedding blood in his halls" — homeless load-bearing (Ned's fatal honor); no beat-node home | S108 B3 research |
| open | food | agot | agot-eddard-14:43 | "a cup of sweet beer" offered to Pycelle in the Hand's solar — hospitality detail | S108 B3 research |
| open | appearance | agot | agot-eddard-14:49 | Littlefinger "blue velvets and silver mockingbird cape … boots dusty from riding" | S108 B3 research |
| open | appearance | agot | agot-eddard-14:51 | Varys "in a wash of lavender, pink from his bath, his plump face scrubbed and freshly powdered, his soft slippers all but soundless" | S108 B3 research |
| open | food | agot | agot-eddard-15:157 | "bread and cheese and the milk of the poppy" — `object.food` (bread/cheese) + `concept.medical` (milk of the poppy); the quote itself already attached to `ned-confesses-to-treason` | S108 B3 research |
