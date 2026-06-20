# Session 108 — B3 Ned's-downfall arc + the harvest-queue mechanism (2026-06-19)

**Model:** Opus 4.8 orchestrator + 3 Sonnet 4.6 `general-purpose` subagents (1 arc-research, 1 fresh edge-verification, 1 graph-only re-dip).
**Shape:** hybrid — the first half was pure execution (reuse the proven arc-mint machine for B3); the second half was a design conversation that produced a new standing mechanism (the harvest queue). This detail file exists for the second half; the B3 record is concise because the worklog entry already covers it.

---

## Part 1 — B3: the Ned's-downfall arc (execution)

**The gap.** The post-B1 re-dip (S107) left Q10 partial: `execution-of-eddard-stark` carried rich role edges (Joffrey `COMMANDS_IN`, Ilyn Payne `AGENT_IN`, Ice `WIELDED_IN`) but **zero upstream causal chain** — "what set Ned's execution in motion / who is to blame" returned nothing causal. The arrest cluster around `agot-eddard-14` was already dense (the `arrest-of-eddard-stark` hub + 3 SUB_BEAT_OF children, all with role edges), but no causal edges connected any of it.

**Built it with the proven 7×-machine:** research subagent (dedup + verbatim quotes + edge proposal) → orchestrator trims/decides the hard interpretive calls → `scripts/mint_b3_ned_downfall_arc.py` (backup + re-run guard) → targeted index + alias rebuild → fresh-subagent verify → `--causal-chain` smoke → re-dip.

3 new beats (`death-of-robert-baratheon` [event.assassination — the boar hunt, missing entirely], `ned-discovers-the-truth-of-joffrey-s-parentage` [the root], `ned-confesses-to-treason` [forced false confession, SUB_BEAT_OF execution]) + 14 edges (9 role/structural + 5 causal Tier-2).

**Causal spine (all Tier-2):**
```
discovery --MOTIVATES--> {eddard-stark, cersei-lannister}      (root motivations)
death-of-robert-baratheon --CAUSES--> arrest --CAUSES--> execution
ned-confesses-to-treason --TRIGGERS--> execution               (immediate public spark)
```

**Interpretive calls I made (the "Opus only for a hard call" part):**
- **`event.assassination` for Robert's death**, NOT the research agent's suggested `event.death` — which isn't even a schema type. The architecture type table literally lists "Death of Robert I via boar hunt" as the canonical `event.assassination` example; the weaponized-accident (Cersei's strongwine via Lancel) is exactly the case it covers.
- **Hub-level causal spine, not sub-beat level.** The research agent proposed `gold-cloaks-betray-ned CAUSES arrest-of-eddard-stark` — but that beat is already `SUB_BEAT_OF` the arrest. A beat can't both be *part of* an event and *cause* it; that's a contradiction. So I connected at the hub level (death → arrest → execution) and put the within-arrest agency (Littlefinger) on role edges instead.
- **Agency-collapse, honored:** Lancel `AGENT_IN` + Cersei `COMMANDS_IN` the death; Littlefinger's betrayal modeled as an *additive* `petyr-baelish COMMANDS_IN gold-cloaks-betray-ned` (the beat previously credited only Cersei) — and I caught that the `petyr-baelish BETRAYS eddard-stark` dyad **already existed** (verified vs `edges.jsonl`, not node prose), so I didn't re-mint it. Joffrey's choice = the pre-existing `COMMANDS_IN execution` edge.
- **Hard-stop held:** nothing into `war-of-the-five-kings`.

**Verification discipline paid off again:** all the research agent's quotes were accurate this time (I spot-checked every load-bearing line number before minting), but the slug work mattered — I used `robert-baratheon` (58 AGOT in-saga edges) for the death beat, NOT the `robert-i-baratheon` wiki/historical dup that the todos had *mislabeled as canonical* (a stale assumption from the S106 Sack-of-KL context). Corrected that todo's merge-direction note.

**Result:** edges 22241 → 22255, nodes 8539 → 8542, orphans 62 unchanged, 128 edge types, pytest 1307 pass / 1 documented `cwd-is-tmp` fail. Fresh verifier returned ALL-CONFIRM on all 9 interpretive edges. Post-B3 re-dip: **Q10 partial → CORRECT**, and **Q8 partial → CORRECT** (first measure of the post-B2 graph). Arc layer now 8 correct / 1 policy-stop-short / 2 partial.

---

## Part 2 — The harvest queue (design)

**How it started.** Matt asked whether we were picking up other quotes/notations while going through the book — recalling a rule from ~15 sessions back. That's `feedback_capture_quotes_during_research` (FIRM: attach load-bearing quotes whenever a session is in the text). Honest answer: the B3 beats were enriched inherently (every node has `## Quotes`, every edge an `evidence_quote`), but my research subagent had read *past* several incidental load-bearing quotes that weren't part of B3's spine. I homed the two that mattered (Littlefinger's bribe setup + the Sansa-head coercion).

**Matt's actual ask** went further: when an agent is already in a passage for *any* reason, it should jot down pointers to notable-but-homeless things — quotes, **food**, **physical descriptions** — as a simple table with `chapter/line`, to act on later. "Wouldn't that save context?"

**Why it saves context (the real mechanism).** Attaching a find inline mid-task is the expensive part: resolve the slug, dedup against the graph, mint the edge/node. Dropping a `book / chapter:line / kind / one-liner` pointer costs almost nothing, and the agent is *already in the text*. So: point now, batch-attach later via a dedicated **harvest pass** whose whole job is draining the queue. Built `working/harvest-queue.md` (append-only table + a `kind` enum + a canonical paste-snippet) seeded with 6 real S108 finds.

**Three corrections from Matt, each sharpening the design:**

1. **"description is not very tight."** The flat `description` bucket lumped a character's looks, a place's atmosphere, and an object's appearance — three things with *different graph homes*. Split into `appearance` (character → cross-identity-relevant), `place` (location), `object` (artifact/material).

2. **"should be a part of each prompt as we do the dips."** Made the harvest instruction a single canonical paste-block in the file, and wired it into *both* the research subagent (machine step 1) *and* the dip subagent (step 5) — not just arc research. Subagents don't load CLAUDE.md, so push is the only reliable channel.

3. **"Why consequence?"** I'd called the opportunistic-extraction reframe ("Pass 0.5 — capture follows traffic, not a calendar") a *consequence*. It isn't — nothing makes it happen on its own. It's an **affordance**: it only becomes Pass 0.5 *if* the snippet keeps getting pasted *and* harvest passes get run. Conceded; reframed in the worklog.

**"Interesting, they're starting to sound like entities."** Matt noticed the `kind` buckets converge on the graph taxonomy. They do — 7 of 9 (`food`/`place`/`object` = proto-nodes; `hospitality`/`relationship`/`foreshadowing` = proto-edges) *are* the taxonomy viewed coarsely. The two that aren't — `quote` (evidence) and `appearance` (a character attribute) — are the ones that *attach to* an existing node rather than mint one. The queue is really a **typed capture stream**: each row is a proto-node, proto-edge, attribute, or evidence, already tagged with where it'll land. The discipline that keeps it honest: `kind` must be a deliberate *projection* of `architecture.md`'s types, not a freelance vocabulary that drifts into a shadow taxonomy (the project's recurring schema-mixing hazard).

**"How does a working markdown affect sessions moving forward?"** Honestly: the file itself doesn't — it's inert (a destination + a copy-source). What carries the behavior across sessions, in descending reliability: (1) **memory** `feedback_harvest_queue`, loaded every session, reminds the orchestrator the queue exists and to push the snippet; (2) the **live continue prompt** wires it into the arc machine; (3) **push** — subagents only harvest if the orchestrator pastes the snippet into their prompt. The weak link is the first hop: it depends on the orchestrator *remembering*. Memory is a nudge, not a guarantee. Hardening options if that proves unreliable: promote to CLAUDE.md (loaded every session) or a settings.json hook (mechanical injection).

**Decision (Matt): smoke-test the buckets over the next ~2 dips; keep the push memory-only for now.** Don't promote to CLAUDE.md/hook or re-cut buckets until real rows show which buckets hold — promoting before the enum stabilizes would bake in churn. Review gate written into both the file and the memory.

---

## What's next
- The causal-arc track continues with **refinements only** (B3 closed the richest gap): #1 Q7 `robb-weds-jeyne-westerling` upstream (why Robb married Jeyne — extends B1); #2 Q3 Trident inbound CAUSES; #3 execution downstream (low). All dip-gated — re-dip to confirm demand before building. Live prompt: `progress/continue-prompts/2026-06-18-causal-arc-execution.md`.
- **Harvest-queue smoke test** runs passively as those dips happen; review buckets + the push-hardening question after ~2 dips' rows.
