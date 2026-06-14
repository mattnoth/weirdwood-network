# Narrative-Arc Reification — Design Memo
**Date:** 2026-06-13 (S95 follow-on, post-infobox-merge ship)
**Status:** Concept memo. First instance shipping with S95 cleanup; deliberate track sequences after Mode 3 dip findings.
**Memory:** `project_narrative_arc_reification`. **Worklog:** Ideas & Backlog HIGH.

---

## The insight in one paragraph

The graph has dense coverage at the dyad level (book-pass1 edges) and the event-hub level (S87 Plate 5 reification: 585 event hubs, role edges, SUB_BEAT_OF for in-event beats). It does NOT carry the causal architecture connecting event hubs to each other. GRRM's narrative IS that architecture — Trident incident → Lady's death + Mycah's death; Rains of Castamere (House Reyne) → Red Wedding scoring → Tyrion's later weaponization at Joffrey's wedding; Tower of Joy → R+L=J → Ned's lie → Jon at the Wall. A reader feels each chain. An agent querying the current graph sees isolated beats and has to LLM-reason the chain back together. Reifying arcs as parent event hubs (with SUB_BEAT_OF children + TRIGGERS/PRECEDES between sub-beats) makes those chains 1-hop or 2-hop traversals.

## What's new vs already-done

| Layer | Status | What it does |
|---|---|---|
| Dyads (book-pass1) | SHIPPED S66-74 | Direct relationships ("Sandor KILLS Mycah") |
| Event-hub reification (Plate 5) | SHIPPED S87 | One event with n-ary structure becomes a hub + role edges (Red Wedding) |
| **Narrative-arc reification** | **CONCEPT, 1 instance** | **Multiple event hubs grouped under a parent arc + causal edges between them** |
| Theory-informed extraction (Pass 5) | NOT STARTED | Different layer: theory-evidence-collection (Azor Ahai, Valonqar, etc.) |

The pattern is structurally the same as Plate 5; the novelty is applying it deliberately one level up to chains spanning multiple existing event hubs.

## Pattern (worked example: Trident incident, S95 Q5)

**Parent node:** `incident-at-the-trident` (`event.incident`)

**Sub-beats** (4 SUB_BEAT_OF children, all attaching to the parent):
- `cersei-maneuvers-for-lady-s-death` (existing standalone hub, retroactively linked)
- `ned-claims-the-execution` (existing standalone hub, retroactively linked)
- `ned-kills-lady` (existing standalone hub, retroactively linked)
- `death-of-mycah` (new hub minted with parent)

**Role edges** live at the BEAT level only (parent has zero direct role edges — all participants attach at sub-beats). This matches Red Wedding precedent.

**Causal directionality** within the arc:
- `cersei-maneuvers-for-lady-s-death TRIGGERS death-of-mycah` (Cersei's demand authorized Sandor's hunt)
- Future: `cersei-maneuvers-for-lady-s-death TRIGGERS ned-kills-lady` (same logic)
- Future: `joffrey-baratheon ATTACKS mycah` (existing dyad) → no causal edge needed; the dyad sits "inside" the parent's umbrella via co-mention

**Existing dyads stay untouched:** `sandor-clegane KILLS mycah` (Tier 1, AGOT Eddard III) is a sibling to the new `death-of-mycah` hub's role edges, per S87 convention.

## Sub-beat / parent vocabulary — what we ALREADY have vs what's new

Locked vocab already supports:
- `SUB_BEAT_OF` (added S86, vocab 165→166)
- `TRIGGERS` (locked, causal)
- `PRECEDES` / `FOLLOWS` (chronological, deferred Tier-3 work per `chronology-extractor` agent stub)
- Event types: `event.incident`, `event.battle`, `event.death`, `event.ceremony`, `event.feast`, `event.execution`, `event.conspiracy`, `event.deception` (S93)

**No new vocab needed for arc reification.** The pattern reuses what exists. Possible future addition (NOT for v1): an `event.arc` type as a syntactic flag for parent-of-parents, distinct from `event.incident` which is a leaf-level type. Defer until 5+ arcs are minted and a type pattern emerges.

## Candidate arc list — seeds for the dip-driven priority queue

Scale-tagged so the dip can pick a small win to validate the pattern before tackling epics. Order = rough priority by "how often this chain comes up in canon-question patterns," NOT a commitment.

### Small arcs (3-7 sub-beats; 1-2 hours research each)

| Arc | Anchor chapters | Existing graph state |
|---|---|---|
| **Trident incident** | AGOT Sansa I + Eddard III | ✅ SHIPPED S95 Q5 |
| **Battle of the Trident / Rhaegar-Robert duel** | AGOT Eddard I, X, XV (POV recall) | Battle node exists; no causal chain to Sack-of-KL parent |
| **Mycah-revenge thread** | AGOT Sansa I → ASOS Arya VIII (kill list mention) → AFFC/ADWD prayer | Dyads exist; no arc |
| **Sansa hairnet → Joffrey poisoning** | ASOS Sansa IV → Sansa V → Sansa VI → AFFC Cersei plot | Some edges; not arc-linked |
| **Catelyn frees Jaime → Robb deposes Catelyn → Jeyne-Robb marriage** | ASOS Catelyn I-V | Dyads; no causal arc |
| **Bran's fall → Cat hunts catspaw → Tyrion accused → trial at Eyrie** | AGOT Bran I-III, Catelyn V-VII, Tyrion VI | Rich dyad coverage; no parent |

### Medium arcs (10-25 sub-beats; ~4-8 hours each)

| Arc | Anchor span | Existing graph state |
|---|---|---|
| **Sack of King's Landing** (Mountain-kills-Elia/Aegon/Rhaenys + Jaime-kills-Aerys + Tywin's loyalty signal + Robert's overlooking) | AGOT recall, ASOS Jaime POV, fSWORD recall | Wiki nodes exist; ~0 causal edges in graph |
| **Tower of Joy → R+L=J reveal staged** | AGOT recall (Ned dream); ADWD Jon-on-Wall | All-dark zone (S89 probe 5: 0 edges) |
| **Robert's Rebellion (Harrenhal → Trident → Storm's End siege)** | TWOIAF + AGOT POV recall | Wiki structural; no graph chain |
| **Red Wedding origins** (Tywin's plan + Bolton-Frey alliance + Olyvar Frey spy + bread-and-salt violation) | ASOS Catelyn VI-VII + AFFC Jaime | Red Wedding ✅ reified S87; upstream causal chain missing |
| **Greyjoy Rebellion → Theon-as-hostage → ironborn invasion of north** | AGOT Bran + Tyrion; ACOK Theon | Theon-as-Stark-ward node exists; chain doesn't |
| **Purple Wedding** | ASOS Sansa I-VI + AFFC Cersei retroactive | F3 in FIX-22 already builds death-of-joffrey-baratheon + ceremony beats |

### Epic arcs (50+ sub-beats; defer to post-Pass-3+)

| Arc | Scope |
|---|---|
| War of the Five Kings | All five books, ~100+ event hubs needed |
| Daenerys's arc | All five books |
| The Long Night (Others vs Watch) | Prologue, AGOT, ACOK, ASOS, ADWD — emergent |

## Open design questions (NOT for this memo to answer)

1. **Mass mint vs dip-driven?** Strong lean: dip-driven. Validate the pattern with 2-3 small arcs after the Trident incident, then scale based on what queries agents actually issue.
2. **Type for parent arcs:** `event.incident` works for the Trident-style mid-scale arc; uncertain for Sack-of-KL (event.battle would over-claim — the sack isn't a single battle). Defer until 5+ arcs are minted and pattern emerges.
3. **Causal-edge density:** TRIGGERS between every adjacent sub-beat, or only at story-load-bearing junctures? Lean: only load-bearing, to avoid TRIGGERS-sprawl polluting graph queries.
4. **Cross-arc edges:** does Sack-of-KL TRIGGER the Mountain's later Harrenhal command? Probably yes, but this is the gateway to cross-arc reification and needs its own design pass.
5. **Wiki-arc anchors:** does AWOIAF ever name an arc as a single concept (e.g., wiki page for "Rains of Castamere thread")? If so, use wiki page as the canonical anchor. Mostly no — arcs are reader-recognized patterns, not AWOIAF entities. So mint slugs are curator-named, like S91 rename convention.
6. **Theories vs arcs:** the `theories/` layer (45 mostly-dark nodes) shares structural shape with arcs (named pattern that spans canon). Are theories a special case of arc? Probably yes — but theories are about *interpretation* (R+L=J reveals), arcs are about *causation* (Trident incident causes Lady's death). Different uses, similar shape. Keep them as separate node-types for now; revisit after both layers have 5+ instances each.

## How this fits the current queue

**Current next-up sessions (S94 + handoff):**
1. **Mode 3 dip** (Opus 4.7) — gate cleared S94; runs on the merged graph
2. **Graph cleanup with S95 resolutions** (Sonnet 4.6) — parallel-safe; ships the Trident-incident reification as Q5 + the other 18 S95 edges + FIX-22 + plate5 followups

**This memo does NOT change either session's scope.** What it adds:

- **Mode 3 dip script enhancement:** add 2-3 arc-shaped questions to the 5-10 dip questions. Examples: "What set the Trident incident in motion?" (now answerable post-cleanup); "What are the consequences of the Battle of the Trident?" (currently unanswerable — that's the gap the arc track fixes); "What's the causal chain from Robert's Rebellion to Joffrey's coronation?" (unanswerable). The dip's failures on arc questions become the priority signal for arc-minting.
- **Cleanup session:** unchanged. Trident incident ships as Q5 either way; that's the prototype for the pattern.
- **New session AFTER both:** "arc-track wave 1" — 3-5 small arcs minted based on dip findings + this candidate list. ~3-4 hours per arc, research-and-mint. Mode: similar to S95 (parallel research subagents + curator review + JSON-ready emit file). Sonnet 4.6 for research; Opus 4.7 to synthesize and review.

**No new continue prompt needed yet.** The arc-track wave-1 session gets a continue prompt when the dip's findings sharpen the candidate list. For now: this memo + the memory entry + the worklog Ideas & Backlog HIGH entry are the durable capture.

## File count audit (per Matt's "no more new files" concern)

This memo + the memory entry + the worklog edit = **1 net new file in the project tree** (this memo). The memory entry lives in `~/.claude/projects/.../memory/` outside the repo; the worklog edit is in-place. No new continue prompts, no new curation files, no new spec docs. The Trident-incident reification rides inside the existing `s95-quarantine-resolutions-2026-06-13.md`.

## Bottom line

The pattern is a small structural addition (no new vocab, no new infrastructure) with outsized agent-traversal payoff. First instance ships with S95 cleanup. Track depth and priority are set by what Mode 3 reveals. Defer the deliberate sweep until then.
