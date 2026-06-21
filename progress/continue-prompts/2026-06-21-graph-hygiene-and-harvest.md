# Continue — Graph hygiene (ATTENDS cleanup) + harvest consume-pass, THEN Essos

> **Recommended model:** Opus 4.8 orchestrator (the ATTENDS retargeting + GARRISONS/HELD_AT vs
> mint-a-node calls carry real judgment) + subagents per item (Sonnet 4.6 for judgment reads;
> Haiku 4.5 fine for pure line-opening). **This is a MAINTENANCE session** — one coherent purpose
> (close loose ends + clear the harvest queue) before the next big build. Do NOT bolt the Essos
> build onto this session; Essos gets its own prompt when this lands (see "What's next").

> **State trust (CLAUDE.md rule #9):** `worklog.md` is authoritative. As of S117: nodes 8,562 ·
> edges 22,342 · vocab 169 (`WITNESS_IN` added S117) · harvest queue 26 open. The AFFC causal-arc
> spine phase is COMPLETE (all 4 fumbles built S114–S117).

## Vocabulary to paste into subagents
Pass (numbered corpus sweep) · Track (named workstream) · step (lowercase ordered piece) · Tier
(confidence 1–5 ONLY). Source: `reference/glossary.md`.

---

## step 1 — ATTENDS relation cleanup (surfaced by the S117 ATTENDS re-audit)

The S117 re-audit of 42 `ATTENDS` edges (worklog S117 Active Decision) flagged a small cleanup set.
These are NOT WITNESS_IN reclassifications — they're mistargets / wrong-relation edges. Fix each,
verifying against the LOCAL cache (never re-fetch). Back up `edges.jsonl` to `_regrounding/` first.

1. **2 mistargeted ATTENDS edges** (target is not an event):
   - `cersei-lannister ATTENDS robert-baratheon` — target is a **character** node (Robert's deathbed
     scene). Decide: retarget to a death/deathbed event node if one exists, else drop the ATTENDS
     (it's mis-typed). Check `graph/nodes/events/` for a Robert-death node first.
   - `ghost-of-high-heart ATTENDS summerhall` — target is a **place**. She canonically survived the
     **Tragedy of Summerhall** ("I gorged on grief at Summerhall", `asos-arya-08:77`). Best fix:
     **mint a `tragedy-of-summerhall` event node** (dedup-check first — `tragedy-at-summerhall` may
     already exist from the historical-anchor wave; see todos line ~89), then retarget this edge as
     `ghost-of-high-heart WITNESS_IN tragedy-of-summerhall`.
2. **5 siege-of-riverrun ATTENDS edges → GARRISONS / HELD_AT** (not attendance): `emmon-frey`,
   `edwyn-frey`, `desmond-grell`, `robin-ryger`, `jeyne-westerling`. These are garrison officers /
   a Frey envoy / a captive — presence/role, not audience. Decide the right relation per edge
   (GARRISONS for the garrison officers; HELD_AT for Jeyne the captive; the Frey envoys may be
   PARTICIPATES_IN or a negotiation relation). **`GARRISONS`/`HELD_AT` may not be in the locked
   vocab** — verify via `scripts/build-edge-type-counts.py`; if absent, either reuse an existing
   type (`GUARDS`, `IMPRISONED_AT`) or file a vocab decision. Don't invent silently.

Mint via a `scripts/mint_attends_cleanup.py` (backup + re-run guard, the S116/S117 pattern). Run
`scripts/verify-edge-quotes.py` on any edge that keeps/gets a verbatim quote. Rebuild indexes +
alias resolver if any node is added (`tragedy-of-summerhall`).

## step 2 — harvest consume-pass (26 open rows in `working/harvest-queue.md`)

The queue is over the ~20–30 trigger and this is the standing "after a text-heavy session" pass.
**Open each `status: open` row's `chapter:line`, verify the quote against the file, attach to the
graph, flip the row to `done`.** Attachment targets by kind: `quote`→node `## Quotes` (book-cite
overlay onto wiki-sourced prose is high-value, memory `feedback_book_citation_overlay_value`);
`food`→`object.food` node; `appearance`/`place`/`object`→description fields; `witness`→`WITNESS_IN`
edge (apply the S117 text-anchor gate — only if the text shows they SAW it); `relationship`→typed
edge; `foreshadowing`→note for the deferred Pass-4 layer.

Notable rows: the 19 Dorne-research rows (several are **Quentyn/Essos-bridge seeds** — the onyx-dragon
"Fire and blood" reveal, Arianne's secret betrothal to Viserys, the Golden Company contract break;
these may be `parked` as Essos-gated rather than consumed now); the Sarella=Alleras cross-identity
hook; 3 happenstance AGOT rows (tarts, Redwyne twins, gold-cloak uniform); 4 ATTENDS-reaudit rows
(Hoster's witness quote — already used; the Summerhall/Ghost foreshadowing — feeds step 1; garrison
loyalty; Genna Frey). **Park, don't force-consume**, any row whose home is a not-yet-built node
(Essos arc) — use `parked (blocked: ...)` per the S116 status convention; parked rows are EXCLUDED
from the trigger count.

Fresh-subagent verify a sample of attachments (the S110 harvest pass verified 23/24). Paste the
harvest snippet into any subagent that reads chapters (they'll refill the queue — that's expected).

## What's next (AFTER this maintenance session) — write the Essos prompt then

The next BIG build is the **ESSOS container** (major-arc backlog #2, `working/major-arc-backlog.md`).
It needs its **own decomposition dip** (the `working/wo5k-decomposition.md` template): enumerate +
rank Essos's load-bearing junctures (Drogo's death/dragon-birth → Slaver's-Bay campaign → escape
from Meereen) + the **first-class Westeros↔Essos bridges** (Robert's assassination order → Dany;
Illyrio↔Varys conspiracy; Jorah-spies-for-Varys). It auto-joins the pre-placed S116 bridge node
`euron-commissions-victarion-to-fetch-daenerys` + the Quentyn/Dorne "Fire and blood" pact.

**The arc-mint machine** (research → dedup → quotes → mint script → index/alias rebuild → fresh-verify
→ smoke-test → root-check 5b → harvest) is documented in the **archived**
`progress/continue-prompts/archive/2026-06-18-causal-arc-execution.md` — restore/reference it for the
Essos build. Apply the S117 rules: **root at the LOCAL antecedent, not the deepest hairnet ancestor**;
declare standalone threads explicitly. (**Sonnet 4.6** for the Essos build orchestration.)

## DO NOT
Re-fetch the wiki (local cache only) · use kebab aliases (SPACED phrases only) · invent edge types
(verify vocab, file a decision) · assert unproven agency as fact (`SUSPECTED_OF`, Tier-2) · run
`/endsession` without explicit permission · bolt the Essos build onto this maintenance session.
