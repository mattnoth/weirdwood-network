# Arc Enrichment Track (second-pass deepening of built arcs)

> **Created 2026-06-20 (S116), Matt-greenlit + smoke-tested.** The companion to the
> spine-build machine: once a major arc's **causal spine** is built, a later
> **enrichment pass** returns to it and adds the braided side-plots that occur *within*
> the arc but weren't on the spine — secondary-character sub-arcs, contemporaneous
> "revelation" events, descriptive/quote depth, and unproven-but-load-bearing edges.

## The cadence (Matt's call, S116)

**Spine-first, then circle back.** Build the *majority of the major narrative-arc spines*
first (the foreshadowed-events backlog + WO5K container), THEN run enrichment passes over
them. Rationale (proven by S116's own deferrals):

1. **Enrichment wires *between* arcs.** The more spines exist, the more an enrichment pass
   has to attach to. Enriching too early forces **forward-dangling stubs** into a void
   (e.g. Aeron→*Forsaken*, Victarion→Essos, Asha's ADWD forced-marriage all dangle until
   their downstream arcs exist).
2. **The harvest queue makes deferral safe.** Every enrichment candidate is preserved as a
   `working/harvest-queue.md` pointer, so deferring the *build* never loses the *find*.
3. **Multi-pass per cluster is expected, not one-and-done.** A cluster can be enriched
   repeatedly; each pass (fresh subagents + accumulated harvest finds + newly-built
   neighbor arcs) yields new connections. S116 was the *first* Kingsmoot enrichment pass.

**Today's S116 Kingsmoot enrichment was a deliberate smoke-test exception** (run while we
were already deep in the cluster). The standing default is spine-first.

### The enrichment-phase TRIGGER (concrete — added S117, "defer to when?")

"Spine-first" is not an open-ended "later." The enrichment PHASE begins — and the whole
backlog below (incl. Dorne, Cersei, Brienne→Stoneheart, and the AGOT/ASOS arcs) becomes
eligible — when the **major-arc spine queue is down to its long tail**. Concrete gate:

> **Enrichment opens once the ESSOS container is spine-built** (the next big build) **AND
> the WO5K junctures #3/#4/#5 are built.** At that point AFFC + Essos + WO5K-core spines
> all exist, the `major-arc-backlog.md` DARK count is just the deep-lore / theory long
> tail, and circling back to enrich is the highest-value next move.

Until that gate, enrichment candidates are PRESERVED as harvest pointers (never lost) and
NOT built — except the same in-cluster smoke-test exception that produced S116 (if a
session is already deep in a cluster's text and the enrichment is cheap, take it). A
single cluster can also jump the queue if Matt names it. This gate is a *condition*, not a
date — it trips when the spine work is done, however many sessions that takes.

## The enrichment-pass machine (smoke-tested S116)

1. **Fan out 2–3 fresh subagents, each a different lens** on the built cluster:
   - secondary-character sub-arcs (the braided side-POVs),
   - thread/revelation + contemporaneous events + any unproven-but-load-bearing claims,
   - descriptive/quote/object depth (the "what does X look like" layer).
   Paste vocab + the harvest snippet; tell them PROPOSE-don't-mint + dedup-check every node.
2. **Synthesize + decide** what's worth minting vs deferring (forward-dangling cross-book
   nodes defer to their downstream container's enrichment pass).
3. **Verify every cited line against the files** (subagents reconstruct quotes — always check),
   mint nodes/edges via a `scripts/mint_<arc>_enrichment.py` (backup + re-run guard),
   **fresh-verify the interpretive edges**, stamp.
4. **Consume the harvest pointers** the dip refilled.

## Enrichment yield is real (S116 evidence)

One already-harvested cluster → **+2 beat-nodes, +6 edges, +12 descriptive attachments,
+1 new edge type (`SUSPECTED_OF`), ~14 fresh harvest pointers**, almost no overlap with the
first harvest pass. The hypothesis ("a cluster can be enriched several times and keep
yielding") held.

---

## Backlog

### Kingsmoot → Euron (spine S116, enrich-pass-1 S116)
**Lesson (Matt, S116): don't defer a node just because its *payoff* is in a later book.** A node is only "forward-dangling" if its UPSTREAM is missing; if its upstream exists, mint it now (downstream-dark is normal for a terminal node) and the cross-book auto-join (S112) lets the later arc find it pre-placed. The two "deferred" nodes both had clean AFFC/ADWD upstreams in the local cache, so they were **MINTED in place S116, not deferred:**
- ✅ `euron-weds-asha-to-erik-ironmaker-in-absentia` — Asha's forced proxy-marriage (ADWD "The Wayward Bride":121,123, in local cache). `kingsmoot CAUSES` it. Closes her AFFC sub-arc.
- ✅ `euron-commissions-victarion-to-fetch-daenerys` — the Essos-bridge seed (AFFC Reaver:281,286). `taking-of-the-shields CAUSES` it. Downstream (Victarion's ADWD Slaver's Bay voyage) left dark — the Essos arc connects its spine to this pre-placed node.

- ✅ `euron-hunts-aeron-damphair` — MINTED S116 (ADWD Wayward Bride:175,183). `aeron-vows… CAUSES` it. Captures the real hunt + Tris Botley's "the Crow's Eye slit his throat" RUMOR as a node quote (NOT a `SUSPECTED_OF death` edge — Aeron's death is unconfirmed in the 5 books; TWOW shows him alive).

Still genuinely deferred (no local upstream/source yet):
- Aeron's eventual CAPTURE by Euron (the *Forsaken* TWOW beat) — downstream of `euron-hunts-aeron-damphair`; TWOW not in corpus. Forward gap, left dark.
- Granular dish nodes from the two ironborn feasts — same open question as S110 (mint granular dishes?). Matt's call.

**Meta-lesson reinforced (Matt, S116): "log it for later" is the same fragile deferral as parking a node — if you have the verbatim quote + a valid home NOW, mint/attach it now.** The only true deferrals are missing-upstream (forward-dangling) or missing-source (not in corpus).

### Other built arcs awaiting a first enrichment pass (when spine-phase is mostly done)
- **WO5K container** — needs MORE than one enrichment pass (Matt: "gonna need more than that treatment"). Many braided sub-plots (Karstark, Frey, Bolton, the Riverlands chevauchée, Robb's westerlands campaign).
- Red Wedding / Purple Wedding / Tywin's death / Blackwater / Ned's downfall / Bran / Robert's Rebellion / Sack of KL — each has side-plots not on its spine.
- Cersei's downfall + Brienne→Stoneheart (AFFC arcs S114/S115) — secondary beats (the Blue Bard, the Faith Militant's rise, the Brotherhood's hangings).
- **Dorne / Myrcella (Queenmaker, spine S117)** — rich secondary layer left on the harvest queue: the unresolved **"Someone always tells" informer mystery**; **Arys Oakheart's seduction sub-arc** (The Soiled Knight POV); the **conspirator dispersal** (Drey→Norvos, Garin→Tyrosh, Sylva→Greenstone marriage); **Darkstar's escape** into the deep sand (downstream-dark — his TWOW payoff); and the **Quentyn/Doran "Fire and blood" reveal** (which is really an Essos-bridge seed → belongs to the Essos container's enrichment, not Dorne's). 19 harvest rows pushed S117.

## Process rules
- Forward-dangling cross-book nodes **defer to the downstream container's enrichment**, not minted into a void.
- Interpretive/causal enrichment edges get the same **fresh-subagent verify** as spine edges.
- `SUSPECTED_OF` (S116) is the type for unproven-but-load-bearing agency (Tier-2, never asserts the act). Reuse for Jon Arryn's murder, Joffrey's parentage, the Purple Wedding poisoner, etc.
