# DEFERRED — Harvest texture-sweep + grep post-pass (design parked)

> **Status: DEFERRED by Matt (2026-06-23, during S135).** Do NOT build yet. **Resurface trigger:**
> *after the first round of major-arc enrichment dips* — i.e. at the **dedicated planning session**
> that sits between the arc phase and the granular phase (Matt S130; see
> `working/arc-enrichment-backlog.md` sequence line). Matt: "defer it, I don't want to lose it, make
> sure it comes up after the first round of enrichments."
>
> This file is the full design so it isn't lost. When the trigger fires, read this and spec the build.

## Why this exists
Matt wants **a LOT of harvest rows** — the capture bar should be LOW (food/meal descriptions incl.
mundane/grim ones like gruel, physical descriptions, hospitality, load-bearing quotes, foreshadowing).
A 3-advisor board (S135) was run on "how to maximize harvest capture." See the worklog S135 entry +
chat for the full board output.

## What was DECIDED (converged in chat, S135) — the shape to build later
1. **Split the bar (Tier 1, board-unanimous, NOT deferred — see below):** in the enrichment dip lens
   prompts, keep a TIGHT threshold for minted edges but a WIDE-OPEN one for the harvest section
   ("capture every food/description/quote; pre-dedup is NOT your job"). Nearly free; landed/loaded
   separately, not part of this deferred build.
2. **Primary sweep = SONNET, full-chapter read, run BROADLY (this is the deferred build):**
   - **Cost is NOT a constraint** (Matt: "for this, sonnet cost is negligible"). So the board's
     Haiku-for-cost recommendation is OVERRIDDEN — use **Sonnet**, because with cost off the table the
     only things left to optimize are **quality + recall**, and Sonnet beats Haiku on both (better
     judgment on "is this notable/funny/load-bearing," and a model reading the prose has far better
     recall than a keyword grep — a grep silently misses "honeyed locusts").
   - **Run broadly, NOT gated to feast/set-piece chapters.** The mundane meals Matt likes (gruel on the
     road) live in the "thin" travel chapters, not the weddings — cost was the only reason to gate, and
     it's gone.
3. **The Python grep = a POST-pass, never a pre-filter (Matt's call).** A pre-filter caps recall (the
   model only sees what grep matched → a missed dish is lost). A post-pass only ADDS. Two roles, same script:
   - **Role A — post-sweep auditor / recall backstop:** after Sonnet sweeps a chapter, grep its
     food/appearance/hospitality lexicon, diff against the harvest rows the sweep produced for that
     chapter, surface any lexicon line with no nearby row ("grep found these N food lines you didn't
     capture — review"). The grep's lexicon ceiling stops mattering — it's a net under the model, not a gate.
   - **Role B — standalone seeder ("harvest enrichment for lack of better work"):** on chapters NO dip
     will touch, run grep alone and dump lexicon-matched lines as candidate rows. Ideal **unsupervised
     background/idle job** — deterministic, additive; the noise is filtered LAZILY at attach time (when
     the target node is re-opened anyway), so no model is paid to filter up front.
4. **Sustainability guardrails (Advisor C, model-independent — apply whenever volume rises):**
   - **`dedup_key` column** on harvest rows (e.g. `robb-is-killed:quote:asos-catelyn-07:135`) — a
     1-second grep-check at capture to block *pointer* dupes (NOT content pre-dedup, which stays
     forbidden). Dupe inflation is the #1 risk of high volume (already visible: same Stoneheart quote
     flagged twice; re-queued Essos rows).
   - **Attach-pass cadence** every ~30-40 open rows so the open backlog never exceeds one session's
     attach work. (Current trigger ~20-30 has held.)

## Mechanics (carry over unchanged from the chat design)
- Lexicons: **food/meal** wordlist *seeded from the actual dish names in `graph/nodes/.../foods/` (object.food)*
  + greedy generic terms (feast/supper/bread/wine/ale/gruel/pie/roast/stew/honey…); **appearance** triggers
  (his/her eyes, his/her hair, wore, clad in, beard, scar); **hospitality** (bread and salt, guest right).
- Emit candidate rows `chapter · line · text · guessed-kind` to a STAGING file
  `working/harvest-candidates.jsonl` — **never** write the live `harvest-queue.md` directly.
- Make the lexicon **greedy** (over-match, filter later) rather than precise — recall > precision here.

## Source threads
- Board run + synthesis: worklog `### Session 135` + the S135 chat.
- Memory: `user_asoiaf_design_values` (food bar is LOW, gruel counts), `feedback_harvest_queue`,
  `feedback_capture_quotes_during_research`, `feedback_python_before_agent`,
  `feedback_model_selection_at_session_start` (note: cost-override above supersedes default model-fit here).
