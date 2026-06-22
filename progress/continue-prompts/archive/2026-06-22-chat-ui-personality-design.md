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
- **Spoiler-gating (`first_available`) is DEFERRED — and stays deferred for this session.** It is gated on a
  fixed precondition: the remaining narrative-arc skeletons (NORTH / AEGON / Bran / WO5K-remainder) built +
  the dip-enrichment passes run over them; only THEN does the deterministic backfill happen. **Do NOT reopen
  that deferral here.** For the persona, treat spoiler behavior as a **full-knowledge default for now**, with a
  "read up to book/chapter X" gate noted as a *known future layer* the persona will support once the field
  backfills — design the voice so that gate can slot in later without a rewrite. This is a note-and-move-on
  item, not a design fork.
- **Theory nodes** exist at Tiers 4–5 (e.g., the deferred theories track) — the persona needs an uncertainty/
  hedging stance for these.

**Do NOT treat `history/archive/sketches/chat-ui-architecture.md` as spec** — memory flags it as a STALE sketch
(shared-password auth / D&D-group framing), NOT Matt's current design. Mine it for ideas only.

## Open design questions to settle WITH Matt (ask — don't assume)
1. **Voice register:** in-world (speaks as if from Westeros — a maester, an oracle) vs out-of-world (a neutral
   literary scholar/analyst) vs a toggle between them?
2. **Persona identity:** a *named* character voice (a Citadel maester, Samwell, a weirwood/three-eyed-crow
   oracle) or an unnamed knowledgeable guide?
3. ~~Spoiler stance~~ — **NOT an open question.** Spoiler-gating is deferred (see context above): persona
   default = full-knowledge now, "read up to X" gate = known future layer. Design the voice to accommodate the
   gate later; do not treat it as a fork to resolve, and do not pull `first_available` forward.
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
