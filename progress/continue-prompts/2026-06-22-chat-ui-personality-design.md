# Continue — Chat-UI personality / voice design (standalone track, Matt-opened S122)

> **Recommended model:** Sonnet 4.6 (design + drafting candidate personas + sample transcripts). Opus only if
> Matt wants deeper persona/voice reasoning.
> **This is a DESIGN session — no graph mutation, no extraction, no wiki fetch.** Deliverable is a spec doc.
> **Independent of the graph-build tracks** (WO5K-remainder etc.) — can run in its own window, any order.

## Goal
Design the **personality / voice the chat UI uses** when people query the Weirwood ASOIAF knowledge graph —
the persona that *answers* questions like "who killed Jon Arryn?", "how are Littlefinger and Lysa connected?",
"what was served at the Red Wedding?", "is R+L=J supported?". Output = a **personality spec** that will become
the system-prompt basis for the chat layer.

## Context the persona must fit (read `reference/architecture.md` first)
The real deliverable of this whole project is the **knowledge graph** (`graph/nodes/` typed entities +
`graph/edges/edges.jsonl` ~22.4k cited edges). The chat UI is the front-end people use to *ask* it things.
The persona's behavior has to match what the graph can actually answer + cite:
- **Confidence Tiers 1–5** are stamped on data: Tier 1 = verified canon … Tier 5 = crackpot. The persona should
  *distinguish* canon from theory, not flatten them.
- **Book citations** — many edges/nodes carry `book chapter:line` cites (navigable provenance). The persona can
  surface evidence ("per AGOT, Eddard XII…").
- **In-world vs meta** — the graph separates in-world entities (Red Wedding, Tywin) from out-of-universe `meta.*`
  (chapters, the books themselves). The persona's voice has to pick a stance on this boundary.
- **Spoiler-gating (`first_available`) is DEFERRED** (not built). So the persona's spoiler behavior is an OPEN
  design choice, not something the data enforces yet — see open question 3.
- **Theory nodes** exist at Tiers 4–5 (e.g., the deferred theories track) — the persona needs an uncertainty/
  hedging stance for these.

**Do NOT treat `history/archive/sketches/chat-ui-architecture.md` as spec** — memory flags it as a STALE sketch
(shared-password auth / D&D-group framing), NOT Matt's current design. Mine it for ideas only.

## Open design questions to settle WITH Matt (ask — don't assume)
1. **Voice register:** in-world (speaks as if from Westeros — a maester, an oracle) vs out-of-world (a neutral
   literary scholar/analyst) vs a toggle between them?
2. **Persona identity:** a *named* character voice (a Citadel maester, Samwell, a weirwood/three-eyed-crow
   oracle) or an unnamed knowledgeable guide?
3. **Spoiler stance** (intersects the deferred `first_available` work): full-knowledge, or warn/gate by a
   user-set "I've read up to book/chapter X" point? This is the highest-leverage choice — it may pull the
   deferred spoiler-gating work onto the critical path.
4. **Evidence surfacing:** how much does it cite? Show Tier? Distinguish Tier-1 canon from Tier-4/5 theory?
   Hedge on low-confidence claims vs state them flat?
5. **Tone:** scholarly / playful / dramatic / terse? How it handles "we don't know" (genuine series mysteries).
6. **Boundaries:** how it represents graph *gaps* (says "not in my records" vs hallucinates); in-character
   refusals; out-of-scope (real-world) questions.
7. **Audience:** the D&D group / general fans / Matt himself? (shapes assumed familiarity + spoiler default)

## Approach
1. Read `reference/architecture.md` (entity types, confidence Tiers, in-world-vs-meta, spoiler-gating section)
   so the persona's promises match the graph's actual capabilities.
2. Draft **2–3 candidate personas** (e.g., "Citadel Maester," "neutral graph-scholar," "three-eyed-crow oracle")
   each with a short **sample Q&A transcript** over real graph content, so Matt compares *voices concretely* —
   not abstract adjectives.
3. Walk Matt through the open questions; lock the choices.
4. Write the spec.

## Deliverable
`working/chat-ui/personality-spec.md` — voice register, persona identity, spoiler stance, citation/evidence
behavior, Tier-handling, tone, refusal/boundary rules, and 2–3 sample transcripts. This is the system-prompt
foundation for the chat layer. Update worklog + todos at the end (note: this opens a new **chat-UI track**
distinct from the graph-build tracks).

## DO NOT
Mutate the graph · re-fetch the wiki · treat the stale `chat-ui-architecture.md` as spec · run `/endsession`
without explicit permission.
