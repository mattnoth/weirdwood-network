---
session: 116
date: 2026-06-20
title: "Kingsmoot → Euron — spine, the first enrichment pass, and three new process mechanisms"
model: Sonnet 4.6 orchestrator + 8 Sonnet 4.6 general-purpose subagents
type: design + execution
---

# Session 116 — Kingsmoot → Euron, and the birth of the enrichment track

## What this session was

It started as a routine arc build (AFFC smoke-test fumble #2, the Kingsmoot → Euron
succession arc) and turned into the session where three durable process mechanisms
were invented under Matt's questioning: **arc enrichment**, the **`SUSPECTED_OF`**
edge type, and the **`parked` harvest status**. The graph grew +7 nodes / +28 edges,
but the lasting output is the method.

## Part 1 — the spine (routine, but two traps)

Standalone arc, prime mover = Balon's death. Spine:
`death-of-balon-greyjoy TRIGGERS euron-seizes-the-seastone-chair CAUSES
kingsmoot-on-old-wyk CAUSES taking-of-the-shields`, plus `euron-seizes MOTIVATES
aeron-greyjoy`. 2 new nodes + `kingsmoot-on-old-wyk` repaired (event.battle →
event.ceremony, the near-bare Path-B wiki node got spaced aliases + a real Identity
+ 4 participant role edges). 11 edges, all fresh-verified.

Two traps, both of the AFFC same-name-different-era class:
- **`anarchy-in-the-reach`** — the handoff named it as the Euron-Reach-invasion
  downstream, but it's the **historical Gardener-era Reach succession war**. Redirected
  to the real node `taking-of-the-shields`.
- The murder framing of Balon's death (see Part 3).

Root-check: 0 upstream on `death-of-balon-greyjoy`, **declared intentional** (genuine
standalone — Balon's death is the prime mover, the machine-5b exception).

## Part 2 — the enrichment pass (the new mechanism)

Matt greenlit a smoke test of a second-pass idea: once a spine is built, fan out fresh
subagents to find the **braided side-plots that occur within the arc but aren't on the
spine**. Three lenses (Asha/Aeron sub-arcs · Victarion-thread+revelation · descriptive
depth) over the *already-harvested* cluster yielded, with almost no overlap with the
first harvest: +2 beat-nodes (`asha-claims-the-kingsmoot` — her "queensmoot" third-way
stand; `aeron-vows-to-raise-the-ironborn-smallfolk` — the Damphair's resistance, the
*Forsaken* seed), +6 edges, +12 descriptive cite-upgrades (Grey King's Hall furnishings,
Nagga's Hill dawn, Silence's figurehead → navigable book cites).

**Cadence decided (Matt):** spine-first — build the *majority* of major-arc spines, THEN
circle back for enrichment. Reason, proven by the session's own deferrals: enrichment
wires *between* arcs, so more spines = more attach points; the harvest queue preserves
finds during deferral; **multi-pass per cluster is expected** (this was the *first*
Kingsmoot enrichment pass, not the last). Today's pass was a deliberate smoke-test
exception. Logged: `working/arc-enrichment-backlog.md` + memory `project_arc_enrichment_track`.

## Part 3 — `SUSPECTED_OF`, born from the Balon question

Matt asked whether Euron's assassination of Balon is *proven* and whether the node should
be `assassination-of-balon-greyjoy`. The honest answer: the 5 published books leave it
**speculation** (AWOIAF: "lead to speculation that Balon may have been murdered by an
assassin at Euron's command"). Euron's actual confession is in the TWOW preview "The
Forsaken" — which we hold only as a **wiki summary**, not primary text. So: keep
`death-of-balon-greyjoy` as `event.death` (renaming to `assassination` would launder a
theory into canon), but model the suspicion at its own tier.

That required a **new edge type**: `SUSPECTED_OF` (actor → event, capped Tier-2, never
asserts the act as fact). First instance `euron-greyjoy SUSPECTED_OF
death-of-balon-greyjoy`, evidenced by Asha's in-saga accusation + Euron's hollow
mute-crew alibi. Added to architecture.md (vocab 167→168). It's a reusable primitive —
Jon Arryn, Joffrey's parentage, the Purple Wedding poisoner all want it.

**On The Forsaken / Tier:** a GRRM preview chapter is primary text (Tier-1-strength) but
**provisional** (preview material has changed before) — so it'd carry its own
`twow-preview` provenance, not plain Tier-1. And we don't have it; ingesting it would be
a deliberate new-source add (outside the no-wiki-refetch rule, since it's published, not
a wiki page). Matt deferred that decision.

## Part 4 — "don't defer what you can build now" (the capture-now rule)

Matt pushed back twice on deferring: first on the forward-dangling bridge nodes
(Asha-marriage, Victarion-mission), then on "logging for later" the Aeron-murder line.
The principle that crystallized: **a node is only worth deferring if its UPSTREAM is
missing (truly forward-dangling) or its SOURCE isn't in the corpus. If you have the
verbatim quote and a valid home now, build it now** — and per S112's cross-book
auto-join, pre-placing terminal nodes lets the future arc find them already wired.

So three "deferred" nodes were minted in place instead:
- `euron-weds-asha-to-erik-ironmaker-in-absentia` (ADWD Wayward Bride is in our cache —
  real book cites; `kingsmoot CAUSES`).
- `euron-commissions-victarion-to-fetch-daenerys` (the Essos-bridge seed;
  `taking-of-the-shields CAUSES`, fresh-verify retargeted from the kingsmoot).
- `euron-hunts-aeron-damphair` — captures the *real* ADWD hunt; Tris Botley's "the Crow's
  Eye slit his throat" is recorded as an in-world **rumor quote**, NOT a `SUSPECTED_OF
  death` edge, because Aeron's death is **unconfirmed** (he's alive in TWOW). The verifier
  endorsed the don't-assert-death call.

Only two things stayed genuinely deferred: Aeron's TWOW *capture* (source not in corpus)
and the Forsaken primary text.

## Part 5 — the `parked` harvest status (the home for blocked notes)

Matt: "we need a home for these kinds of notes" — finds that are real but can't be
consumed yet. Added a third harvest status: **`parked`** (vs `open`/`done`) — blocked &
NOT consumable, **excluded from the 20–30 trigger count**, with the blocker reason
recorded, auto-promoted back to `open` when the arc/node lands. Two blocker kinds:
arc-blocked (home is a future arc's node) and node/cite-blocked. Retagged the 9 blocked
rows (4 Essos-gated + 4 no-home + 1 wrong-cite) → parked; the queue now reads **0 open /
9 parked**, so it won't false-trigger a harvest pass on rows nothing can act on.

## Verification discipline

10 interpretive edges minted across spine + enrichment + 3 bridge nodes; **all 10
fresh-subagent CONFIRMED**, 0 lingering pending. Two verifier adjudications applied:
`kingsmoot CAUSES aeron-vows` → retyped TRIGGERS; the Victarion-commission upstream moved
kingsmoot → `taking-of-the-shields`. 8 subagents total this session (1 research + 3
enrichment lenses + 3 verify + 1 descriptive-attach).

## Totals

Nodes 8,553 → 8,560 (+7). Edges 22,301 → 22,329 (+28). Edge types 129 → 130
(`SUSPECTED_OF`). 0 new orphans. `--causal-chain death-of-balon-greyjoy` = 0 upstream +
8 downstream. Mint scripts: `mint_kingsmoot_euron_arc.py`,
`mint_kingsmoot_euron_enrichment.py`, `mint_kingsmoot_bridge_nodes.py`,
`mint_euron_hunts_aeron.py`.

## What's next

AFFC #4 Dorne / Myrcella (last AFFC smoke-test fumble) — then Essos becomes the next big
container, at which point the parked Essos rows + the deferred bridge work all come due
together. The enrichment track interleaves spine-first.
