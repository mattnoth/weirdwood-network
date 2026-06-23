# Robert's Rebellion enrichment — DEDUP BASELINE (S133)

> Shared ground-truth for the 3 enrichment-proposal lenses. Authored from live `graph-query.py`
> output S133. **Read this BEFORE proposing — do not re-propose anything in the "ALREADY EXISTS"
> list.** Run your own `graph-query.py --neighbors <slug>` on any node you target to re-confirm.

## The RR cluster (existing nodes)
**Hub:** `roberts-rebellion` (event.battle — note: mistyped, should be event.war; a known small-fix, NOT your job).
**Child battles (all PART_OF roberts-rebellion):** `assault-on-dragonstone`, `battle-of-ashford`,
`battle-of-the-bells`, `battle-of-the-trident`, `battles-at-summerhall`, `combat-at-the-tower-of-joy`,
`sack-of-kings-landing`, `siege-of-storms-end`, `taking-of-gulltown`, `wildfire-plot`.
**Upstream causal beats:** `tourney-at-harrenhal`, `abduction-of-lyanna`, `execution-of-brandon-and-rickard-stark`,
`aerys-demands-ned-and-robert`.
**Related existing nodes:** `knight-of-the-laughing-tree` (CHARACTER node, the mystery-knight identity — NOT an event),
`coronation-of-robert-i-baratheon`, `ruby-ford`, `tower-of-joy` (location), `harrenhal` (location).

## ALREADY EXISTS — DO NOT RE-PROPOSE
**Participant layers (minted S97 historical-anchor backfill — RICH, do not re-add):**
- `battle-of-the-trident`: AGENT_IN robert; COMMANDS_IN robert/rhaegar/lewyn-martell; FIGHTS_IN ×8 (barristan-selmy, …); LOCATED_AT ruby-ford; CAUSES→sack-of-kings-landing; PART_OF→RR.
- `combat-at-the-tower-of-joy`: FIGHTS_IN ×10 (eddard-stark, howland-reed, martyn-cassel, theo-wull, ethan-glover, mark-ryswell, willam-dustin, arthur-dayne, …); LOCATED_AT tower-of-joy; PART_OF→RR.
- `tourney-at-harrenhal`: ATTENDS ×16 (aerys, eddard, lyanna, elia, jon-arryn, …); CAUSES→abduction-of-lyanna; LOCATED_AT harrenhal; PRECEDES ashford/summerhall/gulltown.
- `sack-of-kings-landing`: AGENT_IN jaime-lannister/gregor-clegane/amory-lorch; COMMANDS_IN tywin-lannister; CAUSES→coronation-of-robert-i-baratheon; CAUSES←battle-of-the-trident + pycelle-opens-the-gates; LOCATED_AT kings-landing.

**Existing upstream causal spine (do not re-mint these edges):**
`tourney-at-harrenhal CAUSES abduction-of-lyanna CAUSES execution-of-brandon-and-rickard-stark`;
`aerys-demands-ned-and-robert TRIGGERS roberts-rebellion`;
`battle-of-the-trident CAUSES sack-of-kings-landing`; `sack-of-kings-landing CAUSES coronation-of-robert-i-baratheon`.

**Existing dyads:** `rhaegar-targaryen LOVES lyanna-stark`; `rhaegar-targaryen CROWNS_QUEEN_OF_LOVE_AND_BEAUTY lyanna-stark`
(OFF-VOCAB type — flag for recast, see below); `rhaegar-targaryen DEFEATS brandon-stark` (suspicious — verify);
`lyanna-stark BETROTHED_TO/MOURNED_BY robert-baratheon`.

## GENUINELY MISSING — the enrichment yield (propose here)
1. **Downstream is barren.** `roberts-rebellion` has only 1 OUTGOING edge and it is **JUNK** — a misparsed
   `roberts-rebellion GUEST_OF winterfell` with quote "Take the books away…healthy appetites". Flag it for DROP.
   The cluster does not connect FORWARD to the present-day arcs.
2. **No `SUSPECTED_OF` substrate anywhere** despite RR anchoring the series' two deepest mysteries
   (R+L=J; Jon Arryn's murder). Zero attribution/revelation edges.
3. **Near-bare sibling battles:** `wildfire-plot` (PART_OF + PRECEDES only — NO agents, despite Aerys/Rossart),
   `battle-of-the-bells` (PART_OF + PRECEDES only — the Connington-defeat-and-exile beat), `abduction-of-lyanna`
   (2 edges total), `battles-at-summerhall`, `taking-of-gulltown`, `assault-on-dragonstone` (thin).
4. **Missing secondary-event NODES:** `murder-of-elia-martell`, `murders-of-rhaenys-and-aegon` (the Sack atrocities —
   gregor/amory are AGENT_IN the *Sack* but the specific killings have no beat-node), Jon Arryn's murder, the
   Knight-of-the-Laughing-Tree *incident* (the character exists; the tourney sub-arc does not).
5. **Off-vocab edge** `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` — recast into locked vocab or leave + flag (your proposal
   should recommend, not unilaterally churn).
6. **Book-cite overlay opportunity:** many cluster edges cite `wiki:...` refs; the prose exists in book chapters
   (ToJ fever dream agot-eddard-10/-15; Trident asos-jaime/-tyrion; Harrenhal asos-bran-02). Upgrading wiki cite_refs
   to navigable `chapter:line` book cites is high-value (memory `feedback_book_citation_overlay_value`).

## HARD RULES for proposals
- **PROPOSE, don't mint.** Write your proposal to your assigned file; mint nothing into graph/.
- **Dedup every item** against the ALREADY-EXISTS list + your own `--neighbors` check. Mark each proposed item
  `NEW` / `RECAST` / `OVERLAY`.
- **Locked edge vocab ONLY:** CAUSES / TRIGGERS / ENABLES / MOTIVATES / CONSPIRES_WITH / SUSPECTED_OF
  + roles AGENT_IN / VICTIM_IN / COMMANDS_IN / WITNESS_IN / OFFICIATES + structural SUB_BEAT_OF / PART_OF / LOCATED_AT.
  No new capitalized types. If something needs a type outside this set, write `NEEDS_VOCAB: <desc>` and STOP — don't invent.
- **Guard against granularity overclaim:** NO `CAUSES` between mere sibling/sequence beats (use SUB_BEAT_OF / PART_OF /
  PRECEDES). A causal edge needs real causation, not just "happened next."
- **`SUSPECTED_OF` is Tier-2, never Tier-1, and never asserts the act.** Use it for contested/unproven agency.
- **THEORY GATING (critical):** R+L=J, the Jon-Arryn-murder culprit, KotLT identity are GATED READINGS. You build the
  Tier-1/2 EVIDENCE SUBSTRATE (who was present, who is in-world suspected, what the text shows) — you do NOT assert the
  theory. No TWOW-unwritten content, no author-statement-as-canon. Cite the in-text basis for every SUSPECTED_OF.
- **Every proposed edge/node needs:** type, source→target, evidence `chapter:line` (book preferred; wiki fallback ok),
  a VERBATIM contiguous quote (never splice across a `," said X, "` attribution), tier, one-line rationale, dedup tag.
