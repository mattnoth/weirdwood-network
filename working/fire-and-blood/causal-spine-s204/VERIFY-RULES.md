# S204 fresh-verify — RULES (paste-target for every verifier subagent)

You are an INDEPENDENT verifier with no prior context. You did not propose these
edges. Your job is adversarial: try to REFUTE each proposed edge against the
primary text. Do not rubber-stamp; when uncertain, say ADJUST or REJECT, never
CONFIRM.

## Inputs
- Your assigned proposal file: `working/fire-and-blood/causal-spine-s204/proposals/<ID>.json`
- Source text: `sources/chapters/fab/<chapter>.md` for each edge's `chapter` field.
  Read the REAL text around each quote (±40 lines) — judge from context, not the
  quote alone.
- The causal-type rubric (the choice of type is load-bearing):
  - TRIGGERS — immediate spark; B is the very next beat, nothing decisional between.
  - CAUSES — A produces B, mediation allowed. Real causation asserted/narrated by the text.
  - ENABLES — precondition/door-opener; a third party or free decision produces B.
    Campaign step→step transitions are ENABLES, never CAUSES.
  - MOTIVATES — A drives a decision; target is the deciding CHARACTER or the
    decision-EVENT. The SOURCE must be the motivation, not the actor.
  - PREVENTS — A blocks B, only when the text states it.
  - PART_OF — component battle/sub-event → its war. SUB_BEAT_OF — beat inside a
    named event hub. Role edges (AGENT_IN/VICTIM_IN/WITNESS_IN/COMMANDS_IN etc.)
    — the person/entity actually filled that slot in the event.
- Tier rules: plain Gyldayn narration = tier-1. Hedged/partisan/disputed text
  requires tier-2 + disputed:true + in_universe_source. SUSPECTED_OF caps tier-2.

## For EACH edge, judge:
1. QUOTE — is the quote really in the named chapter, and does the surrounding
   text mean what the edge claims? (Watch for quotes torn out of context.)
2. GROUNDING — does the text actually assert/narrate this causal (or role)
   relation, or is it mere sequence/co-occurrence? (The sequence-only trap:
   chronological adjacency is NOT causation.)
3. TYPE — is this the right rung of the ladder? (Would ENABLES be honester than
   CAUSES? Is the "immediate spark" claim of TRIGGERS true? Does MOTIVATES point
   at motivation→actor/decision?)
4. DIRECTION — cause→effect, not backwards.
5. TIER — does the text hedge ("some say", "Mushroom tells us", "it was
   whispered", "a matter of some dispute")? Then tier-2 + disputed + source.
6. AGENCY — if a human decision mediates A→B and the edge says CAUSES/TRIGGERS,
   that is agency-collapse: suggest MOTIVATES/ENABLES instead.

## Verdicts
- CONFIRM — grounded, right type, right direction, right tier.
- ADJUST — the relation is real but something is off (type rung, tier/disputed,
  endpoint slug). Give the exact correction.
- REJECT — not grounded in the text / context contradicts / sequence-only.

## Output — ONE file, valid JSON
Write `working/fire-and-blood/causal-spine-s204/verifications/<ID>.json`:
```json
{
  "assignment": "<ID>",
  "verdicts": [
    {"id": "<edge id>", "verdict": "CONFIRM|ADJUST|REJECT",
     "reason": "<1-2 sentences; for ADJUST give the exact fix, e.g. type CAUSES->ENABLES>"}
  ],
  "new_node_checks": [
    {"slug": "...", "verdict": "OK|PROBLEM", "reason": "<era/year/type sane? genuinely missing from graph? identity accurate?>"}
  ]
}
```
Every edge id in the proposal file gets exactly one verdict row. Your final text
reply: counts only (N CONFIRM / N ADJUST / N REJECT + the ids of non-CONFIRMs).
