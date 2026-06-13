---
session: 93
date: 2026-06-12
model: Opus 4.7
title: Deferred structural restructures + infobox-merge dry-run sign-off + v2.1 citation backfill carve-out
parent_worklog_entry: worklog.md Session 93
execution_writeup: working/session-results/2026-06-12-deferred-restructures.md
---

# Session 93 — Deferred structural restructures + infobox-merge sign-off

> This is the human-narrative version. For technical execution detail (file paths, edge JSON, verification commands), read `working/session-results/2026-06-12-deferred-restructures.md`.

## Context entering the session

Matt opened a fresh window after S92 (Fable audit closeout) and dropped four handoff blocks: the infobox merge ship (gated on his decisions), graph cleanup (gated on the merge), Mode 3 grounded-agent dip (gated on the merge), and the parallel-safe deferred-structural-restructures track. He picked the parallel-safe one with the instruction "Start with the first one, use applicable subagents but verify their work."

The deferred restructures had been queued at the end of S91 because they were bigger than a slug-swap: each required minting a new parent event, reassigning role-edges from two sibling stubs, and resolving type-field ambiguity. The S91 subagent decision packets were reproduced verbatim in the continue prompt, with five open questions for Matt's ratification.

## How the session actually unfolded

### The open questions surfaced real schema decisions

I posed four AskUserQuestion items covering the substantive choices: substitute-criminal node vs fold into parent, Cersei small-council third sub-beat, the `SECRETLY_ALLIED_WITH` vocab gap, and Jaime merge vs SUB_BEAT_OF. Matt dismissed all four with "do not proceed, wait for next instruction" — which I read as a hard pause.

When he came back he said: "research the answers to the above these online - and event.description make sense? also event.conspiracy make sense. conspires with is good."

I read "event.description" as a typo for `event.deception` — the open type question I'd flagged but not asked. The "conspires with is good" line confirmed `CONSPIRES_WITH` as the Wyman-Stannis alliance edge (since `SECRETLY_ALLIED_WITH` isn't in vocab and `CONSPIRES_WITH` is the exact-fit symmetric-secret-pact type from S58).

### Wiki research changed the Wyman arc shape

I hit the local wiki cache (per the hard rule — no external fetches) and read `Wyman_Manderly.json`. The canonical arc has **four** beats, not the 2-3 the subagent packet proposed:

1. Public arrest (existed)
2. Public execution order (existed under `lord-wyman-orders-execution`)
3. **Substitute criminal beheaded; head/hands tarred by Ser Bartimus, mounted above Seal Gate with onion** (missing)
4. **Frey witnesses attest at Cersei's small council; Iron Throne returns Wylis from Maidenpool** (missing)

Wyman's own line — *"the mummer's farce is almost done. My son is home."* — names the whole operation as a discrete deception, not just an arrest+order arc. The Wylis-return is the *payoff*, which I modeled as a consequence of beat 4 rather than a fifth sub-beat (it's an outcome, not a deception act).

### `event.deception` vs `event.conspiracy` — the real type question

The subagent's original framing called it `event.deception` "or whatever Matt prefers — flag if new type." I checked architecture.md and confirmed `event.deception` doesn't exist; `event.conspiracy` does (line 117, defined as ongoing covert *scheme*).

My read: the two are genuinely distinct.
- `event.conspiracy` examples (Grand Northern Conspiracy, Queenmaker plot, Faith Militant uprising) are months-to-years-long political schemes
- The Wyman staged execution is a discrete *act-of-deceiving* — single staged moment, propagates false belief to a specific audience (Cersei's small council), has a payoff (Wylis returned)
- They nest: Wyman's farce sits INSIDE the Grand Northern Conspiracy; using the same type for both would flatten that hierarchy

I researched whether adding the type was cheap or drift-prone:
- TYPE_DIR_MAP only lists 3 event subtypes but the `events/` dir actually carries 8+ (descriptive, not enforced)
- No global event-subtype validator exists
- Drift-detection rule applies to *edge* types in bulk LLM runs — N/A for hand-minted entity types
- 2 lines of documentation (architecture.md entity table + schema-legend.md observed list)

When I surfaced this to Matt with the recurring-instances list (Wyman, Cersei's false-attack claim, Theon's burned boys, Sansa→Alayne, Jeyne-as-Arya), he gave the green light along with both beats 3 and 4. The architecture.md row I added lists those 4 canonical seed examples — future passes can promote the other 3 deliberately.

### Jaime: collapsed instead of parent+children

The subagent recommended minting `attack-on-ned-stark-in-the-streets-of-kings-landing` as a parent and SUB_BEAT_OF-ing both existing children (the `ambushes` stub and the `sheathes` stub). I went the other direction.

Reading the AWOIAF Eddard Stark page (the canonical source for this scene) revealed there's **no discrete event page** for the brawl. The wiki frames it as a "melee" inside Ned's biography — eight men die, four named. If even the wiki treats it as one moment, splitting it into parent + child + sub-beat for graph purposes is over-modeling.

The cleaner move: rename the survivor stub (`jaime-lannister-ambushes-ned-s-party`, which had 7 role edges vs sheathes' 5) directly to the canonical name `attack-on-ned-stark-in-the-streets-of-kings-landing`, change its type from `event.incident` to `event.battle` (the right type per architecture.md:108), absorb the sibling's content into the body, preserve both old slugs + old names as aliases, dedupe overlap edges, repoint the one unique COMMANDS_IN edge. Delete the sibling node file.

This contrasts with Wyman intentionally. Wyman has 4 narratively-distinct beats with different participants and different audiences; Jaime is one ~30-second melee. The right structure follows the source, not a template.

### The Q11 reframing

After the restructures landed I walked Matt through the 11 dry-run decisions on the infobox merge report, 3 at a time. He accepted all defaults through Q1–10, but on Q11 he stopped: *"why null explicit - should we look for the part of the book in case we need dialog / food description etc."*

This was a genuinely good push. My initial framing of Q11 leaned too hard on "false precision — wiki pages cite 70 chapters, you can't say which one." That's true for the *page level*, but it ducked the question of *per-fact* citations encoded inside infobox values (`Spouse: Joanna[12]`-style anchors).

I reframed:
- Q11's actual default is "page-level null because we can't pretend"
- Q11's override is a tiny win for pages citing exactly one chapter
- **Neither does what Matt's instinct was reaching for**
- What he was actually asking about is a per-fact citation backfill — a separate deterministic pass that harvests `[N]` anchors from infobox values, resolves each to a cite_ref → chapter slug, and patches `evidence_chapter` in place

The food/dialog caveat: those aren't infobox-shaped at all. They live in prose and are already captured by Pass 1 extractions with their own `evidence_chapter` + verbatim quotes. The infobox merge can't surface them regardless of Q11.

Matt picked "ship null now + queue v2.1 per-fact citation backfill." I added the TODO under Track 4 of `working/todos.md` (gated on the merge shipping) and updated the Q11 annotation in the report to make the explicit-deferral context clear rather than reading as a flat null-forever.

### "Can I use Opus instead of Sonnet for the merge?"

End-of-session question. The handoff prompt recommends Sonnet 4.6 (deterministic apply, judgment pre-baked). I gave the honest answer: Sonnet is the cost-efficiency call, not a capability requirement. Opus runs the same scripts identically and has insurance value if the dry-run reproduction gate halts (it debugs unexpected drift better). Given Matt's "lots of usage to burn today" framing, Opus is a defensible pick — the model-fit rule is waste-reduction, and he's explicitly opting out today.

## Why this session warranted a detail file

Three reasons:

1. **The wiki-research methodology was load-bearing.** Both arc decisions (Wyman 4 beats not 2; Jaime collapse not parent+child) came from reading canonical pages and letting the source structure guide the model. Worth documenting for future restructure passes — the pattern is "let AWOIAF tell you the shape before you template it."

2. **The `event.deception` vocab call.** This adds the type formally. Future sessions need to know it exists, where the seed examples are, and why it's distinct from `event.conspiracy`. The arch.md row captures the *what*; this captures the *why*.

3. **The Q11 reframing.** A user pushback that improved the project — the v2.1 TODO is a real artifact that wouldn't exist without it. Worth recording the path from "default null is fine" → "you're right, here's a separate pass for the thing you're actually asking about" so future sessions can apply the same lens to other "defaults stand if unmarked" reports.

## What stayed in the writeup (`working/session-results/2026-06-12-deferred-restructures.md`)

The technical execution: every file touched, every edge minted with its JSON shape, the rename-script dry-run outputs, verification commands and their outputs, count tables, the hard-rule audit. If you want to know what code ran, read that. If you want to know why we chose what we chose, read this file.
