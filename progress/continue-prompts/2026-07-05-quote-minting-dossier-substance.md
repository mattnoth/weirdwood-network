# SESSION 193 — Quote minting + dossier substance (Matt-picked, Fable)

> **This is Session 193.** Stamp your worklog entry `### Session 193` at endsession.
> (If another graph/meta session lands first, renumber — check `worklog.md`.)
> Matt-picked S192 over granular dips / front-end-on-Fable: fill the nodes the chat
> actually surfaces BEFORE the receipts/node-UX session makes every node clickable.
> **The front-end track (`2026-07-05-chat-ui-receipts-and-node-ux.md`) runs AFTER
> this session** — the two compound: this fills the dossiers, that makes them reachable.

**Recommended model: Fable, solo or with at most 2–3 cheap verify agents** — the
monthly spend ceiling bit in S191; quote selection is reasoning-heavy (which passage is
load-bearing is a judgment call), verbatim capture + cite verification need care, not
bulk. Python-before-agent rule applies hard (see step 0).

**Track:** graph. **State you inherit:** class-5 dup-slugs applied + hardened +
deployed (S192); query-layer complete (S189–S191); live chat serves search/list/theme.
Read `worklog.md` S191/S192 + STATUS first; trust worklog over this prompt.

## Why (the gap, from the S188 census)

Quote coverage is lopsided: ~73% of character nodes carry curated quotes but ~3% of
descriptive nodes; the descriptive layer (foods/materials/customs) is >90%
edge-islanded. The new `theme`/`list_nodes` tools route visitors straight at those
nodes — the meals question now finds food nodes whose dossiers say "No curated book
quotes on this node yet" over an empty neighbors panel. This is the book-citation
overlay work Matt has called "huge": navigable `chapter:line` cites upgrade wiki
Tier-2 provenance to openable Tier-1 book provenance.

## The work

0. **Deterministic census FIRST (Python, no agents):** which nodes lack `## Quotes`,
   ranked by (a) graph degree, (b) POV characters, (c) theme-index membership (the
   nodes the chat's theme tool exposes), (d) marquee event hubs. Output a ranked
   worklist file under `working/`. Pick the session's slice from the top — this is a
   dip, not a corpus pass; leave a re-runnable worklist for future slices.
1. **Quote minting on the slice:** read the cited chapters (`sources/chapters/`; wiki
   cache for pointers — never fetch), attach load-bearing verbatim quotes to node
   `## Quotes` with navigable `chapter:line` cites (the `bookQuote()` renderer + cite
   gate consume these — match the existing quote+attribution format the build parser
   expects, see `parse_quotes` in `graph/query/weirwood_query/load.py`).
2. **Capture-quotes + harvest rules apply** (paste into any subagent prompt): any
   load-bearing quote found in passing gets attached before moving on; notable
   non-task finds go to `working/harvest-queue.md` as one-line pointers.
3. **Edge wiring: only what quote work naturally surfaces, only existing vocabulary.**
   `SERVED_AT` does NOT exist and stays triple-gated (8d rider — Q21 evidence still
   accumulating); do not mint new edge types. Islanded descriptive nodes get edges
   only where an existing type genuinely fits the evidence.
4. **Close-out:** `weirwood refresh` (quotes feed the SEARCH INDEX — rebuild is not
   optional) + bundle rebuild; prod deploy per `DEPLOY.md` is **Matt-gated**. Fresh
   cite-verify on a sample of minted quotes (the cite gate will hard-reject drifted
   cites at chat time — verify `chapter:line` really holds the text).

## Hard gates

Quote attachment IS graph mutation — Matt launched this track for that purpose, but
anything beyond additive `## Quotes`/prose edits (new nodes, edge retirement, renames)
needs his explicit in-session go. No prod deploy without his go. `sources/` read-only;
never fetch the wiki; don't touch `scr`; never auto-run /endsession. Vocabulary:
**Pass** / **Track** / lowercase **step** / **Tier** = confidence 1–5 only.
