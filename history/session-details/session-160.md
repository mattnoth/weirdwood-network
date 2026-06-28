---
session: 160
date: 2026-06-27
track: graph/meta (chat-UI persona + enrichment design)
model: Opus 4.8
type: design / live demo (no graph mutation)
---

# Session 160 — Chat-UI demo: the dry-Bloodraven persona over the live graph

## What this session was

Matt ran a **live demo of the knowledge graph as a chat UI**, using the orchestrator as a stand-in
front-end voiced in a **dry Bloodraven persona**. He fed it three friend-style questions; each was answered
by querying the real graph (`scripts/graph-query.py`, `graph/edges/edges.jsonl`, node bodies, chapter text),
not from model memory. No graph mutation — this was a design + voice-calibration session that surfaced a
concrete enrichment need and a few backlog items.

The chat-UI persona spec was never written (the S122 design track is archived, `working/chat-ui/` was empty).
Matt is now shaping the voice organically through the demo, so the durable output is **calibration notes**, not
a finished spec.

## The three questions and what they exercised

1. **"Jon's reaction when he learned Robb was killed — who was he with?"** — Answered honestly that **the books
   contain no such scene**: Jon is never shown being told; the knowledge appears already-settled in his POV
   (`asos-jon-10:15`), and the grief is reflective (`asos-jon-12:63` godswood/Ghost; `adwd-jon-01:51`). A
   book/show divergence (the show invents the Sam-tells-Jon scene). This is exactly the case where a naive LLM
   hallucinates a scene that doesn't exist — the persona's value is saying "no." Matt singled out the closing
   line ("he was with a direwolf, and otherwise no one. The text gives you a man's grief, not the giving of the
   news.") as the target voice.

2. **"Diagram the succession Aegon I → Joffrey."** — The graph **does** have the full `SUCCEEDS` chain end to
   end (17 Targaryen kings → Robert I → Joffrey, traced from edges, not memory). Rendered via the visualize
   widget — but **it didn't display in Matt's terminal client** (widget renders on web/app surface only). Fixed
   by falling back to a text ladder + `qlmanage` SVG→PNG (`SendUserFile`). Lesson for a real chat UI: needs a
   render-to-file fallback for terminal contexts.

3. **"What do you know of the white walkers — who's seen them, where from, are wildlings in league?"** — The big
   one. Answered from `graph/nodes/species/others.node.md` + chapter cites: nature, sightings (Waymar/AGOT
   prologue, Eastwatch fisherfolk, the Fist, Sam the Slayer), origin (Lands of Always Winter / Long Night, true
   origin a deliberate mystery), and the **wildlings-flee-not-ally** answer (Mance unites them to escape; Tormund
   `adwd-58`; Craster the lone appeaser). Surfaced two follow-on findings (below).

## Findings / decisions

- **Persona voice rules (Matt-locked, live).** Captured in `working/chat-ui/bloodraven-persona-notes.md`:
  no self-introduction (opener is bare "Ask your questions…"); **never volunteers his own biography/service** —
  instead drops a *light* tidbit about people he knew ("When I knew him, he was…") then stops, user must ask;
  **no meta/provenance editorializing to the user** (the "recorded succession, not my reckoning" line was too
  strong and killed the preceding beat — citations are the dev view, not the persona's mouth); **no over-cute
  obscure references** ("the Unworthy got me" = Aegon IV sired him — opaque; "got" for "sired" doubly flagged);
  honest about text gaps. Golden lines preserved verbatim as calibration anchors.

- **Quote-first persona (the core design call).** Matt's critique of the first Others answer: it **paraphrased
  everything and quoted nothing** — the cardinal sin for this project, whose whole value is verbatim navigable
  text. The fix is **summary-with-embedded-quote**: the sentence carries the claim, the verbatim line sits right
  where the claim lands ("their sword → *'a shard of crystal so thin it seemed almost to vanish'*"). Demonstrated
  by re-answering with a real quote per claim + a dev-view evidence table.

- **Description-quote enrichment (the need this exposed).** For the persona to answer quote-first **at
  answer-time**, the quotes must already live on the node, keyed by claim-facet. The `others` node's `## Quotes`
  was **empty** (body = non-navigable wiki `cite_ref` tags), so quotes had to be grepped live. Matt: "maybe we
  need an enrichment on descriptions of the Others or something." Captured in `working/arc-enrichment-backlog.md`
  as a **generalization of the existing food "ask-and-get-descriptions" model** to a small curated set of
  description-rich non-food classes (supernatural creatures, signature weapons, a few iconic structures);
  deterministic-first mechanism (entity-index → grep candidate descriptive lines → agent selects/frames best
  verbatim per facet → verify line-exact → attach to `## Quotes`); Others as the named pilot. Gated, not launched.

- **Bug found (cleanup chip spawned).** The `others` node carries 3 bogus `GUEST_OF` out-edges
  (→ stannis-baratheon `acok-prologue:287`, → godric-borrell, → ysilla) — slug-collisions on the common word
  "others" in prose. Spawned a background task to remove them + audit the broader common-word slug-collision
  class + the incoming `SWORN_TO` wight edges.

## Artifacts touched

- NEW `working/chat-ui/bloodraven-persona-notes.md` — voice rules + golden lines + anti-patterns.
- `working/arc-enrichment-backlog.md` — description-quote enrichment block (next to the food rule).
- `working/harvest-queue.md` — +8 rows (Others/Eastwatch load-bearing quotes for the pilot to attach).
- `working/todos.md` — lineage-charts + chart→graph wiring (to discuss); persona tidbit-behavior pointer.
- Spawned cleanup task (no repo file) for the `others` slug-collision edges.
- Scratchpad only (not committed): succession.svg / succession.png.

## What's next

No new fireable track — the chat-UI / description-quote-enrichment thread is **backlog** (captured, gated). The
live next remains the enrichment cadence: **A2.4 Tyrion / Essos** (renumbered to fire as **S161** after this
meta session took S160).
