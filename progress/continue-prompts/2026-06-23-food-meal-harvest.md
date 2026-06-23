# SESSION 138 — Food/meal harvest pass (maximal, full-corpus)
> **This is Session 138.** Stamp your worklog entry `### Session 138` at endsession (in `worklog.md` — graph track).
> **Recommended model:** Sonnet 4.6 sweep/verify subagents + Opus 4.8 orchestrator. Cost is NOT a constraint (Matt) — go broad.
> **D&E Pass-1 is PARKED** (Matt). You are NOT running two tracks. Stage only your own files by explicit path; never `git add -A`.

## What this is
A dedicated **maximal food/meal harvest** — the first run of the (now-LIVE, no longer "parked") **harvest texture-sweep**. This is NOT an arc-enrichment dip. The whole job is to capture **every eating/drinking/meal moment in the corpus** and make it queryable.

**Matt's goal (verbatim, S137):** *"I want all meals. Maximal … I want to be able to just ask and get full on meal descriptions."* And (S137): *"make sure like, eating bark or whatever, any time anyone eats, so we capture the disgusting meals like when peasants have no food or whatever."*

→ **Scope = ANY ingestion event, the full register:** feast-grade (the PW 77 courses) → everyday fare → humble/poor → **grim/desperation (gruel, prison rations, bark, leather, grass, rats, horseflesh, boiled boots)** → **the ABSENCE of food (famine, peasants starving, sieges, "nothing to eat")**. Drink counts too (wine, ale, milk, water, dreamwine). **Over-capture is the goal — there is no "too minor."**

## How it already works (the schema supports this — don't reinvent it)
`object.food` nodes already exist as one of the 21 indexed node categories — **~75 today** (`graph/nodes/foods/`: bread, bowl-of-brown, lemon-cake, boar, pigeon, rat, locust, weirwood-paste, …). Each dish node accumulates **every occurrence** in a `## Narrative Arc` section (per-book: verbatim description + `chapter:line` cite + who's eating) plus a `## Quotes` section. Indexed at `graph/index/foods/`. So:
- *"show me all meals"* = the `foods/` category / `graph/index/foods/`.
- *"full descriptions of X"* = that dish node's `## Narrative Arc`.
**Template to copy: `graph/nodes/foods/bread.node.md`** (see its per-book Narrative Arc + Quotes pattern). MAXIMAL = mint a node PER dish/food-type; append every occurrence. Don't economize on node count.

## The method (Python-first, then broad Sonnet sweep, then grep audit)
1. **Inventory first (deterministic).** List the ~75 existing food slugs + aliases (so the sweep dedups against them, not re-mints). `ls graph/nodes/foods/` + read each frontmatter `name`/`aliases`.
2. **Broad full-corpus Sonnet sweep (the core).** Fan out Sonnet subagents over **all 344 chapter files** (`sources/chapters/{agot,acok,asos,affc,adwd}/`), in **resumable batches** (e.g. 10–20 chapters/subagent; keep a swept-chapters manifest so a re-run resumes). Each subagent reads its chapters and emits a structured row PER eating/food/drink/absence-of-food moment:
   `book | chapter:line | food-or-dish (or "NONE — famine/starvation") | register(feast|everyday|humble|grim|starvation|absence) | who's eating | VERBATIM description span (line-checked, incl. internal quote marks)`.
   Tell them: **the bar is WIDE OPEN** (bark, rats, gruel, empty bellies all count); VERBATIM contiguous spans only (the S135 quote-mark rule); cite exact `chapter:line`.
3. **Synthesize + attach (Opus).** Group occurrences by dish → append to the existing food node's Narrative Arc + Quotes, OR mint a new `object.food` node (copy the bread template; `pass_origin: s138-food-harvest`). For starvation/absence-of-food with no "dish," attach to a `famine`/`starvation` concept node (mint if absent) or to the relevant event/character node. **Line-check every cite against the file before writing.**
4. **Grep POST-pass auditor (NOT a pre-filter).** After the sweep, run a Python food-lexicon grep over all chapters (dish names + eat/feast/supper/hungry/starv*/bread/meat…) to surface occurrences the sweep MISSED → feed back as a second attach round. Log what it caught (no silent caps).
5. **Drain the queue too.** `working/harvest-queue.md` has **82 open rows** — do the **food/meal ones first** (flip to `done` as attached); the non-food rows (appearance/quote/object) can wait for a later texture sweep or be done opportunistically.
6. **Verify + refresh.** Fresh-verify a stratified sample of the attachments (a Sonnet that didn't sweep — confirm quote integrity + correct dish). Then `bash scripts/weirwood-refresh.sh` (new nodes → rebuild the foods index + alias resolver). Spot-check: `ls graph/nodes/foods/ | wc -l` grew; a query on a new dish node shows its Narrative Arc.

## Scale / batching (Matt: cost not a constraint)
344 chapters is a lot of subagent work — run it in **resumable waves** (checkpoint a swept-chapters manifest after each wave so a rate-limit wall or `/endsession` doesn't lose progress). **Recommended:** start with a **SMOKE wave** (~6–10 chapters spanning the registers — e.g. a feast chapter [asos-sansa-04 PW], a Flea-Bottom chapter [agot-arya-05], a Wall/starvation chapter [adwd Jon or the Fist], a siege chapter) to validate the sweep→dedup→attach→node-format loop and the node template, THEN scale to the full corpus. Don't one-shot 344 chapters blind.

## DO NOT
Refetch wiki / any HTTP (read local `sources/chapters/` only) · use the grep as a PRE-filter (it's a post-pass auditor — the Sonnet sweep is primary, grep only catches misses) · economize on food-node count (MAXIMAL — node per dish) · skip the grim/starvation/absence-of-food register (that's the whole point of Matt's S137 add) · paraphrase quotes (VERBATIM contiguous spans, internal quote marks included) · silently cap coverage (log dropped/deferred chapters) · run any book-extraction (`feedback_no_extraction_without_asking` — this is harvest/attach, not Pass-1 extraction, but confirm if unsure) · `/endsession` without permission · `git add -A`.

## Read first
- `graph/nodes/foods/bread.node.md` (the node template — Narrative Arc + Quotes pattern)
- `working/harvest-texture-sweep-deferred.md` (the design doc — update its status from "deferred" to LIVE as part of this session)
- `working/harvest-queue.md` (82 open rows; food ones are this session's)
- memory `user_asoiaf_design_values` (maximal-meals + just-ask-retrievability goal)

## Open questions for Matt
- Starvation / absence-of-food with no dish — attach to a `famine`/`starvation` concept node, or to the event/character? (Recommend: a `starvation` concept node accumulating occurrences, mirroring how dish nodes work — so "show me every time someone starves" is also one query.)
