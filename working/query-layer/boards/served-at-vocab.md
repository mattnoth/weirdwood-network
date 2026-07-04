# Board: SERVED_AT / PRACTICES-widening vocab proposal — write now or wait for 8a–c evidence?

> Query-layer track, step-8d fork (design.md §3 D-E, §5 step-8 card). Board convened S189
> per the design doc's advisory-board-fan-out instruction. Deliberation only — no file
> outside this one written; no vocab, no graph mutation.

## Decision

**WAIT-FOR-8ac-EVIDENCE.** Do not write the vocab proposal this session (session C). Write
it after step 5 (search/list/theme) and step 8a/8b (theme index, index repair) ship and the
eval harness (step 3) can score whether the "meals"/descriptive eval rows still fail to reach
event-context answers through retrieval alone.

## Rationale (5 lines)

1. Design.md's own D-E already ranks edge grammar third-order leverage, "gated, last" —
   this board isn't overturning a coin-flip, it's confirming a call the same session already
   made; writing the proposal now would pre-empt evidence the very next steps are built to
   produce.
2. Spot-check of `graph/nodes/foods/*.node.md` (blackberry-tart, black-cherries-in-cream,
   bowl-of-brown) shows the food layer is a **mix**: some nodes have one clean
   food→single-event anchor (Purple-Wedding-supper-adjacent tarts, Illyrio's dinner), others
   (bowl-of-brown) are recurring motifs with no single event to attach to — we don't know the
   ratio without a real census, which 8a/8b's mention-index repair will produce essentially
   for free.
3. Customs orphans sampled (barrow, bedding) are generic wiki culture articles, not
   quote-anchored practice instances — PRACTICES-widening (the cheaper of the two vocab
   options) may not even fit the actual orphan set; that needs investigation the theme index
   would surface, not a same-session guess.
4. The eval harness (step 3) is the mechanism that turns "does search cover this" from a
   vibe into a number; running the fork before that harness exists means the board is
   guessing at exactly the question the harness was designed to answer.
5. Cost is asymmetric: waiting costs a few sessions of latency on a Matt-gated pass anyway
   (edge minting needs his explicit go regardless of when the proposal is drafted); writing
   now costs nothing in isolation but risks anchoring the new-type list (and Matt's mental
   model) on today's 2-node spot-check instead of the real 8a/8b census.

## Advisor positions

- **Traversal purist** — dissents toward WRITE-NOW. "What was served at the Purple Wedding"
  is a real reverse-traversal query no op in the spec answers; the anchor data (located
  quotes naming the event) already exists idle in nodes like `blackberry-tart`. Drafting
  costs nothing and de-risks the eventual pass.
- **Retrieval pragmatist** — WAIT. Step 5 (search + `list --type foods`) likely answers the
  *reachability* half of the meals question outright; the open question is only the
  *aggregation* half ("everything served at event X" as a set), which is narrower than the
  full orphan population suggests. Needs measurement.
- **Vocab guardian** — WAIT, with a scope note: the proposal, when written, must weigh
  PRACTICES-widening vs. a new SERVED_AT type explicitly (architecture.md's own
  deliberation requirement), and the customs sample suggests PRACTICES-widening may be the
  wrong tool for that category — that determination needs the 8a/8b census, not a
  same-session guess.
- **Cost/sequencing lens** — WAIT, strongest voice. The design doc already sequenced this
  (retrieval → index-repair → edge-grammar-last) in the same session; re-opening it now
  without new evidence just re-litigates a decision three lines above the question.

**3 of 4 advisors: WAIT-FOR-8ac-EVIDENCE.** Dissent (traversal purist) noted above and not
overridden by cost — it's a low-cost dissent, but the majority's point stands: the *proposal
content itself* (new type vs. widening, and which nodes qualify) is better-informed after the
census, not before it.

## The eval question that would settle it

Add to the step-3 eval harness's fixed question set (or verify it's already covered by the
"meals" row from the S188 archetype set):

> "What was served at the Purple Wedding?" / "What desserts appear at royal feasts?"

Score after step 5 + 8a/8b ship: does search + theme/list retrieval reach an answer that
**names the dish AND the event context** in one or two tool calls? If yes — the edge pass is
optional polish, not a gap; if the eval still needs 3+ tool calls chaining quote-search →
manual event-inference, or fails to connect dish to event at all, that's the trigger to write
(and prioritize) the SERVED_AT/PRACTICES-widening proposal.
