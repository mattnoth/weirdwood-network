---
session: 186
date: 2026-07-03
track: meta (chat-UI)
model: claude-opus-4-8
api_cost: ~$0.30 (live Opus smoke turns)
---

# Session 186 — Usage logging live, two personas, the theory-leak guardrail, ≥2-quote policy

## Context: a four-agent working tree

This session ran in a shared working tree alongside a **logging agent** (production
logging fixes) and a **styling agent** (Spectral font + header/landing polish + a font
lab), with the S185 chronology work just landed. Coordination was the hard part, not the
code. Key facts that shaped the session:

- The logging agent committed + pushed + **deployed** the S185 code (chronology, logging,
  three-eyed-raven rename, styling) while this session was mid-flight. It also raised the
  spend cap 5→$50, flipped the prod model Sonnet→Opus, added `failedTurn()` logging, fixed
  the empty-`question` bug, and wrote `DEPLOY.md`. All captured in
  `working/s186-production-logging-followup.md` and folded into the worklog + Active Decisions.
- A near-miss: the committed `chat.ts` imported `systemPromptFor`/`Persona` from `agent.ts`,
  but `agent.ts` was uncommitted — so **HEAD was briefly inconsistent** (a clean checkout
  would 502). The live site was fine (deploys ship the *working tree*, which had both). This
  session's persona commit closed the gap. Lesson reinforced: with multiple agents on one
  tree, commit the *interdependent halves together* or verify HEAD consistency.

## The theory leak (the substantive finding)

Matt caught the Bloodraven persona ending a Robert's-Rebellion answer with "the quiet chamber
in Dorne where its last secret still sleeps" — a wink at R+L=J. Diagnosis: the grounding
machinery gates **citations and verbatim quotes** (locked to tool returns) but **not the prose
voice**. Nothing in the system prompt forbade alluding to fan theories, and the persona had an
explicit "symbolism… a single quiet image" license — the exact hole the hint slipped through.
So theories weren't "integrated" into the graph; they were seeping out of the model's weights
into the ungated flourish.

Fix: a **scope guardrail** written as its own block in the *shared* prompt (not the voice), so
it applies to every persona and can't be dropped by switching voice. It forbids asserting,
alluding to, or foreshadowing unconfirmed theories / hidden parentage / "true" identities, and
says to state "the books don't reveal it" rather than wink. Live-verified: "Who are Jon's
parents?" now gives the factual bastard-of-Ned answer and explicitly says the mother is never
named — no R+L=J wink, in both voices.

## Two personas (the design)

Matt asked for a dry, factual "loremaster" voice that reads like a wiki, as an alternative to
the atmospheric "spooky guy," with the spooky one kept as a toggle. Architecture: split the one
system-prompt string into `LOREMASTER_VOICE` (default) + `BLOODRAVEN_VOICE` (toggle) +
`SHARED_RULES` (tools, grounding, quote machinery, scope guardrail, forced quotes);
`systemPromptFor(persona)` composes voice + shared. The two knobs — *voice register* and
*scope/grounding* — are deliberately separated so either can change without touching the other.
A factual voice is structurally more leak-resistant (kill the imagery license, kill the hint
vector) but is **not** a substitute for the scope rule (a dry voice can still assert a theory as
fact), so both ship. Front-end: a sticky localStorage toggle in the composer; the bot-bubble
label follows the choice; persona rides on each `/api/chat` request and is logged.

Portfolio angle noted for Matt: the factual voice may *demo the graph better* — flourish reads
as "the model being creative," which hides the retrieval; dry facts + citations + the chain
panel read as "real grounded retrieval."

## Quote policy

Matt: quotes are the value — floor of **two** verbatim quotes per answer (was one), and stop
rationing them. Relaxed the evidence-discipline rules ("one quote per beat", "prefer paraphrase",
"cut a quote that does no work") to "quote generously, keep each short, prefer the book's own
words." No-fabrication rules still win; family-tree caption / greeting / <2-lines-returned are
the only exceptions. Live-verified: a Red Wedding answer carried 5 quote markers.

## Also this session
- Chronology downstream-inversion fix (`graph.ts linkSortKey` — an undated chain root borrows its
  effect's key) + regression test; live Rebellion downstream now reads cause→effect.
- Everything deployed to prod and smoke-tested (both voices, theory guardrail, ≥2 quotes, no key
  leak). Matt began using the site + populating logs at session close.
