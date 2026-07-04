# Advisory Board — LOREMASTER_VOICE Persona Reframe

> **Status: DELIBERATION ONLY.** One-agent, four-advisor board convened per the S189c
> handoff (`working/query-layer/design.md` §5 step-5c). Nothing here is applied to
> `web/netlify/edge-functions/lib/agent.ts` — this is a proposal for Matt's read and
> a fresh session's/his own hand to paste in before deploy (persona-adjacent text
> per the standing rule requires Matt's sign-off before shipping).
>
> **Fork:** reframe the default `LOREMASTER_VOICE` block around its actual user — Matt's
> only steer, verbatim: *"I want something that a researcher / someone who would read the
> wiki would use kinda thing. I really don't have input other than that."* The S189c design
> note frames this as: *"you are assisting someone doing research and thought experiments on
> the books"* — hypothesis being that the researcher frame licenses fuller, more exploratory
> answers than the current bare encyclopedic register.
>
> **Hard constraint, unmoved by any advisor:** `SHARED_RULES` (theory-scope guardrail, cite
> discipline, the ≥2-quote floor, the quote-marker mechanics, the tool-usage mandates) is
> persona-independent and untouched. This reframe touches `LOREMASTER_VOICE` only — the
> block that ends right before `SHARED_RULES` is concatenated on in `systemPromptFor()`
> (`web/netlify/edge-functions/lib/agent.ts:78-85` is the whole current block; `:116` is
> where `SHARED_RULES` begins). `BLOODRAVEN_VOICE` (lines 88-112) is untouched — it stays the
> toggle-able second persona.

---

## Read-first: the current block, verbatim (for reference)

```
You are a loremaster answering a visitor's questions about the world of A Song of Ice and Fire. You answer from a structured knowledge graph of the books, reached through the tools described below. Your task is to state what the books establish — accurately, plainly, and with sources.

# Voice
- Factual and direct, like a well-written encyclopedia entry. Lead with the answer, then give the causes, the sequence, and the named people, places, and dates, in order.
- Plain declarative sentences in a neutral, informative register. NO mysticism, NO atmosphere, NO imagery or metaphor, NO riddles, NO foreshadowing, NO first-person "voice" or persona. You are a reference, not a storyteller.
- Do not comment on the act of asking ("You ask why…") and do not address the reader. Just give the account.
- Concise. Short paragraphs. State what is known and stop; never pad.
```

Note the framing: it's written entirely from the *speaker's* side (what kind of thing am I)
and never names who's on the other end of the conversation or why they're asking. That
absence is exactly what the reframe targets.

---

## Advisor 1 — The ASOIAF fandom researcher (lives on the wiki/forums)

**Position:** Matt's phrase — "a researcher / someone who would read the wiki" — describes a
very specific, recognizable posture: someone cross-referencing a claim across the show and
the books, building a theory-crafting thread, or trying to reconcile two apparently
contradictory passages. This person doesn't want a Wikipedia summary paragraph; they want a
*collaborator who can trace evidence*. The AWOIAF wiki itself already does the "state the
fact plainly" job — if the persona is just a flatter wiki mirror, it's redundant with the
source it's built on. What a wiki-reader actually values that a wiki page can't give them:

- **Connective reasoning across entries** — a wiki page on "the Trident" and a wiki page on
  "House Baratheon" don't talk to each other; a research assistant can walk the graph and say
  *why* one caused the other, in one answer.
- **Being told what's NOT established**, explicitly and with the same confidence as what is.
  Wiki-readers are used to distinguishing "confirmed" from "fan theory" from "TV-only" — a
  persona that says "the text doesn't give X" in the same breath as stating what it does give
  is doing exactly the epistemic hygiene this audience already practices.
- **A slightly more generous register than encyclopedia-flat.** Real wiki editors and forum
  researchers write with dry enthusiasm, not clinical detachment — compare an AWOIAF talk
  page or a well-argued reddit theory-post to a plain Wikipedia stub. The current voice reads
  more like the second than the first, and that's a small but real loss of the audience it's
  aiming at.

**Wants:** permission to trace implications and connect entries the way a forum poster
piecing together a theory thread would — while still being told plainly where the evidence
runs out. Does NOT want flourish, mysticism, or a persona voice — that's Bloodraven's job,
and mixing them would be the worst outcome.

---

## Advisor 2 — Product/UX voice designer

**Position:** register and length are the two levers that matter here, and they cut in
different directions depending on how literally "researcher" is read.

- **Register:** "encyclopedia entry" is a *closed* register — it signals "look it up and
  leave." "Assisting a researcher" is an *open* register — it signals "let's work through
  this together." The current voice's line *"Do not comment on the act of asking… Just give
  the account"* is a closed-register instruction. If the reframe is going to do anything, it
  has to loosen exactly that clause, or nothing changes — the rest of the current prose
  (factual, sourced, declarative) is compatible with either register and doesn't need to move.
- **Length/exploratoriness risk:** "fuller, more exploratory answers" is the hypothesis to
  test, but exploratory has a failure mode: rambling, hedging, or answering a question that
  wasn't asked. The safe version of "exploratory" is *connective* (drawing lines between
  facts the visitor may not have asked for but that illuminate the answer) — not *discursive*
  (padding with caveats, alternate readings, or meta-commentary about the source material).
  The draft below should explicitly license the former and explicitly still forbid the
  latter, or the "concise, never pad" instruction (which is still good and should survive)
  will fight the new framing turn after turn.
- **A named audience beats an unnamed one.** Every good system-prompt voice section this
  reviewer has seen work names who it's talking to and why, in one line, before laying out
  the rules — it disambiguates every subsequent stylistic instruction. The current block
  never says who the visitor is; it only says what the speaker is. Naming the audience
  ("assisting a researcher") is a cheap, high-leverage change on its own, independent of
  anything else in the block.

**Wants:** one clear audience-naming sentence up top, a register shift from "give the
account and stop" to "help someone work through a question," and an explicit guardrail
distinguishing *connective* fullness from *discursive* padding, so length doesn't balloon.

---

## Advisor 3 — Retrieval engineer

**Position:** the persona text is not just voice — it's load-bearing on tool-routing
behavior, because the model reads the *entire* system prompt (voice + SHARED_RULES) as one
continuous instruction set every turn. Two specific interactions to check:

- **Does "researcher" collide with the theory-gate?** SHARED_RULES already says, forcefully,
  *"do NOT introduce theories… NEVER wink at an answer you cannot cite."* A persona framed as
  "assisting research and thought experiments" could be read by the model as license to
  entertain the visitor's own theory-crafting ("what if Jon really is...") — which
  SHARED_RULES already forbids, but a persona that says "you're helping someone do thought
  experiments" is closer to that line than "you're a reference" was. **This needs an explicit
  clause in the new voice block itself** — not just reliance on SHARED_RULES arriving
  afterward in the same prompt — because voice-block instructions about *what kind of
  thinking to do* interact with rule-block instructions about *what conclusions to avoid*,
  and a model asked to "think through" something is measurably more likely to drift toward
  synthesis than a model told to "state what's established." Cheapest fix: one line in the
  new block that says the thought-experiment framing is about *tracing established
  connections thoroughly*, not entertaining unconfirmed possibilities — a belt-and-suspenders
  restatement, not a rules change.
- **Does it change tool-call behavior?** The routing mandates (resolve→read_node,
  MANDATORY walk_chain for causal, MANDATORY family_tree for lineage) live in SHARED_RULES
  and are unconditional regardless of voice — that's a real firewall and this reframe
  doesn't touch it. But a "fuller" voice could increase the *number* of tool calls per turn
  if the model interprets "researcher" as "gather more evidence before answering" — which is
  actually a *good* interaction (more grounding, more quotes, better use of the ≥2-quote
  floor) as long as it doesn't blow through `MAX_TOOL_ITERATIONS = 6`. Given the tool set is
  narrow (5 tools, no open-ended search yet — pending step 5), the ceiling risk is low today.
  Worth re-checking once `search_quotes` ships (step 5), since a researcher-framed persona
  is exactly the framing most likely to reach for a search tool repeatedly.
- **Caching is unaffected.** Both personas are still stable strings concatenated the same
  way in `systemPromptFor()`; a longer LOREMASTER_VOICE block doesn't change the caching
  mechanics (`chat.ts`'s `cache_control` sits on the composed system blocks either way).

**Wants:** the new block to contain its own explicit "thorough tracing of what's confirmed,
not speculation" restatement (not just trust SHARED_RULES to catch it downstream), and a
note in the A/B eval that specifically re-runs the theory-scope-adjacent questions (any
eval row touching unconfirmed parentage/prophecy framing) to confirm no drift.

---

## Advisor 4 — The skeptic

**Position:** three concrete ways this reframe could go wrong, and what to check before
shipping.

1. **Safety-block leakage risk is real but boundable.** The specific danger isn't that
   SHARED_RULES gets deleted or contradicted (it's textually separate and comes after) — it's
   that the *voice* block starts sounding like it's inviting exactly the thing SHARED_RULES
   forbids ("thought experiments," "what might this mean"), creating a tonal tug-of-war within
   one prompt where two adjacent sections pull opposite ways. The model doesn't parse section
   boundaries as hard walls; it reads the whole thing as one persona. Mitigation: the new
   voice block must not use language that could stand alone as license for speculation
   ("imagine if," "what could this suggest," "explore the possibility") — use "trace," "work
   through the connections," "examine what the text establishes" instead. Verbs matter here.
2. **No test currently pins the voice text — confirmed, and that cuts both ways.** Good news:
   nothing breaks mechanically from editing the string (see Test-pinning finding below). Bad
   news: nothing *catches* a regression either — there's no automated check that the new
   voice still avoids first-person "storyteller" framing, still forbids markdown, still stays
   concise. Those constraints currently live only in `SHARED_RULES` (markdown ban) or as prose
   in the voice block itself (concision, no persona) — the concision/no-persona instruction is
   the one this reframe is editing, so it needs to be re-stated in the new draft, not
   silently dropped because attention moved to the researcher framing.
3. **The "concise, never pad" instruction must survive, explicitly.** The current block ends
   on this line and it's doing real work against a public LLM endpoint with a cost cap
   (`chat.ts`'s daily spend ceiling, `MAX_TOKENS` per request). A "fuller, more exploratory"
   persona is, definitionally, pushing against that same brake. If the new draft drops the
   explicit "stop when you've answered" instruction in favor of vaguer "be thorough" language,
   expect measurably longer average completions — which is a real cost-cap consideration, not
   just a style question. The draft below keeps an explicit stop-condition.
4. **The word "encyclopedia" is being thrown out; make sure nothing else quietly relies on
   it.** A grep of the surrounding code and docs turned up no other place that assumes
   "encyclopedia-style" phrasing or references `LOREMASTER_VOICE`'s literal text (see
   Test-pinning finding) — so this is a clean edit with no other coupling to break.

**Dissent (recorded, not adopted):** Advisor 4 would prefer landing the reframe with the
audience-naming sentence and the explicit anti-speculation restatement, but WITHOUT
Advisor 1's "connective reasoning across entries" language — worried that "connecting
entries the way a forum theory-thread does" is one clause away from re-inviting the
speculation the theory-gate exists to block, and that the safer version of "fuller" is
*more quotes and named specifics*, not *more inference-drawing between facts*. This is a
real, live disagreement with Advisor 1/2 (see Dissents below) rather than a synthesis
point — Matt should read both sides.

---

## Synthesis

**Recommended frame (5 lines):**
1. Name the audience explicitly: the visitor is a researcher / wiki-level reader doing their
   own research or thought-experiments on the series, not a stranger asking trivia.
2. Shift register from "state the account and stop" to "help them work through the
   question" — connective, not discursive; more tool-grounded specifics and named
   people/places/dates, not more hedging or meta-commentary.
3. Keep every existing hard constraint explicit in the new prose rather than relying on it
   surviving by omission: no first-person storyteller voice, no mysticism/imagery, concise
   and stops when answered.
4. Add one restatement (belt-and-suspenders with SHARED_RULES) that "thorough" means tracing
   what the text actually establishes, never entertaining unconfirmed theories or "what ifs"
   — because the voice block is read as one continuous persona with the rules that follow it,
   and the researcher framing sits closer to the theory-gate's line than the old framing did.
5. Do not adopt "connective reasoning across entries" as an explicit license (Advisor 4's
   dissent) — fold the researcher stance into *how thoroughly and specifically it answers*
   (more named specifics, more of the graph's own connections when a tool already returned
   them) rather than *inviting inference-drawing the visitor didn't ask for*.

### Draft replacement for `LOREMASTER_VOICE` (ready to paste, voice only)

```
You are assisting a researcher — someone doing serious research and thought experiments on the world of A Song of Ice and Fire, the kind of person who reads the wiki, cross-references chapters, and wants the text traced carefully, not summarized. You answer from a structured knowledge graph of the books, reached through the tools described below. Your task is to help them work through their question — accurately, plainly, and with sources.

# Voice
- Write for someone doing real research, not someone asking trivia. Be thorough and specific: name the people, places, dates, and sequence of events the tools actually returned, and trace how they connect when the tools give you the connection. Don't summarize down to a single flat sentence when the evidence supports more.
- "Thorough" means tracing what the text establishes carefully and completely — it does NOT mean speculating, inferring, or entertaining a "what if." If the graph doesn't connect two things, say that plainly rather than reasoning your way there. A researcher wants to know the edge of the evidence as much as the evidence itself.
- Plain declarative sentences in a direct, informative register — engaged and precise, not clinical. NO mysticism, NO atmosphere, NO imagery or metaphor, NO riddles, NO foreshadowing, NO first-person "voice" or persona of your own. You are helping with research, not telling a story.
- Do not comment on the act of asking ("You ask why…") and do not address the reader as "you" beyond what's natural in giving a direct answer.
- Answer fully, then stop. Thoroughness is about specificity and traced connections, not length — never pad, never hedge, never add a caveat that isn't grounded in something a tool returned.
```

---

## 3-line rationale
1. Naming the audience ("assisting a researcher... reads the wiki, cross-references
   chapters") is the one change every advisor converged on — it's Matt's literal ask and it
   licenses the register shift without touching a single hard constraint.
2. The register moves from "state and stop" to "trace thoroughly and specifically," which is
   the exploratory-but-bounded middle ground Advisor 2 and the skeptic both wanted — fuller
   via specificity and connection-when-evidenced, not via speculation or padding.
3. The anti-speculation line is stated *inside* the voice block itself (not left to
   SHARED_RULES alone) because the retrieval engineer's finding holds: a model reads the
   whole prompt as one persona, and a researcher/thought-experiment frame sits close enough
   to the theory-gate's line that it needs its own explicit restatement, not just downstream
   backup.

## Dissents worth recording
- **Advisor 4 vs. Advisors 1/2:** whether "connective reasoning across entries" (drawing
  lines between facts the visitor didn't explicitly ask about) should be explicitly licensed.
  The synthesis sided with Advisor 4 — connection-drawing is permitted only *when a tool
  already returned the connection* (walk_chain, neighbors, family_tree results), never as
  freehand inference. This is a real judgment call Matt can overrule; the more generous
  version (explicitly inviting the model to connect graph facts even loosely related to the
  question) would read more like a forum theory-poster and less like a careful researcher's
  assistant, and the board leaned conservative given the theory-gate is the one thing that
  must never regress.
- **Unresolved question for Matt:** whether "engaged and precise, not clinical" (the draft's
  softening of "encyclopedia entry") reads as enough of a register shift, or whether Matt
  wants something closer to Advisor 1's "dry enthusiasm" pitch. The draft is deliberately
  conservative on this axis — easy to loosen further after an A/B read.

## Test-pinning finding
No test pins the current voice text. `web/netlify/edge-functions/lib/agent_test.ts` (the only
`agent`-adjacent test file, confirmed via `find`) contains zero references to `LOREMASTER`,
`systemPromptFor`, or `persona` — grepped directly, no hits. A repo-wide grep for
`LOREMASTER` also turns up only `agent.ts` itself (the constant's definition/comment). This
edit is mechanically safe: no test file needs updating alongside it, and no other file
references the literal prose. The only manual gate is the standing rule that persona-adjacent
prompt text gets Matt's read before deploy, and the A/B eval row below.

## A/B eval note (for the step-5 eval re-run)
Add one eval row comparing **old LOREMASTER_VOICE vs. new draft**, same question set,
same tool stubbing:
- Run a subset of `working/query-layer/evals/questions.md` (recommend: Q11 thematic/meals
  once search ships, one traversal row like Q6, one quote-hunter row like Q12, and any row
  that touches parentage/prophecy-adjacent territory if one exists — to specifically
  stress-test the theory-gate interaction) through both prompt variants.
- Score: (1) answer length/verbosity delta, (2) quote count per answer (floor is 2 either
  way — does the new frame pull more?), (3) any instance of speculative/hedging language the
  old voice wouldn't have produced, (4) tool-call count delta (does "researcher" framing
  increase calls before the answer?), (5) qualitative — does it still read as "helping a
  researcher" rather than drifting into Bloodraven-adjacent atmosphere or first-person voice.
- Pass condition: fuller/more specific answers with zero new theory-gate violations and no
  loop-bound regressions.
