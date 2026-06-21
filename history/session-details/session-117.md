# Session 117 — AFFC #4 Dorne/Myrcella + the `WITNESS_IN` design + citation tooling (2026-06-20 → 2026-06-21)

**Model:** Opus 4.8 orchestrator + 6 Sonnet 4.6 `general-purpose` subagents (1 Dorne research + 1 Dorne edge-verify + 1 ATTENDS re-audit + 3 Q2 edge-vs-node lenses).
**Commit:** this endsession commit. **Nature:** one execution arc (Dorne) followed by a long design conversation (WITNESS_IN, citation provenance, convergence maps, two process rules).

---

## Part 1 — AFFC #4 Dorne / Myrcella (the Queenmaker arc)

The last of the four AFFC smoke-test fumbles. With it, the **AFFC spine phase is complete** (S114 Cersei, S115 Brienne→Stoneheart, S116 Kingsmoot→Euron, S117 Dorne).

**Research found the landscape was richer than the handoff assumed.** Three Queenmaker beats already existed as bare Plate-3 nodes (`arrest-of-the-sand-snakes`, `areo-hotah-springs-the-ambush`, `arianne-collapses-and-is-captured`) — all with role edges but **zero causal edges**, no spaced aliases, and stale "do-NOT-promote" staging boilerplate. Genuinely missing: the Queenmaker plot itself and Myrcella's maiming. So the build was **2 mints + 3 repairs**, not 2 fresh mints.

**The key interpretive call — two threads, not one.** The research subagent established (and the verifier confirmed) that the arc has two threads meeting at Arianne:
- **Rooted thread:** `gregor-confesses-and-kills-oberyn CAUSES arrest-of-the-sand-snakes` — Oberyn's death → Dornish war-fever → Doran jails the Sand Snakes to defuse it. This is a cross-book auto-join; `--causal-chain` walks 5 hops back to Sansa's hairnet.
- **Prime-mover thread:** `the-queenmaker-plot` has 0 causal upstream **by design** — its prime mover is Arianne's birthright-fear (the half-read disinheritance letter, an actor-internal motive, no event node). The verifier explicitly argued *against* adding `arrest CAUSES plot`: the letter predates the arrest by years, so an `arrest CAUSES plot` edge would collapse two timelines the text keeps apart and overstate a secondary motive as a generative cause.

Result: 2 nodes + 11 edges (5 causal/agency Tier-2 fresh-verified + 6 role Tier-1). `conquest-of-dorne` (Daeron I, AC 161) avoided as the era-trap. Arys Oakheart's death folded into the existing ambush node (he's already VICTIM_IN there) rather than minted separately, keeping to the 1–2 mint scope.

---

## Part 2 — the `WITNESS_IN` edge type (the design conversation)

Sparked by a dropped edge: during the Dorne build I considered `arianne-martell WITNESS_IN myrcella-is-maimed-by-darkstar` but dropped it because `WITNESS_IN` had 0 live uses and minting vocab needs a decision. Matt pushed: "kind of makes sense — are there equivalents?"

**The equivalent was `ATTENDS`** — its definition literally bundled "guest, **witness**, or audience," and the `event.execution` node schema already lists "witnesses" as a role field. So the model *anticipated* witnessing but had no clean edge for it. Matt's framing nailed the boundary: you **attend** a tourney (the whole event) but **witness** a specific bout within it (Loras vs Gregor). Same person, different targets.

### The Arya/Sansa text-anchor catch (the proof-of-concept)
Matt floated `arya-witnesses-ned-execution` as an example. I flagged a memory that Yoren shields Arya, then **verified against the text** rather than asserting: `sed -n '161,183p' agot-arya-05.md` showed Yoren grabbing Arya, snarling "Don't look!", forcing her eyes shut — she hears "a soft sighing sound" but never sees the blow. It's **Sansa** who "could not turn her head" (`agot-sansa-06:15`). So the obvious example is canonically *inverted*. This became the worked example baked into the type's **text-anchor gate**: emit only when prose shows the character actually SAW it; present-but-shielded fails.

This also drove a meta-conversation about provenance: memory gives the *lead* (where to look, what to suspect); the file gives the *truth*. A subtly-wrong memory that sounds canonical is more dangerous than an obvious gap — which is exactly why every edge carries a checkable `file:line`.

### Q1 — ATTENDS re-audit (run B, subagent)
A subagent re-classified all 42 `ATTENDS` edges against the new boundary. Net: **1 flip** (`hoster-tully → battle-of-the-camps` — he "watched from the battlements"). The other 41 stay. Key finding: **no tourney-bout targets exist yet** — every tourney edge points at the whole-tourney node, so the Loras-vs-Gregor case is a *future capture* (mint the bout node, then WITNESS_IN), not a reclassification. Side findings routed to follow-up: 2 mistargeted edges (cersei→a character; ghost-of-high-heart→a place), 5 siege-of-Riverrun edges that are really GARRISONS/HELD_AT, and a candidate `tragedy-of-summerhall` node.

### Q2 — edge vs node (3-lens panel, UNANIMOUS)
Three independent advisors (traversal pragmatist / narrative salience / schema consistency) converged on the same rule from different angles:

> `WITNESS_IN` is the observer/perceiver slot on an event hub → **default EDGE**. Reify the witnessing as its own NODE only when the *act of seeing* owns an outgoing causal edge (it CAUSES/TRIGGERS/MOTIVATES a downstream event — the `bran-witnesses-jaime-and-cersei` case) or the witnessed thing has no node. Mechanical test: *does the seeing need an outgoing edge? yes→node, no→edge.* Promotion path: start as edge, promote later if a causal edge gets drawn.

Test cases agreed: Bran = NODE (his seeing causes the fall); Sansa/Ned, Arianne/maiming, feast-lord = EDGE. The schema lens added the doc fix: the "four participant slots cover everything" note was stale — `WITNESS_IN` is a **fifth, perceiver** (epistemic) slot. Three edges minted: sansa→Ned-execution, arianne→maiming, hoster→battle-of-the-camps. `witness` added as a harvest kind.

---

## Part 3 — tooling + process rules

- **Citation checker** (`scripts/verify-edge-quotes.py`): the systematic answer to "can't review every edge." Python-first (normalizes smart/straight quotes + ellipsis, fragments on `...`), checks each edge's `evidence_quote` appears at its `evidence_ref` line, flags reconstructed-not-read quotes. Ran on this session's edges: 16/16 OK. Scoped to verbatim-claiming runs (Plate-3 summary "quotes" + wiki-infobox would false-positive). A fuzzy-adjudication subagent is only needed for the rows it flags.

- **Two process rules pinned** (Matt's pushback on vague deferral + the hairnet super-attractor):
  1. **Enrichment-trigger gate** — "spine-first" is now a concrete condition ("Essos container spine-built AND WO5K junctures #3/#4/#5 built"), not open-ended "later" (`working/arc-enrichment-backlog.md`).
  2. **LOCAL-root, not deepest-ancestor** — report an arc's local root (Dorne → Oberyn's death), not "walks N hops to the hairnet." The hairnet (`sansa-receives-the-poisoned-hairnet`, 14 downstream) is a genuine super-attractor; its centrality is *earned* (GRRM built the Purple Wedding to decapitate House Lannister), but over-rooting (grafting every arc onto the deepest trunk to satisfy the root-check) is the failure mode to guard against (continue-prompt root-check policy).

- **Convergence-map charter** (`graph/convergence-maps/README.md`): captures Matt's overlapping-chains insight (divergence / convergence / offset shapes; the hairnet as a divergence hub) + a tooling sketch (`--braid` / `--fork-hubs` / `--join-hubs`). The dir was empty; now it has its charter. Deferred to the enrichment phase (needs a denser causal layer to map).

---

## Totals
Nodes 8,560 → **8,562** (+2 Dorne beats). Edges 22,329 → **22,342** (+11 Dorne arc + 2 WITNESS_IN adds + 1 ATTENDS→WITNESS_IN flip). Vocab 168 → **169** (+`WITNESS_IN`); edge types in use 130 → **131**. Orphans 62 (0 new). Harvest queue: 0 → **26 open** (19 Dorne research + 3 happenstance from grep output + 4 ATTENDS-reaudit). 0 lingering pending-verify. New scripts: `mint_dorne_myrcella_arc.py`, `mint_witness_edges.py`, `verify-edge-quotes.py`.

## What's next
Maintenance pass (ATTENDS cleanup + harvest consume of 26 rows) bundled as one session, THEN the Essos container decomposition. See `progress/continue-prompts/2026-06-21-graph-hygiene-and-harvest.md`.
