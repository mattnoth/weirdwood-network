# Container-split — orchestrator proposal (S121)

> **Status & caveat.** This is the orchestrator's synthesis of Step 2 (the container-split). The intended
> **4-lens independent fan-out was blocked by a persistent Anthropic API 529 overload** (two dispatch
> rounds, all lenses failed; my own main-loop calls worked, so Step 1 + this doc proceeded). This proposal
> is therefore a **first draft for Matt to react to + the basis for the fan-out to pressure-test when the
> API recovers** — NOT a settled decision. Nothing here is applied to the graph except the already-stamped
> Essos/WO5K tags from Step 1. "Agents propose, Matt decides."
>
> Grounded against: `reference/foreshadowing-events.md` (the 30 anchored events), the live graph
> (`graph-query.py`/`event_alias_resolver.py` node-existence probes), the S120 board, and the two existing
> decomposition docs. Vocabulary: Pass/Track/step/Tier per `reference/glossary.md`.

## Lens A — the container SET + the 30-event mapping

**Recommended set (6 containers):** `essos`, `wo5k`, `north`, `aegon`, plus **two the board didn't name
but the event list forces**: `riverlands` (the Brotherhood / Stoneheart / Arya-Riverlands thread) and a
**KL-Faith** thread. Plus possible `jon`/`bran` (Lens B). The board's NORTH+AEGON are necessary but not
sufficient — ~6 of the 30 events fit none of the four.

### The 30 events → container (backbone — the factual part)

| # | Event | Container(s) | Built? |
|---|-------|--------------|--------|
| 1 | Jon Arryn's murder | **standalone** (Littlefinger backstory; inciting) — or `wo5k` upstream | n/a |
| 2 | Bran's fall | `bran` / standalone (built arc) | ✅ built |
| 3 | Ned's execution | **wo5k** (the root cascade) | ✅ built |
| 4 | Robert's death | **wo5k** (root) | ✅ built |
| 5 | Drogo's death / dragon birth | **essos** | ✅ built (E1) |
| 6 | Catelyn seizes Tyrion | **wo5k** (war trigger) | partial |
| 7 | Battle of the Blackwater | **wo5k** | ✅ built (downstream) |
| 8 | Theon takes Winterfell | **wo5k ∩ north** (seam) | nodes exist, dark |
| 9 | House of the Undying visions | **essos ∩ aegon** (the cloth-dragon = fAegon) — cross-cut | — |
| 10 | Renly's death | **wo5k** | dark |
| 11 | Red Wedding | **wo5k** (built standalone) | ✅ built |
| 12 | Purple Wedding | **wo5k** | ✅ built |
| 13 | Oberyn vs the Mountain | **wo5k** (Tyrion's trial) | ✅ built (Tywin arc) |
| 14 | Tyrion kills Tywin | **wo5k** | ✅ built |
| 15 | Stoneheart reveal | **riverlands** (NEW) | ✅ built (AFFC #3) |
| 16 | Jon becomes Lord Commander | **north** (or `jon`) | dark/unbuilt |
| 17 | Cersei's arrest by the Faith | **kl-faith** (NEW) | ✅ built (AFFC #1) |
| 18 | Pate / Jaqen at the Citadel | **standalone** (Faceless Men; Arya-adjacent) | — |
| 19 | Brienne's "death" | **riverlands** (NEW) | ✅ built (AFFC #3) |
| 20 | Euron's Kingsmoot | **iron-islands** (or fold into a Greyjoy thread) | ✅ built (AFFC #2) |
| 21 | Jon's assassination | **north** (or `jon`) | dark/unbuilt |
| 22 | Dany rides Drogon / escapes | **essos** | ✅ built (E3) |
| 23 | Aegon's landing | **aegon** | node exists, dark |
| 24 | Stannis marches on Winterfell | **wo5k ∩ north** (seam) | dark/unbuilt |
| 25 | Varys assassinates Kevan | **aegon** | unbuilt |
| 26 | Quentyn's death | **essos** | ✅ built (E5) |
| 27 | Manderly's Frey pies | **north** | dark/unbuilt |
| 28 | R+L=J | **standalone** cross-book (or `jon`) | — |
| 29 | The Others' nature | **north** (deep-lore tail) | — |
| 30 | Doom of Valyria | **standalone** deep-lore | — |

**Takeaways:**
- NORTH+AEGON are confirmed and necessary. But **`riverlands` (15,19 + Arya) and `kl-faith` (17) are also
  real container-sized threads** the board missed — and three of their arcs are ALREADY BUILT (AFFC #1/#3),
  currently floating untagged. Recommend naming them now.
- `iron-islands` (20) is built (AFFC #2 Kingsmoot→Euron). Small but coherent; tag it or fold under a future
  Greyjoy thread.
- ~5 events are genuine **standalones** (1 Jon-Arryn, 18 Jaqen-Citadel, 28 R+L=J, 30 Doom) — they should
  stay `containers: null`, not be forced into a container.

### NORTH scope (greenfield — most beats unbuilt)
- **Theater:** the Watch + wildling + political North. NOT "the White Walkers" (sparse).
- **Root:** AGOT-1 prologue deserter → Ned beheads him → (the Watch thread launches). Practically, NORTH's
  causal root is shared with WO5K at `execution-of-eddard-stark` (Jon is already at the Wall by then).
- **Spine/junctures (all need minting):** Jon-to-the-Wall → Benjen vanishes → Jon's Watch rise → Jon
  elected LC (#16) → the wildling/Mance arc → Stannis arrives at the Wall → the Pink Letter → Jon's
  assassination (#21). Parallel northern-political: Bolton-held Winterfell → Stannis marches (#24) →
  Grand Northern Conspiracy / Manderly's Frey pies (#27).
- **Readiness:** near-zero — `jon-snow-elected-lord-commander`, `assassination-of-jon-snow`,
  `stannis-marches-on-winterfell`, `wymans-frey-pies` do NOT exist. NORTH is a full decomposition dip's
  worth of greenfield work (like Essos was).

### AEGON / Targaryen-restoration scope (partially built)
- **Root:** the Varys/Illyrio tunnel conspiracy (AGOT, Arya witnesses — `dyad-queue.md` D1).
- **Spine:** Varys/Illyrio conspiracy → JonCon + fAegon raised in Essos → Golden Company hired →
  `aegons-landing` / `landing-of-the-golden-company` (BOTH EXIST) → Storm's End → Varys kills Kevan (#25,
  unbuilt). HotU "cloth dragon" vision (#9) seeds it.
- **Confirmed:** Essos E7 (Varys/Illyrio) belongs HERE, not Essos (already extracted to `dyad-queue.md`).

## Lens B — Jon / Bran granularity (recommendation: hybrid dual-tag)
- **Jon** is container-sized (Watch politics → LC election → Pink Letter → assassination ≈ 6-8 junctures),
  and it lives almost entirely INSIDE the NORTH theater. Recommend **`jon` as a sub-tag, dual-stamped with
  `north`**: Jon's Watch beats carry `containers: [north, jon]`; pure-NORTH-political beats (Manderly,
  Stannis-marches) carry `[north]` only. This makes `--container jon` and `--container north` both useful
  without a separate maintenance burden.
- **Bran** is a DIFFERENT theater (greensight / Beyond-the-Wall / three-eyed-crow) that barely touches
  Jon's Watch politics. Bran's-fall is already built. Recommend **`bran` as its own tag** (not nested under
  north — the overlap is thin); the Beyond-the-Wall arc is mostly future/TWOW.
- Reject: a flat "everything-north-is-just-`north`" scheme (loses the useful Jon/Bran retrieval) AND a
  proliferation of micro-containers. Never `[]`.

## Lens C — seams + the build-once rule
**Seams found:**
| Seam | Node(s) | Status |
|------|---------|--------|
| wo5k ∩ essos | `robert-orders-daenerys-assassination` | ✅ tagged `[essos, wo5k]` (S121) |
| wo5k ∩ north | `capture-of-winterfell`, `sack-of-winterfell`, the Theon/Reek arc | nodes exist, dark |
| wo5k ∩ north | `stannis-marches-on-winterfell` (Stannis: Blackwater→the Wall→Winterfell) | unbuilt |
| essos ∩ aegon | HotU vision (#9); Dany's Westeros-bound intent | — |
| north ∩ aegon? | (thin) | — |

- **Build-once ownership rule (recommended):** *the container where the node's causal SPINE roots owns the
  build; the other container only adds its tag.* E.g. `robert-orders…` roots in WO5K (Robert's council) but
  is the Essos prime mover → WO5K-adjacent build, Essos tag added (done). `capture/sack-of-winterfell` root
  in the WO5K ironborn-invasion front → **WO5K owns the build, NORTH adds its tag.**
- **Theon/Reek verdict:** Theon's arc roots in WO5K (Greyjoy rebellion → ironborn invasion is a WO5K front)
  and terminates in NORTH (Reek/Ramsay/Winterfell). Recommend **build under WO5K, dual-tag `[wo5k, north]`**;
  the ADWD Reek-recovery tail is NORTH-owned. Don't build it twice.
- **Bridge vs seam:** a *bridge* has causal edges that CROSS the container boundary (`robert-orders…` →
  Essos spine); a pure *seam* is a node both containers claim but causation doesn't cross. Both get the
  multi-value `containers:` tag; only bridges show cross-container edges in `--full-chain`.
- **Builder checklist at a boundary node:** (1) does a node already exist? (`event_alias_resolver --lookup`);
  (2) which container owns the build (spine-root rule)?; (3) stamp ALL containers it belongs to; (4) verify
  `--causal-chain` roots in the owning container, not the tag-only one.

## Lens D — retro-grouping the ~12 built standalones (recommendation: **(b) tag the clean subset now**)
A half-tagged graph makes `--container` *misleading* (looks complete, isn't) — so tag the clean-mapping
arcs now and leave genuine standalones `null`. Recommended tag-now set:

| Built arc (root) | `containers:` |
|------------------|---------------|
| Ned's-downfall (B3) — `execution-of-eddard-stark` & beats | `[wo5k]` |
| Robert's death | `[wo5k]` |
| Purple Wedding — `death-of-joffrey-baratheon` | `[wo5k]` |
| Tywin's death — `assassination-of-tywin-lannister` | `[wo5k]` |
| Blackwater downstream — `battle-of-the-blackwater` | `[wo5k]` |
| Red Wedding (B1 + hub) | `[wo5k]` |
| Greyjoy→Theon-ward (B2) | `[wo5k]` (Theon beats → `[wo5k, north]`) |
| Robb-King — `robb-proclaimed-king-in-the-north` | `[wo5k]` |
| Cersei's downfall (AFFC #1) | `[kl-faith]` |
| Brienne→Stoneheart (AFFC #3) | `[riverlands]` |
| Kingsmoot→Euron (AFFC #2) | `[iron-islands]` |
| Dorne/Queenmaker (AFFC #4) | `[dorne]` (or fold to a Dorne tag; Quentyn already `[essos]`) |
| **Leave `null`:** Robert's Rebellion, Bran's fall (or `[bran]`), R+L=J, Doom of Valyria | `null` |

This is ~30-40 node edits via `scripts/stamp_containers.py` (cheap, idempotent). **Defer until Matt picks
the container SET** (esp. whether `riverlands`/`kl-faith`/`dorne`/`iron-islands` are real containers or
should fold) — tagging before the set is settled would bake in names that might change.

## Open questions for Matt (the genuinely-undecided)
1. **Container SET:** adopt 6 (`essos, wo5k, north, aegon` + `riverlands` + `kl-faith`)? And are
   `iron-islands` / `dorne` their own tags or folded? (The AFFC arcs are built + floating — they need
   homes.)
2. **Jon/Bran:** hybrid dual-tag (recommended) vs north-only vs own-containers?
3. **Build priority after this:** NORTH (greenfield, the biggest gap) vs WO5K-remainder (the original
   Step-3 default) vs AEGON (partially built)? The seam analysis says **WO5K-remainder is safe to build
   now** — its remaining junctures (Blackwater-upstream, Karstark, Balon→Winterfell) are WO5K-owned; only
   Balon→Winterfell touches the NORTH seam (build under WO5K, dual-tag).
4. **Retro-tag now or defer?** Recommend defer the apply until #1 is settled, then one `stamp_containers.py`
   batch.

## NEXT (when the API recovers)
Run the 4-lens fan-out (`working/session-results/2026-06-21-container-split-BRIEFING.md`) to pressure-test
this proposal, fold Matt's decisions in, then build (Step 3).
